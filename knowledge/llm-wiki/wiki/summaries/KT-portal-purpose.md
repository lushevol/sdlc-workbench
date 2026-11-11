---
type: "Summary"
description: "Summarizes the post-trade portal's purpose, shared capabilities, and draft or proposed scope."
doc_type: short
full_text: "sources/KT-portal-purpose.md"
---

> Derived from [KT-portal-purpose, version 2](../../../candidates/background/KT-portal-purpose.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Portal Purpose and Capability Map — Summary

This topic synthesizes supplied UI-platform materials about a [[entities/fmo-post-trade-portal|post-trade portal]]. It describes the portal as a shared entry point and workspace for tenant applications, while application teams keep domain-specific business functions. The platform provides shared design, authentication, composition, administration, integration, observability, and interoperability capabilities.

## Core purpose
- The UI guild aims to provide consistent design, shared components, and utilities across application teams.
- The portal gives post-trade users a common entry and workspace. Named activities include affirmation, confirmation, settlements, and reporting; blotters and a rules engine are examples.
- Responsibility is split: application teams deliver domain functions, while the platform supplies shared integration and UI capabilities.
- The portal introduction remains under edit, so the listed business scope is indicative rather than a complete or approved inventory.

## Shared vocabulary
| Term | Meaning in the materials |
| --- | --- |
| Tenant application | A domain application integrated into the shared portal. |
| Tile | An application view that a user opens in a workspace. |
| Workspace | A user area that holds opened tiles. |
| Container | An application-owned module or the shared base that supplies common context; the role must be made explicit. |
| Import map | A mapping used to locate modules for dynamic loading. |

## Capability boundaries
| Concern | Documented capability |
| --- | --- |
| Entry and identity | Common application entry, SSO, MFA, and session renewal. |
| Composition | Shared themes, dynamic module loading, [[concepts/portal-tile-workspace-model|tiles and workspaces]]. |
| Access | [[entities/ems2|EMS2]] roles and configured [[concepts/portal-entry-and-tile-authorization|tile eligibility]]. |
| Administration | Configuration management and [[concepts/frontend-onboarding|tenant onboarding]]. |
| Integration | Tenant UI and API routing through the portal's [[entities/nginx|Nginx]] boundary. |
| Observation | Analytics for user activity and performance. |
| Interoperability | Cross-application interaction, with [[entities/fdc3|FDC3]] marked as in progress. |

These are documented capabilities. The source does not establish deployed or tested coverage for each one.

## User and application flow
The described flow is one entry, authentication, tile selection, and multiple workspaces. Module loading uses import maps, and session renewal connects to session control. Cross-application context through [[entities/fdc3|FDC3]] is still in progress. This sequence is a synthesis of the capabilities page, not retained execution evidence.

## Draft principles and roadmap
- Draft principles emphasize SSO, [[concepts/portal-entry-and-tile-authorization|tile authorization]], interoperability, action tracing, and a forthcoming notification center. Login and [[concepts/portal-entry-and-tile-authorization|tile-eligibility]] statements remain draft intent.
- A deployment proposal names [[concepts/frontend-onboarding|onboarding changes]], workflow AI, telemetry, and infrastructure migration for 2026 and early 2027.
- Notification, dashboards, and OpenFin appear as refining requirements. The target service list is a proposed decomposition.
- Proposed and draft items must stay separate from the current capability inventory and implementation.

## Evidence limits and open questions
- Source authority and original revisions are unconfirmed; the manifest identifies local bytes only.
- The portal introduction is under edit and the principles are draft, so accepted scope and enforceable rules are not established.
- The capabilities page depends on screenshots absent from the export.
- The deployment proposal has no approval record in these materials.
- Open questions: who can confirm the current portal name, scope, and capability inventory; which draft principles became accepted rules and when; which 2026 and 2027 proposals have approved scope or deployed implementations.

## Related Concepts
- [[concepts/microfrontend-layering]]
- [[concepts/portal-tile-workspace-model]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/shared-dependency-governance]]
- [[concepts/single-ui-sdk-authentication]]
- [[concepts/entitlement-retrieval]]
- [[concepts/frontend-onboarding]]
- [[concepts/application-ownership]]
- [[concepts/portal-ingress-path]]
- Application interoperability (with [[entities/fdc3|FDC3]])
- Observability and performance

<a id="related-concepts-1"></a>

- [[concepts/identity-provider-delegation]]

## Entities
- [[entities/fdc3]]
- [[entities/fmo-post-trade-portal]]
- [[entities/ems2]]
- [[entities/nginx]]
- [[entities/single-spa]]
- [[entities/systemjs]]
- [[entities/mui]]
- [[entities/react]]
- [[entities/single-ui-bff]]
- [[entities/single-ui-sdk]]
- [[entities/api-gateway]]
- [[entities/mfe-base]]
- [[entities/mfe-root-config]]
- [[entities/portal-team]]
