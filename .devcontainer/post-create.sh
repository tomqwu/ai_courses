#!/usr/bin/env bash
# One-time setup for the labs: Python test tooling, Poetry for SignUpFlow, Ollama with the lab model,
# and the three case-study repos cloned beside course/ so every pointer resolves.
set -euo pipefail
cd "$(dirname "$0")/.."

python -m pip install --upgrade pip >/dev/null
python -m pip install pytest pytest-cov httpx playwright >/dev/null
pipx install poetry >/dev/null 2>&1 || python -m pip install poetry >/dev/null

# Ollama: the local daemon the labs talk to. The install script is Ollama's own.
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi
(ollama serve >/tmp/ollama.log 2>&1 &) ; sleep 3
ollama pull qwen3:0.6b || echo "model pull failed — run 'ollama pull qwen3:0.6b' once the network allows"

# The case-study repos (upstream projects with their own history; git-ignored here).
for repo in ListenToMe SignUpFlow ai_qe; do
  [ -d "$repo" ] || git clone --depth 1 "https://github.com/tomqwu/$repo.git"
done

# Prove the environment the way Lab M0 does.
make -C course/03-content/m02-ondevice-app/tinycopilot lab-m2
echo
echo "Ready. Open course/03-content/m00-orientation/lab.md, or 'make -C course serve' for the site on port 8043."
