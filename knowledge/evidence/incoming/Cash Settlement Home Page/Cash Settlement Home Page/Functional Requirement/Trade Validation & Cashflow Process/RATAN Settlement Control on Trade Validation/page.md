# Validation Workflow

| Timeline | MO Workflow | Settlements Workflow | Mitigation Control | Settlement Manual Action with Trade Validation |
| --- | --- | --- | --- | --- |
| Current CN Flow - STELLA | - MO Validated Stella CN Trades in RATAN | Cashflow push to cashflow blotter without Validation check | - The payments will not STP since the trade is not matched and - Settlements team would be doing a Cashflow Affirmation with counterparty before releasing the payment | No |
| Current CN Flow - MX2.11 | - MO Validate trades in MX2.11 | Cashflow push to cashflow blotter without Validation check | - The payments will not STP since the trade is not matched and - Settlements team would be doing a Cashflow Affirmation with counterparty before releasing the payment | No |
| Flow 29th July to 10th Aug( SG/MY/IN/CN) | No changes to process | All entities will be same with current CN BAU | Same with current CN BAU | No |
| From 10th Aug | No changes to process | - Cashflow flow to RATAN cashflow blotter only post Validation(SG/MY/IN) - CN cashflows would follow the current BAU | | - Monitoring the cashflow which trade not validated and manually push to cashflow blotter( For the cases trade validation is not available on value date) |
| Sep 2024( TBC) | Stella/CDU enhancement - Auto Validation - SCF/LoanDepo | - Cashflow flow to RATAN cashflow blotter only post Validation | | Reduction in the manual touch for Stella cashflows |
| Until Trade Migration | | | | Manual action required for pushing Cashflows for exception cases when trade is not validated |

# Validation Workflow Post 10th Aug

# Functionality of group blotter of current production (not related to Trade Validation Status)

- Ensure all cashflows belong to particular market events received - Reversal & Rebook - CCS interest pay & receive( fix VS Fix) - CCS initial notional payments - Initial notional payment & first period interest payment
- Non Eco amendment compare, when full group arrived, Ratan is able to compare all withdrawals/news to find the non-eco amendment and ignore them for decrease ops manual effort to handle reversal and rebook.

# Scenarios requiring manual action on grouping blotter

- Murex fail to send the cashflow: Volume in past 4 months is 46 cashflows - Cashflow suppose sent to RATAN but stuck in the Murex workflow: Sample as below | **Trade Event** | **Payment ID** | **Reversal & Rebook** | **Value Date** | **Date Sent to RATAN** | RATAN Status | Manual Monitoring & Push Action | | --- | --- | --- | --- | --- | --- | --- | | New Booking | 103916452 | | 2024-06-25 | 2024-06-17 | NSTP | | | C&R | 106649728 | Reversal of 103916452 | 2024-06-25 | 2024-06-24 | Pending in blotter waiting for 106649729 | Manually push to Cashflow Blotter | | 106649729 | Rebook of 103916452 | 2024-06-25 | 2024-06-25 | | | - Cashflow suppose sent to RATAN got cancelled before it's feeding to RATAN | **Trade Event** | **Payment ID** | **Murex Payment Status** | **Reversal & Rebook** | **Value Date** | Date Sent to RATAN | RATAN Status | Manual Monitoring & Push Action | | --- | --- | --- | --- | --- | --- | --- | --- | | New Booking | 106267096 | INIT | | 2024-06-13 | NA | NA | | | 106267099 | SNTR | | 2024-06-13 | 2024-06-13 | Pending in blotter waiting for 106267096 | Manually push to Cashflow Blotter | | C&R | 106267096 | CNCL | | 2024-06-13 | NA | | |
- Non Eco Amendment: - Volume of Murex 2.11 Non Eco Amendment: - 200 for H1 entities: SG/MY/IN/CN in 3 months - 2000 for all entities in 3 months - Sample case which manual action required in group blotter | **Murex** | | **RATAN** | | --- | --- | --- | | **Murex Event** | **Trade ID** | **Status** | **Trade id** | **Payment Id** | **Cashflow ID** | **Cashflow Event** | **Cashflow Status** | **STP/NSTP** | | New Booking | 92060188 | CHCK | | | | **92060188** | 101912951 | M00101912951 | New | Pending Validation( expecting trade id 92060188) | NSTP | | Non ECO C&R | 92060188 | CHCK | | | | | | | | 92060252 | CHCK | | | | | | | | | | | | | | | | | | Status update | 92060252 | CHCK | | | | | | | | Validation | **92060252** | VALD | | | | | | | | Confirmation | 92060252 | COMP | | | | | | |