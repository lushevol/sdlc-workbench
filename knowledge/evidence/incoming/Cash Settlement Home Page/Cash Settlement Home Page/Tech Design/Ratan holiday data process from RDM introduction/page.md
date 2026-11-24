# Overall process flow

# DB structure

raw message table – **ratan_static_rdm_holiday_weekend_message**

![image-2025-7-7_16-22-53.png](attachments/image-2025-7-7_16-22-53.png)

structured data table – **ratan_static_cashflow_currency_holiday**

column rdm_unique_key is data combined key, used for duplicate check, it contains: center_id + event_date + event_name + file_type

![image-2025-7-7_16-23-51.png](attachments/image-2025-7-7_16-23-51.png)

# RDM portal

[https://rdm.global.standardchartered.com/rdm/rdm/ember/dist/index.html#/home](https://rdm.global.standardchartered.com/rdm/rdm/ember/dist/index.html#/home) (prod data)

This portal can query RDM prod data from GUI, login account uses SSO.

RDM dev SPOC: [Indrani.Kandasamy@sc.com](mailto:Indrani.Kandasamy@sc.com)

RDM BA: [GokulPrasath.J1@sc.com](mailto:GokulPrasath.J1@sc.com)

1. select Browse Data

![image-2025-7-9_11-3-31.png](attachments/image-2025-7-9_11-3-31.png)

2. select Holiday Calendar

![image-2025-7-9_11-4-3.png](attachments/image-2025-7-9_11-4-3.png)

3. select these 2 weekend panels

![image-2025-7-9_11-5-58.png](attachments/image-2025-7-9_11-5-58.png)

4. can input search text to query

![image-2025-7-9_11-7-17.png](attachments/image-2025-7-9_11-7-17.png)

## Ordinary Holiday wiki from RDM

[Currencies Holiday & Weekend (Solace PubSub)]

[Currencies Holiday & Weekend (Full BCDF)]  full data via fileIT

## Special Holiday wiki from RDM

[Special Holiday (Solace PubSub)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2516700769)

## FileIT full data

prod file path sample: /share/imft054/ratanone/all_rdm_bcdf_CurrencyHolidayWknd_15042025_d_1.dat.gz

prod sample data:

📎 [all_rdm_bcdf_CurrencyHolidayWknd_15042025_d_1.dat.gz](attachments/all_rdm_bcdf_CurrencyHolidayWknd_15042025_d_1.dat.gz)

## FileIT interface wiki

[Solace Message Structure And Taxonomy](https://confluence.global.standardchartered.com/display/IMFT/Solace+Message+Structure+And+Taxonomy) –  as ratan only plays as a consumer from FileIT notification, so in this doc we can only read from chapter "3.1.2.1 Notification Message".

## Message Sample

### service name intro

ordinary holiday: RDM00463 (same in prod and test), RDM00493 (same in prod and test), RDM00827 (same in prod and test)

special holiday: RDM00470 (prod only), RDM00846 (test only)

```js
{
  "code": "200",
  "status": "Success",
  "header": {
    "serviceName": "RDM00827",
    "serviceVersion": "v1",
    "generatedTimestamp": "2025-07-02 20:18:47 HKT",
    "trackingId": "6965a06b-65e1-422c-9314-f3aa7c3fc912"
  },
  "data": {
    "centerId": 7,
    "isoCurrencyCode": "CNY",
    "isoCountryCode": "CN",
    "relatedFinancialCenter": "Beijing",
    "eventYear": 2026,
    "eventDate": "28112026",
    "eventDayOfWeek": "Sat",
    "eventName": "Weekend",
    "dayType": "WKD",
    "fileType": "C",
    "entityState": "ACTIVE",
    "createdTime": "10032022 14:02:50",
    "modifiedTime": "14112023 16:41:44"
  }
}
```

```js
{
    "IMFTFileNotification": {
        "Header": {
            "Version": "1.0",
            "Identifier": "FRDM_HOLIDAY_GL",
            "UUID": "1ee4498a-21ce-4e96-b32f-3c9ee1809af1",
            "SrcJMSID": "ID:10.23.100.84b4c9197dff184690:0",
            "Source": "38430-RDM",
            "Target": "51358-RATAN",
            "Country": "GL",
            "Timestamp": "2025-07-06 21:34:02.95 +0800"
        },
        "Payload": {
            "Status": {
                "Causes": {
                    "Details": [
                        "File Arrived at Receiver"
                    ]
                },
                "Code": "5000",
                "Reason": "CFT_NOTIFICATION"
            },
            "SubComponent": "FRDM_RATAN_HOLIDAY_GL",
            "SrcFilePath": "/share/imft054/ratanone/all_rdm_bcdf_CurrencyHolidayWknd_05072025_d_1.dat.gz",
            "Component": "CFT",
            "TrackingID": "G0621335"
        }
    }
}
```