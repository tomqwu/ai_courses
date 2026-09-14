# Video Scripts — M7: Monetize: Pricing, Packaging, Positioning

> Master recording scripts, one per segment. Pacing: ~130 words/minute. The beats are the spoken
> spine, not a verbatim transcript — read them in your own words and keep every pointer and number
> exactly as written. Open each pointer exactly as named in the on-screen column.

## M7.1 — Pricing the three archetypes

**Target runtime: 12 minutes (≈1,560 words).**

**Cold open (≈15 s).** "Granola charges about fourteen dollars per user per month. MacWhisper charges
about sixty-nine dollars, once. Both transcribe meetings. One of them is pricing a cost that recurs.
Guess which, then open the table and check."

**Beats**

| Time | On screen | Narration |
|---|---|---|
| 0:00 | Title slide | In M1–M6 you built three product cores. Today you price them — from evidence, not instinct. Every number in this segment lives in a file you can open. |
| 0:30 | `ListenToMe/docs/competition-analysis.md`, Price column | This is the raw material: twelve competitor rows, dated 2026-08. Read the header convention first — where a detail could not be confirmed from a primary source, it is qualified "approximately" or "reportedly." That convention is a promise to the reader, and you copy it in the lab. |
| 1:30 | Granola, Otter, Fireflies rows | Granola streams every meeting through third-party cloud ASR — it names Deepgram and AssemblyAI — plus OpenAI or Anthropic summarization. Otter runs its own ASR plus Claude-backed insights. Fireflies runs cloud ASR and cloud AI. All three charge monthly, and the monthly price is a pass-through of a monthly cost. |
| 3:00 | MacWhisper row | MacWhisper runs Whisper fully on-device. Near-zero marginal cost per user. It charges once — about fifty-nine euros, roughly sixty-nine dollars. The pattern is structural, not stylistic. |
| 4:00 | Natively row | Free is also a price. Natively — the open-source peer — reads "Free personal; Pro via lifetime/yearly." The paid tier sits above a complete free core, never as a repair of a crippled one. ListenToMe prices at zero, MIT-licensed, against a category running about eight to one hundred forty-nine dollars a month. |
| 5:00 | Tension paragraph, lines 12–14 | Two structural tensions: privacy versus convenience, where "local-first" usually means local capture only, and opinionated versus open, where most products lock you to one undisclosed engine. The wedge is defensible because copying it destroys the incumbent's business model: their monthly price pays for the cloud compute it removes. |
| 6:30 | `SignUpFlow/README.md`, "Provider-backed Features" | Type 2 prices per seat. Read the gating rule: billing routes remain under `/api/v1`, SMS routes under `/api/sms`, but both return 404 behind `BILLING_ENABLED=false` and `SMS_ENABLED=false`. Paid billing and SMS are deferred; the complete scheduling workflow does not require them. |
| 7:30 | `SignUpFlow/AGENTS.md` line 18 | The rule in one line: "core scheduling must not require either paid integration." That bars charging for a path you cannot yet trust, and it bars gating the core to force upgrades. Monetize after the workflow is trustworthy. |
| 8:15 | `SignUpFlow/README.md`, onboarding | Growth and billing are the same event. Public signup is rejected for existing orgs; every later member joins through an administrator-created invitation. The admin who invites is the buyer, so per-seat pricing tracks real adoption. |
| 9:00 | `ai_qe/index.md` → `ai_qe/discovery.md` → `ai_qe/_data/engagement.json` | Type 3 sells measurement. Four path cards route to `/discovery/`, then a questionnaire, then an engagement whose commercial field reads: fixed-fee or capped discovery; separately capped pilot — no client price or start date agreed. |
| 10:15 | Deep-read §4 | The consultant never promises a savings number. The workshop shows results as "questions rather than conclusions; no savings number yet." The benefits-realization register ties every claimed saving to a Finance-owned budget row, so an inflated number is checkable by the client's own finance team. |
| 11:15 | Action-step slide | Your turn: one sentence per archetype — the model, who pays, and when. Post it. |

**Demo cue.** Open `competition-analysis.md` and scroll the Price column slowly so viewers see model,
price, and channel in one cell. Then open `engagement.json` and let the stage durations sit on screen.

**Action-step close.** "Write the three sentences. Lab M7 makes you defend each one with a table and
a floor — so write them as claims, not preferences."

**Recording notes.**
- Enlarge the table; the Price column is the content.
- If over time, cut the Natively row from the narration, not the MacWhisper comparison.
- Do not state Otter's pricing as a single figure; say "approximately" whenever the source does.

## M7.2 — Packaging and platforms

**Target runtime: 10 minutes (≈1,300 words).**

**Cold open (≈15 s).** "A creator sells a twelve-hundred-dollar cohort, then repackages the same
recordings as a ninety-seven-dollar self-paced course. The recordings are identical. The price
dropped because the value dropped. Here is the rule that explains when that is legitimate."

**Beats**

| Time | On screen | Narration |
|---|---|---|
| 0:00 | Research §C | The research's rule of thumb: the same content might be ninety-seven to two hundred ninety-seven dollars self-paced, or five hundred to two thousand plus as a live four-week cohort, because buyers pay for live instruction, peers, and feedback. |
| 1:00 | Maven bands | Maven's published benchmarks: six to eight live hours plus a project, eight hundred to twelve hundred dollars. Eight to twelve hours plus multiple projects, twelve hundred to eighteen hundred. Twelve to twenty hours plus projects plus a capstone, eighteen hundred to two thousand four hundred fifty. |
| 2:15 | Research §C, fraction rule | Self-paced prices as a fraction of live: seventy to eighty-five percent — only if it keeps projects plus async feedback plus community. Strip all three and a bare library "shouldn't be sold at all." The research's phrasing: "a stack of Zoom recordings is not a self-paced course." |
| 3:30 | Research §C, §D | Platform economics: Udemy keeps thirty-seven percent of marketplace sales — thirty-two cents per dollar in 2025 — controls pricing at nine ninety-nine, and exports no student emails. Own-platform creators charge fifty to two hundred plus. Marketplaces are discovery and validation, never primary. |
| 4:45 | MacWhisper row | For an app, the same reach-versus-margin split: MacWhisper sells at about sixty-nine dollars one-time on Gumroad and six ninety-nine a month to ninety-nine ninety-nine lifetime on the App Store. The store brings reach and subscription expectations and keeps the customer; direct keeps the margin and the email address. |
| 5:45 | `ListenToMe/docs/RELEASING.md` | Direct is not a compromise — you already have the machinery: signed, notarized, stapled releases targeting an exact commit. |
| 6:30 | `course/04-sales/pricing-and-platforms.md`, cost floor | Compute the floor before the price. The course's own month-one record: course platform plus community plus email lands at roughly eighty to one hundred thirty dollars a month, so break-even at the three-hundred-ninety-nine-dollar tier is about two sales a month. A price below your floor is not a price; it is a subsidy. |
| 7:30 | Price ladder | The worked example is this course. Zero-dollar lead product, three hundred ninety-nine self-paced, fourteen ninety live with a nine-hundred-ninety founding price, twenty-five hundred to four thousand for a team of three to five seats. |
| 8:30 | Why-not-cheaper / why-not-more sections | Not cheaper, because marketplace courses priced at nine hundred fifty or more earn fifty to one hundred percent more per landing-page visit, and higher-priced programs complete at far higher rates. Not more expensive yet, because there are no public testimonials, and raising price before social proof inverts the trust order. The founding discount is traded for a testimonial and a feedback interview. |

**Demo cue.** Screen-share the course's own decision record. Point at the floor line and the two
"why not" sections; the double-sided defense is the thing students must copy.

**Action-step close.** "Compute your floor in dollars and write your two-sentence 'why not cheaper,'
citing one benchmark. Paste both into your worksheet."

**Recording notes.**
- Put the Maven bands in a table on screen; numbers read aloud are hard to hold.
- If over time, cut the store-versus-direct beat to one sentence.
- Do not claim a completion rate for this course — no cohort has run yet.
- Call the revenue model a plan, never a forecast.

## M7.3 — Honest marketing that converts

**Target runtime: 11 minutes (≈1,430 words).**

**Cold open (≈15 s).** "A vendor puts a negative independent study on its own website and stamps
every planning number with 'not observed client results.' That sounds like a conversion problem. It
is the reason the executive stops asking whether to believe them and starts asking when to start."

**Beats**

| Time | On screen | Narration |
|---|---|---|
| 0:00 | Research §E | StoryBrand in one line: the student is the hero, you are the guide. Every section answers the buyer's question — does this get me there, and can I trust you? — not yours. |
| 1:00 | Proof-asset list | For a technical audience, real shipped projects are the social proof: repos, demos, dated evidence lines, test badges. Use them. Never invent a testimonial — the course's own rule is ship beta before claiming social proof. |
| 2:00 | Eight-section anatomy | The page skeleton: transformation headline, who it's for and who it isn't, problem and stakes, outcomes per module, instructor proof in one hundred to one hundred fifty words, testimonials in before/after/result form, FAQ, transparent pricing with one call to action. Length: eight hundred to twelve hundred words under two hundred dollars; two to three thousand for five hundred plus or cold traffic. |
| 4:00 | `course/00-research/03-ai-qe-deep-read.md` §1, §3 | Now the counterintuitive part. AI × QE publishes, on its own decks, that the only independent RCT is negative, and marks every planning number with "planning inputs are not observed client results." The deep-read records the effect: the executive stops asking "why should I believe you?" and starts asking "when can we start?" |
| 5:30 | Deep-read §3 | The mechanism: qualified claims with sources are a premium signal. They tell the buyer you audit yourself harder than they would. A buyer who reads your "what this doesn't prove" section has had their cheapest objection — belief — removed, leaving the real question: start date. |
| 6:30 | `ListenToMe/docs/competition-analysis.md:80` | The one-liner is derived, not composed. ListenToMe's: "the free, open-source, fully on-device meeting copilot for macOS — bring your own model, run it private, and shape it to any conversation." |
| 7:30 | Clause-to-column table | Every clause traces to a column: "free" to Price, "open-source" to closed rival pipelines, "fully on-device" to the On-device column (only MacWhisper and Natively also answer yes), "bring your own model" to multi-model, "run it private" to privacy, "shape it to any conversation" to Focus. |
| 9:30 | Deletion test | The test is deletion: remove a clause and the sentence must become false against a row. If no row would notice, the clause is decoration. Cut it. |
| 10:15 | Action-step slide | Your turn: the eight-section skeleton with sections one, two, and five written, plus one "what this doesn't do" line. |

**Demo cue.** Read the one-liner aloud once, then delete one clause on screen and re-read it. The loss
of specificity is audible, which is the whole lesson.

**Action-step close.** "Draft the skeleton and post the headline and the honest-limitation line.
Reply to one peer: which clause would their own table falsify?"

**Recording notes.**
- Spell the file path aloud when you show the one-liner; viewers screenshot it.
- If over time, compress the eight sections to a single screen and slow down on the deletion test.
- Do not quote a conversion number for the eight-section restructure as your own result.
- The limitation you write on screen must be one you would actually publish.
