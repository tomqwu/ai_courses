#!/usr/bin/env bash
# Build every module Marp deck to HTML (and PDF when a Chromium-based renderer is available).
#
#   ./build.sh            # HTML only, into slides/out/
#   ./build.sh --pdf      # HTML + PDF
#   ./build.sh --check    # validate decks (front matter, notes on every slide) and exit non-zero on failure
#
# Uses marp-cli via npx when no global `marp` is installed. Fails loudly with an
# actionable message when no renderer is available — the decks are still valid
# Markdown, so authoring never blocks on tooling.
#
# Portable across bash 3.2 (macOS default) — no mapfile, no associative arrays.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE="$(cd "$HERE/../.." && pwd)"
OUT="$HERE/out"
THEME="$HERE/aps.css"
MODE="${1:-html}"

DECKS_LIST="$(find "$COURSE/03-content" -name slides.md | sort)"
if [ -z "$DECKS_LIST" ]; then
  echo "No slides.md found under $COURSE/03-content — nothing to build." >&2
  exit 1
fi
DECK_COUNT=$(printf '%s\n' "$DECKS_LIST" | wc -l | tr -d ' ')

run_marp() {
  if command -v marp >/dev/null 2>&1; then
    marp "$@"
  elif command -v npx >/dev/null 2>&1; then
    npx --yes @marp-team/marp-cli@latest "$@"
  else
    return 127
  fi
}

echo "== validating $DECK_COUNT decks =="
FAILED=0
for deck in $DECKS_LIST; do
  echo "· ${deck#$COURSE/}"
  if ! head -8 "$deck" | grep -q '^marp: true'; then
    echo "  ✗ missing 'marp: true'"; FAILED=1
  fi
  if ! head -8 "$deck" | grep -q '^theme: aps'; then
    echo "  ✗ missing 'theme: aps'"; FAILED=1
  fi
  notes=$(grep -c '<!-- NOTES:' "$deck" || true)
  seps=$(grep -c '^---$' "$deck" || true)
  echo "  slides(separators)=$seps  speaker-notes=$notes"
  if [ "$notes" -lt 5 ]; then
    echo "  ✗ too few speaker notes (NOTES: required on every slide)"; FAILED=1
  fi
done
[ "$FAILED" -eq 0 ] || { echo "Deck validation FAILED." >&2; exit 2; }
echo "Deck validation passed."

echo
echo "== style lint (bullets, per-slide notes, proof slide) =="
# shellcheck disable=SC2086
python3 "$HERE/deck_lint.py" $DECKS_LIST || { echo "Deck lint FAILED." >&2; exit 2; }

[ "$MODE" = "--check" ] && exit 0

mkdir -p "$OUT"
for deck in $DECKS_LIST; do
  mod="$(basename "$(dirname "$deck")")"
  echo "== rendering $mod =="
  if ! run_marp --theme-set "$THEME" --html --allow-local-files \
        -o "$OUT/$mod.html" "$deck"; then
    echo "Cannot render decks: no marp-cli found." >&2
    echo "Install it with:  npm i -g @marp-team/marp-cli   (or keep using npx)" >&2
    echo "The decks are valid Markdown and render on any Marp-aware viewer." >&2
    exit 127
  fi
  if [ "$MODE" = "--pdf" ]; then
    run_marp --theme-set "$THEME" --pdf --allow-local-files \
      -o "$OUT/$mod.pdf" "$deck" || echo "  (PDF render unavailable — HTML written)"
  fi
done
echo "Decks written to $OUT"
