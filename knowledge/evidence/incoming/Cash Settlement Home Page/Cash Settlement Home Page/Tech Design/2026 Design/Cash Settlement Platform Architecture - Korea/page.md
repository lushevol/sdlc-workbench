# **[N](https://confluence.global.standardchartered.com/display/FMRP/KR%3A+Trade+Settlement)ew Flow**

**EXPAND: Current Flow**

**EXPAND_END**

# **Data flow allocation**

| | Sett Means | Sett Account | Cashflow Status Post Cutoff | Payment Type | Currency | Payment Process | Accounting | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NOS | CCY MAIN | Released/Settled | External Client | FCY | SWIFT into ENISIS | Accounting entry into OLTP | |
| 2 | NOS | CCY KEBSEO | Released/Settled | External Client | FCY | SWIFT into ENISIS | Accounting entry into OLTP | |
| 3 | NOS | CCY WRBSEO | Released/Settled | External Client | FCY | SWIFT into ENISIS | Accounting entry into OLTP | |
| 4 | NOX | CCY UISUS | Released | Internal Movement, 1. credit funds to another branch account hold in SCBK 2. credit funds to client account hold in SCBK 3. Interbank Remittance Network | KRW & FCY | Ratan->TIS->UI(OLTP) | Accounting entry will not flow into OLTP | |
| 5 | NOX | CCY UIBOK | Released | BOK-Wire | KRW | Ratan->TIS->UI(OLTP) | Accounting entry into OLTP | BOK related payment can't directly debit on suspend account. It will directly debit on nostro account, so accounting entry will be required. |
| 6 | NOX | CCY UIDD | Released | Internal Movement, 1. debit funds to another branch account hold in SCBK 2. debit funds to client account hold in SCBK | KRW & FCY | Ratan->TIS->UI(OLTP) | Accounting entry will not flow into OLTP | |
| 7 | NOX | KRO BOKSEO | Released | Client is Bank, through BOK wire | KRW | User will manually query in SSDR, then manually upload into OLTP | Accounting entry into OLTP | Daily volume around 20-30, so user prefer bulk upload directly into OLTP. Accounting behavior same with UIBOK |

# **Open Points**

| ** ** | **Current State** | **Expectation** |
| --- | --- | --- |
| **Trade Confirmation Flow** | 1. MXG KR will only sync trade VALD to MXG GDC 2. UDF field update for Affirmation: MO manual upload to MXG KR via a spreadsheet 3. COMP status: MO manually change one by one 4. Payments in MXG KR post the upload would be STP, ~ 70% | 1. Trade confirmation need to be synced from MXG KR to MXG GDC/TDS3, otherwise no payment will be STP, they will be pending affirmation 2. Current situation: 1. 90% are internal, which can bypass the trade confirmation check 2. 5% are MW 2 sided trade, which confirmed already by broker, can also bypass the confirmation check. However Murex should provide the flag 3. 5% are CORP and FI, which should be NSTP based on the existing rule 3. Potential solution: 1. CDUPS integration might be required for auto confirmation & MXG KR sync the confirmation status to TDS, although now it is manual 2. Give up the confirmation control, perhaps only CORP and FI clients to be NSTP, as Ji Hoon mentioned as the above current situation |
| **OLTP integration** | 1. MXG -> IFOS -> OLTP via batch 2. Manually key in | Ratan <-> KR Solace <-> KR EDMI <-> OLTP Risk: 1. Eventually Yeon Su found that Vendor process to cover the development. Expectation would be below for OLTP: 1. Ratan publish accounting in real time 2. OLTP process accounting and process to FX DB 3. OLTP respond ACK/NACK in real time 4. OLTP follow existing processes for downstream, including PSGL/IFOS 5. OLTP to handle the KRW payments: 1. Build the STP process 2. Or suppress in Ratan, and manually key in OLTP |
| **Murex KR Integration** | NA | Assume Murex KR will replicate the global model, Ratan to process 2 Murex stream Trade id & cashflow id overlap? |
| **SWIFT integration/customization** | MXG -> RATAN -> Enisis -> SAA(SOAP) -> Swift network | MXG -> RATAN -> FMSGW -> SAA, If any customization required: 1. MT210 2. Portfolio level nostro stamping |
| **Tech Integration** | NA | 1. New Korea MQ pair: RATAN ↔ Murex KR 2. New Korea Solace Topic/queue pair 1. RATAN ↔ OLTP 2. RATAN ↔ FMSGW 3. FMSGW ↔ SAA, Expected protocol is SOAP, which may will be a potential risk, IBMMQ might be an alternative solution. |
| **Tactical API for TLM** | NA | Propose an API for tactical solution |

# **Reference**

[KR: Trade Settlement - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/KR%3A+Trade+Settlement)

[Cash Settlements - 2026 - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Cash+Settlements+-+2026)

[RATAN -Integration Points - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/RATAN+-Integration+Points)

[Cash Settlements Migration - Korea - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Cash+Settlements+Migration+-+Korea)

# **Timeline**

| | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Analysis | | | | | | | | | | | | |
| Development | | | | | | | | | | | | |
| SIT | | | | | | | | | | | | |
| UAT | | | | | | | | | | | | |
| CPT | | | | | | | | | | | | |
| Go Live | | | | | | | | | | | | |
| Post Care & BAU | | | | | | | | | | | | |

# **Contact**

| System | Dev SPOC | PSS SPOC | |
| --- | --- | --- | --- |
| Murex Korea | Eric | Yeon Su Terry | |
| Ratan | Geoffrey | Jane | |
| IFOS OLTP | 박주호(Park, Joo Ho) (Finance) 김주만(Kim, Joo Man) <JooMan.Kim@[sc.com](http://sc.com)> (Finance) | 박주호(Park, Joo Ho) | |
| EDMI/Solace | 이화영(Lee, Hwa Young) | 이화영(Lee, Hwa Young) | |
| SAA | 양중모(Yang, Jung Mo) | 양중모(Yang, Jung Mo) | |
| Enisis | 박정현(Park, Jung Hyeon) | 박정현(Park, Jung Hyeon) | ENISIS IP PROD : vip : 10.61.128.71 PROD #1 : 10.61.128.72 PROD #2 : 10.61.128.73 TEST : 10.61.17.228 |
| | | | |
| | | | |