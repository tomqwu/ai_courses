# Solutions M3 — Harden, Prove, Position

> Reference answers for Lab M3; the runnable reference is
> `course/03-content/m02-ondevice-app/tinycopilot/`. Counts match Content Standards §0.2:
> `make lab-m3` → **49 passed**; `make lab-m2` → **201 passed, 100% coverage**; `make e2e` →
> **2 passed** on a live daemon.

## Step 0 — Park the shipped solution

`make m3-start` moves `src/tinycopilot/privacy.py`, `tests/test_privacy.py` and
`tests/test_contract_real_llm.py` into `.m3-solution/` and sets `COV_FLOOR` to 0. The red run that
follows is a collection error, not failing tests, because `src/tinycopilot/__init__.py:28-34`
re-exports the privacy module. Verified:

```text
$ make m3-start   # -> "Lab M3 starting state: parked ... COV_FLOOR is now 0."
$ make lab-m3
ImportError while loading conftest 'tests/conftest.py'.
src/tinycopilot/__init__.py:28: in <module>
    from .privacy import (
E   ModuleNotFoundError: No module named 'tinycopilot.privacy'
make: *** [Makefile:29: lab-m3] Error 4
```

`make lab-m2` is red the same way until Step 1 restores the five names. **Grading note:** a Step 0
red of "49 failed" is fabricated; the honest one is exit 4, zero tests run.

## Step 1 — Privacy hardening, TDD-style

A complete submission has four defenses in `src/tinycopilot/privacy.py` (`PrivacyMode`,
`verify_local_model`, `assert_host_local`, `guard_request`), redirect refusal in the transport
(`httpx_transport(..., reject_redirects=True)` plus an explicit 3xx raise), and a `FakeTransport`
test each — no network, no daemon.

**Red-team test first** — write it before the implementation and record the red run.

```python
REMOTE_ALIAS_SHOW = {"remote_host": "https://ollama.com", "remote_model": "glm-5.3",
                     "details": {"format": "gguf"}, "model_info": {"a": 1}}

def test_remote_host_in_show_metadata_is_rejected_locally():
    ok, reason = verify_local_model(BASE_URL, "glm-5.3:cloud", transport=show_transport(REMOTE_ALIAS_SHOW))
    assert ok is False
    assert "cloud alias" in reason
    assert "send the transcript and context off this device" in reason
```

After Step 0 the red comes in three shapes as the student works inward, any of them a valid
capture: the Step 0 `ModuleNotFoundError`; with a stub `privacy.py` and no test file,
`ERROR: file or directory not found: tests/test_privacy.py` (exit 4); then, against a stub
returning `(True, ...)`, an assertion failure — verified:

```text
F..................                                                      [100%]
>       assert ok is False
E       assert True is False
FAILED tests/test_privacy.py::test_remote_host_in_show_metadata_is_rejected_locally
1 failed, 18 passed in 0.03s
make: *** [Makefile:29: lab-m3] Error 1
```

(The 18 are `test_ollama_provider.py`, also run by `make lab-m3`.) The reference adds a subtler
variant: no `remote_host` but an *empty* `details.format` — what a real `:cloud` alias returns
(`CLOUD_ALIAS_SHOW`, `tests/test_privacy.py:34-37`). It must fail too, naming `details.format`
and `fails closed`.

**Expected outcome per defense:**

| Defense | Mocked payload | Assertion |
|---|---|---|
| Cloud alias rejected | `REMOTE_ALIAS_SHOW` above | `ok is False`; reason contains `cloud alias` |
| Missing metadata fails closed | `{"model_info": {"a": 1}}` (no `details`), then `{"details": {"format": "gguf"}}` (no `model_info`) | `ok is False`; reason names the absent key |
| Non-loopback host rejected | `assert_host_local("https://ollama.example.com")` | raises `PrivacyViolation`, matches `loopback` |
| 3xx refused at both layers | `FakeTransport(status=302)` on `/api/chat`; client built `follow_redirects=False` | raises `ServerError` matching `redirect`; kwarg captured as `False` |

A passing case needs a downloaded model's shape —
`{"details": {"format": "gguf", "family": "qwen3"}, "model_info": {"general.architecture": "qwen3"}}`
→ `(True, "verified local: format='gguf', 1 model_info keys, no remote_host or remote_model")`.

```bash
make lab-m3
# 49 passed in 0.03s      <- timing varies, the count does not
```

**Common wrong answers.** (1) Checking `remote_host` and forgetting `remote_model` — a keyword
match, not a metadata rule. (2) Treating a missing `details` key as acceptable: fail-open, the
anti-pattern the module teaches against. (3) String-matching the URL for `"localhost"`, which
accepts `http://localhost.evil.com`; parse the hostname and compare against
`{"localhost", "127.0.0.1", "::1"}`. (4) Catching the redirect *after* the body is read — the text
has already left.

**Grading note.** A real pass records the red run *before* the green one and names the defense in
each reason string; a fake deletes the assertion, or asserts only the exception type.

## Step 2 — Real-LLM contract test

`tests/test_contract_real_llm.py` uses `pytest.mark.skipif(not os.environ.get("LAB_E2E"), reason=...)`
and sends a real completion through *your* `OllamaProvider`, asserting non-empty content plus an
expected keyword. Run it both ways:

```bash
pytest tests/test_contract_real_llm.py -q
# 2 skipped   (reason: set LAB_E2E=1 ...)

LAB_E2E=1 pytest tests/test_contract_real_llm.py -q
# 2 passed
```

**A cloud-only daemon does not stop this test.** It runs in the provider's default mode on
whatever model `role_defaults(fetch_models(...))` picks, `:cloud` included: its only claim is that
request shape, streaming parse and error typing hold against a real daemon
(`tinycopilot/README.md`, "Verified status"). Both daemon states give the same evidence. Weakening
Step 1 so local-only mode accepts a cloud alias is the wrong answer.

**Common wrong answers.** Posting to the daemon directly rather than through `OllamaProvider`
(tests nothing of your code); asserting only that the call returns (an empty stream passes);
hard-coding a model instead of using the router's auto-selection; gating on local-only mode so a
cloud-only daemon skips it; substituting a mocked stream — a mock cannot prove the seam.

**Grading note.** The reference `make e2e` prints **2 passed**, not more, and both tests must run
through provider code rather than a reimplementation.

## Step 3 — Coverage floor

Step 0 rewrote `COV_FLOOR ?= 90` to `0`; set it back. `lab-m2` already passes
`--cov=src/tinycopilot --cov-fail-under=$(COV_FLOOR)` (in your own project, this is where you add
those two flags). Prove it bites:

```bash
python -m pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=90 -q   # one module skipped
# ERROR: Coverage failure: total of 78.26 is less than fail-under=90   <- exit 1, value varies

make lab-m2                                                            # after restoring
# 201 passed, 2 deselected in 0.08s
# Required test coverage of 90% reached. Total coverage: 100.00%
```

The percentage varies with the module you skip; the *shape* does not — a non-zero exit naming the
floor, then a green run after restoration.

**Common wrong answers.** Only the success run; `--cov-fail-under=90` on a target that emits no
coverage data, so the floor silently never applies; leaving `COV_FLOOR` at `m3-start`'s 0;
deleting tests and lowering the floor to "pass."

**Grading note.** Both runs, with exit codes. A single green run fails regardless of percentage.

## Step 4 — Comparison table

`docs/competition.md` needs ≥5 competitors you have used or visited, ≥6 columns (platform,
on-device, privacy, model choice, price, focus), a source URL or `unverified` in every cell,
uncertainty qualified as in `ListenToMe/docs/competition-analysis.md:3` ("approximately",
"reportedly"), and a one-liner whose clauses each name a column — imitate
`ListenToMe/docs/competition-analysis.md:70-80`.

**Common wrong answers.** Prices from memory; a one-liner of adjectives ("powerful, modern,
private") with no column behind any word; five rows of one shape (five bot-joiners), which cannot
support a wedge.

**Grading note.** Open one row's source URL at random. If the cell does not match the page, treat
every other cell as suspect.

## Step 5 — Tag and checksum the artifact

Run 2026-09-17 on a copy of `tinycopilot/` initialised as its own repository. These are the shapes
a log must show; SHA and digest are the student's.

```bash
git tag -a v0.1.0 -m "Lab M3: privacy hardening, contract test, coverage floor"
git describe --tags --exact-match   # v0.1.0
git rev-parse v0.1.0^{commit}       # 232d172bf044b1a70bfaae5c4c81eb35718f51c5  <- yours differs

python3 -m build   # Successfully built tinycopilot-0.1.0.tar.gz and ...-py3-none-any.whl
python3 -m zipfile -l dist/tinycopilot-0.1.0-py3-none-any.whl | grep privacy
# tinycopilot/privacy.py    2026-09-17 19:25:24    7504

cd dist && sha256sum tinycopilot-0.1.0-py3-none-any.whl | tee SHA256SUMS
# 4fecc4dd9ee336a3a9d46e45fab7fd623ffef842a0823d4303b852fb142bdd29  tinycopilot-0.1.0-py3-none-any.whl

# in a fresh directory holding only the copied wheel + SHA256SUMS
sha256sum -c SHA256SUMS
# tinycopilot-0.1.0-py3-none-any.whl: OK                        exit 0
printf x >> tinycopilot-0.1.0-py3-none-any.whl && sha256sum -c SHA256SUMS
# tinycopilot-0.1.0-py3-none-any.whl: FAILED
# sha256sum: WARNING: 1 computed checksum did NOT match         exit 1
```

`shasum -a 256` prints the same digest and the same `OK`/`FAILED` lines, its warning prefixed
`shasum:`; use whichever your machine has.

**What varies.** The commit SHA, and the digest: the wheel's `.dist-info` entries carry the build
time, so rebuilding the same commit gave `937b1f72…` where the first gave `4fecc4dd…`. So you
checksum the artifact you ship, never recompute it later — and a digest identical to one above, or
to a classmate's, is a copy. Fixed: the names (`0.1.0` from `pyproject.toml`), the `OK`/`FAILED`
lines, the exit codes.

**Common wrong answers.** (1) Writing the manifest from the repo root, so it names `dist/…` and
`-c` elsewhere reports `FAILED open or read` — a path bug that reads as corruption. (2) Tagging
after a further commit, so `git describe --tags --exact-match` exits 128 with `fatal: no tag exactly matches`.
(3) Re-checking the file in place, when the rule is the *downloaded* copy against the local one
(`ListenToMe/docs/RELEASING.md:33-36`). (4) Logging "released v0.1.0" with nothing pushed or
downloaded — the honest rung is *candidate* (`ListenToMe/AGENTS.md:80-82`).

**Grading note.** Ask for the `FAILED` line. A student who ran the check has one; one who pasted a
digest cannot reproduce it.

## Self-check table

| Criterion | Self-verification |
|---|---|
| Step 0 red recorded | `make lab-m3` after `make m3-start`: `ModuleNotFoundError`, exit 4, zero tests run |
| Red-team test green | `make lab-m3` shows 49 passed, the cloud-alias test among them |
| Fail-closed on missing metadata | `details` absent → `ok is False` |
| Non-loopback host rejected | `assert_host_local("http://example.com:11434")` raises `PrivacyViolation` |
| Redirects refused | `FakeTransport(status=302)` raises `ServerError` matching `redirect` |
| Contract test gated | No `LAB_E2E`: 2 skipped with a reason; with it: 2 passed on the router's pick |
| Daemon case documented | Evidence names local-model or only-`:cloud` for Step 1 |
| Coverage floor bites | `COV_FLOOR ?= 90` restored; failure run exit 1; success run ≥90% |
| Table sourced | Every cell a URL or `unverified`; uncertain claims qualified |
| One-liner falsifiable | Each clause annotated with its column |
| Tag and checksum recorded | `git describe --tags --exact-match` → `v0.1.0`; `-c` on the copy → `OK`, corrupted copy → `FAILED`; rung logged *candidate* |
