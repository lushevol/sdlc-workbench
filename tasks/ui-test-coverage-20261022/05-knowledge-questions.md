---
artifact_kind: change-request
id: KNOWLEDGE-QUESTION-BATCH-20261022
version: 1
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

# Knowledge questions and answers — Round 1

> **Critical conclusions: Complete this answer document.**
>
> **This document contains the current clarification batch.**
> Action: Fill its answer fields and hand back this file.
> Consequence: Material unknowns block the affected knowledge decision. Owner: user for answers; other owners remain stated per question.
> Evidence: The [batch-workflow instruction](evidence/clarification-20261022/batched-question-workflow-source.json).

## Current task state

Baseline: `231f3d02a246a1d16814833173375dad789e6fcb`.
This batch contains 60 numbered entries across all 11 domain records.
Two entries carry forward existing scope defaults. Change them only if you want a different scope.
The source map covers all 48 current frontmatter questions and additional source-backed task gaps.
No domain answer or approval is inferred from the request to batch questions.

Named next phase: User answer collection and review. Readiness: `READY`.
The questions are ready for user review. Publication remains pending the returned answers and applicable content review.

## How to answer

Edit this file and keep each question ID. Put your response after its `Answer:` label.
Your explicit answers are the first-priority reference for intended behavior within their stated scope.
Write `unknown` if you cannot answer. Name a contact or evidence location if available.

Write `not applicable` with a reason for unsupported features. Do not repeat answers already recorded below.
Identify any answer that is a proposal rather than a current rule.
Use the shared scope below, then state exceptions beside affected answers.
Leave status labels for me to update.

| Shared review field | Your response |
| --- | --- |
| Respondent name or identifier | |
| Role and authority for these answers | |
| Answer date | |
| Default environment scope | |
| Effective date or applicable release | |
| Topic owners or delegates, if known | |
| Answers that remain proposals | |

Decision questions need the intended rule. Evidence questions need an existing record location or a collection contact.
Ownership questions need an accountable team, role, or named person.
I will collect available engineering evidence. You do not need to repeat source inspections already completed.

## Review and refinement loop

1. You fill this document and hand it back.
2. I preserve your returned bytes before further review.
3. I check scope, conflicts, source bindings, measurable outcomes, and missing evidence.
4. I update affected knowledge, source provenance, versions, and audit events.
5. I record required content review before publishing the resolved ground-truth baseline.
6. I return remaining questions or material wording changes in this same document.

The loop ends when no material question or contradiction remains within the agreed scope.
Implementation and execution claims require their own inspected evidence.

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

## Question navigation

| Group | Entries | Start |
| --- | --- | --- |
| Security, entitlements, and sessions | 20 | [KQ-SEC-01](#kq-sec-01) |
| Portal scope, architecture, and evolution | 17 | [KQ-ARCH-01](#kq-arch-01) |
| Administration and onboarding | 5 | [KQ-OPS-001](#kq-ops-001) |
| Release operations | 6 | [KQ-REL-001](#kq-rel-001) |
| Application interoperability | 6 | [KQ-INT-001](#kq-int-001) |
| Observability and performance | 6 | [KQ-OBS-001](#kq-obs-001) |

## Security, entitlements, and sessions

### KQ-SEC-01

**A tile lists two entities and has an empty subject. Should one matching entity permit visibility and launch?**

The user selected entity-only access for one configured entity. Multiple-entity matching remains unanswered.

Type: `decision`. Current owner: `unknown`.
Consequence: Multiple-entity acceptance cannot select an expected result.
Sources:

- [05-entry-clarification](05-entry-clarification.md#multiple-entity-configuration)
- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)
- [SSDR On Board Discussion](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L17-L20>)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-02

**Who will provide the recorded portal-team review for the three saved entry and tile rules?**

Portal-team ownership and all-environment scope are already recorded. A named review of current candidate content remains absent.

Type: `ownership`. Current owner: `portal team`.
Consequence: Current policy records cannot be published as reviewed ground truth.
Sources:

- [05-entry-clarification](05-entry-clarification.md#current-task-state)
- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#open-questions)
- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-03

**Who owns portal session policy and can review the current renewal criteria?**

The portal team owns the three clarified entitlement rules. That answer does not assign session-policy ownership.

Type: `ownership`. Current owner: `unknown`.
Consequence: Session requirements lack an accountable reviewer.
Sources:

- [REQ-active-session-renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria)
- [10-change-review](../portal-background-session-20261019/10-change-review.md#stage-boundary-and-readiness)
- [GF-session-renewal-verification-gates](../../evidence/knowledge/findings/GF-session-renewal-verification-gates.md#resolution)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-04

**What access, idle, refresh, and provider-session limits should apply in each supported environment?**

Historical sources contain conflicting 105-minute and 225-minute refresh durations. Continuous active renewal is already required.

Type: `decision`. Current owner: `unknown session owner`.
Consequence: Timing expectations cannot be applied consistently.
Sources:

- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#session-concepts-and-intended-lifecycle)
- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#open-questions)
- [REQ-active-session-renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#description)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-05

**Where are deployment bindings for supported environments, starting with UAT? Include artifacts, runtime overrides, token properties, origins, and clocks.**

The photograph shows nearly eight hours remaining. Local YAML declares fifteen minutes; app.conf contains a 480-minute launch value.

Type: `evidence`. Current owner: `unknown authentication owner`.
Consequence: UAT configuration correction and idle-timeout acceptance remain blocked.
Sources:

- [10-change-review](../portal-background-session-20261019/10-change-review.md#uat-timeout-inquiry-21-october-2026)
- [10-change-review](../portal-background-session-20261019/10-change-review.md#unknowns-and-blockers)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-06

**Which login methods, fallback routes, and activation persistence should each supported environment permit?**

The retained design and pilot guide differ on activation values, persistence, rollout dates, and fallback availability.

Type: `decision`. Current owner: `unknown identity owner`.
Consequence: Current login and restart instructions remain ambiguous.
Sources:

- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#authentication-responsibilities)
- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#entra-onboarding-and-user-profile)
- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#evidence-limits)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-07

**Where are the applicable Entra release, deployment, and environment verification records?**

Schedules and pilot guides do not establish completed migration. Existing local source inspection cannot prove effective deployment.

Type: `evidence`. Current owner: `unknown release owner`.
Consequence: The current migration state remains unverified.
Sources:

- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#open-questions)
- [10-change-review](../portal-background-session-20261019/10-change-review.md#unknowns-and-blockers)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-08

**Which identity-profile fields and canonical values may downstream services require?**

The production guide records changed surnames, country codes, and missing locale values after provider migration.

Type: `decision`. Current owner: `unknown identity owner`.
Consequence: Downstream audit and application logic lack a stable profile contract.
Sources:

- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#entra-onboarding-and-user-profile)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-09

**Which FMAA service-account and bank-ID flows remain supported, and what validity limits apply?**

Historical guidance names seventeen-year and seven-day validity. Those examples do not establish current provider contracts.

Type: `decision`. Current owner: `unknown authentication owner`.
Consequence: Historical validity values could be applied to unsupported flows.
Sources:

- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#historical-machine-to-machine-authentication)
- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-10

**Where are current scan, remediation, and retest records for the applicable historical security findings?**

Retained notes report fixes but omit referenced scan attachments and inspected retest results.

Type: `evidence`. Current owner: `unknown security owner`.
Consequence: Current control effectiveness and finding closure remain unestablished.
Sources:

- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#historical-security-observations)
- [KT-authentication-and-sessions](../../knowledge/candidates/security/KT-authentication-and-sessions.md#evidence-limits)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-11

**Where is the current consumer inventory with each SDK artifact, dependency version, effective configuration, and deployment revision?**

The supplied SDK guides span several versions. Exact deployed downstream consumers remain unavailable.

Type: `evidence`. Current owner: `unknown application owners`.
Consequence: Compatibility and request protection cannot be bound to current services.
Sources:

- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#evidence-limits)
- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-12

**Which trusted control authenticates requests when path exclusions or skip headers bypass SDK JWT validation?**

The guides describe bypass settings without identifying a replacement authentication boundary.

Type: `decision`. Current owner: `unknown security owner`.
Consequence: Protected-request expectations and bypass rejection cases remain incomplete.
Sources:

- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-13

**Which protected operations require subject and action permissions, and which application owner defines their denial results?**

The SDK validates authentication and retrieves entitlements. Application data permission enforcement remains a separate responsibility.

Type: `decision`. Current owner: `unknown application owners`.
Consequence: Denied-request assertions cannot target a defined application permission boundary.
Sources:

- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#evidence-limits)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-14

**What cache lifetime and maximum permission-revocation delay must each application enforce across instances?**

Caching is recommended, but distributed invalidation and current expiry rules are not defined.

Type: `decision`. Current owner: `unknown application owners`.
Consequence: Acceptance cannot distinguish permitted cache delay from stale authorization.
Sources:

- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-15

**Which tabs, devices, and downstream instances must logout revoke, and within what maximum delay?**

Historical source shows blacklist cleanup and filter-local revocation. No universal logout boundary is established.

Type: `decision`. Current owner: `unknown session owner`.
Consequence: Refresh reuse and cross-instance logout acceptance lack a required predicate.
Sources:

- [GF-refresh-revocation-scope](../../evidence/knowledge/findings/GF-refresh-revocation-scope.md#proposed-action)
- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-16

**Where are current environment-specific token contracts showing whether authentication JWTs include entitlements?**

The SDK overview announces a DEV change in 2024. It does not establish current token shape elsewhere.

Type: `evidence`. Current owner: `unknown identity owner`.
Consequence: Consumers may rely on fields absent from current authentication tokens.
Sources:

- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#entitlement-retrieval-and-lifecycle)
- [KT-sdk-and-entitlements](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#open-questions)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-17

**Must delayed recovery be corrected before acceptance, or is a specific fallback acceptable?**

The required background scope includes recovery. No fallback or criterion waiver has been accepted.

Type: `decision`. Current owner: `user and unknown authentication owner`.
Consequence: The required background scope cannot receive acceptance.
Sources:

- [10-change-review](../portal-background-session-20261019/10-change-review.md#unknowns-and-blockers)
- [10-change-review](../portal-background-session-20261019/10-change-review.md#requested-decision-and-actual-disposition)

Answer: Required delayed recovery remains in scope. No fallback is accepted.

Status: `CARRIED_FORWARD`. Answer only if you propose a change.

### KQ-SEC-18

**Which specific session criteria, if any, may be deferred from the current acceptance scope?**

The user requested evidence before broader deferrals. No named criterion waiver currently exists.

Type: `decision`. Current owner: `user`.
Consequence: No acceptance waiver can be claimed from the smaller implementation scope.
Sources:

- [10-change-review](../portal-background-session-20261019/10-change-review.md#unknowns-and-blockers)
- [REQ-active-session-renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria)

Answer: No named criterion deferral or acceptance waiver is recorded.

Status: `CARRIED_FORWARD`. Answer only if you propose a change.

### KQ-SEC-19

**Which operation rechecks launch authorization, and what denial state and protected fields must the test observe?**

KNOW-014 proposes permission-loss rejection. Its authorization operation, protected fields, and denial state remain undefined.

Type: `decision`. Current owner: `unknown portal and application owners`.
Consequence: The proposed denial assertion cannot establish business acceptance.
Sources:

- [06-test-cases](06-test-cases.md#know-014)

Answer:

Status: `UNANSWERED`.

### KQ-SEC-20

**Where can we obtain the deployed bindings and retained authorization tests for the three clarified portal rules?**

The entry, empty-entity, and empty-subject answers establish intended behavior. Existing historical tests do not verify every new predicate.

Type: `evidence`. Current owner: `portal team`.
Consequence: Business execution acceptance remains separate from publication of clarified intent.
Sources:

- [05-entry-clarification](05-entry-clarification.md#canonical-case-applicability)
- [05-entry-clarification](05-entry-clarification.md#empty-subject-configuration)

Answer:

Status: `UNANSWERED`.

## Portal scope, architecture, and evolution

### KQ-ARCH-01

**Who confirms the current portal name, scope, and supported capability inventory?**

The introduction remains under edit. The existing inventory already describes shared entry and post-trade capabilities.

Type: `ownership`. Current owner: `unknown`.
Consequence: Unconfirmed names and capability boundaries cannot become the current published scope.
Sources:

- [KT-portal-purpose](../../knowledge/candidates/background/KT-portal-purpose.md#business-purpose)
- [KT-portal-purpose](../../knowledge/candidates/background/KT-portal-purpose.md#capability-boundaries)

Answer guidance: Name the accountable owner and correct only outdated inventory entries. Do not repeat the supplied four-layer explanation.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-02

**Which remaining draft principles are accepted, and from what effective date?**

Entry denial and empty-subject access already have user answers. Remaining draft concerns include interoperability, action tracing, and notifications.

Type: `decision`. Current owner: `unknown`.
Consequence: Unselected draft principles cannot define current required behavior.
Sources:

- [KT-portal-purpose](../../knowledge/candidates/background/KT-portal-purpose.md#scope-and-roadmap)
- [Post Trade Portal Principles (Draft)](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L3-L16>)

Answer guidance: Confirm remaining principles or mark them proposed, superseded, or out of scope.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-03

**Which 2026 and 2027 proposals are approved, deployed, deferred, rejected, or still proposed?**

The proposal lists tenant onboarding, workflow AI, telemetry, infrastructure migration, notification, dashboards, and OpenFin.

Type: `decision`. Current owner: `unknown`.
Consequence: Proposed services cannot define current deployment or accepted delivery scope.
Sources:

- [Portal New Deployment](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L3-L16>)
- [Portal New Deployment](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L49-L70>)
- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#platform-proposals-for-2026-and-early-2027)

Answer guidance: Give each relevant item its status, owner, target environment, and accepted requirement or release reference.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-04

**Which release or upstream revisions bind the supplied repositories to supported environments?**

Local inspection already identifies Root Config, shell, BFF, and SDK commits. Four supplied repositories have filesystem hashes only.

Type: `evidence`. Current owner: `unknown`.
Consequence: Inspected local code cannot establish supported deployment versions without a release binding.
Sources:

- [KT-frontend-composition](../../knowledge/candidates/architecture/KT-frontend-composition.md#current-four-layer-clarification)
- [ARC-portal-service-relationships](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#evidence-limits)
- [source-review](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json)

Answer guidance: Provide release tags, artifact identities, repository links, or the responsible contact. Existing local source inspection need not be repeated.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-05

**Which development guideline and shared dependency versions are currently approved?**

The retained guideline names React 18.2.0, TypeScript, functional components, shared MUI themes, and Context with Reducer.

Type: `decision`. Current owner: `unknown`.
Consequence: Historical guidance cannot define the accepted baseline for new tenant development.
Sources:

- [KT-frontend-composition](../../knowledge/candidates/architecture/KT-frontend-composition.md#development-guidance-and-performance-boundaries)
- [Development Guideline](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L1-L15>)

Answer guidance: Identify the current guideline revision, shared dependency versions, and effective date. Correct obsolete guidance explicitly.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-06

**Who owns compatibility changes across shared modules and tenant applications?**

The source assigns shared repository review to the microfrontend team. Current named ownership and escalation remain unconfirmed.

Type: `ownership`. Current owner: `unknown`.
Consequence: Cross-application interface changes lack an accountable compatibility decision owner.
Sources:

- [KT-frontend-composition](../../knowledge/candidates/architecture/KT-frontend-composition.md#ownership-and-availability)
- [KT-frontend-composition](../../knowledge/candidates/architecture/KT-frontend-composition.md#shared-code-and-compatibility)

Answer guidance: Name the accountable team or role, tenant responsibilities, review boundary, and escalation contact.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-07

**Which external frontend dependency policy and approved exceptions currently apply?**

The source prohibits direct external GUI dependencies without platform review. It permits internal packaging or tenant backend encapsulation.

Type: `decision`. Current owner: `unknown`.
Consequence: Tenant dependency exceptions cannot be accepted without their authority, scope, and expiry or effective date.
Sources:

- [KT-frontend-composition](../../knowledge/candidates/architecture/KT-frontend-composition.md#external-frontend-dependencies)
- [Supplementary Principle_ External Frontend Dependency Control](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L3-L10>)
- [Supplementary Principle_ External Frontend Dependency Control](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L35-L54>)

Answer guidance: Confirm the policy and list exceptions, accountable tenant owners, review records, environments, and effective dates.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-08

**Which standalone template and shared-component versions remain supported?**

The guide describes import-map reuse of MFE-Base. Its simple-app.zip archive and setup screenshot are absent.

Type: `evidence`. Current owner: `unknown`.
Consequence: The available text cannot establish a supported runnable standalone integration.
Sources:

- [KT-frontend-composition](../../knowledge/candidates/architecture/KT-frontend-composition.md#standalone-react-integration-pattern)
- [ReactJS Standalone Project](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L1-L17>)

Answer guidance: Provide the supported template location or release reference. Mark this integration unsupported if it has been retired.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-09

**Which component libraries and licenses are approved, with versions and effective dates?**

The supplied comparison is historical. Its conceptual design contains uncompleted review, deviation, and decision tables.

Type: `decision`. Current owner: `unknown`.
Consequence: Historical comparisons cannot establish an approved component or licensing standard.
Sources:

- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#component-library-evaluation)
- [Conceptual Design DRAFT](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Draft/Conceptual Design DRAFT/page.md#L169-L189>)

Answer guidance: Identify the accepted MUI, Ant Design, or AG Grid choices, applicable license editions, scope, and decision reference.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-10

**Is the build-tool report historical research, or does it support an approved migration decision?**

The report recommends Rspack or Vite. It retains no author, date, benchmark inputs, or project execution provenance.

Type: `evidence`. Current owner: `unknown`.
Consequence: Unbound benchmark rankings cannot justify the current migration baseline.
Sources:

- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#build-tool-research)
- [React Build Tooling Research Report](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L13-L17>)
- [React Build Tooling Research Report](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L52-L62>)

Answer guidance: If adopted, identify the author, report date, tested versions, benchmark records, approved decision, and applicable project pilot.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-11

**Which notification approach is supported, and in which environments?**

The drafts describe GraphQL over SSE, GraphQL over WebSocket, and Spring Boot SSE experiments.

Type: `decision`. Current owner: `unknown`.
Consequence: Experimental locations do not identify a supported notification service or contract.
Sources:

- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#notification-experiments)
- [Notification (DRAFT)](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/page.md#L58-L92>)

Answer guidance: Name the chosen approach, owner, code or release reference, and scope. Answer not adopted if no supported service exists.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-12

**If notifications are supported, what retention, cleanup, and unread-message rules apply?**

The table draft proposes one-hour, six-hour, or 24-hour retention. Its unread-message interaction remains undefined.

Type: `decision`. Current owner: `unknown`.
Consequence: Cleanup and unread behavior cannot receive measurable criteria until their intended rules are selected.
Sources:

- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#notification-entity-and-retention-draft)
- [Table Schema](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L18-L36>)

Answer guidance: State retention periods, cleanup trigger, unread handling, owner, environment, and effective date. Skip if notifications are not adopted.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-13

**If notifications are supported, which schema defines read, display, subscription, and delivery behavior?**

The store draft declares isRead as a string but assigns a boolean. No accepted schema is retained.

Type: `decision`. Current owner: `unknown`.
Consequence: Conflicting draft field types cannot define interoperable notification behavior.
Sources:

- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#notification-experiments)
- [Notification Store and React.useEffect](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L1-L15>)
- [Notification Store and React.useEffect](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L63-L75>)

Answer guidance: Provide the versioned schema or select the field types and delivery semantics. Skip if notifications are not adopted.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-14

**Which unchecked work items have accepted scope, owners, and completion evidence?**

The list proposes central monitoring, Spring Boot 4.0.6, property migration, and removal of account-password login.

Type: `decision`. Current owner: `unknown`.
Consequence: Unchecked proposals cannot establish current versions or enabled login methods.
Sources:

- [KT-architecture-evolution](../../knowledge/candidates/evolution/KT-architecture-evolution.md#unchecked-future-work-list)
- [Markets Operation One TODO List](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operation One TODO List/page.md#L1-L4>)

Answer guidance: Mark each item proposed, approved, completed, deferred, or rejected. Supply the applicable owner and change or release reference.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-15

**Which environment and rendered ingress configuration establish the reported DNS-to-Nginx-to-Gateway route?**

The user already supplied the logical topology. Local Nginx templates also contain direct proxy exceptions.

Type: `evidence`. Current owner: `unknown`.
Consequence: The reported route cannot establish universal gateway traversal in a deployed environment.
Sources:

- [ARC-portal-service-relationships](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#http-and-token-interfaces)
- [ARC-portal-service-relationships](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#evidence-limits)
- [ratan_servers.conf](../../repos/infra/nginx/ratan_servers.conf.j2#L150-L256)

Answer guidance: Identify the environment and rendered configuration or responsible contact. Gateway implementation analysis remains excluded.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-16

**Which Auth Server revision implements the reported Entra SPN and EMS3 delegation?**

The user already stated Auth Server responsibilities. The supplied copy lacks identified Entra SPN and EMS3 paths.

Type: `evidence`. Current owner: `unknown`.
Consequence: Reported delegation cannot be bound to this local Auth implementation.
Sources:

- [ARC-portal-service-relationships](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#ratan-authentication-and-authorization)
- [source-review](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json)

Answer guidance: Provide the applicable repository, branch, artifact, or owner contact. Existing BFF Entra and EMS3 dependencies remain recorded.

Answer:

Status: `UNANSWERED`.

### KQ-ARCH-17

**What does BFF health management cover, and which interface represents that responsibility?**

The user reported health management. Admin controllers exist, but no dedicated health-management controller was identified.

Type: `decision`. Current owner: `unknown`.
Consequence: The reported responsibility lacks an exact interface mapping.
Sources:

- [ARC-portal-service-relationships](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#backend-and-infrastructure-roles)
- [ARC-portal-service-relationships](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#evidence-limits)
- [user-message](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L16-L22)

Answer guidance: Define the term or identify the endpoint, service, or operational function. Correct the term if health management meant administration.

Answer:

Status: `UNANSWERED`.

## Administration and onboarding

### KQ-OPS-001

**Which onboarding and administration procedures apply in each current environment?**

Retained sources describe proposals, a later manual, and environment-specific promotion steps. Current applicability remains unconfirmed.

Type: `decision`. Current owner: `unknown`.
Consequence: Teams could follow obsolete onboarding or administration steps.
Sources:

- [Admin Module](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md#L9-L16>)
- [Admin Module Release Flow](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L17>)

Answer:

Status: `UNANSWERED`.

### KQ-OPS-002

**Which tenant records may each maker, checker, and administrator read or change?**

The proposal separates tenant records. The manual requires different maker and checker users but lists shared administration subjects.

Type: `decision`. Current owner: `unknown`.
Consequence: Tenant isolation and authorization acceptance remain undefined.
Sources:

- [Admin Module](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md#L28-L33>)
- [User Manual](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md#L19-L35>)

Answer:

Status: `UNANSWERED`.

### KQ-OPS-003

**Which approval, audit, rollback, and emergency controls apply to self-service configuration changes?**

The overview proposes avoiding repeated change requests. The later release guide still requires tenant change and pipeline records.

Type: `decision`. Current owner: `unknown`.
Consequence: Configuration changes could bypass applicable production controls.
Sources:

- [Admin Module](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md#L9-L18>)
- [Admin Module Release Flow](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L17>)

Answer:

Status: `UNANSWERED`.

### KQ-OPS-004

**Which deployed BFF artifact and migration history establish the catalog schema in each environment?**

Retained schema drafts and Flyway SQL describe persistence relationships. They do not identify the active schema.

Type: `evidence`. Current owner: `unknown`.
Consequence: Schema-dependent administration and migration claims remain unverified.
Sources:

- [Flywaydb](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md#L77-L99>)
- [Admin Module](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md#L41-L45>)

Answer:

Status: `UNANSWERED`.

### KQ-OPS-006

**For SSDR users without required entitlements, should onboarding add EMS2 grants or use an explicit delegation arrangement?**

The discussion lists both alternatives. Its guest-access proposal is struck through. The selected general portal-entry denial remains applicable.

Type: `decision`. Current owner: `unknown`.
Consequence: SSDR access cannot use an assumed portal-entry exception or delegation bypass.
Sources:

- [SSDR On Board Discussion](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L27-L37>)
- [SSDR On Board Discussion](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L63-L69>)

Answer:

Status: `UNANSWERED`.

## Release operations

### KQ-REL-001

**Which production release duration applies: 10 hours, 24 hours, or another stated duration?**

The proposal summary states 24 hours. Its detailed schedule states 09:00–19:00 SGT and 10 hours.

Type: `decision`. Current owner: `unknown`.
Consequence: Release occupancy, support coverage, and rollback planning remain uncertain.
Sources:

- [Markets Operations One Release](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L13-L19>)
- [Markets Operations One Release](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L44-L54>)

Answer:

Status: `UNANSWERED`.

### KQ-REL-002

**Must every urgent-release stakeholder confirm explicitly, or may silence permit release?**

The same proposal requires all confirmations and also says releases proceed when nobody raises concerns.

Type: `decision`. Current owner: `unknown`.
Consequence: Urgent-release authorization remains ambiguous.
Sources:

- [Markets Operations One Release](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L144-L151>)

Answer:

Status: `UNANSWERED`.

### KQ-REL-003

**Which checklist, release-window rules, and deployment workflow currently govern each environment?**

The checklist is unfinished. Retained guides describe differing procedures, cut-offs, lead times, freeze exceptions, and deployment mechanisms.

Type: `decision`. Current owner: `unknown`.
Consequence: Teams cannot select a governing release procedure or complete its required gates.
Sources:

- [Admin Module Release Checklist Template](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L1-L29>)
- [Markets Operations One Release](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L44-L115>)
- [Admin Module Release Flow](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L17>)

Answer:

Status: `UNANSWERED`.

### KQ-REL-004

**Does FMAA remain supported for configuration uploads? If replacement is planned, which method and migration date apply?**

The upload procedure requires FMAA JWT validation. The checklist separately warns that FMAA decommissioning is planned.

Type: `decision`. Current owner: `unknown`.
Consequence: Configuration promotion could lose its documented authentication dependency.
Sources:

- [Admin Module Release Flow](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L19-L24>)
- [Admin Module Release Checklist Template](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L16>)

Answer:

Status: `UNANSWERED`.

### KQ-REL-005

**Which records separately establish technical deployment, business validation, and business activation for each supported tenant?**

Calendars and requests separate those milestones. Planned dates do not prove completion or acceptance.

Type: `evidence`. Current owner: `unknown`.
Consequence: Technical deployment could be mistaken for business availability.
Sources:

- [Markets Operations One Release](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L79-L98>)
- [Admin Module Release Flow](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L3-L17>)
- [Ratan OpenFin Briefing](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L157-L163>)

Answer:

Status: `UNANSWERED`.

### KQ-REL-006

**Which tenant requests and readiness records define accepted capability scope and completed release gates?**

Retained requests include pending or withdrawn sign-off, connectivity, user profiles, and production verification references.

Type: `evidence`. Current owner: `unknown`.
Consequence: Tenant capability scope and release readiness remain unsupported.
Sources:

- [Admin Module Release Checklist Template](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L15-L29>)
- [Markets Operations One Release](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L85-L98>)

Answer:

Status: `UNANSWERED`.

## Application interoperability

### KQ-INT-001

**For each interoperability feature, which caller and provider teams own delivery, and which readiness gates must both meet?**

The cooperation guide requires provider registration, context agreement, authorization, testing, and deployment. Caller completion alone is insufficient.

Type: `decision`. Current owner: `unknown`.
Consequence: A caller feature could be enabled before the receiving application is ready.
Sources:

- [Interoperability Guide](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L27-L60>)

Answer:

Status: `UNANSWERED`.

### KQ-INT-002

**Which OpenFin and FDC3 features are delivered in each environment, with dated technical and business milestones?**

Sources mix POC demonstrations, planned phases, and reported approval claims. The briefing phase table omits its year.

Type: `evidence`. Current owner: `unknown`.
Consequence: Planned interoperability could be mistaken for supported deployed functionality.
Sources:

- [Ratan OpenFin Briefing](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L135-L163>)

Answer:

Status: `UNANSWERED`.

### KQ-INT-003

**Which versioned intent names, context schemas, payload fields, and responses form the current integration contract?**

The table uses fmchannel.fmoportal, while a launch example declares OpenTile. Development examples in the cooperation guide are empty.

Type: `decision`. Current owner: `unknown`.
Consequence: Caller and provider messages could be incompatible or unhandled.
Sources:

- [4. FMO Portal FDC3 Contract](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1-L5>)
- [4. FMO Portal FDC3 Contract](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L43-L49>)
- [Interoperability Guide](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L13-L25>)

Answer:

Status: `UNANSWERED`.

### KQ-INT-004

**Which production authentication handoff and token transport apply when one application launches another?**

The POC places provider tokens in launch URLs. It does not establish the current production handoff.

Type: `decision`. Current owner: `unknown`.
Consequence: Authentication trust boundaries and accepted credential transport remain undefined.
Sources:

- [3. Application Interoperability](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/3. Application Interoperability/page.md#L1-L23>)
- [4. FMO Portal FDC3 Contract](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L16-L20>)

Answer:

Status: `UNANSWERED`.

### KQ-INT-005

**Which OpenFin runtime and FDC3 library combinations are supported in each environment?**

The POC reports isolated broadcasts and an intent workaround across two libraries. Historical library choices do not establish current support.

Type: `decision`. Current owner: `unknown`.
Consequence: Compatibility expectations remain undefined.
Sources:

- [5. Technical Issue](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L1-L29>)
- [Ratan OpenFin Briefing](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L32-L86>)

Answer:

Status: `UNANSWERED`.

### KQ-INT-006

**Which retained tests establish cross-library broadcasts, intent handling, authorization, and target application outcomes?**

The supplied POC lacks its referenced screenshots and source archives. The retained POC sources supply no matching end-to-end execution evidence.

Type: `evidence`. Current owner: `unknown`.
Consequence: Supported interoperability combinations lack assertion-bearing execution evidence.
Sources:

- [5. Technical Issue](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L8-L29>)
- [Interoperability Guide](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L40-L54>)

Answer:

Status: `UNANSWERED`.

## Observability and performance

### KQ-OBS-001

**Is the supported analytics custom-attribute limit 10, 20, or another stated number?**

AnalyticsData declares 20 attributes. AnalyticsType and the explanatory prose define 10. Producer, transport, and storage agreement remains unconfirmed.

Type: `decision`. Current owner: `unknown`.
Consequence: Analytics attributes could be omitted or rejected.
Sources:

- [Design](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L55-L114>)

Answer:

Status: `UNANSWERED`.

### KQ-OBS-002

**Which measurable response-time, capacity, availability, browser, CPU, and memory limits apply to current supported workloads?**

The May 2023 document provides draft targets. Its limits do not establish accepted current nonfunctional requirements.

Type: `decision`. Current owner: `unknown`.
Consequence: Performance and capacity results cannot receive business acceptance.
Sources:

- [FMO Post Trade Portal Frontend Performance Testing May 2023](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L68-L89>)

Answer:

Status: `UNANSWERED`.

### KQ-OBS-003

**Which dated workload and execution records establish current response time and capacity?**

Historical reports omit their referenced measurement captures and result archives. Their summaries do not establish present capacity.

Type: `evidence`. Current owner: `unknown`.
Consequence: Current sizing and response-time claims remain unverified.
Sources:

- [Throughput Testing in UAT](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Throughput Testing in UAT/page.md#L11-L44>)
- [FMO Post Trade Portal Frontend Performance Testing May 2023](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L230-L256>)

Answer:

Status: `UNANSWERED`.

### KQ-OBS-004

**Which deployed cache headers, entry revalidation rules, asset names, and expiry values apply in each environment?**

The design specifies entry revalidation and 120-day static caching. Its Implementation section supplies no configuration.

Type: `evidence`. Current owner: `unknown`.
Consequence: Update detection and cache freshness cannot be confirmed for active deployments.
Sources:

- [MFE Cache Strategy](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L7-L15>)
- [MFE Cache Strategy](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L33-L45>)

Answer:

Status: `UNANSWERED`.

### KQ-OBS-005

**Which identity and search fields may analytics collect, who may read them, and how long may records remain?**

Examples capture identity context and search values. The bounded sources provide no accepted field-access or retention rules.

Type: `decision`. Current owner: `unknown`.
Consequence: Analytics collection, access, and retention boundaries remain undefined.
Sources:

- [Design](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L43-L47>)
- [Design](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L88-L114>)

Answer:

Status: `UNANSWERED`.

### KQ-OBS-006

**Where are production dashboards, who operates them, and which event completeness checks are required?**

The supplied production dashboard address is a placeholder. Reported dashboard counts do not prove active observation coverage.

Type: `evidence`. Current owner: `unknown`.
Consequence: Production analytics availability and operational ownership remain unconfirmed.
Sources:

- [Analytic Dashboard in Kibana](<../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Analytic Dashboard in Kibana/page.md#L11-L17>)

Answer:

Status: `UNANSWERED`.

## Agent evidence follow-up

These are my follow-up tasks. Supply evidence locations through the linked questions when available.

| Follow-up | Basis and limit | Source |
| --- | --- | --- |
| Inspect deployed parser and browser state against login-mode expectations. | Do not ask the user to repeat local parser inspection. Obtain applicable deployment identity first. | [Evidence](../../knowledge/candidates/security/KT-authentication-and-sessions.md#evidence-limits) |
| Bind UAT configuration, token lifetimes, property origin, clocks, and exact artifacts. | The screenshot arithmetic and local 15-versus-480 configuration comparison are already complete. | [Evidence](../portal-background-session-20261019/10-change-review.md#uat-timeout-inquiry-21-october-2026) |
| Reproduce refresh-token reuse before and after blacklist cleanup once current bindings and required revocation scope are known. | The governance finding records a historical inference, not a deployed defect. | [Evidence](../../evidence/knowledge/findings/GF-refresh-revocation-scope.md#proposed-action) |
| Reconcile historical session-verification finding with newer retained tests before closure. | Missing local Jest dependencies are historical; current local test evidence exists. UAT parity remains unverified. | [Evidence](../../evidence/knowledge/findings/GF-session-renewal-verification-gates.md#evidence) |
| Address demonstrated active-cutoff and stale-credential conditions within authorized implementation scope. | They are existing implementation findings. They do not require inventing a new business rule. | [Evidence](../portal-background-session-20261019/07-code-review-minor-20261021.md#review-findings) |

## Request and source facts

The user requested one answer document and repeated review until no question remains.
The [exact instruction](evidence/clarification-20261022/batched-question-workflow-source.json) is retained.
The [existing task intake](01-intake.md) and [evidence index](evidence/index.md) retain the owning business scope.

## Proposed change

This document replaces separate chat questions with one living answer and review record.
It changes no business rule before the user supplies an answer.

## Scope and affected artifacts

The [source map](evidence/question-batch-20261022/source-map.json) records all 11 domain records, question origins, exact versions, and hashes.
The scope includes current policy, authority, deployment bindings, supported contracts, and material evidence gaps.
Risk: Low for runtime behavior. Incorrect interpretation could change knowledge meaning, so returned answers retain their exact source bytes.

## Options and consequences

The user selected batched document review. Serial chat questioning is superseded for this clarification scope.
Unknown or unsupported items remain explicit. They do not become invented rules or verified deployments.

## Proposed acceptance and validation

Every original open question must map to a stable question ID or a supported known answer.
Each published claim must identify its scope, answer source, applicable review, and remaining evidence limits.
Publication checks cover the actual final record bytes.
The [check receipt](evidence/question-batch-20261022/checks.json) records document, coverage, link, and preservation checks.

## Implementation and release proposal

This stage prepares questions and records the answer workflow. It proposes no application implementation or release.

## Requested decision and actual disposition

Complete the unanswered fields, including shared review identity and scope.
The batching workflow is authorized. No answer to an unresolved domain question is inferred.

## Sources and evidence limits

The inventory was inspected at Git revision `231f3d02a246a1d16814833173375dad789e6fcb`.
All 48 frontmatter questions are mapped. Additional questions come from inspected current task and architecture limits.
The source map records exact source hashes. It does not establish deployment parity or reviewer authority.
No external system, browser behavior, or business scenario ran during this document preparation.

Automated checks do not establish complete ASD-STE100 compliance.

## Unknowns and blockers

Unanswered policy questions block only their affected knowledge decisions.
Missing deployment and execution evidence limits behavior verification separately.
No unknown topic owner is replaced by the portal team without an explicit applicable answer.
Next action: The user completes this file. I then review its returned bytes and refine the affected knowledge.
