# Branch Code

1. data from application.yml in static-service ``` ratanone.sd: branch-code: mappings: - bookingEntitySciFmid: 400001378 branchCode: 73 - bookingEntitySciFmid: 10020899 branchCode: 73 - bookingEntitySciFmid: 235003861 branchCode: 73 - bookingEntitySciFmid: 10078716 branchCode: 73 - bookingEntitySciFmid: 10036642 branchCode: 73 - bookingEntitySciFmid: 10062461 branchCode: 73 - bookingEntitySciFmid: 10032025 branchCode: 73 - bookingEntitySciFmid: 400054708 branchCode: 73 - bookingEntitySciFmid: 400054737 branchCode: 73 - bookingEntitySciFmid: 400054741 branchCode: 73 - bookingEntitySciFmid: 400057714 branchCode: 73 - bookingEntitySciFmid: 400075752 branchCode: 73 - bookingEntitySciFmid: 400085753 branchCode: 73 - bookingEntitySciFmid: 400090093 branchCode: 73 - bookingEntitySciFmid: 400095464 branchCode: 73 - bookingEntitySciFmid: 400130180 branchCode: 73 - bookingEntitySciFmid: 400130178 branchCode: 73 - bookingEntitySciFmid: 400185419 branchCode: 73 - bookingEntitySciFmid: 400193370 branchCode: 73 - bookingEntitySciFmid: 400209000 branchCode: 73 - bookingEntitySciFmid: 400218197 branchCode: 73 - bookingEntitySciFmid: 400220273 branchCode: 73 - bookingEntitySciFmid: 400229749 branchCode: 73 - bookingEntitySciFmid: 400516443 branchCode: 73 - bookingEntitySciFmid: 400516442 branchCode: 73 - bookingEntitySciFmid: 400667486 branchCode: 73 - bookingEntitySciFmid: 400677737 branchCode: 73 - bookingEntitySciFmid: 400683682 branchCode: 73 - bookingEntitySciFmid: 400798477 branchCode: 73 - bookingEntitySciFmid: 400899993 branchCode: 73 - bookingEntitySciFmid: 401053411 branchCode: 73 - bookingEntitySciFmid: 300036368 branchCode: 21 - bookingEntitySciFmid: 3 branchCode: 20 - bookingEntitySciFmid: 400452428 branchCode: 19 - bookingEntitySciFmid: 400451508 branchCode: 18 - bookingEntitySciFmid: 9 branchCode: 28 - bookingEntitySciFmid: 400093619 branchCode: 28 - bookingEntitySciFmid: 4 branchCode: 40 - bookingEntitySciFmid: 400960089 branchCode: 44 - bookingEntitySciFmid: 10075222 branchCode: "02" - bookingEntitySciFmid: 400906330 branchCode: "09" - bookingEntitySciFmid: 10 branchCode: "05" - bookingEntitySciFmid: 400041070 branchCode: "02" - bookingEntitySciFmid: 6 branchCode: 22 - bookingEntitySciFmid: 2 branchCode: 60 - bookingEntitySciFmid: 300075472 branchCode: 60 - bookingEntitySciFmid: 10038345 branchCode: 66 - bookingEntitySciFmid: 300011345 branchCode: 67 - bookingEntitySciFmid: 400018439 branchCode: 98 - bookingEntitySciFmid: 5 branchCode: 51 - bookingEntitySciFmid: 8 branchCode: 27 - bookingEntitySciFmid: 10036428 branchCode: 58 - bookingEntitySciFmid: 7 branchCode: 10 - bookingEntitySciFmid: 10036382 branchCode: 62 - bookingEntitySciFmid: 400032489 branchCode: 71 - bookingEntitySciFmid: 400045551 branchCode: 45 - bookingEntitySciFmid: 300089409 branchCode: 59 - bookingEntitySciFmid: 401036553 branchCode: 34 - bookingEntitySciFmid: 400007847 branchCode: 47 - bookingEntitySciFmid: 400991880 branchCode: 16 - bookingEntitySciFmid: 400910415 branchCode: "05" - bookingEntitySciFmid: 10036430 branchCode: 55 - bookingEntitySciFmid: 10041530 branchCode: 29 - bookingEntitySciFmid: 300011525 branchCode: 39 - bookingEntitySciFmid: 300084297 branchCode: 82 - bookingEntitySciFmid: 10040387 branchCode: 50 - bookingEntitySciFmid: 10037477 branchCode: 35 - bookingEntitySciFmid: 10041903 branchCode: 52 - bookingEntitySciFmid: 10036655 branchCode: 97 - bookingEntitySciFmid: 10036647 branchCode: 84 - bookingEntitySciFmid: 10022098 branchCode: 85 - bookingEntitySciFmid: 10041902 branchCode: UG - bookingEntitySciFmid: 300010782 branchCode: QA - bookingEntitySciFmid: 401081696 branchCode: QA - bookingEntitySciFmid: 300011470 branchCode: 86 - bookingEntitySciFmid: 10036645 branchCode: 70 ``` ![image-2026-8-28_14-36-40.png](attachments/image-2026-8-28_14-36-40.png)
2. related API /v1/branchCode/{branchCode} ![image-2026-8-28_14-37-48.png](attachments/image-2026-8-28_14-37-48.png) being used by ratanone-swift-service take MT103SwiftGenerator.setField20 as an example ![image-2026-9-18_9-32-17.png](attachments/image-2026-9-18_9-32-17.png) being used by accounting-service content stored in ratan_accounting_request_task.branchCode and request_info->narratives ![image-2026-9-18_9-34-6.png](attachments/image-2026-9-18_9-34-6.png)![image-2026-9-18_9-34-53.png](attachments/image-2026-9-18_9-34-53.png)
3. Sample Data ![image-2026-9-1_8-37-53.png](attachments/image-2026-9-1_8-37-53.png) ![image-2026-9-1_8-27-49.png](attachments/image-2026-9-1_8-27-49.png)
4. if not config in swift-service will throw exception ![image-2026-9-18_11-43-20.png](attachments/image-2026-9-18_11-43-20.png)

# Swift Generation Config

1. data from ratanone_swift_service.swift_static_data_sender_bic ratanone_swift_service.swift_static_data_correspondent_bic
2. logic code internal ![image-2026-9-10_16-28-21.png](attachments/image-2026-9-10_16-28-21.png) senderBic is used at swift_message.senderBic countryCode is used at swift_message.countryCode CorrespondentBic is used at MT103SwiftGenerator.Field53A
3. Sample Data ![image-2026-9-1_8-38-3.png](attachments/image-2026-9-1_8-38-3.png) ![image-2026-9-1_8-28-55.png](attachments/image-2026-9-1_8-28-55.png)
4. if not config sender_bic in swift-service will throw exception as bellow ![image-2026-9-18_14-38-35.png](attachments/image-2026-9-18_14-38-35.png)

# Release Time Config

1. data from table: ratan_static_cashflow_currency_cut_off
2. API /cashflow/cutoffs ![image-2026-9-10_16-8-20.png](attachments/image-2026-9-10_16-8-20.png) being used by ratan-cash-settlement-group-management-service at path /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/scb:paymentCutoffTime ![image-2026-9-10_16-10-15.png](attachments/image-2026-9-10_16-10-15.png) which will lead to below change in xml ![image-2026-9-10_16-14-46.png](attachments/image-2026-9-10_16-14-46.png)
3. API /cashflow/cutoffs/batch ![image-2026-8-28_15-17-17.png](attachments/image-2026-8-28_15-17-17.png) being used by ratan-cash-settlement-group-management-service
4. Sample Data ![image-2026-9-1_8-38-21.png](attachments/image-2026-9-1_8-38-21.png) ![image-2026-9-1_8-34-25.png](attachments/image-2026-9-1_8-34-25.png)
5. if not config in static-service will use bellow ``` currency-cutoff: shifter: -1 shifter-unit: BUSINESS DAY time: "18:00:00" ```

# Accounting Generation Config

1. data from ratanone.ratan_static__cashflow_ebbs_txn_code ratanone.ratan_static__cashflow_ebbs_bridge_account
2. API /v1/ebbs/account/{fmId} ![image-2026-9-10_17-17-26.png](attachments/image-2026-9-10_17-17-26.png) being used by ratan-cash-settlement-accounting-service at field ratan_accounting_request_task.bridgeAccountNumber
3. API /v1/ebbs/txn/{fmId} ![image-2026-9-10_17-17-39.png](attachments/image-2026-9-10_17-17-39.png) being used by ratan-cash-settlement-accounting-service at field ratan_accounting_request_task.request_info->data->attributes->request->transaction entry->transaction-code
4. Sample Data ![image-2026-9-1_8-38-34.png](attachments/image-2026-9-1_8-38-34.png) ![image-2026-9-1_8-37-27.png](attachments/image-2026-9-1_8-37-27.png)
5. if not config ebbs_bridge_account in accounting-service will throw exception as bellow ![image-2026-9-18_14-24-48.png](attachments/image-2026-9-18_14-24-48.png)

# CountryZoneId Mapping

1. data from application.yml related mapping(country->zoneId) ``` ratanone: time-zone: mappings: - country: CN zoneId: Asia/Shanghai - country: SG zoneId: Singapore - country: MY zoneId: Asia/Kuching - country: IN zoneId: Asia/Kolkata - country: UK zoneId: GMT - country: GB zoneId: GMT - country: DE zoneId: Europe/Berlin - country: US zoneId: America/New_York - country: TW zoneId: Asia/Taipei - country: HK zoneId: Asia/Hong_Kong - country: TH zoneId: Asia/Bangkok - country: JP zoneId: Asia/Tokyo - country: AE zoneId: Asia/Dubai - country: PH zoneId: Asia/Manila - country: ID zoneId: Asia/Jakarta - country: MU zoneId: Indian/Mauritius - country: ZA zoneId: Africa/Johannesburg - country: EG zoneId: Africa/Cairo - country: NP zoneId: Asia/Kathmandu - country: SA zoneId: Asia/Riyadh - country: JE zoneId: Europe/Jersey - country: KE zoneId: Africa/Nairobi - country: TZ zoneId: Africa/Dar_es_Salaam - country: LK zoneId: Asia/Colombo - country: VN zoneId: Asia/Ho_Chi_Minh - country: PK zoneId: Asia/Karachi - country: BD zoneId: Asia/Dhaka - country: KR zoneId: Asia/Seoul ```
2. logic code internal ![image-2026-9-10_17-31-19.png](attachments/image-2026-9-10_17-31-19.png) fmid->country ![image-2026-9-18_9-48-15.png](attachments/image-2026-9-18_9-48-15.png)
3. if not config in accounting-service will use GMT

# ISO Currency Mapping

1. data from application.yml ``` ratanone.sd: holiday-currency-list: // non-ISO to ISO - BRO|BRL - CNO|CNY - CNH|CNY - EGO|EGP - IDO|IDR - INO|INR - KRO|KRW - MYO|MYR - PHO|PHP - RUO|RUB - TWO|TWD - VNO|VND - THO|THB - LKO|LKR - THN|THB - DOL|USD - NGO|NGN - XD1|XPD - XD2|XPD - XG1|XAG - XR1|XRH - XT1|XPT - XT2|XPT - XT3|XPT - AOH|AOA - XU4|XAU - XU5|XAU - XD3|XPD - XG2|XAG - XU1|XAU - XU2|XAU - XU6|XAU - XU7|XAU - KEH|KES - TZH|TZS - XUC|XAU - NGY|NGN - XU8|XAU - XG3|XAG - XGC|XAG - EUO|EUR - JPO|JPY - CNF|CNY - GHH|GHS - UGH|UGX - SGB|SGD - SGO|SGD - JPB|JPY - EUB|EUR - NGH|NGN - XUD|XUD - ZMH|ZMW - BDO|BDT - NGX|NGN - NGA|NGN - IDY|IDR - LKH|LKR - RUW|RUB - MZH|MZN - PKH|PKR - THS|THB - MYZ|MYR - INY|INR - CNS|CNY - PKO|PKR - NGB|NGN ```
2. API /v1/iso/currency/{currency} ![image-2026-8-28_14-13-38.png](attachments/image-2026-8-28_14-13-38.png) being used by ratanone-swift-service take MT103SwiftGenerator.setField32A as an example ![image-2026-9-18_9-21-20.png](attachments/image-2026-9-18_9-21-20.png) being used by accounting-service content stored in ratan_accounting_request_task.isoCurrency ![image-2026-9-18_9-23-59.png](attachments/image-2026-9-18_9-23-59.png)![image-2026-9-18_9-25-10.png](attachments/image-2026-9-18_9-25-10.png)
3. refers:
4. if not config in static-service will return origianl currency

# Rounding Config

1. data from table ratan_cashflow_group_management_service.ratan_cashflow_rounding_config
2. API /v2/roundingConfig/{currency} ![image-2026-9-10_15-46-7.png](attachments/image-2026-9-10_15-46-7.png) directly used by UI ![image-2026-9-10_15-51-3.png](attachments/image-2026-9-10_15-51-3.png)
3. API /v1/currency/rounding ![image-2026-9-10_15-46-13.png](attachments/image-2026-9-10_15-46-13.png) being used by ratan-cash-settlement-fx-utilization-service ![image-2026-8-28_15-1-46.png](attachments/image-2026-8-28_15-1-46.png)
4. method is used internal ![image-2026-9-10_15-55-17.png](attachments/image-2026-9-10_15-55-17.png)
5. trigger point 1) message inbound processing ![image-2026-9-18_10-21-54.png](attachments/image-2026-9-18_10-21-54.png) 2) message is processed in workflow ![image-2026-9-18_9-11-3.png](attachments/image-2026-9-18_9-11-3.png)
6. Data Sample ![image-2026-9-1_8-37-43.png](attachments/image-2026-9-1_8-37-43.png) ![image-2026-9-18_9-15-26.png](attachments/image-2026-9-18_9-15-26.png)
7. if not config in group-service will return origianl amount

# Config Used Analysis

| | Config | API | Service in use | Multi Service Used(Common) |
| --- | --- | --- | --- | --- |
| 1 | ISO Currency Mapping |
| 2 | ratan_cashflow_rounding_config | /v1/currency/rounding in ratan-cash-settlement-group-management-service | fx-utilization-service group-management-service | Yes |
| 3 | ISO Currency Config: ``` ratanone.sd: holiday-currency-list: - BRO|BRL ``` | /v1/iso/currency/{currency} in ratanone-static-data-service | accounting-service swift-service | Yes |
| 4 | /v1/staticData/cashflow/shifterDate/batch in ratanone-static-data-service | group-management-service |
| 5 | | | | |
| 6 | Branch Code |
| 7 | ``` ratanone.sd: branch-code: mappings: - bookingEntitySciFmid: 400001378 branchCode: 73 ``` | /v1/branchCode/{branchCode} in ratanone-static-data-service | accounting-service swift-service | Yes |
| 8 | | | | |
| 9 | Swift Generation Config |
| 10 | swift_static_data_sender_bic swift_static_data_correspondent_bic in ratanone-swift-service | -- | swift-service | No |
| 11 | | | | |
| 12 | Release Time Config |
| 13 | ratan_static_cashflow_currency_cut_off | /v1/staticData/cashflow/cutoffs in ratanone-static-data-service | group-management-service lifecycle-service | Yes |
| 14 | | | | |
| 15 | Accounting Static |
| 16 | ratan_static__cashflow_ebbs_txn_code ratan_static__cashflow_ebbs_bridge_account | /v1/ebbs/account/{fmId} /v1/ebbs/txn/{fmId} in ratanone-static-data-service | accounting-service | No |