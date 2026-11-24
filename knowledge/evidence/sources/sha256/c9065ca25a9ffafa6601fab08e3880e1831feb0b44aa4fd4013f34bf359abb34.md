[FXU - RATAN analysis - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+-+RATAN+analysis)

# Integration

| | Option | Accounting | Swift | Exception management (FXU coordinator) | FXU details persistence | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | <details> <summary>Expand Details</summary> ![image-2025-4-28_14-28-39.png](attachments/image-2025-4-28_14-28-39.png) </details> | RAZOR | RAZOR | FXU | RATAN, TDS3, FXU | 1. FXU to handle the transactions among systems, TDS3, RATAN and FXU, for data sync up |
| 2 | <details> <summary>Expand Details</summary> ![image-2025-4-28_14-28-50.png](attachments/image-2025-4-28_14-28-50.png) </details> | RAZOR | RAZOR | RATAN | RATAN, TDS3, FXU | 1. RATAN to handle the transactions among systems, TDS3, RATAN and FXU, for data sync up |
| 3 | <details> <summary>Expand Details</summary> ![image-2025-4-29_14-40-1.png](attachments/image-2025-4-29_14-40-1.png) </details> | RATAN | RAZOR | NA | RATAN | 1. Existing Cashflow status driven hard block 2. If TDS3 sync up required for remaining amount, they should be involved for the transactional control. |

# RATAN FXU High Level Design

## Overall Architecture

## Manual Utilize/Reverse

## Auto Utilize/ Pastdue

# FXU Query API

| | |
| --- | --- |
| HOST | [https://fmo-mfe-dev.uk.dev.net](https://fmo-mfe-dev.uk.dev.net)（DEV） |
| PATH | [/api/ratan/stmcn/v1/cashflows](https://fmo-mfe.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows) |
| Header | FMAA-Token：“string” FMAA-UserId:"string" FMAA-AppId:"string" Bank-Id:"string" Country：string" |
| METHOD | POST |
| QUERY PARAMETER | ``` query SettlementCashflowDataUtilizeQuery($payload: RatanUltraQuery!) { cashflowUtilizeQuery(payload: $payload) { totalResult pageIndex itemsPerPage lastPage results { Cashflow { Cashflow_Id, Cashflow_Version, Cashflow_Business_Version, Cashflow_State, Cashflow_Event_Type, Cashflow_Sub_State, Cashflow_Sub_State_Type, Cashflow_Minor_Version, Cashflow_Major_Version, Payment_Currency, Payment_Amount, Remaining_Amount, Payment_Type, Payment_Date, Pay_Receive_Indicator }, Entity { Booking_Entity_SCI_FMCODE }, Settlement_Method, Trade { Settlement_Date, Is_Client_Leg, Trade_Date, Trade_Id, Trade_Version, Trade_State, Physical_Status, Comments, Base_Product, Execution_Date_Time, Buyer_Party_Reference, Seller_Party_Reference, Trade_Lake_External_Message_Id, Trade_Lake_Trade_Major_Version, Trade_Lake_Trade_Minor_Version, Source_System_Trade_Internal_Id, Transaction_Banking_Comments, Trade_Event { Business_Event_Type }, Cash_Financial_Instrument { Exchanged_Currency1_Payment_Amount_Currency, Exchanged_Currency2_Payment_Amount_Currency, Price, Base_Currency, Target_Currency }, Forward_Future_Instrument { Exchanged_Currency1_Payment_Amount_Currency, Exchanged_Currency2_Payment_Amount_Currency, Forward_Price, Quote_Basis, Base_Currency, Target_Currency, FX_Leg { Far_Leg { Exchanged_Currency1_Payment_Amount_Currency, Exchanged_Currency2_Payment_Amount_Currency }, Near_Leg { Exchanged_Currency1_Payment_Amount_Currency, Exchanged_Currency2_Payment_Amount_Currency } } }, Swap_Instrument { Forward_Future_Instrument { Far_Leg { Base_Currency, Quote_Basis, Target_Currency, Buyer_Party_Reference, Seller_Party_Reference, Forward_Price, Exchanged_Currency1_Payer_Party_Reference, Exchanged_Currency2_Receiver_Party_Reference }, Near_Leg { Base_Currency, Quote_Basis, Target_Currency, Seller_Party_Reference, Buyer_Party_Reference, Forward_Price, Exchanged_Currency1_Payer_Party_Reference, Exchanged_Currency2_Receiver_Party_Reference } } }, Entity { Person { Coverage_Marketer_PSID, Trader_PSID, Execution_Initiator_PSID, Booking_Marketer_Source_System_Person_Id }, Booking_Entity_SCI_FMID, Booking_Entity_Country_ISO_Code, General_Ledger_Business_Unit_Name, Counterparty_Name, Counterparty_SCI_LEID, Counterparty_SCI_FMID }, Data_Flow { Data_Source_System }, Portfolio { Booking_Entity_Trade_Portfolio_Name }, Instrument_Common { ISDA_Taxonomy } }, Settlement_Instruction { Account { SCB_Nostro_Account_Number, SCB_Nostro_Account_Type } } } } } ``` |
| GRAPHQL VARIABLES | ``` MVP: { "payload": { "filters": { "or": [ { "filters": [ { "field": "Trade.Trade_Id", "operator": "IN", "values": ["6682101424"] } ] } ] }, "itemsPerPage": 500, "orderArgs": [ ], "pageIndex": 0, "pagingOption": "PAGE_INDEX" } } Phase2: ----------------------------------------------------------------- { "payload": { "filters": { "or": [ { "and": [ { "filters": [ { "field": "Trade.Source_System_Trade_Internal_Id", "operator": "IN", "values": [ "111111" ] }, { "field": "Is_Client_Clearing_Trade", "operator": "EQ", "values": "true" } ] } ] }, { "and": [ { "filters": [ { "field": "Trade_Id", "operator": "IN", "values": [ "111111" ] } ] } ] } ] }, "itemsPerPage": 1000, "orderArgs": [ ], "pageIndex": 0, "pagingOption": "PAGE_INDEX" } } ``` |
| RESP | ``` { "data": { "cashflowUtilizeQuery": { "totalResult": 2, "pageIndex": 0, "itemsPerPage": 500, "lastPage": true, "results": [ { "Cashflow": { "Cashflow_Id": "000036006590", "Cashflow_Version": 0, "Cashflow_Business_Version": 0, "Cashflow_State": "PASTDUE", "Cashflow_Event_Type": "New", "Cashflow_Sub_State": "NA", "Cashflow_Sub_State_Type": "NA", "Cashflow_Minor_Version": 6, "Cashflow_Major_Version": "1", "Payment_Currency": "SAR", "Payment_Amount": "749.98", "Remaining_Amount": "749.98", "Payment_Type": "Cashflow", "Payment_Date": "2026-01-22", "Pay_Receive_Indicator": "Pay" }, "Entity": { "Booking_Entity_SCI_FMCODE": "SCB SAUDI*RYD" }, "Settlement_Method": "UTIL", "Trade": { "Settlement_Date": "2026-01-22", "Is_Client_Leg": false, "Trade_Date": "2026-01-21", "Trade_Id": "7111011106", "Trade_State": "BOOKED", "Physical_Status": "Live", "Comments": [ "" ], "Base_Product": "Forward", "Execution_Date_Time": "2026-01-21T07:53:53.841Z", "Buyer_Party_Reference": [ "party1" ], "Seller_Party_Reference": [ "party2" ], "Trade_Lake_External_Message_Id": "1144a98e-6a41-4209-b563-9a7c1062ef2d", "Trade_Lake_Trade_Major_Version": 1, "Trade_Lake_Trade_Minor_Version": 0, "Source_System_Trade_Internal_Id": "w7fuenndhkmg4sb", "Transaction_Banking_Comments": "", "Trade_Event": { "Business_Event_Type": "Trade" }, "Cash_Financial_Instrument": { "Exchanged_Currency1_Payment_Amount_Currency": "", "Exchanged_Currency2_Payment_Amount_Currency": "", "Price": "0.0", "Base_Currency": "", "Target_Currency": "" }, "Forward_Future_Instrument": { "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency2_Payment_Amount_Currency": "SAR", "Forward_Price": "3.749905", "Quote_Basis": "Currency2PerCurrency1", "Base_Currency": "USD", "Target_Currency": "SAR", "FX_Leg": { "Far_Leg": { "Exchanged_Currency1_Payment_Amount_Currency": "", "Exchanged_Currency2_Payment_Amount_Currency": "" }, "Near_Leg": { "Exchanged_Currency1_Payment_Amount_Currency": "", "Exchanged_Currency2_Payment_Amount_Currency": "" } } }, "Swap_Instrument": { "Forward_Future_Instrument": { "Far_Leg": { "Base_Currency": "", "Quote_Basis": "", "Target_Currency": "", "Buyer_Party_Reference": "", "Seller_Party_Reference": "", "Forward_Price": "0.0", "Exchanged_Currency1_Payer_Party_Reference": "", "Exchanged_Currency2_Receiver_Party_Reference": "" }, "Near_Leg": { "Base_Currency": "", "Quote_Basis": "", "Target_Currency": "", "Seller_Party_Reference": "", "Buyer_Party_Reference": "", "Forward_Price": "0.0", "Exchanged_Currency1_Payer_Party_Reference": "", "Exchanged_Currency2_Receiver_Party_Reference": "" } } }, "Entity": { "Person": { "Coverage_Marketer_PSID": "", "Trader_PSID": "1183119", "Execution_Initiator_PSID": "", "Booking_Marketer_Source_System_Person_Id": "" }, "Booking_Entity_SCI_FMID": "400991880", "Booking_Entity_Country_ISO_Code": "SA", "General_Ledger_Business_Unit_Name": "SCB Saudi Arabia", "Counterparty_Name": "", "Counterparty_SCI_LEID": "11090155", "Counterparty_SCI_FMID": "400045551" }, "Data_Flow": { "Data_Source_System": "Blade" }, "Portfolio": { "Booking_Entity_Trade_Portfolio_Name": "STL-FX-SA" }, "Instrument_Common": { "ISDA_Taxonomy": "ForeignExchange:Forward" } }, "Settlement_Instruction": { "Account": { "SCB_Nostro_Account_Number": "FXBRREC-M", "SCB_Nostro_Account_Type": "FXBRREC-M" } } }, { "Cashflow": { "Cashflow_Id": "000036006591", "Cashflow_Version": 0, "Cashflow_Business_Version": 0, "Cashflow_State": "PASTDUE", "Cashflow_Event_Type": "New", "Cashflow_Sub_State": "NA", "Cashflow_Sub_State_Type": "NA", "Cashflow_Minor_Version": 6, "Cashflow_Major_Version": "1", "Payment_Currency": "USD", "Payment_Amount": "200.0", "Remaining_Amount": "200.0", "Payment_Type": "Cashflow", "Payment_Date": "2026-01-22", "Pay_Receive_Indicator": "Receive" }, "Entity": { "Booking_Entity_SCI_FMCODE": "SCB SAUDI*RYD" }, "Settlement_Method": "UTIL", "Trade": { "Settlement_Date": "2026-01-22", "Is_Client_Leg": false, "Trade_Date": "2026-01-21", "Trade_Id": "7111011106", "Trade_State": "BOOKED", "Physical_Status": "Live", "Comments": [ "" ], "Base_Product": "Forward", "Execution_Date_Time": "2026-01-21T07:53:53.841Z", "Buyer_Party_Reference": [ "party1" ], "Seller_Party_Reference": [ "party2" ], "Trade_Lake_External_Message_Id": "1144a98e-6a41-4209-b563-9a7c1062ef2d", "Trade_Lake_Trade_Major_Version": 1, "Trade_Lake_Trade_Minor_Version": 0, "Source_System_Trade_Internal_Id": "w7fuenndhkmg4sb", "Transaction_Banking_Comments": "", "Trade_Event": { "Business_Event_Type": "Trade" }, "Cash_Financial_Instrument": { "Exchanged_Currency1_Payment_Amount_Currency": "", "Exchanged_Currency2_Payment_Amount_Currency": "", "Price": "0.0", "Base_Currency": "", "Target_Currency": "" }, "Forward_Future_Instrument": { "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency2_Payment_Amount_Currency": "SAR", "Forward_Price": "3.749905", "Quote_Basis": "Currency2PerCurrency1", "Base_Currency": "USD", "Target_Currency": "SAR", "FX_Leg": { "Far_Leg": { "Exchanged_Currency1_Payment_Amount_Currency": "", "Exchanged_Currency2_Payment_Amount_Currency": "" }, "Near_Leg": { "Exchanged_Currency1_Payment_Amount_Currency": "", "Exchanged_Currency2_Payment_Amount_Currency": "" } } }, "Swap_Instrument": { "Forward_Future_Instrument": { "Far_Leg": { "Base_Currency": "", "Quote_Basis": "", "Target_Currency": "", "Buyer_Party_Reference": "", "Seller_Party_Reference": "", "Forward_Price": "0.0", "Exchanged_Currency1_Payer_Party_Reference": "", "Exchanged_Currency2_Receiver_Party_Reference": "" }, "Near_Leg": { "Base_Currency": "", "Quote_Basis": "", "Target_Currency": "", "Seller_Party_Reference": "", "Buyer_Party_Reference": "", "Forward_Price": "0.0", "Exchanged_Currency1_Payer_Party_Reference": "", "Exchanged_Currency2_Receiver_Party_Reference": "" } } }, "Entity": { "Person": { "Coverage_Marketer_PSID": "", "Trader_PSID": "1183119", "Execution_Initiator_PSID": "", "Booking_Marketer_Source_System_Person_Id": "" }, "Booking_Entity_SCI_FMID": "400991880", "Booking_Entity_Country_ISO_Code": "SA", "General_Ledger_Business_Unit_Name": "SCB Saudi Arabia", "Counterparty_Name": "", "Counterparty_SCI_LEID": "11090155", "Counterparty_SCI_FMID": "400045551" }, "Data_Flow": { "Data_Source_System": "Blade" }, "Portfolio": { "Booking_Entity_Trade_Portfolio_Name": "STL-FX-SA" }, "Instrument_Common": { "ISDA_Taxonomy": "ForeignExchange:Forward" } }, "Settlement_Instruction": { "Account": { "SCB_Nostro_Account_Number": "FXBRREC-M", "SCB_Nostro_Account_Type": "FXBRREC-M" } } } ] } } } ``` |

# FXU Request/Response

## Request

| | Content | Description |
| --- | --- | --- |
| TOPIC_REQ | Cash_Settlement_FXU_Request_In | |
| MESSAGE | { "Utilization_Id": "12345678", "Orig_Utilization_Id": "12345678", "Util_Type": "VDATE-FULL-UTIL", "AACode_Comments": "", "Util_Payment_Ref": "", "Maker_ID": "12345678", "Checker_ID": "12345678", "Trade": { "Trade_Id": "12345678", "Trade_Lake_Trade_Major_Version": "1", "Swap_Leg_ID": "Far/Near", "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency1_Util_Amount": "1000.00" } } | 📎 [FXU-RATAN Message Sepc_250915.xlsx](attachments/FXU-RATAN Message Sepc_250915.xlsx) |

## Response

| | Content | Description |
| --- | --- | --- |
| TOPIC_REQ | Cash_Settlement_FXU_Ack | |
| ACK | { "Utilization": { "Utilization_Id": "71110111046", "Response": "ACK", "Error_Reason": null }, "Request_Info": { "Utilization": { "Utilization_Id": "71110111046", "Orig_Utilization_Id": "71110111041", "Util_Type": "VDATE-PART-REV", "AACode_Comments": "FX", "Util_Payment_Ref": "1", "Maker_ID": "1642375", "Checker_ID": "1376381", "Trade": { "Trade_Id": "7111011104", "Trade_Lake_Trade_Major_Version": "1", "Swap_Leg_ID": "", "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency1_Util_Amount": "50.0", "Exchanged_Currency2_Payment_Amount_Currency": "SAR", "Exchanged_Currency2_Util_Amount": "187.5" } } } } | Same to Request |
| NACK | Business NACK message sample: { "Utilization": { "Utilization_Id": "71110111046", "Response": "NACK", "Error_Reason": "Trade is Cancelled." }, "Request_Info": { "Utilization": { "Utilization_Id": "71110111046", "Orig_Utilization_Id": "71110111041", "Util_Type": "VDATE-PART-REV", "AACode_Comments": "FX", "Util_Payment_Ref": "1", "Maker_ID": "1642375", "Checker_ID": "1376381", "Trade": { "Trade_Id": "7111011104", "Trade_Lake_Trade_Major_Version": "1", "Swap_Leg_ID": "", "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency1_Util_Amount": "50.0", "Exchanged_Currency2_Payment_Amount_Currency": "SAR", "Exchanged_Currency2_Util_Amount": "187.5" } } } } Technical NACK message sample: - Invalid Request Data `{` ` ``"Utilization"``: {` ` ``"Utilization_Id"``: ``""``,` ` ``"Response"``: ``"NACK"``,` ` ``"Error_Reason"``: ``"Raw message error."` ` ``},` ` ``"Request_Info"``: {` ` ``"Raw_Request"``: ``"{\n \"Utilization\": {\n \"Utilization_Id\": \"6721092670\",\n \"Util_Type\": \"VDATE-FULL-UTIL\",\n \"AACode_Comments\": \"AACode_Comments\",\n \"Util_Payment_Ref\": \"Util_Payment_Ref\",\n \"Maker_ID\": \"8220478\",\n \"Checker_ID\": \"1633330\",\n \"Trade\": {\n \"Trade_Id\": \"6721092670\",\n \"Trade_Lake_Trade_Major_Version\": \"1\",\n \"Swap_Leg_ID\": \"\",\n \"Exchanged_Currency1_Payment_Amount_Currency\": \"USD\",\n \"Exchanged_Currency1_Util_Amount\": 30.0\n }\n }"` ` ``}` `}` - Ratan Internal Error `{` ` ``"Utilization"``: {` ` ``"Utilization_Id"``: ``"7721092670"``,` ` ``"Response"``: ``"NACK"``,` ` ``"Error_Reason"``: ``"Ratan internal error."` ` ``},` ` ``"Request_Info"``: {` ` ``"Utilization"``: {` ` ``"Utilization_Id"``: ``"7721092670"``,` ` ``"Orig_Utilization_Id"``: ``null``,` ` ``"Util_Type"``: ``"EARLY-PART-UTIL"``,` ` ``"AACode_Comments"``: ``"FX"``,` ` ``"Util_Payment_Ref"``: ``"1"``,` ` ``"Maker_ID"``: ``"1642375"``,` ` ``"Checker_ID"``: ``"1376381"``,` ` ``"Trade"``: {` ` ``"Trade_Id"``: ``"7721092670"``,` ` ``"Trade_Lake_Trade_Major_Version"``: ``"1"``,` ` ``"Swap_Leg_ID"``: ``""``,` ` ``"Exchanged_Currency1_Payment_Amount_Currency"``: ``"USD"``,` ` ``"Exchanged_Currency1_Util_Amount"``: ``"50"` ` ``}` ` ``}` ` ``}` `}` | Same to Request |

## ~~ Auto Utilization Response~~

```
{
  "Utilization_Id": "fxu.7419987178642673665",
  "Trade": {
        "Trade_Id": "7111011225",
    "Trade_Lake_Trade_Major_Version": 1,
    "Swap_Leg_ID": "",
    "Exchanged_Currency1_Payment_Amount_Currency": "EGO",
        "Exchanged_Currency1_Util_Amount": "476.19",
    "Exchanged_Currency1_Remaining_Amount": 0,
        "Exchanged_Currency2_Payment_Amount_Currency": "USD",
    "Exchanged_Currency2_Util_Amount": "100.0",
        "Exchanged_Currency2_Remaining_Amount": 0
}
}
```

## Nack Description

```
    public static final String MVP_NO_REVERSE_UTILIZATION = "Currently reverse is not allowed.";
    public static final String MVP_NO_EARLY_UTILIZATION = "Currently early utilization is not allowed.";
    public static final String MVP_NO_PASTDUE_UTILIZATION = "Currently pastdue utilization is not allowed.";
    public static final String MVP_NO_PARTIAL_UTILIZATION = "Currently partial utilization is not allowed.";
    public static final String INVALID_UTILIZATION_REQ_STATUS = "Invalid utilization request status in Util_Type.";
    public static final String UTILIZATION_ID_NOT_EMPTY = "Utilization_Id can not be empty.";
    public static final String UTILIZATION_OBJECT_NOT_EMPTY = "Utilization object can not be null.";
    public static final String ORIGIN_UTILIZATION_ID_NOT_EMPTY = "Orig_Utilization_Id can not be empty.";
    public static final String AACODE_COMMENTS_NOT_EMPTY = "AACode_Comments can not be empty.";
    public static final String UTIL_PAYMENT_REF_NOT_EMPTY = "Util_Payment_Ref can not be empty.";
    public static final String MAKER_ID_NOT_EMPTY = "Maker_ID can not be empty.";
    public static final String CHECKER_ID_NOT_EMPTY = "Checker_ID can not be empty.";
    public static final String TRADE_NOT_EMPTY = "Trade object can not be empty.";
    public static final String TRADE_ID_NOT_EMPTY = "Trade.Trade_Id can not be empty.";
    public static final String TRADE_VERSION_NOT_EMPTY = "Trade.Trade_Lake_Trade_Major_Version can not be empty.";
    public static final String SWAP_LEG_ID_NOT_EMPTY = "Trade.Swap_Leg_ID is not right.";
    public static final String CURRENCY1_NOT_EMPTY = "Trade.Exchanged_Currency1_Payment_Amount_Currency can not be empty.";
    public static final String CAN_NOT_FIND_ANOTHER_CURRENCY = "Can not find another currency.";
    public static final String UTILIZE_AMOUNT1_NOT_EMPTY = "Trade.Exchanged_Currency1_Util_Amount can not be empty.";
    public static final String AUTO_UTILIZATION_TRADE = "This is auto utilization trade.";
    public static final String MANUAL_UTILIZATION_TRADE = "This is manual utilization trade.";
    public static final String SETTLEMENT_MEANS_OR_ACCOUNT_NOT_RIGHT = "Settlement means or account is not FXBRREC or FXBRREC-M.";
    public static final String TRADE_IS_AMENDED = "Trade is amended.";
    public static final String ILLEGAL_TRADE_ID = "Could not find any data, requested trade id may not in util scope.";
    public static final String TRADE_IS_CANCELLED = "Trade is cancelled.";
    public static final String CASHFLOW_STATE_NOT_AVAILABLE_MANUAL = "Cashflow state not available for manual util.";
    public static final String CASHFLOW_STATE_NOT_AVAILABLE_FOR_AUTO = "Cashflow state not available for auto util.";
    public static final String CASHFLOW_STATE_NOT_AVAILABLE_FOR_PASTDUE = "Cashflow state not available for pastdue.";
    public static final String CASHFLOW_STATE_NOT_AVAILABLE_FOR_PASTDUE_REV = "Cashflow state not available for pastdueReverse.";
    public static final String CASHFLOW_STATE_NOT_AVAILABLE_REVERSE = "Cashflow state not available for reverse.";
    public static final String RATAN_INTERNAL_ERROR = "Ratan internal error.";
    public static final String UTILIZATION_REQ_NOT_BEFORE_VD = "Utilization request is not before value date.";
    public static final String UTILIZATION_REQ_NOT_AFTER_VD = "Utilization request is not after value date.";
    public static final String UTILIZATION_REQ_NOT_ON_VD = "Utilization request is not on value date.";
    public static final String NO_UTILIZATION_CAN_BE_REVERSED = "No available utilization can be reversed.";
    public static final String UTILIZATION_ALREADY_REVERSED = "This utilization has already been reversed.";
    public static final String REMAINING_AMOUNT_NOT_ENOUGH = "Remaining amount is not enough to util.";
    public static final String REVERSE_AMOUNT_NOT_RIGHT = "Reverse amount is not right.";
    public static final String UTILIZE_AMOUNT_NOT_FULL = "Utilization amount is not full utilization.";
    public static final String REVERSE_AMOUNT_NOT_FULL = "Reverse amount is not full reverse.";
    public static final String DUPLICATE_UTILIZE_ID = "Duplicate utilizeId found.";
    public static final String CASHFLOW_CNT_NOT_WRIGHT = "Cashflow count is not consistency with product.";
    public static final String TRADE_CONTAINS_ERROR_CASHFLOW = "Trade contains error cashflow.";
```

# Appendix