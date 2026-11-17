## Nostro Static

Sign off:

## EBBS Bridge account

| Entity | FMID | Legal Entity | Closing Entity | EBBS bridge account | Branch code |
| --- | --- | --- | --- | --- | --- |
| SEOUL | 10036645 | SCB SEOUL*SEL | | 000287(KRW) | 70 |
| SEOUL | 10036645 | SCB SEOUL*SEL | | 040446(ALL) | 70 |

Branch code in static-data-service file

![image-2026-5-15_10-28-39.png](attachments/image-2026-5-15_10-28-39.png)

SQL: select * from ratanone.ratan_static__cashflow_ebbs_bridge_account a , ratanone.ratan_static__cashflow_ebbs_txn_code b  where a.fmid =b.fmid and a.fmid ='10036645'![image-2026-5-15_10-20-17.png](attachments/image-2026-5-15_10-20-17.png)

## Netting configuration

INSERT INTO cash_netting_service.ratan_auto_netting_type_config (id, net_type,net_group_key_config,resultant_mapping_config,is_swift_suppress_when_single_cashflow,priority,description,"version",created_at,updated_at) VALUES

('8','NDS Auto Netting','[{"field":"Cashflow.ND_Parent_Trade_Id","path":"CASHFLOW__ND_PARENT_TRADE_ID"},{"field":"Entity.Booking_Entity_SCI_FMID","path":"ENTITY__BOOKING_ENTITY_SCI_FMID"},{"field":"Entity.Counterparty_SCI_FMID","path":"ENTITY__COUNTERPARTY_SCI_FMID"},{"field":"Cashflow.Payment_Currency","path":"CASHFLOW__PAYMENT_CURRENCY"},{"field":"Cashflow.Payment_Date","path":"CASHFLOW__PAYMENT_DATE"}]','{"Cashflow__Payment_Type":"NDS Auto Netting"}',false,54,'NDS Auto netting',1,'2026-02-09 10:45:15.00171','2026-02-09 10:45:15.00171');

![image-2026-7-9_17-51-27.png](attachments/image-2026-7-9_17-51-27.png)

## Cutoff time

For all currency, cut off time set at 1:30:00 AM GMT (VD 10:30AM (KST)) on value date.

## Swift static

| Entity | FMID | Legal Entity | Sender BIC | Field 53 BIC | Field 53 CCY to be used | Field 58 BIC |
| --- | --- | --- | --- | --- | --- | --- |
| SEOUL | 10036645 | SCB SEOUL*SEL | SCBLKRSEXXX | | | |

## NSTP rule

| # | Date Added | Owner of Requirement | Department | NSTP Code | Rule | Rule Comments | When | Date Completed | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Instrument_Common__Murex_Product_Typology in ("Structured Swap", "Red Trades-StrucSwap", "SLT-Cust") | KR Typology check | | | |
| 2 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Entity__Counterparty_Client_Type == "FININST" | KR - FI Client | | | |
| 3 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Instrument_Common__Murex_Product_Group == "LN_BR" | KR LN_BR -> LNBR to be NSTP and suppress manually by ops | | | |
| 4 | | | | | Instrument_Common__Murex_Product_Typology in ("NDS", "NDCF", "NDFRA", "ND CDS Fixing", "ND CDS", "ND-Convert", "NDS Fixing") && Cashflow__ND_Parent_Typology != "NDIRS" && Cashflow__Cashflow_Event_Reason not in ("Reversal", "Rebook") && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") && ((Cashflow__Duplicate_NDS_FXD == null || Cashflow__Duplicate_NDS_FXD == "")) && (Cashflow__Splitting_Id == null || Cashflow__Splitting_Id == "") && (Cashflow__Payment_Currency != "USD" || Entity__Counterparty_Client_Type not in ("\"INTECOM\"", "\"INTEBCH\"", "\"INTLACC\"") || Entity__Counterparty_SCI_FMID == "10036645") && Entity__Booking_Entity_SCI_FMID != "10036645" | Pending NDS Netting | | | |
| 5 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Cashflow__Cashflow_Amount_USD_Transfered >= 500000000 | KR 500 Mio Payment | | | |
| 6 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Entity__Counterparty_SCI_FMID == "2" | KR HK Payment | | | |

## Cashflow suppression rule

| # | Date Added | Owner of Requirement | Department | Description of requirement | Rule Reason | Date Completed in PROD | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Instrument_Common__Murex_Product_Family == "IRD" && Instrument_Common__Murex_Product_Group == "BOND" && Instrument_Common__Murex_Product_Typology != "SLT-Cust" | KR BOND | | |
| | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Entity__Counterparty_SCI_FMID == "400649418" && (Cashflow__Netting_Id != null && Cashflow__Netting_Id != "") | KR KRX/SEL netted cashflow | | |
| | | | | Entity__Booking_Entity_SCI_FMID not in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "401036553", "400991880", "400007847", "10075222", "400041070", "400906330", "401053411", "300075472", "6", "300011345", "2", "10038345", "400018439", "5", "8", "10036428", "7", "10036382", "400032489", "400045551", "300089409", "400910415", "10036430", "300010782", "300011525", "10041903", "10041902", "10040387", "10037477", "300084297", "10036647", "10022098", "10041530", "10036655", "300011470", "10036645") && Trade_Original_Source_System_Name not matches "(?i)^LOANIQ$" | Non FMRP entities | | |
| | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Cashflow__Payment_Currency in ("XAF", "XAG", "XAU", "XPD", "XPT", "XRH") | KR Precious Metal | | |
| | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Instrument_Common__Murex_Product_Group == "LN_BR" | KR LN_BR | | |

## Auto-Netting rule

| # | Date Added | Owner of Requirement | Department | Rule ID | Rule | Rule Comments | When | Date Completed | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Entity__Counterparty_SCI_FMID == "400649418" && Instrument_Common__Murex_Product_Group == "IRS" && Cashflow__Payment_Currency == "KRO" && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") | KR KRX/SEL auto netting | | | VD-1 15:00 KST |
| 2 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Entity__Counterparty_SCI_FMID == "10075222" && Cashflow__Payment_Currency in ("USD", "EUR") && Instrument_Common__Murex_Product_Type == "FXD" && Instrument_Common__Murex_Product_Typology == "NDF" && Portfolio__Booking_Entity_Trade_Portfolio_Name != "COM_KRO_BTB" && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") | KR SCB/LDN NDF auto netting (duplicate in uat-4) | | | VD-1 15:00 KST |
| 3 | | | | | Entity__Booking_Entity_SCI_FMID == "10036645" && Entity__Counterparty_SCI_FMID == "10075222" && Cashflow__Payment_Currency == "USD" && Instrument_Common__Murex_Product_Type == "FXD" && Instrument_Common__Murex_Product_Typology == "NDF" && Portfolio__Booking_Entity_Trade_Portfolio_Name == "COM_KRO_BTB" && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") | KR SCB/LDN Commodity NDF auto netting | | | VD-1 15:00 KST |
| 4 | | | | | Instrument_Common__Murex_Product_Typology in ("NDS", "NDCF", "NDFRA", "ND CDS Fixing", "ND CDS", "ND-Convert", "NDS Fixing") && Cashflow__ND_Parent_Typology != "NDIRS" && Cashflow__Cashflow_Event_Reason not in ("Reversal", "Rebook") && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") && ((Cashflow__Duplicate_NDS_FXD == null || Cashflow__Duplicate_NDS_FXD == "")) && (Cashflow__Splitting_Id == null || Cashflow__Splitting_Id == "") && Entity__Booking_Entity_SCI_FMID == "10036645" | NDS Auto Netting | | | VD-1 15:00 KST |
| 5 | | | | | ~~Cashflow__Payment_Currency == "USD" && Cashflow__Cashflow_Event_Type == "New" && ((Entity__Booking_Entity_SCI_FMCODE in ("SCB LONDON*LDN") && Entity__Counterparty_SCI_FMCODE in ("SCB SEOUL*SEL")) || (Entity__Booking_Entity_SCI_FMCODE == "SCB SEOUL*SEL" && Entity__Counterparty_SCI_FMCODE in ("SCB LONDON*LDN"))) && Trade_Original_Source_System_Name != "LOANIQ" && Cashflow__Cashflow_Event_Reason not in ("Rebook", "Reversal", "Reversal_Rebook") && Instrument_Common__Murex_Product_Typology != "NDF"~~ | ~~Ratan Inter Entity Netting UK vs KR~~ | | | |

## Swift suppression rule

## BIC_Netting

No BIC_netting rule needed in RATAN for Korea.