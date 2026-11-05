# Release and tenant operation boundaries

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [KT-release-operations, version 2](../../../candidates/operations/KT-release-operations.md#L2-L7).

## Summary

The candidate connects portal release planning, tenant responsibilities, and configuration promotion.
It keeps technical deployment separate from business activation and preserves unresolved release-policy alternatives.
See the canonical [summary](../../../candidates/operations/KT-release-operations.md#summary).

## Key rules and qualifiers

- The proposal separates Portal routing releases from tenant application, backend, database, infrastructure, and validation responsibilities.
  Its present approval remains unconfirmed.
  See [ownership and scope](../../../candidates/operations/KT-release-operations.md#ownership-and-release-scope).
- Proposed scheduling readiness includes solution intent, routing, connectivity, UAT sign-off, and rollback planning.
  These requests do not prove completed checks.
  See [readiness before scheduling](../../../candidates/operations/KT-release-operations.md#readiness-before-scheduling).
- The documented promotion flow exports catalog records as CSV and submits them through a tenant pipeline.
  Its FMAA dependency and replacement plan remain unresolved.
  See [configuration promotion](../../../candidates/operations/KT-release-operations.md#configuration-promotion).
- The proposal contains conflicting 10-hour and 24-hour durations, plus differing urgent-release confirmation rules.
  The candidate selects neither alternative.
  See the [release window proposal](../../../candidates/operations/KT-release-operations.md#release-window-proposal).
- Planned technical dates, business dates, and configuration uploads do not establish business readiness or acceptance.
  See [activation boundaries](../../../candidates/operations/KT-release-operations.md#technical-and-business-activation) and [deployment evolution](../../../candidates/operations/KT-release-operations.md#deployment-evolution).

## Unresolved questions

- Which release duration and urgent-release confirmation rule apply?
- Which checklist, authentication replacement, and deployment procedure govern each environment?
- Which records establish technical readiness and business activation separately?

See the canonical [open questions](../../../candidates/operations/KT-release-operations.md#open-questions).
Owner: unknown. Next action: obtain the governing decisions and evidence for each release gate.

## Connections

- [Administration and onboarding](../KT-admin-and-onboarding/index.md)
- [Frontend composition](../KT-frontend-composition/index.md)
- [Application interoperability](../KT-application-interoperability/index.md)

The canonical [connections](../../../candidates/operations/KT-release-operations.md#connections) define these relationships.
