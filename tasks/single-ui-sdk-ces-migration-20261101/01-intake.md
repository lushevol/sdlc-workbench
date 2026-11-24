---
artifact_kind: requirement
id: REQ-SINGLE-UI-CES-001
version: 1
status: draft
owner: unknown
source_refs: [SRC-USER-001, SRC-INTENT-001, SRC-SDK-001, SRC-CES-001, SRC-CONSUMERS-001, SRC-API-001]
related_ids: [CES-MIGRATION]
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
    - Source inspection does not establish deployment, permission equivalence, or passing business execution.
---

# Update the Single UI SDK from EMS2 to CES

> **Replace the EMS2 client and resolve the SDK output contract before implementation.**
> Action: select the role-compatible or effective-permission approach in [SDK-Q1](#sdk-q1).
> Consequence: the aggregate CES response cannot reproduce each role's grants by itself.
> Owner: unknown. Evidence: [SDK output](evidence/sdk-scope.md#current-call-and-data-path) and [CES mapping limits](evidence/ces-reference.md#mapping-references-and-their-limits).
>
> **Bind the supported SDK artifact before upgrading consumers.**
> Action: resolve [SDK-Q2](#sdk-q2) and compile each actual consumer.
> Consequence: Auth Server's static token-validator calls conflict with this checkout's instance API.
> Owner: unknown. Evidence: [consumer findings](evidence/consumer-scope.md#confirmed-consumers-and-compatibility).

## Current task state

Assessment: Codex, 1 November 2026, Asia/Singapore.
Source assessment is complete. Application implementation, Java builds, live CES checks, and business acceptance are not complete.
The [evidence index](evidence/index.md) links the source identities and validation results.

## Description

The [user request](evidence/user-input.md) asks how to migrate `repos/libraries/single-ui-sdk-starter` from EMS2 to CES.
The change belongs in the SDK's direct entitlement lookup and its consumer configuration.
The JWT filter does not invoke that lookup.
A BFF or Auth Service CES setting therefore cannot migrate this SDK automatically.
Evidence: [lookup and filter boundaries](evidence/sdk-scope.md#jwt-and-filter-boundary).

### Recommended technical direction

Replace both EMS2 requests with a CES client and explicit response normalization.
Use the existing Auth Service and BFF as transport references.
Keep project application identities and mappings in configuration.
Choose the public output approach after inspecting actual consumers in [SDK-Q1](#sdk-q1).

The inspected reference request is:

```http
GET /fmces/v1/entitlement/app/51358/RATAN_ENTITLEMENT_RULE/user/{userId}
Authorization: Bearer <FMAA service token>
```

The SDK currently performs these requests:

```http
GET /ems2/rest/account/{userId}
POST /ems2/rest/entitlements/entitlementList
```

Sources: [SDK requests](evidence/sdk-scope.md#current-call-and-data-path) and [CES request implementation](evidence/ces-reference.md#transport-and-authentication).
The incoming Single UI JWT and outbound FMAA token serve different purposes.

### Files and behavior to update

| Order | File or boundary | Proposed change | Completion evidence |
| --- | --- | --- | --- |
| 1 | [SDK version and consumers](evidence/consumer-scope.md#confirmed-consumers-and-compatibility) | Select the supported Java/Spring line and release version. Record direct-lookup and entitlement-token consumers. | Exact artifact inventory and consumer compilation. |
| 2 | [AuthProperties.java](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java#L26) | Add CES URL and application selectors. Replace EMS2 entity filters with reviewed application/feature scopes. | Configuration binding and invalid-configuration assertions. |
| 3 | New CES transport DTOs and client | Model the array response, `user_data`, and separate functional/data sections. Add an injectable FMAA token provider. | Requested user/application validation and outbound header assertions. |
| 4 | [AuthConfiguration.java](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java#L39) | Wire the CES implementation and token provider. Preserve bounded connect/read timeouts. | Spring context starts with the supported consumer runtime. |
| 5 | [AuthorizationImpl.java](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L30) | Replace account parsing, composite-ID splitting, and entitlement-list POST. Remove numeric role/subject joins from the CES path. | Reviewed grant projection and zero outbound EMS2 requests. |
| 6 | [AuthorizationService.java](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java#L5) | Preserve the existing signature only with a supported semantic mapping. Otherwise introduce a versioned effective-permission API. | Consumer contract review and permitted/denied action assertions. |
| 7 | [Failure handling](evidence/sdk-scope.md#failure-and-compatibility-boundaries) | Distinguish no grants from upstream failure. Define denial, retry, and cache behavior through the service contract. | Malformed-response, unavailable-service, and denied-access assertions. |
| 8 | SDK tests, packaging, and consumers | Add the missing tests. Publish one explicit SDK version and update actual consumers. | Complete applicable unit suites pass, with zero failures and runner errors. |
| 9 | Final configuration | Remove unused EMS2 client settings and DTOs after supported consumers close. | Static inventory and runtime evidence establish CES-only SDK operation. |

These are assessment recommendations. They do not approve unresolved product behavior or deployment.
Each implementation owner remains unknown until assigned.

Proposed configuration shape follows. These CES property names do not exist in the current SDK.
The application selectors belong in this project's configuration, rather than library defaults.

```yaml
fmoportal:
  auth:
    ces:
      base-url: ${CES_BASE_URL}
      app-id: "51358"
      app-name: RATAN_ENTITLEMENT_RULE
```

Use a host-provided service-token interface where feasible.
Do not copy Auth Service Redis internals or token logging into the SDK.
The [reference analysis](evidence/ces-reference.md#transport-and-authentication) explains these reuse limits.

## Rationale

The SDK consumes EMS2-specific DTOs and composite numeric identities.
CES returns a different permission model and requires outbound service authentication.
A host or endpoint substitution cannot satisfy those contracts.
Confidence: HIGH for inspected source. No live migration failure was reproduced.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| SDK lookup, normalization, properties, wiring, token compatibility, consumers, and verification gaps. | Application edits, artifact publication, deployment, and live entitlement changes. | This request asks for an update assessment. |
| Existing Auth and BFF CES code as reference. | Treating that code as approved mappings or deployed behavior. | Local implementation provides source evidence only. |

### Entry route and evidence state

Entry procedure: [lifecycle routes](../README.md#lifecycle-entry-routes).
Route: requirements first, with existing implementation inspected as evidence.
Registration date: 1 November 2026. No retrospective implementation approval is inferred.
SDK baseline: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`, dated 14 October 2026; checkout clean.
Auth baseline: `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`; BFF baseline: `134a340472f29d2a4136e07e516690de6a18e323`.
Both reference commits are dated 30 October 2026. Their checkouts were clean.
Exact source hashes are in the [source manifest](evidence/source-manifest.json).
Bounded coding exploration is not applicable. No experiment or product code was written.
Investigation stop condition: save the edit map, compatibility decisions, and evidence limits.

| Dimension | Current state and evidence |
| --- | --- |
| Implementation | SDK remains EMS2-only. Auth and BFF contain local CES clients. |
| Intent review | User requests migration analysis. Earlier migration inputs establish the final zero-EMS2 objective. Detailed SDK semantics remain open. |
| Execution outcome | NOT_RUN for Java compilation, unit tests, live CES, and business behavior. |
| Business acceptance | Pending. No acceptance or deployment approval is recorded. |

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Migration assessment handoff | READY | Source supports the edit map. Unresolved decisions are explicit. | None for this assessment. | Codex; deliver this account. |
| Product implementation | NEEDS_CLARIFICATION | Output contract, consumer runtime, and service failure policy need resolution. | Finalize product behavior and implement the migration. | unknown; resolve [SDK-Q1](#sdk-q1), [SDK-Q2](#sdk-q2), and [SDK-Q3](#sdk-q3). |

- Expected behavior authority: [current request](evidence/user-input.md) and [earlier migration intent](../ces-entitlement-migration-20261102/01-intake.md#description).
- Existing authorization: source inspection and migration assessment.
- Evidence index: [retained evidence](evidence/index.md).
- Business review: pending. Readiness does not establish approval or verified behavior.

### Qualitative risk and priority

Permission mapping has consequential access risks. Incorrect mapping can remove grants or assign them to incorrect scopes.
This assessment establishes no deployed permission failure, session disruption, or forced logout.
Retain these findings as implementation preconditions. They are not demonstrated production incidents or release blockers.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| SDK maintainer | Final migration objective | SDK performs migrated authorization. | Use CES without EMS2 runtime requests. | [Earlier final objective](../ces-entitlement-migration-20261102/01-intake.md#mig-ac-001). |
| Application maintainer | Application rename | Existing scope is EMS2 `X_RATANONE`. | Use CES application `RATAN_ENTITLEMENT_RULE`. | [Exact user clarification](../ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt). |
| Application maintainer | Feature consolidation | Existing scopes include `RATAN_FUNC` or `RATAN_DATA_ENTITLEMENT`. | Configure them as features under the same CES application. | [Exact user clarification](../ces-entitlement-migration-20261102/evidence/user-input-20261030-api-samples-and-feature-consolidation.txt). |

### Old and new representation

| Boundary | Old SDK source behavior | CES source/sample behavior | Intended SDK treatment |
| --- | --- | --- | --- |
| Account lookup | Parse `entitlementTypes[].uniqueName` into entity and role identities. | Effective endpoint provides `user_data` and `entitlements`. | Replace transport and identity validation. Full account metadata is unused by this SDK. |
| Scope | Filter EMS2 entity names. | Request application ID/name, then receive feature/action pairs. | Apply reviewed application and feature scopes. Preserve other applications' isolation. |
| Permission output | `entityName:roleName -> subjectName -> [actionName]`. | `entitlement_name[]` plus merged `role_entitlements[]`. | Resolve [SDK-Q1](#sdk-q1). Do not assign all merged grants to every role. |
| Names | Subject and action names come from EMS2 objects. | Feature and action names come from CES pairs. | Map feature to subject and action to action within reviewed scope. |
| IDs | Internal joins use numeric role and subject IDs. | Aggregate endpoint omits those IDs and pair-to-role links. | Remove numeric joins. Do not fabricate equivalent IDs. |
| Data | Legacy data scope can appear as an EMS2 entity/role. | CES separates profiles, policies, and `data_entitlements`. | Map only required data behavior. Preserve alphanumeric filter values as strings. |
| Authentication | Filter validates JWTs and publishes `userInfo`. | CES authenticates service requests with FMAA. | Keep these credential and responsibility boundaries separate. |

Sources: [SDK findings](evidence/sdk-scope.md), [CES findings](evidence/ces-reference.md), and [raw sample](../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json).
The [sample facts](evidence/api-shape.json) record hashes and JSON pointers.
These comparisons describe source and sample behavior. They are not old/new execution results.

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| CES-MIGRATION | Parent migration context. | [Existing intake](../ces-entitlement-migration-20261102/01-intake.md). | SDK completion cannot close unrelated Auth data-role dependencies. |
| single-ui-auth-sdk | Owning library. | [SDK identity](evidence/sdk-scope.md#source-identity-and-limits). | Actual released artifacts and deployed consumers remain unbound. |
| ratan-auth-server | Declares SDK dependency `1.1.1`. | [Consumer source](evidence/consumer-scope.md#confirmed-consumers-and-compatibility). | Source checkout is `2.0.0-SNAPSHOT`; static versus instance validator usage needs compatibility work. |
| single-ui-bff | Issues SDK-consumed tokens and supplies CES transport reference. | [Token contracts](evidence/consumer-scope.md#public-contracts-that-the-migration-must-assess). | BFF normalization omits per-role provenance; it is not a complete SDK adapter. |
| CES and FMAA | Supply effective grants and service authentication. | [Reference client](evidence/ces-reference.md#transport-and-authentication). | Credentials, trust, supported errors, and operational policy need environment evidence. |

## Acceptance criteria

### SDK-AC-001

This draft criterion applies the existing final migration objective to SDK entitlement retrieval.
It is not a complete product acceptance inventory. Contract-preservation criteria depend on [SDK-Q1](#sdk-q1).

```gherkin
@REQ-SINGLE-UI-CES-001
Feature: Remove SDK runtime dependence on EMS2
  @SDK-AC-001
  Scenario: Read entitlements after CES cutover
    Given the SDK uses the final CES configuration
    And CES returns valid entitlements for the requested user and application
    When an application requests that user's entitlements through the SDK
    Then the SDK makes 0 requests to EMS2
```

```yaml
acceptance_criteria:
  - id: SDK-AC-001
    given: Given the SDK uses final CES configuration and CES returns valid entitlements for the requested user and application
    when: When an application requests that user's entitlements through the SDK
    then: Then the SDK makes 0 requests to EMS2
    measure:
      metric: outbound EMS2 request count
      operator: equals
      value: 0
      unit: requests
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| [SDK-AC-001](#sdk-ac-001) | Record outbound destinations during lookup. | Exact SDK candidate, final CES settings, and a reviewed fixture. | One lookup; no load threshold is specified. | Candidate identity, request capture, explicit zero-request assertion, and result. Currently unavailable. |

Future verification must cover scope isolation, permission equivalence, denied actions, multiple roles, and functional/data separation.
It must also cover no grants, malformed responses, CES failures, token expiry, token issuers, and consumer startup.
These are verification work areas. Canonical cases and assertions remain undefined until their contracts resolve.
No test case or execution is claimed from this list.

## Traceability

### AC to test coverage

| Criterion | Canonical case | Inspected SDK assertion | Execution |
| --- | --- | --- | --- |
| [SDK-AC-001](#sdk-ac-001) | Not defined. | None. No SDK tests were found. | NOT_RUN. |

Defined case links: 0/1 drafted ACs. Inspected SDK assertion links: 0/1. Passing executions: 0/1.
These denominators cover the single drafted criterion. The complete product AC inventory remains unresolved.

### AC to code-change coverage

| Criterion | Required existing path | Candidate code change | Conformance |
| --- | --- | --- | --- |
| [SDK-AC-001](#sdk-ac-001) | [Current EMS2 lookup](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L30). | None; assessment only. | Not assessed against a candidate. |

Candidate implementation links: 0/1 drafted ACs. No implementation equivalence percentage is claimed.

### Code-change to test coverage

| Changed business unit | Direct assertion chain | Retained execution |
| --- | --- | --- |
| None; no application changes. | Not applicable. | Not applicable. |

Denominator: 0 changed business units. Coverage is not applicable, rather than 100%.
Task documentation changes are supporting analysis. They do not implement the migration.

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SRC-USER-001 | [Current input](evidence/user-input.md). | 2026-11-01 message. | [Manifest](evidence/source-manifest.json). | User; assessment intent. | No detailed output policy. |
| SRC-INTENT-001 | [Rename](../ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt), [consolidation](../ces-entitlement-migration-20261102/evidence/user-input-20261030-api-samples-and-feature-consolidation.txt), and [final objective](../ces-entitlement-migration-20261102/01-intake.md#mig-ac-001). | Retained 30 October records. | [Manifest](evidence/source-manifest.json). | User statements; scope-specific intent. | Publication and deployment remain separate. |
| SRC-SDK-001 | [SDK account](evidence/sdk-scope.md). | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. | [Manifest](evidence/source-manifest.json). | Source owner unknown; implementation evidence. | No execution. |
| SRC-CES-001 | [CES reference](evidence/ces-reference.md). | Auth `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`; BFF `134a340472f29d2a4136e07e516690de6a18e323`. | [Manifest](evidence/source-manifest.json). | Source owners unknown; implementation evidence. | No approved SDK semantics or deployment proof. |
| SRC-CONSUMERS-001 | [Consumer scope](evidence/consumer-scope.md) and [source hashes](evidence/consumer-sources.json). | Exact revisions recorded in the manifest. | [Manifest](evidence/source-manifest.json). | Source owners unknown; dependency and assertion evidence. | Deployed inventory incomplete. |
| SRC-API-001 | [Effective CES response](../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json). | Capture time and environment unknown. | `871f59e5492605af54ab62cd9343f74c6bba24ef8df2298db59946a80cf11aaa`. | User-supplied sample. | Not an authoritative API or synchronized EMS2 comparison. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact; HIGH confidence | CES requires different transport, DTOs, and authentication. | [Inspected request code](evidence/ces-reference.md#transport-and-authentication). | Endpoint substitution is insufficient. | unknown | Implement a CES client after contract resolution. |
| Inference; HIGH confidence | Role-keyed compatibility cannot be reconstructed from merged pairs alone. | [Source and raw sample](evidence/ces-reference.md#mapping-references-and-their-limits). | Role checks can change meaning. | unknown | Resolve [SDK-Q1](#sdk-q1). |
| Fact; HIGH confidence | Auth requests SDK `1.1.1`; this source declares `2.0.0-SNAPSHOT`. | [Consumer evidence](evidence/consumer-scope.md#confirmed-consumers-and-compatibility). | Building this checkout cannot update existing consumers automatically. | unknown | Resolve [SDK-Q2](#sdk-q2). |
| Unknown | Deployed lookup consumers and runtime configuration are unavailable. | [Search scope](evidence/consumer-scope.md#scope-and-source-identities). | Release scope remains incomplete. | unknown | Bind deployment artifacts and grants before implementation acceptance. |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| [SDK knowledge candidate](../../knowledge/records/candidates/security/KT-sdk-and-entitlements.md#entitlement-retrieval-and-lifecycle). | Version 7; hash in source manifest. | Direct lookup and entitlement-token paths. | Historical guides and prior user answers; candidate status. | Actual supported artifacts and callers. |
| [Earlier migration intake](../ces-entitlement-migration-20261102/01-intake.md#description) and exact linked user inputs. | Hashes in source manifest. | Final objective, rename, and feature consolidation. | User-stated intent; deployment unverified. | Detailed SDK contract. |
| SDK, Auth, BFF, and test sources. | Exact revisions and hashes in manifests. | [SDK-AC-001](#sdk-ac-001) and affected interfaces. | Source/assertion inspection. No new business execution. | Candidate tests and retained results. |

### Answer and question log

The application rename and feature consolidation are answered above. They are not repeated as open questions.
The following choices are proposals. No business answer is selected.

#### SDK-Q1

The current method preserves role-specific map keys.
The aggregate endpoint returns merged permission pairs without pair-to-role provenance.
Confidence: HIGH for this structural gap. See [mapping evidence](evidence/ces-reference.md#mapping-references-and-their-limits).

Question: Must existing callers retain role-specific results, or can they consume effective feature/action permissions?

Proposed choices: retain role attribution using a supported detail contract and reviewed mapping; introduce a versioned effective-permission API; another answer; unknown; name a contact.

Answer:

Owner: unknown. Consequence: public output implementation remains blocked.
Next action: inspect caller assertions and record the required contract before coding.
If callers only need effective grants, the versioned API avoids fabricated role attribution.

#### SDK-Q2

The only locally declared SDK dependency is Auth Server `1.1.1`.
Its two static validator calls differ from this checkout's instance method.
Confidence: HIGH for source declarations; deployed artifact confidence is UNKNOWN.
See [compatibility evidence](evidence/consumer-scope.md#confirmed-consumers-and-compatibility).

Question: Which released SDK version, Java/Spring runtime, and applications must this migration support?

Proposed choices: migrate the supplied Boot 4 line and update consumers; maintain the actual deployed SDK line; another answer; unknown; name a contact.

Answer:

Owner: unknown. Consequence: package and consumer implementation scope remains blocked.
Next action: obtain dependency inventories and exact runtime versions.

#### SDK-Q3

CES transport code shows FMAA bearer authentication, but its callers use different empty-result and failure policies.
The current SDK returns an empty map after errors.
Confidence: HIGH for source behavior. Runtime and approved-policy confidence is UNKNOWN.
See [error differences](evidence/ces-reference.md#error-and-empty-result-behavior).

Question: Which existing contract governs token provision, no grants, CES failures, and cached permission freshness for SDK callers?

Proposed choices: link an approved contract; nominate SDK/CES/operations contacts; another answer; unknown.

Answer:

Owner: unknown. Consequence: failure and revocation behavior cannot be finalized.
Next action: reuse existing standards where available and define only missing behavior.
This specializes the [existing migration operational question](../ces-entitlement-migration-20261102/01-intake.md#mig-q5).

### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| SDK assessment | SDK knowledge candidate version 7; existing CES migration records. | No new business clarification was received. Existing rename and consolidation answers were reused. | Not applicable; this stage adds source analysis only. | No governance transition. Existing sources and audit history remain unchanged. | Existing candidates remain unpublished; unknown; apply future answers through governance. |

### Intake investigation plan

- Completed: inspect SDK, callers, imports, transport references, retained API samples, prior intent, and selected test assertions.
- Evidence needed for implementation: resolved output contract, supported artifact/runtime inventory, and applicable operational contract.
- Method and controls: direct source inspection at exact revisions; no graph completeness or deployment inference.
- Retention: this task's [evidence index](evidence/index.md), source manifests, and document checks.
- Next decision: resolve the three questions before product implementation. Reconcile source identities again at that stage.
