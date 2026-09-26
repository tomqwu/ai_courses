# Glossary — M9: Ship a Product Catalog with GitHub Pages

Alphabetical. Each term: definition, then where it lives (repo pointer or course file).

**Absolute path.** A folder address that starts from the top of the disk, such as `C:\Users\ada\code`
or `/Users/ada/code`. It means the same thing wherever you are. Lives in `lesson.md`, Segment M9.2.

**Clone.** A copy of a repository on your computer, with its full history and a link back to the
original, made with `gh repo clone owner/name` or `git clone <address>`. Lands in the folder you are
in. Lives in `lab.md`, Step 3.

**Commit.** One saved version of a repository, with a message, an author and a short code such as
`c02f59f`. Made with `git commit -m "…"` after choosing changes with `git add`. Lives in `lab.md`,
Step 6.

**Deploy from a branch.** The simplest GitHub Pages mode: publish the files in one branch and folder
exactly as they are. Set under Settings → Pages. Lives in `lesson.md`, Segment M9.3.

**Git.** The tool that records versions of a folder on your computer. Installed with
`winget install --id Git.Git -e --source winget` or `brew install git`. Lives in
`setup/check-setup.sh` and `setup/check-setup.ps1`.

**GitHub.** The website that stores copies of repositories and can publish them. Not the same thing as
Git: Git runs on your computer, GitHub on the internet. Lives in `lesson.md`, Segment M9.1.

**GitHub CLI (`gh`).** The command that drives GitHub from the terminal: sign in, create a repository,
clone. Installed with `winget install --id GitHub.cli --source winget` or `brew install gh`. Lives in
`setup/check-setup.sh`.

**GitHub Pages.** GitHub's free hosting for static sites from a repository, at
`https://<owner>.github.io/<repository>/`. Not allowed to run an online shop. The course's own
AI × QE site uses it (`ai_qe/_config.yml:5`).

**Home folder.** The folder a terminal opens in, written `~` on both systems: `C:\Users\ada` on Windows,
`/Users/ada` on a Mac. Lives in `lesson.md`, Segment M9.2.

**Homebrew.** The package manager for macOS. Installs Apple's Command Line Tools along the way and,
on Apple silicon, lives in `/opt/homebrew`. Lives in `lab.md`, Step 1.

**Jekyll.** The site builder GitHub Pages runs by default. The course's AI × QE site uses it on purpose
(`ai_qe/.github/workflows/pages.yml:77`); the catalog turns it off with `.nojekyll`.

**`.nojekyll`.** An empty file that tells GitHub Pages to publish the files as they are, without
running Jekyll. Hidden by default because its name starts with a dot. Lives in
`catalog-starter/.nojekyll`.

**Package manager.** A tool that installs and updates software with one command: winget on Windows,
Homebrew on macOS. Lives in `lesson.md`, Segment M9.1.

**Prompt.** The line in a terminal waiting for you to type, ending in `>` in PowerShell or `%` in the
Mac Terminal. Lives in `lesson.md`, Segment M9.1.

**Push.** Sending your new commits to GitHub with `git push`. Until you push, a commit exists only on
your computer, and Pages cannot publish it. Lives in `lab.md`, Step 6.

**Relative path.** A folder address that starts from where you are, such as `code/my-catalog` or `..`.
Lives in `lesson.md`, Segment M9.2.

**Repository.** A folder whose history Git records, plus its copy on GitHub. Created from the terminal
with `gh repo create`. Lives in `lab.md`, Step 4.

**Setup check.** The script that tests Git, the GitHub CLI, your identity and your sign-in, and prints
the exact fix for any failure. Lives in `setup/check-setup.sh` and `setup/check-setup.ps1`.

**Terminal.** A window where you type commands instead of clicking: Terminal or PowerShell on Windows,
Terminal on macOS. Lives in `lesson.md`, Segment M9.1.

**winget.** The Windows Package Manager, shipped inside Microsoft's App Installer; needs Windows 10
version 1809 or later. Lives in `lab.md`, Step 1.

**Working tree clean.** What `git status` says when every change has been committed. After a push, it
is the proof that everything went. Lives in `lab.md`, Step 6.
