#!/usr/bin/env python3
"""Screenshot copies for figures (#100), with provenance.

A `kind: screenshot` figure shows a real product image. The image is never drawn, cropped or
edited: it is copied byte for byte from a case-study repo at the commit the course pins, and the
copy is recorded in course/figures/manifest.json (name, repo, path, commit, sha256). Callouts are
drawn over it by the page, never into it. `verify.py` (Figures) re-checks every entry.

    python3 course/06-production/figures_shots.py copy SignUpFlow/docs/screenshots/current/basketball/1440/dashboard.png --as signupflow-dashboard.png
    python3 course/06-production/figures_shots.py verify

The commit is the one `.github/workflows/gate.yml` clones the repo at, so a copy always matches
the code the course cites.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # course/
REPO = ROOT.parent                                  # workspace (holds the cloned repos)
FIGURES = ROOT / "figures"
SHOTS = FIGURES / "shots"
MANIFEST = FIGURES / "manifest.json"
GATE = REPO / ".github" / "workflows" / "gate.yml"
KINDS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}


def pins() -> dict[str, str]:
    """{repo: full commit} from the gate's clone lines — the commits the course is verified at."""
    found = dict(re.findall(r"^\s*clone (\S+) ([0-9a-f]{7,40})\s*$", GATE.read_text(encoding="utf-8"), re.M))
    out = {}
    for repo, short in found.items():
        full = subprocess.run(["git", "-C", str(REPO / repo), "rev-parse", f"{short}^{{commit}}"],
                              capture_output=True, text=True)
        out[repo] = full.stdout.strip() if full.returncode == 0 else short
    return out


def load() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"shots": []}


def save(data: dict) -> None:
    data["shots"].sort(key=lambda e: e["name"])
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def blob(repo: str, commit: str, path: str) -> bytes:
    proc = subprocess.run(["git", "-C", str(REPO / repo), "show", f"{commit}:{path}"], capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"{repo}/{path} is not in {repo} at {commit[:12]}: {proc.stderr.decode().strip()}")
    return proc.stdout


def copy(pointer: str, name: str | None) -> None:
    repo, _, path = pointer.partition("/")
    commits = pins()
    if repo not in commits:
        raise SystemExit(f"{repo}: not a pinned case-study repo ({', '.join(commits)})")
    if Path(path).suffix.lower() not in KINDS:
        raise SystemExit(f"{path}: a screenshot is one of {', '.join(sorted(KINDS))}")
    name = name or f"{repo.lower()}-{Path(path).name}"
    data = blob(repo, commits[repo], path)
    SHOTS.mkdir(parents=True, exist_ok=True)
    (SHOTS / name).write_bytes(data)
    manifest = load()
    manifest["shots"] = [e for e in manifest["shots"] if e["name"] != name]
    manifest["shots"].append({"name": name, "repo": repo, "path": path, "commit": commits[repo],
                              "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    save(manifest)
    print(f"copied {repo}/{path}@{commits[repo][:7]} -> course/figures/shots/{name} ({len(data):,} bytes)")


def verify() -> int:
    sys.path.insert(0, str(ROOT / "06-production"))
    import verify as V                                                         # noqa: PLC0415
    count, problems = V.check_figure_manifest()
    for p in problems:
        print(f"  ✗ {p}")
    print(f"screenshots: {count} copies", "match their origin" if not problems else f"— {len(problems)} problem(s)")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("copy", help="copy <Repo>/<path> at the pinned commit into course/figures/shots/")
    c.add_argument("pointer")
    c.add_argument("--as", dest="name")
    sub.add_parser("verify", help="re-check every manifest entry against its origin")
    args = parser.parse_args(argv)
    if args.cmd == "copy":
        copy(args.pointer, args.name)
        return 0
    return verify()


if __name__ == "__main__":
    raise SystemExit(main())
