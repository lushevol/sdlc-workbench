---
artifact_kind: change-request
id: KNOWLEDGE-QUESTION-BATCH-20261022
version: 3
status: draft
owner: unknown
source_refs:
- UI-ENTRY-CLARIFICATION-20261022
- REQ-active-session-renewal
- ARC-portal-service-relationships
related_ids:
- ARC-portal-service-relationships
- KT-frontend-composition
- KT-portal-purpose
- KT-architecture-evolution
- KT-application-interoperability
- KT-observability-and-performance
- KT-admin-and-onboarding
- KT-release-operations
- REQ-active-session-renewal
- KT-authentication-and-sessions
- KT-sdk-and-entitlements
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

# Knowledge questions and answers — investigated refinement

> **Action: Complete eight policy answers and one shared ownership/contact entry.**
> Consequence: Missing policy blocks its affected acceptance definition. Missing review blocks publication separately.
> Owner: user or delegated topic owner; unresolved owners remain unknown.
> Evidence: The [refinement request](evidence/question-refinement-20261026/user-request.json) and [investigated findings](evidence/question-refinement-20261026/reconciliation.json).

## Current task state

Revised: 26 October 2026. Investigation baseline: `568b480e0bfe11f9922d8d133fdd4ed22dd81479`.
All 60 original IDs remain available. Nine entries need your input; eight concern policy, and one consolidates ownership contacts.

Seventeen entries have source-backed answers. Two retain their existing answers. Six consolidate related requests.
Six remain conditional evidence follow-ups. Twenty retain historical findings or limits outside the current decision.
No new business answer comes from the [continuation request](evidence/question-refinement-20261026/user-continuation.json).

Readiness: `READY` for asynchronous answer collection only. Assessor: `agent:codex`, 26 October 2026.
Acceptance for unanswered policy remains `NEEDS_CLARIFICATION`. Publication and deployment verification remain separate decisions.
Knowledge ingestion will resume after you return answers and request continuation.

Confidence concerns the stated finding and its scope. It does not establish approval, deployment, or business execution.
`HIGH` means direct applicable evidence; `MEDIUM` means supported findings with material limits.
`LOW` means weak or conflicting support; `UNKNOWN` means the available evidence cannot determine the answer.
Each open policy has `UNKNOWN` confidence in the intended rule. Source-finding confidence appears separately.

## How to answer

Edit the fields below. Options are unselected proposals. You can give another answer, write `unknown`, or name a contact.
For each answer, state environment, effective date, exceptions, and authority when these affect its scope.

Do not repeat recorded answers. A contact assignment does not complete content review or grant publication approval.
When ready, say: `Continue ingestion using my answers in 05-knowledge-questions.md.`
I will preserve the returned bytes, investigate remaining gaps, and refine affected candidate knowledge with provenance.
We will repeat this document loop until no material question remains. Required publication reviews still apply.

Your [reference-priority instruction](evidence/clarification-20261023/reference-priority-user-input.md#exact-user-input) governs intended behavior.
The [investigation-first rule](../../AGENTS.md#investigation-first-source) governs question selection and confidence.
The [document-review instruction](evidence/clarification-20261023/review-format-user-input.md#exact-user-input) governs this editable handover.

| Shared answer scope | Your response |
| --- | --- |
| Respondent and role | |
| Answer date | |
| Default environments and effective date | |
| Answers that remain proposals | |

## Answer navigation

| Entry | Remaining input |
| --- | --- |
| [KQ-SEC-03](#kq-sec-03) | Shared ownership and review contacts |
| [KQ-SEC-04](#kq-sec-04) | Token and inactivity limits |
| [KQ-SEC-06](#kq-sec-06) | Permitted production login fallback |
| [KQ-SEC-14](#kq-sec-14) | Permission-revocation delay for protected actions |
| [KQ-SEC-15](#kq-sec-15) | Logout scope and propagation delay |
| [KQ-SEC-19](#kq-sec-19) | Tile-launch authorization freshness |
| [KQ-OPS-002](#kq-ops-002) | Tenant audit and reference boundaries |
| [KQ-OBS-002](#kq-obs-002) | Current performance acceptance limits |
| [KQ-OBS-005](#kq-obs-005) | Analytics fields, readers, and retention |

## Answers already recorded

These answers are carried forward. Correct them only if your intended rule has changed.

| Existing answer | Scope or limit | Source |
| --- | --- | --- |
| Deny portal entry without entitlement for any registered application entity. | Portal team; local, test, UAT, production. | [Recorded answer](05-entry-clarification.md#ui-q-002) |
| Hide the tile and deny direct launch when no EMS2 entity is configured. | Portal team; local, test, UAT, production. | [Recorded answer](05-entry-clarification.md#empty-entity-configuration) |
| With one configured entity and an empty subject, allow visibility and launch through the entity check. | Portal team; local, test, UAT, production. | [Recorded answer](05-entry-clarification.md#empty-subject-configuration) |
| Continuous eligible activity must support ongoing renewal across the initial refresh expiry. | Existing session intent; effective deployment remains unconfirmed. | [Recorded answer](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) |
| Mouse, keyboard, and scroll activity count. Refresh-token renewal remains required after inactivity. | Existing session intent; token policy still needs current environment bindings. | [Recorded answer](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) |
| The reported UAT page was Cashflow Blotter. | The earlier Dashboard description is superseded. | [Recorded answer](../portal-background-session-20261019/10-change-review.md#sources-and-evidence-limits) |
| The four MFE layers and reported BFF, SDK, and Auth responsibilities are recorded. | Effective deployment and consumer adoption remain qualified. | [Recorded answer](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#components) |
| API Gateway implementation analysis remains excluded. | The unavailable boundary remains visible in architecture. | [Recorded answer](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#decisions) |

## Remaining questions

### KQ-SEC-03

**Who owns the unassigned topics, and which contacts can provide the required content reviews?**

Portal-team ownership already applies to the three clarified entitlement rules across all portal environments.
Session policy and the complete capability baseline have no recorded accountable owner.
This entry consolidates [KQ-SEC-02](#kq-sec-02) and [KQ-ARCH-01](#kq-arch-01), with separate responsibility rows.

Confidence: `HIGH` for recorded entitlement ownership; `UNKNOWN` for the missing session and baseline assignments.

Rationale: Exact user answers assign entitlement ownership. The other inspected records contain no applicable assignment.

Limit: Naming a reviewer does not record their review, authority, or approval of final candidate bytes.

| Scope | Recorded owner | Your team, reviewer, contact, or evidence location |
| --- | --- | --- |
| Entry denial, empty-entity denial, and single-entity empty-subject access | Portal team; all environments | |
| Session policy and current renewal criteria | unknown | |
| Portal capability baseline and corrections, if any | unknown | |

Suggested options, unselected:

- A. Identify the team and review contact for each unassigned scope.
- B. Name a delegate or existing ownership record for the affected rows.
- C. Give another answer or write `unknown` for unresolved rows.

Answer:

Owner: unknown for missing assignments; portal team for the three entitlement rules.

Consequence: Unassigned review responsibility blocks the affected publication handoff.

Next action: Record contacts once. Request actual content review when candidate bytes are prepared.

Evidence: [REQ-active-session-renewal.md L1-L25](<../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L1-L25>); [REQ-active-session-renewal.md acceptance-criteria](<../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria>); [10-change-review.md unknowns-and-blockers](<../portal-background-session-20261019/10-change-review.md#unknowns-and-blockers>).
Evidence: [index.ejs L8-L16](<../../repos/ui/mfe-root-config/src/index.ejs#L8-L16>); [KT-portal-purpose.md scope](<../../knowledge/candidates/background/KT-portal-purpose.md#scope>); [user-message.txt L7-L22](<../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L7-L22>).
Evidence: [empty-subject-owner-scope-source.json](<evidence/clarification-20261022/empty-subject-owner-scope-source.json>); [KT-authentication-and-sessions.md L1-L120](<../../knowledge/candidates/security/KT-authentication-and-sessions.md#L1-L120>); [KT-sdk-and-entitlements.md L1-L143](<../../knowledge/candidates/security/KT-sdk-and-entitlements.md#L1-L143>).

### KQ-SEC-04

**Which token and inactivity limits apply outside continuous eligible activity?**

Continuous eligible activity must preserve renewal. BFF YAML defaults declare 15-minute access, 225-minute refresh, and 60-minute absolute values.

The recorded active-renewal requirement remains in force. Do not reinterpret fixed values as a cutoff during continuous eligible activity.

Source-finding confidence: `MEDIUM`. Intended-policy confidence: `UNKNOWN`.

Rationale: The user answer overrides historical fixed-session cutoffs. Legacy text conflicts on refresh duration, and the launch file overrides access to 480 minutes.

Limit: Configuration identifies inspected defaults, not approved timeout policy or deployed UAT values. Refresh generation adds 24 seconds to configured minutes. Provider-session limits remain distinct from portal token lifetimes.

Suggested options, unselected:

- A. Use one policy across environments. Specify access lifetime, inactivity limit, and refresh-credential lifetime with units.
- B. Use different policies. Give those values and their effective scope for each environment.
- C. Identify an authoritative policy or responsible contact.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: unknown session owner.

Consequence: Unselected limits prevent measurable inactivity and token-expiry acceptance.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [user-request.txt](<../portal-background-session-20261019/evidence/correction-20261020/user-request.txt>); [application.yml L32-L35](<../../repos/services/single-ui-bff/src/main/resources/application.yml#L32-L35>); [app.conf L2](<../../repos/services/single-ui-bff/app.conf#L2>); [JwtTokenUtil.java L48-L84](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L48-L84>).

### KQ-SEC-06

**Which production fallback policy applies after the planned OneMFA retirement?**

The current shell defaults to Entra in configured environments. URL values true, 1, yes, and y enable Entra; no disables it.

The parser behavior is resolved. The remaining decision concerns permission to use fallback, rather than flag syntax.

Source-finding confidence: `MEDIUM`. Intended-policy confidence: `UNKNOWN`.

Rationale: The parser accepts both documented flag forms. It stores no activation preference; current defaults explain Entra after restart.

Limit: OneMFA and username/password paths remain in source. Their existence does not establish production permission. The rollout calendar planned OneMFA retirement after September, but current release applicability is unbound.

Suggested options, unselected:

- A. Require Entra. Permit no OneMFA fallback in production.
- B. Permit OneMFA only through named exceptions. Specify conditions, expiry, and responsible owner.
- C. Permit ongoing fallback. State its conditions and effective date.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: unknown identity-policy owner.

Consequence: The permitted fallback determines which production login paths acceptance must allow.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [featureFlagController.ts L14-L38](<../../repos/ui/mfe-base/src/utils/featureFlagController.ts#L14-L38>); [common.ts L131-L153](<../../repos/ui/mfe-base/src/utils/common.ts#L131-L153>); [UI SSO Entra Design L7-L30](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md#L7-L30>).

### KQ-SEC-14

**What maximum permission-revocation delay applies to protected application actions?**

The supplied Auth Server supports Redis caching of EMS2 and EMS3 results, using configured expiryTime. EMS3 exposes eviction methods.

This concerns protected application actions. Tile-launch freshness has a separate boundary in [KQ-SEC-19](#kq-sec-19).

Source-finding confidence: `MEDIUM`. Intended-policy confidence: `UNKNOWN`.

Rationale: The source resolves how this implementation caches permissions. It does not establish the maximum acceptable business revocation delay.

Limit: Current deployment overrides and every external application cache remain unbound. A cache TTL is an implementation value, not an approved permission-revocation service level.

Suggested options, unselected:

- A. Require the first protected action after revocation to use current permissions.
- B. Permit a bounded delay. State its duration, start event, affected actions, and environments.
- C. Identify a governing policy or application permission owner.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: application permission owners.

Consequence: The missing revocation deadline prevents measurable protected-action acceptance.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [Ems2EntitlementService.java L112-L170](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems2EntitlementService.java#L112-L170>); [Ems3EntitlementService.java L49-L84](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java#L49-L84>); [Ems3EntitlementService.java L116-L123](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java#L116-L123>).

### KQ-SEC-15

**Which sessions must logout revoke, and within what propagation delay?**

The BFF blacklists the supplied session ID on logout. The SDK maintains a filter-local revocation list for observed logout requests.

State whether identity-provider logout is also required. Code mechanisms cannot select the required cross-device boundary.

Source-finding confidence: `MEDIUM`. Intended-policy confidence: `UNKNOWN`.

Rationale: These mechanisms are directly visible. Neither establishes a required cross-device revocation boundary or maximum propagation delay.

Limit: Current deployment topology and blacklist retention remain separate evidence gaps. The historical governance finding describes a conditional risk, not a proven deployed failure.

Suggested options, unselected:

- A. Revoke the current session across its protected service instances. Specify the maximum delay.
- B. Revoke all sessions for the account, including other devices. Specify the maximum delay.
- C. Define another boundary or identify its governing policy.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: unknown session-policy owner.

Consequence: The missing logout boundary prevents cross-device and service-instance acceptance.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [JwtAuthenticationController.java L365-L378](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365-L378>); [SessionServiceImplementation.java L17-L35](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L17-L35>); [JwtTokenUtil.java L82-L103](<../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java#L82-L103>).

### KQ-SEC-19

**How fresh must the entitlement decision be when a user launches a tile?**

The shell launches a tile from its authorized drawer state. The inspected launch function sends no fresh authorization request.

Application backends still control protected data actions. This question defines the portal launch decision only.

Source-finding confidence: `MEDIUM`. Intended-policy confidence: `UNKNOWN`.

Rationale: buildEntities filters the catalog during authentication. KNOW-014 proposes a later revocation check without defining its business contract.

Limit: A cached catalog does not verify present tenant-data permission. Application backends retain their separate permission responsibility. The proposed protected-field assertion cannot be accepted without a selected revocation boundary.

Suggested options, unselected:

- A. Recheck current entitlements for each launch before admitting the tile.
- B. Reuse the authorized catalog within a stated freshness period. Specify refresh and invalidation conditions.
- C. Define another launch boundary or identify its governing policy.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: portal authorization owner.

Consequence: Expected launch behavior after entitlement revocation remains undefined.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [index.ts L152-L175](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L152-L175>); [JwtAuthenticationController.java L97-L121](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L97-L121>); [06-test-cases.md know-014](<06-test-cases.md#know-014>).

### KQ-OPS-002

**Which tenant boundaries apply to audit reads and category or import-map references?**

Data lists filter by the validated EMS2 role. Update paths compare record ownership and reject maker self-verification. Audit lookup validates credentials but does not compare record ownership. Tile creation also lacks the update path’s reference-owner comparison.

Answer audit access and reference ownership separately. Existing maker-checker rules do not settle these two boundaries.

Source-finding confidence: `HIGH`. Intended-policy confidence: `UNKNOWN`.

Rationale: The controllers and shared validation utility directly expose these different authorization paths. The manual requires distinct maker and checker users.

Limit: These are inspected source predicates, not approved access policy or new execution results. The intended audit and foreign-reference access boundary remains unspecified.

Suggested options, unselected:

- A. Require the same tenant role for both audit reads and referenced records.
- B. Permit specified shared records or audit access. Define the exception and authorizing role separately for each boundary.
- C. Define another boundary or identify its governing policy.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: unknown administration policy owner.

Consequence: This answer determines cross-tenant audit and foreign-reference acceptance expectations.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [AdminModuleUtil.java L41-L68](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L41-L68>); [ImportMapController.java L141-L164](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L141-L164>); [ApplicationTileController.java L46-L64](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46-L64>); [User Manual L19-L35](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md#L19-L35>).

### KQ-OBS-002

**Which current response-time and capacity limits define portal performance acceptance?**

The 2023 draft proposes five-second responses, 100 users, CPU below 50%, and heap below 80%. Its sign-off fields are empty. Those draft values do not establish current acceptance budgets.

The old draft is evidence of a proposal. Historical throughput results cannot establish current acceptance limits.

Source-finding confidence: `HIGH`. Intended-policy confidence: `UNKNOWN`.

Rationale: The only inspected numerical requirement source is explicitly draft and lacks its stated sign-off evidence.

Limit: Observed performance and implementation settings cannot define the intended business budget. No current approved workload, response-time percentile, or capacity baseline is established locally.

Suggested options, unselected:

- A. Define current limits for named journeys, with percentile, concurrent users, workload, data size, environment, and measurement duration.
- B. Identify an approved performance baseline and its applicable journeys and release.
- C. Confirm that no current budget exists, and identify who must define it.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: unknown performance requirement owner.

Consequence: The answer defines measurable performance acceptance instead of treating old draft targets as current requirements.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [FMO Post Trade Portal Frontend Performance Testing May 2023 L5-L36](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L5-L36>); [FMO Post Trade Portal Frontend Performance Testing May 2023 L68-L89](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L68-L89>).

### KQ-OBS-005

**Which analytics fields, readers, and retention periods are permitted?**

The analytics writer adds userId, client IP, and creation time, then clears singleUIAuthorization before serializing the record. Frontend event models permit values and twenty custom attributes. These implementation facts do not establish permitted readers, field policy, or retention duration.

State treatment for search text and custom attributes. The implemented collection path does not establish permission to retain them.

Source-finding confidence: `HIGH`. Intended-policy confidence: `UNKNOWN`.

Rationale: The complete producer-to-controller-to-writer chain is available, but the inspected sources supply no applicable data-governance rule.

Limit: Actual Elasticsearch lifecycle settings and reader-role assignments are not present in the inspected application source. Implementation cannot supply permission to collect or retain particular identity and search values.

Suggested options, unselected:

- A. Permit identified user IDs, client IPs, or search values under stated rules. Specify permitted fields, readers, and retention.
- B. Require removal, masking, or aggregation for specified fields. Define each transformation and its retention.
- C. Identify the applicable data policy or responsible data owner.
- Other or unknown: Give another answer, a contact, or an evidence location.

Answer:

Owner: unknown analytics data owner.

Consequence: The answer defines the accepted collection, access, and retention boundary for the implemented analytics path.

Next action: Review the returned rule and define measurable acceptance criteria within its stated scope.
Evidence: [model.ts L12-L69](<../../repos/ui/mfe-base/src/analytics/model.ts#L12-L69>); [AnalyticServiceImplementation.java L24-L32](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/AnalyticServiceImplementation.java#L24-L32>); [Design L43-L47](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L43-L47>).

## Investigated findings and retained limits

These entries require no repeated answer now. They retain all remaining original IDs and their investigation results.
Conditional gaps remain open evidence work. They become blocking only when the named decision requires them.
Each entry links source evidence; the source map records full revisions, hashes, original questions, and reconciliation.

## Security, entitlements, and sessions

### KQ-SEC-01

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Documented intent and inspected implementation.

Any matching configured EMS2 entity admits an ordinary tile when its subject is empty. The shell launches admitted tiles.

Rationale: The SSDR discussion explicitly says one listed entity suffices. BFF filtering implements that rule and skips blank subjects.

Limit: This answers the retained design and inspected source. It does not establish deployed configuration or recorded policy approval. Template tiles bypass this filter. Later EMS3 filters can apply additional restrictions.

Owner: portal team.

Consequence: Use the documented any-one rule for the qualified knowledge answer. Keep publication review separate.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [SSDR On Board Discussion L17-L20](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L17-L20>); [Post Trade Portal Principles (Draft) L14-L24](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14-L24>); [AdminModuleUtil.java L101-L137](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L101-L137>).

### KQ-SEC-02

Status: `CONSOLIDATED`. Finding confidence: `HIGH`.
Class: Documented intent and recorded review state.

The portal team owns all three clarified rules. Current candidates record no verifier, named review, or publication approval.

Rationale: Exact user answers resolve ownership and environment scope. Candidate metadata retains empty verifier lists.

Limit: Ownership is not missing. Only the actual content reviewer and review event remain unrecorded. The workflow request does not identify a reviewer or approve the current final content bytes.

Owner: portal team.

Consequence: Record the reviewer and reviewed scope once. Do not repeat rule ownership or scope questions.

Next action: Use [KQ-SEC-03](#kq-sec-03) for the consolidated contact or evidence follow-up.

Evidence: [empty-subject-owner-scope-source.json](<evidence/clarification-20261022/empty-subject-owner-scope-source.json>); [KT-authentication-and-sessions.md L1-L120](<../../knowledge/candidates/security/KT-authentication-and-sessions.md#L1-L120>); [KT-sdk-and-entitlements.md L1-L143](<../../knowledge/candidates/security/KT-sdk-and-entitlements.md#L1-L143>).

### KQ-SEC-05

Status: `EVIDENCE_FOLLOWUP`. Finding confidence: `HIGH`.
Class: Inspected implementation and bounded deployment unknown.

Current local repository identities and token defaults are known. No retained binding identifies the effective UAT launcher, artifacts, or property origin.

Rationale: The screenshot gives a remaining delay, not JWT issuance time. Local app.conf and YAML provide competing configuration candidates.

Limit: The effective UAT property value cannot be selected from a local file alone. Browser and server clock agreement and refresh-token expiry remain unbound. Configured connector credentials are unavailable; this does not establish missing external records.

Owner: unknown authentication or deployment owner.

Consequence: Retain a precise deployment-evidence action. No new timing-policy answer is inferred.

Next action: Collect the missing binding when its deployment, release, compatibility, or verification decision requires it.

Evidence: [repository-bindings.json](<evidence/question-refinement-20261026/repository-bindings.json>); [observation.json](<../portal-background-session-20261019/evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json>); [timing-contract-source-receipt.json](<../portal-background-session-20261019/evidence/uat-blotter-browser-20261021/uat-screenshot/timing-contract-source-receipt.json>).

### KQ-SEC-07

Status: `CONSOLIDATED`. Finding confidence: `HIGH`.
Class: Retained migration documentation and missing deployment binding.

The local collection already contains the Entra design, phase plan, production rollout calendar, and non-production verification guide.

Rationale: These sources locate the migration records. They do not bind current deployed artifacts or prove completion of planned milestones.

Limit: Referenced production sign-off attachments are unavailable in the retained guide directory. Current enabled providers must be established through the deployment evidence already requested in KQ-SEC-05.

Owner: unknown release owner.

Consequence: Carry current provider and rollout state into the specific deployment-binding action. Remove the generic record-location question.

Next action: Use [KQ-SEC-05](#kq-sec-05) for the consolidated contact or evidence follow-up.

Evidence: [UI SSO Entra Design L7-L31](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md#L7-L31>); [Post Trade Portal Entra Migration - Phase 1 - UI SSO L15-L57](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md#L15-L57>); [Entra SSO Prod Guide L38-L46](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md#L38-L46>).

### KQ-SEC-08

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Documented profile contract and inspected implementation.

The supplied profile exposes firstName, lastName, fullName, country, emailId, locale, and userId. Entra country is coded; locale may be null.

Rationale: The production guide records these differences. The BFF mapping and shell profile expose the same fields.

Limit: Names can differ from OUD values. The guide directs entitlement checks to the dedicated entitlement system. Uninspected external consumers may impose additional fields; no universal consumer contract is claimed.

Owner: identity and downstream application owners.

Consequence: Record the evidenced profile shape and migration differences. Do not ask for a new universal profile policy.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Entra SSO Prod Guide L48-L83](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md#L48-L83>); [EntraAuthenticationServiceImpl.java L59-L96](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/EntraAuthenticationServiceImpl.java#L59-L96>); [index.tsx L200-L248](<../../repos/ui/mfe-base/src/components/Profile/index.tsx#L200-L248>).

### KQ-SEC-09

Status: `EVIDENCE_FOLLOWUP`. Finding confidence: `MEDIUM`.
Class: Documented historical contract and inspected client implementation.

FMAA client-credentials acquisition and token authentication remain present in the supplied source. Historical guidance states 17-year service-account and seven-day bank-ID validity.

Rationale: The current clients obtain tokens from FMAA. They do not define the provider-issued token lifetimes.

Limit: Historical validity examples are not current token policy. The retained migration plan says the FMAA replacement was unresolved; it does not prove its present external status.

Owner: authentication provider owner.

Consequence: Retain the evidenced client flow as candidate knowledge with limits. Apply required review before publication.

Next action: Collect the missing binding when its deployment, release, compatibility, or verification decision requires it.

Evidence: [Reference of FMAA API L24-L30](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md#L24-L30>); [Post Trade Portal & RATAN Entra Migration - Phase 2 - service account L1-L10](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md#L1-L10>); [FmaaAuth.java L60-L82](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/FmaaAuth.java#L60-L82>).

### KQ-SEC-10

Status: `EVIDENCE_FOLLOWUP`. Finding confidence: `HIGH`.
Class: Historical security reports with unavailable current retest binding.

The collection contains the named penetration, WAS, and API scan notes. They report historical fixes and planned deployments.

Rationale: The notes reference absent attachments. Local review results do not supply a current security scan and assertion-bearing retest.

Limit: This does not prove current exposure or current finding closure. No current deployed artifact and security-retest pair was found within the inspected task evidence.

Owner: security assurance owner.

Consequence: Keep historical remediation statements bounded. Do not use them as current closure evidence.

Next action: Collect the missing binding when its deployment, release, compatibility, or verification decision requires it.

Evidence: [Penetration Testing report for SPT001414 – SSI+ BA L5-L29](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Penetration Testing report for SPT001414 – SSI+ BA/page.md#L5-L29>); [WAS Scan Report SIA-ETASK1854215- 11282023 L31-L53](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/WAS Scan Report SIA-ETASK1854215- 11282023/page.md#L31-L53>); [Web Application Vulnerability Scan - SIA-API-ETASK1837309-01122023 L6-L18](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Web Application Vulnerability Scan - SIA-API-ETASK1837309-01122023/page.md#L6-L18>).

### KQ-SEC-11

Status: `EVIDENCE_FOLLOWUP`. Finding confidence: `HIGH`.
Class: Inspected dependency declarations and configuration.

The supplied Auth Server declares fmoportal-auth-sdk 1.1.1. The SDK checkout declares 2.0.0-SNAPSHOT, Java 17, and Spring Boot 4.0.6.

Rationale: Local Maven declarations and Auth Server filter properties provide a concrete partial inventory without user source inspection.

Limit: No build was run. A dependency declaration does not identify the resolved deployment binary. The two supplied backend repositories cannot establish every external application consumer.

Owner: application deployment owners.

Consequence: Keep the local inventory as an answered finding. Request only missing deployment or external-consumer scope.

Next action: Collect the missing binding when its deployment, release, compatibility, or verification decision requires it.

Evidence: [pom.xml L96-L101](<../../repos/services/ratan-auth-server/pom.xml#L96-L101>); [application.yml L122-L137](<../../repos/services/ratan-auth-server/src/main/resources/application.yml#L122-L137>); [pom.xml L3-L19](<../../repos/libraries/single-ui-sdk-starter/pom.xml#L3-L19>).

### KQ-SEC-12

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `MEDIUM`.
Class: Inspected SDK and Auth Server implementation.

The SDK skips JWT validation for configured paths or any nonempty configured skip header. Auth Server validates alternative credentials inside authentication endpoints.

Rationale: The current Auth Server dispatches X-Token to Redis-backed validation and FMAA-Token to provider validation at /v3/authenticate.

Limit: A skip-header presence check authenticates nothing by itself. It only delegates further request processing. These inspected endpoint controls cannot establish protection for every excluded path or external SDK consumer. Auth Server declares SDK 1.1.1; the supplied SDK checkout is a separate 2.0.0-SNAPSHOT source.

Owner: application security owners.

Consequence: Document the concrete alternate controls and their endpoint scope. Inspect any additional consumer as an evidence task.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [AuthTokenFilter.java L34-L68](<../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java#L34-L68>); [application.yml L127-L138](<../../repos/services/ratan-auth-server/src/main/resources/application.yml#L127-L138>); [AuthenticationController.java L66-L141](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/AuthenticationController.java#L66-L141>).

### KQ-SEC-13

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented responsibility boundary and explicit user architecture.

Each tile application owns its data-view and edit permissions. The portal controls entry and tile visibility; the SDK supplies JWT validation.

Rationale: The tile-security source explicitly delegates data permissions. The user architecture clarification describes the SDK as a validation library.

Limit: The collection does not include every tenant backend or its protected business operations. This boundary does not verify an individual downstream permission implementation.

Owner: respective tile application owners.

Consequence: Record the responsibility boundary. Defer individual business-operation contracts until the relevant application scope is selected.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Tile Security Control - EMS2 L7-L11](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L7-L11>); [user-message.txt L16-L22](<../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L16-L22>); [AuthTokenFilter.java L83-L118](<../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java#L83-L118>).

### KQ-SEC-16

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected token-issuance contract and documented token separation.

The supplied v2/v3 login path places oud and session ID in the authentication payload. Entitlements are issued in a separate token.

Rationale: buildEntities constructs distinct payloads and returns both token types. The SDK guide explicitly forbids entitlement-token authentication.

Limit: This answers the current source contract, not every deployed environment or historical endpoint. SDK compatibility code still reads an optional legacy entitlements claim. Deployment parity remains part of KQ-SEC-05.

Owner: authentication contract owner.

Consequence: Record the evidenced separation. Do not ask the user to repeat local token-shape inspection.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [JwtAuthenticationController.java L97-L121](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L97-L121>); [JwtTokenUtil.java L48-L84](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L48-L84>); [Single UI SDK V1.1.4 L7-L14](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md#L7-L14>).

### KQ-SEC-17

Status: `CARRIED_FORWARD`. Finding confidence: `HIGH`.
Class: Explicit user requirement and later retained local recovery result.

Required delayed recovery remains in scope. No fallback is accepted. Later native local recovery passed after the pending-renewal correction.

Answer: Required delayed recovery remains in scope. No fallback is accepted.

Rationale: The user authorized the two corrections and reruns. Current source awaits renewal before closing; the retained natural result records successful recovery.

Limit: Local natural recovery does not establish complete UAT conformance or production readiness. The retained result binds mfe-base c42e760 and a substituted local BFF. Its clock limits remain recorded. Remaining activity and cancellation failures cannot be converted into accepted fallbacks. The retained result identifies its executed test-source hash. The current modular helper is separately inspected, not byte-identical.

Owner: application implementation owner.

Consequence: Keep the existing required outcome. Remove the repeated correction-versus-fallback question from the current batch.

Next action: Retain the recorded answer. Do not infer a fallback or waiver.

Evidence: [user-request.txt](<../portal-background-session-20261019/evidence/minor-fixes-20261025/user-request.txt>); [REQ-active-session-renewal.md description](<../../knowledge/candidates/requirements/REQ-active-session-renewal.md#description>); [10-change-review.md sequential-minor-corrections-25-october-2026](<../portal-background-session-20261019/10-change-review.md#sequential-minor-corrections-25-october-2026>).

### KQ-SEC-18

Status: `CARRIED_FORWARD`. Finding confidence: `HIGH`.
Class: Explicit retained scope and absence of a named waiver.

No criterion deferral or acceptance waiver is recorded. All applicable session criteria remain required.

Answer: No named criterion deferral or acceptance waiver is recorded.

Rationale: The later correction request and current stage retain the existing requirement scope. The smaller implementation never waived business criteria.

Limit: A future explicit waiver would require its own named scope and review. No waiver is inferred from continuation or local passing results.

Owner: user for any future explicit scope change.

Consequence: Carry the current full requirement scope. Do not solicit optional deferrals to fill an answered status.

Next action: Retain the recorded answer. Do not infer a fallback or waiver.

Evidence: [REQ-active-session-renewal.md acceptance-criteria](<../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria>); [user-request.txt](<../portal-background-session-20261019/evidence/minor-fixes-20261025/user-request.txt>); [10-change-review.md sequential-minor-corrections-25-october-2026](<../portal-background-session-20261019/10-change-review.md#sequential-minor-corrections-25-october-2026>).

### KQ-SEC-20

Status: `CONSOLIDATED`. Finding confidence: `HIGH`.
Class: Retained assertion mapping and local execution with deployment unknown.

The local audit already retains entitlement assertions, BFF bindings, and case outcomes. They do not verify all newly clarified predicates.

Rationale: The inspected spec uses controlled entitlements and catalog fixtures. The ledger keeps canonical acceptance NOT_ESTABLISHED, including a failed no-entity predicate.

Limit: Historical tests are scoped to their original revisions and fixtures. Their passing labels cannot verify successor criteria. The current BFF template exception and separate data permissions remain visible source boundaries. Effective deployed authorization behavior remains the shared missing binding in KQ-SEC-05.

Owner: portal implementation and deployment owners.

Consequence: Keep assertion and execution gaps as agent verification work. Merge deployment-evidence collection into KQ-SEC-05.

Next action: Use [KQ-SEC-05](#kq-sec-05) for the consolidated contact or evidence follow-up.

Evidence: [knowledge-current-bff.spec.ts L15-L69](<../../e2e/audit-specs/knowledge-current-bff.spec.ts#L15-L69>); [auth-and-knowledge-final-validation.json](<evidence/step-audit-20261022/auth-and-knowledge-final-validation.json>); [case-results.json](<evidence/audit-run-20261022/report-006/case-results.json>).

## Portal scope, architecture, and evolution

### KQ-ARCH-01

Status: `CONSOLIDATED`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Root Config names the portal Markets Operations One. Its description covers Operations processing and integrated post-trade applications.

Rationale: The current HTML directly states the name and scope. The candidate record identifies no accountable scope owner.

Limit: This identifies the supplied implementation wording, not a complete deployed capability inventory. Portal-team ownership of three entitlement rules does not establish ownership of every platform capability.

Owner: unknown.

Consequence: The existing name and documented scope need no repeated explanation. Scope ownership remains material to knowledge publication.

Next action: Use [KQ-SEC-03](#kq-sec-03) for the consolidated contact or evidence follow-up.

Evidence: [index.ejs L8-L16](<../../repos/ui/mfe-root-config/src/index.ejs#L8-L16>); [KT-portal-purpose.md scope](<../../knowledge/candidates/background/KT-portal-purpose.md#scope>); [user-message.txt L7-L22](<../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L7-L22>).

### KQ-ARCH-02

Status: `CONSOLIDATED`. Finding confidence: `HIGH`.
Class: Documented intent.

The retained principles are draft. Explicit user answers already select entry denial, empty-entity denial, and single-entity empty-subject access.

Rationale: The draft labels notification as forthcoming. No new selection of every draft principle is required for this refinement.

Limit: Do not infer approval of interoperability, action tracing, or future notification delivery. Publication review remains separate from the recorded user clarification.

Owner: unknown.

Consequence: Keep source statuses and completed user decisions. Review remaining current capability scope through the accountable baseline owner.

Next action: Use [KQ-SEC-03](#kq-sec-03) for the consolidated contact or evidence follow-up.

Evidence: [Post Trade Portal Principles (Draft) L1-L16](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L1-L16>); [ui-q-002-source.json](<evidence/clarification-20261022/ui-q-002-source.json>); [empty-entity-source.json](<evidence/clarification-20261022/empty-entity-source.json>).

### KQ-ARCH-03

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The source lists future onboarding, AI, telemetry, migration, notification, dashboards, and OpenFin proposals. It records no accepted delivery baseline.

Rationale: The target architecture sections are empty. The current user request concerns question refinement rather than roadmap implementation.

Limit: A proposal title does not establish approval, deployment, owner, or completion. Reopen only the selected feature scope when a concrete adoption or implementation decision arises.

Owner: unknown.

Consequence: Retain these items as proposals. No current question requires the user to approve the complete 2026–2027 roadmap.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Portal New Deployment L3-L18](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3-L18>); [Portal New Deployment L49-L70](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L49-L70>); [user-request.json](<evidence/question-refinement-20261026/user-request.json>).

### KQ-ARCH-04

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Root Config, shell, BFF, SDK, and Auth Server have exact current local Git baselines. Container, Blotter, and Nginx use filesystem hashes.

Rationale: Current checkout inspection identifies the available code. Auth Server now has independent Git history, unlike the October 22 snapshot.

Limit: Local commits do not establish deployed or upstream release identities. The shell has an unrelated tsconfig.tsbuildinfo change. Inspected architecture source files remain identified separately. Missing deployment bindings remain evidence limits, not a reason to repeat local repository inspection.

Owner: unknown.

Consequence: The agent can maintain exact local architecture provenance directly. Reuse existing environment-binding questions when deployment verification is selected.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [root.ts L10-L27](<../../repos/ui/mfe-root-config/src/root.ts#L10-L27>); [Container.tsx L10-L32](<../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L10-L32>); [pom.xml](<../../repos/services/single-ui-bff/pom.xml>).

### KQ-ARCH-05

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `MEDIUM`.
Class: Documented intent.

The guideline prescribes TypeScript, React 18.2.0, functional components, MUI themes, and Context with Reducer. Current manifests declare React ^18.2.0.

Rationale: The original guide states the development baseline. Current shell and tenant manifests corroborate the React generation.

Limit: A manifest declaration does not establish installed, deployed, or platform-approved versions. MUI declarations differ between the shell and tenants. No dependency upgrade is selected in this review.

Owner: unknown.

Consequence: Document the inspected baseline and approval limit. Request a compatibility decision only when a concrete dependency change requires it.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Development Guideline L1-L15](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L1-L15>); [package.json](<../../repos/ui/mfe-base/package.json>); [package.json](<../../repos/ui/mfe-ratan-container/package.json>).

### KQ-ARCH-06

Status: `CONSOLIDATED`. Finding confidence: `HIGH`.
Class: Documented intent.

The Micro frontend Team owns shared repository review and approval. Application teams own domain backend availability and application deployment.

Rationale: Development Principle assigns MT and MAT responsibilities directly. A new user explanation of those documented roles is unnecessary.

Limit: The retained guide does not identify current named contacts or prove later ownership changes. Do not infer that portal-team entitlement-policy ownership covers every compatibility decision.

Owner: unknown.

Consequence: Carry forward documented MT and MAT roles. Consolidate any current ownership correction into the baseline-owner review.

Next action: Use [KQ-SEC-03](#kq-sec-03) for the consolidated contact or evidence follow-up.

Evidence: [Development Principle L4-L10](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md#L4-L10>).

### KQ-ARCH-07

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Documented intent.

Direct external GUI dependencies require a platform-approved exception. The documented alternatives are internal packaging or tenant-owned backend encapsulation.

Rationale: The supplementary principle states the prohibition, exception path, alternatives, and tenant ownership duties directly.

Limit: No inspected exception register proves that every tenant complies or that no exception exists. No new external dependency is proposed in this refinement.

Owner: unknown.

Consequence: Retain the stated rule. Obtain a specific exception decision only when an actual tenant dependency requires it.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Supplementary Principle_ External Frontend Dependency Control L3-L10](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L3-L10>); [Supplementary Principle_ External Frontend Dependency Control L23-L54](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L23-L54>).

### KQ-ARCH-08

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The standalone guide describes import-map reuse of MFE-Base and a Jest-configured template. Its linked template archive is unavailable.

Rationale: The original guide supports the integration pattern. No standalone application onboarding or template change is selected in this review.

Limit: An absent archive does not establish that standalone integration is unsupported or retired. A supported runnable template version requires future template-specific evidence when an application needs it.

Owner: unknown.

Consequence: Retain the documented pattern and missing-archive limit. Remove the unsupported current request to choose or recover every standalone template.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [ReactJS Standalone Project L1-L17](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L1-L17>); [repositories.yaml](<../../registry/repositories.yaml>); [user-request.json](<evidence/question-refinement-20261026/user-request.json>).

### KQ-ARCH-09

Status: `EVIDENCE_FOLLOWUP`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Current manifests declare MUI, Ant Design, and AG Grid packages. The supplied component decision tables are incomplete.

Rationale: Package files establish declared library use. The conceptual design contains blank review, deviation, and decision records.

Limit: Declared package use does not establish licensing entitlement, approval, or deployment. This review selects no new component, procurement, or production release.

Owner: unknown.

Consequence: Do not label packages licensing-approved. Collect specific approval evidence when a release or procurement decision requires that claim.

Next action: Collect the missing binding when its deployment, release, compatibility, or verification decision requires it.

Evidence: [package.json](<../../repos/ui/mfe-base/package.json>); [package.json](<../../repos/ui/mfe-ratan-container/package.json>); [package.json](<../../repos/ui/mfe-cashflow-blotter/package.json>).

### KQ-ARCH-10

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The report recommends Rspack migration or Vite for suitable new projects. Current supplied frontend manifests still declare Webpack.

Rationale: The report proposes pilots rather than recording completed platform adoption. No build-tool migration is requested in the current task.

Limit: Comparative benchmark tables do not prove results for these repositories. No project benchmark execution or migration approval was inspected.

Owner: unknown.

Consequence: Keep the report as research. Reopen provenance and pilot questions only when a concrete tooling migration requires them.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [React Build Tooling Research Report L13-L17](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L13-L17>); [React Build Tooling Research Report L261-L271](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L261-L271>); [package.json](<../../repos/ui/mfe-base/package.json>).

### KQ-ARCH-11

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The notification source describes three experiments. The inspected shell has placeholder subscription handlers rather than a selected notification implementation.

Rationale: The draft records alternatives. A bounded shell and BFF source search found no notification transport implementation.

Limit: The bounded search does not establish absence across every tenant or deployment. No notification adoption or implementation decision is requested in the current task.

Owner: unknown.

Consequence: Retain the experiments as proposals. Remove the request to select a supported transport without an active adoption decision.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Notification (DRAFT) L58-L102](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/page.md#L58-L102>); [index.ts L249-L255](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L249-L255>); [repositories.yaml](<../../registry/repositories.yaml>).

### KQ-ARCH-12

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The table draft offers one-hour, six-hour, and 24-hour retention alternatives. It selects no cleanup or unread-message policy.

Rationale: The exact draft states alternatives. The parent notification adoption question has no current implementation decision.

Limit: Do not select a retention period from a draft example. No current supported notification service or required cleanup behavior is established in this scope.

Owner: unknown.

Consequence: Keep the alternatives in historical knowledge. Reopen retention only when an adopted notification service requires measurable cleanup behavior.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Table Schema L18-L36](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L18-L36>); [user-request.json](<evidence/question-refinement-20261026/user-request.json>).

### KQ-ARCH-13

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The store draft declares isRead as a string and assigns false. The table examples also use boolean read flags.

Rationale: The original store and schema contain a direct type inconsistency. They are proposal material, not an adopted current contract.

Limit: Do not repair the draft by inventing an approved field type. No notification contract implementation is selected in this refinement.

Owner: unknown.

Consequence: Preserve the contradiction. Remove the premature request to choose a notification schema before an applicable service decision exists.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Notification Store and React.useEffect L1-L13](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L1-L13>); [Notification Store and React.useEffect L63-L75](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L63-L75>); [Table Schema L28-L36](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L28-L36>).

### KQ-ARCH-14

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The source list remains unchecked. Current Auth Server declares Spring Boot 4.0.6; BFF declares 3.3.4.

Rationale: The TODO source records no approval. Current POMs show partial implementation evidence, not universal completion of the list.

Limit: Unchecked source status does not prove that no later implementation exists elsewhere. Current local code is not a release or approval record.

Owner: unknown.

Consequence: Retain these items as unchecked proposals. Reopen acceptance and completion questions when a selected work item affects a current decision.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Markets Operation One TODO List L1-L4](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operation One TODO List/page.md#L1-L4>); [pom.xml](<../../repos/services/single-ui-bff/pom.xml>); [pom.xml](<../../repos/services/ratan-auth-server/pom.xml>).

### KQ-ARCH-15

Status: `EVIDENCE_FOLLOWUP`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Nginx templates declare Gateway routes and direct query-service/data-ambassador proxies. External Ansible values determine concrete upstream hosts.

Rationale: Current templates directly show routing branches. The user already supplied the logical ingress model, so that explanation needs no repetition.

Limit: Templates do not establish live DNS, rendered hosts, or deployed route selection. API Gateway implementation remains explicitly outside this review. Missing rendered deployment evidence limits runtime claims but does not block the current logical architecture refinement.

Owner: unknown.

Consequence: Retain the reported topology and exact template exceptions. Request rendered bindings only when a selected deployment decision requires them.

Next action: Collect the missing binding when its deployment, release, compatibility, or verification decision requires it.

Evidence: [ratan_servers.conf.j2 L150-L256](<../../repos/infra/nginx/ratan_servers.conf.j2#L150-L256>); [ratan_upstreams.conf.j2 L1-L26](<../../repos/infra/nginx/ratan_upstreams.conf.j2#L1-L26>); [user-message.txt L16-L22](<../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L16-L22>).

### KQ-ARCH-16

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Auth Server commit 7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee implements EMS3 entitlement retrieval. The earlier statement that this copy lacks EMS3 is stale.

Rationale: The new controller calls Ems3EntitlementService, which obtains an FMAA token and calls Ems3Repository for CES entitlements.

Limit: A bounded Java and POM search found no explicit Entra, SPN, or Azure implementation name. Configured provider endpoints and indirect token services do not prove which live identity provider is selected. User-reported Auth responsibilities remain retained. BFF Entra and EMS3 code also remains independently relevant. No business execution or deployment verification occurred.

Owner: unknown.

Consequence: Correct the stale local EMS3 gap directly. Preserve unbound Entra provider scope without requesting the known architecture explanation again.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Ems3EntitlementController.java L15-L27](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/Ems3EntitlementController.java#L15-L27>); [Ems3EntitlementService.java L40-L115](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java#L40-L115>); [Ems3Repository.java L20-L53](<../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java#L20-L53>).

### KQ-ARCH-17

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `MEDIUM`.
Class: Inspected implementation.

BFF declares Spring Boot Actuator and exposes management web endpoints. Separate controllers implement tile, category, import-map, and configuration administration.

Rationale: The POM, endpoint exposure configuration, and administration mappings explain the distinct implementation capabilities without a custom health controller.

Limit: Framework dependency and configuration do not prove a live health response or environment exposure. The source does not define an additional business workflow called health management. A terminology clarification is unnecessary unless a selected endpoint-level requirement depends on that distinction.

Owner: unknown.

Consequence: Use precise Actuator and administration descriptions. Preserve the user-reported responsibility without asking a nonmaterial terminology question.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [pom.xml L138-L142](<../../repos/services/single-ui-bff/pom.xml#L138-L142>); [application.yml L78-L84](<../../repos/services/single-ui-bff/src/main/resources/application.yml#L78-L84>); [ApplicationConfigController.java L33-L60](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigController.java#L33-L60>).

## Administration and onboarding

### KQ-OPS-001

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `MEDIUM`.
Class: Documented intent.

The retained procedure combines frontend and backend onboarding, EMS2 setup, Admin Module maker-checker review, and tenant-owned configuration promotion. The release flow uses exported CSV files and a tenant pipeline calling the BFF upload endpoint.

Rationale: The onboarding guides, later administration manual, release flow, and implemented upload endpoint describe consistent responsibilities.

Limit: This answers the retained procedure, not attested deployment in each environment. Current environment identities and authorization evidence remain separate.

Owner: unknown.

Consequence: The generic procedure question need not return to the user. Any deployment-specific exception needs a concrete supported scope.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Frontend Onboarding Process L1-L15](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L1-L15>); [Backend Onboarding Process L1-L7](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Backend Onboarding Process/page.md#L1-L7>); [Admin Module Release Flow L3-L24](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L24>).

### KQ-OPS-003

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `MEDIUM`.
Class: Documented intent.

The later release flow assigns change requests, ADO work items, and release pipelines to tenant teams. The administration manual requires different maker and checker users and per-function audit history. The earlier self-service proposal does not establish a change-control exemption.

Rationale: The detailed release procedure and implemented activation/audit paths qualify the earlier proposal.

Limit: Current production approval authority and emergency exceptions are not established by these documents. No production configuration change or emergency release is proposed in this knowledge review.

Owner: unknown release owner.

Consequence: Describe the documented controls without treating a historical proposal as an approved production exemption.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Admin Module L9-L18](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md#L9-L18>); [Admin Module Release Flow L3-L17](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L17>); [User Manual L31-L35](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md#L31-L35>).

### KQ-OPS-004

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The supplied BFF uses the post_trade_portal_service schema and Flyway’s post_trade_portal_service_schema_history table. Its V1_1_0 migration adds entry_name and filter_rule to tile and tile-audit records. Active database migration history is not retained.

Rationale: The source configuration, latest supplied migration, and ApplicationTile entity directly identify the local persistence baseline.

Limit: An independent deployment or database record is required before claiming an active environment schema. No environment-specific catalog migration or deployment decision is requested here.

Owner: unknown deployment owner.

Consequence: Retain the exact source schema as bounded knowledge. Restore a deployment-binding question only for an actual environment-dependent decision.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [application.yml L15-L23](<../../repos/services/single-ui-bff/src/main/resources/application.yml#L15-L23>); [V1_1_0__application_tile_modify.sql L1-L4](<../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_0__application_tile_modify.sql#L1-L4>); [ApplicationTile.java L14-L77](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/entity/ApplicationTile.java#L14-L77>).

### KQ-OPS-006

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The selected user policy requires a registered application entity for portal entry. The single-entity tile rule also requires the configured entity entitlement. No SSDR delegation or guest exception was selected. The older document lists alternatives, not an applicable exception.

Rationale: Explicit user clarifications govern the current portal scope. The historic guest proposal is struck through.

Limit: This does not select an authorization design for an independent future SSDR interface. No specific SSDR delegation requirement or active onboarding decision is supplied.

Owner: unknown SSDR requirement owner.

Consequence: Do not reopen a portal-entry exception through a historical tenant discussion. Ask about delegation only for a named new requirement.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [ui-q-002-source.json](<evidence/clarification-20261022/ui-q-002-source.json>); [empty-subject-source.json](<evidence/clarification-20261022/empty-subject-source.json>); [SSDR On Board Discussion L27-L37](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L27-L37>).

## Release operations

### KQ-REL-001

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The historical release proposal conflicts internally. Its summary states 24 hours; its detailed schedule states 10 hours, 09:00–19:00 SGT. Neither value becomes current policy through source inspection.

Rationale: Both incompatible values appear directly in one retained proposal. No production release is proposed by this knowledge review.

Limit: The governing duration remains unresolved for future release scheduling. This does not select a release window or approve a release.

Owner: unknown release policy owner.

Consequence: Record the proposal conflict. Ask for a governing duration only when an actual release-scheduling decision depends on it.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Markets Operations One Release L13-L19](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L13-L19>); [Markets Operations One Release L44-L54](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L44-L54>).

### KQ-REL-002

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The historical urgent-release proposal requires all confirmations by Monday EOD. It also permits proceeding when nobody raises concerns. These are conflicting authorization conditions, not a selected current rule.

Rationale: The conflict is explicit in adjacent source rows. No urgent release or failed-release scheduling decision is requested.

Limit: No current urgent-release approval policy is established. Silence must not be treated as recorded human authorization.

Owner: unknown release policy owner.

Consequence: Preserve the contradiction without asking an irrelevant scheduling question during knowledge clarification.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Markets Operations One Release L144-L151](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L144-L151>).

### KQ-REL-003

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The BFF pipeline extends java-maven.yml; MFE Base extends nodejs-mfe.yml from the shared ADO templates repository. Both expose release-work-item and rollback parameters and select Ansible deployment. The retained tenant promotion flow exports CSV configuration and calls the authenticated BFF upload endpoint.

Rationale: The checked pipeline entrypoints and upload controller provide exact local implementation bindings.

Limit: The external shared template implementation and executed environment pipeline records are unavailable locally. Historical release-window proposals remain qualified rather than selected as current scheduling policy.

Owner: unknown deployment owner.

Consequence: Use the known pipeline entrypoints and documented promotion contract. Obtain executed environment bindings only for an actual deployment decision.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [azure-pipelines-maven.yml L1-L46](<../../repos/services/single-ui-bff/azure-pipelines-maven.yml#L1-L46>); [azure-pipelines-npm.yml L5-L47](<../../repos/ui/mfe-base/azure-pipelines-npm.yml#L5-L47>); [Admin Module Release Flow L3-L24](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L24>).

### KQ-REL-004

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The supplied upload endpoint still requires fmaa_access_token. It calls the configured FMAA verification endpoint and rejects inactive identities. The old checklist’s decommissioning warning supplies no replacement contract or effective migration date.

Rationale: ApplicationConfigController calls ApplicationConfigServiceImpl before processing CSV files. Both current source paths retain FMAA validation.

Limit: This establishes the supplied source contract, not current FMAA service availability in production. No replacement migration is inferred from an historical warning.

Owner: unknown authentication owner.

Consequence: Record FMAA as the implemented dependency. Reopen migration planning only if a named decommissioning or upload-change decision requires it.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [ApplicationConfigController.java L53-L72](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigController.java#L53-L72>); [ApplicationConfigServiceImpl.java L20-L31](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationConfigServiceImpl.java#L20-L31>); [Admin Module Release Checklist Template L16](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L16>).

### KQ-REL-005

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The retained calendar explicitly separates Portal, tenant, technical, and business dates. The request templates permit Portal deployment before application deployment. These are planning and sequencing records, not retained deployment or acceptance results.

Rationale: Calendar rows and request fields directly establish separate milestone identities. They do not establish completion.

Limit: Actual completion requires the selected release’s deployment and business sign-off records. No specific tenant activation or release acceptance decision is requested in this review.

Owner: unknown release owner.

Consequence: Keep technical and business activation distinct. Do not request all tenant execution records without a named release decision.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Markets Operations One Release Calendar L7-L16](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/page.md#L7-L16>); [[Template] Markets Operations One Change Request L21-L23](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/[Template] Markets Operations One Change Request/page.md#L21-L23>); [FSSDS Data Distribution and Reporting (DDR) L9-L17](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L9-L17>).

### KQ-REL-006

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The retained tenant requests describe requested capabilities and expected readiness fields. CDUPS leaves sign-off, profiles, user counts, and UVT users unprovided. VPA withdraws several evidence references. These incomplete requests cannot establish present release readiness.

Rationale: The missing and struck-through fields are directly visible in the retained requests.

Limit: This is not a finding that the tenants remain unready today. A named current tenant release would require its own applicable evidence.

Owner: unknown tenant release owner.

Consequence: Preserve requested capability descriptions as historical intent. Avoid a blanket current-readiness question outside an identified tenant release scope.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Markets Operation One Change Request - CDUPS L14-L21](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/Markets Operation One Change Request - CDUPS/page.md#L14-L21>); [VPA Fix-link and Monitor Change Request L12-L22](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/VPA Fix-link and Monitor Change Request/page.md#L12-L22>); [Admin Module Release Checklist Template L19-L29](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L19-L29>).

## Application interoperability

### KQ-INT-001

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Documented intent.

The requesting tenant owns business demand and caller implementation. Portal routes intents and context and applies its access-control boundary. The receiving tenant owns the handler and business action. Joint readiness requires registration, context agreement, authorization, tests, release readiness, and provider deployment.

Rationale: The interoperability guide explicitly assigns these roles and lists the joint prerequisites.

Limit: The guide defines responsibility roles, not accountable contacts for every possible future feature. A named new integration must identify its specific caller and provider owners.

Owner: caller tenant, provider tenant, and portal roles; named contacts unknown.

Consequence: Use the documented joint-delivery model without asking the user to restate it. Collect feature-specific owners during actual integration intake.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [Interoperability Guide L27-L60](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L27-L60>); [useOpenfin.ts L47-L108](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L47-L108>); [index.ts L152-L178](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L152-L178>).

### KQ-INT-002

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The supplied shell contains an OpenFin hook and launch-intent handling for cashflow, trade, and general target parameters. Home calls this hook. Source availability does not establish delivery dates or active runtime installation in any environment.

Rationale: The current hook and its Home caller establish implemented feature paths. The historical briefing supplies plans rather than environment execution bindings.

Limit: No current production OpenFin rollout or adoption decision is requested. Environment delivery remains unverified and must not be inferred from repository code.

Owner: unknown interoperability deployment owner.

Consequence: Retain implemented capabilities and historical milestones separately. Request dated deployment records only for a named rollout claim.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [useOpenfin.ts L8-L15](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L8-L15>); [useOpenfin.ts L47-L108](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L47-L108>); [index.tsx L43-L50](<../../repos/ui/mfe-base/src/pages/Home/index.tsx#L43-L50>).

### KQ-INT-003

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The current shell registers scb.ViewLaunch. It accepts scb.fmptp.cashflows, scb.fmptp.trade.query, and scb.fmptp.general.parameters contexts. Trade IDs and filters become tile parameters; general parameters pass to the named target. This differs from the older fmchannel and OpenTile examples.

Rationale: The current hook declares the names, payload branches, and dispatcher calls. Direct unit assertions cover these transformations.

Limit: No explicit schema-version field or response contract is declared by this hook. This is the inspected implementation contract, not proof of external producer adoption or business approval.

Owner: unknown interoperability contract owner.

Consequence: Replace the generic contract question with the exact source contract and its limits. Do not force selection of obsolete POC names.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [useOpenfin.ts L8-L15](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L8-L15>); [useOpenfin.ts L50-L106](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L50-L106>); [useOpenfin.test.ts L192-L206](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.test.ts#L192-L206>).

### KQ-INT-004

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The supplied openfintoken URL bootstrap is gated to LOCAL or DEV with window.fin present. Other routing paths use the normal session validation flow. The POC URL-token example does not establish a production handoff contract.

Rationale: The routing controller applies the environment guard explicitly. No production OpenFin handoff requirement is selected here.

Limit: Source guards do not establish deployed environment values or provider configuration. A future production launch integration requires an explicit approved handoff contract.

Owner: unknown production interoperability owner.

Consequence: Describe the implemented development-only bootstrap. Do not ask the user to design an unsupported production integration now.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [useController.ts L38-L72](<../../repos/ui/mfe-base/src/routing/common/useController.ts#L38-L72>); [3. Application Interoperability L1-L23](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/3. Application Interoperability/page.md#L1-L23>).

### KQ-INT-005

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Inspected implementation.

The local root manifest requests OpenFin runtime 26.102.71.8. MFE Base declares fdc3-2.1 at 2.1.x and openfin-fdc3 at ^0.2.3. The historical briefing separately names stable-v41. These declarations do not establish an installed environment support matrix.

Rationale: Exact manifest and dependency declarations are available locally. The package and runtime versions identify different artifacts.

Limit: The browser manifest is a local demonstration configuration. No supported-environment compatibility matrix or actual OpenFin rollout decision is supplied.

Owner: unknown runtime support owner.

Consequence: Retain the exact declared versions with their distinct scopes. Require environment support evidence only for a named runtime decision.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [manifest.fin.json L1-L17](<../../repos/ui/mfe-root-config/public/manifest.fin.json#L1-L17>); [package.json L109-L120](<../../repos/ui/mfe-base/package.json#L109-L120>); [Ratan OpenFin Briefing L56-L61](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L56-L61>).

### KQ-INT-006

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Observed execution.

The 25 October retained run contains 22 passing OpenFin-hook and dispatcher unit cases. Source bindings match the current hook, dispatcher, and inspected test files. Assertions cover listener registration, payload transformation, tile lookup, and workspace parameters.

Rationale: The saved per-case results match inspected assertions and the run’s c42e7609c4e14eb53de32702e4bd3424a223988a source binding.

Limit: Mocks replace FDC3 libraries and provider behavior. These results do not verify real cross-library broadcasts or target rendering. The runner uses forceExit; passing assertions do not prove resource cleanup. No new execution occurred during this investigation.

Owner: unknown interoperability test owner.

Consequence: Use retained assertions for bounded unit evidence. Keep actual runtime interoperability unverified without asking for an unspecified future deployment.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [useOpenfin.test.ts L192-L206](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.test.ts#L192-L206>); [useOpenfin.test.ts L223-L244](<../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.test.ts#L223-L244>); [index.test.ts L19-L52](<../../repos/ui/mfe-base/src/hooks/dispathcer/index.test.ts#L19-L52>).

## Observability and performance

### KQ-OBS-001

Status: `ANSWERED_FROM_EVIDENCE`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Both current frontend analytics interfaces declare attribute1 through attribute20. The BFF request DTO also declares twenty custom fields. The hook spreads those fields into requests; the service serializes the DTO for Elasticsearch. The older ten-field example is stale for this source baseline.

Rationale: Producer types, the posting caller, transport DTO, controller, and storage writer agree on the declared twenty-field contract.

Limit: This does not establish active Elasticsearch mappings or dashboard field availability. No runtime maximum-rejection assertion or deployed storage execution is claimed.

Owner: unknown analytics contract owner.

Consequence: Record the typed twenty-field implementation contract. Do not ask the user to choose between obsolete documentation and directly inspected source.

Next action: Use this bounded answer. Apply separate review gates before any governed publication.

Evidence: [model.ts L12-L69](<../../repos/ui/mfe-base/src/analytics/model.ts#L12-L69>); [index.ts L12-L30](<../../repos/ui/mfe-base/src/analytics/index.ts#L12-L30>); [RequestOfAnalytics.java L9-L39](<../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfAnalytics.java#L9-L39>).

### KQ-OBS-003

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The retained throughput page reports 500 users, 250-second ramp-up, five iterations, and 17,500 successful requests. Its maximum reported response is 2,023 milliseconds for SSO validation. The referenced JMeter plan and result archive are not retained in the inspected source collection.

Rationale: The source directly records the workload and summary. The available material supports a historical report, not current measured capacity.

Limit: These are reported historical figures, not inspected assertion-bearing load-test results. No current sizing or performance-run decision is supplied. Current acceptance budgets remain a separate policy question.

Owner: unknown performance test owner.

Consequence: Keep the historical report qualified. Collect a current run after a concrete workload and acceptance budget are selected.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Throughput Testing in UAT L11-L44](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Throughput Testing in UAT/page.md#L11-L44>); [FMO Post Trade Portal Frontend Performance Testing May 2023 L230-L256](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L230-L256>).

### KQ-OBS-004

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Inspected implementation.

Webpack emits fixed entry filenames and chunkhash-based lazy chunks for the shell, container, and supplied cashflow tile. The shell server uses express.static. A no-cache helper exists but is not registered by that server entrypoint. Active environment cache headers remain unverified.

Rationale: Inspected build output declarations and the server’s middleware registration establish the available implementation.

Limit: The historical design’s 120-day value is not established as an active deployed header. No named cache-defect, environment change, or cache acceptance run is requested here.

Owner: unknown deployment owner.

Consequence: Describe verified build declarations and preserve the deployment limit. Obtain response captures only when an actual environment-specific cache decision needs them.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [webpack.config.js L24-L36](<../../repos/ui/mfe-base/webpack.config.js#L24-L36>); [webpack.config.js L25-L36](<../../repos/ui/mfe-ratan-container/webpack.config.js#L25-L36>); [webpack.config.js L42-L47](<../../repos/ui/mfe-cashflow-blotter/webpack.config.js#L42-L47>).

### KQ-OBS-006

Status: `NOT_CURRENT_DECISION`. Finding confidence: `HIGH`.
Class: Documented intent.

The retained dashboard guide names DEV and UAT locations and describes nine dashboards. Its Production location remains a placeholder. No Kibana saved-object export was found in the inspected application and Nginx file inventories.

Rationale: The exact guide and bounded repository inventory establish available documentation, not active dashboard availability.

Limit: The missing local binding does not prove that production dashboards do not exist. No production-monitoring or dashboard rollout decision is requested in this review.

Owner: unknown analytics operations owner.

Consequence: Preserve the production observation limit. Obtain active URLs and operator contacts only for a named operational-readiness decision.

Next action: Retain the stated limit. Reopen only when a concrete decision requires this scope.

Evidence: [Analytic Dashboard in Kibana L1-L17](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Analytic Dashboard in Kibana/page.md#L1-L17>); [KT-observability-and-performance.md usage-dashboards](<../../knowledge/candidates/observability/KT-observability-and-performance.md#usage-dashboards>).

## Request and source facts

The [refinement request](evidence/question-refinement-20261026/user-request.json) authorizes investigation and revision of this living document.
The [continuation](evidence/question-refinement-20261026/user-continuation.json) supplies no missing business answer.
The [input binding](evidence/question-refinement-20261026/input-binding.json) identifies the preserved version 2 bytes and earlier source map.
The [reconciliation](evidence/question-refinement-20261026/reconciliation.json) accounts for every original question and current disposition.

## Proposed change

Version 3 implements investigation-first question refinement. It reduces 60 answer prompts to nine editable entries.
It preserves recorded answers and stable IDs. It distinguishes source findings, intended policy, review requirements, and execution limits.

## Scope and affected artifacts

This change affects the living question document, clarification-stage navigation, evidence index, and retained investigation evidence.
No application symbol, caller, importer, or runtime interface changes. Runtime risk is low.
Interpretation risk remains material. Evidence classes, authority limits, and exact sources control that risk.
The frozen intake and canonical test definitions retain their existing bytes.

## Options and consequences

The user selected asynchronous document review. Suggested choices remain unselected and editable.
Source-backed answers remove repeated source-inspection requests. Missing policy remains visible for its affected decision.
Historical proposals remain qualified. Conditional evidence gaps remain separate from required business answers.

## Proposed acceptance and validation

Check all 60 IDs, nine editable entries, original answers, source locators, hashes, revisions, links, and protected-file integrity.
Run artifact lint, workspace validation, bounded writing checks, and an independent review.
The [check receipt](evidence/question-refinement-20261026/checks.json) records actual results and evidence limits.
Automated checks do not establish full ASD-STE100 compliance. Full writing review remains pending.

## Implementation and release proposal

This stage refines the review document. Application implementation, new business execution, and release approval are outside this stage.
No new user clarification changes a business rule. Domain ingestion and publication remain pending the applicable returned answers and reviews.
Source corrections here identify investigated evidence. They do not silently revise candidate records or immutable audit events.

## Requested decision and actual disposition

Complete the nine entries in [answer navigation](#answer-navigation), then request review and ingestion continuation.
Resolved findings require no repeated technical explanation. Returning answers does not itself grant publication approval.

## Sources and evidence limits

Original source snapshots, exact registered repository revisions, assertions, and retained execution results were inspected.
The [repository bindings](evidence/question-refinement-20261026/repository-bindings.json) identify local revisions and filesystem copies.
Current source cannot establish deployment parity. Earlier execution remains limited to its recorded revisions and fixtures.

The [Confluence read](evidence/question-refinement-20261026/confluence-source-check.json) failed with `CONNECTOR_FAILURE`.
The [presence check](evidence/question-refinement-20261026/connector-readiness.json) found required connector settings unavailable.
This failure does not establish absence of external records. No new browser or business test execution occurred.

## Unknowns and blockers

Eight missing policies block their affected acceptance definitions. The shared contact entry supports accountable review routing.
Required human review blocks publication separately. Conditional deployment evidence limits only decisions that require deployed behavior.

Owner: unknown where stated. Next action: Complete the meaningful remaining entries, or identify their responsible contacts.
