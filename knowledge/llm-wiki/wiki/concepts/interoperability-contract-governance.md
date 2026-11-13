---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-application-interoperability.md"]
description: "How intent names, context schemas, versions, and readiness gates are agreed and verified across caller and provider teams."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical basis: [contexts, intents and actions](../../../records/candidates/interoperability/KT-application-interoperability.md#contexts-intents-and-actions) and [adoption phases](../../../records/candidates/interoperability/KT-application-interoperability.md#adoption-and-release-phases).

# Interoperability Contract Governance

Interoperability Contract Governance is the set of agreements and evidence that let one application reliably request an action from another. It covers the named intents, the shape of the shared context, the version of the contract in force, and the readiness gates each side must pass before a feature is considered delivered. In the supplied materials the governance is declared in principle but not yet demonstrated in practice.

## The contract surface

[[entities/fdc3]] supplies the abstraction: context data shared between applications, and intents that request another application to perform functionality. [[entities/openfin]] supplies the desktop environment in which those requests are routed. A contract therefore has to pin down at least four things:

- **Intent names** — which action a caller may request.
- **Context schemas** — which fields the caller sends and the provider expects.
- **Versions** — which contract revision, and which API level, both sides implement.
- **Listeners and channels** — the addresses on which requests and broadcasts are delivered.

## What the source documents reveal

The example contract uses application channel `fmchannel`, with listener names including `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`. The documented `openTile` request carries container, module, and tile identifiers or a target URL; `changeTheme` carries a theme value. A single handler is shared between context and intent listeners and branches on `getToken`, `openTile`, and `changeTheme`. The launch example declares API value `1.2` and an `OpenTile` intent.

The contract table and the launch example do not agree on intent and context names. This is the central governance finding: an example is not a specification. Until one versioned schema is agreed and both producer and listener compatibility are verified, an integration can request an action that no handler answers. See [[summaries/KT-application-interoperability]] for the underlying evidence review.

## Readiness gates

Governance is not only naming. The cooperation guide treats interoperability as a joint delivery dependency. Portal receives standardized intents and provides routing, access control, context passing, and dispatch. The requesting tenant team owns business demand and the caller implementation. The provider team registers the intent, implements the handler, consumes context, performs the business action, and may return a result or status.

A completed caller alone does not enable the feature. The provider must also have intent registration, a handler, agreed context, authorization readiness, testing, and production deployment. Because the guide's development code blocks are empty and its diagrams absent from the supplied copy, these gates are stated as intent rather than demonstrated as a runnable contract.

## Verification and evidence

Reported POC observations show why verification belongs in governance, not in release notes. Two FDC3 libraries did not exchange broadcast messages, one library produced intent errors, and the workaround split duties between `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. The documented POC workaround does not establish a supported library contract. Confirm the chosen versions, ownership, and retained compatibility execution before relying on it.

Governance should therefore record, per environment, which features are delivered and retain the execution evidence: compatibility tests across libraries and applications, and dated technical milestones separate from business acceptance records. The briefing's month-based phase table omits the year, and its approval claims carry no attachments.

## Boundaries with adjacent concerns

- [[concepts/intent-based-application-interoperability]] describes the interaction model this governance constrains.
- [[concepts/portal-entry-and-tile-authorization]] covers access control; the contract must state whether the portal enforces it on the caller's behalf or the provider does.
- [[concepts/cross-application-authentication-handoff]] covers token transport, which the POC left unresolved by placing provider tokens in URL parameters.
- [[concepts/application-ownership]] records the stated responsibility split; the accountable owner and sign-off authority for a versioned interoperability contract remain unresolved.
- [[concepts/shared-dependency-governance]] is the analogous problem for library versions rather than message versions.

## Open issues

Which intent names, context schemas, and versions form the approved contract is unresolved. Which caller/provider context contracts and readiness gates apply to each feature is unresolved. Which tests establish cross-library and cross-application interoperability is unresolved. The supplied registry does not establish an approved OpenFin contract, and the connections to the [[entities/fmo-post-trade-portal]] and the [[entities/portal-team]] do not prove that those assets implement the example messages.

See also: [[summaries/KT-release-operations]]