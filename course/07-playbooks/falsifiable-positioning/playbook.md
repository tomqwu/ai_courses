# Competition Table to Falsifiable One-Liner

This playbook is for founders and engineers who have to say, in one sentence, what their product is and why it is different, to buyers who will check. When you finish you will have a dated comparison table in which every cell carries a source or the word "unverified"; a one-line positioning statement in which every clause traces to a column; a deletion test showing which clauses do the separating work and which are decoration; and a short, honest list of what your product does not do, drawn from the same table.

## The method

1. **Choose the rows.** Take at least five products you have used or whose site you have opened. Cover more than one shape of product, and include your nearest rivals, especially free and open-source ones. Five rows of one shape cannot support a wedge.

2. **Choose the columns.** Start with platform, your main axis (on-device or not, if privacy is your story), privacy detail, model choice, price and focus. Then add one column for every claim you intend to make. A differentiator with no column cannot be checked against anyone, so you cannot claim it falsifiably.

3. **Fill every cell from a source you opened.** Record the URL and the date you read it, or write "unverified". Never fill a price from memory. Qualify uncertainty inside the cell, where the reader sees it: "approximately", "reportedly", "reported but unconfirmed". Date the header.

4. **Sort the rows into shapes and name the tension.** Group rivals by how they work, not by what they call themselves. Then write the one sentence that explains why the market looks the way it does. The corner the table leaves empty is your candidate wedge.

5. **Write the one-liner.** Use the form *adjective-wedge × differentiators × audience*: the adjectives that place you in the empty corner, the category noun, who it is for, then two or three differentiators.

6. **Map each clause to a column.** For every clause, name the column that proves it and the rows it excludes. A clause that maps to no column is copy; rewrite it or add a sourced column.

7. **Run the deletion test.** Delete one clause. If the shorter sentence now also describes some row in your table, the clause is load-bearing: name that row. If no row is newly admitted, the clause is redundant or decoration. Cut it and run the test again on the shorter sentence. Stop when deleting any remaining differentiator admits a named row. The audience clause may stay if it is true, because it tells a buyer whether the product is for them; do not count it as a differentiator.

8. **Make ambiguous words precise.** "Free" can mean "has a free tier" or "has no paid tier". Those two readings exclude different rows. Say the one your Price column proves.

9. **Write what the product does not do.** Take it from your own table: platforms you lack, features rivals have, things you have deferred. Then write the three objections a buyer would raise from your table, and answer each with a row and its source, or a file in your repo. If an answer needs you to hide something, change the product, the price or the page.

10. **Keep one canonical sentence, and re-test when the table changes.** New rows can falsify old clauses. Re-run the deletion test whenever you add a row, and update every copy of the sentence at once.

## Template

**`docs/competition.md`**, table first, sources below it.

```markdown
# Competition analysis — <product>
_Last updated: <YYYY-MM-DD>. Every cell carries a source id or "unverified". Where a detail
could not be confirmed from a primary source, it is qualified with "approximately",
"reportedly" or "reported but unconfirmed"._

| Tool | Platform | <Main axis>? | Privacy | Model choice | Price | Focus |
|---|---|---|---|---|---|---|
| <Rival A> | <value> [S1] | <value> [S2] | <value> [S2] | <value> [S1] | <value> [S3] | <value> [S1] |
| <Rival B> | <value> [S4] | unverified | <value> [S4] | reportedly <value> [S4] | <value> [S4] | <value> [S4] |
| **<You>** | <value> [R1] | <value> [R2] | <value> [R2] | <value> [R2] | <value> [R1] | <value> [R1] |

## Sources
- S1: <URL> — read <YYYY-MM-DD>
- R1: `<path in your repo>:<lines>`

## Shapes
- <Shape 1>: <rows>. <Shape 2>: <rows>.
- Tension: <one sentence>. Empty corner: <one phrase>.
```

**`docs/positioning.md`**, the sentence and its proof.

```markdown
## One-liner
<Product> is the <wedge adjectives> <category> for <audience> — <differentiator>, <differentiator>.

## Clause map and deletion test (against the table dated <YYYY-MM-DD>)
| Clause | Column | Rows it excludes | Delete it: rows newly admitted | Verdict |
|---|---|---|---|---|
| "<clause>" | <column> | <row names> | <row names, or none> | load-bearing / redundant (cut) / audience |

## What <product> does not do
- <limit> (<row or column, or repo pointer>)

## Objections our own table invites
1. "<Rival> is <free / cheaper / also on-device>. Why yours?" → <row + source, or repo pointer>
```

**`check_table.py`** checks the first table in a file: every cell after the first column has a source id or "unverified", and every web source has a URL and a read date. Standard library only.

```python
"""Check the first Markdown table in a file: every cell after the first column carries a
source id like [S1] or [R1], or the word "unverified"; every S source has a URL and a read date."""
import re
import sys

lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
start = next(i for i, line in enumerate(lines) if line.startswith("|"))
table = []
for line in lines[start:]:
    if not line.startswith("|"):
        break
    table.append(line)
sources = {m.group(1): m.group(2) for m in (re.match(r"^- ([SR]\d+): (.*)", l) for l in lines) if m}
problems, cited = [], set()
for n, row in enumerate(table[2:], 1):  # skip the header and the |---| line
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    for col, cell in enumerate(cells[1:], 2):
        ids = re.findall(r"\[([SR]\d+)\]", cell)
        cited.update(ids)
        if not ids and "unverified" not in cell.lower():
            problems.append(f"row {n} ({cells[0]}), column {col}: no source, not marked unverified")
for sid in sorted(cited):
    text = sources.get(sid)
    if text is None:
        problems.append(f"{sid}: cited but not listed under Sources")
    elif sid.startswith("S") and not ("http" in text and re.search(r"read \d{4}-\d{2}-\d{2}", text)):
        problems.append(f"{sid}: needs a URL and 'read YYYY-MM-DD'")
print("\n".join(problems) or f"{len(table) - 2} rows: every cell sourced or marked unverified")
sys.exit(1 if problems else 0)
```

## Checklist

- [ ] The table has at least 5 rival rows, each a product you used or whose site you opened.
- [ ] The rows cover at least two shapes and include your nearest free or open-source rival.
- [ ] The table has at least 6 columns, and every claim you plan to make has one.
- [ ] Every cell carries a source id or "unverified"; `check_table.py` exits 0.
- [ ] Every web source has a URL and a read date.
- [ ] Uncertain cells are qualified inside the cell.
- [ ] The header is dated.
- [ ] The one-liner names a category, an audience and at least two differentiators.
- [ ] Every clause maps to a column.
- [ ] Deleting each remaining differentiator admits at least one named row.
- [ ] Every ambiguous word ("free", "private", "local") is stated in the reading your table proves.
- [ ] At least two "does not do" lines, each tied to a row, column or file.
- [ ] Three objections from your own table, each answered with a row and source, or a file.
- [ ] Every copy of the one-liner (README, site, store listing) is identical.

## Worked example from a real repo

**ListenToMe**, a macOS meeting copilot, keeps its analysis in `ListenToMe/docs/competition-analysis.md`.

**The table.** A dated header states the qualification rule: "where a detail could not be confirmed from a primary source, it is qualified with 'approximately' or 'reportedly'" (`ListenToMe/docs/competition-analysis.md:3`). The comparison has 14 rows (13 rival rows, one of them a category of interview-assist tools, plus ListenToMe) and 9 columns (`ListenToMe/docs/competition-analysis.md:20-35`). Uncertainty sits in the cell: Granola's bring-your-own-key support is "reported but unconfirmed" (`ListenToMe/docs/competition-analysis.md:22`); Fireflies is "Reportedly Whisper-based (unconfirmed)" (`ListenToMe/docs/competition-analysis.md:24`). The rivals are sorted into four shapes (`ListenToMe/docs/competition-analysis.md:7-12`), and the tension is named: "nearly every commercial product processes audio and runs its AI in the cloud, even when it markets itself as 'local-first'" (`ListenToMe/docs/competition-analysis.md:14`).

One gap against this playbook's standard: each rival's prose entry ends with one source URL (13 entries, 13 URLs, `ListenToMe/docs/competition-analysis.md:39-76`), so a reader cannot tell which cell a URL supports. Run on that file, `check_table.py` flags all 112 cells (14 rows × 8 columns).

**The one-liner.** "ListenToMe is the free, open-source, fully on-device meeting copilot for macOS — bring your own model, run it private, and shape it to any conversation." (`ListenToMe/docs/competition-analysis.md:88`). The README carries a different version: "... for macOS — with a private capture-and-recall companion for iPhone and iPad. Bring your own model, stay private, shape it to any conversation." (`ListenToMe/README.md:7`). Two versions of one sentence is the drift step 10 warns about.

**The deletion test, against the table as it stands.** The four rows closest to ListenToMe are Natively, Hyprnote/Anarlog, Meetily and MacWhisper (`ListenToMe/docs/competition-analysis.md:30-34`). The last column reads "free" as "has a free tier".

| Clause | Column | Excludes among the four | Delete it alone: newly admitted |
|---|---|---|---|
| "free" | Price | none if a free tier counts; all four if it means no paid tier | none |
| "open-source" | Tool (the "open-source" label) | MacWhisper, which has no such label | none |
| "fully on-device" | On-device? | Hyprnote/Anarlog ("Partial") | none |
| "meeting copilot" | AI features, Focus | Hyprnote/Anarlog ("AI notes/chat"), Meetily ("AI summaries"), MacWhisper ("file/meeting transcription") | **Meetily** |
| "for macOS" | Platform | none: all four run on macOS | none (audience) |
| "bring your own model" | Multi-model/BYO | none: all four read "Yes" | none |
| "run it private" | Privacy | none | none |
| "shape it to any conversation" | Focus | Natively ("interview copilot"), MacWhisper | **Natively** |

Two clauses are load-bearing on their own: "meeting copilot" keeps out Meetily, and "shape it to any conversation" keeps out Natively, which is open-source, on-device, bring-your-own-model and has a "Real-time copilot" (`ListenToMe/docs/competition-analysis.md:30`). The rest exclude the commercial cloud rows, but redundantly: each of those rows fails several of them at once.

Cut the clauses that admit nothing, one at a time, and re-run. After "run it private", "bring your own model" and "open-source" go, deleting "fully on-device" admits Fireflies, whose row lists a "Live Assist real-time copilot" and a broad focus (`ListenToMe/docs/competition-analysis.md:24`). So one privacy clause survives. The minimal sentence against today's table is "the fully on-device meeting copilot for macOS that you shape to any conversation". Cut in a different order and "open-source" can hold that slot instead; redundant clauses compete for one place, so keep the one your buyer checks first.

**Make "free" precise.** Every one of the 13 rival rows lists a paid tier, from Granola's Business plan to MacWhisper's one-time Pro; ListenToMe's cell reads "Free & open-source" (`ListenToMe/docs/competition-analysis.md:22-35`). As "no paid tier", "free" alone separates ListenToMe from every row. As "has a free tier", it separates it from none of the four nearest.

**The analysis already knew.** Its positioning section says on-device, bring-your-own-model and free/open-source are now "table stakes within that open-source cluster rather than a differentiator", and names what does separate: a live, hotkey-driven copilot loop and Apple Intelligence as an on-device path (`ListenToMe/docs/competition-analysis.md:82`), and per-pane model selection (`ListenToMe/docs/competition-analysis.md:84`). None of those has its own column, so none can be checked against a rival. By step 2, add the columns before you claim them. The peers that changed the picture were added after the analysis was first written (`ListenToMe/docs/competition-analysis.md:96`), which is why step 10 exists.

**What it does not do, from the same file.** The table lists ListenToMe on macOS only, while Natively, Hyprnote/Anarlog and Meetily also run on Windows (`ListenToMe/docs/competition-analysis.md:30-35`). Semantic cross-meeting search, meeting auto-start and Notion/Obsidian export are "future ideas, not commitments", and Android is out of scope (`ListenToMe/docs/competition-analysis.md:101`). It ships 18 presets "against the dozens of templates the commercial tools ship" (`ListenToMe/docs/competition-analysis.md:99`); the 18 are in `ListenToMe/Sources/ListenToMeCore/PresetCatalog.swift:23-284`.

**One objection its table invites.** "Natively is free for personal use, open-source, on-device and a real-time copilot. Why ListenToMe?" The answer is a row and a file: Natively's focus is interviews (`ListenToMe/docs/competition-analysis.md:30`), and the preset catalogue above covers standups, lectures, support calls and more.

## Self-check

**Sourcing, runnable.** Save the script as `check_table.py` and run it on your table:

```bash
python3 check_table.py docs/competition.md; echo "exit=$?"
```

A passing file prints `<N> rows: every cell sourced or marked unverified` and `exit=0`. On a test file with one unsourced cell, a source missing its read date and a source never listed, it printed (2026-09-26, Python 3.11.15):

```text
row 1 (Rival A), column 5: no source, not marked unverified
S3: needs a URL and 'read YYYY-MM-DD'
S4: cited but not listed under Sources
exit=1
```

It checks that a source is cited, not that the source says what the cell says. Open one source at random; if it does not match its cell, re-check every cell.

**The sentence, scored.** Score each line 1 or 0.

| # | Criterion | Pass when |
|---|---|---|
| 1 | Rows | At least 5 rivals you used or visited, in at least two shapes |
| 2 | Columns | Every clause of the one-liner has a column |
| 3 | Sourcing | `check_table.py` exits 0 |
| 4 | Dating | The header and every web source carry a date |
| 5 | Qualifiers | Every uncertain cell says so inside the cell |
| 6 | Clause map | Every clause names its column and the rows it excludes |
| 7 | Deletion test | Deleting each remaining differentiator admits a named row |
| 8 | Precision | Every ambiguous word is stated in the reading the table proves |
| 9 | Limits | At least two "does not do" lines, each with a pointer |
| 10 | Objections | Three, each answered with a row and source, or a file |

**Pass criteria.** 9 or 10, with rows 3, 6 and 7 all scoring 1.

## Limits

- A table is a snapshot. Prices and features change; re-read every source before you publish.
- The deletion test is only as strong as your rows. A rival you left out can falsify any clause.
- The checker proves a source is cited, not that it supports the cell.
- The worked example is one reading of ListenToMe's cells at the commit this playbook was written against. Read the cells yourself before you reuse the result.
- This playbook does not cover pricing, the rest of a sales page, or the legal rules for naming competitors in advertising.

## Sources

- `ListenToMe/docs/competition-analysis.md`: header, shapes, table, per-rival entries, positioning and gaps.
- `ListenToMe/README.md:7` and `ListenToMe/Sources/ListenToMeCore/PresetCatalog.swift:23-284`.
- This playbook is extracted from the AI Product Studio course (github.com/tomqwu/ai_courses).
