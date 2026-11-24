Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Terris Li | 2026-01-30 | @Yunzhe Ta @Daiqi Wang | 2026-01-04 | |

### Description:

RATAN provide the entitlement and forward service to let tenant integrated into FMO Portal.

> **INFO**
> | **Tenant** | **Status** |
> | --- | --- |
> | STAMP (VPA) | Technical Online |
> | SSI+ | Online |
> | SSDR | Pending |
> | RATAN ONE | Online |
> | LOANIQ.IL | Online |
> | FSS | Online |
> | FM CES | Pending |

### E2E Data Flow:

Tenant get entitlement list by RATAN SDK, and forward Tenant's request.

> 1. Entitlement list: Tenant -- (RATAN SDK)--> EMS2
> 2. Request forward: Tenant Front End page -- > RATAN Nginx --> Tenant Back End server

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

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