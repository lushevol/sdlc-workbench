Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Zhenzhen Liu | 2026-09-17 | | | |

### **Description **

- The **option expiry / exercise (EXR / EXP) fixing process** involves manual rate inputs in the TP system. Depending on the fixing cut, rates are sourced either from **Market Data Systems (MDS)** or provided by the **Trading Desk via Voice Cuts**. Due to the manual nature of the fixing process, there is a risk of: - Incorrect fixing rate application - Fat‑finger / data entry errors - Fixing significantly away from prevailing market levels - Incorrect exercise / expiry outcomes and downstream settlement or PnL impact To mitigate these risks, Trade Control is required to perform a **daily independent control check** to validate: - The **published fixing index vs the applied TP system rate**, and - That appropriate **tolerance logic** is applied based on the fixing type. The current control relies heavily on manual EUC processing. This ADO proposes an **automated blotter‑based solution** to strengthen governance, consistency, and auditability of the option fixing control.

### **Main Flow Diagram **

A new fixing blotter used by Trade Control user to check the Option expiry/exercise fixing rate.

We need to query all the trade whose expiry date is "Today" and generate a summary report for user to check and compare the rate input by trade control user manually.

### ![Opt fixing summary (1).png](attachments/Opt fixing summary (1).png)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratan_trade_opt_expiry_summary_snapshot | option expiry blotter if user act on the page |
| 2 | ratan_trade_opt_expiry_summary_actived_version | option expiry blotter latest version |
| 3 | ratan_trade_opt_expiry_control_check/ratan_trade_opt_expiry_control_check_audit | user upload rate |
| 4 | ratan_trade_opt_expiry_control_check_event | user upload rate |
| 5 | ratan_trade_opt_expiry_cut_reference/ratan_trade_opt_expiry_cut_reference_audit | static data for fixing source by user uploading |
| 6 | ratan_trade_opt_expiry_cut_reference_event | static data for fixing source by user uploading |

### **Jobs**

List the function related jobs and description

| # | Job Name | Description |
| --- | --- | --- |
| 1 | NA | Short description for job |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Name | Description |
| --- | --- | --- |
| 1 | | |
| 2 | | |
| 3 | | |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| NA | Short description |

### **Issue**

### **Related articles **

- [Requirement - Blotter/Dashboard for Rate Enquiry on Option Expiry Cuts - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3756400571)