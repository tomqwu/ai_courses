# Evidence-Cited Briefing

Buyers of expertise have sat through decks that promise large gains and cite nothing they can check. This playbook is for consultants, analysts, domain experts and founders who sell what they know as a briefing, a deck or a report. When you finish, you will have a dated research log that admits what you could not verify, a benchmark record behind every source, a provenance table in which every number carries a source, a saving level and an epistemic label, audience routes over one slide set that each end on a decision, an edition policy with a signed claim manifest, and a script that fails your briefing if any number appears without its source.

## The method

1. **Log research before you publish it.** Keep one log, newest first. Each dated entry records the Question, what was Checked, the Outcome and what Changed on the page, and you add the entry before you edit a page (`ai_qe/docs/research-log.md:11`). Give the log a Not verified list and an Open questions list. Research you cannot verify goes on the list, not on the slide.

2. **Write a benchmark record for every source.** A link is not a record. "Every benchmark record includes date, sample, method, unit, self-reported vs measured, sponsor, and what claim it can support. Anything unverifiable is listed as such." (`ai_qe/CONTRIBUTING.md:93-94`). Add the caveats. Records keep two real results apart when a deck would average them. One independent trial found work took longer with assistance, while a vendor-affiliated study of a single synthetic task found it faster (`ai_qe/docs/evidence/benchmarks.md:31-42`, `ai_qe/docs/evidence/benchmarks.md:97-108`). Both are measured, and neither is a budget number.

3. **Record every retrieval, including the ones that failed.** For each source keep an ID, URL, retrieval date, status, and for a downloaded file its SHA-256. When a download fails, record `"status": "unavailable"` and the reason. A manifest with an honest failure in it is evidence the manifest is real.

4. **Label every number with one saving level, and never mix levels.** Four levels, each with the party who can confirm it (adapted from `ai_qe/docs/principles.md:52-61`, whose capacity and spend rows name QA specifically):

   | Level | What it measures | Who can confirm it |
   |---|---|---|
   | Task-level efficiency | Net time reduction for one activity, after review, correction and control effort | Pilot measurement |
   | Released capacity | Reduction in human hours across the full workflow, after adoption and eligibility | Pilot measurement plus baseline time capture |
   | Hard-dollar saving | Budgeted cost Finance can actually remove or avoid | Finance, against a named budget line |
   | Total-spend impact | Broader engineering or delivery cost; never mislabel it as the narrower saving | Finance and the CIO office |

   "Mixing them is the most common error in AI business cases." (`ai_qe/docs/principles.md:54`). Task gains dilute: when coding is a small share of total time, "A 50% task gain on coding dilutes to single digits of total engineering time" (`ai_qe/docs/evidence/reading-the-evidence.md:34`).

5. **Add an epistemic label to every number.** Use measured, self-reported, vendor-affiliated or illustrative, and add negative or inconclusive where true. Put the label on the slide itself, not in a footnote. Write one qualifier sentence that a skimming reader cannot miss. The model is "Planning inputs and proposed outcomes are not observed client results." (`ai_qe/README.md:9`).

6. **Build the provenance table, then cite rows from the slides.** One row per claim: the exact slide wording, the source (a URL, or a file path with a line number), the retrieval date, the level and the label. Every quantitative slide names the row it rests on. A number with no row is an orphan; cite it or cut it.

7. **Cut routes over one slide set, and end each route on a decision.** Give every slide a stable ID. A route is an ordered list of IDs plus a closing slide. It reorders and omits and never rewrites, so every shared link still resolves. "Focused routes end on a decision discussion; full decks retain the supporting material." (`ai_qe/README.md:7`). Make the ask decidable: "The decision today is whether to fund the first two phases, not whether to transform QA." (`ai_qe/docs/economics/slide-language.md:39`).

8. **Release in editions, and never overwrite one.** Version the site separately from the content. Each changelog entry states what changed and what was deliberately retained. "An existing published edition is never overwritten" (`ai_qe/CONTRIBUTING.md:110`). Keep superseded editions downloadable.

9. **Publish for the AI engines that read you first, and sign the edition.** Put each statistic and its source in the same sentence. Quote people and studies by name, not "research shows". Give every claim a permalink per edition. Write a crawler policy on purpose: allow or refuse each AI crawler by the user-agent token its vendor documents, and look the token up on the vendor's page the day you write the rule. Being cited and being used for training are separate decisions. Build a machine-readable claim manifest, sign it, and let readers verify it. The reason: engines misattribute often, and a reader holding a link to claim 3 of edition 1.0.0 can check what you actually said.

10. **Publish your own audit.** List your findings with severity and evidence, then a table mapping each finding to its fix and its verification. Keep the refusals too, the changes you deliberately will not make.

## Template

**Research log entry.**

```markdown
## 2026-10-02 · <topic>
**Question.** <the claim you were asked to support>
**Checked.** <sources read, with dates>
**Outcome.** <what the evidence supports, and what it does not>
**Not verified.** <what you looked for and could not confirm>
**Changed.** <the page, slide or row this entry altered>
```

**Benchmark record.**

```markdown
### <Author or organisation>, "<title>", <publication date> — <URL>
**Finding:** <the number, its unit and its interval>
**Supports:** <one saving level, and its direction: positive / negative / inconclusive>
**Caveats:** <who, what task, what it cannot generalise to>
- **Sample and method:** <n, population, design>
- **Metric and denominator:** <what was measured, per what>
- **Measured or self-reported; sponsor:** <label>; <who paid or published>
```

**Retrieval manifest.**

```json
[
  {"id": "S01", "url": "https://…", "retrieved": "2026-10-02", "status": "downloaded",
   "local_path": "research/downloads/S01.pdf", "sha256": "<hex>"},
  {"id": "S02", "url": "https://…", "retrieved": "2026-10-02", "status": "unavailable",
   "reason": "The read operation timed out"}
]
```

**Provenance table.** Keep these headers; the manifest script reads them.

```markdown
| # | Claim (exact slide wording) | Source | Retrieved | Level | Epistemic label |
|---|---|---|---|---|---|
| 1 | "<number and unit, as on the slide>" | https://… or `repo/path.md:31` | 2026-10-02 | Task-level, negative | Measured, independent |
```

**Route declaration.**

```yaml
full_order: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
executive:
  slides: [1, 3, 6, 9, 11, 12]            # the strategic cut
  closing: 12                              # the decision-ask slide
technical:
  slides: [1, 3, 4, 5, 7, 8, 10, 9, 11, 12] # keeps the evidence the executive route skips
  closing: 12
```

**Edition decision record.**

```markdown
## Edition 1.1.0 · 2026-10-16
Changed: slide 3 adds the follow-up study (provenance row 2).
Deliberately retained: audio, caption timing, the 1.0.0 PDF edition.
Bumps: content edition 1.0.0 → 1.1.0; site version with it. Questionnaire edition unchanged.
Manifest: manifest-1.1.0.json, signed. manifest-1.0.0.json stays published and unedited.
```

**Crawler policy skeleton.** Fill each token from the vendor's own documentation on the day you write it.

```text
User-agent: <search/citation crawler token, from the vendor's page>
Allow: /
User-agent: <training crawler token, from the vendor's page>
Disallow: /
```

## Checklist

- [ ] The research log is dated, newest first, and every entry has Question, Checked, Outcome and Changed.
- [ ] At least two entries record something you could not verify.
- [ ] Every source has a benchmark record with date, sample, method, unit, measured or self-reported, sponsor and what it supports.
- [ ] The retrieval manifest records every attempt, including failures with a reason.
- [ ] Every provenance row has a source URL or path with line, an ISO retrieval date, a level and a label.
- [ ] No row claims a higher saving level than its evidence supports.
- [ ] Every quantitative slide cites a row and shows its epistemic label on the slide.
- [ ] Every illustrative number says "illustrative" on the slide itself.
- [ ] Each route uses stable slide IDs, only reorders or omits, and closes on a decidable ask.
- [ ] The site version and the content editions are separate fields.
- [ ] No published edition was edited; the new one has its own number, manifest and signature.
- [ ] `selfcheck.py` exits 0 on the briefing, and `edition_manifest.py verify` reports a good signature.

## Worked example from a real repo

AI × QE (`ai_qe`, commit 6388f0a) is a research-backed briefing site on quality engineering in regulated financial services.

- **Benchmark records.** The METR record gives the finding "AI-allowed issues took 19% longer (CI +2% to +39%)", supports "Task efficiency (negative)", and records the sample, the metric and "Measured (screen recording); independent non-profit" (`ai_qe/docs/evidence/benchmarks.md:31-42`). The Peng record gives "55.8% faster (71.2 vs 160.9 minutes; CI 21% to 89%)" on one synthetic task, "Measured; vendor-affiliated" (`ai_qe/docs/evidence/benchmarks.md:97-108`).
- **The log and its admissions.** The initial evidence entry concludes that "the only independent RCT is negative" and lists what was not verified, including "any Gartner AI-testing productivity figure" (`ai_qe/docs/research-log.md:114-122`). Open questions follow (`ai_qe/docs/research-log.md:144-151`). The log also shows why the ordering rule needs checking. A 9 September entry sits after the open questions, below entries dated 4 September, without the four-part structure (`ai_qe/docs/research-log.md:153-155`). A date sort over the headings would catch it.
- **An honest failure.** The retrieval manifest records one source as `"status": "unavailable"`, reason "The read operation timed out" (`ai_qe/research/document-manifest.json:2-8`). The next record shows a successful download with its size and SHA-256 (`ai_qe/research/document-manifest.json:9-18`).
- **Levels and wording.** The site's use-and-avoid lists turn the levels into slide language. Use "Working hypothesis, to be tested on the bank's own data" and "Capacity released is not a saving until Finance confirms how it is captured" (`ai_qe/docs/economics/slide-language.md:15-17`). Avoid "Industry benchmarks show 30-50% productivity gains" (`ai_qe/docs/economics/slide-language.md:26`).
- **Routes.** The banking executive route plays 14 of the deck's 21 slides and declares slide 12 its closing (`ai_qe/_data/briefing_routes.json:2-22`, `ai_qe/_data/briefing_room.json:12`).
- **Editions.** `ai_qe/_data/release.yml:1-7` keeps the site at version 1.24.1 while the slide edition stays 1.24.0. The changelog says why: "Audio, subtitle timing, and the v1.24.0 PDF editions remain unchanged" (`ai_qe/releases.md:10`). Superseded editions stay in immutable releases (`ai_qe/releases.md:16`).
- **Its own audit.** The site publishes an audit of itself with 14 findings, four of them high priority (`ai_qe/research/reviews/site-audit-2026-09-06.md:7`). A remediation table maps each finding to a response and a verification (`ai_qe/research/reviews/remediation-2026-09-06.md:5-8`). A later record lists refusals: "Do not hide weak economics, convert capacity to cash, or relabel unknown results as observed" (`ai_qe/research/reviews/review-56-resolution-2026-09-10.md:20`).

**Why publishing for AI engines matters.** The evidence is recorded secondhand, and it was not re-read for this playbook. A randomized field experiment with 1,065 Chrome users found organic clicks fell 39.8% when an AI Overview appeared (via PPC Land, https://ppc.land/researchers-find-google-ai-overviews-cut-publisher-clicks-39-8/). Ahrefs, in its own vendor analysis, associates AI Overviews with a 58% lower click-through rate for top-ranking pages (via TNW, https://thenextweb.com/news/google-ai-overviews-publisher-links-search-traffic). The Tow Center found that over 60% of 1,600 queries across eight AI search engines failed to identify the source correctly (via Nieman Lab, https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/). Treat `llms.txt` as speculative: a secondary report quotes Google's John Mueller saying no major AI service uses it, and an Ahrefs crawl finding 97% of such files receive zero requests (https://llmpulse.ai/blog/geo-guide/).

## Self-check

Two scripts live in the AI Product Studio course repository at `course/03-content/m06-expertise-product/`: `selfcheck.py`, with its fixtures in `selfcheck-examples/`, and `edition_manifest.py`. Both use only the standard library and need Python 3.11, and `sign` and `verify` also need OpenSSH 8.1 or later, which `ssh -V` reports [source: the docstrings of both scripts]. Run both self-tests first, from that folder. The output is verbatim [source: the author's run on 2026-09-26]:

```text
$ python3 selfcheck.py --selftest
[PASS] good.md: 0 uncited claim(s), expected 0
[PASS] bad.md: flagged lines [13, 14, 22, 27, 30, 32], expected [13, 14, 22, 27, 30, 32]
    line 13: 55.8%, 71.2, 160.9 minutes, 2026-09-04
    line 14: 47.6%, 2026-09-04
    line 22: 55.8%
    line 27: 10, 15%
    line 30: $450k
    line 32: 3.3x
Full report: selfcheck.py selfcheck-examples/bad.md

SELFTEST: PASS

$ python3 edition_manifest.py --selftest
[PASS] build good.md: 6 claims, same bytes twice
[PASS] check good.md against its own edition: no changes
[PASS] one number edited: ['claim-1: changed (claim)']
[PASS] hand-edited manifest: refused
[PASS] build bad.md: refused ['claim-2', 'claim-3']
[PASS] signature: verifies as issued, fails once the manifest changes

SELFTEST: PASS
```

Both exit 0. Then run them on your own briefing, saved as one Markdown file. The output below is from the passing fixture, copied into a scratch folder on the same day (key path and fingerprint shortened, `ssh-keygen`'s own progress lines omitted):

```text
$ python3 selfcheck.py briefing.md
PASS: 0 uncited quantitative claims in 1 file(s)
$ python3 edition_manifest.py build briefing.md --edition 1.0.0 --base-url https://example.org/briefing/1.0.0
wrote manifest-1.0.0.json: edition 1.0.0, 6 claims, claims_sha256 981261345407
$ ssh-keygen -t ed25519 -f "$HOME/edition_key" -C you@example.com
$ python3 edition_manifest.py sign manifest-1.0.0.json --key "$HOME/edition_key" --signer you@example.com
wrote allowed_signers: you@example.com is the one allowed signer
$ python3 edition_manifest.py verify manifest-1.0.0.json --signer you@example.com --allowed-signers allowed_signers
Good "aps-edition" signature for you@example.com with ED25519 key SHA256:…
# edit one number in the briefing, then:
$ python3 edition_manifest.py check briefing.md manifest-1.0.0.json      # exits 1
briefing.md no longer matches edition 1.0.0:
  claim-1: changed (claim)
Build a new edition for these changes; do not rewrite the published one.
$ python3 edition_manifest.py build briefing.md --edition 1.0.0          # exits 1
manifest-1.0.0.json already exists with different claims. A published edition is never overwritten: choose a new --edition.
```

**Pass criteria.** `selfcheck.py` exits 0. `verify` prints a good signature for every edition. `check` against the old manifest exits 1 and names the claim you changed. `selfcheck.py` counts three citation forms: a backticked path with a line number, a URL, or a `[source: …]` tag. It over-flags on purpose. This playbook file passes it too [source: the author's run on 2026-09-26]. Keep the private key outside the repository; commit the manifest, its `.sig` and `allowed_signers`.

## Limits

- `selfcheck.py` proves that no number is an orphan, not that any number is right. It does not follow a `[source: row N]` tag to check that row N is sourced. A green link check is not evidence either: "the link check does not treat a successful HTTP response as evidence that a claim is correct" (`ai_qe/CONTRIBUTING.md:139-141`).
- A signed manifest proves who said what, in which edition. A signed wrong number is still wrong.
- Structural checks can pass while the content disagrees with itself. The audited site's checks "are valuable and pass" yet did not catch agreement between model data and prose (`ai_qe/research/reviews/site-audit-2026-09-06.md:140`).
- This playbook does not cover pricing, the consulting offer, pilot design, discovery questionnaires, or the legal texts on disclosing AI-generated content.
- The AI-engine figures are secondary reports, dated to their sources, and will age.

## Sources

- AI × QE at commit 6388f0a: `ai_qe/CONTRIBUTING.md`, `ai_qe/README.md`, `ai_qe/docs/principles.md`, `ai_qe/docs/research-log.md`, `ai_qe/docs/evidence/benchmarks.md`, `ai_qe/docs/evidence/reading-the-evidence.md`, `ai_qe/docs/economics/slide-language.md`, `ai_qe/research/document-manifest.json`, `ai_qe/research/reviews/`, `ai_qe/_data/briefing_routes.json`, `ai_qe/_data/briefing_room.json`, `ai_qe/_data/release.yml`, `ai_qe/releases.md`.
- Scripts: `course/03-content/m06-expertise-product/selfcheck.py` and `edition_manifest.py`, in the AI Product Studio course repository.
- AI-engine evidence, as recorded in the course research file `course/00-research/08-domain-currency-2026.md` with the URLs above; secondary, not re-read here.

This playbook is drawn from Module 6 of the AI Product Studio course.
