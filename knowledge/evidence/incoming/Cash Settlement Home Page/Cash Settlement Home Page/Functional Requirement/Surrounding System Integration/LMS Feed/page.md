| Document status | Reviewed and agreed with business owners on July 21, 2023 |
| --- | --- |
| Document owner | Jill Du |
| Product Owner | Dinesh, Arockia |
| Business Owner | Kannan, Kamesh; Balasubramanian, Nivethitha |
| Solution Designer | |
| Developers | Li, Daniel Zhaolei Huang, Caroline Xinmiao |
| QA | Ma, Shimeng |

# Function Flow - FMRP

# Vostro/Nostro data

- SCB Pay cashflow: Both Vostro & Nostro are required.
- SCB Receive cashflow: Only Nostro are mandatory.

# Logics to decide sending LMS or not

## Check the cashflow Status

| Cashflow Status | Send to LMS |
| --- | --- |
| RELEASED | Yes |
| SETTLED | Yes |
| Others | No |

## ~~Check if the booking entity FMID according to below list  ~~

| ~~Entity FM Code~~ | ~~ Entity FMID~~ | ~~Branch Code~~ | ~~Feeding to LMS~~ |
| --- | --- | --- | --- |
| ~~SCB EGYPT*CAI~~ | ~~401036553~~ | ~~34~~ | ~~No~~ |
| ~~SCB SAUDI*RYD~~ | ~~400991880~~ | ~~16~~ | ~~No~~ |
| ~~NEPAL GRINDLAYS*KTM~~ | ~~400007847~~ | ~~47~~ | ~~No~~ |
| ~~SCB KL*KUL?~~ | ~~9~~ | ~~28~~ | ~~No~~ |
| ~~STANCHART SAADIQ*KUL~~ | ~~400093619~~ | ~~28~~ | ~~No~~ |
| ~~SCB TAIPEI*TPE~~ | ~~10038345~~ | ~~66~~ | ~~No~~ |
| ~~SCB TAIPOBU*TPE~~ | ~~300011345~~ | ~~67~~ | ~~No~~ |
| ~~SCB BANGKOK*BKK~~ | ~~6~~ | ~~22~~ | ~~No~~ |
| ~~SCB MAUR*PLO~~ | ~~400018439~~ | ~~98~~ | ~~No~~ |
| ~~SCB JAKARTA*JKT~~ | ~~8~~ | ~~27~~ | ~~No~~ |
| ~~SCB MANILA*MNL ~~ | ~~10036428~~ | ~~58~~ | ~~No~~ |
| ~~SCB TOKYO*TYO~~ | ~~10036382~~ | ~~62~~ | ~~No~~ |
| ~~SCBL*JBG ~~ | ~~400032489~~ | ~~71~~ | ~~No~~ |
| ~~SC PVT BK JE BR*STH~~ | ~~400910415~~ | ~~05~~ | ~~No~~ |
| ~~CAZENOVE*HKGJ@~~ | ~~300075472~~ | ~~60~~ | ~~No~~ |
| ~~SCB MNL FCD*MNL~~ | ~~300089409~~ | ~~59~~ | ~~No~~ |
| ~~Other Manual Entities~~ | ~~Multiple~~ | | ~~Yes~~ |

## Remove Entity Filter on Ratan side, Ratan will send all the entities to LMS

| Entity FM Code | 2025-10-28 Entity FMID | Branch Code | 2025-10-28 Feeding to LMS |
| --- | --- | --- | --- |
| SCB EGYPT*CAI | 401036553 | 34 | No --> Yes |
| SCB SAUDI*RYD | 400991880 | 16 | No --> Yes |
| NEPAL GRINDLAYS*KTM | 400007847 | 47 | No --> Yes |
| SCB KL*KUL? | 9 | 28 | No --> Yes |
| STANCHART SAADIQ*KUL | 400093619 | 28 | No --> Yes |
| SCB TAIPEI*TPE | 10038345 | 66 | No --> Yes |
| SCB TAIPOBU*TPE | 300011345 | 67 | No --> Yes |
| SCB BANGKOK*BKK | 6 | 22 | No --> Yes |
| SCB MAUR*PLO | 400018439 | 98 | No --> Yes |
| SCB JAKARTA*JKT | 8 | 27 | No --> Yes |
| SCB MANILA*MNL | 10036428 | 58 | No --> Yes |
| SCB TOKYO*TYO | 10036382 | 62 | No --> Yes |
| SCBL*JBG | 400032489 | 71 | No --> Yes |
| ~~PHILIP FCU ~~ | | | ~~No~~ |
| SC PVT BK JE BR*STH | 400910415 | 05 | No --> Yes |
| CAZENOVE*HKGJ@ | 300075472 | 60 | No --> Yes |
| SCB MNL FCD*MNL | 300089409 | 59 | No --> Yes |
| Other Manual Entities | Multiple | | Yes |

- ADO: [Story 10917020 LMS - Remove the entity filter in LMS feed](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10917020)
- Requirement: - Remove entity filter on Ratan side and send all entities to LMS - The message template sending to LMS will not changed, refer to Chapter 6 and 6.1

User Case

| No | Scenario | Step | Expected Result |
| --- | --- | --- | --- |
| 1 | Send to LMS-1 | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=NOS - Beneficiary BIC !=REJECTXXALL 2.C1 cashflow 'Released' | 2.Send to LMS |
| | Send to LMS-2 | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=NOS - Beneficiary BIC !=REJECTXXALL - SCB receive - Notice to Receive=N 2.C1 cashflow ‘Settled' | 2.Send to LMS |
| | Not send to LMS-1 | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=Over Account/FXBRREC/Others - Beneficiary BIC !=REJECTXXALL 2.C1 cashflow 'Released' or ‘Settled' | 2.Not send to LMS |
| | Not send to LMS-2 | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=NOS - Beneficiary BIC =REJECTXXALL 2.C1 cashflow 'Released' or ‘Settled' | 2.Not send to LMS |
| | Not send to LMS-3 | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=NOS - Beneficiary BIC !=REJECTXXALL 2.Cashflow in 'Ready' / 'Cashflow Suppressed' / 'Swift Suppressed' /'Failed'/'Hold'/'Unhold' status | 2.Not send to LMS |
| | Send to LMS (Withdrawal released) | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=NOS - Beneficiary BIC !=REJECTXXALL 2.C1 Release or Settled 3.Withdrawal C1 4.Maker checker | 2.Send to LMS 3.C1 in Waiting +Pending Exception 4.C1 in Released Status and send to LMS |
| | Not send to LMS (Withdrawal not released) | 1.Book cashflow C1 meet below condition - Booking entity is one of the above 16 entities - Settlement means=NOS - Beneficiary BIC !=REJECTXXALL 2.C1 Release or Settled 3.Withdrawal C1 | 2.Send to LMS 3.C1 in Waiting +Pending Exception and not send to LMS |

- Releated Document: [LMS - Remove the entity filter in LMS feed - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/LMS+-+Remove+the+entity+filter+in+LMS+feed)

## Check the Nostro settlement means(<u>logical model field name: Settlement_Instruction.Account.SCB_Nostro_Account_Type</u>) as below

| Settlement means | Feed to LMS |
| --- | --- |
| Nos | Yes |
| Over Account | No |
| FXBRREC | No |
| others... | No |

## Check the Vostro Beneficiary BIC(<u>logical model field name: Settlement_Instruction.Account.Beneficiary_BIC_code)</u> as below

| Beneficiary BIC | Feed to LMS |
| --- | --- |
| REJECTXXALL | No |
| Else | Yes |

# Source Systems and Prefix of Field 20

LMS would take the responsibility to generate the field 20 prefix from the raw data received from RATAN, below are the  agreed mapping between RATAN & LMS.

- SABRE EQ -> BCS STELLA -> STELLA -> TDS3 -> RATAN ONE: We are already populating the value ‘STELLA’ in the feed to LMS. RAZOR is already generating the SWIFT with ‘EQ’ as the prefix in field 20 of the payment message
- LOANIQ -> STELLA -> TDS3 -> RATAN ONE: We will populate ‘LOANIQ’ in the feed to LMS. RAZOR will generate the SWIFT with ‘LQ’ as the prefix in field 20 of the payment message for LOANIQ go live
- BLADE/S2BX/CFETS -> STELLA -> TDS3 -> RATAN ONE: We will populate ‘FMRP’ as the value in feed to LMS. RAZOR will generate the SWIFT with ‘MX’ as the prefix in field 20 of the payment message for China go live

| Booking System | Source System | Flow | Prefix of field 20 |
| --- | --- | --- | --- |
| SABRE EQ | STELLA | SABRE EQ -> BCS STELLA -> STELLA -> TDS3 -> RATAN ONE | EQ |
| LOANIQ | LOANIQ | LOANIQ -> STELLA -> TDS3 -> RATAN ONE | LQ |
| BLADE/S2BX/CFETS | FMRP | BLADE/S2BX/CFETS -> STELLA -> TDS3 -> RATAN ONE | DV |

# Enhancement for the new user case of netting on different products

- ADO: [Story 6969335 LMS Feed - Update value as NETTING RESULTANT where taxonomy is empty](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6969335)
- Requirement: RATAN populate the allotment with default value '**NETTING RESULTANT**' with below conditions - Cashflow is netting resultant cashflow, the cashflow id is starting with '**N***' - The original allotment is blank given the netting is from cashflows with different products
- User Case: | **Test Case** | **Netting Type** | **Entity** | **Component Cashflows** | **Netting Resultant Cashflow Sent to LMS** | **LMS Consumed** | | --- | --- | --- | --- | --- | --- | | 1 | Ben BIC Netting | SCB LONDON*LDN | M01737542513- CURR|FXD|XSW M01737542507- CURR|FXD|XSW M01737542502- CURR|FXD|FXD | N00000035675- NETTING RESULTANT | Y | | 2 | Ben BIC Netting | SCB LONDON*LDN | M01737542574- CURR|FXD|FXD M01737542573- CURR|FXD|FXD | N00000035676- CURR|FXD|FXD | Y | | 3 | Bilateral Netting | SCB CN HANGZHOU*HNZ | M01737542658- COM|SWAP M01737542652- COM|SWAP | N00000035677- COM|SWAP | Y | | 4 | Bilateral Netting | SCB LONDON*LDN | M01737542773- IRD|CS M01737542770- CURR|FXD|FXD | N00000035679- NETTING RESULTANT | Y | | 5 | NDS Fixing Netting | SCB LONDON*LDN | M01737542042- IRD|CS M01737542054- CURR|FXD|FXD | N00000035672- NETTING RESULTANT | Y |

# Message Template

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

## Data Mapping

| Field Name in Message Template | xPath | Mandatory | Sample |
| --- | --- | --- | --- |
| stackFlow | "/scb:SCBML/scb:header/scb:originationDetails/scb:messageSender/scb:messageSender[@systemScheme='http://www.sc.com/coding-scheme/stack-flow']" | N | FMRPMUREX |
| messageTimestamp | "/scb:SCBML/scb:header/scb:originationDetails/scb:messageTimestamp" | Y | 2025-10-25T01:50:11.502170181 |
| trackingId | "/scb:SCBML/scb:header/scb:originationDetails/scb:trackingId" | Y | e4629d3f-2b13-45f8-b042-8f4d90eca680 |
| businessEvent | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:event[@eventScheme='[http://www.sc.com/coding-scheme/event/scbml-business-event](http://www.sc.com/coding-scheme/event/scbml-business-event)']" | Y | New/Withdrawal |
| nettingId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:linkId[@linkIdScheme='[http://www.sc.com/coding-scheme/linkId/cashflow/nettingId](http://www.sc.com/coding-scheme/linkId/cashflow/nettingId)']" | Y for netting | c65e315b-afd2-11f0-8792-005056ac01ca |
| cashflowId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:cashflowId[@cashflowIdScheme='[http://www.sc.com/coding-scheme/cashflowId](http://www.sc.com/coding-scheme/cashflowId)']" | Y | M00202510132 |
| receiverPartyReference | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:receiverPartyReference[@href='party2']"), | Y | Debit |
| isoCurrency | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency"), | Y | USD |
| paymentAmount | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount"), | Y | 1870.00 |
| unadjustedDate | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate"), | Y | 2025-07-29 |
| tradeId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme='[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)']"), | Y | 103991599 |
| tradeBookingTimestamp | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeInformation[@xsi:type='scbextn:PartyTradeInformation']/conf:executionDateTime" | N | 2025-06-27T14:27:44Z |
| sourceSystem | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeInformation[@xsi:type='scbextn:PartyTradeInformation']/scbextn:tradeSource[@tradeSourceScheme='http://www.sc.com/coding-scheme/tradeSource/originalSourceSystem']/scbextn:name" | N | Murex |
| productType | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productType[@productTypeScheme='[http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode](http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode)'] | Y | IFXXXX |
| allotment | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productId[@productIdScheme='[http://www.fpml.org/coding-scheme/product-taxonomy](http://www.fpml.org/coding-scheme/product-taxonomy)'] | Y | CURR|FXD|FXD |
| portfolioName | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:tradePortfolio/conf:partyPortfolioName/conf:portfolioName[1]"), | Y | FXI_OP_LDN |
| tradeWorkflowStatus | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:state[@stateScheme='[http://www.sc.com/coding-scheme/state/tradeWorkflowStatus](http://www.sc.com/coding-scheme/state/tradeWorkflowStatus)']"), | N | VALD |
| legalEntityId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/LEID](http://www.sc.com/coding-scheme/partyId/FMID)']"), | N | 11090155 |
| party1FmId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)']"), | Y | 10075222 |
| dealerPersonId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:person//conf:personId[@personIdScheme='http://www.sc.com/coding-scheme/personId/PSID']" | N | 1474102 |
| party2FmId | "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)']"), | Y | 400617196 |
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

# ~~Detail Fields Mapping~~

| ~~Mandatory~~ | ~~field name~~ | ~~xpath~~ |
| --- | --- | --- |
| ~~Y~~ | ~~ "cashflowId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:cashflowId[@cashflowIdScheme='[http://www.sc.com/coding-scheme/cashflowId](http://www.sc.com/coding-scheme/cashflowId)']"),~~ |
| ~~N~~ | ~~ "cashflowVersion"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:cashflowVersion"),~~ |
| ~~N~~ | ~~ "businessVersion"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:businessVersion"),~~ |
| ~~Y~~ | ~~ "businessEvent"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:event[@eventScheme='[http://www.sc.com/coding-scheme/event/scbml-business-event](http://www.sc.com/coding-scheme/event/scbml-business-event)']"),~~ |
| ~~Y for netting~~ | ~~ "nettingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:linkId[@linkIdScheme='[http://www.sc.com/coding-scheme/linkId/cashflow/nettingId](http://www.sc.com/coding-scheme/linkId/cashflow/nettingId)']"),~~ |
| ~~Y~~ | ~~ "receiverPartyReference"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:receiverPartyReference[@href='party2']"),~~ |
| ~~Y~~ | ~~ "payerPartyReference"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:payerPartyReference[@href='party1']"),~~ |
| ~~Y~~ | ~~ "isoCurrency"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency"),~~ |
| ~~Y~~ | ~~ "paymentAmount"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount"),~~ |
| ~~Y~~ | ~~ "unadjustedDate"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate"),~~ |
| ~~Y~~ | ~~ "tradeBookingTimestamp"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeInformation[@xsi:type='scbextn:PartyTradeInformation']/conf:executionDateTime"),~~ |
| ~~Y~~ | ~~ "productType"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productType[@productTypeScheme='[http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode](http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode)']~~ |
| ~~Y~~ | ~~ "allotment"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:productId[@productIdScheme='[http://www.fpml.org/coding-scheme/product-taxonomy](http://www.fpml.org/coding-scheme/product-taxonomy)']~~ |
| ~~Y~~ | ~~ "portfolioName"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:tradePortfolio/conf:partyPortfolioName/conf:portfolioName[1]"),~~ |
| ~~N~~ | ~~ "tradeWorkflowStatus"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:state[@stateScheme='[http://www.sc.com/coding-scheme/state/tradeWorkflowStatus](http://www.sc.com/coding-scheme/state/tradeWorkflowStatus)']"),~~ |
| ~~N~~ | ~~ "cashflowStatus"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:state[@stateScheme='[http://www.sc.com/coding-scheme/state/workflowStatus](http://www.sc.com/coding-scheme/state/workflowStatus)']"),~~ |
| ~~Y~~ | ~~ "party1FmId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)']"),~~ |
| ~~N~~ | ~~ "party2FmId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)']"),~~ |
| ~~N~~ | ~~ "party2FmCode"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMCODE](http://www.sc.com/coding-scheme/partyId/FMCODE)']"),~~ |
| ~~N~~ | ~~ "ssiId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:SSIId"),~~ |
| ~~N~~ | ~~ "intermediaryInformationRoutingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:intermediaryInformation/conf" + ":routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"),~~ |
| ~~N~~ | ~~ "beneficiaryBankRoutingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiaryBank/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"),~~ |
| ~~N~~ | ~~ "beneficiaryRoutingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiary/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"),~~ |
| ~~N~~ | ~~ "beneficiaryRoutingName"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiary/conf:routingIdsAndExplicitDetails/conf:routingName"),~~ |
| ~~N~~ | ~~ "beneficiaryRoutingAccountNumber"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/conf:beneficiary/conf:routingIdsAndExplicitDetails/conf:routingAccountNumber"),~~ |
| ~~N~~ | ~~ "orderingCustomerRoutingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party2']/scb:orderingCustomer/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"),~~ |
| ~~N~~ | ~~ "settlementAccountNo"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction/scb:settlementMeans/scb:settlementAccountNo"),~~ |
| ~~N~~ | ~~ "settlementGateway"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction/scb:settlementMeans/scb:settlementGateway"),~~ |
| ~~N~~ | ~~ "correspondentInformationRoutingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party1']/conf:correspondentInformation/conf:routingIdsAndExplicitDetails/conf:routingIds/conf:routingId"),~~ |
| ~~N~~ | ~~ "beneficiaryBankParty1RoutingId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflowSSI/scb:settlementInstruction[scb:partyReference/@href='party1']/conf:beneficiary/conf" + ":routingIdsAndExplicitDetails/conf:routingIds/conf:routingId[@routingIdCodeScheme='http://www.sc.com/coding-scheme/routingId/ebbsAccountId']"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledCashflowId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:header/scb:cashflowIdentifier/scb:cashflowId[@cashflowIdScheme='[http://www.sc.com/coding-scheme/cashflowId](http://www.sc.com/coding-scheme/cashflowId)']"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledIsoCurrency"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:payment/conf:paymentAmount/conf:currency"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledCashflowVersion"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:header/scb:cashflowIdentifier/scb:cashflowVersion"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledBusinessVersion"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:header/scb:cashflowIdentifier/scb:businessVersion"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledCashflowStatus"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:header/scb:state[@stateScheme='[http://www.sc.com/coding-scheme/state/workflowStatus](http://www.sc.com/coding-scheme/state/workflowStatus)']"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledReceiverPartyReference"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:payment/conf:receiverPartyReference/@href"),~~ |
| ~~Y for admendment~~ | ~~ "cancelledUnadjustedDate"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow[scb:header/scb:event[text()='Withdrawal']]/scb:payment/conf:paymentDate/conf:unadjustedDate"),~~ |
| ~~Y~~ | ~~ "tradeId"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme='[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)']"),~~ |
| ~~N~~ | ~~ "tradeVersion"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier[@xsi:type='scbextn:PartyTradeIdentifier']/conf:versionedTradeId" + "/conf:version" ~~ |
| ~~Y~~ | ~~ "receiverPartyReference"~~ | ~~ "/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:receiverPartyReference/@href"~~ |