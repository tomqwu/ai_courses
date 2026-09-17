# Certificate of Completion — Template & Issuance Rules

The course awards a certificate on **evidence**, not attendance. This file is the template plus the
rules an instructor or automated checker follows, so two graders reach the same verdict.

## Award thresholds

Taken from [`../01-design/assessment-and-rubrics.md`](../01-design/assessment-and-rubrics.md):

| Component | Weight | Requirement |
|---|---|---|
| Module labs (M0–M7) | 60% | **All 8 labs passed** — each with its evidence log (red run before green, commands, outcomes, date, environment, limitations) |
| Module quizzes (M0–M8) | 20% | **≥ 75% average** across the 9 quizzes |
| Capstone (M8 lab) | 20% | **≥ 80%** against the 5-dimension rubric |

All three conditions must hold. A high quiz average does not compensate for a missing lab: the labs are
where the evidence discipline lives.

## Auto-fail conditions

Regardless of scores, no certificate is issued if any of these is true (mirrors the `auto-fail` lists in
each module's `lab-rubrics.md`):

- Evidence was fabricated, back-dated, or copied from another student.
- A "green run" is claimed with no recorded red run for that lab.
- Tests were weakened, skipped, or deleted to make a gate pass.
- The capstone demo was never run, or the recorded demo does not match the submitted artifact.
- Any repo claim in the submission cites a file path that does not exist.

## Template

> ### Certificate of Completion
> **AI Product Studio — Build, Ship & Sell 3 Types of AI Products**
>
> Awarded to **{{student_name}}**
>
> for completing all nine modules and shipping one product through the full Spec-to-Ship Loop with
> recorded evidence.
>
> **Verified evidence**
> - Module labs (M0–M7): {{labs_passed}}/8 passed
> - Module quizzes: {{quiz_average}}% average ({{quizzes_taken}}/9 taken)
> - Capstone: {{capstone_score}}/100 — {{capstone_product_name}} ({{archetype}})
> - Evidence log: {{evidence_log_ref}} · final commit: `{{head_sha}}`
>
> **Track completed:** {{track}} — self-paced / cohort ({{cohort_name}})
>
> Awarded {{award_date}} · Instructor: Tom Wu
>
> Verify this certificate: {{verification_ref}}

## Issuance procedure

1. **Collect** the evidence log, the capstone repository (with the head SHA recorded), and the quiz results.
2. **Recompute** the three thresholds from the artifacts — never from the student's summary of them.
3. **Run the auto-fail list.** Any hit stops issuance and triggers a re-submission conversation, not a
   partial certificate.
4. **Spot-check pointers.** Take 5 repo file pointers from the submission at random and confirm each
   resolves. This mirrors the drift checks the course teaches in M4 and takes under two minutes.
5. **Issue and record.** `python3 issue_certificate.py issue --record award.json` signs the award,
   writes the credential and its verification page, and appends the row to the issuance log below.
6. **Invalidate on change.** If the capstone source changes after issuance, the certificate's SHA no longer
   matches and the record is marked stale — the same rule the course teaches for validation evidence
   (M1/M5).

## The credential: what a stranger can check without asking you

A certificate that lives only in a Markdown table is a claim about a claim. `issue_certificate.py`
signs each award as an **Open Badges 3.0 credential** — a W3C Verifiable Credential signed with
Ed25519 — so the award verifies without this repository's cooperation and without an account
anywhere.

```bash
python3 issue_certificate.py keygen                       # once: the issuer key pair
python3 issue_certificate.py issue --record award.json    # sign one award
python3 issue_certificate.py verify certificates/APS-0001.jsonld
python3 issue_certificate.py revoke APS-0001 --reason "auto-fail found post-issuance"
python3 issue_certificate.py status                       # the issuance log, from the records
```

Each issuance writes three files: the credential (`certificates/APS-0001.jsonld`), its detached
signature (`.jws`), and a verification page under the learner site. The award record it signs is the
one the issuance procedure above recomputed — the three thresholds, the evidence log reference and
the capstone head SHA — so the signature covers the evidence, not just the name.

Four properties are worth stating plainly, because they are what make the credential worth more than
the table:

- **The public key is inside the credential.** The issuer is a `did:key` identifier that carries its
  own Ed25519 public key, so verification needs no directory, no server and nothing from this site.
- **Editing either file is caught.** Changing the JSON after issuance fails verification against the
  signature; changing the signed payload fails the signature itself.
- **Revocation is public and separate from validity.** `status-list.json` records `valid`, `stale`
  (the capstone source moved) or `revoked` (an auto-fail found later). A revoked credential still
  verifies cryptographically and reports as revoked, which is the honest pair of facts.
- **The private key is never committed.** `certificates/.gitignore` excludes it, and `keygen`
  refuses to overwrite one without `--force`, since every credential signed with the old key would
  stop verifying.

`certificates/award.example.json` is the record format. `python3 test_issue_certificate.py` covers
all of it, including the tampering and revocation paths; the gate runs those tests.

## Issuance log format

Keep this beside the certificate records so an awarded certificate is auditable:

| Certificate ID | Student | Track | Cohort | Labs | Quiz avg | Capstone | Head SHA | Awarded | Credential | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| APS-0001 | _name_ | _self-paced / cohort_ | _— / cohort name_ | 8/8 | 88% | 91 | `abc1234` | 2026-01-15 | `APS-0001.jsonld` | valid |

`python3 issue_certificate.py status` prints this table from the signed records, so the log and the
credentials cannot disagree.

**Status values:** `valid` · `stale (source changed)` · `revoked (auto-fail found post-issuance)`.

## Why a SHA on a certificate

The course's own case studies hold releases back when the evidence does not support promotion
(ListenToMe's 1.3.0 was held at 97.24% coverage per
`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md`; ai_qe never overwrites a published
edition). A certificate that names the exact commit it certifies is the same discipline applied to
student work: the claim is bounded to the artifact it was true of.
