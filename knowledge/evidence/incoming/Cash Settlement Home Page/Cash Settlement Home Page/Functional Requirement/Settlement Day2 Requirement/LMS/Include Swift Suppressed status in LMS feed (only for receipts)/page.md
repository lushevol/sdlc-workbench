# Background

# Business Benefits

# ADO

[Story 10917030 Include Swift Suppressed status in LMS feed (only for receipts)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10917030/)

# Open Questions

| | Question | Answer |
| --- | --- | --- |
| 1 | **As-Is** | Cashflow Status | Send to LMS | | --- | --- | | RELEASED | Yes | | SETTLED | Yes | | Others | No | **To Be** For the new requirement we need to add Swift Suppressed status (only for receipt) and feed to LMS | Cashflow Status | Send to LMS | | --- | --- | | RELEASED | Yes | | SETTLED | Yes | | Swift Suppressed(Receive only) | Yes | | Undo Swift Suppression(Receive only) | Need to Confirm with LMS team | | Swift Suppressed(Receive only)-Withdrawal | Need to Confirm with LMS team | | Others | No | | 2025-10-27 Pending agreement with LMS |
| Cashflow Status | Send to LMS |
| RELEASED | Yes |
| SETTLED | Yes |
| Others | No |
| Cashflow Status | Send to LMS |
| RELEASED | Yes |
| SETTLED | Yes |
| Swift Suppressed(Receive only) | Yes |
| Undo Swift Suppression(Receive only) | Need to Confirm with LMS team |
| Swift Suppressed(Receive only)-Withdrawal | Need to Confirm with LMS team |
| Others | No |
| 2 | Why for Swift Suppressed cashflow need to send to LMS ?and why only receive is needed to be covered? | 2025-10-27 For some scenarios, even though is swift suppressed and there is no nostro payment happened in Ratan, but SCB receive the payment from client ,so we need to add this part and send to LMS |
| 3 | What should be the message data send to LMS when cashflow in Swift Suppressed Status? Same with current ? | 2025-10-27 Pending agreement with LMS For the message template need to Confirm with LMS team |
| 4 | If a cashflow in Swift Suppressed status (receive only),then send to LMS ,after that Undo Swift Suppression, do we need to send another message for this Undo Swift Suppression to LMS? What should be the data message ? | 2025-10-27 Dinesh confirmed in this scenario ,need to send a message to LMS For the message template need to Confirm with LMS team |
| 5 | If a cashflow in Swift Suppressed status (receive only),then send to LMS ,after that Withdrawal , the cashflow status will be updated to CANCELLED status ,do we need to send another message to LMS ? What should be the data message ? | 2025-10-27 Dinesh confirmed in this scenario ,need to send a message to LMS For the message template need to Confirm with LMS team |
| 6 | If a cashflow in Swift Suppressed status (receive only),then send to LMS ,after that Manual Failed, the cashflow status will be updated to FAILED status ,do we need to send another message to LMS ? What should be the data message ? | |
| 7 | When the Swift Suppressed status ,maybe at this point we don't have the stamping info (Vostro /Nostro) that LMS need ,do we need to do a stamping to get the Vostro or Nostro info (to check which field is mandatory and if we can get that data) | 2025-10-27 Dinesh Proposed Confirm with LMS team in Swift Suppressed status we don't have any Nostro or Vostro stamping info ,check with LMS if they can process in this case |
| 8 | When Swift Suppressed status, do another stamping ,but got missing vostro etc ,it doesn't matter if the field is not mandatory? | |

| | Scenario | Send to LMS |
| --- | --- | --- |
| 1 | New->Swift Suppressed(Receive Only) | Y |
| 2 | New->Swift Suppressed(Receive Only)->Undo Swift Suppression | Need to Confirm with LMS team |
| 3 | New->Swift Suppressed(Receive Only)->Withdrawal(CANCELLED) Current behavior: Queued/Waiting/Ready-Not send to LMS Withdrawal-Cancelled-Not send to LMS Released/Settled-Send to LMS Withdrawal-Waiting+Pending exception-Released/Settled-Send to LMS | Need to Confirm with LMS team |

# Requirement Details

## Related Document

[LMS Feed - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/LMS+Feed)

## Surrounding System Impact

LMS?

# Business User Case

### **ANCHOR: Message Template**

Message Template

```
<?xml version="1.0" encoding="UTF-8"?>
<!-- edited with XMLSpy v2013 (x64) (http://www.altova.com) by Amit Kumar Singh (STANDARD CHARTERED BANK) -->
<scb:SCBML scbmlVersion="4-0" xmlns:scb="http://www.sc.com/SCBML-1" xmlns:conf="http://www.fpml.org/FpML-5/confirmation" xmlns:scbextn="http://www.sc.com/scbml/extension-2-0"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.sc.com/SCBML-1 ../../../../../core/4-0/scbml-4-0.xsd http://www.sc.com/SCBML-1 ../../../../../payloadType/cashflowPayload/4-0/scbml-cashFlow-4-0.xsd">
    <scb:header>
  <scb:messageDetails>
   <scb:messageVersion>1.0</scb:messageVersion>
   <scb:messageType>
    <scb:typeName>CashflowData</scb:typeName>
   </scb:messageType>
  </scb:messageDetails>
  <scb:originationDetails>
   <scb:messageSender>
    <scb:messageSender systemScheme="http://www.sc.com/coding-scheme/system-1-0">${stackFlow!}</scb:messageSender>
    <scb:senderDomain>
     <scb:domainName domainNameScheme="http://www.sc.com/coding-scheme/domainNamescheme-1-0">FM</scb:domainName>
    </scb:senderDomain>
    <scb:countryCode>ALL</scb:countryCode>
   </scb:messageSender>
   <scb:messageTimestamp>${messageTimestamp!}</scb:messageTimestamp>
   <scb:initiatedTimestamp>2016-08-06T05:20:04Z</scb:initiatedTimestamp>
   <scb:trackingId>${trackingId!}</scb:trackingId>
  </scb:originationDetails>
  <scb:captureSystem>Stella</scb:captureSystem>
  <scb:process>
   <scb:eventType>Insert</scb:eventType>
  </scb:process>
 </scb:header>
 <scb:payload>
  <scb:payloadFormat>XML</scb:payloadFormat>
  <scb:payloadType>cashflowPayload</scb:payloadType>
  <scb:payloadVersion>4-0</scb:payloadVersion>
  <scb:cashflowPayload>
   <scb:cashflow>
    <scb:header>
     <scb:event eventScheme="http://www.sc.com/coding-scheme/event/scbml-business-event">${businessEvent!}</scb:event>
     <scb:linkId linkIdScheme="http://www.sc.com/coding-scheme/linkId/cashflow/nettingId">${nettingId!}</scb:linkId>
     <scb:cashflowIdentifier>
      <scb:cashflowId cashflowIdScheme="http://www.sc.com/coding-scheme/cashflowId">${cashflowId!}</scb:cashflowId>
     </scb:cashflowIdentifier>
    </scb:header>
    <scb:payment>
                    <conf:payerPartyReference href="party1"/>
                    <conf:receiverPartyReference href="party2">${receiverPartyReference!}</conf:receiverPartyReference>
     <conf:paymentAmount>
      <conf:currency currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">${isoCurrency!}</conf:currency>
      <conf:amount>${paymentAmount!}</conf:amount>
     </conf:paymentAmount>
     <conf:paymentDate>
      <conf:unadjustedDate>${unadjustedDate!}</conf:unadjustedDate>
         <conf:dateAdjustments>
                         <conf:businessDayConvention>NONE</conf:businessDayConvention>
                        </conf:dateAdjustments>
     </conf:paymentDate>
    </scb:payment>
   </scb:cashflow>
   <scb:tradeReferenceInformation>
    <conf:partyTradeIdentifier>
     <conf:issuer>party1</conf:issuer>
     <conf:tradeId tradeIdScheme="http://www.sc.com/coding-scheme/tradeId">${tradeId!}</conf:tradeId>
    </conf:partyTradeIdentifier>
    <scb:partyTradeInformation xsi:type="scbextn:PartyTradeInformation">
     <conf:partyReference href="party1"/>
     <conf:executionDateTime>${tradeBookingTimestamp!}</conf:executionDateTime>
     <scbextn:tradeSource tradeSourceScheme="http://www.sc.com/coding-scheme/tradeSource/originalSourceSystem">
      <scbextn:name>${sourceSystem!}</scbextn:name>
     </scbextn:tradeSource>
    </scb:partyTradeInformation>
    <scb:productType productTypeScheme="http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode">${productType!}</scb:productType>
    <scb:productId productIdScheme="http://www.fpml.org/coding-scheme/product-taxonomy">${allotment!}</scb:productId>
    <scb:tradePortfolio>
     <conf:partyPortfolioName>
      <conf:partyReference href="party1"/>
      <conf:portfolioName>${portfolioName!}</conf:portfolioName>
     </conf:partyPortfolioName>
    </scb:tradePortfolio>
    <scb:state stateScheme="http://www.sc.com/coding-scheme/state/tradeWorkflowStatus">${tradeWorkflowStatus!}</scb:state>
   </scb:tradeReferenceInformation>
   <scb:party id="party1">
    <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/LEID">${legalEntityId!}</conf:partyId>
    <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMID">${party1FmId!}</conf:partyId>
    <conf:person id="trader">
     <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">${dealerPersonId!}</conf:personId>
    </conf:person>
   </scb:party>
   <scb:party id="party2">
             <conf:partyId>Dummy</conf:partyId>
             <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMID">${party2FmId!}</conf:partyId>
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMCODE">${party2FmCode!}</conf:partyId>
            </scb:party>
   <scb:cashflowSSI>
       <scb:SSIId>${ssiId!}</scb:SSIId>
    <scb:settlementInstruction>
     <conf:intermediaryInformation>
      <conf:routingIdsAndExplicitDetails>
       <conf:routingIds>
        <conf:routingId>${intermediaryInformationRoutingId!}</conf:routingId>
       </conf:routingIds>
      </conf:routingIdsAndExplicitDetails>
     </conf:intermediaryInformation>
     <conf:beneficiaryBank>
      <conf:routingIdsAndExplicitDetails>
       <conf:routingIds>
        <conf:routingId>${beneficiaryBankRoutingId!}</conf:routingId>
       </conf:routingIds>
      </conf:routingIdsAndExplicitDetails>
     </conf:beneficiaryBank>
     <conf:beneficiary>
      <conf:routingIdsAndExplicitDetails>
       <conf:routingIds>
        <conf:routingId>${beneficiaryRoutingId!}</conf:routingId>
       </conf:routingIds>
       <conf:routingName>${beneficiaryRoutingName!}</conf:routingName>
       <conf:routingAccountNumber>${beneficiaryRoutingAccountNumber!}</conf:routingAccountNumber>
      </conf:routingIdsAndExplicitDetails>
     </conf:beneficiary>
     <scb:orderingCustomer>
      <conf:routingIdsAndExplicitDetails>
       <conf:routingIds>
        <conf:routingId>${orderingCustomerRoutingId!}</conf:routingId>
       </conf:routingIds>
      </conf:routingIdsAndExplicitDetails>
     </scb:orderingCustomer>
     <scb:settlementMeans>
      <scb:settlementAccountNo>${settlementAccountNo!}</scb:settlementAccountNo>
     </scb:settlementMeans>
     <scb:partyReference href="party2"/>
    </scb:settlementInstruction>
    <scb:settlementInstruction>
     <conf:correspondentInformation>
      <conf:routingIdsAndExplicitDetails>
       <conf:routingIds>
        <conf:routingId>${correspondentInformationRoutingId!}</conf:routingId>
       </conf:routingIds>
      </conf:routingIdsAndExplicitDetails>
     </conf:correspondentInformation>
     <conf:beneficiary>
      <conf:routingIds>
       <conf:routingId>${beneficiaryBankParty1RoutingId!}</conf:routingId>
      </conf:routingIds>
     </conf:beneficiary>
     <scb:partyReference href="party1"/>
    </scb:settlementInstruction>
   </scb:cashflowSSI>
  </scb:cashflowPayload>
 </scb:payload>
</scb:SCBML>
 
```

### Data Mapping

| Field Name in Message Template | xPath | Mandatory | Sample |
| --- | --- | --- | --- |
| stackFlow | | | FMRPMUREX |
| messageTimestamp | | | 2025-10-25T01:50:11.502170181 |
| trackingId | | | e4629d3f-2b13-45f8-b042-8f4d90eca680 |
| businessEvent | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:event[@eventScheme='[http://www.sc.com/coding-scheme/event/scbml-business-event](http://www.sc.com/coding-scheme/event/scbml-business-event)']"), | Y | New/Withdrawal |
| nettingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:linkId[@linkIdScheme='[http://www.sc.com/coding-scheme/linkId/cashflow/nettingId](http://www.sc.com/coding-scheme/linkId/cashflow/nettingId)']"), | Y for netting | c65e315b-afd2-11f0-8792-005056ac01ca |
| cashflowId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:cashflowId[@cashflowIdScheme='[http://www.sc.com/coding-scheme/cashflowId](http://www.sc.com/coding-scheme/cashflowId)']"), | Y | M00202510132 |
| receiverPartyReference | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:receiverPartyReference[@href='party2']"), | Y | Debit |
| isoCurrency | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency"), | Y | USD |
| paymentAmount | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount"), | Y | 1870.00 |
| unadjustedDate | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate"), | Y | 2025-07-29 |
| tradeId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme='[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)']"), | Y | 103991599 |
| tradeBookingTimestamp | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeInformation[@xsi:type='scbextn:PartyTradeInformation']/conf:executionDateTime"), | | 2025-06-27T14:27:44Z |
| sourceSystem | | | Murex |
| productType | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productType[@productTypeScheme='[http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode](http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode)'] | Y | IFXXXX |
| allotment | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productId[@productIdScheme='[http://www.fpml.org/coding-scheme/product-taxonomy](http://www.fpml.org/coding-scheme/product-taxonomy)'] | Y | CURR|FXD|FXD |
| portfolioName | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:tradePortfolio/conf:partyPortfolioName/conf:portfolioName[1]"), | Y | FXI_OP_LDN |
| tradeWorkflowStatus | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:state[@stateScheme='[http://www.sc.com/coding-scheme/state/tradeWorkflowStatus](http://www.sc.com/coding-scheme/state/tradeWorkflowStatus)']"), | N | VALD |
| legalEntityId | | | 11090155 |
| party1FmId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)']"), | Y | 10075222 |
| dealerPersonId | | | 1474102 |
| party2FmId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)']"), | N | 400617196 |
| party2FmCode | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMCODE](http://www.sc.com/coding-scheme/partyId/FMCODE)']"), | N | EDELWEISS I S P*SIN |
| ssiId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:SSIId"), | N | 47349561 |
| intermediaryInformationRoutingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:intermediaryInformation/conf" + ":routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"), | N | |
| beneficiaryBankRoutingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiaryBank/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"), | N | SCBLSG22XXX |
| beneficiaryRoutingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiary/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"), | N | |
| beneficiaryRoutingName | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiary/conf:routingIdsAndExplicitDetails/conf:routingName"), | N | EDELWEISS INTERNATIONAL SINGAPORE |
| beneficiaryRoutingAccountNumber | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiary/conf:routingIdsAndExplicitDetails/conf:routingAccountNumber"), | N | 0106533495 |
| orderingCustomerRoutingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/scb:orderingCustomer/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"), | N | |
| settlementAccountNo | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction/scb:settlementMeans/scb:settlementAccountNo"), | N | USD MAIN |
| correspondentInformationRoutingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party1']/conf:correspondentInformation/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"), | N | SCBLUS33XXX |
| beneficiaryBankParty1RoutingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party1']/conf:beneficiary/conf" + ":routingIdsAndExplicitDetails/conf:routingIds/conf:routingId[@routingIdCodeScheme='http://www.sc.com/coding-scheme/routingId/ebbsAccountId']"), | N | 15199166301 |

### NEW and Withdrawal Message Comparison(Send to LMS)

📎 [M00202510132NEW-RELEASED-SEND TO LMS.XML](attachments/M00202510132NEW-RELEASED-SEND TO LMS.XML)
           
📎 [M00202510132WITHDRAWAL-RELEASED-SEND TO LMS.XML](attachments/M00202510132WITHDRAWAL-RELEASED-SEND TO LMS.XML)

| | |
| --- | --- |
| ![image-2025-10-25_11-56-26.png](attachments/image-2025-10-25_11-56-26.png) | |
| ![image-2025-10-25_11-56-47.png](attachments/image-2025-10-25_11-56-47.png) | |
| ![image-2025-10-25_11-57-10.png](attachments/image-2025-10-25_11-57-10.png) | |
| ![image-2025-10-25_11-57-39.png](attachments/image-2025-10-25_11-57-39.png) | |