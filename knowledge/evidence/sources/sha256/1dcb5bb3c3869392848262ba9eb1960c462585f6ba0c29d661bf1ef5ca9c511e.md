1 Work Flow Design

2 Notice Payload

The notice payload based on the json format

| attribute name | type | note |
| --- | --- | --- |
| cashFlowId | string | |
| cashflowBusinessVersion | int | |
| cashflowVersion | int | |
| cashflowMinorVersion | int | |
| cashFlowStatus | string | same with cashflow status define in the CN team（[Status Machine]） |
| eventAction | string | CASHFLOW_UPDATE, CASHFLOW_CREATE |
| cashflow | cashflow | cashflow info |

```diff
{
    "cashFlowId": "008690236384",
    "cashflowBusinessVersion": 0,
    "cashflowVersion": 0,
    "cashflowMinorVersion": 0,
    "eventAction": "CASHFLOW_CREATE",
    "cashFlowStatus": "PROJECTED",
    "cashflow": {
        "entity": {
            "person": {
                "trader_PSID": "",
                "event_Execution_Marketer_PSID": null,
                "event_Coverage_Marketer_PSID": null,
                "booking_Marketer_PSID": "",
                "event_Booking_Marketer_PSID": null,
                "event_Trader_PSID": null,
                "coverage_Marketer_PSID": "",
                "execution_Marketer_PSID": ""
            },
            "booking_Entity_General_Ledger_Business_Unit_Id": "110",
            "counterparty_Source_System_Entity_Id": "",
            "general_Ledger_Business_Unit_Name": null,
            "booking_Entity_SCI_FMCODE": null,
            "booking_Entity_SCI_FMID": "10075222",
            "counterparty_SCI_FMID": "400640613",
            "counterparty_SCI_FMCODE": null,
            "counterparty_CIF_Code": null
        },
        "instrument_Common": {
            "isda_Taxonomy": "Equity:Other",
            "cfi_Code": "SEXXXX",
            "source_System_Instrument_Sub_Type": "Equity Swap",
            "equity_Instrument_Reference": "",
            "parent_Trade_Instrument": ""
        },
        "settlement_Instruction": {
            "charge_Bearer": null,
            "ssi_Unique_Id": null,
            "ssi_Source": null,
            "ssi_Priority": null,
            "sender_To_Receiver_Information_6": null,
            "sender_To_Receiver_Information_3": null,
            "sender_To_Receiver_Information_2": null,
            "sender_To_Receiver_Information_4": null,
            "sender_To_Receiver_Information_5": null,
            "sender_To_Receiver_Information_1": null,
            "remittance_Information_4": null,
            "remittance_Information_3": null,
            "nostro_Swift_Message_Type": null,
            "remittance_Information_1": null,
            "remittance_Information_2": null,
            "swift_Payment_Method": null,
            "swift_Message_Type": null,
            "is_Third_Party_Payment": null,
            "account": {
                "beneficiary_Bank_Street_Address": null,
                "booking_Entity_Correspondent_Account_Name": null,
                "booking_Entity_Correspondent_Account_Number": null,
                "beneficiary_Correspondent_Account_Name": null,
                "ordering_Customer_Account_Name": null,
                "ordering_Customer_Street_Address": null,
                "beneficiary_Correspondent_Account_Number": null,
                "beneficiary_Correspondent_BIC_code": null,
                "booking_Entity_Correspondent_Street_Address": null,
                "beneficiary_Bank_Account_Number": null,
                "counterparty_CMS_Account_Number": null,
                "beneficiary_Correspondent_Street_Address": null,
                "booking_Entity_Correspondent_BIC_code": null,
                "beneficiary_Correspondent_City": null,
                "booking_Entity_Correspondent_City": null,
                "ordering_Customer_Account_Number": null,
                "beneficiary_City": null,
                "beneficiary_BIC_code": null,
                "beneficiary_Account_Number": null,
                "intermediary_Street_Address": null,
                "beneficiary_Account_Name_2": null,
                "beneficiary_Street_Address": null,
                "intermediary_BIC_code": null,
                "scb_Nostro_Account_Type": null,
                "intermediary_Account_Name": null,
                "intermediary_City": null,
                "intermediary_Account_Number": null,
                "beneficiary_Bank_BIC_code": null,
                "ordering_Customer_BIC_Code": null,
                "beneficiary_Bank_Account_Name": null,
                "ordering_Customer_City": null,
                "ebbs_Account_Number": null,
                "scb_Nostro_Account_Number": null,
                "beneficiary_Account_Name": null,
                "beneficiary_Bank_City": null,
                "ebbs_Bridge_Account_Number": null
            }
        },
        "trade_Version": 0,
        "portfolio": {
            "booking_Entity_Trade_Portfolio_Unique_Name": "SABRE||BCS_FSS_UK_BTBLTQ",
            "booking_Entity_Trade_Portfolio_Name": "BCS_FSS_UK_BTBLTQ"
        },
        "position_Id": "3690235984",
        "bcs_Trade_Id": "1816352",
        "trade_Id": "1816352",
        "trade_State": "VALIDATED",
        "data_Flow": {
            "data_Type": "CashflowData",
            "data_Sender": null,
            "data_Source_System_Country_Code": "ALL",
            "data_Source_System_Domain_Name": "FM",
            "data_Publication_Date_Time": "2022-10-20T17:13:30",
            "unique_Identifier_Message_Id": null,
            "data_Publication_Id": "GEOFFREY_007690235349",
            "data_Source_System": "Stella"
        },
        "trade": {
            "action_Type": "Project",
            "trade_Lake_Raw_Event_Date_Time": "null",
            "trade_Lake_Valid_From_Date_Time": "2022-10-20T17:13:30",
            "trade_Lake_Transaction_From_Date_Time": "2022-10-20T17:13:35.594",
            "trade_Lake_Latest_Event_Date_Time": "null",
            "trade_Original_Source_System_Name": null,
            "trade_Lake_Transaction_To_Date_Time": "9999-12-31T08:00",
            "event_Physical_Status": "Live",
            "trade_Lake_Valid_To_Date_Time": "9999-12-31T08:00",
            "resultant_Position_Id": "1816352"
        },
        "cashflow": {
            "cashflow_Version": 0,
            "cashflow_Business_Version": "0",
            "cashflow_Event_Type": "New",
            "nstp_Reason": "",
            "payer_Name": "",
            "netting_Id": "",
            "payment_Date": "2022-03-11",
            "is_STP_RATAN": null,
            "is_STP": null,
            "payment_Type": "netAmount",
            "event_Date": "2022-10-20",
            "cashflow_Sub_State_Updater": "System",
            "cashflow_Id": "008690236384",
            "payment_Date_Business_Day_Convention": "NONE",
            "payment_Receiver_Party_Reference": "party2",
            "cashflow_Sub_State_Type": "NA",
            "next_Cashflow_Id": null,
            "exception_Reason": null,
            "stp_Cutoff_Date_Time": "null",
            "prev_Cashflow_Id": null,
            "validation_Status": null,
            "payment_Payer_Party_Reference": "party1",
            "status_Event_Type": "",
            "payment_Currency": "JPY",
            "payment_Amount": "1000",
            "cashflow_State": "PROJECTED",
            "is_Private_Banking_Cashflow": false,
            "is_Amended_Post_Settlement": null,
            "is_Cashflow_Unnet": false,
            "transaction_Details": "H4sIAAAAAAAAAKVWWW/bRhD+KwXRR1rlZdoSkAddbpzIjizJLgpDMJbkUFqb5DK7S8VCkf/e2eVtp46RCgJE7c7xzTcX742QpQMRBgNBAg6DOOWQDyKWEpoNNpxkgoSSssww/zGKgkbGyLAs1x9ajns6tC3DNA7AhRIYWaaREw6Z7KqN7t9ycIsW7yr91sFkun6wz23f9eye/e9bE41lkqPtSyXYCtXH6Dp8otnurgMKniXwjCR4F4HSy4okaVXWkkhAYwt6ALREiojKDU3x6N6xHMe0LdOxzKFpu6aLv77nnp1bloVYII4BozzAf4g7vjm0qg+KC1bwENZHISEto1xv5ovFGJ1+Y/wpTti3CsubnAklM/irp4Hc1SauSfo+CxHENKMqSY0xrYu2VBbOTCPTpowpEfvf1iBlAilm11BpoNn4Pfl95WncFJPygUTVTpacPSKZHS6Esv1IDmRQSJoMPiIKBGGY968AbbcKkng3dx08DX0Kju23cFZfPs2nm/nslwEpSEEhaAZCzA94qit2Uhz/WEOSoFlQhysgQrFYluSBJDRCQLpSjVFMEgEYWGO4qepSPMMLrPW2pHecCXGNpxD1erAyFCJMneZSbwUxYLuGUKvn5Ah8Sbg8ItJc/TqIk0MIWOP9C9VzUqGclaSXpW+bLkb9tSCZpEq2oislcj+Y0N0MQpoSjN3edqP6gYn28grkninmlvujoKHSLh3XbdvNVMiKDHtdI9R0e5ble5Zvu4rvClQVK+MyZgllZb/omXOxXj/cfn6YbCaLzQ1q5JyGsDnm2s18NcWjgLMn4LWRlPAnkO3/QgCfslTXQOdIQ2l6PX5eaeTlffy8JJR3MjpOVRBvcGdZ53oOpjmRNKBJN6gDaZKdM6FLXDvvDWxVBsZI8gIqKq+ZEkTjNWZsjqWKvYmTRTQeTwnWSvIivu5VfRaBds54C0xZm4aqfG7XKlNtgrunGs2CBK0pQRIQlxlG2zIGIOpnxumOZkRVczPdO1uB1xW+7JBRahIpSbiHqHvT0cxxjZBdZ1tgltOup6r8qlVSNdYVyXNVDd0xMWVJAroPxe+3maaLkiABlMW5owdXGKRNwGollWGQIdi+F5wFYUCcM8+BwAXPOiWB5Z35Q/BUfPHXFmFQZFHSQRzIYPkyCpoJzLuivbt5f2VHw+np0PLAPnEDPzrxnOD8JHBt+8TxvVOIgig88/1Xy7t1/xOfl63g/3BZdgnL1PBtDIr3pWdFMsQyDkMc3wsq1Jjfbqv0iM7kfDOMmf75EqjN1upUEfWGuWKn8+ZRdw2LivBnXC0rqXqnNnrVZFuSo4p7lFB8WzmGCVawHpVcwnOlW824qT4bXK7we4HlPNCVrtgYVEbU+9Fux2FHysXy44Iy98ecmf1hbJbj1+zP3dac8tJbVJXHElrT+epv0/0kSZgsqwnfVqiYNoOtX2wlES874NX6a68+akMvTz91NjU855QfZ50Z0G69+vVSkfliY8ua0AkR4HuK80fXufpsXbjen+PxzTiarnPx9818rD+L8V3iiJl6vLu7nq8+n+PThw/1asJdk8V01/eo3oChN01EXWLft/8CPL0lbe4LAAA=",
            "pay_Receive_Indicator": "Pay",
            "execution_Date_Time": "2022-10-20T17:13:31",
            "cashflow_Sub_State": "NA",
            "cashflow_Affirmation_Status": "affirmed",
            "cashflow_Minor_Version": 0,
            "bypass_Workflow_Indicator": null,
            "is_Payment_Intent_To_Settle": false,
            "netting_Cuttoff_Date": "null",
            "booking_Entity_SCI_FMCODE": null,
            "payment_Cutoff_Time": "2022-12-23T08:00",
            "cashflow_Audit_Version": "null",
            "minor_Version_Description": "0",
            "fmo_Comment": null,
            "fmo_Comment_Updater": null,
            "fmo_Comment_Timestamp": "null"
        },
        "settlement_Method": "Cash",
        "delivery_Method": "",
        "parent_Trade_Id": "1816352",
        "bcs_Parent_Trade_Id": "1816352"
    }
}
```

# UI Workflow

## User Requirements

1. Key benefit of auto refresh is that any new cashflow automatically shows up in the blotter without user having to refresh the data. This is essential especially for new cashflows which are value today / close to cutoff.
2. Cashflow Blotter must be Auto Refreshed, no pop-up required. We should highlight to user that the cashflow has newly arrived in the queue, either using a color or a column. Notification centre can be looked at in Q2 as we have to overlay the currency cutoff information.
3. If a cashflow is refreshed while a user has it open (irrespective of whether the change was due to trade event or update by another user), user must get notification pop-up that the cashflow has been refreshed, do you want to reload the cashflow – Y/N. No closes the cashflow, Yes reopens the cashflow in its latest version and allowable actions should be based on the latest status / exceptions.

📎 [RE_ Cashflow blotter notification.msg](attachments/RE_ Cashflow blotter notification.msg)

## Approaches

Checked with Blade on the UI notification, suggest we can follow the same pattern, let me know if anything missed for Day1/Q1

1. Any new records included, it will always popup on the top of the list
2. Entitlement should be applied to notification as well
3. Notification should be full data but not require UI to query again
4. Filter will not be applied to backend, but notification will be published to UI, and UI to determine whether display or not based on the filter applied
5. Second level UI will directly refresh on real time, suggest we popup an alert and “OK” is the only option for user to accept the refreshing

📎 [Cashflow blotter notification and auto refresh.msg](attachments/Cashflow blotter notification and auto refresh.msg)

## Approach Diagram

Highlights:

1. level2 alert should cover all content of dialog and forbid any action except "Refresh".
2. level2 updated cashflow should compare with current cashflow details first, otherwise not take any action. (Comparing condition: cashflow version & cashflow business version && cashflow minor version)
3. level1 updated cashflows should be applied search conditions and sorting condition.

## Snapshots on Notification implement

![image-2025-3-4_14-4-17.png](attachments/image-2025-3-4_14-4-17.png)![image-2025-3-4_14-4-22.png](attachments/image-2025-3-4_14-4-22.png)![image-2025-3-4_14-4-34.png](attachments/image-2025-3-4_14-4-34.png)