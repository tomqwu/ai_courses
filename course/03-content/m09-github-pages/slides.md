---
marp: true
theme: aps
paginate: true
title: M9 — Ship a Product Catalog with GitHub Pages
---

<!-- _class: lead -->

# M9 — Ship a Product Catalog with GitHub Pages

**AI Product Studio (APS-3)** · ~45 minutes · Free and standalone · No prerequisites

From nothing installed to a public catalog page.

<!-- NOTES: Welcome to M9. This module is free and needs nothing: take it first if you have never used a terminal. Promise: by the end the learner has the tools installed and proven, a repository they cloned and pushed, and a public product catalog at their own github.io address. Say plainly that every command is given for Windows and for macOS, side by side. Timing: 1 minute. Transition: the five outcomes. -->

---

## By the end you can…

- **Install** Git and the GitHub CLI, then prove it
- **Move** through folders from the terminal
- **Clone**, change and push a repository
- **Publish** a static site with GitHub Pages
- **State** what Pages allows, and what it forbids

<!-- NOTES: Read the five outcomes as the lab's checklist in advance: Lab M9 has an item for each, and Quiz M9 checks the same five. Stress the last one, because it shapes the design: the catalog shows products and links out to a checkout. Timing: 1 minute. Transition: the tools. -->

---

## M9.1 — Four things, one job each

| Name | What it does |
|---|---|
| **Terminal** | a window where you type commands instead of clicking |
| **Git** | records versions of a folder; each saved version is a commit |
| **GitHub** | stores a copy of that folder, a repository, and can publish it |
| **gh** | the GitHub CLI: drives GitHub from the terminal |

<!-- NOTES: Keep this concrete. Git is on the learner's computer; GitHub is a website; gh connects the two from the terminal. Most beginner confusion is mixing up Git and GitHub, so name the difference once and move on. Timing: 1 minute. Transition: opening a terminal. -->

---

## Open a terminal

| | Windows | macOS |
|---|---|---|
| The app | Terminal, or PowerShell | Terminal |
| How | Windows key, type `terminal`, Enter | Cmd+Space, type `terminal`, Enter |
| The prompt | `PS C:\Users\ada>` | `ada@Adas-Mac ~ %` |

The prompt is waiting for you. Type after it, then press Enter.

<!-- NOTES: Have everyone open a terminal now, not later. On Windows 11 the app is Terminal and its default shell is PowerShell, which is what every Windows command in this module assumes. Point at the prompt and say it is just a place to type. Timing: 1 minute. Transition: installing the tools. -->

---

## Install with one command each

Windows — PowerShell. `winget` ships inside App Installer.

```powershell commands
winget install --id Git.Git -e --source winget
winget install --id GitHub.cli --source winget
```

**Then open a new terminal window.** macOS — install Homebrew, run the setup lines it prints, then:

```bash commands
brew install git
brew install gh
```

<!-- NOTES: Windows: winget ships in App Installer and needs Windows 10 1809 or later; if it is not recognised, install App Installer from the Store. macOS: Homebrew's own install line, then the shell setup lines it prints, which people skip. The Windows trap is the bold line: a window opened before the install cannot see the new command, so open a new window, not a tab. Package names are the maintainers' own: Git.Git in the winget repository, GitHub.cli in the CLI's Windows instructions. Timing: 3 minutes, plus waiting. Transition: identity and sign-in. -->

---

## Tell Git who you are, then sign in

```bash commands
git config --global user.name "Ada Example"
git config --global user.email "ada@example.com"
gh auth login
```

Answer **GitHub.com**, then **HTTPS**, then **Yes**, then **Login with a web browser**.

Paste the one-time code in the browser, and Git can push without a password.

<!-- NOTES: Two identity lines, once per computer. Suggest the GitHub noreply address for anyone who does not want their email in public history. Then gh auth login: four prompts, and the browser flow is the default. After it, git uses those credentials for pushes. Timing: 2 minutes. Transition: proving it. -->

---

<!-- _class: proof -->

## Proof: a script, not a feeling

```text output
PASS  git is installed: git version 2.43.0
FAIL  GitHub CLI (gh) is not installed
      fix: winget install --id GitHub.cli --source winget   then open a NEW terminal window
PASS  git knows who you are: Ada Example <ada@example.com>
FAIL  not signed in to GitHub from the terminal
      fix: gh auth login   (choose GitHub.com, HTTPS, yes to git credentials, ...)

2 of 4 checks passed.
```

`course/03-content/m09-github-pages/setup/check-setup.ps1` · macOS: `setup/check-setup.sh`

<!-- NOTES: This is real output from the Windows script under PowerShell, with only the name changed. The point: setting up a machine is the step people most often believe they finished when they did not, so the check names the exact fix for each failure. Fix the first FAIL, open a new window, run again until 4 of 4. Timing: 2 minutes. Transition: the action step. -->

---

## Action step — M9.1

- Run the check until it says **4 of 4**
- Paste the whole output into `evidence.md`
- Keep every failure, and the line that fixed it

<!-- NOTES: Make evidence.md now. The failures with their fixes are worth more than a clean run: they are what the next learner needs. Timing: 30 seconds, then the time the installs take. Transition: finding your way around. -->

---

## M9.2 — You are always somewhere

| What you want | Windows and macOS | Notes |
|---|---|---|
| Where am I? | `pwd` | prints the current folder |
| What is here? | `ls` | PowerShell also takes `dir` |
| Go into a folder | `cd code` | relative to where you are |
| Go up one level | `cd ..` | two dots: the folder above |
| Go home | `cd ~` | the tilde is your home folder |
| Open it in the file window | `start .` · `open .` | Windows · macOS |

<!-- NOTES: The same five commands work in PowerShell and in the Mac Terminal, which surprises people. Demonstrate each once. Mention Tab completion out loud: it is the fastest way to avoid typos. Timing: 3 minutes. Transition: paths. -->

---

## Paths: absolute, relative, and the slash

| | Windows | macOS |
|---|---|---|
| Absolute: from the top | `C:\Users\ada\code` | `/Users/ada/code` |
| Relative: from here | `code\my-catalog` | `code/my-catalog` |
| Works on both | `code/my-catalog` | `code/my-catalog` |

A name with a space needs quotes: `cd "My Projects"`. Better: no spaces, `my-catalog`.

<!-- NOTES: PowerShell accepts forward slashes, so commands copied from the internet usually work on Windows as written. The space-in-names trap causes more lost time than any other in first sessions. Timing: 2 minutes. Transition: cloning. -->

---

## Clone: a copy, with its history

```bash commands
cd ~/code
pwd
gh repo clone tomqwu/ai_courses
git clone https://github.com/tomqwu/ai_courses.git
```

Either clone command makes a folder **where you are**. Run `pwd` first.

<!-- NOTES: gh repo clone takes owner/name and uses the sign-in; git clone takes the full address from the green Code button. The common mistake is cloning from the home folder and then not finding the project in code. Timing: 2 minutes. Transition: sending changes back. -->

---

## The loop that sends a change back

<!-- _diagram: flow -->
- `git status` — what changed?
- `git add .` — choose every change
- `git commit -m "…"` — save one version
- `git push` — send it to GitHub

Read `git status` before and after. Clean afterwards means it all went.

<!-- NOTES: Four commands, always in this order. Silence from git add is success, which unsettles beginners; say it. The after-status is the proof. Timing: 2 minutes. Transition: the loop run for real. -->

---

<!-- _class: proof -->

## Proof: the loop, run for real

```text output
$ git status
Untracked files:  .nojekyll  app.js  index.html  products.js  styles.css
$ git commit -m "Add the catalog starter"
[main c02f59f] Add the catalog starter
 6 files changed, 497 insertions(+), 1 deletion(-)
$ git push
   699905a..c02f59f  main -> main
$ git status
nothing to commit, working tree clean
```

<!-- NOTES: This is the loop as Git actually printed it on the catalog starter, with the untracked list condensed onto one line. Your short codes will differ. Point at the last line: that is the proof. Timing: 1 minute. Transition: the action step. -->

---

## Action step — M9.2

- `cd ~/code`, then clone the course
- `cd` into it and run `ls`
- `cd ..`, then `pwd` to prove where you are
- Paste both outputs into `evidence.md`

<!-- NOTES: Everyone should end this segment with the course cloned into code and a pwd in their evidence. Timing: 30 seconds, plus the clone. Transition: the catalog. -->

---

## M9.3 — Five files, and you edit one

| File | What it is | Edit it? |
|---|---|---|
| `products.js` | store name, contact, the products | **yes** |
| `index.html` | the page | the description line only |
| `styles.css` | colours and layout | the colours, if you like |
| `app.js` | draws cards, filters, search, sort | no |
| `.nojekyll` | an empty file | no, keep it |

`course/03-content/m09-github-pages/catalog-starter/`

<!-- NOTES: The starter is deliberately small: no framework, no build step, nothing beyond Git to install. The learner edits one file. Timing: 2 minutes. Transition: why the data is a script. -->

---

## Why the data is a script, not JSON

```js template
{
  id: "everyday-mug",
  name: "Everyday Mug",
  category: "Mugs",
  price: 32,
  summary: "A 350 ml mug with a thumb rest.",
  buyUrl: ""
}
```

A page opened from disk cannot read a data file, but it can run a script. Double-click to preview.

<!-- NOTES: This is the one design decision worth explaining. A browser blocks a page opened with file:// from fetching a separate JSON file, but it runs a script loaded with a tag. So the preview is a double-click and it is identical to the published page. Timing: 2 minutes. Transition: the same pattern at scale. -->

---

## Same pattern, larger site

| | Your catalog | AI × QE |
|---|---|---|
| The data | `products.js` | `ai_qe/_data/briefing_room.json` |
| Drawn by | `app.js` | a template loop, `ai_qe/releases.md:222` |
| Published by | deploy from a branch | an Actions workflow with checks |
| Address | `<you>.github.io/my-catalog` | `tomqwu.github.io/ai_qe` |

`ai_qe/_config.yml:5` · `ai_qe/.github/workflows/pages.yml:155`

<!-- NOTES: The course's own expertise case study is a GitHub Pages site. Its four briefing cards live in one data file that a template loops over, the same separation as the starter. The difference is the publishing mode: AI x QE builds with Jekyll and runs its own checks in an Actions workflow before deploying. Same host, two modes. Timing: 2 minutes. Transition: publishing. -->

---

## Publish from a branch

<!-- _diagram: steps -->
- Repository **Settings**, then **Pages**
- Source: **Deploy from a branch**
- Branch `main`, folder `/ (root)`
- **Save**, then wait up to ten minutes

Your address: `https://<username>.github.io/<repository>/`

<!-- NOTES: These are GitHub's own steps for publishing from a branch. It can take up to 10 minutes after a push for a change to appear; the Actions tab shows a pages build and deployment run. Every later push republishes; they never repeat these steps. Timing: 2 minutes. Transition: the limits. -->

---

## The limits, from GitHub's own page

| Limit | Value | Kind |
|---|---|---|
| Published site size | 1 GB | hard |
| Bandwidth | 100 GB a month | soft |
| Builds | 10 an hour | soft |
| One deployment | 10 minutes | hard |

Free for **public** repositories; a **private** one needs a paid plan.

<!-- NOTES: All four numbers are from GitHub's limits page, and plan availability from its gated-features note. Generous for a catalog. Keep photos under about 500 KB each and the size limit never matters. Timing: 1 minute. Transition: the rule that shapes the design. -->

---

## A catalog, not a shop

> GitHub Pages "is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service".

So the starter has no cart. `buyUrl` links out to a checkout that runs elsewhere; without one, the button reads **Ask about this**.

<!-- NOTES: Quote the rule verbatim: it is GitHub's own limits page. This is why the starter was designed the way it was, and building it right from the start means nothing to undo later. Timing: 2 minutes. Transition: the action step. -->

---

## Action step — M9.3

- Replace the samples with three of your own products
- Double-click `index.html` to preview
- Note where each button points, in `evidence.md`

<!-- NOTES: Real products, or the product they are building in the course. The note about button destinations forces the payments decision early. Timing: 30 seconds. Transition: the lab. -->

---

## Lab M9 — Publish your product catalog

| Steps | You finish with |
|---|---|
| 0–1 | a GitHub account and **4 of 4** from the setup check |
| 2–3 | `~/code`, and the course cloned into it |
| 4 | your own public `my-catalog` repository, cloned |
| 5 | your products, previewed on your computer |
| 6 | a commit, pushed, and a clean `git status` |
| 7–8 | a live address on your phone, then republished |

<!-- NOTES: 60 to 90 minutes, most of it installs. Eight checklist items, all objectively verifiable, and evidence.md committed into my-catalog at the end. Timing: 1 minute. Transition: the quiz. -->

---

## Quiz M9 — what it checks

- Why a new window after installing on Windows
- What a missing identity actually blocks
- Where a clone lands, and why
- What `push` does that `commit` does not
- Why the catalog links out to a checkout

<!-- NOTES: Six multiple choice and two short answers, one objective each, with the map at the end of the key. The short answers are applied: a classmate's broken Homebrew setup, and a same-day publish for a shop owner. Timing: 1 minute. Transition: recap. -->

---

## Recap

- **Tools, proven:** winget or Homebrew, then **4 of 4**
- **Folders:** `pwd`, `ls`, `cd`, `cd ..`, `mkdir`
- **The loop:** status, add, commit, push
- **Publish:** Settings, Pages, deploy from `main`
- **The boundary:** show products; link out to sell

<!-- NOTES: Five lines, one per outcome. Timing: 1 minute. Transition: the discussion prompt. -->

---

## Discussion prompt

Post your catalog's address and the setup step that took longest, with the line that fixed it.

Then open a classmate's catalog on your phone, and tell them the first thing you tapped that did not do what you expected.

<!-- NOTES: The second half is usability testing in miniature, and it is where most learners find their first real improvement. Timing: 1 minute. -->
