Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Junying Jiang | 2026-03-10 | | | |

### **Description **

- Uber Json would keep both Trade and Cashflow in one message, and upstream would do the validation before sending out to downtime.
- Ratan would refer the validation status and do the Uber validation
- If Validation error, message would save with filtered in Ratan, but same can not view from Ratan UI, User needs to check from upstream UI ET
- Once validation passed, Uber validated event would be published for further processing.
- Cashflow would be extracted and check if the cashflow was processed based on cashflow id +version, if all processed, filter, if not, extra cashflow could batch published and process.

### **Main Flow **

### ![image-2026-3-10_9-10-21.png](attachments/image-2026-3-10_9-10-21.png)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratan_cashflow_group_management_service.ratan_inbound_message | ratan inbound message |
| 2 | ratan_cashflow_group_management_service.ratan_cashflow_rounding_config | amount rounding |

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
| 1 | FMEDMI2_GDCW_PROD?q-51358-ratanone-uber-msg | Received Uber from upstream |
| 2 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-fx-other-msg |
| 3 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-fx-spot-msg |
| 4 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-cash-msg |
| 5 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-com-msg |
| 6 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-interestrate-msg |
| 7 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-loan-msg |
| 8 | FMEDMI2_GDCW_PROD?q-51358-ratanone-fmrptdsx-uber-credit-msg |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here

### **Related articles **

- List the related articles