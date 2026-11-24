Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| | | | | |

### **Description **

- To automatically check whether a trade is valid or not against a set of pre-defined rules. All of the violations would be record in Ratan Exception Platform to assist Trade Review.

### **Main Flow Diagram **

After trade received in Ratan from TDS3 , Ratan would build facts based on the trade info received and  identify if hitting any rule , if no matching rules, close pre-version exception if any. if matching rule, close pre-version exception and generate exception of current version

Same would show to user to view from exception blotter

### **![](https://confluence.global.standardchartered.com/download/attachments/3501535281/trade%20auto-valication.png?api=v2)**

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratan_trade_auto_rule_validation | All trades received with exception details |
| 2 | ca_trade | Trade with PV information for CnA PV check |

### **Jobs**

List the function related jobs and description

| # | Job Name | Description |
| --- | --- | --- |
| 1 | NA | Short description for job |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Name | Description |
| --- | --- | --- |
| 1 | TDS3_Trade_Message_Process_In | Trades received from upstream |
| 2 | TDS3_Trade_Murex_Message_Process_In | Trades received from upstream |
| 3 | Trade_Service_TDS3_Trade_Replay | Trades received from upstream |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| NA | Short description |

### **Issue**

### **Related articles **

- [Ratan Trade Control Onboarding - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+Trade+Control+Onboarding)