#

# Korea migration End-to-End Flow

#

# Upload SCBML file in the GUI

As Korea entity have not on board in TDS3, trade status can't be synchronize through TDS3. In order to affirm cashflows automatically and record trades 'COMP' status, before the automatic transmission of COMP status is launched, RATAN provides an interface function to help users automatically upload the 'COMP' status of transactions.

| Number | Steps | Screenshots |
| --- | --- | --- |
| 1 | Prepare CSV file before upload 'COMP' status trade information. File size limitation: 20M Number limitation: 2000 | Sample CSV: SCBML in CSV file: |
| 2 | Log in with an authorized account | All authorized accounts: 1372116-Yang, Ji Hoon 1371935-Cho, Hye Won 1372224-Choo, Ji Won |
| 3 | Click on the button 'KR COMP' | ![image-2026-7-26_23-22-4.png](attachments/image-2026-7-26_23-22-4.png) |
| 4 | Select the prepared CSV file | ![image-2026-7-26_23-24-18.png](attachments/image-2026-7-26_23-24-18.png) |
| 5 | Click on 'Open'. If the upload is successful, a prompt message will pop up indicating successful upload. | ![image-2026-7-26_23-24-10.png](attachments/image-2026-7-26_23-24-10.png) |
| 6 | If file format or any data error in CSV file, a prompt message will pop up with the specific reasons for the failure. Users can make corresponding modifications according to the prompts. | ![image-2026-7-3_17-15-48.png](attachments/image-2026-7-3_17-15-48.png) |

# TIS Payment Processing

As some payment need to manually key-in everyday via OLTP(UI), user hope that those payment information could get automatically from API.

API Details:

- Payment: [https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/v1/tis/query/payment/*{payment*](https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/v1/tis/query/payment/%7bpayment)* date}*
- Receipt: [https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/v1/tis/query/receipt/*{payment*](https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/v1/tis/query/receipt/%7bpayment)* date}*

TIS Scope:

1. 'Released' or 'Settled' cashflow
2. STTL_MEANS = NOX
3. No reversal event
4. Entity FMID: 10036645

| | Pay/Receive | Conditions | Screenshots |
| --- | --- | --- | --- |
| 5338 | Pay | 57BIC: SCBLKR Settlement Account: KRO UISUS Beneficiary Customer Account: mandatory, start with 'BR%' | ![image-2026-7-28_0-40-19-1.png](attachments/image-2026-7-28_0-40-19-1.png) |
| 5339 | Pay | 57BIC: SCBLKR Settlement Account: FCY UISUS Beneficiary Customer Account: mandatory, start with 'BR%' | ![image-2026-7-28_0-42-34-1.png](attachments/image-2026-7-28_0-42-34-1.png) |
| 5318 | Pay | 57BIC: SCBLKR Settlement Account: KRO UISUS Beneficiary Customer Account: mandatory, not start with 'BR%' | ![image-2026-7-28_6-51-44-1.png](attachments/image-2026-7-28_6-51-44-1.png) |
| 5319 | Pay | 57BIC: SCBLKR Settlement Account: FCY UISUS Beneficiary Customer Account: mandatory, not start with 'BR%' | ![image-2026-7-28_6-52-3-1.png](attachments/image-2026-7-28_6-52-3-1.png) |
| 5323 | Pay | 57BIC: No-SCBLKR Settlement Account: KRO UISUS Beneficiary Customer Account: mandatory, not start with 'BR%' | ![image-2026-7-28_6-54-34-1.png](attachments/image-2026-7-28_6-54-34-1.png) |
| 5324 | Pay | 57BIC: No-SCBLKR Settlement Account: KRO UIBOK Beneficiary Customer Account: NULL or 'dummy' | ![image-2026-7-28_6-55-4-1.png](attachments/image-2026-7-28_6-55-4-1.png) |
| 5325 | Pay | 57BIC: No-SCBLKR Settlement Account: KRO UIBOK Beneficiary Customer Account: mandatory, not start with 'BR%' | ![image-2026-7-28_6-55-17-1.png](attachments/image-2026-7-28_6-55-17-1.png) |
| 0201 | Receive | Settlement Account: KRO UIDD | ![image-2026-7-28_6-55-52-1.png](attachments/image-2026-7-28_6-55-52-1.png) |
| 3013 | Receive | Settlement Account: FCY UIDD | ![image-2026-7-28_6-56-2-1.png](attachments/image-2026-7-28_6-56-2-1.png) |

## TIS exception code

If no exception, status code will be 200. If exception happens when call API, RATAN will sent back with error code as below. Downstream should adjust parameter as error code.

| Success | 200 | Indicates that the request succeeded and that the requested information is in the response. This is the most common status code to receive. |
| --- | --- | --- |
| NotFound | 404 | Indicates that the requested resource does not exist on the server. |
| BadRequest | 400 | Indicates that the parameter format doesn't meet the requirement. |
| Unauthorized | 401 | Indicates that the token is invalid |
| InternalServerError | 500 | Indicates that an error has occurred in the service. |

# OLTP Accounting

Cashflow status scope: Failed/Swift_suppressed/Released/Settled

Except below condition, accounting will need send to OLTP.

Sett Means = 'NOX' and Sett Account in ('%UIDD%', '%UISUS%')

#### Accounting Monitoring

Users could monitor accounting error in 'Cashflow Dashboard'. Click on 'Accounting Error' button. Filter by cashflow accounting status, can see yesterday, today, tomorrow's error accounting, which includes 'SENT', 'REJECTED', 'MISSING_INFO' status.

![image-2026-7-28_0-44-50.png](attachments/image-2026-7-28_0-44-50.png)

Filter by cashflow accounting status, can see yesterday, today, tomorrow's error accounting, which includes 'SENT', 'REJECTED', 'MISSING_INFO' status. Ops need to process in OLTP system.

![image-2026-7-28_0-46-58.png](attachments/image-2026-7-28_0-46-58.png)

![image-2026-7-28_7-14-2.png](attachments/image-2026-7-28_7-14-2.png)

Double click on cashflow, select 'Accounting Detail' tag, check accounting info, status and reason as below.

![image-2026-7-28_0-48-17.png](attachments/image-2026-7-28_0-48-17.png)

# SWIFT exception check

RATAN will generate swifts only for non KRO. All KRO payments will be manually handled via TIS.

Users could monitor swift error in cashflow dashboard. Click on 'Swift Error' button.

![image-2026-7-28_7-17-0.png](attachments/image-2026-7-28_7-17-0.png)

Filter by cashflow swift status, can see yesterday, today, tomorrow's swift error , especially 'FinalCancelled', that is NACK status from ENISIS. Then user could process them in exception blotter or replay in ENISIS.

![image-2026-7-28_7-18-8.png](attachments/image-2026-7-28_7-18-8.png)

# Reference Link:

[Settlement - KR Murex 2.11 DOI Document - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Settlement+-+KR+Murex+2.11+DOI+Document)