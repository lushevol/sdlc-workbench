# 1.Main Scenario

| | Test Case | Test Steps | Expected Result | Tested Data | Tested By | Result Pass/Fail | Test Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Split over gross cashflow, child cashflow partial released | manual split 1.released one child | generate accounting info | parent: M00123889310 S00000050000 | @Li1, Johnny | Pass | ![image-2025-11-11_11-44-28.png](attachments/image-2025-11-11_11-44-28.png) ![image-2025-11-11_11-44-47.png](attachments/image-2025-11-11_11-44-47.png) ![image-2025-11-11_11-45-38.png](attachments/image-2025-11-11_11-45-38.png) |
| 2 | 2.swift_suppress one child | generate accounting info | parent: M00123889310 S00000049998 | @Li1, Johnny | Pass | ![image-2025-11-11_11-46-44.png](attachments/image-2025-11-11_11-46-44.png) ![image-2025-11-11_11-46-54.png](attachments/image-2025-11-11_11-46-54.png) ![image-2025-11-11_11-47-10.png](attachments/image-2025-11-11_11-47-10.png) |
| 3 | 3.cashflow_suppress one child | **do not **generate accounting info | parent: M00123889310 S00000049999 | @Li1, Johnny | Pass | ![image-2025-11-11_11-47-59.png](attachments/image-2025-11-11_11-47-59.png) ![image-2025-11-11_11-48-8.png](attachments/image-2025-11-11_11-48-8.png) |
| 4 | 4.fail one child | generate accounting info | parent: M00123889310 S00000050001 | @Li1, Johnny | Pass | ![image-2025-11-11_11-48-34.png](attachments/image-2025-11-11_11-48-34.png) ![image-2025-11-11_11-48-43.png](attachments/image-2025-11-11_11-48-43.png) ![image-2025-11-11_11-48-59.png](attachments/image-2025-11-11_11-48-59.png) |
| 5 | Split over gross cashflow, child cashflow all released | one parent cashflow, auto split | all child released and generate accounting info | parent: M01760959502 S00000050019 S00000050020 | @Li1, Johnny | Pass | ![image-2025-11-11_12-1-3.png](attachments/image-2025-11-11_12-1-3.png) S00000050019 ![image-2025-11-11_12-1-32.png](attachments/image-2025-11-11_12-1-32.png) ![image-2025-11-11_12-2-11.png](attachments/image-2025-11-11_12-2-11.png) S00000050020 ![image-2025-11-11_12-1-51.png](attachments/image-2025-11-11_12-1-51.png) ![image-2025-11-11_12-2-22.png](attachments/image-2025-11-11_12-2-22.png) |
| 6 | auto distribution over net resultant cashflow, child cashflow all released | net+auto spit case | all child released | M01760959503,M01760959504,N00000050021 S00000050022,S00000050023 | @Li1, Johnny | Pass | ![image-2025-11-11_12-5-10.png](attachments/image-2025-11-11_12-5-10.png) S00000050022 ![image-2025-11-11_12-5-40.png](attachments/image-2025-11-11_12-5-40.png) ![image-2025-11-11_12-5-52.png](attachments/image-2025-11-11_12-5-52.png) S00000050023 ![image-2025-11-11_12-5-25.png](attachments/image-2025-11-11_12-5-25.png) ![image-2025-11-11_12-6-6.png](attachments/image-2025-11-11_12-6-6.png) |
| 7 | | | | | | | |
| 8 | | SG | | | | | |
| 9 | | UK | | | | | |
| 10 | | | | | | | |
| 11 | | | | | | | |

# 2.With Request Info Attachment

📎 [ratan_accounting_request_task_202511111213.csv](attachments/ratan_accounting_request_task_202511111213.csv)

using sql:

select cashflow_id, business_version, minor_version, payment_date,trade_id ,country ,booking_entity_fmid,booking_entity_fmcode ,counterparty_fmid ,counterparty_fmcode,external_system_key,currency, request_info 
from ratan_cash_accounting_service.ratan_accounting_request_task
where cashflow_id in ('S00000050000','S00000049998','S00000049999','S00000050001','S00000050019','S00000050020','S00000050022','S00000050023')