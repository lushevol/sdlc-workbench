---
sources: ["summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md"]
type: "Product"
description: "Cross-application interoperability standard used with OpenFin in the FMO Post Trade Portal."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# FDC3

## What it is

FDC3 is named in the portal materials as a cross-application interoperability capability. In [[summaries/KT-portal-purpose]], it appears in the capability-boundary table under interoperability and is explicitly marked as **in progress**. It is associated with the [[entities/fmo-post-trade-portal]] platform.

In [[summaries/KT-application-interoperability]], FDC3 supplies the documented context and intent abstraction. Context data is information shared between applications. Intents are requests for another application to perform functionality. [[entities/openfin]] supplies the desktop environment in those materials.

## Key facts from the source

- The portal capabilities page lists cross-application interaction, with FDC3 marked as in progress.
- The draft principles emphasize interoperability among their focus areas.
- The supplied material does not establish deployed or tested FDC3 coverage.
- The deployment proposal describes future changes without an approval record. FDC3 should not be treated as a current implementation fact from this source alone.
- The interoperability sources provide example API and channel details, including `fdc3InteropApi` value `1.2`, without establishing an approved or deployed FDC3 version or production contract.

## Documented interoperability details

The proof of concept uses FDC3 concepts to open Portal, open a tile, change theme, and broadcast messages. Opening a new Portal view differs from opening a workspace inside an existing view, and the demonstration procedure describes both paths.

The example contract uses application channel `fmchannel`. Its listener names include `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`. The documented `openTile` request carries container, module, and tile identifiers, or a target URL. The documented `changeTheme` request carries a theme value. The example shares one handler between context and intent listeners, and that handler branches on `getToken`, `openTile`, and `changeTheme`. Its view-creation example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent.

These names describe example integration messages. They do not establish an approved production schema. The different intent names and context entries require reconciliation before the example can be treated as an integration specification. See [[concepts/intent-based-application-interoperability]] and [[concepts/interoperability-contract-governance]].

The technical-issue page reports that two FDC3 libraries did not exchange broadcast messages in its POC. It reports intent errors with one library and successful intent handling with the other. Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. This is a reported POC observation, without current reproduction or a supported compatibility guarantee.

The POC launches pass a provider token in URL parameters after provider authentication. That handoff is presented as a way to avoid another login prompt, and no production authentication design or security approval was inspected. See [[concepts/cross-application-authentication-handoff]].

## Status and evidence limits

FDC3 is a stated area of work, not confirmed deployed functionality. It belongs to the draft and roadmap side of the material and must stay separate from the current capability inventory. The accountable owner and acceptance status remain unconfirmed.

No desktop agent, provider, application, or compatibility test ran during ingestion. Missing archives and screenshots prevent reproduction of the POC from this copy alone. Original revisions, approval evidence, deployed versions, and current applicability remain unresolved.

## Related pages

- [[summaries/KT-portal-purpose]]
- [[summaries/KT-application-interoperability]]
- [[entities/fmo-post-trade-portal]]
- [[entities/openfin]]
- [[concepts/intent-based-application-interoperability]]
- [[concepts/interoperability-contract-governance]]
- [[concepts/cross-application-authentication-handoff]]
- [[concepts/portal-tile-workspace-model]]
- [[concepts/microfrontend-layering]]
- [[concepts/portal-entry-and-tile-authorization]]

See also: [[summaries/KT-architecture-evolution]]