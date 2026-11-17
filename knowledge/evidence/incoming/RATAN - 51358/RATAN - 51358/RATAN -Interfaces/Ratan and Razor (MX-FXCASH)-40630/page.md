Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang | 2026-02-02 | @Yunzhe Ta @Pengpeng Li @Jie Cai | 2026-03-25 | |

### Description:

RATAN extracts/receives the data from Razor (MX-FXCASH)

| Data Feed | Countries in scope |
| --- | --- |
| Cashflows feed | London, Singapore, Hong Kong, Jersey , Egypt & China 30 Branches |
| Payment status messages | London, Singapore, Hong Kong, Jersey, Egypt & China 30 Branches |
| ACK/NACK | London, Singapore, Hong Kong, Jersey, Egypt & China 30 Branches |
| Cashflow Affirmation messages | London, Singapore, Hong Kong, Jersey, Egypt & China 30 Branches |
| Cashflow Failed status | London, Singapore, Hong Kong, Jersey, Egypt & China 30 Branches |
| Trade & Event messages | China 30 Branches & UK, HK, Taiwan, Germany, Malaysia, Singapore, Thailand, Philippines, India, Sri Lanka, Bangladesh |
| Utilization request | Egypt, Nepal, Saudi |
| Utilization response ACK/NACK | Egypt, Nepal, Saudi |

### E2E Data Flow:

**Trade STP :Ratan -> MX-FXCASH (**FX replication ,which will send trade with "BOOKED" status from Ratan to Razor **)**

Ratan -> MX-FXCASH (trade & event)

Product: FX Spot, Forward, Swap

Message format: SCBML V4.0

* *

***BCS settlement flow:***

MX-FXCASH -> Ratan (payment status)

Payment status:  Released, Settled, Netted, Split, CCPNetted of eligible payments except UTIL trades and reversal/resultant payments for SPLIT & Netting event.

Message format: SCBML V4.0, size limit 2M.

**FXU flow:**

refer to  [RATAN and FXU - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+and+FXU)

### Connection details:

### Interface Specification:

[*https://confluence.global.standardchartered.com/display/RZPSS/RATAN+-+51358*](https://confluence.global.standardchartered.com/display/RZPSS/RATAN+-+51358)

[*https://confluence.global.standardchartered.com/display/FMEDMI/FM+Derivatives+Replatforming+RATAN+-+FMRP+-+Service+Specs*](https://confluence.global.standardchartered.com/display/FMEDMI/FM+Derivatives+Replatforming+RATAN+-+FMRP+-+Service+Specs)

[*RAZOR Cash Settlement Processing Guide - Razor Development - Confluence (standardchartered.com)*](https://confluence.global.standardchartered.com/display/Razor/RAZOR+Cash+Settlement+Processing+Guide)

*[Requirements-12 entities FX replication - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Requirements-12+entities+FX+replication)*

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