# Handout — M6 (The Expertise Product)

**Mental model.** In the expertise archetype the product is not the content, it is the auditability of
the content: one research base, every claim carrying a date, sample, method, unit and level, re-cut
into audience-specific routes under versioned, tested, immutable releases.

## Decision table — which level am I claiming?

| If the number is… | It is | Who must confirm it |
|---|---|---|
| Net time for one activity, after review and correction | Task-level efficiency | A pilot you ran |
| Human hours freed across the workflow, after adoption | Released capacity | Pilot plus baseline time capture |
| Budgeted cost that can be removed or avoided | Hard-dollar saving | Finance, against a named budget line |
| Broader engineering or delivery cost | Total-spend impact | Finance and the CIO office |
| A modelled or planning scenario | **Illustrative** | Nobody — label it on the slide |

Mixing these is the most common error in AI business cases (`ai_qe/docs/principles.md`).

## Templates and commands worth keeping

**Benchmark record fields** (all seven before a number reaches a slide):
`date · sample · method · unit · self-reported vs measured · sponsor · what claim it supports`

**Provenance row:**
`| # | Claim (exact slide wording) | Source URL | Retrieved | Level 1–4 | Epistemic label | What it supports |`

**Route declaration:**
```yaml
executive: { slides: [1, 3, 6, 9, 11, 12], closing: 12 }
technical: { slides: [1, 3, 4, 5, 7, 8, 10, 9, 11, 12], closing: 12 }
full_order: [1,2,3,4,5,6,7,8,9,10,11,12]
```

```bash
grep -ciE 'not verified' docs/research-log.md    # your honest list is not empty
grep -n 'unavailable' research/document-manifest.json   # failures are logged
python3 -m json.tool _data/pilot_gates.json      # gates are data, not prose
make check                                        # models → build → site → browser
```

**Edition decision template:** what changes · what is **deliberately retained** · which edition bumps
(`version` vs `slide_edition`, as separated in `ai_qe/_data/release.yml`).

## Pointers to open

- `ai_qe/CONTRIBUTING.md` — "Research conventions"; release validation.
- `ai_qe/docs/evidence/benchmarks.md` — METR and Peng records, read end to end.
- `ai_qe/docs/research-log.md` — the not-verified and open-questions lists.
- `ai_qe/research/document-manifest.json` — 11 hashed retrievals, including failure M02.
- `ai_qe/docs/principles.md` — the four levels of saving, quoted exactly.
- `ai_qe/_data/briefing_routes.json` — routes over stable slide IDs; `closing`.
- `ai_qe/docs/economics/slide-language.md` — the Use and Avoid wording lists.
- `ai_qe/docs/method/discovery-questionnaire.md` — role routing and the failed-form post-mortem.
- `ai_qe/docs/method/phased-pilot.md` and `ai_qe/_data/pilot_gates.json` — frozen criteria, gates.

## Three gotchas

1. **A working link is not evidence.** The link check refuses to treat a successful HTTP response as
   proof a claim is correct (`ai_qe/CONTRIBUTING.md`). Date, sample, method and unit or no row.
2. **Never bump every edition together.** A player-only patch advances `version` and deliberately
   retains `slide_edition`; changelogs say what was retained (`ai_qe/releases.md`).
3. **A confidence interval crossing a gate is not a near-miss.** It is insufficient evidence for that
   boundary, "even if its point estimate appears favorable" (`ai_qe/docs/method/phased-pilot.md`).

## You're done when…

- [ ] `research-log.md` has ≥6 dated entries with ≥2 marked not-verified or open.
- [ ] Every quantitative slide cites a provenance row by number, with no orphan numbers.
- [ ] Every row carries a source URL, a retrieval date and a claim level.
- [ ] Each quantitative slide carries its epistemic label on the slide itself.
- [ ] The executive route is exactly 6 slides and its decision ask is quoted.
- [ ] The technical route keeps ≥3 evidence slides the executive route skips.
- [ ] The edition record separates site from content and states what v2 retains.
- [ ] A named peer confirms in writing that no quantitative claim is uncited.
