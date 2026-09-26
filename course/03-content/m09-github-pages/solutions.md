# Solutions — Lab M9: Publish your product catalog

> Reference answers per step, with the output a correct run produces, the wrong answers seen most
> often, and a grading note. The local outputs below were produced for real: the starter was copied
> into a clone and committed, and both setup checks were run, the Windows one under PowerShell 7.5.
> Your short codes, paths and version numbers will differ; the shape will not.

## Step 1 — Tools installed and proven

**Reference.** The check prints four PASS lines and **4 of 4 checks passed**, then exits 0. On the way
most learners see at least one FAIL. This is the real Windows output from a machine with Git but no
GitHub CLI and no sign-in:

```text
Lab M9 setup check - Windows

PASS  git is installed: git version 2.43.0
FAIL  GitHub CLI (gh) is not installed
      fix: winget install --id GitHub.cli --source winget   then open a NEW terminal window
PASS  git knows who you are: Ada Example <ada@example.com>
FAIL  not signed in to GitHub from the terminal
      fix: gh auth login   (choose GitHub.com, HTTPS, yes to git credentials, log in with a web browser)

2 of 4 checks passed.
```

On a Mac with no Homebrew, the GitHub CLI line's fix starts with Homebrew's own install line, then
`brew install gh`. With Homebrew present it is just `brew install gh`.

**Common wrong answers.**
- *"I installed it but the check still says FAIL."* The check ran in the window that was open during
  the install. Open a new window, not a tab; the CLI's own Windows instructions say the same.
- *`brew: command not found` right after installing Homebrew.* The shell setup lines Homebrew printed
  at the end were skipped. Scroll back, run them, open a new window.
- *Retyping the output.* Paste it. A retyped check is the first auto-fail.

**Grading note.** Full marks need the final 4 of 4 *and* the failures along the way. A learner who
started with nothing installed and records no failure gets one question, not a deduction.

## Step 2 — Find your way around

**Reference.** `pwd` prints `/Users/<you>/code` on a Mac and, under a `Path` heading,
`C:\Users\<you>\code` on Windows. `ls` prints nothing: the folder is new.

**Common wrong answers.** `mkdir` complaining the folder exists is not an error worth fixing — carry on.
A `pwd` that ends in `Documents\code` is fine if the learner says so; the rubric wants them to know
where they are, not to be in one particular place.

## Step 3 — Clone the course

**Reference.** In the starter folder, `ls` shows `README.md`, `app.js`, `index.html`, `products.js`
and `styles.css`. `.nojekyll` appears only with `ls -a` on a Mac or `ls -Force` in PowerShell.
`cd ../../../../..` from the starter lands back in `code` — five levels, one per folder entered.

**Common wrong answers.** Cloning from the home folder, then "the repository is not in code". Nothing
failed; the clone is in the home folder. `pwd` before cloning prevents it.

## Step 4 — Your own repository

**Reference.** After `gh repo create my-catalog --public --add-readme --clone`, `git status` says
**On branch main** and **nothing to commit, working tree clean**. After copying the starter:

```text
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
```

Both copy commands include the hidden `.nojekyll`: `Copy-Item -Recurse -Force …\*` in PowerShell and
`cp -R …/catalog-starter/. .` on a Mac. Each was run and the result listed to confirm it.

**Common wrong answers.**
- *No `--add-readme`.* The repository starts empty and the local branch may be named `master`, so the
  first `git push` has nowhere obvious to go. Recreate with the flag, or `git push -u origin HEAD:main`.
- *`.nojekyll` missing.* The copy left out `-Force` or the trailing `/.`. The site still publishes, but
  through Jekyll, and a later file whose name starts with an underscore silently disappears.

## Step 5 — Make it yours

**Reference.** At least three products with `id`, `name`, `category`, a numeric `price` and a
`summary`; one category button per category used; the preview opens by double-click. The starter was
checked in a headless browser opened from disk: six products, filters, search and sort working, no
sideways scroll at phone width, no console errors, WCAG AA contrast in light and dark mode.

**Common wrong answers.** *"products.js did not load."* A missing comma between two product blocks,
or a quote opened and never closed. The browser console (F12, or Cmd+Option+I) names the line.
*A price written as `"$32"`.* It must be the number `32`; the page formats it.

## Step 6 — Commit and push

**Reference** (real output on the starter):

```text
$ git commit -m "Add the catalog starter"
[main c02f59f] Add the catalog starter
 6 files changed, 497 insertions(+), 1 deletion(-)
$ git push
   699905a..c02f59f  main -> main
$ git log --oneline -2
c02f59f Add the catalog starter
699905a Initial commit
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Common wrong answers.** *"Your branch is ahead of 'origin/main' by 1 commit"* — committed, never
pushed. Run `git push`.

## Steps 7–8 — Publish, then republish

**Reference.** Settings → Pages → Deploy from a branch → `main`, `/ (root)` → Save. The Actions tab
shows **pages build and deployment**; the address is `https://<username>.github.io/my-catalog/`. GitHub
says a change can take up to 10 minutes to publish. Step 8's second push starts a second run.

**Common wrong answers.**
- *404 at the address.* Usually the folder was set to `/docs`, which does not exist here, or the first
  run is still going.
- *A private repository.* Pages on a private repository needs a paid plan; make it public.

## Self-check

| Your evidence says | You are done when |
|---|---|
| Setup check | it ends **4 of 4 checks passed** |
| `git status` before committing | `.nojekyll` and four other files are listed |
| `git log --oneline -2` | your commit sits on top of the initial one |
| The address | it opens on your phone and shows your products |
| Every button | it goes to a checkout elsewhere, or says "Ask about this" |
