Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Terris Li | 2026-03-25 | @Quill Li @Terris Li | 2026-03-25 | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> CES (formerly known as EMS3) is the strategic entitlement solution in FM. It aims to provide a centric approach for FM system to manage data entitlement and provides a consolidated view on data accessing rules. FM-CES (strategic data entitlement solution),
>
> The integration will leverage CES APIs for entitlement checks, ensure authentication via FMAA tokens, and include mechanisms for service resilience, selective enablement, and caching.
>
> By regulatory requirement, Ratan integrated with FMCES on data entitlement, allow OPS to view on need to know basis, different profile/location would see cashflows only under allowed list of entities.
>
>
>
> **Core concepts:**
>
> - **Data Policy**: A set of rules are linked user’s HR profile. This will be automatically inherited by a new user. The data policy is managed by Policy Owner / COO.
> - **Data Profile**: A set of rules linked to user’s Role profile. Data profile is assigned to a user based on his role by the EMS3 operator.
> - **Role**: Role is a representation of the specific activities that a user is allowed to perform within the Business functions that he/she has access to within an application.
>
> Data Profile (Role based) rules will take precedence as a general rule over Data Policy (HR Profile) rules.  Example:
>
> Data policy constraints Korea trading by non Korea users, and to allow users from GB to trade Korea trades in non Korea trading hours a Data Profile override need to be setup.

### E2E Data Flow:

Describe the end to end  flow.

> RATAN call CES API to get data entitlement. 
>
> 1. RATAN --(API)--> FM CES
>
> NOTE: For menu and button function entitlement is still controlled by calling EMS2 API. So far CES is for data entitlement of RATAN Cashflow blotter and BCS Cashflow blotter only.

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