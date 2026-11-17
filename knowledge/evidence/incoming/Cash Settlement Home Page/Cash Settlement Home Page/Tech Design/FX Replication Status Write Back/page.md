## Background

## Sample Data

**EXPAND: Sample Json**

<?xml version="1.0" encoding="UTF-8"?>
<scb:SCBML xmlns:scb="[http://www.sc.com/SCBML-1](http://www.sc.com/SCBML-1)"
    xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)" scbmlVersion="4-0" xsi:schemaLocation="[http://www.sc.com/SCBML-1](http://www.sc.com/SCBML-1) ../../../../../core/4-0/scbml-4-0.xsd [http://www.sc.com/SCBML-1](http://www.sc.com/SCBML-1) ../../../../../payloadType/cashflowPayload/4-0/scbml-cashFlow-4-0.xsd">
    <scb:header>
        <scb:messageDetails>
            <scb:messageVersion>1.0</scb:messageVersion>
            <scb:messageType>
                <scb:typeName>CashflowStatusChange</scb:typeName>
            </scb:messageType>
        </scb:messageDetails>
        <scb:originationDetails>
            <scb:messageSender>
                <scb:messageSender systemScheme="http://www.sc.com/coding-scheme/system-1-0">Razor</scb:messageSender>
                <scb:senderDomain>
                    <scb:domainName domainNameScheme="http://www.sc.com/coding-scheme/domainNamescheme-1-0">FM</scb:domainName>
                </scb:senderDomain>
                <scb:countryCode>ALL</scb:countryCode>
            </scb:messageSender>
            <scb:initiatedTimestamp>2023-11-02T10:27:28Z</scb:initiatedTimestamp>
            <scb:trackingId>MX_FXCASH_373670953_330134747_1698892048219</scb:trackingId>
            <scb:uniqueIdentifierMessageId/>
        </scb:originationDetails>
        <scb:captureSystem/>
        <scb:process>
            <scb:eventType>Insert</scb:eventType>
        </scb:process>
    </scb:header>
    <scb:payload>
        <scb:payloadFormat>XML</scb:payloadFormat>
        <scb:payloadType>cashflowPayload</scb:payloadType>
        <scb:payloadVersion>4-0</scb:payloadVersion>
        <scb:cashflowPayload>
            <scb:cashflowStatus>
                <scb:cashflowIdentifier>
                    <scb:cashflowId cashflowIdScheme="http://www.sc.com/coding-scheme/cashflowId/Razor">373670953</scb:cashflowId>
                </scb:cashflowIdentifier>
                <scb:isPaymentReversal>false</scb:isPaymentReversal>
                <scb:linkId linkIdScheme="http://www.sc.com/coding-scheme/tradeId/Razor">330134747</scb:linkId>
                <scb:id IdScheme="http://www.sc.com/coding-scheme/tradeId/Razor/version">1</scb:id>
                <scb:state stateScheme="http://www.sc.com/coding-scheme/state/workflowStatus">Settled</scb:state>
                <scb:paymentDate>20230707</scb:paymentDate>
            </scb:cashflowStatus>
            <scb:cashbalance>
                <scb:cashbalanceInfo>
                    <scb:settledCashCurrency>CNH</scb:settledCashCurrency>
                </scb:cashbalanceInfo>
            </scb:cashbalance>
        </scb:cashflowPayload>
    </scb:payload>
</scb:SCBML>

**EXPAND_END**