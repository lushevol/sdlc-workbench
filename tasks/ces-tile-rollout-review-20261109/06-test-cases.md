---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Canonical review probe cases

> **Observed failures require correction before their affected behavior can be accepted.**
> Action: address the [review findings](10-change-review.md#findings). Owner: unknown.
> Consequence: dependency failures and shared CES denial remain present.

These cases define bounded observations. They do not create new business policy.
Each result states its substitutions and source identity.
A probe can pass by correctly asserting a defect. That result does not establish product conformance.

## TC-DEP-JACKSON

```gherkin
Scenario: Compare Jackson initialization with the managed dependency family
  Given Spring Boot 3.3.4 manages Jackson core and annotations at 2.17.2
  And the baseline uses databind 2.17.2
  And the candidate overrides databind to 2.21.8
  When the same probe constructs ObjectMapper and reads an empty JSON object
  Then the baseline reads the object successfully
  And the candidate throws NoClassDefFoundError for JsonSerializeAs
```

Assertions: [dependency probe](evidence/probe_bff_dependencies.py).
Result: [paired dependency execution](evidence/bff-dependencies.json).
The probe uses actual cached dependency bytes and Java 17. The BFF application does not start.

## TC-DEP-VALIDATOR

```gherkin
Scenario: Compare validator initialization against the managed logging API
  Given Jakarta Validation 3.0.2 and JBoss Logging 3.5.3.Final
  And a compatible comparison uses Hibernate Validator 8.0.2.Final
  And the candidate uses Hibernate Validator 9.0.2.Final
  When the same probe builds a validator factory
  Then the compatible comparison creates a validator
  And the candidate throws NoSuchMethodError for Logger.getMessageLogger
```

Assertions: [dependency probe](evidence/probe_bff_dependencies.py).
Result: [paired dependency execution](evidence/bff-dependencies.json).
Boot manages baseline Validator 8.0.1. The comparison substitutes cached 8.0.2 and is not exact baseline execution.

## BFF-ROLLOUT-MIXED

```gherkin
Scenario: Admit mixed providers during normal reads
  Given EMS2 tile 1 and CES application A tile 2 and application B tile 3
  And both CES applications return matching feature and read grants
  When dual-read authorization and drawer filtering run
  Then visible tile IDs equal [1, 2, 3]
  And CES granted tile IDs equal [2, 3]
```

Assertions: [rollout probe](evidence/probe_bff_rollout.py).
Result: [actual service and drawer execution](evidence/bff-rollout-probe.json).
CES transport and private error classes are substituted. The executor runs synchronously.

## BFF-ROLLOUT-FAILURE

```gherkin
Scenario: Observe collateral denial after one CES application fails
  Given the mixed-provider setup in BFF-ROLLOUT-MIXED
  And CES application A returns its valid grant
  And CES application B throws IllegalStateException
  When dual-read authorization and drawer filtering run
  Then visible tile IDs equal [1]
  And CES granted tile IDs equal []
  And tile 2 disappears despite its successful application response
```

Setup: [BFF-ROLLOUT-MIXED](#bff-rollout-mixed).
Assertions: [rollout probe](evidence/probe_bff_rollout.py).
Result: [actual service and drawer execution](evidence/bff-rollout-probe.json).
The isolated application failure is synthetic. The observed collateral filtering uses unchanged production source.

## BFF-ROLLOUT-EMPTY

```gherkin
Scenario: Observe collateral denial after one application returns no functional grants
  Given the mixed-provider setup in BFF-ROLLOUT-MIXED
  And CES application A returns its valid grant
  And CES application B returns role_entitlements equal to []
  When dual-read authorization and drawer filtering run
  Then visible tile IDs equal [1]
  And CES granted tile IDs equal []
  And tile 2 disappears despite its successful application response
```

Setup: [BFF-ROLLOUT-MIXED](#bff-rollout-mixed).
Assertions: [rollout probe](evidence/probe_bff_rollout.py).
Result: [actual service and drawer execution](evidence/bff-rollout-probe.json).
The real mapper rejects the empty response. Live CES empty-assignment representation remains unknown.

## BFF-ROLLOUT-REQUEST

```gherkin
Scenario: Distinguish omitted and explicit null migration fields
  Given the production RequestOfApplicationTile DTO
  When Jackson deserializes {} and {"entitlementSource":null}
  Then the omitted source equals EMS2
  And the explicit null source remains null
```

Assertions: [rollout probe](evidence/probe_bff_rollout.py).
Result: [actual DTO execution](evidence/bff-rollout-probe.json).
The update controller was not executed. Its persisted-provider consequence is source-derived.

## AUTH-PROBE-001

```gherkin
Scenario: Observe the mapping revision emitted after a configuration change
  Given the configured mapping revision equals ems3-v2
  And a synthetic CES assignment maps to ROLE_AFTER_CHANGE and TRADE:READ
  When the production mapper creates its unified entitlement
  Then the mapped role equals ROLE_AFTER_CHANGE
  And the mapped actions include TRADE:READ
  And the emitted revision equals ems3-v1
```

Assertions: [mapper probe](evidence/AuthMappingProbe.java).
Result: [actual mapper execution](evidence/auth-mapping-probe.json).
Java 26 executes release-21 bytecode. Redis acceptance and authentication effects were not executed.

## TC-CONTRACT-PROFILE

```gherkin
Scenario: Compare the scalar profile consumed by the existing Cashflow request
  Given a legacy session supplies a defined role through its X_RATANONE entity
  And a CES-only session supplies its CES entity and roleList without a legacy role fallback
  And the selected cashflow has sub-state PendingVerification
  When the unchanged getUser and Cashflow authorization-limit request chain reads the scalar profile
  Then the legacy source chain supplies the defined role as the profile
  And the candidate source chain supplies an undefined profile
  And the candidate URL contains /profileLimitation/checkLimitation/undefined/
```

Status: `NOT_RUN` for the HTTP and backend flow.
This case records the source-predicted comparison. It does not record a passing execution.
The [source trace](evidence/bff-contract-followup.json) binds exact consumer bytes and relevant lines.
The [shared accessor](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L27-L69) supplies the role.
The [Cashflow service](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/services/index.ts#L128-L134) inserts that profile into the URL.
A preserving correction must use a sourced business mapping. No scalar profile is inferred from `roleList`.
