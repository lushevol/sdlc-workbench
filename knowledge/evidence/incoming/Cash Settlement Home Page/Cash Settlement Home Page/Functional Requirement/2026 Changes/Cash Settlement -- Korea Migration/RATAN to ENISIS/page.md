# Background

As part of project Cash Settlement Migration, cashflow settlement move to RATAN align with global model. Currently, RATAN get MT message  from MXG KR and transfer to MX message, then send to ENISIS via SFTP. Target flow is that RATAN only get payment initial message from MXGKR and send MT(only MT210)/MX message to ENISIS via FM solace.

Condition: Cashflow Status in (RELEASED, SETTLED) and Settlement Mean='NOS' per existing SWIFT Logic

# Sample MT message

**EXPAND: MT Message**

{1:F01SCBLGB2LATSY0000000000}{2:I210SCBLGB2LXTSYN}{4:
:20:DV02278728504469
:30:260403
:21:DV02278728504469
:32B:GBP1,
:52D:TMG MJ CEB DUCB NCCFMU
22E GIXYVXEV COXEISESV IHBSE SHA
CHINA
-}

**EXPAND_END**

# Sample MX message

**EXPAND: MX Message**

<?xml version="1.0"?>
<AMHMessage>
  <Header>
    <Direction>I</Direction>
    <UniqueID>DV02M01774601589</UniqueID>
    <TrafficType>REQ</TrafficType>
    <Country>GB</Country>
    <MsgType>pacs.009.001.08</MsgType>
    <Service>swift.finplus</Service>
    <Sender>ou=tsy,o=scblgb2l,o=swift</Sender>
    <Receiver>ou=tsy,o=scblgb2l,o=swift</Receiver>
    <ApplicationID>54949-FMSGW-MX</ApplicationID>
    <DataOwner>GBFMKT</DataOwner>
    <JMStopic>v1/settlement/51358-ratanone/fmsgw/-/scbml-4.0/cash/swift/mx</JMStopic>
    <RequestSubType>swift.cbprplus.03</RequestSubType>
  </Header>
  <Payload>
    <RequestOption>
      <NetworkPriority>Normal</NetworkPriority>
    </RequestOption>
    <RequestHeader>
      <Requestor>ou=tsy,o=scblgb2l,o=swift</Requestor>
      <Responder>ou=tsy,o=scblgb2l,o=swift</Responder>
      <Service>swift.finplus</Service>
      <RequestType>pacs.009.001.08</RequestType>
      <RequestRef>DV02M01774601589</RequestRef>
    </RequestHeader>
    <RequestPayload>
      <AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.02">
        <Fr>
          <FIId>
            <FinInstnId>
              <BICFI>SCBLGB2LTSY</BICFI>
            </FinInstnId>
          </FIId>
        </Fr>
        <To>
          <FIId>
            <FinInstnId>
              <BICFI>SCBLGB2LTSY</BICFI>
            </FinInstnId>
          </FIId>
        </To>
        <BizMsgIdr>DV02M01774601589</BizMsgIdr>
        <MsgDefIdr>pacs.009.001.08</MsgDefIdr>
        <BizSvc>swift.cbprplus.03</BizSvc>
        <CreDt>2026-03-27T08:53:23+00:00</CreDt>
      </AppHdr>
      <Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.009.001.08">
        <FICdtTrf>
          <GrpHdr>
            <MsgId>DV02M01774601589</MsgId>
            <CreDtTm>2026-03-27T08:53:23+00:00</CreDtTm>
            <NbOfTxs>1</NbOfTxs>
            <SttlmInf>
              <SttlmMtd>INDA</SttlmMtd>
              <SttlmAcct>
                <Id>
                  <IBAN>GB26SCBL60910491997874</IBAN>
                </Id>
              </SttlmAcct>
            </SttlmInf>
          </GrpHdr>
          <CdtTrfTxInf>
            <PmtId>
              <InstrId>DV02M01774601589</InstrId>
              <EndToEndId>DV02M01774601589</EndToEndId>
              <UETR>565f9648-4e58-41ee-8ad1-8f65414474cc</UETR>
            </PmtId>
            <IntrBkSttlmAmt Ccy="GBP">100</IntrBkSttlmAmt>
            <IntrBkSttlmDt>2026-03-27</IntrBkSttlmDt>
            <InstgAgt>
              <FinInstnId>
                <BICFI>SCBLGB2LTSY</BICFI>
              </FinInstnId>
            </InstgAgt>
            <InstdAgt>
              <FinInstnId>
                <BICFI>SCBLGB2LTSY</BICFI>
              </FinInstnId>
            </InstdAgt>
            <Dbtr>
              <FinInstnId>
                <BICFI>SCBLGB2LTSY</BICFI>
                <LEI>RILFO74KP1CM8P6PCT96</LEI>
              </FinInstnId>
            </Dbtr>
            <CdtrAgt>
              <FinInstnId>
                <BICFI>NBOKKWKWXXX</BICFI>
                <ClrSysMmbId>
                  <ClrSysId>
                    <Cd>GBDSC</Cd>
                  </ClrSysId>
                  <MmbId>AUTOTEST</MmbId>
                </ClrSysMmbId>
                <LEI>549300NB7FE83IH6BW96</LEI>
              </FinInstnId>
            </CdtrAgt>
            <Cdtr>
              <FinInstnId>
                <BICFI>SCBLGB2LTSY</BICFI>
                <LEI>RILFO74KP1CM8P6PCT96</LEI>
              </FinInstnId>
            </Cdtr>
            <CdtrAcct>
              <Id>
                <IBAN>KW43NBOK0000000000002023872477</IBAN>
              </Id>
            </CdtrAcct>
            <InstrForNxtAgt>
              <InstrInf>/FIN53/SCBLGB2LTSY</InstrInf>
            </InstrForNxtAgt>
            <Purp>
              <Cd>FREX</Cd>
            </Purp>
            <RmtInf>
              <Ustrd>/BNF/DERIVATIVES SETTLEMENTS</Ustrd>
            </RmtInf>
          </CdtTrfTxInf>
        </FICdtTrf>
      </Document>
    </RequestPayload>
  </Payload>
</AMHMessage>

**EXPAND_END**

# Sample ACK Message (For Both MT and MX)

| Field | M/O | Source | Values | Remarks | Used in Ratan | Comment From ENISIS |
| --- | --- | --- | --- | --- | --- | --- |
| /AMHMessage/Header/UniqueID | M | Ratan JMS Header | same with JMS Header | Tracking ID | Y | |
| /AMHMessage/Payload/ResponseHeader/Status | M | AMH Status | 0 = ACK, 1 = NAK, 2 = Technical Ack | | Y | Once ENISIS send the Technical Ack, Status will be presented '2'. |
| /AMHMessage/Payload/ResponseHeader/StatusText | M | AMH Status Text | FinalSentOK | FinalCancelled | FirstSentOK | | Y | Ack = FinalSentOK | Nak = FinalCancelled | Technical Ack = FirstSentOK |
| /AMHMessage/Payload/ResponseHeader/StatusDate | M | AMH Timestamp | 2021-01-07T15:35:51.443Z | | Y | |
| /AMHMessage/Payload/ResponseHeader/StatusSource | M | AMH Node Identifier | PN1 | | N | |
| /AMHMessage/Payload/ResponseHeader/StatusMessage | M | AMH Status Description | ACK received | T28027 | If Address Line is present and any other Postal Address element(s) are present, then Town Name and Country are mandatory in Postal Address and a maximum of two occurrences of Address Line are allowed | | Y | Ack, Technical Ack = ACK received Nak -MT=T28027 *(Finerrorcode) -MX=Nak Text |
| /AMHMessage/Payload/ResponsePayload/StatusAttributes | C | As per SWIFTNet SwGbl StatusAttributes schema | <StatusAttributes> <Severity>Fatal</Severity> <Code>Sw.Stds.D00001</Code> <Parameter>Level=1</Parameter> <Parameter>seev.047.001.01-ShareholdersIdentificationDisclosureResponseV01/ RequestPayload/BusAppHeader/head:BusinessApplicationHeaderV02_doc/ Fr/FIId/FinInstnId/BICFI</Parameter> <Text>Invalid BIC</Text> </StatusAttributes> | Repeats for multiple SWIFTNet NAK errors | N | |
| /AMHMessage/Payload/XTSResponsePayload/ | C | For XtremeSec response | <XTSResponsePayload> <versionTag>002</versionTag> <businessUnit>ROOT</businessUnit> <messageId>2345687</messageId> <status>001</status> <decision>UAM HIT</decision> <requestType>O</requestType> <comments>XYZ</comments> <owner> XYZ </owner> <checksum> XYZ </checksum> <systemIdentifier> XYZ </systemIdentifier> </XTSResponsePayload> | Refer to "Sample XtremeSec Response" | N | |

**EXPAND: ACK Message**

<AMHMessage>

<Header>

<UniqueID>bf32797f-80d7-4f73-8173-b34644767dd9_MT103</UniqueID>  <-- Used in Ratan

</Header>        
    <Payload>                
        <ResponseHeader>                
            <Status>0</Status>                <-- Used in Ratan
            <StatusText>FinalSentOK</StatusText>                <-- Used in Ratan
            <StatusDate>2025-09-11T09:28:27.068Z</StatusDate>                <-- Used in Ratan
            <StatusSource>AMHCENT_PN1</StatusSource>                
            <StatusMessage>ACK received</StatusMessage>                <-- Used in Ratan

</ResponseHeader>                
        <ResponsePayload>                
            <StatusAttributes>                
                <Severity>Fatal</Severity>                
                <Code>Sw.Stds.D00001</Code>                
                <Parameter>Level=1</Parameter>                
                <Parameter>seev.047.001.01-ShareholdersIdentificationDisclosureResponseV01/                
                  RequestPayload/BusAppHeader/head:BusinessApplicationHeaderV02_doc/                
                  Fr/FIId/FinInstnId/BICFI</Parameter>                
                <Text>Invalid BIC</Text>                
              </StatusAttributes>                
        </ResponsePayload>                
        <XTSResponsePayload>                    
            <versionTag>002</versionTag>                
            <businessUnit>ROOT</businessUnit>                
            <messageId>211221PN102694764</messageId>                <-- AMH Unique Reference (RFK)
            <status>001</status>                
            <decision>UAM HIT</decision>                
            <requestType>O</requestType>                
            <comments>LN1</comments>                <-- return what AMH <AppCode> sent
            <owner>1317756</owner>                <--  XTS user ID 
            <checksum>XYZ</checksum>                <-- blank
            <systemIdentifier>XTS123456</systemIdentifier>                <-- XTS case number
        </XTSResponsePayload>                   
    </Payload>                      
</AMHMessage>

**EXPAND_END**

# Message Header between Ratan and ENISIS

| | Field | Ratan MX/MT | Expected Response | Enisis logic | Comment |
| --- | --- | --- | --- | --- | --- |
| 1 | X-Outbound-Property-mxDocID | bf32797f-80d7-4f73-8173-b34644767dd9_MT103 | bf32797f-80d7-4f73-8173-b34644767dd9_MT103 | Same with Request | Can be used by ENISIS |
| 2 | X-Outbound-Property-messageType | Settlement | Settlement | Same with Request | Can be used by ENISIS |
| 3 | X-Outbound-Property-trackingId | bf32797f-80d7-4f73-8173-b34644767dd9_MT103 | bf32797f-80d7-4f73-8173-b34644767dd9_MT103 | Same with Request | Can be used by ENISIS |
| 4 | X-Outbound-Property-sender | RATAN | ENISIS | Can be empty | Can be used by ENISIS |
| 5 | X-Outbound-Property-targetSystem | ENISIS | RATAN | Can be empty | Can be used by ENISIS |
| 6 | X-Outbound-Property-OPICSBranch | 45 | 45 | Can be empty | Can be used by ENISIS |
| 7 | X-Outbound-Property-bookingSystem | RATAN | RATAN | Can be empty | Can be used by ENISIS |
| 8 | imsCorrelationId | M00AER010001 | M00AER010001 | Same with Request | Used by IMS |
| 9 | imsEvent | SENT | RECEIVED | Hardcode | Used by IMS |
| 10 | imsTimestamp | 1775113029668 | 1775113090000 | To be Updated by ENISIS as system time | Used by IMS |
| 11 | imsTraceId | 88e7b18e-6521-42c6-bd18-65929c7e6ba6 | 88e7b18e-6521-42c6-bd18-65929c7e6ba6 | Same with Request | Used by IMS |
| 12 | imsPreviousCorrelationId | M00AER010001 | M00AER010001 | Same with Request | Used by IMS |
| 13 | imsSpans | RATAN | RATAN,ENISIS | Hardcode | Used by IMS |
| 14 | trackingId | bf32797f-80d7-4f73-8173-b34644767dd9_MT103 | bf32797f-80d7-4f73-8173-b34644767dd9_MT103 | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Mandatory for SOLACE |
| 15 | sender | RATAN | ENISIS | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Mandatory for SOLACE |
| 16 | domainName | FM | FM | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Mandatory for SOLACE |
| 17 | initiatedTimestamp | 1775113029668 | 1775113029668 | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Mandatory for SOLACE |
| 18 | countryCode | KR | KR | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Mandatory for SOLACE |

# RATAN task:

1. Compare MT messages with those generated from Murex KR.
2. Build connection between RATAN and ENISIS via FM solace.
3. Confirm format of messages sent to ENISIS and ACK/NACK messages from ENISIS.
4. Exception scenarios processing

# Reference :

[FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)

[Cash Settlements Migration -Korea- Scope & Plan - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3588497557#CashSettlementsMigrationKoreaScope&Plan-Objective:)

[ISO20022 Korea - Murex workshop - Murex Development Team - Confluence](https://confluence.global.standardchartered.com/display/BODSD/ISO20022+Korea+-+Murex+workshop#ISO20022KoreaMurexworkshop-MTtemplateusedinKRMurex)