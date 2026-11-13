## Murex market operation scenario breakdown

| **Sno** | **Type** | **Market Operation** | **Market Operation Volume** (Based on totally **53875 **Trades containing CN Day1 Ratan Eligible payment, with VD>=12-JUL-2022, out of which **33%** ie.**17693 **trades were performed Market operation) | **Market Operation Impact** | **Highlight points to RATAN usage** | **Documents with samples** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Market Operation Scenarios | **Cancel&Reissue (RPL_M) ** **Restructure (RPL) ** **EXPAND: breakdown scenarios** RPL_M and RPL could amend trade including but not limited to below attributes. Here just list for CN day1 scope the key attributes being amended. 1. Economic - Rate (trade level) 2. Economic - Notional 3. Economic - Margin ( on floating leg) 4. Schecule - Expire Date 5. Schecule - Generator(Index,Schdule) 6. Schecule - Start Date 7. Static - Portfolio 1) post within same entity 2) post in different entity 8. Static - Counterpart 9. Static - SI 10. Other - UDF **EXPAND_END** | Count of mktops RPL_M is **8701**, which is **49**% against **17693 **trades performed mktops. **EXPAND: breakdown distribution** one RPL_M could impact multiple trade attributes, below is distribution of how may RPL_M impact key attributes. 1. Ecnomic - Rate (trade level) - 3.48% 2. Ecnomic - Notional -3.05% 3. Ecnomic - Margin ( on floating leg) -0.53% 4. Schecule - Expire Date -1.87% 5. Schecule - Generator(Index,Schdule) -7.44% 6. Schecule - Start Date -0.53% 7. Static - Portfolio - 78.38% (high volume due to China HO project) 1) post within same entity -19.93% 2) post in different entity -58.45% 8. Static - Counterpart - 1.2% 9. Static - SI - 63.79% (high volume due to China HO project) 10. Other - UDF (count not assessable) **EXPAND_END** Count of mktops RPL is **923**, which is **5**% against **17693 **trades performed mktops. **EXPAND: breakdown distribution** one RPL could impact multiple trade attributes, below is distribution of how may RPL impact key attributes. 1. Ecnomic - Rate (trade level) - 0.65% 2. Ecnomic - Notional -63.38% (most cases) 3. Ecnomic - Margin ( on floating leg) -0% 4. Schecule - Expire Date -1.19% 5. Schecule - Generator(Index,Schdule) -13.98% 6. Schecule - Start Date -0% 7. Static - Portfolio - 6.28% 1) post within same entity -0% 2) post in different entity -6.28% 8. Static - Counterpart - 6.28% 9. Static - SI - 14.08% 10. Other - UDF (count not assessable) **EXPAND_END** | 1. Cancel&Reissue (RPL_M) and Restructure (RPL) may or may NOT impact payment depends on the attributes being amended, those attributes #1~#10 are the most cases impact payemnt for CN day1 scope. 2. RPL_M and RPL amendment could happen on trade level or cashflow level. Trade level amendment impact all trade belonging payment. Cashflow level amendment impact the one cashflow only. 3. RPL(Restructure) normally impact future cashflow only. Special case is RPL amend portfolio, if post portfolio on different entity from pre, RPL will impact past cash. 4. Currently in murex RPL_M and RPL will CNCL original and generate 'new' for INIT payment. Will generate reverse and new for SENT pyament 5. post migration,RATAN eligible payment will be in SNTR, RPL_M and RPL will generate 'reverse' and 'new' for SNTR payment. Post migration value date beyond 7 BD payment will keep in murex in INIT,RPL_M and RPL will CNCL original and generate new. 6. Currently murex BAU process could STP settle reversal payment only if original payment is SENT(assume other STP rule is not breached), Otherwise will NSTP reversal with REASON as 'REV' 7. 'Reverse' and 'new' may not be generated at same time, in the case of 're-fixing', the re-fixing cashflow could be generated some hours or even some days later than 'reverse' 8. Currently in murex IRS net fixed and floating leg into one payment for settlement. post migration, murex will send netted payment to Ratan, subsequent RPL_M and RPL will generate reverse of the netted flow, meanwhile depends on whether floating leg perform fixing on fixing date or not - If floating leg already performed fixing on fixing date, then generate 'new' with netted amount of 2 legs - Otherwise generate 'new' for fixed leg, which to be again netted with floating leg once re-fixing on floating leg. 9. when RPL and RPL_M change portfolio, if post portfolio with different entity as pre, then generate reverse and new. if post portfolio with same entity as pre, then won't generate reverse and new, but update portfolio and TRN_REF on existing original flow. | RPL Generic-3 sheet demonstrate period N+1 fixing could happen in prior to period N LAST_MKTOP will be PRL/RPL_M | **RATAN MIGRAION DOC**<u>** **</u> **RATAN TEMPLATING** [RATAN-14373](https://jira.global.standardchartered.com/browse/RATAN-14373) **MUREX BEHAVIOR DOC** |
| 3 | Market Operation Scenarios | **Modify (MOD) ** **EXPAND: breakdown scenarios** **Ops Modify** Below list the key attributes being impacted by Modify Fixed leg: Rate value maturity date Nominal Trade start date Trade last date generator Portfolio or Counterpart **S&M (may happen on Released pmt)** generator **EXPAND_END** | Count of mktops MOD: 12328 , including Ops Modify and S&M, which is **69**% against **17693 **trades performed mktops. **EXPAND: breakdown distribution** S&M is not assessable, but deduce S&M should take larger proportion of MOD operation. Can only assess count of Ops Modify impacting below key attributes Fixed leg: Rate value 336 maturity date 201 Nominal 132 Trade start date 122 Trade last date 93 generator 81 Portfolio or Counterpart 55 **EXPAND_END** | Two types of MOD >>Ops Modify 1. Modify won't generate new trade, it's like a update on existing trade, so Modify don't make change on Trn reference and last market operation reference. 2.Currently in murex MOD will CNCL original and generate 'new' for INIT payment.This is the most case today for MOD, it's very rare case MOD generate reverse and new today. While post go live RATAN eligible payment will be SNTR in murex, MOD will generate reverse and new in most cases. >>S&M (Scan Modify) 1. In murex can be done by PSS only, it will bypass system rule (like hard blocker) so post go live S&M may produce reverse and new even for RLSR(released in RATAN) payment Refer to one recent production sample (RTRS) in sheet S&M_Reverse that Scan Modify was performed on COMP trade where payment has been SENT. The Scan Modify generated reverse and new Difference between S&M and Modify Modify impact cashflow immediately once Modify action done. however in Scan Modify usually modification happen first (for eg. modify generator index) without any impact on payment unitl S&M procedure is triggered. | MOD don't make change on Trn reference and last market operation reference. MOD will CNCL original and generate 'new' for INIT payment, generate reverse and new for SNTR payment. Attribute 'Action' will be '**MOD**' for the 'new' payment. MOD may happen on COMP (confirmation matched) trade MOD may impact RLSR payment (bypass hard blocker) Currently in murex 99% User modify is on INIT payment which don't generate reverse and new. However post migration original payment will be on SNTR payment thus Modify (as long as it impact payment) will generate reverse and new and send to Ratan | |
| 4 | Market Operation Scenarios | **Cancellation (RPL_DEL) ** | count of mktops RPL_DEL: 608, which is **3**% against **17693 **trades performed mktops. | 1. currently If original payment is SENT, Cancellation (RPL_DEL) will generate reverse for SENT payments. post migration,RATAN eligible payment will be in SNTR, Cancellation will generate reverse for SNTR payment. 2. currently if original payment is INIT, will CNCL it (without reverse). post migration value date beyond 7 BD payment will keep in murex in INIT,Cancellation will CNCL it. (without reverse) | | <u></u> |
| 5 | Market Operation Scenarios | **Removal of Mktops (CNCL) ** **EXPAND: breakdown scenarios** 1.RPL/RPL_M → CNCL 2.XIT →CNCL **EXPAND_END** | count of mktops CNCL: 1812, which is **10**% of **17693 **trades performed mktops. | 1. CNCL will try to revert back those cashflow generated from last Mkt operation, ie. CNCL for INIT payment, generated reverse for SENT payment. 2. if last mktops is RPL/RPL_M which generated new trade, CNCL will physically delete the new trade, and in payment table the payment (generated from CNCL onward) will tag TRN_REF as original number. for eg. A→ RPL_M/RPL→B→CNCL, trade B will be deleted from db and payment generated from CNCL onward will use TRN_REF as A. | The TrnRef, which is the most recent trade number associated with the payment, may go back last version post removal of market operation. for eg. A→ RPL_M/RPL→B→CNCL, trade B will be deleted from db and payment generated from CNCL onward will use TRN_REF as A. | typical case refer to: 86402705_Reverse Cancel Pre migration murex behavior sum up 01 - SENT(SNTR) 02 reverse - INIT 03 new - INT->CNCL **CNCL (remove mktops)** 04 new - replace 01 |
| 6 | Market Operation Scenarios | **Exercise (EXR)** **EXPAND: breakdown scenarios** 1.Settlement method = Cash 2.Settlement method = Deliverable **EXPAND_END** | count of mktops EXR: 674, which is **4**% of **17693 **trades performed mktops. | 1. Exercise will insert new cashflow for cash settled Option 2. Exercise will genreate fx spot for deliverable settled Option 3. EXR no impact on existing payment. 3. For deliverable settled Option which has been genreated fx sopt ticket, the 'Remove Mktops EXR' is disallowed | | <u></u> |
| 7 | Market Operation Scenarios | **NET** **EXPAND: breakdown scenarios** 1. ETD (95% volume) - not in scope as no cashflow 2. Option (Deliverable settled) - NET no impact on existing cashflow. **EXPAND_END** | Descope from analysis as 95% are ETD which has no cashflow. The rest are all Option trade (Deliverable settled),- NET no impact on existing cashflow. | Descope from analysis | | |
| 8 | Market Operation Scenarios | **XIT ** **EXPAND: breakdown scenarios** 1. partial XIT(not valid case) 2. full XIT **EXPAND_END** | count of mktops XIT: 4800, which is **27**% of **17693 **trades performed mktops. **EXPAND: breakdown distribution** 1. partial XIT 0% (not valid case) 2. full XIT 100% **EXPAND_END** | 1.CN don't have partial XIT case 2. XIT don't impact past value date payment 3. Currently For future value date payment in INIT, will CNCL it. Post migration for future payment, if value date within 7BD, payment will be in SNTR, XIT will genreate reverse for SNTR payment. Payment value date beyong 7BD will be in INIT, XIT will CNCL it. | | <u></u> |
| 9 | Market Operation Scenarios | **Fixing** **EXPAND: breakdown scenarios** 1. fixing generate cashflow - analysis covered by RPL 2. re-fixing via market operation - analysis covered by RPL 3. re-fixing via fixing modify - analysis covered by #13-8 4. dummy fixing on fixed leg **EXPAND_END** | | | IRS_CPTY_QTY demonstrate IRS fixed leg may also perform fixing and generate cashflow Action as FIX_DEF | dummy fixing on fixed leg is covered in IRS_CPTY_QTY in |
| 10 | Ad-hoc Scenarios | **IRS FixedFloating Leg cashflow in sequence** **EXPAND: breakdown scenarios** 1. murex generate one payment with netted amount of fixed leg and floating leg. 2. murex generate fixed leg payment in prior to floating leg. Fixed leg payment status keep in INIT due to VD in future till floating leg cashflow generated. 3. murex generate fixed leg payment in prior to floating leg. Fixed leg payment send to Ratan before floating leg generate cashflow **EXPAND_END** | | | | covered in IRS FixFloat in Sequence in <u></u> |
| 11 | Ad-hoc Scenarios | **Additional Flow** **EXPAND: breakdown scenarios** 11.1. Additional flow being added upon market operation 11.1.1) Amendment fee - sample trade 42393800 (remove mktops case) 11.1.2) Termination fee - sample trade 85146698 (customiza caculation start date-> impact VD; customise calculation start and fixing date-> no impact to future cashflow ) 11.2. Additional flow being added upon trade insertion - sample trade 84817757 **EXPAND_END** | | | 11.2_70155924_XITFee demonstrate if CnR amended on cashflow level instead of trade level (for eg. changed VD on one particular cashflow) which impact the one cashflow only, then only the impacted cashflow will generate reverse and new. in this context, the CnR is more like a cashflow customization, not contract cancel&reissue | 11.2 coverred by RPL analysis (port,ctp) 11.1.2 also cover 0,1,2. |
| 12 | Ad-hoc Scenarios | **Amortizaiton** **EXPAND: breakdown scenarios** 1. IRS amortization -Sample trade 84462276 2. CCS amortization - Sample trade 87035450 **EXPAND_END** | | | 12.2_87035450_AmortCCS in CCS amortization scenario - payment will be sum of amortization impacted capital and current period cupon interest. subsequent reversal and new will be based on the sum up value, to Ratan it is transparent | |
| 13 | Ad-hoc Scenarios | **Cashlfow Customization** **EXPAND: breakdown scenarios** China has below types of customization 0-Payment date 1-Fixing date 2-Calculation start date 3-Capital date 5-Interest flow 8-Fixing 34-Capital payment flow (ie.amortization capital flow) 99-Initial Premium payment date 100-End Premium payment date refer to sample trades in 'Customization Breakdown'. **EXPAND_END** | | | 13.3_83494206_C#99#100 This case demonstrate the possibility that Cancel&Reissue impact 2 original cashflow and generate 2 reverse and 4 'new'. Ratan may need to pair 4 new with 2 reverse. 12.2_87035450_AmortCCS is sample for #34 | |
| 14 | Exception Scenarios | **Messge lost** | | | | |

## Murex Global vs. CN Payment STP Ratio

| **Data Set: Payments being STP/NSTP during period 12-JUL-2022 to 11-JUL-2023 (1Y)** |
| --- |
| **Global** | **CN** |
| **/** | **Count of Payments** | **Percentage** | **SUPP&SENT STP Count** | **SUPP&SENT STP Percentage** | **Count of Payments** | **Percentage** | **SUPP&SENT STP Count** | **SUPP&SENT STP Percentage** |
| **STP** | 317188 | **11.16%** | **SUPP : **12129 | 0.43% | 3183 | **7.11%** | **SUPP :**118 | 0.26% |
| **SENT : **305059 | 10.73% | **SENT :**3,065 | 6.84% |
| **NSTP** | 2526235 | **88.84%** | | | **41611** **Download CN NSTP Raw Data:** <u></u> | **92.89%** | | |
| Sum | 2843423 | 100% | | | 44794 | 100% | | |

| **Data Set: Payments excluding SHACLHO/SHA' and being STP/NSTP during period 12-JUL-2022 to 11-JUL-2023 (1Y)** |
| --- |
| **Global** | **CN** |
| **/** | **Count of Payments** | **Percentage** | **SUPP&SENT STP Count** | **SUPP&SENT STP Percentage** | **Count of Payments** | **Percentage** | **SUPP&SENT STP Count** | **SUPP&SENT STP Percentage** |
| **STP** | 317157 | **%** | **SUPP : **12107 | % | 1147 | **9%** | **SUPP :**83 | 0.7% |
| **SENT : **305050 | % | **SENT :**1064 | 8.3% |
| **NSTP** | 1910791 | **%** | | | 11725 | **91%** | | |
| Sum | | 100% | | | 12872 | 100% | | |

Based on above NSTP payments (Global vs. CN payments within 1 year), Below is distribution of times of Reason code being tagged to NSTP payment. (Note: Multiple Reason code could tag to one cashflow).

**Reason Code Dictionary** Refer to : <u>*[CN Settlement - Murex 2.11 Payment Non-STP Exception - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex+2.11+Payment+Non-STP+Exception)*</u>

**EXPAND: Expand for details**

| **Global** | **CN** | **RATAN Handling** |
| --- | --- | --- |
| **NSTP Reason Code** | **Times of Reason code tagged to payment** | **Percentage** | **Times of Reason code tagged to payment** | **Percentage** | **Comment** | Cashflow Migration | CM readiness | CN New Booking / Trade Migration | FMRP Strategic State |
| **NET** | 1217437 | **19.85%** | 21377 | **23.41%** | The payments elligible for counterpart netting must not flow down STP. In order to identify them a configuration table TABLE#LIST#PAYSTP_N_DBF allow to specify the combination of Counterparty, family, group, type, typology and strategy for which Ops may do counterpart netting/CPN and the settlement should therefore not go STP. For CN NSTP payment, **SHACLHO/SHA ** is the only one ctp that payment blocked by NET rule ![image2023-7-28_12-55-11.png](attachments/image2023-7-28_12-55-11.png) | Y | 1. New fields to be added to Ratan cashflow data. | Y | Y |
| **SI** | 713537 | **11.64%** | 3631 | **3.98%** | Missing nostro or vostro SI | Y | Y | Y | Y |
| **CORP** | 712560 | **11.62%** | 26448 | **28.97%** | this exception code is taggeed when counterparty type is non-bank and non-internal. Ctp type identification: Ctp UDF filed M_CTRTY_TYPE One more static table defined STP type for spefic ctp type. (TABLE#LIST#TYPE_CTR_DBF). STP is eligible when STP type is Bank or Internal | Y | Y with SCI client type | Y | Y |
| **SI(MUL)** | 632730 | **10.32%** | 10542 | **11.55%** | If counterparty has multiple si defined in murex, payment STP should not happen, even if the multiple SSI available in the counterparty is not assigned to current payment flow.As long as the key fields match the payment details and the SSI can be selected by system or manually, it will be considered. | Y | Y | Y | Y |
| **LIMIT TYPE** | 573398 | 9.35% | 400 | 0.44% | Payment STP only process cashflow amount (dollar equivalent) below threshold (2 mio by default). Amount above threshold will tag exception code as 'AMOUNT'. Threshold is configrable in static table setup. Pay/Rec limit type set in counterparty udf (field PAY_STP,REC_STP). If ctp limit type is not config-ed as 'limited' or 'unlimited', will tag exception code as 'LIMIT TYPE'. Threshold is setup in TABLE#LIST#PAYTHRES_DBF per limit type. | N | | N | Y |
| **AMOUNT** | 542412 | 8.85% | 76 | 0.08% | N | | N | Y |
| **PROD** | 400179 | 6.53% | 1173 | 1.28% | Define Family, Group, Type, typology, strategy combination for which the STP should not process in UDF table TABLE#LIST#PAY_STPN_DBF **EXPAND: Data of UDF table** | M_FAMILY | M_GROUP | M_STATUS | M_STRATEGY | M_TYPE | **M_TYPOLOGY** | | --- | --- | --- | --- | --- | --- | | IRD | IRS | | | | Structured Swap | | CURR | FXD | | | FXD | 3in1 ver4 | | CURR | FXD | | | FXD | BULLION NETTING | | CURR | FXD | | | FXD | Forward | | CURR | FXD | | | FXD | IDR_DELIVERABLE | | CURR | FXD | | | FXD | PHYS OFFTAKE | | CURR | FXD | | | FXD | PRC_BTB_TRF | | CURR | FXD | | | FXD | PayModeSett | | CURR | FXD | | | FXD | SGE_BILATERAL | | CURR | FXD | | | FXD | - | | COM | FWD | | | | EDHIP_BS | | COM | FWD | | | | Phy_Com | | COM | SWAP | | | | COM_ILLIQUID | | COM | SWAP | | | | EFS | | COM | SWAP | | | | OTC CLEARED | | COM | SWAP | | | | Phy_Com | | COM | SWAP | | | | SIP REPO | | COM | SWAP | | | CLR | | | CRD | CDS | | | | ND CDS | | CRD | CRDIO | | | | | | CRD | RLOAN | | | | | | CRD | RTRS | | | | | | CURR | FXD | | | XSW | SGE_BILATERAL | | CURR | FXD | | | XSW | Spot/Forward | | CURR | FXD | | | XSW | Structured Swap | | CURR | OPT | | | ASN | | | CURR | OPT | | | BAR2 | | | CURR | OPT | | | FLEX | | | CURR | OPT | | | LST | | | CURR | OPT | | | RBT | | | CURR | OPT | | | SMP | COM_DEPO_STRUCT | | CURR | OPT | | | SMP | ND_CCY_DELIVERABLE | | CURR | OPT | | | SMP | PayModeSett | | CURR | OPT | | | SMPS | | | IRD | CF | | | | SCB Issued Note | | IRD | CF | | | | Structured Deposit | | IRD | CF | | | | Structured Swap | | IRD | CS | | | | Cross-Ccy-swaption | | IRD | CS | | | | EquityBuy | | IRD | CS | | | | EquitySell | | IRD | CS | | | | ExtinguishableSwap | | IRD | CS | | | | ExtinguishableSwapND | | IRD | CS | | | | FWD_START_SWAP | | IRD | CS | | | | Mark-to-market | | IRD | CS | | | | SCB Issued Note | | IRD | CS | | | | Structured Deposit | | IRD | CS | | | | Structured Swap | | IRD | IRS | | | | 5 Year & Every 5 Yrs | | IRD | IRS | | | | Amber Trades-IR | | IRD | IRS | | | | Amber Trd-StrucSwap | | IRD | IRS | | | | CMS STEEPENER | | IRD | IRS | | | | Early_Term | | IRD | IRS | | | | EquityBuy | | IRD | IRS | | | | EquitySell | | IRD | IRS | | | | ExtinguishableSwap | | IRD | IRS | | | | MTM Monitoring | | IRD | IRS | | | | NDF | | IRD | IRS | | | | NDIRS | | IRD | IRS | | | | NDS | | IRD | IRS | | | | NEED_LEG_ADJ | | IRD | IRS | | | | NEED_VAL_ADJ | | IRD | IRS | | | | NEED_VALLEG_ADJ | | IRD | IRS | | | | OIS | | IRD | IRS | | | | Red Trades-StrucSwap | | IRD | IRS | | | | RedTrades StrucSwap | | IRD | IRS | | | | RedTrades StructCR | | IRD | IRS | | | | SCB Issued Note | | IRD | IRS | | | | Structured Deposit | | IRD | OPT | | | ORG | | | IRD | OPT | | | OTC | | | IRD | REPO | | | REPO | | | IRD | LN_BR | | | | | | IRD | BOND | | | | | | IRD | CS | | | | NDS | | IRD | CS | | CCS_CORP_DVP | | | | IRD | CS | | CCS_FI_DVP | | | **EXPAND_END** | N | | N | Y (TBC on equivalent) |
| M_FAMILY | M_GROUP | M_STATUS | M_STRATEGY | M_TYPE | **M_TYPOLOGY** |
| IRD | IRS | | | | Structured Swap |
| CURR | FXD | | | FXD | 3in1 ver4 |
| CURR | FXD | | | FXD | BULLION NETTING |
| CURR | FXD | | | FXD | Forward |
| CURR | FXD | | | FXD | IDR_DELIVERABLE |
| CURR | FXD | | | FXD | PHYS OFFTAKE |
| CURR | FXD | | | FXD | PRC_BTB_TRF |
| CURR | FXD | | | FXD | PayModeSett |
| CURR | FXD | | | FXD | SGE_BILATERAL |
| CURR | FXD | | | FXD | - |
| COM | FWD | | | | EDHIP_BS |
| COM | FWD | | | | Phy_Com |
| COM | SWAP | | | | COM_ILLIQUID |
| COM | SWAP | | | | EFS |
| COM | SWAP | | | | OTC CLEARED |
| COM | SWAP | | | | Phy_Com |
| COM | SWAP | | | | SIP REPO |
| COM | SWAP | | | CLR | |
| CRD | CDS | | | | ND CDS |
| CRD | CRDIO | | | | |
| CRD | RLOAN | | | | |
| CRD | RTRS | | | | |
| CURR | FXD | | | XSW | SGE_BILATERAL |
| CURR | FXD | | | XSW | Spot/Forward |
| CURR | FXD | | | XSW | Structured Swap |
| CURR | OPT | | | ASN | |
| CURR | OPT | | | BAR2 | |
| CURR | OPT | | | FLEX | |
| CURR | OPT | | | LST | |
| CURR | OPT | | | RBT | |
| CURR | OPT | | | SMP | COM_DEPO_STRUCT |
| CURR | OPT | | | SMP | ND_CCY_DELIVERABLE |
| CURR | OPT | | | SMP | PayModeSett |
| CURR | OPT | | | SMPS | |
| IRD | CF | | | | SCB Issued Note |
| IRD | CF | | | | Structured Deposit |
| IRD | CF | | | | Structured Swap |
| IRD | CS | | | | Cross-Ccy-swaption |
| IRD | CS | | | | EquityBuy |
| IRD | CS | | | | EquitySell |
| IRD | CS | | | | ExtinguishableSwap |
| IRD | CS | | | | ExtinguishableSwapND |
| IRD | CS | | | | FWD_START_SWAP |
| IRD | CS | | | | Mark-to-market |
| IRD | CS | | | | SCB Issued Note |
| IRD | CS | | | | Structured Deposit |
| IRD | CS | | | | Structured Swap |
| IRD | IRS | | | | 5 Year & Every 5 Yrs |
| IRD | IRS | | | | Amber Trades-IR |
| IRD | IRS | | | | Amber Trd-StrucSwap |
| IRD | IRS | | | | CMS STEEPENER |
| IRD | IRS | | | | Early_Term |
| IRD | IRS | | | | EquityBuy |
| IRD | IRS | | | | EquitySell |
| IRD | IRS | | | | ExtinguishableSwap |
| IRD | IRS | | | | MTM Monitoring |
| IRD | IRS | | | | NDF |
| IRD | IRS | | | | NDIRS |
| IRD | IRS | | | | NDS |
| IRD | IRS | | | | NEED_LEG_ADJ |
| IRD | IRS | | | | NEED_VAL_ADJ |
| IRD | IRS | | | | NEED_VALLEG_ADJ |
| IRD | IRS | | | | OIS |
| IRD | IRS | | | | Red Trades-StrucSwap |
| IRD | IRS | | | | RedTrades StrucSwap |
| IRD | IRS | | | | RedTrades StructCR |
| IRD | IRS | | | | SCB Issued Note |
| IRD | IRS | | | | Structured Deposit |
| IRD | OPT | | | ORG | |
| IRD | OPT | | | OTC | |
| IRD | REPO | | | REPO | |
| IRD | LN_BR | | | | |
| IRD | BOND | | | | |
| IRD | CS | | | | NDS |
| IRD | CS | | CCS_CORP_DVP | | |
| IRD | CS | | CCS_FI_DVP | | |
| **CP_EXCL** | 302532 | 4.93% | 1660 | 1.82% | For Fx precious metal trade, define counterparts for which the STP should not process in static table. Counterparty list defined in PAYSTP_EXCP_DBF table. | N | | N | Y |
| **CURR** | 299922 | 4.89% | Data Not Found | | define currency which is eligible to STP or not in static table Ccy eligibility identification: Currency UDF filed TABLE#DATA#CURRENCY_DBF.M_PAYSTP | N | | N | Y |
| **FIXING** | 171617 | 2.79% | 13808 | **15.12%** | If fixed cashflow has a respective cashflow from estimated floating cashflow, cashflow will be excluded from STP with exception code 'FIXING' (Fixed leg should not be STP-ed, but wait for floating leg and perform NET before settlement.) | Y (for IRS alone) | Function built, but a few items still open | Y (for IRS alone) | Y (for IRS alone) |
| **STRAT** | 151182 | 2.47% | 7002 | **7.67%** | Define strategys which is eligible for payment STP in static table TABLE#LIST#PAY_STRA_DBF | N | | N | Y (TBC on equivalent) |
| **ENTITY** | 87320 | 1.42% | 1858 | 2.03% | For internal trade(ie. Trade booked with ctp type is 'Internal'), the related payments can be STPed only if both entities have a payment module. static table TABLE#LIST#PAYSTP_M_DBF setup for entities that payment mode is enabled. | N | | N | N |
| **INTER NET** | 62854 | 1.02% | Data Not Found | | Murex perfrom auto netting for internal entity cashflow for which the STP should not process. There is static table defined entity&ctp used for checking auto netting eligibility. China entity is not applied. | N | | N | Y |
| **MOP** | 41056 | 0.67% | 2442 | 2.67% | If cashflow is gnereated from market operation (CnR, Restructure, Exercise, Early termination), MOP was not validated or was done within last 7 days should not STP payment | N | | N | N |
| **NDS** | 39593 | 0.65% | 60 | 0.07% | If casfflow is generated from NDS fixing, and ccy is non-deliverable, should be excluded from payment STP. NDS fixing cashflow Iendification: typology='NDS Fixing' and Strategy='FEDSVALIDATOR' and TABLE#DATA#PAYFLOW_DBF.M_NID >0 | N | | N | N |
| **CROSS-NET** | 37389 | 0.61% | Data Not Found | | this excepton code is tagged when cashflow got Netted by payment 'NDS Invoicing (NINV)' or 'INTER ENTITY NET (ICIV)' payment queue INTER ENTITY NET is not China related, it is used for internal entity netting. (ctp+entity static table based) NDS Invoicing is used by China entity to do Cross Netting for products between NDS and FXD out of NDS fixing | N | | N | Y |
| **STP_HOLD** | 34568 | 0.56% | Data Not Found | | Hold the payments if entry match with STP_HOLD UDT. TABLE#LIST#STP_HOLD_DBF config combination of Entity + ctp+ + family+ group+ type+ typo + currency + strategy + pay/rec | N | | N | Y |
| **S&M** | 15776 | 0.26% | 24 | 0.03% | Scan&Modify was performed on trade and impacting this cashflow | N | | N | N |
| **REV** | 15203 | 0.25% | 68 | 0.07% | this exception code is tagged when cashflow is a reversal flow, but original flow has NOT been settled (status<>SENT), or market operation is has not validated. | N | | N | N |
| **XIT** | 10067 | 0.16% | 278 | 0.30% | this exception indicate flow from Simple option deal is NOT from premium. Only Premium for CURR OPT SMP to be STP-ed. | N | | N | N |
| **SI(AWI)** | 5610 | 0.09% | Data Not Found | | if cashflow vostro field 57 (Account With Institution) is not given, payment STP should not happen | N | | N | N |
| **PX_CAP** | 124 | 0.00% | 2 | 0.00% | This Rule check for Conservative trades. STP don't process conservative trades. conservative trades identification: if trade UDF filed M_PRICE_CAP is not null, then trade is conservative trade. For CN NSTP payment, found 2 payments hit PX_CAP **EXPAND: trade/payment detail** ![image2023-7-28_12-48-32.png](attachments/image2023-7-28_12-48-32.png) **EXPAND_END** | N | | N | TBC |
| **LIEN** | 112 | 0.00% | Data Not Found | | Check for Lien trades. STP don't process Lien trade. Lien trade identification: Trade UDF field M_LIEN_MONIT = N or null | N | | N | Y |
| **CLEARING STATUS** | 28 | 0.00% | Data Not Found | | for IRD trades sourced from Markitware/Eclipse and yet to be clearing-ed, correspoding cashflow should be excluded from STP | N | | N | Y |
| SUM | 6132359 | 100% | 91307 | 100.00% | | 67% | | 43% | 64% |

**EXPAND_END**

## Murex Global **Reversal **Payment STP Ratio

| **Data Set: Payments performed STP/NSTP during period 12-JUL-2022 to 11-JUL-2023 (1Y), and as reversal payment** |
| --- |
| **/** | **Count of Payments** | **Percentage** | **SUPP&SENT STP Count** | **SUPP&SENT STP Percentage** |
| **STP** | 343 | **2.26%** | **SUPP : **0 | 0% |
| **SENT : **343 | **2.26%** |
| **NSTP** | 14827 | **97.74%** | | |
| Sum | 15170 | 100% | | |

Based on above NSTP reversal payments (totally 15170 payments within 1 year), Below is distinct of 'NSTP Reason' column tagged on NSTP reversal payments. (Note: Multiple Reason code could tag to one cashflow).

Refer to Reason Code dictionary: <u>*[CN Settlement - Murex 2.11 Payment Non-STP Exception - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex+2.11+Payment+Non-STP+Exception)*</u>

**EXPAND: Expand for details**

| **Distinct of 'Reason' column** | **Count** | **Percentage** |
| --- | --- | --- |
| REV | 13386 | **90.28%** |
| REV;FIXING; | 1154 | **7.78%** |
| NO ERROR (payment was NSTP somehow rule was not explicitly recognized. ) | 232 | 1.56% |
| FIXING | 55 | 0.37% |
| SUM | 14827 | 100% |

**EXPAND_END**

## Murex XML attribute to Ratan

| ***Label*** | ***Desc*** | ***Xpath*** |
| --- | --- | --- |
| **Flow id** | murex flow id | /MxPayML/flowID |
| **Action** | FIX_DEF means payment is fixing related. Fixing related payment may also have this field as ‘INS’ (good find from Garvey that if floating payment is eventually trigger by PAY FIX then Action value as INS) 'Action’ value on reverse should be same as original payment. but 'new' might be different from 'original'. if 'new' generated from Modify operation, Action value is 'MOD' Fixed leg may also perform fixing and generate cashflow Action=FIX_DEF for eg. trade 85506175 92537548 original, Action=INS 93385066 Reverse of 92537548,Action=INS 93385067 new genreated by refixing,Action=FIX_DEF | /MxPayML/scbExtraInfoBlock/action |
| **Trade Last Operation** | belonging trade come from which market operation. Noted 'Modify' (MOD) is NOT defined as market operation in murex hence if a trade got MOD, this field won't make any change. Noted 'Removal of Mktops' (CNCL) is NOT defined as market operation in murex hence if a trade got RPL_DEL, this field won't make any change. | k/MxPayML/scbExtraInfoBlock/tradeLastMKT |
| **TrnRef** | the most recent trade number associated with the payment it's not solid value but changed following latest trade number for example trade 60951119 produced flowid 69883981, with TrnRef=60951119 on Day1: 60951119 ->CnR->69300532, CnR did no impact on flowid 69883981, TrnRef changed to 69300532 on Day2: 69300532 -> CnR -> 69690000, generate reverse and new on flowid 69883981, TrnRef changed to 69690000 | /MxPayML/transactionID |
| **TrnID** | the trade number the payment was originally created off of for example trade 60951119 produced flowid 69883981, with TrnID=60951119 on Day1: 60951119 ->CnR->69300532, but CnR did no impact on flowid 69883981, now TrnID=60951119 on Day2: 69300532 -> CnR -> 69690000, generate reverse and new on flowid 69883981, now it is 69883981, original, TrnID=60951119 72732655 ,Reverse of flow 69883981, TrnID=60951119 72732657 ,new, TrnID=69690000 | /MxPayML/transactionOriginID |
| **TrnParentID** | the creator trade number of current trade. if trade don't have creator then value is 0 For example A->B->C, from B perspective, TrnParentID=A from C perspective, TrnParentID=B | /MxPayML/scbExtraInfoBlock/TrnParentID |
| **TrnOriginalID** | the RPL original trade number of current trade. if trade has not got RPL, then value is 0 For example A->B->C, from B and C perspective, TrnOriginalID=A | /MxPayML/scbExtraInfoBlock/TrnOrginalID |
| **Comment** | value as 'Reverse of flow' for reverse flow for new flow it will be blank | /MxPayML/comment |
| **CpuDate** | system date that cashflow persist to murex db | /MxPayML/computerDate |
| **CpuTime** | system time that cashflow persist to murex db | /MxPayML/computerTime |
| **Mx payment snapshot** | Snapshot of payments under belonging trade at the moment of this tag being enriched into murex xml. Array data type contains multiple attribute: Flowid - murex flow ids status - SNTR, RLSR indicate cashflow suppose to send to Ratan. value_date - value date of respective payment | /MxPayML/scbExtraInfoBlock/Flows/flow |