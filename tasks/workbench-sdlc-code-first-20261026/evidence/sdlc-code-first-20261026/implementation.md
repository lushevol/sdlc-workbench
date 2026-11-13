---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Implement code-first lifecycle entry

**Completed: Workbench now supports requirements-first, existing implementation, and bounded exploration through its portable agent procedures.**
No critical conclusions require user attention or action.

## Authority and scope

The [adoption request](user-input.md#adoption-request-26-october-2026) authorizes this enhancement.
The [assessment](assessment.md) records the prior design and evidence limits.
This stage implements agent procedures, templates, and distribution checks.
It adds no executable workflow engine or business deployment authorization.

## Affected scope and risk

- Consumers: Business intake, task status, change review, verification, and generated workspace users.
- Primary contract: [Task guide](../../../tasks/README.md).
- Shared procedures: Intake, impact analysis, code review, and verification.
- Authoring resources: Requirement, defect, and change-request templates.
- Qualitative risk: Moderate. Conflicting guidance could cause agents to skip intent review or misuse readiness states.
- Source boundary: Preserve unrelated work and all frozen business task records.
- Baseline revision: `d4553033f1adb520fd8279634c4996ffa0833e54`.
- Validation summary and retained file hashes: [Implementation checks](implementation-checks.json).

## Delivered behavior

The [task guide](../../../tasks/README.md#lifecycle-entry-routes) defines the canonical entry routes.
[Project instructions](../../../AGENTS.md#requirement-and-issue-intake) route agents to that procedure before further work.
[Architecture](../../../ARCHITECTURE.md#core-workflow) and [workspace design](../../../docs/WORKSPACE_DESIGN.md#task-intake-and-evidence-ownership) describe the same boundaries.

| Entry | Delivered control |
| --- | --- |
| Requirements first | Preserve ordinary intent refinement and named-stage readiness. |
| Existing implementation | Register actual code history and exact source identities. Keep inferred ACs proposed until supported intent review. |
| Bounded exploration | Require a defined experiment, owner, authorization, edit limits, evidence, stop condition, and disposition before coding. |

Full product ACs can follow a bounded experiment.
`READY` covers that named experiment only. `READY_WITH_LIMITS` continues to permit intake evidence collection only.
Missing authorization or material experiment boundaries block dependent coding actions.
Experimental code can enter reconciliation before product conformance is established.

The [requirement](../../../core/knowledge/templates/sdlc/requirement.md#template), [defect](../../../core/knowledge/templates/sdlc/defect-report.md#template), and [change-request](../../../core/knowledge/templates/sdlc/change-request.md#template) templates record independent evidence states.
They separate implementation, intent review, execution outcome, and business acceptance in existing document bodies.
The shared intake, impact, review, verification, and task-status procedures consume the canonical route.
No new artifact kind, metadata schema, runtime status, dependency, or execution grant was added.

Code-derived requirements cannot approve themselves through matching code or passing tests.
All routes retain the existing three coverage mappings and separate knowledge publication and deployment authorization.

## Validation and observed limits

| Check | Result and retained evidence |
| --- | --- |
| Runtime suite | [658 tests completed; two skipped](validation/unittest.log). All executed tests passed. |
| Initial sandbox suite | [Twenty loopback fixture errors](validation/unittest-sandbox.log). These tests could not bind local mock servers. |
| Wheel build | [PASSED with installed build dependencies](validation/wheel-local.log). No runtime dependency changed. |
| Initial isolated build | [Blocked build-dependency download; compressed raw log](validation/wheel-isolated.log.gz). The sandbox denied the configured proxy connection. |
| Installed wheel | [PASSED outside this checkout](validation/wheel-workspace-check.json). Sixteen changed shipped files match source bytes. |
| Source workspace | [VALID](validation/workspace-validation.json), with no validation findings. |
| Skill validation | Four affected skills passed their existing metadata validator. |
| Independent forward test | [Both procedural cases behaved as intended](validation/forward-review/report.md). No business experiment or acceptance occurred. |
| Reference and diff checks | See [final checks](implementation-checks.json). |

The initial environment failures remain retained. They do not establish application defects.
The installed-wheel check reused existing declared dependencies on macOS.
It confirmed generated workspaces exclude runtime source, business task contents, and project evidence.
Windows execution and isolated dependency downloads remain untested in this stage.

The forward test retained supplied unverified revisions without treating them as inspected code.
It blocked acceptance for an unsupported timeout rule.
It allowed the separately authorized disposable experiment without inventing a product duration policy.
Retained source snapshots and hashes bind that evaluation to its inspected instructions.

## Completion and remaining boundary

The procedural enhancement is complete. No blocker remains for this stage.
Agents still assess lifecycle readiness. The runtime does not enforce task transitions.
An incomplete requirement draft can still fail artifact lint while its bounded exploration has a valid readiness decision.
Record that limit without inventing business thresholds or presenting draft lint failure as approval.
Automated checks remain separate from the pending ASD writing review.
