---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md"]
description: "Existing hasPermission(code) calls accept a mapped grant from either EMS2 or CES, with the provider logged."
---

# Provider-union hasPermission check

## Definition

A provider-union `hasPermission` check lets an existing `hasPermission(code)` call in an upper application accept a matching grant from either the legacy [[entities/ems2]] provider or the [[entities/ces]] provider. The caller keeps its original one-argument contract; the union is resolved internally and the supplying provider is logged.

This rule was introduced by the user's provider-union clarification of 9 November 2026 and is recorded in [[summaries/KT-ces-migration-parity]]. It changes permission-check intent only; it does not prove implementation or deployed log collection.

## Why a union was needed

During per-tile migration, some tiles still admit through EMS2 while others already use CES. Upper applications and shared containers call a single functional permission check. Replacing the provider wholesale would have forced caller changes; keeping only the EMS2 provider would have hidden CES grants. The union keeps the functional check stable across the transition while [[concepts/per-tile-provider-selection]] governs which provider admits each tile.

## Behavior

- The caller passes only the permission code. No new scope argument is required.
- The check evaluates reviewed application, feature, and action mappings, consistent with [[concepts/ems2-to-ces-permission-mapping]].
- A matching grant from either provider yields `true`; only the absence of a matching grant in both providers yields `false`.
- Each accepted decision emits at least one log identifying the provider that supplied the matching grant.
- A denial produces no accepted-grant log, because neither provider supplied a match.

| EMS2 matching grant | CES matching grant | Returned value |
| --- | --- | --- |
| 1 | 0 | true |
| 0 | 1 | true |
| 1 | 1 | true |
| 0 | 0 | false |

These four rows define the union cases. They do not limit the number of accounts, applications, or permission codes covered.

## Relationship to tile admission

The union is a shared functional permission check, not an admission rule. Tile admission remains provider-specific and independent:

- An EMS2 tile keeps its existing EMS2 admission logic.
- A CES tile uses CES admission logic, the configured CES application identity, and the CES permission structure.
- The wire value `EMS3` denotes the CES path in the migration contract.

See [[concepts/portal-entry-and-tile-authorization]] for the broader admission model and [[concepts/microfrontend-layering]] for the container and tile boundaries involved.

## Acceptance criterion

The intended target behavior is captured as FE-COMPAT-AC-004 in [[summaries/KT-ces-migration-parity]]:

```gherkin
Feature: Preserve hasPermission during provider migration
  Scenario Outline: Read either provider without changing the caller
    Given a reviewed application, feature, and action mapping exists for the requested code
    And EMS2 has <ems2_grant> matching grant
    And CES has <ces_grant> matching grant
    When the upper application calls hasPermission with only that code
    Then the returned boolean equals <expected>
    And the number of required additional caller arguments equals 0
    And an accepted decision has at least 1 log identifying a provider that supplied its matching grant
```

Measure: the four boolean results match the grant union, with zero additional caller arguments and provider logs for accepted decisions.

## Limits

- The rule does not select a scalar role and does not resolve saved-item ownership; see [[concepts/ces-role-multiplicity]].
- CES saved-view and filter writes requiring one owner role stay deferred, independent of this check.
- The clarification does not merge legacy EMS2 and CES tile admission choices.
- Its expectation about returned legacy entities remains an implementation question, separate from the intended rule.
- No implementation, deployed log collection, or execution result is established.

## Related pages

- [[concepts/ems2-to-ces-permission-mapping]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[entities/ems2]]
- [[entities/ces]]
- [[entities/ems3]]
- [[entities/ratan]]
- [[entities/single-ui-bff]]
- [[summaries/KT-ces-migration-parity]]
