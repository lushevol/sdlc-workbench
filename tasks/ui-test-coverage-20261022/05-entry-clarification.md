---
artifact_kind: change-request
id: UI-ENTRY-CLARIFICATION-20261022
version: 1
status: draft
owner: unknown
source_refs: [SRC-ui-entry-clarification-20261022, SRC-ui-entry-scope-clarification-20261022, SRC-ui-entry-owner-clarification-20261022, SRC-ui-empty-entity-clarification-20261022, SRC-ui-claude-recovery-20261022]
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
> **Confirm the empty-entity tile rule's owner and environment scope.**
> Action: Answer the pending scope question. Consequence: Scope-specific acceptance remains blocked.
> Owner: unknown. Evidence: The [selected tile rule](evidence/clarification-20261022/empty-entity-source.json).

## Current task state

This living stage covers portal-entry intent and the empty-entity tile rule.
The user selected denial for an authenticated SC user without entitlement for any registered application entity.
The user selected local, test, UAT, and production environments.
The user also selected hidden tiles and denied direct launch when a tile has no configured EMS2 entity.
Ownership and environment scope remain unanswered for that separate tile rule.
These answers establish user-stated intent, not authenticated owner authority, publication approval, or implementation verification.

Both security topics remain version 4 candidate drafts, with `owner: unknown` and `verified: []`.

Named next phase: Approved-policy acceptance and downstream behavior verification.
Readiness: `NEEDS_CLARIFICATION`.
The user identifies `portal team` as the entry-policy owner only. Owner authority, approval, and deployed enforcement remain unconfirmed.

Further questions and authorized evidence collection can continue.
The selected scope includes candidate records, provenance, validation, and the required project commit.
Implementation, publication, and application execution remain outside this clarification stage.
Assessor: `agent:codex`. Assessment time: `2026-10-22T09:13:41Z`.

## Proposed change

Record the selected entry and tile rules in candidate knowledge.
Preserve historical conflicts, prior answers, case definitions, and earlier execution results.

## Scope and affected artifacts

The affected records are the two security topics, their navigation, this stage, source provenance, and new audit events.
No runtime symbol, caller, importer, or application interface changes.
Qualitative risk: Low for runtime behavior. Incorrect authority wording could misstate policy, so review limits remain explicit.

## Options and consequences

The user selected entry denial instead of the older allow-entry proposal.
The user selected hidden tiles and denied direct launch instead of implicit access through missing EMS2 configuration.
Both selections remain candidate intent. Neither grants publication approval.

## Requested decision and actual disposition

The entry rule, entry scope, entry owner, and tile behavior have recorded answers.
The tile-rule owner and environment scope remain unanswered.

## Request and source facts

The user requested one blocker question at a time.
The [source snapshots](#sources-and-evidence-limits) retain the exact questions, choices, and supplied answers.
Capture times do not identify response times.
The [recovered session excerpt](evidence/clarification-20261022/recovered-session-source.json) retains recorded response timestamps from the original Claude session.
Original snapshots retain their earlier null response timestamps and exact bytes.
The supplemental scope source does not rewrite the first snapshot's earlier applicability limit.

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
| Answer status | Tile behavior resolved as user-stated intent. Ownership and environment scope remain unanswered. |
| Pending question | Does the portal team own this rule across all portal environments? |
| Resolution owner | unknown |
| Consequence | Scope-specific acceptance remains blocked. |
| Next action | Obtain the pending ownership and scope answer. Do not repeat the answered tile behavior question. |
| Limits | No approved policy, deployment binding, denial wording, HTTP status, or passing execution is established. |

The [historical question](evidence/knowledge-inspection.md#open-rule-decisions) retains its earlier unresolved state.
The [empty-role example, lines 13–19](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L13-L19>) does not define empty-entity behavior.

## Unknowns and blockers

Tile-rule ownership and environment scope block scope-specific acceptance. Owner: unknown.
Owner approval and deployment evidence block approved-policy acceptance and downstream verification.
The user identifies `portal team` for entry policy only.
The next action remains the pending tile-rule ownership and scope question.

## Proposed acceptance and validation

Review [UI-ENTRY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001) and [UI-EMPTY-ENTITY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001) against the retained answers.
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

## Knowledge-update log

| Question | Affected record | Change and criterion | Finding disposition | Audit |
| --- | --- | --- | --- | --- |
| [UI-Q-002](#ui-q-002) | [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule), version 3 → 4 | Record denial, scope, and user-reported entry-policy owner. Link [UI-ENTRY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001). | Resolve user-reported selection, scope, and owner identity only. Keep authority, approval, and enforcement open. | [Version 4 event](../../evidence/knowledge/audit/AUD-20261022-KT-authentication-and-sessions-v4.yaml) |
| [UI-Q-002](#ui-q-002) | [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-portal-entry-rule), version 3 → 4 | Record denial, scope, user-reported owner, historical conflict, and [UI-ENTRY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001). | Resolve user-reported facts only. Keep authority, approval, and enforcement open. | [Version 4 event](../../evidence/knowledge/audit/AUD-20261022-KT-sdk-and-entitlements-v4.yaml) |
| [Empty entity configuration](#empty-entity-configuration) | [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-entity-rule), version 3 → 4 | Record hidden tiles, denied direct launch, and [UI-EMPTY-ENTITY-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001). Link the rule from [authentication knowledge](../../knowledge/candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule). | Resolve behavior selection only. Keep tile-rule ownership, environment scope, approval, and enforcement open. | Both linked version 4 events cover this candidate update. |

Both records retain candidate/draft state and unknown owners. Neither record receives a verifier or human approval.
The candidate index links this clarification. Other policy decisions and case revisions remain outside scope.
No standalone governance finding existed for this question. The linked task question retains the unresolved limits.

Paragraph checks required formatting corrections after the first events.
The [authentication correction](../../evidence/knowledge/audit/AUD-20261022-KT-authentication-and-sessions-v4-format.yaml) and [SDK correction](../../evidence/knowledge/audit/AUD-20261022-KT-sdk-and-entitlements-v4-format.yaml) bind the final version 4 bytes.
Both corrections reference their preserved earlier events and hashes.

## Sources and evidence limits

Baseline Git revision: `059a25e5eb072d1b0dcd27c3ddc2ccac6cf6d047`.

| Source or baseline | Locator | Revision or SHA-256 |
| --- | --- | --- |
| Entry selection | [SRC-ui-entry-clarification-20261022](evidence/clarification-20261022/ui-q-002-source.json) | `user-answer-20261022-1`; `37a187bd71bab24fcf9bb385d3b0d1fd4537a27b36aa7208235f3dbc159ac358` |
| Environment selection | [SRC-ui-entry-scope-clarification-20261022](evidence/clarification-20261022/ui-q-002-scope-source.json) | `user-answer-20261022-1`; `9c25ae12ffbdb26736d99561724581855a188fc314869118c805044d41c3262d` |
| User-reported policy owner | [SRC-ui-entry-owner-clarification-20261022](evidence/clarification-20261022/ui-q-002-owner-source.json) | `user-answer-20261022-1`; `05316ef14f6fa8cc4171579e4e05faea5ef95d8e6155efd3fa8ceda8b1469b11` |
| Empty-entity selection | [SRC-ui-empty-entity-clarification-20261022](evidence/clarification-20261022/empty-entity-source.json) | `user-answer-20261022-1`; `5fb6e6b3a5fe36510a2d8d47339d83b9ba55b2c6dbcd123949cd3ed61e252d17` |
| Original session response excerpts | [SRC-ui-claude-recovery-20261022](evidence/clarification-20261022/recovered-session-source.json) | `session-excerpt-20261022-1`; `8c968c266c1129248980b4704260eed268bbf437af777d930ef4e39697f05614` |
| Frozen intake | [01-intake.md](01-intake.md) | `e819973066ef6668495472728e4785d70ed8bad3600e9cb84c1c58f313d68204` |
| Canonical catalog | [06-test-cases.md](06-test-cases.md#know-007) | `86fbd03391baacd246d490934d7b2fa7ca5cc56a2eb8378c2b4c717ab17aa6e4` |
| Authentication predecessor | [Version 3 history](../../evidence/knowledge/audit/AUD-20261020-KT-authentication-and-sessions-v3.yaml) | `b213cb77e0ee42787d62da2e0f4b3dfaaa82f5d490e4226a08dd37d53e0ef441` |
| SDK predecessor | [Version 3 history](../../evidence/knowledge/audit/AUD-20261020-KT-sdk-and-entitlements-v3.yaml) | `f398b389166b7b1da2faffa28fd4be17ce16dc6222021dfef421c823d99af007` |

The [manifest](../../evidence/knowledge/manifest.yaml) registers all five new source identities and exact hashes through appended records.
Frozen intake, historical reports, canonical cases, and earlier audit events retain their bytes.

## Checks and review limits

The [check receipt](evidence/clarification-20261022/checks.json) records workspace validation, authored prose lint, links, preservation, and hash bindings.
Local discovery succeeded through the installed Workbench command. It exposes no registered knowledge resource for `call`.
Direct local inspection supplied the bounded review.
Earlier connector failures do not establish missing configuration or unavailable business policy.
No application test or browser execution occurred.

Automated checks do not authenticate users, approve policy, or verify business behavior.
Full ASD-STE100 review remains `PENDING`.
