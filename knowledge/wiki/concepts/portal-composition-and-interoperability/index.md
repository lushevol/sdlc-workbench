# Portal composition and interoperability

Derived navigation, 6 November 2026.
**The linked records remain candidate/draft. This synthesis grants no knowledge approval or implementation acceptance.**

## Shared workspace and application ownership

The Portal aims to connect post-trade applications through common entry, themes, authentication, tiles, and workspaces.
Tenant teams retain domain functions while shared platform modules supply integration capabilities.
The stated examples include affirmation, confirmation, settlements, reporting, blotters, and a rules engine.
They do not define a complete application inventory.
See [Portal purpose](../../../candidates/background/KT-portal-purpose.md#business-purpose), candidate/draft, version 2.

The composition design separates the shared shell from application containers and feature tiles.
Import maps locate named modules; SystemJS loading and application lifecycle management have distinct responsibilities.
The intended benefit is independent team delivery within one user workspace.
Shared interfaces and dependencies still require coordinated compatibility review.
See [frontend ownership and loading](../../../candidates/architecture/KT-frontend-composition.md#roles-in-composition), candidate/draft, version 3.

## From module loading to business interaction

Loading a tile and requesting another application's action are different integration concerns.
The interoperability guide describes passing initial context from a source tile to a target tile.
The caller defines business demand; the provider implements the receiving handler and business action.
Portal coordinates routing, access control, context passing, and dispatch in that documented cooperation model.
See [caller and provider cooperation](../../../candidates/interoperability/KT-application-interoperability.md#portal-mediated-tile-navigation), candidate/draft, version 2.

A completed caller alone does not establish joint readiness.
The provider also needs registration, agreed context, authorization readiness, testing, and coordinated delivery.
The OpenFin materials connect desktop applications through contexts and intents.
Their proof-of-concept messages do not establish an approved production contract.
See [contexts and intents](../../../candidates/interoperability/KT-application-interoperability.md#contexts-intents-and-actions), candidate/draft, version 2.

## Evolution and unresolved boundaries

Build-tool research, notification experiments, and proposed service decomposition represent separate investigations.
They do not establish one approved roadmap or replace the documented composition responsibilities.
Notification retention alternatives and unread-message behavior remain unresolved.
See [architecture proposals](../../../candidates/evolution/KT-architecture-evolution.md#documented-knowledge), candidate/draft, version 2.

Current shared dependency versions, compatibility ownership, and supported standalone templates need confirmation.
Interoperability also needs one agreed intent schema and a reviewed production authentication handoff.
Missing examples and proof-of-concept observations cannot establish deployed interoperability.
Owners remain unknown in the linked [composition questions](../../../candidates/architecture/KT-frontend-composition.md#open-questions) and [interoperability questions](../../../candidates/interoperability/KT-application-interoperability.md#open-questions).

## Canonical records and related topics

| Canonical record | Version | Source state |
| --- | --- | --- |
| [KT-portal-purpose](../../../candidates/background/KT-portal-purpose.md) | 2 | candidate/draft |
| [KT-frontend-composition](../../../candidates/architecture/KT-frontend-composition.md) | 3 | candidate/draft |
| [KT-application-interoperability](../../../candidates/interoperability/KT-application-interoperability.md) | 2 | candidate/draft |
| [KT-architecture-evolution](../../../candidates/evolution/KT-architecture-evolution.md) | 2 | candidate/draft |

Use [service responsibilities](../../entities/portal-service-responsibilities/index.md) for the reported service roles.
Use [administration and release](../admin-onboarding-and-release/index.md) for configuration and delivery boundaries.
Return to the [wiki index](../../index.md).
