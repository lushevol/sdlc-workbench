# Self-Evolving Capability System

The user supplied the [exact implementation directive](evidence/user-directive.txt) on 22 November 2026 in this Codex session.
The directive authorizes local Workbench implementation and fixture-based tests.
It protects production deployment and entitlement operations.

Baseline Workbench revision is `3ded0689336f7926e025d6545a9f5652c698446b`.
The deleted connector lockfile and untracked release-report source were present at entry.

## Workbench gap analysis

| Area | Reuse | Gap |
| --- | --- | --- |
| Runtime and configuration | Installed Python CLI, workspace declarations, existing JSON Schema validator, local atomic file helpers | Capability learning commands and local switches |
| Registry | Existing capability, contract, repository, service and tool catalogs | Scoped discovery and change records, reconciliation and revision history |
| Knowledge and experience | Canonical knowledge, governed transitions, retained sources and reviewed experience packets | Lightweight automatic capture and checkpoint-based semantic review |
| Agent discovery | Canonical Agent Skills folders and Claude discovery aliases | Learning skill and read-only ADO skill |
| Agent lifecycle | Installed Codex, Claude and Copilot hook adapters, explicit task bindings and advisory checks | Sanitized learning observations, extra lifecycle events and native verification |
| Integration | Granted ADO connector operations, release report, CES migration baselines and candidate records | Read-only artifact resolution and reusable CES classification with policy protection |
| Verification | Existing unit suite, wheel build, workspace validation, Git and task evidence | End-to-end fixture cases and capability-learning audit checks |

## Implementation plan

1. Extend the installed Python CLI and reuse its validation, path and atomic write helpers.
2. Keep revision history alongside the existing capability catalog. Reuse canonical contract and skill references.
3. Keep scratch observations and proposals in ignored local storage. Bind reviewed evidence to exact hashes.
4. Retrieve related capabilities by identity, category, applicability and terms before reconciliation.
5. Use a scoped revision journal to activate a validated change atomically and retain rollback history.
6. Allow automatic promotion for typed ADO artifact selection data with independent local checks.
7. Route executable content and CES policy through established review and governance.
8. Extend native adapters with bounded metadata capture and preserve explicit task checkpoints.
9. Package skills and current documentation. Verify ADO, CES and cross-session reuse with fixtures.
10. Run native checks where available, then run the unit suite, build the wheel and validate an initialized workspace.

The installed runtime and shared registry change. Invalid revisions can affect future sessions.
Strict validation, atomic promotion and isolated fixtures reduce that risk.

## Implemented outcome

The Workbench now captures minimized lifecycle events and accepts evidence-bound discoveries at task checkpoints.
The CLI reconciles scopes, holds conflicts, and stores promoted revisions in the existing registry area.
Earlier revisions remain available for audit and rollback. Existing provider grants remain the execution authority.

The ADO resolver reuses two granted artifact metadata reads. Its checks bind each result to an exact build and commit.
Local pipeline wrappers use shared templates. Their source does not establish the artifact naming and deployment rules.
Fixture discoveries extended one ADO skill across two branch conditions. A new process reused the selected rule.
Automatic promotion requires two matching builds with distinct commits and one artifact each.
The resolver reports metadata integrity. Artifact bytes, deployment mechanisms, and target approvals still need authorized evidence.

The CES foundation reuses the migration coverage replay and retained knowledge candidates.
CES discoveries preserve migration time, instance, environment, and application scope.
Protected proposals stay pending for canonical governance. Live entitlement state was outside validation.

Skill instructions remain reviewed source. The engine validates their identity and records the reviewed hash.
Typed ADO improvements change the skill's selection through scoped data.
The existing agent performs general semantic extraction at checkpoints. Native hooks supply lifecycle hints.

## Verification

- The complete Workbench suite passed 1,155 tests, including optional connector integration. Zero failures or skips.
- The wheel installed outside the checkout. A generated workspace completed learning, revision extension, and cross-session reuse.
- The two new skills passed structure validation. Workspace validation checked 119 knowledge documents with zero findings.
- Claude Code and the embedded Copilot runtime both dispatched six event classes in isolated macOS probes.
- Workbench-owned Claude and Copilot registrations were upgraded locally. Their configuration reports ready.
- Standalone Copilot CLI, cloud dispatch, native Windows, live ADO, and live CES were unverified.

[Validation evidence](evidence/validation.txt)

Current guidance is in [architecture](../../ARCHITECTURE.md#skills-and-adapters), [capability learning](../../docs/CAPABILITY_LEARNING.md),
[native hooks](../../docs/HOOKS.md#learning-capture), and the [CES reference](../../.agents/skills/ces-migration-scan/references/capability-learning.md).

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```

## Skill lifecycle suggestion review

The user supplied the [exact suggestion](evidence/skill-lifecycle-suggestion.txt) for review on 22 November 2026.
The review compares it with committed Workbench revision `b04f3cf74`.

## Review of the supplied Skill Lifecycle Manager suggestion

The proposal is directionally correct as a lifecycle model.
It maps to discovery, checkpoint extraction, reconciliation, validation, promotion, and revision maintenance.
Its Node.js engine location conflicts with the Workbench single-Python-runtime boundary.
Its compatibility Node.js text would misdescribe this runtime.

The implementation does not automatically generate or edit SKILL.md.
It validates linked skill identity and hash, then keeps general authoring under reviewed skill procedures.
The CES capability reuses the existing migration-scan skill to avoid duplicate responsibility.
The proposal's references, templates, examples, explicit learning-feedback headings, and skill-authoring reference remain possible documentation improvements.
They are not required for the current vertical slice.

The isolated A/B/C acceptance probe confirmed the suggested cross-session behavior with separate CLI processes and a local fixture bridge.
It confirmed that the learned scoped rule changed ado-resolve behavior in a new workspace.
The canonical skill bytes remained unchanged.
[Review evidence](evidence/proposal-review.md)
