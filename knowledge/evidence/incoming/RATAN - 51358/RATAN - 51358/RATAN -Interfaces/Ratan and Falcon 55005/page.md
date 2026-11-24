Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| | | | | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> As part of C&A project, Ratan need to run PV check for BTS trade, and to calc BTS bond PV, to achieve that Ratan will call Falcon API to fetch bond price and fx rate.

### E2E Data Flow:

Describe the end to end  flow.

> 2 flow here, one is consume trade, and another one to fetch bond price and fx rate
>
> 1. TDS3 BTS trade --(Solace)--> Ratan
> 2. Falcon --(API)--> Ratan
>
> Ratan will calculate PV trade in real time based on trade info (flow 1) + market data info (flow 2).

### Connection details:

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

### OLA:

Application self OLA consolidate link can add here

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.