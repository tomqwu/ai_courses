#!/usr/bin/env python3
"""Publish the learner site to the `gh-pages` branch.

The site is generated, and the decks, the manifest and the audio are deliberately not committed to
`main`, so GitHub Pages cannot serve the repository as-is. This builds the site, stages it, and pushes
the result to `gh-pages` — the one branch where build output belongs.

The published copy is **text-first by default**: the recordings exist, but the 233 audio files are
~62 MB and are throwaway until the release voice is recorded, so the player is told there are no
recordings. That is not cosmetic — it means no Play button offers a file the copy does not contain and
nothing 404s. The decks, the full ai_qe design, every transcript and the print stylesheet all work.

    python3 course/publish_site.py                 # text-first (default)
    python3 course/publish_site.py --with-audio    # include the recordings and captions
    python3 course/publish_site.py --dry-run       # build and stage, do not push

The gate (`course/check.sh`) runs first and the publish is refused unless it is green: a deploy is the
last place to discover the site is broken.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COURSE = Path(__file__).resolve().parent
REPO = COURSE.parent
SITE = COURSE / "learner-site"

# Everything the pages need that build_site.py does not emit itself.
STATIC_ASSETS = ("player.css", "player.js", "narration-media.js")
AUDIO_DIR = SITE / "assets" / "audio"


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise SystemExit(f"command failed ({' '.join(cmd)}):\n{detail}")
    return result


def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], cwd=cwd or REPO, check=check)


def clear_directory(path: Path) -> None:
    """Empty a directory, keeping the worktree's .git file."""
    for child in path.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def stage_site(stage: Path, with_audio: bool) -> None:
    args = [sys.executable, str(SITE / "build_site.py"), "--out", str(stage)]
    if not with_audio:
        args.append("--no-narration")
    print(f"· building {'with audio' if with_audio else 'text-first'}")
    run(args, cwd=SITE)

    assets = stage / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for name in STATIC_ASSETS:
        shutil.copy2(SITE / "assets" / name, assets / name)
    shutil.copytree(SITE / "assets" / "fonts", assets / "fonts", dirs_exist_ok=True)

    if with_audio:
        if not AUDIO_DIR.is_dir():
            raise SystemExit(f"--with-audio: {AUDIO_DIR} does not exist. "
                             f"Run `make -C course narration-preview` first.")
        shutil.copytree(AUDIO_DIR, assets / "audio", dirs_exist_ok=True)

    # Without this, GitHub runs the files through Jekyll first.
    (stage / ".nojekyll").write_text("", encoding="utf-8")


def publish(stage: Path, branch: str, remote: str, dry_run: bool, message: str) -> bool:
    """Commit the staged site onto `branch` and push it. Returns True if something was pushed."""
    git("fetch", remote, branch, check=False)
    has_branch = git("rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{branch}",
                     check=False).returncode == 0
    base = f"{remote}/{branch}" if has_branch else "HEAD"

    work = Path(tempfile.mkdtemp(prefix="aps-publish-"))
    try:
        git("worktree", "add", "--detach", str(work), base)
        if not has_branch:
            git("checkout", "--orphan", branch, cwd=work)
        clear_directory(work)
        shutil.copytree(stage, work, dirs_exist_ok=True)
        git("add", "-A", cwd=work)
        status = git("status", "--porcelain", cwd=work)
        if has_branch and not status.stdout.strip():
            print("· nothing changed since the last publish")
            return False
        git("commit", "-m", message, cwd=work)
        if dry_run:
            print(f"· dry run — a commit is staged on {branch} but was not pushed")
            return False
        git("push", "--force", remote, f"HEAD:refs/heads/{branch}")
        return True
    finally:
        git("worktree", "remove", "--force", str(work), check=False)
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--with-audio", action="store_true",
                        help="include the recordings and captions (~62 MB) so narration plays")
    parser.add_argument("--dry-run", action="store_true", help="build and stage, do not push")
    parser.add_argument("--skip-verify", action="store_true",
                        help="do not run course/check.sh first (not recommended)")
    parser.add_argument("--branch", default="gh-pages", help="deploy branch (default gh-pages)")
    parser.add_argument("--remote", default="origin", help="git remote (default origin)")
    args = parser.parse_args(argv)

    if not args.skip_verify:
        print("· running the gate before publishing")
        gate = subprocess.run(["bash", str(COURSE / "check.sh")], capture_output=True, text=True)
        if gate.returncode != 0:
            tail = "\n".join((gate.stdout or "").strip().splitlines()[-15:])
            raise SystemExit(f"refusing to publish: the gate is not green\n{tail}")
        print("· gate green")

    stage = Path(tempfile.mkdtemp(prefix="aps-site-stage-"))
    try:
        stage_site(stage, args.with_audio)
        files = sum(1 for p in stage.rglob("*") if p.is_file())
        size = sum(p.stat().st_size for p in stage.rglob("*") if p.is_file())
        print(f"· staged {files} files, {size / 1_048_576:.1f} MB")

        source = git("rev-parse", "--short", "HEAD").stdout.strip()
        mode = "with the recordings" if args.with_audio else "text-first, no recordings"
        message = (f"Publish the learner site from {source}\n\n"
                   f"Published copy: {mode}.\n"
                   f"Generated by course/publish_site.py — do not edit this branch by hand.\n")
        pushed = publish(stage, args.branch, args.remote, args.dry_run, message)
    finally:
        shutil.rmtree(stage, ignore_errors=True)

    owner_repo = git("remote", "get-url", args.remote).stdout.strip()
    slug = owner_repo.removesuffix(".git").split(":")[-1].split("github.com/")[-1]
    owner, _, name = slug.partition("/")
    url = f"https://{owner}.github.io/{name}/"

    if pushed:
        print(f"\nPushed to {args.remote}/{args.branch}.")
        print(f"  site: {url}")
    print("\nIf Pages is not enabled yet, turn it on once:")
    print(f"  gh api -X POST repos/{owner}/{name}/pages "
          f"-f 'source[branch]={args.branch}' -f 'source[path]=/'")
    print("  (or Settings → Pages → Deploy from a branch → "
          f"{args.branch} / (root))")
    if not args.with_audio:
        print("\nThis copy is text-first, so Play narration is off and no audio is fetched.")
        print("  add the recordings later with: python3 course/publish_site.py --with-audio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
