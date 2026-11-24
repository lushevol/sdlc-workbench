## 1. Current Architecture Overview

Our current web platform is a Single-SPA + System.js–based micro-frontend system running purely in the browser.

### Four-Layer Structure

| Layer | Responsibility | Ownership |
| --- | --- | --- |
| Root Config | Entry HTML + import map for all tenants | Platform |
| Base | Global routing, login, authorization, and landing page | Platform |
| Container | Tenant-level shared utilities, routing, and reusable components | Tenant team |
| Tile | Business-level React applications under each tenant | Tenant team |

All layers are compiled into static frontend bundles deployed independently on their own domains.
A central Nginx routes requests for both static resources and APIs to their corresponding tenant environments.

![image-2025-10-28_12-57-37.png](attachments/image-2025-10-28_12-57-37.png)

*                                                          Post Trade Portal GUI*

*                                          4 Layers architecture of Post Trade Portal GUI*

Communication between tiles currently relies on direct function calls through the base container (e.g., `base.callTileB()`), all within the same JS runtime.

## 2. Pain Points and Limitations

| Problem | Description |
| --- | --- |
| Tight coupling between tiles | Tiles call each other’s exported functions directly; fragile across deployments and versions. |
| No interoperability standard | Communication protocol is custom; difficult to extend across tenants or integrate with OpenFin. |
| Scalability risk | Each new tile requires manual registration and runtime linkage. |
| No unified intent directory | No metadata describing which tile handles which action. |
| Limited access control granularity | Authorization only applies to UI components, not to cross-tile actions or intents. |

## 3. Introduction to FDC3

FDC3 (Financial Desktop Connectivity and Collaboration Consortium) is an open interoperability standard defining how financial applications communicate and share data.

[https://fdc3.finos.org/](https://fdc3.finos.org/)

### Core Concepts

- **Intents**: Verb, named actions like ViewAccount, OpenTrade, ShowClientProfile.
- **Context**: Nun, structured payloads passed with intents, e.g., ClientContext, OrderContext.
- **App Directory**: A registry describing which applications (or tiles) can handle which intents.
- **Desktop Agent API**: Standardized interfaces for broadcasting context and raising/handling intents.

![](https://fdc3.finos.org/assets/images/api-1-a8645dce7dbaae1a17d6b95bb19f25f8.png)

*                                                                                FDC3 Diagram*

> **INFO**
> FDC3 is natively supported by OpenFin, making it an ideal interoperability layer for our planned desktop adoption.

## 4. How FDC3 Works in Our Setup

The FDC3 Broker (in the Base layer, alias for FDC3 Desktop Agent) acts as the communication hub:

`

`

**Intent Flow Example:**

1. Tile1 raises an intent (ViewCashflows, context=TradeId:93843).
2. Base’s FDC3 broker queries the App Directory.
3. Finds Tenant B’s Tile 2 registered forViewCashflows.
4. Broker checks user access entitlement → allows routing.
5. Tile 2 opens or handles the context accordingly.

## 7. FDC3 Features Benefits

| Feature | Advantages | Description |
| --- | --- | --- |
| Intent-based communication | - Decoupled inter-tile communication | Tiles raise/handle intents instead of hard-coded calls |
| Context channels | - Standardized context objects | Shared real-time context between tiles |
| App Directory registry | - Centralized registry for intents and tiles | Directory-driven intent resolution |
| Access-aware routing | - Fine-grained access control per intent | Entitlement model applied to intents |
| Cross-tenant interoperability | - Scalable multi-tenant model - Intent-based routing and discoverability | Enable communication between different tenant tiles when allowed |

## 8. FDC3 Broker Design

After adopt FDC3 in Post Trade Portal, here are new architecture diagram overall,

The FDC3 Broker in the Base layer acts as:

- Intent Router: Matches intents → handlers via registry lookup
- Context Dispatcher: Manages context channels
- Access Verifier: Checks user entitlements before routing
- Registry Integrator: Communicates with the central App Directory
- Telemetry Source: Logs all raised/handled intents for audit & analytics

## 8. Intent & Context Declaration

please refer to

## 9. App Directory Structure

App Directory is build base on Admin Module,

<details>
<summary>Expand Details</summary>

### intent schema example

| Field | Type | Description | Sample |
| --- | --- | --- | --- |
| id | Integer | id | 1 |
| tile_id | String | the module name of tile, refer to importmap key | ratan_cashflow_blotter |
| intent | String | the intent name declared in tile | scb.fmptp.ViewCashflows |
| context_type | String | the context type of intent | scb.fmptp.cashflows |
| description | String | description of intent | View Cashflows in Cashflow Blotter |
| permit_source_tile | String | permitted source tile for this intent | ratan_trades if empty then no control on source tile |

### context schema example

| Field | Type | Description | Sample |
| --- | --- | --- | --- |
| id | Integer | id | 1 |
| context_type | String | the context type of intent | scb.fmptp.cashflows |
| schema | String | the json schema of context | { type: "object", properties: { type: { const: "scb.fmptp.cashflows" }, id: { type: "object", properties: { tradeId: { type: "string" } } } } } |

</details>

### intent declarations

| id | tile | intent | context_type | description | permit_source_tile |
| --- | --- | --- | --- | --- | --- |
| 1 | ratan_cashflow_blotter | scb.fmptp.ViewCashflows | scb.fmptp.cashflows | Search and display cashflows in ratan cashflow blotter | ratan_trades |
| | | | | | |

### context declarations

| id | context_type | schema | description |
| --- | --- | --- | --- |
| 1 | scb.fmptp.cashflows | { type: "object", properties: { type: { const: "scb.fmptp.cashflows" }, id: { type: "object", properties: { tradeId: { type: "string" } } } } } | search criteria for cashflows |
| | | | |

## 11. Access Control Model

Intent access control follows the same entitlement model used for UI components.

- Each intent registration includes a subject and actions array.
- The Base broker, upon intent raise, verifies: - User authentication (login session) - Entitlement to perform action on subject
- Unauthorized intents are rejected before dispatch.

**Example:**

```js
{
  "intent": "scb.fmptp.ViewCashflows",
  "entity": "X_RATANONE",
  "subject": "" // empty means skip checking
}
```

## 12. Multi-Tenant Scaling

Each tenant team owns:

- Its own container and tiles
- Its own FDC3 intent definitions

**Scaling rules:**

- Add/Update intents: - Tenant registers its intents to App Directory in the central registry. - Base broker reloads registry dynamically (hot reload).
- Remove intents: - Delete intents from App Directory. - Base broker ignores intents or context from inactive tenants.

## 13. Tenant Onboarding

**Onboarding Workflow:**

1. Define Intents - Tenant team defines supported intents and context schema. - Version and entitlement metadata added.
2. Implement Intent Handlers - Implement FDC3 APIs (addIntentListener, raiseIntent) inside tile.
3. Register in App Directory - Submit metadata manifest to central registry. - Validation ensures schema correctness and version compatibility.
4. Approval & Review - Architecture committee reviews registration for conflicts or access violations.
5. Deploy to Staging → Production - Tile deployment via static hosting (Nginx), registry entry updated.
6. Runtime Verification - Broker validates registration and exposes intent at runtime.

## 14. Tenant Team Involvement

| Step | Responsibility | Owner |
| --- | --- | --- |
| Intent definition | Define intent name, context, version, entitlement | Tenant team |
| Implementation | Add FDC3 APIs in tile frontend | Tenant team |
| Manifest registration | Submit App Directory manifest | Tenant team |
| Review | Schema validation and access model review | Platform architecture |
| Deployment | Publish static files & activate manifest | Tenant DevOps |
| Monitoring | Log intent usage and handle deprecations | Platform |

## 15. Architectural Impact Summary

| Area | Impact | Notes |
| --- | --- | --- |
| Base Layer | High | Adds FDC3 broker and App Directory integration |
| Security | High | Access verification and isolation per tenant |
| Container | Moderate | Tiles interact via standardized APIs |
| Tile | Moderate | Implements FDC3 handlers |
| Deployment | Low | No major change; static build remains |
| Performance | Low | Lightweight in-memory registry and routing |

## 16. Testing & Regression Strategy

- Mock Intent Registry Tests Validate resolution logic between intents and tiles.
- Access Control Tests Simulate various entitlements and confirm allowed/denied results.
- Version Compatibility Tests Validate fallback across intent versions.
- Tenant Lifecycle Tests Add/remove tenants dynamically and verify broker reload.
- End-to-End Interop Scenarios Simulate multi-tile workflows (ClientTile → TradeTile → ReportTile).

## 17. Future Vision

The adoption of FDC3 as our interoperability backbone will:

- Transform our microfrontend platform into an intent-driven ecosystem.
- Enable cross-tenant communication with standardized security.
- Ensure smooth OpenFin migration with minimal code change.
- Provide observability and control through centralized intent analytics.

This positions our platform for long-term scalability, modularity, and enterprise desktop readiness.

# OpenFin Adoption

We will wrap the existing browser SPA URLs in OpenFin. The same Base Broker code runs unmodified. When OpenFin is present, our Broker adapts to OpenFin’s DesktopAgent / Interop Broker to support external (desktop-wide) intents in addition to internal (in-app) intents.

## User Sight When Ratan Users Launch OpenFin

## Business Flow from Ratan Cashflows to Blade Trade

## Business Flow from Blade Trade to Ratan Cashflows

#### OpenFin Platform Provider FDC3 Broker Logics

<details>
<summary>Expand Details</summary>

![](https://resources.here.io/docs/core/assets/images/here-core-interop-fdc3-Intent-diagram-75d3c2ebfeaa716db952257f57abab17.png)

</details>

## OpenFin Adoption Overview

- **Deployment Mode (Phase 1):** All tenants render within a single OpenFin workspace (mirrors the single-site browser model).
- **Hosting Strategy:** OpenFin loads tenant Container/Tile from existing URLs (served by Nginx). No repackaging.
- **Auth Flow:** Same login in Base; tokens reused inside OpenFin (redirects/cookies/storage per SSO policy).
- **Interop Scope:** - **Browser mode:** internal intents only (tiles inside our SPA). - **OpenFin mode:** internal + external intents (other OpenFin apps).

## OpenFin Architecture Integration (Dual-Broker Model)

**Key principle:**

- Base Broker always handles policy & ACL first (our security boundary).
- If the route is external, Base delegates to OpenFin Interop Broker.
- For incoming external intents, OpenFin delivers to our Broker (via DesktopAgent), then Base applies ACL & Directory and dispatches to our tiles.

## OpenFin Testing & Certification Plan

- **Environment parity:** run the same E2E flows in Browser & OpenFin.
- **Interop tests:** - Outbound to a stub external OpenFin app. - Inbound from a stub app to our tiles.
- **Security:** - Verify external origins against allowedExternalOrigins. - Entitlement checks on both outbound and inbound path.
- **Resilience:** - Network failures to Directory/External → retries & fallbacks. - Broker restart/reconnect scenarios.
- **Performance:** - Intent round-trip latency budgets & dashboards.
- **Ops:** - Telemetry from Broker & OpenFin broker (correlate intent IDs). - Incident runbooks: policy blocks, handler not found, version mismatch.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Version drift between tenants | Directory compatibility map + schema transforms |
| External app overreach | allowedExternalOrigins, per-intent ACL, audit |
| Broker split-brain | Make Base authoritative for ACL; OpenFin for routing |
| Latency spikes | Cache directory; pre-warm tiles; retry policy |
| Auth tokens in OpenFin | Use same SSO; short-lived tokens; secure storage |

## Conclusion

This design keeps your SPA as the primary entry, adds a standards-based interop layer (FDC3) in Base, and seamlessly extends to desktop with OpenFin:

- **Browser:** Internal interoperability via our Base Broker.
- **OpenFin:** Same Broker + DesktopAgent integration for internal + external intents.
- **Governed & secure:** Versioned intents, per-intent ACL, tenant isolation, and central App Directory.
- **Scalable:** Add/remove tenants by manifest; policy-driven routing; telemetry for ops.