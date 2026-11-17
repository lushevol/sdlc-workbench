# Background

For ID go live, RDM-day0 data should be init

**EXPAND: prod data status**

select substr(event_date ,5),count(1)  from ratanone.ratan_static_cashflow_currency_holiday group by substr(event_date ,5)

select * from  ratanone.ratan_static_cashflow_currency_holiday
 where event_date_timestamp>'2026-01-01 00:00:00' and  event_date_timestamp < '2027-01-01 00:00:00'    and created_at>'2025-11-28 01:00:00' and created_at<'2025-11-30 23:00:00'

| substr(event_date ,5) | count(1) | question |
| --- | --- | --- |
| 2022 | 17772 | 【17439】create 2021-04-24 19:44:00.000 update null |
| 2023 | 17928 | 【17666】create 2021-04-24 19:44:00.000 update null |
| 2024 | 18081 | 【17391】create 2021-04-24 19:44:00.000 update 2023-11-25 18:02:42 |
| 2025 | 18079 | 【17308】create 2021-04-24 19:44:00.000 update 2024-11-30 18:10:16 |
| 2026 | 17917 | 【17057】create 2025-11-29 17:50:37 update 2025-11-30 09:05:29 but, in RDM【17285】records created at 24/04/2021 11:44， |
| 2027 | 395 | RDM.currencyHoliday.count = 17630 |
| 2028 | 359 | RDM.currencyHoliday.count = 17888 |
| 2029 | 350 | RDM.currencyHoliday.count = 17808 |
| 2030 | 353 | |
| 2031 | 352 | |
| 2032 | 344 | |
| 2033 | 351 | |
| 2034 | 340 | |
| 2035 | 348 | |
| 2036 | 353 | |
| 2037 | 347 | |
| 2038 | 343 | |
| 2039 | 346 | |
| 2040 | 352 | |
| 2041 | 353 | |
| 2042 | 356 | |
| 2043 | 346 | |
| 2044 | 341 | |
| 2045 | 344 | |
| 2046 | 345 | |
| 2047 | 353 | |
| 2048 | 349 | |
| 2049 | 345 | |
| 2050 | 342 | |
| 2051 | 338 | |
| 2052 | 353 | |
| 2053 | 351 | |
| 2054 | 348 | |
| 2055 | 17543 | create 2024-01-04 13:02:40 |
| 2056 | 17775 | create 2025-01-04 12:00:16 |
| 2057 | 17712 | create 2026-01-06 12:45:40 |

**EXPAND_END**

# Options

| dataSource | plan | keyPoint | comment | steps |
| --- | --- | --- | --- | --- |
| RDM | 1 | /v1/cashflow/currency/holiday/upload | need extra effort, cause column **rdm_unique_key **was introduced later, but the upload logic has not been updated to persist this field. | csv column | db more column | | --- | --- | | Iso_Currency_Code, Event_Date, Event_Date_Timestamp, Event_Day_Of_Week | iso_country_code center_id event_name file_type day_type rdm_unique_key | | (1) get csv (each year 547KB*30 >16M) (2)change code |
| csv column | db more column |
| Iso_Currency_Code, Event_Date, Event_Date_Timestamp, Event_Day_Of_Week | iso_country_code center_id event_name file_type day_type rdm_unique_key |
| **2 prefer** | add sql in dbRepo | yes, prod env ratanone.ratan_static_cashflow_currency_holiday.count = 152604 but we only need date between 2026.9.1-2027.12.31, That's =23370 records | (0)export excel from [RDM - Reference Data Management](https://rdm.global.38430.app.standardchartered.com/rdm/rdm/ember/dist/index.html#/home) about currencyHoliday and specialHoliday in 2026.9.1-2027.12.31 , import the csv to (in GDC-DEV) (1) export sql from ratanone.ratan_static_cashflow_currency_holiday_gjl (in GDC-DEV) (2)add 23370 records in dbrepo to init |
| 3 | RDM API | need extra effort, (date range will return you the data created/modified within the range). currencyHoliday.count = 638007 (23/04/2021 to today) specialHoliday.count = 11590 (23/04/2021 to today) add a cutoffDate 2026.9.1-2027.12.31 | (1) controlM call currencyHolidayAPI (2) controlM call specialHolidayAPI exception: api will return in 6m |
| GDC | 4 | currencyHoliday migration from GDC to ID | NO, event_date_timestamp>2026-09-01 | (1)migrate from GDC, dump data when eventDate>20260901 (for countryCode, trigger api by control-M schedule) (2)manually trigger api by ansible pipeline or PSS trigger control-m job to sync holiday form day0 to business golive |

# Control-M job

| no | function | [PROD]url [https://fmo-mfe.gdc.standardchartered.com:8453/](https://fmo-mfe.gdc.standardchartered.com:8453/) | [STG] url https://[fmo-mfe-preprod.id.standardchartered.com](http://fmo-mfe-preprod.id.standardchartered.com):8453 | variable parameter |
| --- | --- | --- | --- | --- |
| 1 | reconCurrencyHoliday | [~~https://fmo-shell.gdc.standardchartered.com:8453~~/api/idns](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/currencyHoliday?dateFrom=20220209&dateTo=20260210)[/ratan](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/countryCode)[/v1/static/data/recon/currencyHoliday?dateFrom=20260929&dateTo=20270101](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/currencyHoliday?dateFrom=20220209&dateTo=20260210) | [https://fmo-mfe-preprod.id.standardchartered.com:8453](https://fmo-mfe-fmrp1.pi.dev.net:8453/)/api/ratan/v1/static/data/recon/currencyHoliday?dateFrom=20260929&dateTo=20270101 | dateFrom dateTo |
| 2 | reconSpecialHoliday | [~~https://fmo-shell.gdc.standardchartered.com:8453~~/api/idns](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/specialHoliday?dateFrom=20220209&dateTo=20260210)[/ratan](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/countryCode)[/v1/static/data/recon/specialHoliday?dateFrom=20260929&dateTo=20270101](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/specialHoliday?dateFrom=20220209&dateTo=20260210) | [https://fmo-mfe-preprod.id.standardchartered.com:8453/](https://fmo-mfe-fmrp1.pi.dev.net:8453/)[api/ratan/v1/static/data/recon/specialHoliday?dateFrom=20260929&dateTo=20270101](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/specialHoliday?dateFrom=20220209&dateTo=20260210) | dateFrom dateTo |
| 3 | reconCountryCode | [~~https://fmo-shell.gdc.standardchartered.com:8453~~/api/idns/ratan/v1/static/data/recon/countryCode](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/countryCode) | [https://fmo-mfe-preprod.id.standardchartered.com:8453/](https://fmo-mfe-fmrp1.pi.dev.net:8453/)[api/ratan/v1/static/data/recon/countryCode](https://fmo-shell.gdc.standardchartered.com:8453/api/idns/v1/static/data/recon/countryCode) | |