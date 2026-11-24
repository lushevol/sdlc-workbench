# Background

## ENTRA onboarding

Standard Chartered Bank is migrating its enterprise Identity & Access Management (IAM) platform from ForgeRock (OneMFA / OneDS) to Microsoft Entra ID. The legacy ForgeRock platform is scheduled for full decommission by end of Q3 2026.

RATAN currently integrates with OneMFA (ForgeRock) and *OUD* for browser-based SSO, and relies on FMAA for service-to-service authentication. Both integrations must be migrated to Entra ID ahead of the ForgeRock decommission deadline.

## ID Isolated Deployment

RatanOne needs to be deployed for Indonesia (ID) as a regulatory-compliant instance with isolated data storage, separate from the global deployment. This introduces additional architectural constraints and objectives beyond the core Entra migration.

Regulatory Requirement: Indonesian financial regulation mandates that customer and transaction data must reside within in-country infrastructure. RatanOne's data storage (PostgreSQL, Redis) and session management must be provisioned as isolated, country-scoped instances.

## EMS2 Decommission & FMCES Migration

RATAN's functional entitlement currently depends on EMS2. The target platform is FMCES (FM Capital Entity Service / CES), which has a fundamentally different data model and API contract. Planning this migration early is critical — SNOW onboarding for data entitlements cannot proceed until the CES migration is complete.

## Prior Discussion: Data Entitlement Responsibility

There is existing tech debt around where data entitlement should be resolved. Two approaches were discussed — resolving at the API gateway and forwarding via headers, versus each service fetching entitlement on demand from the auth server. No decision was finalised; this remains an open design point to be revisited as part of this migration

# Current status

## ENTRA Login Flow

## API authorization

## Data entitlement check

# Solution

## Embedding entitlement into token

First, we need to embedding function entitlement and data entitlement into the bff-issued token like below:

```js
{
  "header": { "typ": "JWT", "alg": "RS512" },
  "payload": {
    "role_entitlements": [
      { "feature": "Cashflow", "action": "Query" },
      { "feature": "NostroBlotter", "action": "View" },
      { "feature": "ID Access", "action": "View" }
    ],
    "data_entitlements_logical_indicator": "OR",
    "data_entitlements": [
      { "key": "Entity.Booking_Entity_SCI_FMID", "values": ["10036382", "300010633"] },
      { "key": "Entity.Counterparty_Country_ISO_Code", "values": ["JP"] }
    ],
    "sub": "2022123",
    "iss": "single-ui-bff-entitlement",
    "exp": 1778783332,
    "iat": 1778740132,
    "jti": "single-ui-bff-id"
  }
}
```

Historical note: This approach was tried previously — the `Single-UI-Entitlement` JWT originally carried the full EMS2 entity tree in its payload. It was subsequently removed because the EMS2 response could reach ~21 KB per user (see Figure 1), making the token unworkably large. CES `data_entitlements` use a much more compact flat condition format; however, the same size risk applies and must be monitored during FMCES migration before committing to this option at full scale.

Payload size estimate: Embedding both entitlement types into the `Single-UI-Entitlement` JWT adds roughly **3–5 KB** to every API request that sends the token:

- `role_entitlements` (functional) — CES returns one object per permitted feature/action combination. For a typical trader with access to 5–10 features this is small, but power users with broad application access may have 20–40 entries, contributing approximately *2–3 KB*.
- `data_entitlements` (data filter conditions) — each condition is a key plus a list of allowed values. With up to ~100 FMID values (booking entities) this reaches approximately *1 KB*.

This is well within HTTP/2 header and body limits for normal API calls. The concern is JWT size in the `single-ui-entitlement` header: most reverse proxies and browsers cap individual headers at 8–16 KB, so a 3–5 KB token payload leaves comfortable headroom. Monitor actual CES response sizes per user profile during FMCES migration to validate this estimate before Go Live.

Login flow after merge:

Entitlement check & filtering flow after merge:

## Migrate features to API gateway

Below apis need to be merged to API gateway:

- GET /v3/token
- GET /v3/kong/token

Consumers using the above apis need to update to fetch from API gateway.

## Remove legacy login APIs

Legacy login apis need to be removed. including:

- /v1/login
- /v2/login

- [x] Need to confirm if frontend is using them

## ID tile display via data entitlement in token

![image-2026-5-19_16-37-17.png](attachments/image-2026-5-19_16-37-17.png)

For ID tiles, the frontend can already handle it: if user has function entitlement of cashflow blotter, and the data entitlement contains fmid="8"(ID) then display ID cashflow blotter tile.

ID Gateway need to filter using same logic.

## EMS2 to CES migration

RATAN currently uses *EMS2* as the source of truth for both functional entitlement (which screens a user may access) and data entitlement (which booking entities they may see). EMS2 is being decommissioned and replaced by *FMCES / CES*, which has a fundamentally different data model.

This migration is a *hard prerequisite* for SNOW onboarding: entitlement requests for new users or role changes cannot be raised via ServiceNow until RATAN is registered in CES and the mapping from the old EMS2 model to the CES model is defined.

| EMS2 concept | CES concept | Remark |
| --- | --- | --- |
| Subject | Feature | |
| Role | Entitlement | |
| Action | Action | CES recommends more standard action names like View, Edit, Download |

Example:

| EMS2 | CES |
| --- | --- |
| subject=`RATAN_CASHFLOW_BLOTTER`, action=`F_Export_Data` | feature=`CashflowBlotter`, action=`Export` |
| subject=`RATAN_TRADE_BLOTTER`, action=`F_Export_Data` | feature=`TradeBlotter`, action=`Export` |
| subject=`RATAN_CASHFLOW_BLOTTER`, action=`ACCESS_FMO_POST_TRADE_PORTAL` | feature=`CashflowBlotter`, action=`View` |