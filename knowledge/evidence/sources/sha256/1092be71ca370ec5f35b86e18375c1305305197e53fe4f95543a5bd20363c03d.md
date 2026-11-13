# **Requirements**

1. Cashflows of NDS must be Auto Netted by system based on NID (MX2.11 must stop NDS netting & RATAN will do the Auto Netting)
2. STP requirement for Component cashflow - original Typology where netting is not required (same or better than MX2.11) 1. Confirmation match status must follow MX2.11 logic 2. ND IRS 1. USD from NDS Fixing must be STP - always settles in deliverable currency, so no netted involved. Correlation id between NDS Fixing trade/payment & parent NDIRS trade/payment is NID 3. All remaining include ND CCS to be NSTP
3. STP requirement for Net resultant Cashflow (same or better than MX2.11) 1. Confirmation match status must follow MX2.11 logic
4. Product Scope: Typology in (NDS, NDS Fixing, NDIRS, NDCF, NDFRA, ND CDS Fixing, ND CDS and ND-Convert)
5. Netting Key: Booking Entity, Counterparty, same VD, CCY, NID
6. Netting scope: Run netting every 30 mins (currently its every 2 hours in MX2.11) with VD = Business VD Today, Tomorrow & Day After
7. Ability to manually net the resultant cashflow with other product cashflows as long as it is not released
8. Component Cashflows must be NSTP to wait for Auto Netting
9. Group Blotter handling - cashflows must pass through Group Blotter without getting stuck as a normal process then become eligible for Auto Netting
10. Events handling

1. 1. Amendment post Auto Netting but before release of net resultant - Auto Un-net the Net resultant, system to auto net the reversal & new in next cycle of Auto Netting 2. Amendment post Auto Netting but after release of net resultant - Reversal and New get stuck as NSTP ('REVERSAL' and 'REBOOK' exception). User to manually handle 3. Cancellation post Auto Netting but before release of net resultant - Auto Un-net the Net resultant, original cashflow goes to cancelled status. Another cashflow will be waiting to be netted in the next cycle. If another cashflow did not arrive, it will stay in WAITING status. Ops will have to investigate and take manual action 4. Cancellation post Auto Netting but after release of net resultant - Reversal on Component should be held as Reversal. Un-net not allowed by system / manual post payment release. Ops to handle manually. 5. Re-fixing post Auto Netting but before release of net resultant - Same as amendment 6. Re-fixing post Auto Netting but after release of net resultant - Same as amendment 7. Fixed vs Floating scenarios - as per below table

# **Solutioning**

1. Ratan will query parent trade typology (trade in the same NID) once metalized.
2. If cashflow satisfies NSTP rule (NDS Fixing), Typology in(NDS, NDS Fixing, NDCF, NDFRA, ND CDS Fixing, ND CDS and ND-Convert) and ND_Parent_typology != NDIRS, then cashflow will be in WAITING + Pending Exception status.
3. Ratan will scan all cashflows every 30 mins, if it satisfies below condition, cashflow will be auto net together. - Cashflow value date is in [Today, Today+2 business day] - Same Booking Entity, Counterparty, same VD, CCY, NID - Status = WAITING + Pending Exception - Pending Exception contains 'Pending NDS Netting'

****

*NSTP Rule (Pending NDS Netting) needs to be live when perform auto netting

# Tech Design

| | Field | Path | Source |
| --- | --- | --- | --- |
| 1 | Cashflow.ND_Parent_Trade_Id | userDefinedField: NID | Murex |
| 2 | Cashflow.ND_Parent_Typology | If current cashflow typology ='NDS Fixing' Then query Instrument_Common.Source_System_Instrument_Type with Source_System_Internal_Trade_Id = ND_Parent_Trade_Id Source_System_Instrument_Type will take the last data with separator "|" - When querying TDS3 data, there is a possibility that TDS3 didn't get data from Murex yet, then RATAN would get empty value as parent typology | TDS3 |
| 3 | | | |

Netting Resultant cashflow generation

| Logical model field | Generation Logic | Comment |
| --- | --- | --- |
| Data_Flow.Unique_Identifier_Message_Id | UUID | |
| Execution_Date_Time | latest time stmap | |
| Cashflow.Cashflow_Id | fix length 12: 'N' + 11 numeric | |
| Cashflow.Cashflow_Event_Type | pre-config: New | |
| Cashflow.Cashflow_State | pre-config: QUEUED | |
| Cashflow.Cashflow_Affirmation_Status | pre-config: Unaffirmed | |
| Cashflow.Cashflow_Sub_State | pre-config: Blank | |
| Cashflow.Cashflow_Sub_State_Updater | pre-config: Blank | |
| Cashflow.Cashflow_Sub_State_Type | pre-config: Blank | |
| Cashflow.Payment_Type | pre-config: Blank | |
| Cashflow.Netting_Id | UUID | |
| **Family** | Inherit from component cashflow if the values are same, empty if value are different | |
| **Group** | Inherit from component cashflow if the values are same, empty if value are different | |
| **Type** | Inherit from component cashflow if the values are same, empty if value are different | |
| **Typology** | Inherit from component cashflow if the values are same, empty if value are different | |
| **Strategy** | Inherit from component cashflow if the values are same, empty if value are different | |
| **Trade_Id** | Inherit from component cashflow if the values are same, empty if value are different | |
| **Taxonomy** | Inherit from component cashflow if the values are same, empty if value are different | |
| **CFI Code** | Same with NDS cashflow (the one whose typology is not NDS Fixing) | |
| **Settlement Method** | Pre-config: GROSS | |
| **Delivery Method** | Pre-config: CASH | |
| **Cashflow.Payment_Type** | Pre-config: NDS Fixing Netting | |
| Parent_Trade_Id | NA | |
| Trade_State | pre-config: TOBESENT | |
| Cashflow.Cashflow_Version | Pre-Config: 0 | |
| Cashflow.Cashflow_Business_Version | Pre-Config: 0 | |
| Cashflow.FMO_Comment | Pre-config: Blank | |
| Cashflow.FMO_Comment_Updater | Pre-config: Blank | |
| Cashflow.FMO_Comment_Timestamp | Pre-config: Blank | |
| Data_Flow.Data_Publication_Date_Time | Latest timestamp | |
| Other Attributes | Copy from first cashflow | |

# Potential Risk

| 18 | **NDIRS & Non Eco Amendment - Duplicate payment** |
| --- | --- |
| | Steps | Murex Actions | RATAN Checking | RATAN Testing Restult |
| | Trade Booking | 1. Book ND IRS trade(Fix VS Floating) T1 with entity as AG/UK/CN/SG/IN/MY, CCY as CNY | | |
| | Interest rate payment generation | 1. Generate fix leg payment p1 in CNY on VD-2 2. Peform fixing event on floating leg, p1 moved to cancelled & generate p2 in CNY ( netted amount between fix leg & floating leg) on VD-2 | | |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-2 2. p3 in CNY to offset p2, p4 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p4 to RATAN | Publish p4 to RATAN by batch file on VD-2 | p4 is STP in Ratan | |
| | Non Eco C&R | 1.Trade id changed from T1 to T2 2. No change on payment | | |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-2 2. p5 in CNY to offset p2, p6 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p6 to RATAN | Publish p6 to RATAN by batch file on VD-2 | p6 is STP in Ratan, but it's duplicate payment | |
| 19 | **NDS & Non Eco Amendment - Duplicate payment** |
| | Steps | Murex Actions | RATAN Actions & Checking | RATAN Testing Restult |
| | Trade Booking | 1. Book NDS CCS USD(floating) VS COP(Floating) T1 with entity as AG/UK/CN/SG/IN/MY | | |
| | Floating leg payment(CLP) generation | 1. Generate floaging leg payment p1 with CCY==COP on VD-2 | | |
| | Floating leg payment(USD) generation & send to RATAN | 1. Generate floating leg payment p2 with CCY==USD & typology==NDS & NID=T1 on VD-2 2. Send p2 to RATAN by batch file on VD-2 | p2 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-1 2. p3 in COP to offset p1, p4 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p4 to RATAN | Publish p4 to RATAN by realtime workflow on VD-1 | p4 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) 2. p4(typology == NDS Fixing, NID == T1) |
| | Non Eco C&R | 1.Murex trade id changed from T1 to T2 on VD-1 2. No change on underlying payment, just trade ref refresh | | |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-1 2. p5 in COP to offset p1, p6 in USD(Typology == NDS Fixing, NID=T2) | | |
| | Murex publish p6 to RATAN | Publish p6 to RATAN by real time workflow | p6 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING'. P6 is duplicate payement. | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) 2. p4(typology == NDS Fixing, NID == T1) 3. p6(typology == NDS Fixing, NID == T2) |
| | RATAN auto net p2, p4 | | RATAN auto net p2, p4 to N1 | 1. p2(typology == NDS, NID == T1) - NETTED 2. p4(typology == NDS Fixing, NID == T1) - NETTED 3. N1 - WAITING/Pending Exception 4. p6(typology == NDS Fixing, NID == T2) - WAITING |
| 20 | **NDIRS & MO manually booked wrong additional FXD book** |
| | Steps | Murex Actions | RATAN Checking | RATAN Testing Restult |
| | Trade Booking | 1. Book ND IRS trade(Fix VS Floating) T1 with entity as AG/UK/CN/SG/IN/MY, CCY as CNY | | |
| | Interest rate payment generation | 1. Generate fix leg payment p1 in CNY on VD-2 2. Peform fixing event on floating leg, p1 moved to cancelled & generate p2 in CNY ( netted amount between fix leg & floating leg) on VD-2 | | |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-2 2. p3 in CNY to offset p2, p4 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p4 to RATAN | Publish p4 to RATAN by batch file on VD-2 | p4 is STP in Ratan | |
| | MO wrongly manually book anohter NDS Fixing | 1. MO manually book the FXD trade on VD-2 2. p5 in CNY to offset p2, p6 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p6 to RATAN | Publish p6 to RATAN by batch file on VD-2 | p6 is STP in Ratan, but it's duplicate payment | |
| 21 | **NDS & MO manually booked wrong additional FXD book** |
| | Steps | Murex Actions | RATAN Actions & Checking | RATAN Testing Restult |
| | Trade Booking | 1. Book NDS CCS USD(floating) VS COP(Floating) T1 with entity as AG/UK/CN/SG/IN/MY | | |
| | Floating leg payment(CLP) generation | 1. Generate floaging leg payment p1 with CCY==CLP on VD-2 | | |
| | Floating leg payment(USD) generation & send to RATAN | 1. Generate floating leg payment p2 with CCY==USD & typology==NDS & NID=T1 on VD-2 2. Send p2 to RATAN by batch file on VD-2 | p2 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-1 2. p3 in COP to offset p1, p4 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p4 to RATAN | Publish p4 to RATAN by realtime workflow on VD-1 | p4 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) 2. p4(typology == NDS Fixing, NID == T1) |
| | Non Eco C&R | 1.Murex trade id changed from T1 to T2 on VD-1 2. No change on underlying payment, just trade ref refresh | | |
| | MO wrongly manually book another NDS Fixing | 1. Run NDS Fixing job to book the FXD trade on VD-1 2. p5 in COP to offset p1, p6 in USD(Typology == NDS Fixing, NID=T2) | | |
| | Murex publish p6 to RATAN | Publish p6 to RATAN by real time workflow | p6 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) 2. p4(typology == NDS Fixing, NID == T1) 3. p6(typology == NDS Fixing, NID == T1) |
| | RATAN Auto Net p2, p4,p6 | | RATAN auto netted p2, p4, p6 to N1 | N1 in NSTP Exception with the wrong amount from p2, p4, p6. p6 is the duplicate payment |
| 22 | **NDS CCS USD(Floating) VS CLP(Floating) + C&R - Duplicate FXD** |
| | Steps | Murex Actions | RATAN Actions & Checking | RATAN Testing Restult |
| | Trade Booking | 1. Book NDS CCS USD(floating) VS CLP(Floating) T1 with entity as AG/UK/CN/SG/IN/MY | | |
| | Floating leg payment(CLP) generation | 1. Generate floaging leg payment p1 with CCY==CLP on VD-2 | | |
| | Floating leg payment(USD) generation & send to RATAN | 1. Generate floating leg payment p2 with CCY==USD & typology==NDS & NID=T1 on VD-2 2. Send p2 to RATAN by batch file on VD-2 | p2 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade FT1 on VD-1 2. p3 in CLP to offset p1, p4 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p4 to RATAN | Publish p4 to RATAN by realtime workflow on VD-1 | p4 hold as NSTP exception 'Pending NDS Netting' in RATAN, cashflow main status is 'WAITING' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) 2. p4(typology == NDS Fixing, NID == T1) |
| | C&R update notional in Murex 2.11 | 1.Murex trade id changed from T1 to T2 on VD-1 2. p5 generated in USD to reverse p2, p6 generated as rebook of p2. p5 & P6 are in USD & typology == NDS && NID == T2 3. p1 is cancelled and p8 generated as rebook of p1. | | |
| | Murex publish p5 & p6 to RATAN | Publish p5 & p6 to RATAN by real time workflow | 1. p2(USD) is cancelled by p5, p6 hold as 'Pending NDS Netting'( NID== T2) | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) - Cancelled 2. p4(typology == NDS Fixing, NID == T1) 3. p6(typology == NDS, NID== T2) |
| | NDS Fixing amount will be manually amended correspondingly | 1. FXD will be amended for p3 & p4. 2. 3 payments generated from the amendment, p3 is cancelled & p10 generated as rebook of p3. P11(USD) to reverse p4 & p12 to generated as rebook of P4. Typology==NDS Fixing & NID == T2 | | |
| | Murex publish p11 & p12 to RATAN | Publish p11 & p12 to RATAN by real time workflow | p12 in NSTP exception 'Pending NDS Netting' | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) - Cancelled 2. p4(typology == NDS Fixing, NID == T1) - Cancelled 3. p6(typology == NDS, NID== T2) 4. p12(typology == NDS Fixing, NID==T2) |
| | NDS Fixing | 1. Murex Run NDS Fixing job, additional FXD FT2 booked from p8 2. p15 in CLP to offset p8, p16 in USD (Typology == NDS Fixing, NID=T2) | | |
| | Murex publish p14 & p16 to RATAN | Publish p16 to RATAN by real time workflow | p16 in NSTP exception 'Pending NDS Netting' as duplicate | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) - Cancelled 2. p4(typology == NDS Fixing, NID == T1) - Cancelled 3. p6(typology == NDS, NID== T2) 4. p12(typology == NDS Fixing, NID==T2) 5. p16(typology == NDS Fixing, NID==T2) |
| | Auto Netting | | p6,p12,p16 auto netted to N1 with NID==T2 | Pending NDS Netting' cashflows 1. p2(typology == NDS, NID == T1) - Cancelled 2. p4(typology == NDS Fixing, NID == T1) - Cancelled 3. p6(typology == NDS, NID== T2) 4. p12(typology == NDS Fixing, NID==T2) 5. p16(typology == NDS Fixing, NID==T2) |
| 23 | **NDIRS + C&R - Duplicate FXD** |
| | Steps | Murex Actions | RATAN Checking | RATAN Testing Restult |
| | Trade Booking | 1. Book ND IRS trade(Fix VS Floating) T1 with entity as AG/UK/CN/SG/IN/MY, CCY as CNY | | |
| | Interest rate payment generation | 1. Generate fix leg payment p1 in CNY on VD-2 2. Peform fixing event on floating leg, p1 moved to cancelled & generate p2 in CNY ( netted amount between fix leg & floating leg) on VD-2 | | |
| | NDS Fixing | 1. Run NDS Fixing job to book the FXD trade FT1 on VD-2 2. p3 in CNY to offset p2, p4 in USD(Typology == NDS Fixing, NID=T1) | | |
| | Publish p4 to RATAN | Publish p4 to RATAN by batch file on VD-2 | p4 is STP in Ratan | 1. p4(typology == NDIRS, NID == T1) - Released |
| | C&R update notional in Murex 2.11 | 1.Murex trade id changed from T1 to T2 on VD-1 2. p2 is cancelled, p6 generated in CNY as rebook of p2. typology == NDIRS && NID == T2 | | |
| | NDS Fixing amount will be manually amended correspondingly | 1. FXD will be amended FT1 for p3 & p4. 2. 3 payments generated from the amendment, p3 is cancelled & p10 generated as rebook of p3. 3. p11(USD) to reverse p4 & p12 generated as rebook of p4 Typology==NDS Fixing & NID == T2 | | |
| | Murex publish p11 & p12 to RATAN | Publish p11 & p12 to RATAN by real time workflow | p11 & p12 is NSTP in Ratan as 'Reversal' and 'Rebook' | 1. p4(typology == NDS Fixing, NID == T1) - Released 2. p11(typology == NDS Fixing, NID==T2) - Released -P4 Withdrawal 3. p12(typology == NDS Fixing, NID==T2) - Released |
| | NDS Fixing | 1. Murex Run NDS Fixing job, additional FXD FT2 booked from p8 2. p15 in USD to offset p6, p16 in USD (Typology == NDS Fixing, NID=T2) | | |
| | Murex publish p14 & p16 to RATAN | Publish p16 to RATAN by real time workflow | p16 in STPed as duplicate | 1. p4(typology == NDS Fixing, NID == T1) - Released 2. p11(typology == NDS Fixing, NID==T2) - Waiting -p4 Withdrawal 3. p12(typology == NDS Fixing, NID==T2) - Waiting 4. p16(typology == NDS Fixing, NID==T2) - Released |

# Test Case

📎 [NDS Auto Netting test cases 2024_10_23.xlsx](attachments/NDS Auto Netting test cases 2024_10_23.xlsx)