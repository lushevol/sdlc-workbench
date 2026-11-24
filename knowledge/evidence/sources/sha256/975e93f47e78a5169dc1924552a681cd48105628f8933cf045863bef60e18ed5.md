## Background

PostgreSQL will be the primary choice for Cash Settlement Platform,  it is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

- Different schema to be used by different business domain services
- Payment storage, including latest payment and payment list
- Suppression rules storage
- SSI stamping information storage
- SWIFT messages storage
- Audit information storage for operations by users
- Camunda native storage

## Data Required

| | Title | User Story | Owner | Type | Retention | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cashflow | Users need to view all payments and go into details on demand, as well as history query 1. Economics 2. Payment status 3. SSI information 4. Downstream processing message, like FMSRE | Cashflow Lifecycle Service | Storage | | |
| 2 | Camunda native data | Camunda will be the workflow to orchestration settlement processing, native storage required, tables start with "act_" | Settlement Orchestration | Storage | | |
| 3 | Suppression rules | Users need a self defined rules on cashflow suppression | Suppression Service | Storage | Forever | |
| 4 | Processed raw messages | Keep the messages on concerned events received from STELLA | Payment Lake Service | Storage | | |
| 5 | Audit | Users need to view the audit history on the manual review process as well as automated events | Audit Service | Storage | | |
| 6 | User login/logout audit | Group level requirement | Audit Service | Storage | | |
| 7 | Exception | Exceptions occurred during the processing | Exception Service | Storage | | |
| 8 | Customized filters/views | User need to create self-defined filters and views for blotter querying and searching | BFF | Storage | Forever | |
| 9 | SWIFT messages | SWIFT messages need to be displayed | SWIFT processing Service | Storage | | |
| 10 | | | | | | |

## Sample Data

**EXPAND: Sample Json**

{
    "Delivery_Method":"",
    "Trade_State":"TOBESENT",
    <u>**"Cashflow_Sub_Status_Type"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
    "Parent_Trade_Id":"3294505081",
    "Trade_Lake_Transaction_From_Date_Time":"2022-10-12T02:24:03.692Z",
    "Trade_Id":"3294505081",
    **<u>"Cashflow_Sub_Status"</u>****<u>:</u>****<u>null</u>****<u>,</u>**
    "Trade_Lake_Valid_To_Date_Time":"9999-12-31T00:00:00Z",
    <u>**"Cashflow_Sub_Status_Updater"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
    "Trade_Lake_Latest_Event_Date_Time":null,
    "Data_Flow":{
        "Data_Publication_Date_Time":"2022-10-12T02:23:17Z",
        "Data_Type":"CashflowData",
        "Data_Source_System_Domain_Name":"FM",
        "Unique_Identifier_Message_Id":null,
        "Data_Source_System_Country_Code":"ALL",
        "Data_Source_System":"Stella",
        "Data_Publication_Id":"71f2132e-04da-4539-8015-7f474b6c4be8-2_1001",
        "Data_Sender":"STELLA"
    },
    "Trade_Version":"4",
    "Settlement_Instruction":{
        "Sender_To_Receiver_Information_1":"",
        "Remittance_Information_1":"",
        "Swift_Payment_Method":"",
        "Swift_Message_Type":"",
        "Nostro_Swift_Message_Type":"",
        "Sender_To_Receiver_Information_6":"",
        "SSI_Unique_Id":"",
        "Remittance_Information_2":"",
        "Sender_To_Receiver_Information_5":"",
        "Sender_To_Receiver_Information_4":"",
        "Is_Third_Party_Payment":"",
        "Remittance_Information_4":"",
        "SSI_Priority":"",
        "SSI_Source":"",
        "Remittance_Information_3":"",
        "Charge_Bearer":"",
        "Sender_To_Receiver_Information_3":"",
        "Account":{
            "Intermediary_Account_Number":"",
            "Beneficiary_Street_Address":"",
            "Beneficiary_Account_Name":"",
            "Beneficiary_Bank_Street_Address":"",
            "Beneficiary_Bank_BIC_code":"",
            "Beneficiary_Correspondent_Street_Address":"",
            "Beneficiary_Account_Number":"",
            "Beneficiary_Correspondent_City":"",
            "Beneficiary_Correspondent_Account_Number":"",
            "Beneficiary_Bank_Account_Number":"",
            "Beneficiary_Bank_City":"",
            "Ordering_Customer_City":"",
            "Beneficiary_Correspondent_Account_Name":"",
            "Counterparty_CMS_Account_Number":"",
            "EBBS_Account_Number":"",
            "Intermediary_Account_Name":"",
            "Intermediary_BIC_code":"",
            "Booking_Entity_Correspondent_BIC_code":"",
            "Booking_Entity_Correspondent_Account_Name":"",
            "Ordering_Customer_Street_Address":"",
            "Booking_Entity_Correspondent_Account_Number":"",
            "Intermediary_City":"",
            "Booking_Entity_Correspondent_City":"",
            "SCB_Nostro_Account_Number":"",
            "Beneficiary_City":"",
            "EBBS_Bridge_Account_Number":"",
            "Beneficiary_Account_Name_2":"",
            "Booking_Entity_Correspondent_Street_Address":"",
            "Beneficiary_Correspondent_BIC_code":"",
            "Beneficiary_Bank_Account_Name":"",
            "Beneficiary_BIC_code":"",
            "Ordering_Customer_Account_Number":"",
            "Ordering_Customer_BIC_Code":"",
            "Ordering_Customer_Account_Name":"",
            "Intermediary_Street_Address":"",
            "SCB_Nostro_Account_Type":""
        },
        "Sender_To_Receiver_Information_2":""
    },
    "Instrument_Common":{
        "Parent_Trade_Instrument":null,
        "Source_System_Instrument_Sub_Type":"",
        "Equity_Instrument_Reference":null,
        "ISDA_Taxonomy":"ForeignExchange:Spot",
        "CFI_Code":"ForeignExchange:Spot"
    },
    "Entity":{
        "Counterparty_SCI_FMCODE":"UNILEVER NEPAL*KTM",
        "Counterparty_CIF_Code":"",
        "Counterparty_SCI_FMID":"400594382",
        "Booking_Entity_General_Ledger_Business_Unit_Id":"236",
        "General_Ledger_Business_Unit_Name":null,
        "Booking_Entity_SCI_FMCODE":"NEPAL GRINDLAYS*KTM",
        "Counterparty_Source_System_Entity_Id":"",
        "Booking_Entity_SCI_FMID":"400007847"
    },
    "Trade_Lake_Transaction_To_Date_Time":"9999-12-31T00:00:00Z",
    "Position_Id":"3294505082",
    <u>**"Settlement_Method"**</u><u>**:**</u><u>**""**</u><u>**,**</u>
    "Trade_Lake_Raw_Event_Date_Time":null,
    "Cashflow":{
        <u>**"Cashflow_Affirmation_Status"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
        "Payer_Name":null,
        "Bypass_Workflow_Indicator":null,
        "Payment_Type":"Cashflow",
        "Is_STP":"false",
        <u>**"NSTP_Reason"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
        "Payment_Date":"2020-07-20T00:00:00Z",
        "Payment_Receiver_Party_Reference":"party2",
        "Cashflow_Ratan_Internal_Version":null,
        "Cashflow_Business_Version":"N/A",
        <u>**"Netting_Cutoff_Date"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
        "Status_Event_Type":"",
        "Payment_Date_Business_Day_Convention":"NONE",
        "Pay_Receive_Indicator":"Pay",
        <u>**"STP_Cutoff_Date_Time"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
        "Next_Cashflow_Id":null,
        <u>**"Netting_Id"**</u><u>**:**</u><u>**""**</u><u>**,**</u>
        "Is_Private_Banking_Cashflow":"false",
        "Payment_Amount":"1111100.0",
        "Payment_Cutoff_Time":null,
        "Cashflow_Version":"1",
        "Validation_Status":null,
        "Cashflow_Id":"003294505082",
        "Cashflow_Event_Type":"Withdrawal",
        "Cashflow_Minor_Version":null,
        <u>**"Cashflow_State"**</u><u>**:**</u><u>**"SUPPRESSED"**</u><u>**,**</u>
        "Prev_Cashflow_Id":null,
        <u>**"Is_Cashflow_Unnet"**</u><u>**:**</u><u>**"false"**</u><u>**,**</u>
        <u>**"Is_STP_Ratan"**</u><u>**:**</u><u>**null**</u><u>**,**</u>
        "Payment_Payer_Party_Reference":"party1",
        "Minor_Version_Description":null,
        "Payment_Currency":"USD",
        "Event_Date":"2022-10-12T00:00:00Z",
        "Is_Amended_Post_Settlement":"false",
        **"Adjusted_Payment_Date"****:"2022-10-12T00:00:00Z",
       **** "Payment_Version"****:"1"**

},
    "BCS_Parent_Trade_Id":"",
    "Trade_Lake_Valid_From_Date_Time":"2022-10-12T02:23:17Z",
    "BCS_Trade_Id":"",
    "Portfolio":{
        "Booking_Entity_Trade_Portfolio_Unique_Name":"SABRE||STL-FXFW-NP-NPR",
        "Booking_Entity_Trade_Portfolio_Name":"STL-FXFW-NP-NPR"
    }
}

**EXPAND_END**

Requirements on PostgreSQL

| # | Title | User Story | Importance | Notes |
| --- | --- | --- | --- | --- |
| 1 | Global Replication | Writes to one instance should be automatically propagated to other instances. | Must Have | |
| 2 | High Availability | DB instance DR will be transparent to us, failure on DB operation is not accepted. | Must Have | |
| 3 | Continuous Consistency | Data should be in sync in real time | Must Have | |

## Questions

Below is a list of questions to be addressed as a result of this requirements document:

| Question | Outcome |
| --- | --- |
| (e.g. How we make users more aware of this feature?) | Communicate the decision reached |

## Not Doing

- List the features discussed which are out of scope or might be revisited in a later release.

# Attachment

[GraphiQL (dev.net)](https://api-dqslrtdev.uk.dev.net/cashflow/graphiql?query=%7B%0A%20%20cashflows(filter%3A%20%5B%7Bfield%3A%20%22Cashflow.Cashflow_Id%22%2C%20operator%3A%20IN%2C%20values%3A%20%5B%22003294505060%22%2C%22003294505082%22%2C%22003294505083%22%5D%7D%5D%2C%20page%3A%200%2C%20size%3A%2050)%20%7B%0A%20%20%20%20pageInfo%20%7B%0A%20%20%20%20%20%20totalHits%0A%20%20%20%20%20%20pageNo%0A%20%20%20%20%20%20pageSize%0A%20%20%20%20%20%20lastPage%0A%20%20%20%20%7D%0A%20%20%20%20results%20%7B%0A%20%20%20%20%20%20Delivery_Method%0A%20%20%20%20%20%20Trade_State%0A%20%20%20%20%20%20Cashflow_Sub_Status_Type%0A%20%20%20%20%20%20Parent_Trade_Id%0A%20%20%20%20%20%20Trade_Lake_Transaction_From_Date_Time%0A%20%20%20%20%20%20Trade_Id%0A%20%20%20%20%20%20Cashflow_Sub_Status%0A%20%20%20%20%20%20Trade_Lake_Valid_To_Date_Time%0A%20%20%20%20%20%20Cashflow_Sub_Status_Updater%0A%20%20%20%20%20%20Trade_Lake_Latest_Event_Date_Time%0A%20%20%20%20%20%20Data_Flow%7B%0A%20%20%20%20%20%20%20%20Data_Publication_Date_Time%0A%20%20%20%20%20%20%20%20Data_Type%0A%20%20%20%20%20%20%20%20Data_Source_System_Domain_Name%0A%20%20%20%20%20%20%20%20Unique_Identifier_Message_Id%0A%20%20%20%20%20%20%20%20Data_Source_System_Country_Code%0A%20%20%20%20%20%20%20%20Data_Source_System%0A%20%20%20%20%20%20%20%20Data_Publication_Id%0A%20%20%20%20%20%20%20%20Data_Sender%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20Trade_Version%0A%20%20%20%20%20%20Settlement_Instruction%7B%0A%20%20%20%20%20%20%20%20Sender_To_Receiver_Information_1%0A%20%20%20%20%20%20%20%20Remittance_Information_1%0A%20%20%20%20%20%20%20%20Swift_Payment_Method%0A%20%20%20%20%20%20%20%20Swift_Message_Type%0A%20%20%20%20%20%20%20%20Nostro_Swift_Message_Type%0A%20%20%20%20%20%20%20%20Sender_To_Receiver_Information_6%0A%20%20%20%20%20%20%20%20SSI_Unique_Id%0A%20%20%20%20%20%20%20%20Remittance_Information_2%0A%20%20%20%20%20%20%20%20Sender_To_Receiver_Information_5%0A%20%20%20%20%20%20%20%20Sender_To_Receiver_Information_4%0A%20%20%20%20%20%20%20%20Is_Third_Party_Payment%0A%20%20%20%20%20%20%20%20Remittance_Information_4%0A%20%20%20%20%20%20%20%20SSI_Priority%0A%20%20%20%20%20%20%20%20SSI_Source%0A%20%20%20%20%20%20%20%20Remittance_Information_3%0A%20%20%20%20%20%20%20%20Charge_Bearer%0A%20%20%20%20%20%20%20%20Sender_To_Receiver_Information_3%0A%20%20%20%20%20%20%20%20Account%7B%0A%20%20%20%20%20%20%20%20%20%20Intermediary_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Street_Address%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Account_Name%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Bank_Street_Address%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Bank_BIC_code%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Correspondent_Street_Address%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Correspondent_City%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Correspondent_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Bank_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Bank_City%0A%20%20%20%20%20%20%20%20%20%20Ordering_Customer_City%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Correspondent_Account_Name%0A%20%20%20%20%20%20%20%20%20%20Counterparty_CMS_Account_Number%0A%20%20%20%20%20%20%20%20%20%20EBBS_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Intermediary_Account_Name%0A%20%20%20%20%20%20%20%20%20%20Intermediary_BIC_code%0A%20%20%20%20%20%20%20%20%20%20Booking_Entity_Correspondent_BIC_code%0A%20%20%20%20%20%20%20%20%20%20Booking_Entity_Correspondent_Account_Name%0A%20%20%20%20%20%20%20%20%20%20Ordering_Customer_Street_Address%0A%20%20%20%20%20%20%20%20%20%20Booking_Entity_Correspondent_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Intermediary_City%0A%20%20%20%20%20%20%20%20%20%20Booking_Entity_Correspondent_City%0A%20%20%20%20%20%20%20%20%20%20SCB_Nostro_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_City%0A%20%20%20%20%20%20%20%20%20%20EBBS_Bridge_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Account_Name_2%0A%20%20%20%20%20%20%20%20%20%20Booking_Entity_Correspondent_Street_Address%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Correspondent_BIC_code%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_Bank_Account_Name%0A%20%20%20%20%20%20%20%20%20%20Beneficiary_BIC_code%0A%20%20%20%20%20%20%20%20%20%20Ordering_Customer_Account_Number%0A%20%20%20%20%20%20%20%20%20%20Ordering_Customer_BIC_Code%0A%20%20%20%20%20%20%20%20%20%20Ordering_Customer_Account_Name%0A%20%20%20%20%20%20%20%20%20%20Intermediary_Street_Address%0A%20%20%20%20%20%20%20%20%20%20SCB_Nostro_Account_Type%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20Sender_To_Receiver_Information_2%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20Instrument_Common%7B%0A%20%20%20%20%20%20%20%20Parent_Trade_Instrument%0A%20%20%20%20%20%20%20%20Source_System_Instrument_Sub_Type%0A%20%20%20%20%20%20%20%20Equity_Instrument_Reference%0A%20%20%20%20%20%20%20%20ISDA_Taxonomy%0A%20%20%20%20%20%20%20%20CFI_Code%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20Entity%7B%0A%20%20%20%20%20%20%20%20Counterparty_SCI_FMCODE%0A%20%20%20%20%20%20%20%20Counterparty_CIF_Code%0A%20%20%20%20%20%20%20%20Counterparty_SCI_FMID%0A%20%20%20%20%20%20%20%20Booking_Entity_General_Ledger_Business_Unit_Id%0A%20%20%20%20%20%20%20%20General_Ledger_Business_Unit_Name%0A%20%20%20%20%20%20%20%20Booking_Entity_SCI_FMCODE%0A%20%20%20%20%20%20%20%20Counterparty_Source_System_Entity_Id%0A%20%20%20%20%20%20%20%20Booking_Entity_SCI_FMID%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20Trade_Lake_Transaction_To_Date_Time%0A%20%20%20%20%20%20Position_Id%0A%20%20%20%20%20%20Settlement_Method%0A%20%20%20%20%20%20Trade_Lake_Raw_Event_Date_Time%0A%20%20%20%20%20%20Cashflow%7B%0A%20%20%20%20%20%20%20%20Cashflow_Affirmation_Status%0A%20%20%20%20%20%20%20%20Payer_Name%0A%20%20%20%20%20%20%20%20Bypass_Workflow_Indicator%0A%20%20%20%20%20%20%20%20Payment_Type%0A%20%20%20%20%20%20%20%20Is_STP%0A%20%20%20%20%20%20%20%20NSTP_Reason%0A%20%20%20%20%20%20%20%20Payment_Date%0A%20%20%20%20%20%20%20%20Payment_Receiver_Party_Reference%0A%20%20%20%20%20%20%20%20Cashflow_Ratan_Internal_Version%0A%20%20%20%20%20%20%20%20Cashflow_Business_Version%0A%20%20%20%20%20%20%20%20Netting_Cutoff_Date%0A%20%20%20%20%20%20%20%20Status_Event_Type%0A%20%20%20%20%20%20%20%20Payment_Date_Business_Day_Convention%0A%20%20%20%20%20%20%20%20Pay_Receive_Indicator%0A%20%20%20%20%20%20%20%20STP_Cutoff_Date_Time%0A%20%20%20%20%20%20%20%20Next_Cashflow_Id%0A%20%20%20%20%20%20%20%20Netting_Id%0A%20%20%20%20%20%20%20%20Is_Private_Banking_Cashflow%0A%20%20%20%20%20%20%20%20Payment_Amount%0A%20%20%20%20%20%20%20%20Payment_Cutoff_Time%0A%20%20%20%20%20%20%20%20Cashflow_Version%0A%20%20%20%20%20%20%20%20Validation_Status%0A%20%20%20%20%20%20%20%20Cashflow_Id%0A%20%20%20%20%20%20%20%20Cashflow_Event_Type%0A%20%20%20%20%20%20%20%20Cashflow_Minor_Version%0A%20%20%20%20%20%20%20%20Cashflow_State%0A%20%20%20%20%20%20%20%20Prev_Cashflow_Id%0A%20%20%20%20%20%20%20%20Is_Cashflow_Unnet%0A%20%20%20%20%20%20%20%20Is_STP_Ratan%0A%20%20%20%20%20%20%20%20Payment_Payer_Party_Reference%0A%20%20%20%20%20%20%20%20Minor_Version_Description%0A%20%20%20%20%20%20%20%20Payment_Currency%0A%20%20%20%20%20%20%20%20Event_Date%0A%20%20%20%20%20%20%20%20Is_Amended_Post_Settlement%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20BCS_Parent_Trade_Id%0A%20%20%20%20%20%20Trade_Lake_Valid_From_Date_Time%0A%20%20%20%20%20%20BCS_Trade_Id%0A%20%20%20%20%20%20Portfolio%7B%0A%20%20%20%20%20%20%20%20Booking_Entity_Trade_Portfolio_Unique_Name%0A%20%20%20%20%20%20%20%20Booking_Entity_Trade_Portfolio_Name%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

📎 [SampleJsonForCashflow.json](attachments/SampleJsonForCashflow.json)