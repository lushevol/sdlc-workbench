Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Junying Jiang @Yunzhe Ta | 2026-01-26 | @Yunzhe Ta @Daiqi Wang | 2026-01-26 | |

### Description:

Accounting message sending from Ratan to EBBS on real-time basis.

One of the major objective of FMRP 2024 H1 is Ratan is going to build the capacity generating the payment accounting entry and feed to **eBBS**. It would be **real time feeding **by **Solace **between Ratan and eBBS, the accounting entry message format would be **Json**. For below entities, they are all eBBS countries.

| country code | Countries in scope |
| --- | --- |
| CN, MY, IN, SG | China, Malaysia, India, Singapore |
| UK, DE | United Kingdom, Germany |
| MU, AE, ID, PH, US, JP, ZA, HK, EG, NP, SA | MAURITIUS,DUBAI,JAKARTA,MANILA,NEWYORK,TOKYO,JOBURG,DIFC,PHILIP FCU, Hong Kong, Egypt, Nepal, Saudi |

### E2E Data Flow:

Ratan →Central solace ->Ebbs

### Connection details:

### Interface Specification:

![image-2026-1-26_10-46-38.png](attachments/image-2026-1-26_10-46-38.png)

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