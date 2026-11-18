---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - The fixture is synthetic and establishes no actual business execution or adoption.
---

# Reader draft evaluation and corrected answers

Draft C covers all twelve questions and their core source predicates. Draft A contains four unsupported or contradicted substantive claims. Draft B answers four questions and leaves eight unanswered.

This evaluation uses the 25 supplied fixture inputs and both selected skills. All input and skill hashes match evaluation-input.json. Source dates and revision labels describe supplied evidence. Actual deployment and current business policy remain unverified.

## Evaluation method

The inventory below contains 45 question-level predicates derived from the questions and inspected sources. Related facts form one predicate where listed together. Repeated conditions count separately when two questions require them. Coverage can appear anywhere within each draft.

Missing predicates include omissions and contradictions. Invented findings count separate unsupported or contradicted assertions. These counts describe supplied drafts. They do not grade this evaluation.

| Question | Required predicates | A covered | B covered | C covered |
| --- | --- | --- | --- | --- |
| Q-01 | Qualifying activities, usable refresh credentials, unspecified fixed duration, unresolved suspension, unestablished production adoption | 3/5 | 3/5 | 5/5 |
| Q-02 | Event frequency, observation window and zero renewals, historical local date/revision, code delay, implementation classification, controlled clock/stub issuer, UAT/real-duration limits | 6/7 | 0/7 | 7/7 |
| Q-03 | Proposed weekday time/zone, unconfirmed current policy, undecided holidays, proposed next-business-date handling requiring approval | 4/4 | 0/4 | 4/4 |
| Q-04 | Rejected retry permitted, original reference, accepted-reference duplicate prevention, unresolved retention without a default | 1/4 | 4/4 | 4/4 |
| Q-05 | Union across roles, application/feature-or-subject/action chain, undefined primary scalar role | 3/3 | 0/3 | 3/3 |
| Q-06 | Denial without a matching action grant | 0/1 | 1/1 | 1/1 |
| Q-07 | Omission preserves state, empty array clears state | 2/2 | 0/2 | 2/2 |
| Q-08 | Unresolved identifier meaning, preserved upper calls without edits, unestablished parity | 3/3 | 0/3 | 3/3 |
| Q-09 | Default 15 minutes, effective local 480 minutes, UAT sample 900 seconds, unknown issuer configuration, unknown clock offset | 3/5 | 5/5 | 5/5 |
| Q-10 | Deployment plan, unconfirmed completion, unknown release owner | 3/3 | 0/3 | 3/3 |
| Q-11 | Prior consumer/provenance review, meaningful failures and canonical payload retained, incomplete consumer inventory | 3/3 | 0/3 | 3/3 |
| Q-12 | Failed traces retained, canonical payload linked, unspecified directory, insufficient hash equality, incomplete consumer inventory | 4/5 | 0/5 | 5/5 |
| Total | 45 predicates | 35/45 | 13/45 | 45/45 |

Draft A's implementation classification supports its answer about policy timing. Its migration wording supports the preservation constraint. Its Q-11 and Q-12 answers supply shared retention qualifications. These statements receive coverage credit.

## Review of each draft

| Dimension | Draft A | Draft B | Draft C |
| --- | --- | --- | --- |
| Factual fidelity | Four unsupported or contradicted claims, listed below | No invented substantive findings in its four answers | No invented substantive findings in its twelve core answers |
| Completeness | Ten missing predicates | Thirty-two missing predicates, eight questions omitted | All 45 core predicates covered |
| Organization | Twelve short, labeled answers | Four labeled answers, missing questions lack visible status | Twelve answers in a wide table with classes and sources |
| Visible qualifications | Several limits retained, duration, suspension, real-duration testing, and UAT uncertainty remain deficient | Covered answers preserve key qualifications, Q-01 remains incomplete | Draft status, historical scope, proposals, and unresolved evidence remain visible |
| Action clarity | Some review constraints supplied, material corrections remain necessary | Missing questions provide no next evidence | Follow-ups are explicit, scoped task-owner assignments can improve routing |

Draft evidence comes from [A, lines 3–25](../drafts/answer-a.md#L3-L25), [B, lines 3–6](../drafts/answer-b.md#L3-L6), and [C, lines 18–33](../drafts/answer-c.md#L18-L33).

### Material corrections and unanswered scope

| Question | Draft A outcome and correction | Draft B outcome | Draft C outcome | Supporting source |
| --- | --- | --- | --- | --- |
| Q-01 | Partly answered. Add unspecified duration and unresolved browser suspension. | Partly answered, same omissions | Answered | [Activity, lines 3–7](../sources/portal/activity.md#L3-L7) |
| Q-02 | Partly answered. Add the exclusion of continuous real-duration conclusions. | Unresolved, omitted | Answered | [Observation, lines 3–7](../sources/portal/observation.md#L3-L7) |
| Q-03 | Answered as a proposal, current applicability remains unconfirmed. | Unresolved, omitted | Answered | [Cutoff, lines 3–7](../sources/settlement/cutoff.md#L3-L7) |
| Q-04 | Partly answered, with contradiction. Add original references and duplicate prevention, remove the seven-day retention claim. | Answered | Answered | [Recovery, lines 3–7](../sources/settlement/recovery.md#L3-L7) |
| Q-05 | Answered | Unresolved, omitted | Answered | [Grants, lines 3–6](../sources/access/grants.md#L3-L6) |
| Q-06 | Contradicted. Replace navigation permission and first-role selection with denial. | Answered | Answered | [Grants, lines 5–7](../sources/access/grants.md#L5-L7) |
| Q-07 | Answered | Unresolved, omitted | Answered | [Migration, lines 3–5](../sources/access/migration.md#L3-L5) |
| Q-08 | Answered, entity meaning and parity remain unresolved. | Unresolved, omitted | Answered | [Migration, lines 3–7](../sources/access/migration.md#L3-L7) |
| Q-09 | Partly answered, with contradiction. Retain the sample, state issuer configuration and clock offset are unknown. | Answered | Answered | [Runtime, lines 3–6](../sources/operations/runtime.md#L3-L6) |
| Q-10 | Answered | Unresolved, omitted | Answered | [Runtime, line 7](../sources/operations/runtime.md#L7) |
| Q-11 | Answered using its Q-12 inventory qualification | Unresolved, omitted | Answered using its Q-12 failure-retention qualification | [Retention, lines 3–7](../sources/operations/retention.md#L3-L7) |
| Q-12 | Partly answered. State that the supplied instruction names no storage directory. | Unresolved, omitted | Answered | [Retention, lines 3–7](../sources/operations/retention.md#L3-L7) |

Draft A invents four substantive claims. These are seven-day retention, navigation permission without a matching grant, first-role selection, and proven effective UAT configuration. The corresponding source predicates contradict or fail to support each claim. [A, lines 9, 13, 19](../drafts/answer-a.md#L9-L19)

Draft C records automated_check as PASSED. The supplied inputs contain no execution receipt supporting that historical check assertion. This remains an unverified process claim, counted separately from substantive answer fidelity. [C, lines 1–9](../drafts/answer-c.md#L1-L9)

Some task-owner labels exist within exact scopes. KQ-12 assigns UAT v1 late-arrival policy to owner:settlement. KQ-11 assigns local v1 retention policy to maintainer. Their actual individual identities remain unspecified. Broader suspension, compatibility, issuer, and release ownership remain unresolved. [Living questions, lines 7–18](../tasks/questions.md#L7-L18)

## Supported corrected answers

### Q-01

Mouse, keyboard, and scroll activity keep renewal eligible while refresh credentials remain usable. The draft specifies no fixed active-session duration. Browser suspension recovery remains unresolved. Production adoption is unestablished.

Class is draft requirement for Portal operators, dated 1 November 2026. Confidence is high for the documented draft. Suspension needs a behavior decision, and adoption needs production evidence. The supplied files assign no suspension owner. [Activity, lines 3–7](../sources/portal/activity.md#L3-L7)

### Q-02

On 24 October 2026, local ui-42 received mouse events every 100 ms. The 15-second observation produced zero renewal requests. Inspected code schedules runExtend after 5,000 ms. This timing describes implementation. Intended policy duration remains unspecified by that observation and code delay.

Class is historical local execution and inspected implementation. Confidence is high for the bounded report. The fixture used a controlled clock and stub issuer. UAT and continuous real-duration renewal remain untested by that observation. [Observation, lines 3–7](../sources/portal/observation.md#L3-L7)

### Q-03

Current applicable cutoff policy is unknown. A 2022 demonstration proposes a weekday cutoff of 16:00 Asia/Singapore. Holiday treatment remains undecided. After-cutoff processing is proposed for the next business date, subject to owner approval.

Class is historical proposal. Confidence is high for proposal contents and limited for present applicability. The settlement owner must resolve holidays and approve handling. The source names no individual owner. [Cutoff, lines 3–7](../sources/settlement/cutoff.md#L3-L7)

### Q-04

A rejected payment can be retried with its original payment reference. Repeating an accepted reference must prevent a second payment. Late-arrival retention duration remains unresolved. The draft supplies no default duration.

Class is draft target behavior, dated 10 November 2026. Confidence is high for those statements. KQ-12 assigns the scoped UAT v1 retention decision to owner:settlement. That assignment supplies no retention duration or individual identity. [Recovery, lines 3–7](../sources/settlement/recovery.md#L3-L7), [Living questions, line 18](../tasks/questions.md#L18)

### Q-05

Evaluate the union of grants across roles through application, feature or subject, and action. Several roles can contribute grants. The draft defines no primary scalar role.

Class is draft CES rule, dated 10 November 2026. Confidence is high for this intent. The supplied files contain no implementation or rollout proof for the rule. [Grants, lines 3–6](../sources/access/grants.md#L3-L6)

### Q-06

A caller without a matching action grant is denied.

Class is draft CES rule, dated 10 November 2026. Confidence is high because the source states denial explicitly. The source contains no retained execution of a denial case. [Grants, lines 3–7](../sources/access/grants.md#L3-L7)

### Q-07

Omitting drawers preserves existing state. An empty drawers array clears existing state. The migration constraint requires existing upper-application calls to remain usable without caller edits.

Class is supplied inspected legacy contract api-9 and migration constraint dated 15 November 2026. Confidence is high for that supplied contract. Implementation parity remains unestablished. [Migration, lines 3–7](../sources/access/migration.md#L3-L7)

### Q-08

Identifier compatibility and implementation parity remain unestablished. The replacement identifier may name a different entity. Its mapping remains unresolved. The adapter must preserve existing upper-application calls without edits to those callers.

Class is unresolved identity mapping and supplied migration constraint. Confidence is high for the documented uncertainty. Compatibility requires resolved entity mapping and evidence against existing caller contracts. The supplied source names no responsible owner. [Migration, lines 3–7](../sources/access/migration.md#L3-L7)

### Q-09

Evidence captured on 26 October 2026 records a 15-minute YAML default. The effective local JVM override is 480 minutes. One UAT token sample has a 900-second lifetime. Effective issuer configuration and UAT clock offset remain unknown.

Class is captured environment evidence. Confidence is high for the recorded settings and single sample. Resolving effective UAT settings requires issuer configuration and clock-offset evidence. KQ-09 records its owner as unknown. [Runtime, lines 3–6](../sources/operations/runtime.md#L3-L6), [Living questions, line 15](../tasks/questions.md#L15)

### Q-10

The candidate's deployment remains unconfirmed. The release note records a deployment plan. The release owner is unknown.

Class is deployment planning with unresolved completion. Confidence is high for the source's stated limits. A deployment claim requires completion evidence and an identified accountable release owner. [Runtime, line 7](../sources/operations/runtime.md#L7)

### Q-11

Historical payload deletion requires prior consumer and provenance review. Retain meaningful failed traces. Link one canonical payload to avoid duplication. The historical consumer inventory remains incomplete. The supplied evidence identifies no specific payload as cleared for deletion.

Class is recorded maintainer instruction, dated 30 October 2026. Confidence is high for these conditions. Complete consumer and provenance review before selecting deletion candidates. KQ-11 names maintainer within local v1 retention scope. [Retention, lines 3–7](../sources/operations/retention.md#L3-L7), [Living questions, line 17](../tasks/questions.md#L17)

### Q-12

Retain meaningful failed traces and link one canonical payload. The supplied retention instruction specifies no storage directory. Equal hashes alone provide no deletion authorization. Consumer and provenance review remains necessary because the historical inventory is incomplete.

Class is recorded maintainer instruction. Confidence is high for retention conditions and the bounded absence of a directory. A required directory remains unspecified within the supplied files. The scoped maintainer assignment applies as described for Q-11. [Retention, lines 3–7](../sources/operations/retention.md#L3-L7), [Living questions, line 17](../tasks/questions.md#L17)

## Evidence applicability and conflicting summaries

The four knowledge records remain candidates. They provide no human publication approval. Portal and operations records point to historical observations. Access omits the explicit denial clause. Settlement says recovery has not been incorporated. Direct sources support the corrected answers despite those candidate omissions. [Selection, lines 46–53](../selection.json#L46-L53), [Access, lines 3–8](../knowledge/records/access.md#L3-L8), [Settlement, lines 3–8](../knowledge/records/settlement.md#L3-L8)

The saved progress summary claims all selected sources are complete. Its checkpoint marks recovery unfinished and grants held for canonical review. Reviewed receipt labels and listed wiki inputs cannot resolve those conflicting saved states. Meeting context introduces no new intent. [Progress, lines 3–4](../tasks/progress.md#L3-L4), [Checkpoint, lines 3–20](../tasks/checkpoint.json#L3-L20), [Selection, lines 16–53](../selection.json#L16-L53), [Context, line 3](../sources/context.md#L3)

The proposed wiki conflicts with direct sources on session duration, production adoption, cutoff scope, scalar roles, and failed-trace deletion. Its claims receive no evidentiary authority here. [Proposed wiki, lines 3–6](../wiki/proposed.md#L3-L6)

## Inspected primary-source register

All nine raw sources were opened in full. Each hash matches the supplied manifest. Exact supporting line ranges appear above.

| Source | Date or revision, evidence class | SHA-256 |
| --- | --- | --- |
| [Portal activity](../sources/portal/activity.md#L3-L7) | 1 November 2026, draft intent | 584404867d329bdcf7e7cc596e196b14d3fa0228fe9649a94d37a83624785c24 |
| [Portal observation](../sources/portal/observation.md#L3-L7) | 24 October 2026, ui-42 historical local evidence | cf8429472ac69752a878619fed615307829f55af52081dfc129b1a72012d2520 |
| [Settlement cutoff](../sources/settlement/cutoff.md#L3-L7) | 2022, demonstration proposal | aaef4a4467652a75c6b5a25583846d49de6356eba5f8a35244f5da4d3f1e5c69 |
| [Settlement recovery](../sources/settlement/recovery.md#L3-L7) | 10 November 2026, draft target | 7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6 |
| [Access grants](../sources/access/grants.md#L3-L7) | 10 November 2026, draft CES rule | c6fd5728e9254ead6e161621637de1d9293c3ba0c87fab184836ed26e42fb833 |
| [Access migration](../sources/access/migration.md#L3-L7) | api-9, 15 November 2026 migration constraint | ed3eec1fddb50b9c274e57504beee2beb38d32e3df97e8841474fdc8ba841582 |
| [Operations runtime](../sources/operations/runtime.md#L3-L7) | 26 October 2026, environment evidence and deployment plan | 2afa0ea96678a1c031456d6da1f3453ca33dab1c03ebce7568e9fcff6c6aa397 |
| [Operations retention](../sources/operations/retention.md#L3-L7) | 30 October 2026, maintainer instruction | cce786feee9068aa4b924701c77b63052a5c2083afa385893332805b790cd574 |
| [Meeting context](../sources/context.md#L3) | Date unspecified, navigation with no new intent | c22959f0afa460d3ab28c82054719a714013081a2bc27f9ec450e27a714f1031 |

The action log retains hashes for every inspected fixture input and selected skill. The manifest supplies base e1fd1e0efb2599ded0f940b77b86e18728e1963d and candidate d329c55e9e687adca6b9425b0cceae46adeff8d6. These labels received no independent Git or runtime verification. repo/revision.txt contains only a synthetic candidate description. [Repository label, line 1](../repo/revision.txt#L1)

## Review limits

This is a single-respondent review. No independent reader participated. Factual evaluation covers supplied files and their stated applicability. Automated validation checks hashes, links, question coverage, arithmetic, output boundaries, and review fields. Complete ASD writing review remains pending.
