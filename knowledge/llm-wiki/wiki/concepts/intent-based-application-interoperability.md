---
type: "Concept"
sources: ["summaries/KT-application-interoperability.md"]
description: "Portal-mediated sharing of context and intent requests between applications via FDC3 on OpenFin."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Intent-Based Application Interoperability

Intent-based application interoperability lets one application ask another to perform an action, and pass the context that the action needs. In the Portal material, a source tile sends an intent to the Portal, and a target tile receives the context as initial data. [[entities/fdc3]] supplies the abstraction for context and intents, and [[entities/openfin]] supplies the desktop environment.

## Mechanism

A desktop agent exposes an API to applications in its context. The documentation describes a platform provider as the coordination hub. Platform windows frame the interface, and platform views contain application content.

For tile navigation, the source supplies context that becomes the target tile's initial data. The screen then transitions to the target tile. Portal receives standardized intents and provides routing, access control, context passing, and dispatch.

The documented POC use cases are: open a new Portal view, open a tile, change theme, and broadcast a message. Opening a new Portal view differs from opening a workspace inside an existing view.

## Caller and provider responsibilities

The documented model assigns three sets of responsibilities:

- The requesting tenant team owns business demand and the caller implementation.
- [[entities/fmo-post-trade-portal]] receives standardized intents and provides routing, access control, context passing, and dispatch.
- The provider team registers the intent, implements the receiving handler, consumes context, performs the business action, and may return a result or status.

A completed caller alone cannot enable the feature. The provider also needs intent registration, a handler, agreed context, authorization readiness, testing, and production deployment. Interoperability is therefore a joint delivery dependency, not a one-sided change. See [[concepts/application-ownership]] for how ownership boundaries are assigned.

## Example contract

The POC contract uses application channel `fmchannel`. Listener names include `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`. One handler is shared between context and intent listeners, and it branches on `getToken`, `openTile`, and `changeTheme`.

`openTile` carries container, module, and tile identifiers, or a target URL. `changeTheme` carries a theme value. The launch example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent.

The intent and context names are not fully consistent between the contract table and the launch example. Teams must reconcile them before treating the example as an approved integration specification. [[concepts/interoperability-contract-governance]] covers how such schemas, versions, and approvals should be controlled.

## Dependencies on Portal and session design

Intent navigation depends on the Portal container, module, tile, and workspace identifiers described in [[concepts/portal-tile-workspace-model]]. Access control during dispatch relates to [[concepts/portal-entry-and-tile-authorization]].

The POC passes a provider token in URL parameters to avoid a second login prompt. It also states that a real provider should run hidden after authentication. Production token transport and trust boundaries remain unresolved, which links this concept to [[concepts/cross-application-authentication-handoff]].

## Known technical limits

The technical-issue note reports that two FDC3 libraries did not exchange broadcast messages in the POC. It reports intent errors with one library and successful intent handling with the other. The workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. This is a reported POC observation, not a supported compatibility guarantee.

The briefing declares `stable-v41` as its runtime strategy. It separates the Runtime from the Runtime Version Manager. These are historical declarations, and current support and approval are not verified.

## Delivery model

The later briefing separates production identity verification, blotter onboarding, and business user onboarding as distinct milestones. Its timelines omit the year, and its approval claims have no supplied attachments. Intended capability must not be mistaken for delivered behavior.

## Open questions

- Which intent names, context schemas, and versions form the approved integration contract?
- Which caller and provider readiness gates apply to each feature?
- How does production authentication avoid unsafe token handling across launches?
- Which tests establish cross-library and cross-application interoperability?

## Related pages

- [[summaries/KT-application-interoperability]]
- [[concepts/interoperability-contract-governance]]
- [[concepts/cross-application-authentication-handoff]]
- [[concepts/portal-tile-workspace-model]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/application-ownership]]
- [[entities/fdc3]]
- [[entities/openfin]]