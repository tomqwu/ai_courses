#!/usr/bin/env python3
"""Tests for the certificate issuer: `python3 test_issue_certificate.py`.

Every test runs against a temporary issuer and temporary files, so no test can touch a real
certificate or the real issuer key. The failure paths matter more than the happy one — a credential
that cannot be shown failing proves nothing — so tampering with either file, revoking, and issuing
twice each have a test.
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

import unittest.mock                     # noqa: E402

import issue_certificate as IC             # noqa: E402

try:                                        # Ed25519 lives in `cryptography`; the rest is stdlib.
    import cryptography                     # noqa: F401
    HAVE_CRYPTO = True
except ImportError:                         # pragma: no cover
    HAVE_CRYPTO = False

RECORD = {
    "student_name": "Ada Example", "track": "cohort", "labs_passed": 8, "quiz_average": 88,
    "capstone_score": 91, "capstone_product_name": "MeetingLedger", "archetype": "on-device AI app",
    "evidence_log_ref": "docs/evidence/2026-09-17.md", "head_sha": "abc1234def",
    "award_date": "2026-09-17",
}


def quiet(fn, *args) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


@unittest.skipUnless(HAVE_CRYPTO, "needs `cryptography` for Ed25519: python3 -m pip install cryptography")
class CertificateTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.certs = root / "certificates"
        self.site = root / "verify"
        for name, value in (("CERTS", self.certs), ("KEY_PATH", self.certs / "issuer-key.json"),
                            ("DID_PATH", self.certs / "issuer-did.json"),
                            ("STATUS_PATH", self.certs / "status-list.json"), ("SITE_VERIFY", self.site)):
            patcher = unittest.mock.patch.object(IC, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.record_path = root / "award.json"
        self.record_path.write_text(json.dumps(RECORD), encoding="utf-8")
        self.addCleanup(self.tmp.cleanup)
        quiet(IC.main, ["keygen"])

    def issue(self, **overrides) -> str:
        if overrides:
            self.record_path.write_text(json.dumps({**RECORD, **overrides}), encoding="utf-8")
        quiet(IC.main, ["issue", "--record", str(self.record_path)])
        return "APS-0001"


class TestKeys(CertificateTestCase):
    def test_keygen_writes_a_private_key_that_is_git_ignored_and_a_public_did(self):
        self.assertTrue(IC.KEY_PATH.is_file())
        self.assertIn("issuer-key.json", (self.certs / ".gitignore").read_text())
        did = json.loads(IC.DID_PATH.read_text())["id"]
        self.assertTrue(did.startswith("did:key:z6Mk"), did)

    def test_keygen_refuses_to_overwrite_without_force(self):
        before = IC.KEY_PATH.read_text()
        self.assertEqual(quiet(IC.main, ["keygen"]), 1)
        self.assertEqual(IC.KEY_PATH.read_text(), before)
        self.assertEqual(quiet(IC.main, ["keygen", "--force"]), 0)
        self.assertNotEqual(IC.KEY_PATH.read_text(), before)

    def test_base58_round_trips_and_rejects_junk(self):
        for raw in (b"\x00\x01\x02", bytes(range(32)), b"\x00" * 4 + b"\xff"):
            self.assertEqual(IC.b58_decode(IC.b58(raw)), raw)
        with self.assertRaises(IC.IssueError):
            IC.b58_decode("0OIl")


class TestIssue(CertificateTestCase):
    def test_a_signed_credential_verifies_and_carries_the_evidence(self):
        cert_id = self.issue()
        credential = json.loads((self.certs / f"{cert_id}.jsonld").read_text())
        results = {r["resultDescription"]: r["value"] for r in credential["credentialSubject"]["result"]}
        self.assertEqual(results["labs_passed"], "8/8")
        self.assertEqual(results["quiz_average"], "88%")
        self.assertIn("abc1234def", credential["evidence"][0]["narrative"])
        self.assertIn("OpenBadgeCredential", credential["type"])
        self.assertEqual(quiet(IC.main, ["verify", str(self.certs / f"{cert_id}.jsonld")]), 0)

    def test_the_verification_page_is_written_beside_the_site(self):
        cert_id = self.issue()
        page = (self.site / f"{cert_id}.html").read_text()
        self.assertIn("Ada Example", page)
        self.assertIn("abc1234def", page)
        self.assertIn(json.loads(IC.DID_PATH.read_text())["id"], page)

    def test_an_incomplete_record_is_refused_by_name(self):
        self.record_path.write_text(json.dumps({"student_name": "No Evidence"}), encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(IC.main(["issue", "--record", str(self.record_path)]), 2)
        self.assertIn("labs_passed", err.getvalue())

    def test_issuing_a_certificate_id_twice_needs_force(self):
        self.record_path.write_text(json.dumps({**RECORD, "certificate_id": "APS-0001"}), encoding="utf-8")
        self.assertEqual(quiet(IC.main, ["issue", "--record", str(self.record_path)]), 0)
        self.assertEqual(quiet(IC.main, ["issue", "--record", str(self.record_path)]), 2)
        self.assertEqual(quiet(IC.main, ["issue", "--record", str(self.record_path), "--force"]), 0)

    def test_ids_increment_across_awards(self):
        self.issue()
        self.record_path.write_text(json.dumps({**RECORD, "student_name": "Grace Example"}), encoding="utf-8")
        quiet(IC.main, ["issue", "--record", str(self.record_path)])
        self.assertTrue((self.certs / "APS-0002.jsonld").is_file())


class TestVerify(CertificateTestCase):
    def test_editing_the_json_after_issuance_is_caught(self):
        cert_id = self.issue()
        path = self.certs / f"{cert_id}.jsonld"
        credential = json.loads(path.read_text())
        credential["credentialSubject"]["result"][2]["value"] = "100"
        path.write_text(json.dumps(credential, indent=2))
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(IC.main(["verify", str(path)]), 2)
        self.assertIn("does not match what was signed", err.getvalue())

    def test_a_tampered_signature_payload_does_not_verify(self):
        cert_id = self.issue()
        header, payload, signature = (self.certs / f"{cert_id}.jws").read_text().strip().split(".")
        credential = json.loads(IC.b64u_decode(payload))
        credential["credentialSubject"]["result"][0]["value"] = "8/8 (edited)"
        forged = IC.b64u(IC.canonical(credential))
        with self.assertRaises(IC.IssueError) as ctx:
            IC.verify_jws(f"{header}.{forged}.{signature}")
        self.assertIn("signature does not verify", str(ctx.exception))

    def test_a_credential_from_another_issuer_does_not_verify_here(self):
        cert_id = self.issue()
        jws = (self.certs / f"{cert_id}.jws").read_text().strip()
        quiet(IC.main, ["keygen", "--force"])          # new issuer, same repository
        IC.verify_jws(jws)                             # still verifies: the key is inside the credential
        header, payload, signature = jws.split(".")
        other = IC.b64u(IC.canonical(json.loads(IC.b64u_decode(payload)) | {"issuer": {"id": "did:key:z6MkjunK"}}))
        with self.assertRaises(IC.IssueError):
            IC.verify_jws(f"{header}.{other}.{signature}")

    def test_a_missing_signature_file_is_refused_rather_than_assumed_valid(self):
        cert_id = self.issue()
        (self.certs / f"{cert_id}.jws").unlink()
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(IC.main(["verify", str(self.certs / f"{cert_id}.jsonld")]), 2)
        self.assertIn("no signature beside", err.getvalue())


class TestRevoke(CertificateTestCase):
    def test_a_revoked_certificate_still_verifies_but_reports_revoked(self):
        cert_id = self.issue()
        quiet(IC.main, ["revoke", cert_id, "--reason", "auto-fail found post-issuance"])
        entry = json.loads(IC.STATUS_PATH.read_text())["certificates"][cert_id]
        self.assertEqual(entry["status"], "revoked")
        self.assertEqual(quiet(IC.main, ["verify", str(self.certs / f"{cert_id}.jsonld")]), 1)
        IC.verify_jws((self.certs / f"{cert_id}.jws").read_text().strip())   # signature is untouched

    def test_stale_is_separate_from_revoked(self):
        cert_id = self.issue()
        quiet(IC.main, ["revoke", cert_id, "--reason", "capstone source moved", "--stale"])
        self.assertEqual(json.loads(IC.STATUS_PATH.read_text())["certificates"][cert_id]["status"], "stale")

    def test_the_verification_page_is_rewritten_with_the_new_status(self):
        cert_id = self.issue()
        quiet(IC.main, ["revoke", cert_id, "--reason", "specimen"])
        self.assertIn("revoked", (self.site / f"{cert_id}.html").read_text())

    def test_revoking_an_unknown_certificate_is_an_error(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(IC.main(["revoke", "APS-9999", "--reason", "typo"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
