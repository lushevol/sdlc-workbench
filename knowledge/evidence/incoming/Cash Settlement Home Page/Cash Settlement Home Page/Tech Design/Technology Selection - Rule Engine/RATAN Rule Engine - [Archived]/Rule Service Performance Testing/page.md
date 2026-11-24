# *Rule service performance testing*

**EXPAND: Document History**

## Document History

### Document Information

| Document Name | Rule Service Performance Testing |
| --- | --- |
| **Status** | Done |
| **Date Last Edited** | 2024-01-15 |
| **Author** | @Jialin Wang |
| **File URL** | |

### Version History

| Version | Updated By | Revision Date | Summary of Changes |
| --- | --- | --- | --- |
| 1.0 | @Jialin Wang | 2024-01-15 | Initial draft |
| 1.1 | @Jialin Wang | 2024-01-16 | attached JMeter report and PT is done |

### Consulted with

| Version | Name | Role | Date |
| --- | --- | --- | --- |
| 1.0 | | Head Derivatives Trade Processing Development (AO) | |

### Sign-Off

| Version | Name | Role | Attach Sign-off Email | Sign-off Date |
| --- | --- | --- | --- | --- |
| 1.0 | | Head Derivatives Trade Processing Development (AO) | | |

By signing off, the sign-off parties acknowledge that they are signing-off the Test Strategy based on the risk appetite of technology and the business. Endorsement from the PWC and/or PSC to be obtained if there are changes made after signed-off.

**EXPAND_END**

**EXPAND: 1. Introduction**

## 1. Introduction

***This performance testing is using for detect and prove the performance of rule service.***

This document provides a summary of key information related to performance testing to be conducted for Ratan One rule service, Once signed-off, this will serve as the plan for performance testing.

**Project ****Overviews**

The bank is currently using two Murex 2.11 instances (GDC and Korea) for derivatives booking, processing, PnL/risk reporting, accounting and settlement. Since Murex 2.11 is at end-of-life
vendor support with high operational risk, FM T&I designed a decommissioning strategy which will be gradually migrating the Derivatives desks to the FM end-state architecture made of 6 core
components; Sabre, Blade, RATAN, DQSL/FM DATA Platform, CDU and Razor. This multi-year strategy consists in delivering the benefits of the target systems while gradually reducing the
business criticality and operational risk associated with the current platform. It is called re-platforming because it will also oversee the progress made by the other decommissioning programs
towards.

**Rule service Overviews**

Rule engine is regarded as a sophisticated if/then statement interpreted; it can easily separate the business logic from the source code. Drools is the one of most mature open-source rule engines in the world.  It has been widely adopted in the industries as its' powerful and rich features. In Ratan One, there're various types of rules, e.g., suppression rules, validation rules and entitlement rules etc. Drools is considered as a better alternative to define and trigger the rules.

**EXPAND_END**

**EXPAND: 2. NFR and Volumetrics**

## 2. NFR and Volumetrics

NFR and Volumetrics should detail the performance and stability NFR from the supporting documents. Any additional information required to produce the test plan and supporting evidence of the source of this information. Details of the volumetrics for UI or batch and the calculations used to generate the TPH used in testing. Any sources should be stored in share point and hyperlinked in the document. Note the volumes listed below should be Production volumes any reduction for testing purposes should be fully documented and all adjustments and assumptions explained and detailed.

### NFR

| # | NFR | Comment |
| --- | --- | --- |
| 1 | Availability | 24x7* |
| 2 | API Latency : Expected average response time under normal load | 15 sec* |
| 3 | Stress Load : Max Concurrent User/Applications: | 60* |
| 4 | Stress Load : Max Concurrent Request (per hour): | 9344 |
| 5 | Endurance(Soak test) : response time under sustained load | Load % : 1x Duration : 12 hours |
| 6 | Average CPU usage | < 50% |
| 7 | Memory Usage | < 80% |

### Volumetrics and Flows

**We define peak hour as 9344 API calls based on best estimation of combination of multiple different workflows. **

| **API** | **Name** |
| --- | --- |
| [https://uklvadapp1346.uk.dev.net:8868/v1/rules/validate](https://uklvadapp1346.uk.dev.net:8868/v1/rules/validate) | Rule Service Query |

**Body:**

```
{
"businessFlow": "FX_REPLICATE",
"ruleType": "FILTERING",
"scbml": "<scb:SCBML xmlns:scb=\"http://www.sc.com/SCBML-1\"           xmlns:cortexextn=\"http://www.sc.com/scbml/cortex-extension-1-0\"           xmlns:dsig=\"http://www.w3.org/2000/09/xmldsig#\"           xmlns:fpmlextn=\"http://www.fpml.org/FpML-5/ext\"           xmlns:conf=\"http://www.fpml.org/FpML-5/confirmation\"           xmlns:scbextn=\"http://www.sc.com/scbml/extension-2-0\"           xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"           scbmlVersion=\"4-0\"           xsi:schemaLocation=\"\">   <scb:correlationId correlationIdScheme=\"http://www.sc.com/coding-scheme/tradeLake/requestId\"/>   <scb:header>      <scb:messageDetails>         <scb:messageVersion>1.0</scb:messageVersion>         <scb:messageType>            <scb:typeName>TradeData</scb:typeName>         </scb:messageType>      </scb:messageDetails>      <scb:originationDetails>         <scb:messageSender>            <scb:messageSender systemScheme=\"http://www.sc.com/coding-scheme/system-1-0\">STELLA</scb:messageSender>            <scb:senderDomain>               <scb:domainName domainNameScheme=\"http://www.sc.com/coding-scheme/domainNamescheme-1-0\">FM</scb:domainName>               <scb:subDomainName>                  <scb:subDomainType>Blade</scb:subDomainType>               </scb:subDomainName>            </scb:senderDomain>            <scb:countryCode>ALL</scb:countryCode>         </scb:messageSender>         <scb:messageReceiver>            <scb:messageReceiver idType=\"http://www.sc.com/coding-scheme/ITAM-id\"                                 systemScheme=\"http://www.sc.com/coding-scheme/system-1-0\"/>         </scb:messageReceiver>         <scb:initiatedTimestamp>2024-01-11T10:42:26.000000Z</scb:initiatedTimestamp>         <scb:messageId>\"tlRawEventTime\":1704940946000,\"sourceSystem\":\"STELLA\",\"externalMessageId\":\"892cfc3d-7f12-4d26-8fc6-05aef73ea3a9\",\"correlationId\":\"100000777A\",\"topic\":\"tlclus3-sit-stella-raw\"</scb:messageId>         <scb:trackingId>STELLA.892cfc3d-7f12-4d26-8fc6-05aef73ea3a9</scb:trackingId>         <scb:temporalInformation>            <scb:temporality>               <scb:validFrom>2024-01-11T10:42:26.000000Z</scb:validFrom>               <scb:validTo>9999-12-31T00:00:00Z</scb:validTo>               <scb:transactionFrom>2024-01-11T10:42:26.000000Z</scb:transactionFrom>               <scb:transactionTo>9999-12-31T00:00:00Z</scb:transactionTo>            </scb:temporality>         </scb:temporalInformation>      </scb:originationDetails>      <scb:captureSystem>Blade</scb:captureSystem>      <scb:process>         <scb:eventType>Insert</scb:eventType>      </scb:process>   </scb:header>   <scb:payload>      <scb:payloadFormat>XML</scb:payloadFormat>      <scb:payloadType>fmpayload</scb:payloadType>      <scb:payloadVersion>4-0</scb:payloadVersion>      <scb:FPMLPayload>         <scb:header>            <scb:process>               <scb:state stateScheme=\"http://www.sc.com/coding-scheme/event/scbml-state\">valid</scb:state>               <scb:subState stateScheme=\"http://www.sc.com/coding-scheme/state/tradeWorkflowStatus\">TOBESENT</scb:subState>               <scb:subState stateScheme=\"http://www.sc.com/coding-scheme/state/physicalStatus\">Live</scb:subState>               <scb:event eventScheme=\"http://www.sc.com/coding-scheme/event/scbml-business-event\">Trade</scb:event>               <scb:transactionType transactionTypeScheme=\"http://www.sc.com/coding-scheme/action\">Book</scb:transactionType>               <scb:transactionType transactionTypeScheme=\"http://www.sc.com/coding-scheme/transactionType/lastAction\">Book</scb:transactionType>               <scb:eventId eventIdScheme=\"http://www.sc.com/coding-scheme/eventId\">892cfc3d-7f12-4d26-8fc6-05aef73ea3a9</scb:eventId>               <scb:eventVersion>0</scb:eventVersion>               <scb:actionedBy>                  <scb:id idScheme=\"http://www.sc.com/coding-scheme/actionedBy/Id\">1597692</scb:id>               </scb:actionedBy>               <scb:actionTimestamp>2024-01-11T10:42:26.000000Z</scb:actionTimestamp>               <scb:trackingVersion>0</scb:trackingVersion>            </scb:process>         </scb:header>         <conf:trade xsi:type=\"scbextn:Trade\">            <conf:tradeHeader xsi:type=\"scbextn:TradeHeader\">               <conf:partyTradeIdentifier>                  <conf:partyReference href=\"party1\"/>                  <conf:tradeId tradeIdScheme=\"http://www.sc.com/coding-scheme/tradeId/tradeLake/eventId\">Blade|-|2024-01-11T10:42:26.000000Z|-|892cfc3d-7f12-4d26-8fc6-05aef73ea3a9|-|100000777A</conf:tradeId>                  <conf:tradeId tradeIdScheme=\"http://www.sc.com/coding-scheme/tradeId\">100000777A</conf:tradeId>                  <conf:versionedTradeId xsi:type=\"scbextn:VersionedTradeId\">                     <conf:tradeId tradeIdScheme=\"http://www.sc.com/coding-scheme/tradeId/tradeLake\">100000777A</conf:tradeId>                     <conf:version>1</conf:version>                     <scbextn:minorVersion>0</scbextn:minorVersion>                  </conf:versionedTradeId>                  <conf:tradeId tradeIdScheme=\"http://www.sc.com/coding-scheme/tradeId/Blade\">pq71cf5wb0zzd2y</conf:tradeId>                  <conf:linkId linkIdScheme=\"http://www.sc.com/coding-scheme/linkId/executionId\">1234</conf:linkId>                  <conf:linkId linkIdScheme=\"http://www.sc.com/coding-scheme/linkId/tradeLake/externalMessageId\">892cfc3d-7f12-4d26-8fc6-05aef73ea3a9</conf:linkId>                  <conf:linkId linkIdScheme=\"http://www.sc.com/coding-scheme/linkId/tradeLake/correlationId\">100000777A</conf:linkId>                  <conf:originatingTradeId>                     <conf:issuer>party1</conf:issuer>                     <conf:tradeId tradeIdScheme=\"http://www.sc.com/coding-scheme/tradeId/originatingTradeId\">100000777A</conf:tradeId>                  </conf:originatingTradeId>               </conf:partyTradeIdentifier>               <conf:partyTradeIdentifier>                  <conf:partyReference href=\"executionFacility\"/>                  <conf:tradeId tradeIdScheme=\"http://www.sc.com/coding-scheme/tradeId\">1234</conf:tradeId>               </conf:partyTradeIdentifier>               <conf:partyTradeInformation xsi:type=\"scbextn:PartyTradeInformation\">                  <conf:partyReference href=\"party1\"/>                  <conf:relatedParty>                     <conf:partyReference href=\"party1\"/>                     <conf:role>Buyer</conf:role>                  </conf:relatedParty>                  <conf:relatedParty>                     <conf:partyReference href=\"party2\"/>                     <conf:role>Seller</conf:role>                  </conf:relatedParty>                  <conf:relatedParty>                     <conf:partyReference href=\"party2\"/>                     <conf:role>Counterparty</conf:role>                  </conf:relatedParty>                  <conf:relatedParty>                     <conf:partyReference href=\"executionFacility\"/>                     <conf:role>ExecutionFacility</conf:role>                  </conf:relatedParty>                  <conf:relatedParty>                     <conf:partyReference href=\"party2\"/>                     <conf:role>ReportingParty</conf:role>                  </conf:relatedParty>                  <conf:relatedParty>                     <conf:partyReference href=\"ultimateParent\"/>                     <conf:role>UltimateParent</conf:role>                  </conf:relatedParty>                  <conf:relatedBusinessUnit>                     <conf:businessUnitReference href=\"gLBusinessUnit\"/>                     <conf:role>GLBusinessUnit</conf:role>                  </conf:relatedBusinessUnit>                  <conf:relatedPerson>                     <conf:personReference href=\"coverageMarketer\"/>                     <conf:role>CoverageMarketer</conf:role>                  </conf:relatedPerson>                  <conf:relatedPerson>                     <conf:personReference href=\"executionMarketer\"/>                     <conf:role>ExecutionMarketer</conf:role>                  </conf:relatedPerson>                  <conf:relatedPerson>                     <conf:personReference href=\"bookingMarketer\"/>                     <conf:role>BookingMarketer</conf:role>                  </conf:relatedPerson>                  <conf:relatedPerson>                     <conf:personReference href=\"trader\"/>                     <conf:role>Trader</conf:role>                  </conf:relatedPerson>                  <conf:relatedPerson>                     <conf:personReference href=\"tPSystemLastUpdatedBy\"/>                     <conf:role>TPSystemLastUpdatedBy</conf:role>                  </conf:relatedPerson>                  <conf:relatedPerson>                     <conf:personReference href=\"tPSystemCreatedBy\"/>                     <conf:role>TPSystemCreatedBy</conf:role>                  </conf:relatedPerson>                  <conf:executionDateTime>2024-01-11T10:42:26.000000Z</conf:executionDateTime>                  <conf:timestamps>                     <conf:timestamp>                        <conf:type>TPSystemCapture</conf:type>                        <conf:value>2024-01-11T10:42:26.000000Z</conf:value>                     </conf:timestamp>                     <conf:timestamp>                        <conf:type>TPSystemLastUpdated</conf:type>                        <conf:value>2024-01-11T10:42:26.000000Z</conf:value>                     </conf:timestamp>                     <conf:timestamp>                        <conf:type>EffectiveDateTime</conf:type>                        <conf:value>2024-01-11T10:42:26.000000Z</conf:value>                     </conf:timestamp>                     <conf:timestamp>                        <conf:type>TLLatestEventTime</conf:type>                        <conf:value>2024-01-11T10:42:26.000000Z</conf:value>                     </conf:timestamp>                     <conf:timestamp>                        <conf:type>TLRawEventTime</conf:type>                        <conf:value>2024-01-11T10:42:26.000000Z</conf:value>                     </conf:timestamp>                  </conf:timestamps>                  <conf:executionType executionTypeScheme=\"http://www.fpml.org/coding-scheme/execution-type\">Voice</conf:executionType>                  <conf:executionVenueType executionVenueTypeScheme=\"http://www.fpml.org/coding-scheme/execution-venue-type\">OTF</conf:executionVenueType>                  <conf:confirmationMethod confirmationMethodScheme=\"http://www.fpml.org/coding-scheme/confirmation-method\">N</conf:confirmationMethod>                  <conf:compressedTrade>false</conf:compressedTrade>                  <scbextn:isNovationTrade>false</scbextn:isNovationTrade>                  <scbextn:clientClearing>false</scbextn:clientClearing>                  <scbextn:tradeSource tradeSourceScheme=\"http://www.sc.com/coding-scheme/tradeSource/transactionProcessing\">                     <scbextn:name>SABRE</scbextn:name>                  </scbextn:tradeSource>                  <scbextn:tradeSource tradeSourceScheme=\"http://www.sc.com/coding-scheme/tradeSource/originalSourceSystem\">                     <scbextn:name>Blade</scbextn:name>                  </scbextn:tradeSource>                  <scbextn:tradeSource tradeSourceScheme=\"http://www.sc.com/coding-scheme/tradeSource/executionSystem\">                     <scbextn:name>BLADE</scbextn:name>                  </scbextn:tradeSource>                  <scbextn:isClientTrade>false</scbextn:isClientTrade>                  <scbextn:excludeFromCSA>false</scbextn:excludeFromCSA>                  <scbextn:isFXSecuritiesConversionTrade>false</scbextn:isFXSecuritiesConversionTrade>                  <scbextn:isClientConsent>true</scbextn:isClientConsent>                  <scbextn:contractTenor>                     <conf:periodMultiplier>1</conf:periodMultiplier>                     <conf:period>D</conf:period>                  </scbextn:contractTenor>                  <scbextn:tradeInterventionFlag>false</scbextn:tradeInterventionFlag>                  <scbextn:isClientLeg>false</scbextn:isClientLeg>                  <scbextn:isRevenueSharedBetweenUnits>false</scbextn:isRevenueSharedBetweenUnits>               </conf:partyTradeInformation>               <conf:productSummary xsi:type=\"scbextn:ProductSummary\">                  <conf:settlementType>Physical</conf:settlementType>                  <scbextn:priceConvention>                     <scbextn:priceMultiplier>1</scbextn:priceMultiplier>                  </scbextn:priceConvention>               </conf:productSummary>               <conf:tradeDate>2024-01-11</conf:tradeDate>               <scbextn:settlementDate>2024-01-11</scbextn:settlementDate>               <scbextn:positionId positionIdScheme=\"http://www.sc.com/coding-scheme/positionId\">100000777A</scbextn:positionId>            </conf:tradeHeader>            <scbextn:fxSingleLeg>               <conf:primaryAssetClass assetClassScheme=\"http://www.sc.com/coding-scheme/primaryAssetClass\">ForeignExchange</conf:primaryAssetClass>               <conf:productType productTypeScheme=\"http://www.sc.com/coding-scheme/productType/Blade\">ForeignExchange:Forward</conf:productType>               <conf:productType productTypeScheme=\"http://www.sc.com/coding-scheme/external/product-classification/financialInstrumentCode\">JFXXXX</conf:productType>               <conf:productType productTypeScheme=\"http://www.sc.com/coding-scheme/productType/baseProduct\">Forward</conf:productType>               <conf:productType productTypeScheme=\"http://www.sc.com/coding-scheme/productType/subProduct\">FX Forward</conf:productType>               <conf:productType productTypeScheme=\"http://www.fpml.org/coding-scheme/external/product-classification/iso10962\">IFXXXP</conf:productType>               <conf:productId productIdScheme=\"http://www.fpml.org/coding-scheme/product-taxonomy\">ForeignExchange:Forward</conf:productId>               <conf:productId productIdScheme=\"http://www.sc.com/coding-scheme/productId/UUID\">c9325a84-3976-45b6-9474-3e6b0ec20bd2</conf:productId>               <conf:productId productIdScheme=\"http://www.sc.com/coding-scheme/productId/UPI\">10002</conf:productId>               <conf:productId productIdScheme=\"http://www.fpml.org/coding-scheme/external/instrument-id-ISIN-1-0\">None.NotRequired</conf:productId>               <conf:exchangedCurrency1>                  <conf:payerPartyReference href=\"party2\"/>                  <conf:receiverPartyReference href=\"party1\"/>                  <conf:paymentAmount>                     <conf:currency currencyScheme=\"http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15\">CNO</conf:currency>                     <conf:amount>1000.00</conf:amount>                  </conf:paymentAmount>               </conf:exchangedCurrency1>               <conf:exchangedCurrency2>                  <conf:payerPartyReference href=\"party1\"/>                  <conf:receiverPartyReference href=\"party2\"/>                  <conf:paymentAmount>                     <conf:currency currencyScheme=\"http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15\">USD</conf:currency>                     <conf:amount>139.16</conf:amount>                  </conf:paymentAmount>               </conf:exchangedCurrency2>               <conf:dealtCurrency>ExchangedCurrency1</conf:dealtCurrency>               <conf:valueDate>2024-01-11</conf:valueDate>               <conf:exchangeRate>                  <conf:quotedCurrencyPair>                     <conf:currency1 currencyScheme=\"http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15\">CNO</conf:currency1>                     <conf:currency2 currencyScheme=\"http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15\">USD</conf:currency2>                     <conf:quoteBasis>Currency2PerCurrency1</conf:quoteBasis>                  </conf:quotedCurrencyPair>                  <conf:rate>0.139160000000</conf:rate>                  <conf:spotRate>0.100000000000</conf:spotRate>                  <conf:forwardPoints>0.039160000000</conf:forwardPoints>               </conf:exchangeRate>            </scbextn:fxSingleLeg>            <scbextn:pricing>               <scbextn:partyReference href=\"party1\"/>               <scbextn:valuationSet>                  <conf:assetValuation>                     <conf:quote>                        <conf:value>0.039160000000</conf:value>                        <conf:measureType assetMeasureScheme=\"http://www.sc.com/coding-scheme/asset-measure\">GrossForwardSpread</conf:measureType>                     </conf:quote>                  </conf:assetValuation>                  <conf:assetValuation>                     <conf:quote>                        <conf:value>0.13916</conf:value>                        <conf:measureType assetMeasureScheme=\"http://www.sc.com/coding-scheme/asset-measure\">TransactedGrossPrice</conf:measureType>                     </conf:quote>                  </conf:assetValuation>                  <conf:assetValuation>                     <conf:quote>                        <conf:value>0.100000000000</conf:value>                        <conf:measureType assetMeasureScheme=\"http://www.sc.com/coding-scheme/asset-measure\">GrossSpotRate</conf:measureType>                     </conf:quote>                  </conf:assetValuation>                  <conf:assetValuation>                     <conf:quote>                        <conf:value>0.000000000000</conf:value>                        <conf:measureType assetMeasureScheme=\"http://www.sc.com/coding-scheme/asset-measure\">SpotMargin</conf:measureType>                        <conf:quoteUnits priceQuoteUnitsScheme=\"http://www.sc.com/coding-scheme/price-quote-units\">ExchangeRate</conf:quoteUnits>                     </conf:quote>                  </conf:assetValuation>                  <conf:assetValuation>                     <conf:quote>                        <conf:value>0.000000000000</conf:value>                        <conf:measureType assetMeasureScheme=\"http://www.sc.com/coding-scheme/asset-measure\">ForwardMargin</conf:measureType>                        <conf:quoteUnits priceQuoteUnitsScheme=\"http://www.sc.com/coding-scheme/price-quote-units\">ExchangeRate</conf:quoteUnits>                     </conf:quote>                  </conf:assetValuation>               </scbextn:valuationSet>               <scbextn:commissions>                  <scbextn:commission id=\"fixedMarketerCommission\">                     <conf:commissionDenomination>FixedAmount</conf:commissionDenomination>                     <conf:commissionAmount>0</conf:commissionAmount>                     <conf:currency currencyScheme=\"http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15\">USD</conf:currency>                  </scbextn:commission>                  <scbextn:commission id=\"marketerCommission\">                     <conf:commissionDenomination>FixedAmount</conf:commissionDenomination>                     <conf:commissionAmount>0</conf:commissionAmount>                     <conf:currency currencyScheme=\"http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15\">USD</conf:currency>                  </scbextn:commission>               </scbextn:commissions>            </scbextn:pricing>         </conf:trade>         <conf:party id=\"party1\">            <conf:partyId>party1</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.fpml.org/coding-scheme/external/iso17442\">549300VGE7QN15BPTZ72</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.sc.com/coding-scheme/partyId/LEID\">11202982</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.sc.com/coding-scheme/partyId/subprofileId\">10</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.sc.com/coding-scheme/partyId/FMID\">400054741</conf:partyId>            <conf:country countryScheme=\"http://www.fpml.org/coding-scheme/external/iso3166\">CN</conf:country>            <conf:businessUnit id=\"gLBusinessUnit\">               <conf:name>SCB (CN) Ltd. Chengdu Branch</conf:name>               <conf:businessUnitId>620</conf:businessUnitId>            </conf:businessUnit>            <conf:person id=\"coverageMarketer\">               <conf:personId personIdScheme=\"http://www.sc.com/coding-scheme/personId/PSID\">1597692</conf:personId>            </conf:person>            <conf:person id=\"executionMarketer\">               <conf:personId personIdScheme=\"http://www.sc.com/coding-scheme/personId/PSID\">1597692</conf:personId>            </conf:person>            <conf:person id=\"bookingMarketer\">               <conf:personId personIdScheme=\"http://www.sc.com/coding-scheme/personId/PSID\">1597692</conf:personId>            </conf:person>            <conf:person id=\"trader\">               <conf:personId personIdScheme=\"http://www.sc.com/coding-scheme/personId/PSID\">1230004</conf:personId>            </conf:person>            <conf:person id=\"tPSystemLastUpdatedBy\">               <conf:personId personIdScheme=\"http://www.sc.com/coding-scheme/personId/PSID\">1597692</conf:personId>            </conf:person>            <conf:person id=\"tPSystemCreatedBy\">               <conf:personId personIdScheme=\"http://www.sc.com/coding-scheme/personId/PSID\">1597692</conf:personId>            </conf:person>            <scbextn:additionalPartyName>               <scbextn:type>EntityLabel</scbextn:type>               <scbextn:name>CHENGDU</scbextn:name>            </scbextn:additionalPartyName>            <scbextn:additionalCountryRegion>               <scbextn:type>LegalEntity</scbextn:type>               <scbextn:country countryScheme=\"http://www.fpml.org/coding-scheme/external/iso3166\">CN</scbextn:country>               <scbextn:region regionScheme=\"http://www.fpml.org/coding-scheme/region\">ASIA</scbextn:region>            </scbextn:additionalCountryRegion>            <scbextn:additionalCountryRegion>               <scbextn:type>Incorporated</scbextn:type>               <scbextn:country countryScheme=\"http://www.fpml.org/coding-scheme/external/iso3166\">CN</scbextn:country>            </scbextn:additionalCountryRegion>         </conf:party>         <conf:party id=\"party2\">            <conf:partyId partyIdScheme=\"http://www.sc.com/coding-scheme/partyId/FMID\">400095464</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.fpml.org/coding-scheme/external/iso17442\">549300VGE7QN15BPTZ72</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.sc.com/coding-scheme/partyId/LEID\">11202982</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.sc.com/coding-scheme/partyId/subprofileId\">10</conf:partyId>            <conf:partyName>SC_IRCD_BTB</conf:partyName>            <conf:classification industryClassificationScheme=\"http://www.sc.com/coding-scheme/counterparty-classification-segment\">S</conf:classification>            <conf:classification industryClassificationScheme=\"http://www.sc.com/coding-scheme/counterparty-classification-subsegment\">S1</conf:classification>            <conf:classification industryClassificationScheme=\"http://www.sc.com/coding-scheme/partyClassification/CDDCategory\">Applicable</conf:classification>            <conf:classification industryClassificationScheme=\"http://www.sc.com/coding-scheme/partyClassification/CDDSubCategory\">Eligible</conf:classification>            <conf:country countryScheme=\"http://www.fpml.org/coding-scheme/external/iso3166\">CN</conf:country>            <conf:contactInfo>               <conf:email>PORTFOLIO.RECONCILIATION@SC.COM</conf:email>            </conf:contactInfo>            <scbextn:additionalPartyName>               <scbextn:type>LongName</scbextn:type>               <scbextn:name>STANDARD CHARTERED BANK (CHINA) LIMITED</scbextn:name>            </scbextn:additionalPartyName>            <scbextn:additionalCountryRegion>               <scbextn:type>Incorporated</scbextn:type>               <scbextn:country countryScheme=\"http://www.fpml.org/coding-scheme/external/iso3166\">CN</scbextn:country>            </scbextn:additionalCountryRegion>         </conf:party>         <conf:party id=\"executionFacility\">            <conf:partyId partyIdScheme=\"http://www.fpml.org/coding-scheme/external/exchange-id-MIC-1-0\">BGCO</conf:partyId>            <conf:partyId partyIdScheme=\"http://www.fpml.org/coding-scheme/external/iso17442\">ZWNFQ48RUL8VJZ2AIC12</conf:partyId>            <conf:partyName>BGC BROKERS LP - OTF</conf:partyName>         </conf:party>         <conf:party id=\"ultimateParent\">            <conf:partyId partyIdScheme=\"http://www.fpml.org/coding-scheme/external/iso17442\">RILFO74KP1CM8P6PCT96</conf:partyId>         </conf:party>         <scb:tradePortfolio id=\"booking\">            <conf:partyPortfolioName>               <conf:partyReference href=\"party1\"/>               <conf:portfolioName>BTB_CHENGDU_IR_STL</conf:portfolioName>               <conf:portfolioName portfolioNameScheme=\"http://www.sc.com/coding-scheme/portfolioUniqueName\">SABRE||BTB_CHENGDU_IR_STL</conf:portfolioName>            </conf:partyPortfolioName>            <scbextn:volckerReporting>               <scbextn:volckerBusinessLine>Rates</scbextn:volckerBusinessLine>            </scbextn:volckerReporting>            <scbextn:portfolioOwner>               <scbextn:person>                  <conf:personId>1348375</conf:personId>               </scbextn:person>            </scbextn:portfolioOwner>            <scbextn:hierarchy>               <scbextn:type hierarchyTypeScheme=\"http://www.sc.com/coding-scheme/portfolio/hierarchyType\">BusinessHierarchy</scbextn:type>               <scbextn:hierarchyLevels>                  <scbextn:level>L1</scbextn:level>                  <scbextn:value>|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Rates|EM Rates|EM Rates - Greater China</scbextn:value>               </scbextn:hierarchyLevels>            </scbextn:hierarchy>            <scbextn:portfolioId portfolioIdScheme=\"http://www.sc.com/coding-scheme/portfolioId\">99016</scbextn:portfolioId>            <scbextn:portfolioType portfolioTypeScheme=\"http://www.sc.com/coding-scheme/portfolioType\">Risk Portfolio</scbextn:portfolioType>         </scb:tradePortfolio>      </scb:FPMLPayload>   </scb:payload></scb:SCBML>"
}
```

**Steps：**

```
ssh ratanrt@10.198.199.160
Passwd: ******
cd /apps/ratanrt/jeffrey/git
git clone https://bitbucket.global.standardchartered.com/scm/ratanrt/ratanone-performancetest-api.git
cd /apps/ratanrt/jeffrey/git/ratanone-performancetest-api/cn/\query_cashflows_new_loop
/apps/ratanrt/goldenversions/apache-jmeter-5.5/bin/jmeter -n -t query_cashflows.jmx -l ./report/result.jtl -e -o ./report -JthreadNumber=25 -Jduration=900
rm -rf ./report

#Check Report
nohup python -m SimpleHTTPServer 8888 &
http://10.198.199.160:8888/report/
```

**Test Strategy：**

| **User Case** | API Name & Param | Response |
| --- | --- | --- |
| Concurrent User/Applications (pcs) | Duration (s) | Sample (pcs) | 90% Line (ms) | 99% Line (ms) | Error Rate (%) | Throughtput (pcs/s) | Query/s | Received (KB/sec) | Comment |
| Check Trade Validation | 1 | 600 | | | | | | | | |
| 10 | 600 | | | | | | | | |
| 30 | 600 | | | | | | | | |
| 40 | 600 | | | | | | | | |
| 60 | 600 | | | | | | | | |

Below is the JMeter script follow upon user case.

[https://bitbucket.global.standardchartered.com/projects/RATANRT/repos/ratanone-performancetest-api/browse](https://bitbucket.global.standardchartered.com/projects/RATANRT/repos/ratanone-performancetest-api/browse)

*P.S. *Statements in parentheses *in "User Case" means happen by chance.*

**EXPAND_END**

**EXPAND: 3. Performance Test Environment Analysis**

## 3.  Performance Test Environment Analysis

Below table and diagrams contain a logical description of the PT environment with the table describing the differences between PT and Production environments. For each difference, the impact on the validity of performance testing and impact on PT results has been captured

**
**

**System Architecture:**

****

**Client Side Environment Details**

| | System Type | CPU Processor | Memory (RAM) | Display Resolution |
| --- | --- | --- | --- | --- |
| Dell Laptop | Windows 10 64-bit operating system, x64-based processor | Intel(R) Core(TM) i5-10310U CPU @ 1.70GHz 2.21 GHz | 16.0 GB (15.6 GB usable) | 1920 x 1080 |

**PT Servier Side Environment Details**

| Hostname | Type | IP Address | Env | System Model | Processor Clock Rate(MHz) | Cores | Processor Model | System Description | Memory Configured (GB) | DC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uklvadapp1341 | App-X86 | 10.198.199.161 | UAT/Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |
| uklvadapp1342 | App-X86 | 10.198.199.162 | UAT/Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |
| uklvadapp1343 | App-X86 | 10.198.199.163 | UAT/Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |
| uklvadapp1344 | App-X86 | 10.198.199.164 | UAT/Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |
| uklvadapp1345 | App-X86 | 10.198.199.165 | UAT/Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |
| uklvadapp1346 | App-X86 | 10.198.199.166 | UAT/Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |

**Production Servier Side Environment details**

| Hostname | Type | IP Address | Env | System Model | Processor Clock Rate(MHz) | Cores | Processor Model | System Description | Memory Configured (GB) | DC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uklvapapp590 | App-X86 | 10.4.194.78 | Production | VMware Virtual Platform | 2095 | 16 | Intel(R) Xeon(R) Gold 6152 | RHEL Server release 7.7 | 64 | ARK |
| uklvasapp590 | App-X86 | 10.4.194.179 | Production | VMware Virtual Platform | 2095 | 16 | Intel(R) Xeon(R) Gold 6152 | RHEL Server release 7.7 | 64 | WT |
| uklvapapp591 | App-X86 | 10.4.194.79 | Production | VMware Virtual Platform | 2095 | 16 | Intel(R) Xeon(R) Gold 6152 | RHEL Server release 7.7 | 64 | ARK |
| uklvasapp591 | App-X86 | 10.4.194.180 | Production | VMware Virtual Platform | 2095 | 16 | Intel(R) Xeon(R) Gold 6152 | RHEL Server release 7.7 | 64 | WT |
| uklvapapp676 | App-X86 | 10.4.197.46 | Production | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | ARK |
| uklvasapp676 | App-X86 | 10.4.197.146 | Production | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 7.7 | 64 | WT |
| uklvapdbs047 | DB-X86 | 10.4.200.206 | Production | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.2(Ootpa) | 64 | WT |
| uklvasdbs047 | DB-X86 | 10.4.200.226 | Production | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.2(Ootpa) | 64 | WT |

The capacity of PT environments is the same as production environment, so we expect similar behavior and performance between production environment and PT environment.

**EXPAND_END**

**EXPAND: 4. RAID**

# 4. RAID

List all risks and issues that could adversely impact testing. List All assumption and dependencies on the execution of performance testing

### Risk and Issues

| # | Risk/Issue Description | Severity H/M/L | Probability H/M/L | Mitigation Plan | Owner |
| --- | --- | --- | --- | --- | --- |
| 1 | PT is designed according to our best estimation on how it will be used in PROD. Once the application is live in PROD, we'll adjust the test cases based on real user behaviors and use cases and re-test accordingly. | L | L | Re-test based on MVP user behaviors and use cases. | Dev team |

### Key Assumptions and Dependencies

| # | Assumption/Dependency | Rationale | Impact | Owner |
| --- | --- | --- | --- | --- |
| 1 | External Dependencies/systems will exhibit at least same performance, if not better, in PROD environment comparing to PT environment | PROD normally comes with LB and have better capacity/performance. | Slowing down of dependencies/ systems will result in slowing down of API calls relating to them. | @Jialin Wang |

**EXPAND_END**

**EXPAND: 5. Scope**

5.  Scope

Table details the upstream and downstream interfaces. if not tested a clear rationale behind why that will not be the case. Details all other out of scope items for performance testing and rationale:

## Interfaces

| Interface | Direction | In/out scope | Rationale for not in scope |
| --- | --- | --- | --- |
| TDS3+SSI+DQSL | Upstream | In | |
| STELLA | Downstream | In | |
| BACKEND API | Upstream | In | |

## Out of Scope

| Item | Rationale for not in scope |
| --- | --- |
| NA | NA |

**EXPAND_END**

**EXPAND: 6. Test Approach**

# 6.  Test Approach

Full details of UI and Live messaging tests including Workmix and flows all adjustments to production volumetrics should be detailed and assumptions and adjustments explained fully. It should include elements of any of the following UI, MQ, API, REST etc –Include all non batch flows that are to be tested..

## 6.1 Workflow Description

the rule service is a service provider, as a consumer trade service will call validation api.

Scenario Flow Description

| Use Case | Detail |
| --- | --- |
| Trade Validation | Verify trades by rules |

## 6.2 Data Requirements

This section will detail the data requirements of the performance testing including batch files and backend databases.  These sections detail these requirements strategy and teams that will own the data population and file creations, note please state if data is not a production cut or data does not match production volumetrics and if not the rationale of why this will not impact performance results.

### Not include.

## 6.3 Tooling and Monitoring

Details of all test tools including monitoring and execution tools. Details of all Metrics being taken as part of the test execution. Minimum monitoring should be – CPU, Memory, IO, Garbage Collection

| Tool/Monitoring | Usage | Coverage |
| --- | --- | --- |
| Jmeter | JMeter is an open source solution, that can be used as a load testing tool for analyzing and measuring the performance of a variety of services, with a focus on web applications. | API end to end request and response performance test, As of now overall 4.5transactions/Second are happening by giving user thread number as 80 |
| Kibana | monitoing server's performance | Web server CPU, Memory, IO , GC |
| Grafana | monitoring HBase performance | HBase server CPU usage, Memory usage, Load , IO |

## 6.4 Execution Checklist

List of Activities that is required before each test can be Run. Details of the area where issues and defects are being tracked. If JIRA project this should be linked here.

### Pre and Post Execution checklist

| Activity | Description | Owner |
| --- | --- | --- |
| BACK-END API | All Backend Service including BFF Should be Up and connected. Received response should be available within time. | Dev Team |

**EXPAND_END**

**EXPAND: 7. Test Result**

# 7. Test Result

This section is tracking PT result. Track details report as below.

| **Test Case** | API Name & Param | JMeter Moniter | Server Monitor |
| --- | --- | --- | --- |
| Concurrent Users/Applications (pcs) | Duration (s) | Sample (pcs) | 90% Line (ms) | 99% Line (ms) | Error Rate (%) | Throughtput (pcs/s) | Sent (KB/sec) | Received (KB/sec) | CPU usage | Memory usage |
| Check Trade Validation | 1 | 600 | 922 | 745.70 | 851.54 | 0.00% | 1.54 | 40.09 | 1.80 | <28% | <75% |
| 10 | 600 | 6628 | 1622.00 | 2836.13 | 0.00% | 11.04 | 288.25 | 12.96 | <29% | <75.1% |
| 15 | 600 | 5935 | 5387.00 | 7209.92 | 0.00% | 9.86 | 257.43 | 11.57 | <31% | <74.8% |
| **20** | **600** | **5680** | **8061.90** | **12055.19** | **0.00%** | **9.42** | **245.95** | **11.06** | <24% | <74.9% |
| 30 | 600 | 9264 | 12295.50 | 16923.35 | 0.00% | 10.17 | 265.64 | 11.94 | <30% | <75% |

**Conclusion**

In uat/prod env rule service will have 6 instance which can provide 6 times capacity, the applications which are the consumer of rules service will not overload.

| Scenarios | Rule Service Instance | Consumer Applications | Test Status |
| --- | --- | --- | --- |
| Support Trade Service Only | 6 | 6 | PASS |
| Onboard 3 time new services | 6 | 18 | PASS |
| Max Consumers | 6 | 120 | PASS |

Evidence

| Case | Case 1 | Case 2 | Case 3 | Case 4 | Case 5 |
| --- | --- | --- | --- | --- | --- |
| Concurrent Users | 1 | 10 | 15 | 20 | 30 |
| Test Report | ![Screen Shot 2024-01-15 at 18.25.45.png](attachments/Screen Shot 2024-01-15 at 18.25.45.png) | ![Screen Shot 2024-01-15 at 18.24.45.png](attachments/Screen Shot 2024-01-15 at 18.24.45.png) | ![Screen Shot 2024-01-15 at 18.27.59.png](attachments/Screen Shot 2024-01-15 at 18.27.59.png) | ![Screen Shot 2024-01-15 at 18.49.58.png](attachments/Screen Shot 2024-01-15 at 18.49.58.png) | ![Screen Shot 2024-01-16 at 09.18.06.png](attachments/Screen Shot 2024-01-16 at 09.18.06.png) |
| CPU usage | ![Screen Shot 2024-01-15 at 18.44.29.png](attachments/Screen Shot 2024-01-15 at 18.44.29.png) | ![Screen Shot 2024-01-15 at 18.39.12.png](attachments/Screen Shot 2024-01-15 at 18.39.12.png) | ![Screen Shot 2024-01-15 at 18.46.22.png](attachments/Screen Shot 2024-01-15 at 18.46.22.png) | ![Screen Shot 2024-01-15 at 18.52.31.png](attachments/Screen Shot 2024-01-15 at 18.52.31.png) | ![Screen Shot 2024-01-16 at 09.29.53.png](attachments/Screen Shot 2024-01-16 at 09.29.53.png) |
| Memory usage | ![Screen Shot 2024-01-15 at 18.42.10.png](attachments/Screen Shot 2024-01-15 at 18.42.10.png) | ![Screen Shot 2024-01-15 at 18.40.38.png](attachments/Screen Shot 2024-01-15 at 18.40.38.png) | ![Screen Shot 2024-01-15 at 18.48.52.png](attachments/Screen Shot 2024-01-15 at 18.48.52.png) | ![Screen Shot 2024-01-15 at 18.51.29.png](attachments/Screen Shot 2024-01-15 at 18.51.29.png) | ![Screen Shot 2024-01-16 at 09.30.18.png](attachments/Screen Shot 2024-01-16 at 09.30.18.png) |

**EXPAND_END**