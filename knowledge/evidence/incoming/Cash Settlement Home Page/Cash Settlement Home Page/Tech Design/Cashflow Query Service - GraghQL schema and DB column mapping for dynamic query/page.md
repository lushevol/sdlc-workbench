---

Recently we found there are mismatching between UI and query service on filter definition, the reason is UI get fields list defined in rule service, but query service maintained a separate mapping.
Here is a solution on data modelling management.
Rule service is defined as a domain service to maintain all the fields defined, it should work as the central system to provide all the supported fields, to ensure query service always maintain a list that can cover all fields displayed on UI.

| Module | Changes | |
| --- | --- | --- |
| Rule service | 1. Expose an API to provide the mapping of logical model vs. xpath (by version and context) 2. Versioned xpath data 3. Publish event on data version upgrading (Optional) | |
| Query service | 1. Remove the xpath mapping locally and transform with SDK 2. Query and indexing based on the jsonb | |
| SDK (ratanone-foundation) | 1. Predefined mapping file + version (from rule service latest version) 2. Provide an API to transform from SCBML to logical model json 3. Query the mapping from Rules service (by version and context (RATAN_DATA + CASHFLOW_DATA)) (Optional) 4. Cache the data based on the active version, refresh hourly (Optional) 5. Consume data version upgrading event and refresh the cache (Optional) | Version changed > Cache > Local mapping |

This table used for cashflow dynamic query mapping which includes:

1. GraghQA filter to DB column naming convention and mapping rule. Common mapping rule is 1. Replace "." to "__" 2. Replace "Settlement_Instruction" to "ssi" 3. To lowercase
2. DB column to GraghQL Response schema mapping.

| SN. | Category | Logical Model(Filter Field) | Table Column Name | Comments | | |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | - | id | Technical/Audit | | |
| 2 | | - | created_at | Technical/Audit | | |
| 3 | | - | updated_at | Technical/Audit | | |
| 4 | | - | ratan_label | Technical/Audit | | |
| 5 | Cashflow | Cashflow.Cashflow_Id | cashflow__cashflow_id | Business | | |
| 6 | Cashflow | Cashflow.Cashflow_Version | cashflow__cashflow_version | Business | | |
| 7 | Cashflow | Cashflow.Cashflow_Business_Version | cashflow__cashflow_business_version | Business | | |
| 8 | Cashflow | Cashflow.Cashflow_State | cashflow__cashflow_state | Business | | |
| 9 | Cashflow | Cashflow.Cashflow_Event_Type | cashflow__cashflow_event_type | Business | | |
| 10 | Cashflow | Cashflow.Status_Event_Type | cashflow__status_event_type | Business | | |
| 11 | Cashflow | Cashflow.Event_Date | cashflow__event_date | Business | | |
| 12 | Cashflow | Cashflow.Payment_Payer_Party_Reference | cashflow__payment_payer_party_reference | Business | | |
| 13 | Cashflow | Cashflow.Payment_Receiver_Party_Reference | cashflow__payment_receiver_party_reference | Business | | |
| 14 | Cashflow | Cashflow.Payment_Currency | cashflow__payment_currency | Business | | |
| 15 | Cashflow | Cashflow.Payment_Amount | cashflow__payment_amount | Business | | |
| 16 | Cashflow | Cashflow.Payment_Date | cashflow__payment_date | Business | | |
| 17 | Cashflow | Cashflow.Payment_Date_Business_Day_Convention | cashflow__payment_date_business_day_convention | Business | | |
| 18 | Cashflow | Cashflow.Netting_Id | cashflow__netting_id | Business | | |
| 19 | Cashflow | Cashflow.Pay_Receive_Indicator | cashflow__pay_receive_indicator | Business | | |
| 20 | Cashflow | Cashflow.Payer_Name | cashflow__payer_name | Business | | |
| 21 | Cashflow | Cashflow.Is_Private_Banking_Cashflow | cashflow__is_private_banking_cashflow | Business | | |
| 22 | Cashflow | Cashflow.Is_Amended_Post_Settlement | cashflow__is_amended_post_settlement | Business | | |
| 23 | Cashflow | Cashflow.Payment_Type | cashflow__payment_type | Business | | |
| 24 | Cashflow | Cashflow.Is_Cashflow_Unnet | cashflow__is_cashflow_unnet | Business | | |
| 25 | Cashflow | Cashflow.Transaction_Details | cashflow__transaction_details | Business | | |
| 26 | Cashflow | Cashflow.Cashflow_Affirmation_Status | cashflow__cashflow_affirmation_status | Business | | |
| 27 | Cashflow | Cashflow.Is_STP | cashflow__is_stp | Business | | |
| 28 | Cashflow | Cashflow.Is_STP_RATAN | cashflow__is_stp_ratan | Business | | |
| 29 | Cashflow | Cashflow.NSTP_Reason | cashflow__nstp_reason | Business | | |
| 30 | Cashflow | Cashflow.Execution_Date_Time | cashflow__execution_date_time | Business | | |
| 31 | Cashflow | Cashflow.Cashflow_Sub_State | cashflow__cashflow_sub_state | Business | | |
| 32 | Cashflow | Cashflow.Cashflow_Sub_State_Updater | cashflow__cashflow_sub_state_updater | Business | | |
| 33 | Cashflow | Cashflow.Cashflow_Sub_State_Type | cashflow__cashflow_sub_state_type | Business | | |
| 34 | Cashflow | Cashflow.Prev_Cashflow_Id | cashflow__prev_cashflow_id | Business | | |
| 35 | Cashflow | Cashflow.Next_Cashflow_Id | cashflow__next_cashflow_id | Business | | |
| 36 | Cashflow | Cashflow.Validation_Status | cashflow__validation_status | Business | | |
| 37 | Cashflow | Cashflow.Exception_Reason | cashflow__exception_reason | Business | | |
| 38 | Cashflow | Cashflow.FMO_Comment | cashflow__fmo_comment | Business | | |
| 39 | Cashflow | Cashflow.FMO_Comment_Updater | cashflow__fmo_comment_updater | Business | | |
| 40 | Cashflow | Cashflow.FMO_Comment_Timestamp | cashflow__fmo_comment_timestamp | Business | | |
| 41 | Cashflow | Cashflow.STP_Cutoff_Date_Time | cashflow__stp_cutoff_date_time | Business | | |
| 42 | Cashflow | Cashflow.Netting_Cuttoff_Date | cashflow__netting_cuttoff_date | Business | | |
| 43 | Cashflow | Cashflow.Booking_Entity_SCI_FMCODE | cashflow__booking_entity_sci_fmcode | Business | | |
| 44 | Cashflow | Cashflow.Cashflow_Audit_Version | cashflow__cashflow_audit_version | Business | | |
| 45 | Cashflow | Cashflow.Payment_Cutoff_Time | cashflow__payment_cutoff_time | Business | | |
| 46 | Cashflow | Cashflow.Minor_Version_Description | cashflow__minor_version_description | Business | | |
| 47 | Cashflow | Cashflow.Bypass_Workflow_Indicator | cashflow__bypass_workflow_indicator | Business | | |
| 48 | Cashflow | Cashflow.Cashflow_Minor_Version | cashflow__cashflow_minor_version | Business | | |
| 49 | Cashflow | Cashflow.Is_Payment_Intent_To_Settle | cashflow__is_payment_intent_to_settle | Business | | |
| 50 | | | cashflow_cashflow_affirmation_status | Duplicate? | | |
| 51 | | | cashflow_cashflow_business_version | Duplicate? | | |
| 52 | | | cashflow_cashflow_version | Duplicate? | | |
| 53 | | | cashflow_id | Duplicate? | | |
| 54 | | | cashflow_index | Unused? | | |
| 55 | | | cashflow_minor_version | Duplicate? | | |
| 56 | | | cashflow_status | Duplicate? | | |
| 57 | | | cashflow_sub_status | Duplicate? | | |
| 58 | | | cashflow_sub_status_type | Duplicate? | | |
| 59 | | | cashflow_sub_status_updater | Duplicate? | | |
| 60 | Data Flow | Data_Flow.Data_Publication_Date_Time | data_flow__data_publication_date_time | Business | | |
| 61 | Data Flow | Data_Flow.Data_Publication_Id | data_flow__data_publication_id | Business | | |
| 62 | Data Flow | Data_Flow.Data_Sender | data_flow__data_sender | Business | | |
| 63 | Data Flow | Data_Flow.Data_Source_System | data_flow__data_source_system | Business | | |
| 64 | Data Flow | Data_Flow.Data_Source_System_Country_Code | data_flow__data_source_system_country_code | Business | | |
| 65 | Data Flow | Data_Flow.Data_Source_System_Domain_Name | data_flow__data_source_system_domain_name | Business | | |
| 66 | Data Flow | Data_Flow.Data_Type | data_flow__data_type | Business | | |
| 67 | Data Flow | Data_Flow.Unique_Identifier_Message_Id | data_flow__unique_identifier_message_id | Business | | |
| 68 | Entity | Entity.Booking_Entity_SCI_FMCODE | entity__booking_entity_sci_fmcode | Business | | |
| 69 | Entity | Entity.Booking_Entity_SCI_FMID | entity__booking_entity_sci_fmid | Business | | |
| 70 | Entity | Entity.Counterparty_SCI_FMID | entity__counterparty_sci_fmid | Business | | |
| 71 | Entity | Entity.Counterparty_SCI_FMCODE | entity__counterparty_sci_fmcode | Business | | |
| 72 | Entity | Entity.Counterparty_CIF_Code | entity__counterparty_cif_code | Business | | |
| 73 | Entity | Entity.Counterparty_Source_System_Entity_Id | entity__counterparty_source_system_entity_id | Business | | |
| 74 | Entity | Entity.General_Ledger_Business_Unit_Name | entity__general_ledger_business_unit_name | Business | | |
| 75 | Entity | Entity.Booking_Entity_General_Ledger_Business_Unit_Id | entity__booking_entity_general_ledger_business_unit_id | Business | | |
| 76 | Entity Person | Entity.Person.Coverage_Marketer_PSID | entity__person__coverage_marketer_psid | Business | | |
| 77 | Entity Person | Entity.Person.Event_Coverage_Marketer_PSID | entity__person__event_coverage_marketer_psid | Business | | |
| 78 | Entity Person | Entity.Person.Execution_Marketer_PSID | entity__person__execution_marketer_psid | Business | | |
| 79 | Entity Person | Entity.Person.Event_Execution_Marketer_PSID | entity__person__event_execution_marketer_psid | Business | | |
| 80 | Entity Person | Entity.Person.Booking_Marketer_PSID | entity__person__booking_marketer_psid | Business | | |
| 81 | Entity Person | Entity.Person.Event_Booking_Marketer_PSID | entity__person__event_booking_marketer_psid | Business | | |
| 82 | Entity Person | Entity.Person.Trader_PSID | entity__person__trader_psid | Business | | |
| 83 | Entity Person | Entity.Person.Event_Trader_PSID | entity__person__event_trader_psid | Business | | |
| 84 | Instrument | Instrument_Common.Source_System_Instrument_Sub_Type | instrument_common__source_system_instrument_sub_type | Business | | |
| 85 | Instrument | Instrument_Common.CFI_Code | instrument_common__cfi_code | Business | | |
| 86 | Instrument | Instrument_Common.ISDA_Taxonomy | instrument_common__isda_taxonomy | Business | | |
| 87 | Instrument | Instrument_Common.Equity_Instrument_Reference | | Missing? | | |
| 88 | Instrument | Instrument_Common.Parent_Trade_Instrument | | Missing? | | |
| 89 | Portfolio | Portfolio.Booking_Entity_Trade_Portfolio_Name | portfolio__booking_entity_trade_portfolio_name | Business | | |
| 90 | Portfolio | Portfolio.Booking_Entity_Trade_Portfolio_Unique_Name | portfolio__booking_entity_trade_portfolio_unique_name | Business | | |
| 91 | SSI Account | Settlement_Instruction.Account.SCB_Nostro_Account_Number | ssi__account__scb_nostro_account_number | Business | | |
| 92 | SSI Account | Settlement_Instruction.Account.SCB_Nostro_Account_Type | ssi__account__scb_nostro_account_type | Business | | |
| 93 | SSI Account | Settlement_Instruction.Account.Beneficiary_BIC_code | ssi__account__beneficiary_bic_code | Business | | |
| 94 | SSI Account | Settlement_Instruction.Account.Beneficiary_Account_Name | ssi__account__beneficiary_account_name | Business | | |
| 95 | SSI Account | Settlement_Instruction.Account.Beneficiary_Account_Name_2 | ssi__account__beneficiary_account_name_2 | Business | | |
| 96 | SSI Account | Settlement_Instruction.Account.Beneficiary_Street_Address | ssi__account__beneficiary_street_address | Business | | |
| 97 | SSI Account | Settlement_Instruction.Account.Beneficiary_City | ssi__account__beneficiary_city | Business | | |
| 98 | SSI Account | Settlement_Instruction.Account.Beneficiary_Account_Number | ssi__account__beneficiary_account_number | Business | | |
| 99 | SSI Account | Settlement_Instruction.Account.Intermediary_BIC_code | ssi__account__intermediary_bic_code | Business | | |
| 100 | SSI Account | Settlement_Instruction.Account.Intermediary_Account_Name | ssi__account__intermediary_account_name | Business | | |
| 101 | SSI Account | Settlement_Instruction.Account.Intermediary_Street_Address | ssi__account__intermediary_street_address | Business | | |
| 102 | SSI Account | Settlement_Instruction.Account.Intermediary_City | ssi__account__intermediary_city | Business | | |
| 103 | SSI Account | Settlement_Instruction.Account.Intermediary_Account_Number | ssi__account__intermediary_account_number | Business | | |
| 104 | SSI Account | Settlement_Instruction.Account.Beneficiary_Bank_BIC_code | ssi__account__beneficiary_bank_bic_code | Business | | |
| 105 | SSI Account | Settlement_Instruction.Account.Beneficiary_Bank_Account_Name | ssi__account__beneficiary_bank_account_name | Business | | |
| 106 | SSI Account | Settlement_Instruction.Account.Beneficiary_Bank_Street_Address | ssi__account__beneficiary_bank_street_address | Business | | |
| 107 | SSI Account | Settlement_Instruction.Account.Beneficiary_Bank_City | ssi__account__beneficiary_bank_city | Business | | |
| 108 | SSI Account | Settlement_Instruction.Account.Beneficiary_Bank_Account_Number | ssi__account__beneficiary_bank_account_number | Business | | |
| 109 | SSI Account | Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code | ssi__account__beneficiary_correspondent_bic_code | Business | | |
| 110 | SSI Account | Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name | ssi__account__beneficiary_correspondent_account_name | Business | | |
| 111 | SSI Account | Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address | ssi__account__beneficiary_correspondent_street_address | Business | | |
| 112 | SSI Account | Settlement_Instruction.Account.Beneficiary_Correspondent_City | ssi__account__beneficiary_correspondent_city | Business | | |
| 113 | SSI Account | Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number | ssi__account__beneficiary_correspondent_account_number | Business | | |
| 114 | SSI Account | Settlement_Instruction.Account.Ordering_Customer_BIC_Code | ssi__account__ordering_customer_bic_code | Business | | |
| 115 | SSI Account | Settlement_Instruction.Account.Ordering_Customer_Account_Name | ssi__account__ordering_customer_account_name | Business | | |
| 116 | SSI Account | Settlement_Instruction.Account.Ordering_Customer_Street_Address | ssi__account__ordering_customer_street_address | Business | | |
| 117 | SSI Account | Settlement_Instruction.Account.Ordering_Customer_City | ssi__account__ordering_customer_city | Business | | |
| 118 | SSI Account | Settlement_Instruction.Account.Ordering_Customer_Account_Number | ssi__account__ordering_customer_account_number | Business | | |
| 119 | SSI Account | Settlement_Instruction.Account.Counterparty_CMS_Account_Number | ssi__account__counterparty_cms_account_number | Business | | |
| 120 | SSI Account | Settlement_Instruction.Account.EBBS_Bridge_Account_Number | ssi__account__ebbs_bridge_account_number | Business | | |
| 121 | SSI Account | Settlement_Instruction.Account.EBBS_Account_Number | ssi__account__ebbs_account_number | Business | | |
| 122 | SSI Account | Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code | ssi__account__booking_entity_correspondent_bic_code | Business | | |
| 123 | SSI Account | Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name | ssi__account__booking_entity_correspondent_account_name | Business | | |
| 124 | SSI Account | Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address | ssi__account__booking_entity_correspondent_street_address | Business | | |
| 125 | SSI Account | Settlement_Instruction.Account.Booking_Entity_Correspondent_City | ssi__account__booking_entity_correspondent_city | Business | | |
| 126 | SSI Account | Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number | ssi__account__booking_entity_correspondent_account_number | Business | | |
| 127 | SSI | Settlement_Instruction.SSI_Unique_Id | ssi__ssi_unique_id | Business | | |
| 128 | SSI | Settlement_Instruction.SSI_Source | ssi__ssi_source | Business | | |
| 129 | SSI | Settlement_Instruction.SSI_Priority | ssi__ssi_priority | Business | | |
| 130 | SSI | Settlement_Instruction.Swift_Message_Type | ssi__swift_message_type | Business | | |
| 131 | SSI | Settlement_Instruction.Remittance_Information_1 | ssi__remittance_information_1 | Business | | |
| 132 | SSI | Settlement_Instruction.Remittance_Information_2 | ssi__remittance_information_2 | Business | | |
| 133 | SSI | Settlement_Instruction.Remittance_Information_3 | ssi__remittance_information_3 | Business | | |
| 134 | SSI | Settlement_Instruction.Remittance_Information_4 | ssi__remittance_information_4 | Business | | |
| 135 | SSI | Settlement_Instruction.Sender_To_Receiver_Information_1 | ssi__sender_to_receiver_information_1 | Business | | |
| 136 | SSI | Settlement_Instruction.Sender_To_Receiver_Information_2 | ssi__sender_to_receiver_information_2 | Business | | |
| 137 | SSI | Settlement_Instruction.Sender_To_Receiver_Information_3 | ssi__sender_to_receiver_information_3 | Business | | |
| 138 | SSI | Settlement_Instruction.Sender_To_Receiver_Information_4 | ssi__sender_to_receiver_information_4 | Business | | |
| 139 | SSI | Settlement_Instruction.Sender_To_Receiver_Information_5 | ssi__sender_to_receiver_information_5 | Business | | |
| 140 | SSI | Settlement_Instruction.Sender_To_Receiver_Information_6 | ssi__sender_to_receiver_information_6 | Business | | |
| 141 | SSI | | ssi__is_third_party_payment | Unused? | | |
| 142 | SSI | | ssi__charge_bearer | Unused? | | |
| 143 | SSI | | ssi__nostro_swift_message_type | Unused? | | |
| 144 | SSI | | ssi__swift_payment_method | Unused? | | |
| 145 | Trade | Trade.Event_Physical_Status | trade__event_physical_status | Business | | |
| 146 | Trade | Trade.Resultant_Position_Id | trade__resultant_position_id | Business | | |
| 147 | Trade | Trade.Trade_Original_Source_System_Name | trade__trade_original_source_system_name | Business | | |
| 148 | Trade | Trade.Action_Type | trade__action_type | Business | | |
| 149 | Trade | Trade.Trade_Lake_Valid_From_Date_Time | trade__trade_lake_valid_from_date_time | Business | | |
| 150 | Trade | Trade.Trade_Lake_Valid_To_Date_Time | trade__trade_lake_valid_to_date_time | Business | | |
| 151 | Trade | Trade.Trade_Lake_Latest_Event_Date_Time | trade__trade_lake_latest_event_date_time | Business | | |
| 152 | Trade | Trade.Trade_Lake_Raw_Event_Date_Time | trade__trade_lake_raw_event_date_time | Business | | |
| 153 | Trade | Trade.Trade_Lake_Transaction_From_Date_Time | trade__trade_lake_transaction_from_date_time | Business | | |
| 154 | Trade | Trade.Trade_Lake_Transaction_To_Date_Time | trade__trade_lake_transaction_to_date_time | Business | | |
| 155 | Trade | Trade.BCS_Parent_Trade_Id | trade__bcs_parent_trade_id | Business | | |
| 156 | Trade | Trade.BCS_Trade_Id | trade__bcs_trade_id | Business | | |
| 157 | Trade | Trade.Trade_Version | trade__trade_version | Business | | |
| 158 | Trade | Trade.Trade_State | trade__trade_state | Business | | |
| 159 | Trade | Trade.Trade_Id | trade__trade_id | Business | | |
| 160 | Trade | Trade.Position_Id | trade__position_id | Business | | |
| 161 | Trade | Trade.Parent_Trade_Id | trade__parent_trade_id | Business | | |
| 162 | Trade | Trade.Settlement_Method | trade__settlement_method | Business | | |
| 163 | Trade | Trade.Delivery_Method | trade__delivery_method | Business | | |