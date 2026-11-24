1, book a ForeignExchange:Swap trade, and generate 4 cashflows, cashflow status = Ready, Settlement-method = Util

tradeId: 6709074617

cashflows: 006709074618(C1), 006709074619(C2), 006709074620(C3), 006709074621(C4)

1, Remove action for netting/swift suppress/cashflow suppress/fail/update affirmation/early release/hold /Settle As Gross for Util cashflow

2, Add Cashflow.Remaining_Amount on view builder

3, Add Trade.Source_System_Trade_Internal_Id on view builder/customer filters

![image-2025-11-3_18-37-47.png](attachments/image-2025-11-3_18-37-47.png)

Add cashflow status UTILIZED, PARTIALLY-UTILIZED, PASTDUE

![image-2025-11-3_18-32-46.png](attachments/image-2025-11-3_18-32-46.png)

Settlement method in cashflow blotter to add UTIL

![image-2025-11-3_18-34-3.png](attachments/image-2025-11-3_18-34-3.png)

Add Settlement Means value--FXBRREC-M in vostro

![image-2025-11-3_18-30-50.png](attachments/image-2025-11-3_18-30-50.png)