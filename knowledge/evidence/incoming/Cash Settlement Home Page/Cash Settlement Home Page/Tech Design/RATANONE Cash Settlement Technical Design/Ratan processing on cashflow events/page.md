# Background

# Principle:

1. Concepts | Attribute | Source | Meaning | Value | SCBML path | | --- | --- | --- | --- | --- | | Major Version | SCBML | Each action on trade, that will cause major version + 1, and same value will be reflected into cashflow | | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:cashflowMajorVersion | | Trade Id | SCBML | The trade id, that never change during | | For Stella Cashflow: /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:tradeId[@tradeIdScheme='http://www.sc.com/coding-scheme/tradeId'] For Murex Cashflow: /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:originatingTradeId/conf:tradeId[@tradeIdScheme='http://www.sc.com/coding-scheme/tradeId/originatingTradeId'] | | Count | SCBML | The count number within the same Group (Trade Id + Major Version), indicating how many cashflow events generated within same group | 1_5 to indicate 1st of 5 cashflows | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:tradeReferenceInformation/scb:partyTradeIdentifier/conf:linkId[@linkIdScheme="[http://www.sc.com/coding-scheme/linkId/cashflowSequence](http://www.sc.com/coding-scheme/linkId/cashflowSequence)"] | | Amendment flag | RATAN to attach in SCBML | Ratan generated field, indicating the cashflow event id depending on a withdrawal processing status, this field will be used by status machine: 1. For a new event, based on the flag, the status will be moved to "WAITING+Reversal_Rebook+Pending Verification" by status machine 2. For a withdrawal, the flag will be used in NSTP rule check | Amendment NonEcoAmend | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:event[@eventScheme='http://www.sc.com/coding-scheme/event/scbml-business-event/Ratan'] | | | | | | |
2. The whole group of cashflows won't be processed until 1. All cashflows received in same group 2. No previous major versions group in PENDING status
3. If group contains withdrawal, it will be marked "Amendment" 1. New will be tagged with Amendment, blocked in workflow as WAITING+Reversal_Rebook+Pending Verification 2. Withdrawal will be tagged with Amendment, to be processed by workflow
4. The events of withdrawal will drive STP of the new in same group 1. Withdrawals are all with below status in one group, will drive new in same group to be STP | main status | sub status | sub status type | | --- | --- | --- | | CANCELLED | NA | NA | | NOSTRO_MATCHED | NA | NA | | NETTED | NA | NOSTRO_MATCHED | 2. Best matching to be applied on identifying linked new ????
5. (TBD) When a group's withdrawal and new will perfectly match 1. Recall original batch of cashflows
6. How to identify a non-economic change: | Logical model | Physical model | | --- | --- | | Entity.Booking_Entity_SCI_FMID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party1']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)'] | | Entity.Counterparty_SCI_FMID | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:partyId[@partyIdScheme='[http://www.sc.com/coding-scheme/partyId/FMID](http://www.sc.com/coding-scheme/partyId/FMID)'] | | Cashflow.Payment_Currency | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency[@currencyScheme="[http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15](http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15)"] | | Cashflow.Payment_Amount | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount | | Cashflow.Payment_Date | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate | | Cashflow.Pay_Receive_Indicator | If (/scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:payerPartyReference/@href== party1 Pay Else Receive |
7. COMPLETED and PENDING_WITHDRAWAL event on group will try driving later PENDING_PRE_GROUP groups to be processed.
8. Group Status: | Status | Meaning | | --- | --- | | PENDING | Waiting for other cashflows in same group | | PENDING_PRE_GROUP | Waiting for previous groups consumed all necessary messages | | READY | All cashflows arrived in same group and ready to be processed | | PENDING_WITHDRAWAL | Withdrawal and new exist in the group, and the withdrawals have not ended yet | | COMPLETED | Group completed, no dependency | | PENDING_TRADE_VALIDATION | [ New ] All messages arrived within a group but trade not validated |
9. Group Message Status: | Status | Meaning | | --- | --- | | PENDING | Waiting for other cashflows in same group | | DELIVERED | Delivered to workflow, but pending on end status of withdrawal | | END | Completed and nothing pending on other cashflows | | OFFSET | [ New ] Both new and withdrawal came with both groups PENDING or PENDING_TRADE_VALIDATION |

# Overall technical module design:

# Technical detailed design for Strategic Group Management Service:

Table: ratan_cashflow_mapping

| TABLE: ratan_cashflow_mapping | | TABLE: ratan_cashflow_mapping_history | |
| --- | --- | --- | --- |
| Column name | | Column name | Data Type | Sample Value |
| id | | mapping_id | int | 1,2,3 |
| | | id | int | 1,2,3 |
| original_cashflow_id | | original_cashflow_id | text | C01 |
| original_business_version | | original_business_version | text | 0 |
| original_cashflow_version | | original_cashflow_version | text | 0 |
| original_major_version | | original_major_version | text | 0 |
| replaced_cashflow_id | | replaced_cashflow_id | text | C03 |
| replaced_business_version | | replaced_business_version | text | 1 |
| replaced_cashflow_version | | replaced_cashflow_version | text | 1 |
| replaced_major_version | | replaced_major_version | text | 1 |
| ratan_status | | ratan_status | text | PROJECTED,NETTED,RELEASED,SETTLED,NOSTROMATCHED |
| upstream | | upstream | text | STELLA/MUREX |
| upstream_status | | upstream_status | text | PROJECTED,NETTED,RELEASED,SETTLED,NOSTROMATCHED |
| status | | status | text | ACTIVE/OVERDUE |
| created_at | | created_at | timestamp | |
| updated_at | | updated_at | timestamp | |
| version | | version | int | 1 |

# Technical detailed design for Murex Adaptor:

**EXPAND: Out of date diagram**

**EXPAND_END**

# Exception handling (TBD)

| | Group Message Consumer | Group Processor | Future Group Enabler | Cashflow Event Consumer | Amendment STP Enabler | Stella status update |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Received more than the count | | | | | Status write back failure, which could lead further WnN on wrong cashflows |
| 2 | Several group messages never come | | | | | |
| 3 | Duplicated message received | | | | | |
| 4 | | | | | | |

# Modules

| Module | Feature | Status | JIRA |
| --- | --- | --- | --- |
| Cashflow Group Management Service | Group management, if no group flag (major version + trade id + count) from SCBML, directly flow into current flow 1. Kafka consumer: 1. Publish to workflow when group flag (major version + trade id + count) exist in SCBML 2. Otherwise stop 2. API to list the group details for UI to display, query by trade id, cashflow id, major version | | [[RATAN-14250] [Backend] Major Version - event consumer and new cashflow resumer - Jira (standardchartered.com)](https://jira.global.standardchartered.com/browse/RATAN-14250) |
| Lifecycle service | 1. Status to be added "**WAITING**+**Pending Verification**+**Reversal_Rebook**", the status will be tagged to cashflows: 1. 1. New cashflow with amendment flag 2. Withdrawal cashflow on RELEASED status and amendment flag 2. Add major version into the cashflow data object 3. Major version to be added on cashflow query on consuming trade confirmation status We can limit the manual action to move the cashflows to STP to checker only, to solve | | [[RATAN-14224] [Backend] Trade and Cashflow Linkage with Major Version - Jira (standardchartered.com)](https://jira.global.standardchartered.com/browse/RATAN-14224) |
| Trade service | 1. Add major version into trade data object 2. Data extraction logic enhancement for both trade consuming and confirmation status consuming on major version 3. Publish trade confirmation with major version as well 4. Query API to add major version as parameter | | |
| UI | Create a new tile to display group details Query by trade id, cashflow id, major version | | [[RATAN-14225] [Frontend] Trade and Cashflow Linkage with Major Version - Jira (standardchartered.com)](https://jira.global.standardchartered.com/browse/RATAN-14225) |

# Event

## Status

```
public Enum GroupStatus {
	PENDING,
	PENDING_PRE_GROUP,
	READY,
	PENDING_WITHDRAWAL,
	COMPLETED
}
public Enum GroupMessageStatus {
	PENDING,
	DELIVERED,
	COMPLETED
}
```

## Group event

```
public class GroupEvent {
   
   private String id;
   private String majorVersion;
   private String tradeId;
   private GroupStatus status;
}
```

## Group Message Resume event

```
public class GroupMessageResumeEvent {
   private String id;
 }
```

# Detailed data