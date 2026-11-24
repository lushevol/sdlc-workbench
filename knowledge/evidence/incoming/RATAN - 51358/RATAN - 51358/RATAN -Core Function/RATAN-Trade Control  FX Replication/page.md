Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Zhenzhen Liu@Yunzhe Ta | 2026-01-13 | | | |

### **Description **

- Murex Trades (**FX Cash trades **booked by RATES desk) are replication to Razor for the purpose of Settlements in Pre-FMRP stack. These trades are replicated to Non-Standard Portfolios (NSP) only for the purpose of Settlements. As part of FMRP, Razor will continue to remain as one of the key systems in the overall settlements process. Before replicating to Razor, Ratan needs to real-time filter and only replicate eligible FX trades, which RAZOR is supporting for settlement.

### **Main Flow Diagram **

Only Rules Satisfied, same would be sent to downstream
![](https://confluence.global.standardchartered.com/download/attachments/3501535281/Fx%20Replication.png?api=v2)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratanone.ratan_trade_replay | save replication trade |
| 2 | ratanone_rule_service.ratan_rule_engine rre where business_flow = 'FX_REPLICATE' | Rule configuration |

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
| 1 | TDS3_Trade_Message_Process_In, Trade_Service_TDS3_Trade_Replay, Confirmation_Rule_Process_Out_To_Razor | Kafka topic |
| 2 | v1/post-trade/51358-ratanone/razor/scbml-4.0/trade/fx/pub | send trade to Razor |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- User is able to check & modify rule in "MO Rules" blotter, screenshot as below.

![image-2026-1-13_17-9-54-1.png](attachments/image-2026-1-13_17-9-54-1.png)![image-2026-1-13_17-9-36-1.png](attachments/image-2026-1-13_17-9-36-1.png)

### **Related articles **

- [Ratan Trade Control Onboarding - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+Trade+Control+Onboarding)