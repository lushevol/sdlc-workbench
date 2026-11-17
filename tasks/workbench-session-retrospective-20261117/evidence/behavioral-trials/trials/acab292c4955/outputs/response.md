# Wiki excerpt review

> All four proposed sentences require correction. Two selected sources have material coverage gaps despite reviewed receipt declarations.

## Scope and review evidence

This read-only review covers every listed fixture input and both selected skill files.
All 24 input hashes and both skill hashes match evaluation-input.json.
The fixture describes synthetic sources and candidate records with no human publication approval.
Confidence is high for textual support and omission findings because the original sources are complete within this fixture.

The semantic reviewer is the current assistant, respondent_acab292c4955.
The reviewed excerpt hash is a239dcb3dac3ff6526fbf6008e52362ca3fd7d0fd1c85affec92363aa1a03ba4.
The action log records review timing, exact source hashes, commands, results, and available execution settings.
Model identity, reasoning setting, and host client remain UNKNOWN.
The checkpoint requests luna with max reasoning and records a null observed dispatch.
Those declarations provide no observation of current execution settings. [Checkpoint, lines 16–20](../tasks/checkpoint.json)

The declared base revision is e1fd1e0efb2599ded0f940b77b86e18728e1963d.
The declared candidate revision is d329c55e9e687adca6b9425b0cceae46adeff8d6.
The supplied revision file contains only a synthetic candidate label.
The inspected evidence supports source comparison within this fixture. [Revision file](../repo/revision.txt)

## Proposed claim register

| Claim and classification | Evidence and finding | Consequence | Owner and next action |
| --- | --- | --- | --- |
| Wiki line 3. Fixed 15-second production renewal. Mixed intent, execution, and deployment. | Activity keeps renewal eligible while refresh credentials remain usable. The source specifies no fixed duration. Browser suspension remains unresolved. Production adoption is unverified. The 15 seconds belongs to a historical local observation. | Readers could adopt a fabricated production limit and assume deployment. | owner:portal for policy scope. Deployment owner unknown. Replace this sentence with qualified activity intent. Retain the local observation separately. |
| Wiki line 4. Daily 16:00 settlement cutoff. Intent. | The 2022 demonstration proposes weekday 16:00 Asia/Singapore. After-cutoff processing moves to the next business date, subject to owner approval. Holiday treatment remains undecided. | Readers could apply an unapproved daily cutoff across holidays and time zones. | owner:settlement. Preserve proposal status and both unresolved decisions. |
| Wiki line 5. Single primary scalar role. Intent. | The draft evaluates the union of application, feature or subject, and action grants across roles. It defines no primary scalar role. A missing matching action grant denies access. | The proposed role model could change access decisions and hide the denial rule. | Owner unknown. Restore the draft grant model and review the omitted denial clause. |
| Wiki line 6. Delete matching failed traces as noise. Intent. | The maintainer requires consumer and provenance review before historical deletion. Meaningful failed traces require retention. Equal hashes provide insufficient deletion authority. The consumer inventory remains incomplete. | Readers could discard meaningful failures before identifying consumers and provenance. | Maintainer. Withdraw this deletion claim and preserve the retention instruction. |

Evidence for line 3 comes from draft intent and qualified historical execution.
The observation used revision ui-42, a controlled clock, and a stub issuer.
Its scope excludes UAT and continuous real-duration renewal conclusions. [Activity, lines 3–7](../sources/portal/activity.md), [Observation, lines 3–7](../sources/portal/observation.md), [Portal record, lines 3–8](../knowledge/records/portal.md)

The settlement proposal supplies its own age, status, timezone, weekday condition, and approval dependency. [Cutoff, lines 3–7](../sources/settlement/cutoff.md), [Settlement record, lines 3–8](../knowledge/records/settlement.md)

The access source explicitly supports both multi-role grants and denial.
The existing candidate preserves the grant union but omits denial. [Grants, lines 3–7](../sources/access/grants.md), [Access record, lines 3–8](../knowledge/records/access.md)

The retention instruction and existing candidate agree on retention and cleanup constraints. [Retention, lines 3–7](../sources/operations/retention.md), [Operations record, lines 3–5](../knowledge/records/operations.md)

## Claim and omission inventory

| Reader scope | Supported content and required qualification | Current gap and destination |
| --- | --- | --- |
| Q-01 | Portal operators qualify through mouse, keyboard, and scroll activity while refresh credentials remain usable. No fixed active-session duration is specified. Browser suspension recovery is unresolved. Production adoption is unverified. | Replace wiki line 3. Preserve all conditions in the Portal Activity summary, sourced through knowledge/records/portal.md#activity. |
| Q-02 | At ui-42 on 24 October 2026, mouse events every 100 ms produced zero renewal requests during 15 seconds. Code schedules runExtend after 5,000 ms. Controlled clock and stub issuer constrain the evidence. | Preserve the complete historical implementation and execution evidence in tasks/gaps.md#portal-local-investigation. Link it from the Portal investigation summary. |
| Q-03 | The 2022 proposal supplies weekday 16:00 Asia/Singapore and next-business-date processing after cutoff. Owner approval and holiday treatment remain pending. | Replace wiki line 4 with qualified proposal content from knowledge/records/settlement.md#cutoff. |
| Q-04 | A rejected payment can be retried with its original reference. Repeating an accepted reference must prevent a second payment. Late-arrival retention remains unresolved, with no supplied default. | Material canonical omission. Continue tasks/recovery-draft.md, then propose recovery content for knowledge/records/settlement.md#recovery under later authorization. |
| Q-05 | Several roles may contribute application, feature or subject, and action grants. No primary scalar role is defined. | Replace wiki line 5 using knowledge/records/access.md#grants. Preserve draft status beside the derived claim. |
| Q-06 | Absence of a matching action grant denies access. | Material canonical omission. Add this draft intent to the proposed access review scope before deriving a complete grant summary. |
| Q-07 | Omitted drawers preserves state. An empty array clears state. | Preserve knowledge/records/access.md#caller-migration and include these conditions in its derived migration summary. |
| Q-08 | The adapter must preserve upper-application calls without caller edits. Replacement identifiers may identify different entities. Identifier mapping is unresolved, and implementation parity is unverified. | Preserve the migration constraint and uncertainty together. Identifier compatibility requires further engineering evidence. |
| Q-09 | YAML default is 15 minutes. Effective local JVM override is 480 minutes. One UAT token sample lived 900 seconds. Effective issuer configuration and UAT clock offset remain unknown. | Preserve these environment-specific observations in tasks/gaps.md#environment. Link them from the derived operations context. |
| Q-10 | The candidate release note describes a deployment plan. Completion is unconfirmed. Release owner is unknown. | Preserve the deployment limit in tasks/gaps.md#environment and beside any release claim. |
| Q-11 | Historical cleanup requires consumer and provenance review. Retain meaningful failures and link one canonical payload. | Replace wiki line 6 using knowledge/records/operations.md#retention. |
| Q-12 | Meaningful failed traces require retention. Equal hashes alone provide insufficient deletion authority. The historical consumer inventory is incomplete. | Preserve meaningful failed-trace payloads at their canonical evidence locations, with links. Exact payload paths are absent from this fixture. |

The question inventory defines these twelve reader scopes. [Reader questions, lines 3–25](../questions.md)

The recovery source supports the missing original-reference and duplicate conditions directly.
Its unresolved retention duration remains a policy question.
The saved recovery draft omits these source details. [Recovery source, lines 3–7](../sources/settlement/recovery.md), [Recovery draft, line 3](../tasks/recovery-draft.md)

Migration statements derive from inspected legacy API revision api-9 and the supplied 15 November 2026 constraint.
The runtime observations derive from captured local evidence dated 26 October 2026. [Migration, lines 3–7](../sources/access/migration.md), [Runtime, lines 3–7](../sources/operations/runtime.md)

## Source destinations and reviewed dispositions

These are review dispositions and proposed destinations. Authorized output writes are confined to this review and its action log.

| Original source | Authority and disposition | Existing or proposed destination |
| --- | --- | --- |
| sources/portal/activity.md | Draft requirement, 1 November 2026. Existing candidate preserves the complete stated meaning. Supported no-change canonical disposition. | knowledge/records/portal.md#activity. Derived Portal summary must retain conditions, suspension uncertainty, and production limits. |
| sources/portal/observation.md | Historical local execution, 24 October 2026, revision ui-42. Preserve as implementation and execution evidence. | tasks/gaps.md#portal-local-investigation, linked by knowledge/records/portal.md#investigation-evidence. |
| sources/settlement/cutoff.md | 2022 demonstration proposal. Preserve proposal status, conditions, and pending owner decisions. | knowledge/records/settlement.md#cutoff and its derived settlement summary. |
| sources/settlement/recovery.md | Draft target, 10 November 2026. Incorporation remains incomplete. The declared no-change receipt lacks semantic support. | Continue tasks/recovery-draft.md. Proposed canonical destination is knowledge/records/settlement.md#recovery. |
| sources/access/grants.md | Draft CES rule, 10 November 2026. Union rules are retained. Denial remains absent from the canonical candidate. Partial incorporation. | knowledge/records/access.md#grants needs a reviewed proposal for the missing denial clause. |
| sources/access/migration.md | Inspected api-9 contract and supplied 15 November migration constraint. Existing candidate retains the contract and limits. | knowledge/records/access.md#caller-migration and the linked derived migration summary. |
| sources/operations/runtime.md | Captured local evidence, 26 October 2026. Preserve separated environment observations and deployment uncertainty. | tasks/gaps.md#environment, linked from knowledge/records/operations.md. |
| sources/operations/retention.md | Recorded maintainer instruction, 30 October 2026. Existing candidate preserves the rule. | knowledge/records/operations.md#retention. Keep failed traces linked to one canonical payload. |
| sources/context.md | Navigation agenda. It explicitly supplies no new conditions, exceptions, or target behavior. Supported no-change disposition. | Existing Portal Activity context suffices. selection.json retains the explicit navigation disposition. |

## Receipt and checkpoint reconciliation

| Selected source | Recorded receipt | Review result |
| --- | --- | --- |
| portal/activity.md | Reviewed no_change, with Portal record destination and matching-intent reason. | Supported within this fixture. |
| settlement/recovery.md | Reviewed no_change, empty outputs, and absent reason. | Unsupported completion claim. The candidate says no recovery source has been incorporated. The checkpoint marks recovery unfinished. |
| access/grants.md | Reviewed no_change, empty outputs, and absent reason. | Partial coverage. The denial clause remains missing. The checkpoint holds canonical review. |
| context.md | Reviewed no_change, with explicit navigation reason. | Supported. The source supplies no new behavior. |

The progress summary treats reviewed receipt flags and wiki freshness as proof that all four sources are complete.
The inspected content supports two completed no-change dispositions and two remaining semantic gaps.
The checkpoint preserves accepted Portal and context work.
It directs continuation from the recovery draft and retains the access review hold. [Selection, lines 16–53](../selection.json), [Progress, lines 3–4](../tasks/progress.md), [Checkpoint, lines 3–11](../tasks/checkpoint.json)

Recovery details and access denial already have direct draft-source support.
Their incorporation review can proceed within appropriate authorization.
Late-arrival retention requires a remaining owner answer.
Candidate publication requires its separate human review. [Recovery source](../sources/settlement/recovery.md), [Grants source](../sources/access/grants.md), [Living questions, lines 14–18](../tasks/questions.md)

## Retention mapping for removed or changed facts

| Fact | Classification | Disposition and exact evidence |
| --- | --- | --- |
| Exactly 15 seconds of production renewal | Unsupported intent and deployment assertion | Withdrawn as a policy claim. Preserve 15 seconds as historical local execution in sources/portal/observation.md, lines 3–7, and tasks/gaps.md, line 4. |
| Mouse events every 100 ms, zero requests over 15 seconds | Execution | Preserved in sources/portal/observation.md, lines 3–7, and tasks/gaps.md, line 4, including ui-42, date, controlled clock, and stub issuer. |
| 5,000 ms runExtend delay | Implementation | Preserved in sources/portal/observation.md, line 6, and tasks/gaps.md, line 4. Policy duration remains unspecified. |
| Daily 16:00 cutoff | Unsupported widening of intent | Withdrawn. Preserve the weekday 16:00 Asia/Singapore proposal and next-business-date condition in sources/settlement/cutoff.md, lines 3–7. |
| One primary scalar role | Unsupported intent | Withdrawn. Preserve multi-role grants and explicit denial from sources/access/grants.md, lines 3–7. |
| Failed traces treated as deletable noise | Unsupported intent | Withdrawn. Preserve failed traces, canonical payload linkage, and consumer review from sources/operations/retention.md, lines 5–7. |
| Seven-day late-arrival retention in reader draft A | Unsupported intent | Withdrawn. Preserve unresolved duration from sources/settlement/recovery.md, line 7. |
| 15-minute YAML default, 480-minute local override, 900-second UAT sample | Implementation and observed token evidence | Preserved separately in sources/operations/runtime.md, lines 5–6, and tasks/gaps.md, line 7. Effective UAT configuration remains unknown. |

All dispositions describe review conclusions.
The inspected original files, candidate records, drafts, receipts, checkpoint, and proposed wiki remain preserved byte-for-byte.

## Reader-draft checks

Draft A covers all question identifiers but contains three additional material errors.
Q-04 invents seven-day retention and omits original-reference and accepted-duplicate conditions.
Q-06 invents navigation allowance and first-role selection.
Q-09 treats one token sample as proof of effective UAT configuration. [Draft A, lines 9–19](../drafts/answer-a.md)

Draft A Q-01 also omits the unspecified duration and unresolved browser suspension.
Draft B preserves the missing Q-04 reference conditions and corrects Q-06 and Q-09.
Its Q-01 retains activity eligibility and production uncertainty but also omits duration and suspension.
Draft B covers four question identifiers.
A complete reader answer needs the remaining eight scopes above.
Both recovery answers also need the source's draft status. Use “can be retried” to preserve the permitted-retry scope. [Draft A, line 3](../drafts/answer-a.md), [Draft B, lines 3–6](../drafts/answer-b.md), [Recovery source, line 3](../sources/settlement/recovery.md)

## Remaining findings and limits

| Finding | Evidence and consequence | Owner | Next action |
| --- | --- | --- | --- |
| Recovery incorporation incomplete | Direct recovery rules remain outside the candidate. Readers lose reference reuse and duplicate prevention. | Canonical reviewer unknown. Retention policy owner is owner:settlement. | Continue the saved draft. Preserve unresolved retention. |
| Access denial omitted | The draft source explicitly denies a caller lacking a matching action grant. Existing candidate coverage is partial. | Unknown | Review and propose the missing draft clause. |
| Cutoff approval and holiday handling unresolved | The 2022 proposal provides insufficient support for a current daily operating rule. | owner:settlement | Obtain the owner's scoped decision before describing an effective cutoff policy. |
| Browser suspension and production adoption unresolved | Activity intent leaves suspension open and supplies no production adoption evidence. | owner:portal for policy. Deployment owner unknown. | Preserve the uncertainty and obtain evidence for each affected conclusion. |
| Identifier mapping and parity unresolved | The migration source warns of different entity meanings. Existing callers require preservation. | Unknown | Resolve mapping and inspect compatible implementation evidence. |
| UAT configuration and deployment evidence incomplete | A token sample and deployment plan leave configuration, clock offset, completion, and owner unknown. | Unknown | Retain the observed values and seek environment-bound evidence. |
| Historical cleanup inventory incomplete | Hash equality leaves consumer and provenance requirements unresolved. | Maintainer | Complete consumer and provenance review before authorized historical cleanup. |

Saved answers retain their exact scope.
KQ-01 resolves qualifying event classes for operator/UAT/v1.
Touch, synthetic events, input subtypes, ui-42 touch implementation, and v2 timing remain separately unanswered.
KQ-08 publication approval remains unanswered.
KQ-10 preserves the recovery resume direction.
KQ-11 supplies the consumer-review constraint.
KQ-12 leaves retention duration unresolved. [Living questions, lines 3–18](../tasks/questions.md)

The review establishes textual claim support, omissions, and source dispositions within a synthetic fixture.
Implementation conformance, live behavior, production adoption, and human approval remain outside the available evidence.
Linked skill references outside the permitted fixture and selected skill files were outside the inspection scope.
The two selected SKILL.md files supplied the applied review instructions.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cover input hashes, output structure, local evidence links, and preserved input bytes.
  - Automated checks do not establish complete writing review.
```
