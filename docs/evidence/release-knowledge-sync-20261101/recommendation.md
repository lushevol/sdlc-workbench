# Suggested release-to-knowledge reconciliation

Source: [exact user request](user-input.md#exact-user-input), 1 November 2026.
Disposition: proposed workflow; no domain record or publication state changed.
Confidence: HIGH that this proposal fits the inspected Workbench contracts.
Limit: no automatic release-to-knowledge reconciliation workflow was implemented or exercised in this discussion.

## Recommendation

Use release review as a final knowledge reconciliation checkpoint.
Update resolved business clarifications before the next SDLC handoff. Do not defer those updates until release.
Prepare candidate changes when intended business meaning changes. Retain execution results as linked task evidence.
Confirm deployed applicability separately after an actual rollout with matching deployment evidence.

1. Bind the release scope to exact requirements, source revisions, artifacts, environments, and retained evidence.
2. Map changed behaviors, workflows, contracts, and responsibilities to existing knowledge IDs.
3. Record each disposition: no meaning change, candidate update, new candidate, unresolved conflict, or evidence-only change.
4. Draft old and new meaning with supporting sources, affected criteria, applicability, owner, and unresolved questions.
5. Review final content and complete applicable human approval, audit, validation, and publication requirements.
6. Record the affected knowledge versions and dispositions in the task's knowledge-update log and release handoff.

A release approval does not supply knowledge publication approval.
Knowledge review, implementation identity, observed execution, and deployed applicability remain separate claims.
Avoid knowledge version changes solely because another execution passed.
Changed content requires its own provenance and applicable review. Earlier approval does not transfer to changed bytes.

## Storage and handoff

| Material | Destination and handling |
| --- | --- |
| Reusable domain rule, workflow, contract, or responsibility | Existing knowledge record or candidate successor; preserve identity and prior content. |
| Workbench logging and release-report procedure | Skills and engineering guides. |
| Test results, logs, metrics, anomalies, and release recommendation | Owning task evidence and reports; link them from relevant records when useful. |
| Source provenance and governance changes | Source manifest, findings, and new immutable audit events under existing contracts. |

Keep one reconciliation table in the release handoff.
Suggested columns: change, knowledge ID and version, proposed meaning, disposition, evidence, owner, and review state.
Keep its material claims synchronized across existing Markdown and HTML views.
The table is a proposed reporting addition. It is not an implemented release gate or a new publication authority.

## Session-renewal example

The [renewal requirement](../../../knowledge/candidates/requirements/REQ-active-session-renewal.md) remains version 5, candidate, and draft.
Its pending, success, and retry criteria already define the behavior exercised by the [local pilot](../../../tasks/portal-background-session-20261019/10-runtime-log-pilot.md).
The pilot adds bounded corroboration: three candidate cases, 56 passing assertions, and five assessed observations from six planned observations.
It does not establish full conformance, remote UAT completion, deployment, or human publication approval.
The stale-response diagnostic remains unverified. It cannot silently become an approved additional business requirement.
No automatic requirement rewrite or promotion follows from these results.

## Supporting claims

| Claim | Evidence class and confidence | Source | Limit |
| --- | --- | --- | --- |
| Knowledge contains reusable domain meaning; task evidence retains logs and results. | Documented procedure; HIGH. | [Knowledge standards](../../../knowledge/README.md). | These are repository rules, not proof of domain correctness. |
| Resolved material clarification updates knowledge before handoff. | Documented procedure; HIGH. | [Clarification feedback](../../../knowledge/README.md#clarification-feedback). | Unresolved policy still needs an answer and applicable review. |
| Changed knowledge requires provenance and actual review gates. | Documented procedure; HIGH. | [Review gates](../../../knowledge/README.md#review-gates), [governance workflow](../../../.agents/skills/govern-knowledge/SKILL.md). | Validation cannot authenticate reviewers or establish factual truth. |
| Session-renewal intent remains candidate; the pilot provides bounded local evidence. | Inspected records; HIGH. | [Requirement delivery status](../../../knowledge/candidates/requirements/REQ-active-session-renewal.md#delivery-status), [pilot conclusion](../../../tasks/portal-background-session-20261019/10-runtime-log-pilot.md#verification-conclusion). | No release, UAT, or publication approval is inferred. |

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
