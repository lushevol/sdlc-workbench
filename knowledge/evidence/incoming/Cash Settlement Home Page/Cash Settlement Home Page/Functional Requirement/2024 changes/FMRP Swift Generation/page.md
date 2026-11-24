# Background

As the FMRP 2024 roadmap Ratan is going to build the capacity generating swift message, Ratan would take the cashflow + SSI(Vostro & Nostro) and generate the swift message. As agreed in the FMRP programme level, Ratan will send the swift message to FM Swift Gateway and

they will take responsibility to communicate with AMH/SCPAY and return the ACK/NACK to Ratan.

# Query Swift Message From UI

- MT message generated from Ratan (CN,MY,IN, partial SG) - Query from Ratan with cashflow ID
- MT message generated from Razor (LOANIQ, EG, NP, SA) - Query from FMSRE with tag20
- MX message generated from Ratan - Query with cashflow ID (SG) – Query from Ratan with cashflow ID

# Cashflow/Swift Status Event

| Event | RATAN Cashflow Status | RATAN Cashflow Sub Status | Swift Status | Swift Status Reason |
| --- | --- | --- | --- | --- |
| Single MT Message | MT103/202 COV | |
| Cashflow Stamped and before release cutoff | READY | N/A | | | |
| Cashflow stamped and past the release cutoff, msg sent to swift generation service | READY | Pending Ack | Pending Swift Init | | |
| Swift Generation Failed for different reason: 1. technical issue 2. validation failed | READY (will be changed to FAILED by EOD job) | Pending Ack | Ratan Internal Error | If latest response received for both swift msg are the same, set the value to the same as received sub status else set the field to "Check in FMSGW" or "Check in FMSRE" | {Swift Error Description} |
| Swift send to MX process | READY | Pending Ack | Pending MX Ack | |
| tech ack from MX generation | READY | Pending Ack | MX Generation Received | |
| MX generation failed | READY | Pending Ack | MX Generation Error | |
| MX message sent to FMSRE | RELEASED | | Pending FMSRE Ack | |
| Swift generated successfully and sent to FMSGW | RELEASED | | Pending FMSGW Ack | |
| Receive Response: Pending FMSGW Disp Pending FMSRE Disp Pending Manual Rel Released to FMSWG FMSGW Error FMSRE Error AMH Error SCSTAR Error | RELEASED | | Pending FMSGW Disp Pending FMSRE Disp Pending Manual Rel Released to FMSWG FMSGW Error FMSRE Error AMH Error SCPAY Error | {Sub Status Description} |
| Released by AMH Released by SCSTAR FMSGW Deleted FMSRE Deleted Manual Delete | SETTLED | | Released by AMH SCPAY Processed FMSGW Deleted FMSRE Deleted Manual Delete | Both msg received is one of below: Released by AMH SCPAY Processed FMSGW Deleted FMSRE Deleted Manual Delete | |

- Technical ACK/NACK is expected from FMSWIFTGATEWAY within 5 mins as the timeout setup.

# FMSGW Integration Event

**EXPAND: FMSGW Integration Event**

| **Queue** | **Description** | **Response Status** | **Response Sub Status** | **Comment** | **RATAN Cashflow Status** | **Swift Status** ** **(New field to display returned swift sub status) **NOTE**: for MT103/202 COV, need to check the response status from both message, if they are the same, follow below mapping. if they are different, set the Swift Status to "**Check in FMSGW**" |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | No swift generated, settled in Ratan | SETTLED | |
| | | | | Payment released from RATAN, no response yet from FMSGW | RELEASED | Pending FMSGW Ack |
| | FMSGW Tech ACK | ACK | Pending FMSGW Disp | Tech ACK means FMSGW received the message | RELEASED (Already in RELEASED status when message sent to FMSGW, no change in status) | Pending FMSGW Disp |
| Eligible Currency Failure Duplicate Message Queue Back Valued Queue Original Missing Cancel Queue Manual Cancel Queue Low Value/Threshold/highValue Approval Queue | FMSGW Business ACK | ACK | Pending Manual Rel | MT validation success, imported by FMSGW. Next status 1. user manual release the msg, next status will be based on the subsequent queue / status in FMSGW 2. user manual terminate the msg, next status will be "Manual Delete" | RELEASED | Pending Manual Rel |
| Any Queue Deleted Message Queue | ACK | FMSGW Deleted | Next status： User can do manual un-delete, but this will not send any status back to Ratan | **SETTLED** (Expectation is for User to perform manual payment via Oscar / AMH) | FMSGW Deleted |
| Swift Validation Failure SCB Validation Failure Static Validation Failure | FMSGW Business NACK | NACK | FMSGW Error | Next status： User can only do Terminate action, but this will not send any status back to Ratan | RELEASED (Since user terminated it manually, expectation is for User to perform manual payment via Oscar / AMH) | FMSGW Error |
| No Match Message Queue | FMSGW Business NACK | NACK | Manual Delete | User manual delete in FMSGW | **SETTLED** (Since user deleted it manually, expectation is for User to perform manual payment via Oscar / AMH) | Manual Delete |
| | AMH NACK | NACK | AMH Error | The only NACK sub status from AMH | RELEASED | AMH Error |
| | AMH ACK | ACK | Released by AMH | The only ACK sub status from AMH | ** SETTLED** | Released by AMH |

**EXPAND_END**

## Message Header to FMSGW

| **#** | **Header attribute** | **Field Mapping** | **sample value** | **Comment** |
| --- | --- | --- | --- | --- |
| 1 | bookingSystem | RATAN | MX_FXCASH RATAN | |
| 2 | OPICSBranch | **{Field_Branch_Code}** | 73 | |
| 3 | targetSystem | FMSGW | FMSGW | |
| 4 | messageType | Settlement | Settlement Confirmation | |
| 5 | mxDocID | {Tracking ID} | 2818964550 | for Razor, this mxDocID will map to Response SystemRef field. |
| 6 | trackingId | {Tracking ID} | MX_FXCASH_DLV_395178218_2818964550_1707907993965 | |

## Message Template to FMSGW

**EXPAND: Message Template to FMSGW**

<?xml version="1.0" encoding="UTF-8"?>
<scb:SCBML scbmlVersion="4-0" xmlns:scb="[http://www.sc.com/SCBML-1](http://www.sc.com/SCBML-1)" xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)" xmlns="[http://www.sc.com/scbml/communication/external-1](http://www.sc.com/scbml/communication/external-1)" xmlns:fpmlrep="[http://www.fpml.org/FpML-5/reporting](http://www.fpml.org/FpML-5/reporting)" xsi:schemaLocation="[http://www.sc.com/SCBML-1](http://www.sc.com/SCBML-1) ../../../core/4-0/scbml-4-0.xsd [http://www.sc.com/scbml/communication/external-1](http://www.sc.com/scbml/communication/external-1) ../../../payloadType/externalCommunicationPayload/4-0/scbml-externalCommunicationPayload-4-0.xsd">
<scb:header>
<scb:messageDetails>
<scb:messageVersion>1.0</scb:messageVersion>
<scb:messageType>
<scb:typeName>ExternalCommunication</scb:typeName>
<scb:subType>
<scb:subTypeName>SWIFTMessage</scb:subTypeName>
</scb:subType>
</scb:messageType>
</scb:messageDetails>
<scb:originationDetails>
<scb:messageSender>
<scb:messageSender systemScheme="[http://www.sc.com/coding-scheme/system](http://www.sc.com/coding-scheme/system)">RATAN</scb:messageSender>
<scb:senderDomain>
<scb:domainName domainNameScheme="[http://www.sc.com/coding-scheme/domain-name](http://www.sc.com/coding-scheme/domain-name)">FM</scb:domainName>
<scb:subDomainName subdomainNameScheme="[http://www.sc.com/coding-scheme/subdomain-name](http://www.sc.com/coding-scheme/subdomain-name)">
<scb:subDomainType>PaymentData</scb:subDomainType>
</scb:subDomainName>
</scb:senderDomain>
<scb:countryCode>ALL</scb:countryCode>
</scb:messageSender>
<scb:messageTimestamp>**{Message sent out time, sample format: 2023-03-30T09:29:02Z}**</scb:messageTimestamp>
<scb:initiatedTimestamp>**{Message sent out time, sample format: 2023-03-30T09:29:02Z}**</scb:initiatedTimestamp>
<scb:trackingId>**{uuid}**</scb:trackingId>
</scb:originationDetails>
<scb:captureSystem>FMSwiftGateway</scb:captureSystem><!--Hardcoded as FMSwiftGateway if message sent to FMSGW-->
<scb:process>
<scb:processName>ExternalCommunicationNotification</scb:processName>
<scb:eventType>Report</scb:eventType>
<scb:workflowState></scb:workflowState>
<scb:trackingVersion></scb:trackingVersion><!-- fill actual version or hardcode as 1, this is optional field for data modelling-->
<scb:tradeId tradeIdScheme="[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)">**{Cashflow Id}**</scb:tradeId><!- fill any ref data-->
</scb:process>
</scb:header>
<scb:payload>
<scb:payloadFormat>XML</scb:payloadFormat>
<scb:payloadVersion>ExternalCommunication-4-0</scb:payloadVersion>
<externalCommunicationNotification fpmlVersion="5-9">
<tradeSource tradeSourceScheme="[http://www.sc.com/coding-scheme/tradeSource/originalSourceSystem](http://www.sc.com/coding-scheme/tradeSource/originalSourceSystem)">
<name>**{Data_Flow.Data_Source_System}**</name><!--get the value from cashflow and set to this path-->
</tradeSource>
<externalSnapshotReport>
<communicationDomain>SWIFTGateway</communicationDomain>
<communicationFormat>MT</communicationFormat><!--for MT message use MT, for MX please fill as MX-->
<communicationName>SWIFTMessage</communicationName>
<confirmationOrPaymentReport>
<confirmationMethod>SWIFT</confirmationMethod>
<linkId linkIdScheme="[http://www.sc.com/coding-scheme/linkId/confirmationDocumentLinkId](http://www.sc.com/coding-scheme/linkId/confirmationDocumentLinkId)"></linkId>
<reportRawData>
<tradeID>**{Cashflow Id}**</tradeID><!--you can fill any ref data-->
<tradeVersion></tradeVersion><!--Confirmed with Nicole this can be set to null -->
<legIndicator></legIndicator><!- Confirmed with Nicole this can be set to null -->
</reportRawData>
<resources>
<resourceId resourceIdScheme="[http://www.sc.com/coding-scheme/resourceId](http://www.sc.com/coding-scheme/resourceId)">Payment</resourceId>
<resourceType resourceTypeScheme="[http://www.sc.com/coding-scheme/resourceType](http://www.sc.com/coding-scheme/resourceType)">Embedded</resourceType> <--hardcode value-->
<message>**{****Swift Message****}**</message>
</resources>
</confirmationOrPaymentReport>
</externalSnapshotReport>
<party id="Party1">
<fpmlrep:businessUnit>
<fpmlrep:businessUnitId>**{Sender Branch Code}**</fpmlrep:businessUnitId>
<fpmlrep:country>**{Sender Country}**</fpmlrep:country><!--sender country code -->
</fpmlrep:businessUnit>
</party>
</externalCommunicationNotification>
</scb:payload>
</scb:SCBML>

**EXPAND_END**

# MX Generation Integration Event

**EXPAND: MX Generation Integration Event**

| **Description** | **Response Status** | **Response Sub Status** | **Comment** | **RATAN Cashflow Status** | **Swift Status** | **Swift Status Reason (50 Charaters)** |
| --- | --- | --- | --- | --- | --- | --- |
| | | | MT message sent to MX generation, no response yet | **READY** | Ready for Swift **NOTE**: for MT103/202 COV, need to check the response status from both message, if they are the same, follow below mapping. if they are different, set the Swift Status to "Check in FMSRE" | |
| | | | MX message sent to FMSRE | **RELEASED** | Pending Ack | |
| FMSRE Tech ACK | ACK | Pending FMSRE Disp | Tech ACK means FMSRE received the message | RELEASED (Already in RELEASED status when message sent to FMSRE, no change in status) | Pending FMSRE Disp | |
| FMSRE Business ACK | ACK | Pending Manual Rel | | RELEASED | Pending Manual Rel | |
| ACK | FMSRE Deleted | | **SETTLED** (Expectation is for User to perform manual payment via Oscar / AMH) | FMSRE Deleted | |
| FMSRE Business NACK | NACK | FMSRE Error | | RELEASED (Since user terminated it manually, expectation is for User to perform manual payment via Oscar / AMH) Razor will confirm if another status can be sent to RATAN based on terminate action | FMSRE Error | |
| FMSRE Business NACK | NACK | Manual Delete | | **SETTLED** (Since user deleted it manually, expectation is for User to perform manual payment via Oscar / AMH) | Manual Delete | |
| AMH NACK | NACK | SCSTAR Error? | | RELEASED | SCSTAR Error | |
| AMH ACK | ACK | Released by SCSTAR | | ** SETTLED** | Released by SCSTAR | |

**EXPAND_END**

## MX Message Header

| | FMRP Mapping | Sample from Murex | Comment |
| --- | --- | --- | --- |
| "entity_fmid": | Entity.Booking_Entity_SCI_FMID | "10075222", | |
| "cms_account": | if (Settlement_Instruction.Account.SCB_Nostro_Account_Type ='Over-Account') then 'Y' else 'N' | "N", | ratan send over account flag instead |
| "benificial_code": | Settlement_Instruction.Account.Beneficiary_BIC_code | | |
| "entity_label": | entity.booking_Entity_SCI_FMCODE | "LONDON" | Optional, only for exception GUI, will FMCODE be OK? SCB LONDON*LDN |
| "ebbs_nos": "15267980996", | settlement_Instruction.account.EBBS_Account_Number | "15267980996", | |
| "pb_account": "N", | cashflow.is_Private_Banking_Cashflow | | |
| "uetr": "21c2ab39-d8e8-4173-8704-fd96ccc594fa", | | | Only required for 192/292 set with the 121 value to link original message |
| "counterparty_fmid": "401031402", | Entity.Counterparty_SCI_FMID | | |
| "currency": "EUR", | cashflow.payment_Currency | | |
| ~~ "beneficiary_fmid": "",~~ | ~~TBC~~ | | ~~only used for MT202~~ |
| "counterparty_label": "EFIVTALBOTP/LDN" | entity.counterparty_SCI_FMCODE | | Optional, only for exception GUI, will FMCODE be OK? SCB LONDON*LDN |
| "Settlement_Instruction": { "Account": { "SCB_Nostro_Account_Number": "CNO MAIN", "SCB_Nostro_Account_Type": "NOS", "Beneficiary_BIC_code": "", "Beneficiary_Account_Name": "", "Beneficiary_Account_Name_2": "", "Beneficiary_Street_Address": "", "Beneficiary_City": "", "Beneficiary_Account_Number": "", "Intermediary_BIC_code": "", "Intermediary_Account_Name": "", "Intermediary_Street_Address": "", "Intermediary_City": "", "Intermediary_Account_Number": "", "Beneficiary_Bank_BIC_code": "", "Beneficiary_Bank_Account_Name": "", "Beneficiary_Bank_Street_Address": "", "Beneficiary_Bank_City": "", "Beneficiary_Bank_Account_Number": "", "Beneficiary_Correspondent_BIC_code": "", "Beneficiary_Correspondent_Account_Name": "", "Beneficiary_Correspondent_Street_Address": "", "Beneficiary_Correspondent_City": "", "Beneficiary_Correspondent_Account_Number": "", "Ordering_Customer_BIC_Code": "", "Ordering_Customer_Account_Name": "", "Ordering_Customer_Street_Address": "", "Ordering_Customer_City": "", "Ordering_Customer_Account_Number": "", "Counterparty_CMS_Account_Number": "", "EBBS_Bridge_Account_Number": "370203191524643010", "EBBS_Account_Number": "370203191524643010", "Booking_Entity_Correspondent_BIC_code": "SCBLCNSXJNA", "Booking_Entity_Correspondent_Account_Name": "SCB CHINA JINAN BRANCH JNA", "Booking_Entity_Correspondent_Street_Address": "G/F N 9F, BLOCK B, WANDA PLAZA NO 5 JINGSI RD", "Booking_Entity_Correspondent_City": "JINAN SHANDO", "Booking_Entity_Correspondent_Account_Number": "370203191524643010" }, | | | need to send the raw data values got from SSI+ consider swift generation may truncate the values because of length limitation in MT message |

# ENISIS Integration Event

**EXPAND: enisis integration event**

| **Description** | **/AMHMessage/Payload/ResponseHeader/Status** | **Comment** | **RATAN Cashflow Status** | **Swift Status** | **Swift Status Reason (50 Charaters)** |
| --- | --- | --- | --- | --- | --- |
| | | MT message sent to MX generation, no response yet | **READY** | Ready for Swift **NOTE**: for MT103/202 COV, need to check the response status from both message, if they are the same, follow below mapping. if they are different, set the Swift Status to "Check in FMSRE" | |
| | | Swift (MT/MX) generated successfully and sent to ENISIS | **RELEASED** | Pending ENISIS Ack | |
| ENISIS Tech ACK | 2 | Tech ACK means ENISIS received the message | **RELEASED** (Already in RELEASED status when message sent to ENISIS, no change in status) | Pending ENISIS Disp | |
| ENISIS Business ACK | 0 | Business ACK means ENISIS received ACK from SAA/AMH | **SETTLED** (Expectation is for User to perform manual payment via Oscar / AMH) | Released by AMH | /AMHMessage/Payload/ResponseHeader/StatusMessage |
| 1 | Business NACK means ENISIS received NACK from SAA/AMH | **RELEASED** | AMH Error | /AMHMessage/Payload/ResponseHeader/StatusMessage |

Tracking ID refer to path /AMHMessage/Header/UniqueID

**EXPAND_END**

Reference: [RATAN to ENISIS - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+to+ENISIS)

# Swift Message Type

- PM (Precious Metal) Currency list **EXPAND: PM Currency List** | PM Currency | | --- | | XAU | | XAG | | XPD | | XPT | | XRH | | XU5 | | XG2 | | XT3 | | XD3 | | XRU | | XS9 | | XS5 | | XSD | | XU6 | | XU7 | | XG5 | | XUC | | XG3 | | XGC | | XD1 | | XD2 | | XG1 | | XR1 | | XT1 | | XT2 | | XU1 | | XU2 | | XU3 | | XU4 | | XU8 | | XTN | | XDN | | XUD | | XG4 | | XG6 | | XGF | | XS6 | | XSF | | XSI | | XS4 | | XGI | | XGA | | XG7 | **EXPAND_END**
- ISO MX condition: Swift Type not in (MT604,MT605,MT692,MT210) and NOT( Swift type = MT292 and Original_Swift_Type = MT210) and Field_Sender_BIC (0,7) in ('SCBLSGSG','SCBLSG22') and (Receiver = internal branches BIC (Starting with SCBL*) or Botswana BIC SCHBBWGX*) | | | SG Entity BIC | | --- | --- | --- | | 300036368 | ACU SING | SCBLSGSGXXX | | 3 | DBU SING | SCBLSGSGXXX | | 400451508 | SCB SG LTD*SIN | SCBLSG22XXX | | 400452428 | SCB SG LTDACU*SIN | SCBLSG22XXX |

# Swift Message Template - H1 2024

- MT202 {1:F01**{Field_Sender_BIC}**0000000000} {2:I202**{Field_Receiver_BIC}**N} {3:{121:**{Field_121_REF}**}} {4: :20:DV**{Field_Branch_Code}{Field_Cashflow_Id}** :21:DV**{Field_Branch_Code}{Field_Cashflow_Id}** :32A:**{Field_Value_Date}{Field_Currency}{Field_Amount} ~~{Field_52_Ordering Institution_202}~~** **If {Field_53_Sender_Correspondent} return blank, populate exception {Field_56_Intermediary_Institution} if {Field_57_Account_Institution_2} return blank, populate exception** **if {Field_58_Benificiary} return blank, populate exception {Field_72_Sender_To_Receiver}** -}
- MT103

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I103**{Field_Receiver_BIC}**N}
{3:{121:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}
**:23B:CRED
:26T:{**Field_26T**}
:32A:**{Field_Value_Date}{Field_Currency}{Field_Amount}**
:33B:**{Field_Currency}{Field_Amount}**
**If {Field_50_Ordering_Customer} return blank, populate exception**
**If {Field_53_Sender_Correspondent} return blank, populate exception
{Field_56_Intermediary_Institution}**
**if {Field_57_Account_Institution_2} return blank, populate exception
if {Field_59_Benificiary} return blank, populate exception
{Field_70_Remittance_Information}
if {Field_71_Charges_Bearer} return blank, populate exception
{Field_72_Sender_To_Receiver}
****{Field_77_POP (Dubai)}**
-}

- MT202 Flip

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I202**{Field_Receiver_BIC}**N}
{3:{121:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:32A:**{Field_Value_Date}{Field_Currency}{Field_Amount}**
**If {Field_52_Ordering_Institution} return blank, populate exception
****If {Field_53_Beneficiary} return blank, populate exception
if {Field_57_Account_Institution_2} return blank, populate exception
****if {Field_58_Sender_Correspondent} return blank, populate exception
{Field_72_Sender_To_Receiver}**
-}

- **MT202 CrossDebit**

{1:F01**{Field_Sender_BIC_CD}**0000000000}
{2:I202**{Field_Receiver_BIC_2}**N}
{3:{121:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:32A:**{Field_Value_Date}{Field_Currency}{Field_Amount}**
**If {Field_52_Ordering_Institution} return blank, populate exception
****If {Field_53_Beneficiary} return blank, populate exception
if {Field_57_Sender_Correspondent} return blank, populate exception
****if {Field_58_Sender_Correspondent_CD} return blank, populate exception
{Field_72_Sender_To_Receiver}**
-}

- MT103/202 COV (**NOTE**: this will generate 2 Swift message and send separately; in Swift message UI, display 103 above 202 )

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I103**{Field_Receiver_BIC_2}**N}
{3:{121:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}
**:23E:CORT
:26T:{**Field_26T**}
:32A:**{Field_Value_Date}{Field_Currency}{Field_Amount}**
:33B:**{Field_Currency}{Field_Amount}**
**If {Field_50_Ordering_Customer} return blank, populate exception
If {Field_53_Sender_Correspondent_103COV} return blank, populate exception
****If {Field_54_Receiver_Correspondent} return blank, populate exception**
**if {Field_57_Account_Institution} return blank, populate exception
if {Field_59_Benificiary} return blank, populate exception
{Field_70_Remittance_Information}
if {Field_71_Charges_Bearer} return blank, populate exception
{Field_72_Sender_To_Receiver}**
-}

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I202**{Field_Receiver_BIC}**N}
{3:{119:COV}{121:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:32A:**{Field_Value_Date}{Field_Currency}{Field_Amount} 
If {Field_53_Sender_Correspondent} return blank, populate exception**
**if {Field_57_Receiver_Correspondent} return blank, populate exception
if {****Field_58_Account_Institution****} return blank, populate exception
If {Field_50_Ordering_Customer} return blank, populate exception
if {Field_57_Account_Institution_2} return blank, populate exception
if {****Field_59_Benificiary****} return blank, populate exception
****{Field_72_Sender_To_Receiver}
:33B:{Field_Currency}{Field_Amount}**
-}

- MT192/MT292

{1:F01**{Same as original message}**0000000000}
{2:I{**Swift_Type**}**{Same as original message**} // Swift_Type will be 192 or 292
{3:{121:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:21:**{Same as tag 20 in original message**}
:11S:**{Original_Swift_Type}
{Field_Event_Date} 
{Original_Message_body}**
-}

- MT210

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I210**{Field_Receiver_BIC}**N}
~~{3:{121:**{Field_121_REF}**}}~~
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}
{Field_25_Account_Number}**
:30:**{Field_Value_Date} 
**:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}****
**:32B:**{Field_Currency}{Field_Amount}
if {Field_50/52_Customer} return blank, populate exception
~~{Field_56_Account_BIC}~~
**-}

- MT604

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I604**{Field_Receiver_BIC_PM}**N}
{3:{108:**{Field_121_REF}**}}
{4:
**If {Field_26_Commodity_Identity} return blank, populate exception
**:30:**{Field_Value_Date}
**:20:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}
**:23:**{Field_23_Identification}**
:32F:**{Field_32_Unit}{Field_Amount} 
****If {Field_82_Instructing_Party} return blank, populate exception**
**{Field_86_Intermediary_Institution}
{Field_87_Account_Institution} //is mandatory if currency =HAU**
**if {Field_88_Benificiary} return blank, populate exception
{Field_72_Sender_To_Receiver}**
-}

- MT605

{1:F01**{Field_Sender_BIC}**0000000000}
{2:I605**{Field_Receiver_BIC_PM}**N}
{3:{108:**{Field_121_REF}**}}
{4:
**:20:DV{Field_Branch_Code}{Field_Cashflow_Id}
If {Field_26_Commodity_Identity} return blank, populate exception
**:30:**{Field_Value_Date}**
:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}
**:23:**{Field_23_Identification}**
:32F:**{Field_32_Unit}{Field_Amount} 
****If {Field_82_Instructing_Party_605} return blank, populate exception**
**{Field_86_Intermediary_Institution}
If {Field_87_Account_Institution} return blank, populate exception
{Field_88_Benificiary_605}//is mandatory if currency = HAU, not required for other ccy**
**{Field_72_Sender_To_Receiver}**
-}

- MT692

{1:F01**{Same as original message}**0000000000}
{2:I692**{**Same as original message**}**N}
{3:{108:**{Field_121_REF}**}}
{4:
:20:DV**{Field_Branch_Code}{Field_Cashflow_Id} //if currency =HAU, **:20:CANC**{Field_Cashflow_Id}**
:21:DV**{Field_Branch_Code}{Field_Cashflow_Id}**
:11S:**{Original_Swift_Type}
{Field_Event_Date} 
{Original_Message_body} **//replace** :26C: **in the original message to **:79:**
-}

# Field Formula

****Field_Sender_BIC
****

**EXPAND: Field_Sender_BIC**

1. Get the entity FMID(Entity.Booking_Entity_SCI_FMID) from cashflow data
2. Query the entityBIC with FMID from static data

**EXPAND: Sender BIC**

| City | BIC | FMID | Country Code |
| --- | --- | --- | --- |
| BEIJING | SCBLCNSXBJG | 400001378 | CN |
| NANJING | SCBLCNSXNJG | 10020899 | CN |
| TIANJIN | SCBLCNSXTJN | 235003861 | CN |
| ZHUHAI | SCBLCNSXZHU | 10078716 | CN |
| SHANGHAI | SCBLCNSXSHA | 10036642 | CN |
| XIAMEN | SCBLCNSXIMN | 10062461 | CN |
| SHENZHEN | SCBLCNSXSHZ | 10032025 | CN |
| GUANGZHOU | SCBLCNSXGZH | 400054708 | CN |
| SUZHOU | SCBLCNSXSZH | 400054737 | CN |
| CHENGDU | SCBLCNSXCDU | 400054741 | CN |
| QINGDAO | SCBLCNSXQDO | 400057714 | CN |
| CHONGQING | SCBLCNSXCHQ | 400075752 | CN |
| HHANGZHOU | SCBLCNSXHZH | 400085753 | CN |
| NNCHANG | SCBLCNSXNCH | 400090093 | CN |
| DALIAN | SCBLCNSXDLN | 400095464 | CN |
| NINGBO | SCBLCNSXNBO | 400130180 | CN |
| HOHHOT | SCBLCNSXHHT | 400130178 | CN |
| WUHAN | SCBLCNSXWUH | 400185419 | CN |
| XXIAN | SCBLCNSXSIA | 400193370 | CN |
| FOSHAN | SCBLCNSXFSH | 400209000 | CN |
| JINAN | SCBLCNSXJNA | 400218197 | CN |
| CHANGSHA | SCBLCNSXCHS | 400220273 | CN |
| FUZHOU | SCBLCNSXFUZ | 400229749 | CN |
| TAEYUAN | SCBLCNSXTAY | 400516443 | CN |
| ZHENGZHOU | SCBLCNSXZZH | 400516442 | CN |
| KUNMING | SCBLCNSXKMG | 400667486 | CN |
| FT2 SHA | SCBLCNSXFTU | 400677737 | CN |
| HARBIN | SCBLCNSXHRB | 400683682 | CN |
| SHENYANG | SCBLCNSXSHY | 400798477 | CN |
| CHINA HO | SCBLCNSXXXX | 400899993 | CN |
| ACU & DBU | SCBLSGSGXXX | 300036368 3 | SG |
| SACU & SDBU | SCBLSG22XXX | 400451508 400452428 | SG |
| KL | SCBLMYKXXXX | 9 | MY |
| STANCHART SAADIQ*KUL | SCBLMYKXXXX | 400093619 | MY |
| SCB BOMBAY*MMB | SCBLINBBXXX | 4 | IN |
| GIFT CITY TM*MUM | SCBLINAAXXX | 400960089 | IN |
| SCB LONDON*LDN | SCBLGB2LTSY | 10075222 | GB |
| Indonesia | SCBLIDJXXXX | 8 | ID |
| Philippines | SCBLPHMMXXX | 400077978 | PH |
| MANILA | SCBLPHMMXXX | 10036428 | PH |
| Mauritius | SCBLMUMUXXX | 400018439 | MU |
| Japan | SCBLJPJTXXX | 10036382 | JP |
| Dubai | SCBLAEADXXX | 5 | AE |
| New York | SCBLUS33XXX | 7 | US |
| Johannesburg | SCBLZAJJXXX | 400032489 | ZA |
| DIFC | SCBLAEADDIF | 400045551 | AE |
| BANGKOK | SCBLTHBXXXX | 6 | TH |
| HONGKONG | SCBLHKHHXXX | 2 | HK |
| SCS HK | SCBLHKHHXXX | 300075472 | HK |
| TAIPEI | SCBLTWTPXXX | 10038345 | TW |
| OBU TAIPEI | SCBLTWTPXXX | 300011345 | TW |

**EXPAND_END**

if(length of entityBIC=11) {
       return senderBIC  = left(entityBIC,8) + "A" + right(entityBIC,3)
}else if (length of entityBIC=8){
      return senderBIC =entityBIC+"AXXX"
}else {return exception}

**EXPAND_END**

**Field_Sender_BIC_CD**

entityBIC= Settlement_Instruction.Account.Beneficiary_Bank_BIC_code

if(length of entityBIC=11) {
       return receiverBIC  = left(entityBIC,8) + "A" + right(entityBIC,3)
}else if (length of entityBIC=8){
      return receiverBIC =entityBIC+"AXXX"
}else {return exception}

**Field_Swift_Type:**

<details>
<summary>Expand Details</summary>

- Get Settlement_Instruction.Nostro_Swift_Message_Type, value can be 'MT103' or 'MT202'
- take the last 3 digital value '103' or '202' and return

</details>

**Original_Swift_Type **

<details>
<summary>Expand Details</summary>

1. NOTE: this is only for Withdrawal event
2. Get swift type from original swift message (Block 2)
3. the format will be 3 digital value, such as '103', '202'

</details>

**Original_Message_body**

**EXPAND: Click here to expand**

1. for cashflow withdrawal event
2. get the content in the block 4 of original message, sample as below (left side is the 292 sample, get the message body from original 202 message (right side)) ![image2024-2-19_11-57-10.png](attachments/image2024-2-19_11-57-10.png)

**EXPAND_END**

****Field_Receiver_BIC:****

<details>
<summary>Expand Details</summary>

entityBIC= Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code

If (entityFMID = '401036553' and Settlement_Instruction.Account.SCB_Nostro_Account_Type ='NOS' and Settlement_Instruction.Account.SCB_Nostro_Account_Number contains 'RTGS' and message_type in (MT103/MT202){
        return receiverBIC =SCBLEGCAXXXX
}else if (length of entityBIC=11) {
       return receiverBIC  = left(entityBIC,8) + "X" + right(entityBIC,3)
}else if (length of entityBIC=8){
      return receiverBIC =entityBIC+"XXXX"
}else {return exception}

</details>

**Field_Receiver_BIC_2****:**

<details>
<summary>Expand Details</summary>

entityBIC= Settlement_Instruction.Account.Beneficiary_Bank_BIC_code

if(length of entityBIC=11) {
       return receiverBIC  = left(entityBIC,8) + "X" + right(entityBIC,3)
}else if (length of entityBIC=8){
      return receiverBIC =entityBIC+"XXXX"
}else {return exception}

</details>

**Field_Receiver_BIC_PM**

<details>
<summary>Expand Details</summary>

~~entityBIC= Settlement_Instruction.Account.Beneficiary_Bank_BIC_code~~

entityBIC= Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code 
entityFMID=Entity.Booking_Entity_SCI_FMID

if (entityFMID in ('300036368','3','400451508','400452428','2', '**400906330**') and {**Field_Currency} **in ( XAU,XAG,XPD,XPT)){ //add AG FMID as required in ADO#9493232
        return receiverBIC =CHASGB2LXXXX
}else if (length of entityBIC=11) {
       return receiverBIC  = left(entityBIC,8) + "X" + right(entityBIC,3)
}else if (length of entityBIC=8){
      return receiverBIC =entityBIC+"XXXX"
}else {return exception}

</details>

**Field_121_REF: **Generate UUID and return. Length: <=36 for tag 121; <=16 for tag 108.

**Filed_Branch_Code**

- Get the booking entity FMID(Entity.Booking_Entity_SCI_FMID) from cashflow data
- Lookup the branch code from the static data table , get the 2 digital branch code and return

**Field_Cashflow_Id: **Get the cashflow id **Cashflow.Cashflow_Id** from cashflow data and return

**Field_Value_Date**

<details>
<summary>Expand Details</summary>

payment_date= Cashflow.Payment_Date
updated_date= Settlement_Instruction.Value_Date

if updated_date is not blank
    value_date = updated_date
else 
     value_date = payment_date

Format the value_date as YYMMDD(**no delimiter**) and return, the YY is the last 2 digital of original YYYY.

</details>

**Field_Event_Date
**

<details>
<summary>Expand Details</summary>

- Get Cashflow.Event_Date
- Format the date as YYMMDD(**no delimiter**) and return, the YY is the last 2 digital of original YYYY.

</details>

**Field_Currency:**

- Get the Cashflow.Payment_Currency from cashflow data and return
- Query the ISO currency from static data and return. mapping refer to // for non- ISO ccy?

**Field_Amount: **

- Get the Cashflow.Payment_Amount from cashflow data
- use "," to replace the "." in the amount value, such as 1. 100.56 return 100,56 2. 100.00 return 100,
- No rounding logic in day1

**Field_25_Account_Number
**

<details>
<summary>Expand Details</summary>

Correspondent_Account_Number = Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number //Nostro account number

if （{**Field_Currency}**='KRW' and Correspondent_Account_Number is not null){
    return :25:{Correspondent_Account_Number}
}else{
    return blank
**}**

</details>

**Field_26_Commodity_Identity**

**Elena: 2026-06-13 [Feature 13630360 [RATAN Setts] Update Precious metals Spot/Forward/Swap/Loan/SCF cashflows data and logic according to new DM](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13630360). Update this table by 'Yellow' part.**

2026-07-03  **Newest static data, pls find attached email.**
📎 [FW FMRP Commodities - Strategies Migration Signoff required.msg](attachments/FW FMRP Commodities - Strategies Migration Signoff required.msg)

<details>
<summary>Expand Details</summary>

** **

**EXPAND: UDF_Strategy**

| | **Murex & Tactical Stella Flow** | **FMRP9.0 Flow** |
| --- | --- | --- |
| Strategy | M_ALLOCATION | M_AVAIL_LOC | **Custodian_SCI_FMID** | **Delivery_Location** | **Comment(No Need this col in static data table)** |
| COM_BOE_DELIV | ALLOC | BOE | 10036317 | London | **15th June - Elena** MMs Attendees: Vivek / Carrie / Shyam / Elena 1. FMRP flow: **Strategy **replaced by **Custodian_SCI_FMID + Delivery_Location ~~+ Settlement_Method~~ **to get {M_AVAIL_LOC}/{M_ALLOCATION} 2. ~~Custodian_Name &~~ Custodian_SCI_FMID & Delivery_Location ~~& Settlement_Method~~ - **from Upstream - uber msg - Trade Level** 3. **Settlement Method: DVP / NET → DVP / NET_DVP** - **DVP → Gross Settle** - **NET_DVP → Bilateral Net Settle** 4. ~~**Use Intent_To_Allocate" : [ true ] to replace M_ALLOCATION**~~ - ~~true -> ALLOC~~ - ~~false / null -> blank~~ - **Elena 2026-08-14 M_ALLOCATION -> Re-use static data table instead of field: Intent_To_Allocate in uber msg.** 5. Ratan Settlement may still need to store Static data for fields {M_AVAIL_LOC} / {M_TYPE} / {M_QUALITY} 1. 2026-06-29 agreed again with @Ruiheng Cao @Arockia Dinesh @Vivek Aggarwal @Divya Prabhakar shyam 6. Sample msg to be provide. |
| COM_CHAS_LDN | | LONDON | 300011128 | London | e.g. 26C/**{M_AVAIL_LOC}**/{M_ALLOCATION}{M_TYPE}{M_QUALITY} {1:F01SCBLSG22AXXX0000000000}{2:I604CHASGB2LXXXXN}{3:{108:MxuzPbbsAMfOAVHk}}{4: :[26C:/**LONDON**/UNALLSILV9990](http://26C/LONDON/UNALLSILV9990) :30:240717 :20:DV19M00107419299 :21:DV19M00107419299 :23:TRANSFER :32F:GOZ0,1 :82A:SCBLSG22XXX :87A:SUPPRESSXXX :88A:SCBLGB2LTSY -} |
| COM_CHAS_ZRH | | ZURICH | 10042751 | Zurich | |
| COM_JMUK_DELIV | | JMUK | 400060476 | London | |
| COM_JMVF_DELIV | | JMVF | 400060476 | Valley Forge | |
| COM_RAND_DELIV | | RAND | 400108023 | Germiston | |
| COM_BDF_DELIV | ALLOC | PARIS | 400425608 | | |
| COM_BDF_DVP | ALLOC | PARIS | 400425608 | | |
| COM_LDN_DVP | | LONDON | 300011128 | London | |
| COM_BOE_DELIV_S | ALLOC | BOE | 10036317 | London | |
| COM_ZRH_DELIV_S | | ZURICH | 10042751 | Zurich | |
| COM_BDF_DELIV_S | ALLOC | PARIS | 400425608 | | |

**EXPAND_END**

**EXPAND: UDF_SWF_LS**

| M_ALLOCATION | M_AVAIL_LOC | M_CURR | M_PAPER_YN | M_QUALITY | M_TYPE | M_UNIT |
| --- | --- | --- | --- | --- | --- | --- |
| UNALL | LONDON | XAG | N | 9990 | SILV | GOZ |
| UNALL | LONDON | XAQ | Y | | GOLD | FOZ |
| UNALL | LONDON | XAU | N | 9950 | GOLD | FOZ |
| ALLOC | TBC | XD1 | N | 9995 | PALL | GOZ |
| ALLOC | TBC | XD2 | N | 9995 | PALL | GOZ |
| ALLOC | TBC | XD3 | Y | Palladium Warrants | PALL | GOZ |
| ALLOC | TBC | XG1 | N | 9990 | SILV | GOZ |
| ALLOC | TBC | XG2 | N | 9990 | SILV | GOZ |
| ALLOC | TBC | XG3 | N | 9990 | SILV | GOZ |
| ALLOC | TBC | XG5 | N | 9995 | SILV | GOZ |
| UNALL | LONDON | XGC | Y | | SILV | GOZ |
| UNALL | LONDON | XGD | Y | | SILV | GOZ |
| UNALL | ZURICH | XPD | N | 9995 | PALL | GOZ |
| UNALL | ZURICH | XPT | N | 9995 | PLAT | GOZ |
| ALLOC | TBC | XR1 | Y | 995 | RHOD | TOZ |
| UNALL | LONDON | XRH | Y | | RHOD | TOZ |
| UNALL | LONDON | XRU | Y | | RUTH | TOZ |
| ALLOC | TBC | XS5 | N | 9995 | GOLD | FOZ |
| ALLOC | TBC | XS9 | N | 9999 | GOLD | FOZ |
| UNALL | LONDON | XSD | Y | | GOLD | FOZ |
| ALLOC | TBC | XT1 | N | 9995 | PLAT | GOZ |
| ALLOC | TBC | XT2 | N | 9995 | PLAT | GOZ |
| ALLOC | TBC | XT3 | Y | Platinum Warrants | PLAT | GOZ |
| ALLOC | TBC | XU1 | N | 9999 | GOLD | FOZ |
| ALLOC | TBC | XU2 | N | 995 | GOLD | FOZ |
| ALLOC | TBC | XU3 | N | 995 | GOLD | FOZ |
| ALLOC | TBC | XU4 | N | 9999 | GOLD | FOZ |
| ALLOC | NEW YORK | XU5 | N | | GOLD | FOZ |
| ALLOC | TBC | XU6 | N | 999 | GOLD | FOZ |
| ALLOC | TBC | XU7 | N | 999 | GOLD | FOZ |
| ALLOC | TBC | XU8 | N | 995 | GOLD | FOZ |
| UNALL | LONDON | XUC | Y | | GOLD | FOZ |
| ALLOC | TBC | XGI | N | 9990 | SILV | GOZ |
| ALLOC | TBC | XG7 | N | 9990 | SILV | GOZ |

**EXPAND_END**

Strategy=Instrument_Common.Murex_Product_Strategy

**Custodian_SCI_FMID=tradeRecord.Entity.Custodian_SCI_FMID**

**Delivery_Location=tradeRecord.Delivery_Location**

if (**Custodian_SCI_FMID **is not blank){
**        **query "M_AVAIL_LOC", "M_ALLOCATION" from UDF_Strategy with Custodian_SCI_FMID and Delivery_Location

**   **} else if (Strategy is not blank){
        query "M_AVAIL_LOC", "M_ALLOCATION" from UDF_Strategy with Strategy

} Else{
        query "M_AVAIL_LOC","M_ALLOCATION" from UDF_SWF_LS withPayment_Currency
   }
    if (M_AVAIL_LOC is blank){
        query "M_AVAIL_LOC" from UDF_SWF_LS with Payment_Currency
    }
    if (M_ALLOCATION is blank){
        query "M_AVAIL_LOC" from UDF_SWF_LS with Payment_Currency
    }
    query "M_TYPE", "M_QUALITY" from UDF_SWF_LS with Payment_Currency
}

return :26C/{M_AVAIL_LOC}/{M_ALLOCATION}{M_TYPE}{M_QUALITY}

</details>

**Field_23_Identification
**

<details>
<summary>Expand Details</summary>

query "M_ALLOCATION" from UDF_SWF_LS with Currency

if (M_ALLOCATION='ALLOC'){
    return DELIVERY
}else {
    return TRANSFER    
}

</details>

**Field_26T**

<details>
<summary>Expand Details</summary>

If payment_currency = AED & Entity FMID=5 & Settlement means =NOS

return :26T:TOF

else no tag: 26T

[Story 9078297 [Tranche2] 26T in SWIFT for AED](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9078297)

</details>

**Field_32_Unit
**return "M_UNIT" got from UDF_SWF_LS with Currency

**Field_50_Ordering_Customer**

<details>
<summary>Expand Details</summary>

Ordering_Customer_Account=Settlement_Instruction.Account.Ordering_Customer_Account_Number
Ordering_Customer_Name=Settlement_Instruction.Account.Ordering_Customer_Account_Name
Ordering_Customer_Address=Settlement_Instruction.Account.Ordering_Customer_Street_Address
Ordering_Customer_Country=Settlement_Instruction.Account.Ordering_Customer_City

if (Ordering_Customer_Account is not blank and Ordering_Customer_Name is not blank and Ordering_Customer_Address is not blank and Ordering_Customer_Country is not blank ){
    if(length of Ordering_Customer_Name >35){
          return below text
           :50K:/{Ordering_Customer_Account} **-- this is line 1**
           {Ordering_Customer_Name} [1,35]**-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
          ** {Ordering_Customer_Name} [36,70] --**this is line 3
          ** {Ordering_Customer_Address}[1,35] --**discard the rest part if length >35
           **{Ordering_Customer_Country} --**this is line 5
      ** } else if (length of Ordering_Customer_Name <=35){
            return below text
           :50K:/{Ordering_Customer_Account} **-- this is line 1**
           {Ordering_Customer_Name}  **-- **** this is line 2  ****
          ** {Ordering_Customer_Address}[1,35] -- **split the value to 2 lines if length>35, [1,****35][36,70], discard the rest part if length >70
****    **       {Ordering_Customer_Address}[36,70]**
           **{Ordering_Customer_Country} --**this is line 4 or 5**
       }
} else {
    return blank
}

</details>

**Field_50/52_Customer**

<details>
<summary>Expand Details</summary>

Cient_Type=Entity.Counterparty_Client_Type
~~Beneficiary_BIC = Settlement_Instruction.Account.Beneficiary_BIC_code~~

Ordering_Customer_BIC = Settlement_Instruction.Account.Ordering_Customer_BIC_Code
Ordering_Customer_Name=Settlement_Instruction.Account.Ordering_Customer_Account_Name
Ordering_Customer_Address=Settlement_Instruction.Account.Ordering_Customer_Street_Address
Ordering_Customer_Country=Settlement_Instruction.Account.Ordering_Customer_City

if (Cient_Type in ('BANK','MULTDEV','INTEBCH','FININST','HDGEFND','INTLACC','INTECOM','INTDESK','FUNDMGR','CENTBK','OSEASBK')){ 
     if (Ordering_Customer_BIC is not null) {
         return below text
         :52A:{Ordering_Customer_BIC }
     } else {
         if ( Ordering_Customer_Name is not null or Ordering_Customer_Address is not null or  Ordering_Customer_Country is not null){
              if(length of Ordering_Customer_Name>35){
                    return below text
                   :52D:{Ordering_Customer_Name}[1,35] **-- split the value to 2 lines, [1,35][36,70], discard the rest part if length >70**
                   {Ordering_Customer_Name}[36,70] **-- this is line 2****
**                   {Ordering_Customer_Address}[1,35]--**this is line 3,-discard the rest part if length >35**
                   {Ordering_Customer_Country} ----**this is line 4**
              }else if (length of Ordering_Customer_Name<=35) {      
                    return below text
                   :52D:{Ordering_Customer_Name} **-- this is line 1
                 ** {Ordering_Customer_Address} [1,35]**-- split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
                  **{Ordering_Customer_Address}[36,70] 
                  {Ordering_Customer_Country} --**this is line 3 or 4****
**           }
       } else if ( Ordering_Customer_Name is ~~not~~ null and Ordering_Customer_Address is ~~not ~~null and Ordering_Customer_Country is ~~not ~~null){
                return Blank
       }
} else ~~if (Cient_Type in ('CORP','GOVTCOM','INCOMNB','INDIV','POSACC','PUBSECT','INVINST','GOVTOFF','UNKNOWN','BROKER','INTORG','CLGHSE','EXCHANG'))~~{
     if(length of Ordering_Customer_Name>35){
          return below text
          :50:{Ordering_Customer_Name}[1,35] **-- split the value to 2 lines, [1,35][36,70], discard the rest part if length >70**
         {Ordering_Customer_Name}[36,70] **-- this is line 2****
**         {Ordering_Customer_Address}[1,35]--**this is line 3,-discard the rest part if length >35**
         {Ordering_Customer_Country} ----**this is line 4**
     }else if (length of Ordering_Customer_Name<=35) {      
         return below text
          :50:{Ordering_Customer_Name} **-- this is line 1
        ** {Ordering_Customer_Address} [1,35]**-- split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
         **{Ordering_Customer_Address}[36,70] 
         {Ordering_Customer_Country} --**this is line 3 or 4
**     }
}

</details>

**Field_52_Ordering_Institution // for 202 Flip only & 202 CrossDebit**

<details>
<summary>Expand Details</summary>

Beneficiary_Account_Number =Settlement_Instruction.Account.Beneficiary_Account_Number~~
~~Beneficiary_BIC = Settlement_Instruction.Account.Beneficiary_BIC_code
Beneficiary_Account_Name = Settlement_Instruction.Account.Beneficiary_Account_Name + " "+ Settlement_Instruction.Account.Beneficiary_Account_Name_2 
Beneficiary_Address = Settlement_Instruction.Account.Beneficiary_Street_Address
Beneficiary_Country = Settlement_Instruction.Account.Beneficiary_City

Ordering_Customer_BIC = Settlement_Instruction.Account.Ordering_Customer_BIC_Code
Ordering_Customer_Name=Settlement_Instruction.Account.Ordering_Customer_Account_Name
Ordering_Customer_Address=Settlement_Instruction.Account.Ordering_Customer_Street_Address
Ordering_Customer_Country=Settlement_Instruction.Account.Ordering_Customer_City

~~if( Ordering_Customer_BIC is not blank and Beneficiary_Account_Number is not blank ){~~
~~      return below text~~
~~      :52A:/{Beneficiary_Account_Number } **-- this is line 1**~~
~~      {Ordering_Customer_BIC } **-- this is line 2
** } else if(Ordering_Customer_BIC is not blank and Beneficiary_Account_Number is blank  ){         ~~
~~      return below text~~
~~       :52A:{Ordering_Customer_BIC } **--this is line 1**~~
~~ } else if (Ordering_Customer_BIC is blank and Beneficiary_Account_Number is not blank and (Ordering_Customer_Name is not blank or Ordering_Customer_Address is not blank or Ordering_Customer_Country is not blank)){~~
~~     if(length of Ordering_Customer_Name>35){~~
~~          return below text~~
~~          :52D:/{Beneficiary_Account_Number} **-- this is line 1**~~
~~         {Ordering_Customer_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Ordering_Customer_Name}[36,70]--**this is line 3**~~
~~         {Ordering_Customer_Address} --**discard the rest part if length >35**~~
~~         {Ordering_Customer_Country} --**this is line 5**~~
~~     }else if (length of Ordering_Customer_Name <=35)       ~~
~~         return below text~~
~~          :52D:/{Beneficiary_Account_Number } **-- this is line 1
        ** {Ordering_Customer_Name} **-- this is line 2
         **{Ordering_Customer_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {Ordering_Customer_Address}[36,70] ~~
~~         {Ordering_Customer_Country} --**this is line 4 or 5
**     }~~
~~}else~~ if ( Beneficiary_BIC is not blank and Beneficiary_Account_Number is not blank ){
      return below text
      :52A:/{Beneficiary_Account_Number } **-- this is line 1**
      {Beneficiary_BIC } **-- this is line 2
** } else if(Beneficiary_BIC is not blank and Beneficiary_Account_Number is blank  ){         
      return below text
       :52A:{Beneficiary_BIC} **--this is line 1**
 } else if (Beneficiary_BIC is blank and ~~Beneficiary_Account_Number is not blank and~~ (Beneficiary_Account_Name is not blank or Beneficiary_Address is not blank or Beneficiary_Country is not blank)){
     if(length of Beneficiary_Account_Name >35){
          return below text
          :52D:/{Beneficiary_Account_Number} **-- this is line 1**
         {Beneficiary_Account_Name }[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Beneficiary_Account_Name }[36,70]--**this is line 3**
         {Beneficiary_Address } --**discard the rest part if length >35**
         {Beneficiary_Country } --**this is line 5**
     }else if (length of Beneficiary_Account_Name <=35)      
         return below text
          :52D:/{Beneficiary_Account_Number } **-- this is line 1
        ** {Beneficiary_Account_Name } **-- this is line 2
         **{Beneficiary_Address }[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {Beneficiary_Address }[36,70] 
         {Beneficiary_Country } --**this is line 4 or 5
**     }
} else {
    return blank
}

</details>

**Field_52_Ordering Institution_202
**

<details>
<summary>Expand Details</summary>

Ordering_Customer_BIC = Settlement_Instruction.Account.Ordering_Customer_BIC_Code
if Ordering_Customer_BIC is not blank {
    return :52A:Ordering_Customer_BIC  }
else {
    return blank}

</details>

**Field_53_Beneficiary //For 202 Flip Only & 202Cross Debit
**

<details>
<summary>Expand Details</summary>

Beneficiary_Account_Number =Settlement_Instruction.Account.Beneficiary_Account_Number
if (Beneficiary_Account_Number is not blank ){
         return below text
         :53B:/{Beneficiary_Account_Number} **-- this is line 1**
}else {
         return blank
}

</details>

**Field_53_Sender_Correspondent**

<details>
<summary>Expand Details</summary>

**EXPAND: 53/58 BIC Mapping**

| **FMID** | **Name** | **Currency** | **53 BIC (Rule1)** | **58 BIC (Rule2)** |
| --- | --- | --- | --- | --- |
| 400054741 | SCB CHENGDU*CGD | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400095464 | SCB CHINA DALIAN*DLN | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400130178 | SCB CHINA HOHHOT*HHH | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400130180 | SCB CHINA NINGBO*NGB | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400001378 | SCB CHINA*BJG | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400090093 | SCB CHINA*NCG | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 10020899 | SCB CHINA*NJG | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 10032025 | SCB CHINA*SZN | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 235003861 | SCB CHINA*TIA | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 10062461 | SCB CHINA*XMN | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 10078716 | SCB CHINA*ZHU | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400220273 | SCB CN CHANGSHA*CGS | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400899993 | SCB CN CHO*CHO | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400075752 | SCB CN CHONGQING*CQG | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400209000 | SCB CN FOSHAN*FOS | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400229749 | SCB CN FUZHOU*FZH | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400085753 | SCB CN HANGZHOU*HNZ | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400683682 | SCB CN HRB*HRB | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400218197 | SCB CN JINAN BR*JNA | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400667486 | SCB CN KMG*KMG | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400798477 | SCB CN SYG*SYG | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400185419 | SCB CN WUHAN*WUH | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400054708 | SCB GUANGZHOU*GZU | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400057714 | SCB QINGDAO*QDO | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400677737 | SCB SHA FTU*FT2 | CNY | SCBLCNSXFTU | SCBLCNSXGMO |
| 10036642 | SCB SHANGH*SHA | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400054737 | SCB SUZHOU*SUZ | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 400193370 | SCBLXIAN*XIN | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| 300036368 | ACU SING | SGD | SCBLSG22GMO | SCBLSG22GMO |
| 3 | DBU SING | SGD | SCBLSG22GMO | SCBLSG22GMO |
| 400451508 | SCB SG LTD*SIN | SGD | SCBLSG22GMO | SCBLSG22GMO |
| 400452428 | SCB SG LTDACU*SIN | SGD | SCBLSG22GMO | SCBLSG22GMO |
| 400093619 | STANCHART SAADIQ*KUL | MYR | SCBLMYKXGMO | SCBLMYKXGMO |
| 9 | SCB KL*KUL | MYR | SCBLMYKXGMO | SCBLMYKXGMO |
| 4 | SCB BOMBAY*MMB | INR | SCBLINBBXXX | SCBLINBBXXX |
| 400960089 | GIFT CITY TM*MUM | INR | SCBLINAAXXX | SCBLINAAXXX |
| 10075222 | SCB LONDON*LDN | GBP | SCBLGB2LTSY | SCBLGB2LTSY |
| 6 | BANGKOK | THB | SCBLTHBXGMO | SCBLTHBXGMO |
| 2 | HONGKONG | HKD | SCBLHKHHTRY | SCBLHKHHTRY |
| 300075472 | SCS HK | HKD | SCBLHKHHTRY | SCBLHKHHTRY |
| 10038345 | TAIPEI | TWD | SCBLTWTPXXX | SCBLTWTPXXX |
| 300011345 | OBU TAIPEI | TWD | SCBLTWTPXXX | SCBLTWTPXXX |
| 8 | Indonesia | MUR | SCBLIDJXGMO | SCBLIDJXGMO |
| 400077978 | Philippines | AED | SCBLPHMMXXX | SCBLPHMMXXX |
| 10036428 | MANILA | IDR | SCBLPHMMXXX | SCBLPHMMXXX |
| 400018439 | Mauritius | PHP | SCBLMUMUXXX | SCBLMUMUXXX |
| 10036382 | Japan | USD | SCBLJPJTXXX | SCBLJPJTXXX |
| 5 | Dubai | JPY | SCBLAEADGMO | SCBLAEADGMO |
| 7 | New York | ZAR | SCBLUS33XXX | SCBLUS33XXX |
| 400032489 | Johannesburg | AED | SCBLZAJJXXX | SCBLZAJJXXX |
| 400045551 | DIFC | PHP | SCBLAEADDIF | SCBLAEADDIF |
| | | | | |

**EXPAND_END**

Settlement_Means = Settlement_Instruction.Account.SCB_Nostro_Account_Type

If (entityFMID = '401036553' and Settlement_Instruction.Account.SCB_Nostro_Account_Type ='NOS' and Settlement_Instruction.Account.SCB_Nostro_Account_Number contains 'RTGS' and message_type in (MT103/MT202/MT192/MT292){
        Correspondent_Account_Number =Settlement_Instruction.Account.EBBS_Account_Number
}else Correspondent_Account_Number = Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number

If ((Settlement_Means ='Over-Account' and Swift msg type in (MT103,MT202))
or ((Settlement_Means ='NOS' and Swift msg type in (MT202/MT202COV/MT103) and **{Field_Currency}** is local ccy)))  {
    Correspondent_BIC = query from above static with fmid
} else 
    Correspondent_BIC = Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code
}

If (entityFMID='10041530' and Settlement_Instruction.Account.SCB_Nostro_Account_Number ='VNO SBV' and Swift msg type in (MT103,MT202)){
    Correspondent_BIC ='STBVVNVXXXX' // required in 15865347
}

if( Correspondent_Account_Number is not blank and Correspondent_BIC is not blank){
    return below text
    :53A:/{Correspondent_Account_Number } **-- this is line 1**
    {Correspondent_BIC} **-- this is line 2**
} else if (Correspondent_Account_Number is blank and Correspondent_BIC is not blank ){
    return below text
     :53A:{Correspondent_BIC} **--this is line 1
**} else {
    return blank
}

</details>

**Field_53_Sender_Correspondent_103COV
**

<details>
<summary>Expand Details</summary>

Correspondent_Account_Number = Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number
Correspondent_BIC = Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code**
**

if( Correspondent_Account_Number is not blank and Correspondent_BIC is not blank){
    return below text
    :53A:/{Correspondent_Account_Number } -- **this is line 1**
    {Correspondent_BIC} -- **this is line 2**
} else if (Correspondent_Account_Number is blank and Correspondent_BIC is not blank ){
    return below text
     :53A:{Correspondent_BIC} **--this is line 1**
} else {
    return blank
}

</details>

**Field_54_Receiver_Correspondent
**

<details>
<summary>Expand Details</summary>

Rec_Correspondent_Account_Number = Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number
Rec_Correspondent_BIC = Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code
Stamped_Settlement_Method=Settlement_Instruction.Settlement_Method
Stamped_SSI_Id=Settlement_Instruction.SSI_Id

if( Rec_Correspondent_Account_Number is not blank ){
      if (**{Field_Currency}**** **== USD){
            if (Stamped_Settlement_Method == 'FEDWIRE  && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with //FW, /FW, FW) {
                        Rec_Correspondent_Account_Number = remove the //FW, /FW, FW of the value
                 }
                 Rec_Correspondent_Account_Number =//FW{Rec_Correspondent_Account_Number }
            }else if ((~~Stamped_Settlement_Method != 'FEDWIRE'~~ && Rec_Correspondent_Account_Number starts with 'FW') {
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number }
            }else{
                 Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
            }
      }else if (**{Field_Currency}**** **== GBP){
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with //SC, /SC, SC) {
                        Rec_Correspondent_Account_Number = remove the //SC, /SC, SC of the value
                 }
                 Rec_Correspondent_Account_Number =//SC{Rec_Correspondent_Account_Number }**
**            }else if (Stamped_SSI_Id is null && Rec_Correspondent_Account_Number starts with 'SC')
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number } 
           }else{
                 Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
            }
     }else if (**{Field_Currency}**** **== EUR){
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with //RT, /RT, RT) {
                        Rec_Correspondent_Account_Number = remove the //RT, /RT, RT of the value
                 }
                  Rec_Correspondent_Account_Number =//RT{Rec_Correspondent_Account_Number } **
**            }else if (Stamped_SSI_Id is null && Rec_Correspondent_Account_Number starts with 'RT') {
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number} 
           }else{
                 Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
            }
**   ** }if (**{Field_Currency}**** **== INR){ *//requested in ADO#9971484*
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with // or /) {
                        Rec_Correspondent_Account_Number = remove the // or / of the value
                 }
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number }**
**            }else{
                 Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
            }
     }else{
           Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
   }
}

if( Rec_Correspondent_Account_Number is not blank and Rec_Correspondent_BIC is not blank){
    if (Rec_Correspondent_Account_Number is not blank ) {  
         if (Rec_Correspondent_Account_Number starts with "//FW"){
              return below text
              :54D:{Rec_Correspondent_Account_Number } -- **this is line 1**
              {Rec_Correspondent_BIC } --** this is line 2**
**   **   }else{return below text
             :54A:{Rec_Correspondent_Account_Number } **-- this is line 1**
            {Rec_Correspondent_BIC } **-- this is line 2
**     }
} else if (Rec_Correspondent_Account_Number is blank and Rec_Correspondent_BIC is not blank ){
    return below text
    :54A:{Rec_Correspondent_BIC } **--this is line 1
**} else {
    return blank
}

</details>

**Field_56_Intermediary_Institution
**

<details>
<summary>Expand Details</summary>

Intermediary_BIC=Settlement_Instruction.Account.Intermediary_BIC_code
Intermediary_Account_Number=Settlement_Instruction.Account.Intermediary_Account_Number    
Intermediary_Name=Settlement_Instruction.Account.Intermediary_Account_Name
Intermediary_Address=Settlement_Instruction.Account.Intermediary_Street_Address
Intermediary_City=Settlement_Instruction.Account.Intermediary_City
Stamped_Settlement_Method=Settlement_Instruction.Settlement_Method
Stamped_SSI_Id=Settlement_Instruction.SSI_Id

if( Intermediary_Account_Number is not blank ){
      if (**{Field_Currency}**** **== USD){
            if (Stamped_Settlement_Method == 'FEDWIRE' && **Settlement_Instruction.Swift_Routing_Code_Block==56**){
                 if (Intermediary_Account_Number starts with //FW, /FW, FW) {
                        Intermediary_Account_Number = remove the //FW, /FW, FW of the value
                 }
                 Intermediary_Account_Number =//FW{Intermediary_Account_Number}
            }else if (**~~Stamped_Settlement_Method != 'FEDWIRE' &&~~ Intermediary_Account_Number starts with 'FW') {**
                 Intermediary_Account_Number=//{Intermediary_Account_Number}
            }else{
                 Intermediary_Account_Number=/{Intermediary_Account_Number}
            }
      }else if (**{Field_Currency}**** **== GBP){
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==56**){
                 if (Intermediary_Account_Number starts with //SC, /SC, SC) {
                        Intermediary_Account_Number = remove the //SC, /SC, SC of the value
                 }
                 Intermediary_Account_Number =//SC{Intermediary_Account_Number}**
**            }else if (**Stamped_SSI_Id is null && **Intermediary_Account_Number starts with 'SC')
                 Intermediary_Account_Number =//{Intermediary_Account_Number} 
           }else{
                 Intermediary_Account_Number=/{Intermediary_Account_Number}
            }
     }else if (**{Field_Currency}**** **== EUR){
            if (Stamped_SSI_Id is not null **Settlement_Instruction.Swift_Routing_Code_Block==56**){
                 if (Intermediary_Account_Number starts with //RT, /RT, RT) {
                        Intermediary_Account_Number = remove the //RT, /RT, RT of the value
                 }
                  Intermediary_Account_Number=//RT{Intermediary_Account_Number} **
**            }else if (**Stamped_SSI_Id is null && **Intermediary_Account_Number starts with 'RT') {
                 Intermediary_Account_Number =//{Intermediary_Account_Number} 
           }else{
                 Intermediary_Account_Number=/{Intermediary_Account_Number}
            }
**   ** }if (**{Field_Currency}**** **== INR){ *//requested in ADO#9971484*
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==56**){
                 if (Intermediary_Account_Number starts with // or /) {
                        Intermediary_Account_Number = remove the // or / of the value
                 }
                 Intermediary_Account_Number =//{Intermediary_Account_Number }**
**            }else{
                 Intermediary_Account_Number =/{Intermediary_Account_Number }
            }
     }else{
           Intermediary_Account_Number=/{Intermediary_Account_Number}
   }
}

if( Intermediary_BIC is not blank){
    if (Intermediary_Account_Number is not blank ) {  
         if (Intermediary_Account_Number starts with "//FW"){
              return below text
              :56D:{Intermediary_Account_Number} -- **this is line 1**
              {Intermediary_BIC} --** this is line 2**
**   **   }else{
              return below text
              :56A:{Intermediary_Account_Number}  **-- this is line 1**
             {Intermediary_BIC} **-- this is line 2
**    } else {         
       return below text
       :56A:{Intermediary_BIC} **--this is line 1
**    }
} else {
    if (Intermediary_Account_Number is blank and Intermediary_Name is blank and Intermediary_Address is blank and Intermediary_City is blank) {
        return blank
} else {
     if(length of Intermediary_Name >35){ 
          return below text
          :56D:{Intermediary_Account_Number} **-- this is line 1**
         {Intermediary_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Intermediary_Name}[36,70]--**this is line 3**
         {Intermediary_Address} --**discard the rest part if length >35**
         {Intermediary_City} --**this is line 5**
     }else if (length of Intermediary_Name<=35){
         if (length of Intermediary_Address>35) {     
             return below text
              :56D:{Intermediary_Account_Number}**-- this is line 1
        **     {Intermediary_Name} **-- this is line 2
             **{Intermediary_Address}[1,35] **--split the value to 2 lines, [1,35][36,70], discard the rest part if length >70
**             {Intermediary_Address}[36,70] --**this is line 4**
             {Intermediary_City} --**this is line 5
**         }else if (length of Intermediary_Address<=35){
             return below text
              :56D:{Intermediary_Account_Number}**-- this is line 1
        **     {Intermediary_Name} **-- this is line 2
             **{Intermediary_Address} **-- this is line 3
**             {Intermediary_City} --**this is line 4**
        }
    }
}

</details>

**Field_56_Account_BIC //for MT210
**

<details>
<summary>Expand Details</summary>

beneficiary_Correspondent_BIC=settlement_Instruction.account.beneficiary_Correspondent_BIC_code //54BIC
Intermediary_BIC=Settlement_Instruction.Account.Intermediary_BIC_code //56BIC
beneficiary_Bank_BIC=settlement_Instruction.account.beneficiary_Bank_BIC_code //57BIC

if (beneficiary_Correspondent_BIC is not null){
      return :56A:{beneficiary_Correspondent_BIC}
} else if (Intermediary_BIC is not null){
      return :56A:{Intermediary_BIC}
}else if (beneficiary_Bank_BIC is not null) {
      return :56A:{beneficiary_Bank_BIC}
}else{
      return blank
}

</details>

**Field_57_Account_Institution**

<details>
<summary>Expand Details</summary>

Institution_Account_Number=Settlement_Instruction.Account.Beneficiary_Bank_Account_Number
Institution_BIC=Settlement_Instruction.Account.Beneficiary_Bank_BIC_code
Stamped_Settlement_Method=Settlement_Instruction.Settlement_Method
Stamped_SSI_Id=Settlement_Instruction.SSI_Id

if( Institution_Account_Number is not blank ){
      if (**{Field_Currency}**** **== USD){
            if (Stamped_Settlement_Method == 'FEDWIRE' && **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with //FW, /FW, FW) {
                        Institution_Account_Number = remove the //FW, /FW, FW of the value
                 }
                 Institution_Account_Number=//FW{Institution_Account_Number}
            }else if (~~**Stamped_Settlement_Method != 'FEDWIRE'** **&& **~~Institution_Account_Number starts with 'FW') {
                 Institution_Account_Number=//{Institution_Account_Number}
            }else{
                 Institution_Account_Number=/{Institution_Account_Number}
            }
      }else if (**{Field_Currency}**** **== GBP){
            if (Stamped_SSI_Id is not null **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with //SC, /SC, SC) {
                        Institution_Account_Number = remove the //SC, /SC, SC of the value
                 }
                 Institution_Account_Number=//SC{Institution_Account_Number}**
**            }else if (**Stamped_SSI_Id is null &&** Institution_Account_Number starts with 'SC')
                 Institution_Account_Number=//{Institution_Account_Number} 
           }else{
                 Institution_Account_Number=/{Institution_Account_Number}
            }
     }else if (**{Field_Currency}**** **== EUR){
            if (Stamped_SSI_Id is not null **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with //RT, /RT, RT) {
                        Institution_Account_Number = remove the //RT, /RT, RT of the value
                 }
                  Institution_Account_Number=//RT{Institution_Account_Number} **
**            }else if (**Stamped_SSI_Id is null && **Institution_Account_Number starts with 'RT') {
                 Institution_Account_Number=//{Institution_Account_Number} 
           }else{
                 Institution_Account_Number=/{Institution_Account_Number}
            }
**   ** }if (**{Field_Currency}**** **== INR){ *//requested in ADO#9971484*
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with // or /) {
                        Institution_Account_Number = remove the // or / of the value
                 }
                 Institution_Account_Number =//{Institution_Account_Number }**
**            }else{
                 Institution_Account_Number =/{Institution_Account_Number }
            }
     }else{
           Institution_Account_Number=/{Institution_Account_Number}
   }
}

if (Institution_Account_Number is not blank and Institution_BIC is not blank ) {
     if (Institution_Account_Number starts with "//FW"){
              return below text
              :57D:{Institution_Account_Number} -- **this is line 1**
              {Institution_BIC} --** this is line 2**
**   **   }else{
              return below text
              :57A:{Institution_Account_Number }**--this is line 1**
              {Institution_BIC}    **– this is line 2
**     }
} else if (Institution_Account_Number is blank and Institution_BIC is not blank){
     return below text
     :57A:{Institution_BIC}**--this is line 1
**}

</details>

**Field_57_Account_Institution_2**

<details>
<summary>Expand Details</summary>

Institution_Account_Number=Settlement_Instruction.Account.Beneficiary_Bank_Account_Number
Institution_BIC=Settlement_Instruction.Account.Beneficiary_Bank_BIC_code
Institution_Account_Name=Settlement_Instruction.Account.Beneficiary_Bank_Account_Name
Institution_Address=Settlement_Instruction.Account.Beneficiary_Bank_Street_Address
Institution_City=Settlement_Instruction.Account.Beneficiary_Bank_City
Stamped_Settlement_Method=Settlement_Instruction.Settlement_Method
Stamped_SSI_Id=Settlement_Instruction.SSI_Id

if( Institution_Account_Number is not blank ){
      if (**{Field_Currency}**** **== USD){
            if (Stamped_Settlement_Method == 'FEDWIRE' && **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with //FW, /FW, FW) {
                        Institution_Account_Number = remove the //FW, /FW, FW of the value
                 }
                 Institution_Account_Number=//FW{Institution_Account_Number}
            }else if (~~**Stamped_Settlement_Method != 'FEDWIRE'** **&&**~~Institution_Account_Number starts with 'FW') {
                 Institution_Account_Number=//{Institution_Account_Number}
            }else{
                Institution_Account_Number=/{Institution_Account_Number}
            }
      }else if (**{Field_Currency}**** **== GBP){
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with //SC, /SC, SC) {
                        Institution_Account_Number = remove the //SC, /SC, SC of the value
                 }
                 Institution_Account_Number=//SC{Institution_Account_Number}**
**            }else if ( **Stamped_SSI_Id is null &&** institution_Account_Number starts with 'SC')
                 Institution_Account_Number=//{Institution_Account_Number} 
           }else{
                 Institution_Account_Number=/{Institution_Account_Number}
          }
    }else if (**{Field_Currency}**** **== EUR **Settlement_Instruction.Swift_Routing_Code_Block==57**){
            if (Stamped_SSI_Id is not null){
                 if (Institution_Account_Number starts with //RT, /RT, RT) {
                        Institution_Account_Number = remove the //RT, /RT, RT of the value
                 }
                  Institution_Account_Number=//RT{Institution_Account_Number} **
**            }else if (**Stamped_SSI_Id is null && **Institution_Account_Number starts with 'RT') {
                 Institution_Account_Number=//{Institution_Account_Number} 
            }else{
                 Institution_Account_Number=/{Institution_Account_Number}
           }
**   ** }if (**{Field_Currency}**** **== INR){ *//requested in ADO#9971484*
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==57**){
                 if (Institution_Account_Number starts with // or /) {
                        Institution_Account_Number = remove the // or / of the value
                 }
                 Institution_Account_Number =//{Institution_Account_Number }**
**            }else{
                 Institution_Account_Number =/{Institution_Account_Number }
            }
     }else{
           Institution_Account_Number=/{Institution_Account_Number}
   }
}

if( Institution_BIC is not blank and Institution_Account_Number is not blank ){
     if (Institution_Account_Number starts with "//FW"){
              return below text
              :57D:{Institution_Account_Number} -- **this is line 1**
              {Institution_BIC} --** this is line 2**
**   **   }else{
             return below text
              :57A:{Institution_Account_Number} -- **this is line 1**
              {Institution_BIC} -- **this is line 2****
      **}**
** } else if(Institution_BIC is not blank and Institution_Account_Number is blank  ){         
      return below text
      :57A:{Institution_BIC} **--this is line 1**
 } else if (Institution_BIC is blank and (Institution_Account_Number is not blank or Institution_Account_Name is not blank or Institution_Address is not blank or Institution_City is not blank)){
     if(length of Institution_Account_Name >35){
          return below text
         :57D:{Institution_Account_Number} **-- this is line 1**
         {Institution_Account_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Institution_Account_Name}[36,70]--**this is line 3**
         {Institution_Address} --**discard the rest part if length >35**
         {Institution_City} --**this is line 5**
     }else if (length of Institution_Account_Name<=35)      
         return below text
         :57D:{Institution_Account_Number} **-- this is line 1
        ** {Institution_Account_Name} **-- this is line 2
         **{Institution_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {Institution_Address}[36,70] 
         {Institution_City} --**this is line 4 or 5
**     }
}else {
    return blank
}

</details>

**Field_57_Receiver_Correspondent
**

<details>
<summary>Expand Details</summary>

Rec_Correspondent_Account_Number = Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number
Rec_Correspondent_BIC = Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code
Rec_Correspondent_Account_Name = Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name
Rec_Correspondent_Address = Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address
Rec_Correspondent_City = Settlement_Instruction.Account.Beneficiary_Correspondent_City
Stamped_Settlement_Method=Settlement_Instruction.Settlement_Method
Stamped_SSI_Id=Settlement_Instruction.SSI_Id

if( Rec_Correspondent_Account_Number is not blank ){
      if (**{Field_Currency}**** **== USD){
            if (Stamped_Settlement_Method == 'FEDWIRE' && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with //FW, /FW, FW) {
                        Rec_Correspondent_Account_Number = remove the //FW, /FW, FW of the value
                 }
                 Rec_Correspondent_Account_Number =//FW{Rec_Correspondent_Account_Number }
            }else if (~~**Stamped_Settlement_Method != 'FEDWIRE' &&**~~ Rec_Correspondent_Account_Number starts with 'FW') {
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number }
            }else{
                Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number }
           }
      }else if (**{Field_Currency}**** **== GBP){
            if (Stamped_SSI_Id is not null &&  **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with //SC, /SC, SC) {
                        Rec_Correspondent_Account_Number = remove the //SC, /SC, SC of the value
                 }
                 Rec_Correspondent_Account_Number =//SC{Rec_Correspondent_Account_Number }**
**            }else if (**Stamped_SSI_Id is null &&** Rec_Correspondent_Account_Number starts with 'SC')
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number } 
           }else{
                Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number }
           }
     }else if (**{Field_Currency}**** **== EUR){
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with //RT, /RT, RT) {
                        Rec_Correspondent_Account_Number = remove the //RT, /RT, RT of the value
                 }
                  Rec_Correspondent_Account_Number =//RT{Rec_Correspondent_Account_Number } **
**            }else if (**Stamped_SSI_Id is null &&** Rec_Correspondent_Account_Number starts with 'RT') {
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number} 
           }else{
                Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number }
           }
**   ** }if (**{Field_Currency}**** **== INR){ *//requested in ADO#9971484*
            if (Stamped_SSI_Id is not null && **Settlement_Instruction.Swift_Routing_Code_Block==54**){
                 if (Rec_Correspondent_Account_Number starts with // or /) {
                        Rec_Correspondent_Account_Number = remove the // or / of the value
                 }
                 Rec_Correspondent_Account_Number =//{Rec_Correspondent_Account_Number }**
**            }else{
                 Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
            }
     }else{
           Rec_Correspondent_Account_Number =/{Rec_Correspondent_Account_Number}
   }
}

if( Rec_Correspondent_BIC is not blank and Rec_Correspondent_Account_Number is not blank ){
      if (Institution_Account_Number starts with "//FW"){
              return below text
              :57D:{Institution_Account_Number} -- **this is line 1**
              {Institution_BIC} --** this is line 2**
**   **   }else{
              return below text
              :57A:{Rec_Correspondent_Account_Number } **-- this is line 1**
              {Rec_Correspondent_BIC } **-- this is line 2
     ** }**
** } else if(Rec_Correspondent_BIC is not blank and Rec_Correspondent_Account_Number is blank  ){         
      return below text
      :57A:{Rec_Correspondent_BIC } **--this is line 1**
 } else if (Rec_Correspondent_BIC is blank and Rec_Correspondent_Account_Number is not blank and Rec_Correspondent_Account_Name is not blank and Rec_Correspondent_Address is not blank and Rec_Correspondent_City is not blank){
     if(length of Rec_Correspondent_Account_Name >35){
          return below text
          :57D:/{Rec_Correspondent_Account_Number } **-- this is line 1**
         {Rec_Correspondent_Account_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Rec_Correspondent_Account_Name}[36,70]--**this is line 3**
         {Rec_Correspondent_Address} --**discard the rest part if length >35**
         {Rec_Correspondent_City} --**this is line 5**
     }else if (length of Rec_Correspondent_Account_Name <=35)      
         return below text
          :57D:/{Rec_Correspondent_Account_Number } **-- this is line 1
         {Rec_Correspondent_Account_Name} **-- this is line 2****
         ****{Rec_Correspondent_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {Rec_Correspondent_Address}[36,70] 
         {Rec_Correspondent_City} --**this is line 4 or 5
**     }
}else {
    return blank
}

</details>

**Field_57_Sender_Correspondent**

<details>
<summary>Expand Details</summary>

Correspondent_BIC = Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code

if( Correspondent_BIC is not blank){
    return below text
    :57A:{Correspondent_BIC}
 else {
    return blank
}

</details>

**Field_58_Benificiary
**

<details>
<summary>Expand Details</summary>

benificiary_BIC=Settlement_Instruction.Account.Beneficiary_BIC_code
benificiary_Account_Number=Settlement_Instruction.Account.Beneficiary_Account_Number       
benificiary_Name=Settlement_Instruction.Account.Beneficiary_Account_Name  
benificiary_Name_2=Settlement_Instruction.Account.Beneficiary_Account_Name_2  
benificiary_Address=Settlement_Instruction.Account.Beneficiary_Street_Address
benificiary_City=Settlement_Instruction.Account.Beneficiary_City

if( benificiary_BIC is not blank and benificiary_Account_Number is not blank ){
      return below text
      :58A:/{benificiary_Account_Number} **-- this is line 1**
      {benificiary_BIC} **-- this is line 2
** } else if(benificiary_BIC is not blank and benificiary_Account_Number is blank  ){         
      return below text
      :58A:{benificiary_BIC} **--this is line 1**
 } else if (benificiary_BIC is blank and benificiary_Account_Number is not blank and benificiary_Name is not blank and benificiary_Address is not blank and benificiary_City is not blank){
     if(benificiary_Name_2 is not blank){
          return below text
          :58D:/{benificiary_Account_Number} **-- this is line 1**
         {benificiary_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {benificiary_Name_2}[1,35]--**this is line 3**
         {benificiary_Address} --**discard the rest part if length >35**
         {benificiary_City} --**this is line 5**
     }else if (length of benificiary_Name_2 is blank)      
         return below text
          :58D:/{benificiary_Account_Number} **-- this is line 1
        ** {benificiary_Name} **-- this is line 2
         **{benificiary_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {benificiary_Address}[36,70] 
         {benificiary_City} --**this is line 4 or 5
**     }
}else {
    return blank
}

</details>

**Field_58_Account_Institution**

<details>
<summary>Expand Details</summary>

Institution_Account_Number=Settlement_Instruction.Account.Beneficiary_Bank_Account_Number
Institution_BIC=Settlement_Instruction.Account.Beneficiary_Bank_BIC_code
Institution_Account_Name=Settlement_Instruction.Account.Beneficiary_Bank_Account_Name
Institution_Address=Settlement_Instruction.Account.Beneficiary_Bank_Street_Address
Institution_City=Settlement_Instruction.Account.Beneficiary_Bank_City

if( Institution_BIC is not blank and Institution_Account_Number is not blank ){
      return below text
      :58A:/{Institution_Account_Number} **-- this is line 1**
      {Institution_BIC} **-- this is line 2
** } else if(Institution_BIC is not blank and Institution_Account_Number is blank  ){         
      return below text
      :58A:{Institution_BIC} **--this is line 1**
 } else if (Institution_BICis blank and Institution_Account_Number is not blank and Institution_Account_Name is not blank and Institution_Address is not blank and Institution_City is not blank){
     if(length of Institution_Account_Name >35){
          return below text
          :58D:/{Institution_Account_Number} **-- this is line 1**
         {Institution_Account_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Institution_Account_Name}[36,70]--**this is line 3**
         {Institution_Address} --**discard the rest part if length >35**
         {Institution_City} --**this is line 5**
     }else if (length of Institution_Account_Name<=35)      
         return below text
          :58D:/{Institution_Account_Number} **-- this is line 1
        ** {Institution_Account_Name} **-- this is line 2
         **{Institution_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {Institution_Address}[36,70] 
         {Institution_City} --**this is line 4 or 5
**     }
}else {
    return blank
}

</details>

**Field_58_Sender_Correspondent
**

<details>
<summary>Expand Details</summary>

correspondent_Account_Number = Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number
correspondent_Account_Name = Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name
correspondent_Address = Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address
correspondent_Country = Settlement_Instruction.Account.Booking_Entity_Correspondent_City 
correspondent_BIC = query from static data table the same as Field_53_Sender_Correspondent with entity fmid

if( correspondent_BIC is not blank and correspondent_Account_Number is not blank ){
      return below text
      :58A:/{correspondent_Account_Number } **-- this is line 1**
      {correspondent_BIC } **-- this is line 2
** } else if(correspondent_BIC is not blank and correspondent_Account_Number is blank  ){         
      return below text
      :58A:{correspondent_BIC } **--this is line 1**
 } ~~else if (correspondent_BIC is blank and correspondent_Account_Number is not blank and correspondent_Account_Name is not blank and correspondent_Address is not blank and correspondent_Country is not blank){~~
~~     if(length of correspondent_Account_Name>35){~~
~~          return below text~~
~~          :58D:/{correspondent_Account_Number } **-- this is line 1**~~
~~         {correspondent_Account_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {correspondent_Account_Name}[36,70]--**this is line 3**~~
~~         {correspondent_Address} --**discard the rest part if length >35**~~
~~         {correspondent_Country} --**this is line 5**~~
~~     }else if (length of correspondent_Account_Name<=35)       ~~
~~         return below text~~
~~          :58D:/{correspondent_Account_Number } **-- this is line 1
        ** {correspondent_Account_Name} **-- this is line 2
         **{correspondent_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {correspondent_Address}[36,70] ~~
~~         {correspondent_Country} --**this is line 4 or 5
**     }~~
}else {
    return blank
}

</details>

**Field_58_Sender_Correspondent_CD
**

<details>
<summary>Expand Details</summary>

correspondent_Account_Number = Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number
correspondent_BIC = query from static data table defined in {**Field_Sender_BIC**} with entity fmid

if( correspondent_BIC is not blank and correspondent_Account_Number is not blank ){
      return below text
      :58A:/{correspondent_Account_Number } **-- this is line 1**
      {correspondent_BIC } **-- this is line 2
** } else if(correspondent_BIC is not blank and correspondent_Account_Number is blank  ){         
      return below text
      :58A:{correspondent_BIC } **--this is line 1
** }else {
    return blank
}

</details>

**Field_59_Benificiary**

<details>
<summary>Expand Details</summary>

benificiary_Account_Number=Settlement_Instruction.Account.Beneficiary_Account_Number       
benificiary_Name=Settlement_Instruction.Account.Beneficiary_Account_Name
benificiary_Name_2=Settlement_Instruction.Account.Beneficiary_Account_Name_2     
benificiary_Address=Settlement_Instruction.Account.Beneficiary_Street_Address
benificiary_City=Settlement_Instruction.Account.Beneficiary_City

if ( benificiary_Account_Number is not blank and benificiary_Name is not blank and benificiary_Address is not blank and benificiary_City is not blank){
    if(benificiary_Name_2 is not blank){
          return below text
           :59:/{benificiary_Account_Number} **-- this is line 1**
           {benificiary_Name } [1,35]**-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
          ** {benificiary_Name_2} [1,35] --**this is line 3
          ** {benificiary_Address}[1,35] --**discard the rest part if length >35
           **{benificiary_City} --**this is line 5
      ** } else if (benificiary_Name_2 is blank){
            return below text
           :59:/{benificiary_Account_Number} **-- this is line 1**
           {benificiary_Name }  **-- **** this is line 2  ****
          ** {benificiary_Address}[1,35] -- **split the value to 2 lines if length>35, [0,****35][36,70], discard the rest part if length >70
****    **       {benificiary_Address}[36,70]**
           **{benificiary_City} --**this is line 4 or 5**
       }
} else {
    return blank
}

</details>

**Field_70_Remittance_Information
**

<details>
<summary>Expand Details</summary>

Remittance_Information1=Settlement_Instruction.Remittance_Information_1
Remittance_Information2=Settlement_Instruction.Remittance_Information_2
Remittance_Information3=Settlement_Instruction.Remittance_Information_3
Remittance_Information4=Settlement_Instruction.Remittance_Information_4**

**Remittance_Information_List= List.of(Remittance_Information1,Remittance_Information2,Remittance_Information3,Remittance_Information4)

Booking_Entity_FMID=Entity.Booking_Entity_SCI_FMID
Payment_Amount=Cashflow.Payment_Amount
Cashflow_Direction=Cashflow.Pay_Receive_Indicator
Settlement_Means = settlement_Instruction.account.SCB_Nostro_Account_Type 
Counterparty_LEI : get LEI from SCI with Entity.Counterparty_SCI_FMID  : legalEntity.regulatoryInfo.regulatoryFieldText where regulatoryTypeValue = 'MIFID' and regulatoryFields ='LEI'
![](https://confluence.global.standardchartered.com/download/attachments/3331053286/image-2025-5-16_17-3-38.png?version=1&modificationDate=1747386219000&api=v2)

if(message_type ='MT103' and Booking_Entity_FMID ='4' and **{Field_Currency}**='INR' and Payment_Amount>=500 Mio and Cashflow_Direction ='Pay' and Settlement_Means ='NOS'){ //2025-05-20 update for ADO 7412111, the change only applied to MT103, not MT103COv
     if({Counterparty_LEI} is null){
            return exception ：field 70 LEI is blank
      }else{
            if( Remittance_Information_List.size ==0){
                  return below text
                  :70:**/SL/**RILFO74KP1CM8P6PCT96
**                  //BL/**{Counterparty_LEI}
            }else{
                 loop Remittance_Information_List{
                 return below text
                 :70: [**/SL/**RILFO74KP1CM8P6PCT96](http://0.0.0.72/SL/RILFO74KP1CM8P6PCT96)
**                //BL/**{Counterparty_LEI}
               //{Remittance_Information_List(0)} 
               //{Remittance_Information_List(1)} **-****-discard the rest part if length >35; if there is  no "//" at the beginning of the value, add "//" prefix. else, no extra prefix needed. **
           }
      }
}else{
      if( Remittance_Information_List.size ==0){
            return blank
      }else{
            loop Remittance_Information_List{
            return below text
            :70:/{Remittance_Information_List(0)} **-- this is line 1，discard the rest part if length >35; If there is  no "/" at the beginning of the value, add "/" prefix. else, no extra prefix needed. **
            //{Remittance_Information_List(n)} **-****-this is line n, discard the rest part if length >35; if there is  no "//" at the beginning of the value, add "//" prefix. else, no extra prefix needed. **
      }
}

</details>

****Field_71_Charges_Bearer****

<details>
<summary>Expand Details</summary>

Charge_Bearer = Settlement_Instruction.charge_Bearer

if (Charge_Bearer is blank){
    return below text
    :71A:OUR
}else if (Charge_Bearer is not 'OUR'){
    return below text
    :71A:{Charge_Bearer}
    :71F:**{Field_Currency}**0,
}else{
    return below text
    :71A:{Charge_Bearer}
}

</details>

****Field_72_Sender_To_Receiver
****

<details>
<summary>Expand Details</summary>

Sender_To_Receiver_Information1=Settlement_Instruction.Sender_To_Receiver_Information_1
Sender_To_Receiver_Information2=Settlement_Instruction.Sender_To_Receiver_Information_2
Sender_To_Receiver_Information3=Settlement_Instruction.Sender_To_Receiver_Information_3
Sender_To_Receiver_Information4=Settlement_Instruction.Sender_To_Receiver_Information_4
Sender_To_Receiver_Information3=Settlement_Instruction.Sender_To_Receiver_Information_5
Sender_To_Receiver_Information4=Settlement_Instruction.Sender_To_Receiver_Information_6

Sender_To_Receiver_Information_List= List.of(Sender_To_Receiver_Information1,Sender_To_Receiver_Information2,Sender_To_Receiver_Information3,Sender_To_Receiver_Information4,Sender_To_Receiver_Information5,Sender_To_Receiver_Information6)

Booking_Entity_FMID=Entity.Booking_Entity_SCI_FMID
Payment_Amount=Cashflow.Payment_Amount
Cashflow_Direction=Cashflow.Pay_Receive_Indicator
Settlement_Means = settlement_Instruction.account.SCB_Nostro_Account_Type 
Counterparty_LEI : get LEI from SCI with Entity.Counterparty_SCI_FMID  : legalEntity.regulatoryInfo.regulatoryFieldText where regulatoryTypeValue = 'MIFID' and regulatoryFields ='LEI'
![](https://confluence.global.standardchartered.com/download/attachments/3331053286/image-2025-5-16_17-3-38.png?version=1&modificationDate=1747386219000&api=v2)

if (Cashflow.Payment_Currency = 'HAU'){
    if (Settlement method ='PVP' or Murex Product Strategy ='PVP'){
       return below text 
           :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF)
            /OCMT/{ISO ccy of the other leg}{amount of the other leg} //more details, please refer to [HKCS initiative - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/HKCS+initiative)
            //{Sender_To_Receiver_Information_List(0)} 
           //{Sender_To_Receiver_Information_List(n)} **- ****discard the rest part if length >35; if there is  no "//" at the beginning of the value, add "//" prefix. else, no extra prefix needed. **
    }else{
         return below text
          :[72:/ACC/SCRTRF](http://0.0.0.72/ACC/SCRTRF)
         //{Sender_To_Receiver_Information_List(0)} 
           //{Sender_To_Receiver_Information_List(n)} **- ****discard the rest part if length >35; if there is  no "//" at the beginning of the value, add "//" prefix. else, no extra prefix needed. **    }
}

if(message_type ='MT202' and Booking_Entity_FMID ='4' and **{Field_Currency}**='INR' and Payment_Amount>=500 Mio and Cashflow_Direction ='Pay' and Settlement_Means ='NOS'){ //2025-05-20 update for ADO 7412111, the change only applied to MT202, not MT202COv/Flip
      if({Counterparty_LEI} is null){
            return exception ：field 72 LEI is blank
      }else{
            if(Sender_To_Receiver_Information_List.size ==0){
                 return below text
                 :72:**/SL/**RILFO74KP1CM8P6PCT96
**                 //BL/**{Counterparty_LEI}
            }else{
                 loopSender_To_Receiver_Information_List{
                 return below text
                 :72: **/SL/**RILFO74KP1CM8P6PCT96
**                 //BL/**{Counterparty_LEI}
                 //{Sender_To_Receiver_Information_List(0)} 
                //{Sender_To_Receiver_Information_List(n)} **- ****discard the rest part if length >35; if there is  no "//" at the beginning of the value, add "//" prefix. else, no extra prefix needed. **
            }
      }
}else{
      if( Sender_To_Receiver_Information_List.size ==0){
              return blank 
      }else{
             loop Sender_To_Receiver_Information_List{
             return below text
             :72:/{Sender_To_Receiver_Information_List(0)} **-- this is line 1，discard the rest part if length >35.  If there is  no "/" at the ****beginning**** of the value, add "/" prefix. else, no extra prefix needed. **
             //{Sender_To_Receiver_Information_List(n)} **-- this is line n, discard the rest part if length >35. if there is  no "//" at the ****beginning**** of the value, add "//" prefix. else, no extra prefix needed. **
      }
}

</details>

**Field_77_POP (Dubai)
**

<details>
<summary>Expand Details</summary>

**if entity = DUBAI & currency != AED & settlement means=’NOS‘ & settlement account contains 'MAIN'& Settlement_Instruction.Account.Beneficiary_Bank_BIC_code != 'SUPPRESSXXX' => :[77B:/ORDERRES/AE//{POP_DUBAI](http://77B/ORDERRES/AE//{POP_DUBAI)} **

</details>

**Field_82_Instructing_Party**

Get the entity FMID(Entity.Booking_Entity_SCI_FMID) from cashflow data
Query the entityBIC with FMID from static data (refer to the static data in **Field_Sender_BIC**)

return :82A:entityBIC

**Field_82_Instructing_Party****_605
**

<details>
<summary>Expand Details</summary>

Ordering_Customer_BIC = Settlement_Instruction.Account.Ordering_Customer_BIC_Code
Beneficiary_BIC=Settlement_Instruction.Account.Beneficiary_BIC_code
Beneficiary_Account_Number =Settlement_Instruction.Account.Beneficiary_Account_Number
Ordering_Customer_Name=Settlement_Instruction.Account.Ordering_Customer_Account_Name
Ordering_Customer_Address=Settlement_Instruction.Account.Ordering_Customer_Street_Address
Ordering_Customer_Country=Settlement_Instruction.Account.Ordering_Customer_City

if( ~~Ordering_Customer_BIC ~~Beneficiary_BIC is not blank){
      return below text
      :82A:{Beneficiary_BIC}~~{Ordering_Customer_BIC}~~ **
**  } else if (~~Ordering_Customer_BIC ~~Beneficiary_BIC is blank and (~~Beneficiary_Account_Number is not blank or~~ Ordering_Customer_Name is not blank or Ordering_Customer_Address is not blank or Ordering_Customer_Country is not blank)){
     if(length of Ordering_Customer_Name>35){
          return below text
          :82D:/{Beneficiary_Account_Number} **-- this is line 1 //if any field value is null, no placeholder reserved**
         {Ordering_Customer_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {Ordering_Customer_Name}[36,70]--**this is line 3**
         {Ordering_Customer_Address} --**discard the rest part if length >35**
         {Ordering_Customer_Country} --**this is line 5**
     }else if (length of Ordering_Customer_Name <=35)      
         return below text
          :82D:/{Beneficiary_Account_Number } **-- this is line 1
        ** {Ordering_Customer_Name} **-- this is line 2
         **{Ordering_Customer_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {Ordering_Customer_Address}[36,70] 
         {Ordering_Customer_Country} --**this is line 4 or 5
**     }
}else {
    return blank
}

</details>

**Field_86_Intermediary_Institution
**

<details>
<summary>Expand Details</summary>

Intermediary_BIC=Settlement_Instruction.Account.Intermediary_BIC_code
Intermediary_Name=Settlement_Instruction.Account.Intermediary_Account_Name

if( Intermediary_BIC is not blank ){
      return below text
      :86A:{Intermediary_BIC } **-- this is line 1****
** } else if(Intermediary_BIC is blank and Intermediary_Name is not blank  ){         
      return below text
      :86D:{Intermediary_Name} [1,35]**--this is line 1, discard the rest part if length >35**
}else {
    return blank
}

</details>

**Field_87_Account_Institution**

<details>
<summary>Expand Details</summary>

Institution_BIC=Settlement_Instruction.Account.Beneficiary_Bank_BIC_code
Institution_Account_Name=Settlement_Instruction.Account.Beneficiary_Bank_Account_Name

if (Institution_BIC is not blank ) {
     return below text
     :87A:{Institution_BIC}**--this is line 1****
**} else if (Cashflow.Payment_Currency!='HAU' andInstitution_BIC is blank and Institution_Account_Name is not blank ){
     return below text
     :87D:{Institution_Account_Name}[1,35]**--this is line 1,discard the rest part if length >35
**}else {
    return blank
}

</details>

**Field_88_Benificiary**

<details>
<summary>Expand Details</summary>

benificiary_BIC=Settlement_Instruction.Account.Beneficiary_BIC_code
benificiary_Account_Number=Settlement_Instruction.Account.Beneficiary_Account_Number       
benificiary_Name=Settlement_Instruction.Account.Beneficiary_Account_Name
benificiary_Name_2 =Settlement_Instruction.Account.Beneficiary_Account_Name_2    
benificiary_Address=Settlement_Instruction.Account.Beneficiary_Street_Address
benificiary_City=Settlement_Instruction.Account.Beneficiary_City

if( benificiary_BIC is not blank and benificiary_Account_Number is not blank ){
      return below text
      :88A:/{benificiary_Account_Number} **-- this is line 1**
      {benificiary_BIC} **-- this is line 2
** } else if(benificiary_BIC is not blank and benificiary_Account_Number is blank  ){         
      return below text
      :88A:{benificiary_BIC} **--this is line 1**
 } else if (benificiary_BIC is blank and benificiary_Account_Number is not blank and benificiary_Name is not blank and benificiary_Address is not blank and benificiary_City is not blank){
     if(benificiary_Name_2 is not blank){
          return below text
          :88D:/{benificiary_Account_Number} **-- this is line 1**
         {benificiary_Name}[1,35] **-- split the value to 2 lines, [1,****35][36,70], discard the rest part if length >70
**         {benificiary_Name_2}[1,35]--**this is line 3**
         {benificiary_Address} --**discard the rest part if length >35**
         {benificiary_City} --**this is line 5**
     }else if (benificiary_Name_2 is blank)      
         return below text
          :88D:/{benificiary_Account_Number} **-- this is line 1
        ** {benificiary_Name} **-- this is line 2
         **{benificiary_Address}[1,35] **--split the value to 2 lines if length>35, [0,35][36,70], discard the rest part if length >70
**         {benificiary_Address}[36,70] 
         {benificiary_City} --**this is line 4 or 5
**     }
}else {
    return blank
}

</details>

**Field_88_Benificiary_605**

<details>
<summary>Expand Details</summary>

Get the entity FMID(Entity.Booking_Entity_SCI_FMID) from cashflow data
Query the entityBIC with FMID from static data (refer to the static data in **Field_Sender_BIC**)

return :88A:entityBIC

</details>

**EXPAND: Swift Field Format**

# Swift Fields Mapping

# ![image2024-1-9_17-49-34.png](attachments/image2024-1-9_17-49-34.png)

- Header - blocker 1 Sample: {1:F01SCBLCNSXAXXX0000000000} Rules: 1. **Field_Sender_BIC **
- Header - blocker 2 Sample: {2:I202SCBLCNSXXXXXN} | # | Tag or field name | M / O | Description and Semantic | Content / Options | Example | | --- | --- | --- | --- | --- | --- | | | Start of block indicator | M | The character { indicates the beginning of a block. | Left curly bracket { | { | | | Block identifier | M | 1 to 3 alphanumeric characters used to define block contents. Basic header block identifier is 2. | 3c | 2 | | | Separator | M | The character : indicates the end of the block identifier. | Colon : | : | | 1 | Input / Output ID | M | For an input message, the Input/Output Identifier consists of the single letter 'I' | 1a | I | | 2 | SWIFT Message Type | M | BIC of receiver | 3n | 103 | | 3 | Destination Address | M | This address is the 12-character SWIFT address of the receiver of the message. It defines the destination to which the message should be sent. | 12x | SCBLCNSXXXXX | | 4 | Priority | O | This character, used within FIN Application Headers only, defines the priority with which a message is delivered. The possible values are: S = System U = Urgent N = Normal | 1a | U | | 5 | Delivery Monitoring | O | Delivery monitoring options apply only to FIN user-to-user messages. The chosen option is expressed as a single digit: 1 = Non-Delivery Warning 2 = Delivery Notification 3 = Non-Delivery Warning and Delivery Notification If the message has priority 'U', the user must request delivery monitoring option '1' or '3'. If the message has priority 'N', the user can request delivery monitoring option '2' or, by leaving the option blank, no delivery monitoring. | 1x | 3 | | 6 | Obsolescence Period | O | The obsolescence period defines the period of time after which a Delayed Message (DLM) trailer is added to a FIN user-to-user message when the message is delivered. For urgent priority messages, it is also the period of time after which, if the message remains undelivered, a Non-Delivery Warning is generated. The values for the obsolescence period are: 003 (15 minutes) for 'U' priority, and 020 (100 minutes) for 'N' priority. | 3n | 003 | | | End of block indicator | M | The Block identifier end tag | Right curly bracket | } |
- Header - blocker 3

**EXPAND_END**

# Open Question

| # | Item Desc | Comment | Status |
| --- | --- | --- | --- |
| 1 | FMSGW Integration: Received message trigger Ratan status/sub-status change logic | 2024-02-27 @Wayne Wang to be confirmed with PO 2024-02-29 got updated event mapping, need further check with PO 2024-03-06updated the event mapping ,need further check with FMSRE to align. | |
| 2 | PM Swift Message (MT6**) Swift type generation condition | 2024-02-27 to be confirmed with Murex team? 2024-03-18 version 1 confirmed | Closed |
| 3 | PM swift message field mapping | 2024-02-27 raised request to Murex team to check 2024-03-15 version 1 confirmed | Closed |
| 4 | The scope and condition to generate MX message | 2024-03-12 MY descoped from ISO side, only SG will be sent to MX, condition updated | Closed |
| 5 | Field Sender BIC query condition: Murex is using "mediumUsage=MXR and mediumCode=SWIFT" to get the value fom SCI | 2024-02-26 sent mail to PO to confirm 2024-03-18 query the value from static data (List shared by users) | Closed |
| 6 | For field 53 in MT202 Flip, current logic is as below, can we use BIC exist/not instead of Bank/corp in the decision point? Corp Client: Beneficiary Customer Account ( Vostro 59) Beneficiary Name ( Vostro 59) Bank: Beneficiary Customer Account (Vostro 58) Beneficiary BIC (Vostro 58) | 2024-04-17 Confirmed with Wayne and we will keep the client type condition | Closed |
| 7 | ~~Branch code for CN/SG/IN/MY~~ | 2024-02-27 sent mail to confirm 2024-02-28 User confrimed in mail, confluence updated | Closed |
| 8 | 1. Payment amount rounding logic TBC 2. format in the swift 100.00 will show as 100, 100.120000 will show as 100,12 shall we follow the same format? | 2024-03-18 confirmed with Wayne, no rounding logic for day1 | Closed |
| 9 | Exception handling - mandatory field missing (source from vostro, nostro, SCI, cashflow...) - Technical issue failed - integration timeout | 2024-03-15 confirmed With Wayne/Geoffrey: no exception handling | Closed |
| 10 | Cashflow Dashboard swift status mapping: for the FMSGW/FMSRE returned status. not clear enough to see if the message is pending user action or not, need further analysis to define the mapping in dashboard | 2024-03-06 Created ADO STORY 3460132 to track this | |
| 11 | will the swift generation scope include loanIQ cashflow? if yes, currently loanIQ has LQ prefix which is different from CN, also need to synchronize with LMS | 2024-03-08 question raised 2024-03-15 LOANIQ will still go to the legcy process, send to Razor for swift generation | Closed |
| 12 | Query Swift message from Ratan UI for loanIQ/CN from different source | 2024-03-15 ADO task to be added in CN backlog | |
| 13 | TBC and null value in the static data | 2024-03-20 need to raise to PO to highlight the process 2024-04-17 updated the logic to get static data | Closed |
| 14 | if the original msg is directly settled without Swift msg, Withdrawal event after that should be directly settled as well? | 2024-04-23 Confirmed with PO and the withdrawal event in the scenario should be directly settled with no swift | |
| 15 | negative case for fields involved account number/name/address/city. | no exception expected in swift generation, double check samples | |
| 16 | Account Number is mandatory for SCPAY markets - separate checking in the Vostro submit stage? | this is required for 53 and beneficiary , add validation for user manually input si | |
| 17 | MX message template display in UI | send sample to dinesh to confrim | |
| 18 | Need to confirm if the BIC will always be set for 56,57,58 | have sent mail to SSI+ and the mail was fw to data ops, no response yet. 2024-04-23 | |
| 19 | No specific replay function for swift generation, | failed/reinstate to replay if needed | |
| 20 | withdrawal component cashflow after netting resultant cashflow released will be failed C1, C2 net to C3 and released withdrawal C1 will got exception in swift generation since Original C1 didn't generate swift | no change required. | |
| | do we need to cover swift generation error in dashboard? | yes | |