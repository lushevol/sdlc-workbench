# Background

In the Murex trade booking model, there're market events to place Lien on the trade level and the Lien information is feeding to TDS3. Settlement ops request to populate NSTP exception on cashflows if there's Lien available on trade, RATAN is going to source the trade Lien information from TDS3 and use this drive the cashflow NSTP exception.

# Detail Requirement - Lien Placement

When LIEN is placed & Lien amount update on a trade, all of its cashflows (including interest) must be NSTP in RATAN with 'LIEN' exception (Maker +  Checker)

NSTP rule setup: **Cashflow.Lien_Monitoring != empty**, Cashflow.Lien_Monitoring is new RATAN internal logical model field which the value is copied from parent trades. Field details can be found in [Cashflow Logical Model Fields & Data Store - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2560595214)

- '**LIEN on Trade**' exception would be system pre-defined maker/checker exception which ops(business rule and data ops profiles) can't update/remove.
- Exception for Gross Cashflow: RATAN need to lookup the Lien amount from latest event from parent trade(by original trade id), if there's Lien available from trade then generate '**LIEN on Trade**' exception on cashflow
- Exception for netting resultant cashflow: - For each of component cashflow, lookup the latest Lien amount from parent trade - If there's Lien from any of component cashflow, populate '**LIEN on Trade**' on the resultant cashflow
- NETTED cashflow: Auto un-net would happen only with the below criteria - Netting resultant cashflow not in the status ( **READY + Pending Ack, RELEASED, SETTLED**) - Netting resultant cashflow doesn't have the '**LIEN on Trade**' exception so far - There's Lien placement from latest trade event
- WAITING cashflow: Reprocess the cashflow to regenerate the exception with below criteria - Cashflow in WAITING status - Sub Status Type == 'Pending Exception' - There's no '**LIEN on Trade**' exception yet - There's Lien placement from latest trade event
- HOLD/READY Cashflow: Reprocess the cashflow to regenerate the exception with below criteria - Cashflow in HOLD/READY status - There's no '**LIEN on Trade**' exception yet - There's Lien placement from latest trade event

# The Lien Field in TDS3

- The logical & physical model of lien field | Logical Model Fiedl | SCBML Path | | --- | --- | | Lien_Monitoring | (/scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade|/scb:SCBML/scb:payload/scb:FPMLPayload/((*/(*:originalTrade|*:trade))|((*:novation|*:cancelReissue)/*:newTrade)))/conf:tradeHeader/conf:partyTradeInformation/scbextn:lienMonitoring |

# Trades & Cashflow Linkage

- Correlation id between cashflow & trade is original trade id. - Original trade id in cashflow | **Logical Model Field** | **SCBML Path** | | --- | --- | | Parent_Trade_Id | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:linkId[@linkIdScheme="[http://www.sc.com/coding-scheme/linkId/eve](http://www.sc.com/coding-scheme/linkId/eventId) | - Original trade id in TDS3 trade | **Logical Model Field** | **SCBML Path** | | --- | --- | | Trade_Id | (/scb:SCBML/scb:payload/scb:FPMLPayload/conf:trade|/scb:SCBML/scb:payload/scb:FPMLPayload/((*/(*:originalTrade|*:trade))|((*:novation|*:cancelReissue)/*:newTrade)))/conf:tradeHeader/conf:partyTradeIdentifier[conf:partyReference/@href="party1"]/conf:tradeId[@tradeIdScheme=[http://www.sc.com/coding-scheme/tradeId](http://www.sc.com/coding-scheme/tradeId)] |

# How RATAN use the Lien from TDS3

- **Single trade query from TDS3 ES**: RATAN will get the cashflows from Murex and call the TDS3 trade, each cashflow would trigger one call to TDS3 ES by the Trade_Id( from Murex cashflow). The overall projected daily Murex cashflow daily volume is around 50k. Can refer to TDS3 document how to query the latest record from ES API [TL API: Query Hints - SABRE - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/SABRE/TL+API%3A+Query+Hints).![image2024-11-12_15-7-34.png](attachments/image2024-11-12_15-7-34.png)
- **For Notification: **If cashflow comes before trade update, it may not have LIEN exception. Then when trade notification comes, it will be reflected in cashflow according to original trade ID.
- Current design, RATAN will only consume trade notification with VALD/COMP status by priority.

# Function Flow

There's original trade id concept in both Murex trade