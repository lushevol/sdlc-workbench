```text
{
  cashflowsNew(
    filter: [
        # {field: "Cashflow.Is_STP_Ratan", operator: NE, values: "false"}, 
        {field: "Cashflow.Cashflow_Id", operator: EQ, values: "12070687922588"}]
    page: 0
    size: 5
  ) {
        pageInfo{
        totalHits
        pageNo
        pageSize
        lastPage
        }
        results{
            Trade_Id
            Delivery_Method
                                    Instrument_Common{
                 Source_System_Instrument_Sub_Type
                                                CFI_Code
                                                ISDA_Taxonomy
                                                Equity_Instrument_Reference
                                                Parent_Trade_Instrument
                                    }
                                    Data_Flow{
                                                Data_Publication_Date_Time

                                                Data_Publication_Id

                                                Data_Sender

                                                Data_Source_System

                                                Data_Source_System_Country_Code

                                                Data_Source_System_Domain_Name

                                                Data_Type

                                                Unique_Identifier_Message_Id
                                    }
                                    Entity{
                                                Person{
                                                Coverage_Marketer_PSID

                                                Event_Coverage_Marketer_PSID

                                                Execution_Marketer_PSID

                                                Event_Execution_Marketer_PSID

                                                Booking_Marketer_PSID

                                                Event_Booking_Marketer_PSID

                                                Trader_PSID

                                                Event_Trader_PSID
                                                }
                 
                                                Booking_Entity_SCI_FMCODE
                                                Booking_Entity_SCI_FMID
                                                Counterparty_SCI_FMID
                                                Counterparty_SCI_FMCODE
                                                Counterparty_CIF_Code
                                                Counterparty_Source_System_Entity_Id
                                                General_Ledger_Business_Unit_Name
                                                Booking_Entity_General_Ledger_Business_Unit_Id          
                                                
                                    }
            
                                    Cashflow{
                Cashflow_Id
                                                Cashflow_Version
                                                Cashflow_Business_Version
                                                Cashflow_State
                                                Cashflow_Event_Type
                                                Status_Event_Type
                                                Event_Date
                                                Payment_Payer_Party_Reference
                                                Payment_Receiver_Party_Reference
                                                Payment_Currency
                                                Payment_Amount
                                                Payment_Date
                                                Payment_Date_Business_Day_Convention
                                                Netting_Id
                                                Pay_Receive_Indicator
                                                Payer_Name
                                                Is_Private_Banking_Cashflow
                                                Is_Amended_Post_Settlement
                                                Payment_Type
                                                Is_Cashflow_Unnet
                                                Transaction_Details
                                                Cashflow_Affirmation_Status
                                                Is_STP
                                                Is_STP_RATAN
                                                NSTP_Reason
                                                Execution_Date_Time
                                                Cashflow_Sub_State
                                                Cashflow_Sub_State_Updater
                                                Cashflow_Sub_State_Type
                                                Prev_Cashflow_Id
                                                Next_Cashflow_Id
                                                Validation_Status
                                                Exception_Reason
                                                FMO_Comment
                                                FMO_Comment_Updater
                                                FMO_Comment_Timestamp
                                                STP_Cutoff_Date_Time
                                                Netting_Cuttoff_Date
                                                Booking_Entity_SCI_FMCODE
                                                Cashflow_Audit_Version
                                                Payment_Cutoff_Time
                                                Minor_Version_Description
                                                Bypass_Workflow_Indicator
                                                Cashflow_Minor_Version
                                                Is_Payment_Intent_To_Settle
              }
          
                                    Trade{
             Event_Physical_Status

                                    Resultant_Position_Id

                                    Trade_Original_Source_System_Name

                                    Action_Type

                                    Trade_Lake_Valid_From_Date_Time

                                    Trade_Lake_Valid_To_Date_Time

                                    Trade_Lake_Latest_Event_Date_Time

                                    Trade_Lake_Raw_Event_Date_Time

                                    Trade_Lake_Transaction_From_Date_Time

                                    Trade_Lake_Transaction_To_Date_Time

                                    BCS_Parent_Trade_Id

                                    BCS_Trade_Id

                                    Trade_Version

                                    Trade_State

                                    Position_Id

                                    Parent_Trade_Id

                                    Settlement_Method
          }
         
                                    Settlement_Instruction{
                                                Account{
                                                            SCB_Nostro_Account_Number
                                                            SCB_Nostro_Account_Type
                                                            Beneficiary_BIC_code
                                                            Beneficiary_Account_Name
                                                            Beneficiary_Account_Name_2
                                                            #  Beneficiary_Street_Address
                                                            Beneficiary_City
                                                            Beneficiary_Account_Number
                                                            Intermediary_BIC_code
                                                            Intermediary_Account_Name
                                                            Intermediary_Street_Address
                                                            Intermediary_City
                                                            Intermediary_Account_Number
                                                            Beneficiary_Bank_BIC_code
                                                            Beneficiary_Bank_Account_Name
                                                            Beneficiary_Bank_Street_Address
                                                            Beneficiary_Bank_City
                                                            Beneficiary_Bank_Account_Number
                                                            Beneficiary_Correspondent_BIC_code
                                                            Beneficiary_Correspondent_Account_Name
                                                            Beneficiary_Correspondent_Street_Address
                                                            Beneficiary_Correspondent_City
                                                            Beneficiary_Correspondent_Account_Number
                                                            Ordering_Customer_BIC_Code
                                                            Ordering_Customer_Account_Name
                                                            Ordering_Customer_Street_Address
                                                            Ordering_Customer_City
                                                            Ordering_Customer_Account_Number
                                                            Counterparty_CMS_Account_Number
                                                            EBBS_Bridge_Account_Number
                                                            EBBS_Account_Number
                                                            Booking_Entity_Correspondent_BIC_code
                                                            Booking_Entity_Correspondent_Account_Name
                                                            Booking_Entity_Correspondent_Street_Address
                                                            Booking_Entity_Correspondent_City
                                                            Booking_Entity_Correspondent_Account_Number
                                                                                                }
                                                            SSI_Unique_Id

                                                            SSI_Source

                                                            SSI_Priority

                                                            Swift_Message_Type

                                                            Remittance_Information_1

                                                            Remittance_Information_2

                                                            Remittance_Information_3

                                                            Remittance_Information_4

                                                            Sender_To_Receiver_Information_1

                                                            Sender_To_Receiver_Information_2

                                                            Sender_To_Receiver_Information_3

                                                            Sender_To_Receiver_Information_4

                                                            Sender_To_Receiver_Information_5

                                                            Sender_To_Receiver_Information_6

                                                            Is_Third_Party_Payment

                                                            Swift_Payment_Method

                                                            Charge_Bearer

                                                            Nostro_Swift_Message_Type
                                                }
              Portfolio{
                Booking_Entity_Trade_Portfolio_Name
                Booking_Entity_Trade_Portfolio_Unique_Name
              }
              FMO_Comments{
                FMO_Comment
                FMO_Comment_Updater
                FMO_Comment_Timestamp
              }
        }
  }}
   
```

```bash
{
  "data": {
    "cashflowsNew": {
      "pageInfo": {
        "totalHits": 42,
        "pageNo": 0,
        "pageSize": 5,
        "lastPage": false
      },
      "results": [
        {
          "DataFlow": {
            "data_publication_date_time": "2022-11-17 09:01:30.0",
            "data_publication_id": "STELLA_002022111701_0_1829946-1_1001",
            "data_sender": null,
            "data_source_system": "Stella",
            "data_source_system_country_code": "ALL",
            "data_source_system_domain_name": "FM",
            "data_type": "CashflowData",
            "unique_identifier_message_id": null
          },
          "Entity": {
            "person": {
              "coverage_marketer_psid": "",
              "event_coverage_marketer_psid": null,
              "execution_marketer_psid": "",
              "event_execution_marketer_psid": null,
              "booking_marketer_psid": "",
              "event_booking_marketer_psid": null,
              "trader_psid": "",
              "event_trader_psid": null
            },
            "booking_entity_sci_fmcode": null,
            "booking_entity_sci_fmid": "10075222",
            "counterparty_sci_fmid": null,
            "counterparty_sci_fmcode": "",
            "counterparty_cif_code": "",
            "counterparty_source_system_entity_id": "",
            "general_ledger_business_unit_name": null,
            "booking_entity_general_ledger_business_unit_id": "110"
          },
          "Cashflow": {
            "cashflow_id": "002022111701",
            "cashflow_version": 0,
            "cashflow_business_version": "0",
            "cashflow_state": "PROJECTED",
            "cashflow_event_type": "New",
            "status_event_type": "",
            "event_date": "2022-11-17",
            "payment_payer_party_reference": "party2",
            "payment_receiver_party_reference": "party1",
            "payment_currency": "USD",
            "payment_amount": "1008",
            "payment_date": "2022-11-28",
            "payment_date_business_day_convention": "NONE",
            "netting_id": "",
            "pay_receive_indicator": "party2",
            "payer_name": "",
            "is_private_banking_cashflow": false,
            "is_amended_post_settlement": false,
            "payment_type": "netAmount",
            "is_cashflow_unnet": false,
            "transaction_details": "H4sIAAAAAAAAAKVWWW/bRhD+KwXRR1rlZdoSkAddbpzIjizJLgpDMJbkUFqb5DK7S8VCkf/e2eVtp46RCgJE7c7xzTcX742QpQMRBgNBAg6DOOWQDyKWEpoNNpxkgoSSssww/zGKgkbGyLAs1x9ajns6tC3DNA7AhRIYWaaREw6Z7KqN7t9ycIsW7yr91sFkun6wz23f9eye/e9bE41lkqPtSyXYCtXH6Dp8otnurgMKniXwjCR4F4HSy4okaVXWkkhAYwt6ALREiojKDU3x6N6xHMe0LdOxzKFpu6aLv77nnp1bloVYII4BozzAf4g7vjm0qg+KC1bwENZHISEto1xv5ovFGJ1+Y/wpTti3CsubnAklM/irp4Hc1SauSfo+CxHENKMqSY0xrYu2VBbOTCPTpowpEfvf1iBlAilm11BpoNn4Pfl95WncFJPygUTVTpacPSKZHS6Esv1IDmRQSJoMPiIKBGGY968AbbcKkng3dx08DX0Kju23cFZfPs2nm/nslwEpSEEhaAZCzA94qit2Uhz/WEOSoFlQhysgQrFYluSBJDRCQLpSjVFMEgEYWGO4qepSPMMLrPW2pHecCXGNpxD1erAyFCJMneZSbwUxYLuGUKvn5Ah8Sbg8ItJc/TqIk0MIWOP9C9VzUqGclaSXpW+bLkb9tSCZpEq2oislcj+Y0N0MQpoSjN3edqP6gYn28grkninmlvujoKHSLh3XbdvNVMiKDHtdI9R0e5ble5Zvu4rvClQVK+MyZgllZb/omXOxXj/cfn6YbCaLzQ1q5JyGsDnm2s18NcWjgLMn4LWRlPAnkO3/QgCfslTXQOdIQ2l6PX5eaeTlffy8JJR3MjpOVRBvcGdZ53oOpjmRNKBJN6gDaZKdM6FLXDvvDWxVBsZI8gIqKq+ZEkTjNWZsjqWKvYmTRTQeTwnWSvIivu5VfRaBds54C0xZm4aqfG7XKlNtgrunGs2CBK0pQRIQlxlG2zIGIOpnxumOZkRVczPdO1uB1xW+7JBRahIpSbiHqHvT0cxxjZBdZ1tgltOup6r8qlVSNdYVyXNVDd0xMWVJAroPxe+3maaLkiABlMW5owdXGKRNwGollWGQIdi+F5wFYUCcM8+BwAXPOiWB5Z35Q/BUfPHXFmFQZFHSQRzIYPkyCpoJzLuivbt5f2VHw+np0PLAPnEDPzrxnOD8JHBt+8TxvVOIgig88/1Xy7t1/xOfl63g/3BZdgnL1PBtDIr3pWdFMsQyDkMc3wsq1Jjfbqv0iM7kfDOMmf75EqjN1upUEfWGuWKn8+ZRdw2LivBnXC0rqXqnNnrVZFuSo4p7lFB8WzmGCVawHpVcwnOlW824qT4bXK7we4HlPNCVrtgYVEbU+9Fux2FHysXy44Iy98ecmf1hbJbj1+zP3dac8tJbVJXHElrT+epv0/0kSZgsqwnfVqiYNoOtX2wlES874NX6a68+akMvTz91NjU855QfZ50Z0G69+vVSkfliY8ua0AkR4HuK80fXufpsXbjen+PxzTiarnPx9818rD+L8V3iiJl6vLu7nq8+n+PThw/1asJdk8V01/eo3oChN01EXWLft/8CPL0lbe4LAAA=",
            "cashflow_affirmation_status": "Unaffirmed",
            "is_stp": null,
            "is_stp_ratan": null,
            "nstp_reason": "",
            "execution_date_time": "null",
            "cashflow_sub_state": "NA",
            "cashflow_sub_state_updater": "System",
            "cashflow_sub_state_type": "NA",
            "prev_cashflow_id": null,
            "next_cashflow_id": null,
            "validation_status": null,
            "exception_reason": null,
            "fmo_comment": null,
            "fmo_comment_updater": null,
            "fmo_comment_timestamp": "null",
            "stp_cutoff_date_time": "2022-11-23T21:00:00Z",
            "netting_cuttoff_date": "2022-11-23T21:00:00Z",
            "booking_entity_sci_fmcode": null,
            "cashflow_audit_version": null,
            "payment_cutoff_time": "2022-11-25T00:00:00Z",
            "minor_version_description": "",
            "bypass_workflow_indicator": null,
            "cashflow_minor_version": "",
            "is_payment_intent_to_settle": false
          },
          "Portfolio": {
            "booking_entity_trade_portfolio_name": null,
            "booking_entity_trade_portfolio_unique_name": null
          },
          "Trade": {
            "event_physical_status": "Live",
            "resultant_position_id": "1816352",
            "trade_original_source_system_name": null,
            "action_type": "Project",
            "trade_lake_valid_from_date_time": "null",
            "trade_lake_valid_to_date_time": "null",
            "trade_lake_latest_event_date_time": "null",
            "trade_lake_raw_event_date_time": "null",
            "trade_lake_transaction_from_date_time": "null",
            "trade_lake_transaction_to_date_time": "null",
            "bcs_parent_trade_id": "1816352",
            "bcs_trade_id": "1816352",
            "trade_version": 0,
            "trade_state": "VALIDATED",
            "trade_id": "1816352",
            "position_id": "3690235984",
            "parent_trade_id": "1816352",
            "settlement_method": "",
            "delivery_method": ""
          },
          "Settlement_Instruction": null,
          "FMO_Comments": {
            "FMO_Comment": null,
            "FMO_Comment_Updater": null,
            "FMO_Comment_Timestamp": "null"
          }
        },
        {
          "DataFlow": {
            "data_publication_date_time": "2022-11-16 17:13:30.0",
            "data_publication_id": "STELLA_012022111601_0_1829946-1_1001",
            "data_sender": null,
            "data_source_system": "Stella",
            "data_source_system_country_code": "ALL",
            "data_source_system_domain_name": "FM",
            "data_type": "CashflowData",
            "unique_identifier_message_id": null
          },
          "Entity": {
            "person": {
              "coverage_marketer_psid": "",
              "event_coverage_marketer_psid": null,
              "execution_marketer_psid": "",
              "event_execution_marketer_psid": null,
              "booking_marketer_psid": "",
              "event_booking_marketer_psid": null,
              "trader_psid": "",
              "event_trader_psid": null
            },
            "booking_entity_sci_fmcode": null,
            "booking_entity_sci_fmid": "10075222",
            "counterparty_sci_fmid": null,
            "counterparty_sci_fmcode": "",
            "counterparty_cif_code": "",
            "counterparty_source_system_entity_id": "",
            "general_ledger_business_unit_name": null,
            "booking_entity_general_ledger_business_unit_id": "110"
          },
          "Cashflow": {
            "cashflow_id": "012022111601",
            "cashflow_version": 0,
            "cashflow_business_version": "0",
            "cashflow_state": "PROJECTED",
            "cashflow_event_type": "New",
            "status_event_type": "",
            "event_date": "2022-11-16",
            "payment_payer_party_reference": "party2",
            "payment_receiver_party_reference": "party1",
            "payment_currency": "USD",
            "payment_amount": "1008",
            "payment_date": "2022-11-25",
            "payment_date_business_day_convention": "NONE",
            "netting_id": "",
            "pay_receive_indicator": "party2",
            "payer_name": "",
            "is_private_banking_cashflow": false,
            "is_amended_post_settlement": false,
            "payment_type": "netAmount",
            "is_cashflow_unnet": false,
            "transaction_details": "H4sIAAAAAAAAAKVWWW/bRhD+KwXRR1rlZdoSkAddbpzIjizJLgpDMJbkUFqb5DK7S8VCkf/e2eVtp46RCgJE7c7xzTcX742QpQMRBgNBAg6DOOWQDyKWEpoNNpxkgoSSssww/zGKgkbGyLAs1x9ajns6tC3DNA7AhRIYWaaREw6Z7KqN7t9ycIsW7yr91sFkun6wz23f9eye/e9bE41lkqPtSyXYCtXH6Dp8otnurgMKniXwjCR4F4HSy4okaVXWkkhAYwt6ALREiojKDU3x6N6xHMe0LdOxzKFpu6aLv77nnp1bloVYII4BozzAf4g7vjm0qg+KC1bwENZHISEto1xv5ovFGJ1+Y/wpTti3CsubnAklM/irp4Hc1SauSfo+CxHENKMqSY0xrYu2VBbOTCPTpowpEfvf1iBlAilm11BpoNn4Pfl95WncFJPygUTVTpacPSKZHS6Esv1IDmRQSJoMPiIKBGGY968AbbcKkng3dx08DX0Kju23cFZfPs2nm/nslwEpSEEhaAZCzA94qit2Uhz/WEOSoFlQhysgQrFYluSBJDRCQLpSjVFMEgEYWGO4qepSPMMLrPW2pHecCXGNpxD1erAyFCJMneZSbwUxYLuGUKvn5Ah8Sbg8ItJc/TqIk0MIWOP9C9VzUqGclaSXpW+bLkb9tSCZpEq2oislcj+Y0N0MQpoSjN3edqP6gYn28grkninmlvujoKHSLh3XbdvNVMiKDHtdI9R0e5ble5Zvu4rvClQVK+MyZgllZb/omXOxXj/cfn6YbCaLzQ1q5JyGsDnm2s18NcWjgLMn4LWRlPAnkO3/QgCfslTXQOdIQ2l6PX5eaeTlffy8JJR3MjpOVRBvcGdZ53oOpjmRNKBJN6gDaZKdM6FLXDvvDWxVBsZI8gIqKq+ZEkTjNWZsjqWKvYmTRTQeTwnWSvIivu5VfRaBds54C0xZm4aqfG7XKlNtgrunGs2CBK0pQRIQlxlG2zIGIOpnxumOZkRVczPdO1uB1xW+7JBRahIpSbiHqHvT0cxxjZBdZ1tgltOup6r8qlVSNdYVyXNVDd0xMWVJAroPxe+3maaLkiABlMW5owdXGKRNwGollWGQIdi+F5wFYUCcM8+BwAXPOiWB5Z35Q/BUfPHXFmFQZFHSQRzIYPkyCpoJzLuivbt5f2VHw+np0PLAPnEDPzrxnOD8JHBt+8TxvVOIgig88/1Xy7t1/xOfl63g/3BZdgnL1PBtDIr3pWdFMsQyDkMc3wsq1Jjfbqv0iM7kfDOMmf75EqjN1upUEfWGuWKn8+ZRdw2LivBnXC0rqXqnNnrVZFuSo4p7lFB8WzmGCVawHpVcwnOlW824qT4bXK7we4HlPNCVrtgYVEbU+9Fux2FHysXy44Iy98ecmf1hbJbj1+zP3dac8tJbVJXHElrT+epv0/0kSZgsqwnfVqiYNoOtX2wlES874NX6a68+akMvTz91NjU855QfZ50Z0G69+vVSkfliY8ua0AkR4HuK80fXufpsXbjen+PxzTiarnPx9818rD+L8V3iiJl6vLu7nq8+n+PThw/1asJdk8V01/eo3oChN01EXWLft/8CPL0lbe4LAAA=",
            "cashflow_affirmation_status": "Unaffirmed",
            "is_stp": null,
            "is_stp_ratan": null,
            "nstp_reason": "",
            "execution_date_time": "null",
            "cashflow_sub_state": "NA",
            "cashflow_sub_state_updater": "System",
            "cashflow_sub_state_type": "NA",
            "prev_cashflow_id": null,
            "next_cashflow_id": null,
            "validation_status": null,
            "exception_reason": null,
            "fmo_comment": null,
            "fmo_comment_updater": null,
            "fmo_comment_timestamp": "null",
            "stp_cutoff_date_time": "2022-11-22T21:00:00Z",
            "netting_cuttoff_date": "2022-11-22T21:00:00Z",
            "booking_entity_sci_fmcode": null,
            "cashflow_audit_version": null,
            "payment_cutoff_time": "2022-11-23T00:00:00Z",
            "minor_version_description": "",
            "bypass_workflow_indicator": null,
            "cashflow_minor_version": "",
            "is_payment_intent_to_settle": false
          },
          "Portfolio": {
            "booking_entity_trade_portfolio_name": null,
            "booking_entity_trade_portfolio_unique_name": null
          },
          "Trade": {
            "event_physical_status": "Live",
            "resultant_position_id": "1816352",
            "trade_original_source_system_name": null,
            "action_type": "Project",
            "trade_lake_valid_from_date_time": "null",
            "trade_lake_valid_to_date_time": "null",
            "trade_lake_latest_event_date_time": "null",
            "trade_lake_raw_event_date_time": "null",
            "trade_lake_transaction_from_date_time": "null",
            "trade_lake_transaction_to_date_time": "null",
            "bcs_parent_trade_id": "1816352",
            "bcs_trade_id": "1816352",
            "trade_version": 0,
            "trade_state": "VALIDATED",
            "trade_id": "1816352",
            "position_id": "3690235984",
            "parent_trade_id": "1816352",
            "settlement_method": "",
            "delivery_method": ""
          },
          "Settlement_Instruction": null,
          "FMO_Comments": {
            "FMO_Comment": null,
            "FMO_Comment_Updater": null,
            "FMO_Comment_Timestamp": "null"
          }
        },
        {
          "DataFlow": {
            "data_publication_date_time": "2022-11-12 17:13:30.0",
            "data_publication_id": "STELLA_1816352_0_1829946-1_1001",
            "data_sender": null,
            "data_source_system": "Stella",
            "data_source_system_country_code": "ALL",
            "data_source_system_domain_name": "FM",
            "data_type": "CashflowData",
            "unique_identifier_message_id": null
          },
          "Entity": {
            "person": {
              "coverage_marketer_psid": "",
              "event_coverage_marketer_psid": null,
              "execution_marketer_psid": "",
              "event_execution_marketer_psid": null,
              "booking_marketer_psid": "",
              "event_booking_marketer_psid": null,
              "trader_psid": "",
              "event_trader_psid": null
            },
            "booking_entity_sci_fmcode": null,
            "booking_entity_sci_fmid": "10075222",
            "counterparty_sci_fmid": null,
            "counterparty_sci_fmcode": "",
            "counterparty_cif_code": "",
            "counterparty_source_system_entity_id": "",
            "general_ledger_business_unit_name": null,
            "booking_entity_general_ledger_business_unit_id": "110"
          },
          "Cashflow": {
            "cashflow_id": "003690235976",
            "cashflow_version": 0,
            "cashflow_business_version": "0",
            "cashflow_state": "QUEUED",
            "cashflow_event_type": "New",
            "status_event_type": "",
            "event_date": "2022-10-20",
            "payment_payer_party_reference": "party2",
            "payment_receiver_party_reference": "party1",
            "payment_currency": "USD",
            "payment_amount": "2008",
            "payment_date": "2022-11-20",
            "payment_date_business_day_convention": "NONE",
            "netting_id": "11111111111-01",
            "pay_receive_indicator": "party2",
            "payer_name": "",
            "is_private_banking_cashflow": false,
            "is_amended_post_settlement": false,
            "payment_type": "netAmount",
            "is_cashflow_unnet": false,
            "transaction_details": "H4sIAAAAAAAAAKVWWW/bRhD+KwXRR1rlZdoSkAddbpzIjizJLgpDMJbkUFqb5DK7S8VCkf/e2eVtp46RCgJE7c7xzTcX742QpQMRBgNBAg6DOOWQDyKWEpoNNpxkgoSSssww/zGKgkbGyLAs1x9ajns6tC3DNA7AhRIYWaaREw6Z7KqN7t9ycIsW7yr91sFkun6wz23f9eye/e9bE41lkqPtSyXYCtXH6Dp8otnurgMKniXwjCR4F4HSy4okaVXWkkhAYwt6ALREiojKDU3x6N6xHMe0LdOxzKFpu6aLv77nnp1bloVYII4BozzAf4g7vjm0qg+KC1bwENZHISEto1xv5ovFGJ1+Y/wpTti3CsubnAklM/irp4Hc1SauSfo+CxHENKMqSY0xrYu2VBbOTCPTpowpEfvf1iBlAilm11BpoNn4Pfl95WncFJPygUTVTpacPSKZHS6Esv1IDmRQSJoMPiIKBGGY968AbbcKkng3dx08DX0Kju23cFZfPs2nm/nslwEpSEEhaAZCzA94qit2Uhz/WEOSoFlQhysgQrFYluSBJDRCQLpSjVFMEgEYWGO4qepSPMMLrPW2pHecCXGNpxD1erAyFCJMneZSbwUxYLuGUKvn5Ah8Sbg8ItJc/TqIk0MIWOP9C9VzUqGclaSXpW+bLkb9tSCZpEq2oislcj+Y0N0MQpoSjN3edqP6gYn28grkninmlvujoKHSLh3XbdvNVMiKDHtdI9R0e5ble5Zvu4rvClQVK+MyZgllZb/omXOxXj/cfn6YbCaLzQ1q5JyGsDnm2s18NcWjgLMn4LWRlPAnkO3/QgCfslTXQOdIQ2l6PX5eaeTlffy8JJR3MjpOVRBvcGdZ53oOpjmRNKBJN6gDaZKdM6FLXDvvDWxVBsZI8gIqKq+ZEkTjNWZsjqWKvYmTRTQeTwnWSvIivu5VfRaBds54C0xZm4aqfG7XKlNtgrunGs2CBK0pQRIQlxlG2zIGIOpnxumOZkRVczPdO1uB1xW+7JBRahIpSbiHqHvT0cxxjZBdZ1tgltOup6r8qlVSNdYVyXNVDd0xMWVJAroPxe+3maaLkiABlMW5owdXGKRNwGollWGQIdi+F5wFYUCcM8+BwAXPOiWB5Z35Q/BUfPHXFmFQZFHSQRzIYPkyCpoJzLuivbt5f2VHw+np0PLAPnEDPzrxnOD8JHBt+8TxvVOIgig88/1Xy7t1/xOfl63g/3BZdgnL1PBtDIr3pWdFMsQyDkMc3wsq1Jjfbqv0iM7kfDOMmf75EqjN1upUEfWGuWKn8+ZRdw2LivBnXC0rqXqnNnrVZFuSo4p7lFB8WzmGCVawHpVcwnOlW824qT4bXK7we4HlPNCVrtgYVEbU+9Fux2FHysXy44Iy98ecmf1hbJbj1+zP3dac8tJbVJXHElrT+epv0/0kSZgsqwnfVqiYNoOtX2wlES874NX6a68+akMvTz91NjU855QfZ50Z0G69+vVSkfliY8ua0AkR4HuK80fXufpsXbjen+PxzTiarnPx9818rD+L8V3iiJl6vLu7nq8+n+PThw/1asJdk8V01/eo3oChN01EXWLft/8CPL0lbe4LAAA=",
            "cashflow_affirmation_status": "Unaffirmed",
            "is_stp": null,
            "is_stp_ratan": null,
            "nstp_reason": "",
            "execution_date_time": "null",
            "cashflow_sub_state": "NA",
            "cashflow_sub_state_updater": "System",
            "cashflow_sub_state_type": "NA",
            "prev_cashflow_id": null,
            "next_cashflow_id": null,
            "validation_status": null,
            "exception_reason": null,
            "fmo_comment": null,
            "fmo_comment_updater": null,
            "fmo_comment_timestamp": "null",
            "stp_cutoff_date_time": "2022-11-17T21:00:00Z",
            "netting_cuttoff_date": "2022-11-17T21:00:00Z",
            "booking_entity_sci_fmcode": null,
            "cashflow_audit_version": null,
            "payment_cutoff_time": "2022-11-18T00:00:00Z",
            "minor_version_description": "",
            "bypass_workflow_indicator": null,
            "cashflow_minor_version": "",
            "is_payment_intent_to_settle": false
          },
          "Portfolio": {
            "booking_entity_trade_portfolio_name": null,
            "booking_entity_trade_portfolio_unique_name": null
          },
          "Trade": {
            "event_physical_status": "Live",
            "resultant_position_id": "1816352",
            "trade_original_source_system_name": null,
            "action_type": "Project",
            "trade_lake_valid_from_date_time": "null",
            "trade_lake_valid_to_date_time": "null",
            "trade_lake_latest_event_date_time": "null",
            "trade_lake_raw_event_date_time": "null",
            "trade_lake_transaction_from_date_time": "null",
            "trade_lake_transaction_to_date_time": "null",
            "bcs_parent_trade_id": "1816352",
            "bcs_trade_id": "1816352",
            "trade_version": 0,
            "trade_state": "VALIDATED",
            "trade_id": "1816352",
            "position_id": "3690235984",
            "parent_trade_id": "1816352",
            "settlement_method": "",
            "delivery_method": ""
          },
          "Settlement_Instruction": null,
          "FMO_Comments": {
            "FMO_Comment": null,
            "FMO_Comment_Updater": null,
            "FMO_Comment_Timestamp": "null"
          }
        },
        {
          "DataFlow": {
            "data_publication_date_time": "2022-11-12 17:13:30.0",
            "data_publication_id": "STELLA_1816352_0_1829946-1_1001",
            "data_sender": null,
            "data_source_system": "Stella",
            "data_source_system_country_code": "ALL",
            "data_source_system_domain_name": "FM",
            "data_type": "CashflowData",
            "unique_identifier_message_id": null
          },
          "Entity": {
            "person": {
              "coverage_marketer_psid": "",
              "event_coverage_marketer_psid": null,
              "execution_marketer_psid": "",
              "event_execution_marketer_psid": null,
              "booking_marketer_psid": "",
              "event_booking_marketer_psid": null,
              "trader_psid": "",
              "event_trader_psid": null
            },
            "booking_entity_sci_fmcode": null,
            "booking_entity_sci_fmid": "10075222",
            "counterparty_sci_fmid": null,
            "counterparty_sci_fmcode": "",
            "counterparty_cif_code": "",
            "counterparty_source_system_entity_id": "",
            "general_ledger_business_unit_name": null,
            "booking_entity_general_ledger_business_unit_id": "110"
          },
          "Cashflow": {
            "cashflow_id": "008888000004",
            "cashflow_version": 1,
            "cashflow_business_version": "1",
            "cashflow_state": "QUEUED",
            "cashflow_event_type": "Amendment",
            "status_event_type": "",
            "event_date": "2022-11-15",
            "payment_payer_party_reference": "party2",
            "payment_receiver_party_reference": "party1",
            "payment_currency": "USD",
            "payment_amount": "1500",
            "payment_date": "2022-11-23",
            "payment_date_business_day_convention": "NONE",
            "netting_id": null,
            "pay_receive_indicator": "party2",
            "payer_name": "",
            "is_private_banking_cashflow": false,
            "is_amended_post_settlement": false,
            "payment_type": "netAmount",
            "is_cashflow_unnet": false,
            "transaction_details": "H4sIAAAAAAAAAKVWWW/bRhD+KwXRR1rlZdoSkAddbpzIjizJLgpDMJbkUFqb5DK7S8VCkf/e2eVtp46RCgJE7c7xzTcX742QpQMRBgNBAg6DOOWQDyKWEpoNNpxkgoSSssww/zGKgkbGyLAs1x9ajns6tC3DNA7AhRIYWaaREw6Z7KqN7t9ycIsW7yr91sFkun6wz23f9eye/e9bE41lkqPtSyXYCtXH6Dp8otnurgMKniXwjCR4F4HSy4okaVXWkkhAYwt6ALREiojKDU3x6N6xHMe0LdOxzKFpu6aLv77nnp1bloVYII4BozzAf4g7vjm0qg+KC1bwENZHISEto1xv5ovFGJ1+Y/wpTti3CsubnAklM/irp4Hc1SauSfo+CxHENKMqSY0xrYu2VBbOTCPTpowpEfvf1iBlAilm11BpoNn4Pfl95WncFJPygUTVTpacPSKZHS6Esv1IDmRQSJoMPiIKBGGY968AbbcKkng3dx08DX0Kju23cFZfPs2nm/nslwEpSEEhaAZCzA94qit2Uhz/WEOSoFlQhysgQrFYluSBJDRCQLpSjVFMEgEYWGO4qepSPMMLrPW2pHecCXGNpxD1erAyFCJMneZSbwUxYLuGUKvn5Ah8Sbg8ItJc/TqIk0MIWOP9C9VzUqGclaSXpW+bLkb9tSCZpEq2oislcj+Y0N0MQpoSjN3edqP6gYn28grkninmlvujoKHSLh3XbdvNVMiKDHtdI9R0e5ble5Zvu4rvClQVK+MyZgllZb/omXOxXj/cfn6YbCaLzQ1q5JyGsDnm2s18NcWjgLMn4LWRlPAnkO3/QgCfslTXQOdIQ2l6PX5eaeTlffy8JJR3MjpOVRBvcGdZ53oOpjmRNKBJN6gDaZKdM6FLXDvvDWxVBsZI8gIqKq+ZEkTjNWZsjqWKvYmTRTQeTwnWSvIivu5VfRaBds54C0xZm4aqfG7XKlNtgrunGs2CBK0pQRIQlxlG2zIGIOpnxumOZkRVczPdO1uB1xW+7JBRahIpSbiHqHvT0cxxjZBdZ1tgltOup6r8qlVSNdYVyXNVDd0xMWVJAroPxe+3maaLkiABlMW5owdXGKRNwGollWGQIdi+F5wFYUCcM8+BwAXPOiWB5Z35Q/BUfPHXFmFQZFHSQRzIYPkyCpoJzLuivbt5f2VHw+np0PLAPnEDPzrxnOD8JHBt+8TxvVOIgig88/1Xy7t1/xOfl63g/3BZdgnL1PBtDIr3pWdFMsQyDkMc3wsq1Jjfbqv0iM7kfDOMmf75EqjN1upUEfWGuWKn8+ZRdw2LivBnXC0rqXqnNnrVZFuSo4p7lFB8WzmGCVawHpVcwnOlW824qT4bXK7we4HlPNCVrtgYVEbU+9Fux2FHysXy44Iy98ecmf1hbJbj1+zP3dac8tJbVJXHElrT+epv0/0kSZgsqwnfVqiYNoOtX2wlES874NX6a68+akMvTz91NjU855QfZ50Z0G69+vVSkfliY8ua0AkR4HuK80fXufpsXbjen+PxzTiarnPx9818rD+L8V3iiJl6vLu7nq8+n+PThw/1asJdk8V01/eo3oChN01EXWLft/8CPL0lbe4LAAA=",
            "cashflow_affirmation_status": "Unaffirmed",
            "is_stp": null,
            "is_stp_ratan": null,
            "nstp_reason": "",
            "execution_date_time": "null",
            "cashflow_sub_state": "NA",
            "cashflow_sub_state_updater": "System",
            "cashflow_sub_state_type": "NA",
            "prev_cashflow_id": null,
            "next_cashflow_id": null,
            "validation_status": null,
            "exception_reason": null,
            "fmo_comment": null,
            "fmo_comment_updater": null,
            "fmo_comment_timestamp": "null",
            "stp_cutoff_date_time": "2022-11-21T21:00:00Z",
            "netting_cuttoff_date": "2022-11-21T21:00:00Z",
            "booking_entity_sci_fmcode": null,
            "cashflow_audit_version": null,
            "payment_cutoff_time": "2022-11-22T00:00:00Z",
            "minor_version_description": "",
            "bypass_workflow_indicator": null,
            "cashflow_minor_version": "",
            "is_payment_intent_to_settle": false
          },
          "Portfolio": {
            "booking_entity_trade_portfolio_name": null,
            "booking_entity_trade_portfolio_unique_name": null
          },
          "Trade": {
            "event_physical_status": "Live",
            "resultant_position_id": "1816352",
            "trade_original_source_system_name": null,
            "action_type": "Project",
            "trade_lake_valid_from_date_time": "null",
            "trade_lake_valid_to_date_time": "null",
            "trade_lake_latest_event_date_time": "null",
            "trade_lake_raw_event_date_time": "null",
            "trade_lake_transaction_from_date_time": "null",
            "trade_lake_transaction_to_date_time": "null",
            "bcs_parent_trade_id": "1816352",
            "bcs_trade_id": "1816352",
            "trade_version": 0,
            "trade_state": "VALIDATED",
            "trade_id": "1816352",
            "position_id": "3690235984",
            "parent_trade_id": "1816352",
            "settlement_method": "",
            "delivery_method": ""
          },
          "Settlement_Instruction": null,
          "FMO_Comments": {
            "FMO_Comment": null,
            "FMO_Comment_Updater": null,
            "FMO_Comment_Timestamp": "null"
          }
        },
        {
          "DataFlow": {
            "data_publication_date_time": "2022-11-12 17:13:30.0",
            "data_publication_id": "STELLA_1816352_0_1829946-1_1001",
            "data_sender": null,
            "data_source_system": "Stella",
            "data_source_system_country_code": "ALL",
            "data_source_system_domain_name": "FM",
            "data_type": "CashflowData",
            "unique_identifier_message_id": null
          },
          "Entity": {
            "person": {
              "coverage_marketer_psid": "",
              "event_coverage_marketer_psid": null,
              "execution_marketer_psid": "",
              "event_execution_marketer_psid": null,
              "booking_marketer_psid": "",
              "event_booking_marketer_psid": null,
              "trader_psid": "",
              "event_trader_psid": null
            },
            "booking_entity_sci_fmcode": null,
            "booking_entity_sci_fmid": "10075222",
            "counterparty_sci_fmid": null,
            "counterparty_sci_fmcode": "",
            "counterparty_cif_code": "",
            "counterparty_source_system_entity_id": "",
            "general_ledger_business_unit_name": null,
            "booking_entity_general_ledger_business_unit_id": "110"
          },
          "Cashflow": {
            "cashflow_id": "113690235975",
            "cashflow_version": 0,
            "cashflow_business_version": "0",
            "cashflow_state": "DEAD",
            "cashflow_event_type": "New",
            "status_event_type": "",
            "event_date": "2022-10-20",
            "payment_payer_party_reference": "party2",
            "payment_receiver_party_reference": "party1",
            "payment_currency": "USD",
            "payment_amount": "3016",
            "payment_date": "2022-11-20",
            "payment_date_business_day_convention": "NONE",
            "netting_id": "11111111111-01",
            "pay_receive_indicator": "party2",
            "payer_name": "",
            "is_private_banking_cashflow": false,
            "is_amended_post_settlement": false,
            "payment_type": "netAmount",
            "is_cashflow_unnet": false,
            "transaction_details": "H4sIAAAAAAAAAKVWWW/bRhD+KwXRR1rlZdoSkAddbpzIjizJLgpDMJbkUFqb5DK7S8VCkf/e2eVtp46RCgJE7c7xzTcX742QpQMRBgNBAg6DOOWQDyKWEpoNNpxkgoSSssww/zGKgkbGyLAs1x9ajns6tC3DNA7AhRIYWaaREw6Z7KqN7t9ycIsW7yr91sFkun6wz23f9eye/e9bE41lkqPtSyXYCtXH6Dp8otnurgMKniXwjCR4F4HSy4okaVXWkkhAYwt6ALREiojKDU3x6N6xHMe0LdOxzKFpu6aLv77nnp1bloVYII4BozzAf4g7vjm0qg+KC1bwENZHISEto1xv5ovFGJ1+Y/wpTti3CsubnAklM/irp4Hc1SauSfo+CxHENKMqSY0xrYu2VBbOTCPTpowpEfvf1iBlAilm11BpoNn4Pfl95WncFJPygUTVTpacPSKZHS6Esv1IDmRQSJoMPiIKBGGY968AbbcKkng3dx08DX0Kju23cFZfPs2nm/nslwEpSEEhaAZCzA94qit2Uhz/WEOSoFlQhysgQrFYluSBJDRCQLpSjVFMEgEYWGO4qepSPMMLrPW2pHecCXGNpxD1erAyFCJMneZSbwUxYLuGUKvn5Ah8Sbg8ItJc/TqIk0MIWOP9C9VzUqGclaSXpW+bLkb9tSCZpEq2oislcj+Y0N0MQpoSjN3edqP6gYn28grkninmlvujoKHSLh3XbdvNVMiKDHtdI9R0e5ble5Zvu4rvClQVK+MyZgllZb/omXOxXj/cfn6YbCaLzQ1q5JyGsDnm2s18NcWjgLMn4LWRlPAnkO3/QgCfslTXQOdIQ2l6PX5eaeTlffy8JJR3MjpOVRBvcGdZ53oOpjmRNKBJN6gDaZKdM6FLXDvvDWxVBsZI8gIqKq+ZEkTjNWZsjqWKvYmTRTQeTwnWSvIivu5VfRaBds54C0xZm4aqfG7XKlNtgrunGs2CBK0pQRIQlxlG2zIGIOpnxumOZkRVczPdO1uB1xW+7JBRahIpSbiHqHvT0cxxjZBdZ1tgltOup6r8qlVSNdYVyXNVDd0xMWVJAroPxe+3maaLkiABlMW5owdXGKRNwGollWGQIdi+F5wFYUCcM8+BwAXPOiWB5Z35Q/BUfPHXFmFQZFHSQRzIYPkyCpoJzLuivbt5f2VHw+np0PLAPnEDPzrxnOD8JHBt+8TxvVOIgig88/1Xy7t1/xOfl63g/3BZdgnL1PBtDIr3pWdFMsQyDkMc3wsq1Jjfbqv0iM7kfDOMmf75EqjN1upUEfWGuWKn8+ZRdw2LivBnXC0rqXqnNnrVZFuSo4p7lFB8WzmGCVawHpVcwnOlW824qT4bXK7we4HlPNCVrtgYVEbU+9Fux2FHysXy44Iy98ecmf1hbJbj1+zP3dac8tJbVJXHElrT+epv0/0kSZgsqwnfVqiYNoOtX2wlES874NX6a68+akMvTz91NjU855QfZ50Z0G69+vVSkfliY8ua0AkR4HuK80fXufpsXbjen+PxzTiarnPx9818rD+L8V3iiJl6vLu7nq8+n+PThw/1asJdk8V01/eo3oChN01EXWLft/8CPL0lbe4LAAA=",
            "cashflow_affirmation_status": "Unaffirmed",
            "is_stp": null,
            "is_stp_ratan": null,
            "nstp_reason": "",
            "execution_date_time": "null",
            "cashflow_sub_state": "NA",
            "cashflow_sub_state_updater": "1481696",
            "cashflow_sub_state_type": "NA",
            "prev_cashflow_id": null,
            "next_cashflow_id": null,
            "validation_status": null,
            "exception_reason": null,
            "fmo_comment": null,
            "fmo_comment_updater": null,
            "fmo_comment_timestamp": "null",
            "stp_cutoff_date_time": "2022-11-17T21:00:00Z",
            "netting_cuttoff_date": "2022-11-17T21:00:00Z",
            "booking_entity_sci_fmcode": null,
            "cashflow_audit_version": null,
            "payment_cutoff_time": "2022-11-18T00:00:00Z",
            "minor_version_description": "",
            "bypass_workflow_indicator": null,
            "cashflow_minor_version": "0",
            "is_payment_intent_to_settle": false
          },
          "Portfolio": {
            "booking_entity_trade_portfolio_name": null,
            "booking_entity_trade_portfolio_unique_name": null
          },
          "Trade": {
            "event_physical_status": "Live",
            "resultant_position_id": "1816352",
            "trade_original_source_system_name": null,
            "action_type": "Project",
            "trade_lake_valid_from_date_time": "null",
            "trade_lake_valid_to_date_time": "null",
            "trade_lake_latest_event_date_time": "null",
            "trade_lake_raw_event_date_time": "null",
            "trade_lake_transaction_from_date_time": "null",
            "trade_lake_transaction_to_date_time": "null",
            "bcs_parent_trade_id": "1816352",
            "bcs_trade_id": "1816352",
            "trade_version": 0,
            "trade_state": "VALIDATED",
            "trade_id": "1816352",
            "position_id": "",
            "parent_trade_id": "1816352",
            "settlement_method": "",
            "delivery_method": ""
          },
          "Settlement_Instruction": null,
          "FMO_Comments": {
            "FMO_Comment": null,
            "FMO_Comment_Updater": null,
            "FMO_Comment_Timestamp": "null"
          }
        }
      ]
    }
  }
}
```

```gherkin

```

```bash

```