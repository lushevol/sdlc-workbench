# Background & Operation Control:

As requested by FMO Ops different roles required in their BAU to control the operation risk considering the seniority of the ops colleagues.

- Different profiles defined from junior to senior.
- Junior profile can handle the payment under the predefined threshold, while senior profiles have higher threshold.
- Threshold defined in USD for each profile would be static data which can be updated in the BAU.

# New profiles to be added:

- 5 is for on shore MO with limit action only, like Netting & Cashflow affirmation.
- 6 is global Maker profile.
- 7-10 are the global checker profiles with different limit threshold. | **SL** | **Persona** | **Profile Description** | **Current RATAN Profile** | **New RATAN profile** | **Static Profile Actions** | **Business Rules Profile Actions** | **Equivalent RAZOR Profile** | **USD Limit** | **Settlement Actions Allowed** | **Settlement High Risk Actions Allowed** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | 1 | FMO user excluding Setts/Conf | FMO Read Only Profile | FMO_RO | - | - | - | - | 0 | - | - | | 2 | Non FMO user | Non-FMO Read Only Profile | NON_FMO_RO | - | 0 | | 3 | PSS user | PSS Read Only Profile | PSS_RO | - | 0 | | 4 | Middle Office user | FMO Middle Office Profile | FMO_MO | - | 0 | | 6 | FMO Maker | FMO Maker Profile | FMO_OPS | FMO_OPS_MKR | 0 | Maker actions like SI Input, Netting etc | | 7 | FMO Checker (Standard) | FMO Clerk Profile | FMO_OPS_BOC | GBL_BOC_ST | < 30 Million | Maker actions + Approve exceptions below USD 30 Million | | 8 | FMO Officer Profile | FMO_OPS_BO | GBL_BO_ST | < 100 Million | Maker actions + Approve exceptions below USD 100 Million | | 9 | FMO Checker (High Value) | FMO Lead Profile | FMO_OPS_SUP | FMO_OPS_BOL | GBL_BOL_ST | < 1 Billion | Maker actions + Approve exceptions below USD 1 Billion | Approve 1) Adhoc Netting 2) Amendment / cancellation post payment release 3) Exceptions >= USD 100 Mio 4) CPN across FX and Deriv | | 10 | FMO Manager Profile | FMO_OPS_BOM | GBL_BOM_ST | <= 4 Billion | Maker actions + Approve exceptions Upto USD 4 Billion | | 11 | Static Data Maker | Static Maker Profile | - | FMO_STA_MKR | Client Level Netting Flag | - | 0 | - | - | | 12 | Static Data Checker | Static Checker Profile | - | FMO_STA_CKR | 0 | | 13 | Business Rules Maker | Settlement Business Rules Maker | - | FMO_BR_MKR | | 1) USD Limit amount of profiles 2) Suppression Rules Table 3) NSTP Rules Table 4) Netting Rules Table | 0 | | 14 | Business Rules Approver | Settlement Business Rules Approver | - | FMO_BR_APR | 0 |

# Profile & Limit Static data GUI:

- Maker/Checker required for record creation/update/delete.
- The Maker form | Filed Name | Field Type | Comment | | --- | --- | --- | | Profile Name | Text | Type in by user | | Limit | Numeric | Type in by user |

# USD Amount calculation

- Get the currency from cashflow, logical model field is Cashflow.Payment_Currency
- Get the payment amount from cashflow, logical model field is Cashflow.Payment_Amount
- If Cashflow.Payment_Currency == USD then the payment amount would be the final value, otherwise call Stella FX Conversion API to fetch the spot rate. 1. API fx/rates/date/eodTag/baseCurrency/quoteCurrency 2. Base currency would be the currency in cashflow e.g. GBP 3. quote currency would be USD 4. Get the spotRate from API response and calculate the USD amount, target USD amount = Non USD Amount( e.g. GBP) * spotRate. ```js Response Payload : { "status":"SUCCESS", "data": [ { "date": "2021-03-15", "eodTag": "OFFICIAL_EOD_UK", "baseCurrency": "GBP", "quoteCurrency": "USD", "spotRate": "1.356" } ] } ```

<u>***Auth Limt***</u>

Currently the Auth limit is calculated on the fly and without any table, However going forward, we should use the Auth limit in a different table as this is only for Ratan, 
we would have to create a new table in the DB with 4 Important Fields

1 Profile

2 Currency

3 USDConverted

4 Limit,

when ever the trade is booked, the system should check if the user has the limit to verify/Approve the cashflow  If Yes, show Submit/Approve button if not Do not show