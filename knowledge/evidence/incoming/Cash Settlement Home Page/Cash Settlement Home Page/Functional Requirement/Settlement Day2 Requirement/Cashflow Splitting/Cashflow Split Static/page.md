##

## NSTP Rule

| Action | Rule ID | Description | Rule Condition | Exception Code | Operation Level | Exception Category | Bulk Eligible | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| New | | NSTP rule for split child cashflow | Cashflow__Splitting_Id != null && Cashflow__Splitting_Id != "" | Split Cashflow | MAKER_CHECKER | NSTP | un-ticked | |
| New | | NSTP rule for amended split child cashflow | Cashflow__Is_Split_Amend_Amount == true | Split Amend | MAKER_CHECKER | NSTP | un-ticked | |
| New | | NSTP rule for unsplit cashflow | Cashflow__Is_Cashflow_Unsplit == true | Un-Split | MAKER_CHECKER | NSTP | un-ticked | |
| New | | NSTP rule for withdrawal event of split cashflow | Cashflow__Is_Withdrawal_On_Split == true | Withdrawal on Split | MAKER_CHECKER | NSTP | un-ticked | |
| Update | 7350773637874561024 | add condition to exclude split child from pending NDS auto netting rule | Instrument_Common__Murex_Product_Typology in ("NDS", "NDCF", "NDFRA", "ND CDS Fixing", "ND CDS", "ND-Convert", "NDS Fixing") && Cashflow__ND_Parent_Typology != "NDIRS" && Cashflow__Cashflow_Event_Reason not in ("Reversal", "Rebook") && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") && ((Cashflow__Duplicate_NDS_FXD == null || Cashflow__Duplicate_NDS_FXD == "")) **&& (Cashflow__Splitting_Id == null || Cashflow__Splitting_Id == "")** | Pending NDS Netting | MAKER_CHECKER | NSTP | ticked | |

## Nostro Threshold Static

Refer to existing static and need confirmation from Dinesh to onboard selected one:

![image-2025-11-24_20-48-45.png](attachments/image-2025-11-24_20-48-45.png)