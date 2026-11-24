---
artifact_kind: risk-issue-register
id: SDK-SEAMLESS-GAPS-20261108
version: 1
status: draft
owner: unknown
source_refs: [USER-SEAMLESS, SDK-INTENT, API-COMPARISON, SOURCE-BINDINGS]
related_ids: [SDK-OPT-20261107, KT-sdk-and-entitlements, KT-ces-migration-parity]
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

# Gaps to seamless SDK migration

> **Seven SDK and integration gaps prevent a complete unchanged-behavior claim.**
> Action: establish the CES contract, approved projections, consumer compatibility, and actual execution evidence.
> Consequence: matching map structure and selected grants cannot establish unchanged business-user behavior.
> Owner: unknown for migration acceptance. Evidence: [gap register](#risk-and-issue-entries) and [source bindings](evidence/gap-source-bindings-20261108.json).

## Scope and source facts

The [latest user request](evidence/user-seamless-migration-gaps-20261108.md#exact-user-input) asks for a detailed explanation.
This assessment treats seamless migration as unchanged business-user access, data visibility, and supported workflows.
Backend configuration and integration can change. A separate zero-consumer-source-change constraint would require additional compatibility design.
No application fix, entitlement decision, deployment, or publication is authorized by this explanation.

The intended permission contract has zero missing and zero unsupported additional role-specific permissions.
Its source is [SDK intent version 8](../../knowledge/records/candidates/security/KT-sdk-and-entitlements.md#sdk-ces-intent-ac-001).
That knowledge remains candidate and draft. It does not establish deployed parity or publication approval.
The SDK already supports multiple distinct role keys. Role multiplicity alone is not an SDK defect.

| Source | Comparison identity | Limit |
| --- | --- | --- |
| SDK EMS2 baseline | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | Supplied source baseline; not the released `1.1.1` binary. |
| Current SDK | `0240b1c260337bf3c38f2b5ecaad2d1ec157296d` | Forty-four controlled tests pass; real integration remains unverified. |
| Auth Server | `cacc4d218747e1591d5fb990eb5a8d8bcfb231a5` | Declares SDK `1.1.1`; source inspected without a consumer build. |
| BFF | `95480c0e2563bc2a5a639bca1f22ecedb61936c2` | Has independent authorization and data-filter paths. |
| Cashflow | Filesystem source; hashes and decisive excerpts in [source bindings](evidence/gap-source-bindings-20261108.json). | No independent Git or deployed artifact identity. |
| API examples | [Eighteen request captures and exact hashes](evidence/api-compatibility-20261108.json) | EMS2 PROD/UAT examples and CES UAT responses have unmatched capture timing. |
| Additional source review | [Source bindings](evidence/gap-source-bindings-20261108.json) | Read-only review; no new live execution. |

Assessments below distinguish confirmed source conditions, conditional consequences, and unavailable execution.
Confidence is high for inspected schemas, mapping capabilities, and source-call incompatibility.
Confidence in unchanged live business behavior remains unresolved.
No live user disruption or production regression is established by these findings.

## Risk and issue entries

| ID | Type | Finding or uncertain event | Evidence | Consequence | Likelihood and basis | Impact and basis | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [SG-01](#sg-01) | risk; contract | Supported current CES endpoint and parser agreement remain unverified. | Current DTO and supplied aggregate schemas. | Incompatible responses yield errors or no grants. | Conditional on the actual endpoint. | Potential denied business actions; no live failure observed. | unknown | OPEN |
| [SG-02](#sg-02) | issue; integration | Complete reviewed legacy entity/role routing is not established. | Existing mapping controls and three sample scopes. | Correct actions can appear under incorrect legacy keys. | Predicted for an unrestricted single-entity mapping. | Permission-dependent callers can lose or broaden access. | unknown | OPEN |
| [SG-03](#sg-03) | risk; semantic parity | Full assignments and action equivalence remain unproved. | Exact role matches and differing effective responses. | Missing or additional user permissions remain possible. | Snapshot differences exist; live applicability is unknown. | Consequence depends on affected business actions. | unknown | OPEN |
| [SG-04](#sg-04) | risk; integration | Real FMAA lifecycle and permission-failure recovery remain unverified. | Provider contract and controlled failure tests. | Token or CES failures can become empty permission maps. | Source behavior is confirmed; live frequency is unknown. | Functions may disappear; forced logout is not demonstrated. | unknown | OPEN |
| [SG-05](#sg-05) | issue; compatibility | A historical consumer uses an incompatible static validator call. | Auth Server calls and SDK instance method. | A direct dependency replacement predicts a compilation problem. | Confirmed source mismatch; build not run. | Consumer adoption can be blocked before deployment. | unknown | OPEN |
| [SG-06](#sg-06) | risk; data semantics | A matching data-role marker does not establish matching record restrictions. | Separate backend data-policy paths. | Users might see different records or authorization limits. | Resolved-policy equality is unassessed. | Potential data exposure or missing business records. | unknown | OPEN |
| [SG-07](#sg-07) | risk; verification | Complete current-artifact and real-consumer equivalence is unavailable. | Controlled tests and the existing verifier's stated limits. | The seamless-migration claim remains unsupported. | Evidence absence is confirmed; defect probability is unknown. | Assurance limit; no automatic product failure or release hold. | unknown | OPEN |

### SG-01

**Gap: establish a supported source contract before assuming the existing adapter can consume current CES APIs.**

Setup: use a scoped human account from the retained EMS2 and CES examples.
The [existing malformed-response case](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-004) defines the controlled rejection boundary.

1. Inspect the old account-role and grant responses expected by the baseline SDK.
2. Compare the candidate endpoint and DTO against the current app/user response.

- Intended result: the adapter obtains authoritative assigned grants and preserves their role attribution.
- Old result: baseline source joins EMS2 grant rows to assigned entity and role identities.
- New result: the SDK expects `/fmces/v1/entitlement/user/{userId}` and camel-case assigned-role rows.
- Difference: supplied app/user examples contain role names beside one merged permission set.
- Predicted result if substituted: the explicit API rejects missing role application identity; the legacy API returns an empty map.
- Evidence: [endpoint property](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java:38), [DTO](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/entity/CesRole.java:12), and [response validation](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:165).

The assigned-role endpoint is not proved unavailable. A historical response supports its earlier parser shape.
Verify its supported current contract first. If supported, this gap can close without replacing the mapper.
If unsupported, a supported role-specific loader or adapter is required.
The application catalog may contribute role definitions and membership, subject to CES contract guarantees.
Its membership and the effective-user response are not fully consistent in these captures.
Do not reconstruct assignments from catalog names or copy merged grants to every role.

Owner: unknown. Suggested responsibility: CES API owner and SDK maintainer.
Closure requires successful current human and service-account responses, correct role attribution, and actual SDK consumption.

### SG-02

**Gap: retain legacy permission keys across the consolidated CES application.**

Setup: use the three retained PROD accounts and their existing legacy entity scopes.
The [scope case](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-002) defines isolation requirements.

1. Read each legacy entity/role key from the EMS2 response.
2. Trace its proposed CES role through each configured entity mapping.

- Intended result: callers receive the same required legacy keys and their own grants.
- Old result: EMS2 carries separate `X_RATANONE`, `RATAN_DATA_ENTITLEMENT`, and `RATAN_FUNC` identities.
- New result: each selected CES role receives the configured legacy entity prefix.
- Difference: one unrestricted `X_RATANONE` mapping can route `Global` and `SYS_RO` under the wrong entity.
- Limit: this is a configuration-dependent source prediction, not an executed deployed failure.

| Legacy output | Candidate configuration treatment for these samples |
| --- | --- |
| `X_RATANONE:FMO_RO` and `X_RATANONE:NON_FMO_RO` | Select the reviewed functional roles within `X_RATANONE`. |
| `RATAN_DATA_ENTITLEMENT:Global` | Select `Global` separately and retain its data-marker feature. |
| `RATAN_FUNC:SYS_RO` | Select `SYS_RO` separately and retain its three system features. |

Existing role allowlists and feature selectors can express this bounded projection after compatible role input is available.
No generic mapper change is required for these matched sample rows.
This configuration covers three samples only. It is not a complete production mapping.
The SDK correctly rejects collisions instead of silently merging unrelated roles or features.

Evidence: [mapping properties](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java:43), [mapping logic](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:169), and [sample comparisons](evidence/api-compatibility-20261108.json).
Owner: unknown. Suggested responsibility: application entitlement owner and SDK integrator.
Closure requires reviewed mappings and exact output equality for every declared legacy scope.

### SG-03

**Gap: preserve each user's actual allowed and denied actions, including additional CES roles.**

Setup: compare equivalent assignments for each declared account and role.
The [paired compatibility case](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-008) supplies the existing equality objective.

1. Compare complete entity/role/subject/action outputs for the declared account.
2. Examine every missing and additional permission against approved migration scope.

- Intended result: no missing required permission and no unsupported additional permission.
- Old result: the three PROD samples contain 60 grant rows across selected legacy roles.
- New source evidence: the selected CES role definitions contain exactly the same pair sets as those 60 PROD grant rows.
- This comparison does not execute the SDK or prove complete account assignments.
- Difference: effective-user unions contain 47 versus 28 pairs and 31 versus 29 pairs for the two human samples.
- Limit: CES is UAT and capture timing is unmatched. Individual union grants omit their role and legacy-entity attribution.

Some extra grants concern CES administration. They are not automatically migrated business permissions.
Exclude them from legacy output where the reviewed scope requires exclusion.
Catalog presence alone does not establish equal complete assignments.

A separate UAT role comparison shows an adapter limit.
For `FMO_OPS_BOM`, `RATAN_VALIDATION_EXCEPTION` has one old action and six CES catalog actions.
The five additional actions include exception replay and manual closure.
Current `feature-names` filtering selects the entire feature. It cannot remove individual actions from that feature.
Current sampled CES accounts are not assigned this role, so this is not a demonstrated user-access regression.
If this role enters the migration scope, resolve its assignment and action differences first.
Correct CES definitions or add an explicitly approved action projection only if the required semantics demand it.

Evidence: [static action comparison](evidence/gap-source-bindings-20261108.json) and [action emission](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:192).
Owner: unknown. Suggested responsibility: IAM/CES assignment owner and application entitlement owner.
Closure requires equivalent assignments, explained extra roles, and zero unexplained missing or additional permissions.

### SG-04

**Gap: integrate service credentials and verify failure recovery without changing business-user authentication.**

Setup: inspect an existing one-argument entitlement caller and its application-owned token provider.
Existing [token](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-003) and [failure](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-006) cases cover controlled boundaries.

1. Trace entitlement lookup with valid, expired, missing, and renewed service credentials.
2. Trace the consumer's response to no grants, CES failure, and recovery.

- Intended result: service authentication remains an integration responsibility without business-user token handling.
- Old result: the baseline lookup has no caller-provided FMAA token contract and returns empty maps after failures.
- New result: the legacy overload needs `FmaaTokenProvider`; without one it returns an empty map immediately.
- Difference: a service integration omission can remove permissions while portal authentication still succeeds.
- Limit: no live token expiry, renewal, outage, recovery, or forced logout was observed.

The provider is called afresh, but the application owns token acquisition, expiry, refresh, audience, and permissions.
The SDK has no independent token acquisition, automatic retries, or permission caching.
The legacy API intentionally collapses lookup errors and valid no-grant results into the same map shape.
Its compatibility behavior does not establish sufficient operational diagnostics.
Retain sanitized failure classification and verify consumer recovery without widening permissions or inventing retry policy.

Evidence: [provider and explicit API](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:53) and [44-test result](evidence/candidate-result.json).
Owner: unknown. Suggested responsibility: token-provider and application integration owners.
Closure requires actual token renewal, bounded failure handling, recovery, and consumer behavior observations.

### SG-05

**Gap: establish compatibility with the released SDK versions used by actual consumers.**

Setup: use the registered Auth Server source and its declared SDK `1.1.1` dependency.
The [Spring compatibility case](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-012) covers controlled SDK wiring, not this consumer build.

1. Inspect the SDK methods used by the actual consumer.
2. Compare those calls with the candidate API and required runtime dependencies.

- Intended result: the consuming application compiles, starts, and retains authentication behavior after adoption.
- Old result: consumer source declares `1.1.1` and calls `JwtTokenUtil.validateToken` statically.
- New result: the supplied SDK validator uses an instance with configured key material.
- Difference: a direct dependency replacement predicts a source-compatibility failure.
- Limit: the released `1.1.1` binary and actual consumer compilation were not inspected or executed here.

This mismatch exists in the supplied pre-migration source baseline. The mapper optimization did not introduce it.
Either adapt the consumer's validator injection or provide a compatible SDK surface after assessing configuration and security.
Do not add a static wrapper without resolving how it obtains the correct configured validator.
If zero consumer-source changes are required, compatibility must be provided below those existing call sites.
The Java 17 and Spring Boot `4.0.6` dependency line also requires actual consumer validation.

Evidence: [dependency](../../repos/services/ratan-auth-server/pom.xml:98), [login call](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/LoginController.java:157), [authenticate call](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/AuthenticationController.java:87), and [instance method](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java:42).
Owner: unknown. Suggested responsibility: SDK and consuming-application maintainers.
Closure requires actual artifact resolution, compilation, Spring startup, and authenticated request execution for each supported consumer.

### SG-06

**Gap: retain resolved data access and required profiles beyond the SDK's functional marker.**

Setup: trace a user with `RATAN_DATA_ENTITLEMENT:Global` and protected business records.
The current SDK map does not contain resolved data-policy fields or values.

1. Trace the legacy data role into the application's data restriction and authorization-limit contracts.
2. Compare the CES policies, resolved field/value restrictions, and consumer profile decisions.

- Intended result: the same records remain visible, excluded records stay excluded, and required limits retain their meaning.
- Old result: consumers use separate data-role and data-filter paths in addition to functional permission checks.
- New result: the SDK map exposes marker actions; separate backend paths process CES data restrictions.
- Difference: matching `Global` and `VIEW_ENTITLEMENT` proves no equality of resolved record restrictions.
- Limit: old and new policy definitions, field values, and actual allowed/excluded records are not fully bound.

Compare relevant booking entities, country and account restrictions, and AND/OR combinations where they apply.
The Auth Server recognizes `Global`, `GBS`, and `Onshore` marker names separately from actual policy evaluation.
A role name cannot replace an authoritative data profile.
Do not expand SDK responsibilities unnecessarily; close this boundary in the owning data services and consuming applications.

Evidence: [data-role resolver](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/Ems3DataRoleResolver.java:11), [separate data-role path](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/dataentitlement/DataEntitlementService.java:53), and [resolved data filters](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java:115).
Owner: unknown. Suggested responsibility: data-policy owner and protected business API owner.
Closure requires equal intended field restrictions and actual allowed/excluded record outcomes.

### SG-07

**Gap: obtain complete current-artifact evidence through real consuming applications.**

Setup: declare the migration population, environments, configuration, source versions, and acceptance predicates.
Reuse the [existing verifier](../ces-entitlement-migration-20261102/spring-verifier/README.md#6-establish-complete-migration-acceptance).

1. Compare both actual SDKs for the same authoritative accounts and equivalent assignments.
2. Exercise the resulting allowed and denied business operations through each declared consumer.

- Intended result: every declared account is assessed and every required behavior has matching execution evidence.
- Old result: retained paired SDK checks use controlled fixtures and a supplied source baseline.
- New result: the latest SDK passes all 44 controlled tests; existing synthetic SDK replays use the earlier migration candidate.
- Difference: live current-artifact, complete-population, data restriction, and real-consumer outcomes remain unverified.
- Limit: complete migration population and the full business behavior denominator are unknown.

The verifier already compares role keys, subjects, action values, duplicate counts, action order, and empty roles.
Its current candidate pin is `fd9a157`; current SDK source is `0240b1c`.
Use a verified current artifact binding before reusing that result for the latest candidate.
The verifier deliberately keeps `migrationVerified` false because SDK-map parity excludes wider business boundaries.

The next evidence must include service accounts, no-grant users, additional roles, grant changes, and revocation.
Include token renewal, failure recovery, and relevant existing-session behavior.
Bind results and remote runtime logs to the tested build, configuration, time window, and request/session correlations.
The missing offline formatter dependencies limit local packaging verification; they do not establish a product defect.
Cutover and rollback behavior require an explicit environment plan and evidence when migration execution is authorized.

Evidence: [latest controlled results](evidence/candidate-result.json), [verifier limits](../ces-entitlement-migration-20261102/spring-verifier/src/main/java/com/example/migration/VerificationRunner.java:24), and [packaging limit](evidence/packaging-result.json).
Owner: unknown. Suggested responsibility: application verification and migration operations owners.
Closure requires zero unexplained differences and zero unassessed accounts within an authoritative declared scope.
Each applicable candidate test must pass. Scoped parity does not establish unexecuted business or deployment behavior.

### Wider portal boundary

This is an additional scope observation, rather than an eighth SDK defect.
The SDK upgrade does not replace the independent BFF, Auth Server, or frontend role contracts.
The [existing portal audit](../ces-entitlement-migration-20261102/11-zero-upper-change-audit.md#findings) records their separate gaps.

Cashflow passes one profile into authorization-limit URLs.
Shared saved views and filters require scalar ownership values.
CES users can have several roles, so arbitrary first-role selection or comma-joined roles cannot establish an equivalent owner or profile.
Current [ownership intent](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#interim-rule-for-ces-role-owned-writes) keeps affected CES writes pending until agreement.
That preserves the recorded interim rule but does not supply a seamless full-feature migration.

Evidence: [Cashflow profile call](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/components/CashflowDetails/MultiExceptions/hooks/useData.ts:688), [profile URL](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/services/index.ts:128), and [BFF role list](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:84).
These are source-derived consequences. No live application journey ran during this explanation.
If the goal covers the whole portal, define authoritative role/profile/ownership semantics and verify the affected journeys separately.

## Proposed responses

| Entry ID | Response | Next action | Trigger | Action owner | Target date | Closure condition | Actual closure evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [SG-01](#sg-01) | Reduce | Confirm the supported current CES contract. | Before selecting an adapter source. | unknown | null | Actual SDK consumes authoritative role-specific input. | Pending |
| [SG-02](#sg-02) | Reduce | Review legacy-scope mapping and role allowlists. | After source contract agreement. | unknown | null | Exact legacy keys and isolated grants for declared scopes. | Three static samples only. |
| [SG-03](#sg-03) | Reduce | Reconcile complete assignments and action deltas. | Before asserting permission equality. | unknown | null | Zero unexplained missing or additional scoped grants. | Selected role definitions match; full parity remains open. |
| [SG-04](#sg-04) | Reduce | Integrate FMAA and observe recovery. | Before application adoption. | unknown | null | Correct service token lifecycle and acceptable consumer failure behavior. | Controlled tests only. |
| [SG-05](#sg-05) | Reduce | Verify actual artifacts and consumer calls. | Before replacing dependencies. | unknown | null | Real consumers compile, start, and preserve authentication. | Source mismatch only. |
| [SG-06](#sg-06) | Reduce | Compare resolved data restrictions and profiles. | Before claiming unchanged record visibility. | unknown | null | Required included and excluded records match. | Unassessed |
| [SG-07](#sg-07) | Reduce | Use the existing verifier and real applications. | After contract, mapping, and integration are ready. | unknown | null | Complete scoped execution with matching build and remote log bindings. | Local controlled evidence only. |

## Decisions and residual exposure

The recommended sequence is contract agreement, projection and assignment review, consumer integration, then actual comparative execution.
This sequence follows technical dependencies. It is not a numerical severity score or deployment authorization.
No new SDK feature is justified merely by an evidence gap.
Implement additional logic only when a supported contract or approved projection requires it.
Unobserved production effects retain lower priority than demonstrated business disruption under the project user-impact rule.
The critical current consequence is an unsupported seamless-migration claim, rather than a confirmed production incident.

## Sources and evidence limits

| Source ID | Locator | Exact revision or hash binding | Owner, authority, and limit |
| --- | --- | --- | --- |
| USER-SEAMLESS | [Exact user request](evidence/user-seamless-migration-gaps-20261108.md#exact-user-input) | 8 November 2026 chat. | Human user; explanation scope only. |
| SDK-INTENT | [SDK intended compatibility](../../knowledge/records/candidates/security/KT-sdk-and-entitlements.md#sdk-300-ces-migration-intent) | Version 8; [hash binding](evidence/gap-source-bindings-20261108.json). | User-sourced target; candidate publication remains pending. |
| API-COMPARISON | [Retained API analysis](evidence/api-compatibility-20261108.json) | Eighteen exact request hashes remain unchanged. | Static examples; no current deployment proof. |
| SOURCE-BINDINGS | [Additional source review](evidence/gap-source-bindings-20261108.json) | Exact source revisions and SHA-256 values. | Codex inspection; no new business execution. |

The existing [three coverage matrices](../single-ui-sdk-ces-migration-20261101/09-coverage.md) trace six local criteria and seven original changed units.
Those local assertion links do not establish the live boundaries listed here.
This explanation introduces zero application code changes and no new executable test case.
The scoped local suite denominator is 44 tests. The complete user and business-behavior inventories remain unknown.
No full-migration coverage percentage is supported.

## Unresolved questions

Reuse the domain's [existing open questions](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#open-questions) for unresolved business mappings.
The meaningful remaining decisions concern supported CES role attribution, scoped extra grants, resolved data restrictions, and scalar role/profile/ownership rules.
These decisions have no invented answers. Their accountable owners remain unknown.
Resolve technical contract questions through the CES owner before requesting user policy clarification.
No clarification in this explanation changes governed knowledge meaning.

## Review control

- Required reviewers: actual owners of CES contracts, entitlement mappings, data policies, and consuming applications; identities unknown.
- Actual human review reference: null.
- Next review trigger: current contract evidence, approved mapping, resolved policy, or actual consumer execution becomes available.
- Automated checks and source reconciliation: record in the task's gap-check result.
- Full ASD writing review: pending.
