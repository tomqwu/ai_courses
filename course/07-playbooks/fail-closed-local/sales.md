# Sales Page: Fail-Closed Local-Only Mode

## [Hero]

# "Stays on your device" is a claim. This playbook makes it code.

A standalone playbook for AI features backed by a local model server such as Ollama. It turns a privacy promise into a mode that refuses to send a prompt until the server's own metadata proves the model is local, with a loopback allowlist, redirect refusal, proxy refusal, truthful labels and a prompt-injection fence.

**You leave with:** a standard-library Python guard, 18 tests that each fail when their defense is removed, and a claim-to-enforcement table for your sales page.

## [Who this is for — and isn't]

**For you if you:**
- Ship, or plan to ship, an AI feature that says "local", "private" or "on-device".
- Use Ollama or a similar local server and check only that the URL says `localhost`.
- Need to tell a user, a reviewer or an app store exactly where their data goes.

**Not for you if you:**
- Run all inference in a vendor's cloud and say so. You need disclosure, not this guard.
- Need a legal opinion on privacy law. This is engineering.

## [The problem]

A `localhost` URL proves nothing. A local Ollama daemon can serve cloud-backed aliases that answer on `localhost` and run remotely; ListenToMe's own review says "a local endpoint is not proof of local inference" (`ListenToMe/docs/reviews/2026-09-10/design-and-gap-review.md:46`). Redirects and proxy settings are two more ways text leaves while the URL still reads `localhost`. The last one is easy to miss: in a test on 2026-09-26, Python's default `urllib` opener and a default `httpx` client both sent a `localhost` request, body included, to the proxy named in `HTTP_PROXY`.

## [What you get]

- `playbook.md`: eleven numbered steps, three copy-paste files (`local_guard.py`, `prompt_fence.py`, `test_local_guard.py`), a claim-to-enforcement table, a checklist, a worked example, a self-check and a list of limits.
- The three privacy tiers (on-device, platform private cloud, third-party cloud including bring-your-own-key) and the sentence each one lets you publish.
- A break table: remove each defense, see which test fails.

## [What you'll be able to do]

- Verify a model's locality from the server's own metadata on every request, and fail closed on anything short of proof.
- Refuse non-loopback hosts, redirects and proxies before a byte of the prompt is written.
- Label every mode by where the data goes.
- Defend each privacy sentence on your page with a file and a test.

## [Proof]

- ListenToMe, a macOS meeting copilot, enforces the same checks in Swift: `isVerifiedLocal` (`ListenToMe/Sources/ListenToMeCore/ModelPrivacy.swift:17-24`), the loopback check and per-request `/api/show` (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:144-157`), and `RejectRedirects` (`ListenToMe/Sources/ListenToMeCore/OllamaProvider.swift:208-214`).
- TinyCopilot, a Python re-implementation of the same defenses, passes its 49 privacy and provider tests (run 2026-09-26).
- The playbook's own 18 tests pass, and each of eight deliberate breaks fails the test named in the playbook (run 2026-09-26, Python 3.11.15).

## [Instructor]

Written from the AI Product Studio course by Tom Wu, who builds in public. ListenToMe is his; this playbook uses it and TinyCopilot as its worked examples.

## [Testimonials]

None yet. No buyer has used this playbook. This section stays empty until one does.

## [FAQ]

**I'm not using Python.** The method is language-neutral and the Swift reference is pointed to line by line. The template is Python.

**Does this make my product private?** It makes one path, the model request, fail closed. Downloads, telemetry and the server itself are outside it; the playbook's Limits section lists them.

**Does it stop prompt injection?** No. The fence hardens a prompt. The playbook says so, as the reference code does.

**Refunds?** Set by the owner with the final price. This draft promises none.

## [Pricing]

**$49** (proposed; the owner sets the final price).

The full AI Product Studio course ($399, `course/04-sales/landing-page.md`) includes this material and the TinyCopilot labs in a nine-module path. If you want the whole on-device product path, it is the better value.

## [Final call]

Replace "we respect your privacy" with a guard that refuses, a test that proves it, and one sentence that says where the guarantee ends.
