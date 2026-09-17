#!/usr/bin/env bash
# The Ollama daemon does not survive a container restart; bring it back quietly.
command -v ollama >/dev/null 2>&1 && ! pgrep -x ollama >/dev/null && (ollama serve >/tmp/ollama.log 2>&1 &)
exit 0
