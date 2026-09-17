#!/usr/bin/env python3
"""Issue the completion certificate as a signed, machine-verifiable credential.

`certificate.md` binds an award to the capstone's commit SHA, which is the right idea and, until
now, unenforceable: the SHA sat in a Markdown table anyone could edit. This issues the same award as
an Open Badges 3.0 credential — a W3C Verifiable Credential signed with Ed25519 — so a reader can
check the signature and the SHA without asking the issuer anything.

    python3 issue_certificate.py keygen                      # once: the issuer's key pair
    python3 issue_certificate.py issue --record award.json   # sign one award
    python3 issue_certificate.py verify certificates/APS-0001.jsonld
    python3 issue_certificate.py revoke APS-0001 --reason "auto-fail found post-issuance"
    python3 issue_certificate.py status                      # the issuance log, from the records

What is signed is what `certificate.md` says is awarded: the three thresholds, the evidence log
reference and the capstone head SHA. Change the capstone source after issuance and the SHA in the
credential no longer matches the repository — the credential stays valid and the *claim* it makes is
visibly about a commit that has moved on, which is the honest outcome and the one the course teaches.

The issuer key never leaves the machine that holds it. The public half is published as a `did:key`
identifier inside every credential, so verification needs no server, no directory and no account.

Needs `cryptography` (`python3 -m pip install cryptography`) for Ed25519. Everything else is
standard library, and the verifier refuses rather than guesses when anything is missing.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

PROD = Path(__file__).resolve().parent
COURSE = PROD.parent
CERTS = PROD / "certificates"
KEY_PATH = CERTS / "issuer-key.json"            # private; git-ignored
DID_PATH = CERTS / "issuer-did.json"            # public; committed
STATUS_PATH = CERTS / "status-list.json"        # public; committed
SITE_VERIFY = COURSE / "learner-site" / "verify"
COURSE_URL = "https://github.com/tomqwu/ai_courses"

CONTEXT = [
    "https://www.w3.org/ns/credentials/v2",
    "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json",
]
ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class IssueError(RuntimeError):
    pass


def _ed25519():
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519   # noqa: PLC0415
    except ImportError as error:                                        # pragma: no cover
        raise IssueError("this command needs the `cryptography` package: "
                         "python3 -m pip install cryptography") from error
    return ed25519


def b58(data: bytes) -> str:
    """base58btc, the encoding `did:key` uses. Leading zero bytes become leading '1's."""
    number = int.from_bytes(data, "big")
    out = bytearray()
    while number:
        number, remainder = divmod(number, 58)
        out.append(ALPHABET[remainder])
    for byte in data:
        if byte:
            break
        out.append(ALPHABET[0])
    return bytes(reversed(out)).decode()


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def b64u_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def did_key(public_bytes: bytes) -> str:
    """did:key for an Ed25519 public key: multicodec 0xed01, then base58btc with a 'z' prefix."""
    return "did:key:z" + b58(b"\xed\x01" + public_bytes)


def load_key() -> tuple[object, str]:
    ed25519 = _ed25519()
    if not KEY_PATH.is_file():
        raise IssueError(f"no issuer key at {KEY_PATH}. Run: python3 issue_certificate.py keygen")
    stored = json.loads(KEY_PATH.read_text(encoding="utf-8"))
    private = ed25519.Ed25519PrivateKey.from_private_bytes(b64u_decode(stored["d"]))
    return private, stored["did"]


def canonical(payload: dict) -> bytes:
    """The exact bytes that get signed. Sorted keys, no spare whitespace, so it re-serializes."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


# ---------------------------------------------------------------- commands

def cmd_keygen(args) -> int:
    ed25519 = _ed25519()
    CERTS.mkdir(parents=True, exist_ok=True)
    if KEY_PATH.exists() and not args.force:
        print(f"refusing to overwrite {KEY_PATH} — every credential signed with the old key would "
              f"stop verifying. Pass --force only if you mean that.", file=sys.stderr)
        return 1
    private = ed25519.Ed25519PrivateKey.generate()
    raw_private = private.private_bytes_raw()
    raw_public = private.public_key().public_bytes_raw()
    did = did_key(raw_public)
    KEY_PATH.write_text(json.dumps({
        "_warning": "PRIVATE KEY. Never commit this file. certificates/.gitignore excludes it.",
        "kty": "OKP", "crv": "Ed25519", "d": b64u(raw_private), "x": b64u(raw_public), "did": did,
    }, indent=2), encoding="utf-8")
    KEY_PATH.chmod(0o600)
    DID_PATH.write_text(json.dumps({
        "id": did,
        "verificationMethod": [{"id": f"{did}#{did.split(':')[-1]}", "type": "Multikey",
                                "controller": did, "publicKeyMultibase": did.split(":")[-1]}],
        "assertionMethod": [f"{did}#{did.split(':')[-1]}"],
        "_note": "The public half of the issuer key. Committed on purpose: it is what verifies a "
                 "certificate, and publishing it is what makes verification need no server.",
    }, indent=2), encoding="utf-8")
    gitignore = CERTS / ".gitignore"
    gitignore.write_text("# The private issuer key never leaves the machine that signed with it.\n"
                         "issuer-key.json\n", encoding="utf-8")
    print(f"issuer key written to {KEY_PATH} (mode 600, git-ignored)")
    print(f"public identifier   {did}")
    return 0


def build_credential(record: dict, did: str, cert_id: str, issued: str) -> dict:
    """The award, as an Open Badges 3.0 AchievementCredential."""
    subject_id = record.get("student_id") or f"urn:aps:student:{hashlib.sha256(record['student_name'].encode()).hexdigest()[:16]}"
    return {
        "@context": CONTEXT,
        "id": f"urn:uuid:{hashlib.sha256((cert_id + issued).encode()).hexdigest()[:8]}-{cert_id.lower()}",
        "type": ["VerifiableCredential", "OpenBadgeCredential"],
        "issuer": {"id": did, "type": ["Profile"], "name": record.get("issuer_name", "AI Product Studio"),
                   "url": COURSE_URL},
        "validFrom": issued,
        "credentialSubject": {
            "id": subject_id,
            "type": ["AchievementSubject"],
            "identifier": [{"type": "IdentityObject", "identityType": "name",
                            "hashed": False, "identityHash": record["student_name"]}],
            "achievement": {
                "id": f"{COURSE_URL}#aps-completion",
                "type": ["Achievement"],
                "name": "AI Product Studio — Build, Ship & Sell 3 Types of AI Products",
                "description": ("Completed all nine modules and shipped one product through the full "
                                "Spec-to-Ship Loop with recorded evidence."),
                "criteria": {"id": f"{COURSE_URL}/blob/main/course/06-production/certificate.md",
                             "narrative": ("All 8 labs passed with evidence logs, quiz average at or above "
                                           "75 percent across 9 quizzes, capstone at or above 80 against the "
                                           "5-dimension rubric, and no auto-fail condition found.")},
            },
            # The evidence is the point: each number is the one the issuance procedure recomputed
            # from the artifacts, and the SHA bounds the claim to the commit it was true of.
            "result": [
                {"type": ["Result"], "resultDescription": "labs_passed", "value": f"{record['labs_passed']}/8"},
                {"type": ["Result"], "resultDescription": "quiz_average", "value": f"{record['quiz_average']}%"},
                {"type": ["Result"], "resultDescription": "capstone_score", "value": str(record["capstone_score"])},
            ],
        },
        "evidence": [{
            "id": record.get("capstone_url", f"urn:aps:capstone:{record['head_sha']}"),
            "type": ["Evidence"],
            "name": record.get("capstone_product_name", "Capstone"),
            "description": (f"{record.get('archetype', 'capstone')} · evidence log "
                            f"{record.get('evidence_log_ref', 'recorded with the submission')}"),
            "genre": record.get("track", "self-paced"),
            "narrative": f"Certified at commit {record['head_sha']}.",
        }],
        "credentialStatus": {
            "id": f"{COURSE_URL}/blob/main/course/06-production/certificates/status-list.json#{cert_id}",
            "type": "AchievementCredentialStatus", "certificateId": cert_id,
        },
    }


def sign(credential: dict, private, did: str) -> str:
    """A compact JWS over the credential — the enveloping proof form of VC-JOSE-COSE."""
    header = {"alg": "EdDSA", "typ": "vc+jwt", "kid": f"{did}#{did.split(':')[-1]}"}
    signing_input = f"{b64u(canonical(header))}.{b64u(canonical(credential))}".encode()
    return f"{signing_input.decode()}.{b64u(private.sign(signing_input))}"


def verify_jws(jws: str) -> dict:
    """Verify a credential's signature against the DID inside it. Raises on any mismatch."""
    ed25519 = _ed25519()
    try:
        header_b64, payload_b64, signature_b64 = jws.split(".")
    except ValueError as error:
        raise IssueError("not a compact JWS: expected three dot-separated segments") from error
    header = json.loads(b64u_decode(header_b64))
    credential = json.loads(b64u_decode(payload_b64))
    if header.get("alg") != "EdDSA":
        raise IssueError(f"unexpected algorithm {header.get('alg')!r}; this issuer signs with EdDSA")
    did = credential.get("issuer", {}).get("id", "")
    if not did.startswith("did:key:z"):
        raise IssueError(f"issuer is not a did:key identifier: {did!r}")
    multibase = did.split(":")[-1]
    if header.get("kid") != f"{did}#{multibase}":
        raise IssueError("the key id in the header does not name the credential's issuer")
    decoded = b58_decode(multibase[1:])
    if decoded[:2] != b"\xed\x01":
        raise IssueError("the issuer identifier does not carry an Ed25519 key")
    public = ed25519.Ed25519PublicKey.from_public_bytes(decoded[2:])
    try:
        public.verify(b64u_decode(signature_b64), f"{header_b64}.{payload_b64}".encode())
    except Exception as error:                                          # noqa: BLE001
        raise IssueError("signature does not verify — the credential was altered or is not this issuer's") from error
    return credential


def b58_decode(text: str) -> bytes:
    number = 0
    for char in text.encode():
        index = ALPHABET.find(char)
        if index < 0:
            raise IssueError(f"not base58btc: {chr(char)!r}")
        number = number * 58 + index
    body = number.to_bytes((number.bit_length() + 7) // 8, "big")
    pad = len(text) - len(text.lstrip("1"))
    return b"\x00" * pad + body


def read_status() -> dict:
    if STATUS_PATH.is_file():
        return json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    return {"_note": "Certificate status. A credential is only as good as the issuer's willingness "
                     "to revoke it; this file is that willingness, in public.",
            "issuer": "", "updated": "", "certificates": {}}


def write_status(status: dict) -> None:
    status["updated"] = dt.date.today().isoformat()
    STATUS_PATH.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")


def verification_page(credential: dict, cert_id: str, jws: str, status_entry: dict) -> str:
    subject = credential["credentialSubject"]
    results = {r["resultDescription"]: r["value"] for r in subject["result"]}
    evidence = credential["evidence"][0]
    name = subject["identifier"][0]["identityHash"]
    state = status_entry.get("status", "valid")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Certificate {cert_id} — AI Product Studio</title>
<link rel="stylesheet" href="../assets/player.css">
</head>
<body class="doc-body" data-site-base="..">
<main class="doc-main">
<article class="doc">
<h1>Certificate {cert_id}</h1>
<p class="doc-lede">Awarded to <strong>{name}</strong> · status <strong>{state}</strong></p>
<table>
<tbody>
<tr><th scope="row">Labs passed</th><td>{results.get('labs_passed', '—')}</td></tr>
<tr><th scope="row">Quiz average</th><td>{results.get('quiz_average', '—')}</td></tr>
<tr><th scope="row">Capstone</th><td>{results.get('capstone_score', '—')} — {evidence['name']}</td></tr>
<tr><th scope="row">Capstone commit</th><td><code>{evidence['narrative'].split()[-1].rstrip('.')}</code></td></tr>
<tr><th scope="row">Issued</th><td>{credential['validFrom'][:10]}</td></tr>
<tr><th scope="row">Issuer</th><td><code>{credential['issuer']['id']}</code></td></tr>
</tbody>
</table>
<h2>Verify it yourself</h2>
<p>The signature is over the credential below, made with the issuer's Ed25519 key. The public half is
inside the identifier, so checking it needs nothing from this site and no account anywhere.</p>
<pre><code>python3 course/06-production/issue_certificate.py verify course/06-production/certificates/{cert_id}.jsonld</code></pre>
<p>Any verifier that reads a compact JWS and a <code>did:key</code> identifier will do; this one is
here so a reader who has the repository can check without installing anything but one library.</p>
<h2>The credential</h2>
<details><summary>Signed credential (JWS)</summary><pre><code>{jws}</code></pre></details>
<details><summary>Credential (JSON)</summary><pre><code>{json.dumps(credential, indent=2)}</code></pre></details>
<p class="doc-foot">A certificate names the commit it certifies. If the capstone source has moved on
since, this credential still verifies and still describes that commit — which is the point.</p>
</article>
</main>
</body>
</html>
"""


def cmd_issue(args) -> int:
    record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    for field in ("student_name", "labs_passed", "quiz_average", "capstone_score", "head_sha"):
        if field not in record:
            raise IssueError(f"the award record is missing {field!r}")
    private, did = load_key()
    status = read_status()
    cert_id = record.get("certificate_id") or f"APS-{len(status['certificates']) + 1:04d}"
    if cert_id in status["certificates"] and not args.force:
        raise IssueError(f"{cert_id} has already been issued; pass --force to re-issue it")
    issued = record.get("award_date") or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if len(issued) == 10:
        issued += "T00:00:00Z"

    credential = build_credential(record, did, cert_id, issued)
    jws = sign(credential, private, did)
    CERTS.mkdir(parents=True, exist_ok=True)
    (CERTS / f"{cert_id}.jsonld").write_text(json.dumps(credential, indent=2) + "\n", encoding="utf-8")
    (CERTS / f"{cert_id}.jws").write_text(jws + "\n", encoding="utf-8")

    status["issuer"] = did
    status["certificates"][cert_id] = {
        "status": "valid", "student": record["student_name"], "issued": issued[:10],
        "head_sha": record["head_sha"], "track": record.get("track", "self-paced"),
        "credential": f"{cert_id}.jsonld", "credential_id": credential["id"],
    }
    write_status(status)

    SITE_VERIFY.mkdir(parents=True, exist_ok=True)
    (SITE_VERIFY / f"{cert_id}.html").write_text(
        verification_page(credential, cert_id, jws, status["certificates"][cert_id]), encoding="utf-8")

    print(f"issued {cert_id}")
    print(f"  credential   course/06-production/certificates/{cert_id}.jsonld")
    print(f"  signature    course/06-production/certificates/{cert_id}.jws")
    print(f"  verify page  course/learner-site/verify/{cert_id}.html")
    print(f"  issuer       {did}")
    return 0


def cmd_verify(args) -> int:
    path = Path(args.credential)
    if not path.is_file():
        raise IssueError(f"no such credential: {path}")
    jws_path = path.with_suffix(".jws")
    if not jws_path.is_file():
        raise IssueError(f"no signature beside the credential: {jws_path}")
    jws = jws_path.read_text(encoding="utf-8").strip()
    credential = verify_jws(jws)
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    if canonical(on_disk) != canonical(credential):
        raise IssueError(f"{path.name} does not match what was signed — the JSON file was edited "
                         f"after issuance; the signed credential inside the JWS is the record")
    cert_id = credential["credentialStatus"]["certificateId"]
    entry = read_status()["certificates"].get(cert_id, {})
    state = entry.get("status", "unknown")
    subject = credential["credentialSubject"]
    print(f"signature    valid (EdDSA, {credential['issuer']['id']})")
    print(f"certificate  {cert_id} — {subject['identifier'][0]['identityHash']}")
    print(f"awarded      {credential['validFrom'][:10]} · commit "
          f"{credential['evidence'][0]['narrative'].split()[-1].rstrip('.')}")
    print(f"status       {state}" + (f" — {entry['reason']}" if entry.get("reason") else ""))
    if state == "revoked":
        return 1
    if state == "unknown":
        print("             (not in this repository's status list — check you have the issuer's copy)")
        return 1
    return 0


def cmd_revoke(args) -> int:
    status = read_status()
    if args.certificate not in status["certificates"]:
        raise IssueError(f"{args.certificate} is not in the status list")
    entry = status["certificates"][args.certificate]
    entry["status"] = "revoked" if not args.stale else "stale"
    entry["reason"] = args.reason
    entry["changed"] = dt.date.today().isoformat()
    write_status(status)
    page = SITE_VERIFY / f"{args.certificate}.html"
    if page.is_file():
        jws = (CERTS / f"{args.certificate}.jws").read_text(encoding="utf-8").strip()
        credential = json.loads((CERTS / f"{args.certificate}.jsonld").read_text(encoding="utf-8"))
        page.write_text(verification_page(credential, args.certificate, jws, entry), encoding="utf-8")
    print(f"{args.certificate} marked {entry['status']}: {args.reason}")
    return 0


def cmd_status(args) -> int:
    status = read_status()
    certificates = status.get("certificates", {})
    if not certificates:
        print("no certificates issued yet")
        return 0
    print(f"issuer {status.get('issuer', '—')} · updated {status.get('updated', '—')}\n")
    print(f"{'ID':<10} {'Student':<24} {'Track':<12} {'Commit':<10} {'Issued':<11} Status")
    for cert_id, entry in sorted(certificates.items()):
        print(f"{cert_id:<10} {entry['student'][:23]:<24} {entry.get('track', '—')[:11]:<12} "
              f"{entry['head_sha'][:9]:<10} {entry['issued']:<11} {entry['status']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_key = sub.add_parser("keygen", help="generate the issuer key pair (once)")
    p_key.add_argument("--force", action="store_true", help="overwrite an existing key (invalidates every credential)")
    p_key.set_defaults(func=cmd_keygen)

    p_issue = sub.add_parser("issue", help="sign one award record into a credential")
    p_issue.add_argument("--record", required=True, help="the award record JSON (see award.example.json)")
    p_issue.add_argument("--force", action="store_true", help="re-issue a certificate id that already exists")
    p_issue.set_defaults(func=cmd_issue)

    p_verify = sub.add_parser("verify", help="check a credential's signature and status")
    p_verify.add_argument("credential", help="path to a .jsonld credential (its .jws must sit beside it)")
    p_verify.set_defaults(func=cmd_verify)

    p_revoke = sub.add_parser("revoke", help="mark a certificate revoked or stale")
    p_revoke.add_argument("certificate", help="certificate id, e.g. APS-0001")
    p_revoke.add_argument("--reason", required=True)
    p_revoke.add_argument("--stale", action="store_true", help="mark stale (source moved) rather than revoked")
    p_revoke.set_defaults(func=cmd_revoke)

    p_status = sub.add_parser("status", help="print the issuance log from the records")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except IssueError as error:
        print(f"issue_certificate: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
