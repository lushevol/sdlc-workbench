# background

In bank transactions, we need to deal on BUSINESS DAY, meanwhile different country got different calendar for BUSINESS DAY, so we need to markdown the CURRENCY HOLIDAY for each party. and in service【51358-ratan-cash-settlement-group-management-service】will write Cutoff date according to currency holiday set in 【51358-ratanone-static-data-service】

For Indonesia(here we refer to it as ID), 'cause of the policy restrictions, we** can not mount NAS in ID server**, which means the RDM files cannot be read. but we still need to consider the currency holiday compensation function. therefore comes the following analysis.

There are 2 ways to set currency holiday in 【51358-ratanone-static-data-service】,and the way2 is a compensation to way1.

**EXPAND: way 1: real-time call**

| topic | Rdm_Currency_Holiday_Weekend_In | consumer |
| --- | --- | --- |
| | { "code": "200", "status": "Success", "header": { ** "serviceName": "RDM00463",(specialHoliday,**RDM00470 ||RDM00846**)** "serviceVersion": "v1", "generatedTimestamp": "2022-03-29 17:38:27 HKT", "trackingId": "c9a6c97b-77ae-4a47-8099-8bf6d948907d" }, "data": { "centerId": 43, "isoCurrencyCode": "ZWL", ** "isoMicCode": "****XAG****",(specialHoliday , replace isoCurrencyCode)** "isoCountryCode": "ZW", "relatedFinancialCenter": "Harare", "eventYear": 2052, "eventDate": "28122053", "eventDayOfWeek": "Sat", "eventName": "Weekend", "dayType": "WKD", "fileType": "C", "entityState": "ACTIVE", "createdTime": "29032022 17:30:45", "modifiedTime": null } } | RdmMessageConsumer.onRdmHolidayWeekendMessageReceived() 1.insert a "new RdmMessage()" to ratan_static_rdm_holiday_weekend_message 2. syncData to ratan_static_cashflow_currency_holiday 2.1 entityState case ACTIVE: save/update case DELETED: delete 3.send msg to topic = **Static_Data_Holiday_Update_In** but no consume find |

**EXPAND_END**

**EXPAND: way 2: EOD call for file notification**

**EXPAND: kafka topic**

1.rdm file notification

| topic = Rdm_FileIT_Notification_In |
| --- |
| { "IMFTFileNotification": { "Header": { "Version": "1.0", "Identifier": "BRDM_BNKCODE_GL", "UUID": "5d127960-2cf6-42fa-82fa-f6604ca119fd", "SrcJMSID": "ID:10.23.100.84865f197508a37380:0", "Source": "38430-RDM", "Target": "51358-RATAN", "Country": "GL", "Timestamp": "2025-06-09 01:15:29.487 +0800" }, "Payload": { "Status": { "Causes": { "Details": [ "File Arrived at Receiver" ] }, "Code": "5000", "Reason": "CFT_NOTIFICATION" }, "SubComponent": "BRDM_RATAN_BNKCODE_GL", "SrcFilePath": "/share/imft070/ratanone/all_rdm_bcdf_15a6_registered_staff_§_1.dat.gz", "Component": "CFT", "TrackingID": "F0901193" } } } |
![image-2026-7-6_10-57-56.png](attachments/image-2026-7-6_10-57-56.png)

**EXPAND_END**

**EXPAND: code analyze-4 consumers**

| | consumer1: BcdfReconFileConsumer | consumer2: RdmCommonFileConsumer | consumer3: CountryCodeBcdfReconFileConsumer | consumer4: BrdmMessageConsumer |
| --- | --- | --- | --- | --- |
| groupId | Static-Data-Bcdf-FileIT-Group | Static-Data-Rdm-Bcdf-Common-FileIT-Group | Static-Data-Bcdf-FileIT-Country-Code-Group | Static-Data-Brdm-Group |
| checkMessageAndGetFileName（） | 1.reconFileName contains "all_rdm_bcdf_CurrencyHoliday" 2. reconFileName today or yesterday | 1.reconFileName contains "rdm_bcdf_rules_engine_configuration" "rdm_bcdf_murex_structures_and_strategies" "rdm_bcdf_15a6_registered_staff" 2. reconFileName today or yesterday | 1.reconFileName contains "rdm_bcdf_countrycode" 2. reconFileName today or yesterday | 1.reconFileName contains "rdm_bcdf_bankcode" 2. reconFileName today or yesterday |
| getRdmFileData（） | holidayWeekendService.extractBcdfData（） filter data f.startsWith("d§PayloadData§") f.contains("§ACTIVE§") f.contains(thisYearDelimiter)|| f.contains(nextYearDelimiter) | 1.findByFileNameOrderByUpdatedAtDesc from table =ratan_static_brdm_history 2.isPresent?updateBrdmHistoryDataRecord:createBrdmHistoryDataRecord 3.process(sourceFile); 3.1 processFile operate table ratan_rdm_15a6_registered_staff ratan_rdm_structures_strategies ratan_rdm_rules_engine_configuration 3.2 purgeAgedFiles 3.3 updateActionTypeHistory | rdmCountryCodeService.extractBcdfData（） filter data f.startsWith("d§PayloadData§") f.contains("§ACTIVE§") | 1.findByFileNameOrderByUpdatedAtDesc from table=ratan_static_brdm_history 2.isPresent?updateBrdmHistoryDataRecord:createBrdmHistoryDataRecord 3.process(sourceFile); 3.1 processFile ratan_static_brdm_record 3.2 purgeAgedFiles 3.3 updateActionTypeHistory 4.return null; |
| reconData() | holidayWeekendService.reconData() 1.getCurrentVersion from table = ratan_static_cashflow_currency_holiday 2.find CashflowHoliday with currentVersion in table = ratan_static_cashflow_currency_holiday 3.holidayDbMoreList bcdfMoreList commonList 4.emailService.sendEmail() 5.1 if holidayDbMoreList.size() + bcdfMoreList.size()>20 no auto sync ratan process 5.2** recon-result-sync-to-db: false** no autoSyncDB | no implementation needed | 1.find RDMCountryInfo from table =ratan_static_cashflow_country_mapping 2.countryDbMoreList countryBcdfMoreList commonList 3.**recon-country-result-sync-to-db: true** autoSyncDB | empty method |
| **find usages** | **endpoint**: @PostMapping(value = "/v1/staticData/cashflow/shifterDate") @PostMapping(value = "/v1/staticData/cashflow/cutoffs")CashflowCutoffsController --- **entrypoint**: 51358-ratan-cash-settlement-group-management-service CashflowCutoffCommand.execute() (1)getMaterializeCutoff() (2)getCurrencyCutoff() | **endpoint**: @GetMapping(value = "v1/static/details") RuleStaticController --- **entrypoint**: 1. 51358-ratanone-ca-control-service 2. 51358-ratanone-rule-service (1)DefaultRuleEngineExecutionServiceTest.setUp() (2)[V2_0_2__add_constraint_insert.sql](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-rule-service?path=/src/main/resources/db/migration/V2_0_2__add_constraint_insert.sql&_a=contents&version=GBmain) ratan_scbml_field_rest_config | **endpoint**: @RequestMapping(path = "/v1/cashflow/country/countryName") CashflowCountryController --- **entrypoint**: 51358-ratan-cash-settlement-ssi-stamping-service （1）trade vostro ssi, findAvailableAccounts new VostroAccountFacade queryCountryNameByCode when ssiEntity is riskCountry (2) cashflow vostro ssi, filterOutInvalidSsi new VostroAccountFacade queryCountryNameByCode when ssiEntity is riskCountry Counterparty_Incorporated_Country_ISO_Code | **endpoint**: @RequestMapping(value = "/v1/static/lei") @PostMapping(value = "/query") BrdmLeiController LEI (Legal Entity Identifier) --- **entrypoint**: 51358-ratanone-swift-service (1) TOPIC=KR_MXG_SWF_IN_Internal GROUP =cash-settlement-swift-service internalConsumptionForKoreaMurex>customizeFields>leiEnhancement call queryLei (2) @RequestMapping("/v1/iso/exception")@PostMapping("/replay/{trackingId}/{sourceSystem}/{businessFlow}/{originalExceptionId}")ExceptionHandlingController.replayException() |
| **need the func for ID** | **yes** | **no，only trade ongoing rulecheck will call** **confirmed with @Dong, ziqian** | **yes** | **no, only UK chaps will queryLei** **confirmed with @Feng, xinxin** |

**EXPAND_END**

**EXPAND: [consumer 1]-Currency Holiday concumer**

**EXPAND_END**

**EXPAND: [consumer 3] data usage-[ssi service]**

**EXPAND_END**

**EXPAND: [consumer 4] bankcode Consumer**

**EXPAND_END**

**EXPAND_END**

# conclusion

| | consumer 1: BcdfReconFileConsumer | consumer 2: RdmCommonFileConsumer | consumer 3: CountryCodeBcdfReconFileConsumer | consumer 4: BrdmMessageConsumer |
| --- | --- | --- | --- | --- |
| RDM-FILE | all_rdm_bcdf_CurrencyHoliday | "rdm_bcdf_rules_engine_configuration" "rdm_bcdf_murex_structures_and_strategies" "rdm_bcdf_15a6_registered_staff" | rdm_bcdf_countrycode | rdm_bcdf_bankcode |
| TABLE | ratan_static_brdm_history | ratan_rdm_15a6_registered_staff ratan_rdm_structures_strategies ratan_rdm_rules_engine_configuration | ratan_static_cashflow_country_mapping | ratan_static_brdm_record |
| NEED FOR ID | yes | no, only trade to call this rulecheck | yes | no, only UK will queryLei |

---

# Tech design

## currencyHoliday+specialHoliday

### **option 1**: no rdm-flie syncDB, keep the current behavior to GDC (**not chosen**, ID need the compensation data)

no code change, then on RDM compensation

### **option 2**: sync from GDC  (**not chosen**, we need to separate GDC and ID, and may not use RDM-FILEIT in the future, confirmed with @Geoferry)

need code change to compatible to both GDC and ID

**EXPAND: Detail**

**EXPAND_END**

### **option 3**: EOD call API (**chosen**, may valid for both GDC and ID)

| env | currencyHoliday-url | specialHoliday-url |
| --- | --- | --- |
| dev | https://[10.83.161.226:8453/rdm_api/service/v2/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231](https://10.83.161.226:8453/rdm_api/service/v2/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231)&page=1&entityState=DELETED | https://[10.83.161.226:8453](https://10.83.161.226:8453/rdm_api/service/v2/holidayCalendarSpecial?dateFrom=20250101&dateTo=20261231&page=2)[/rdm_api/service/v2/holidayCalendarSpecial?dateFrom=20250101&dateTo=20261231&page=2](https://10.83.161.226:8453/rdm_api/service/v2/holidayCalendarSpecial?dateFrom=20250101&dateTo=20261231&page=2) |
| stg | [https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v2/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231](https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v1/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231) | [https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v2/holidayCalendarSpecial?dateFrom=20250101&dateTo=20261231&page=2](https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v1/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231) |
| prod | [https://gateway.51242.app.standardchartered.com/rdm_api/service/v2/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231](https://gateway.51242.app.standardchartered.com) | [https://gateway.51242.app.standardchartered.com/rdm_api/service/v2/holidayCalendarSpecial?dateFrom=20250101&dateTo=20261231&page=2](https://gateway.51242.app.standardchartered.com) |

**EXPAND: Detail**

**EXPAND_END**

## countryCode

### option: call RDM API

| env | url |
| --- | --- |
| dev | https://[10.83.161.226:8453/rdm_api/service/v1/countries](https://10.83.161.226:8453/rdm_api/service/v1/countries) |
| stg | <u>[https://gateway-stg.51242.app.standardchartered.com/rdm_api](https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v1/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231)[/service/v1/countries](https://10.83.161.226:8453/rdm_api/service/v1/countries)</u> |
| prod | [https://gateway.51242.app.standardchartered.com](https://gateway.51242.app.standardchartered.com)/rdm_api/service/v1/countries |

**EXPAND: detail**

**EXPAND_END**

## PT

| URL | COUNT | TIME | ES |
| --- | --- | --- | --- |
| [https://fmo-mfe-preprod.id.standardchartered.com:8453/api/ratan/v1/static/data/recon/currencyHoliday?dateFrom=20220209&dateTo=20250209](https://fmo-mfe-preprod.id.standardchartered.com:8453/api/ratan/v1/static/data/recon/currencyHoliday?dateFrom=20220209&dateTo=20250209) | totalRecord = 587089+2262 totalPage=296 eachTime=2+0.5=2.5s totalTime =12m | Sep 22, 2026 @ 19:50:12.522 Sep 22, 2026 @ 20:02:57.526 | Discover - Elastic |

## Question

**EXPAND: Q&A**

| NO | Q | A |
| --- | --- | --- |
| 1 | RDM-FILEIT working mechanism | (1) HK 8am RDM call third-party CoppClark (2) if data available, then download files>compare>(Delta/dfiff)data to RDM (3) SO, after 9AM the date will offer in RDM (4)before 6PM IST,ID will add the date temporarily for currencyHoliday |
| 2 | has CountryCode realtime topic? | no, countryCode changed rarely. |
| 3 | in ID-STG better use domain name to call API? need LDAP ID to set in Kong Gateway [https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v1/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231](https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/v1/holidayCalendarCurrencyHldyWkend?dateFrom=20250101&dateTo=20261231) | (1) Kong token‘s expire time, should store it in localThread? (2) [https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/rdmdata?api=/v2/holidayCalendarCurrencyHldyWkend&dateFrom=20220209&dateTo=20260210](https://gateway-stg.51242.app.standardchartered.com/rdm_api/service/rdmdata?api=/v2/holidayCalendarCurrencyHldyWkend&dateFrom=20220209&dateTo=20260210) status:200 response body is null |
| 4 | about consumer4:BrdmMessageConsumer--→for bankcode | was called in swift-service only UK-chaps need call queryLei API, this will set the response to xmlEntity, if ID do need to call this API, and the result is null, no error uk-chaps-condition: sender: "^SCBLGB.*" receiver: "^SCBLGB.*" currency: "^GBP$" |
| 5 | when call api by CTRL-M job with parameters, what's the actions in open-api.auth ? 5 url : [https://fmo-shell.gdc.standardchartered.com:8453/api/](https://fmo-shell.gdc.standardchartered.com:8453/api/v1/cashflow/lifecycle/holding-release%27)idns/ --- [http://localhost:8989/v1/static/data/recon/currencyHoliday](http://localhost:8989/v1/static/data/recon/currencyHoliday) [http://localhost:8989/v1/static/data/recon/specialHoliday](http://localhost:8989/v1/static/data/recon/specialHoliday?dateFrom=20260209&dateTo=20260210&page=2) [http://localhost:8989/v1/static/data/recon/countryCode](http://localhost:8989/v1/static/data/recon/countryCode) | (1)default search params: (no dynamic params suggested by @Cai1, jie) dateFrom: yesterday dateTo: today page:1 (2)open-api: auth: required: true actions: - RATAN_INTERNAL_FUNC:STATIC_SERVICE:**FETCHANDUPDATE** (3)no need to add actions in ratanone-auth-server for - username: ratanone-control-m password: ${RATANONE_CONTROL_M_PWD} actions: - RATAN_INTERNAL_FUNC:CASHFLOW_SERVICE:AUTO_NETTING - RATAN_INTERNAL_FUNC:CASHFLOW_SERVICE:AUTO_FAILING - RATAN_INTERNAL_FUNC:CASHFLOW_SERVICE:HOLDING_RELEASE - RATAN_INTERNAL_FUNC:DA_SERVICE:REFRESH_COUNTERPARTY_CACHE - RATAN_INTERNAL_FUNC:STATIC_SERVICE:**FETCHANDUPDATE** - RATAN_INTERNAL_FUNC:DA_SERVICE:REFRESH_HASHICORP_CACHE - RATAN_INTERNAL_FUNC:STATIC_SERVICE:PORTFOLIO (4) GDC control-m to call id in prod? （cause control-m is deprecated, will be replaced by others） |
| 6 | (1)to compare the diff between RDM and RATAN findByEventDateTimestampBetweenAndVersionAndRatanLabel take time longer, is this filter good? (2) when does a holiday will mark as updated or deleted? if 4 fileds(centerId,eventDate,eventName,fileType )keep the same??? | (1)query by rdmUniqueKeys ~~@Query(""" SELECT * FROM ratan_static_cashflow_currency_holiday holiday WHERE holiday.version = :version AND holiday.rdm_unique_key IN (:rdmUniqueKeys) AND holiday.ratan_label = :ratanLabel """)~~ ~~findByVersionAndRdmUniqueKeysAndRatanLabel~~ findByVersionAndRdmUniqueKeyIn (2)just insert/delete no need to update ratan holiday, cause query by RdmUniqueKeys from RDM-API.response.data(only filter RdmUniqueKeys) （3）in RDM, currencyHoliday.primaryKey = ( center_id, event_date, event_name, file_type) **only 1 center Id for each currency** DELETE: if primaryKey change --->DELETE UPDATE: if !primaryKey change --->UPDATE |
| 7 | API result of dateFrom , dateTo | >=dateFrom,<dateTo |
| 8 | TIMEZONE HK: UTC+8 --- WIB: UTC+7 (Jakarta) WITA: UTC+8 WIT: UTC+9 | ID control-M :After 8am IST GDC control-M: After 9am HK |
| 9 | HTTPS request about RDM-API in dev, no domain name, can not pass the truststore in JVM | skip ssl @Profile("dev") |
| 10 | date format diff ( RDM-realtime-MSG and RDM-API) RDM-realtime-MSG example: "eventDate": "28122053", "createdTime": "29032022 17:30:45", --- RDM-API response example: "eventDate": "17/05/2025", "createdTime": "03/03/2025 01:29", "modifiedTime": "31/07/2025 15:30" | call DateConvertUtil while get response from RDM, so I can use previous method to createHolidayEntity while insert |
| 11 | Can RDM return lastPage flag in response? | (1)using the following expression to cycle the RDM-API: loop 1: Integer totalPageNo = (totalRecords+ pageSize-1) / pageSize; loop n: Boolean fetchNextPage = dataQuery.getPage()<= totalPageNo; |
| 12 | RDM-API-countryCode the first page is different between currencyHoliday and countryCode? currencyHoliday.first.pageNo =1 countryCode.first.pageNo =0 | **For RDM: ** (1)no configure pageSize for country, default value is 100 **For RATAN: ** (1)coz we have got totalPageNo in the first call, so no risk here |
| 13 | Location of RDM? Location of KONG gateway? | RDM ---> HK and SG KONG --->not sure |
| 14 | for RDM.specialHolidayApi.response, no dayType specialHoliday { "centerId": 96, "isoMicCode": "PLTS-NAC", "isoCountryCode": "US", "exchangeName": "Platts North America Crudewire", "eventYear": 2026, "eventDate": "18/01/2026", "eventDayOfWeek": "Sun", "eventName": "Weekend", "fileType": "X", "entityState": "ACTIVE", "createdTime": "09/02/2026 23:13", "modifiedTime": "" } currencyHoliday { "centerId": 51, "isoCurrencyCode": "AED", "isoCountryCode": "AE", "relatedFinancialCenter": "Dubai", "eventYear": 2022, "eventDate": "02/01/2022", "eventDayOfWeek": "Sun", "eventName": "Weekend", "dayType": "WKD", "fileType": "C", "entityState": "ACTIVE", "createdTime": "05/05/2022 17:34", "modifiedTime": "21/04/2025 20:11" } rdm_unique_key ='138|09052026|Weekend|X' or rdm_unique_key ='138|12122026|Weekend|X' | dayType |

**EXPAND_END**