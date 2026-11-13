---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-release-operations.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md"]
description: "Portal tile/workspace model with intent-mediated navigation and context handoff."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Portal Tile and Workspace Model

The portal tile and workspace model is the user-facing composition pattern described in [[summaries/KT-portal-purpose]]. A user enters the [[entities/fmo-post-trade-portal]] once, authenticates, and opens application views called tiles inside one or more workspaces. The portal supplies the shared shell and composition context; tenant applications keep their domain functions. Tiles can also request actions from one another through portal-mediated intents, with context passed as the target tile's initial data.

## Core elements

| Element | Role in the model |
| --- | --- |
| Entry | A common application entry point for post-trade users. |
| Identity | SSO, MFA, and session renewal before workspace use. |
| Tile | An application view that a user opens in a workspace. |
| Workspace | A user area that holds opened tiles; the documented flow supports multiple workspaces. |
| Container | An application-owned module or the shared base that supplies common context. The role must be made explicit. |
| Import map | A mapping used to locate modules for dynamic loading. |
| Tenant application | A domain application integrated into the shared portal. |
| Intent | A standardized request for another application to perform an action, such as opening a tile or changing theme. |
| Context | Data supplied by a caller that becomes the target tile's initial data. |
| Caller | The requesting tenant team's application or tile that raises the intent. |
| Provider | The receiving team's application that registers the intent, consumes context, and performs the business action. |
| Desktop agent | The environment API that exposes context and intent services to applications; [[entities/openfin]] is the documented environment. |

## Flow

The documented sequence is: one entry, authentication, tile selection, and multiple workspaces. Module loading uses import maps. Session renewal connects to session control.

For intent navigation, a source tile supplies context, the portal routes the request, the target tile receives the context as initial data, and the screen transitions to the target. The proof of concept describes opening the portal, opening a tile, changing theme, and broadcasting messages. It distinguishes opening a new portal view from opening a workspace inside an existing view.

Cross-application interaction through [[entities/fdc3]] is described as in progress, not complete. The example contract uses application channel `fmchannel`; listener names include `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`. The documented `openTile` request carries container, module, and tile identifiers, or a target URL. The documented `changeTheme` request carries a theme value. A launch example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent. These names and context entries need reconciliation before the example can be treated as an approved integration specification.

## Ownership and composition

The model separates common UI work from application teams' business delivery. Application teams retain domain functions; the platform supplies shared themes, shared components, dynamic module loading, tiles, and workspaces. This division is closest to [[concepts/application-ownership]] and [[concepts/microfrontend-layering]]. The composition vocabulary in adjacent pages includes [[entities/mfe-base]], [[entities/mfe-root-config]], [[entities/single-spa]], and [[entities/systemjs]]; the purpose topic does not confirm each component as deployed.

Intent navigation adds a caller/provider split. The requesting tenant team owns business demand and caller implementation. The portal receives standardized intents and provides routing, access control, context passing, and dispatch. The provider team registers the intent, implements the receiving handler, consumes context, performs the business action, and can optionally return a result or status.

A completed caller alone cannot enable the full feature. The provider also needs intent registration, a handler, agreed context, authorization readiness, testing, and production deployment. Interoperability is therefore a joint delivery dependency, which relates to [[concepts/interoperability-contract-governance]].

## Access and integration

The supplied capability map describes tile eligibility in [[entities/ems2]] role terms. The current candidate migration intent requires each tile to select EMS2 or CES admission independently, while the shared `hasPermission(code)` provider-union check remains separate from tile admission. See the [canonical provider boundary](../../../records/candidates/security/KT-ces-migration-parity.md#independent-tile-provider-selection), [[concepts/portal-entry-and-tile-authorization]], and [[concepts/entitlement-retrieval]]. The cooperation guide says portal routing provides access control, but the supplied copy does not establish that access-control enforcement is in place.

Tenant UI and API traffic are described as routed through the portal's [[entities/nginx]] boundary, which relates to [[concepts/portal-ingress-path]]. Frontend onboarding of a tenant application is a separate concern described in [[concepts/frontend-onboarding]].

The proof of concept describes provider authentication followed by application launches that pass a provider token in URL parameters. It presents this as a way to avoid another login prompt and simplifies the provider UI for the proof of concept; a real provider should run hidden after authentication. No production authentication design, security approval, or token-handling verification was inspected. See [[concepts/cross-application-authentication-handoff]] and [[concepts/single-ui-sdk-authentication]].

The technical-issue page reports that two FDC3 libraries did not exchange broadcast messages in its proof of concept. It reports intent errors with one library and successful intent handling with the other. Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. This is a reported proof-of-concept observation, not a supported compatibility guarantee.

## Limits

This is a documented model, not evidence of deployed or tested coverage. The portal introduction remains under edit; draft principles and the 2026–2027 deployment proposal are not accepted scope. Development code blocks in the cooperation guide are empty, and its diagrams are absent from the supplied copy. Missing archives and screenshots prevent reproduction of the proof of concept from this copy alone. Later briefing approval and prioritization claims have no supplied approval attachments or completed execution records, and its phase timelines omit the year. No desktop agent, provider, application, or compatibility test ran during ingestion. The sources do not provide an approval record, complete application inventory, or retained execution evidence.

## Related pages

- [[summaries/KT-portal-purpose]]
- [[summaries/KT-application-interoperability]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/intent-based-application-interoperability]]
- [[concepts/interoperability-contract-governance]]
- [[concepts/cross-application-authentication-handoff]]
- [[concepts/microfrontend-layering]]
- [[concepts/application-ownership]]
- [[concepts/entitlement-retrieval]]
- [[concepts/frontend-onboarding]]
- [[concepts/portal-ingress-path]]
- [[concepts/single-ui-sdk-authentication]]
- [[entities/fmo-post-trade-portal]]
- [[entities/ems2]]
- [[entities/fdc3]]
- [[entities/openfin]]
- [[entities/nginx]]

See also: [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-release-operations]]