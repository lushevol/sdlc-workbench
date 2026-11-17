# Background

One of the  major objective of FMRP 2025 H1 is Ratan is going to build the capacity generating the payment accounting entry and feed to Aspire. It would be EOD feeding by FileIT between Ratan and Aspire, the accounting entry file format would be csv.

For BANGKOK/TAIPEI/OBU TAIPEI/SCS HK/~~HONG KONG~~/NEWYORK entities, they are all Aspire countries, so accounting model is:

# Accounting Eligibility

Same with EBBS, refer to [Cash Settlement - EBBS Accounting - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2950676666)

| Cashflow Event | Action | CF Status | Accounting type | Comment |
| --- | --- | --- | --- | --- |
| New | | Release/Settled/SWIFT_SUPPRESSED/FAILED | New | Accounting entry generated with HOLDING/SENT status |
| Withdrawal | | SWIFT_SUPPRESSED/FAILED | New | On component cashflow, will need separate logic |
| Withdrawal | Release/Settle/Failed/SWIFT_SUPPRESSED | | Reversal | only sent when withdraw is in released |
| New/Withdrawal | Reinstate | | Reversal | reversal will be triggered immediately when reinstate |
| New | Unsuppressed | | Reversal | If SWIFT_SUPPRESS is send, reversal will be sent when checker approve unsuppress If SWIFT_SUPPRESS is holding, new will be disabled when maker trigger unsuppress |
| New | Un-net on SWIFT_SUPPRESSED/FAILED | DEAD | Reversal | If Netting resultant cashflow SWIFT_SUPPRESS/FAILED is sent, then un-net will send reversal If Netting resultant cashflow SWIFT_SUPPRESS/FAILED is holding, then un-net will be ignored |

- Reversal would be reverse flow of the latest accounting entry on the cashflow.

## Exception scenario and handling

| 1 | **Scenario** | **Exception Handling** |
| --- | --- | --- |
| 1 | Ratan didn’t generate accounting posting, as missing mandatory field value | Accounting will be hold in RATAN as MISSING_INFO accounting status |

# Accounting Status

| **Accounting Status** | **Account Status Reason** | **Comment** | **Action to fix the failure** |
| --- | --- | --- | --- |
| HOLD | | Accounting entry generated but not reaching VD yet, so holding the posting | Not Required |
| DISABLED | | Accounting entry generated but before posting, reversal scenario happened, so holding entry is disabled | Not Required |
| SUCCESS | | Accounting entry generated and sent to Aspire | Not Required |
| MISSING_INFO | | It's for the SWIFT_SUPPRESSED case when the Nostro is not available, Ratan won't generate the accounting entry Or if any mandatory field value is missing. | User manually fix outside of Ratan( maybe Oscar) |

# Business Scenario

| Action Type | Accounting Behavior |
| --- | --- |
| New | For cashflow with new action, If SCB pay, debit on Bridge account, credit on Nostro account (including over account/suspense account) If SCB receive, debit on Nostro account, credit on Bridge account |
| Reverse | For cashflow with withdrawal (cashflow event)/Unsuppressed/Reinstate action, If SCB pay, debit on Nostro account, credit on Bridge account If SCB receive, debit on Bridge account, credit on Nostro account |
| SWIFT_SUPPRESS/FAILED On Withdrawal component cashflow | NDF New(C1 released) -> Amend amount (N1 released =C1 withdrawal + C2) -> Withdrawal C2 (C2 withdrawal SWIFT_SUPPRESSED for accounting generation, N1 and C1 MT192 will be manually drafted in AMH) |

# 📎 [Accounting Scenarios.xlsx](attachments/Accounting Scenarios.xlsx)

# Technical Scenario

## Agreement:

1. EOD file should only include value date [past date, today] and released/settled/failed/swift_suppressed before **10 PM** local time's cashflow no matter whenever job is run
2. EOD file for each business day (Monday- Friday) is mandatory to have for Aspire, who can't skip (25th Dec and 1st Jan will be an exception).
3. If any delay post cutoff time for Aspire, RATAN still need to send the delayed file once ready. (Instruction required for Aspire to manually hold 0212 file, until 0211 file is processed to TLM).

## Happy Cases

| Cashflow ID | File Generated at 10 PM Normally | Sample Cashflow Value Date | Sample Cashflow Released/Settled/Failed/SWIFT_SUPP | Expected in File | Expected AsOfDate | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | Yes | 20250211 | Before 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250211_01.csv | 20250211 | |
| C02 | Yes | 20250211 | After 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250212_01.csv | 20250212 | |
| C03 | Yes | 20250212 | Before 20250212 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250212_01.csv | 20250212 | |

## Exception Case1 (10 PM job failed in RATAN, rerun at 10:20 PM)

| Cashflow ID | Sample Cashflow Value Date | Sample Cashflow Released/Settled/Failed/SWIFT_SUPP | Expected in File | Expected AsOfDate | Comment |
| --- | --- | --- | --- | --- | --- |
| At 20250211 10 PM, file generation to Apire failed |
| C01 | 20250211 | Before 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250211_01.csv | 20250211 | |
| C02 | 20250211 | After 20250211 10 PM | Will no be included in Aspire file, as cashflow not released yet | |
| At 20250211 10:20 PM, file generation to Apire rerun successfully |
| C01 | 20250211 | Before 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250211_01.csv | 20250211 | |
| C02 | 20250211 | After 20250211 10 PM | Will no be included in 20250211 file, as cashflow was released after 10 PM | |
| At 20250212 10:00 PM, file generated to Apire successfully |
| C02 | 20250211 | After 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250212_01.csv | 20250212 | |

## Exception Case2 (Both 10 PM and 10:20 PM job failed in RATAN, service ready at 1 AM next day)

| Cashflow ID | Sample Cashflow Value Date | Sample Cashflow Released/Settled/Failed/SWIFT_SUPP | Expected in File | Expected AsOfDate | Comment |
| --- | --- | --- | --- | --- | --- |
| Both 10 PM and 10:20 PM job failed in RATAN. At 20250212 1 AM, service is up and generate 20250211 file |
| C01 | 20250211 | Before 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250211_01.csv | 20250211 | |
| C02 | 20250211 | After 20250211 10 PM | Will no be included in 20250211 file, as cashflow was released after 10 PM | |
| At 20250212 10 PM, file generated to Apire successfully |
| C02 | 20250211 | After 20250211 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250212_01.csv | 20250212 | |
| C03 | 20250212 | Before 20250212 10 PM | RATAN_PAYMENT_TRANSACTION_TH_20250212_01.csv | 20250212 | |

# Aspire file field mapping

**Data truncation is required according to agreed length below**

# Aspire File Format

File Name: RATAN_PAYMENT_TRANSACTION_TH_YYYYMMDD_01.csv

RATAN should send same file format with Murex file.

📎 [MXG_PAYMENTTRANSACTION_20231017.csv.gz](attachments/MXG_PAYMENTTRANSACTION_20231017.csv.gz)

# Static Data

| # | Murex Entities | FMID | 2025 Bucket | Country Code | PSGL Business Unit | TPEntityName |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | BANGKOK | 6 | Tranche 1 | TH | 265 | BAN |
| 2 | TAIPEI | 10038345 | Tranche 1 | TW | 647 | TAI |
| 3 | OBU TAIPEI | 300011345 | Tranche 1 | TW | 648 | OBU |
| 4 | SCS HK | 300075472 | Tranche 1 | HK | 437 | SCS |
| 5 | ~~HONGKONG ~~ | ~~2~~ | ~~Tranche 1~~ | ~~HK~~ | ~~238~~ | ~~HON~~ |
| 6 | MAURITIUS | | Tranche 2 | | | |
| 7 | DUBAI | | Tranche 2 | | | |
| 8 | JAKARTA | | Tranche 2 | | | |
| 9 | MANILA | | Tranche 2 | | | |
| 10 | TOKYO | | Tranche 2 | | | |
| 11 | JOBURG | | Tranche 2 | | | |
| 12 | PHILIP FCU | | Tranche 2 | | | |
| 13 | DIFC | | Tranche 2 | | | |
| 15 | NEWYORK | 7 | Tranche 1 | US | 104 | NEW |
| 16 | JERSEY_BR | 400910415 | Tranche 3 | JE | 123 | |

| M_ENTITY | FMID | Bridge Account |
| --- | --- | --- |
| ~~HONGKONG ~~ | ~~2~~ | ~~238725180028890191098~~ |
| SCS HK | 300075472 | ~~437720380028890191098~~ , 437705380028890191098 |
| BANGKOK | 6 | 265725180028890191098 |
| TAIPEI | 10038345 | 647725180028890191098 |
| OBU TAIPEI | 300011345 | 648725180028890191098 |
| Jersey | 400910415 | 123613180028890791098 |

| Country | Entity Name | Entity Fmid | Branch code |
| --- | --- | --- | --- |
| US | NEWYORK | 7 | 10 |
| TH | BANGKOK | 6 | 22 |
| ~~HK~~ | ~~HONGKONG ~~ | ~~2~~ | ~~60~~ |
| SCS HK | SCS HK | 300075472 | 60 |
| TW | TAIPEI | 10038345 | 66 |
| OBU TW | OBU TAIPEI | 300011345 | 67 |
| JE | JERSEY_BR | 400910415 | 05 |

Nostro Account in attachment

📎 [Nostro template- 18feb.xlsx](attachments/Nostro template- 18feb.xlsx)

# Tech Design

[Settlement Accounting for Aspire Tech design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Settlement+Accounting+for+Aspire+Tech+design)

# Meeting Minutes 2024-11-28

**<u>Attendance</u>**

Lina, Anindya, Balaji, Karthick, Dendi, Ahamed, Evelyn, Wayne, Geoffrey

**<u>Meeting Minutes</u>**

1. RATAN – Aspire accounting file name format: RATAN_PAYMENT_TRANSACTION_TH_YYYYMMDD_01.csv
2. RATAN should send same file format with Murex file.
3. Filtering for file generation in RATAN:
4. File sent at: 10 PM local time from Monday to Friday, if any cashflow post 10 PM local time, it will be included in Today+1 Business day's file (25th Dec and 1st Jan will be an exception)
5. Within file, detailed format can be found in attachment:

Aspire – PSGL format would be "DV" + Branch code +cashflow ID|Sequence in same cashflow|trade id(for gross)/NET(SPACE)taxonomy(SPACE)counterparty FMCODE(SPACE)cashflow Status, order is settled, Anindya to check any concern from Aspire (action on [@Dasgupta, Anindya](mailto:Anindya.Dasgupta@sc.com))

1. FileIT will be used for file transfer, ACK/NACK is not required, Balaji help to follow up the setup (action on [@Sittrarasu, Balaji](mailto:Balaji.Sittrarasu@sc.com))

# Infra info

<u>**FileIT info**</u>

Already exists in prod, FileIT will add new mapping on CR day.

FileIT can be configured whether to remove source file after file delivered or not.

##### DEV

source path: /share/**imft070**/ratanone/aspire

target path:

- /share/**imft115**/ASPIRE/RATAN/HK/data/incoming/<file_name>
- /share/**imft115**/ASPIRE/RATAN/TW/data/incoming/<file_name>
- /share/**imft115**/ASPIRE/RATAN/TH/data/incoming/<file_name>
- /share/**imft115**/ASPIRE/RATAN/JE/data/incoming/<file_name>

##### PROD

source path: /share/**imft054**/ratanone/aspire

target path:

- /share/**imft157**/ASPIRE/RATAN/HK/data/incoming/<file_name>
- /share/**imft157**/ASPIRE/RATAN/TW/data/incoming/<file_name>
- /share/**imft157**/ASPIRE/RATAN/TH/data/incoming/<file_name>
- /share/**imft157**/ASPIRE/RATAN/JE/data/incoming/<file_name>

<u>prod golive cmd to be executed: </u>

mkdir -p -m 775 /share/imft054/ratanone/aspire/archive/
chgrp imft /share/imft054/ratanone/aspire/
chgrp imft /share/imft054/ratanone/aspire/archive/

<u>**Solace connection info**</u>

Already exists in prod, Ratan will onbard new MB mapping.

**topic name:** v1/51358-ratan-one/fileit/imft-json-1.0/-/req    (MB topic name: Cash_Settlement_Aspire_FileIT_Process_Out)

**ack queue name:** q-51358-ratan-one-imft-ack-all (FileIT will publish ack message to this queue)  (MB topic name: Cash_Settlement_Aspire_FileIT_Ack)

DEV:

- <u>**HOST:** [smfs://hk-np3.fs-solace.dev.net:55443,smfs://hk-np4.fs-solace.dev.net:55443](smfs://hk-np3.fs-solace.dev.net:55443,smfs:)</u>
- **VPN**: vpn-fs-imft-t1
- **USERNAME**: 51358-ratan

PROD:

- <u>**HOST:** </u>[smfs://hk-prd3.fs-solace.sc.net:55443,smfs://hk-prd4.fs-solace.sc.net:55443](smfs://hk-prd3.fs-solace.sc.net:55443,smfs:)
- **VPN**: vpn-fs-imft-p1
- **USERNAME**: 51358-ratan

Request solace message to FileIT:

```js
"ImftFileRequest": {
      "header": {
        "messageVersion": "v1",
        "flowIdentifier": "RATAN_CASHSTLMT_GL",
        "uuid": "74e081a1-e599-45a7-b6a2-ab7540ff0b37",  -- <generate new for each request>
        "country": "GL",
        "sourceName": "51358-RATAN"
      },
      "payload": {
        "source": {
          "srcFilePath": "/share/imft054/ratanone/xxx.gz"
        },
        "target": {
          "dstName": "51282-ASPIRE",
          "dstFilePath": "/some-nas/consumer-use/ratanone/xxx.gz"
        }
      }
    }
```

Ack from FileIT:

```js
{
   "IMFTFileNotification" : {
        "Header" : {
            "Version" : " ",            //1.0
            "Identifier" : "",          //EBBS_MT940_HK
            "UUID" : " ",               //90e6bb42-66bf-11ea-bc55-0242ac130003
            "SrcJMSID" : " ",           //1234569999999
            "Source": "",               //43454-EBBS
            "Target": "",               //50821-IMFT
            "Country": " "              //HK
            "Timestamp":" "             //yyyy-MM-dd HH:mm:ss.S Z ("2020-05-04 20:46:19.511 +0800")
        },
        "Payload" : {
            "Component" : "",           // IS/CFT/GW/TDE
            "SubComponent" : " ",       // EBBS_IMFT_MT940_HK for CFT or EBBS.EBS.HK.IMFT.IMFT.HK.MT940 at TDE
            "TrackingID": " ",          //tracking id specific component
            "SrcFilePath" : " ",        // /imft/shared/ebbs/sample.zip/
            "Status" : {
                "Code":"",              //2000
                "Reason" : "",          //CFT_SUCCESSFUL
                "Causes" : {
                   "Details":["",""]   // File Transfer completed to destination
                }                     
            }
        }
    }
}
```

more details for request and response taxonomy at: [Solace Message Structure And Taxonomy](https://confluence.global.standardchartered.com/display/IMFT/Solace+Message+Structure+And+Taxonomy)

## Return Codes

| Notification Type | code | Reason | Description |
| --- | --- | --- | --- |
| ftaccepted | 1000 | ACCEPTED | File Transfer Request Accepted for flow |
| failed | 1001 | NOT_AUTHORIZED | Not Authorized to trigger flow |
| 1002 | BAD_REQUEST | Invalid Request |
| 1003 | INVALID_ROUTING_RULE | Missing Routing Rule for flow |
| 1004 | CFT_AUTHORIZATION_FAILURE | Invalid CFT API Credential |
| 1005 | CFT_UNAVAILABLE | Source CFT is down |
| 1006 | COPILOT_UNAVAILABLE | Source Copilot is down |
| ftinitiated | 1100 | INITIATED | File Transfer Request Accepted for flow |
| ftsuccessful | 2000 | CFT_SUCCESSFUL | File Transfer Successful for flow |
| failed | 2001 | CFT_SOURCE_PATH_INVALID | Source path does not exit |
| 2002 | CFT_SOURCE_PRE_PROCESSING_FAILED | Source Pre-processing Script failed |
| 2003 | CFT_SOURCE_POST_PROCESSING_FAILED | Source Post-processing script failed |
| 2004 | CFT_PARTNER_INVALID | Target CFT name not correctly mentioned |
| 2005 | CFT_TARGET_PATH_INVALID | Destination path not correctly mentioned |
| 2006 | CFT_TARGET_POST_PROCESSING_FAILED | Target Post processing script failed |
| 2007 | CFT_SOURCE_FILE_INSUFFICIENT_PERMISSION | Source file do not have permission |
| 2008 | CFT_TARGET_PATH_INSUFFICIENT_PERMISSION | Target path do not have permission |
| 2010 | CFT_SOURCE_IDF_INVALID | Idf not correctly mentioned |
| 2020 | CFT_TRANSFER_FAILED | Transfer failed |
| notify | 5000 | CFT_NOTIFICATION | Receiver notification successful from Receiver processing script |
| 5001 | CFT_NOTIFICATION | Receiver notification failure from Error processing script |

# Exception Scenario for PSS support

| | Scenario | Auto Compensation | PSS Action |
| --- | --- | --- | --- |
| 1 | File didn't generate at 10/10:30 PM local time | Job will auto run and try to regenerate file in following batch | Monitoring |
| 2 | File didn't generate until 11 PM local time | Job will auto run and try to regenerate file in following batch | Inform Dev for investigation/manually rerun failed job |
| 3 | File didn't generate until 12 PM local time | Job will auto run and try to regenerate file in following batch | Inform Aspire PSS to hold PSGL processing and provide ETA/manually rerun failed job |
| 4 | File didn't generate until 3 AM local time | NA | NA, as it would break Aspire-PSGL OLA timing, missing generated data will be included in next day's file File name and AsOfDate should be next day |
| 5 | | | |