# Phase 1 - BCS Authorization Limit Control

In Ratan UAT2 env,  testing with different users. The users' profile limit details are shown in the table below

| Profile Name | Ccy | Limitation |
| --- | --- | --- |
| FMO_OPS_BOM | USD | 90 |
| FMO_OPS_BOL | USD | 999999999 |

Test case:

| Checker Actions | Cashflow Detail | User Profile | Result |
| --- | --- | --- | --- |
| NSTP Checker Approval | cashflow id: 010363213787 amount: 2,797.98, ccy: USD | FMO_OPS_BOM | ![release1.png](attachments/release1.png) |
| FMO_OPS_BOL | ![release2.png](attachments/release2.png) |
| Cashflow Affirmation | cashflow id: 010364809654 amount: 2,108.00, ccy: USD | FMO_OPS_BOM | ![affirm.png](attachments/affirm.png) |
| FMO_OPS_BOL | ![affirm2.png](attachments/affirm2.png) |
| Failed Cashflow Release | cashflow id: 010365445001 amount: 900.10, ccy: USD | FMO_OPS_BOM | ![faild0.png](attachments/faild0.png) |
| FMO_OPS_BOL | ![fail1.png](attachments/fail1.png) |

# Phase 2