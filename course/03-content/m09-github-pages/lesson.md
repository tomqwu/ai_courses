# Module 9 — Ship a Product Catalog with GitHub Pages
> Part of AI Product Studio (APS-3) · Free and standalone · ~45 minutes of lesson, plus 60–90 minutes at the keyboard (most of it installs) · No prerequisites: take it first if you have never used a terminal

## Overview

Every product in this course eventually needs a page a stranger can open: what it is, what it costs, how to get it. This module builds that page and puts it on the internet for free, using **GitHub Pages**, from a computer that has none of the tools installed yet. It is written for someone who has never opened a terminal. If you have, skim Segments M9.1 and M9.2 and go straight to the lab.

By the end you will have three things you can point at. A terminal that proves its own setup, with a script that prints four PASS lines. A GitHub repository you created, cloned, changed and pushed from that terminal. And a public product catalog at an address of the form `https://<your-username>.github.io/<repository-name>/`, with filters, search and a working "Buy" or "Ask about this" button on every product.

The site you build is small on purpose: three files you edit and one you never touch. No framework, no build step, nothing to install beyond Git itself. That is not a beginner's compromise. It is the same shape the course's own expertise case study uses at a much larger scale: **AI × QE is a GitHub Pages site**, published at `tomqwu.github.io/ai_qe` (`ai_qe/_config.yml:5`, `ai_qe/_config.yml:13`), and it keeps its four briefing cards in one data file that a template draws onto the page (`ai_qe/CONTRIBUTING.md:23`). Your catalog keeps its products in one data file that a script draws onto the page. Same idea, fewer moving parts.

Every command in this module is given for **Windows** and **macOS**, side by side. Linux users can follow the macOS column; the commands are the same once Git and the GitHub CLI are installed.

**By the end of this module you can:**

- Install Git and the GitHub CLI on Windows or macOS, sign in, and prove the setup with a script rather than a guess.
- Move around your computer's folders from the terminal: know where you are, list what is there, go in and back out, and make a folder.
- Clone a repository to your computer, change it, and send the change back with `status → add → commit → push`.
- Publish a static site with GitHub Pages from a branch, and find its public address.
- State what GitHub Pages is for and what it is not — including why a catalog must link out to a checkout rather than be a shop.

## Segment M9.1 — Your tools, installed and proven (~15 min)

### Objective

Install Git and the GitHub CLI, tell Git who you are, sign in to GitHub from the terminal, and run a check that proves all four instead of assuming them.

### Lesson

**What the tools are.** *Git* records versions of a folder: every change you save is a *commit* you can return to. *GitHub* is a website that stores a copy of that folder, called a *repository*, and publishes it if you ask. The *GitHub CLI*, a command called `gh`, lets you talk to GitHub from the terminal — create a repository, sign in, clone — without clicking through the website. The *terminal* is a window where you type commands instead of clicking.

**Open a terminal.**

| | Windows | macOS |
|---|---|---|
| The app | **Terminal** (Windows 11) or **PowerShell** — press the Windows key, type `terminal`, press Enter | **Terminal** — press Cmd+Space, type `terminal`, press Enter |
| What you see | a line ending in `PS C:\Users\ada>` | a line ending in `ada@Adas-Mac ~ %` |

That line is the *prompt*. It is waiting for you to type. Everything in this module is typed after it, and you press Enter to run it.

**Install the package manager.** A package manager installs software from one command, and updates it later the same way. Both systems have one.

- **Windows** uses **winget**, the Windows Package Manager. It ships inside Microsoft's App Installer package and needs Windows 10 version 1809 or later, or Windows 11 (`github.com/microsoft/winget-cli`, README). Type `winget --version`. If the terminal says it does not recognise `winget`, install **App Installer** from the Microsoft Store and open a new terminal.
- **macOS** uses **Homebrew**. Install it with the one line from Homebrew's own instructions:

  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

  It asks for your Mac password, installs Apple's Command Line Tools along the way, and on Apple silicon Macs installs into `/opt/homebrew` (`github.com/Homebrew/install`, README). When it finishes it prints a few lines of shell setup instructions that add `brew` to your terminal. Copy and run them exactly — skipping them is the usual reason `brew` is "not found" afterwards.

**Install Git and the GitHub CLI.**

| | Windows | macOS |
|---|---|---|
| Git | `winget install --id Git.Git -e --source winget` | `brew install git` |
| GitHub CLI | `winget install --id GitHub.cli --source winget` | `brew install gh` |
| Then | close the terminal and open a **new window** | nothing — it is ready |

The Windows step that trips people up is the last row. Installing a tool changes the list of places the terminal looks for commands, and a terminal that was already open does not see the change; the GitHub CLI's own instructions say to open a new window, not just a new tab (`github.com/cli/cli`, `docs/install_windows.md`). The package names are the ones the maintainers publish: `Git.Git` in the Windows package repository (`github.com/microsoft/winget-pkgs`, `manifests/g/Git/Git`), `GitHub.cli` in the GitHub CLI's Windows instructions, and `git` and `gh` in Homebrew (`github.com/cli/cli`, `docs/install_macos.md`).

**Tell Git who you are.** Every commit records a name and an email. Set them once, for every repository on this computer:

```bash
git config --global user.name "Ada Example"
git config --global user.email "ada@example.com"
```

Use the email on your GitHub account, or the private "noreply" address GitHub offers in your email settings if you would rather not publish your own.

**Sign in to GitHub from the terminal.**

```bash
gh auth login
```

It asks four things. Answer **GitHub.com**, then **HTTPS**, then **Yes** to authenticating Git with your GitHub credentials, then **Login with a web browser**. It shows a one-time code, opens your browser, and you paste the code there. The default is this browser flow (`github.com/cli/cli`, `pkg/cmd/auth/login/login.go`). After it, `git` can push to your repositories without asking for a password each time.

**Prove it.** Setting up a machine is the step people most often believe they finished when they did not. So the module ships a check that looks at all four and prints the fix for anything missing (`course/03-content/m09-github-pages/setup/check-setup.sh`, `course/03-content/m09-github-pages/setup/check-setup.ps1`). Run the one for your system from the folder that contains it:

| Windows | macOS |
|---|---|
| `powershell -ExecutionPolicy Bypass -File .\check-setup.ps1` | `bash check-setup.sh` |

A finished setup prints four PASS lines and **4 of 4 checks passed**. Anything less prints a FAIL with the exact command that fixes it — on a Mac with no Homebrew, it prints the Homebrew line first. Fix the first FAIL, open a new terminal, and run it again. The Windows flag `-ExecutionPolicy Bypass` lets this one script run without changing your computer's settings for any other script.

### Action step

Run the check until it says 4 of 4, and paste the whole output into a new file called `evidence.md` — you will add to it for the rest of the module. If a step failed along the way, paste the failure too, with what fixed it. That record is worth more than a clean one.

## Segment M9.2 — Find your way around, then clone (~15 min)

### Objective

Know where you are in the folder tree, move in and out of folders, make one, and clone a repository into it — then send a change back with the four-command loop.

### Lesson

**You are always somewhere.** The terminal always has a *current folder*, the way a file window always shows one folder. When it opens, that is your **home folder**: `C:\Users\ada` on Windows, `/Users/ada` on a Mac. Both systems let you write your home folder as `~`.

| What you want | Windows (PowerShell) | macOS | Notes |
|---|---|---|---|
| Where am I? | `pwd` | `pwd` | prints the current folder |
| What is here? | `ls` | `ls` | PowerShell also accepts `dir` |
| Go into a folder | `cd code` | `cd code` | relative to where you are |
| Go up one level | `cd ..` | `cd ..` | two dots means "the folder above" |
| Go home | `cd ~` | `cd ~` | from anywhere |
| Make a folder | `mkdir code` | `mkdir code` | |
| Open this folder in the file window | `start .` | `open .` | one dot means "here" |
| Finish a long name for you | press Tab | press Tab | the fastest way to avoid typos |

**Absolute and relative paths.** A path that starts from the top of the disk is *absolute*: `C:\Users\ada\code` or `/Users/ada/code`. A path that starts from where you are is *relative*: `code`, or `..\Documents`. Windows separates folders with a backslash `\` and macOS with a forward slash `/`. PowerShell accepts either on Windows, so `cd code/my-catalog` works on both systems — a small thing that saves a lot of confusion when you copy commands from the internet.

**Names with spaces need quotes.** `cd My Projects` tries to go into a folder called `My`. Type `cd "My Projects"`, or avoid spaces in project folder names entirely, which is what most developers do: `my-catalog`, not `My Catalog`.

**Keep your projects in one place.** Make a folder called `code` in your home folder and put every repository in it. Then "where is my project?" always has the same answer:

```bash
cd ~
mkdir code
cd code
pwd
```

On a Mac the last line prints `/Users/ada/code`; on Windows, `C:\Users\ada\code`, under a `Path` heading.

**Cloning is copying a repository to your computer, with its history.** Two ways, and they do the same thing:

```bash
gh repo clone tomqwu/ai_courses
git clone https://github.com/tomqwu/ai_courses.git
```

`gh repo clone` takes the short `owner/name` form and uses the sign-in you set up; `git clone` takes the full address, which is what you will see on any repository's green **Code** button. Either one makes a new folder named after the repository inside the folder you are in. That is the most common beginner mistake in reverse: cloning while in your home folder, then not finding the project in `code`. Run `pwd` first.

**The loop that sends a change back.** Once a folder is a repository, every change goes through the same four commands:

| Command | What it does | What you should see |
|---|---|---|
| `git status` | shows what changed since your last commit | files listed as modified or untracked |
| `git add .` | chooses every change in this folder for the next commit | nothing; silence is success |
| `git commit -m "Say what changed"` | saves those changes as one version, with your message | a line with a short code and the number of files |
| `git push` | sends your new commits to GitHub | a line ending `main -> main` |

Here is the loop run for real on the catalog starter, in a folder cloned from a repository that had only a README (the output is exactly what Git printed; your short codes will differ):

```text
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
	modified:   README.md

Untracked files:
	.nojekyll
	app.js
	index.html
	products.js
	styles.css

$ git commit -m "Add the catalog starter"
[main c02f59f] Add the catalog starter
 6 files changed, 497 insertions(+), 1 deletion(-)

$ git push
   699905a..c02f59f  main -> main
```

Read `git status` before and after, every time. Before, it tells you what you are about to commit. After, **nothing to commit, working tree clean** tells you it all went.

### Action step

From your `code` folder, clone this course's repository with either command, `cd` into it, and run `ls`. Then go back up with `cd ..` and run `pwd` to prove where you are. Add both outputs to `evidence.md`.

## Segment M9.3 — Build the catalog and publish it (~15 min)

### Objective

Turn the starter into your own catalog, preview it on your computer, publish it with GitHub Pages, and state what the host allows and what it does not.

### Lesson

**The starter is five files, and you edit one of them.** It lives at `course/03-content/m09-github-pages/catalog-starter/`:

| File | What it is | Edit it? |
|---|---|---|
| `products.js` | your store's name and contact, and a list of products | **yes** |
| `index.html` | the page | two lines near the top: the description a search result shows |
| `styles.css` | colours and layout | only the colours in `:root`, if you like |
| `app.js` | draws the cards, the category buttons, search and sort | no |
| `.nojekyll` | an empty file | no — keep it |

Each product is a small block with a name, a category, a price and a one-line summary. Add `image` to show a photo, and `buyUrl` to link out to a checkout; without one, the button becomes **Ask about this** and opens an email. One filter button appears for each category you use.

**Why products live in a `.js` file, not a `.json` one.** A browser will not let a page opened from your disk read a separate data file, but it will run a script loaded with a `<script>` tag. Keeping the products in `products.js` means you can double-click `index.html` and see exactly what the world will see, with no server, no install and no build. That is also why the preview is honest: there is no step between your computer and the published site that could change what appears.

**Separate the data from the layout.** AI × QE does the same at scale: its homepage cards come from `_data/briefing_room.json`, "the four presentation cards" (`ai_qe/CONTRIBUTING.md:23`), and a template loops over that file to draw them (`ai_qe/releases.md:222`). When a product changes, you change one entry in one data file. Nobody has to touch the page.

**Preview it.** In the file window, double-click `index.html`. Or from the terminal, in the project folder:

| Windows | macOS |
|---|---|
| `start index.html` | `open index.html` |

The starter was checked this way in a headless browser, opened straight from disk, at phone and desktop widths in light and dark mode: six products render, the filter, search and sort work, nothing scrolls sideways, and every piece of text meets the WCAG AA contrast minimum (`course/03-content/m09-github-pages/catalog-starter/README.md`).

**Publish it.** GitHub Pages publishes the files in a repository as a website. For a project like this one, the steps are GitHub's own (`github.com/github/docs`, `content/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site.md`):

1. On GitHub, open your repository and choose **Settings**, then **Pages** in the left column.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Choose the branch `main` and the folder `/ (root)`, then **Save**.

The site appears at `https://<your-username>.github.io/<repository-name>/` — the address pattern for a project site (`github.com/github/docs`, `content/pages/getting-started-with-github-pages/what-is-github-pages.md`) — and GitHub says it can take up to 10 minutes after a push for a change to publish. The **Visit site** button on the same Settings page shows the exact address once it is live. Every later `git push` republishes it; you never repeat these steps.

The `.nojekyll` file matters here. By default, GitHub Pages runs every site through **Jekyll**, a tool that turns templates into pages; an empty `.nojekyll` file turns that off, so your files are published exactly as they are.

**Two ways to publish, same host.** Your catalog uses the simplest mode: publish a branch as it is. AI × QE uses the other one: a GitHub Actions workflow that builds the site with Jekyll, runs its own checks on links, narration and PDF editions, and only then deploys (`ai_qe/.github/workflows/pages.yml:77`, `ai_qe/.github/workflows/pages.yml:155`). The deploy step needs two explicit permissions, `pages: write` and `id-token: write` (`ai_qe/.github/workflows/pages.yml:148-149`). You do not need any of that today. The point is that the host is the same, and a site can grow from one mode to the other without moving.

**What GitHub Pages is for, and what it is not.** GitHub publishes the limits, and they are generous for a catalog (`github.com/github/docs`, `content/pages/getting-started-with-github-pages/github-pages-limits.md`):

| Limit | Value | Kind |
|---|---|---|
| Published site size | 1 GB | hard |
| Bandwidth | 100 GB a month | soft |
| Builds | 10 an hour | soft |
| A single deployment | 10 minutes before it times out | hard |

Pages is free for **public** repositories on a free account; publishing from a **private** repository needs a paid plan (`github.com/github/docs`, `data/reusables/gated-features/pages.md`).

The rule that shapes this whole design is the last one on that page: GitHub Pages "is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service". A catalog that describes your products is fine. A shop is not. That is why the starter has no cart and no checkout: each product can link out with `buyUrl` to a checkout that runs somewhere built for payments, and the catalog stays what Pages allows it to be. Build it that way from the start and there is nothing to undo later.

### Action step

Replace the six sample products with at least three of your own — real ones, or the product you are building in this course. Preview with a double-click, then write one line in `evidence.md` naming where your "Buy" button will point, or why it says "Ask about this" for now.

## Recap

- **Tools, proven.** Git records versions; GitHub stores and publishes them; `gh` drives GitHub from the terminal. Install with winget on Windows and Homebrew on macOS, open a new window after installing on Windows, set your name and email, `gh auth login`, and run the setup check until it says 4 of 4.
- **Folders.** `pwd`, `ls`, `cd`, `cd ..`, `mkdir` work the same on both systems in PowerShell and Terminal. Keep projects in `~/code`. Check `pwd` before you clone.
- **The loop.** `git status → git add . → git commit -m "…" → git push`, reading `status` before and after.
- **Publish.** Settings → Pages → Deploy from a branch → `main`, `/ (root)` → Save. The address is `https://<username>.github.io/<repository>/`, up to 10 minutes after each push.
- **The boundary.** Pages shows products; it does not sell them. Link out to a checkout.

## Discussion prompt

Post your catalog's address and one thing that went wrong during setup, with the line that fixed it. Then open a classmate's catalog on your phone and tell them the first thing you tried to tap that did not do what you expected.

## Sources

Read on 2026-09-26 from the maintainers' own repositories. The rendered documentation sites were not reachable from the environment this module was written in, so each source is the file those sites are built from.

- GitHub Pages: publishing from a branch, site types and addresses, limits and prohibited uses, plan availability, publishing time — `github.com/github/docs`, `content/pages/getting-started-with-github-pages/` and `data/reusables/`.
- GitHub CLI: Windows and macOS install commands, the new-window note, `gh auth login`, `gh repo create` flags — `github.com/cli/cli`, `docs/install_windows.md`, `docs/install_macos.md`, `pkg/cmd/auth/login/login.go`, `pkg/cmd/repo/create/create.go`.
- Git for Windows package id `Git.Git` — `github.com/microsoft/winget-pkgs`, `manifests/g/Git/Git`.
- winget requirements and App Installer — `github.com/microsoft/winget-cli`, README.
- Homebrew install line, Command Line Tools, `/opt/homebrew` — `github.com/Homebrew/install`, README; Git formula — `github.com/Homebrew/homebrew-core`, `Formula/g/git.rb`.
