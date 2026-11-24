# Reminder:

- ## *For entitlement X_RATANONE and RATAN_DATA_ENTITLEMENT, currently can only use bulk request to grant access, corresponding E-Form still in progress of upgrade*

# Navigation

- ## Go to myIT Service Catalogue, search for RATAN and select RATAN ID Creation/Amendment with URL: [Catalog Item - Service Portal (service-now.com)](https://scbnow01.service-now.com/itsp?id=sp_sc_cat_item&sys_id=c5b6df4887d5a9501e0deb150cbb35b9)

![image2023-10-25_14-22-29.png](attachments/image2023-10-25_14-22-29.png)

- ## Select your Group and Sub Group as requirement

![image2023-10-31_14-7-47.png](attachments/image2023-10-31_14-7-47.png)

- ## Select required Role as your access, then submit the request.

| Request Category | Request Group | Request Sub-Group | Role | Request Data Entitlement Role | New/Existing |
| --- | --- | --- | --- | --- | --- |
| ~~RATAN Function Access Role~~ | ~~FMO~~ | ~~Business Rule Approver~~ | ~~FMO_BR_APR~~ | ~~Global/GBS/Onshore~~ | Removed |
| ~~RATAN Function Access Role~~ | ~~FMO~~ | ~~Business Rule Maker~~ | ~~FMO_BR_MKR~~ | ~~Global/GBS/Onshore~~ | Removed |
| RATAN Function Access Role | FMO | MO User | FMO_MO | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | MO Super User | FMO_MO_SUP | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Operations User | FMO_OPS | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Operations Back Office Officer | FMO_OPS_BO | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Clerk | FMO_OPS_BOC | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Leader | FMO_OPS_BOL | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Manager | FMO_OPS_BOM | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Investigator | FMO_OPS_INV | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Maker | FMO_OPS_MKR | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Super User | FMO_OPS_SUP | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | FMO Read Only User | FMO_RO | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Static Data Checker | FMO_STA_CKR | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Static Data Maker | FMO_STA_MKR | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | NON FMO | NON FMO Read Only User | NON_FMO_RO | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | PSS | PSS | PSS_RO | Global/GBS/Onshore | Existing |
| RATAN Data Entitlement Role | N/A | N/A | GBS | GBS | New |
| RATAN Data Entitlement Role | N/A | N/A | Global | Global | New |
| RATAN Data Entitlement Role | N/A | N/A | Onshore | Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Supervisor | FMO_OPS_BOS | Global/GBS/Onshore | New |

- ## Select required Subject as your access, then submit the request.

| | Subject in request | Tile in RATAN ONE |
| --- | --- | --- |
| 1 | RATAN_TRADE_BLOTTER | Trade Processing - Trade Blotter |
| 2 | RATAN_CASHFLOW_BLOTTER | Settlement - Cashflow Blotter [FX & Equity] |
| 3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Settlement - Cashflow Blotter |
| 4 | RATAN_CASHFLOW_GROUP_BLOTTER | Settlement - Grouping Blotter |
| 5 | RATAN_VALIDATION_EXCEPTION | Exception Management - Validation Exceptions |
| 6 | RATAN_SETTLEMENT_EXCEPTION | Exception Management - Settlement Exceptions |
| 7 | RATAN_PROFILE_LIMITS | Business Rule- Authorization Limits |
| 8 | RATAN_SETTLEMENT_STP_RULE | Business Rule - Settlement NSTP Rules Business Rule - Settlement NSTP Rules [FX & Equity] |
| 9 | RATAN_SUPPRESSION_RULE | Business Rule - Suppresion Rules Business Rule - Suppresion Rules [Swift] Business Rule - Suppresion Rules [Cashflow] |
| 10 | RATAN_AUTO_NETTING_RULE | Business Rule - Auto Netting Rules |
| 11 | RATAN_ENTITLEMENT_RULE | Business Rule - Data Entitlement Rules |
| 12 | RATAN_NOSTRO_BLOTTER | Static - Nostro Static |
| 13 | RATAN_NETTING_RULE | Static - Netting Static |
| 14 | RATAN_NOSTRO_BLOTTER | Static - BIC Netting Static |
| 15 | ~~RATAN_MO_EXCEPTION~~ | Unused for now |

- ## Request Approver list.

| Profile | Approver_Group | Approvers |
| --- | --- | --- |
| FMO_MO | Ratan_FMO_MO_User_Approvers | 1579123;1658668;1551697 |
| FMO_MO_SUP | Ratan_FMO_MO_Sup_User_Approvers | 1579123;1658668;1551697 |
| PSS_RO | Ratan_PSS_RO_User_Approvers | 1612478;1399585 |
| FMO_STA_CKR | Ratan_FMO_Sta_Dat_User_Approvers | 1624508;1629651;1165312 |
| FMO_STA_MKR |
| NON_FMO_RO | Ratan_NON_FMO_RO_User_Approvers | 1607036;1364100;1166409;1658804 |
| FMO_OPS | Ratan_FMO_Ops_User_Approvers | 1607036;1364100;1166409;1658804 |
| FMO_OPS_SUP | Ratan_FMO_Ops_Sup_User_Approvers | 1598139;1658804;1364100;1166409 |
| FMO_RO | Ratan_FMO_RO_User_Approvers | 1607036;1364100;1166409;1658804 |
| FMO_BR_APR | Ratan_FMO_Ops_BusinessRules_User_Approver | 1364100;1166409;1658804 |
| FMO_BR_MKR |
| FMO_OPS_BO | Ratan_FMO_Settlement_User_Approvers | 1364100;1166409;1658804 |
| FMO_OPS_BOC |
| FMO_OPS_BOL |
| FMO_OPS_BOM |
| FMO_OPS_MKR |
| FMO_OPS_BOS |
| FMO_OPS_INV | Ratan_FMO_Investigation_User_Approvers | 1207323;1658804 |
| GBS | Ratan_Data_Entitlement_Approvers | |
| Global |
| Onshore |