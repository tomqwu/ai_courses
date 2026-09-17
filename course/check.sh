#!/usr/bin/env bash
# The full verification gate, without depending on `make`.
#
# Why this exists: on macOS /usr/bin/make and cc are shims that refuse to run until the Xcode
# licence is accepted (`sudo xcodebuild -license accept`). A gate that cannot run because of an
# unrelated toolchain licence is a gate people skip, so the steps live here and `make check` just
# calls this script. One definition, two front doors.
#
#   bash course/check.sh
#
# Every step must pass; the script stops at the first failure and reports which one.
set -u

cd "$(dirname "$0")" || exit 1
PYTHON="${PYTHON:-python3}"
failures=0

step() {
  local label="$1"; shift
  printf '\n── %s\n' "$label"
  if ! "$@"; then
    printf '   ✗ %s FAILED\n' "$label"
    failures=$((failures + 1))
  fi
}

step "unit tests — caption engine" "$PYTHON" 06-production/narration/test_captions.py
step "unit tests — TTS providers" "$PYTHON" 06-production/narration/test_providers.py
step "narration scripts"          "$PYTHON" 06-production/narration/validate_narration.py --scripts-only
step "narration media"            "$PYTHON" 06-production/narration/validate_narration.py
step "learner site build"         "$PYTHON" learner-site/build_site.py --check
step "browser check"              "$PYTHON" learner-site/check_player.py --all --print-skip
step "package verification"       "$PYTHON" 06-production/verify.py

# The pinned facts are re-derived from the case-study clones. Without the clones the step cannot
# run, so it says how to get them and does not fail — the same posture as the pointer check.
if [ -d ../ListenToMe ] && [ -d ../SignUpFlow ] && [ -d ../ai_qe ]; then
  step "facts re-derived (strict)"  "$PYTHON" 06-production/check_facts.py --strict
else
  printf '\n── facts re-derived (strict)\n   skipped: clone ListenToMe, SignUpFlow and ai_qe beside course/ to run it\n'
fi

printf '\n'
if [ "$failures" -ne 0 ]; then
  printf 'GATE FAILED: %d step(s) did not pass\n' "$failures"
  exit 1
fi
printf 'GATE PASSED: all steps green\n'
