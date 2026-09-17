#!/usr/bin/env python3
"""Tests for the three tools. Standard library only: `python3 test_aps_tools.py`.

Each test builds a small repository in a temporary directory and asserts on what the tool reports,
including the failures — a checker that cannot be shown failing is not evidence of anything.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agents_audit as AA            # noqa: E402
import facts_drift as FD             # noqa: E402
import pointer_lint as PL            # noqa: E402


def quiet(fn, *args) -> int:
    """Run a tool's main() without letting its report land in the test output."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class TestPointerLint(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write(self.root, "src/app.py", "\n".join(f"line {i}" for i in range(1, 51)))
        self.addCleanup(self.tmp.cleanup)

    def test_a_pointer_that_resolves_is_counted_not_reported(self):
        write(self.root, "docs/guide.md", "See `src/app.py:10-20` and `src/app.py`.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertEqual(report["problems"], [])
        self.assertEqual(report["pointers"], 2)
        self.assertEqual(report["ranges"], 1)

    def test_a_missing_file_is_reported_with_its_line(self):
        write(self.root, "docs/guide.md", "intro\nSee `src/gone.py:3`.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertEqual(len(report["problems"]), 1)
        self.assertEqual(report["problems"][0]["line"], 2)
        self.assertIn("no such file", report["problems"][0]["problem"])

    def test_a_range_past_the_end_of_the_file_is_reported(self):
        write(self.root, "docs/guide.md", "See `src/app.py:45-60`.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertIn("outside 1-50", report["problems"][0]["problem"])

    def test_a_range_on_a_directory_is_reported(self):
        write(self.root, "docs/guide.md", "See `src/pkg:1-2`.")
        (self.root / "src" / "pkg").mkdir(parents=True, exist_ok=True)
        report = PL.lint([self.root / "docs"], self.root)
        self.assertIn("directory", report["problems"][0]["problem"])

    def test_multiple_ranges_in_one_pointer_are_each_checked(self):
        self.assertEqual(PL.parse_ranges("73-81, 99"), [(73, 81), (99, 99)])
        write(self.root, "docs/guide.md", "See `src/app.py:10-20, 90`.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertEqual(report["ranges"], 2)
        self.assertEqual(len(report["problems"]), 1)

    def test_roots_limit_which_pointers_are_linted(self):
        write(self.root, "docs/guide.md", "`other/thing.py:1` and `src/app.py:1`")
        report = PL.lint([self.root / "docs"], self.root, roots={"src"})
        self.assertEqual(report["pointers"], 1)
        self.assertEqual(report["problems"], [])

    def test_routes_slugs_and_timezones_are_not_mistaken_for_pointers(self):
        write(self.root, "docs/guide.md",
              "`/v1/things` and `/solutions/{id}/export` and `America/Toronto` and `owner/repo`.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertEqual(report["pointers"], 0)
        self.assertEqual(report["problems"], [])

    def test_an_extensionless_token_counts_when_it_resolves_to_a_directory(self):
        (self.root / "src" / "pkg").mkdir(parents=True, exist_ok=True)
        write(self.root, "docs/guide.md", "See `src/pkg` and `src/gone`.")
        report = PL.lint([self.root / "docs"], self.root)
        # The directory that exists was a pointer; the one that does not is indistinguishable from
        # a slug, so it is neither counted nor reported.
        self.assertEqual(report["pointers"], 1)
        self.assertEqual(report["problems"], [])

    def test_an_extensionless_token_with_a_line_reference_is_always_a_pointer(self):
        write(self.root, "docs/guide.md", "See `src/gone:3`.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertEqual(len(report["problems"]), 1)
        self.assertIn("no such file", report["problems"][0]["problem"])

    def test_code_fences_and_urls_are_not_mistaken_for_pointers(self):
        write(self.root, "docs/guide.md", "`https://example.com/a/b` is a link.")
        report = PL.lint([self.root / "docs"], self.root)
        self.assertEqual(report["problems"], [])

    def test_exit_status_is_one_when_a_pointer_fails(self):
        write(self.root, "docs/guide.md", "See `src/gone.py`.")
        self.assertEqual(quiet(PL.main, ["--base", str(self.root), str(self.root / "docs")]), 1)
        write(self.root, "docs/guide.md", "See `src/app.py`.")
        self.assertEqual(quiet(PL.main, ["--base", str(self.root), str(self.root / "docs")]), 0)


class TestFactsDrift(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write(self.root, "AGENTS.md", "\n".join(f"rule {i}" for i in range(1, 13)))
        write(self.root, "src/a.py", "one\ntwo\nthree\n")
        write(self.root, "src/b.py", "one\ntwo\n")
        write(self.root, "CHANGELOG.md", "## v2.1.0\nnotes\n## v2.0.0\n")
        write(self.root, "api/main.py", "import os\nprint('Health score')\n")
        write(self.root, "docs/table.md", "| a | b |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n")
        self.addCleanup(self.tmp.cleanup)

    def d(self, spec):
        return FD.derive(spec, self.root)

    def test_each_derivation_kind_reads_what_it_claims(self):
        self.assertEqual(self.d({"kind": "file_lines", "path": "AGENTS.md"}), 12)
        self.assertEqual(self.d({"kind": "glob_count", "glob": "src/**/*.py"}), 2)
        self.assertEqual(self.d({"kind": "glob_lines", "glob": "src/**/*.py"}), 5)
        self.assertEqual(self.d({"kind": "regex_capture", "path": "CHANGELOG.md", "pattern": r"## (v[0-9.]+)"}), "v2.1.0")
        self.assertEqual(self.d({"kind": "regex_count", "path": "AGENTS.md", "pattern": r"^rule"}), 12)
        self.assertEqual(self.d({"kind": "line_of", "path": "api/main.py", "pattern": "Health score"}), 2)
        self.assertEqual(self.d({"kind": "table_rows", "path": "docs/table.md"}), 2)

    def test_an_unknown_kind_is_refused_rather_than_guessed(self):
        with self.assertRaises(FD.DerivationError):
            self.d({"kind": "run_command", "cmd": "rm -rf /"})

    def test_a_missing_file_is_an_error_not_a_drift(self):
        rows = FD.check({"k": {"pinned": 1, "derive": {"kind": "file_lines", "path": "nope.md"}}}, self.root, [])
        self.assertEqual(rows[0]["status"], "error")

    def test_drift_lists_the_documents_that_still_print_the_old_value(self):
        write(self.root, "docs/guide.md", "intro\nThe file is 9 lines long.\n")
        facts = {"agents.lines": {"pinned": 9, "derive": {"kind": "file_lines", "path": "AGENTS.md"},
                                  "literals": ["is 9 lines"]}}
        rows = FD.check(facts, self.root, FD.doc_files([self.root / "docs"]))
        self.assertEqual(rows[0]["status"], "drift")
        self.assertEqual(rows[0]["derived"], 12)
        self.assertTrue(rows[0]["where"][0].endswith("guide.md:2"))

    def test_strict_is_what_turns_drift_into_a_failure(self):
        facts_path = self.root / "facts.json"
        facts_path.write_text(json.dumps(
            {"agents.lines": {"pinned": 9, "derive": {"kind": "file_lines", "path": "AGENTS.md"}}}), encoding="utf-8")
        args = ["--facts", str(facts_path), "--base", str(self.root)]
        self.assertEqual(quiet(FD.main, args), 0)
        self.assertEqual(quiet(FD.main, args + ["--strict"]), 1)


class TestAgentsAudit(unittest.TestCase):
    def test_a_rule_with_an_anchor_and_an_imperative_is_checkable(self):
        self.assertEqual(AA.classify("Every query MUST filter by `org_id`.")[0], "checkable")
        self.assertEqual(AA.classify("Keep `AGENTS.md` under 200 lines.")[0], "checkable")

    def test_a_hedged_rule_is_vague_and_names_the_phrase(self):
        verdict, why = AA.classify("Be careful with multi-tenancy.")
        self.assertEqual(verdict, "vague")
        self.assertEqual(why, "be careful")
        self.assertEqual(AA.classify("Where possible, prefer composition.")[0], "vague")

    def test_an_imperative_with_nothing_to_open_is_unenforced(self):
        self.assertEqual(AA.classify("You MUST write clean code.")[0], "unenforced")
        self.assertEqual(AA.classify("NEVER regress.")[0], "unenforced")

    def test_code_fences_are_not_read_as_rules(self):
        text = "# Rules\n\n- Use `x`.\n\n```\n- not a rule\n```\n\n- NEVER skip `tests/`.\n"
        self.assertEqual([r for _, r in AA.rules_in(text)], ["Use `x`.", "NEVER skip `tests/`."])

    def test_a_repeated_rule_is_reported_once_as_a_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(Path(tmp), "AGENTS.md", "- Every query MUST filter by `org_id`.\n"
                                                 "- Every query MUST filter by `org_id`.\n")
            report = AA.audit(path, 200)
        duplicates = [f for f in report["findings"] if f["verdict"] == "duplicate"]
        self.assertEqual(len(duplicates), 1)
        self.assertIn("line 1", duplicates[0]["why"])

    def test_the_line_budget_and_the_checkable_threshold_both_fail_the_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            long_file = write(Path(tmp), "AGENTS.md", "\n".join(f"- Rule {i} MUST use `x{i}.py`." for i in range(1, 21)))
            self.assertEqual(quiet(AA.main, ["--max-lines", "5", str(long_file)]), 1)
            self.assertEqual(quiet(AA.main, ["--max-lines", "50", str(long_file)]), 0)
            vague = write(Path(tmp), "VAGUE.md", "- Be careful.\n- Try to be nice.\n- Use `x.py` for parsing.\n")
            self.assertEqual(quiet(AA.main, ["--min-checkable", "0.8", str(vague)]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
