# Layout:

- Trade Details | Attributes | Logical Model Path | | --- | --- | | Trade ID | Trade.Trade_Id | | Trade Version | Trade.Trade_Version | | Trade Status | Trade.Trade_State | | Confirmation Status | | | Booking Entity | Entity.Booking_Entity_SCI_FMCODE | | Coiunterpart | Entity.Counterparty_SCI_FMCODE | | Portfolio | Portfolio.Booking_Entity_Trade_Portfolio_Name | | Product Taxnomy | Instrument_Common.ISDA_Taxonomy | | CFI Code | Instrument_Common.CFI_Code |
- Cashflow Details | Attributes | Logical Model Path | | --- | --- | | Cashflow ID | Cashflow.Cashflow_Id | | Netting ID | Cashflow.Netting_Id | | Cashflow Business Version | Cashflow.Cashflow_Business_Version | | Cashflow Event | Cashflow.Cashflow_Event_Type | | Cashflow Affirmation | Cashflow.Cashflow_Affirmation_Status | | Value Date | Cashflow.Payment_Date | | Currency | Cashflow.Payment_Currency | | Amount | Cashflow.Payment_Amount | | Pay/Receive | If Cashflow.Payment_Payer_Party_Reference=='party1' then 'Pay' Else 'Receive'. | | Payment Cutoff | | | Cashflow Status | Cashflow.Cashflow_State |
- Sub Status
- Action History
- Exceptions

![image2023-4-17_17-40-58.png](attachments/image2023-4-17_17-40-58.png)