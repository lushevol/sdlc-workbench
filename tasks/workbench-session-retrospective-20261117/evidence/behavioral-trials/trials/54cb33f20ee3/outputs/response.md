# Source processing review

> Two selected no-change results can stand. Payment recovery and access denial still require canonical work.
> The saved all-complete summary and proposed wiki need correction.

## Scope and evidence

Review date is 17 November 2026. This review uses the selected ingestion and source-preparation skills.
The synthetic fixture supplies four selected sources, current candidates, drafts, saved questions, and recovery metadata.
All 24 fixture input hashes and five skill hashes matched their supplied SHA-256 values.
The review inspected every supplied fixture input. Engineering evidence contains summaries and one synthetic revision label.
The declared base and candidate revisions were supplied metadata. Their implementation differences were not inspected.

The requested work is review-only. Findings below propose subsequent work within the existing task ownership.
The source selection declares candidate publication without human approval and historical local execution only. [Selection](../selection.json#L46)

## Selected-source dispositions

| Source | Finding and evidence | Consequence | Owner and next action |
| --- | --- | --- | --- |
| Portal activity | The saved `no_change` can stand. The candidate preserves qualifying events, usable credentials, unspecified duration, suspension uncertainty, and production limits. | Existing candidate bytes support this source's draft intent. Retain accepted work. | `owner:portal`. Preserve the current candidate and accepted checkpoint item. [Source](../sources/portal/activity.md#L3), [candidate](../knowledge/records/portal.md#L3), [checkpoint](../tasks/checkpoint.json#L3) |
| Payment recovery | The saved `no_change` is unsupported. The candidate explicitly says recovery has no incorporated source. The saved draft remains incomplete. | Original-reference retry and accepted-reference duplicate prevention are absent. Retention remains unresolved. | `owner:settlement` owns the retention decision. Canonical editing owner is unknown. Resume the saved draft and propose the missing rules. [Source](../sources/settlement/recovery.md#L3), [candidate](../knowledge/records/settlement.md#L7), [draft](../tasks/recovery-draft.md#L3) |
| Access grants | The saved `no_change` is unsupported. Union-of-grants and multiple-role semantics exist, while the required denial clause is absent. | A consumer could miss the explicit outcome when no action grant matches. | Canonical editing owner is unknown. Propose adding the draft denial rule and review the affected answers. [Source](../sources/access/grants.md#L3), [candidate](../knowledge/records/access.md#L3) |
| Meeting context | The saved `no_change` can stand. The source declares duplicate navigation context and introduces no target behavior. | Empty output lists alone do not invalidate a reviewed no-change result. Its stated rationale supports reuse here. | Processing owner is unknown. Retain the accepted checkpoint item. [Source](../sources/context.md#L3), [rationale](../selection.json#L39), [checkpoint](../tasks/checkpoint.json#L3) |

Draft status permits retaining explicit proposed intent. Human approval remains necessary for publication.
Access denial needs canonical review and incorporation. It needs no invented business answer before that review. [Checkpoint](../tasks/checkpoint.json#L9)

The fixture receipts are declarations. They do not establish runtime receipt validity or successful sealed checkpoints.
The all-complete summary conflicts with source content and the saved unfinished and held items.
A fresh authorized processing attempt should preserve accepted work and reopen only affected items. [Selection](../selection.json#L3), [summary](../tasks/progress.md#L3), [checkpoint](../tasks/checkpoint.json#L7)

## Current outputs and supported topic map

| Topic and output | Result that can stand | Work or limit |
| --- | --- | --- |
| Portal activity, `knowledge/records/portal.md` | Activity intent matches its source. The link to task investigation evidence preserves the historical observation. | Browser suspension remains unresolved. Production adoption and real-duration renewal remain unverified. [Source](../sources/portal/activity.md#L5), [observation](../sources/portal/observation.md#L3), [task evidence](../tasks/gaps.md#L3) |
| Settlement, `knowledge/records/settlement.md` | The cutoff remains a 2022 proposal. Weekday timing, after-cutoff processing, and unresolved holiday treatment are preserved. | Recovery needs incorporation. The settlement owner must decide retention, holidays, and cutoff approval. Source age supplies no exclusion reason. [Cutoff](../sources/settlement/cutoff.md#L3), [recovery](../sources/settlement/recovery.md#L3) |
| Access, `knowledge/records/access.md` | Grant union and role semantics stand. Migration preserves omitted versus empty drawers and existing upper calls. | Add draft denial intent. Identifier mapping and implementation parity remain unresolved. Mapping owner is unknown. [Grants](../sources/access/grants.md#L5), [migration](../sources/access/migration.md#L3) |
| Operations, `knowledge/records/operations.md` | Consumer review, meaningful-failure retention, and canonical-payload reuse match the maintainer instruction. | Consumer inventory remains incomplete. Keep environment observations in the independent task gap document. [Retention](../sources/operations/retention.md#L3), [environment](../sources/operations/runtime.md#L3), [task evidence](../tasks/gaps.md#L6) |

Activity, recovery, grants, and cutoff supply proposed intent with their recorded status.
Retention supplies maintainer direction. Migration supplies a caller-preservation constraint alongside inspected legacy evidence.
Local observation and runtime captures supply implementation or execution evidence in task gaps.
The meeting agenda supplies navigation context. These relationships form the proposed topic map without new records.

## Reader drafts

Draft A can preserve Q-01–03, Q-05, Q-07–08, and Q-10–12 within their stated evidence limits.
Its Q-04, Q-06, and Q-09 need these corrections. [Draft A](../drafts/answer-a.md#L3)

| Question | Supported answer | Consequence and next action |
| --- | --- | --- |
| Q-04 | A rejected payment can be retried with its original reference. Repeating an accepted reference must prevent a second payment. Late-arrival retention is unresolved. | Remove the invented seven-day duration and restore duplicate prevention. Draft editing owner is unknown. [Source](../sources/settlement/recovery.md#L3) |
| Q-06 | A caller without a matching action grant is denied. Several roles may contribute grants. No primary scalar role is defined. | Remove navigation allowance and first-role fallback. Draft editing owner is unknown. [Source](../sources/access/grants.md#L5) |
| Q-09 | YAML default is 15 minutes. Effective local JVM override is 480 minutes. One UAT token sample has a 900-second lifetime. Issuer configuration and UAT clock offset remain unknown. | Remove the claimed configuration proof. Engineering evidence owner is unknown. [Source](../sources/operations/runtime.md#L3) |

Draft B supports its four covered questions, including these three corrections.
It omits Q-02–03, Q-05, Q-07–08, and Q-10–12. Preserve supported Draft A answers when completing coverage. [Draft B](../drafts/answer-b.md#L3)

For Q-01, renewal stays eligible while credentials remain usable. No fixed active-session duration is specified.
Browser suspension remains unresolved. Production adoption is unverified. [Activity](../sources/portal/activity.md#L3)

For Q-02, the ui-42 fixture observed zero renewal requests during 15 seconds with mouse events every 100 ms.
The inspected 5,000 ms delay describes implementation. Controlled clocks and a stub issuer limit the observation.
Continuous real-duration renewal and UAT behavior remain unverified. [Observation](../sources/portal/observation.md#L3)

For Q-12, retain meaningful failed traces and link one canonical payload.
The existing failed-observation summary remains in `tasks/gaps.md`. No physical trace path is supplied by this fixture.
Equal hashes supply no cleanup permission. Consumer and provenance review remain required. [Retention](../sources/operations/retention.md#L5), [task evidence](../tasks/gaps.md#L3)

## Proposed wiki

All four statements require correction. The declared fresh-input list establishes no semantic completeness. [Proposed excerpt](../wiki/proposed.md#L3), [input list](../selection.json#L46)

| Statement | Evidence-backed replacement | Consequence and next action |
| --- | --- | --- |
| Exactly 15 seconds in production | No fixed active-session duration is specified. Production adoption remains unverified. | The local observation window cannot establish a production duration. Wiki owner is unknown. [Activity](../sources/portal/activity.md#L5), [observation](../sources/portal/observation.md#L3) |
| 16:00 every day | The 2022 proposal specifies weekday 16:00 Asia/Singapore. After-cutoff next-business-date processing needs approval. Holiday treatment is undecided. | Preserve proposal status and exceptions. Wiki owner is unknown. [Cutoff](../sources/settlement/cutoff.md#L3) |
| Single primary scalar role | Several roles can contribute grants through application, feature or subject, and action. No primary scalar role is defined. | Remove the invented identity mapping. Wiki owner is unknown. [Grants](../sources/access/grants.md#L5) |
| Delete matching failed traces | Retain meaningful failed traces. Review consumers and provenance before cleanup. Equal hashes alone grant no deletion authority. | Preserve historical evidence during later correction. Wiki owner is unknown. [Retention](../sources/operations/retention.md#L5) |

Any later wiki repair must use reconciled canonical inputs through the authorized wiki workflow.
Canonical completeness, semantic wiki quality, publication approval, and deployment remain separate review outcomes.

## Saved questions and continuation

The living question table has no machine Status column. Evaluate each Answer cell within its exact scope. [Living questions](../tasks/questions.md#L3)

- Retain KQ-01's saved UAT v1 policy answer for mouse, keyboard, and scroll.
- KQ-05 can inherit broad keyboard and scroll eligibility. Specific input distinctions remain unspecified.
- KQ-02 and KQ-03 still need scoped touch-policy decisions from `owner:portal`.
- KQ-04 remains an engineering question about ui-42 touch implementation. Its owner is unknown.
- KQ-06 concerns v2 timing. The ui-42 delay supplies no v2 answer. Its owner is unknown.
- KQ-07 synthetic-event eligibility remains unresolved with `owner:portal`.
- KQ-08 publication permission remains unanswered with `owner:portal`. Event eligibility supplies no publication authority.
- KQ-09 effective UAT issuer configuration remains unknown. Its engineering owner is unknown.
- Retain KQ-10's instruction to continue the saved recovery draft and preserve accepted work.
- Retain KQ-11's consumer-review requirement. KQ-12 retention duration still needs `owner:settlement`.

These answers do not automatically propagate across authority, actor, environment, version, decision, or question boundaries.
The checkpoint requests `luna` with `max` reasoning. Its observed dispatch is null.
Actual worker model, reasoning, and client settings remain `UNKNOWN`. Requested settings do not establish observed execution. [Checkpoint](../tasks/checkpoint.json#L16)

## Checks and limits

Actual checks covered source-to-output comparison, saved question scope, and all 29 supplied input hashes.
Planner, source verification, completion, and ingestion harness execution are `NOT_RUN` under this read-only review boundary.
Collection readiness remains unestablished. Business execution is `NOT_VERIFIED`.
The review created only the requested response and action log. All supplied inputs remained unchanged.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks covered input hashes and output presence only.
  - Automated checks do not establish complete writing review.
  - Synthetic fixtures do not establish business behavior.
  - Runtime source readiness, publication, and deployment were not verified.
```
