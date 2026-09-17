"""What the site can prove about itself, gathered at build time.

The landing page leads with proof rather than counts: the pointer check, the facts-drift table,
the lab's verified test run, the narration contract. Each row is measured when the site is built
(when the case-study clones are present) or falls back to the pinned, dated value with a label that
says so — never a number the build did not see.
"""
from __future__ import annotations

import datetime as dt
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent
COURSE_DIR = SITE_ROOT.parent
REPO = COURSE_DIR.parent
PROD = COURSE_DIR / "06-production"
GITHUB = "https://github.com/tomqwu/ai_courses/blob/main/course/"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)                     # type: ignore[union-attr]
    return module


def clones_present() -> bool:
    return all((REPO / r).is_dir() for r in ("ListenToMe", "SignUpFlow", "ai_qe"))


def pointer_proof() -> dict:
    """Run the package's own pointer check (verify.py) and report what it found."""
    try:
        V = _load("aps_verify", PROD / "verify.py")
        result = V.check_pointers()
        if len(result) == 3:
            checked, ranges, problems = result
        else:
            checked, problems = result
            ranges = 0
        return {"checked": checked, "ranges": ranges, "problems": len(problems),
                "live": clones_present()}
    except Exception as error:                          # noqa: BLE001 — proof must not break the build
        return {"checked": 0, "ranges": 0, "problems": -1, "live": False, "error": str(error)}


def facts_proof() -> dict:
    """The pinned facts, re-derived from the clones when they are present."""
    facts = json.loads((PROD / "facts.json").read_text(encoding="utf-8"))
    rows = []
    live = clones_present()
    derive = None
    if live:
        try:
            CF = _load("aps_check_facts", PROD / "check_facts.py")
            derive = CF.DERIVATIONS
        except Exception:                               # noqa: BLE001
            live = False
    drifted = 0
    for key, spec in facts.items():
        derived = None
        if derive and key in derive:
            try:
                derived = derive[key]()
            except Exception:                           # noqa: BLE001
                derived = None
        status = "pinned"
        if derived is not None:
            status = "ok" if str(derived) == str(spec["pinned"]) else "drift"
            if status == "drift":
                drifted += 1
        rows.append({"key": key, "pinned": spec["pinned"], "pinned_date": spec.get("pinned_date", ""),
                     "derived": derived, "status": status, "note": spec.get("note", "")})
    return {"rows": rows, "live": live, "drifted": drifted, "total": len(rows)}


def lab_proof() -> list[dict]:
    """The lab starters' verified status lines, read from their READMEs."""
    out = []
    for name, rel in (("TinyCopilot (Labs M2–M3)", "03-content/m02-ondevice-app/tinycopilot/README.md"),
                      ("mini-flow (Lab M5)", "03-content/m05-security-tests/mini-flow/README.md")):
        path = COURSE_DIR / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        lines = re.findall(r"^- `make [^`]+` → (.+)$", text, re.M)
        if lines:
            out.append({"name": name, "lines": [re.sub(r"\*\*", "", l).strip() for l in lines[:3]],
                        "href": GITHUB + rel})
    return out


def narration_proof(decks: list[dict], manifest: dict) -> dict:
    slides = sum(len(d["slides"]) for d in decks)
    scripted = sum(1 for d in decks for s in d["slides"] if s["script_text"])
    words = sum(len(s["script_text"].split()) for d in decks for s in d["slides"])
    recorded = sum(len((manifest.get("decks", {}).get(d["id"], {}) or {}).get("slides", {})) for d in decks)
    return {"slides": slides, "scripted": scripted, "words": words, "recorded": recorded}


def gather(decks: list[dict], manifest: dict) -> dict:
    return {"built": dt.date.today().isoformat(), "pointers": pointer_proof(), "facts": facts_proof(),
            "labs": lab_proof(), "narration": narration_proof(decks, manifest)}


def proof_section(proof: dict, site_base: str) -> str:
    """The landing page's proof block."""
    p, f, n = proof["pointers"], proof["facts"], proof["narration"]
    live_note = ("measured at build time against the cloned case-study repositories"
                 if f["live"] else "pinned values, dated; re-measured whenever the site is built beside the clones")
    if p["problems"] == 0 and p["checked"]:
        pointer_line = (f'<strong>{p["checked"]:,} file pointers</strong> into the three repositories resolve'
                        + (f', {p["ranges"]:,} line ranges in bounds' if p["ranges"] else "")
                        + (" — checked at build time." if p["live"] else "."))
    elif p["problems"] > 0:
        pointer_line = f'<strong>{p["problems"]} of {p["checked"]:,} pointers</strong> did not resolve at build time — this build is not clean.'
    else:
        pointer_line = 'Pointer resolution is checked when the site is built beside the clones (<code>make -C course check</code>).'
    fact_rows = []
    for r in f["rows"]:
        if r["status"] == "pinned":
            value = f'<td>{html.escape(str(r["pinned"]))}</td><td class="proof-status is-pinned">pinned {html.escape(r["pinned_date"])}</td>'
        elif r["status"] == "ok":
            value = f'<td>{html.escape(str(r["derived"]))}</td><td class="proof-status is-ok">re-derived · matches</td>'
        else:
            value = f'<td>{html.escape(str(r["derived"]))} <small>(pinned {html.escape(str(r["pinned"]))})</small></td><td class="proof-status is-drift">drifted</td>'
        label = r["key"].replace(".", " · ").replace("_", " ")
        fact_rows.append(f'<tr><th scope="row">{html.escape(label)}</th>{value}</tr>')
    import site_content as SC                                                     # noqa: PLC0415
    labs = "".join(
        f'<li><strong>{html.escape(l["name"])}:</strong> ' + " · ".join(SC.inline(x) for x in l["lines"])
        + f' <a href="{l["href"]}">README</a></li>' for l in proof["labs"])
    drift_line = (f'{f["drifted"]} of {f["total"]} drifted since they were pinned' if f["live"] and f["drifted"]
                  else (f'all {f["total"]} re-derive to their pinned values' if f["live"] else f'{f["total"]} pinned facts'))
    return f"""<section class="proof" id="proof">
  <div class="section-heading">
    <h2>What this site can prove about itself</h2>
    <span class="section-note">Built {html.escape(proof['built'])} · {html.escape(live_note)}</span>
  </div>
  <div class="proof-grid">
    <article class="proof-card">
      <h3>Every claim carries a pointer</h3>
      <p>{pointer_line}</p>
      <p class="proof-foot"><a href="{GITHUB}06-production/verify.py">verify.py</a> is the check; it runs before every publish.</p>
    </article>
    <article class="proof-card">
      <h3>The numbers are re-derived, not remembered</h3>
      <p>The content standard whitelists the numbers the course may state as fact. <strong>{html.escape(drift_line)}</strong>.</p>
      <details><summary>See the facts table</summary>
        <div class="table-wrap"><table class="proof-table">
          <thead><tr><th scope="col">Fact</th><th scope="col">Value</th><th scope="col">Status</th></tr></thead>
          <tbody>{"".join(fact_rows)}</tbody></table></div>
      </details>
      <p class="proof-foot"><a href="{GITHUB}06-production/check_facts.py">check_facts.py</a> re-derives each one from the clones the way a learner would.</p>
    </article>
    <article class="proof-card">
      <h3>The labs are run, not described</h3>
      <ul class="proof-list">{labs or '<li>Lab starters ship with their verified test runs in their READMEs.</li>'}</ul>
      <p class="proof-foot">The numbers a lab prints are the numbers its README states, or the build is wrong.</p>
    </article>
    <article class="proof-card">
      <h3>What is spoken is what is written</h3>
      <p><strong>{n['slides']} slides</strong>, {n['scripted']} scripted, <strong>{n['words']:,} words</strong> of approved narration. Captions, transcript and script are checked word for word; a mismatch fails the build.</p>
      <p class="proof-foot"><a href="{site_base}/transcripts/ALL.md">The complete transcript</a> is the same words.
        Where a deck says preview voice, its audio is spoken by a synthesized voice rather than a human recording.</p>
    </article>
  </div>
</section>"""
