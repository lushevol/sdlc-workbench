Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Zhenzhen Liu @Junying Jiang | 2026-01-28 | @Yunzhe Ta @Jie Cai | 2026-01-28 | |

### Description:

RATAN calls Markets UDP to retrieve PV data for P&L calculations and generates CnA exceptions—for user to review from exception blotter .

### E2E Data Flow:

- OVV (a service within Markets UDP) will send a notification to RATAN via Solace when PV data is ready,
- Ratan fetches PV data via Markets UDP API

| | **Expected Timing Sabre Feed to ****OVV**** (Market UDP)** | **Expected Timing Ratan to generate exceptions** |
| --- | --- | --- |
| **Batch 1** | T 03:00 PM SGT (6:00AM UTC) | T 04:00 PM SGT (7:00AM UTC) |
| **Batch 2** | T 03:00 PM UKT (2:00PM UTC) | T 04:00 PM UKT (3:00PM UTC) |
| **Batch 3** | T 03:00 PM UST (6:00PM UTC) | T 04:00 PM UST (7:00PM UTC) |
| **Batch EOD** | T+1 00:00AM UTC | T+1 01:00AM UTC to get the previous version trade's PV •The PV from this EOD file is for Ratan to get the previous version trade's PV when calculate PV impact |

### Connection details:

### Interface Specification:

![](https://confluence.global.standardchartered.com/download/attachments/3449110848/image-2025-9-15_14-11-49.png?version=1&modificationDate=1757916710000&api=v2)

### Interface team contact:

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

For view **VALUATION_DATA_VER_HIS**, Sabre may has release on Friday and SABRE team will send a upfront notification of delay risk if MRB release activities happen on Friday, which will potentially impact the data readiness of **VALUATION_DATA_VER_HIS** on Friday.