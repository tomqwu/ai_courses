#!/usr/bin/env python3
"""Lab M6 edition manifest: every claim in an edition, with its source, level and hash, signed.

Usage:
    python3 edition_manifest.py build BRIEFING.md --edition 1.0.0 [--base-url URL] [--out FILE]
    python3 edition_manifest.py check BRIEFING.md MANIFEST.json
    python3 edition_manifest.py sign MANIFEST.json --key PRIVATE_KEY [--signer EMAIL]
    python3 edition_manifest.py verify MANIFEST.json --signer EMAIL --allowed-signers FILE
    python3 edition_manifest.py --selftest

build   reads the briefing's provenance table (the Lab M6 template: a Markdown table whose header
        names a claim column and a source column) and writes one record per row: id, claim,
        source, retrieved, level, epistemic label and a SHA-256 of those fields. It refuses a row
        with no claim, no level, no ISO retrieval date, or a source that is neither a URL nor a
        backticked pointer with a line anchor -- the same citation forms selfcheck.py accepts.
        The output has no timestamp, so the same briefing and edition always give the same bytes.
check   rebuilds the records from the briefing and compares them with the manifest. Any claim
        added, removed or changed since that edition exits 1: publish a new edition, never
        rewrite the old one ("An existing published edition is never overwritten",
        `ai_qe/CONTRIBUTING.md`).
sign    runs `ssh-keygen -Y sign` and writes MANIFEST.json.sig next to the manifest. It needs
        OpenSSH 8.1 or later; `ssh -V` prints yours. If Windows' own is older, Git for Windows
        ships its own ssh-keygen under usr\\bin. With --signer it also writes allowed_signers
        beside the manifest (EMAIL and the public key from PRIVATE_KEY.pub), the file readers
        pass to verify. The script writes it because shell redirection cannot be trusted to:
        Windows PowerShell 5.1's `>` writes UTF-16, which ssh-keygen cannot read.
verify  runs `ssh-keygen -Y verify` against an allowed-signers file, feeding the manifest on
        stdin itself, so the same command works in PowerShell, which has no `<` redirection.

Why this shape: AI engines cite a page, not a claim, and they often cite it wrongly, so each claim
gets a stable id and, with --base-url, a permalink per claim and per edition. The hash lets anyone
holding the manifest see which claims a later edition changed; the signature lets them see that
you issued it. Neither says a claim is true -- a signed wrong number is still wrong, which is why
the provenance table and selfcheck.py come first. stdlib only; Python 3.11.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FORMAT = "aps-edition-manifest/1"
NAMESPACE = "aps-edition"      # ssh-keygen -Y signing namespace; sign and verify must agree
EXAMPLES = Path(__file__).resolve().parent / "selfcheck-examples"

POINTER_RE = re.compile(r"`[A-Za-z0-9_.-]+/[^`\s]+:\d+(?:-\d+)?`")
URL_RE = re.compile(r"https?://\S+")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EDITION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PLACEHOLDERS = {"", "…", "...", "-", "—", "tbd", "todo", "?"}

FIELDS = ("claim", "source", "retrieved", "level", "label")


class ManifestError(Exception):
    """The briefing cannot be turned into an edition as it stands."""


def _cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def _column_map(header: list[str]) -> dict[str, int] | None:
    """Map field -> column index from the header, or None if this is not a provenance table."""
    cols: dict[str, int] = {}
    for i, name in enumerate(h.lower() for h in header):
        if name in ("#", "id", "row"):
            cols.setdefault("row", i)
        elif "claim" in name and "type" not in name:
            cols.setdefault("claim", i)
        elif "source" in name:
            cols.setdefault("source", i)
        elif "retrieved" in name:
            cols.setdefault("retrieved", i)
        elif "level" in name:
            cols.setdefault("level", i)
        elif "epistemic" in name or name == "label":
            cols.setdefault("label", i)
    return cols if {"claim", "source"} <= cols.keys() else None


def provenance_rows(text: str) -> list[tuple[int, dict[str, str]]]:
    """Return (line number, fields) for each row of the first provenance table in the text."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.lstrip().startswith("|") or not re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            continue
        cols = _column_map(_cells(line))
        if cols is None:
            continue
        rows = []
        for n in range(i + 2, len(lines)):
            if not lines[n].lstrip().startswith("|"):
                break
            cells = _cells(lines[n])
            fields = {f: (cells[c] if c < len(cells) else "") for f, c in cols.items()}
            rows.append((n + 1, fields))
        return rows
    raise ManifestError("no provenance table found: need a Markdown table with Claim and Source columns")


def _missing(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDERS


def record(fields: dict[str, str], position: int) -> tuple[dict[str, str], list[str]]:
    """Build one claim record and list what is wrong with it."""
    rec = {f: " ".join(fields.get(f, "").split()) for f in FIELDS}
    row = fields.get("row", "").strip() or str(position)
    rec = {"id": f"claim-{row}", **rec}
    problems = []
    if _missing(rec["claim"]):
        problems.append("no claim")
    if not (URL_RE.search(rec["source"]) or POINTER_RE.search(rec["source"])):
        problems.append("source is not a URL or a `path:line` pointer")
    if not DATE_RE.match(rec["retrieved"]):
        problems.append("retrieved is not a YYYY-MM-DD date")
    if _missing(rec["level"]):
        problems.append("no level")
    payload = json.dumps({f: rec[f] for f in FIELDS}, sort_keys=True, ensure_ascii=False)
    rec["sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return rec, problems


def build(text: str, edition: str, file_name: str, base_url: str | None = None) -> dict:
    if not EDITION_RE.match(edition):
        raise ManifestError(f"edition {edition!r} must be letters, digits, dots, dashes or underscores")
    claims, errors, seen = [], [], set()
    for position, (line, fields) in enumerate(provenance_rows(text), start=1):
        rec, problems = record(fields, position)
        if rec["id"] in seen:
            problems.append(f"duplicate id {rec['id']}")
        seen.add(rec["id"])
        if problems:
            errors.append(f"line {line} ({rec['id']}): " + "; ".join(problems))
        if base_url:
            rec["permalink"] = f"{base_url.rstrip('/')}/#{rec['id']}"
        claims.append(rec)
    if not claims:
        raise ManifestError("the provenance table has no rows")
    if errors:
        raise ManifestError("refusing to issue an edition with unsourced rows:\n  " + "\n  ".join(errors))
    digest = hashlib.sha256("".join(c["sha256"] for c in claims).encode("ascii")).hexdigest()
    return {"format": FORMAT, "edition": edition, "file": file_name, "claims": claims,
            "claims_sha256": digest}


def dumps(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def compare(text: str, manifest: dict) -> list[str]:
    """Differences between the briefing now and the edition the manifest records."""
    if manifest.get("format") != FORMAT:
        return [f"not an {FORMAT} manifest"]
    listed = manifest.get("claims", [])
    digest = hashlib.sha256("".join(c.get("sha256", "") for c in listed).encode("ascii")).hexdigest()
    if digest != manifest.get("claims_sha256"):
        return ["the manifest's claims_sha256 does not match its own claims: it was edited by hand"]
    then = {c["id"]: c for c in listed}
    now = {}
    for position, (_, fields) in enumerate(provenance_rows(text), start=1):
        rec, _ = record(fields, position)
        now[rec["id"]] = rec
    diffs = []
    for cid, rec in now.items():
        if cid not in then:
            diffs.append(f"{cid}: added")
        elif rec["sha256"] != then[cid]["sha256"]:
            changed = [f for f in FIELDS if rec[f] != then[cid].get(f)]
            diffs.append(f"{cid}: changed ({', '.join(changed)})")
    diffs += [f"{cid}: removed" for cid in then if cid not in now]
    return diffs


def _ssh_keygen() -> str:
    exe = shutil.which("ssh-keygen")
    if not exe:
        raise ManifestError("ssh-keygen not found. macOS: built in. Windows: Settings > Optional features "
                            "> OpenSSH Client, or use the one in Git for Windows (usr\\bin). Linux: openssh-client.")
    return exe


def sign(manifest_path: Path, key: Path, signer: str | None = None) -> int:
    key = key.expanduser()
    cmd = [_ssh_keygen(), "-Y", "sign", "-f", str(key), "-n", NAMESPACE, str(manifest_path)]
    code = subprocess.run(cmd, check=False).returncode
    if code == 0 and signer:
        pub = key.with_name(key.name + ".pub").read_text(encoding="utf-8").strip()
        allowed = manifest_path.with_name("allowed_signers")
        allowed.write_text(f"{signer} {pub}\n", encoding="ascii", newline="\n")
        print(f"wrote {allowed}: {signer} is the one allowed signer")
    return code


def verify(manifest_path: Path, signer: str, allowed: Path, sig: Path | None = None) -> int:
    sig = sig or manifest_path.with_name(manifest_path.name + ".sig")
    cmd = [_ssh_keygen(), "-Y", "verify", "-f", str(allowed.expanduser()), "-I", signer,
           "-n", NAMESPACE, "-s", str(sig)]
    with manifest_path.open("rb") as data:
        return subprocess.run(cmd, stdin=data, check=False).returncode


def selftest() -> int:
    """Build, check, tamper and (where ssh-keygen exists) sign the bundled examples."""
    good, bad = EXAMPLES / "good.md", EXAMPLES / "bad.md"
    ok = True

    def report(passed: bool, what: str) -> None:
        nonlocal ok
        ok &= passed
        print(f"[{'PASS' if passed else 'FAIL'}] {what}")

    text = good.read_text(encoding="utf-8")
    manifest = build(text, "1.0.0", good.name, "https://example.com/briefing/1.0.0")
    report(len(manifest["claims"]) == 6 and dumps(manifest) == dumps(build(text, "1.0.0", good.name,
           "https://example.com/briefing/1.0.0")), f"build {good.name}: 6 claims, same bytes twice")
    report(compare(text, manifest) == [], f"check {good.name} against its own edition: no changes")
    edited = text.replace("took 19% longer", "took 20% longer", 1)
    diffs = compare(edited, manifest)
    report(diffs == ["claim-1: changed (claim)"], f"one number edited: {diffs}")
    forged = json.loads(dumps(manifest))
    forged["claims"][0]["claim"] = "AI-allowed issues took 20% longer"
    forged["claims"][0]["sha256"] = "0" * 64
    report(compare(text, forged)[0].startswith("the manifest's claims_sha256"), "hand-edited manifest: refused")
    try:
        build(bad.read_text(encoding="utf-8"), "1.0.0", bad.name)
        report(False, f"build {bad.name}: should refuse rows 2 and 3")
    except ManifestError as exc:
        refused = re.findall(r"\((claim-\d+)\)", str(exc))
        report(refused == ["claim-2", "claim-3"], f"build {bad.name}: refused {refused}")

    if not shutil.which("ssh-keygen"):
        print("[SKIP] sign and verify: ssh-keygen not on PATH")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            key, man = d / "edition_key", d / "manifest.json"
            man.write_text(dumps(manifest), encoding="utf-8")
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "selftest@example.com",
                            "-f", str(key)], check=True)
            pub = (d / "edition_key.pub").read_text(encoding="utf-8").strip()
            (d / "allowed_signers").write_text(f"selftest@example.com {pub}\n", encoding="utf-8")
            quiet = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
            signed = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", str(key), "-n", NAMESPACE, str(man)],
                                    check=False, **quiet).returncode == 0
            good_sig = signed and subprocess.run(
                ["ssh-keygen", "-Y", "verify", "-f", str(d / "allowed_signers"), "-I", "selftest@example.com",
                 "-n", NAMESPACE, "-s", str(man) + ".sig"], stdin=man.open("rb"), check=False, **quiet).returncode == 0
            man.write_text(dumps(forged), encoding="utf-8")
            bad_sig = subprocess.run(
                ["ssh-keygen", "-Y", "verify", "-f", str(d / "allowed_signers"), "-I", "selftest@example.com",
                 "-n", NAMESPACE, "-s", str(man) + ".sig"], stdin=man.open("rb"), check=False, **quiet).returncode
            report(good_sig and bad_sig != 0, "signature: verifies as issued, fails once the manifest changes")

    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    if argv[0] == "--selftest":
        return selftest()
    parser = argparse.ArgumentParser(prog="edition_manifest.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("briefing", type=Path)
    b.add_argument("--edition", required=True)
    b.add_argument("--base-url")
    b.add_argument("--out", type=Path)
    c = sub.add_parser("check")
    c.add_argument("briefing", type=Path)
    c.add_argument("manifest", type=Path)
    s = sub.add_parser("sign")
    s.add_argument("manifest", type=Path)
    s.add_argument("--key", type=Path, required=True)
    s.add_argument("--signer")
    v = sub.add_parser("verify")
    v.add_argument("manifest", type=Path)
    v.add_argument("--signer", required=True)
    v.add_argument("--allowed-signers", type=Path, required=True)
    v.add_argument("--sig", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.cmd == "build":
            manifest = build(args.briefing.read_text(encoding="utf-8"), args.edition, args.briefing.name,
                             args.base_url)
            out = args.out or args.briefing.with_name(f"manifest-{args.edition}.json")
            if out.exists() and out.read_text(encoding="utf-8") != dumps(manifest):
                print(f"{out} already exists with different claims. A published edition is never "
                      "overwritten: choose a new --edition.")
                return 1
            out.write_text(dumps(manifest), encoding="utf-8")
            print(f"wrote {out}: edition {args.edition}, {len(manifest['claims'])} claims, "
                  f"claims_sha256 {manifest['claims_sha256'][:12]}")
            return 0
        if args.cmd == "check":
            manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
            diffs = compare(args.briefing.read_text(encoding="utf-8"), manifest)
            if not diffs:
                print(f"{args.briefing.name} matches edition {manifest['edition']}: "
                      f"{len(manifest['claims'])} claims unchanged")
                return 0
            print(f"{args.briefing.name} no longer matches edition {manifest.get('edition')}:")
            for d in diffs:
                print(f"  {d}")
            print("Build a new edition for these changes; do not rewrite the published one.")
            return 1
        if args.cmd == "sign":
            return sign(args.manifest, args.key, args.signer)
        return verify(args.manifest, args.signer, args.allowed_signers, args.sig)
    except (ManifestError, OSError, json.JSONDecodeError) as exc:
        print(f"edition_manifest.py: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
