# Component view

# Logic  workflow

# Interface design

## Stamping enriched URL for trade

| ENV | URL | Note |
| --- | --- | --- |
| UAT | [https://ratan-api.uk.dev.net:8453/v1/stampings/trade/enrich](https://ratan-api.uk.dev.net:8453/v1/stampings/trade/enrich) | |

| Attribute | Describe |
| --- | --- |
| Method | POST |
| Header | `Authorization: Basic base64encode(username+":"+password）//Basic c3J2LjUxNTEyLmNkdXBzLjAwMTpTdGFuZGFyZEAxMjM=` |
| Request Body | ```js { "trackingId": "MX_FXCASH_CONF_XXXX", "tradeId": "111", "productType": "spot", "message": "<Base64 trade scbml>" } ``` |
| Response Body (HTTP Status == 200) | ```js Spot/Forward/Bullion Spot/Bullion Forward/IRS/NDIRS/NDCCS { "trackingId": "MX_FXCXXXXXX", "tradeId": "111", "message": "<Base64 trade ssi enriched scbml>", "singleLegResult": [ { "direction": "Buyer", "code": "700400325", "message": "SCB_RECEIVE_UNIQUE_NOSTRO", "vostroResult": "SUCCESS", "nostroResult": "SUCCESS" }, { "direction": "Seller", "code": "700400323", "message": "SCB_PAY_UNIQUE_VOSTRO_UNIQUE_NOSTRO", "vostroResult": "SUCCESS", "nostroResult": "SUCCESS" } ], } Swap/ccs/Bullion Swap/ MTM CCS { "trackingId": "MX_FXCXXXXXX", "tradeId": "111", "message": "<Base64 trade ssi enriched scbml>", "nearLegResult": [ { "direction": "Buyer", "code": "700400325", "message": "SCB_RECEIVE_UNIQUE_NOSTRO", "vostroResult": "SUCCESS", "nostroResult": "SUCCESS" }, { "direction": "Seller", "code": "700400323", "message": "SCB_PAY_UNIQUE_VOSTRO_UNIQUE_NOSTRO", "vostroResult": "SUCCESS", "nostroResult": "SUCCESS" } ], "farLegResult": [ { "direction": "Buyer", "code": "700400325", "message": "SCB_RECEIVE_UNIQUE_NOSTRO", "vostroResult": "SUCCESS", "nostroResult": "SUCCESS" }, { "direction": "Seller", "code": "700400323", "message": "SCB_PAY_UNIQUE_VOSTRO_UNIQUE_NOSTRO", "vostroResult": "SUCCESS", "nostroResult": "SUCCESS" } ] } ``` |

## Response Code

| HTTP Status | sellResult | buyResult |
| --- | --- | --- |
| 200 | SCB_PAY_UNIQUE_VOSTRO_UNIQUE_NOSTRO("700400323") | SCB_RECEIVE_UNIQUE_NOSTRO("700400325") |
| 400 | SCB_PAY_BLANK_VOSTRO_DEFAULT_NOSTRO("700400320") SCB_PAY_BLANK_VOSTRO_BLANK_NOSTRO("700400321") SCB_PAY_UNIQUE_VOSTRO_BLANK_NOSTRO("700400322") CLIENT_DATA_INVALID_EXCEPTION("700400001") NOT_DEFINED_SCENARIO_ERROR("700400326") | SCB_RECEIVE_BLANK_NOSTRO("700400324") CLIENT_DATA_INVALID_EXCEPTION("700400001") NOT_DEFINED_SCENARIO_ERROR("700400326") |
| 500 | STAMPING_SERVICE_IO_EXCEPTION("700500002") | |

"vostroResult" and "nostroResult" available value list

| SUCCESS |
| --- |
| MISSING_VOSTRO_ERROR |
| MULTI_VOSTRO_ERROR |
| MISSING_NOSTRO_ERROR |
| MULTI_NOSTRO_ERROR |
| DEFAULT_NOSTRO |

## Request  SCBML file

**EXPAND: Request SCBML**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<scb:SCBML scbmlVersion="4-0" xmlns:conf="http://www.fpml.org/FpML-5/confirmation"
           xmlns:fpmlextn="http://www.fpml.org/FpML-5/ext" xmlns:scb="http://www.sc.com/SCBML-1"
           xmlns:scbextn="http://www.sc.com/scbml/extension-2-0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.sc.com/SCBML-1 ../../../../../../../core/4-0/scbml-4-0.xsd http://www.sc.com/SCBML-1 ../../../../../../../payloadType/fmPayload/4-0/scbml-fmpayload-4-0.xsd">
    <scb:header>
        <scb:messageDetails>
            <scb:messageVersion>1.0</scb:messageVersion>
            <scb:messageType>
                <scb:typeName>TradeData</scb:typeName>
            </scb:messageType>
        </scb:messageDetails>
        <scb:originationDetails>
            <scb:messageSender>
                <scb:messageSender systemScheme="http://www.sc.com/coding-scheme/system-1-0">Blade</scb:messageSender>
                <scb:senderDomain>
                    <scb:domainName domainNameScheme="http://www.sc.com/coding-scheme/domainNamescheme-1-0">FM
                    </scb:domainName>
                </scb:senderDomain>
                <scb:countryCode>ALL</scb:countryCode>
            </scb:messageSender>
            <scb:initiatedTimestamp>2022-08-11T07:07:58Z</scb:initiatedTimestamp>
            <scb:trackingId>882e7f22-147e-4965-9647-739452cb114d</scb:trackingId>
        </scb:originationDetails>
        <scb:captureSystem>Blade</scb:captureSystem>
        <scb:process>
            <scb:eventType>Insert</scb:eventType>
        </scb:process>
    </scb:header>
    <scb:payload>
        <scb:payloadFormat>XML</scb:payloadFormat>
        <scb:payloadType>fmpayload</scb:payloadType>
        <scb:payloadVersion>4-0</scb:payloadVersion>
        <scb:FPMLPayload>
            <scb:header>
                <scb:process>
                    <scb:event eventScheme="http://www.sc.com/coding-scheme/event/scbml-business-event">Trade
                    </scb:event>
                    <scb:transactionType transactionTypeScheme="http://www.sc.com/coding-scheme/action">Book
                    </scb:transactionType>
                    <scb:actionedBy>
                        <scb:id idScheme="http://www.sc.com/coding-scheme/actionedBy/Id">1597692</scb:id>
                    </scb:actionedBy>
                    <scb:actionTimestamp>2022-08-11T07:07:58Z</scb:actionTimestamp>
                </scb:process>
            </scb:header>
            <conf:trade xsi:type="scbextn:Trade">
                <conf:tradeHeader xsi:type="scbextn:TradeHeader">
                    <conf:partyTradeIdentifier>
                        <conf:partyReference href="party1"/>
                        <conf:tradeId tradeIdScheme="http://www.sc.com/coding-scheme/tradeId/Blade">0m04e090hwbz2eh
                        </conf:tradeId>
                        <conf:linkId linkIdScheme="http://www.sc.com/coding-scheme/linkId/executionId">1234
                        </conf:linkId>
                    </conf:partyTradeIdentifier>
                    <conf:partyTradeInformation xsi:type="scbextn:PartyTradeInformation">
                        <conf:partyReference href="party1"/>
                        <conf:relatedParty>
                            <conf:partyReference href="party2"/>
                            <conf:role>Counterparty</conf:role>
                        </conf:relatedParty>
                        <conf:relatedParty>
                            <conf:partyReference href="party2"/>
                            <conf:role>ReportingParty</conf:role>
                        </conf:relatedParty>
                        <conf:relatedParty>
                            <conf:partyReference href="executingBroker"/>
                            <conf:role>ExecutingBroker</conf:role>
                        </conf:relatedParty>
                        <conf:relatedPerson>
                            <conf:personReference href="coverageMarketer"/>
                            <conf:role>CoverageMarketer</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="executionMarketer"/>
                            <conf:role>ExecutionMarketer</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="bookingMarketer"/>
                            <conf:role>BookingMarketer</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="trader"/>
                            <conf:role>Trader</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="tPSystemLastUpdatedBy"/>
                            <conf:role>TPSystemLastUpdatedBy</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="tPSystemCreatedBy"/>
                            <conf:role>TPSystemCreatedBy</conf:role>
                        </conf:relatedPerson>
                        <conf:executionDateTime>2022-08-11T07:07:00Z</conf:executionDateTime>
                        <conf:timestamps>
                            <conf:timestamp>
                                <conf:type>TPSystemCapture</conf:type>
                                <conf:value>2022-08-11T07:07:58Z</conf:value>
                            </conf:timestamp>
                            <conf:timestamp>
                                <conf:type>TPSystemLastUpdated</conf:type>
                                <conf:value>2022-08-11T07:07:58Z</conf:value>
                            </conf:timestamp>
                            <conf:timestamp>
                                <conf:type>EffectiveDateTime</conf:type>
                                <conf:value>2022-08-11T07:07:00Z</conf:value>
                            </conf:timestamp>
                        </conf:timestamps>
                        <conf:executionType executionTypeScheme="http://www.fpml.org/coding-scheme/execution-type">
                            Voice
                        </conf:executionType>
                        <conf:executionVenueType
                                executionVenueTypeScheme="http://www.fpml.org/coding-scheme/execution-venue-type">
                            OffFacility
                        </conf:executionVenueType>
                        <scbextn:isNovationTrade>false</scbextn:isNovationTrade>
                        <scbextn:tradeSource
                                tradeSourceScheme="http://www.sc.com/coding-scheme/tradeSource/originalSourceSystem">
                            <scbextn:name>Blade</scbextn:name>
                        </scbextn:tradeSource>
                        <scbextn:tradeSource
                                tradeSourceScheme="http://www.sc.com/coding-scheme/tradeSource/executionSystem">
                            <scbextn:name>BLADE</scbextn:name>
                        </scbextn:tradeSource>
                        <scbextn:comments>
                            <scbextn:type>General_1</scbextn:type>
                            <scbextn:comment>test</scbextn:comment>
                        </scbextn:comments>
                    </conf:partyTradeInformation>
                    <conf:productSummary xsi:type="scbextn:ProductSummary">
                        <conf:settlementType>Physical</conf:settlementType>
                        <scbextn:priceConvention>
                            <scbextn:priceMultiplier>1</scbextn:priceMultiplier>
                        </scbextn:priceConvention>
                    </conf:productSummary>
                    <conf:tradeDate>2022-08-11</conf:tradeDate>
                </conf:tradeHeader>
                <scbextn:fxSingleLeg>
                    <conf:primaryAssetClass assetClassScheme="http://www.sc.com/coding-scheme/primaryAssetClass">
                        ForeignExchange
                    </conf:primaryAssetClass>
                    <conf:productType productTypeScheme="http://www.sc.com/coding-scheme/productType/Blade">
                        ForeignExchange:Spot
                    </conf:productType>
                    <conf:productId productIdScheme="http://www.fpml.org/coding-scheme/product-taxonomy">
                        ForeignExchange:Spot
                    </conf:productId>
                    <conf:productId productIdScheme="http://www.sc.com/coding-scheme/productId/UPI">10001
                    </conf:productId>
                    <conf:exchangedCurrency1>
                        <conf:payerPartyReference href="party2"/>
                        <conf:receiverPartyReference href="party1"/>
                        <conf:paymentAmount>
                            <conf:currency
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">EUR
                            </conf:currency>
                            <conf:amount>980392.16</conf:amount>
                        </conf:paymentAmount>
                    </conf:exchangedCurrency1>
                    <conf:exchangedCurrency2>
                        <conf:payerPartyReference href="party1"/>
                        <conf:receiverPartyReference href="party2"/>
                        <conf:paymentAmount>
                            <conf:currency
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD
                            </conf:currency>
                            <conf:amount>1000000.00</conf:amount>
                        </conf:paymentAmount>
                    </conf:exchangedCurrency2>
                    <conf:dealtCurrency>ExchangedCurrency1</conf:dealtCurrency>
                    <conf:valueDate>2022-08-15</conf:valueDate>
                    <conf:exchangeRate>
                        <conf:quotedCurrencyPair>
                            <conf:currency1
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">EUR
                            </conf:currency1>
                            <conf:currency2
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD
                            </conf:currency2>
                            <conf:quoteBasis>Currency2PerCurrency1</conf:quoteBasis>
                        </conf:quotedCurrencyPair>
                        <conf:rate>1.020000000000</conf:rate>
                    </conf:exchangeRate>
                </scbextn:fxSingleLeg>
                <scbextn:pricing>
                    <scbextn:partyReference href="party1"/>
                    <scbextn:valuationSet>
                        <conf:assetValuation>
                            <conf:quote>
                                <conf:value>10</conf:value>
                                <conf:measureType assetMeasureScheme="http://www.sc.com/coding-scheme/asset-measure">
                                    CVA
                                </conf:measureType>
                                <conf:currency
                                        currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">
                                    USD
                                </conf:currency>
                            </conf:quote>
                        </conf:assetValuation>
                        <conf:assetValuation>
                            <conf:quote>
                                <conf:value>20</conf:value>
                                <conf:measureType assetMeasureScheme="http://www.sc.com/coding-scheme/asset-measure">
                                    FVA
                                </conf:measureType>
                                <conf:currency
                                        currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">
                                    USD
                                </conf:currency>
                            </conf:quote>
                        </conf:assetValuation>
                        <conf:assetValuation>
                            <conf:quote>
                                <conf:value>1.020000000000</conf:value>
                                <conf:measureType assetMeasureScheme="http://www.sc.com/coding-scheme/asset-measure">
                                    TransactedGrossPrice
                                </conf:measureType>
                            </conf:quote>
                        </conf:assetValuation>
                        <conf:assetValuation>
                            <conf:quote>
                                <conf:value>0.000000000000</conf:value>
                                <conf:measureType assetMeasureScheme="http://www.sc.com/coding-scheme/asset-measure">
                                    SpotMargin
                                </conf:measureType>
                                <conf:quoteUnits
                                        priceQuoteUnitsScheme="http://www.sc.com/coding-scheme/price-quote-units">
                                    ExchangeRate
                                </conf:quoteUnits>
                            </conf:quote>
                        </conf:assetValuation>
                    </scbextn:valuationSet>
                    <scbextn:commissions>
                        <scbextn:commission id="marketerCommission">
                            <conf:commissionDenomination>FixedAmount</conf:commissionDenomination>
                            <conf:commissionAmount>40</conf:commissionAmount>
                            <conf:currency
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD
                            </conf:currency>
                        </scbextn:commission>
                        <scbextn:commission id="floatingMarketerCommission">
                            <conf:commissionDenomination>FixedAmount</conf:commissionDenomination>
                            <conf:commissionAmount>20</conf:commissionAmount>
                            <conf:currency
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD
                            </conf:currency>
                        </scbextn:commission>
                        <scbextn:commission id="fixedMarketerCommission">
                            <conf:commissionDenomination>FixedAmount</conf:commissionDenomination>
                            <conf:commissionAmount>20</conf:commissionAmount>
                            <conf:currency
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD
                            </conf:currency>
                        </scbextn:commission>
                        <scbextn:commission id="extraMarketerCommission">
                            <conf:commissionDenomination>FixedAmount</conf:commissionDenomination>
                            <conf:commissionAmount>20</conf:commissionAmount>
                            <conf:currency
                                    currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD
                            </conf:currency>
                        </scbextn:commission>
                    </scbextn:commissions>
                </scbextn:pricing>
            </conf:trade>
            <conf:party id="party1">
                <conf:partyId>NA</conf:partyId>
                <conf:person id="coverageMarketer">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1597692
                    </conf:personId>
                </conf:person>
                <conf:person id="executionMarketer">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1597692
                    </conf:personId>
                </conf:person>
                <conf:person id="bookingMarketer">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1597692
                    </conf:personId>
                </conf:person>
                <conf:person id="trader">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1632004
                    </conf:personId>
                </conf:person>
                <conf:person id="tPSystemLastUpdatedBy">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1597692
                    </conf:personId>
                </conf:person>
                <conf:person id="tPSystemCreatedBy">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1597692
                    </conf:personId>
                </conf:person>
            </conf:party>
            <conf:party id="party2">
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMID">400092120</conf:partyId>
                <conf:partyName>SNAME 400092120</conf:partyName>
            </conf:party>
            <conf:party id="executingBroker">
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMID">400638469</conf:partyId>
                <conf:partyName>360 TRADING NETWORKS INC BR AC NY-+-360 TRADING NETWORKS INC BROKER ACCOUNT
                </conf:partyName>
            </conf:party>
            <scb:tradePortfolio id="booking">
                <conf:partyPortfolioName>
                    <conf:partyReference href="party1"/>
                    <conf:portfolioName>ISAL-FX-SA</conf:portfolioName>
                </conf:partyPortfolioName>
            </scb:tradePortfolio>
        </scb:FPMLPayload>
    </scb:payload>
</scb:SCBML>


```

**EXPAND_END**

**EXPAND: spot input xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<scb:SCBML
        xmlns:je="java:dagger.rt.xslt.JmsEnricher"
        xmlns:fn="http://www.w3.org/2005/xpath-functions"
        xmlns:scb="http://www.sc.com/SCBML-1"
        xmlns:conf="http://www.fpml.org/FpML-5/confirmation"
        xmlns:scbextn="http://www.sc.com/scbml/extension-2-0"
        xmlns:mlssystem="java:java.lang.System"
        xmlns:smc="java:dagger.rt.xslt.StaticMappingCache"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:fpmlextn="http://www.fpml.org/FpML-5/ext"
        xmlns:ciu="java:dagger.rt.xslt.CountryInfoUtils"
        xmlns:saxon="http://saxon.sf.net/" scbmlVersion="4-0" xsi:schemaLocation="http://www.sc.com/SCBML-1 ../../../../../../core/4-0/scbml-4-0.xsd http://www.sc.com/SCBML-1 ../../../../../../payloadType/fmPayload/4-0/scbml-fmpayload-4-0.xsd">
    <scb:header>
        <scb:messageDetails>
            <scb:messageVersion>1.0</scb:messageVersion>
            <scb:messageType>
                <scb:typeName>Confirmation</scb:typeName>
                <scb:subType>
                    <scb:subTypeName>Confirmation</scb:subTypeName>
                </scb:subType>
            </scb:messageType>
        </scb:messageDetails>
        <scb:originationDetails>
            <scb:messageSender>
                <scb:messageSender systemScheme="http://www.sc.com/coding-scheme/system-1-0">MX_FXCASH</scb:messageSender>
                <scb:senderDomain>
                    <scb:domainName domainNameScheme="http://www.sc.com/coding-scheme/domainNamescheme-1-0">FM</scb:domainName>
                </scb:senderDomain>
                <scb:countryCode>KE</scb:countryCode>
            </scb:messageSender>
            <scb:initiatedTimestamp>2022-05-10T10:37:32Z</scb:initiatedTimestamp>
            <scb:trackingId>MX_FXCASH_CONF_241717169_1_1961588139_1652179054616</scb:trackingId>
        </scb:originationDetails>
        <scb:captureSystem>MX_FXCASH</scb:captureSystem>
        <scb:process>
            <scb:eventType>Insert</scb:eventType>
        </scb:process>
    </scb:header>
    <scb:payload>
        <scb:payloadFormat>XML</scb:payloadFormat>
        <scb:payloadType>fmpayload</scb:payloadType>
        <scb:payloadVersion>4-0</scb:payloadVersion>
        <scb:FPMLPayload>
            <scb:header>
                <scb:process>
                    <scb:state stateScheme="http://www.sc.com/coding-scheme/event/scbml-state">PendingCDUProduce</scb:state>
                    <scb:subState stateScheme="http://www.sc.com/coding-scheme/state/physicalStatus">live</scb:subState>
                    <scb:subState stateScheme="http://www.sc.com/coding-scheme/state/MX_FXCASH/physicalStatus">live</scb:subState>
                    <scb:subState stateScheme="http://www.sc.com/coding-scheme/state/confirmationWorkflowStatus">PendingGeneration</scb:subState>
                    <scb:subState stateScheme="http://www.sc.com/coding-scheme/state/confirmationEventStatus">mock</scb:subState>
                    <scb:event eventScheme="http://www.sc.com/coding-scheme/event/scbml-business-event">Trade</scb:event>
                    <scb:eventReason eventReasonScheme="http://www.sc.com/coding-scheme/eventReason">NEW</scb:eventReason>
                    <scb:transactionType transactionTypeScheme="http://www.sc.com/coding-scheme/action/MX_FXCASH">insertion</scb:transactionType>
                    <scb:transactionType transactionTypeScheme="http://www.sc.com/coding-scheme/transactionType/lastAction"/>
                </scb:process>
            </scb:header>
            <conf:trade xsi:type="scbextn:Trade">
                <conf:tradeHeader>
                    <conf:partyTradeIdentifier>
                        <conf:issuer issuerIdScheme="http://www.fpml.org/coding-scheme/external/cftc/issuer-identifier">party1</conf:issuer>
                        <conf:tradeId tradeIdScheme="http://www.fpml.org/coding-scheme/external/unique-transaction-identifier"/>
                    </conf:partyTradeIdentifier>
                    <conf:partyTradeIdentifier>
                        <conf:issuer issuerIdScheme="http://www.fpml.org/coding-scheme/external/issuer-identifier">party1</conf:issuer>
                        <conf:tradeId tradeIdScheme="http://www.fpml.org/coding-scheme/external/unique-transaction-identifier"/>
                    </conf:partyTradeIdentifier>
                    <conf:partyTradeIdentifier>
                        <conf:partyReference href="party1"/>
                        <conf:versionedTradeId>
                            <conf:tradeId tradeIdScheme="http://www.sc.com/coding-scheme/tradeId">241717169</conf:tradeId>
                            <conf:version>1</conf:version>
                        </conf:versionedTradeId>
                        <conf:tradeId tradeIdScheme="http://www.sc.com/coding-scheme/tradeId/sourceSystem">MX_FXCASH</conf:tradeId>
                        <conf:tradeId tradeIdScheme="http://www.sc.com/coding-scheme/tradeId/Dealhub"/>
                    </conf:partyTradeIdentifier>
                    <conf:partyTradeInformation xsi:type="scbextn:PartyTradeInformation">
                        <conf:partyReference href="party1"/>
                        <conf:relatedParty>
                            <conf:partyReference href="SCB_RAZOR_FX"/>
                            <conf:role>ReportingParty</conf:role>
                        </conf:relatedParty>
                        <conf:relatedParty>
                            <conf:partyReference href="_180533"/>
                            <conf:role>Counterparty</conf:role>
                        </conf:relatedParty>
                        <conf:relatedParty>
                            <conf:partyReference href="executingBroker"/>
                            <conf:role>ExecutingBroker</conf:role>
                        </conf:relatedParty>
                        <conf:relatedPerson>
                            <conf:personReference href="executionMarketer"/>
                            <conf:role>ExecutionMarketer</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="bookingMarketer"/>
                            <conf:role>BookingMarketer</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="tpSystemCreatedBy"/>
                            <conf:role>TPSystemCreatedBy</conf:role>
                        </conf:relatedPerson>
                        <conf:relatedPerson>
                            <conf:personReference href="tpSystemLastUpdatedBy"/>
                            <conf:role>TPSystemLastUpdatedBy</conf:role>
                        </conf:relatedPerson>
                        <conf:reportingRegime>
                            <conf:supervisorRegistration>
                                <conf:supervisoryBody/>
                            </conf:supervisorRegistration>
                            <conf:notionalType>Notional</conf:notionalType>
                        </conf:reportingRegime>
                        <conf:reportingRegime>
                            <conf:supervisorRegistration>
                                <conf:supervisoryBody/>
                            </conf:supervisorRegistration>
                            <conf:notionalType>Notional</conf:notionalType>
                        </conf:reportingRegime>
                        <conf:reportingRegime>
                            <conf:supervisorRegistration>
                                <conf:supervisoryBody/>
                            </conf:supervisorRegistration>
                            <conf:notionalType>Notional</conf:notionalType>
                        </conf:reportingRegime>
                        <conf:reportingRegime>
                            <conf:supervisorRegistration>
                                <conf:supervisoryBody/>
                            </conf:supervisorRegistration>
                            <conf:notionalType>Notional</conf:notionalType>
                        </conf:reportingRegime>
                        <conf:reportingRegime>
                            <conf:supervisorRegistration>
                                <conf:supervisoryBody/>
                            </conf:supervisorRegistration>
                            <conf:notionalType>Notional</conf:notionalType>
                        </conf:reportingRegime>
                        <conf:reportingRegime>
                            <conf:supervisorRegistration>
                                <conf:supervisoryBody/>
                            </conf:supervisorRegistration>
                            <conf:notionalType>Notional</conf:notionalType>
                        </conf:reportingRegime>
                        <conf:executionDateTime>2022-05-10T10:37:32Z</conf:executionDateTime>
                        <conf:timestamps>
                            <conf:timestamp>
                                <conf:type>TPSystemCapture</conf:type>
                                <conf:value>2022-04-01T10:37:30Z</conf:value>
                            </conf:timestamp>
                        </conf:timestamps>
                        <conf:offMarketPrice>false</conf:offMarketPrice>
                        <scbextn:isNovationTrade>false</scbextn:isNovationTrade>
                    </conf:partyTradeInformation>
                    <conf:tradeDate>2022-04-01</conf:tradeDate>
                </conf:tradeHeader>
                <scbextn:fxSingleLeg>
                    <conf:primaryAssetClass assetClassScheme="http://www.sc.com/coding-scheme/primaryAssetClass">ForeignExchange</conf:primaryAssetClass>
                    <conf:productType productTypeScheme="http://www.sc.com/coding-scheme/productType/MX_FXCASH">CURR|FXD|FXD</conf:productType>
                    <conf:productType productTypeScheme="http://www.sc.com/coding-scheme/productType/strategy"/>
                    <conf:productType productTypeScheme="http://www.sc.com/coding-scheme/productType/instrument">GBP/USD</conf:productType>
                    <conf:productType productTypeScheme="http://www.sc.com/coding-scheme/productType/typology">Outright</conf:productType>
                    <conf:productId productIdScheme="http://www.fpml.org/coding-scheme/product-taxonomy">ForeignExchange:Forward</conf:productId>
                    <conf:productType productTypeScheme="http://www.sc.com/coding-scheme/mx3/foreign-exchange/sub-product-type">Spot</conf:productType>
                    <conf:exchangedCurrency1>
                        <conf:payerPartyReference href="party2"/>
                        <conf:receiverPartyReference href="party1"/>
                        <conf:paymentAmount>
                            <conf:currency currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">GBP</conf:currency>
                            <conf:amount>86452840.00000000</conf:amount>
                        </conf:paymentAmount>
                        <conf:paymentDate>
                            <conf:unadjustedDate>2022-04-01</conf:unadjustedDate>
                            <conf:dateAdjustments>
                                <conf:businessDayConvention>FOLLOWING</conf:businessDayConvention>
                                <conf:businessCenters>
                                    <conf:businessCenter>GBLO</conf:businessCenter>
                                </conf:businessCenters>
                            </conf:dateAdjustments>
                        </conf:paymentDate>
                    </conf:exchangedCurrency1>
                    <conf:exchangedCurrency2>
                        <conf:payerPartyReference href="party1"/>
                        <conf:receiverPartyReference href="party2"/>
                        <conf:paymentAmount>
                            <conf:currency currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD</conf:currency>
                            <conf:amount>113754127.76810700</conf:amount>
                        </conf:paymentAmount>
                        <conf:paymentDate>
                            <conf:unadjustedDate>2022-04-01</conf:unadjustedDate>
                            <conf:dateAdjustments>
                                <conf:businessDayConvention>FOLLOWING</conf:businessDayConvention>
                                <conf:businessCenters>
                                    <conf:businessCenter>USNY</conf:businessCenter>
                                </conf:businessCenters>
                            </conf:dateAdjustments>
                        </conf:paymentDate>
                    </conf:exchangedCurrency2>
                    <conf:dealtCurrency>ExchangedCurrency1</conf:dealtCurrency>
                    <conf:valueDate>2022-04-01</conf:valueDate>
                    <conf:exchangeRate>
                        <conf:quotedCurrencyPair>
                            <conf:currency1 currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD</conf:currency1>
                            <conf:currency2 currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">GBP</conf:currency2>
                            <conf:quoteBasis>Currency1PerCurrency2</conf:quoteBasis>
                        </conf:quotedCurrencyPair>
                        <conf:rate>1.31579399553</conf:rate>
                        <conf:spotRate>1.31575</conf:spotRate>
                    </conf:exchangeRate>
                    <scbextn:spotDate>2022-04-05</scbextn:spotDate>
                </scbextn:fxSingleLeg>
            </conf:trade>
            <conf:party id="party1">
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/LEID">11045261</conf:partyId>
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMID">400823485</conf:partyId>
                <conf:partyName>SCBLKEN*NBO</conf:partyName>
                <conf:person id="tpSystemCreatedBy">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/MX_FXCASH">1644409</conf:personId>
                </conf:person>
                <conf:person id="tpSystemLastUpdatedBy">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/MX_FXCASH">1644409|KE_TR_FX</conf:personId>
                </conf:person>
                <conf:person id="executionMarketer">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID">1644409</conf:personId>
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/MX_FXCASH">1644409</conf:personId>
                </conf:person>
                <conf:person id="bookingMarketer">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/MX_FXCASH">1644409</conf:personId>
                </conf:person>
                <conf:person id="coverageMarketer">
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/PSID"/>
                    <conf:personId personIdScheme="http://www.sc.com/coding-scheme/personId/MX_FXCASH"/>
                </conf:person>
            </conf:party>
            <conf:party id="party2">
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/LEID">11087176</conf:partyId>
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/FMID">400816559</conf:partyId>
                <conf:partyName>SYNGENTAEAST*NBO</conf:partyName>
            </conf:party>
            <conf:party id="executingBroker">
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/LEID">NA</conf:partyId>
                <conf:partyId partyIdScheme="http://www.sc.com/coding-scheme/partyId/S2BX/brokerCode">NA</conf:partyId>
                <conf:partyName>mockBrokerName</conf:partyName>
            </conf:party>
            <conf:party id="intermediary">
                <conf:partyId>NA</conf:partyId>
            </conf:party>
            <conf:party id="accountWithBank">
                <conf:partyId>NA</conf:partyId>
            </conf:party>
            <conf:party id="receiverCorrespondent">
                <conf:partyId>NA</conf:partyId>
            </conf:party>
            <scb:tradePortfolio>
                <conf:partyPortfolioName>
                    <conf:partyReference href="party1"/>
                    <conf:portfolioName>AFR-FW-KE-FX</conf:portfolioName>
                </conf:partyPortfolioName>
            </scb:tradePortfolio>
            <scb:confirmation>
                <scbextn:manualDraftFlag>false</scbextn:manualDraftFlag>
                <scbextn:comments>
                    <scbextn:comment id="RFRIndexValue">mock</scbextn:comment>
                </scbextn:comments>
                <scbextn:isInboundRequired>true</scbextn:isInboundRequired>
                <scbextn:confirmationMethod>PAPER</scbextn:confirmationMethod>
                <scbextn:linkId linkIdScheme="http://www.sc.com/coding-scheme/linkId/confirmationDocumentId"/>
            </scb:confirmation>
            <scb:settlementInstruction>
                <conf:correspondentInformation>
                    <conf:routingIdsAndExplicitDetails>
                        <conf:routingIds>
                            <conf:routingId>SCBLGB20XXX</conf:routingId>
                        </conf:routingIds>
                        <conf:routingName>SNAME 400825299</conf:routingName>
                        <conf:routingAddress>
                            <conf:streetAddress>
                                <conf:streetLine>STANDARD CHARTERED BANK BILLITER STREET LONDON</conf:streetLine>
                            </conf:streetAddress>
                            <conf:city>LONDON UK</conf:city>
                        </conf:routingAddress>
                        <conf:routingAccountNumber>05199460301</conf:routingAccountNumber>
                    </conf:routingIdsAndExplicitDetails>
                    <conf:correspondentPartyReference href="party1"/>
                </conf:correspondentInformation>
                <conf:beneficiary>
                    <conf:routingIdsAndExplicitDetails>
                        <conf:routingIds>
                            <conf:routingId/>
                        </conf:routingIds>
                        <conf:routingName/>
                        <conf:routingAddress>
                            <conf:streetAddress>
                                <conf:streetLine/>
                            </conf:streetAddress>
                            <conf:city/>
                        </conf:routingAddress>
                        <conf:routingAccountNumber/>
                    </conf:routingIdsAndExplicitDetails>
                </conf:beneficiary>
                <conf:depositoryPartyReference href="party2"/>
                <scbextn:currency currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">GBP</scbextn:currency>
                <scbextn:settlementNature>Capital</scbextn:settlementNature>
                <scbextn:settlementAccountType>Nostro</scbextn:settlementAccountType>
            </scb:settlementInstruction>
            <scb:settlementInstruction>
                <conf:correspondentInformation>
                    <conf:routingIdsAndExplicitDetails>
                        <conf:routingIds>
                            <conf:routingId>SCBLUS30XXX</conf:routingId>
                        </conf:routingIds>
                        <conf:routingName>SNAME 400825303</conf:routingName>
                        <conf:routingAddress>
                            <conf:streetAddress>
                                <conf:streetLine>1 MADISON AVENUE  NEW YORK</conf:streetLine>
                            </conf:streetAddress>
                            <conf:city>NEW YORK US</conf:city>
                        </conf:routingAddress>
                        <conf:routingAccountNumber>3582088350001-EBS</conf:routingAccountNumber>
                    </conf:routingIdsAndExplicitDetails>
                    <conf:correspondentPartyReference href="party1"/>
                </conf:correspondentInformation>
                <conf:beneficiary>
                    <conf:routingIdsAndExplicitDetails>
                        <conf:routingIds>
                            <conf:routingId/>
                        </conf:routingIds>
                        <conf:routingName/>
                        <conf:routingAddress>
                            <conf:streetAddress>
                                <conf:streetLine/>
                            </conf:streetAddress>
                            <conf:city/>
                        </conf:routingAddress>
                        <conf:routingAccountNumber/>
                    </conf:routingIdsAndExplicitDetails>
                </conf:beneficiary>
                <conf:depositoryPartyReference href="party1"/>
                <scbextn:currency currencyScheme="http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15">USD</scbextn:currency>
                <scbextn:settlementNature>Capital</scbextn:settlementNature>
                <scbextn:settlementAccountType>Nostro</scbextn:settlementAccountType>
            </scb:settlementInstruction>
        </scb:FPMLPayload>
    </scb:payload>
</scb:SCBML>
```

**EXPAND_END**

** Query  P[arameter](http://www.baidu.com/link?url=kV7PnviYcSw5YEc58WV97dw8uUD93wXvNaonwvaO10QKVs6gNIiDq6F_wUyxnXLMCI69Hg2F1200qRHhEgvraAFOexhX1f6iXnGBAancbUu)  need to provide by CDU**

| Query P[arameter](http://www.baidu.com/link?url=kV7PnviYcSw5YEc58WV97dw8uUD93wXvNaonwvaO10QKVs6gNIiDq6F_wUyxnXLMCI69Hg2F1200qRHhEgvraAFOexhX1f6iXnGBAancbUu) | Data Source | Path Exist(YES/NA) |
| --- | --- | --- |
| Legal Entity FMID | /scb:SCBML/scb:payload/scb:FPMLPayload/conf:party[1]/conf:partyId[1]][partyIdScheme="[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)"] | Yes |
| Counterpart FMID | /scb:SCBML/scb:payload/scb:FPMLPayload/conf:party[2]/conf:partyId[@partyIdScheme="[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)"] | Yes |
| Payment Currency | should be a list which is parse from the xml info and then identified by SSI Stamping service logic | Product type | CFI Code | CFI Code data path | Payment Currency data path | | --- | --- | --- | --- | | FX Spot | I-F-X-X-X-X | | | | FX Forward | J-F-X-X-X-X | | | | FX Swap | S-F-X-X-X-X | | | | wait for confirm |
| Product type | CFI Code | CFI Code data path | Payment Currency data path |
| FX Spot | I-F-X-X-X-X | | |
| FX Forward | J-F-X-X-X-X | | |
| FX Swap | S-F-X-X-X-X | | |
| CFI Code | | wait for confirm |
| Settlement Method | | wait for confirm |
| Settlement Type | | wait for confirm |
| Debit/Credit | should be derived from SCBML by SSI Stamping service logic Credit : SCB (Payer) Debit: SCB (receiver) | NA |
| SSI Status(Active/inactive) | Hard code （"Active", "New", "Update"） | NA |

**Vostro Query P[arameter](http://www.baidu.com/link?url=kV7PnviYcSw5YEc58WV97dw8uUD93wXvNaonwvaO10QKVs6gNIiDq6F_wUyxnXLMCI69Hg2F1200qRHhEgvraAFOexhX1f6iXnGBAancbUu)**

| Query P[arameter](http://www.baidu.com/link?url=kV7PnviYcSw5YEc58WV97dw8uUD93wXvNaonwvaO10QKVs6gNIiDq6F_wUyxnXLMCI69Hg2F1200qRHhEgvraAFOexhX1f6iXnGBAancbUu) | Data Source | Path Exist(YES/NA) |
| --- | --- | --- |
| Counterpart FMID | `/scb:SCBML/scb:payload/scb:party[@id='party2']``/conf:partyId` [@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)'] | YES |
| Branch FM Code | get from SSI Stamping service logic query result | NA |
| Currency | should be a list which is parse from the xml info and then identified by SSI Stamping service logic | YES |
| CFI Code | set " *F**** " as default | wait for confirm |
| Settlement Method | set " cash " as default | wait for confirm |
| Settlement Type | set " cash " as default | wait for confirm |
| Debit/Credit | should be identified by SSI Stamping servce logic based on the info parsed from xml Credit : SCB (Payer ) Debit: SCB (receiver) | NA |
| SSI Status(Active/Inactive) | Hard code （"Active", "New", "Update"） | NA |

**Nostro Query P[arameter](http://www.baidu.com/link?url=kV7PnviYcSw5YEc58WV97dw8uUD93wXvNaonwvaO10QKVs6gNIiDq6F_wUyxnXLMCI69Hg2F1200qRHhEgvraAFOexhX1f6iXnGBAancbUu)**

| Query P[arameter](http://www.baidu.com/link?url=kV7PnviYcSw5YEc58WV97dw8uUD93wXvNaonwvaO10QKVs6gNIiDq6F_wUyxnXLMCI69Hg2F1200qRHhEgvraAFOexhX1f6iXnGBAancbUu) | Data Source | Path Exist(YES/NA) |
| --- | --- | --- |
| Legal Entity FMID | `/scb:SCBML/scb:payload/scb:party[@id='party1']``/conf:partyId` [@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)'] | YES |
| Payment Currency | should be a list which is parse from the xml info and then identified by SSI Stamping service logic | YES |
| Settlement Means | from Vostro query result | NA |
| Settlement Account | from Vostro query result | NA |

**[Vostro  MatchingRule](https://confluence.global.standardchartered.com/display/DSP/BCS+Cash+Settlements)**

## Response Scenarios

Response code for Sell ( SCB Pay) currency:

| SN | Vostro Query Result | Nostro Query Result | API Response | Confirmation Document Enrichment Result |
| --- | --- | --- | --- | --- |
| 1 | Missing Vostro | Default Nostro | Blank Vostro + Default Nostro | - Enrich account details for party A(SCB) - Party B(Counterpart) account info as 'Please advise' |
| 2 | Multi Vostro | Default Nostro |
| 3 | Missing Vostro | Missing Nostro | Blank Vostro + Blank Nostro | - Party A(SCB) account info default as 'To Be Advise' - Party B(Counterpart) account info default as 'Please advise' |
| 4 | Multi Vostro | Missing Nostro |
| 5 | Unique Vostro | Missing Nostro | Unique Vostro + Blank Nostro | - Party A(SCB) account info default as 'To Be Advise' - Enrich account details for party B |
| 6 | Unique Vostro | Multi Nostro |
| 7 | Unique Vostro | Unique Nostro | Unique Vostro + Unique Nostro | - Enrich account details for party A - Enrich account details for party B |

Response code for Buy (SCB Receive) Currency:

| SN | Nostro Query Result | API Response | Confirmation Document Enrichment Result |
| --- | --- | --- | --- |
| 3 | Missing Nostro | Blank Nostro | - Party A(SCB) account info default as 'To Be Advise' |
| 4 | Multi Nostro |
| 7 | Unique Nostro | Unique Nostro | - Enrich account details for party A |

# Data Model

## trade_stamping_service

![image2023-3-20_11-26-5.png](attachments/image2023-3-20_11-26-5.png)

# Open questions

| Number | Question | Status | Note |
| --- | --- | --- | --- |
| 1 | the rule of trade product mapping with stamping records | Close | I-F-X-X-X-X (FX Spot) J-F-X-X-X-X (FX Forward) S-F-X-X-X-X (FX Swap) |
| 2 | default nostro information | Close | Currency + MAIN |
| 3 | data modeling of repsonse xml | Close | confirmed by data modeling team |
| 4 | attribute definition in trade xml （ CFI Code，Settlement Method，Settlement Type） | Open | wait for PO confirm |
| 5 | Does it need to support notification event | Close | So far, out of scope |
| 6 | best match logic | Close | https://confluence.global.standardchartered.com/display/DSP/BCS+Cash+Settlements |

# Technical implementation update

To support new products (bullion spot/forward, etc), a refactor of existing code was performed due to the following reasons:

- The xpath in scbml is upgraded to Xpath2.0 specification, while existing xpaths are 1.0 and could not be recognized
- Existing implementation of scbml generating is leveraging on template engine, which requires a specific template for each product type, and thus hard to reuse the generation logic

The goal is to keep existing implementation as is and use new implementation for new products.

![image2024-12-13_17-3-35.png](attachments/image2024-12-13_17-3-35.png)