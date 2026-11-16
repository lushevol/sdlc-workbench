---
type: KnowledgeTopic
id: KT-settlement-security-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/API Gateway & Auth server merge solution design/page.md
  revision: sha256:9e364369b0769e8472bd2ff7bbb252f002cb22b6bc87c2b6a92ca433c35096e1
  sha256: 9e364369b0769e8472bd2ff7bbb252f002cb22b6bc87c2b6a92ca433c35096e1
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Data entitlement solution/Authentication flow/page.md
  revision: sha256:01c8ed2e50585ffcbc038b18a6ddbc6746b65f7fa0c68a91a41960c2526b696f
  sha256: 01c8ed2e50585ffcbc038b18a6ddbc6746b65f7fa0c68a91a41960c2526b696f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/ENTRA integration (draft)/page.md
  revision: sha256:507b7219a2e41ad2ca806f77d656791f127518715ef281d69fc4ced62c3e8fcf
  sha256: 507b7219a2e41ad2ca806f77d656791f127518715ef281d69fc4ced62c3e8fcf
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    Settlement Security Architect/page.md
  revision: sha256:d7051675177ec49a96f044d62d0eb14bc45bac8d6240742edef024a9c229cf8c
  sha256: d7051675177ec49a96f044d62d0eb14bc45bac8d6240742edef024a9c229cf8c
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:20:32.801639+08:00'
verified: []
scope: Historical selected-source design for settlement security p3.
classification: security
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which identity, Indonesia isolation, external-user scope, and entitlement mapping
  contracts are approved?
- How will existing token/login consumers remain compatible with the gateway merge
  and entitlement token transport?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement security p3

## Scope

Historical selected-source design for settlement security p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Historical network and access design

The settlement security design specifies an internal active/passive deployment, internal-only microservices, TLS messaging, vaulted secrets, and firewall port allowlists.
User terminals reach services through Nginx and the API gateway.
The gateway validates tokens with FMAA.
UI communication uses HTTPS.

The source limits access to internal users with password and MFA; it excludes external clients in this settlement scope.
This historical scope does not decide other Portal external-user designs.

Sources: [original lines 1–15](../../../evidence/sources/sha256/d7051675177ec49a96f044d62d0eb14bc45bac8d6240742edef024a9c229cf8c.md#L1-L15), [original lines 21–29](../../../evidence/sources/sha256/d7051675177ec49a96f044d62d0eb14bc45bac8d6240742edef024a9c229cf8c.md#L21-L29).

### Identity and Indonesia isolation objectives

The migration proposal targets Entra identity and isolated Indonesian data/session infrastructure.
It identifies CES migration as a prerequisite for new ServiceNow entitlement onboarding.
The ENTRA draft recommends MSAL for tokens.
These are documented objectives and recommendations, without adopted SDK or completed identity migration.

The source-stated regulatory interpretation requires its governing authority and effective scope.

Sources: [original lines 1–35](../../../evidence/sources/sha256/9e364369b0769e8472bd2ff7bbb252f002cb22b6bc87c2b6a92ca433c35096e1.md#L1-L35), [original lines 3–3](../../../evidence/sources/sha256/507b7219a2e41ad2ca806f77d656791f127518715ef281d69fc4ced62c3e8fcf.md#L3-L3), [original lines 14–14](../../../evidence/sources/sha256/507b7219a2e41ad2ca806f77d656791f127518715ef281d69fc4ced62c3e8fcf.md#L14-L14).

### Entitlement and API migration alternatives

The historical authentication flow places function-entitlement retrieval and checks in BFF, gateway, and auth-service.
The merge proposal considers embedding function/data entitlements in the BFF-issued token and monitoring actual payload sizes.
It proposes moving GET /v3/token and GET /v3/kong/token to the gateway and removing /v1/login and /v2/login.
Those changes are unapproved contract proposals requiring caller compatibility analysis.

They do not authorize endpoint removal or consumer changes.
The proposal combines function access and ID data entitlement for ID tile visibility and equivalent gateway filtering.
Its EMS2-subject/CES-feature and action examples are illustrative mappings, not complete grants.

Sources: [original lines 19–21](../../../evidence/sources/sha256/01c8ed2e50585ffcbc038b18a6ddbc6746b65f7fa0c68a91a41960c2526b696f.md#L19-L21), [original lines 46–60](../../../evidence/sources/sha256/01c8ed2e50585ffcbc038b18a6ddbc6746b65f7fa0c68a91a41960c2526b696f.md#L46-L60), [original lines 60–117](../../../evidence/sources/sha256/9e364369b0769e8472bd2ff7bbb252f002cb22b6bc87c2b6a92ca433c35096e1.md#L60-L117).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which identity, Indonesia isolation, external-user scope, and entitlement mapping contracts are approved?
- How will existing token/login consumers remain compatible with the gateway merge and entitlement token transport?
