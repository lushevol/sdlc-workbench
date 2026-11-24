# 1. Background

Group management service will receive all cashflows inbounded to RATAN, before publishing to workflow, it will group the cashflows by trade id and major version, if there are Withdrawal and New events exist in one group, it will be tag as amendment group, cashflows inside group has two cases:

1. Non economic amendment(Two cashflows in group has same **Booking Entity Id**, **Counterparty FM Id**, **Payment Currency**, **Payment Amount**, **Value Date,** **Direction**, business event are opposite, 1 is Withdrawal, the other is New, then these two cashflows can be treated as a non-economic amendment pair)
2. Economic amendment(cashflow in amendment group are not non-economic amendment)

This page is mainly talking about functions related to non-economic amendment and technical design of related functions.

# 2. Overall Design Diagram

# 3. Cashflow Mapping

## 2.1 DB Design

| **ratan_cashflow_mapping** |
| --- |
| Column name | Column description | Sample Value |
| id | primary key | 1720275970604654592 |
| original_cashflow_id | Cashflow id of New event | 200094700143 |
| original_business_version | Cashflow business version of New event | 0 |
| original_cashflow_version | Cashflow version of New event | 0 |
| original_major_version | Cashflow major version of New event | 1 |
| replaced_cashflow_id | Cashflow id of New event on non-eco amend | 200094700145 |
| replaced_business_version | Cashflow business version of New event on non-eco amend | 1 |
| replaced_cashflow_version | Cashflow version of New event on non-eco amend | 1 |
| replaced_major_version | Cashflow major version of New event on non-eco amend | 2 |
| source_system | Cashflow source system | STELLA |
| created_at | | |
| updated_at | | |
| version | | |

| **ratan_cashflow_mapping_history** |
| --- |
| Column name | Column description | Sample Value |
| id | primary key | 1720275971888111616 |
| mapping_id | ratan_cashflow_mapping primary key | 1720275970604654592 |
| original_cashflow_id | Cashflow id of New event | 200094700143 |
| original_business_version | Cashflow business version of New event | 0 |
| original_cashflow_version | Cashflow version of New event | 0 |
| original_major_version | Cashflow major version of New event | 1 |
| replaced_cashflow_id | Cashflow id of New event on non-eco amend | 200094700145 |
| replaced_business_version | Cashflow business version of New event on non-eco amend | 1 |
| replaced_cashflow_version | Cashflow version of New event on non-eco amend | 1 |
| replaced_major_version | Cashflow major version of New event on non-eco amend | 2 |
| source_system | Cashflow source system | STELLA |
| created_at | | |
| updated_at | | |
| version | | |

| **ratan_cashflow_message_io** |
| --- |
| Column name | Column description | Sample Value |
| id | primary key | |
| header | kafka message header | |
| content | kafka message payload | |
| direction | message inbound or outbound | IN OUT |
| message_key | message aggregate id, tradeId|majorVersion|cashflowId | 15700093|1|M00017700002 |
| version | technical version | |
| created_at | | |
| updated_at | | |

# Diagram based on current workflow

# 3. Stella sync up & Response handling in lifecycle

# 3. Trade Confirmation

# 4. POC Use Cases

| Component | Scenarios | Check point | Status |
| --- | --- | --- | --- |
| Cashflow Mapping | | | |
| Stella status sync up | 1. Stella Cashflow C301(T04 + 1 + New) inbound 2. Cashflow C301(T04 + 2 + Withdrawal), C302(T04 + 2 + New) inbound, They are non-economic amendment cashflows 3. C401 Netting 4. Receive failed ack from Stella ambassador 5. C401 Unnet 6. Netting sync up exception replay 7. Receive Netting sync up success ack from Stella ambassador | 1. Check existing on GUI 2. Mapping created 3. a. Action is Net, Cashflow status is NETTED b. Check cashflow id in blocking queue record is replaced cashflow id and status is IN_PROGRESS 4. a. Blocking queue process_status change to FAILED b. Generate exception and sync to exception platform 5. Unnet status sync up process_status is ACTIVE as previous status is failed. 6. a. Netting status sync up exception is CLOSED b. blocking queue record process_status is IN_PROGRESS 7. a. Netting status sync up record in blocking queue process_status update to SUCCESS b. Auto trigger Unnet status sync up | |
| Trade Confirmation | 1. Cashflow C101(T01 + 1 + New) inbound, generate "Pending Affirmation" exception 2. Trade event (T01) inbound which is match the trade confirmation condition | 1. Check existing on GUI 2. Exception auto closed | |
| | 1. Cashflow C201(T02 + 1 + New) inbound, generate "Pending Affirmation" exception 2. Cashflow C201(T02 + 2 + Withdrawal), C202(T02 + 2 + New) inbound, They are non-economic amendment cashflows 3. Trade event (T01) inbound which is match the trade confirmation condition | 1. Check existing on GUI 2. Mapping created correctly 3. Pending Affirmation exception should be closed for C201 | |
| | | | |

# 5. Enhanced non-eco amend handling on non touched payments 2024-06-14

Currently non eco amend will be ignored directly, however, it should only be ignored if payments have been touched by users or already settled.

Let's consider below cases, that non-eco amendment should still go to workflow:

1. Payment to be replaced in PROJECTED status
2. Payment to be replaced in QUEUED status