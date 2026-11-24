This may only  FE impact,but need double confirm with UI developer

Double click a cashflow, refer to "Cashflow Details-Counterparty", there is   "i" icon

![image-2025-7-4_15-45-53.png](attachments/image-2025-7-4_15-45-53.png)

![image-2025-7-4_15-44-57.png](attachments/image-2025-7-4_15-44-57.png)

2.

As-Is(Current) solution : Call SCI to get the BIC type value  then set the value to "SWIFT BIC"

To-Be solution: Call SCI to get the below item,then set the  value of "addrLine" to "SWIFT BIC" when "mediumUsage" ='MAIN' if the "SWIFT BIC " !=SCBLGB2LXXX"

![image-2025-7-2_15-5-6.png](attachments/image-2025-7-2_15-5-6.png)