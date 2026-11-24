Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Junying Jiang | 2026-01-12 | | | |

### **Description **

- Ratan would query SSI+ ES to get the Vostro, based on the vostro data, Ratan can do the nostro matching for swift generation
- If any update from SSI+ , notification would send from SSI+ to Ratan and Cashflow pending in Ratan still would perform SSI refreshing

### **Main Flow Diagram **

1. We would try to query SSI+ ES API for one time only to get all possible **Vostro ** **Parameter used as sample below.** QueryVostroAccount query string is: *query {* * ssis(filter: [* * {field: "Settlement_Instruction.BranchId_Murex3Id", operator: IN, values: ["SCB HONGKON*HKG","Global"] },* * {field: "Settlement_Instruction.Payment_Currency", operator: IN, values: ["USD"] },* * {field: "Settlement_Instruction.CFI_Code", operator: IN, values: ["*Y****","DY****","DYX***","******"] },* * {field: "Settlement_Instruction.Counterparty_SCI_FMID", operator: IN, values: ["400016898"] },* * {field: "Settlement_Instruction.Debit_Credit", operator: IN, values: ["Debit","Both"] },* * {field: "Settlement_Instruction.Settlement_Type", operator: IN, values: ["CASH"] },* * {field: "Settlement_Instruction.Settlement_Method", operator: IN, values: ["CASH","FEDWIRE"] },* * {field: "Settlement_Instruction.SSI_Status", operator: IN, values: ["Active","New","Update"] } *
2. There can be multi Vostro setup from different dimensions, there was [best matching logic](https://confluence.global.standardchartered.com/display/DSP/Vostro+SSI+Best+Matching+-+UK+Cashflow+Migration) defined to decide which SSI is the best to use for settlement. normally below principle followed 1. Entity(branchIdMurex3Id)to check first , Entity prior to Global 2. CFI_code, most detail granular level prior others 3. Is_Default_SSI, primary SSI as high priority.
3. **Nostro , based on the user configured Nostro Mapping in Ratan to query the nostro information and enrich **1) Use **portfolio+****ccy **to query nostro data(for **RFI**) 2) Based on trade 1) legal entity fmid 2) currency, vostro 3) settlement Means 4) settlement account
4. ![](https://confluence.global.standardchartered.com/download/attachments/2402083192/FMRP%20-%20Trade%20SSI%20Stamping.png?api=v2)

SSI + also send notification to Ratan if any

5.  If stamping from SSI+ ,but user think update is required, Adhoc update can perform by user, if swift type is MT103, address information would capture from SCI (cache first, if not available, adhoc call )

![image-2026-5-14_10-42-50.png](attachments/image-2026-5-14_10-42-50.png)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | Only available to check for BCS flow , not listed | |
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

- [**FMRP - SSI Stamping Flow - Derivative Strategy Projects - Confluence**](https://confluence.global.standardchartered.com/display/DSP/FMRP+-+SSI+Stamping+Flow)
- [**Vostro SSI Best Matching - UK Cashflow Migration - Derivative Strategy Projects - Confluence**](https://confluence.global.standardchartered.com/display/DSP/Vostro+SSI+Best+Matching+-+UK+Cashflow+Migration)
- **[Cashflow Dedicated Nostro Stamping Design(like RFI/STRATEGY/etc.) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3554628740)**
- ****