#!/usr/bin/env bash
# One-time setup for the labs: Python test tooling, Poetry for SignUpFlow, Ollama with the lab model,
# and the three case-study repos cloned beside course/ so every pointer resolves.
set -euo pipefail
cd "$(dirname "$0")/.."

# The gate's preview voice and audio measurement (the narration step of `make -C course check`), and
# zstd, which Ollama's installer now needs to unpack itself (without it post-create stops there).
sudo apt-get update -q >/dev/null && sudo apt-get install -y -q --no-install-recommends ffmpeg espeak-ng zstd >/dev/null

python -m pip install --upgrade pip >/dev/null
python -m pip install pytest pytest-cov httpx playwright >/dev/null
pipx install poetry >/dev/null 2>&1 || python -m pip install poetry >/dev/null

# Ollama: the local daemon the labs talk to. The install script is Ollama's own.
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi
(ollama serve >/tmp/ollama.log 2>&1 &) ; sleep 3
ollama pull qwen3:0.6b || echo "model pull failed — run 'ollama pull qwen3:0.6b' once the network allows"

# The case-study repos (upstream projects with their own history; git-ignored here), checked out
# at the commits the course's pointers were verified against: the same pins as CI's gate
# (.github/workflows/gate.yml), so a later upstream push cannot shift a line range under you.
clone() { [ -d "$1" ] || { git clone --quiet "https://github.com/tomqwu/$1.git" && git -C "$1" checkout --quiet "$2"; }; }
clone ListenToMe a9bde8e
clone SignUpFlow c550d46
clone ai_qe 6388f0a

# Prove the environment the way Lab M0 does.
make -C course/03-content/m02-ondevice-app/tinycopilot lab-m2
echo
echo "Ready. Open course/03-content/m00-orientation/lab.md, or 'make -C course serve' for the site on port 8043."
