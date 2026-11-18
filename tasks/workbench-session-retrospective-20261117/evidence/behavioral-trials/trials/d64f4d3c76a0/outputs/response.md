---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - The supplied fixture is synthetic.
  - Corrected answers have no independent reader review.
---

# Reader draft evaluation and corrected answers

Draft C covers all twelve substantive questions with direct source support.
Its late-arrival follow-up omits the recorded settlement role owner.
Draft A needs four completions and one denial correction.
Draft B answers three questions fully and one partly.

All conclusions concern the supplied synthetic fixture.
Implementation and execution statements describe claims in supplied sources.
The supplied material leaves current policy, production adoption, compatibility, and deployment evidence incomplete.

## Evaluation scope

The review covered all three drafts, twelve questions, nine raw sources, four candidate records, and supplied task context.
The selection file, checkpoint, proposed wiki, and synthetic revision marker were also inspected.
All 25 declared fixture input hashes matched.
Both selected skill hashes matched.

The same respondent evaluated the drafts and wrote the corrections.
Independent reader review remains pending.
Exact inspected paths, hashes, commands, and retrieval results appear in [the action log](actions.json).

### Question coverage

“Answered” means every substantive question part has supported coverage.
“Partly answered” marks material omissions or incorrect claims.
“Unresolved” marks an absent answer or a wholly contradicted answer.

| Question | Draft A | Draft B | Draft C | Supporting locator and required correction |
| --- | --- | --- | --- | --- |
| Q-01 | Partly answered. Duration and suspension are omitted. | Partly answered. Duration and suspension are omitted. | Answered. | Duration is unspecified. Suspension recovery is unresolved. Production adoption remains unverified. [Activity, lines 3–7](../sources/portal/activity.md) |
| Q-02 | Answered. Historical scope and timing class are retained. | Unresolved. Answer absent. | Answered. | Preserve the local observation, controlled clock, stub issuer, and implementation timing. [Observation, lines 3–7](../sources/portal/observation.md) |
| Q-03 | Answered. Proposal and unresolved approvals are retained. | Unresolved. Answer absent. | Answered. | Current policy remains unconfirmed. Preserve weekday, timezone, holiday uncertainty, and after-cutoff approval. [Cutoff, lines 3–7](../sources/settlement/cutoff.md) |
| Q-04 | Partly answered. Seven-day retention is unsupported. Original references and accepted duplicates are omitted. | Answered. | Answered. Follow-up owner needs correction. | Retry is permitted with the original reference. Accepted-reference repetition must preserve one payment. Retention duration is unresolved. [Recovery, lines 3–7](../sources/settlement/recovery.md) |
| Q-05 | Answered. | Unresolved. Answer absent. | Answered. | Preserve multi-role grant union through the complete application, feature or subject, and action chain. [Grants, lines 3–6](../sources/access/grants.md) |
| Q-06 | Unresolved. Navigation allowance and first-role selection contradict the rule. | Answered. | Answered. | A missing matching action grant causes denial. [Grants, line 7](../sources/access/grants.md) |
| Q-07 | Answered. | Unresolved. Answer absent. | Answered. | Omission preserves state. An empty array clears state. [Migration, lines 3–5](../sources/access/migration.md) |
| Q-08 | Answered. | Unresolved. Answer absent. | Answered. | Identifier meaning may differ. Mapping and implementation parity remain unresolved. Preserve upper callers without edits. [Migration, lines 6–7](../sources/access/migration.md) |
| Q-09 | Partly answered. One token sample cannot establish effective UAT configuration. | Answered. | Answered. | Retain both local values, the single UAT lifetime, and unknown issuer configuration and clock offset. [Runtime, lines 3–6](../sources/operations/runtime.md) |
| Q-10 | Answered. | Unresolved. Answer absent. | Answered. | The release note supplies a plan. Completion and release owner remain unknown. [Runtime, line 7](../sources/operations/runtime.md) |
| Q-11 | Answered. | Unresolved. Answer absent. | Answered. | Consumer and provenance review governs cleanup eligibility. The inventory remains incomplete. [Retention, lines 3–7](../sources/operations/retention.md) |
| Q-12 | Partly answered. The storage-location uncertainty is omitted. | Unresolved. Answer absent. | Answered. | Retain meaningful failed traces and link one canonical payload. The storage directory remains unspecified. [Retention, lines 5–7](../sources/operations/retention.md) |

Draft A has seven answered questions, four partly answered questions, and one unresolved question.
Draft B has three answered questions, one partly answered question, and eight unresolved questions.
Draft C has twelve substantively answered questions.

Draft C identifies the late-arrival owner as unknown.
The living question records the responsible role as `owner:settlement`.
The individual remains unnamed. [Draft C, line 21](../drafts/answer-c.md), [KQ-12, line 18](../tasks/questions.md)

Drafts A and B provide no exact source locators.
Draft C supplies locators for each answer.
The review reopened the cited raw files and checked their recorded dates and revisions.

## Supported corrected answers

Confidence describes support within the supplied files.
It gives no assurance of actual business execution.

| Question and corrected answer | Evidence class and applicability | Confidence and rationale | Exact source locator | Material limit and next evidence |
| --- | --- | --- | --- | --- |
| **Q-01** Mouse, keyboard, and scroll activity keep renewal eligible while refresh credentials remain usable. Fixed active-session duration remains unspecified. Browser suspension recovery remains unresolved. Production adoption remains unverified. | Draft requirement, 1 November 2026, Portal operators. | High for the documented draft and its qualifications. | [Activity, lines 3–7](../sources/portal/activity.md) | Obtain suspension intent and production adoption evidence. Responsible owners for those exact questions remain unknown. |
| **Q-02** Mouse events every 100 ms produced zero renewal requests during a 15-second local observation. The observation occurred on 24 October 2026 at ui-42. The source reports runExtend scheduling after 5,000 ms. That delay describes implementation. Policy duration remains unspecified. | Historical local execution and reported inspected implementation, ui-42. | High for the recorded bounded observation. | [Observation, lines 3–7](../sources/portal/observation.md), [Activity, line 5](../sources/portal/activity.md) | The controlled clock and stub issuer limit the evidence to this fixture. UAT and continuous real-duration renewal remain unverified. |
| **Q-03** Current cutoff policy remains unconfirmed. The 2022 demonstration proposes a weekday cutoff of 16:00 Asia/Singapore. Holiday treatment remains undecided. After-cutoff processing is proposed for the next business date, subject to owner approval. | Historical demonstration proposal. Current applicability remains unknown. | High for proposal contents. Current policy support is insufficient. | [Cutoff, lines 3–7](../sources/settlement/cutoff.md) | The settlement owner must resolve holidays and approve after-cutoff handling. The individual owner remains unknown. |
| **Q-04** The draft permits retrying a rejected payment with its original payment reference. Repeating an accepted reference must preserve a single payment. Late-arrival retention duration remains unresolved, with no supplied default. | Draft target behavior, 10 November 2026. | High for the explicit retry, duplicate, and retention clauses. | [Recovery, lines 3–7](../sources/settlement/recovery.md) | Resolve retention duration with `owner:settlement`. The individual remains unnamed. [KQ-12, line 18](../tasks/questions.md) |
| **Q-05** Evaluate the union of grants through application, feature or subject, and action. Several roles can contribute grants. A primary scalar role remains undefined. | Draft CES rule, 10 November 2026. | High for the stated evaluation rule. | [Grants, lines 3–6](../sources/access/grants.md) | Implementation and rollout require separate evidence. Owner remains unknown. |
| **Q-06** A caller without a matching action grant is denied. | Draft CES rule, 10 November 2026. | High for the explicit denial clause. | [Grants, lines 3–7](../sources/access/grants.md) | Executed denial behavior remains unverified. Owner remains unknown. |
| **Q-07** Omitting drawers preserves existing state. An empty drawers array clears state. | Supplied inspected legacy contract, api-9, and migration constraint dated 15 November 2026. | High for the documented contract. | [Migration, lines 3–5](../sources/access/migration.md) | Implementation parity remains unestablished. |
| **Q-08** Compatibility remains unestablished. The replacement identifier may name a different entity. Its mapping remains unresolved. The adapter must preserve existing upper-application calls without caller edits. | Migration constraint dated 15 November 2026 and unresolved identity mapping. | High for the uncertainty and preservation requirement. | [Migration, lines 3–7](../sources/access/migration.md) | Establish identifier meaning and adapter parity through source and execution evidence. Owner remains unknown. |
| **Q-09** Evidence captured on 26 October 2026 records a 15-minute YAML default and effective 480-minute local JVM override. One UAT token sample has a 900-second lifetime. Effective issuer configuration and UAT clock offset remain unknown. | Captured local environment evidence and one UAT token sample. | High for the recorded values. The effective UAT setting remains unresolved. | [Runtime, lines 3–6](../sources/operations/runtime.md) | Capture effective issuer configuration and clock offset. The sample alone supports only its observed lifetime. Owner remains unknown. |
| **Q-10** Deployment completion remains unconfirmed. The candidate release note describes a deployment plan. The release owner remains unknown. | Deployment plan and unresolved completion, recorded 26 October 2026. | High for the documented qualification. | [Runtime, lines 3–7](../sources/operations/runtime.md) | Obtain deployment completion evidence and identify the release owner. |
| **Q-11** Historical cleanup requires consumer and provenance review. Retain meaningful failed traces and link one canonical payload. The historical consumer inventory remains incomplete. | Recorded maintainer instruction, 30 October 2026. | High for the explicit review and retention requirements. | [Retention, lines 3–7](../sources/operations/retention.md) | Identify eligible payloads through completed consumer and provenance review. Inventory completion owner remains unknown. |
| **Q-12** Retain meaningful failed traces and link one canonical payload. The supplied instruction leaves the storage directory unspecified. Consumer and provenance review remains required when hashes match. | Recorded maintainer instruction, 30 October 2026. | High for retention and deletion conditions. Storage location remains unresolved. | [Retention, lines 3–7](../sources/operations/retention.md) | Obtain an authoritative directory decision if a storage path is required. The directory owner remains unknown. |

## Source register and retrieval limits

The following nine raw files supplied the answer evidence.
Full SHA-256 values appear in [the action log](actions.json).

| Source and exact locator | Recorded date or revision | Evidence class |
| --- | --- | --- |
| [Portal activity, lines 3–7](../sources/portal/activity.md) | 1 November 2026 | Draft requirement for Portal operators |
| [Portal observation, lines 3–7](../sources/portal/observation.md) | 24 October 2026, ui-42 | Historical local observation and reported code timing |
| [Settlement cutoff, lines 3–7](../sources/settlement/cutoff.md) | 2022 | Demonstration proposal |
| [Settlement recovery, lines 3–7](../sources/settlement/recovery.md) | 10 November 2026 | Draft target behavior |
| [Access grants, lines 3–7](../sources/access/grants.md) | 10 November 2026 | Draft CES rule |
| [Access migration, lines 3–7](../sources/access/migration.md) | api-9, 15 November 2026 | Legacy contract and migration constraint |
| [Operations runtime, lines 3–7](../sources/operations/runtime.md) | 26 October 2026 | Environment evidence and deployment plan |
| [Operations retention, lines 3–7](../sources/operations/retention.md) | 30 October 2026 | Recorded maintainer instruction |
| [Meeting context, line 3](../sources/context.md) | Unknown | Navigation context duplicating activity intent |

Candidate records retain draft status.
The settlement candidate omits the recovery source.
The access candidate omits the denial clause.
Raw-source review therefore supplies material answer details. [Settlement candidate, lines 7–8](../knowledge/records/settlement.md), [Access candidate, lines 3–8](../knowledge/records/access.md)

The saved progress summary declares all selected sources complete.
The checkpoint records recovery as unfinished and access grants as held.
Receipt labels and wiki freshness provide insufficient support for that completion claim. [Progress, lines 3–4](../tasks/progress.md), [Checkpoint, lines 3–10](../tasks/checkpoint.json), [Selection, lines 16–53](../selection.json)

The proposed wiki contradicts the raw sources on renewal duration, production adoption, cutoff scope, scalar roles, and retention.
Its claims cannot support the corrected answers. [Proposed wiki, lines 3–6](../wiki/proposed.md)

Saved answers retain their exact authority, actor, environment, version, decision, and question scope.
KQ-01 answers qualifying events for UAT v1.
KQ-12 identifies the late-arrival role owner.
Other unanswered questions retain their uncertainty. [Living questions, lines 3–18](../tasks/questions.md)

The repository marker contains only a synthetic candidate description.
The supplied revision declarations provide identifiers for this exercise.
They supply no independently inspected implementation history. [Repository marker, line 1](../repo/revision.txt), [Evaluation input](../evaluation-input.json)

Retrieval remained within the named fixture and the two selected skill files.
Draft and source hashes were checked before and after output creation.
Writes were confined to the requested evaluation and action-log files.

## Automated checks

The retained check result covers these mechanical conditions.

- All 25 declared fixture input hashes match their supplied values.
- Both selected skill hashes match their supplied values.
- The evaluation table contains all twelve question identifiers.
- The corrected-answer register contains all twelve question identifiers.
- Every Markdown link resolves to an existing local file.
- Required writing-review fields remain present.

Complete ASD writing review and independent reader review remain pending.

