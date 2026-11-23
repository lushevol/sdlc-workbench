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
[native hooks](../../docs/HOOKS.md#learning-capture), and the [CES domain skill](../../.agents/skills/ces-domain-capability/SKILL.md).

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
Use the six responsibilities as the model for the existing skill and Python engine.
The ADO fixture completed the proposed reuse sequence across CLI processes and two workspaces.
A separate probe confirmed that instruction-only updates fall outside the current promotion workflow.
The review record explains the gap and the smallest follow-up. [Review evidence](evidence/proposal-review.md)

## CES domain skill replacement

The user supplied the [exact request](evidence/ces-domain-skill-request-20261123.txt) in Codex on 23 November 2026.
Baseline Workbench revision is `9441e157f`.
The change affects CES skill routing, packaging, and the registry entry.
The existing scanner and evidence remain available for migration work.

The new CES domain skill covers effective access, data scope, integration contracts, and mixed-provider compatibility.
The registry resolves the existing capability ID to the new skill.
The scaffold ships the canonical skill and its Claude alias.
Migration review uses the relocated scanner and report guidance.
The scanner produces the existing report format and tool identifier.
[File relocation and source hashes](evidence/ces-skill-relocation-20261123.json)

Validation ran on macOS with Python 3.14.5.

- The full suite passed 1,155 tests with connector integration enabled and zero skips.
- The new skill passed the Agent Skills structure validator. Workbench validation checked 119 knowledge documents with zero findings.
- The wheel installed outside the source checkout. CLI discovery, the Claude alias, relative links, and an isolated scanner fixture passed.
- An independent read-only review traced a CES record-visibility question through application, entitlement, functional access, and data restrictions.

The wheel SHA-256 is `fac98c9efe09bf8af4dc86792ef6a5ac40257a5d0f22c1d154de57c6affedaff`.
The suite log at `.workbench/ces-domain-skill-validation/full-suite.log` has SHA-256
`683e2db700380f952c0f5f0320fca4960f1068045b63e23ffedc4f0db3bb7da1`.
The checks cover skill distribution and offline operation. Live CES and native client activation remain unverified for this change.

See the [CES domain skill](../../.agents/skills/ces-domain-capability/SKILL.md)
and its entry in [capability learning](../../docs/CAPABILITY_LEARNING.md#integration-examples).

## Standalone CES capability

The user supplied the [exact follow-up](evidence/ces-standalone-skill-request.txt) in this Codex session on 23 November 2026.
Baseline Workbench revision is `4301ebcee1de55e7ffc49375a08e38337d3f2dd4`.
The skill must package CES contracts, domain knowledge, workflows, and scripts.
Remove migration scan content from the skill and verify the package outside Workbench.

The package now contains CES response contracts, a domain model, investigation workflows, an offline inspector, and synthetic captures.
The inspector uses the Python standard library.
The active skill links resolve within its own folder.
The Workbench capability registry points to the same skill entry.
The change replaces one diagnostic tool and its supporting migration material with a CES capture inspector.
[Removed files and recovery revision](evidence/ces-standalone-skill-removals.json)

The response shapes follow four retained CES GET captures.
The evidence covers the application catalog and effective-user views.
[Captured API field mapping](../ces-entitlement-migration-20261102/03-output-mapping.md#operations-and-delivery)

- All 1,157 Workbench tests passed on macOS with connector integration enabled.
- The Agent Skills validator and Workbench validation passed. Workbench found zero issues in 119 knowledge documents.
- An installed wheel shipped all nine package files. CLI discovery, the Claude alias, and internal links passed in a fresh workspace.
- The inspector passed from a copied folder with Python isolated mode and site imports disabled.
- The independent walkthrough verified exact feature/action checks and compared assignment, grant, and data-section changes.

The offline checks cover captured responses. Data-policy interpretation and current CES enforcement need scoped evidence.
Current instructions are in [CES domain capability](../../.agents/skills/ces-domain-capability/SKILL.md)
and the [Workbench capability guide](../../docs/CAPABILITY_LEARNING.md#integration-examples).
