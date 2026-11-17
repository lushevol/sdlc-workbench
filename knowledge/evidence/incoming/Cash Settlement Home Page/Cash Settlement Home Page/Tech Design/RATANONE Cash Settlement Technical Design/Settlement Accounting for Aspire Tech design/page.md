## Background

[Cash Settlement - Aspire Accounting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+Aspire+Accounting)

## High level design

[RATANONE Cash Settlement Technical Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2560471970)

## Principle

1. Event driven EBBS feed generation
2. Value date is the cutoff for feed publishing 1. Hold if VD not arrived 2. Publish as batch file if VD 22:05(local time) already arrived
3. Withdrawal will be generated as reversal direction of the New instead of totally new generated feed

## Open point

DB desgin: 2 columns for EBBS and Aspire feed or in same column

## Status Machine

## Processing Design

## Control-M job

1.The job will trigger every 30min from 22:05(local time) till 02:05.  And the job will fetch tasks which payment date <= current date and create_time < current date 10:00 PM . It will only generate 1 file for each work day job.

2. generate empty file job will trigger at 3:30 am (local time).

# Business Scenario

| | | | task table | job execution table | |
| --- | --- | --- | --- | --- | --- |
| | cashflow info | Current Time | external_system_key | action | task_status | as_of_date | filename | execution id | country | as_of_date | file_sent | reason |
| 1 | cf1 - 20250220 | 20250220 09:00 (local) 20250220 01:00 (GMT) | cf1.0.3 | Fail/SwiftSuppress | HOLD/MISSING_INFO | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 11:00 (local) 20250220 03:00 (GMT) | cf1.0.3 | Reinstate/UnSwiftSuppress | DISABLED | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 22:00 (local) 20250220 14:00 (GMT) | | | | | RATAN_PAYMENT_TRANSACTION_HK_20250220_01.csv | 2 | HK | 20250220 | SENT | |
| | | 20250220 22:02 (local) 20250220 14:02 (GMT) | | | | | | 2 | HK | 20250220 | ACKED | SUCCESS |
| | | 20250220 22:30 (local) 20250220 14:30 (GMT) | | | | | RATAN_PAYMENT_TRANSACTION_HK_20250220_01.csv existed , so this job will skip | 2 | HK | 20250220 | ACKED | SUCCESS |
| 2 | cf2 - 20250220 | 20250220 09:00 (local) 20250220 01:00 (GMT) | cf2.0.3 | Release/Fail/SwiftSuppress | HOLD | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 22:00 (local) 20250220 14:00 (GMT) | cf2.0.3 | | SUCCESS | | RATAN_PAYMENT_TRANSACTION_HK_20250220_01.csv | 2 | HK | 20250220 | SENT | |
| | | 20250220 22:02 (local) 20250220 14:02 (GMT) | | | | | | 2 | HK | 20250220 | ACKED/NACK | SUCCESS/Invalid Request |
| 3 | cf3 - 20250220 | 20250220 22:05 (local) 20250220 14:05(GMT) | cf3.0.3 | Release/Fail/SwiftSuppress | HOLD | | | 2 | HK | 20250220 | ACKED | SUCCESS |
| | | 20250221 22:00 (local) 20250221 14:00 (GMT) | cf3.0.3 | | SUCCESS | | RATAN_PAYMENT_TRANSACTION_HK_20250221_01.csv | 3 | HK | 20250221 | SENT | |
| | | 20250221 22:02 (local) 20250221 14:02 (GMT) | | | | | | 3 | HK | 20250221 | ACKED/NACK | SUCCESS/Invalid Request |
| 4 | cf4 - 20250220 | 20250220 09:00 (local) 20250220 01:00 (GMT) | cf4.0.3 | Release/Fail/SwiftSuppress | MISS_INFO | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 11:00 (local) 20250220 03:00 (GMT) | cf4.0.3 | NostroStamped | DISABLED | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 11:01 (local) 20250220 03:01 (GMT) | cf4.0.4 | NostroStamped | HOLD | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 22:00 (local) 20250220 14:00 (GMT) | cf4.0.4 | | SUCCESS | | RATAN_PAYMENT_TRANSACTION_HK_20250220_01.csv | 2 | HK | 20250220 | SENT | |
| | | 20250220 22:02 (local) 20250220 14:02 (GMT) | | | | | | 2 | HK | 20250220 | ACKED/NACK | SUCCESS/Invalid Request |
| 5 | cf5 - 20250220 | 20250220 09:00 (local) 20250220 01:00 (GMT) | cf5.0.3 | Release/Fail/SwiftSuppress | HOLD | | | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 22:00 (local) 20250220 14:00 (GMT) | | | HOLD | | RATAN_PAYMENT_TRANSACTION_HK_20250220_01.csv generate fail | 1 | HK | 20250219 | ACKED | SUCCESS |
| | | 20250220 22:30(local) 20250220 14:30(GMT) | | | SUCCESS | | RATAN_PAYMENT_TRANSACTION_HK_20250220_01.csv regenerate | 2 | HK | 20250220 | SENT | |
| | | 20250220 22:32(local) 20250220 14:32(GMT) | | | | | | 2 | HK | 20250220 | ACKED | SUCCESS |

job Scenario demo: HK

1. current GMT time (2022-02-2014:05:00 GMT)→ 2025-02-2022:05:00 (Local)
2. find latest asOfDate by HK from accounting_aspire_execution table 1. exist 2025-02-19record
3. then get the task list and generate 2 transaction records for each task 1. country = HK and systemDate = 2025-02-20
4. create HK_20250220_01.csv and write above transaction records in this file
5. call lifecycle for each cashflow status update
6. call FileIT to copy the file 1. insert execution table : HK; 2025-02-20; SENT; and update task table filename = HK_20250220_01.csv in above task id
7. receive response from fileIT 1. update execution table response_code = 2000 , response_desc = SUCCESS which record is country = HK and asOfDate = 2025-02-20 and file_sent = SENT
8. job complete