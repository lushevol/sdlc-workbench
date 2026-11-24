#

# Background

Static data and external API are strongly depended by domain services, most of the static data will fetch from DB, and external API depend on the external stable system.

DB and network access will expend a lot of IO and network performance

Remote data as a local cache can avoid the the exhaustion risk of the system.

# Design Principles

Cache-Aside Pattern

Read Flow

1. Application checks the cache for a key.
2. **Cache hit** → return cached value.
3. **Cache miss** → load from database, store in cache with TTL, return value. - The cache never fetches from the database automatically. - The own application take responsibilities for all logic for population and freshness.

Write Flow

1. Application writes updated data to the database.
2. Application invalidates or deletes the corresponding cache entry.
3. Next read repopulates the cache with fresh data.

# Stag1 Scope

- Self static: Settlement Method
- External static: SSI Vostro
- CES

# Static data dependencies

| Type | Domain Services | Dependency | Target | Condition | Cache |
| --- | --- | --- | --- | --- | --- |
| Settlement method | ratan-cash-settlement-group-management-service | ratanone-static-data-service | table : ratanone.ratan_settlement_method_config | booking_entity_fmid + counterparty_fmid + taxonomy + currency | |
| ratan-cash-settlement-ssi-stamping-service | ratanone-static-data-service | table: ratanone.ratan_settlement_method_config | booking_entity_fmid + counterparty_fmid + taxonomy + currency |
| SSI | ratan-cash-settlement-ssi-stamping-service | ratanone-data-ambassador | ssiplus | sample: {field: "Settlement_Instruction.BranchId_Murex3Id", operator: IN, values: ["SCB LONDON*LDN","Global"] }, {field: "Settlement_Instruction.Payment_Currency", operator: IN, values: ["KRO"] }, {field: "Settlement_Instruction.CFI_Code", operator: IN, values: ["STX***","ST****","*T****","******"] }, {field: "Settlement_Instruction.Counterparty_SCI_FMID", operator: IN, values: ["10036422"] }, {field: "Settlement_Instruction.Debit_Credit", operator: IN, values: ["Credit","Both"] }, {field: "Settlement_Instruction.Settlement_Type", operator: IN, values: ["CASH"] }, {field: "Settlement_Instruction.Settlement_Method", operator: IN, values: ["CASH","FEDWIRE"] }, {field: "Settlement_Instruction.SSI_Status", operator: IN, values: ["Active","New","Update"] } | |
| CES | ratan-cash-settlement-query-service | ratanone-auth-server | EMS3 | | |
| | | | | | |

# 4. Cache Lifecycle

## Settlement method

## SSI

## CES

# Generic Cache Design

Define a generic prefix for different static data type

SETTLEMENT_METHOD:

SSI_STAMP:

CES:

## Overview Of Generic Cache

## Settlement Method Cache

### Key Rule

Type:  StringKey

Cache Key: SettlementMethod:[BookingEntityFmId]-[CounterpartyFmId]-[Taxonomy]-[Currency]

e.g.

SettlementMethod:400007847-400934291-ForeignExchange-ALL

### Component Flow

## Ssi Stamping

### Key Rule

Type:  **HashKey**

Cache key:  String Key + Reverse Index

e.g

String Key:  SSI:a1b2c3   Value: List<VostroStampingResponse>

Reverse Index:   SSI:a1b2c3 {ssi_id_1, ssi_id_2, ssi_id_3, .........}

Convert the query condition to a hashcode, and query result will be cached with a List<>

condition e.g.
{field: "Settlement_Instruction.BranchId_Murex3Id", operator: IN, values: ["SCB LONDON*LDN","Global"] },
{field: "Settlement_Instruction.Payment_Currency", operator: IN, values: ["KRO"] },
{field: "Settlement_Instruction.CFI_Code", operator: IN, values: ["STX***","ST****","*T****","******"] },
{field: "Settlement_Instruction.Counterparty_SCI_FMID", operator: IN, values: ["10036422"] },
{field: "Settlement_Instruction.Debit_Credit", operator: IN, values: ["Credit","Both"] },
{field: "Settlement_Instruction.Settlement_Type", operator: IN, values: ["CASH"] },
{field: "Settlement_Instruction.Settlement_Method", operator: IN, values: ["CASH","FEDWIRE"] },
{field: "Settlement_Instruction.SSI_Status", operator: IN, values: ["Active","New","Update"] }

### Component Flow

## CES Cache

Key Rule

CES: