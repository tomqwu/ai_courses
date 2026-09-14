# Solutions M3 — Harden, Prove, Position

> Reference answers for Lab M3. The runnable reference lives at
> `course/03-content/m02-ondevice-app/tinycopilot/`. The tests are the spec; these are the
> answers with the expected outputs. Expected counts match Content Standards §0.2:
> `make lab-m3` → **49 passed**; `make lab-m2` → **191 passed, 100% coverage**;
> `make e2e` → **2 passed** against a live daemon.

## Step 1 — Privacy hardening, TDD-style

A complete submission contains the four defenses in `src/tinycopilot/privacy.py`
(`PrivacyMode`, `verify_local_model`, `assert_host_local`, `guard_request`), the redirect
refusal in the transport (`httpx_transport(..., reject_redirects=True)` plus an explicit 3xx
raise), and one test per defense using a `FakeTransport` — no network, no daemon.

**Red-team test first.** Write this before the implementation and record the red run.

```python
REMOTE_ALIAS_SHOW = {
    "remote_host": "https://ollama.com", "remote_model": "glm-5.3",
    "details": {"format": "gguf"}, "model_info": {"a": 1},
}

def test_remote_host_in_show_metadata_is_rejected_locally():
    ok, reason = verify_local_model(BASE_URL, "glm-5.3:cloud", transport=show_transport(REMOTE_ALIAS_SHOW))
    assert ok is False
    assert "cloud alias" in reason
    assert "send the transcript and context off this device" in reason
```

Before the fix, `verify_local_model` does not exist (or returns True), so the test fails with an
`ImportError` or an assertion failure on `ok is False`. **Expected after the fix:** pass. The
reference keeps a second, subtler variant: a payload with no `remote_host` but an *empty*
`details.format` — the shape a real `:cloud` alias returns (`CLOUD_ALIAS_SHOW` in
`tests/test_privacy.py:34-37`). It must also fail, with `"details.format"` and `"fails closed"`
in the reason.

**Expected assertion outcomes, one per required defense:**

| Defense | Mocked payload | Assertion |
|---|---|---|
| Cloud alias rejected | `{"remote_host": "https://ollama.com", "details": {"format": "gguf"}, "model_info": {"a": 1}}` | `ok is False`; reason contains `cloud alias` |
| Missing metadata fails closed | `{"model_info": {"a": 1}}` (no `details`) | `ok is False`; reason contains `details.format` |
| Also fail closed | `{"details": {"format": "gguf"}}` (no `model_info`) | `ok is False`; reason contains `model_info` |
| Non-loopback host rejected | `assert_host_local("https://ollama.example.com")` | raises `PrivacyViolation`, message matches `loopback` |
| 3xx refused | `FakeTransport(status=302, events=[])` on `/api/chat` | raises `ServerError`, message matches `redirect` |
| Redirect blocked at transport | httpx client built with `follow_redirects=False` | captured kwarg `follow_redirects is False` |

A passing metadata case needs the shape of a downloaded model, for example
`{"details": {"format": "gguf", "family": "qwen3"}, "model_info": {"general.architecture": "qwen3"}}`
→ `(True, "verified local: format='gguf', 1 model_info keys, no remote_host or remote_model")`.

**Commands and expected output:**

```bash
make lab-m3
# ................................................. [100%]
# 49 passed in 0.03s
```

Timing varies by machine; the count (49) does not.

**Common wrong answers.** (1) Checking only `"remote_host" not in info` and forgetting
`remote_model` — fails the `remote_model`-alone test; signals a keyword-match implementation
instead of a metadata rule. (2) Treating a missing `details` key as acceptable and proceeding —
this is fail-open, the exact anti-pattern the module teaches against. (3) Enforcing the host check
by string-matching the full URL for `"localhost"`, which accepts
`http://localhost.evil.com`; the correct rule parses the hostname and compares against the
allowlist `{"localhost", "127.0.0.1", "::1"}`. (4) Implementing redirect refusal by catching the
redirect *after* the body is read, so text has already left; refusal must happen before
forwarding.

**Grading note.** A real pass shows the red run recorded *before* the green run, and the failure
messages name the defense in the reason string; a plausible fake deletes the assertion or asserts
only the exception type without checking that no request was sent.

## Step 2 — Real-LLM contract test

`tests/test_contract_real_llm.py` uses `pytest.mark.skipif(not os.environ.get("LAB_E2E"), reason="set LAB_E2E=1 ...")`.
The test sends a real completion through *your* `OllamaProvider` with a fixed prompt and asserts
minimum content (non-empty and an expected keyword). Run both ways:

```bash
pytest tests/test_contract_real_llm.py -q
# 2 skipped  (reason: set LAB_E2E=1 to run the real-LLM contract test ...)

LAB_E2E=1 pytest tests/test_contract_real_llm.py -q
# 2 passed
```

**Two valid daemon outcomes.** These are not a bug and not a fixable failure:

- **A local model installed** (e.g. `qwen3:0.6b`): local-only mode accepts it and the contract
  test passes against your real daemon.
- **Only `:cloud` aliases** (e.g. `glm-5.3:cloud`): local-only mode rejects every model. This is
  the red-team scenario happening for real — fail-closed working. Document the daemon state, and
  satisfy the step by proving the contract seam with a mocked `/api/chat` NDJSON stream that runs
  through your provider's real streaming-parse path and yields deltas. Both outcomes are correct;
  weakening the checks to make the second one "pass" is the only wrong answer.

**Common wrong answers.** Calling `requests.post` directly instead of through `OllamaProvider`
(tests nothing about your code); asserting only that the call returns without exception (an empty
stream passes); hard-coding the model name and failing on machines where it is absent instead of
using the router's auto-selection.

**Grading note.** The reference `make e2e` output is **2 passed**, not more — the contract file has
two tests, and both must run through provider code, not a reimplementation.

## Step 3 — Coverage floor

Add `--cov=tinycopilot --cov-fail-under=90` to the test target. Prove it bites:

```bash
# failure run: temporarily skip one module's tests
python -m pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=90 -q
# ERROR: Coverage failure: total of 78.26 is less than fail-under=90   <- shape varies
# exit code 1

# success run after restoring
make lab-m2
# 191 passed, 2 deselected in 0.08s
# Required test coverage of 90% reached. Total coverage: 100.00%
```

The failure percentage varies with which module you skip and how large it is; the *shape* is
fixed — a non-zero exit naming the floor, then a green run after restoration.

**Common wrong answers.** Recording only the success run; setting `--cov-fail-under=90` on a
target that never emits coverage data (the floor silently does not apply); deleting tests
permanently and lowering the floor to "pass."

**Grading note.** Both runs must be present, with exit codes. A single green run is a fail
regardless of percentage.

## Step 4 — Comparison table

`docs/competition.md` needs ≥5 competitors you have actually used or visited, ≥6 columns
(platform, on-device, privacy, model choice, price, focus), a source URL or `unverified` in every
cell, uncertainty qualified the way `ListenToMe/docs/competition-analysis.md:3` qualifies it
("approximately", "reportedly"), and a one-liner whose clauses each name a column.
The reference artifact to imitate is `ListenToMe/docs/competition-analysis.md:70-80`.

**Common wrong answers.** Prices from memory; a one-liner of adjectives ("powerful, modern,
private") with no column behind any word; five rows that are all the same shape (five
bot-joiners), which cannot support a wedge.

**Grading note.** Pick one row at random and open its source URL. If the cell does not match the
page, treat every other cell as suspect.

## Self-check table

| Criterion | Self-verification |
|---|---|
| Red-team test green | `make lab-m3` shows 49 passed; the cloud-alias test is in that run |
| Fail-closed on missing metadata | Test with `details` absent asserts `ok is False` |
| Non-loopback host rejected | `assert_host_local("http://example.com:11434")` raises `PrivacyViolation` |
| Redirects refused | `FakeTransport(status=302)` raises `ServerError` matching `redirect` |
| Contract test gated | Without `LAB_E2E`: 2 skipped with a stated reason; with it: 2 passed |
| Daemon case documented | Evidence note names local-model or only-`:cloud` |
| Coverage floor bites | Failure run exit code 1 recorded; success run shows ≥90% |
| Table sourced | Every cell has a URL or `unverified`; uncertain claims qualified |
| One-liner falsifiable | Each clause annotated with its column |
