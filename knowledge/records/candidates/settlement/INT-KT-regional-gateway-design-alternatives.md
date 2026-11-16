---
type: KnowledgeTopic
id: INT-KT-regional-gateway-design-alternatives
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-d7922598e4bbf46425081cda
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/(Deprecated)API Gateway
    & Auth Server Combination/page.md
  revision: sha256:b018f5049fab42b04c41afb977138dd1cd672f88c033b7817eac17eeb4555772
  sha256: b018f5049fab42b04c41afb977138dd1cd672f88c033b7817eac17eeb4555772
- id: SRC-064d27036e5d1fc4382c5bc5
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/(Foundation 2.0)API Gateway
    Feature Upgrade/page.md
  revision: sha256:49b17377ec45cde1cfa43531fc9e0e5c4782cc618775011b8ec9e84799df8063
  sha256: 49b17377ec45cde1cfa43531fc9e0e5c4782cc618775011b8ec9e84799df8063
generated:
  by: agent:codex:sol-integrations-review
  at: '2026-11-16T01:30:46.147015+00:00'
verified: []
classification: settlement
scope: Regional gateway design alternatives
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related:
- KT-sdk-and-entitlements
open_questions:
- 'KDQ-9384a93b2e: Which gateway design replaces the deprecated merger, and which
  key/fallback contract preserves existing portal behavior?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Regional gateway design alternatives

## Scope

Regional gateway design alternatives.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### GW-01 — Deprecated consolidation alternative

The explicitly deprecated page proposes combining the gateway and authorization server for Indonesia deployment.
It also proposes FMCES functional entitlement, smaller entitlement tokens, Entra service-account integration, and an Entra/FMAA fallback.
Its Q3 2026 ForgeRock decommission date is a plan, not completion evidence.
The page expands FMAA as a mobile authentication application. This review does not equate that term with an authentication adapter.
These deprecated options supply historical context only and cannot supersede later migration intent.

[Selected original evidence](../../../evidence/sources/sha256/b018f5049fab42b04c41afb977138dd1cd672f88c033b7817eac17eeb4555772.md#L7-L36), [Selected original evidence](../../../evidence/sources/sha256/b018f5049fab42b04c41afb977138dd1cd672f88c033b7817eac17eeb4555772.md#L38-L50).

### GW-02 — Gateway resilience upgrade proposal

The upgrade proposes configurable rate limits with user/token, then IP, then path key fallback.
`deny-empty-key` remains a choice between permissive false and strict true.
Per-route circuit breakers use an internal fallback route and a response containing error code, message, routeId, traceId, and timestamp.
Environment-specific threshold tuning remains proposed without accepted values.
The source requires proposed tests for timeout/5xx state changes, fallback payloads, rate-limit recovery, and key strategies.
Suggested metrics cover rejected requests, fallback counts, and open circuits. No test or performance result is established.

[Selected original evidence](../../../evidence/sources/sha256/49b17377ec45cde1cfa43531fc9e0e5c4782cc618775011b8ec9e84799df8063.md#L66-L90), [Selected original evidence](../../../evidence/sources/sha256/49b17377ec45cde1cfa43531fc9e0e5c4782cc618775011b8ec9e84799df8063.md#L98-L123), [Selected original evidence](../../../evidence/sources/sha256/49b17377ec45cde1cfa43531fc9e0e5c4782cc618775011b8ec9e84799df8063.md#L129-L147), [Selected original evidence](../../../evidence/sources/sha256/49b17377ec45cde1cfa43531fc9e0e5c4782cc618775011b8ec9e84799df8063.md#L149-L165).

## Connections

Related canonical IDs: `KT-sdk-and-entitlements`.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
