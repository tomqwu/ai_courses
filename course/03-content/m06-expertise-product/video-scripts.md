# Video Scripts — M6 (The Expertise Product)

> Pacing is **~130 words per minute**. Word budgets below are narration only; on-screen demo beats add
> 30–45 seconds of silence each, which is why a five-minute segment carries about 520 spoken words.
> Read the narration aloud as written; it is already trimmed to the budget.

## M6.1 — Credibility is the product

**Target runtime:** 5:00 · **Narration budget:** ~520 words

**Cold open (0:00–0:15).** A vendor deck promises thirty to fifty percent productivity gains. This
site promises nothing, publishes the study that says AI made developers slower, and logs the source
it could not download. That is the product.

| Time | On screen | Narration |
|---|---|---|
| 0:15 | `ai_qe/CONTRIBUTING.md`, section "Research conventions" | "Read the first rule with me. Research sources are cited by name because the citation is the evidence; no vendor is endorsed. Then the required fields: date, sample, method, unit, self-reported versus measured, sponsor, and what claim the record can support. Anything unverifiable is listed as such. That last field is the one every other site omits, because a number without a stated limit is an advertisement." |
| 1:00 | `ai_qe/docs/evidence/benchmarks.md`, METR entry | "Here is the record that costs this site something. AI-allowed issues took nineteen percent longer, confidence interval plus two to plus thirty-nine. Developers expected twenty-four percent faster and afterwards believed twenty percent faster. Supports: task efficiency, negative. Caveats: sixteen experienced maintainers, two hundred forty-six real issues, measured by screen recording, independent non-profit." |
| 1:55 | Same file, Peng entry | "Two records down: fifty-five point eight percent faster, ninety-five freelancers, one synthetic JavaScript task, measured, but vendor-affiliated — Microsoft Research, GitHub and MIT. Two real results, one negative and independent, one positive and vendor-funded. The record structure forces you to see the difference instead of averaging them into a single cheerful claim." |
| 2:45 | `ai_qe/docs/research-log.md`, "Not verified" list | "Nothing reaches a slide before it reaches the log. Entries are dated and structured Question, Checked, Outcome, Changed. The initial evidence base entry says the only independent randomized controlled trial is negative. Then the list most sites would delete: World Quality Report cost-of-quality share, any Gartner AI-testing productivity figure, Snyk accuracy claims. Published as unverified. That list is what makes the rest believable." |
| 3:35 | `ai_qe/research/document-manifest.json`, entry M02 | "Eleven retrievals are logged here with URL, date, status and a SHA-256 hash. Entry M02, a McKinsey PDF, has status unavailable and the reason recorded verbatim: the read operation timed out. A spotless manifest is suspicious. A manifest that logs its own failure is checkable, because you can re-run it. Even the two hero illustrations have a provenance file." |
| 4:15 | `ai_qe/docs/principles.md`, "Four levels of saving" | "Finally, the taxonomy the whole site runs on. Task-level efficiency: net time for one activity after review and correction. Capacity released: hours freed across the workflow. Hard-dollar saving: budgeted cost Finance can remove, against a named budget line. Total software-spend impact. Every number is labelled with one of the four, and mixing them is the most common error in AI business cases." |

**Demo cue.** Terminal on `research/` — run `grep -n "unavailable" research/document-manifest.json`
and let the M02 line sit on screen. The viewer should notice the reason string is recorded, not
paraphrased. That single line is the whole segment.

**Action-step close.** Open the cloned `ai_qe` repo and verify all four files yourself, then draft one
dated entry about a claim in your own field — including one thing you could not verify. The
not-verified line is what makes the other three believable.

**Recording notes.** Enlarge the terminal font before recording the manifest grep; the M02 reason
string is the money shot. Cut the Peng beat first if you run long — METR plus the manifest carries the
argument. Do not say "AI makes developers faster" or slower: say what each record measured and who
funded it. Keep "the citation is the evidence" verbatim.

## M6.2 — One research base, many audiences

**Target runtime:** 5:00 · **Narration budget:** ~520 words

**Cold open (0:00–0:15).** One hundred sixteen slides serve four different audiences, and nobody
forked a single one. The trick is not summarisation. It is stable IDs and declared routes.

| Time | On screen | Narration |
|---|---|---|
| 0:15 | `ai_qe/_data/briefing_room.json` | "This file defines the presentation room. Four decks along two axes: audience, executive or technical, and scenario, banking or industry. Banking executive, twenty-one slides, twenty-five to thirty minutes. Banking technical, thirty-three. Industry executive, twenty-six. Industry technical, thirty-six. Twenty-one plus thirty-three plus twenty-six plus thirty-six is one hundred sixteen. Nothing is forked: both cuts trace back to the same source records." |
| 1:05 | `ai_qe/_data/briefing_routes.json`, `evp` block | "Routes are declared, not hand-cut. The banking executive route plays fourteen of the twenty-one slides — one, three, nineteen, twenty, six, twenty-one, eighteen, seventeen, thirteen, fourteen, fifteen, sixteen, ten, twelve — and declares closing twelve. Full order retains everything. Read the README rule: focused routes end on a decision discussion; full decks retain the supporting material. The invariant is the slide ID, so a route reorders and omits but never rewrites." |
| 1:50 | `ai_qe/briefings/index.md`, 30-minute script | "The page embeds a suggested thirty-minute conversation. Align, five minutes: which part of QA creates the most delay or repeated work? Explore, fifteen: follow one workflow and show the platform services behind it. Agree, ten: choose the process, the owner and the evidence for a first pilot. Half the meeting is spent on the buyer's problem and it closes on a decision, not a feature list." |
| 2:35 | `ai_qe/docs/economics/slide-language.md` | "Then the wording rules. Use: working hypothesis, to be tested on the bank's own data. Capacity released is not a saving until Finance confirms how it is captured. Avoid: industry benchmarks show thirty to fifty percent gains, ROI of X percent before a pilot has measured anything, and any squad-level headcount arithmetic. The executive message ends: the decision today is whether to fund the first two phases, not whether to transform QA." |
| 3:25 | `ai_qe/docs/method/discovery-questionnaire.md`, post-mortem | "The funnel's filter is one form, role-routed at the first question. Executive sponsor, Finance and procurement answer Sections one, five B and six; engineering, delivery, QE and platform answer two, three, four, five A and six. Priority questions are single-select. Ranges are mutually exclusive and gap-free, with an unknown option so a guess is not recorded as data. The predecessor had twenty-nine questions and one hundred eighty-six checkbox options and took twenty to thirty minutes." |
| 4:15 | `ai_qe/discovery.md`, decision-brief section | "The largest omission in that form was the financial-capture set: budget ownership, variable share of spend, renewal windows, what happens to released capacity, and what Finance will recognise as a saving. Without it, the same four percent capacity result can be booked as a hard saving, as cost avoidance, or as nothing. That is why the Agree segment lands on the discovery guide and the one-page decision brief." |

**Demo cue.** Open `briefing_routes.json`, then the deck URL with `?route=client` appended (README's
shareable link form; `CONTRIBUTING.md` documents `?route=client#slide-N`). The viewer should notice
the route plays the same slide IDs in a different order, and the link still resolves.

**Action-step close.** Take a ten-to-twelve-slide body of content you know and write two route
declarations over stable IDs: a five-or-six-slide executive route ending in a fundable ask, and a
technical route that retains the evidence. Both routes over the same slides is the whole exercise.

**Recording notes.** Enlarge the `evp` slides array. Cut the questionnaire beat first if you run long.
Never say "we cut the deck down for executives"; the content is not reduced, the route is curated.
Never present the illustrative four percent figure as a client result.

## M6.3 — Content as code

**Target runtime:** 5:00 · **Narration budget:** ~520 words

**Cold open (0:00–0:15).** A client holds your version 1.24.0 PDF. You fix a subtitle. What stops you
from silently invalidating every copy they printed? Two numbers and a changelog sentence.

| Time | On screen | Narration |
|---|---|---|
| 0:15 | `ai_qe/_data/release.yml` | "Five separate fields. Version one point twenty-four point one identifies the site and the player. Slide edition, fintech edition and questionnaire edition are one point twenty-four point zero, one point twenty-four point zero and four. Research edition one point seven point zero. The README states the rule: public content changes require a new edition before deployment. Contributing dot md is harder — content changes without a new edition are rejected on main before deployment." |
| 1:00 | `ai_qe/releases.md`, v1.24.1 entry | "Open the changelog for one point twenty-four point one. Subtitles now use the available player width and wrap naturally on smaller screens. Then the sentence that is the whole discipline: audio, subtitle timing and the version one point twenty-four point zero PDF editions remain unchanged. The patch advanced the site version and deliberately retained the slide and PDF editions. A changelog records what changed and what you chose not to touch." |
| 1:50 | `ai_qe/Makefile` and `ai_qe/tools/qa-groups.json` | "Content changes require tests to pass. Make check is models, build, site, browser. The browser suite is five CI-identical groups — playback, flows, site, models, architecture — in both Chromium and WebKit at twelve eighty by seven twenty, nineteen twenty by ten eighty, and three seventy-five by eight twelve. A slide that overflows a projector viewport fails the build like a unit test. And the link check does not treat a successful HTTP response as evidence that a claim is correct." |
| 2:40 | `ai_qe/tools/narration-review.cjs` | "One hundred sixteen slides carry recorded narration, so a silent slide edit would desynchronise the voice from the slide. This tool hashes each rendered slide with its script, recording and caption-flow definitions. A changed destination requires a deliberate retained or refreshed decision with a specific reason, committed to narration-review dot json. Then the line to tattoo on your pipeline: never reset the baseline to silence a stale-review failure. A reset converts a drift alarm into a rubber stamp." |
| 3:30 | `ai_qe/docs/method/phased-pilot.md` | "Now the commercial end. The engagement is five phases, zero to four, each with an objective, a duration, deliverables and a cost guardrail. Effort is in person-day ranges, deliberately not converted to dollars. Each phase ends with a written go/no-go memo signed by the sponsor. And the criteria are frozen first: record the primary outcome and acceptance criteria before observing pilot results, and do not choose a different success metric after seeing a favourable one." |
| 4:20 | `ai_qe/_data/pilot_gates.json` | "The exact boundaries are data, not prose: fifteen percent net-effort go threshold, ten percent review band, three-week baseline, eight-week pilot, two observed releases, at least thirty comparable tasks per arm, one extension of at most four weeks. A confidence interval crossing ten or fifteen percent is insufficient evidence for that boundary, even if its point estimate looks favourable. A noisy result is no result. That is what selling measurement instead of outcomes means." |

**Demo cue.** Terminal: run `python3 -m json.tool _data/pilot_gates.json` and leave the numbers on
screen while you say the boundary rules. The viewer should notice the thresholds are machine-readable
— that is what stops them being renegotiated after the result arrives.

**Action-step close.** Pick one quantitative claim you actually make to clients. Write it at all four
levels from `ai_qe/docs/principles.md`, mark each supported or not supported, and name who could
confirm it. Then check which level your current materials claim. Carry it into Lab M6.

**Recording notes.** Enlarge the JSON block — the go, review and sample numbers are the takeaway. Cut
the narration-hash beat first if you run long; the edition and pilot beats are load-bearing. Do not say
"savings of X dollars" about the illustrative model, and do not imply the thirty-task floor is a
statistical power guarantee — the method file explicitly calls it a reporting floor.
