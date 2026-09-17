# Handout M3 — Privacy, Testing, Shipping

**Mental model:** Privacy is an engineered mode, not an adjective — verify the model's metadata on
every request, fail closed on anything missing, and let the release end only at a downloaded,
checksum-verified artifact.

## Decision table: which tier can see this risk?

| Risk | Tier | Why this tier and not another |
|---|---|---|
| Logic: parsing, error typing, prompt builders | Unit, mocked transport, in CI | Fast, deterministic, no daemon |
| The wire contract: request shape, stream parse | Real-LLM contract, outside CI | A mock can only assume the seam; this proves it |
| Privacy routing: is this model actually local? | Unit red-team test + per-request `/api/show` | Cloud aliases appear on a local daemon |
| Mic, system audio, permission grants | Human smoke test | Needs a GUI session and manual grants |
| Untested core logic creeping in | Coverage floor in CI | Fails only when lines go unexecuted |

## The five rules worth keeping

1. **Mode is explicit; keys never switch it.** Adding a cloud key stores the key; routing changes
   only when the user picks cloud.
2. **Labels name the data.** "Ollama Cloud — sends transcript and context", not "enhanced".
3. **Verify per request, fail closed.** `remote_host`/`remote_model` absent, `details.format` and
   `model_info` non-empty — else reject.
4. **Refuse redirects.** A 3xx kills the request; text must never be silently forwarded.
5. **Done = downloaded and checksum-verified**, with the release pinned to the exact commit.

## Commands to keep

```bash
make lab-m3                    # privacy + streaming hardening suite → 49 passed
make lab-m2                    # unit suite + coverage floor ≥90 → 191 passed, 100%
make e2e                       # real-LLM contract test (needs LAB_E2E=1, live daemon)
pytest tests/test_contract_real_llm.py -q    # 2 skipped — with a stated reason
LAB_E2E=1 pytest tests/test_contract_real_llm.py -q   # 2 passed
python -m pytest tests -m "not e2e" --cov=src/tinycopilot --cov-fail-under=90 -q
```

## Files to open

- `ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:3-13, 15-24` — modes, truthful labels,
  the fail-closed `isVerifiedLocal` guard.
- `ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:138-157, 208-214` — host check,
  per-request verification, `RejectRedirects`.
- `ListenToMe/Sources/ListenToMeCore/ModelRanking.swift:72-77` — local-first auto-selection.
- `ListenToMe/scripts/check-coverage.sh` + `ListenToMe/.github/workflows/ci.yml:36-42` — the floor.
- `ListenToMe/Makefile:39-53` + `ListenToMe/Tests/ListenToMeCoreTests/OllamaContractE2ETests.swift:4-22`
  — the gated contract test.
- `ListenToMe/docs/manual-smoke-test.md:1-7` — what only a human can verify.
- `ListenToMe/docs/RELEASING.md:18-31, 120-134` — bundle-id separation and checksum verification.
- `ListenToMe/docs/competition-analysis.md:1-14, 70-80` — sourced table and the one-liner.

## Three gotchas

1. **A localhost URL proves nothing.** A `:cloud` alias installs, lists, and answers through your
   local daemon — with remote compute.
2. **Fail-open hides in missing keys.** If a missing `details` dict skips the check instead of
   rejecting, you have built the anti-pattern.
3. **Your daemon decides Step 1's flavor.** With only `:cloud` aliases, local-only mode correctly
   rejects everything. Document it; do not weaken the checks. Step 0 is `make m3-start`: the
   shipped answer is parked and `make lab-m3` goes red — record that first.

## You're done when…

- ☐ A mocked `/api/show` with `remote_host` is rejected in local-only mode, with the red run recorded first.
- ☐ Missing `format`/`model_info` fails closed; a non-loopback host raises; a 3xx is refused.
- ☐ `LAB_E2E` contract test passes with output recorded — on whatever chat model the router picks, `:cloud` aliases included; it is a contract test, not a privacy test.
- ☐ Coverage floor: both the failure run and the success run recorded.
- ☐ `docs/competition.md` has ≥5 rows, ≥6 columns, per-cell sources or `unverified`.
- ☐ The one-liner's every clause names the column that proves it.
