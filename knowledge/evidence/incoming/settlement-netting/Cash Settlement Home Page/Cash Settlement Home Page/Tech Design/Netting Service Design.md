## Background

FMO need to do netting in RATANONE, especially CPN to net cashflows from STELLA and Murex2.11 on different products. Maker/checker process required.

DoD:

1) Interface for netting that component cashflows from Pending/Validated/Queued/Projected to Netted, sum up the amount and generate resultant cashflow, status Queued
2) Interface for netting validation
3) Interface for unnet that component cashflows back to Pending, and resultant cashflow to be Dead
4) Maker/checker process
5) Netting eligible check and update the sub-status
6) Status write back to STELLA

## Package structure

## Process Flow

| | IRS aggregation | Bilateral Netting |
| --- | --- | --- |
| Cashflows | Status | Payment Type | Amount | Netting Id | Status | Payment Type | Amount | Netting Id |
| C01 | NETTED | Fixed | 100 | 1111 | NETTED | Fixed | 100 | 2222 |
| C02 | NETTED | Float | 200 | 1111 | NETTED | Float | 200 | 2222 |
| N01 | WAITING | IRS | 300 | 1111 | DEAD | IRS | 300 | |
| C03 | WAITING | Fee | 400 | | NETTED | Fee | 400 | 2222 |
| N02 | NA | | | | WAITING | | 700 | 2222 |

| | IRS aggregation | C02 withdrawal |
| --- | --- | --- |
| Cashflows | Status | Payment Type | Amount | Netting Id | Status | Payment Type | Amount | Netting Id |
| C01 | NETTED | Fixed | 100 | 2222 | WAITING PAL | | | 333 |
| C02 | NETTED | Float | 200 | 2222 | CANCELLED | | | 333 |
| N01 | DEAD | IRS | 300 | | | | | |
| C03 | NETTED | Fee | 400 | 2222 | WAITING | | | |
| N02 | WAITING | | 700 | 2222 | DEAD | | | |
| N03 | | | | | WAITING | | 300 | 333 |

| | IRS aggregation | Split |
| --- | --- | --- |
| Cashflows | Status | Payment Type | Amount | Netting Id | Status | Payment Type | Amount | Split Id | Netting Id |
| C01 | NETTED | Fixed | 100 | 1111 | NETTED | Fixed | 100 | | 2222 |
| C02 | NETTED | Float | 200 | 1111 | NETTED | Float | 200 | | 2222 |
| N01 | WAITING | IRS | 300 | 1111 | SPLIT | | 300 | 3333 | |
| S01 | | | | | WAITING | | 150 | 3333 | |
| S02 | | | | | WAITING | | 150 | 3333 | |

## Database Tables

**t_request:**

| Column | Type | Nullable | Sample value | Unique |
| --- | --- | --- | --- | --- |
| id | Text | Mandatory | 1 | Yes |
| action | Text | Mandatory | NET / UNNET / SPLIT | |
| process_type | Text | Mandatory | MANUAL / AUTO | |
| request_body | JSON | Mandatory | **EXPAND: request** [ { "cashflowId":"003690235910", "businessVersion":"0", "cashflowVersion":"0", "fmid":"123123", "currency":"USD", "entity":"CN", "valueDate":"2022-10-20", "settlementMethod":"NET", "payRec":"Pay", "cashflowAmount":"100", "netId":"" }, { "cashflowId":"003690235911", "businessVersion":"0", "cashflowVersion":"0", "fmid":"123123", "currency":"USD", "entity":"CN", "valueDate":"2022-10-20", "settlementMethod":"NET", "payRec":"Pay", "cashflowAmount":"200", "netId":"" } ] **EXPAND_END** | |
| group_id | Text | Mandatory | 11111111111 | Yes |
| fmo_comments | JSON | Nullable | | |
| updated_by | Text | Mandatory | 1481696 | |
| ratan_label | Text | Nullable | live | |
| created_at | Timestamp | Mandatory | | |
| updated_at | Timestamp | Mandatory | | |

**t_cashflow**:

| Column | Type | Nullable | Sample | Unique |
| --- | --- | --- | --- | --- |
| id | Text | Mandatory | 1 | Yes |
| request_id | Text | Mandatory | 1 | |
| character | Text | Mandatory | COMPONENT / RESULTANT | |
| action | Text | Mandatory | NET / UNNET / SPLIT | |
| cashflow__netting_id | Text | Mandatory | 11111111111 | |
| cashflow__cashflow_id | Text | Mandatory | 003690235910 | |
| cashflow__cashflow_business_version | Text | Mandatory | 0 | |
| cashflow__cashflow_version | Text | Mandatory | 0 | |
| cashflow__cashflow_minor_version | Text | Nullable | 2 | |
| cashflow__payment_amount | Number | Mandatory | 1,000,000 | |
| cashflow__payment_currency | Text | Mandatory | USD | |
| entity__counterparty_sci_fmid | Text | Mandatory | 2 | |
| entity__booking_entity_sci_fmid | Text | Mandatory | 21 | |
| payment_date | Date | Mandatory | 2022-10-20 | |
| message_event_row_key | Text | Nullable | | |
| ratan_label | Text | Nullable | | |
| created_at | Timestamp | Mandatory | | |
| updated_at | Timestamp | Mandatory | | |
| data_source_system | Text | Nullable | Stella | |

**t_cashflow**:

| Column | Type | Nullable | Sample |
| --- | --- | --- | --- |
| message_event_row_key | Text | Mandatory | 1111-1111-1111 |
| message | Text | Mandatory | <SCBML>message</SCBML> |

## Resultant cashflow generation

## API Information

| | URL | Parameters | Response | Notes |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## Netting process