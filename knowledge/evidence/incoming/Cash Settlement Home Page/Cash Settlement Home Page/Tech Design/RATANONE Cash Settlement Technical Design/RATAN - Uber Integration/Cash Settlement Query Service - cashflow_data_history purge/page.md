# Background

Cashflow_data_history table growth very fast will impact our DB resource (Disk space) not enough. So we need to consider how to purge this table

# Purge Plan

1. Directly update big jsonb data to small jsonb.
2. Use temporary table to do the same thing, and rename.

**Testing Env: DEV**

| table name | description | rows estimation | Index Created |
| --- | --- | --- | --- |
| cashflow_data_history | original table | ~169w | yes |
| cashflow_data_history_temp_original | original table structure with 1000000 records | 100w | no |
| cashflow_data_history_temp_slim_key_column | only cashflow data change to small object | 100w | no |
| cashflow_data_history_temp_slim_all_column | only keep key columns value, others set to null | 100w | no |
| cashflow_data_history_temp_slim | only keep key columns | 100w | no |

## Option 1 Direct update table

### Before update - query table size

table size of cashflow_data_history_temp_original is

```sql
table_name                                |relid     |total_size|table_size|fsm_size|vm_size|toast_size_index_size|
------------------------------------------+----------+----------+----------+--------+-------+---------------------+
cashflow_data_history                     |1500907339|10 GB     |1648 MB   |432 kB  |56 kB  |8677 MB              |
cashflow_data_history_temp_original       |4252381026|5535 MB   |1004 MB   |272 kB  |32 kB  |4530 MB              |
cashflow_data_history_temp_slim_key_column|4252124751|1703 MB   |1412 MB   |376 kB  |48 kB  |291 MB               |
cashflow_data_history_temp_slim_all_column|4251832532|537 MB    |537 MB    |152 kB  |24 kB  |8192 bytes           |
cashflow_data_history_temp_slim           |4251828143|519 MB    |519 MB    |152 kB  |24 kB  |8192 bytes           |
```

### Execute update

```sql
update
	cash_settlement_query_cn.cashflow_data_history
set
	cashflow = json_build_object('Cashflow',
json_build_object(
'Cashflow_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Id'),
'Cashflow_Minor_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Minor_Version'),
'Cashflow_Business_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Business_Version'),
'Cashflow_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Version'),
'Cashflow_Sub_State', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Sub_State'),
'Cashflow_Event_Type', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Event_Type'),
'Cashflow_State', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State'),
'Status_Event_Type', jsonb_extract_path_text(cashflow, 'Cashflow', 'Status_Event_Type'),
'Cashflow_Sub_State_Updater', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Sub_State_Updater'),
'Payment_Date', jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date'),
'Netting_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Netting_Id'),
'Splitting_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Splitting_Id'),
'NSTP_Exception', jsonb_extract_path_text(cashflow, 'Cashflow', 'NSTP_Exception')
)
)
where
	id in (
	select
		id
	from
		cash_settlement_query_cn.cashflow_data_history
	where
		cashflow__payment_date < (
		select
			current_timestamp - interval '3 months')
	limit 100000);
```

### After update - query table size

table size of cashflow_data_history_temp_original is

```sql
table_name                                |relid     |total_size|table_size|fsm_size|vm_size|toast_size_index_size|
------------------------------------------+----------+----------+----------+--------+-------+---------------------+
cashflow_data_history_purge               |1500907339|10 GB     |1649 MB   |432 kB  |56 kB  |8685 MB              |
cashflow_data_history_temp_original       |4252381026|6933 MB   |2402 MB   |624 kB  |80 kB  |4530 MB              |
cashflow_data_history_temp_slim_key_column|4252124751|1703 MB   |1412 MB   |376 kB  |48 kB  |291 MB               |
cashflow_data_history                     |4265672353|677 MB    |586 MB    |168 kB  |24 kB  |91 MB                |
cashflow_data_history_temp_slim           |4251828143|519 MB    |519 MB    |152 kB  |24 kB  |8192 bytes           |
```

### Vacuum table cashflow_data_history_temp_original; --37.553

```sql
vacuum full cash_settlement_query_cn.cashflow_data_history_temp_original; -- time cost is 37.553
```

### After Vacuum - query table size

table size of cashflow_data_history_temp_original is

```sql
table_name                                |relid     |total_size|table_size|fsm_size|vm_size|toast_size_index_size|
------------------------------------------+----------+----------+----------+--------+-------+---------------------+
cashflow_data_history_purge               |1500907339|10 GB     |1649 MB   |432 kB  |56 kB  |8685 MB              |
cashflow_data_history_temp_original       |4252381026|1692 MB   |1399 MB   |0 bytes |0 bytes|293 MB               |
cashflow_data_history_temp_slim_key_column|4252124751|1703 MB   |1412 MB   |376 kB  |48 kB  |291 MB               |
cashflow_data_history                     |4265672353|677 MB    |586 MB    |168 kB  |24 kB  |91 MB                |
cashflow_data_history_temp_slim           |4251828143|519 MB    |519 MB    |152 kB  |24 kB  |8192 bytes           |
```

## Conclusion:

jsonb column update will cause table size increase a bit(5535M->6933M), but will decrease more(6933M→1692M) after vacuum.

vacuum 1million record need 37s+ time cost, so it will take longer time on prod table volumn(54 million by now)

## Option 2 Use temporary table and rename

Query table size

SQL:

```sql
SELECT 
    st.relname AS table_name,
    relid,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    pg_size_pretty(pg_relation_size(relid)) AS table_size,
--    pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS index_size, -- index + toast +  FSM&VM
    pg_size_pretty(pg_relation_size(relid, 'fsm')) AS fsm_size,
    pg_size_pretty(pg_relation_size(relid, 'vm')) AS vm_size
FROM 
    pg_catalog.pg_statio_user_tables st
--    pg_class c
where schemaname = 'cash_settlement_query_cn'
and st.relname like 'cashflow_data_history%'
--and c.relnamespace = 21914
ORDER BY 
    pg_total_relation_size(relid) DESC;
```

```sql
table_name                                |relid     |total_size|table_size|fsm_size|vm_size|toast_size_index_size|
------------------------------------------+----------+----------+----------+--------+-------+---------------------+
cashflow_data_history                     |1500907339|10 GB     |1648 MB   |432 kB  |56 kB  |8677 MB              |
cashflow_data_history_temp_original       |4252381026|5535 MB   |1004 MB   |272 kB  |32 kB  |4530 MB              |
cashflow_data_history_temp_slim_key_column|4252124751|1703 MB   |1412 MB   |376 kB  |48 kB  |291 MB               |
cashflow_data_history_temp_slim_all_column|4251832532|537 MB    |537 MB    |152 kB  |24 kB  |8192 bytes           |
cashflow_data_history_temp_slim           |4251828143|519 MB    |519 MB    |152 kB  |24 kB  |8192 bytes           |
```

The result indicate the toast_size + index_size with big jsonb object is very huge, then query index

```sql
select
	n.nspname as schema_name,
	c.relname as index_name,
	t.relname as table_name,
	pg_size_pretty(pg_relation_size(c.oid)) as index_size
from
	pg_class c
join 
    pg_namespace n on
	n.oid = c.relnamespace
join 
    pg_index i on
	i.indexrelid = c.oid
join 
    pg_class t on
	i.indrelid = t.oid
where
	nspname = 'cash_settlement_query_cn'
	and t.relname like 'cashflow_data_history%'
order by
	pg_relation_size(c.oid) desc;
```

```sql
schema_name             |index_name                                  |table_name           |index_size|
------------------------+--------------------------------------------+---------------------+----------+
cash_settlement_query_cn|cashflow_data_history_pkey                  |cashflow_data_history|131 MB    |
cash_settlement_query_cn|cashflow_data_history_cashflowa_id_idx      |cashflow_data_history|30 MB     |
cash_settlement_query_cn|cashflow_history_jsonb_nettingid_idx        |cashflow_data_history|21 MB     |
cash_settlement_query_cn|index_cashflow_history_jsonb_nettingid_btree|cashflow_data_history|21 MB     |
cash_settlement_query_cn|cashflow_data_history_cashflowaction_idx    |cashflow_data_history|20 MB     |
cash_settlement_query_cn|cashflow_data_history_jsonb_splitting_id    |cashflow_data_history|11 MB     |

```

Total Index size for table cashflow_data_history is only 234M, far less than 8677 MB, the difference is TOAST size.

**TOAST - Oversized-Attribute Storage Technique**

**Reference Documents**

1. Why PostgreSQL's TOAST is a Critical Player for Managing Large Rows:

https://kenwagatsuma.com/blog/postgresql-toast-for-managing-large-rows

2. What Is TOAST (and Why It Isn’t Enough for Data Compression in Postgres):

[https://www.tigerdata.com/blog/what-is-toast-and-why-it-isnt-enough-for-data-compression-in-postgres](https://www.tigerdata.com/blog/what-is-toast-and-why-it-isnt-enough-for-data-compression-in-postgres)

Query Toast table name and size

```sql
select
--	c.*,
    c.relname AS table_name,
    t.relname AS toast_table_name,
    pg_size_pretty(pg_total_relation_size(c.reltoastrelid)) AS toast_table_size
FROM
    pg_class c
JOIN
    pg_class t ON c.reltoastrelid = t.oid
WHERE
    c.relname like 'cashflow_data_history%' order by c.relname, pg_total_relation_size(c.reltoastrelid) desc;
```

```sql
table_name                                |toast_table_name   |toast_table_size|
------------------------------------------+-------------------+----------------+
cashflow_data_history                     |pg_toast_1500907339|8446 MB         |
cashflow_data_history                     |pg_toast_2357637590|142 MB          |
cashflow_data_history                     |pg_toast_2242926923|98 MB           |
cashflow_data_history                     |pg_toast_1448300701|496 kB          |
cashflow_data_history                     |pg_toast_841781793 |112 kB          |
cashflow_data_history                     |pg_toast_690958259 |112 kB          |
cashflow_data_history                     |pg_toast_601010368 |64 kB           |
cashflow_data_history                     |pg_toast_665051007 |8192 bytes      |
cashflow_data_history                     |pg_toast_3426431952|8192 bytes      |
cashflow_data_history_temp_original       |pg_toast_4252381026|4530 MB         |
cashflow_data_history_temp_slim           |pg_toast_4251828143|8192 bytes      |
cashflow_data_history_temp_slim_all_column|pg_toast_4251832532|8192 bytes      |
cashflow_data_history_temp_slim_key_column|pg_toast_4252124751|291 MB          |
```

We can see the **pg_toast_1500907339 **and **pg_toast_4252381026 **are too large because the jsonb object is not slimmed.

**Conclusion**: The size of a jsonb column occupies a significant portion of the overall table size, because PostgreSQL creates a separate TOAST table for large objects.

Slimmed object will only have several key columns: (**Netting ID and splitting ID to be added**)

```sql
(json_build_object('Cashflow', 
json_build_object(
'Cashflow_Id',jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Id'),
'Cashflow_Minor_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Minor_Version'),
'Cashflow_Business_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Business_Version'),
'Cashflow_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Version'),
'Cashflow_Sub_State', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Sub_State'),
'Cashflow_Event_Type', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Event_Type'),
'Cashflow_State', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State'),
'Status_Event_Type', jsonb_extract_path_text(cashflow, 'Cashflow', 'Status_Event_Type'),
'Cashflow_Sub_State_Updater', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Sub_State_Updater'),
'Payment_Date', jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date'),
'Netting_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Netting_Id'),
'Splitting_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Splitting_Id'),
'NSTP_Exception', jsonb_extract_path_text(cashflow, 'Cashflow', 'NSTP_Exception')
)
)) as cashflow,
```

cashflow_data_history_temp_slim_all_column is chosen as the final table, reason as below:

```sql
-- drop
drop table cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column;

-- create
create table cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column as
select
	cdh.id,
	cdh.cashflow__cashflow_id ,
	cdh.cashflow__cashflow_business_version ,
	cdh.cashflow__cashflow_minor_version,
	cdh.cashflow__cashflow_event_type ,
	cdh.cashflow__cashflow_state ,
	cdh.cashflow__cashflow_sub_state,
	cdh.cashflow__status_event_type,
	cdh.cashflow__cashflow_sub_state_updater,
	cdh.cashflow__payment_date,
	cdh.cashflow__nstp_exception,
	cdh.cashflow__netting_id ,
	cdh.cashflow__splitting_id ,
	(json_build_object('Cashflow', 
json_build_object(
'Cashflow_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Id'),
'Cashflow_Minor_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Minor_Version'),
'Cashflow_Business_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Business_Version'),
'Cashflow_Version', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Version'),
'Cashflow_Sub_State', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Sub_State'),
'Cashflow_Event_Type', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Event_Type'),
'Cashflow_State', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State'),
'Status_Event_Type', jsonb_extract_path_text(cashflow, 'Cashflow', 'Status_Event_Type'),
'Cashflow_Sub_State_Updater', jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_Sub_State_Updater'),
'Payment_Date', jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date'),
'Netting_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Netting_Id'),
'Splitting_Id', jsonb_extract_path_text(cashflow, 'Cashflow', 'Splitting_Id'),
'NSTP_Exception', jsonb_extract_path_text(cashflow, 'Cashflow', 'NSTP_Exception')
)
)) as cashflow,
	cdh.created_at,
	cdh.updated_at,
	null as cashflow_index,
	null as cashflow_status,
	null as cashflow_sub_status,
	null as cashflow_sub_status_type,
	null as cashflow_sub_status_updater,
	null as cashflow__cashflow_version,
	null as cashflow__cashflow_affirmation_status,
	null as data_flow__data_publication_date_time,
	null as data_flow__data_publication_id,
	null as data_flow__data_sender,
	null as data_flow__data_source_system,
	null as data_flow__data_source_system_country_code,
	null as data_flow__data_source_system_domain_name,
	null as data_flow__data_type,
	null as cashflow__event_date,
	null as cashflow__payment_payer_party_reference,
	null as cashflow__payment_receiver_party_reference,
	null as cashflow__payment_currency,
	null as cashflow__payment_amount,
	null as cashflow__payment_date_business_day_convention,
	null as instrument_common__cfi_code,
	null as instrument_common__isda_taxonomy,
	null as trade_state,
	null as trade_id,
	null as position_id,
	null as parent_trade_id,
	null as entity__booking_entity_sci_fmcode,
	null as entity__booking_entity_sci_fmid,
	null as entity__counterparty_sci_fmid,
	null as settlement_method,
	null as delivery_method,
	null as entity__counterparty_sci_fmcode,
	null as entity__counterparty_cif_code,
	null as entity__counterparty_source_system_entity_id,
	null as cashflow__pay_receive_indicator,
	null as cashflow__payer_name,
	null as cashflow__is_private_banking_cashflow,
	null as cashflow__is_amended_post_settlement,
	null as cashflow__payment_type,
	null as cashflow__is_cashflow_unnet,
	null as cashflow__transaction_details,
	null as data_flow__unique_identifier_message_id,
	null as cashflow__execution_date_time,
	null as entity__general_ledger_business_unit_name,
	null as entity__booking_entity_general_ledger_business_unit_id,
	null as trade__trade_lake_valid_from_date_time,
	null as trade__trade_lake_valid_to_date_time,
	null as trade__trade_lake_latest_event_date_time,
	null as trade__trade_lake_raw_event_date_time,
	null as trade__trade_lake_transaction_from_date_time,
	null as trade__trade_lake_transaction_to_date_time,
	null as bcs_parent_trade_id,
	null as bcs_trade_id,
	null as trade_version,
	null as portfolio__booking_entity_trade_portfolio_name,
	null as cashflow__is_stp,
	null as cashflow__is_stp_ratan,
	null as cashflow__nstp_reason,
	null as ssi__account__ebbs_bridge_account_number,
	null as ssi__account__ebbs_account_number,
	null as ssi__account__booking_entity_correspondent_bic_code,
	null as ssi__account__booking_entity_correspondent_account_name,
	null as ssi__account__booking_entity_correspondent_street_address,
	null as ssi__account__booking_entity_correspondent_city,
	null as ssi__account__booking_entity_correspondent_account_number,
	null as cashflow__cashflow_sub_state_type,
	null as cashflow__prev_cashflow_id,
	null as cashflow__next_cashflow_id,
	null as cashflow__validation_status,
	null as cashflow__exception_reason,
	null as cashflow__fmo_comment,
	null as cashflow__fmo_comment_updater,
	null as cashflow__fmo_comment_timestamp,
	null as cashflow__stp_cutoff_date_time,
	null as cashflow__netting_cuttoff_date,
	null as cashflow__booking_entity_sci_fmcode,
	null as cashflow__cashflow_audit_version,
	null as cashflow__payment_cutoff_time,
	null as ssi__nostro_swift_message_type,
	null as cashflow__minor_version_description,
	null as cashflow__bypass_workflow_indicator,
	null as ssi__ssi_unique_id,
	null as ssi__ssi_source,
	null as ssi__ssi_priority,
	null as ssi__swift_message_type,
	null as ssi__account__scb_nostro_account_number,
	null as ssi__account__scb_nostro_account_type,
	null as ssi__account__beneficiary_bic_code,
	null as ssi__account__beneficiary_account_name,
	null as ssi__account__beneficiary_account_name_2,
	null as ssi__account__beneficiary_street_address,
	null as ssi__account__beneficiary_city,
	null as ssi__account__beneficiary_account_number,
	null as ssi__account__intermediary_bic_code,
	null as ssi__account__intermediary_account_name,
	null as ssi__account__intermediary_street_address,
	null as ssi__account__intermediary_city,
	null as ssi__account__intermediary_account_number,
	null as ssi__account__beneficiary_bank_bic_code,
	null as ssi__account__beneficiary_bank_account_name,
	null as ssi__account__beneficiary_bank_street_address,
	null as ssi__account__beneficiary_bank_city,
	null as ssi__account__beneficiary_bank_account_number,
	null as ssi__account__beneficiary_correspondent_bic_code,
	null as ssi__account__beneficiary_correspondent_account_name,
	null as ssi__account__beneficiary_correspondent_street_address,
	null as ssi__account__beneficiary_correspondent_city,
	null as ssi__account__beneficiary_correspondent_account_number,
	null as ssi__account__ordering_customer_bic_code,
	null as ssi__account__ordering_customer_account_name,
	null as ssi__account__ordering_customer_street_address,
	null as ssi__account__ordering_customer_city,
	null as ssi__account__ordering_customer_account_number,
	null as ssi__remittance_information_1,
	null as ssi__remittance_information_2,
	null as ssi__remittance_information_3,
	null as ssi__remittance_information_4,
	null as ssi__sender_to_receiver_information_1,
	null as ssi__sender_to_receiver_information_2,
	null as ssi__sender_to_receiver_information_3,
	null as ssi__sender_to_receiver_information_4,
	null as ssi__sender_to_receiver_information_5,
	null as ssi__sender_to_receiver_information_6,
	null as ssi__account__counterparty_cms_account_number,
	null as ssi__is_third_party_payment,
	null as ssi__swift_payment_method,
	null as ssi__charge_bearer,
	null as instrument_common__source_system_instrument_sub_type,
	null as portfolio__booking_entity_trade_portfolio_unique_name,
	null as entity__person__coverage_marketer_psid,
	null as entity__person__event_coverage_marketer_psid,
	null as entity__person__execution_marketer_psid,
	null as entity__person__event_execution_marketer_psid,
	null as entity__person__booking_marketer_psid,
	null as entity__person__event_booking_marketer_psid,
	null as entity__person__trader_psid,
	null as entity__person__event_trader_psid,
	null as trade__event_physical_status,
	null as trade__resultant_position_id,
	null as trade_original_source_system_name,
	null as cashflow__is_payment_intent_to_settle,
	null as trade__action_type,
	null as ratan_label,
	null as cashflowaction,
	null as cashflowactiontime,
	null as cashflowexceptiontype,
	null as entity__counterparty_client_type,
	null as trade_purpose,
	null as tp_system_name,
	null as ssi__value_date_business_day_convention,
	null as ssi__value_date,
	null as instrument_common__financial_instrument_code,
	null as entity__booking_entity_country_iso_code,
	null as effective_date_time,
	null as cashflow_sequence,
	null as cashflow__position_id,
	null as cashflow__event_physical_status,
	null as cashflow__cashflow_subevent_type,
	null as cashflow__cashflow_major_version,
	null as cashflow__cashflow_event_reason,
	null as cashflow__action_type,
	null as ssi__nostro_id,
	null as cashflow__general_ledger_owner_id,
	null as cashflow__is_netting_required,
	null as entity__counterparty_is_internal,
	null as cashflow__accounting_reason,
	null as cashflow__accounting_status,
	null as instrument_common__murex_product_family,
	null as instrument_common__murex_product_group,
	null as instrument_common__murex_product_type,
	null as instrument_common__murex_product_typology,
	null as instrument_common__murex_product_strategy,
	null as cashflow__swift_status,
	null as cashflow__swift_reason,
	null as cashflow__swift_message_standard,
	null as trade_date,
	null as entity__counterparty_murex_display_shortcode,
	null as entity__counterparty_sci_bic_code,
	null as entity__counterparty_sci_domicile_country,
	null as entity__counterparty_sci_bic_net_flag,
	null as cashflow__is_commodity,
	null as linked_trade_id,
	null as cashflow__is_pending_fixing,
	null as cashflow__clearing_alpha,
	null as cashflow__nd_parent_trade_id,
	null as cashflow__nd_parent_typology,
	null as cashflow__pending_fixing_flag,
	null as cashflow__duplicate_nds_fxd,
	null as ssi__account__pop_dubai
from
	cash_settlement_query_cn.cashflow_data_history cdh
limit 1000000;
```

1. No DB structure changes, no entity changes, all fields in entity definition are there, no need to change entities and domain event processing logic.
2. toast table size is good， only 8192 bytes/million
3. code change is minor change, only need to keep key columns has value, others we can set to null.

But still need to test:
1. null value fields don't make NPE happen.
2. Function will not be impact for data processing.
3. The purge script will not take long time.

After indexes created:

```sql
ALTER TABLE cash_settlement_query_cn.cashflow_data_history ADD CONSTRAINT cashflow_data_history_pkey PRIMARY KEY (id);
CREATE INDEX cashflow_data_history_new_cashflowa_id_idx ON cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column USING btree (cashflow__cashflow_id);
CREATE INDEX cashflow_data_history_new_cashflowaction_idx ON cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column USING btree (cashflowaction);
CREATE INDEX cashflow_data_history_new_jsonb_nettingid_idx ON cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column USING btree (jsonb_extract_path_text(cashflow::jsonb, VARIADIC ARRAY['Cashflow'::text, 'Netting_Id'::text]));
CREATE INDEX cashflow_data_history_new_jsonb_splitting_id ON cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column USING btree (jsonb_extract_path_text(cashflow::jsonb, VARIADIC ARRAY['Cashflow'::text, 'Splitting_Id'::text]));
```

```sql
table_name                                |relid     |total_size|table_size|fsm_size|vm_size|toast_size_index_size|
------------------------------------------+----------+----------+----------+--------+-------+---------------------+
cashflow_data_history_purge               |1500907339|10 GB     |1649 MB   |432 kB  |56 kB  |8685 MB              |
cashflow_data_history_temp_original       |4252381026|6933 MB   |2402 MB   |624 kB  |80 kB  |4530 MB              |
cashflow_data_history_temp_slim_key_column|4252124751|1703 MB   |1412 MB   |376 kB  |48 kB  |291 MB               |
cashflow_data_history                     |4265672353|677 MB    |586 MB    |168 kB  |24 kB  |91 MB                |
cashflow_data_history_temp_slim           |4251828143|519 MB    |519 MB    |152 kB  |24 kB  |8192 bytes           |
```

Seems the result looks good. Start to swap the table.

```sql
alter table cash_settlement_query_cn.cashflow_data_history rename to cashflow_data_history_purge;
alter table cash_settlement_query_cn.cashflow_data_history_temp_slim_all_column rename to cashflow_data_history;
```

![image-2025-11-24_18-39-29.png](attachments/image-2025-11-24_18-39-29.png)

![image-2025-11-24_18-40-0.png](attachments/image-2025-11-24_18-40-0.png)