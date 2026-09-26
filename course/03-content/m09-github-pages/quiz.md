# Quiz M9 — Ship a Product Catalog with GitHub Pages

> 8 questions (6 multiple choice, 2 short answer) · Answer key below · References lesson segments M9.1–M9.3

## Questions

**Q1 (MC).** On Windows you just ran `winget install --id GitHub.cli --source winget` and it reported success. In the same terminal window, `gh --version` says the command is not recognised. What is the right next move?

- a) Uninstall and reinstall the GitHub CLI
- b) Close that terminal and open a new window, then run `gh --version` again
- c) Switch from PowerShell to Command Prompt
- d) Install the CLI with Homebrew instead

**Q2 (MC).** Your setup check prints three PASS lines and one FAIL: "git does not know your name and email yet". What does that FAIL actually stop you doing?

- a) Cloning any repository
- b) Signing in to GitHub with `gh auth login`
- c) Making a commit, because every commit records a name and an email
- d) Opening `index.html` in a browser

**Q3 (MC).** You open a terminal, run `gh repo clone tomqwu/ai_courses`, then look in your `code` folder and the project is not there. What most likely happened?

- a) The clone failed silently
- b) You were not in `code` when you ran it, so the new folder was made wherever the terminal was — usually your home folder
- c) Cloned repositories are hidden until you run `git status`
- d) `gh repo clone` only downloads a zip file

**Q4 (MC).** After editing `products.js`, you run `git add .` and `git commit -m "Add my products"`, but the published site still shows the old products twenty minutes later. `git status` says "Your branch is ahead of 'origin/main' by 1 commit." What is missing?

- a) `git push` — the commit exists only on your computer until you push it
- b) Nothing; GitHub Pages can take up to a day
- c) The `.nojekyll` file
- d) Re-saving the Pages settings

**Q5 (MC).** Why does the starter keep its products in `products.js` rather than in a `products.json` file?

- a) JSON cannot hold prices
- b) GitHub Pages does not publish `.json` files
- c) A browser will not let a page opened from your disk read a separate data file, but it will run a script loaded with a `<script>` tag — so the preview works with a double-click and no server
- d) JavaScript loads faster than JSON

**Q6 (MC).** A friend wants to add a shopping cart and card payments to their GitHub Pages catalog so customers can pay without leaving the page. What does GitHub's own limits page say about that?

- a) It is allowed on a paid plan
- b) It is allowed if the site stays under 1 GB
- c) Pages is not allowed to be used as free hosting for an online business or e-commerce site, or any site primarily for commercial transactions — so the catalog should link out to a checkout hosted elsewhere
- d) It is allowed as long as the repository is public

**Q7 (Short answer).** A classmate on a Mac pastes this: "I ran the Homebrew install line, it finished, and now `brew install gh` says `command not found: brew`." Write the reply you would post: the most likely cause, the fix, and how they can prove the whole setup is ready afterwards without guessing.

**Q8 (Short answer).** Your catalog is live. A shop owner asks you to add their products and publish them the same day, and mentions they will want to take card payments "later". Describe the change you would make to `products.js` for one product, the four-command loop you would run to publish it, how you would confirm it went live, and what you would tell them about payments.

## Answer key

**A1: b.** Installing a tool changes where the terminal looks for commands, and a window that was already open does not see the change. The GitHub CLI's own Windows instructions say to open a new terminal window — not just a new tab — after installing. (a) wastes time on an install that worked; (c) has the same problem, because it is still an old window; (d) is the macOS package manager. *Ref: M9.1 — `github.com/cli/cli`, `docs/install_windows.md`; `course/03-content/m09-github-pages/setup/check-setup.ps1`.*

**A2: c.** Git stamps every commit with a name and an email and refuses to commit without them. Cloning, signing in and previewing all work without an identity, which is why the check tests it on its own line. The fix is the two `git config --global` lines the check prints. *Ref: M9.1 — `course/03-content/m09-github-pages/setup/check-setup.sh`.*

**A3: b.** A clone makes a new folder inside whatever folder the terminal is in. The terminal opens in your home folder, so a clone typed straight away lands there, not in `code`. Run `pwd` before cloning, or `cd ~/code` first. (a) is possible but would print an error; (c) and (d) are false. *Ref: M9.2.*

**A4: a.** `commit` saves a version on your computer; `push` sends it to GitHub, and Pages publishes only what is on GitHub. "Ahead of 'origin/main' by 1 commit" is Git saying exactly that. Publishing can take up to 10 minutes after a push, so (b) is wrong on the time and on the cause. (c) affects how the site is built, not whether your commit arrived. *Ref: M9.2, M9.3 — `github.com/github/docs`, `data/reusables/pages/twenty-minutes-to-publish.md`.*

**A5: c.** The design choice is about the preview: a browser blocks a page opened from disk from fetching a separate file, but it runs scripts loaded with a tag. Keeping the data in a script means the double-clicked preview and the published page are the same files with no step in between. AI × QE makes the same separation of data from layout at larger scale, with a data file its template loops over. *Ref: M9.3 — `course/03-content/m09-github-pages/catalog-starter/products.js`, `ai_qe/CONTRIBUTING.md:23`.*

**A6: c.** GitHub Pages "is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service". The plan, the size limit and the visibility do not change that. A catalog that describes products and links to a checkout run elsewhere is the shape Pages allows, which is why the starter has `buyUrl` and no cart. *Ref: M9.3 — `github.com/github/docs`, `content/pages/getting-started-with-github-pages/github-pages-limits.md`.*

**A7.** A strong reply names the cause: the Homebrew installer ends by printing a few lines of shell setup instructions that add `brew` to the terminal, and they were skipped — on Apple silicon Macs Homebrew lives in `/opt/homebrew`, which the terminal does not search until those lines run. The fix is to scroll back, copy those lines exactly, run them, and open a new terminal window. The proof is not "`brew` works now" but the setup check: `bash check-setup.sh` until it prints **4 of 4 checks passed**, pasted into the evidence log, because it tests Git, the CLI, the identity and the sign-in in one run. Accept any reply that gives a cause, a fix and a check that runs; reject "reinstall everything" with no cause. *Ref: M9.1 — `github.com/Homebrew/install`, README; `course/03-content/m09-github-pages/setup/check-setup.sh`.*

**A8.** A strong answer covers four things. **The change**: one block in `products.js` with `id`, `name`, `category`, `price` as a number and `summary`, commas intact, and either a `buyUrl` to a checkout the owner runs elsewhere or no `buyUrl`, so the button reads "Ask about this". **The loop**: `git status`, `git add .`, `git commit -m` with a message that says what changed, `git push` — then `git status` showing a clean tree. **Confirming it**: the Actions tab's pages build and deployment run turns green, then the live address shows the product, allowing up to 10 minutes. **Payments**: Pages may not host an online shop, so payments stay on a checkout hosted elsewhere and the catalog links to it — say this before they build around a cart. Mark down answers that preview only locally and call it published, or that promise payments on the page. *Ref: M9.2, M9.3 — `github.com/github/docs`, `content/pages/getting-started-with-github-pages/github-pages-limits.md`.*

## Objective → assessment map

Every "By the end of this module you can" line in `course/03-content/m09-github-pages/lesson.md`, and what checks it.

| Objective (lesson.md) | Checked by |
|---|---|
| **Install** Git and the GitHub CLI on Windows or macOS, sign in, and prove the setup with a script | Q1, Q2, Q7; Lab M9 Step 1, checklist item 1 |
| **Move** around folders from the terminal | Q3; Lab M9 Steps 2–3, checklist item 2 |
| **Clone**, change and send back with status → add → commit → push | Q3, Q4, Q8; Lab M9 Steps 4 and 6, checklist items 3–4 |
| **Publish** a static site with GitHub Pages from a branch and find its address | Q4, Q5, Q8; Lab M9 Steps 5, 7 and 8, checklist items 5, 7 and 8 |
| **State** what GitHub Pages is for and what it is not | Q6, Q8; Lab M9 Step 5, checklist item 6 |
