---
artifact_kind: change-request
id: UI-ENTRY-CLARIFICATION-20261022
version: 4
status: draft
owner: unknown
source_refs: [SRC-ui-entry-clarification-20261022, SRC-ui-entry-scope-clarification-20261022, SRC-ui-entry-owner-clarification-20261022, SRC-ui-empty-entity-clarification-20261022, SRC-ui-claude-recovery-20261022, SRC-ui-empty-entity-owner-scope-20261022, SRC-ui-empty-subject-clarification-20261022, SRC-ui-empty-subject-owner-scope-20261022]
related_ids: [UI-COVERAGE-20261022, KT-authentication-and-sessions, KT-sdk-and-entitlements]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal-entry and tile-policy clarification

> **Critical conclusions: Owner approval remains unconfirmed**
>
> **The user selected denial in all portal environments and identified `portal team` as the entry-policy owner.**
> Action: Obtain applicable owner approval evidence. Consequence: Policy acceptance and publication remain blocked.
> Owner: `portal team`, user-reported for entry policy only. Evidence: The [owner answer](evidence/clarification-20261022/ui-q-002-owner-source.json).
>
> **Answer the consolidated knowledge questions.**
> Action: Complete the [single question document](05-knowledge-questions.md).
> Consequence: Unanswered material questions block the affected policy or evidence decision. Owner: unknown for unresolved topics.
> Evidence: The [batch-workflow instruction](evidence/clarification-20261022/batched-question-workflow-source.json).

## Current task state

This living stage covers portal-entry intent, empty-entity denial, and empty-subject access through one configured entity.
The [question document](05-knowledge-questions.md) now owns the active clarification questions across the knowledge collection.
The user selected denial for an authenticated SC user without entitlement for any registered application entity.
The user selected local, test, UAT, and production environments.
The user also selected hidden tiles and denied direct launch when a tile has no configured EMS2 entity.
The user identifies `portal team` as the tile-rule owner across local, test, UAT, and production.

These answers establish user-stated intent, not authenticated owner authority, publication approval, or implementation verification.

Both security topics remain version 6 candidate drafts, with `owner: unknown` and `verified: []`.
The onboarding topic is version 3 and retains the same review limits.
The reference-priority instruction changes evidence procedure only.
The later empty-subject answers change domain knowledge.

Named next phase: Approved-policy acceptance and downstream behavior verification.
Readiness: `NEEDS_CLARIFICATION`.
The user identifies `portal team` for entry policy, empty-entity denial, and empty-subject access across all portal environments.
Owner authority, approval, and deployed enforcement remain unconfirmed.

Further questions and authorized evidence collection can continue.
The selected scope includes candidate records, provenance, validation, and the required project commit.
Implementation, publication, and application execution remain outside this clarification stage.
Assessor: `agent:codex`. Assessment time: `2026-10-22T12:36:31Z`.

## Proposed change

Record the selected entry and tile rules in candidate knowledge.
Preserve historical conflicts, prior answers, case definitions, and earlier execution results.

## Scope and affected artifacts

The affected records are three domain topics, their navigation, this stage, source provenance, and new audit events.
No runtime symbol, caller, importer, or application interface changes.
Qualitative risk: Low for runtime behavior. Incorrect authority wording could misstate policy, so review limits remain explicit.

The later workflow instruction updates this record, task navigation, and the project guide.
It changes no domain rule.
Qualitative risk: Low. The procedure preserves evidence classes and existing publication gates.

## Options and consequences

The user selected entry denial instead of the older allow-entry proposal.
The user selected hidden tiles and denied direct launch instead of implicit access through missing EMS2 configuration.
The user selected visibility and launch through one configured entity when the subject setting is empty.
These selections remain candidate intent. They grant no publication approval.

## Requested decision and actual disposition

The entry rule, entry scope, entry owner, and tile behavior have recorded answers.
The user also confirmed the tile-rule owner and all-environment scope.
The user selected empty-subject access through one configured entity and confirmed portal-team ownership across all environments.
Multiple-entity matching remains the next unresolved tile-policy question.

## Request and source facts

The user requested one blocker question at a time.
The [source snapshots](#sources-and-evidence-limits) retain the exact questions, choices, and supplied answers.
Capture times do not identify response times.
The [recovered session excerpt](evidence/clarification-20261022/recovered-session-source.json) retains recorded response timestamps from the original Claude session.
Original snapshots retain their earlier null response timestamps and exact bytes.
The supplemental scope source does not rewrite the first snapshot's earlier applicability limit.

### User reference priority

The user instructed the agent to record their input as the first-priority reference.
The [exact instruction](evidence/clarification-20261022/user-reference-priority-source.json) retains the original wording.
The [project procedure](../../AGENTS.md#user-input-and-reference-priority) applies that preference before further investigation or delegation.
The latest explicit user clarification governs intended behavior within its stated scope.
Historical sources remain available when they conflict.
Observed behavior, execution verification, and publication approval remain separate.

The process instruction supplies no business answer.
The later [empty-subject answers](#empty-subject-configuration) supply the rule, owner, and environment scope.
Domain knowledge update: not applicable, because this input changes evidence procedure only.
No governed record version, source manifest entry, or governance audit event changes for this instruction.

### UI-Q-002

| Field | Current record |
| --- | --- |
| Question | The [exact entry question](evidence/clarification-20261022/ui-q-002-source.json) concerns an authenticated SC user without registered application entity entitlement. |
| Answer | `A. Deny entry` |
| User-stated rule | An authenticated SC user with no entitlement for any registered application entity must be denied portal entry. |
| Status | Rule, scope, and owner identity resolved as user reports. Owner authority, approval, and deployed enforcement remain unconfirmed. |
| Scope answer | `All portal environments`; local, test, UAT, and production. See the [exact scope question and answer](evidence/clarification-20261022/ui-q-002-scope-source.json). |
| Resolution owner | `portal team`, user-reported for entry policy only. See the [exact owner question and answer](evidence/clarification-20261022/ui-q-002-owner-source.json). |
| Consequence | The historical entry conflict no longer blocks recording the user's selection. Policy acceptance remains blocked. |
| Next action | Obtain portal-team approval evidence. Do not repeat the answered rule, environment, or owner question. |

### Empty entity configuration

What behavior applies when an application's configured entity list is empty?
The [retained answer](evidence/clarification-20261022/empty-entity-source.json) selects `Deny tile access (Recommended)`.
Hide the tile and deny direct launch until an EMS2 entity is configured.
This answer leaves application data permissions separate.
The [business criterion](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001) isolates the tile rule from portal-entry eligibility.

| Field | Current record |
| --- | --- |
| Answer status | Tile behavior, ownership, and environment scope are resolved as user reports. |
| Owner and scope answer | `Yes—portal team, all environments`. See the [exact answer](evidence/clarification-20261022/empty-entity-owner-scope-source.json). |
| Resolution owner | `portal team`, user-reported for this rule. |
| Environment scope | local, test, UAT, and production. |
| Consequence | Owner approval and deployed enforcement remain unconfirmed. |
| Next action | Continue with the [multiple-entity question](#multiple-entity-configuration). Do not repeat the answered tile-rule ownership or scope question. |
| Limits | No approved policy, deployment binding, denial wording, HTTP status, or passing execution is established. |

The [historical question](evidence/knowledge-inspection.md#open-rule-decisions) retains its earlier unresolved state.
The [empty-role example, lines 13–19](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L13-L19>) does not define empty-entity behavior.

### Empty subject configuration

The [exact rule answer](evidence/clarification-20261022/empty-subject-source.json) selects `Allow access through the entity check`.
The [owner and scope answer](evidence/clarification-20261022/empty-subject-owner-scope-source.json) selects `Yes—portal team, all environments`.
These explicit user answers are the first-priority references for intended behavior within their stated scope.
The user must satisfy portal-entry requirements and hold entitlement for the tile's single configured EMS2 entity.
When the subject setting is empty, the portal must show the tile and authorize launch through the entity check.

Owner: `portal team`. Scope: local, test, UAT, and production.
Rule, owner, and scope questions are answered. Publication approval and deployed enforcement remain unconfirmed.
[UI-EMPTY-SUBJECT-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001) defines the measurable result.
The answer selects no multiple-entity matching rule or application data permission.

### Multiple entity configuration

The active multiple-entity question is in the [consolidated question document](05-knowledge-questions.md).
Its answer remains unknown. The earlier single-entity answer does not select that rule.
Keep answers in the consolidated document. Do not maintain a second answer field here.

### Batched review workflow

The user requested one question document, followed by answer handback, review, refinement, and repeated clarification rounds.
The [exact instruction](evidence/clarification-20261022/batched-question-workflow-source.json) is retained before further investigation.
The [project procedure](../../AGENTS.md#user-input-and-reference-priority) now applies this workflow.
The [question document](05-knowledge-questions.md) retains stable question IDs and the user's existing answers.
This workflow instruction changes no domain rule. No governed record or audit event changes for this instruction.

## Unknowns and blockers

Owner approval blocks policy publication. Deployment evidence limits downstream behavior verification.
The user identifies `portal team` for entry policy, empty-entity denial, and empty-subject access across all portal environments.
Multiple-entity behavior blocks acceptance for that separate configuration. Owner: unknown.
The next action is user handback of the [consolidated question document](05-knowledge-questions.md).

## Proposed acceptance and validation

Review [UI-ENTRY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001), [UI-EMPTY-ENTITY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001), and [UI-EMPTY-SUBJECT-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001) against the retained answers.
Check workspace records, source hashes, unchanged historical bytes, links, and the final diff.
These checks establish record consistency within their stated scope.
They do not establish policy approval or passing business behavior.

## Implementation and release proposal

Retain candidate state and continue focused policy clarification.
This stage proposes no application implementation or release.

## Selected rule and historical conflict

The [draft principles, line 14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>) support the denial direction.
The [older security proposal, line 7](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L7>) permits entry for SC accounts.
The user selected denial, not that historical allow-entry proposal.
Neither source establishes approved applicability or owner authority.
The entry answer selects no HTTP status, denial wording, or additional entity-versus-role semantics.

The [measurable business criterion](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001) requires zero granted entries for the stated attempt.
Its observation binding remains unverified. It adds no UI details or executable test case.

## Canonical case applicability

[KNOW-007](06-test-cases.md#know-007), version 2, already describes denial without a registered entity.
Its fixture grants only `E-UNREGISTERED`, which does not match any registered application entity.
Its existing form steps and UI assertions remain historical case details, not newly authorized policy.
The [retained ledger](evidence/audit-run-20261022/report-006/case-results.json#L565904) reports `localPredicateStatus: FAIL` and `canonicalAcceptanceStatus: NOT_ESTABLISHED`.
That result retains its own source, fixture, assertion, and execution limits.
This clarification neither reruns that case nor changes its result.

The canonical catalog retains its exact bytes and version.
Its execution records bind those definitions and line locations.
Changing the case here could change historical execution interpretation.
This stage records applicability instead. It creates no duplicate case definition.

[KNOW-015](06-test-cases.md#know-015), version 2, checks protected fields for a user without tenant entities.
It defines no hidden-tile assertion or direct-launch denial assertion.
That user can fail portal entry before the tile rule applies.
Its definition cannot establish the newly selected tile behavior.
Any future successor must use a user who satisfies portal-entry eligibility.
No new case or application execution occurred during this clarification.

[KNOW-005](06-test-cases.md#know-005), version 2, combines an empty subject with two configured entities.
Its user holds one listed entity. Its assertion covers tile visibility only.
[KNOW-001](06-test-cases.md#know-001) and [KNOW-009](06-test-cases.md#know-009) also include multiple-entity matching.
Those definitions do not isolate the newly selected single-entity visibility and launch criterion.
Their historical outcomes cannot verify that criterion.

## Knowledge-update log

| Question | Affected record | Change and criterion | Finding disposition | Audit |
| --- | --- | --- | --- | --- |
| [UI-Q-002](#ui-q-002) | [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule), version 3 → 4 | Record denial, scope, and user-reported entry-policy owner. Link [UI-ENTRY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001). | Resolve user-reported selection, scope, and owner identity only. Keep authority, approval, and enforcement open. | [Version 4 event](../../evidence/knowledge/audit/AUD-20261022-KT-authentication-and-sessions-v4.yaml) |
| [UI-Q-002](#ui-q-002) | [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-portal-entry-rule), version 3 → 4 | Record denial, scope, user-reported owner, historical conflict, and [UI-ENTRY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001). | Resolve user-reported facts only. Keep authority, approval, and enforcement open. | [Version 4 event](../../evidence/knowledge/audit/AUD-20261022-KT-sdk-and-entitlements-v4.yaml) |
| [Empty entity configuration](#empty-entity-configuration) | [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-entity-rule), version 3 → 4 | Record hidden tiles, denied direct launch, and [UI-EMPTY-ENTITY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001). Link the rule from [authentication knowledge](../../knowledge/candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule). | Resolve behavior selection only. Keep tile-rule ownership, environment scope, approval, and enforcement open. | Both linked version 4 events cover this candidate update. |
| [Empty-entity owner and scope](#empty-entity-configuration) | [Authentication](../../knowledge/candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule) and [SDK entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-entity-rule), version 4 → 5 | Record `portal team` ownership and all-environment applicability as user reports. | Resolve ownership and scope only. Keep approval and enforcement open. | [Authentication event](../../evidence/knowledge/audit/AUD-20261022-KT-authentication-and-sessions-v5.yaml) and [SDK event](../../evidence/knowledge/audit/AUD-20261022-KT-sdk-and-entitlements-v5.yaml). |
| [Empty-subject rule and scope](#empty-subject-configuration) | [Authentication](../../knowledge/candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule), version 5 → 6; [SDK entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule), version 5 → 6; [onboarding](../../knowledge/candidates/operations/KT-admin-and-onboarding.md#current-empty-subject-clarification), version 2 → 3 | Record entity-based visibility and launch, portal-team ownership, all environments, and [UI-EMPTY-SUBJECT-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001). | Resolve the selected single-entity scope. Keep multiple-entity matching, approval, and enforcement open. | [Authentication event](../../evidence/knowledge/audit/AUD-20261022-KT-authentication-and-sessions-v6.yaml), [SDK event](../../evidence/knowledge/audit/AUD-20261022-KT-sdk-and-entitlements-v6.yaml), and [onboarding event](../../evidence/knowledge/audit/AUD-20261022-KT-admin-and-onboarding-v3.yaml). |

All three affected domain records retain candidate/draft state and unknown topic-wide owners. No record receives a verifier or human approval.
The candidate index links this clarification. Other policy decisions and case revisions remain outside scope.
No standalone governance finding existed for this question. The linked task question retains the unresolved limits.

The version 4 update and its check receipt remain historical at Git revision `ef004e9c8d83e41e600a88d3445c65c96e42ab1f`.
Version 5 adds the empty-entity owner and environment answer.
Version 6 adds the empty-subject rule and scope. The onboarding successor records the same clarification.

Paragraph checks required formatting corrections after the first events.
The [authentication correction](../../evidence/knowledge/audit/AUD-20261022-KT-authentication-and-sessions-v4-format.yaml) and [SDK correction](../../evidence/knowledge/audit/AUD-20261022-KT-sdk-and-entitlements-v4-format.yaml) bind the final version 4 bytes.
Both corrections reference their preserved earlier events and hashes.
The version 5 events supersede those content bindings without changing earlier event bytes.

## Sources and evidence limits

Baseline Git revision: `059a25e5eb072d1b0dcd27c3ddc2ccac6cf6d047`.

| Source or baseline | Locator | Revision or SHA-256 |
| --- | --- | --- |
| Entry selection | [SRC-ui-entry-clarification-20261022](evidence/clarification-20261022/ui-q-002-source.json) | `user-answer-20261022-1`; `37a187bd71bab24fcf9bb385d3b0d1fd4537a27b36aa7208235f3dbc159ac358` |
| Environment selection | [SRC-ui-entry-scope-clarification-20261022](evidence/clarification-20261022/ui-q-002-scope-source.json) | `user-answer-20261022-1`; `9c25ae12ffbdb26736d99561724581855a188fc314869118c805044d41c3262d` |
| User-reported policy owner | [SRC-ui-entry-owner-clarification-20261022](evidence/clarification-20261022/ui-q-002-owner-source.json) | `user-answer-20261022-1`; `05316ef14f6fa8cc4171579e4e05faea5ef95d8e6155efd3fa8ceda8b1469b11` |
| Empty-entity selection | [SRC-ui-empty-entity-clarification-20261022](evidence/clarification-20261022/empty-entity-source.json) | `user-answer-20261022-1`; `5fb6e6b3a5fe36510a2d8d47339d83b9ba55b2c6dbcd123949cd3ed61e252d17` |
| Original session response excerpts | [SRC-ui-claude-recovery-20261022](evidence/clarification-20261022/recovered-session-source.json) | `session-excerpt-20261022-1`; `8c968c266c1129248980b4704260eed268bbf437af777d930ef4e39697f05614` |
| Tile-rule owner and scope | [SRC-ui-empty-entity-owner-scope-20261022](evidence/clarification-20261022/empty-entity-owner-scope-source.json) | `user-answer-20261022-1`; `6cc27aa29d2a6237beea2c8a6939fbffb27a7ba19be5a7734c70c33e18b9ca3b` |
| Empty-subject selection | [SRC-ui-empty-subject-clarification-20261022](evidence/clarification-20261022/empty-subject-source.json) | `user-answer-20261022-1`; `4da94ea5220bc719456ca0d73907dbceb9204c51ed3f6e7665a5297862f6505d` |
| Empty-subject owner and scope | [SRC-ui-empty-subject-owner-scope-20261022](evidence/clarification-20261022/empty-subject-owner-scope-source.json) | `user-answer-20261022-1`; `a7a47d9c0c0db6952379c3960d8e6ebb15b9da82e58a0b8229796191cc39f3ee` |
| Frozen intake | [01-intake.md](01-intake.md) | `e819973066ef6668495472728e4785d70ed8bad3600e9cb84c1c58f313d68204` |
| Canonical catalog | [06-test-cases.md](06-test-cases.md#know-007) | `86fbd03391baacd246d490934d7b2fa7ca5cc56a2eb8378c2b4c717ab17aa6e4` |
| Authentication predecessor | [Version 3 history](../../evidence/knowledge/audit/AUD-20261020-KT-authentication-and-sessions-v3.yaml) | `b213cb77e0ee42787d62da2e0f4b3dfaaa82f5d490e4226a08dd37d53e0ef441` |
| SDK predecessor | [Version 3 history](../../evidence/knowledge/audit/AUD-20261020-KT-sdk-and-entitlements-v3.yaml) | `f398b389166b7b1da2faffa28fd4be17ce16dc6222021dfef421c823d99af007` |

The [manifest](../../evidence/knowledge/manifest.yaml) registers all eight clarification source identities and exact hashes through appended records.
Frozen intake, historical reports, canonical cases, and earlier audit events retain their bytes.

## Checks and review limits

The [policy check receipt](evidence/clarification-20261022/checks-owner-scope.json) records the prior policy-stage validation and hash bindings.
The [current check receipt](evidence/clarification-20261022/checks-empty-subject.json) covers the reference-priority procedure and empty-subject clarification.
The [question-batch checks](evidence/question-batch-20261022/checks.json) cover the later document and workflow update.
Local discovery succeeded through the installed Workbench command. It exposes no registered knowledge resource for `call`.
Direct local inspection supplied the bounded review.

Earlier connector failures do not establish missing configuration or unavailable business policy.

No application test or browser execution occurred.

Automated checks do not authenticate users, approve policy, or verify business behavior.
Full ASD-STE100 review remains `PENDING`.
