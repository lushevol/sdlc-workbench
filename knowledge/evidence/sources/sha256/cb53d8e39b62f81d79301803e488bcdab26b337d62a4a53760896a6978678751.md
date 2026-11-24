###

### Background

Two upgrade:

1. We are going to increase the work_mem of PostgreSQL from 4MB to 30MB in each session of query service to optimize the bitmap index scan(avoid lossy mode). This change will impact the machine memory usage of postgreSQL DB.
2. User defined postgres function `to_number_ratan` to delegate the postgres inner` to_number` function for the expression index used on the JSONB column 'cashflow' of cashflow_data table(because the IMMUTABLE feature of inner `to_number `function does not support expression index ).

Function test has been covered by QA regression test, now we need to assess the impact of performance and memory usage.

### Estimate Max Memory Use

In product environment, we have 6 instances of query service now, each of them have a DB connection pool with max connection size set to 40.

Suppose all the 40 connections will be in use during peak hours, the increment usage of DB memory will be:

40  * 6  * (30 - 4) = 240 * 26 = 6240MB = 6.24GB(4 is the work_mem now in use).

Postgres machine memory use of production environment(around 55%, total memory is 64GB):

![image-2025-5-20_10-26-50.png](attachments/image-2025-5-20_10-26-50.png)

**In the assumption above, based on the 64GB total memory, the memory usage will be up to around 64%. That is safe.**

### Test From SQL

- to_number_ratan()

| Test Case | Condition | Aspect | Before(use the created_at index) | After(use to_number_ratan() index on the condition column) |
| --- | --- | --- | --- | --- |
| Numeric Field Query | test from SQL in daily DB, 4,000,000 records in cashflow_data table ``` SELECT * FROM CASH_SETTLEMENT_QUERY_CN.CASHFLOW_DATA CFD1_0 WHERE CASH_SETTLEMENT_QUERY_CN.TO_NUMBER_RATAN ( JSONB_EXTRACT_PATH_TEXT(CFD1_0.CASHFLOW, 'Cashflow', 'Payment_Amount'), '99999999999999999.999999' ) = 43454.7 ORDER BY CFD1_0.CREATED_AT DESC LIMIT 1000; ``` | | 339321.217 ms ![image-2025-5-21_16-4-19.png](attachments/image-2025-5-21_16-4-19.png) | 0.323 ms ![image-2025-5-21_15-9-56.png](attachments/image-2025-5-21_15-9-56.png) |

- work_mem

| Test Case | Condition | Aspect | Before(work_mem=4MB) | After(work_mem=30MB) |
| --- | --- | --- | --- | --- |
| Bitmap Index Scan | test from SQL in daily DB, 4,000,000 records in cashflow_data table ``` EXPLAIN ANALYZE SELECT * FROM CASH_SETTLEMENT_QUERY_CN.CASHFLOW_DATA CFD1_0 WHERE JSONB_EXTRACT_PATH_TEXT( CFD1_0.CASHFLOW, 'Entity', 'Booking_Entity_SCI_FMID' ) = '10075222' AND JSONB_EXTRACT_PATH_TEXT(CFD1_0.CASHFLOW, 'Cashflow', 'Payment_Date') BETWEEN ('2025-04-01') AND ('2025-05-07') AND JSONB_EXTRACT_PATH_TEXT( CFD1_0.CASHFLOW, 'Instrument_Common', 'ISDA_Taxonomy' ) = 'InterestRate:IRSwap:FixedFloat' AND JSONB_EXTRACT_PATH_TEXT(CFD1_0.CASHFLOW, 'Cashflow', 'Is_Commodity') = 'false' AND JSONB_EXTRACT_PATH_TEXT( CFD1_0.CASHFLOW, 'Entity', 'Counterparty_Client_Type' ) IN ('INTEBCH', 'INTECOM', 'INTLACC') ORDER BY CFD1_0.CREATED_AT DESC LIMIT 1000; ``` | | Execution Time: 10073.726 ms ![image-2025-5-23_15-33-32.png](attachments/image-2025-5-23_15-33-32.png) | Execution Time: 534.751 ms ![image-2025-5-23_15-34-34.png](attachments/image-2025-5-23_15-34-34.png) |

### PT From Query Service

#### PT Structure

#### Test Situation

- to_number_ratan()

| Test Case | Condition | Aspect | Before(no index on numeric field query) | After(expression index on to_number_ratan()) |
| --- | --- | --- | --- | --- |
| Numeric Field Query | 500 users ![image-2025-5-22_14-32-12.png](attachments/image-2025-5-22_14-32-12.png) ``` You should capture the HTTP Body from network in explore to use it in JMeter. http://localhost:9006/graphiql?path=/graphql { cashflowUltraQuery( payload: { filters: { filters: {field: "Cashflow.Payment_Amount", operator: EQ, values: ["43454.7"]} } orderArgs: [] pagingOption: PAGE_INDEX pageIndex: 0 itemsPerPage: 1000 } ) { results { BCS_Trade_Id BCS_Parent_Trade_Id FMO_Comments { FMO_Comment FMO_Comment_Timestamp FMO_Comment_Updater } Cashflow { Cashflow_Id Cashflow_Business_Version Cashflow_Version Cashflow_State Cashflow_Affirmation_Status Cashflow_Event_Type Cashflow_Minor_Version Payment_Currency Payment_Date Payment_Type Payment_Cutoff_Time Pay_Receive_Indicator Payment_Amount Netting_Id Netting_Cuttoff_Date Payment_Receiver_Party_Reference Payment_Payer_Party_Reference Cashflow_Sub_State Cashflow_Sub_State_Type Cashflow_Sub_State_Updater Status_Event_Type Cashflow_Swift_Message_Standard Event_Date Cashflow_Event_Reason } Delivery_Method Settlement_Method Trade_Id Trade_Version Entity { Booking_Entity_SCI_FMID Booking_Entity_SCI_FMCODE Counterparty_SCI_FMID Counterparty_SCI_FMCODE Counterparty_SCI_BIC_Net_Flag } Instrument_Common { ISDA_Taxonomy Source_System_Instrument_Sub_Type } Trade_Original_Source_System_Name Data_Flow { Data_Source_System } Parent_Trade_Id Trade_State Portfolio { Booking_Entity_Trade_Portfolio_Name } } } } ``` | QPS | 5.4(but most of the results are invalid, because every single query will cost minutes) ![image-2025-5-22_14-32-40.png](attachments/image-2025-5-22_14-32-40.png) | 45.4 ![image-2025-5-22_13-45-25.png](attachments/image-2025-5-22_13-45-25.png) |
| CPU | ![image-2025-5-22_14-51-57.png](attachments/image-2025-5-22_14-51-57.png) | ![image-2025-5-22_14-52-52.png](attachments/image-2025-5-22_14-52-52.png) |
| Memory | ![image-2025-5-22_14-52-19.png](attachments/image-2025-5-22_14-52-19.png) | ![image-2025-5-22_14-53-12.png](attachments/image-2025-5-22_14-53-12.png) |
| Network | ![image-2025-5-22_14-46-37.png](attachments/image-2025-5-22_14-46-37.png) | ![image-2025-5-22_14-48-43.png](attachments/image-2025-5-22_14-48-43.png) |
| Disk IO | ![image-2025-5-22_14-50-16.png](attachments/image-2025-5-22_14-50-16.png) | ![image-2025-5-22_14-50-46.png](attachments/image-2025-5-22_14-50-46.png) |

- work_mem

| Test Case | Condition | Aspect | Before(work_mem=4MB) | After(work_mem=30MB) |
| --- | --- | --- | --- | --- |
| Bitmap Index Scan | 500 users ![image-2025-5-22_14-32-12.png](attachments/image-2025-5-22_14-32-12.png) ``` You should capture the HTTP Body from network in explore to use it in JMeter. http://localhost:9006/graphiql?path=/graphql { cashflowUltraQuery( payload: { filters: { and: [ { filters: [ { field: "Entity.Booking_Entity_SCI_FMID", operator: EQ, values: "10075222" }, { field: "Cashflow.Payment_Date", operator: BET, values: [ "2025-04-01", "2025-05-07" ] }, { field: "Instrument_Common.ISDA_Taxonomy", operator: EQ, values: "InterestRate:IRSwap:FixedFloat" }, { field: "Cashflow.Is_Commodity", operator: EQ, values: "false" }, { field: "Entity.Counterparty_Client_Type", operator: IN, values: [ "INTEBCH", "INTECOM", "INTLACC" ] } ] } ] }, orderArgs: [], pagingOption: PAGE_INDEX, pageIndex: 0, itemsPerPage: 1000} ) { results { BCS_Trade_Id BCS_Parent_Trade_Id FMO_Comments { FMO_Comment FMO_Comment_Timestamp FMO_Comment_Updater } Cashflow { Cashflow_Id Cashflow_Business_Version Cashflow_Version Cashflow_State Cashflow_Affirmation_Status Cashflow_Event_Type Cashflow_Minor_Version Payment_Currency Payment_Date Payment_Type Payment_Cutoff_Time Pay_Receive_Indicator Payment_Amount Netting_Id Netting_Cuttoff_Date Payment_Receiver_Party_Reference Payment_Payer_Party_Reference Cashflow_Sub_State Cashflow_Sub_State_Type Cashflow_Sub_State_Updater Status_Event_Type Cashflow_Swift_Message_Standard Event_Date Cashflow_Event_Reason } Delivery_Method Settlement_Method Trade_Id Trade_Version Entity { Booking_Entity_SCI_FMID Booking_Entity_SCI_FMCODE Counterparty_SCI_FMID Counterparty_SCI_FMCODE Counterparty_SCI_BIC_Net_Flag } Instrument_Common { ISDA_Taxonomy Source_System_Instrument_Sub_Type } Trade_Original_Source_System_Name Data_Flow { Data_Source_System } Parent_Trade_Id Trade_State Portfolio { Booking_Entity_Trade_Portfolio_Name } } } } ``` | QPS | 5.5(but most of the results are invalid, because the db connection timeout) ![image-2025-5-23_14-39-56.png](attachments/image-2025-5-23_14-39-56.png) | 24.7 ![image-2025-5-23_13-54-40.png](attachments/image-2025-5-23_13-54-40.png) |
| CPU | ![image-2025-5-23_14-42-30.png](attachments/image-2025-5-23_14-42-30.png) | ![image-2025-5-23_13-52-5.png](attachments/image-2025-5-23_13-52-5.png) |
| Memory | 33.3GB→34.5GB ![image-2025-5-23_14-42-53.png](attachments/image-2025-5-23_14-42-53.png) | 33.3GB->35.3GB ![image-2025-5-23_13-52-27.png](attachments/image-2025-5-23_13-52-27.png) |
| Network | ![image-2025-5-23_14-44-4.png](attachments/image-2025-5-23_14-44-4.png) | ![image-2025-5-23_13-52-57.png](attachments/image-2025-5-23_13-52-57.png) |
| Disk IO | ![image-2025-5-23_14-44-37.png](attachments/image-2025-5-23_14-44-37.png) | ![image-2025-5-23_13-53-20.png](attachments/image-2025-5-23_13-53-20.png) |