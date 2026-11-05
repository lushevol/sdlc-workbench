# Frontend composition and application ownership

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [KT-frontend-composition, version 3](../../../candidates/architecture/KT-frontend-composition.md#L2-L7).

## Summary

The candidate separates shared platform modules from application-owned containers and tiles.
Its composition and onboarding guidance retains historical version and compatibility limits.
See the canonical [summary](../../../candidates/architecture/KT-frontend-composition.md#summary) and [scope](../../../candidates/architecture/KT-frontend-composition.md#scope).

## Key rules and qualifiers

- The reported architecture separates Root Config, Base shell, application container, and feature tile.
  See the [four-layer clarification](../../../candidates/architecture/KT-frontend-composition.md#current-four-layer-clarification).
- SystemJS resolves modules; Single-spa manages application lifecycle.
  See [composition roles](../../../candidates/architecture/KT-frontend-composition.md#roles-in-composition).
- Application teams supply static-file and API URLs. Shared-repository review remains a platform responsibility in the documented principles.
  See [ownership and availability](../../../candidates/architecture/KT-frontend-composition.md#ownership-and-availability).
- Shared dependency upgrades require coordination. Specific consumer impact still requires exact provider and consumer evidence.
  See [shared code and compatibility](../../../candidates/architecture/KT-frontend-composition.md#shared-code-and-compatibility).
- Direct external GUI dependencies require a reviewed exception under the source-stated principle.
  Its authority and effective applicability remain unconfirmed.
  See [external frontend dependencies](../../../candidates/architecture/KT-frontend-composition.md#external-frontend-dependencies).

## Unresolved questions

- Which current revisions implement container, tile, and routing interfaces?
- Which shared dependency versions and standalone templates remain supported?
- Which owner controls compatibility changes and dependency exceptions?

See the canonical [open questions](../../../candidates/architecture/KT-frontend-composition.md#open-questions).
Owner: unknown. Next action: confirm applicable versions and ownership before a shared change or new application.

## Connections

- [Portal purpose](../KT-portal-purpose/index.md)
- [Administration and onboarding](../KT-admin-and-onboarding/index.md)
- [Architecture evolution](../KT-architecture-evolution/index.md)

The canonical [connections](../../../candidates/architecture/KT-frontend-composition.md#connections) define these relationships.
