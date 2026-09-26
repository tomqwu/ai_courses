# Handout — M9: Ship a Product Catalog with GitHub Pages

One page to keep beside the terminal. Windows commands are for PowerShell.

## Install and prove

| | Windows | macOS |
|---|---|---|
| Package manager | `winget --version` (else App Installer from the Store) | Homebrew's install line, then the setup lines it prints |
| Git | `winget install --id Git.Git -e --source winget` | `brew install git` |
| GitHub CLI | `winget install --id GitHub.cli --source winget` | `brew install gh` |
| After installing | **open a new terminal window** | — |
| Prove it | `powershell -ExecutionPolicy Bypass -File .\check-setup.ps1` | `bash check-setup.sh` |

Once per computer:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
gh auth login        # GitHub.com → HTTPS → Yes → Login with a web browser
```

## Find your way

| | Both systems |
|---|---|
| Where am I? | `pwd` |
| What is here? | `ls` |
| In / up / home | `cd code` · `cd ..` · `cd ~` |
| Make a folder | `mkdir code` |
| Open in the file window | `start .` (Windows) · `open .` (macOS) |

Keep every project in `~/code`. No spaces in folder names. Press Tab to finish names.

## Clone, then the loop

```bash
cd ~/code
gh repo clone owner/name          # or: git clone https://github.com/owner/name.git
git status                        # what changed?
git add .                         # choose every change
git commit -m "Say what changed"  # save one version
git push                          # send it to GitHub
```

A clone lands in the folder you are in. After `push`, `git status` should say **working tree clean**.

## Publish

Repository → **Settings** → **Pages** → Source **Deploy from a branch** → `main`, `/ (root)` → **Save**.
Address: `https://<username>.github.io/<repository>/`. Up to 10 minutes after each push.

## The limits

1 GB published site · 100 GB a month bandwidth (soft) · 10 builds an hour (soft) · 10 minutes per
deployment. Free for public repositories.

**Pages shows products; it does not sell them.** GitHub's terms forbid running an online shop on
Pages. Link each product's `buyUrl` to a checkout that runs elsewhere, or leave it out and the button
reads "Ask about this".

## When it goes wrong

| You see | Do this |
|---|---|
| a command "is not recognized" right after installing | open a new terminal window |
| `brew: command not found` | run the setup lines Homebrew printed |
| "products.js did not load" | find the missing comma; the browser console names the line |
| "ahead of 'origin/main' by 1 commit" | `git push` |
| 404 at your address | wait for the Actions run; check the folder is `/ (root)` |
