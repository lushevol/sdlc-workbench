**EXPAND: Document Info**

## Document Information

| Release | Aug-26 |
| --- | --- |
| **Status** | |
| **Date Last Edited** | 2026-07-28 |
| **Author** | Song, Yinghua |

### Consulted with

| Name | Role |
| --- | --- |
| Dinesh, Arockia | PO |
| Cao, Geoffrey Ruiheng | Dev leader |
| Yang, Ji Hoon | Ops leader |
| RATAN DEV Team & QA Team | |

### PT Plan

1. Prepare 3 dump in Murex Korea. 15-June EOD dump; 16-June EOD dump; 18-June EOD dump.
2. Push the first dump data, recon, analysis and process it, run auto-netting job, reprocess 'waiting' cashflows, compare swift messages for VD17 payments.
3. Push the second dump data, recon, analysis and process it, run auto-netting job, reprocess 'waiting' cashflows, compare swift messages for VD18 payments.
4. Push the third dump data, recon, analysis and process it, run auto-netting job, reprocess 'waiting' cashflows, compare swift messages for VD22 payments.

### Sign-Off

| Test | Signoff |
| --- | --- |
| Yang, Ji Hoon | |
| Cao, Geoffrey Ruiheng | |

**EXPAND_END**

**EXPAND: Performance Testing Overview**

### Performance Data Preparation

| | Dump date in Murex Korea | Value date Scope | Key value day | Batch Volume | Key day volume | SWIFT volume | Start Time | End Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Batch1 | 15-June-2026 | 12-June-2026 to 24-June-2026 | 17-June-2026 | 6000+ | 2300+ | 1001 | Batch1: 2026-07-14 02:07:30.496767 Batch2: 2026-07-17 01:28:13.404785 | Batch1: 2026-07-14 08:14:11.418731 Batch2: 2026-07-17 08:23:44.70244 |
| Batch2 | 16-June-2026 | 13-June-2026 to 25-June-2026 | 18-June-2026 | 2000+ | 2300+ | 1061 | 2026-07-22 01:54:35.073492 | 2026-07-22 05:58:13.727789 |
| Batch3 | 18-June-2026 | 17-June-2026 to 29-June-2026 | 22-June-2026 | 5000+ | 4800+ | 2322 | 2026-07-24 01:16:44.050978 | 2026-07-24 11:08:12.524929 |

As payments need to be process manually in Murex Korea testing environment, total duration will be longer than actual duration. Average time is 10 cashflows/minutes.

### Pre-auto-netting-process

| Cashflow Status | Result | Reason | |
| --- | --- | --- | --- |
| CASHFLOW_SUPPRESSED | PASS | Suppress by Murex 2.11 label | ![image-2026-7-28_9-33-11.png](attachments/image-2026-7-28_9-33-11.png) |
| WAITING(Pending Exception) | PASS | NSTP rule 1. KR Typology check 2. KR FI Client Check 3. KR LNBR 4. DVP Strategy 5. Missing Vostro 6. Missing Nostro 7. Multi Vostro | |
| WAITING(Pending Another Leg) | PASS | Pending Fixing Flag=Y | ![image-2026-7-28_9-38-40.png](attachments/image-2026-7-28_9-38-40.png) |
| WAITING(Pending Auto Netting) | PASS | KR KRX/SEL auto netting KR SCB/LDN NDF auto netting KR SCB/LDN Commodity NDS Auto Netting | |

### Auto-netting process

Run auto netting job.

| | Netting type | Result |
| --- | --- | --- |
| 1 | KR KRX/SEL auto netting | Netted resultant cashflow & single resultant cashflow will trigger 'Auto Netting' Exception Resultant cashflow will be suppressed if amount=0 |
| 2 | KR SCB/LDN NDF auto netting | Netted resultant cashflow & single resultant cashflow will trigger 'Auto Netting' Exception Resultant cashflow will be suppressed if amount=0 |
| 3 | KR SCB/LDN Commodity NDF auto netting | Netted resultant cashflow & single resultant cashflow will trigger 'Auto Netting' Exception Resultant cashflow will be suppressed if amount=0 |
| 4 | NDS Auto Netting | Netted resultant cashflow & single resultant cashflow will trigger 'Auto Netting' Exception Resultant cashflow will be suppressed if amount=0 |

### Post-auto-netting-process

After auto netting job done, need to process new net resultant cashflow and single resultant cashflow.

### Swift Comparison Result

| **1001** | **VD=17 in dump 15 data** |
| --- | --- |
| 917 | PASS (SAME FLOW ID) |
| 19 | PASS(DIFF FLOW ID) |
| 4 | DROP(SUPPRESSED IN PROD) |
| 16 | DROP(REVERSAL CASE) |
| 1 | PASS(NET RESULT) |
| 2 | PASS(MT210) |
| 2 | DROP(NETTED IN PROD) |
| 1 | DROP(CANCEL CASE) |
| 26 | PASS(DIFF FLOW ID) |
| 13 | DROP(SUPPRESSED IN PROD) |

| **1061** | **VD=18 in dump 15 and dump 16 data ** |
| --- | --- |
| 1031 | Pass |
| 9 | Pass(diff flow id) |
| 4 | Pass(Net resultant) |
| 11 | Netted in Murex prod |
| 6 | Suppressed in Murex Prod |

| **2322** | **VD=22 ** |
| --- | --- |
| 2316 | Pass |
| 1 | Netted in Murex prod |
| 4 | Suppressed in Murex Prod |

### Open Risks and Issues

| | Description | Reason | Action | Status |
| --- | --- | --- | --- | --- |
| 1 | No related NDS leg in RATAN side when need to test NDS netting | 1. Data is not enough from Murex Korea 2. For SOFR type index, fixing day is one day before value day KOFR KRO KOFR CMP SONIA GBP TONAR JSCC USD SOFR ALM USD SOFR CMP USD SOFR CMP5LB USD SOFR KTB 45 | Recheck in Murex Korea testing environment, and repush related data | Closed |
| 2 | Swift comparison diff ![image-2026-7-28_9-55-17.png](attachments/image-2026-7-28_9-55-17.png) | Vostro info from SSI+ is different with that in Murex Korea. Ratan symbol limitation. | User accept the difference. | Closed |

**EXPAND_END**

**EXPAND: Data Scope & Analysis**

NDS Volume in VD 22-June-2026

| Typology | Volume | ND_Parent Typology | Volume |
| --- | --- | --- | --- |
| NDS Fixing | 4404 | NDIRS | 4395 |
| | | NDS | 5 |
| | | ND-Convert | 4 |
| ND-Convert | 2 | | |

NDS CASE Sample

![image-2026-7-28_10-21-53.png](attachments/image-2026-7-28_10-21-53.png)

| | Counterparties | | FMID | | Currencies | | Typology | | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | |
| [S.no](http://S.no) | Row Labels | Count of M_IDENTITY | | FMID | Count of M_IDENTITY | | Row Labels | Count of M_IDENTITY | | Row Labels | Count of M_IDENTITY | | Row Labels | Count of M_IDENTITY |
| 1 | 3972ANSEONG/SEL | 2 | | 401014360 | 2 | | | 1 | | | 55562 | | CNCL | 8488 |
| 2 | ABU COMMLBK/ABU | 49 | | 400063813 | 49 | | AUD | 60 | | Bond _Forward | 557 | | INIT | 75017 |
| 3 | ADIDASKOREA/SEL | 1 | | 400115084 | 1 | | BRL | 70 | | Early_Term | 183 | | INV | 82558 |
| 4 | AEB/NY | 9 | | 300010735 | 9 | | CHF | 19 | | Loan/Deposit | 4 | | NET | 101508 |
| 5 | AIAKOREA/SEL | 29 | | 400095426 | 29 | | CLP | 7 | | ND Swaption | 22 | | SENT | 63728 |
| 6 | AIAKRINVT/SEL | 255 | | 400530483 | 255 | | CNH | 266 | | ND-BOND | 164 | | SUPP | 3840 |
| 7 | AIPEUGRE13/SEL | 8 | | 401004917 | 8 | | CNO | 668 | | ND-Convert | 623 | | Grand Total | 335139 |
| 8 | ALM_KRFB_NONHG | 2 | | 401001088 | 2 | | CNY | 413 | | NDF | 61824 | | | |
| 9 | ANZBANKING/SEL | 159 | | 10023260 | 159 | | COP | 25 | | NDIRS | 56067 | | | |
| 10 | BARC/LDN | 5 | | 10036739 | 5 | | DKK | 8 | | NDS | 1258 | | | |
| 11 | BATKML/SEL | 66 | | 400115699 | 66 | | EUR | 1935 | | NDS Fixing | 83815 | | | |
| 12 | BK OF CHIN/SEL | 5 | | 400052159 | 5 | | GBP | 81 | | OIS | 38 | | | |
| 13 | BKTYOMITUFJ/SEL | 789 | | 400052150 | 789 | | HKD | 5 | | Red Trades-StrucSwap | 32 | | | |
| 14 | BMVSHIPPING/SEL | 10 | | 401012522 | 10 | | INO | 207 | | Spot/Forward | 43 | | | |
| 15 | BMWAG/MNN | 36 | | 400201864 | 36 | | INR | 6 | | Structured Deposit | 674 | | | |
| 16 | BMWFINANCKR/SEL | 84 | | 400083567 | 84 | | JPY | 308 | | Structured Note | 76 | | | |
| 17 | BMWHOLDBV/SEL | 28 | | 400886012 | 28 | | KRO | 54977 | | Structured Swap | 512 | | | |
| 18 | BNPPAR/SEL | 85 | | 10038861 | 85 | | KRW | 137112 | | Vanilla IR Swap | 38877 | | | |
| 19 | BOA/SEL | 409 | | 400003597 | 409 | | NOK | 8 | | Vanilla X-ccy swap | 23751 | | | |
| 20 | CENTRALCORP/SEL | 102 | | 400775996 | 102 | | RON | 1 | | XVA Premium | 11057 | | | |
| 21 | CITI/SEL | 449 | | 10057153 | 449 | | SEK | 37 | | Grand Total | 335139 | | | |
| 22 | CL/SEL | 416 | | 10040402 | 416 | | SGD | 6 | | | | | | |
| 23 | CZNB/SEL | 1258 | | 10057106 | 1258 | | THB | 142 | | | | | | |
| 24 | DACHRY/STU | 10 | | 300084182 | 10 | | THO | 21 | | | | | | |
| 25 | DAEGBK/SEL | 11 | | 10057479 | 11 | | TWD | 374 | | | | | | |
| 26 | DAESUNGEL/GNG | 406 | | 400055255 | 406 | | TWO | 382 | | | | | | |
| 27 | DAEWOOENGCO/SEL | 43 | | 400048042 | 43 | | USD | 137976 | | | | | | |
| 28 | DAIMLERCHF/SEL | 7 | | 400056392 | 7 | | XU5 | 16 | | | | | | |
| 29 | DAISHINSTR/SEL | 8 | | 400230175 | 8 | | ZAR | 8 | | | | | | |
| 30 | DB28035/SEL | 4 | | 400927996 | 4 | | Grand Total | 335139 | | | | | | |
| 31 | DB28036/SEL | 4 | | 400927997 | 4 | | | | | | | | | |
| 32 | DBS/SEL | 674 | | 10054889 | 674 | | | | | | | | | |
| 33 | DBSKRSIP/SEL | 84 | | 400926912 | 84 | | | | | | | | | |
| 34 | DCRECOLTD/SEL | 6 | | 401020682 | 6 | | | | | | | | | |
| 35 | DELKORCORP/SEL | 106 | | 400058894 | 106 | | | | | | | | | |
| 36 | DEUTB/SEL | 621 | | 10042944 | 621 | | | | | | | | | |
| 37 | DLLIRLDDSGN/SEL | 934 | | 401016283 | 934 | | | | | | | | | |
| 38 | DONGBUINSUR/SEL | 48 | | 400108875 | 48 | | | | | | | | | |
| 39 | DONGBULIFEI/SEL | 130 | | 400064905 | 130 | | | | | | | | | |
| 40 | DONGKUKIND/SEL | 104 | | 400074984 | 104 | | | | | | | | | |
| 41 | DONGKUKRNS/SEL | 10 | | 400906323 | 10 | | | | | | | | | |
| 42 | DOOSANHEA/SEL | 172 | | 400049722 | 172 | | | | | | | | | |
| 43 | ELANDRETAIL/SEL | 9 | | 400769000 | 9 | | | | | | | | | |
| 44 | EMIRATE BK/DUB | 24 | | 10018141 | 24 | | | | | | | | | |
| 45 | EMVSHIPPING/SEL | 10 | | 401012524 | 10 | | | | | | | | | |
| 46 | EXPORTIMP/SEL | 168 | | 10063764 | 168 | | | | | | | | | |
| 47 | FARMSCO/SEL | 14 | | 401024090 | 14 | | | | | | | | | |
| 48 | FRLKOREA/SEL | 14 | | 400763077 | 14 | | | | | | | | | |
| 49 | GMVSHIPPING/SEL | 10 | | 401012525 | 10 | | | | | | | | | |
| 50 | GOODMORNING/SEL | 87 | | 400052199 | 87 | | | | | | | | | |
| 51 | GREENCROSS/SEL | 27 | | 400177982 | 27 | | | | | | | | | |
| 52 | GSENGNCON/SEL | 40 | | 400041784 | 40 | | | | | | | | | |
| 53 | HANACAP/SEL | 9 | | 401045180 | 9 | | | | | | | | | |
| 54 | HANADAESTR/SEL | 7 | | 400230321 | 7 | | | | | | | | | |
| 55 | HANADAETOO/SEL | 1419 | | 400052183 | 1419 | | | | | | | | | |
| 56 | HANALIFEINS/SEL | 12 | | 400828344 | 12 | | | | | | | | | |
| 57 | HANHWA SEC/SEL | 55 | | 400052188 | 55 | | | | | | | | | |
| 58 | HANONSYSTEM/SEL | 50 | | 400923898 | 50 | | | | | | | | | |
| 59 | HANWHACHEM/SEL | 50 | | 400091465 | 50 | | | | | | | | | |
| 60 | HANWHAINSUR/SEL | 39 | | 400177055 | 39 | | | | | | | | | |
| 61 | HANWHAOCEAN/SEL | 43 | | 401056617 | 43 | | | | | | | | | |
| 62 | HANWHATRUST/SEL | 7 | | 400203940 | 7 | | | | | | | | | |
| 63 | HARIMCOLTD/SEL | 68 | | 401024088 | 68 | | | | | | | | | |
| 64 | HDC HD DEV/SEL | 12 | | 400910318 | 12 | | | | | | | | | |
| 65 | HEESUNGENG/SEL | 113 | | 400068599 | 113 | | | | | | | | | |
| 66 | HEESUNGMETA/SEL | 170 | | 400727856 | 170 | | | | | | | | | |
| 67 | HEESUNGPMTE/GNG | 396 | | 400065095 | 396 | | | | | | | | | |
| 68 | HHAIGLB2/SEL | 6 | | 400538222 | 6 | | | | | | | | | |
| 69 | HHEURCRE3/SEL | 2 | | 400798466 | 2 | | | | | | | | | |
| 70 | HHEUROPP2/SEL | 15 | | 400660133 | 15 | | | | | | | | | |
| 71 | HHGLBINFR10/SEL | 9 | | 400897985 | 9 | | | | | | | | | |
| 72 | HHGLBINFRA8/SEL | 4 | | 400894080 | 4 | | | | | | | | | |
| 73 | HHGLBINFRA9/SEL | 10 | | 400894101 | 10 | | | | | | | | | |
| 74 | HHGLBREF1/SEL | 4 | | 400230741 | 4 | | | | | | | | | |
| 75 | HHGLBREF3/SEL | 6 | | 400789533 | 6 | | | | | | | | | |
| 76 | HHGLREAL2/SEL | 10 | | 400908042 | 10 | | | | | | | | | |
| 77 | HHVENTURE2/SEL | 14 | | 400904808 | 14 | | | | | | | | | |
| 78 | HICS37/SEL | 2 | | 401064687 | 2 | | | | | | | | | |
| 79 | HIHOMETAL/SEL | 23 | | 400059965 | 23 | | | | | | | | | |
| 80 | HITAVIA12/SEL | 12 | | 400892323 | 12 | | | | | | | | | |
| 81 | HITMUFST30/SEL | 9 | | 400965571 | 9 | | | | | | | | | |
| 82 | HLINESHIP/SEL | 259 | | 400755316 | 259 | | | | | | | | | |
| 83 | HNBN/SEL | 26 | | 10058532 | 26 | | | | | | | | | |
| 84 | HPKOREAINC/SEL | 48 | | 400797606 | 48 | | | | | | | | | |
| 85 | HPPRINTKR/SEL | 38 | | 400941671 | 38 | | | | | | | | | |
| 86 | HSBC/SEL | 797 | | 300072385 | 797 | | | | | | | | | |
| 87 | HUNGKUKLIFE/SEL | 41 | | 400046589 | 41 | | | | | | | | | |
| 88 | HWASHINCO/SEL | 2 | | 401027507 | 2 | | | | | | | | | |
| 89 | HWVIETOPPO1/SEL | 5 | | 401017015 | 5 | | | | | | | | | |
| 90 | HYMAFI/SEL | 181 | | 400023629 | 181 | | | | | | | | | |
| 91 | HYMOCO/SEL | 51 | | 400003124 | 51 | | | | | | | | | |
| 92 | HYNIXSEMICO/SEL | 6 | | 400072788 | 6 | | | | | | | | | |
| 93 | HYOSUNGHEAV/SEL | 170 | | 401022100 | 170 | | | | | | | | | |
| 94 | HYUHEA/SEL | 256 | | 400039064 | 256 | | | | | | | | | |
| 95 | HYUNDAIASSA/SEL | 6 | | 401006669 | 6 | | | | | | | | | |
| 96 | HYUNDAIELEC/SEL | 25 | | 400885831 | 25 | | | | | | | | | |
| 97 | HYUNDAIMIPO/ULS | 18 | | 400046751 | 18 | | | | | | | | | |
| 98 | HYUNDAISAMH/SEL | 61 | | 400046436 | 61 | | | | | | | | | |
| 99 | HYUNDAISEC/SEL | 24 | | 400052171 | 24 | | | | | | | | | |
| 100 | IBK/SEL | 300 | | 300072418 | 300 | | | | | | | | | |
| 101 | IBKSECS/SEL | 57 | | 400096840 | 57 | | | | | | | | | |
| 102 | IBKSECTR1/SEL | 7 | | 400183765 | 7 | | | | | | | | | |
| 103 | IBMKOREAINC/SEL | 4 | | 400109131 | 4 | | | | | | | | | |
| 104 | IGISGLO4022/SEL | 2 | | 400995812 | 2 | | | | | | | | | |
| 105 | IGISUSR221/SEL | 8 | | 400918611 | 8 | | | | | | | | | |
| 106 | ING/SEL | 644 | | 75000886 | 644 | | | | | | | | | |
| 107 | INTL/ALM | 5 | | 300036053 | 5 | | | | | | | | | |
| 108 | INTL/ALM DESK | 3547 | | 400009156 | 3547 | | | | | | | | | |
| 109 | INTL/FWD DESK | 210 | | 400009154 | 210 | | | | | | | | | |
| 110 | INTL/SPOT DESK | 1479 | | 300079654 | 1479 | | | | | | | | | |
| 111 | JNOFFWP/SEL | 4 | | 401033985 | 4 | | | | | | | | | |
| 112 | JOONGANGPNI/SEL | 22 | | 401062762 | 22 | | | | | | | | | |
| 113 | JPMC/SEL | 1377 | | 10039303 | 1377 | | | | | | | | | |
| 114 | KB7501/SEL | 2 | | 400998294 | 2 | | | | | | | | | |
| 115 | KBCARD/SEL | 8 | | 400194506 | 8 | | | | | | | | | |
| 116 | KBCVC2/SEL | 8 | | 400958457 | 8 | | | | | | | | | |
| 117 | KBGLOREDT17/SEL | 2 | | 401013041 | 2 | | | | | | | | | |
| 118 | KBLIFEINSRC/SEL | 158 | | 400133956 | 158 | | | | | | | | | |
| 119 | KBNBPVT3/SEL | 10 | | 401020374 | 10 | | | | | | | | | |
| 120 | KBPVREDF14/SEL | 4 | | 401006183 | 4 | | | | | | | | | |
| 121 | KBSSSHIP1/SEL | 4 | | 400674848 | 4 | | | | | | | | | |
| 122 | KDB/SEL | 3632 | | 10038283 | 3632 | | | | | | | | | |
| 123 | KEB/SEL | 1366 | | 300048648 | 1366 | | | | | | | | | |
| 124 | KEMCO/SEL | 21 | | 401042758 | 21 | | | | | | | | | |
| 125 | KEPCOENC/SEL | 5 | | 400180762 | 5 | | | | | | | | | |
| 126 | KFOCC/SEL | 26 | | 400052207 | 26 | | | | | | | | | |
| 127 | KIAMCOABU/SEL | 2 | | 400962652 | 2 | | | | | | | | | |
| 128 | KIAMCOIIDF/SEL | 8 | | 401063192 | 8 | | | | | | | | | |
| 129 | KIAMCOSHIP2/SEL | 4 | | 400998115 | 4 | | | | | | | | | |
| 130 | KIAMIFM1/SEL | 6 | | 400847460 | 6 | | | | | | | | | |
| 131 | KIAMOT/SEL | 18 | | 400017647 | 18 | | | | | | | | | |
| 132 | KIM06G78/SEL | 8 | | 400896785 | 8 | | | | | | | | | |
| 133 | KIRA07J15/SEL | 2 | | 401027849 | 2 | | | | | | | | | |
| 134 | KIRA07K95/SEL | 4 | | 401027850 | 4 | | | | | | | | | |
| 135 | KIWOOM SEC/SEL | 59 | | 400052185 | 59 | | | | | | | | | |
| 136 | KOLON/SEL | 27 | | 400823827 | 27 | | | | | | | | | |
| 137 | KOREAEXPRES/SEL | 2 | | 400113019 | 2 | | | | | | | | | |
| 138 | KOREAHSEFIN/SEL | 46 | | 400041790 | 46 | | | | | | | | | |
| 139 | KOREANATOIL/SEL | 5 | | 400102389 | 5 | | | | | | | | | |
| 140 | KOREAZINC/SEL | 15 | | 400049815 | 15 | | | | | | | | | |
| 141 | KORELEPOW/SEL | 47 | | 400049708 | 47 | | | | | | | | | |
| 142 | KORLIF/SUL | 161 | | 400038118 | 161 | | | | | | | | | |
| 143 | KRCMCRCPWEL/SEL | 11 | | 401028355 | 11 | | | | | | | | | |
| 144 | KRINVNSECS/SEL | 339 | | 400064333 | 339 | | | | | | | | | |
| 145 | KRLANDNHOUS/SEL | 11 | | 400450328 | 11 | | | | | | | | | |
| 146 | KRSTUDENT/SEL | 13 | | 400397668 | 13 | | | | | | | | | |
| 147 | KRUSDS13/SEL | 4 | | 400972948 | 4 | | | | | | | | | |
| 148 | KRX/SEL | 34837 | | 400649418 | 34837 | | | | | | | | | |
| 149 | KYOBLI/SEL | 93 | | 400011681 | 93 | | | | | | | | | |
| 150 | KYOBOSEC/SEL | 332 | | 400052175 | 332 | | | | | | | | | |
| 151 | LANDESBKBW/SEL | 180 | | 400087300 | 180 | | | | | | | | | |
| 152 | LAUTOWORSEC/SEL | 8 | | 400937131 | 8 | | | | | | | | | |
| 153 | LGEL/SEL | 30 | | 400005762 | 30 | | | | | | | | | |
| 154 | LGENERGYSOL/SEL | 18 | | 400986990 | 18 | | | | | | | | | |
| 155 | LGPHLCD/SEL | 60 | | 400024288 | 60 | | | | | | | | | |
| 156 | LOTTECARD/SEL | 4 | | 400082878 | 4 | | | | | | | | | |
| 157 | LOTTEINS/SEL | 109 | | 400089058 | 109 | | | | | | | | | |
| 158 | LSCABLE/SEL | 123 | | 400098191 | 123 | | | | | | | | | |
| 159 | LSINDUSTRIA/SEL | 64 | | 400141570 | 64 | | | | | | | | | |
| 160 | LSLPRVPL10/SEL | 2 | | 400892313 | 2 | | | | | | | | | |
| 161 | LSLPRVPL6/SEL | 2 | | 400887177 | 2 | | | | | | | | | |
| 162 | LSNIKKOCOP/SEL | 344 | | 400052507 | 344 | | | | | | | | | |
| 163 | MERITZFOF14/SEL | 2 | | 401038000 | 2 | | | | | | | | | |
| 164 | MERITZPR14/SEL | 2 | | 400908169 | 2 | | | | | | | | | |
| 165 | MERITZR2/SEL | 4 | | 400852799 | 4 | | | | | | | | | |
| 166 | MERREFOF8/SEL | 4 | | 401010807 | 4 | | | | | | | | | |
| 167 | METLIFEINS/SEL | 47 | | 400228550 | 47 | | | | | | | | | |
| 168 | MGNCHPSMCDT/SEL | 2 | | 400971151 | 2 | | | | | | | | | |
| 169 | MINCO/SEL | 10 | | 400013212 | 10 | | | | | | | | | |
| 170 | MINCOSV/SEL | 6 | | 400138854 | 6 | | | | | | | | | |
| 171 | MIRAEASSLI/SEL | 40 | | 400058083 | 40 | | | | | | | | | |
| 172 | MIZCOR/SEL | 597 | | 400052162 | 597 | | | | | | | | | |
| 173 | MORGSTBKIN/SEL | 129 | | 400052864 | 129 | | | | | | | | | |
| 174 | MRGLOREITS1/SEL | 4 | | 401011813 | 4 | | | | | | | | | |
| 175 | NAAGCF/SEL | 111 | | 400226859 | 111 | | | | | | | | | |
| 176 | NACF/SEL | 901 | | 215003167 | 901 | | | | | | | | | |
| 177 | NATLFEDFISH/SEL | 255 | | 400052165 | 255 | | | | | | | | | |
| 178 | NHMRMAPUS1/SEL | 10 | | 400875822 | 10 | | | | | | | | | |
| 179 | NHMRPOLAND1/SEL | 2 | | 400923218 | 2 | | | | | | | | | |
| 180 | NOMURAINTL/SEL | 436 | | 400089146 | 436 | | | | | | | | | |
| 181 | NONGHYUPLI/SEL | 11 | | 400225688 | 11 | | | | | | | | | |
| 182 | NOVELISKR/SEL | 356 | | 400097978 | 356 | | | | | | | | | |
| 183 | OCI COMPANY/SEL | 5 | | 401073821 | 5 | | | | | | | | | |
| 184 | ORIXAUTOLE/SEL | 12 | | 400055611 | 12 | | | | | | | | | |
| 185 | POSCO2/SEL | 54 | | 401019863 | 54 | | | | | | | | | |
| 186 | POSCOCHEMCO/SEL | 7 | | 400965078 | 7 | | | | | | | | | |
| 187 | POSCOENGCO/SEL | 14 | | 400049822 | 14 | | | | | | | | | |
| 188 | PRUDLIFEINS/SEL | 2 | | 400043237 | 2 | | | | | | | | | |
| 189 | PSDBP3I4/SEL | 2 | | 401078183 | 2 | | | | | | | | | |
| 190 | PSGLCOF62/SEL | 2 | | 400985729 | 2 | | | | | | | | | |
| 191 | PSGLOCF3/SEL | 2 | | 400985708 | 2 | | | | | | | | | |
| 192 | PSGLOCF6/SEL | 2 | | 400980475 | 2 | | | | | | | | | |
| 193 | PSGLOINF2/SEL | 4 | | 401074734 | 4 | | | | | | | | | |
| 194 | PSINFCR1/SEL | 14 | | 401018446 | 14 | | | | | | | | | |
| 195 | PUSANBK/SEL | 38 | | 10055169 | 38 | | | | | | | | | |
| 196 | QESOLSE/SEL | 2 | | 401061258 | 2 | | | | | | | | | |
| 197 | RCIFINSERK/SEL | 19 | | 400631287 | 19 | | | | | | | | | |
| 198 | RLNKSDA/SEL | 217 | | 400057113 | 217 | | | | | | | | | |
| 199 | ROTHMANFARE/SEL | 6 | | 400110838 | 6 | | | | | | | | | |
| 200 | SABMILLERKR/SEL | 2 | | 400660447 | 2 | | | | | | | | | |
| 201 | SAMCOR/SEO | 75 | | 220003386 | 75 | | | | | | | | | |
| 202 | SAMSUNGENG/SEL | 174 | | 400049692 | 174 | | | | | | | | | |
| 203 | SAMSUNGFIRE/SEL | 90 | | 400049718 | 90 | | | | | | | | | |
| 204 | SAMSUNGSECU/SEL | 35 | | 400031867 | 35 | | | | | | | | | |
| 205 | SAMTEKCORP/SEL | 106 | | 400054689 | 106 | | | | | | | | | |
| 206 | SC_IRKR_CONTFD | 21 | | 400060382 | 21 | | | | | | | | | |
| 207 | SC_IRKR_EXFBBTB | 5 | | 400048061 | 5 | | | | | | | | | |
| 208 | SC_NDFHK_BTBHK | 33 | | 2 | 33 | | | | | | | | | |
| 209 | SCB SG LTD/SIN | 30 | | 400451508 | 30 | | | | | | | | | |
| 210 | SCB TAIPEI/TPE | 4 | | 10038345 | 4 | | | | | | | | | |
| 211 | SCB/BKK | 102 | | 6 | 102 | | | | | | | | | |
| 212 | SCB/HKG | 4857 | | 2 | 4857 | | | | | | | | | |
| 213 | SCB/LDN | 244647 | | 10075222 | 244647 | | | | | | | | | |
| 214 | SCB/MMB | 37 | | 4 | 37 | | | | | | | | | |
| 215 | SCBEQUITY/HK | 62 | | 400167650 | 62 | | | | | | | | | |
| 216 | SCBKWMPS/SEL | 6 | | 400817019 | 6 | | | | | | | | | |
| 217 | SCFB_SQKRO_RLN | 26 | | 400057103 | 26 | | | | | | | | | |
| 218 | SEAHCW/SEL | 4 | | 400885295 | 4 | | | | | | | | | |
| 219 | SHAIMFOF3A/SEL | 5 | | 400937361 | 5 | | | | | | | | | |
| 220 | SHAIMFOF3B/SEL | 9 | | 400933739 | 9 | | | | | | | | | |
| 221 | SHAIMFOF3C/SEL | 8 | | 400944206 | 8 | | | | | | | | | |
| 222 | SHAIMFOF3D/SEL | 8 | | 400946305 | 8 | | | | | | | | | |
| 223 | SHALTAIM1A/SEL | 8 | | 400904867 | 8 | | | | | | | | | |
| 224 | SHALTFOF3/SEL | 9 | | 400925757 | 9 | | | | | | | | | |
| 225 | SHAPDV1/SEL | 4 | | 401004924 | 4 | | | | | | | | | |
| 226 | SHBH/SEL | 1038 | | 10039816 | 1038 | | | | | | | | | |
| 227 | SHBNP2P1768/SEL | 2 | | 400965608 | 2 | | | | | | | | | |
| 228 | SHBNP2P1802/SEL | 2 | | 400955245 | 2 | | | | | | | | | |
| 229 | SHBNPCOINV1/SEL | 4 | | 400884594 | 4 | | | | | | | | | |
| 230 | SHBNPCOINV2/SEL | 2 | | 400892620 | 2 | | | | | | | | | |
| 231 | SHBNPDOVX6/SEL | 2 | | 400972229 | 2 | | | | | | | | | |
| 232 | SHBNPEULON1/SEL | 2 | | 400884087 | 2 | | | | | | | | | |
| 233 | SHBNPGBOND1/SEL | 2 | | 400928558 | 2 | | | | | | | | | |
| 234 | SHBNPHL2019/SEL | 2 | | 400926511 | 2 | | | | | | | | | |
| 235 | SHBNPPDOV3/SEL | 2 | | 400939540 | 2 | | | | | | | | | |
| 236 | SHC20223/SEL | 29 | | 401032363 | 29 | | | | | | | | | |
| 237 | SHDOVERXI7H/SEL | 4 | | 401058393 | 4 | | | | | | | | | |
| 238 | SHDVXI2H/SEL | 4 | | 401042988 | 4 | | | | | | | | | |
| 239 | SHDVXI6H/SEL | 4 | | 401044921 | 4 | | | | | | | | | |
| 240 | SHEURCO1/SEL | 2 | | 401019508 | 2 | | | | | | | | | |
| 241 | SHG1REIT/SEL | 6 | | 401025243 | 6 | | | | | | | | | |
| 242 | SHHPSSLFV1/SEL | 2 | | 401004921 | 2 | | | | | | | | | |
| 243 | SHINHAINVTR/SEL | 7 | | 400227589 | 7 | | | | | | | | | |
| 244 | SHINHANCAP/SEL | 17 | | 401045058 | 17 | | | | | | | | | |
| 245 | SHINHANLIFI/SEL | 150 | | 400101794 | 150 | | | | | | | | | |
| 246 | SHINHEUNGSE/SEL | 62 | | 400052177 | 62 | | | | | | | | | |
| 247 | SHINSEGAECS/SEL | 10 | | 401072703 | 10 | | | | | | | | | |
| 248 | SHJPPHOTO3/SEL | 8 | | 401011166 | 8 | | | | | | | | | |
| 249 | SHLCPX2H/SEL | 6 | | 401039665 | 6 | | | | | | | | | |
| 250 | SHLCPX3H/SEL | 4 | | 401043424 | 4 | | | | | | | | | |
| 251 | SHLCPXPVT1/SEL | 4 | | 401013768 | 4 | | | | | | | | | |
| 252 | SKEANDS/SEL | 8 | | 400713556 | 8 | | | | | | | | | |
| 253 | SKECOENG/SEL | 27 | | 401019778 | 27 | | | | | | | | | |
| 254 | SKENGNCONS/SEL | 2 | | 400075204 | 2 | | | | | | | | | |
| 255 | SKONCOLTD/SEL | 4 | | 401033987 | 4 | | | | | | | | | |
| 256 | SKSHIPPING/SEL | 56 | | 400074320 | 56 | | | | | | | | | |
| 257 | SKTELECOM/SEL | 6 | | 400077198 | 6 | | | | | | | | | |
| 258 | SL CORP/SEL | 16 | | 400333008 | 16 | | | | | | | | | |
| 259 | SOCGEN/SEL | 615 | | 10040044 | 615 | | | | | | | | | |
| 260 | SRASTRE27/SEL | 14 | | 401040763 | 14 | | | | | | | | | |
| 261 | SRASTRE28/SEL | 4 | | 401041226 | 4 | | | | | | | | | |
| 262 | SS231904/SEL | 20 | | 401043223 | 20 | | | | | | | | | |
| 263 | SS232011/SEL | 22 | | 401045485 | 22 | | | | | | | | | |
| 264 | SS232906/SEL | 49 | | 400948306 | 49 | | | | | | | | | |
| 265 | SS232942/SEL | 8 | | 401005842 | 8 | | | | | | | | | |
| 266 | SS233004/SEL | 5 | | 401036881 | 5 | | | | | | | | | |
| 267 | SS233005/SEL | 6 | | 401032241 | 6 | | | | | | | | | |
| 268 | SSANGYONGFM/SEL | 22 | | 400059154 | 22 | | | | | | | | | |
| 269 | SSARDIAN1/SEL | 8 | | 400873199 | 8 | | | | | | | | | |
| 270 | SSCBACU/SIN | 285 | | 400452428 | 285 | | | | | | | | | |
| 271 | SSHV/SEL | 1670 | | 400017103 | 1670 | | | | | | | | | |
| 272 | SSIFMGD1/SEL | 6 | | 400877679 | 6 | | | | | | | | | |
| 273 | SSLI/SEL | 99 | | 400009389 | 99 | | | | | | | | | |
| 274 | SSPOWERPT1/SEL | 4 | | 400789534 | 4 | | | | | | | | | |
| 275 | SSSAUDCOLTD/SEL | 52 | | 401068239 | 52 | | | | | | | | | |
| 276 | SSSRAGCOPR2/SEL | 2 | | 400898332 | 2 | | | | | | | | | |
| 277 | SSSRAMDUS1/SEL | 16 | | 401037999 | 16 | | | | | | | | | |
| 278 | SSSRAMDUS2/SEL | 2 | | 401063972 | 2 | | | | | | | | | |
| 279 | SSSRAPRV39/SEL | 4 | | 400917562 | 4 | | | | | | | | | |
| 280 | SSSRAPVT26/SEL | 4 | | 401040761 | 4 | | | | | | | | | |
| 281 | SSSRAPVT56/SEL | 2 | | 401029595 | 2 | | | | | | | | | |
| 282 | SSSRARE54/SEL | 4 | | 401014069 | 4 | | | | | | | | | |
| 283 | SSSRARE65/SEL | 12 | | 401013902 | 12 | | | | | | | | | |
| 284 | SSSRARE65A/SEL | 12 | | 401013957 | 12 | | | | | | | | | |
| 285 | SSSRASTR1/SEL | 8 | | 400978268 | 8 | | | | | | | | | |
| 286 | SSSRAUSDRE1/SEL | 4 | | 401021351 | 4 | | | | | | | | | |
| 287 | STANCHAAG/FRA | 25 | | 400906330 | 25 | | | | | | | | | |
| 288 | STXPANOCEAN/SEL | 31 | | 400056464 | 31 | | | | | | | | | |
| 289 | SWISSREASIA/SEL | 20 | | 401005368 | 20 | | | | | | | | | |
| 290 | TETRAPAKLTD/SEL | 64 | | 400084379 | 64 | | | | | | | | | |
| 291 | TIGERALT61/SEL | 4 | | 401022510 | 4 | | | | | | | | | |
| 292 | TONGYANGLIN/SEL | 82 | | 400043309 | 82 | | | | | | | | | |
| 293 | TONGYANGSEC/SEL | 6 | | 400052174 | 6 | | | | | | | | | |
| 294 | TORECOMCORP/SEL | 209 | | 400152794 | 209 | | | | | | | | | |
| 295 | TRATONTRAAB/SEL | 273 | | 401054897 | 273 | | | | | | | | | |
| 296 | TRSTGIQPVT6/SEL | 2 | | 400934106 | 2 | | | | | | | | | |
| 297 | UBSAG SELBR/SEL | 1 | | 401071669 | 1 | | | | | | | | | |
| 298 | UOVB/SEL | 81 | | 400034919 | 81 | | | | | | | | | |
| 299 | VOGODEB3/SEL | 4 | | 400873286 | 4 | | | | | | | | | |
| 300 | VOGODEBT11/SEL | 2 | | 400941124 | 2 | | | | | | | | | |
| 301 | VOGODEBT2/SEL | 6 | | 400919116 | 6 | | | | | | | | | |
| 302 | VOGODEBT4/SEL | 8 | | 400919117 | 8 | | | | | | | | | |
| 303 | VOGOEUB2/SEL | 6 | | 400881731 | 6 | | | | | | | | | |
| 304 | VOLVOTSYASI/SIN | 657 | | 10063131 | 657 | | | | | | | | | |
| 305 | WOORI BK/SEL | 1555 | | 400052152 | 1555 | | | | | | | | | |
| 306 | WOORIAVIVAL/SEL | 14 | | 400152941 | 14 | | | | | | | | | |
| 307 | WOORIINVEST/SEL | 90 | | 400052197 | 90 | | | | | | | | | |
| 308 | WOORYINDUST/SEL | 32 | | 400775317 | 32 | | | | | | | | | |
| 309 | WRG817/SEL | 2 | | 401050323 | 2 | | | | | | | | | |
| 310 | WRG819/SEL | 5 | | 401050322 | 5 | | | | | | | | | |
| 311 | XVAOMNBUS/LDN | 10955 | | 400795971 | 10955 | | | | | | | | | |
| 312 | YOUNGONE/SEL | 20 | | 400121434 | 20 | | | | | | | | | |
| 313 | YOUNGWOODIG/SEL | 4 | | 400069741 | 4 | | | | | | | | | |
| 314 | YUHANKMBRLY/SEL | 287 | | 401005021 | 287 | | | | | | | | | |
| 315 | Grand Total | 335139 | | | 335139 | | | | | | | | | |

**EXPAND_END**

**EXPAND: Swift Date Analysis**

Swift Sample Difference type

| Diff type | Sample Flow id | Murex MT | Ratan MT | Reason | Result |
| --- | --- | --- | --- | --- | --- |
| Field3 Line1 miss in murex | M00005843966 | {1:F01SCBLKRSEXXXX0000000000}{2:I202SCBLUS33XXXXN}{4: :20:MX700005843965B :21:MX700005843965B :32A:260617USD203632,51 :52A:SCBLKRSEXXX :57A:SCBLUS33XXX :[58A:/3582088442001](http://58A/3582088442001) SCBLGB2LTSY -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202SCBLUS33XXXXN}{3:{121:07c20de0-233d-4d2c-afa7-cb69b20b4219}}{4: :20:DV70M00005843966 :21:DV70M00005843966 :32A:260617USD203632,51 :[53A:/3582070313001](http://53A/3582070313001) SCBLUS33XXX :57A:SCBLUS33XXX :58A:SCBLGB2LTSY -} | Murex Korea did not generate UETR in tag121. As expected. | Closed |
| Field32A Line1 is not same | M00005840277 | {1:F01SCBLKRSEXXXX0000000000}{2:I202SCBLUS33XXXXN}{4: :20:MX700005840277B :21:MX700005840277B :32A:260617USD20110,31 :52A:SCBLKRSEXXX :57A:SCBLUS33XXX :[58A:/3582088442001](http://58A/3582088442001) SCBLGB2LTSY -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202SCBLUS33XXXXN}{3:{121:b8c8c0b8-3dc0-4905-9774-8c57d6698b54}}{4: :20:DV70M00005840277 :21:DV70M00005840277 :32A:260617USD20110,32 :[53A:/3582070313001](http://53A/3582070313001) SCBLUS33XXX :57A:SCBLUS33XXX :58A:SCBLGB2LTSY -} | Decimal diff. As expected. | Closed |
| Field52A Line1 miss in ratan | M00005779526 | {1:F01SCBLKRSEXXXX0000000000}{2:I202ANZBAU3MXXXXN}{4: :20:MX700005779526B :21:MX700005779526B :32A:260617AUD151232,87 :52A:SCBLKRSEXXX :57A:ANZBAU3MXXX :[58A:/949040AUD00001](http://58A/949040AUD00001) SCBLHKHHXXX -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202ANZBAU3MXXXXN}{3:{121:b8715f77-a6e0-4796-b6a4-e94d5ad6a7b6}}{4: :20:DV70M00005779526 :21:DV70M00005779526 :32A:260617AUD151232,87 :[53A:/949024AUD00001](http://53A/949024AUD00001) ANZBAU3MXXX :57A:ANZBAU3MXXX :58A:SCBLHKHHXXX -} | No tag52 in RATAN. As expected. | Closed |
| Field53A Line1 miss in murex | M00005779526 | {1:F01SCBLKRSEXXXX0000000000}{2:I202ANZBAU3MXXXXN}{4: :20:MX700005779526B :21:MX700005779526B :32A:260617AUD151232,87 :52A:SCBLKRSEXXX :57A:ANZBAU3MXXX :[58A:/949040AUD00001](http://58A/949040AUD00001) SCBLHKHHXXX -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202ANZBAU3MXXXXN}{3:{121:b8715f77-a6e0-4796-b6a4-e94d5ad6a7b6}}{4: :20:DV70M00005779526 :21:DV70M00005779526 :32A:260617AUD151232,87 :[53A:/949024AUD00001](http://53A/949024AUD00001) ANZBAU3MXXX :57A:ANZBAU3MXXX :58A:SCBLHKHHXXX -} | No tag32 in Murex Korea. As expected. | Closed |
| Field57A Line1 is not same | M00005834484 | {1:F01SCBLKRSEXXXX0000000000}{2:I202SCBLGB2LXTSYN}{4: :20:MX700005834484B :21:MX700005834484B :32A:260617GBP500000000, :52A:SCBLKRSEXXX :57A:SCBLGB2LTSY :[58A:/0009199787401](http://58A/0009199787401) SCBLGB2LTSY :[72:/INF/IBAN](http://72/INF/IBAN) GB26SCBL60910491997874 -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202SCBLGB2LXTSYN}{3:{121:33818f05-d0d9-4928-8bc1-f7d89af98ba1}}{4: :20:DV70M00005834484 :21:DV70M00005834484 :32A:260617GBP500000000, :[53A:/01254635301](http://53A/01254635301) SCBLGB2LTSY :57A:SCBLGB2LXXX :58A:SCBLGB2LTSY :[72:/INF/IBAN](http://72/INF/IBAN) GB26SCBL60910491997874 -} | 57BIC 8-11 digit diff. As expected. | Closed |
| Field58A Line2 miss in ratan | M00005779526 | {1:F01SCBLKRSEXXXX0000000000}{2:I202ANZBAU3MXXXXN}{4: :20:MX700005779526B :21:MX700005779526B :32A:260617AUD151232,87 :52A:SCBLKRSEXXX :57A:ANZBAU3MXXX :[58A:/949040AUD00001](http://58A/949040AUD00001) SCBLHKHHXXX -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202ANZBAU3MXXXXN}{3:{121:b8715f77-a6e0-4796-b6a4-e94d5ad6a7b6}}{4: :20:DV70M00005779526 :21:DV70M00005779526 :32A:260617AUD151232,87 :[53A:/949024AUD00001](http://53A/949024AUD00001) ANZBAU3MXXX :57A:ANZBAU3MXXX :58A:SCBLHKHHXXX -} | No 58 account in SSI+. As expected. | Closed |
| Field72 Line1 miss in murex | M00005839826 | {1:F01SCBLKRSEXXXX0000000000}{2:I202SCBLUS33XXXXN}{4: :20:MX700005839826B :21:MX700005839826B :32A:260617USD1371436,58 :52A:SCBLKRSEXXX :57A:SCBLUS33XXX :58A:SCBLHKHHXXX -} | {1:F01SCBLKRSEAXXX0000000000}{2:I202SCBLUS33XXXXN}{3:{121:90ca5ae4-8299-4150-b2d3-5349c4b548c7}}{4: :20:DV70M00005839826 :21:DV70M00005839826 :32A:260617USD1371436,58 :[53A:/3582070313001](http://53A/3582070313001) SCBLUS33XXX :57A:SCBLUS33XXX :[58A:/3582088658001](http://58A/3582088658001) SCBLHKHHXXX :[72:/INF/CHIPS](http://72/INF/CHIPS) UID 078600 -} | Different input by user. | Closed |

**EXPAND_END**