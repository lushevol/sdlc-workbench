# CES evidence and capability learning

Use the `ces-entitlement-migration` capability ID when CES work discovers reusable information about entitlements or their verification.
Retrieve the applicable capability and records by instance, environment, application, and version.
Inspect the original revision or capture before relying on the recorded conclusion.

| Discovery | Category | Evidence to retain |
| --- | --- | --- |
| Domain terminology and entitlement model | System knowledge | Source terminology, model revision, and application boundary |
| API fields, identity, cardinality, errors, schema | Contract | Dated source locator and a minimized request or response assertion |
| Legacy-to-CES mappings and migration principles | Business rule | Exact mapping decision, authority, effective date, and affected application |
| Baseline definitions and historical decisions | Business rule | Baseline revision, decision date, inventory, and allowed use |
| Reconciliation procedures and verification rules | Workflow | Renormalization inputs, asserted differences, and comparator result |
| Known exceptions and failed or successful probes | Experience | Reproduction scope, actual outcome, and verified resolution or open question |

An observed permission response establishes behavior for the selected identity, application, environment, and time.
A migration baseline applies to its recorded comparison. Recheck current state when a task depends on it.
Keep role membership, effective functional permissions, data profiles, and data policies distinct.
Keep only aggregate or pseudonymous evidence references in a discovery payload.
Exclude user IDs, assignments, raw response bodies, and credentials from the learning record.

For read-only verification, use the existing migration coverage runner. Select replay and a task-owned comparison configuration.
`python -m ai_sdlc_workbench.coverage_suite --mode replay --config TASK_CONFIG` uses retained responses.
Review the candidate and baseline inventories, unassessed identities, and exact asserted differences.
Replay establishes the selected comparison over its captured inputs. Current service parity needs an authorized, environment-bound check.

At the checkpoint, associate the discovery with `ces-entitlement-migration` and attach the sanitized, hash-bound result.
Send new or changed entitlement policy through the existing knowledge review and publication process.
Use the approving authority's recorded decision before modifying the canonical rule.
Keep protected changes pending in the learning engine. Capability promotion supplies no permission to change entitlements.
[Capability learning](../../capability-learning/SKILL.md)

## Locate source material

Search the active workspace for the applicable entitlement control record and permission preservation baseline.
In the Workbench source checkout, initial candidates include `KT-ces-entitlement-control-20261115` and `KT-ces-migration-parity`.
Check their lifecycle status, exact source references, and scope before using them.
The migration coverage task in the source checkout documents replay inputs, comparison definitions, and report limits.
