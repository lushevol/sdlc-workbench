Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang | 2026-02-04 | @Yunzhe Ta @Pengpeng Li | 2026-03-18 | |

### Description:

**Settlement Processing Flow:**

1. RATAN retrieves the **Spot Rate** from the Stella API to comply with settlement processing profile constraints.
2. In **BCS flow**, RATAN call Stella API to **check fixed/floating leg for netting.**
3. RATAN ****writes back calculated cashflows' status and updated trade status** to **Stella: ****RATAN publishes continuous, real-time streams of **confirmation events** and** settlement workflow events **to the Sabre (Stella) SDK Booking API.This is done by posting an SCBML via Kafka dedicated topic. Stella reads the messages from the Kafka topic and pushes the message into the trade booking engine. Upon receipt of the message, the Stella booking engine will respond with an ACK or NACK based on successful processing.

---

**Trade Control Flow:**

1. **RATAN **queries the** Trade lock status** from the **Stella SDK Booking REST API** via the **Ratan Stella Ambassador **service.

This enables **Middle Office (MO) users** to determine whether a trade or trade package is currently locked prior to initiating manual intervention. If a lock is in place, Stella provides detailed information including:

- The identity of the user or system that acquired the lock,
- The lock duration or expiry time.

The **RSA microservice** serves as the secure integration gateway between RATAN and Stella, facilitating key operations such as trade validation, rejection, and affirmation.

2. **RATAN **publishes **Economic Affirmation (E0) events **directly to **Stella via API.**

### E2E Data Flow:

Describe the end to end  flow.

### Connection details:

| **API Provider ** | **Consumer ** | **Data type ** | **Connection Detail** | **Version** | **METHOD** | **Query/Parameter** | **Query Frequency** | **API limitation** | **API timeout** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29126-FMRP STELLA | 51358-RATAN | confirmation events and settlement workflow events | [https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-stella-ep/prod](https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-stella-ep/prod) | version would update to 2025.10.23-1-cfda1ef9 | | | real-time | | |
| 29126-FMRP STELLA | 51358-RATAN | trade validation status | [https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-stella-ep/prod](https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-stella-ep/prod) StellaBookingApi, /v1/stella/{type}/{operation}/{action} | | | | real-time | | |
| 29126-FMRP STELLA | 51358-RATAN | trade lock status | - **StellaBookingRestApi** PROD URL: [https://sabre-prod-cloud-global.gdc.standardchartered.com//fmrp-stella-ts/prod/getLockStatusByContractId/](https://sabre-prod-cloud-1.gdc.standardchartered.com//fmrp-stella-ts/prod/getLockStatusByContractId/5028387294){contract_id} - eg: [https://sabre-prod-cloud-global.gdc.standardchartered.com//fmrp-stella-ts/prod/getLockStatusByContractId/5028387294](https://sabre-prod-cloud-1.gdc.standardchartered.com//fmrp-stella-ts/prod/getLockStatusByContractId/5028387294) | Trade validation change the channel to : RATAN_VALIDATION | | | real-time | | |

for cashflow status write back and trade lock status retrieved, all use sdk as '**sabre-booking-api**' which contains below APIs.

- cashflow/trade status write back: **StellaBookingApi**
- trade lock status: **StellaBookingRestApi**

### Interface Specification:

[Process Model - Contract Matching Service (from CDU/RATAN) - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=1702274658)

[MO Validation - Design - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/MO+Validation+-+Design)

[Trade and Lifecycle Events - Workflows - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Trade+and+Lifecycle+Events+-+Workflows)
[FMRP STELLA Booking API - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/FMRP+STELLA+Booking+API)

### Interface team contact:

| **ROLE** | **Name** | **CONTACT NO.** |
| --- | --- | --- |
| SABRE PSS Manager | Brito, Paulo - 1547035 | +65 6981 3784 |
| PSS Change Contact | SABRE PSS | [SABREPSS@sc.com](mailto:SABREPSS@sc.com) |

### OLA:

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

[Requirements-New Validation Flow with BOOKED State - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Requirements-New+Validation+Flow+with+BOOKED+State)

[RATAN Settlement Flow Scope](https://confluence.global.standardchartered.com/display/PSS/Knowledge+sharing---RATANONE+Latest+settlement+flow+scope+-+20250612)

[Ratan -> FMRP Stella API integration - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+-%3E+FMRP+Stella+API+integration)

[Trade Level Affirmation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Trade+Level+Affirmation)

[Trade Lock/Unlock for MO Validation Tech Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3263145506)

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.