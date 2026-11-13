Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| | | | | |

### **Description 

**

When cashflow in status "Pending Netting "

1. NDS Netting->No*n-D*eliverable Interest Rate Swap Cashflows of NDS must be Auto Netted by system based on NID
2. IRS Netting When there's IRS booked by Blade/Stella, all the fix leg cashflow would be generated as the rate are known. These fix leg interest payment will be available in Ratan in advance probably in 'PROJECTED' status. The corresponding floating leg payment will be generate when the floating rate is fixed which normally happen on VD-2. As the Settlement practice client would expect SCB to settle the net amount of the** fix leg & floating leg** for each schedule. [IRS Fix Leg & Floating leg payment handling - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2726685251#IRSFixLeg&Floatinglegpaymenthandling-Fixleg&floatingleginRatan:(SourcefromStella))
3. Netting by Auto Netting Rules
4. CCIL Netting For India market there're trades booked with CCIL counterparties and settlement ops would net these to one cashflow against the **CCIL central counterparty**. Swift generation would be bypassed for the netting resultant cashflow and only accounting required.
5. Beneficiary BIC Netting BIC netting should have higher priority than Bilateral manual netting.
6. Bilateral Netting Netting based on the Rules set up by User, usually specific for some counterparties
7. Inter Entity Netting

There should be Linkage for cash flows on 2 sides, before auto netting, checks should happen

- - CCY, VD. amount should be the same between C1 C2 - Direction of C1 C2 should be opposite - C1 booking entity fmid = C2 counterparty mapped value - C2 booking entity fmid = C1 counterparty mapped value

### **Main Flow Diagram **

**![](https://confluence.global.standardchartered.com/download/attachments/3121440072/BIC%20Net.png?api=v2)**

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | select * from cash_netting_service.ratan_auto_netting_cashflow ranc | Short description for job |
| 2 | select * from cash_netting_service.ratan_auto_netting_type_config | |

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

- List the related articles