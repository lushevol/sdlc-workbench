---
type: KnowledgeTopic
id: KT-ces-entitlement-control-20261115
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Data entitlement solution/Option2  RATAN existing
    data entitlement implementation/page.md
  revision: sha256:363618fc61d3a60ebca3c95c03ecb4591473020d4ecbbcfaf385459af6e79288
  sha256: 363618fc61d3a60ebca3c95c03ecb4591473020d4ecbbcfaf385459af6e79288
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Data entitlement solution/Race condition zombie
    session issue in cashflow notification/page.md
  revision: sha256:bd23c7abb0f651a5a5ab5350550361cfa90f2afc618bbd6a98cb588d45a4834c
  sha256: bd23c7abb0f651a5a5ab5350550361cfa90f2afc618bbd6a98cb588d45a4834c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Data entitlement solution/page.md
  revision: sha256:9c3fb5aa5ccbbf1e490ef5c6725741dec97bce0c5ab34ee566c8aa5e0a26e371
  sha256: 9c3fb5aa5ccbbf1e490ef5c6725741dec97bce0c5ab34ee566c8aa5e0a26e371
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Data entitlement solution/FM CES Integration
    Technical Design/page.md
  revision: sha256:846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b
  sha256: 846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:20:32.774655+08:00'
verified: []
scope: Historical selected-source design for ces entitlement control 20261115.
classification: security
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which compliance-approved policy versions, fields, precedence, and feature coverage
  apply?
- Which emergency-bypass authority, cache staleness, error contract, and reconciliation
  transport are approved?
- Which notification destination and session/buffer contract are approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Ces entitlement control 20261115

## Scope

Historical selected-source design for ces entitlement control 20261115.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Business access scope

The requirement seeks configurable data access by user location and function, including downstream SSDR queries.
Country examples describe onshore, support, cross-country, and prohibited access scenarios.
The source explicitly leaves actual prohibitions to country compliance inputs.
CES is the intended strategic option; the local-data plan B is struck through.

Day-one scope includes SSDR, cashflow blotter, and notifications.
History, group-blotter, and legacy query coverage are incomplete or unconfirmed; BCS data-ambassador scope is excluded from day one.

Sources: [original lines 5–24](../../../evidence/sources/sha256/9c3fb5aa5ccbbf1e490ef5c6725741dec97bce0c5ab34ee566c8aa5e0a26e371.md#L5-L24), [original lines 39–51](../../../evidence/sources/sha256/9c3fb5aa5ccbbf1e490ef5c6725741dec97bce0c5ab34ee566c8aa5e0a26e371.md#L39-L51), [original lines 53–56](../../../evidence/sources/sha256/9c3fb5aa5ccbbf1e490ef5c6725741dec97bce0c5ab34ee566c8aa5e0a26e371.md#L53-L56).

### CES policy interpretation

The design distinguishes HR-based data policy from role-based data profile.
It generally gives data-profile rules precedence over data policy.
CES management and user onboarding remain the CES team responsibility.
The integration authenticates with FMAA and obtains evaluated entitlement conditions by user PSID.

Its assumptions retain EMS2 function entitlements and limit initial field support to booking-entity FMID and counterparty domicile country.
Other fields need support confirmation.

Sources: [original lines 1–3](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L1-L3), [original lines 12–24](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L12-L24), [original lines 34–36](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L34-L36), [original lines 44–49](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L44-L49), [original lines 60–66](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L60-L66).

### Query and notification enforcement

The design translates CES conditions to JPA specification JSON, SQL JSONB predicates, or direct single-record evaluation.
GraphQL filtering adds entitlement predicates transparently.
SSDR SQL filtering injects converted entitlement conditions.
Notification delivery requires per-user destinations and outbound entitlement checks.

The selected text alternates /user/{psid}/cashflow/notification and /user/{username}/cashflow/notification.
Its review note adds /queue/ to the subscription.
One approved client/server destination contract remains unresolved.

Sources: [original lines 81–84](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L81-L84), [original lines 110–119](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L110-L119), [original lines 121–124](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L121-L124), [original lines 136–147](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L136-L147), [original lines 160–160](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L160-L160), [original lines 175–180](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L175-L180), [original lines 181–187](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L181-L187), [original lines 189–194](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L189-L194), [original lines 770–790](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L770-L790).

### Cache, errors, and emergency configuration

CES results use Redis with a default one-hour expiry and no additional query-service cache.
The normal fallback fails the query with a CES error for missing onboarding, wrong data, or unavailability.
The design defaults entitlement control on.
Its chosen configuration option has a query-service toggle plus auth-service global and per-user controls.

Disabled auth returns disabled:true, permitting privileged no-data-filter behavior in the design.
This emergency bypass needs explicit policy authority; it is not a grant to change configuration.
Only cashflow_data fields present in its JSONB model are supported.
Cached entitlement latency remains a stated design constraint.

Sources: [original lines 210–216](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L210-L216), [original lines 218–224](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L218-L224), [original lines 232–238](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L232-L238), [original lines 244–262](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L244-L262), [original lines 301–304](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L301-L304), [original lines 306–311](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L306-L311).

### Reconciliation and ownership alternatives

The draft reconciliation compares entitlements with previous snapshots and reports changes to the policy owner.
It retains an application-job option and a Control-M script option.
CES concurrency, time, and frequency need agreement.
Review notes move entitlement responsibility toward auth-service.

A separate comparison retains gateway-header forwarding versus service-to-auth retrieval tradeoffs, including WebSocket and nested-call handling.
The selected sources do not establish a final transport choice.

Sources: [original lines 569–576](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L569-L576), [original lines 770–790](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L770-L790), [original lines 792–802](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L792-L802), [original lines 812–822](../../../evidence/sources/sha256/846705479674caa6f1eb8a8d217fb1eafd743e22f4818f791afd4eff1d45d13b.md#L812-L822).

### Historical local-data alternative and session proposal

The withdrawn local alternative separates function permissions from visible data and models Global, GBS, and OnShore data roles.
Its feasibility table leaves region, function, hierarchy, multi-tagging, and some role exceptions unsupported or partial.
Those roles and examples do not define CES mappings.
The notification fix proposal replaces create-if-missing session access with pure lookup and drops delivery after session removal.

A four-megabyte send-buffer proposal is secondary and does not replace the session-lifecycle correction.
The selected before/after result table is not business intent or verified execution.

Sources: [original lines 3–12](../../../evidence/sources/sha256/363618fc61d3a60ebca3c95c03ecb4591473020d4ecbbcfaf385459af6e79288.md#L3-L12), [original lines 79–95](../../../evidence/sources/sha256/363618fc61d3a60ebca3c95c03ecb4591473020d4ecbbcfaf385459af6e79288.md#L79-L95), [original lines 99–137](../../../evidence/sources/sha256/363618fc61d3a60ebca3c95c03ecb4591473020d4ecbbcfaf385459af6e79288.md#L99-L137), [original lines 143–143](../../../evidence/sources/sha256/363618fc61d3a60ebca3c95c03ecb4591473020d4ecbbcfaf385459af6e79288.md#L143-L143), [original lines 165–169](../../../evidence/sources/sha256/bd23c7abb0f651a5a5ab5350550361cfa90f2afc618bbd6a98cb588d45a4834c.md#L165-L169), [original lines 185–201](../../../evidence/sources/sha256/bd23c7abb0f651a5a5ab5350550361cfa90f2afc618bbd6a98cb588d45a4834c.md#L185-L201).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which compliance-approved policy versions, fields, precedence, and feature coverage apply?
- Which emergency-bypass authority, cache staleness, error contract, and reconciliation transport are approved?
- Which notification destination and session/buffer contract are approved?
