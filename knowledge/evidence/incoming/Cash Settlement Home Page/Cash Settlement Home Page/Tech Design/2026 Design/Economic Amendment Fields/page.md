story1: [Story 12659039 [FMRP 8.0] G10 & FXO New Eco Fields](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12659039/?view=edit)

story2 （from BAU）: [RFI Nostro stamping based on Portfolio - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFI+Nostro+stamping+based+on+Portfolio)

| Trade Id | Cashflow Id | Business Event | Amount(economic field change） | Swap Agent Id(key field change) | CF blotter Status | Expected Booking System Event | Case Description | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | C01 | Withdrawal | 100 USD | | New Waiting, no manual touch | NonEcoAmend_Replace | C01, C04 1. non eco amend 2. not manual touched and not released | Check key fields first or manualtouch/release first |
| | C02 | Withdrawal | 200 CNY | | Released | NonEcoAmend | C02, C05 1. non eco amend 2. post released 3. key fields not changed | |
| | C03 | Withdrawal | 300 JPY | | Waiting | Amendment | C03, C06 1. eco amend | |
| | C04 | New | 100 USD | | NA | NonEcoAmend_Replace | C01, C04 1. non eco amend 2. not manual touched and not released | |
| | C05 | New | 200 CNY | | NA | NonEcoAmend | C02, C05 1. non eco amend 2. manual touched 3. key fields not changed | |
| | C06 | New | 400 JPY | | NA | Amendment | C03, C06 1. eco amend | |
| | C07 | Withdrawal | 500 EUR | MTM/Coupon | New Waiting, user manual touch | NonEcoAmend_Replace | C07, C08 1. non eco amend 2. manual touched 3. key field changed | manual touched check not required if 3 matched. |
| | C08 | New | 500 EUR | Coupon | | NonEcoAmend_Replace | C07, C08 1. non eco amend 2. manual touched 3. key field changed | |

Edge case

| Trade Event | | | Group | | | | Group Message | | | | Cashflow Blotter | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | Trade Id | Lien Monitoring | major version | count | batch_id | | cashflow id | business event | ccy+direction+vd+fmid+cptyid+amt+method | | | | |
| Booking | T01 | Yes | 1 | 1 | b01 | | C01 | N | ABC | | | | |
| | | | | | | | | | | | | | |
| Fixing | T01 | Yes | 1 | 1 | b02 | | C02 | N | ABC | | Waiting + Pending Exception + Submitted | | |
| | | | | | | | | | | | | | |
| Refixing | T01 | Yes | 1 | 2 | b03 | | C02 | W | ABC | | | Pre development: C02 and C03 will be tagged as NonEcoAmend |
| | | | | | | | C03 | N | ABC | | |
| | | | | | | | | | | | | | |
| | | | | | | | | | | | | | |
| Trade Event | | | Group | | | | Group Message | | | | Cashflow Blotter | | |
| | | Lien Monitoring | major version | count | batch_id | | cashflow id | business event | ccy+direction+vd+fmid+cptyid+amt+method | | | | |
| Booking | T01 | Yes | 1 | 1 | b01 | | C01 | N | ABC | | | | |
| | | | | | | | | | | | | | |
| Fixing | T01 | Yes | 1 | 1 | b02 | | C02 | N | ABC | | Waiting + Pending Exception + Submitted | | |
| | | | | | | | | | | | | | |
| Refixing | T01 | Yes | 1 | 2 | b03 | | C02 | W | ABC | | | @Junli GaoEcoAmend Note: (1)majorversion=1, should check cashflow only, and will be classfied as [Amendment], since eco-field changed while refixing (2)if majorVersion>1 && preGroup does not exsit ---[Amendment] | |
| | | | | | | | C03 | N | ABC | | | @Junli Gao same as above | |

code level

key point: set bookingSystemEvent While moving groupMessages from sourceMsgs to targetMsgs

**FYI: from BAU, add  dedicatedChange, if dedicatedChange will drive into nopair first**