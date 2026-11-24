Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Zhenzhen Liu | 2026-02-04 | @Yunzhe Ta @Pengpeng Li | 2026-02-04 | |

### Description:

**TDSX** - Trade Data Store X, which is:

- A unified API layer that sits on top of both TDS2 and TDS3
- Part of the Trade Store Convergence Program
- Designed to abstract away the existence of two physical stores from consumers

**RATAN **and **TDSX:**

- **T****rade control flow** retrieves '**P****ayment Schedule'** from **TDSX **for display on the **Trade Blotter (See below screenshot)**.
- RATAN calls the **TDSX REST API** for **trade validation**** **
- **Uber messages** are published by **TDSX** and delivered to **RATAN** via a **Solace.**

![image-2026-3-12_9-59-54.png](attachments/image-2026-3-12_9-59-54.png)

### E2E Data Flow:

Describe the end to end  flow.

### Connection details:

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

| **service** | **Contact Name** | **Email Address** | **Phone Number** |
| --- | --- | --- | --- |
| RATAN (RATAN ONE) | RATAN ONE PSS | [FM_BPMS.SUPPORT@sc.com](mailto:FM_BPMS.SUPPORT@sc.com) | +862259806892 |
| SABRE TDSX | SABRE_TDSX_BA <S[ABRE_TDSX_BA@exchange.standardchartered.com](mailto:ABRE_TDSX_BA@exchange.standardchartered.com)>PSS, SABRE <S[ABRE.PSS@sc.com](mailto:ABRE.PSS@sc.com)> | SABRE_TDSX_BA <S[ABRE_TDSX_BA@exchange.standardchartered.com](mailto:ABRE_TDSX_BA@exchange.standardchartered.com)>PSS, SABRE <S[ABRE.PSS@sc.com](mailto:ABRE.PSS@sc.com)> | |

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.