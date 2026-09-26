#!/usr/bin/env bash
# Lab M9 setup check for macOS (it also runs on Linux).
#
# Proves your tools are ready instead of assuming they are. Each check prints PASS or FAIL, and
# every FAIL prints the exact command that fixes it. Nothing here changes your machine: it only
# looks. Run it again after each fix until it says 4 of 4.
#
#   bash check-setup.sh
#
# Exit status is 0 when everything passes and 1 otherwise, so you can also run it in a script.

set -u

passed=0
total=4
os="$(uname -s)"

if [ -t 1 ]; then GREEN=$'\033[32m'; RED=$'\033[31m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else GREEN=""; RED=""; BOLD=""; RESET=""; fi

pass() { printf '%sPASS%s  %s\n' "$GREEN" "$RESET" "$1"; passed=$((passed + 1)); }
fail() { printf '%sFAIL%s  %s\n' "$RED" "$RESET" "$1"; printf '      fix: %s\n' "$2"; }

install_hint() {
  # $1 = the tool: git or gh
  if [ "$os" = "Darwin" ]; then
    if command -v brew >/dev/null 2>&1; then
      echo "brew install $1"
    else
      echo 'install Homebrew first: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  then run: brew install '"$1"
    fi
  else
    if [ "$1" = "gh" ]; then
      echo "see https://github.com/cli/cli/blob/trunk/docs/install_linux.md for your distribution"
    else
      echo "sudo apt install git   (or your distribution's package manager)"
    fi
  fi
}

printf '%sLab M9 setup check%s — %s\n\n' "$BOLD" "$RESET" "$os"

# 1. git
if command -v git >/dev/null 2>&1; then
  pass "git is installed: $(git --version)"
else
  fail "git is not installed" "$(install_hint git)"
fi

# 2. gh, the GitHub CLI
if command -v gh >/dev/null 2>&1; then
  pass "GitHub CLI is installed: $(gh --version | head -n 1)"
else
  fail "GitHub CLI (gh) is not installed" "$(install_hint gh)"
fi

# 3. your name and email on commits
name="$(git config --global user.name 2>/dev/null || true)"
email="$(git config --global user.email 2>/dev/null || true)"
if [ -n "$name" ] && [ -n "$email" ]; then
  pass "git knows who you are: $name <$email>"
else
  fail "git does not know your name and email yet" \
       'git config --global user.name "Your Name"   and   git config --global user.email "you@example.com"'
fi

# 4. signed in to GitHub
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  account="$(gh api user --jq .login 2>/dev/null || echo 'your account')"
  pass "signed in to GitHub as $account"
else
  fail "not signed in to GitHub from the terminal" "gh auth login   (choose GitHub.com, HTTPS, yes to git credentials, log in with a web browser)"
fi

printf '\n%s%d of %d checks passed.%s\n' "$BOLD" "$passed" "$total" "$RESET"
if [ "$passed" -eq "$total" ]; then
  echo "You are ready for Lab M9. Paste this output into your evidence log."
  exit 0
fi
echo "Fix the first FAIL above, open a new terminal window, and run this again."
exit 1
