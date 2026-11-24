Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Junying Jiang | 2026-01-12 | | | |

### **Description 

**

1. LEIN flag query : When LIEN is placed & Lien amount update on a trade, all of its cashflows (including interest) must be NSTP in RATAN with 'LIEN' exception (Maker + Checker)
2. Fixing flag query : When there's IRS booked by Blade/Stella, all the fix leg cashflow would be generated as the rate are known. These fix leg interest payment will be available in Ratan in advance probably in 'PROJECTED' status. The corresponding floating leg payment will be generate when the floating rate is fixed which normally happen on VD-2. As the Settlement practice client would expect SCB to settle the net amount of the fix leg & floating leg for each schedule.
3. BIC net flag query: if cashflow satisfy with details "BIC Netting Static" Tile, , the cashflow would mark BIC net flag as "Y"
4. Currency SpotRate query: cashflow needs to set a flag "Cashflow_Amount_USD_Transfered" to indicate the equivalent amount in USD currency

### **Main Flow Diagram **

1. Lien Flag, if any issue with TDS3 ES, Lien flag can not be checked, the cashflow might be wrong stped to downstream **Single trade query from TDS3 ES**: RATAN will get the cashflows from Murex and call the TDS3 trade, each cashflow would trigger one call to TDS3 ES by the Trade_Id( from Murex cashflow). The overall projected daily Murex cashflow daily volume is around 50k. Can refer to TDS3 document how to query the latest record from ES API [TL API: Query Hints - SABRE - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/SABRE/TL+API%3A+Query+Hints). ![image-2026-2-11_12-9-57.png](attachments/image-2026-2-11_12-9-57.png) **For Notification: **If cashflow comes before trade update, it may not have LIEN exception. Then when trade notification comes, it will be reflected in cashflow according to original trade ID. Current design, RATAN will only consume trade notification with VALD/COMP status by priority.
2. Fixing flag Logic to Identify IRS Interest cashflows - applicable for **Stella **cashflows if (CashFlowInfo.Data_Flow__Data_Source_System=='Stella' and Instrument_Common.ISDA_Taxonomy in(' InterestRate:IRSwap:FixedFloat','InterestRate:IRSwap:OIS','InterestRate:IRSwap:FloatFloat','InterestRate:IRSwap:FixedFixed') and Cashflow.Payment_Type in('**Coupon/Fixed**','**Coupon/Float**') ) and Cashflow.Cashflow_Event_Type != Withdrawal Then compare cashflow number with TDX for same cashflow ID and value date, If RATAN cashflow number < TDX cashflow number, then update status to** "WAITING + Pending another leg"** else go to next check - applicable for **Murex **cashflows if (CashFlowInfo.Data_Flow__Data_Source_System=='Murex' and pending_fixing flag='Y' and Cashflow.Cashflow_Event_Type != Withdrawal If pending_fixing flag='Y', then update status to** "WAITING + Pending another leg"** else go to next check For MUREX cashflows, Fixed leg sent to Ratan first, and after floating leg is fixed, there would be cashflow sent to reverse the original fixed leg one, and then another netted cashflow to send with fix flag is N For Stella Cashflows, Fixed leg and Floating leg would send to Ratan separately, IRS netting would be performed automatically

3. Cashflow_Amount_USD_Transfered flag

There are two places in the process where this flag is used, one is the high-value payment check of nstp rule, and the other is the inter entity netting check of autonetting netting rule.

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | | |
| 2 | | |

### **Jobs**

List the function related jobs and description

| # | Job Name | Description |
| --- | --- | --- |
| 1 | Job name | Short description for job |
| 2 | | |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Name | Description |
| --- | --- | --- |
| 1 | name | Short description |
| 2 | | |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here

### **Related articles **

- [Fixing flag notification - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Fixing+flag+notification)
- [LIEN Processing & Pending Fixing Flag Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3186834133)
- ****