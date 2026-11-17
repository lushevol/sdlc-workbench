# Uber Logical Diagram

# New Table Created (FXU related table not included）

--- group - ratan_inbound_message ---CREATE TABLE if not exists ratan_cashflow_group_management_service.ratan_inbound_message (
id bigserial NOT NULL,
correlation_id text NOT NULL,
trade_id text NOT NULL,
status text NOT NULL DEFAULT 'VALIDATED'::text,
message text NOT NULL,
message_type text NOT NULL,
created_at timestamp NOT NULL,
updated_at timestamp NOT NULL,
version int4 NOT NULL,
CONSTRAINT ratan_uber_message_pk PRIMARY KEY (id)
);
CREATE INDEX if not exists ratan_inbound_message_trade_id_idx ON ratan_cashflow_group_management_service.ratan_inbound_message (trade_id);
CREATE INDEX if not exists ratan_inbound_message_tracking_id_idx ON ratan_cashflow_group_management_service.ratan_inbound_message (correlation_id);

--- group - ratan_cashflow_rounding_config ---
CREATE TABLE IF NOT EXISTS ratan_cashflow_group_management_service.ratan_cashflow_rounding_config (
k_currency text NOT NULL,
v_precision int2 NULL,
v_type text NULL,
CONSTRAINT ratan_cashflow_rounding_config_pkey PRIMARY KEY (k_currency)
);
CREATE INDEX if not exists idx_ratan_cashflow_rounding_config ON ratan_cashflow_group_management_service.ratan_cashflow_rounding_config USING btree (k_currency);

--- static data - fxu config ---
CREATE TABLE IF NOT EXISTS ratanone.ratan_fxu_config (
id SERIAL PRIMARY KEY,
booking_entity_fmid TEXT NOT NULL,
counterparty_fmid TEXT NOT NULL,
booking_entity_fmcode TEXT NOT NULL,
counterparty_fmcode TEXT NOT NULL,
is_auto_utilize BOOLEAN NOT NULL,
settlement_means TEXT NOT NULL,
settlement_account TEXT NOT NULL,
data_status text NULL,
maker_id text NULL default 'System',
checker_id text NULL default 'System',
update_record_id int8 NULL,
created_at timestamp NOT NULL DEFAULT now(),
updated_at timestamp NOT NULL DEFAULT now()
);

--- static data - fxu config audit ---
CREATE TABLE IF NOT EXISTS ratanone.ratan_fxu_config_audit (
id SERIAL PRIMARY KEY,
ratan_fxu_config_id int8 NOT NULL,
snapshot text NOT NULL,
data_status text NULL,
user_id text NULL default 'System',
created_at timestamp NOT NULL
);

# Existing Table Updated (FXU related table not included）

--- group ---
ALTER TABLE ratan_cashflow_group_management_service.ratan_cashflow_group_message ADD COLUMN IF NOT EXISTS raw_message_type text NOT NULL DEFAULT 'XML';
ALTER TABLE ratan_cashflow_group_management_service.ratan_cashflow_group_message_history ALTER COLUMN raw_message DROP NOT NULL;
--- accounting ---
ALTER TABLE ratan_cash_accounting_service.ratan_accounting_request_task ADD COLUMN IF NOT EXISTS meta_data varchar NULL;
ALTER TABLE ratan_cash_accounting_service.ratan_accounting_request_task_history ADD COLUMN IF NOT EXISTS meta_data varchar NULL;