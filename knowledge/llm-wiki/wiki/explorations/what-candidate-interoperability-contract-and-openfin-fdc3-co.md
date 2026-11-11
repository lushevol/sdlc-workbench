---
query: "What candidate interoperability contract and OpenFin/FDC3 context readiness are required between caller and provider applications?"
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

## Short answer

The wiki records a **candidate** contract and a **set of stated readiness gates** — but no approved one. The materials declare the governance in principle and never demonstrate it in practice ([[concepts/interoperability-contract-governance]], [[summaries/KT-application-interoperability]]).

## Candidate interoperability contract (as documented)

Four things must be pinned down for any caller/provider pair: **intent names, context schemas, versions, and listeners/channels** ([[concepts/interoperability-contract-governance]]).

The example contract (explicitly an example, not a spec) contains:

- **Application channel:** `fmchannel`
- **Listeners:** `fmchannel.provider`, `fmchannel.reactapp`, `fmchannel.fmoportal`
- **`openTile`** request — carries container, module, and tile identifiers, *or* a target URL
- **`changeTheme`** request — carries a theme value
- **`getToken`** — handled by the same shared handler that branches across context and intent listeners
- **Launch example:** declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent

Critical caveat: the contract table and the launch example **disagree on intent and context names**. So "an example is not a specification" — until one versioned schema is agreed and producer/listener compatibility verified, a caller can request an action no handler answers ([[concepts/intent-based-application-interoperability]], [[entities/fdc3]]).

## Readiness gates: who owes what

**Caller (requesting tenant team):** owns the business demand and the caller implementation. It supplies context that becomes the target tile's initial data, then the screen transitions to the target.

**Provider team:** registers the intent, implements the receiving handler, consumes context, performs the business action, and may optionally return a result or status.

**Portal:** receives standardized intents and provides routing, access control, context passing, and dispatch.

**Key rule:** a completed caller alone cannot enable the feature. The provider must independently have intent registration, a handler, agreed context, authorization readiness, testing, and production deployment. Interoperability is therefore a **joint delivery dependency**, not a one-sided change (see [[concepts/portal-tile-workspace-model]], [[concepts/application-ownership]]).

## OpenFin / FDC3 readiness status

- FDC3 cross-application interaction is listed as **in progress**, not complete — stated work on the draft/roadmap side, not confirmed deployed functionality ([[entities/fdc3]]).
- OpenFin runtime strategy recorded as **`stable-v41`**, with Runtime distinguished from the **Runtime Version Manager**; manifest configures bootstrap and requested runtime. These are *historical declarations* — current support, installation, and approval unverified ([[entities/openfin]]).
- **Compatibility gap:** two FDC3 libraries did not exchange broadcast messages in the POC; one produced intent errors, the other handled intents successfully. Workaround splits duties: `fdc3-2.1` for broadcast, `openfin-fdc3` for intents. A reported POC observation, **not a supported compatibility guarantee**.
- **Auth handoff unresolved:** POC passes a provider token in URL parameters to avoid a re-login; a real provider "should run hidden" after authentication. No production auth design, security approval, or token-transport review exists ([[concepts/cross-application-authentication-handoff]]).
- OpenFin's relationship to the existing portal shell — replace, wrap, or coexist — is **not settled**.

## What is still missing

No approved contract exists: which intent names, context schemas, and versions form it is unresolved; which caller/provider contracts and gates apply *per feature* is unresolved; which OpenFin/FDC3 capabilities ship in *each environment* is unresolved; which tests establish cross-library and cross-application interoperability is unresolved. The cooperation guide's development code blocks are empty and its diagrams absent, so the gates are stated intent rather than a runnable contract. The briefing's month-based phase timelines omit the year, and its approval claims carry no attachments or completed execution records.
