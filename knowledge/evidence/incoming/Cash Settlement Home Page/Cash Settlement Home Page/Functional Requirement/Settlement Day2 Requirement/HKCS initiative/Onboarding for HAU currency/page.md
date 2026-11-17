# check list

| | item | check item | status | change in ratan? | impact scope | comment |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | static data | static data - spot rate conversion for HAU | | no change | service: ratanone-static-data-service table: ratanone.ratan_static_spot_rate interface: StaticSpotRateController.getSpotRate <details> <summary>Expand Details</summary> select * from ratanone.ratan_static_spot_rate where quote_currency = 'HAU'; </details> | |
| 2 | static data - holiday config for HAU | | no change | service: ratanone-static-data-service <details> <summary>Expand Details</summary> select * from ratanone.ratan_static_cashflow_currency_holiday where iso_currency_code = 'HAU' and text("version") = (select activated_version from ratanone.ratan_static_activated_version where table_name = 'ratan_static_cashflow_currency_holiday' and active = true); </details> | how does pseudo currency map to ISO currency to get holiday config <details> <summary>Expand Details</summary> ![image-2026-7-22_11-30-20.png](attachments/image-2026-7-22_11-30-20.png) </details> |
| 3 | static data - currency cutoff config for HAU | | change | service: ratanone-static-data-service table: ratanone.ratan_static_cashflow_currency_cut_off <details> <summary>Expand Details</summary> select * from ratanone.ratan_static_cashflow_currency_cut_off where currency = 'HAU' and text("version") = (select activated_version from ratanone.ratan_static_activated_version where table_name = 'ratan_static_cashflow_currency_cut_off' and active = true); </details> | copy from XAU <details> <summary>Expand Details</summary> ![image-2026-7-22_14-5-11.png](attachments/image-2026-7-22_14-5-11.png) </details> |
| 4 | static data - PM currency static data for HAU | | change | service: ratanone-swift-service table: ratanone_swfit_service.swift_static_pm_currency | |
| 5 | static data - ISO currency mapping for HAU | | no change | service: ratanone-static-data-service config: [ratanone.sd](http://ratanone.sd).holiday-currency-list (onshore|offshore) | |
| 6 | static data - rounding config for HAU | | change | service: ratan-cash-settlement-group-service | copy from XAU, 3 decimals, rounding off |
| 7 | frontend static data - currency dropdown list for HAU in GUI | | change | | add dropdown list item for HAU <details> <summary>Expand Details</summary> ![image-2026-7-22_11-13-59.png](attachments/image-2026-7-22_11-13-59.png) </details> |
| 8 | vostro setup | | no change | SSI+ | |
| 9 | nostro setup | | no change | service: ratanone-data-ambassador table: ratanone.ratan_static__cashflow_nostro | |
| 10 | micro service | swift service | | change | service: ratanone-swift-service | need customization, detail in requirement |
| 11 | accounting service | | change | service: ratan-cash-settlement-accounting-service | not need to publish accounting for HAU |
| | ssi stamping service | | change | service: ratan-cash-settlement-ssi-stamping-service | need generate missing vostro exception for HAU receive due to it is mandatory |
| | static data service | | change | service: ratanone-static-data-service | separately maintain holiday non iso currency to iso currency |
| 12 | lms message publishing | | no change | service: ratan-cash-settlement-lms-service | need to publish lms message |

# TBD list

| | item | |
| --- | --- | --- |
| 1 | for HAU, MT605 update field 20 prefix to CANC | |
| 2 | separately maintain holiday non iso currency to iso currency mapping | |

# test in lower environment

## test for HAU in UAT1

| | step | comment |
| --- | --- | --- |
| 1 | setup nostro | <details> <summary>Expand Details</summary> ``` INSERT INTO ratanone.ratan_static__cashflow_nostro (id, legal_entity, legal_entity_fmid, settlement_currency, ebbs_nostro_account, settlement_means, settlement_account, senders_correspondent53_swift, senders_correspondent53_fullname, senders_correspondent53_address, senders_correspondent53_city, senders_correspondent53_postcode, senders_correspondent53_account, created_at, updated_at, notice_to_receive, ratan_label, "version", currency_pair, data_status, maker_id, checker_id, tlm_set_id, primary_flag, nostro_static_id, start_date, end_date, data_version, nostro_type) VALUES('id-hk8ebce-00ba-4c1f-aa8f-98f64c651111', 'HONGKONG', '2', 'HAU', '99999191742', 'NOS', 'HAU MAIN', 'SCBLGB2LTSY', '', '', '', '', '', '2026-07-22 15:23:24.370', '2026-07-22 15:23:24.370', 'Y', 'live', 1, '', 'SAVE_CONFIRMED', 'SYSTEM', 'SYSTEMconfirm', '', true, 50300012, '2020-01-01', '9999-12-31', 3, 'DEFAULT'); ``` </details> |
| 2 | setup PM config for HAU | <details> <summary>Expand Details</summary> INSERT INTO ratanone_swift_service.swift_static_pm_currency(currency) VALUES ('HAU') ON CONFLICT (currency) DO NOTHING; </details> |
| 3 | setup swift static data for HAU | <details> <summary>Expand Details</summary> INSERT INTO ratanone_swift_service.swift_static_udf_swf_ls (k_currency, v_allocation, v_available_location, v_quality, v_type, v_unit) VALUES('HAU', 'UNALL', 'HONGKONG', '9950', 'GOLD', 'FOZ'); </details> |
| 4 | generate cashflow for HAU | cashflow id: M00127675004 ![image-2026-7-22_18-48-9.png](attachments/image-2026-7-22_18-48-9.png) |
| 5 | maker input vostro and select nostro then submit | ![image-2026-7-22_18-50-17.png](attachments/image-2026-7-22_18-50-17.png) |
| 6 | checker approve | ![image-2026-7-22_18-51-15.png](attachments/image-2026-7-22_18-51-15.png) |
| 7 | generate swift message for HAU | ![image-2026-7-22_18-51-55.png](attachments/image-2026-7-22_18-51-55.png) |

# service changes

| | service | feature branch | pr | pipeline | comment |
| --- | --- | --- | --- | --- | --- |
| 1 | ratan-cash-settlement-lifecycle-service | feature/14724643-HKCS-Initiative | | | |
| 2 | ratan-cash-settlement-accounting-service | feature/14724643-HKCS-Initiative | | | |
| 3 | ratanone-swift-service | feature/14724643-HKCS-Initiative | | | |
| 4 | ratan-cash-settlement-ssi-stamping-service | feature/14724643-HKCS-Initiative | | | |
| 5 | ratanone-static-data-service | feature/14724643-HKCS-Initiative | | | |
| 6 | db-repository | feature/14724643-HKCS-Initiative | | | **EXPAND: check sql** ``` --rounding logic for HAU select * from ratan_cashflow_group_management_service.ratan_cashflow_rounding_config where k_currency = 'HAU'; --PM currency for HAU select * from ratanone_swift_service.swift_static_pm_currency where currency = 'HAU'; select * from ratanone_swift_service.swift_static_udf_swf_ls where k_currency = 'HAU'; --cut off for HAU select * from ratanone.ratan_static_cashflow_currency_cut_off where id in ('hkcs0001da4e-d3e7-41ee-ae84-91cac3115648','hkcs0001da4e-d3e7-41ee-ae84-91cac5120724','hkcs0001da4e-d3e7-41ee-ae84-91cac5120767','hkcs0001da4e-d3e7-41ee-ae84-91cac5120810','hkcs0001da4e-d3e7-41ee-ae84-91cac5120853','hkcs0001da4e-d3e7-41ee-ae84-91cac3115251','hkcs0001da4e-d3e7-41ee-ae84-91cac4115363','hkcs0001da4e-d3e7-41ee-ae84-91cac5115487','hkcs0001da4e-6ac8-49c2-bd99-593500cfff04','hkcs0001da4e-3820-4298-9bc4-ca6a4f201546','hkcs0001da4e-1772-4619-a26d-473f82bc39bb','hkcs0001da4e-0a28-4d2e-aebf-c9f4dbf6c5e1','hkcs0001da4e-4c31-4f39-93b2-5c42d8be7c77','hkcs0001da4e-6e77-4a5f-8d17-2baf4f1e6a90','hkcs0001da4e-8f0d-46d1-a9a3-1d5c0b9f2e84','hkcs0001da4e-3e54-4c80-9f6e-7a2d13c8de35','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef0411','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef0630','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef0849','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef1068','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef1287','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef1506','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef1725','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef1944','hkcs0001da4e-2d44-43f0-9f5f-5fd5b7ef2163'); ``` **EXPAND_END** |

# ADO

| | ADO |
| --- | --- |
| 1 | [Story 15548535 [HKCS Initiative] sort the checklist for HAU currency onboarding](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15548535) |
| 2 | [Story 14900306 [HKCS Initiative] accounting processing for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14900306) |
| 3 | [Story 14900316 [HKCS Initiative] swift processing for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14900316) |
| 4 | [Story 15548867 [HKCS Initiative] vostro setup for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15548867) |
| 5 | [Story 14923453 [HKCS Initiative] nostro setup for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14923453) |
| 6 | [Story 14969343 [HKCS Initiative] FX rate verification](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14969343) |
| 7 | [Story 15548232 [HKCS Initiative] add a dropdown item in frontend for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15548232) |
| 8 | [Story 15548335 [HKCS Initiative] prepare cutoff data for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15548335) |
| 9 | [Story 15548837 [HKCS Initiative] prepare rounding config data for HAU currency](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15548837) |

# reference document

[HONG KONG Physical Gold Settlement initiative - Financial Markets Solutions Delivery - Confluence](https://confluence.global.standardchartered.com/display/GMSD/HONG+KONG+Physical+Gold+Settlement+initiative)

# test cases

| | test case | step | expect |
| --- | --- | --- | --- |
| 1 | for field 72 | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2(Receive) is waiting in ratan 3. after maker and checker submit and approve C2(Receive) 4. C2(Receive) will generate MT605 swift message | C2(Receive) will find another leg C1(Pay) |
| 2 | for field 72 - amendment | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2(Receive) was waiting in ratan 3. user perform amendment 4. C1(Pay), C2(Receive) will be cancelled and C3(Pay) and C4(Receive) will be generated 5. C3(Pay) and C4(Receive) is waiting in ratan 6. after maker and checker submit and approve C4(Receive) 7. C4(Receive) will generate MT605 swift message | C4(Receive) will find another leg C3(Pay) |
| 3 | for field 72 - amendment | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2(Receive) was waiting in ratan 3. user only amend C1(Pay) 4. C1(Pay) will be cancelled and C3(Pay) will be generated 5. C2(Receive) and C3(Pay) is waiting in ratan 6. after maker and checker submit and approve C2(Receive) 7. C2(Receive) will generate MT605 swift message | C2(Receive) can't find another leg C3(Pay) due to they belong to different major version |
| 4 | for field 72 - amendment | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2Receive) was waiting in ratan 3. after maker and checker submit and approve C2(Receive) 4. C2(Receive) generate MT605 swift message and settled 5. user perform amendment 6. C1(Pay) will be cancelled and C3(Pay) and C4(Receive) will be generated 7. C2(Receive), C3(Pay) and C4(Receive) is waiting in ratan 8. after maker and checker submit and approve C4(Receive) 9. C4(Receive) will generate MT604 swift message | C4(Receive) will find another leg C3(Pay) |
| | for field 72 - re-fixing | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2Receive) was waiting in ratan 3. user perform re-fixing 4. C1(Pay), C2Receive) will be cancelled and C3(Pay) and C4(Receive) will be generated 5. C3(Pay) and C4(Receive) is waiting in ratan 6. after maker and checker submit and approve C4(Receive) 7. C4(Receive) will generate MT605 swift message | C4(Receive) will find another leg C3(Pay) but shouldn't find C1(pay) due to it cancelled |
| 5 | for field 72 - re-fixing | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2(Receive) was waiting in ratan 3. user only re-fixing C1(Pay) 4. C1(Pay) will be cancelled and C3(Pay) will be generated 5. C2(Receive) and C3(Pay) is waiting in ratan 6. after maker and checker submit and approve C2(Receive) 7. C2(Receive) will generate MT605 swift message | C2(Receive) will find another leg C3(Pay) |
| 6 | for field 72 - re-fixing | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2Receive) was waiting in ratan 3. after maker and checker submit and approve C2(Receive) 4. C2(Receive) generate MT605 swift message and settled 5. user perform re-fixing 6. C1(Pay) will be cancelled and C3(Pay) and C4(Receive) will be generated 7. C2(Receive), C3(Pay) and C4(Receive) is waiting in ratan 8. after maker and checker submit and approve C4(Receive) 9. C4(Receive) will generate MT604 swift message | C4(Receive) will find another leg C3(Pay) but shouldn't find C1(pay) due to it withdrawal |
| 7 | for field 72 - re-fixing(edge case) | 1. user book C1(Pay) and C2(Receive) 2. C1(Pay) and C2Receive) was waiting in ratan 3. user perform re-fixing 4. C1(Pay) withdrawal and C2(Receive) withdrawal were not received by ratan 5. C3(Pay) and C4(Receive) is waiting in ratan 6. after maker and checker submit and approve C2(Receive) 7. C2(Receive) generate MT605 swift message and settled | C2(Receive) will find another leg C1(Pay) and C3(Pay) so C2(Receive) will be swift error due to multiple legs found |

# Appendix

| | scenario | |
| --- | --- | --- |
| 1 | adjusting the set-field order will affect the order of swift message**(in swift service)** | ![image-2026-9-2_15-44-41.png](attachments/image-2026-9-2_15-44-41.png) |
| | | |