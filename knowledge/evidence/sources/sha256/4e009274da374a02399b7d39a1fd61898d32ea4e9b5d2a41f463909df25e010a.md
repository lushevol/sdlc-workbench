Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang | 2026-02-04 | @Yunzhe Ta @Pengpeng Li | 2026-02-04 | |

### Description:

**TDS3** - known as FM Trade Lake, which is:

- The data lake for trade data in SABRE
- Feeds a wide range of consumers such as regulatory reporting
- Built around extendable but formalized data models
- Uses Hadoop (big-data) and Elastic infrastructure
- Data is segregated into indexes (Trade Index, Fixings Index, Cashflow Index, etc.)

**RATAN **and **TDS3:**

<u>**Trade Flow**</u>

1.**FX Replication: **RATAN acts as an intermediary between **TDS3** and **RAZOR**, enforcing filtering logic to ensure only intended **trades** are forwarded to RAZOR.

2.**Trade Blotter Integration**

- RATAN retrieves trade data from TDS3 to populate the **trade blotter **(store TDS3 data in database).
- RATAN real-time querying trade data from TDS3 for display in **trade blotter **(api call).

3.RATAN will query **rate fixing information **from **TDS3 (**via the ratanone rule service) to support **FM COO exception management**.

4.RATAN fetches the **latest trade version** directly from **TDS3** during manual trade validation

---

<u>**Settlement Flow**</u>

1.**Cashflow Processing: **Settlement cashflows are sourced from **TDS3** and processed in **RATAN**.

2.**Trade Identifier Enrichment: **Retrieves `trade_external_id` and `clearing_organization_trade_id` from **TDS3**, caches them, and displays on the cashflow blotter.

3. **Instrument Reference Data: **Queries and displays the following fields from TDS3 in the BCS cashflow blotter (FX & Equity ):

- - *Parent Trade Instrument* - *Equity Instrument Reference*

4.**Spot Rate Query & FX Conversion: RATAN **retrieves **spot rates** from TDS3 to convert cashflow amount into **USD, **related OPS can do per amount limitation.

### E2E Data Flow:

1 FX replication (trade):TDS3-->Ratan-->Razor

2 Trade flow: Blade → FMRP Stella → TDS3 → RATAN

3 Settlement flow: BCS Stella/Blade → FMRP Stella → TDS3 → Solace → Ratan → Razor/FMSGW

4 Ratan query TDS3 API for querying data and showing on GUI

### Connection details:

### Interface Specification:

FX replication:

![image-2026-2-4_18-56-26.png](attachments/image-2026-2-4_18-56-26.png)

### Interface team contact:

| **service** | **Contact Name** | **Email Address** | **Phone Number** |
| --- | --- | --- | --- |
| RATAN (RATAN ONE) | RATAN ONE PSS | [FM_BPMS.SUPPORT@sc.com](mailto:FM_BPMS.SUPPORT@sc.com) | +862259806892 |
| SABRE TDS3 | Dutt, Ankur <[Ankur.Dutt@sc.com](mailto:Ankur.Dutt@sc.com)>; SABRE TDS3 BAs <S[ABRETDS3BAs@exchange.standardchartered.com](mailto:ABRETDS3BAs@exchange.standardchartered.com)>; SABRE PSS <S[ABREPSS@sc.com](mailto:ABREPSS@sc.com)> | [Rameshkumar.Visvanathan@sc.com](mailto:Rameshkumar.Visvanathan@sc.com) SABRE PSS <S[ABREPSS@sc.com](mailto:ABREPSS@sc.com)> | +6569814653 |

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.