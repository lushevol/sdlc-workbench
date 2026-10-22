---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Source inspection and reported architecture do not establish deployment or business execution.
  - Browser policy blocks local file URLs. Rendered-script checks do not establish browser layout quality.
---

# Graph architecture clarification

The graph now includes the user's four-layer MFE architecture and reported service responsibilities.
The reusable skill owns validation, publication, queries, and the separate architecture view.
The [project context](../../relationships/service-dependencies/architecture-context.json) supplies project-specific content.
The source-derived graph retains 9 repositories, 6,401 nodes, and 17,444 edges.
Reported context adds four layers, 15 subjects, 17 directed links, and eight qualification notes.
These annotations add no canonical source nodes, source edges, or resolved provider matches.

## Scope and risk

This change maintains graph tooling and records descriptive architecture clarification.
It changes no business repository, business behavior, or approved policy.
Therefore, it creates no business requirement task or business acceptance criterion.

Publication and freshness boundaries have medium risk.
Incorrect source handling could display stale explanations as current context.
New regressions check references, source hashes, portable evidence, mutation during generation, input aliases, and canonical isolation.
The implementation adds no dependency or external startup request.

## Architecture interpretation

The [candidate architecture](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md) records the explanation and source qualifications.
The [frontend topic](../../knowledge/candidates/architecture/KT-frontend-composition.md#current-four-layer-clarification) advances from version 2 to version 3.
Both records retain candidate state, unknown owners, and no verification entries.
New immutable [architecture](../../evidence/knowledge/audit/AUD-20261022-ARC-portal-service-relationships-v1.yaml) and [frontend](../../evidence/knowledge/audit/AUD-20261022-KT-frontend-composition-v3.yaml) events bind their final bytes.

| Boundary | Recorded interpretation | Evidence |
| --- | --- | --- |
| MFE composition | Root Config → Base shell → container → tile. Only the shell has Single-SPA application registration. | [User explanation](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L5-L12) and [source review](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) |
| UI loading | SystemJS loads modules. Router props select successive container, module, and tile paths. | [Source observations](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) |
| Ingress | The user reports one domain and Nginx → gateway → backend forwarding. Active DNS and gateway bindings remain unconfirmed. | [Ingress explanation](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L16-L18) |
| BFF | Logical MFE API dependency remains distinct from ingress transport. BFF responsibilities cover the reported portal scope. | [Candidate interfaces](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#http-and-token-interfaces) |
| SDK | Java library for application backend token validation. Exact universal consumer adoption remains unconfirmed. | [SDK explanation](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L20) |
| RATAN Auth | User-reported authentication and authorization delegation. Local provider support has explicit qualifications. | [Auth explanation](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L22) |

## Source differences and limits

| Finding and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Nginx templates](../../repos/infra/nginx/ratan_servers.conf.j2#L150-L256) contain direct proxy exceptions. | Universal gateway traversal cannot follow from this local copy. | unknown | Compare rendered configuration when effective ingress confirmation becomes necessary. |
| [Source review](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) finds no Auth Server Entra SPN or EMS3 implementation. | These reported delegations remain unconfirmed locally. BFF integrations remain separate source facts. | unknown | Inspect the applicable Auth revision when implementation confirmation becomes necessary. |
| [Build configuration](../../repos/ui/mfe-base/webpack.config.js#L28-L35) permits additional chunks. | One entry bundle does not imply one physical output file. | unknown | Retain entry-bundle terminology. |
| [Header handling](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L17-L28) contains request exceptions. | JWT injection is conditional and uses `Single-UI-Authorization`. | unknown | Preserve exact header identity and request scope. |
| The [review](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) identifies no dedicated BFF health-management controller. | The supplied responsibility lacks an exact endpoint mapping. | unknown | Clarify that term when endpoint mapping becomes necessary. |

These limits do not block graph generation or descriptive candidate retention.
They block stronger deployment, universal-consumer, and runtime-verification claims.
The clarification grants no publication approval.

## Validation

The skill suite passed 151 tests.
The Workbench suite completed 611 tests with two optional connector integration skips.
The local graph build and validation passed.
Source freshness and architecture-context freshness report `CURRENT`.
Wheel construction, clean workspace initialization, and six installed-skill context smoke tests passed.
The package excludes this project's context input and business knowledge.

The ingestion harness passed preparation and final sealed checks.
Independent retrieval review found no material unsupported topology or approval claim.
The primary agent checked all 31 source hashes and line ranges.
The [check receipt](../evidence/graph-architecture-context-20261022/checks.json) retains results, artifact hashes, and limitations.
The [retrieval review](../evidence/graph-architecture-context-20261022/retrieval-review.json) records the independent review and two corrected locator gaps.
The [package smoke](../evidence/graph-architecture-context-20261022/package-smoke-final.json) records wheel isolation and shipped assets.

Browser policy rejected the local `file://` URL, so browser layout verification remains unavailable.
Rendered-script tests exercised hierarchy, filters, escaping, and evidence links without a browser.
The full ASD-STE100 writing review remains pending.
