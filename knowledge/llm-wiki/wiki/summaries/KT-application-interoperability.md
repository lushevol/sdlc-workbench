---
type: "Summary"
description: "Portal interoperability via FDC3/OpenFin: caller-provider duties and evidence limits."
doc_type: short
full_text: "sources/KT-application-interoperability.md"
---

> Derived from [KT-application-interoperability, version 2](../../../records/candidates/interoperability/KT-application-interoperability.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Portal application interoperability and OpenFin context

This topic summarizes Portal-mediated application interoperability: how a source tile requests an action from a target tile, how context moves between applications, and what the caller and provider must each deliver. The supplied materials combine design guidance, a proof of concept (POC), an example FDC3 contract, technical-issue notes, and a later business briefing.

## Core idea

Portal receives standardized intents and provides routing, access control, context passing, and dispatch. A caller tile supplies context that becomes the target tile's initial data, and the screen then transitions to the target. [[entities/openfin]] is the desktop environment in these materials. [[entities/fdc3]] is the documented abstraction for shared context and intents.

The POC describes opening Portal, opening a tile, changing theme, and broadcasting messages. It distinguishes opening a new Portal view from opening a workspace inside an existing view.

## Key concepts

- [[concepts/intent-based-application-interoperability]] — sharing context and requesting actions across financial applications.
- [[entities/fdc3]] — context data shared between applications and intents that request another application to perform functionality.
- [[entities/openfin]] — the desktop agent API, platform provider, platform windows, platform views, Runtime, Runtime Version Manager, and manifest configuration.
- [[concepts/portal-tile-workspace-model]] — intent-based navigation from a source tile to a target tile with context handoff.
- [[concepts/application-ownership]] — the split between requesting-tenant caller work and provider-side intent handling.
- [[concepts/cross-application-authentication-handoff]] — the POC token-in-URL handoff and unresolved production security questions.
- Technical versus business release phases — separation of identity verification, onboarding, and business user adoption.

## Findings

### Portal navigation and responsibilities

The cooperation guide assigns business demand and caller implementation to the requesting tenant team. Portal receives standardized intents and provides routing, access control, context passing, and dispatch. The provider team registers the intent, implements the receiving handler, consumes context, performs the business action, and can optionally return a result or status. See [[concepts/interoperability-contract-governance]] for the related contract concerns.

A completed caller alone cannot enable the full feature. The provider also needs intent registration, a handler, agreed context, authorization readiness, testing, and production deployment. The guide therefore treats interoperability as a joint delivery dependency. Its development code blocks are empty and its diagrams are absent from the supplied copy, so it supplies cooperation intent rather than a runnable integration contract.

### Example contract and technical gaps

The example contract uses application channel `fmchannel`. Listener names include `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`. The documented `openTile` request carries container, module, and tile identifiers or a target URL. `changeTheme` carries a theme value. One handler is shared between context and intent listeners and branches on `getToken`, `openTile`, and `changeTheme`. The launch example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent. These names and context entries need reconciliation before the example can be treated as an approved integration specification.

### Authentication, compatibility, and release

The POC describes provider authentication followed by application launches that pass a provider token in URL parameters. It presents this as a way to avoid another login prompt. The document simplifies the provider UI for the POC and says a real provider should run hidden after authentication. No production authentication design, security approval, or token-handling verification was inspected.

The technical-issue page reports that two [[entities/fdc3]] libraries did not exchange broadcast messages in its POC. It reports intent errors with one library and successful intent handling with the other. Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. This is a reported POC observation, not a supported compatibility guarantee.

The later briefing limits its stated business scope to application rendering and interoperability. Third-party integrations and native adapters are outside that stated plan. It distinguishes the Runtime from the Runtime Version Manager, and it records `stable-v41` as its runtime strategy. It also separates production identity verification, blotter onboarding, and business user onboarding as distinct milestones. Its month-based timelines omit the year, and its approval and prioritization claims have no supplied attachments or completed execution records.

## Evidence limits

Local hashes identify supplied document bytes. Original revisions, approval evidence, deployed versions, and current applicability remain unresolved. Missing archives and screenshots prevent reproduction of the POC from this copy alone. No desktop agent, provider, application, or compatibility test ran during ingestion. No credential, token value, personal identifier, or private contact detail is reproduced here.

## Open questions

- Which caller/provider context contracts and readiness gates govern each Portal interoperability feature?
- Which OpenFin and FDC3 capabilities are delivered in each environment?
- Which intent names, context schemas, and versions form the approved integration contract?
- How does production authentication avoid unsafe token handling across application launches?
- Which [[entities/fdc3]] tests establish cross-library and cross-application interoperability?

## Related topics

[[summaries/KT-frontend-composition]] supplies the Portal container, module, tile, and workspace context. [[concepts/single-ui-sdk-authentication]] supplies related session concepts. Technical deployment versus business activation is a related distinction. [[summaries/KT-architecture-evolution]] provides broader platform context.

## Related Concepts
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/shared-dependency-governance]]
- [[concepts/microfrontend-layering]]
- [[concepts/identity-provider-delegation]]

## Entities
- [[entities/fmo-post-trade-portal]]
- [[entities/mfe-cashflow-blotter]]
- [[entities/portal-team]]
- [[entities/single-ui-bff]]
