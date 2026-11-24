- Maker API: **/v3/adhoc/ssis/makerInput/{cashflowId}**

requestbody->fitVostro→ add **manualTag70 **+ **manualTag72 **field, the **ssiId **is already exist.

when the ssiId has value and the fields of 70/72 are updated, pls set the manualTag70/manualTag72 to Y as need, otherwise set the value to N

- Checker API: 1. approve 1. /v2/stamping/exception/{exceptionId}/approve 2. requestbody->fitVostro→ the **manualTag70 **** **+ **manualTag72 should be same** with the value in the Maker_Request_Body, 2. reject 1. /v2/stamping/exception/{exceptionId}/reject 2. requestbody keep same as current

- After checker approved, the **Manual_Tag_70**+ **Manual_Tag_72 **are in the cashflow → Settlement_Instruction
- if there is an Adhoc SSI exception, and there is Maker_Request_Body in the Stashing, you should find the manualTag70/manualTag72 from the Maker_Request_Body, not from cashflow → Settlement_Instruction
- when query cashflow details, should add **Manual_Tag_70+ Manual_Tag_72 in the Settlement_Instruction, after Nostro_Swift_Message_Type**
- **Exist cashflow, the value of Manual_Tag_70/Manual_Tag_72 is null**