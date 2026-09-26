# Playbooks

Six units of the course that work without it. Each is one method a working engineer can apply to
their own project in an afternoon, with a template to copy, a binary checklist, a worked example
from a real repository, and a self-check that runs. They were extracted where the content audit
found the case-study material to be illustration rather than load-bearing
(`course/00-research/09-content-audit-2026.md`, §7).

| Playbook | Extracted from | You leave with | Self-check | Proposed price |
|---|---|---|---|---|
| [Agent governance files and an evidence log](agent-governance/playbook.md) | M1.1, M1.3 | `AGENTS.md` imported by `CLAUDE.md`, a rule/hook/skill/subagent decision, an evidence log a Stop hook enforces | the hook's six log states; `aps-tools/agents_audit.py` | $39 |
| [Fail-closed local-only mode](fail-closed-local/playbook.md) | M3.1 | a stdlib guard that verifies the model's own metadata, refuses non-loopback hosts, redirects and proxies, and fences untrusted text | 18 tests, each defense removable to a named failure | $49 |
| [Competition table to falsifiable one-liner](falsifiable-positioning/playbook.md) | M3.3, M7.3 | a sourced table, a one-liner whose clauses each trace to a column, the deletion test | a table checker; the clause map against the dated table | $29 |
| [Agent-executable specs: the checklist and the drift checks](agent-executable-specs/playbook.md) | M4.1–M4.3 | a pre-planning checklist gate, a stranger test, and a drift script for generated spec folders | `drift-check.sh` on a real spec folder | $39 |
| [Multi-tenant negative-path test kit](tenant-negative-path/playbook.md) | M5.1–M5.2 | tenant-bound credentials, a route policy test that catches missing, stale and miswired routes, and the negative-path matrix | the mini-flow starter's suite, red then green | $49 |
| [Evidence-cited briefing](evidence-cited-briefing/playbook.md) | M6 | a provenance table with levels and labels, a dated research log, routes that end on a decision, a signed edition manifest | `selfcheck.py` and `edition_manifest.py` | $49 |

Each folder also holds `sales.md`, a short page in the course's eight-section anatomy
(`course/04-sales/landing-page.md`). Every price above is a proposal; the owner sets the final
prices and any bundle (the six proposals sum to $254). None has a testimonial yet, and each sales
page says so.

**What a buyer needs.** The playbooks point at scripts that live in this repository
(`course/03-content/m05-security-tests/mini-flow/`, `course/03-content/m06-expertise-product/`,
`aps-tools/`). Selling them standalone therefore needs the delivery decision in #35 and the licence
in #59 first; until then they are drafts that the gate keeps honest.

**What the gate checks.** `course/06-production/verify.py` holds every playbook to 1,500–3,000
words and every sales page to 400–750, requires the playbook sections in order (The method,
Template, Checklist, Worked example, Self-check, Limits, Sources), fails a playbook that points
back into a module or a lab ("Lab M3", "M3.1", "as we saw"), requires each price to be labelled a
proposal, and range-checks every repository pointer they cite, like the rest of the course.
