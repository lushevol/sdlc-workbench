---
query: "What telemetry and performance or capacity evidence exists for portal interactions, cache behavior, and response time, and what remains proposed or missing?"
---

## What evidence exists

**Telemetry / interaction analytics (design-level, not verified operating system)**
- Event vocabulary is documented: tiles and modals emit `open`/`close`; workspace tabs, buttons and switches emit `click`; dropdowns emit `select`. Event identity combines container, tile, and component name, with optional values and custom attributes (e.g. search text). See [[concepts/interaction-analytics]].
- An example `useAnalytics` hook posts to `/analytics/v1/fmo/print?extend=false`, while the prose names `/api/analytics/v1/fmo/print?extend=false` as the requested API — the two paths differ. Authorization is session-derived; client addresses come from request headers and remote address.
- A [[entities/kibana]] dashboard guide reports **nine dashboards** (authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, themes), with `traceId` exposed on the error dashboard and downloadable raw data.
- Schema inconsistency: `AnalyticsData` declares **20** custom attribute fields, `AnalyticsType` declares **10** (prose also says 10).

**Frontend performance / response time (draft, historical)**
- The May 2023 performance document is explicitly a **draft** with an unsigned sign-off table. Draft targets: **5-second response time, 100 users, CPU < 50%, JS heap < 80%**. Scenarios: login, home, trade, cashflow, exception, rules. Tools: browser performance monitoring and Lighthouse.
- Reported results: login FCP **0.8 s** / LCP **1.3 s**; home FCP **0.9 s** / LCP **1.3 s** — but screenshots and measurement captures are absent.
- A monitoring page proposes weekly review of development performance (login, post-login, blotter rendering with cache/compression changes) — intent only.

**Service throughput / capacity (summary only)**
- UAT throughput page: **500 users, 250-second ramp-up, 5 iterations, 17,500 successful requests, max response time 2,023 ms** for `/api/auth/v2/sso/validate`. The linked [[entities/apache-jmeter]] plan and result archive are **absent**.
- A newer deployment page reports additional user estimates and performance figures, with test results and metrics not supplied.

**Cache behaviour (documented rules, no configuration)**
- Proposed split: revalidate layer entry files; long-cache subsequent static assets at **120 days** for chunks, images, CSS, fonts, JSON, icons; a changed entry should reference new hashed files. Users still need logout or page refresh; first-load improvement is explicitly **excluded**. See [[concepts/mfe-cache-strategy]].
- No measured effect on load time; no response headers or build naming verified; the cache implementation section contains **no configuration**.

## What remains proposed or missing

| Gap | Consequence |
| --- | --- |
| May 2023 targets are unapproved drafts; the named NFR page has **no substantive text** | No accepted service targets or measurable acceptance criteria — draft numbers cannot be read as current service limits |
| Missing screenshots, Lighthouse captures, JMeter plan and result archive, deployment test metrics | Current response time and capacity cannot be established; figures lack workload/date/environment/assertions |
| Production Kibana dashboard URL is a **placeholder** | Production observation coverage and event completeness unknown; no owner confirmed |
| Analytics attribute mismatch (20 vs 10) and no approved vocabulary per tenant event | Producers may emit attributes downstream systems or dashboards silently drop |
| Identity context and search values collected with **no retention/redaction rules** | Permitted fields, access control, and retention unconfirmed — a governance gap |
| Cache strategy is design-only | Deployed headers, entry revalidation through every proxy, and chunk naming unverified |
| Future work (2026–2027 platform proposals incl. a separate telemetry target service, central-monitoring foundation) is a proposal list with no accepted scope or completion records | Cannot support sizing or implementation planning; see [[summaries/KT-architecture-evolution]] |
| Ingress path (DNS → [[entities/nginx]] → [[entities/api-gateway]] → [[entities/single-ui-bff]]) unexercised; Nginx template mixes gateway and direct routes | Response-time attribution along the path and universal gateway traversal unproven; see [[concepts/portal-ingress-path]] |

**Bottom line:** the wiki holds *design intent, draft targets, and summary-level historical numbers*, but no dated execution artifacts, no approved non-functional limits, no verified dashboard in Production, and no evidence that the documented cache rules are deployed. No browser measurement, telemetry query, load test, or server-header check was performed during ingestion ([[concepts/frontend-performance]]).
