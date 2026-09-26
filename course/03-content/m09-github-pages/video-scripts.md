# Video Scripts — M9: Ship a Product Catalog with GitHub Pages

> Master recording scripts, one per segment. Pacing: ~130 words/minute. The beats are the spoken
> spine, not a verbatim transcript — read them in your own words and keep every command, pointer and
> number exactly as written. Record the terminal twice where the systems differ: once in PowerShell on
> Windows, once in Terminal on a Mac, and cut between them at the same beat.

## M9.1 — Your tools, installed and proven

**Target runtime: 15 minutes (≈1,950 words of screen time, most of it installs running).**

**Cold open (≈15 s).** "Here is a computer with nothing on it. No Git, no GitHub CLI, never signed in.
In fifteen minutes it will print four PASS lines, and you will not have to take my word for any of
them."

**Beats**

| Time | On screen | Narration |
|---|---|---|
| 0:00 | Title slide | This module is free and needs nothing. If you have never opened a terminal, you are in the right place. Every command is shown for Windows and for a Mac, side by side. |
| 0:30 | Slide: four names, one job each | Git records versions of a folder on your computer. GitHub stores a copy and can publish it. The GitHub CLI connects the two from the terminal. Most confusion is mixing up Git and GitHub, so hold that difference. |
| 1:30 | Windows: Windows key, `terminal`; Mac: Cmd+Space, `terminal` | Open a terminal now. That line ending in your folder name is the prompt. It is waiting for you to type. |
| 2:30 | Windows: `winget --version` | Windows ships a package manager called win get, inside App Installer. If it is not recognised, install App Installer from the Microsoft Store and open a new window. |
| 3:30 | Mac: Homebrew install line running, then its closing setup lines | On a Mac, the package manager is Homebrew. Paste its one install line. At the end it prints a few setup lines — run those too, or brew will not be found. |
| 6:00 | Windows: `winget install --id Git.Git -e --source winget`, then `GitHub.cli` | One command each for Git and the GitHub CLI. Then the step everyone skips: close this window and open a new one. A window that was open during the install cannot see the new command. |
| 8:00 | Mac: `brew install git`, `brew install gh` | On a Mac, the same two tools, one line each. |
| 9:30 | `git config --global user.name` and `user.email` | Every commit records a name and an email. Set them once. The private no-reply address from your GitHub settings is fine. |
| 10:30 | `gh auth login`, four prompts, the one-time code in the browser | Sign in: GitHub dot com, HTTPS, yes, log in with a web browser. Paste the code. From now on Git can push without a password. |
| 12:30 | Windows: `check-setup.ps1` printing two FAILs with fixes | Now prove it. This is the setup check on a machine that is not finished. Each FAIL prints the exact command that fixes it: `course/03-content/m09-github-pages/setup/check-setup.ps1`. |
| 14:00 | Mac: `bash check-setup.sh` printing **4 of 4 checks passed** | Fix the first failure, open a new window, run it again, until it says four of four. Paste the whole output, failures included, into `evidence.md`. |

## M9.2 — Find your way around, then clone

**Target runtime: 12 minutes (≈1,560 words).**

**Cold open (≈15 s).** "Every beginner loses ten minutes the same way: they clone a project, go to
their projects folder, and it is not there. By the end of this segment you will know exactly why."

**Beats**

| Time | On screen | Narration |
|---|---|---|
| 0:00 | Slide: you are always somewhere | The terminal always has a current folder. When it opens, that is your home folder, and both systems write it as a tilde. |
| 1:00 | Split screen: `pwd`, `ls`, `cd code`, `cd ..`, `cd ~` on both systems | Five commands, the same on both. Print where you are, list what is here, go in, go up, go home. |
| 3:00 | `start .` on Windows, `open .` on a Mac | To see the same folder in a normal window: start dot on Windows, open dot on a Mac. |
| 4:00 | Slide: absolute and relative paths | An absolute path starts from the top of the disk; a relative one starts from here. PowerShell accepts forward slashes too, so `code/my-catalog` works on both. |
| 5:30 | `cd My Projects` failing, then `cd "My Projects"` | A space in a folder name breaks the command. Quote it, or never use spaces: my-catalog, with a hyphen. |
| 6:30 | `cd ~`, `mkdir code`, `cd code`, `pwd` | Make one folder for every project, called code, in your home folder. |
| 7:30 | `gh repo clone tomqwu/ai_courses` | Clone copies a repository to your computer with its history. It lands in the folder you are in. That is the ten minutes from the cold open: check with P W D first. |
| 9:00 | Slide: the loop, then the real output | Every change goes back through four commands: status, add, commit, push. Here they are, run for real on the catalog starter. The last status says working tree clean. That is the proof. |

## M9.3 — Build the catalog and publish it

**Target runtime: 15 minutes (≈1,950 words, including the wait for the first build).**

**Cold open (≈15 s).** "This is a product catalog. Filters, search, a button on every product. It is
five files, you edit one, and it costs nothing to host — as long as you respect one rule, which I will
read to you word for word."

**Beats**

| Time | On screen | Narration |
|---|---|---|
| 0:00 | The starter open in a browser from disk, filters clicked | Five files. You edit `products.js`. The page is drawn by a script you never touch. |
| 1:30 | `products.js`, one product block | Each product is one block: id, name, category, a price as a plain number, a summary. A missing comma is the most common mistake, and the browser console names the line. |
| 3:00 | Slide: why a script, not JSON | A page opened from your disk cannot read a separate data file, but it can run a script. So you preview with a double-click, and what you see is what the world will see. |
| 4:30 | `ai_qe/_data/briefing_room.json`, then `ai_qe/releases.md:222` | The course's own AI times Q E site does the same thing at scale: its briefing cards live in one data file, and a template loops over it. |
| 6:00 | `gh repo create my-catalog --public --add-readme --clone`, copy, `git status` | Create your repository from the terminal, copy the starter in, and check the status lists all five files, including the hidden one. |
| 8:00 | Settings → Pages → Deploy from a branch → `main`, `/ (root)` → Save | Four clicks, once. GitHub says a change can take up to ten minutes to publish. Watch the Actions tab while it runs. |
| 10:00 | Slide: the limits | One gigabyte, one hundred gigabytes a month, ten builds an hour, ten minutes a deployment. Generous for a catalog. |
| 11:00 | GitHub's limits page, the prohibited-use sentence highlighted | Here is the rule. Read it as written: Pages is not allowed to be used as free hosting to run an online business or an e-commerce site. A catalog, yes. A shop, no. |
| 12:30 | A product's `buyUrl`, then "Ask about this" opening an email | So each product links out to a checkout that runs somewhere built for payments, or asks the visitor to get in touch. |
| 13:30 | The live address on a phone; a price change pushed; the new price appearing | Open your address on your phone. Change one price, push, and watch it republish. That is the whole loop, and it is yours now. |
