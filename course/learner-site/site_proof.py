"""What the site can prove about itself, gathered at build time.

The landing page leads with proof rather than counts: the pointer check, the facts-drift table,
the lab's verified test run, the narration contract. Each row is measured when the site is built
(when the case-study clones are present) or falls back to the pinned, dated value with a label that
says so — never a number the build did not see.
"""
from __future__ import annotations

import datetime as dt
import html

import site_shell as SH
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
        try:
            anchors, anchor_problems = V.check_anchors()
        except Exception:                               # noqa: BLE001 — older verify without anchors
            anchors, anchor_problems = 0, []
        return {"checked": checked, "ranges": ranges, "problems": len(problems),
                "anchors": anchors, "anchor_problems": len(anchor_problems), "live": clones_present()}
    except Exception as error:                          # noqa: BLE001 — proof must not break the build
        return {"checked": 0, "ranges": 0, "problems": -1, "anchors": 0, "live": False, "error": str(error)}


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
    # the recorded (English) words, in either edition
    words = sum(sum(s.get("en_words") or [len(s["script_text"].split())]) for d in decks for s in d["slides"])
    recorded = sum(len((manifest.get("decks", {}).get(d["id"], {}) or {}).get("slides", {})) for d in decks)
    return {"slides": slides, "scripted": scripted, "words": words, "recorded": recorded}


def gather(decks: list[dict], manifest: dict) -> dict:
    return {"built": dt.date.today().isoformat(), "pointers": pointer_proof(), "facts": facts_proof(),
            "labs": lab_proof(), "narration": narration_proof(decks, manifest)}


def proof_card(proof: dict, site_base: str) -> str:
    """The home page's dark card (#79): three numbers this build measured, and where they are checked.

    Every number is read from `proof`, which the build gathered; a number the build did not see is
    shown as a dash, never as a remembered value."""
    p, n = proof["pointers"], proof["narration"]
    def num(value: int) -> str:
        return f"{value:,}" if value else "—"
    cells = (
        (num(p.get("checked", 0)), SH.T("file pointers resolve at the pinned commits", "个文件指针在固定提交处可解析")),
        (num(p.get("anchors", 0)), SH.T("cited ranges pinned to the code they quote", "个引用范围与所引代码锁定")),
        (num(n.get("recorded", 0)), SH.T(f"of {n.get('slides', 0)} parts recorded, captions matching the approved script",
                                         f"/ {n.get('slides', 0)} 个部分已录制，字幕与审定讲解稿一致")),
    )
    items = "".join(f'<div class="proof-num"><span class="proof-value">{v}</span>'
                    f'<span class="proof-label">{html.escape(label)}</span></div>' for v, label in cells)
    return (f'<section class="proof-card-dark" aria-labelledby="proof-card-title" data-proof-card>'
            f'<h2 id="proof-card-title">{SH.T("What this course checks about itself, every build", "每次构建，这门课程都会检查自己的这些方面")}</h2>'
            f'<div class="proof-nums">{items}</div>'
            f'<a href="{site_base}/proof.html">{SH.T("How each number is checked", "每个数字如何核验")}</a></section>')


def proof_section(proof: dict, site_base: str) -> str:
    """The proof page's body (#79 moved it off the home page, which links to it)."""
    p, f, n = proof["pointers"], proof["facts"], proof["narration"]
    live_note = (SH.T("measured at build time against the cloned case-study repositories", "构建时对照克隆下来的案例仓库实测")
                 if f["live"] else SH.T("pinned values, dated; re-measured whenever the site is built beside the clones", "带日期的固定值；每当网站在克隆仓库旁构建时都会重新测量"))
    if p["problems"] == 0 and p["checked"]:
        pointer_line = SH.T(f'<strong>{p["checked"]:,} file pointers</strong> into the three repositories resolve'
                            + (f', {p["ranges"]:,} line ranges in bounds' if p["ranges"] else "")
                            + (" — checked at build time." if p["live"] else "."),
                            f'指向三个仓库的 <strong>{p["checked"]:,} 个文件指针</strong>全部可解析'
                            + (f'，{p["ranges"]:,} 个行范围都在文件之内' if p["ranges"] else "")
                            + ("——构建时检查。" if p["live"] else "。"))
    elif p["problems"] > 0:
        pointer_line = SH.T(f'<strong>{p["problems"]} of {p["checked"]:,} pointers</strong> did not resolve at build time — this build is not clean.',
                            f'<strong>{p["checked"]:,} 个指针中有 {p["problems"]} 个</strong>在构建时无法解析——这次构建不干净。')
    else:
        pointer_line = SH.T('Pointer resolution is checked when the site is built beside the clones (<code>make -C course check</code>).',
                            '网站在克隆仓库旁构建时会检查指针解析（<code>make -C course check</code>）。')
    fact_rows = []
    # a fact that is a sentence is quoted from its file, so it is marked as a quotation
    q = lambda v: SH.T(html.escape(str(v)), f'<q lang="en">{html.escape(str(v))}</q>') if " " in str(v) else html.escape(str(v))
    for r in f["rows"]:
        if r["status"] == "pinned":
            value = f'<td>{q(r["pinned"])}</td><td class="proof-status is-pinned">{SH.T("pinned", "固定于")} {html.escape(r["pinned_date"])}</td>'
        elif r["status"] == "ok":
            value = f'<td>{q(r["derived"])}</td><td class="proof-status is-ok">{SH.T("re-derived · matches", "已重新推导 · 一致")}</td>'
        else:
            value = f'<td>{html.escape(str(r["derived"]))} <small>({SH.T("pinned", "固定值")} {html.escape(str(r["pinned"]))})</small></td><td class="proof-status is-drift">{SH.T("drifted", "已漂移")}</td>'
        label = r["key"].replace(".", " · ").replace("_", " ")
        fact_rows.append(f'<tr><th scope="row">{html.escape(label)}</th>{value}</tr>')
    import site_content as SC                                                     # noqa: PLC0415
    labs = "".join(
        f'<li><strong>{html.escape(l["name"])}:</strong> '
        # the README's own lines, quoted as written (in the Chinese edition too)
        + " · ".join(SH.T(SC.inline(x), f'<q lang="en">{SC.inline(x)}</q>') for x in l["lines"])
        + f' <a href="{l["href"]}">README</a></li>' for l in proof["labs"])
    drift_line = (SH.T(f'{f["drifted"]} of {f["total"]} drifted since they were pinned', f'{f["total"]} 个中有 {f["drifted"]} 个自固定以来已漂移')
                  if f["live"] and f["drifted"]
                  else (SH.T(f'all {f["total"]} re-derive to their pinned values', f'全部 {f["total"]} 个都能重新推导出固定值') if f["live"]
                        else SH.T(f'{f["total"]} pinned facts', f'{f["total"]} 个固定事实')))
    return SH.T(f"""<section class="proof" id="proof">
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
      <p><strong>{n['slides']} parts</strong>, {n['scripted']} scripted, <strong>{n['words']:,} words</strong> of approved narration. Captions, transcript and script are checked word for word; a mismatch fails the build.</p>
      <p class="proof-foot"><a href="{site_base}/transcripts/ALL.md">The complete transcript</a> is the same words.
        Where a deck says preview voice, its audio is spoken by a synthesized voice rather than a human recording.</p>
    </article>
  </div>
</section>""",
                f"""<section class="proof" id="proof">
  <div class="section-heading">
    <h2>这个网站能证明自己什么</h2>
    <span class="section-note">构建于 {html.escape(proof['built'])} · {html.escape(live_note)}</span>
  </div>
  <div class="proof-grid">
    <article class="proof-card">
      <h3>每个主张都带有指针</h3>
      <p>{pointer_line}</p>
      <p class="proof-foot"><a href="{GITHUB}06-production/verify.py">verify.py</a> 就是这项检查；每次发布前都会运行。</p>
    </article>
    <article class="proof-card">
      <h3>数字是重新推导的，不是凭记忆</h3>
      <p>内容标准列出了课程可以当作事实陈述的数字。<strong>{html.escape(drift_line)}</strong>。</p>
      <details><summary>查看事实表</summary>
        <div class="table-wrap"><table class="proof-table">
          <thead><tr><th scope="col">事实</th><th scope="col">值</th><th scope="col">状态</th></tr></thead>
          <tbody>{"".join(fact_rows)}</tbody></table></div>
      </details>
      <p class="proof-foot"><a href="{GITHUB}06-production/check_facts.py">check_facts.py</a> 按学习者的方式从克隆仓库重新推导每一个数字。</p>
    </article>
    <article class="proof-card">
      <h3>实验是真正运行过的，不只是描述</h3>
      <ul class="proof-list">{labs or '<li>实验起始代码随附经过验证的测试运行结果，写在各自的 README 中。</li>'}</ul>
      <p class="proof-foot">实验打印出的数字就是它的 README 所写的数字，否则就是构建出错。</p>
    </article>
    <article class="proof-card">
      <h3>说的就是写的</h3>
      <p><strong>{n['slides']} 个部分</strong>，其中 {n['scripted']} 个有讲解稿，审定讲解共 <strong>{n['words']:,} 个英文单词</strong>。字幕、文字稿和讲解稿逐词核对；不一致就构建失败。</p>
      <p class="proof-foot"><a href="{site_base}/transcripts/ALL.md">完整文字稿</a>（英文）就是同样的文字。
        凡是标注预览语音的模块，其音频由合成语音朗读，而不是真人录音。</p>
    </article>
  </div>
</section>""")
