# Source disposition review

The Portal activity and navigation-context dispositions can stand. Payment recovery and access grants require further canonical work.

All four receipt declarations say `no_change`. Two declarations lack complete source-to-output coverage.
The saved progress summary overstates completion. The checkpoint preserves the supported resume position.

## Scope and evidence

This synthetic review covers four selected identities and their existing outputs.
Supporting sources explain current candidates, reader answers, observations, and the proposed wiki.
All 24 supplied fixture hashes and five selected-skill hashes match their declared values.

The declarations in `selection.json` use a fixture format. Runtime receipt validity remains unverified.
Publication remains candidate-only. Business execution evidence remains historical and local. [Selection](../selection.json)

## Selected-source accounting

| Selected source and material clause | Current destination or disposition | Review result and next action |
| --- | --- | --- |
| Portal activity, L3 | Draft requirement dated 1 November 2026, applicable to Portal operators. | Retain this source qualification when reusing the candidate. |
| Portal activity, L5 | `knowledge/records/portal.md#activity`, L4, preserves mouse, keyboard, scroll, usable refresh credentials, and unspecified duration. | Existing coverage can stand. Eligibility alone supplies no successful-renewal guarantee. |
| Portal activity, L6 | `knowledge/records/portal.md#activity`, L5, preserves unresolved browser suspension. | Existing coverage can stand with this uncertainty visible. |
| Portal activity, L7 | `knowledge/records/portal.md#activity`, L5, preserves unverified production adoption. | Existing coverage can stand. |
| Payment recovery, L3 | Draft target behavior dated 10 November 2026. | Preserve draft status during later canonical work. |
| Payment recovery, L5 | `tasks/recovery-draft.md`, L3, preserves retry permission partially. Original-reference preservation remains absent. | Pending. Extend the saved draft with the original payment reference. |
| Payment recovery, L6 | No canonical destination. `knowledge/records/settlement.md#recovery`, L8, explicitly records absent incorporation. | Pending. Preserve accepted-reference duplicate suppression in the saved draft. |
| Payment recovery, L7 | No canonical destination. The saved draft flags unfinished late-arrival detail. | Pending. Preserve the unresolved duration and absence of a default. Obtain the settlement owner's decision. |
| Access grants, L3 | Draft CES rule dated 10 November 2026. | Retain draft qualification during later review. |
| Access grants, L5–L6 | `knowledge/records/access.md#grants`, L4–L5, preserves the grant chain, multiple roles, and absent primary scalar role. | These predicates can stand. |
| Access grants, L7 | No canonical destination. The Grants section omits denial without a matching action grant. | Pending. Incorporate the explicit denial rule as draft intent. |
| Navigation context, L3 | Contextual disposition. The source declares an activity-agenda repetition without additional conditions, exceptions, or behavior. | Justified redundancy can stand with no new canonical output. |

These mappings follow the inspected source bytes and current candidate sections.
[Portal source](../sources/portal/activity.md), [Portal candidate](../knowledge/records/portal.md),
[recovery source](../sources/settlement/recovery.md), [recovery draft](../tasks/recovery-draft.md),
[settlement candidate](../knowledge/records/settlement.md), [grants source](../sources/access/grants.md),
[access candidate](../knowledge/records/access.md), [context source](../sources/context.md)

### Completion denominators

| Measure | Result | Meaning |
| --- | --- | --- |
| Selected identities | 4 | All four remain in the requested denominator. |
| Declared reviewed `no_change` results | 4/4 | Fixture declarations alone. |
| Satisfactory source dispositions after this review | 2/4 | Portal existing coverage and justified navigation redundancy. |
| Identities fully represented by existing canonical meaning | 1/4 | Portal activity. Context needs no additional intent record. |
| Identities requiring further canonical work | 2/4 | Recovery and grants. |
| Approved publication | 0 established | The supplied selection records no human approval. |

The two supported dispositions permit retaining existing work.
The review supplies accounting findings without changing historical declarations.
A later authorized completion must bind existing-coverage targets and record inspected clause dispositions.
Pending clauses keep their identities queued. The synthetic declarations supply no verified runtime completion state.

## Existing-output findings

| Finding | Evidence and consequence | Owner and next action |
| --- | --- | --- |
| The progress summary overstates completion. | It equates four reviewed declarations and wiki freshness with completion. Two selected sources remain incomplete. | Maintainer. Reconcile the summary during authorized task maintenance. |
| Recovery remains unfinished. | The draft omits original-reference and duplicate predicates. Settlement records no incorporated recovery source. | Maintainer for drafting. Settlement owner for retention duration. Resume the saved draft. |
| Access coverage omits explicit denial. | Existing grants preserve positive evaluation only. An output-free declaration conceals the uncovered denial rule. | Canonical reviewer unknown. Retain the sourced draft denial rule during authorized canonical review. |
| Wiki meaning requires correction. | Every proposed statement changes or contradicts its supporting source. Fresh-input metadata cannot establish semantic accuracy. | Wiki maintainer unknown. Repair from reviewed canonical candidates after authorized canonical reconciliation. |

The checkpoint accepts Portal and context, names the recovery draft, and holds access for canonical review.
These details agree with the inspected content. Its access hold requires reviewer work.
No additional human answer is needed to retain the explicit draft denial rule.
[Progress](../tasks/progress.md), [checkpoint](../tasks/checkpoint.json), [recovery draft](../tasks/recovery-draft.md)

### Proposed wiki corrections

- Preserve activity eligibility, usable refresh credentials, unspecified fixed duration, and unresolved suspension. Production adoption remains unverified.
- Preserve the 2022 weekday 16:00 Asia/Singapore proposal, pending holiday treatment, and owner approval.
- Preserve combined grants across roles and the absence of a primary scalar role.
- Preserve meaningful failed traces. Historical cleanup requires consumer and provenance review. Equal hashes alone supply no deletion authorization.

The current wiki asserts production renewal for exactly 15 seconds, daily cutoff, scalar roles, and hash-based failed-trace deletion.
Each assertion needs correction before reuse. [Wiki proposal](../wiki/proposed.md),
[Portal candidate](../knowledge/records/portal.md), [settlement candidate](../knowledge/records/settlement.md),
[access candidate](../knowledge/records/access.md), [retention source](../sources/operations/retention.md)

## Reader-answer review

Draft A contains three material answer defects.
Q-04 omits original references and accepted-duplicate suppression, and invents seven-day retention.
Q-06 invents navigation permission and first-role fallback.
Q-09 converts one token observation into effective UAT configuration. [Draft A](../drafts/answer-a.md)

Draft B preserves the important corrections across its four answers.
Its Q-04 wording should preserve retry permission with “can be retried.”
It covers Q-01, Q-04, Q-06, and Q-09 only.
Eight reader questions remain absent from that draft. [Draft B](../drafts/answer-b.md)

The supported answers follow.

| Question | Supported answer and limits |
| --- | --- |
| Q-01 | Mouse, keyboard, and scroll keep renewal eligible while refresh credentials remain usable. No fixed active-session duration is specified. Suspension recovery remains unresolved. Production adoption is unverified. |
| Q-02 | The ui-42 local fixture produced zero renewal requests over 15 seconds, despite mouse events every 100 ms. Code schedules `runExtend` after 5,000 ms. Controlled clocks and a stub issuer limit the observation. Timing remains implementation evidence. |
| Q-03 | The 2022 proposal specifies weekday 16:00 Asia/Singapore cutoff and next-business-date processing afterwards. Holiday treatment and owner approval remain unresolved. |
| Q-04 | A rejected payment can be retried with its original reference. An accepted reference must never create a second payment. Late-arrival retention remains unresolved without a supplied default. |
| Q-05 | Multiple roles contribute grants through application, feature or subject, and action. No primary scalar role is defined. |
| Q-06 | A caller without a matching action grant is denied under the draft CES rule. |
| Q-07 | Omitting drawers preserves state. An empty drawers array clears state. |
| Q-08 | Replacement identifier meaning remains unresolved. The adapter must preserve existing upper-application calls. Compatibility and implementation parity remain unverified. |
| Q-09 | YAML defaults to 15 minutes. The effective local JVM override is 480 minutes. One UAT token lived 900 seconds. Effective UAT issuer configuration and clock offset remain unknown. |
| Q-10 | The candidate release note describes planned deployment. Deployment completion remains unconfirmed. The release owner is unknown. |
| Q-11 | Historical cleanup requires consumer and provenance review. Retain meaningful failures and link one canonical payload. The consumer inventory remains incomplete. |
| Q-12 | Retain meaningful failed traces in the investigation evidence and preserve provenance. No concrete evidence directory is specified here. Equal hashes alone do not authorize deletion. |

Answer support comes from the exact source ranges reviewed above and the supporting evidence.
[Activity L3–L7](../sources/portal/activity.md), [observation L3–L7](../sources/portal/observation.md),
[cutoff L3–L7](../sources/settlement/cutoff.md), [recovery L3–L7](../sources/settlement/recovery.md),
[grants L3–L7](../sources/access/grants.md), [migration L3–L7](../sources/access/migration.md),
[runtime L3–L7](../sources/operations/runtime.md), [retention L3–L7](../sources/operations/retention.md)

The existing task gap document preserves local observations and environment limits.
Its historical findings can stand within their stated scope. [Task gaps](../tasks/gaps.md)

## Resume position and topic map

Resume at the saved payment recovery draft.
Preserve accepted Portal and contextual work, current candidates, prior declarations, saved answers, and unresolved questions.
Complete the explicit recovery predicates independently of the missing retention-duration decision.
Review the access denial predicate independently of publication approval. [Checkpoint](../tasks/checkpoint.json),
[saved answers](../tasks/questions.md)

KQ-01, KQ-10, and KQ-11 contain saved answers.
Nine question rows have empty answers. Preserve their exact authority, actor, environment, version, and decision scopes.
KQ-01 answers qualifying event categories for UAT v1.
It supplies no answer about touch, synthetic events, input subtypes, PROD, or v2 timing.
The ui-42 observation supplies no effective UAT configuration answer.
KQ-12 requires the settlement owner's retention-duration decision. [Living questions](../tasks/questions.md)

| Existing topic | Proposed review scope |
| --- | --- |
| Portal | Keep activity intent connected to separately retained local observations and unresolved suspension questions. |
| Settlement | Preserve qualified cutoff proposal. Continue recovery draft and retain the unresolved late-arrival decision. |
| Access | Preserve combined grants and migration constraints. Add the explicit sourced denial predicate during authorized canonical work. |
| Operations | Preserve retention instructions and incomplete cleanup inventory. Keep environment and deployment observations in the task gap document. |

The checkpoint requests model `luna` and reasoning `max`.
Its dispatch observation is null. Actual respondent model, reasoning level, and client settings are UNKNOWN.

## Checks and limits

Actual checks covered all supplied file hashes, selected-skill hashes, source predicates, current outputs, and saved-answer scope.
Output validation checks local Markdown destinations and confirms unchanged fixture inputs.

Source planner, source verifier, ingestion harness, business tests, and model execution are `NOT_RUN`.
The permitted review used synthetic declarations and local evidence.
No runtime collection readiness, sealed checkpoint, deployment, or publication outcome was established.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - This synthetic review supplies no business execution or publication evidence.
```

