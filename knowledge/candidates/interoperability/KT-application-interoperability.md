---
type: KnowledgeTopic
id: KT-application-interoperability
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/OpenFin/1. Overview/page.md
  revision: sha256:ff546826f3f04dea2c9cd44d1d4b8ce7cb95c3d5889179ce440e92617fb2971e
  sha256: ff546826f3f04dea2c9cd44d1d4b8ce7cb95c3d5889179ce440e92617fb2971e
- resource: knowledge/raw/confluence/FM TPT UI Guild/OpenFin/2. Getting Started/page.md
  revision: sha256:c441671d80ab719e3f8a2d8fd211e9f54af4cc0d71257284f883e8e3b1e84b18
  sha256: c441671d80ab719e3f8a2d8fd211e9f54af4cc0d71257284f883e8e3b1e84b18
- resource: knowledge/raw/confluence/FM TPT UI Guild/OpenFin/3. Application Interoperability/page.md
  revision: sha256:46cd29f49215cf8cb7468f7ec403e5ce57a83c82519ec3165802df6e63007e31
  sha256: 46cd29f49215cf8cb7468f7ec403e5ce57a83c82519ec3165802df6e63007e31
- resource: knowledge/raw/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md
  revision: sha256:839b37307c84eccc1e46a2c16055786c5ce02314feae7f71c7f5d8d2a1b2a6a9
  sha256: 839b37307c84eccc1e46a2c16055786c5ce02314feae7f71c7f5d8d2a1b2a6a9
- resource: knowledge/raw/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md
  revision: sha256:89b668f9618f7bff06e40901c8b8abf135994e6322f70f856e5bee94da96e756
  sha256: 89b668f9618f7bff06e40901c8b8abf135994e6322f70f856e5bee94da96e756
- resource: knowledge/raw/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md
  revision: sha256:e8ec00d527cdf7ef33f2b901ddca98d7df4870d30f130cfc434b80b6d16255df
  sha256: e8ec00d527cdf7ef33f2b901ddca98d7df4870d30f130cfc434b80b6d16255df
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md
  revision: sha256:71c8c3952ed4d36f3b6f1ec5b099aa3edf5a11bc13993f28c1d064d5ddaab978
  sha256: 71c8c3952ed4d36f3b6f1ec5b099aa3edf5a11bc13993f28c1d064d5ddaab978
generated:
  by: agent:codex
  at: '2026-10-15T00:38:52.657060+00:00'
verified: []
classification: interoperability
scope: Portal-mediated tile navigation, caller/provider cooperation, OpenFin architecture, FDC3 examples, and technical and business release phases.
summary: Portal interoperability requires agreed context, caller and provider readiness, and coordinated delivery; OpenFin examples retain separate POC evidence limits.
related:
- KT-portal-purpose
- KT-frontend-composition
- KT-authentication-and-sessions
- KT-release-operations
- KT-architecture-evolution
- single-ui-web
- single-ui-workspace-composition
open_questions:
- Which caller/provider context contracts and readiness gates govern each Portal interoperability feature?
- Which OpenFin and FDC3 capabilities are delivered in each environment?
- Which intent names, context schemas, and versions form the approved integration contract?
- How does production authentication avoid unsafe token handling across application launches?
- Which tests establish cross-library and cross-application interoperability?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Portal application interoperability and OpenFin context

## Scope

This topic connects Portal intent navigation, desktop architecture, shared context, authentication handoff, and coordinated delivery.
The supplied materials include a Portal cooperation guide, an explicit proof of concept, and a later briefing.
They do not establish the delivered status of every described capability.

## Summary

The documented objective is sharing context and requesting actions across financial applications.
OpenFin supplies the desktop environment in these materials.
FDC3 supplies the documented context and intent abstraction.
The proof of concept describes Portal opening, tile opening, theme changes, and message broadcast.
Later planning separates technical onboarding from business user adoption.

## Documented knowledge

### Purpose and architecture terms

The overview seeks to avoid repeated data entry and connect actions across applications.
A desktop agent exposes an API to applications in its context.
The documentation describes a platform provider as the coordination hub.
Platform windows frame the interface, while platform views contain application content.
The briefing states that the Ratan provider customizes intent routing.
These statements describe the supplied architecture, without verifying current deployed components.
[Overview, objective and FDC3 parts, lines 1–21](<../../raw/confluence/FM TPT UI Guild/OpenFin/1. Overview/page.md#L1>)
[Getting Started, desktop agent and platform components, lines 1–28](<../../raw/confluence/FM TPT UI Guild/OpenFin/2. Getting Started/page.md#L1>)
[Briefing, platform provider, lines 111–125](<../../raw/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L111>)

The briefing limits its stated business scope to application rendering and interoperability.
Third-party integrations and native adapters are outside that stated plan.
It distinguishes the Runtime from the Runtime Version Manager.
The manifest configures an application or platform bootstrap and its requested runtime.
The briefing records `stable-v41` as its runtime strategy.
This is a historical declaration, without verification of current support, installation, or approval.
[Briefing, scope, runtime, and manifest, lines 32–86](<../../raw/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L32>)

### Portal-mediated tile navigation

The interoperability guide describes intent navigation from a source tile to a target tile.
The source supplies context that becomes the target's initial data.
The screen then transitions to the target tile.
These are documented interaction semantics, without inspected implementation or execution evidence.
[Interoperability guide, intent navigation, lines 1–9](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L1>)

The guide assigns business demand and caller implementation to the requesting tenant team.
Portal receives standardized intents and provides routing, access control, context passing, and dispatch.
The provider team implements the receiving handler, consumes context, and performs the business action.
It can optionally return a result or status.
These responsibility declarations do not establish operational ownership or passing access-control enforcement.
[Interoperability guide, cooperation model, lines 27–38](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L27>)

A completed caller alone cannot enable the full feature under this guide.
The provider also needs intent registration, a handler, agreed context, authorization readiness, testing, and production deployment.
The guide therefore treats interoperability as a joint delivery dependency.
Its development code blocks are empty, and its diagrams are absent from this supplied copy.
The guide supplies cooperation intent, without a runnable integration contract.
[Interoperability guide, development and readiness, lines 13–25 and 40–60](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L13>)

### Contexts, intents, and actions

The overview defines context data as information shared between applications.
It defines intents as requests for another application to perform functionality.
The proof of concept uses these concepts to open Portal, open a tile, change theme, and broadcast messages.
Opening a new Portal view differs from opening a workspace inside an existing view.
The supplied demonstration procedure describes both paths.
[Overview, FDC3 parts and use cases, lines 15–31](<../../raw/confluence/FM TPT UI Guild/OpenFin/1. Overview/page.md#L15>)
[Interoperability POC, functional use cases, lines 25–71](<../../raw/confluence/FM TPT UI Guild/OpenFin/3. Application Interoperability/page.md#L25>)

The example contract uses application channel `fmchannel`.
Its listener names include `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`.
The documented `openTile` request carries container, module, and tile identifiers, or a target URL.
The documented `changeTheme` request carries a theme value.
These names describe example integration messages, without establishing an approved production schema.
[FDC3 contract, channel and listener table, lines 1–5](<../../raw/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1>)

The example shares one handler between context and intent listeners.
That handler branches on `getToken`, `openTile`, and `changeTheme`.
Its view-creation example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent.
The different intent names and context entries require reconciliation before treating this example as an integration specification.
[FDC3 contract, listener and launch examples, lines 7–55](<../../raw/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L7>)

### Authentication handoff boundary

The POC describes provider authentication followed by application launches using a provider token in URL parameters.
It presents that handoff as a way to avoid another login prompt.
The document explicitly simplifies the provider UI for the POC.
It says a real provider should run hidden after authentication.
No production authentication design, security approval, or token-handling verification was inspected during ingestion.
[Interoperability POC, provider authentication, lines 1–23](<../../raw/confluence/FM TPT UI Guild/OpenFin/3. Application Interoperability/page.md#L1>)

### Compatibility observations

The technical issue page reports that two FDC3 libraries did not exchange broadcast messages in its POC.
It reports intent errors with one library and successful intent handling with the other.
Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents.
These are reported POC observations, without current reproduction or a supported compatibility guarantee.
The referenced screenshots and source archives are absent from this supplied copy.
[Technical issue, observations and workaround, lines 1–29](<../../raw/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L1>)
[Getting Started, source archives, lines 30–36](<../../raw/confluence/FM TPT UI Guild/OpenFin/2. Getting Started/page.md#L30>)

### Adoption and release phases

The briefing describes separate business cases for viewing trade details and remaining amounts across applications.
Its phase table separates production identity verification, blotter onboarding, and business user onboarding.
Those are distinct milestones.
The month-based timelines provide no year in that table.
The briefing records approval and prioritization claims, without supplied approval attachments or completed execution records.
This topic therefore preserves them as reported claims and plans.
[Briefing, approval claims, business cases, and phases, lines 135–163](<../../raw/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L135>)

## Connections

[Frontend composition](../architecture/KT-frontend-composition.md) supplies the Portal container, module, tile, and workspace context.
[Authentication and sessions](../security/KT-authentication-and-sessions.md) supplies related session concepts.
[Release operations](../operations/KT-release-operations.md) distinguishes technical deployment from business activation.

Registry service `single-ui-web` and capability `single-ui-workspace-composition` provide related Portal context.
These connections do not prove that those assets implement the example FDC3 messages.
The supplied registry does not establish an approved OpenFin contract.

## Evidence limits

Local hashes identify supplied document bytes.
Original revisions, approval evidence, deployed versions, and current applicability remain unresolved.
Missing archives and screenshots prevent reproduction of the POC from this copy alone.
No desktop agent, provider, application, or compatibility test ran during ingestion.
No credential, token value, personal identifier, or private contact detail is reproduced here.

## Open questions

| Issue and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Caller/provider cooperation is described without populated development examples. See interoperability guide, lines 13–25 and 40–60. | Joint readiness cannot be inferred from caller completion. | unknown | Agree provider capacity, context contracts, authorization checks, and release evidence. |
| Sources mix POC examples, approval claims, and planned phases. See interoperability, line 9, and briefing, lines 135–163. | Intended capability could be mistaken for delivered behavior. | unknown | Record delivered features and retained execution evidence by environment. |
| Contract table and launch example use different intent and context names. See FDC3 contract, lines 1–5 and 43–49. | Integrations could request an unhandled action. | unknown | Agree one versioned schema and verify producer and listener compatibility. |
| POC launches include provider tokens in URLs. See interoperability, lines 18–23. | Production token exposure and trust boundaries remain unresolved. | unknown | Review production authentication handoff and approved token transport. |
| POC reports library isolation and intent failures. See technical issue, lines 8–29. | Cross-application behavior could depend on an undocumented workaround. | unknown | Reproduce compatibility using the selected supported runtime and libraries. |
| Phase deadlines omit the year and completion evidence. See briefing, lines 157–163. | Planning context cannot establish current rollout status. | unknown | Confirm dated technical milestones and separate business acceptance records. |
