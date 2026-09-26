# Lab M9 — Publish your product catalog

> Free and standalone · Prerequisites: none — a Windows 10 (1809 or later), Windows 11 or macOS computer, and a free GitHub account · Time: 60–90 minutes, most of it installs · Pass = every checklist item below is objectively verifiable

**Goal.** Go from a computer with nothing installed to a public product catalog at `https://<your-username>.github.io/my-catalog/`, built from files you cloned, changed and pushed from the terminal.

**Where to work.** A folder called `code` in your home folder. Keep a file called `evidence.md` open beside you and paste into it as you go: every step below says what to paste.

**How to read the commands.** Where Windows and macOS differ, both are given. Type everything after the prompt and press Enter. Windows commands are for **PowerShell** — the default in Windows Terminal. If a command is the same on both, it is shown once.

## Step 0 — Make a GitHub account (~5 min)

If you do not have one, sign up at `github.com` with an email you can open. Choose your username carefully: it becomes part of your catalog's address. Paste your username into `evidence.md`.

## Step 1 — Install the tools and prove them (~30 min, mostly waiting)

Open a terminal (Windows: press the Windows key, type `terminal`, Enter; macOS: Cmd+Space, type `terminal`, Enter).

1. **Package manager.**
   - Windows: run `winget --version`. If it is not recognised, install **App Installer** from the Microsoft Store, then open a new terminal window.
   - macOS: install Homebrew, then run the shell setup lines it prints at the end:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
2. **Git and the GitHub CLI.**

   | Windows | macOS |
   |---|---|
   | `winget install --id Git.Git -e --source winget` | `brew install git` |
   | `winget install --id GitHub.cli --source winget` | `brew install gh` |
   | **Close the terminal and open a new window.** | |

3. **Your name and email** (the email on your GitHub account, or its private noreply address):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
4. **Sign in:** `gh auth login` → **GitHub.com** → **HTTPS** → **Yes** (authenticate Git) → **Login with a web browser** → paste the one-time code in the browser.
5. **Prove it.** The setup check ships with the course. Until you have cloned the course (Step 3), download just the script for your system from GitHub — open it in the browser, choose **Raw**, save it into your home folder — then run it from there:

   | Windows | macOS |
   |---|---|
   | `powershell -ExecutionPolicy Bypass -File .\check-setup.ps1` | `bash check-setup.sh` |

   The scripts are `course/03-content/m09-github-pages/setup/check-setup.ps1` and `course/03-content/m09-github-pages/setup/check-setup.sh` in `github.com/tomqwu/ai_courses`. Fix the first FAIL it names, open a new terminal, and run it again until it prints **4 of 4 checks passed**.

**Paste:** the final check output, and every FAIL you hit on the way with the command that fixed it.

## Step 2 — Find your way around (~5 min)

```bash
cd ~
mkdir code
cd code
pwd
ls
```

`pwd` should print your home folder followed by `code` — `/Users/<you>/code` on a Mac, `C:\Users\<you>\code` on Windows. `ls` prints nothing yet: the folder is empty. If `mkdir` says the folder already exists, that is fine; carry on.

**Paste:** the output of `pwd`.

## Step 3 — Clone the course, and find the starter (~5 min)

Still in `code`:

```bash
gh repo clone tomqwu/ai_courses
cd ai_courses/course/03-content/m09-github-pages/catalog-starter
ls
```

`ls` lists `README.md`, `app.js`, `index.html`, `products.js` and `styles.css`. The fifth file, `.nojekyll`, is hidden because its name starts with a dot: `ls -a` on a Mac or `ls -Force` in PowerShell shows it.

Now go back to `code`. Any one of these works, which is the point of Segment M9.2:

```bash
cd ../../../../..     # up five levels: one for each folder you went into
cd ~/code             # straight there from anywhere, using the home shortcut
```

Run `pwd` afterwards to prove where you landed.

**Paste:** the `ls` output from the starter folder.

## Step 4 — Create your own repository (~5 min)

From `code`:

```bash
gh repo create my-catalog --public --add-readme --clone --description "My product catalog"
cd my-catalog
git status
```

`--add-readme` gives the new repository a first commit on a branch called `main`, so the clone starts on `main` and `git push` knows where to go later. `git status` says **On branch main** and **nothing to commit, working tree clean**.

Copy the starter in — including the hidden `.nojekyll` — from inside `my-catalog`:

| Windows | macOS |
|---|---|
| `Copy-Item -Recurse -Force ..\ai_courses\course\03-content\m09-github-pages\catalog-starter\* .` | `cp -R ../ai_courses/course/03-content/m09-github-pages/catalog-starter/. .` |

Both forms copy the hidden `.nojekyll` too: `-Force` does it in PowerShell, and the trailing `/.` does it on a Mac. Run `git status` again. It should show `README.md` as **modified** — the starter's README replaced the one GitHub made — and `.nojekyll`, `app.js`, `index.html`, `products.js`, `styles.css` as **untracked**. If `.nojekyll` is missing from that list, the copy left out `-Force` or the `/.`; run it again as written.

**Paste:** this `git status` output.

## Step 5 — Make it yours and preview it (~15 min)

1. Open `products.js` in any text editor (Notepad or TextEdit is fine; if you use TextEdit, choose **Format → Make Plain Text** first).
2. Change `store.name`, `store.tagline` and `store.contact` (your email as `mailto:you@example.com`).
3. Replace the sample products with **at least three of your own**. Keep the commas between blocks.
4. In `index.html`, change the `description` line near the top to one sentence about your products.
5. Preview:

   | Windows | macOS |
   |---|---|
   | `start index.html` | `open index.html` |

   Your products appear with a category button for each category you used. If the page says **products.js did not load**, a comma or quote is missing: the browser's developer console (F12 on Windows, Cmd+Option+I on a Mac) names the line.

**Paste:** a screenshot of the preview, and one line saying where each product's button points — a `buyUrl` to a checkout you run elsewhere, or "Ask about this" for now.

## Step 6 — Commit and push (~5 min)

```bash
git status
git add .
git commit -m "Add my catalog"
git push
git log --oneline -2
git status
```

`git commit` prints a line starting `[main` with a short code and the number of files changed. `git push` ends with a line like `699905a..c02f59f  main -> main`. The last `git status` says **nothing to commit, working tree clean** — the proof that everything went.

**Paste:** the output of `git log --oneline -2` and the last `git status`.

## Step 7 — Publish with GitHub Pages (~10 min, including the wait)

1. Open your repository on GitHub: `gh repo view --web` opens it in your browser.
2. **Settings** → **Pages** (left column).
3. Under **Build and deployment**, **Source**: **Deploy from a branch**. Branch: `main`. Folder: `/ (root)`. **Save**.
4. Wait. It can take up to 10 minutes. The **Actions** tab shows a run called **pages build and deployment**; when it is green, the Pages settings show **Visit site** with your address.
5. Open `https://<your-username>.github.io/my-catalog/` on your computer **and** on your phone.

**Paste:** the address, and a screenshot of the published page on your phone.

## Step 8 — Change it and watch it republish (~10 min)

Change one product's price in `products.js`. Preview it, then run the Step 6 loop with a message that says what changed, for example `git commit -m "Lower the mug price to 30"`. Watch the **Actions** tab run again, then reload the published page.

**Paste:** the new `git log --oneline -1` and the time between your push and the new price appearing.

## Acceptance checklist (binary — pass = every box checked)

1. ☐ The setup check prints **4 of 4 checks passed**, pasted in full.
2. ☐ `pwd` output shows your `code` folder inside your home folder.
3. ☐ `my-catalog` exists on GitHub as a **public** repository you created from the terminal.
4. ☐ `git status` before your first commit lists `.nojekyll`, `app.js`, `index.html`, `products.js` and `styles.css`.
5. ☐ `products.js` holds at least three of your own products; none of the six samples remain.
6. ☐ Every product's button points to a checkout hosted outside GitHub Pages, or reads "Ask about this" — there is no cart or payment form on the page.
7. ☐ The published address opens on a phone and shows your products.
8. ☐ Step 8's change is visible on the published page, with its commit in `git log`.

## Evidence to record

`evidence.md` holds, in order: your GitHub username; the setup check output and every failure you fixed; `pwd`; the starter `ls`; `git status` before the first commit; the preview screenshot and button destinations; `git log --oneline -2`; the published address and the phone screenshot; the Step 8 commit and how long it took to appear. Commit `evidence.md` into `my-catalog` as well — it is the first entry in the habit the rest of this course is built on: a claim is only as good as the record behind it.

## Stretch (optional, ~30 min)

- Add real photos: an `images` folder, `image: "images/your-file.jpg"` per product, each under about 500 KB.
- Give one product a `buyUrl` that goes to a payment link from a payment provider or a marketplace listing, and test it from your phone.
- Read AI × QE's publishing workflow (`ai_qe/.github/workflows/pages.yml`) and list, in plain words, three checks it runs before it deploys that your branch-published catalog does not.

## Discussion prompt

Post your catalog's address and the one setup step that took longest, with the line that fixed it. Reply to one classmate with the first thing you tried to tap on their catalog that did not do what you expected.
