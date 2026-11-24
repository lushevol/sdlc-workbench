# 1. NSTP rule setup

| No | NSTP Rule Condition | Exception Code | Operation Level | Exception Category | Bulk Eligible | Requestor/Eops reference | eOps | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ((Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT" && Cashflow__Payment_Type in ("Coupon", "Interim MTM")) || Cashflow__Is_Hard_Blocker == true) | Hard Block Swap Agent | MAKER_CHECKER | HARD_BLOCKER | Not ticked | Hard Block Swap Agent-Single cashflow | **SCH202G210A1190925068117 ** | ** ** |

# 2.FE checklist

| 1 | Settlement NSTP Rule (New) | When user do CRUD and add Exception Config, "HARD_BLOCKER" should display under Exception Category drop down list | "HARD_BLOCKER" should display under Exception Category | ![image-2025-9-11_16-34-16.png](attachments/image-2025-9-11_16-34-16.png) | |
| --- | --- | --- | --- | --- | --- |
| 2 | Cashflow Blotter - Single Cashflow | 1. User double click one cashflow with hardblocker exception and going to fix exception | exception code under "HARD_BLOCKER" category will show as the first one of Exceptions with error color same as high risk exception | ![image-2025-9-11_14-46-51.png](attachments/image-2025-9-11_14-46-51.png) | |
| 3 | Cashflow Blotter - Single Cashflow | 2. Maker "Submit" should be blocked | User click "Submit" button, error message in top of screen with "This is a Swap Agent Coupon or Interim MTM cashflow, can't be release from Ratan." | ![image-2025-9-11_14-56-28.png](attachments/image-2025-9-11_14-56-28.png) | |
| 4 | Cashflow Blotter - Single Cashflow | 3. Checker "Approve" should be blocked | User click "Approve" button, error message in top of screen with "This is a Swap Agent Coupon or Interim MTM cashflow, can't be release from Ratan." | same as above | |
| 5 | Cashflow Blotter - Bulk fix exception | 1. Choose multiple cashflow and some of those are met hard block exception and choose Bulk Submit. 2. User click "Submit" those cashflow met hard block exceptions cannot be post to BE. | Hard blocker exception will validation error and with strikethrough. When user click Submit button hard blocker would't post data to BE. | ![image-2025-9-11_14-59-58.png](attachments/image-2025-9-11_14-59-58.png) ![image-2025-9-11_15-0-18.png](attachments/image-2025-9-11_15-0-18.png) | |
| 6 | | | | | |

# 3.BE checklist

| service | version | sql |
| --- | --- | --- |
| ratan-cash-settlement-netting-service | 1.5.7 | select * from cash_netting_service.t_cashflow tc where tc.message like '%hardBlockerComponentType%' and tc.created_at > '2025-09-27'; |
| ratanone-rule-service | 2.3.11 | |
| ratan-rule-service | 2.2.4.5 | |
| ratanone-db-repository | | --check below field exists or not and check version is correct. -- field config select * from ratan_rule_service.ratan_suppression_fields_config where id in ('a770a624-b4dd-4dfd-bf41-d889cf78222f'); -- field select * from ratan_rule_service.ratan_suppression_fields where id in('069b1939-577f-47d4-8253-901e89d40777'); -- ratan_suppression_fields_xpath select * from ratan_rule_service.ratan_suppression_fields_xpath where id in ('5bfa098c-1142-4764-9ee8-996cf3f0b61f'); --check version select * from ratan_rule_service.ratan_suppression_fields_activated_version a where table_name in ('ratan_suppression_fields_config','ratan_suppression_fields'); |