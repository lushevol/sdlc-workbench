Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Zhenzhen Liu @Junying Jiang | 2026-01-22 | @Yunzhe Ta @LiPing Gao | 2026-03-26 | |

### Description:

Users require access to the **Payment Holiday description** on the Trade Detail page. However, the data received from TDS3 only includes the **Payment Holiday Source Name**.

Since the **golden source** for the Payment Holiday description is **MDS**, RATAN will retrieve the description data from MDS and enrich the corresponding field in the trade details.

### E2E Data Flow:

RATAN periodically queries two tables—**SD_TP_SYSTEM_MAP** and **SD_CALENDAR_MAIN**—from the MDS API on a daily basis.

The job is scheduled and triggered by Control-M.

**Synchronization Details:**

- **Frequency:** Once per working day
- **Execution Time:** 05:00 AM GMT
- **Maximum Records per Request (SD_TP_SYSTEM_MAP):** 3,000 rows
- **Request Timeout:** 60 seconds

Upstream MDS api will ensure the data quality and own the validation of the cobdate.

| MDS api Green Zone | From | To |
| --- | --- | --- |
| SGT | Sat 12:00 PM | Sun 6:00 PM |
| GMT | Sat 4:00 AM | Sun 10:00 AM |

[TD-006: Design of MDS Payment Holiday Description Data Integration - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/TD-006%3A+Design+of+MDS+Payment+Holiday+Description+Data+Integration)

### Connection details:

### Interface Specification:

![image-2026-1-22_22-19-55.png](attachments/image-2026-1-22_22-19-55.png)

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