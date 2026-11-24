| Document Author | |
| --- | --- |
| Document Version | v1.0 |
| Document Status | |

## **Introduction**

To determine the optimal architectural approach for Blade to access FX utilization data (e.g., remaining unutilized amounts, specific cashflow statuses) managed by RATAN (strategic settlement system).

This data is critical for Blade to:

- Display accurate unutilized amounts at the trade level
- Implement hard blocks/controls on "UTIL" trades based on their real-time utilization status from RATAN
- Validate user actions in Blade (e.g. amendments, withdrawals) against the remaining utilizable amount

## **Background: FX Utilization Process Recap**

<u>Overview</u>:

- Non-FM clients, such as transaction banking clients, book FX deals in FM systems to meet their business needs. However, the settlement of these deals should be managed by non-FM systems like SCPAY, TradeXpress, etc. Once a forward deal is booked on behalf of a client, the client should have the opportunity to utilize the FX deal either partially or fully on the value date or through early utilization.
- FM systems will settle the utilized FX deals in the FX Branch Suspense Account. If the deal is not utilized, it will be settled in the Past Due Account. Clients will have the opportunity to utilize their FX deals from the Past Due Account for a limited period, ranging from 3 to 7 days post the value date of the FX deal, based on country regulations. After this period, any unutilized FX deals should be reversed, and any costs related to rate differences should be charged to the client.

<u>Key Systems</u>:

- Blade, S2BX: Trade booking
- STELLA and TDS3: Trade lifecycle management and persistence
- FXU: Orchestrates Utilization requests
- RATAN: Golden source of cashflow settlement, utilization amounts, and detailed utilization statuses

<u>Business Benefits:</u>

- Clients will have the flexibility to utilize FX deals for multiple cross-border payments.
- Multiple FX deals can be consolidated for a single net payment based on the client's needs.
- Clients will have the flexibility to utilize their FX deals either fully or partially before the maturity date. The Past Due process will assist clients in utilizing FX deals after the maturity date without the need to book new FX deals.
- The past due utilization process will help monitor unutilized deals and charge the client for any FX rate fluctuations

## **Current Architectural State & Data Gap**

Blade primarily sources data from TDS3. RATAN updates TDS3 with cashflow settlement statuses.

<u>Gap</u>: Granular FX utilization data (e.g., per-cashflow remaining amounts, specific statuses) from RATAN is not currently propagated back to TDS3 (via STELLA). This data is required for Blade to implement the required controls.

## **Architectural Decision: Sourcing Utilization Data for Blade**

We need a decision on how Blade will access the FX utilization details that are mastered in RATAN

| | Description | Pros/Cons |
| --- | --- | --- |
| Option#1 | **RATAN → TDS3 Enhancement:** RATAN to send detailed FX utilization updates back to TDS3 (via STELLA). Blade will continue to source all trade and utilization-related data exclusively from TDS3 **Key Points**: 1. **Why TDS3?**: To maintain Blade's existing architectural pattern of a single, consistent data source for trade lifecycle information, thereby simplifying Blade's data access logic 2. **Golden Source**: RATAN would remain the actual golden source for settlement and utilization. TDS3 would become an authoritative, replicated source specifically for consumers like Blade. | <u>Pros</u>: 1. Consistent Architecture for Blade to maintain a single integration point with TDS3 2. Centralized data access point for other consumer systems (if any, now or in future) could potentially leverage TDS3 for this consolidated trade and utilization view <u>Cons</u>: 1. Data Latency: Inherent latency between RATAN updating and TDS3 reflecting the change. Real-time RATAN to TDS3 sync would be crucial 2. Increased Complexity: This may require data model changes to store utilization data. Potential performance/scalability impact on TDS3 3. Scope Expansion: Storing dynamic, settlement-driven utilization data might be seen as expanding TDS3's remit from a "trade event store" to a more "trade state store" 4. TDS3 is already overloaded and adding more data will increase this issue 5. All updates would impact all downstream consumers of TDS3 6. This creates a data denormalisation (silver source) and against the FMRP strategy of data being retrieved from the golden source 7. Requires rec back to RATAN to ensure data is up to date |
| Option#2 | **Blade Integration with RATAN: **Blade would be enhanced to make direct API calls to RATAN to fetch FX utilization data for "UTIL" trades on an as-needed basis (e.g., when user performs an action on a trade in Blade) | <u>Pros</u>: 1. Access to Real-time Data: Blade could potentially get the most current utilization data directly from the golden source (RATAN), minimizing latency for critical controls 2. TDS3's role remains unchanged regarding this specific granular utilization data 3. Accessing data from golden source means data is guaranteed to be correct 4. Fits with agreed FM architectural pattern <u>Cons</u>: 1. Blade would now source related data from two primary systems (TDS3 for core trade data, RATAN for utilization data), increasing its internal complexity 2. Blade becomes directly coupled to RATAN's availability, API contract, and performance (at least for Utilization trades) 3. Blade's backend would need to merge data from TDS3 and RATAN. Any inconsistencies need to be managed carefully. 4. Requires Robust and Performant APIs from RATAN 5. Blade needs to assess the potential performance impact for this new integration |
| Option#3 | **Blade → RATAN UI Integration (OpenFin)** | <u>Pros</u> 1. This can provide a quick way for users in Blade to visually see utilization data before performing an action <u>Cons</u>: 1. Primarily a UX Solution: This approach solves the display requirement but does not address Blade's backend needs for this data. 2. Data not natively available to Blade's core processes |

## **FX Util Trade Booking and Utilization Flow**

**![image-2025-5-27_13-23-55.png](attachments/image-2025-5-27_13-23-55.png)**