Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Junying Jiang@Yunzhe Ta | 2026-01-13 | | | |

### **Description **

- As the FMRP Program, Ratan takes the responsibility to generate the swift message with cashflow data+ SSI(Vostro & Nostro) data . Ratan will send the swift message to FM Swift Gateway, and FMSGW will take responsibility to communicate with AMH/SCPAY and return the ACK/NACK to Ratan. Ratan has the capability to generate MT or MX format message per requirement.

### **Main Flow Diagram **

1 Cashflow Status +Cashflow Sub Status is on  Ready +NA,  Cashflow is ready for swift generation, Pending release cutoff 
![image-2026-1-9_15-56-25.png](attachments/image-2026-1-9_15-56-25.png)

2 Control-M job RAT_CN_HOLD_RELEASE will pick up the cashflow with release cutoff reached start the MT message generation, please refer the diagram below to get the swift type generation logic

3 As ISO project, per specific logic defined in [application.yml - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service?path=/src/main/resources/application.yml) ,  if no MT conversion is required , MT sent to FMSGW, if conversion is required, convert MT to MX and send MX to FMSGW

**Design flow diagram shows as below**

![](https://confluence.global.standardchartered.com/download/attachments/2974005425/Current%20Data%20flow_full.png?api=v2)

**MT generation logic shows as below **

![](https://confluence.global.standardchartered.com/download/attachments/2948198420/Swift.png?api=v2)

**Ratan cashflow Status change logic **shows as below

![](https://confluence.global.standardchartered.com/download/attachments/2948198420/Swift%20Status-new.png?api=v2)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratanone_swift_service.swift_message | Short description for job |
| 2 | SELECT x.* FROM ratanone_swift_service.swift_raw_message | |

### **Jobs**

List the function related jobs and description

| # | Job Name | Description |
| --- | --- | --- |
| 1 | RAT_CN_HOLD_RELEASE | Release cashflow with Queued Cut Off |
| 2 | | |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Name | Description |
| --- | --- | --- |
| 1 | Cash_Settlement_Orchestration_Swift_Out | Cashflow published for swift generation |
| 2 | Cash_Settlement_Swift_Process_Out | Generated MT send to FMSGW |
| 3 | Cash_Settlement_Release_Response_Process_In | MT response received from FMSGW |
| 4 | MX_FMSGW_Out | Generated MX send to FMSGW |
| 5 | Swift_MX_ENISIS_Out | For MX KR, Generated MX send to ENISIS |
| 6 | Swift_MX_FMSGW_Ack | MX response received from FMSGW |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Provider | Short description |
| Swift translator | Published from Swift Network, used for swift generation and swift validation. yearly swift upgrade is managed by FM |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here

### **Related articles **

- [FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)
- [RATAN Swift Generation Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2974005425)