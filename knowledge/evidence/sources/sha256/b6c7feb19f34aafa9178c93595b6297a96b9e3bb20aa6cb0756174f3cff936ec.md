Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang @Zhenzhen Liu | 2026-03-12 | @Yunzhe Ta @Pengpeng Li | 2026-03-12 | |

### Description:

Ratan call SSI+ api to get Vostro data:

Upon receiving a cashflow, RATAN uses the information contained within it—such as booking entity FMID, counterparty FM code, currency, and CFI code—to **call SSI+ api **and identify the corresponding matching SSI record.

It then attaches the relevant data from the SSI record to the cashflow, thereby achieving the **SSI stamping** functionality.

All SSI information is centrally maintained in SSI+. Whenever there is a change (e.g., update, addition, or deletion) to any SSI record , SSI+ will proactively sends **SSI notification** messages to RATAN via solace.

These updates may potentially impact previously processed cashflows, requiring re-evaluation or adjustment to ensure data consistency and accuracy.

SSI is the abbreviation for **Standard Settlement Instruction**.

### E2E Data Flow:

**SSI+ →solace → Ratan (Realtime SSI+ publish for any updating)**

**RATAN call SSI+ ES cluster (real-time api call)**

### Connection details:

### Interface Specification:

[Vostro SSI Best Matching - UK Cashflow Migration - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Vostro+SSI+Best+Matching+-+UK+Cashflow+Migration)

[FMRP - SSI Stamping Flow - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+-+SSI+Stamping+Flow)

### Interface team contact:

| **Service ** | **Contact Name** | **Email Address** | **Phone Number** |
| --- | --- | --- | --- |
| RATAN (RATAN ONE) | RATAN ONE PSS | [FM_BPMS.SUPPORT@sc.com](mailto:FM_BPMS.SUPPORT@sc.com) | N/A |
| SSI+ | 50509 (SSI+) | FMProdMgt - SharedServices <FMProdMgt-SharedServices@[exchange.standardchartered.com](http://exchange.standardchartered.com)> | +91 9686785999 |

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

- SSI+ PSS to monitor the SSI notification and API availability and agreed response time.
- SSI+ PSS need to inform RATAN PSS on any planned downtime outside of greenzone or any issue caused unexpected outage.
- RATAN PSS to monitor SSI subscribing via solace and reach out to SSI+ PSS in case the committed API response time breached.