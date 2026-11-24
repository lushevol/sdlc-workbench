Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang @Zhenzhen Liu | 2026-01-22 | @Yunzhe Ta @Daiqi Wang | 2026-01-22 | |

### Description:

When a user views trade details in the trade blotter, RATAN calls the DQSL API to retrieve counterparty information.

RATAN sends a GraphQL request to **DQSL**, which in turn invokes **BPSI api** to obtain an authentication token required to access **counterparty data** from the **SCI**.

RATAN caches the retrieved SCI data and refreshes this cache daily at 03:00 SGT. If the counterparty information is not present in the cache, a real-time call to the downstream systems is triggered to fetch the data.

It should be noted that BPSI is used only for authentication purposes—to acquire a valid token—and does not provide business data itself.

### E2E Data Flow:

RATAN → (via GraphQL request) → DQSL → (via BPSI for authentication) → SCI → (returns SCI data) → RATAN

### Connection details:

### Interface Specification:

![image-2026-1-22_23-3-51.png](attachments/image-2026-1-22_23-3-51.png)

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