# FMRP Cashflow Blotter

| | Menu Item | Cashflow State | Cashflow Sub State | Cashflow Sub State Type | Other Condition |
| --- | --- | --- | --- | --- | --- |
| 1 | Early Materialization | PROJECTED | | | |
| 2 | ReInstate | FAILED | | | |
| 3 | QUEUED | | Pending Exception | |
| 4 | Settle As Gross | WAITING | NA Pending Operator | Pending Another Leg | Settlement_Method<> "UTIL" |
| 5 | WAITING | | Pending Netting Pending Auto Netting | Settlement_Method<> "UTIL" |
| 6 | Status Write Back | RELEASED SETTLED NOSTRO_MATCHED | | | |
| 7 | Regenerate Swift | READY | | Pending Ack | Cashflow Swift Message Standard = 'STRATEGIC' |
| 8 | Resend To Razor | READY | | Pending Ack | Cashflow Swift Message Standard <> 'STRATEGIC' |
| 9 | Early Release | READY | NA | NA | Settlement_Method<> "UTIL" |
| 10 | Update Affirmation | WAITING | | Pending Exception | Cashflow Affirmation Status<>Affirmed and Settlement_Method<> "UTIL" |
| 11 | Swift Suppression | PROJECTED WAITING READY | | <>Swift Suppression <>Undo Swift Suppression <>Cashflow Suppression <>Undo Cashflow Suppression | Settlement_Method<> "UTIL" |
| 12 | Verify Swift Suppression | WAITING | Pending Verification | Swift Suppression | Settlement_Method<> "UTIL" |
| 13 | Undo Swift Suppression | SWIFT_SUPPRESSED | | | Settlement_Method<> "UTIL" |
| 14 | Verify Undo Swift Suppression | WAITING | Pending Verification | Undo Swift Suppression | Settlement_Method<> "UTIL" |
| 15 | Suppress Cashflow | "PROJECTED", "WAITING", "READY" | | <>Swift Suppression <>Undo Swift Suppression <>Cashflow Suppression <>Undo Cashflow Suppression | Settlement_Method<> "UTIL" |
| 16 | **FAILED && after value date.** | | | Settlement_Method<> "UTIL" |
| 17 | Confirm Suppression | WAITING | Pending Verification | Cashflow Suppression | Settlement_Method<> "UTIL" |
| 18 | Un-Suppress Cashflow | CASHFLOW_SUPPRESSED | | | Settlement_Method<> "UTIL" |
| 19 | Confirm Un-Suppression | WAITING | Pending Verification | Undo Cashflow Suppression | Settlement_Method<> "UTIL" |
| 20 | Manual Fail | "QUEUED", "WAITING", "READY" | | | Settlement_Method<> "UTIL" |
| 21 | SWIFT_SUPPRESSED", "CASHFLOW_SUPPRESSED | | | Current Date > Payment_Date and Settlement_Method<> "UTIL" |
| 22 | Confirm Manual Fail | | Pending Verification | Pending Manual Fail | Settlement_Method<> "UTIL" |
| 23 | BIC Net Selected Cashflow | WAITING | | Pending Netting Pending Auto Netting | Booking Entity SCI FMCODE='SCB LONDON*LDN' ~~Booking Entity SCI FMCODE <> 'SCB HONGKON*HKG'~~ and Counterparty SIC BIC Net Flag ='Y' and Splitting Id is empty and Settlement_Method<> "UTIL" |
| 24 | CCIL Net Selected Cashflow | WAITING | | Pending Netting Pending Auto Netting | Counterparty SCI FMID<>400021949 and Counterparty SIC BIC Net Flag <>Y and Settlement Method = 'CCIL' and Splitting Id is empty and Settlement_Method<> "UTIL" |
| 25 | Net Selected Cashflow | "PROJECTED", "WAITING", "READY" | | | Counterparty SIC BIC Net Flag <>Y and Settlement Method <> 'CCIL' and Splitting Id is empty and Settlement_Method<> "UTIL" |
| 26 | WAITING | | Pending Netting Pending Auto Netting | Counterparty SCI FMID=400021949 and Counterparty SIC BIC Net Flag <>Y and Settlement Method = 'CCIL' and Splitting Id is empty and Settlement_Method<> "UTIL" |
| 27 | Un-Net Cashflow | <>NETTED and <> SPLIT | | | Netting Id is not null and Settlement_Method<> "UTIL" |
| 28 | Hold | ~~"QUEUED", ~~"WAITING", "READY" | | | Settlement_Method<> "UTIL" |
| 29 | Unhold | HOLD | | | Settlement_Method<> "UTIL" |
| 30 | Send To WAITING | HOLD | | | Settlement_Method<> "UTIL" |
| 31 | View Swift Message | RELEASED SETTLED | | | |
| 32 | Manual Settle | RELEASED | | | swift status list ("AMH Error", "Check in FMSGW", "Check in FMSRE", "FMSGW Deleted", "FMSGW Error", "FMSRE Deleted", "FMSRE Error", "Manual Delete", "SCPAY Error", "Pending FMSGW Disp", "Pending FMSRE Disp") |
| 33 | Bulk Submit | “WAITING” | "Pending Operator" | "Pending Exception" | |
| 34 | Bulk Approve | | "Pending Verification" | "Pending Exception" | |
| 35 | Bulk Submit/Approve | | | | (selected cashflow sub state same but not follow above bulk status will show with disabled) |
| 36 | Split Cashflow | "WAITING", "READY" | | | Netting Is is empty and Splitting Id is empty and Cashflow Event Type = "New" and Trade Original Source System Name <>'LOANIQ' and Settlement_Method<> "UTIL" |
| 37 | Amend Split Amount | WAITING | | | Splitting Id Exists and Cashflow Event Type = "New" and Settlement_Method<> "UTIL" |
| 38 | **Un-Split Cashflow** | NOT IN ('RELEASED','SETTLED') | | | Splitting Id Exists and Cashflow Event Type = "New" and Settlement_Method<> "UTIL" |
| 39 | ** Settlement Method Update** ** **** ** | WAITING | | | Settlement Method in ('GROSS','') and Data_Flow.Data_Source_System <>Ratan and Instrument_Common.ISDA_Taxonomy in ('ForeignExchange:Forward','ForeignExchange:Spot','ForeignExchange:Swap') |
| 40 | READY | NA | NA |
| 41 | WAITING, READY, PASTDUE | | | Settlement Method is UTIL and Data_Flow.Data_Source_System <>Ratan and Instrument_Common.ISDA_Taxonomy in ('ForeignExchange:Forward','ForeignExchange:Spot','ForeignExchange:Swap') |
| 42 | **Comment** | | | | |
| 43 | **adhoc SSI** | | | | |
| 44 | **Submit** | | | | |
| 45 | **Approve** | | | | |

**EXPAND: Historical info**

| **Action Name** | **Action Description** | **Action Limitation** | **Maker/Checker** | **Action Result** | **Requirement Detail ****Page** | **Screenshot** |
| --- | --- | --- | --- | --- | --- | --- |
| Early Materialization | | | | | | |
| Settle As Gross | User may want to "Settle as Gross", when there is no need to do netting, e.g. only 1 cashflow is 'waiting netting' or 'pending another leg', or the user does not want to net the multiple cashflows anymore even they are under 'waiting netting' or 'pending another leg'. | Only when cashflows are in 'waiting netting' or 'pending another leg' status. | | - Exception '**NET to Gross' **will be generated together with other exceptions( if any), the exception '**NET to Gross' **would be only visible to checker(exception maker/checker concept) which means exception fix maker can't see this exception. - If Checker agrees to settle as Gross, after he/she approve the multiple exception, the cashflow status updates to "Ready" | Netting Service - GUI & API intergration - Derivative Strategy Projects - Confluence (standardchartered.com) | |
| Status Write Back | | | | | | |
| Manual Fail | When the cashflow is not settled in time, settlement platform need to move the cashflows to 'FAILED' status. Settlement Ops will pay additional attention to the 'FAILED' cashflows and a separate 'Failed Re-Process' flow will be followed to re-process the cashflows. ‘FAIELD’ is one of the cashflow main status for below purpose. 1. - Highlight the cashflows which are not settled before the due date/time( the cutoff) - Ops can explicitly set a new ‘Swift Value Date’ for the swift message generation. | | | No further actions( e.g. exception handling) can be done on the 'FAILED' cashflow, the only action in Ratan is 'Re-Instate' from Cashflow Blotter. But the new cashflow events from Stella can overwrite the cashflows. | | |
| ReInstate | - Cashflows re-instate from 'FAILED' status will generate exception 'Re-Instate' and pending for Maker/Checker to re-process cashflow & fix this exception, Maker/Checker will select the '**Swift Value Date**'(Settlement_Instruction.Value_Date) as part of exception fix. - FMO Ops can right click on the 'FAILED' cashflow from cashflow blotter and perform action 'Re Instate'. | | | - Cashflow will go to 'QUEUED' status and run through the 'Netting client Check'/'Exception Check' process. - As the result of 'Exception Check' there'll be dedicated exception 'Cashflow Re-Instate' generated. - This is Maker/Checker exception and default as Maker's exception ('Pending Operator') when exception populated. | | |
| Hold | When the cashflow does not reach cashflow "cutoff day" yet, user may want to put the cashflow on hold due to any reason (e.g. user finds some issue or wants to supplement the cashflow/trade info later). | - Cashflow can be put on hold after any status (unless its RELEASED, NET or SPLIT). - Eligible User for Hold Action: All users, regardless of profile access: e.g. MKR, BOC, BO, BOL, BOM | Maker & Checker | After Hold action, main status will update to "ON HOLD" , sub status to ‘Pending Verification’ | [Hold/UnHold - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2742543606) | |
| Unhold | - Eligible User for Unhold Action: BOC, BO, BOL, BOM - Same user who put on hold cannot do unhold action. | Checker | After Unhold action, cashflow status will revert back to the previous status before Hold and continue processing from there | |
| Net | For FMRP Strategy Netting would be handled in Ratan, the cashflow can source from multi TP systems( Stella/Murex 2.11/MXCash). After the netting in Ratan, there's possibility new cashflow events flow down to Ratan from the trade market events( Amendment/Cancellation/Termination & etc). | Conditions to allow the netting actions: 1. - Cashflow not in "Settled" nor "Released": e.g. in 'Projected'/ 'Queued'/ 'Pending'/ 'Validated'/ 'Ready'/ 'Waiting'/ 'Hold' status - Netting Id is blank for the selected cashflows | - Checker to review & approve exception '**Net Cashflow' **on the netting resultant cashflow, as part of multi exception fix. | - Calculate the amount & direction, generate Netting Resultant cashflow - Netting Status update: Update the Netting component cashflow to 'Netted' and netting resultant cashflow as 'Queued'. Call the status update API with the required fields (not all the required listed in the below table). - Netting Exception generation & close | [Netting Service - GUI & API intergration - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2594781981#NettingServiceGUI&APIintergration-GUIGuide) | [Netting Service - GUI & API intergration - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2594781981#NettingServiceGUI&APIintergration-NettingPreviewGUI:) |
| Un-Net | Ratan need to identify the new market events on these netted cashflow and automatically perform the un-net, the un-net cashflow will be hold as NSTP and waiting for user further review and actions. | Conditions to do the un-net actions - - Cashflow not in "Settled" nor "Released": e.g. in 'Queued'/ 'Pending'/ 'Validated'/ 'Hold' status - Netting id is not blank | Checker to approve the exception '**Previously Netted' ** on the component cashflow and proceed as Gross. | - update cashflow status - Generate the exception '**Previously Netted' **on the netted component cashflow, this can be closed if | |
| Swift Suppression | To be used for scenarios where we know that **<u>payment is not required</u>** | | - Maker to initiate action - (Checker Approve/Reject action) | Cashflow status changes to "WAITING"/ "Swift Suppression"/"Pending Verification" | [Cashflow/Swift Suppression - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2738540597) | |
| Verify Swift Suppression | After Maker initiate the Swift Suppression action, Checker is required to Approve/Reject this Swift Suppression action | | Checker | Cashflow status changes to "SWIFT SUPPRESSED"/ "NA"/ "NA" | |
| Undo Swift Suppression | If suppression was done in error, Un-suppression can be done until Value date. | Un-suppression cannot be done beyond value date. If payment required, it has to be handled via AMH / Oscar | Maker | Cashflow status changes to "WAITING" / "Undo Swift Suppression"/"Pending Verification" | |
| Verify Undo Swift Suppression | After Maker initiate the Undo Swift Suppression action, Checker is required to Approve/Reject this Undo Swift Suppression action | | Checker | Cashflow status changes to "QUEUED"/ "NA"/ "NA" | [Cashflow/Swift Suppression - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2738540597) |
| Suppress Cashflow | To be used for scenarios where **<u>payment and settlement accounting is not required</u>** | | Maker | Cashflow status changes to "WAITING"/ "Cashflow Suppression"/"Pending Verification" | |
| Confirm Suppression | After Maker initiate the Cashflow Suppression action, Checker is required to Approve/Reject this Cashflow Suppression action | | Checker | Cashflow status changes to "CASHFLOW SUPPRESSED"/ "NA"/ "NA" | |
| Un-Suppress Cashflow | If Cashflow suppression was done in error, Un-suppression can be done until Value date. | Un-suppression cannot be done beyond value date. If payment + accounting is required, it has to be handled via Oscar | Maker | Cashflow status changes to "WAITING" / "Undo Cashflow Suppression"/"Pending Verification" | |
| Confirm Un-Suppression Cashflow | After Maker initiate the Undo Cashflow Suppression action, Checker is required to Approve/Reject this Undo Cashflow Suppression action | | Checker | Cashflow status changes to "QUEUED"/ "NA"/ "NA" | |
| View Cashflow Details | | | Maker & Checker | | | [▶ Multi Exceptions - Exceptions in Cashflow CN (figma.com)](https://www.figma.com/proto/crlFDt3cKfWzIXWdUhrtQ7/Exceptions-in-Cashflow-CN?type=design&node-id=521-2&scaling=contain&page-id=0%3A1&starting-point-node-id=521%3A2&show-proto-sidebar=1) |
| View Trade Details | | | Maker & Checker | | | |
| Fix Exceptions (Maker/Checker in Cashflow Details) | | | Maker & Checker | | | |
| Manual Settle | When cashflow stays in 'Released' status, and swift status stays in ("AMH Error", "Check in FMSGW", "Check in FMSRE", "FMSGW Deleted", "FMSGW Error", "FMSRE Deleted", "FMSRE Error", "Manual Delete", "SCPAY Error"), user is allowed to do 'Manual Settle' to settle this cashflow | | | | | |

**EXPAND_END**

# BCS Cashflow Blotter

| | Menu Name | Maker/Checker action? | lastChecker | StpFlag (true STP) | Permission | Cashflow.Cashflow_State | Cashflow_Sub_Status | Cashflow_Sub_Status_Type | Other Condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Reinstate | maker | | N | RATAN_CASHFLOW_BLOTTER:F_Reinstate | FAILED | Pending Operator | NSTP Release | |
| 2 | **Update Affirmation Status** | maker | **user maker id as the checker** | N | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Affirmation_Status_Change | PROJECTED|QUEUED|PENDING | | | |
| 3 | Net Selected Cashflow | maker | | N | RATAN_CASHFLOW_BLOTTER:F_Perform_Ad_Hoc_Netting | PROJECTED|QUEUED | | Must NOT be Auto Netting for selected rows | |
| 4 | Un-Net Cashflow | | | N | RATAN_CASHFLOW_BLOTTER:F_Perform_Un_Net_Initiate | QUEUED (for maker role) | Pending Operator (for maker role) | NSTP Release (for maker role) | |
| 5 | Verify Un-Net Cashflow | | | | RATAN_CASHFLOW_BLOTTER:F_Perform_Un_Net_Verify | QUEUED (for checker role) | Pending Verification | Un-Net | |
| 6 | Adhoc SSI Input - Maker | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_SSI_Initiate | PROJECTED|QUEUED | EMPTY or Pending Operator | EMPTY or Adhoc SSI Amendment or NSTP Release | |
| 7 | Adhoc SSI Input - Checker | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_SSI_Verify | PROJECTED|QUEUED | Pending Verification | Adhoc SSI Amendment | |
| 8 | Release Cashflow | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | QUEUED or FAILED | Pending Operator | NSTP Release | |
| 9 | Confirm Release > Accept Release | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | QUEUED or FAILED | Pending Verification | NSTP Release | |
| 10 | Confirm Release > Reject Release | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | QUEUED or FAILED | Pending Verification | NSTP Release | |
| 11 | Release Failed Cashflow > Set Value Date to Deal Value Date | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | FAILED | Pending Operator | NSTP Release | |
| 12 | Release Failed Cashflow > Set Value Date to Current System Date | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | FAILED | Pending Operator | NSTP Release | |
| 13 | Confirm Release Failed Cashflow > Accept Deal Value Date | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | FAILED | Pending Verification | NSTP Release | |
| 14 | Confirm Release Failed Cashflow > Confirm Current System Date | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | FAILED | Pending Verification | NSTP Release | |
| 15 | Confirm Release Failed Cashflow > Reject Release | | | | RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release | FAILED | Pending Verification | NSTP Release | |
| 16 | Add Comment | | | | RATAN_CASHFLOW_BLOTTER:F_Add_Settlement_Comment | | | | |
| 17 | Suppress Cashflow | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress | PROJECTED|QUEUED | | != Adhoc Suppression | |
| 18 | Confirm Suppression > Accept Suppression | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress | PROJECTED|QUEUED | Pending Verification | Adhoc Suppression | |
| 19 | Confirm Suppression > Reject Suppression | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress | PROJECTED|QUEUED | Pending Verification | Adhoc Suppression | |
| 20 | Un-Suppress Cashflow | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress | SUPPRESSED | | | |
| 21 | View Trade Details | | | | None | Any, but hidden for non-NETTED rows with Netting_Id | | | |
| 22 | Manual Fail | | | | RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress | FAILED|QUEUED | | | |
| 23 | View Cashflow Details | | | | None | Any | | | |
| 24 | View Cashflow History | | | | None | Any | | | |
| 25 | View Swift Message | | | | None | RELEASED|SETTLED | | | |