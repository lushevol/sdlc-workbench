---
sources: ["summaries/KT-release-operations.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md"]
type: "Product"
description: "Desktop runtime and platform product referenced in Portal materials for application hosting and onboarding phases."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# OpenFin

## What it is

OpenFin is a desktop runtime and platform product referenced in the Portal materials as the environment that hosts applications and mediates some cross-application behavior. The interoperability topic describes a desktop agent that exposes an API to applications in its context, a platform provider as the coordination hub, platform windows that frame the interface, and platform views that contain application content. These are documented architecture terms, not verified descriptions of a current deployment.

Earlier architecture material mentioned OpenFin only as a planning item whose requirements were still being refined. The newer topic supplies more detail but does not resolve ownership, approval, or delivery status.

## Mentions in the source material

### Architecture and scope

The briefing limits its stated business scope to application rendering and interoperability. Third-party integrations and native adapters are outside that stated plan. It states that the Ratan provider customizes intent routing.

OpenFin is paired in the materials with [[entities/fdc3]], which supplies the documented context and intent abstraction. The proof of concept describes Portal opening, tile opening, theme changes, and message broadcast through this combination.

### Runtime and manifest configuration

The briefing distinguishes the Runtime from the Runtime Version Manager. A manifest configures an application or platform bootstrap and its requested runtime. The briefing records `stable-v41` as its runtime strategy. This is a historical declaration; current support, installation, and approval were not verified.

### Interoperability and tile navigation

The Portal cooperation guide describes intent navigation from a source tile to a target tile, where the source supplies context that becomes the target's initial data. OpenFin is the desktop environment in which that interaction is described. See [[concepts/intent-based-application-interoperability]] and [[concepts/portal-tile-workspace-model]].

The example contract uses an application channel named `fmchannel`, with listeners for provider, React application, and Portal. It documents `openTile` and `changeTheme` requests, and a launch example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent. The intent and context names are not yet reconciled into one approved schema; see [[concepts/interoperability-contract-governance]].

### Authentication handoff

The proof of concept describes provider authentication followed by application launches that pass a provider token in URL parameters. It presents this as a way to avoid another login prompt and simplifies the provider UI for the POC. A real provider is said to run hidden after authentication. No production authentication design, security approval, or token-handling verification was inspected; see [[concepts/cross-application-authentication-handoff]].

### Compatibility observations

The technical-issue page reports that two FDC3 libraries did not exchange broadcast messages in its POC. It reports intent errors with one library and successful intent handling with the other. Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. These are reported POC observations, not a supported compatibility guarantee.

### Onboarding phases

The release operations topic cites the OpenFin briefing as separating technical onboarding from business user onboarding. This mirrors the broader distinction between technical deployment and business activation described in that topic. The briefing's month-based timelines omit the year and cannot establish current rollout status; the separation is a documented planning concept without evidence of completed onboarding for any specific tenant. See [[summaries/KT-release-operations]] and [[concepts/tenant-production-readiness]].

## Status and evidence limits

The materials now describe OpenFin architecture, a POC, a later briefing, and a reference in release planning, but they still do not establish an approved production capability. In particular:

- No original revisions, approval attachments, or completed execution records were supplied.
- The briefing's month-based timelines omit the year and cannot establish current rollout status.
- Deployed versions, current support, and installation status remain unresolved.
- Missing archives and screenshots prevent reproduction of the POC from this copy alone.
- No actual desktop agent, provider, application, or compatibility test ran during ingestion.
- OpenFin's relationship to the existing [[entities/fmo-post-trade-portal]] shell — whether it replaces, wraps, or coexists with it — is not settled in these materials.

This entity page should be revised when an accepted requirement, design record, or authenticated deployment record for OpenFin is located.

## Related pages

- [[summaries/KT-application-interoperability]] — the topic that records OpenFin architecture, POC behavior, and evidence limits.
- [[summaries/KT-architecture-evolution]] — the earlier topic that listed OpenFin only as a planning item.
- [[summaries/KT-release-operations]] — the release planning topic that references the OpenFin briefing's separation of technical and business onboarding.
- [[entities/fmo-post-trade-portal]] — the portal whose deployment and interoperability materials reference OpenFin.
- [[entities/fdc3]] — the context and intent abstraction paired with OpenFin in these materials.
- [[concepts/intent-based-application-interoperability]] — the cross-application intent and context model.
- [[concepts/interoperability-contract-governance]] — the unresolved schema and contract questions around the example messages.
- [[concepts/cross-application-authentication-handoff]] — the POC token handoff and its open security questions.
- [[concepts/portal-tile-workspace-model]] — the tile and workspace hosting model that a desktop-container decision would affect.
- [[concepts/application-ownership]] — the ownership questions that an unassigned or unapproved product raises.
- [[concepts/tenant-production-readiness]] — the broader readiness model that distinguishes technical from business activation.