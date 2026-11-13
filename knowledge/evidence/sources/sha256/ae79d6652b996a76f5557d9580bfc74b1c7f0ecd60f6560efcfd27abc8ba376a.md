Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Zhenzhen Liu @Junying Jiang @Terris Li | 2026-02-04 | @Yunzhe Ta @Daiqi Wang | 2026-02-04 | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> Sub application would trigger Rest API call to query data from Ratan for different purpose

### E2E Data Flow:

Describe the end to end  flow.

> Sub application would trigger Rest API call to query cashflow data from Ratan
>
> 1. FMMIS–(REST API)-->RATAN
> 2. CIS–(REST API)-->RATAN
> 3. PacMan–(REST API)→RATAN
> 4. MarketUDP(SSDR)–(REST API)→RATAN
> 5. CNEDMp–(REST API)-->RATAN

### Connection details:

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.