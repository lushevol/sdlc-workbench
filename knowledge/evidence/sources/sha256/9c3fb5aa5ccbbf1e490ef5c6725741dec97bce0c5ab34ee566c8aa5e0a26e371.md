#

# Background

## Business requirement

- Related story: <u>[Story 7177438 Data Entitlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7177438)</u>
- See also: [FM-CES Entitlement Policy (Data Sovereignty) - Country Requirements - FM COO - Conduct and Controls - Confluence](https://confluence.global.standardchartered.com/display/FMCOOCC/FM-CES+Entitlement+Policy+%28Data+Sovereignty%29+-+Country+Requirements)

As regulation requirement we must implement data access restriction to solve the **M7 **risk.

For example, only the approved profiles can access TW business data.

Snapshot of the requirements:

1. Allow data access based on Users Location + Function (configurable to support changes)
2. Onshore Country Ops users can access only their location (example: Indonesia data cannot be accessed by country ops in Philippines)
3. Users based in one country will need access to another country data (example: users based in Dubai support processing for Egypt & Saudi)
4. GBS users can access the locations which they support (example: GBS India cannot access Pakistan data)
5. Ability to prohibit specific access 1. Onshore China Users do not view TAIWAN data 2. But DEV & PSS users based in China get TAIWAN data access for production support 3. Taiwan data can be viewed by users based in Approved locations - Singapore, UK, India & Malaysia 1. India based users should not access Pakistan data 2. Users based in Pakistan should not access India data 1. Korea data can be accessed only by Korea domiciled users
6. Apply these restrictions when data is queried from downstream applications like SSDR where they rely on RATAN's data entitlement control
7. Other possible scenarios in [EMS3 - Entitlement scenarios - FM COO - Conduct and Controls - Confluence](https://confluence.global.standardchartered.com/display/FMCOOCC/EMS3+-+Entitlement+scenarios)

Note: these are only examples, the actual prohibitions will be set based on inputs by respective Country Compliance teams

Previously we've already implemented similar entitlement requirements for other regions including Pakistan, India, Egypt, etc.

## Current Status

As of 10, Dec 2025, the current status is:

- Ratan own entitlement solution is enabled for SSDR
- Cashflow blotter is using mock entitlements

Configured rules:

![image-2025-12-10_9-49-50.png](attachments/image-2025-12-10_9-49-50.png)

## Scope

Impacted components:

| Feature | Service | API | Change | Note |
| --- | --- | --- | --- | --- |
| SSDR report | Query service | v2/data/provider/query/cashflows | Switch to CES | |
| Cashflow blotter | Query service | /graphql | Add entitlement control | using mock entitlement |
| Cashflow notification | Query service | /api/ratan/notification/subscriptions (WebSocket) | Add entitlement control | using mock entitlement |
| Cashflow history | Query service | /graphql | | |
| Group blotter | Group service | | | |
| ?? | Query service | /v1/query/cashflows | | Unconfirmed |
| BCS blotter | Data ambassador | /graphql | Not in day1 scope | |

# Proposals

- <u>[FM CES Integration Technical Design]:</u> This is the intended solution, since CES is the strategic data entitlement solution in FM.
- <u>~~[Option2: RATAN existing data entitlement implementation](https://confluence.global.standardchartered.com/display/DSP/Option2%3A+RATAN+existing+data+entitlement+implementation)~~:</u> This is a plan B to solve M7 risk in case that CES is not ready for integration. This option is no longer an option since we're targeting to integrate with CES and go live at Mar, 2026.