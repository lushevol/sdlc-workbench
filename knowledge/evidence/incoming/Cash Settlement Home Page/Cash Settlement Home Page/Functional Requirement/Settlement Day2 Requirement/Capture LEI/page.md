# Background

The is regulatory Requirement from India. user is expecting system to auto populate the value for in scope payments to save manual efforts and avoid the mistake.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7412111](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7412111)

# Requirement Details

- LEI needs to be captured for - SCB Payments, not required for receipts - ISO currency in Swift is INR, means cashflow currency in (INR, INO, INY) - payment amount equal to or above INR 500 Mio - India branch only (FMID =4, FMCODE = SCB BOMBAY*MMB) - Settlement Means = 'NOS', Not required for 'Over-Account' or any other Settlement Means
- Both SCB and Counterparty LEI needs to be captured in Line 1 & 2. SCB LEI is RILFO74KP1CM8P6PCT96 - **SCB LEI**: get LEI from SCI with Entity.Booking_Entity_SCI_FMID (**NOTE**: current scope is only for fmid =4, so the LEI will always be "[RILFO74KP1CM8P6PCT96](http://72/SL/RILFO74KP1CM8P6PCT96)" ) - **Counterparty LEI**: get LEI from SCI with Entity.Counterparty_SCI_FMID - get LEI from SCI: legalEntity.regulatoryInfo.regulatoryFieldText where regulatoryTypeValue = 'MIFID' and regulatoryFields ='LEI' ![image-2025-5-16_17-20-12.png](attachments/image-2025-5-16_17-20-12.png) ![image-2025-5-16_17-3-38.png](attachments/image-2025-5-16_17-3-38.png)
- LEI to be captured on the SWIFT, no need to capture on the SI screen
- If SSI has value in field 70 / 72 line 1, then it must be pushed to Line 3 onwards
- In MT103, capture in field 70. In MT202, capture in field 72
- MT103+202COV scenario not required, MT202Flip not required
- no logic change for MT192/MT292, but value show up in 103/202 should automatically reflected in 192/292
- **sample data**: [**72:/SL/**RILFO74KP1CM8P6PCT96](http://72/SL/RILFO74KP1CM8P6PCT96) **//BL/**5493001JZ37UBBZF6L49
- **Exception case:** - LEI value will take the line 1 and line2 of field 70/72, system will ignore the values beyond line2 for 70 or line4 for 72 ![image-2025-5-20_14-10-50.png](attachments/image-2025-5-20_14-10-50.png)
- Impact to Swift message template : details updated to , please check tag70/72 logic for MT103 and MT202

# Release Note

# Business User Case

| AC-No | Function | Scenario | Expected Result | Sample in UAT |
| --- | --- | --- | --- | --- |
| | MT103 with LEI | 1. book cashflow (SCB pay, payment amount >=INR 500,000,000, booking entity FMID=4) 2. maker/checker release the cashflow | 1. cashflow received in Ratan and stamped to vostro with message type = MT103, settlement means= NOS 2. Swift generated with LEI added to field 70 | M02756535371 |
| | MT202 with LEI | 1. book cashflow (SCB pay, payment amount >=INR 500,000,000, booking entity FMID=4) 2. maker/checker release the cashflow | 1. cashflow received in Ratan and stamped to vostro with message type = MT202, settlement means= NOS 2. Swift generated with LEI added to field 72 | M01756535168 |
| | Other swift type with no LEI (MT202 Flip, MT103/202Cov, MT210) | 1. book cashflow (SCB pay, payment amount >=INR 500,000,000, booking entity FMID=4) 2. maker/checker release the cashflow | 1. cashflow received in Ratan and stamped SI to generate different swift type (MT202 Flip, MT103/202Cov, MT210) 2. Swift generated with no LEI added | |
| | MT103/202 but not meet the required condition | 1. book cashflow not meet any one of below condition (SCB pay, payment amount >=INR 500,000,000, booking entity FMID=4) 2. maker/checker release the cashflow | 1. cashflow received in Ratan and stamped to vostro with message type = MT103/MT202 2. Swift generated with no LEI added | |
| | | | | |

# Linkage

[FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)