# 1.Main Scenario

| 1 | Country | Test Case | Test Steps | Expected Result | Tested Data | tradeId | Tested By | Result Pass/Fail | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HK | Split over gross cashflow, child cashflow partial released | manual split 1.release one child | generate accounting info | parent: M00122424780 child: **S00000051615** | 68025226 | @Li1, Johnny | Pass | |
| 2 | 2.fail one child | generate accounting info | child: **S00000051616** | | | |
| 3 | 3.swift_suppress one child | generate accounting info | child: **S00000051617** | | | |
| 4 | | | | | | | | |
| 5 | Split over gross cashflow, child cashflow all released | one parent cashflow, auto split | all child released and generate accounting info | parent: M00122424782 child: **S00000051625, S00000051626** | 5566578732 | @Li1, Johnny | Pass | |
| 6 | | | | | | | | |
| 7 | auto distribution over net resultant cashflow, child cashflow all released | net+auto spit case | all child released | M00122424785,M00122424786,N00000051630 **S00000051631,S00000051632** | 5566671447 | @Li1, Johnny | Pass | |
| 8 | | | | | | | | |
| 9 | **Withdrawal **after gross cashflow splitted | manual split + coming withdrawl 1.manul release continuely | generate accounting info | parent: M00122424787 child: **S00000051633** | 6256305220 | @Li1, Johnny | Pass | |
| 10 | 2.auto cancel failed child | generate accounting info | **S00000051634** | | | |
| 11 | 3.auto cancel swift_suppressed child | generate accounting info | **S00000051635** | | | |
| 12 | | | | | | | | |
| 13 | **Withdrawal **after netting resultant cashflow auto distributed | 1.net+auto split 2.coming withdrawl and swift_suppress | | parent: M00122424788,M00122424789,N00000051636 child: **S00000051637,S00000051638** coming withdraw: **M00122424788** | 5566653478 | @Li1, Johnny | Pass | |
| 14 | | | | | | | | | |
| 15 | | | | | | | | | |
| 16 | | | | | | | | | |
| 17 | TW | Split over gross cashflow, child cashflow partial released | manual split 1.release one child | generate accounting info | parent: M00127104626 child: **S00000051639** | 6257385409 | @Li1, Johnny | Pass | |
| 18 | 2.fail one child | generate accounting info | child: **S00000051640** | | | |
| 19 | 3.swift_suppress one child | generate accounting info | child: **S00000051641** | | | |
| 20 | | | | | | | | |
| 21 | Split over gross cashflow, child cashflow all released | one parent cashflow, auto split | all child released and generate accounting info | parent: M00127104628 child: **S00000051642,S00000051643** | 6254883622 | @Li1, Johnny | Pass | |
| 22 | | | | | | | | |
| 23 | auto distribution over net resultant cashflow, child cashflow all released | net+auto spit case | all child released | M00127104629,M00127104630,N00000051644 **S00000051645,S00000051646** | 6254418480 | @Li1, Johnny | Pass | |
| 24 | | | | | | | | |
| 25 | **Withdrawal **after gross cashflow splitted | manual split + coming withdrawl 1.manul release continuely | | parent: M00127104631 child: **S00000051647** | 6254976527 | @Li1, Johnny | Pass | |
| 26 | 2.auto cancel failed child | | child: **S00000051648** | | | |
| 27 | 3.auto cancel swift_suppressed child | | child: **S00000051649** | | | |
| 28 | | | | | | | | |
| 29 | **Withdrawal **after netting resultant cashflow auto distributed | [1.net](http://1.net)+auto split 2.coming withdrawl and swift_suppress | | parent: M00127104632,M00127104633,N00000051650 child: **S00000051651,S00000051652** coming withdraw: **M00127104632** | 6254922935 | @Li1, Johnny | Pass | |
| 30 | | | | | | | | | |
| 31 | | | | | | | | | |
| 32 | | | | | | | | | |
| 33 | TH | Split over gross cashflow, child cashflow partial released | manual split 1.release one child | generate accounting info | parent: M00127068878 child: **S00000051653** | 6256746462 | @Li1, Johnny | Pass | |
| 34 | 2.fail one child | generate accounting info | child: **S00000051654** | | | |
| 35 | 3.swift_suppress one child | generate accounting info | child: **S00000051655** | | | |
| 36 | | | | | | | | |
| 37 | Split over gross cashflow, child cashflow all released | one parent cashflow, auto split | all child released and generate accounting info | parent: M00127068879 child: **S00000051656,S00000051657** | 6253104737 | @Li1, Johnny | Pass | |
| 38 | | | | | | | | |
| 39 | auto distribution over net resultant cashflow, child cashflow all released | net+auto spit case | all child released | M00127068882,M00127068883,N00000051662 **S00000051663,S00000051664** | 6253092784 | @Li1, Johnny | Pass | |
| 40 | | | | | | | | |
| 41 | **Withdrawal **after gross cashflow splitted | manual split + coming withdrawl 1.manul release continuely | | parent: M00127068884 child: **S00000051665** | 6256770730 | @Li1, Johnny | Pass | |
| 42 | 2.auto cancel failed child | | child: **S00000051666** | | | |
| 43 | 3.auto cancel swift_suppressed child | | child: **S00000051667** | | | |
| 44 | | | | | | | | |
| 45 | **Withdrawal **after netting resultant cashflow auto distributed | [1.net](http://1.net)+auto split 2.coming withdrawl and swift_suppress | | parent: M00127068885,M00127068886,N00000051668 child: **S00000051669,S00000051670** coming withdraw: **M00127068885** | 6254922770 | @Li1, Johnny | Pass | |

cashflowIds:
HK:
S00000051615,S00000051616,S00000051617,S00000051625, S00000051626,S00000051631,S00000051632,S00000051633,S00000051634,S00000051635,S00000051637,S00000051638,M00122424788
TW:
S00000051639,S00000051640,S00000051641,S00000051642,S00000051643,S00000051645,S00000051646,S00000051647,S00000051648,S00000051649,S00000051651,S00000051652,M00127104632
TH:
S00000051653,S00000051654,S00000051655,S00000051656,S00000051657,S00000051663,S00000051664,S00000051665,S00000051666,S00000051667,S00000051669,S00000051670,M00127068885

# 2.With Request Info Attachment

using sql:

select cashflow_id, business_version, minor_version, payment_date,trade_id ,country ,booking_entity_fmid,booking_entity_fmcode ,counterparty_fmid ,counterparty_fmcode,external_system_key,currency, request_info 
from ratan_cash_accounting_service.ratan_accounting_request_task
where cashflow_id in ('S00000050000','S00000049998','S00000049999','S00000050001','S00000050019','S00000050020','S00000050022','S00000050023')