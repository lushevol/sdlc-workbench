# Selected-source review

> Two of four selected identities have supportable processing results.
> Payment recovery and access grants require further work.
> The saved complete summary and proposed wiki need correction.

This review covers the synthetic fixture and its four selected identities.
Confidence is high for the documented omissions and contradictions.
Business behavior, deployment, publication, and runtime completion remain unverified.

## Selected-source accounting

All four selected identities remain in the denominator.
One has existing canonical coverage.
One has a justified contextual disposition.
Two have incomplete substantive coverage.
Reviewed flags and declared wiki freshness cannot establish clause coverage. [Selection](../selection.json), [saved summary](../tasks/progress.md)

| Selected identity | Processing result | Evidence and consequence | Owner and next action |
| --- | --- | --- | --- |
| `portal/activity.md` | Existing-coverage `no_change` can stand semantically. | The Activity section preserves eligible events, credential usability, duration limits, and unresolved suspension. Preserve the accepted work. | Reviewer unknown. Retain the exact source-to-section accounting below. |
| `settlement/recovery.md` | Incomplete. The output-free `no_change` cannot stand. | Recovery explicitly contains no incorporated source. The saved draft omits original-reference and accepted-duplicate rules. | Reviewer unknown. Resume the saved draft. Retain the open duration question for owner:settlement. |
| `access/grants.md` | Partial. The output-free `no_change` cannot stand. | Grants preserves multi-role evaluation and scalar-role limits. It omits denial without a matching action grant. | Reviewer unknown. Review and preserve the explicit draft denial rule. |
| `context.md` | Context/redundancy `no_change` can stand semantically. | The agenda declares repeated activity context and supplies no additional intent. An empty output list is justified. | Reviewer unknown. Retain the redundancy rationale and accepted work. |

These are review findings about the supplied bytes.
The fixture declares its receipts outside the runtime receipt schema.
Runtime bindings and a passed completion checkpoint are unavailable. [Selection](../selection.json)

### Portal activity

The source is a draft dated 1 November 2026.
Its actor scope is Portal operators.
The existing output remains a candidate.

| Original range | Material clause | Existing destination | Disposition |
| --- | --- | --- | --- |
| L5 | Mouse, keyboard, and scroll keep renewal eligible while refresh credentials remain usable. | `knowledge/records/portal.md#activity`, L4 | Existing coverage |
| L5 | No fixed active-session duration is specified. | Same section, L4 | Existing coverage |
| L6 | Browser suspension recovery is unresolved. | Same section, L5 | Existing coverage of an unresolved boundary |
| L7 | Production adoption lacks evidence. | Same section, L5 | Preserved qualification |

The source status and operator scope constrain reuse.
The Investigation evidence link preserves access to the historical observation. [Source L3–L7](../sources/portal/activity.md#L3-L7), [candidate L3–L8](../knowledge/records/portal.md#L3-L8)

### Payment recovery

The source records draft target behavior dated 10 November 2026.

| Original range | Material clause | Current destination | Disposition and required work |
| --- | --- | --- | --- |
| L5 | A rejected payment can be retried with its original payment reference. | No canonical destination. The saved draft preserves retry alone. | Pending. Preserve the original-reference condition. |
| L6 | Repeating an accepted reference must prevent a second payment. | None | Pending. Preserve the duplicate-prevention rule. |
| L7 | Late-arrival retention duration is unresolved, with no default. | None | Pending. Preserve the unresolved boundary and owner question. |

The cutoff section supplies independent proposal context.
It does not account for these recovery clauses.
The recovery source remains selected and unfinished. [Source L3–L7](../sources/settlement/recovery.md#L3-L7), [current Recovery](../knowledge/records/settlement.md#recovery), [saved draft](../tasks/recovery-draft.md)

### Access grants

The source records a draft CES rule dated 10 November 2026.

| Original range | Material clause | Existing destination | Disposition |
| --- | --- | --- | --- |
| L5 | Evaluate grants through application, feature or subject, and action. | `knowledge/records/access.md#grants`, L4 | Existing coverage |
| L6 | Several roles can contribute grants. | Same section, L4 | Existing coverage |
| L6 | No primary scalar role is defined. | Same section, L5 | Existing coverage |
| L7 | A caller without a matching action grant is denied. | None | Pending substantive omission |

The missing denial clause prevents complete source coverage.
The source already supplies draft intent.
Its canonical review can proceed independently of unanswered policy questions.
Any future existing-coverage result must bind the Access output. [Source L3–L7](../sources/access/grants.md#L3-L7), [candidate L3–L5](../knowledge/records/access.md#L3-L5), [checkpoint](../tasks/checkpoint.json)

### Meeting context

Source L3 identifies repeated Portal activity context without new conditions, exceptions, or behavior.
Its disposition is `context_or_redundancy`, with target `none`.
A new canonical record would add no supported intent.
This selected identity counts as justified context, with zero new canonical outputs. [Context L3](../sources/context.md#L3), [existing Activity](../knowledge/records/portal.md#activity)

## Current answers and wiki

| Output | Results that can stand | Required work |
| --- | --- | --- |
| Draft A | Q-01, Q-02, Q-03, Q-05, Q-07, Q-08, Q-10, Q-11, and Q-12 retain supported limits. | Correct Q-04, Q-06, and Q-09 below. |
| Draft B | Its four answers preserve the supplied recovery, denial, and environment qualifications. | It covers Q-01, Q-04, Q-06, and Q-09 only. Eight reader questions remain absent. |
| Proposed wiki | Its four substantive statements require correction. | Preserve source status, evidence limits, multi-role semantics, and retention restrictions. |

These judgments concern the actual statements supplied in each output. [Draft A](../drafts/answer-a.md), [Draft B](../drafts/answer-b.md), [reader questions](../questions.md), [proposed wiki](../wiki/proposed.md)

- Q-04 must retain original-reference retry and accepted-reference duplicate prevention. Late-arrival retention remains unresolved. The seven-day value has no support. Owner:settlement must resolve duration. [Recovery source](../sources/settlement/recovery.md)
- Q-06 must deny a caller without a matching action grant. Navigation allowance and first-role selection lack support. Reviewer unknown must correct the answer and omitted candidate clause. [Grants source](../sources/access/grants.md)
- Q-09 must retain the 15-minute YAML default and effective 480-minute local override. One UAT sample lived 900 seconds. Effective issuer configuration and UAT clock offset remain unknown. Engineering owner is unknown. [Environment source](../sources/operations/runtime.md)

The proposed wiki's exact production duration contradicts the qualified Activity intent.
The 15 seconds describe one historical local observation.
That observation used revision ui-42, a controlled clock, and a stub issuer.
Mouse events every 100 ms produced zero renewal requests.
The inspected 5,000 ms delay describes implementation.
UAT and continuous real-duration renewal remain untested in that observation. [Activity](../sources/portal/activity.md), [historical observation](../sources/portal/observation.md), [retained gap evidence](../tasks/gaps.md)

The wiki's daily cutoff claim loses weekday, timezone, proposal status, holiday uncertainty, and owner approval.
The source proposes 16:00 Asia/Singapore on weekdays.
After-cutoff handling is proposed for the next business date.
The settlement owner must confirm the current policy and holiday treatment. [Cutoff proposal](../sources/settlement/cutoff.md), [existing Cutoff](../knowledge/records/settlement.md#cutoff)

The wiki's primary-role claim conflicts with the explicit multi-role rule.
Its failed-trace deletion claim conflicts with the retention instruction.
Preserve meaningful failures and one canonical payload.
Consumer and provenance review remains required.
The historical consumer inventory is incomplete.
The wiki maintainer is unknown and must review each affected statement. [Grants](../sources/access/grants.md), [retention instruction](../sources/operations/retention.md), [existing Retention](../knowledge/records/operations.md#retention)

The release note supplies a deployment plan.
Deployment completion and the release owner remain unknown.
The candidate publication declaration records absent human approval. [Environment evidence](../sources/operations/runtime.md), [selection declaration](../selection.json)

## Resume and outstanding questions

Resume from the saved payment recovery draft.
Preserve accepted Portal activity and context work.
Then complete the grant-denial review independently.
This follows the saved checkpoint and KQ-10.
The current exercise's deliverable is this review. [Checkpoint](../tasks/checkpoint.json), [saved answers](../tasks/questions.md)

KQ-01, KQ-10, and KQ-11 have saved answers.
Their answers retain their exact authority, actor, environment, version, and decision scope.
KQ-05 concerns keyboard and scroll inputs within the same policy scope.
KQ-01 supports their general eligibility.
Specific input subtype treatment remains unspecified if that is KQ-05's intended distinction.
Preserve the question pending that clarification. [Living questions](../tasks/questions.md)

KQ-02, KQ-03, KQ-04, KQ-06, KQ-07, KQ-08, KQ-09, and KQ-12 remain unanswered.
Touch policy, PROD applicability, touch implementation, v2 timing, and synthetic input eligibility need separate evidence.
Publication needs its own authority.
Effective UAT configuration and late-arrival duration remain open.
Policy owners are owner:portal and owner:settlement where recorded.
Engineering owners remain unknown. [Living questions](../tasks/questions.md), [historical timing scope](../sources/portal/observation.md), [environment limits](../sources/operations/runtime.md)

The requested worker settings are `luna` and `max`.
The checkpoint records no observed dispatch.
Actual model, reasoning setting, and client are `UNKNOWN`.
The requested settings remain unverified. [Checkpoint](../tasks/checkpoint.json)

## Topic map and checks

Reuse the existing Portal, Settlement, Access, and Operations topics.
Link recovery and grant-denial work to their existing candidate sections.
Keep implementation and deployment observations linked through task gap evidence.
The contextual agenda needs no new topic.

All 24 listed fixture inputs match their supplied SHA-256 values.
All five selected skill files match their supplied hashes.
All four selected-source bindings match the current source bytes.
The action log records actual local reads, writes, commands, and checks.
Input hashes remain unchanged.

The source planner, source verifier, and ingestion harness were `NOT_RUN`.
This fixture supplies declarations without a registered collection or runtime completion artifacts.
The named output-only review scope governs the work.
Business execution and production conformance are `NOT_VERIFIED`.
The synthetic evidence supports the findings within this fixture.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cover hashes, output structure, and local link targets.
  - Automated checks do not establish complete writing review.
  - Synthetic inputs do not establish business behavior.
```
