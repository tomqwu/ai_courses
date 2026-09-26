# Lab Rubrics — Lab M9: Publish your product catalog

> Lab M9 is free and standalone, so it sits outside the certificate's eight graded labs
> (`course/06-production/certificate.md`). It is graded the same way anyway, because the habit it
> builds — a claim is only as good as the record behind it — is the one every later lab assumes.
> Cohort students are reviewed by the instructor; self-paced students check themselves against these
> tables and post the address for one peer review. **Pass = ≥80 total, no criterion scored Missing,
> and no auto-fail condition present.** Weights sum to 100 across the three tables.

## Table A — Tools installed and proven (Lab M9 Steps 0–2) · 30 points

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Setup check at 4 of 4 | 15 | Full output pasted, ending **4 of 4 checks passed**, run after the last fix | 4 of 4 pasted, but no record of any earlier run | Output pasted at 3 of 4 with the fix named but not re-run | No output, or output retyped rather than pasted | `evidence.md`, setup section |
| Failures kept, with fixes | 10 | Every FAIL hit on the way is pasted with the exact line that fixed it | Failures described in words with the fix | Mentions a problem without the fix | Claims nothing went wrong while the output shows an earlier FAIL | `evidence.md` |
| Knows where they are | 5 | `pwd` shows `code` inside the home folder, and the starter `ls` is pasted from the right folder | `pwd` correct, `ls` missing | `pwd` shows a different folder, noticed and explained | No `pwd` | `evidence.md` |

## Table B — Repository and the loop (Steps 3–4, 6) · 35 points

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Public repository created from the terminal | 10 | `my-catalog` exists, public, with a first commit from `--add-readme` | Exists and public; created in the browser instead | Exists but private, so Pages needs a paid plan | No repository | The repository address |
| Starter copied whole | 10 | Pre-commit `git status` lists `.nojekyll`, `app.js`, `index.html`, `products.js`, `styles.css` and a modified `README.md` | All five present; `README.md` untouched because it was deleted first | `.nojekyll` missing | Files typed in by hand or pasted from the browser | `git status` output |
| The loop, with its proof | 15 | `git log --oneline -2` shows the learner's commit on top of the initial one, and the final `git status` says **working tree clean** | Both pasted; the commit message says nothing about what changed | Commit present but never pushed | No commit | `git log`, final `git status` |

## Table C — The published catalog (Steps 5, 7–8) · 35 points

| Criterion | Wt | Exemplary | Proficient | Developing | Missing | Evidence required |
|---|---|---|---|---|---|---|
| Their products, not the samples | 10 | ≥3 real products; store name, tagline and contact changed; description line in `index.html` changed | ≥3 products, but one sample remains or the contact is still the example address | Fewer than 3 products | The six samples, unchanged | Live page, `products.js` |
| Live on a phone | 10 | Address pasted; phone screenshot shows the learner's products | Address works; screenshot from a desktop | Pages enabled but the site returns 404, with the cause identified | No address | Address, screenshot |
| Republished after a change | 10 | Step 8 commit in `git log`, change visible live, and the time to appear recorded | Change visible, time not recorded | Change pushed but not yet visible, and the Actions run named | No second change | `git log --oneline -1`, live page |
| A catalog, not a shop | 5 | Every button is a `buyUrl` to a checkout run elsewhere, or "Ask about this"; destinations listed in the evidence | Buttons correct, destinations not listed | A `buyUrl` points back into the catalog itself | A cart or payment form on the page | Live page, `evidence.md` |

## Auto-fail conditions

Any one of these fails the lab regardless of score:

1. **Fabricated output** — setup check, `git status` or `git log` output that was retyped, edited, or does not match the repository on GitHub.
2. **Someone else's catalog** — a published address that is not the learner's own repository.
3. **Payments on the page** — a cart, a card form or any payment collection on the GitHub Pages site. GitHub's own terms forbid using Pages to run an online business or e-commerce site (`github.com/github/docs`, `content/pages/getting-started-with-github-pages/github-pages-limits.md`).
4. **Secrets committed** — a password, token or private key anywhere in the repository or its history.

## How to distinguish a real pass from a plausible fake

- **The short codes line up.** The commit code in the pasted `git log` must appear on the repository's commits page on GitHub. Retyped output rarely survives that check.
- **The setup check is the machine's, not the reader's.** A real run prints the learner's own GitHub username on the fourth line. A pasted example from the lesson prints someone else's.
- **The Actions tab keeps time.** The pages build and deployment runs show when each push published. A Step 8 time that is shorter than the run's own duration was not measured.
- **Failures are normal.** An evidence file with no failure at all, from someone who started with nothing installed, is worth one follow-up question: which terminal window did you install from, and which did you run the check in?
