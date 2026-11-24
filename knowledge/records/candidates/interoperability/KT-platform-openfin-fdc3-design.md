---
type: KnowledgeTopic
id: KT-platform-openfin-fdc3-design
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/2026 Plan/FSS Portal Copy/page.md
  revision: sha256:caa19d69d68cdec7a6a1a0f3cbec9890f47aa22f53e2ad14236eb8ae463dbd34
  sha256: caa19d69d68cdec7a6a1a0f3cbec9890f47aa22f53e2ad14236eb8ae463dbd34
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/FDC3 & OpenFin Integration Design/App Directory/page.md
  revision: sha256:b4d79c83c63bc94c878c0d26d88e28be958ca31b6f8502b48b5445be95690eb9
  sha256: b4d79c83c63bc94c878c0d26d88e28be958ca31b6f8502b48b5445be95690eb9
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/FDC3 & OpenFin Integration Design/Intent Declarations/page.md
  revision: sha256:6a2eb282e31f59221e99cc2e7c4390fb804678020d371d2b1c20ebab3ced4f43
  sha256: 6a2eb282e31f59221e99cc2e7c4390fb804678020d371d2b1c20ebab3ced4f43
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/FDC3 & OpenFin Integration Design/page.md
  revision: sha256:b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d
  sha256: b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/Openfin Integration with Blade and POC/Openfin & PTP memo/page.md
  revision: sha256:6b0e5c10ceb1229431c338fea704cc63d08a35f1c2004a5fa060e79aa8cfac05
  sha256: 6b0e5c10ceb1229431c338fea704cc63d08a35f1c2004a5fa060e79aa8cfac05
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/Openfin Integration with Blade and POC/Ratan & Blade Integration
    Records/page.md
  revision: sha256:9e645ddb670d5115e99e955ba9bbcc4ac197dbe63f15695530e2e566affaa6a5
  sha256: 9e645ddb670d5115e99e955ba9bbcc4ac197dbe63f15695530e2e566affaa6a5
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/RATAN Design System Plan/page.md
  revision: sha256:c0cf6f9b6cacbd44838b59a269fa68a151e1063a1e8c81f0cd7bfaf055175b33
  sha256: c0cf6f9b6cacbd44838b59a269fa68a151e1063a1e8c81f0cd7bfaf055175b33
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/Ratan OpenFin Installation/page.md
  revision: sha256:34d1eb3d3fa56f3e062cd8a78fce5727333a4bbd26d78a1e13a501facaf00694
  sha256: 34d1eb3d3fa56f3e062cd8a78fce5727333a4bbd26d78a1e13a501facaf00694
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Ratan OpenFin
    & FDC3 Explore/2026 Plan/page.md
  revision: sha256:547bf72264645739975423296477d0e3383abead13f40107845562ae4a18d739
  sha256: 547bf72264645739975423296477d0e3383abead13f40107845562ae4a18d739
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:09:46.303860+08:00'
verified: []
scope: Historical selected-source design for platform openfin fdc3 design.
classification: interoperability
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which intent schema, empty-subject exception, source-tile rule, version fallback,
  and external-origin policy are approved?
- Which current SSO and entitlement handoff governs Ratan/Blade users and OpenFin
  adoption?
- Which dated adoption scope, design-system milestone, and desktop compatibility criteria
  apply?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Platform openfin fdc3 design

## Scope

Historical selected-source design for platform openfin fdc3 design.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Portal adoption dependencies

The FSS Portal copy marks mfe-root-config, mfe-base, single-ui-bff, and the authentication SDK as mandatory.
DNS is mandatory. Nginx, PostgreSQL, and Elasticsearch are optional with stated alternatives or purposes.
The copy marks EMS2 and OneMFA/Entra mandatory.
OpenDJ is optional for non-production; FMAA is optional when uploads do not use its API.

These historical dependencies do not establish the current CES migration contract.

Sources: [original lines 3–11](../../../evidence/sources/sha256/caa19d69d68cdec7a6a1a0f3cbec9890f47aa22f53e2ad14236eb8ae463dbd34.md#L3-L11), [original lines 13–22](../../../evidence/sources/sha256/caa19d69d68cdec7a6a1a0f3cbec9890f47aa22f53e2ad14236eb8ae463dbd34.md#L13-L22), [original lines 24–29](../../../evidence/sources/sha256/caa19d69d68cdec7a6a1a0f3cbec9890f47aa22f53e2ad14236eb8ae463dbd34.md#L24-L29).

### External login boundary

The selected Blade login description uses `/silent-login` with an S2B JWT header.
The backend validates S2B JWT and creates a session JWT without an FMAA token.
Successful login sets JWT cookies.
Internal users require credential validation and can require MFA.

This described handoff is distinct from the memo proposal to send an FMAA token without a Ratan login.

Sources: [original lines 301–304](../../../evidence/sources/sha256/547bf72264645739975423296477d0e3383abead13f40107845562ae4a18d739.md#L301-L304), [original lines 306–309](../../../evidence/sources/sha256/547bf72264645739975423296477d0e3383abead13f40107845562ae4a18d739.md#L306-L309), [original lines 311–317](../../../evidence/sources/sha256/547bf72264645739975423296477d0e3383abead13f40107845562ae4a18d739.md#L311-L317), [original lines 1–6](../../../evidence/sources/sha256/6b0e5c10ceb1229431c338fea704cc63d08a35f1c2004a5fa060e79aa8cfac05.md#L1-L6).

### Intent and context contracts

Portal intent names and context types use prefix `scb.fmptp`.
The examples use `scb.fmptp.ViewCashflows` and `scb.fmptp.cashflows` with an `id.tradeId` value.
The Admin Module provides the App Directory.
Its proposed registrations bind a tile importmap key, intent, context type, description, and permitted source tile.

An empty permitted-source field imposes no source-tile control.
The context registry stores a JSON schema.

Sources: [original lines 1–1](../../../evidence/sources/sha256/b4d79c83c63bc94c878c0d26d88e28be958ca31b6f8502b48b5445be95690eb9.md#L1-L1), [original lines 112–131](../../../evidence/sources/sha256/6a2eb282e31f59221e99cc2e7c4390fb804678020d371d2b1c20ebab3ced4f43.md#L112-L131), [original lines 99–135](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L99-L135).

### Broker routing and entitlement

The Base FDC3 broker looks up handlers, dispatches contexts, verifies access, integrates the directory, and logs intent activity.
It checks authentication and subject/action entitlements before dispatch and rejects unauthorized requests.
The example skips subject checking when subject is empty.
This exception needs a defined applicability rule.

Tenants own their intents and handlers.
Registry changes reload dynamically; inactive-tenant intents and contexts are ignored.

Sources: [original lines 57–58](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L57-L58), [original lines 63–69](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L63-L69), [original lines 85–91](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L85-L91), [original lines 136–167](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L136-L167).

### Onboarding and verification design

The design requires versioned context and entitlement metadata, tile handlers, manifest registration, and schema/compatibility validation.
Architecture review checks conflicts and access.
Deployment activates the manifest; runtime validation exposes the intent.
Tenant, platform architecture, tenant DevOps, and platform monitoring have distinct named responsibilities.

The test plan covers registry resolution, access decisions, version fallback, tenant lifecycle, and multi-tile workflows.
These are planned responsibilities and tests, without retained execution evidence.

Sources: [original lines 169–189](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L169-L189), [original lines 202–208](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L202-L208).

### Browser and OpenFin integration

The proposal wraps existing SPA URLs without repackaging and reuses Base login under the SSO policy.
Browser mode supports internal intents; OpenFin adds desktop-wide external intents.
Base applies policy and ACL before outbound delegation and after inbound delivery.
OpenFin supplies external routing.

The certification plan includes browser/OpenFin parity, stub inbound/outbound flows, origins, entitlements, retries, restart, telemetry, and latency budgets.
No numerical latency budget is selected here.

Sources: [original lines 221–223](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L221-L223), [original lines 240–272](../../../evidence/sources/sha256/b5886ca1b0b6e01f91a26bd960a7681d8107040a5cbfa02a0882226a4ce72a0d.md#L240-L272).

### Blade use cases and unresolved scope

The memo proposes normal MFE authentication, authorization, and permission behavior within OpenFin.
It proposes a central broker, tile routing, listeners, Admin registrations, and frameless calls.
It leaves user populations, shared SSO, and cross-system entitlement unresolved.
The integration record describes Ratan opening Blade trade tickets and Blade opening Ratan cashflows by Trade_Id.

These recorded use cases do not establish approved or executed interoperability.

Sources: [original lines 1–6](../../../evidence/sources/sha256/6b0e5c10ceb1229431c338fea704cc63d08a35f1c2004a5fa060e79aa8cfac05.md#L1-L6), [original lines 48–55](../../../evidence/sources/sha256/6b0e5c10ceb1229431c338fea704cc63d08a35f1c2004a5fa060e79aa8cfac05.md#L48-L55), [original lines 3–4](../../../evidence/sources/sha256/9e645ddb670d5115e99e955ba9bbcc4ac197dbe63f15695530e2e566affaa6a5.md#L3-L4).

### Design and desktop plans

The design-system plan keeps minor AppShell styling changes through year-end and selects GDS as default.
It proposes tenant foundations before migration, verification, and go-live.
Desktop materials describe taskbar presence, compact workspaces, automatic restart, and floating tiles.
Claims of independence from browser performance and absence of compatibility concerns are unverified source claims.

They do not establish performance or compatibility guarantees.

Sources: [original lines 14–18](../../../evidence/sources/sha256/c0cf6f9b6cacbd44838b59a269fa68a151e1063a1e8c81f0cd7bfaf055175b33.md#L14-L18), [original lines 33–45](../../../evidence/sources/sha256/c0cf6f9b6cacbd44838b59a269fa68a151e1063a1e8c81f0cd7bfaf055175b33.md#L33-L45), [original lines 1–7](../../../evidence/sources/sha256/34d1eb3d3fa56f3e062cd8a78fce5727333a4bbd26d78a1e13a501facaf00694.md#L1-L7).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

This bounded topic complements existing interoperability knowledge; it does not replace previously retained POC and cooperation sources.

## Open questions

Owner: unknown.

- Which intent schema, empty-subject exception, source-tile rule, version fallback, and external-origin policy are approved?
- Which current SSO and entitlement handoff governs Ratan/Blade users and OpenFin adoption?
- Which dated adoption scope, design-system milestone, and desktop compatibility criteria apply?
