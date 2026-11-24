Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Zhenzhen Liu @Junying Jiang @Yunzhe Ta | 2026-01-26 | @Zhenzhen Liu @Daiqi Wang | 2026-01-26 | |

### Description:

For user management, Ratan connects to **EMS2**, where user entities are centrally managed.

When a Ratan user logs in, the system calls **EMS2** to retrieve the list of **subjects** under the **`X_RATANONE`** entity.

This subject list is then used to:

- Determine which **blotters** should be displayed to the user.
- Control **right-click operation permissions** (i.e., who has access to context menu actions).

This mechanism enables dynamic, role-based UI customization based on the user’s assigned subjects.

For other applications try to connect to RATAN, access is secured through **FMAA authentication (**FM Authentication Adapter (FMAA) is the name for the authentication API).

Upon successful authentication, FMAA will issue a tken that can be used to authorize access to the respective systems.

### E2E Data Flow:

For user management, Ratan connects to **EMS2**, where user entities are centrally managed.

For other applications try to connect to RATAN, access is secured through **FMAA authentication**

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

**Below as sample to get the user role  **

[https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/account/1431837](https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/account/1431837)

**Below as sample to get user list for [X_RATANONE](https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entitlements/entity/name/X_RATANONE)**

Prod - [https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entitlements/entity/name/X_RATANONE](https://sabre-prod-ems2.gdc.standardchartered.com:16443/ems2/rest/entitlements/entity/name/X_RATANONE)

Non-Prod - [https://uklvauems01a.uk.standardchartered.com:16443/ems2/rest/entitlements/entity/name/X_RATANONE](https://uklvauems01a.uk.standardchartered.com:16443/ems2/rest/entitlements/entity/name/X_RATANONE)

![image-2026-4-23_11-45-10.png](attachments/image-2026-4-23_11-45-10.png)