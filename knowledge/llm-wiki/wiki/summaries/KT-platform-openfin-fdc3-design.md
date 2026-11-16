---
type: Summary
description: "Summarizes candidate FDC3 and OpenFin intent, context, entitlement, onboarding, and browser integration proposals."
doc_type: short
full_text: sources/KT-platform-openfin-fdc3-design.md
---

# Platform OpenFin and FDC3 design

> **Source status:** Candidate/draft. Historical materials and plans do not establish an approved production contract or completed adoption.

The retained designs describe intent and context names, JSON context schemas, tile registrations, handler ownership, and broker checks. An empty permitted-source field removes the described source-tile restriction; empty-subject behavior also needs a defined rule. Registry changes may reload dynamically, but no execution evidence is supplied. [Intent and context contracts](../../../records/candidates/interoperability/KT-platform-openfin-fdc3-design.md#intent-and-context-contracts) [Broker routing and entitlement](../../../records/candidates/interoperability/KT-platform-openfin-fdc3-design.md#broker-routing-and-entitlement)

The proposal keeps existing SPA URLs and uses browser intents internally, with OpenFin routing external desktop intents. Testing and onboarding gates are planned, not verified. Its historical dependency list names EMS2 and OneMFA/Entra; it does not settle current CES migration scope. [Portal adoption dependencies](../../../records/candidates/interoperability/KT-platform-openfin-fdc3-design.md#portal-adoption-dependencies) [Browser and OpenFin integration](../../../records/candidates/interoperability/KT-platform-openfin-fdc3-design.md#browser-and-openfin-integration)

FDC3/API names, SSO and entitlement handoff, empty-subject rules, external-origin controls, and latency targets remain unresolved. The desktop plan's compatibility claims are unverified. See [[entities/openfin]], [[entities/fdc3]], [[concepts/interoperability-contract-governance]], and [[concepts/intent-based-application-interoperability]].
