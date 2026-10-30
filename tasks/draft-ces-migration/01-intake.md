---
artifact_kind: requirement
id: CES-MIGRATION
version: 1
status: draft
owner: unknown
source_refs: [USER-20261030, CHATGPT-20261028-29, API-SAMPLES, BACKEND-SOURCE, FRONTEND-SOURCE, PRIOR-REVIEW]
related_ids: []
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
    - Source investigation does not establish business approval, deployment, or passing execution.
---

# EMS2 to CES migration: current understanding and questions

> **Complete remaining EMS2 dependencies before final cutover.**
> Action: replace Auth data-role reads and reconcile the deployed SDK and all consumers.
> Consequence: selecting `EMS3_ONLY` alone cannot satisfy the final migration objective.
> Owner: unknown. Evidence: [current backend source](evidence/backend-analysis-20261030.md#remaining-legacy-dependencies).
>
> **Confirm the current rollout baseline and mappings before implementation planning.**
> Action: answer the [migration question batch](#answer-and-question-log), or identify the responsible contacts.
> Consequence: the complete implementation scope and verification workload remain unresolved.
> Owner: unknown. Evidence: [source limits](#evidence-and-open-questions).

Assessment date: 30 October 2026, Asia/Singapore. Assessor: Codex.
This is the living intake and single migration question document.
The [evidence index](evidence/index.md) links exact captures and source manifests.

## Description

Migrate RATAN from EMS2 to CES, also called EMS3.
Cover human users, tiles, functional permissions, data permissions, service accounts, and direct or indirect dependencies.
The final state requires zero EMS2 runtime dependencies across RATAN.
Legacy field names can remain when CES supplies their reviewed business meaning.
Sources: [current request](evidence/user-input-20261030-migration-plan.txt) and [historical user statements](evidence/historical-user-inputs-20261028-29.json).

The user requests an evidence-based migration account and meaningful remaining questions.
This stage changes task documents and evidence only.

## Rationale

This migration changes authorization providers and permission representations across multiple system boundaries.
A host change alone cannot establish equivalent access.
Account synchronization, entitlement provisioning, role assignments, application changes, verification, and release approval require separate evidence.
Source: [recovered conversation](evidence/chatgpt-conversation-20261030.json), particularly user turn `4ca9129d-15cf-4f08-a5d9-76052c0b0741`.

## Scope

| Track | Required migration coverage | Source and limit |
| --- | --- | --- |
| Human access | Portal entry, tile visibility, launch, actions, admin roles, and business data scope. | [Historical intent](evidence/historical-user-inputs-20261028-29.json); complete application inventory unavailable. |
| Service authorization | Internal, upstream, and downstream service accounts calling RATAN APIs. | [Historical intent](evidence/historical-user-inputs-20261028-29.json); complete consumer inventory unavailable. |
| Shared dependencies | Auth SDKs, shared UI helpers, caches, configuration, proxies, and operational procedures. | [Backend investigation](evidence/backend-analysis-20261030.md) and [frontend investigation](evidence/frontend-analysis-20261030.md). |
| Current authorized work | Inspect sources, explain changes, retain evidence, and prepare questions. | [Current request](evidence/user-input-20261030-migration-plan.txt). |

### Entry route and evidence state

Entry procedure: [lifecycle routes](../README.md#lifecycle-entry-routes).
Entry route: requirements first, with existing implementation and prior review supplied as investigation evidence.
Task registration: 30 October 2026. Earlier implementation dates retain their actual identities.

| Dimension | Current state and evidence |
| --- | --- |
| Implementation | Local Auth and BFF commits named `CES Migration`, dated 30 October. See [exact identities](evidence/backend-analysis-20261030.md#scope-and-source-identity). |
| Intent review | High-priority user statements establish final zero-EMS2 scope. Detailed mappings and product criteria remain incomplete. |
| Execution outcome | NOT_RUN for this investigation. Source assertions were inspected. |
| Business acceptance | Pending. No migration acceptance or deployment authorization was supplied. |

Auth head: `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2`, 30 October, 07:49:37 Singapore time.
BFF head: `134a340472f29d2a4136e07e516690de6a18e323`, 30 October, 07:52:24 Singapore time.
The inspected SDK head is `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`, dated 14 October.
Frontend and filesystem identities appear in the [frontend manifest](evidence/frontend-sources-20261030.json).
Existing frontend and test-engine local changes remain preserved.

Bounded coding exploration: not applicable. No application implementation or live business execution was authorized by this analysis request.
Investigation stop condition: save the sourced migration account and remaining question batch.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Migration understanding handoff | READY | Sources support this account. Unknowns remain explicit. | None for this document handoff. | Codex; deliver account and questions. |
| Complete implementation plan | NEEDS_CLARIFICATION | Approved mappings, complete inventory, deployed versions, and operational limits remain incomplete. | Finalize implementation scope and acceptance workload. | unknown; resolve [question batch](#answer-and-question-log). |

- Expected behavior authority: [current request](evidence/user-input-20261030-migration-plan.txt) and [historical user inputs](evidence/historical-user-inputs-20261028-29.json).
- Existing authorization: source investigation, migration explanation, and task evidence retention.
- Evidence index: [task evidence](evidence/index.md).
- Business review: pending. Readiness does not grant approval.

### Working milestone baseline

The latest assistant guide uses the dates below.
They remain planning targets, not current approvals or deployment evidence.
The user revised provisioning toward mid-November and requested UAT completion within a week.
Exact dates below need current confirmation in [MIG-Q1](#mig-q1).

| Milestone | Latest recovered plan | Authority and freshness limit |
| --- | --- | --- |
| DEV completion and smoke verification | User reported implementation completed in DEV; squads should verify core flows. | User statement, 29 October; no deployed artifacts inspected. |
| Business UAT and service integration sign-off | 6 November 2026. | Latest assistant draft translates the user's relative deadline. |
| CES production accounts, entitlements, and profiles | Mid-November; 13 November is proposed. | User requested mid-November. Exact CES CR schedule unavailable. |
| RATAN production cutover | 28 November 2026. | Repeated assistant draft target; direct current user date confirmation unavailable. |

Earlier assistant drafts used 18 November UAT and 25 November provisioning.
These conflict with the later working plan.
Sources: [raw exchanges](evidence/chatgpt-conversation-20261030.json), ordered by recorded timestamps.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Settlement, Trade Control, FlowZero | MIG-HUMAN | DEV and UAT verification. | Nominate contacts and accounts; verify workflows and provide business sign-off. | [User statements](evidence/historical-user-inputs-20261028-29.json), 28–29 October. |
| Integration owners | MIG-SERVICE | Service accounts call RATAN APIs. | Verify permitted and denied calls; provide integration sign-off. | [User statements](evidence/historical-user-inputs-20261028-29.json). |
| Tile owners | MIG-STAGED | Testing before final cutover. | Switch each tile independently between EMS2 and CES. | User turn `aa007a0a-cf55-4d71-9710-754a6abb00c1` in [capture](evidence/chatgpt-conversation-20261030.json). |
| RATAN migration owners | MIG-FINAL | Final November release. | Use CES for every tile and service authorization; remove remaining EMS2 dependencies. | Same [user turn](evidence/chatgpt-conversation-20261030.json). |
| Portal users | Existing entry rules | Entry and tile configuration checks. | Preserve recorded denial and empty-configuration behavior through reviewed CES mappings. | [Existing answered rules](evidence/frontend-analysis-20261030.md#existing-intended-rules-already-answered). |

Existing user answers already require entry denial without a registered application entitlement.
An unconfigured entity hides the tile and denies direct launch.
An empty subject permits access through one configured entitled entity.
These answers cover local, test, UAT, and production.
Multiple-entity semantics remain open. CES feature matching also needs explicit mapping review.
Source: [original answer locators](evidence/frontend-analysis-20261030.md#existing-intended-rules-already-answered).

## Dependencies

### Reported provisioning status

Confidence: HIGH that the user reported these states on 28 October.
Confidence in their current deployment status: UNKNOWN without CES CR or environment evidence.

| Asset | User-reported status | Remaining migration action |
| --- | --- | --- |
| Human accounts under `X_RATANONE` | Synchronized to UAT and production; incremental synchronization scheduled. | Verify representative assignments and current synchronization evidence. |
| `RATAN_DATA_ENTITLEMENTS` | In production. | Confirm profiles, user assignments, and effective data access. |
| `X_RATANONE` and `RATAN_FUNC` entitlements | Remaining production onboarding requires CES CRs. | Confirm CR contents, dates, and profile assignments. |
| Service authorization accounts | Available in UAT; production onboarding pending. | Confirm every service identity and production permission. |

Source: user turn `4ca9129d-15cf-4f08-a5d9-76052c0b0741` in [historical input](evidence/historical-user-inputs-20261028-29.json).
The EMS2 sample uses singular `RATAN_DATA_ENTITLEMENT`.
The user uses plural `RATAN_DATA_ENTITLEMENTS`.
Their identity mapping remains unconfirmed; neither spelling was silently corrected.

### Implemented migration mechanisms

Confidence: HIGH for exact local source, with deployment and execution limits.

| Boundary | Inspected implementation | Practical implication |
| --- | --- | --- |
| Auth full entitlements | Supports `EMS2_ONLY`, `EMS3_PRIMARY_DUAL_READ`, and `EMS3_ONLY`. CES uses app ID/name, user ID, and FMAA bearer authentication. | Dual read returns CES and compares EMS2 asynchronously. CES failure does not automatically select EMS2. |
| Auth projections | Converts CES features/actions into `feature:action`; system actions use `RATAN_FUNC:action:feature`. | Role mappings and action semantics need reviewed configuration. |
| Auth data roles | JWT conversion separately reads EMS2 account data in every migration mode. | Current local `EMS3_ONLY` retains an EMS2 dependency. |
| BFF tile routing | Stores source, app ID, app names, and app features. Groups CES requests by application. | Missing source defaults to EMS2. Existing tile records require explicit migration. |
| BFF visibility | Matches any configured feature, ignoring case. Stores per-tile grants and source-tagged subjects. | Tile visibility differs from business action and data authorization. |
| BFF persistence | Adds live and audit columns; handles CSV fields and preserves omitted settings during updates. | These areas changed since the 27 October review. Deployment history remains unbound. |
| Frontend | Consumes normalized entities, roles, subjects, actions, and token fields. Admin editors retain legacy fields. | Preserve or version the response contract and provide a supported CES configuration workflow. |
| Auth SDK | Inspected older source calls EMS2 account and entitlement endpoints. | Bind actual deployed SDK versions and migrate applicable consumers. |
| CES data cache | Auth fetches CES on cache miss and writes filter data. Reset endpoints exist. | Verify live ingestion, downstream enforcement, and revocation separately from Redis fixtures. |
| Infrastructure | CES Nginx routes exist in supplied configuration. | Templates do not establish effective routing or connectivity. |

Exact provider, caller, configuration, and assertion links: [backend account](evidence/backend-analysis-20261030.md) and [frontend account](evidence/frontend-analysis-20261030.md).
The frontend names `/auth/v3/sso/login` as `loginEntra`. That version name does not select CES authorization.
Source: [frontend service calls](evidence/frontend-analysis-20261030.md#fe-01-the-shell-consumes-a-normalized-bff-contract).

Auth and BFF dual modes compare different scopes.
BFF can partition legacy and migrated tiles, so its comparison logs cannot establish equivalent same-scope permissions.

### API differences and compatibility

Confidence: HIGH for the eight retained samples; business equivalence remains UNKNOWN.
All eight samples parse as JSON. Two aggregate samples are byte-identical.

| Concern | EMS2 sample | CES samples | Required treatment |
| --- | --- | --- | --- |
| Account data | Account status, type, name, owner, and composite role identities. | User/application identifiers and grants; no equivalent full account sample. | Resolve account attributes and service-account contracts separately. |
| Functional permissions | Entity, role, subject, action hierarchy. | CamelCase role details or snake_case feature/action grants. | Select the effective-permission endpoint and explicit DTO mapping. |
| Application identity | Named applications and composite IDs. | `appId`, `appUID`, `itamId`, or `itam_id`, depending on shape. | Keep external ITAM and internal application identities distinct. |
| Data permissions | Legacy data-role assignments. | Policies, profiles, field rules, and string values. | Review role-to-profile and data-scope mappings. Preserve alphanumeric values. |
| Permission sets | 63 unique subject/action pairs. | 30 unique feature/action pairs. | Only 23 names overlap; different roles and unknown captures prevent a parity conclusion. |
| Membership | Account assignments. | User response includes entitlement 149; catalog membership is empty for that entry. | Resolve direct/effective membership and capture timing before treating this as a defect. |

Sources and exact JSON pointers: [API analysis](evidence/api-analysis-20261030.md#confirmed-sample-differences).
Full hashes and permission differences: [sample manifest](evidence/api-sample-manifest-20261030.json).
The samples establish examples, not authoritative API versions, errors, pagination, or operational limits.

### Proposed sequence

This sequence is an inference from the objective and inspected dependencies.
It requires owner review before becoming an executable implementation or deployment plan.

1. Bind all applications, tiles, APIs, SDK consumers, service accounts, deployment artifacts, and accountable contacts.
2. Confirm CES contracts, account provisioning, entitlement profiles, and approved permission mappings.
3. Complete Auth data-role and SDK migration, while preserving reviewed frontend and token semantics.
4. Align BFF tile configuration, CSV import, administration, audit, database migrations, and environment settings.
5. Run DEV smoke verification for each squad and every integration family.
6. Run UAT permission, workflow, service integration, data-scope, revocation, and performance verification against the EMS2 baseline.
7. Collect squad sign-offs, integration sign-offs, CES CR evidence, and the complete applicable passing unit suites.
8. Rehearse cutover and recovery with explicit triggers, owners, cache handling, and mixed-version constraints.
9. Set all final tiles and service authorization to CES, then establish zero EMS2 traffic and remaining operational dependencies.
10. Retire EMS2 configuration and credentials after observed independence and the approved recovery window.

Rollback during testing can switch individual tiles, as the user specified.
Permanent post-cutover EMS2 fallback would contradict the final objective.
Recovery windows, thresholds, and authorization remain unresolved in [MIG-Q5](#mig-q5).

## Acceptance criteria

The criterion below records the explicit final objective.
It is a draft acceptance definition, not a complete approved migration AC inventory.
Detailed access, failure, identity, and data criteria await the question batch.

### MIG-AC-001

Source: [final migration objective](evidence/historical-user-inputs-20261028-29.json), user statement dated 29 October.

```gherkin
@CES-MIGRATION @MIG-AC-001
Feature: Complete RATAN authorization migration to CES

  Scenario: Final cutover removes EMS2 dependencies
    Given the approved inventory covers RATAN users, tiles, services, SDK consumers, and service accounts
    And the migration verification workload covers every applicable inventory entry
    When the final CES deployment executes that workload
    Then zero authorization or account requests use EMS2
    And every applicable upstream authorization dependency uses CES
```

```yaml
acceptance_criteria:
  - id: MIG-AC-001
    given: Given the approved inventory and workload cover all applicable RATAN consumers
    when: When the final CES deployment executes that workload
    then: Then zero authorization or account requests use EMS2 and all applicable upstream dependencies use CES
    measure:
      metric: EMS2 authorization and account requests across the approved workload
      operator: equals
      value: 0
      unit: requests
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| [MIG-AC-001](#mig-ac-001) | Inspect effective dependencies and observe outbound requests across every inventory entry. | Target candidate and representative human/service identities; inventory pending. | Verification workload, observation window, and load require owner agreement. | Exact artifacts, settings, request traces, assertions, and retained results. |

A quiet observation period cannot prove absent dependencies without workload and inventory coverage.
Passing unit tests cannot establish deployed provider independence.

## Traceability

The approved AC denominator remains UNKNOWN.
One draft final-objective criterion exists. No matching executed migration case is established.
Existing tests and historical review cases do not supply complete migration coverage.

### AC-to-test matrix

| Definition and denominator | Test/assertion evidence | Execution and limit |
| --- | --- | --- |
| [MIG-AC-001](#mig-ac-001); draft inventory: 1; approved denominator UNKNOWN. | No complete zero-EMS2 assertion chain established. [Current assertions](evidence/backend-analysis-20261030.md#assertion-evidence) explicitly retain an EMS2 data read. | NOT_RUN; no passing coverage percentage. |

### AC-to-code-change matrix

| Definition and denominator | Code evidence | Conformance and limit |
| --- | --- | --- |
| [MIG-AC-001](#mig-ac-001); approved denominator UNKNOWN. | [Auth/BFF changes and SDK boundary](evidence/backend-analysis-20261030.md#remaining-legacy-dependencies). | Current local source retains EMS2 dependencies. Full change-unit inventory remains incomplete. |

### Code-change-to-test matrix

| Changed scope and denominator | Inspected assertions | Execution and limit |
| --- | --- | --- |
| Full migration changed-unit denominator UNKNOWN. | [Backend assertion links](evidence/backend-analysis-20261030.md#assertion-evidence) and [frontend assertion links](evidence/frontend-analysis-20261030.md#test-evidence-and-limits). | NOT_RUN. Shared AC links do not establish direct change-to-test coverage. |

No conformance percentage follows from source links or test existence.
The CES cashflow Robot suite injects Redis data directly.
Its assertions do not prove live CES ingestion or complete provider migration.
Source: [setup and assertions](evidence/frontend-analysis-20261030.md#test-evidence-and-limits).

## Sources

Exact source hashes resolve through the [source register](evidence/source-register-20261030.json).
Historical sources retain their bytes and existing locations.

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| USER-20261030 | [Exact request](evidence/user-input-20261030-migration-plan.txt) | Current chat, 30 October | Source register | User; high-priority intent. | Does not establish detailed mappings or deployment. |
| CHATGPT-20261028-29 | [Exact historical user inputs](evidence/historical-user-inputs-20261028-29.json) and [raw capture](evidence/chatgpt-conversation-20261030.json) | Turn IDs and Singapore timestamps retained. | Source register | User wording has high priority. Assistant drafts remain secondary. | Five returned exchanges; earlier context unavailable. |
| API-SAMPLES | [Eight supplied files](api/) | Untracked supplied bytes at registration. | [Sample manifest](evidence/api-sample-manifest-20261030.json) | Owner unknown; supplied examples. | Environments and capture dates unknown. |
| BACKEND-SOURCE | [Backend manifest](evidence/backend-source-manifest-20261030.json) | Exact Auth, BFF, and SDK commits above. | Per-file manifest | Local implementation evidence. | No deployment or passing execution. |
| FRONTEND-SOURCE | [Frontend manifest](evidence/frontend-sources-20261030.json) | Commits or per-file hashes. | Per-file manifest | Local implementation and prior user-answer evidence. | Some supplied copies lack Git history. |
| PRIOR-REVIEW | [27 October review](../ems3-entitlement-review-20261027/07-code-review.md#comparison-identity) | Auth `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`; BFF `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`. | Source register | Prior source analysis; no acceptance authority. | Predates current commits; its cases were not executed. |

## Evidence and open questions

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Workspace status and catalogs | [Retained discovery](evidence/workspace-status-20261030.json). | Declared repository and tool scope. | Catalog metadata does not prove runtime relationships. | Whole-RATAN consumer inventory. |
| Knowledge indexes, security, architecture, and prior answers | [Inspected sources](evidence/frontend-sources-20261030.json). | Existing entry and tile rules. | Candidate records retain review limits. An older Auth EMS3 absence statement is stale. | CES mapping and unresolved multi-entity rule. |
| API samples | [Eight hashes](evidence/api-sample-manifest-20261030.json). | [MIG-AC-001](#mig-ac-001) and future access criteria. | Payload facts only; capture comparability unavailable. | Effective contracts and approved mappings. |
| Current backend/frontend/test source | [Backend](evidence/backend-source-manifest-20261030.json) and [frontend](evidence/frontend-sources-20261030.json) manifests. | Migration implementation and compatibility. | Exact source and assertions; no business execution. | Deployed baseline and complete verification workload. |
| Historical review and retained validation | [Old review validation](../ems3-entitlement-review-20261027/07-code-review.md#validation-evidence). | Historical findings and environment limits. | Earlier compilation stopped at private dependencies. Today's heads were not tested here. | Current dependency access and execution results. |

Current source addresses several earlier findings, including CSV, audit columns, omitted settings, and tile-specific grants.
This observation neither closes all historical findings nor carries them forward as current defects.
A current review must reconcile each relevant finding against current source and execution.
No source-predicted issue here has demonstrated disruptive production user impact.
Unavailable execution does not establish a product failure or automatic release hold.

### Answer and question log

The following answers are already resolved from high-priority user sources.
They need no repeat confirmation of business intent.

| ID | Answer | Confidence and rationale | Source | Status and limit |
| --- | --- | --- | --- | --- |
| MIG-A1 | Final migration covers whole RATAN with zero EMS2 dependencies. | HIGH; explicit user statement. | [Historical user inputs](evidence/historical-user-inputs-20261028-29.json). | Answered; deployment unproved. |
| MIG-A2 | Each tile can switch during testing; all final tiles use CES. | HIGH; explicit user statement. | Same [source](evidence/historical-user-inputs-20261028-29.json). | Answered; configuration workload incomplete. |
| MIG-A3 | Service authorization migrates fully to CES through central Auth. | HIGH; explicit user statement. | Same [source](evidence/historical-user-inputs-20261028-29.json). | Answered; all external consumers not inventoried. |
| MIG-A4 | Settlement, Trade Control, and FlowZero own business verification; integration owners verify service calls. | HIGH; explicit user statements. | Same [source](evidence/historical-user-inputs-20261028-29.json). | Answered; named contacts and sign-offs unavailable. |

Each question below follows the bounded source investigation above.
Suggested choices are proposals. No business answer is preselected.
Another answer, `unknown`, or a named contact is acceptable.

#### MIG-Q1

The latest draft targets 6 November UAT, mid-November CES provisioning, and 28 November cutover.
Earlier draft dates differ. Current CES and RATAN CR evidence is unavailable.

Question: Are these targets current, and which CRs confirm the outstanding production accounts, entitlements, and profile assignments?

Proposed choices: retain these targets and provide CR references; provide revised dates; name the release/CES contact; unknown.

Answer:

Confidence: MEDIUM for the working plan; UNKNOWN for current committed dates and CR completion.
Owner: unknown. Consequence: release sequencing and provisioning gates remain unbound.
Next action: link the current CRs and schedule. Source: [milestone baseline](#working-milestone-baseline).

#### MIG-Q2

Local Auth and BFF heads are known. The inspected SDK predates the reported DEV migration.
The historical assistant guide mentions SDK CES support in DEV; the user did not identify its exact revision.

Question: Where is the current DEV/UAT deployment inventory, including SDK versions and all direct or indirect EMS2 consumers?

Proposed choices: provide the release/component manifest; nominate squad and integration contacts to complete it; provide another inventory; unknown.

Answer:

Confidence: HIGH for inspected source identities; UNKNOWN for complete deployed coverage.
Owner: unknown. Consequence: full migration scope and remaining dependency work cannot be finalized.
Next action: bind artifacts, environments, tiles, APIs, service accounts, and accountable contacts.
Sources: [backend identities](evidence/backend-analysis-20261030.md#scope-and-source-identity) and [frontend identities](evidence/frontend-analysis-20261030.md#scope-and-source-identity).

#### MIG-Q3

Samples and code expose different account, role, feature, data-profile, and service permission representations.
Account-status and CES service-account samples are missing.
The singular/plural data-entitlement names also need an explicit identity mapping.

Question: Which CES contract and mapping source is authoritative for human, admin, data-profile, and service-account permissions?

Proposed choices: provide approved contracts and mappings; nominate the CES and RATAN policy owners; review an agent-drafted mapping later; unknown.

Answer:

Confidence: HIGH for structural differences; UNKNOWN for approved semantic mappings.
Owner: unknown. Consequence: unintended denials, grants, or data-scope changes cannot be excluded.
Next action: obtain the canonical mapping and synchronized representative EMS2/CES account snapshots.
Sources: [API differences](evidence/api-analysis-20261030.md#confirmed-sample-differences) and [backend mappings](evidence/backend-analysis-20261030.md#confirmed-auth-server-behavior).

#### MIG-Q4

Current CES tile matching accepts any configured feature without requiring a named action.
Existing user answers cover one entity with an empty subject; multiple-entity matching remains unanswered.

Question: What approved rule maps multiple entities/features and action requirements into CES tile visibility and direct launch?

Proposed choices: any mapped feature grant; require a specified access action; provide another rule or policy contact; unknown.

Answer:

Confidence: HIGH for current source behavior; UNKNOWN for the unresolved mapping policy.
Owner: portal team for existing entry policy; migration mapping owner unknown.
Consequence: tile visibility tests lack a stable expected result for these boundaries.
Next action: record the rule and define its positive, negative, and boundary criteria.
Sources: [BFF matcher](evidence/backend-analysis-20261030.md#confirmed-bff-behavior) and [existing answers](evidence/frontend-analysis-20261030.md#existing-intended-rules-already-answered).

#### MIG-Q5

Current code uses several independent caches, deadlines, and failure controls.
Configured TTLs do not establish acceptable revocation delay or performance limits.
Final CES-only intent already excludes permanent EMS2 fallback.

Question: Which operational standards define acceptable revocation delay, latency, outage behavior, and cutover recovery triggers?

Proposed choices: apply linked existing standards; nominate security/operations owners to define limits; provide another policy; unknown.

Answer:

Confidence: HIGH for the existence of separate controls; UNKNOWN for approved operational limits.
Owner: unknown. Consequence: performance, revocation, and recovery acceptance cannot be finalized.
Next action: identify the standards and measurable limits before UAT completion and cutover rehearsal.
Source: [configuration and cache boundaries](evidence/backend-analysis-20261030.md#confirmed-auth-server-behavior).

### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| Migration source investigation | No governed migration record was edited. | Historical intent was recovered and linked; no new policy answer received. | This task intake and evidence account only. | Not applicable; no governance transition occurred. | Unpublished; unknown; process returned answers before a governed update. |
| Stale Auth architecture statement | Candidate architecture topic and later question record disagree. | Current source and [later answer](../ui-test-coverage-20261022/05-knowledge-questions.md#kq-arch-16) establish Auth CES support. | No knowledge edit in this source-query stage. | Existing provenance remains unchanged. | Candidate; unknown; reconcile through knowledge governance before publication. |

### Intake investigation plan

- Completed: preserve current and recovered historical user inputs before deriving intent.
- Completed: discover workspace resources and inspect knowledge, reports, API samples, code, callers, and selected assertions.
- Completed: save API, backend, and frontend investigations immediately with hashes and explicit execution limits.
- Completed: reconcile today's commits with the historical review without inventing defect closure.
- Pending: collect the user's batch answers and identified owner evidence.
- Pending: refine complete migration criteria and canonical cases after material mappings become clear.
- Pending: run authorized integration and browser verification against exact deployments and approved expectations.
- Validation evidence: [document checks](evidence/document-checks-20261030.json) and [artifact lint](evidence/intake-lint-20261030.json).
