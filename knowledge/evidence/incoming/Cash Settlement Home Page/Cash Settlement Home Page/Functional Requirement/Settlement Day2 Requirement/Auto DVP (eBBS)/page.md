#

# Background

Currently checks are done manually with CMO / Investigation team to validate if funds are received before payments are released . Automation of the DvP payment notification /instructions process in RATAN allows increased efficiency and reduced manual touch points especially handling same-value date settlements.

# ADO

[Feature 11718782 Auto DVP (eBBS)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11718782)

[Generic Task 11759674 [Auto DVP] Requirement analysis](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11759674/)

# Requirement Details

## Definifion of DVP cashflows

- - Stella Cashflows: Settlement Method = DVP - Murex Cashflows: List of Strategies – re-use DVP NSTP condition from prod : Instrument_Common__Murex_Product_Strategy in ("CCS_DVP", "CM_PMASIANFWDVP", "COM_AMES_DVP", "COM_BDF_DVP", "COM_BOE_DVP", "COM_JMUK_DVP", "COM_JMVF_DVP", "COM_LDN_DVP", "COM_OUTRGHT_DVP", "COM_RAND_DVP", "COM_SOUK_DVP", "COM_UBS_DVP", "COM_ZUR_DVP", "CR_RTM_CCS_DVP", "FX_PMTRF_DVP", "FX_TRF_DVP", "IR_AFR_DVP", "PAR FWD DVP", "PM_TRF_DVP", "PRC_OFFTAKE_DVP", "CM_PMASIANFWDP", "SGE_TRIPARTY_FW", "CCS_CORP_DVP", "CCS_FI_DVP")

## Flow

1. Receive RTA for Netting resultant cashflow (Netting resultant cashflow settled from RATAN and receive RTA of the netting resultant cashflow) not covered in current scope, system will do nothing-Confirmed with Deepak ,it's OK.
2. Receive RTA for Split cashflow (Splitted child cashflow settled from RATAN and receive RTA of the splitted child cashflow) not covered in current scope, system will do nothing -Confirmed with Deepak ,it's OK.
3. System will ignore withdraw event, means if receive withdraw event of receive cashflow ,will do nothing and not to find pay cashflow -Confirmed with Deepak ,it's OK.
4. After system find pay cashflow based on receive ,system only check if pay cashflow in 'Waiting' status and hit DVP exception, for the other status not in 'Waiting' ,system will do nothing-Confirmed with Deepak ,it's OK.
5. After system find pay cashflow based on receive ,if pay cashflow id is start with N, system will do nothing -Confirmed with Weng Hien, it's OK
6. One receive cashflow link to more than one pay cashflows.-Confirmed with Deepak ,it's OK. a. One receive cashflow link to one pay cashflow, and pay cashflow is splitted to many child cashflows ,child cashflows in 'Waiting' status and hit DVP exception, system will auto close DVP exception for these child cashflows. b. For the other one receive cashflow link to more than one pay cashflow case ,many pay cashflows and not split child cashflows, system will do nothing, need user manually handle.
7. ND CCS netting resultant is pay and hit DVP exception, will not receive EBBS RTA for the receive cashflow ,not in scope-Confirmed with Deepak ,it's OK.
8. In case unexpected reasons causing RTA consumption failure, can't auto close DVP exception of pay cashflow ,need user to manually handle.

## Upstream

Currently for RATAN, only EBBS is in scope.

| Country | FM ID | FM Code | EBBS RTA Topic |
| --- | --- | --- | --- |
| GH | 10037477 | SCB GHANA*ACC | v1/14147-ebbs-/casa/scbml-1.0/gh/pub/corp-fin/all |
| ID | 8 | SCB JAKARTA*JKT | v1/14147-ebbs-/casa/scbml-1.0/id/pub/corp-fin/all |
| MY | 9 | SCB KL*KUL? | v1/14147-ebbs-/casa/scbml-1.0/my/pub/corp-fin/all |
| 400093619 | STANCHART SAADIQ*KUL |
| ZA | 400032489 | SCBL*JBG | v1/14147-ebbs-/casa/scbml-1.0/za/pub/corp-fin/all |
| CN | 10020899 | SCB CHINA*NJG | v1/14147-ebbs-/casa/scbml-1.0/cn/pub/corp-fin/all |
| 10032025 | SCB CHINA*SZN |
| 10036642 | SCB SHANGH*SHA |
| 10062461 | SCB CHINA*XMN |
| 10078716 | SCB CHINA*ZHU |
| 235003861 | SCB CHINA*TIA |
| 400001378 | SCB CHINA*BJG |
| 400054708 | SCB GUANGZHOU*GZU |
| 400054737 | SCB SUZHOU*SUZ |
| 400054741 | SCB CHENGDU*CGD |
| 400057714 | SCB QINGDAO*QDO |
| 400075752 | SCB CN CHONGQING*CQG |
| 400085753 | SCB CN HANGZHOU*HNZ |
| 400090093 | SCB CHINA*NCG |
| 400095464 | SCB CHINA DALIAN*DLN |
| 400130178 | SCB CHINA HOHHOT*HHH |
| 400130180 | SCB CHINA NINGBO*NGB |
| 400185419 | SCB CN WUHAN*WUH |
| 400193370 | SCBLXIAN*XIN |
| 400209000 | SCB CN FOSHAN*FOS |
| 400218197 | SCB CN JINAN BR*JNA |
| 400220273 | SCB CN CHANGSHA*CGS |
| 400229749 | SCB CN FUZHOU*FZH |
| 400516442 | SCB CN ZHENGZHOU*ZZU |
| 400516443 | SCB CN TAIYUAN*TYA |
| 400667486 | SCB CN KMG*KMG |
| 400677737 | SCB SHA FTU*FT2 |
| 400683682 | SCB CN HRB*HRB |
| 400798477 | SCB CN SYG*SYG |
| 400899993 | SCB CN CHO*CHO |
| 401053411 | SCB CHINA*HFI |
| AE | 400045551 | SCB DUBAI DFC*DUB | v1/14147-ebbs-/casa/scbml-1.0/ae/pub/corp-fin/all |
| 5 | SCB DUBAI*DUB |
| BD | 300011470 | SCB DHAKA*DAC | v1/14147-ebbs-/casa/scbml-1.0/bd/pub/corp-fin/all |
| BH | 10036430 | SCB BAHRAI*MAN | v1/14147-ebbs-/casa/scbml-1.0/bh/pub/corp-fin/all |
| BW | | | v1/14147-ebbs-/casa/scbml-1.0/bw/pub/corp-fin/all |
| CI | | | v1/14147-ebbs-/casa/scbml-1.0/ci/pub/corp-fin/all |
| GB | 400041070 | SCB TH GRP*LDN | v1/14147-ebbs-/casa/scbml-1.0/gb/pub/corp-fin/all |
| 10075222 | SCB LONDON*LDN |
| KE | 300011525 | SCB KENYA B*NBO | v1/14147-ebbs-/casa/scbml-1.0/ke/pub/corp-fin/all |
| LK | 10036647 10022098 | SCB COLOMBO*CMB SCB COL FCB*CMB | v1/14147-ebbs-/casa/scbml-1.0/lk/pub/corp-fin/all |
| MU | 400018439 | SCB MAUR*PLO | v1/14147-ebbs-/casa/scbml-1.0/mu/pub/corp-fin/all |
| NG | 300084297 | SCB NIGERIA*LAG | v1/14147-ebbs-/casa/scbml-1.0/ng/pub/corp-fin/all |
| OM | | | v1/14147-ebbs-/casa/scbml-1.0/om/pub/corp-fin/all |
| PH | 300089409 | SCB MNL FCD*MNL | v1/14147-ebbs-/casa/scbml-1.0/ph/pub/corp-fin/all |
| 10036428 | SCB MANILA*MNL |
| PK | 10036655 | SCB KARACHI*KHI | v1/14147-ebbs-/casa/scbml-1.0/pk/pub/corp-fin/all |
| QA | 300010782 | SCB DOHA*DOH | v1/14147-ebbs-/casa/scbml-1.0/qa/pub/corp-fin/all |
| SA | 400991880 | SCB SAUDI*RYD | v1/14147-ebbs-/casa/scbml-1.0/sa/pub/corp-fin/all |
| SG | 400451508 | SCB SG LTD*SIN | v1/14147-ebbs-/casa/scbml-1.0/sg/pub/corp-fin/all |
| 3 | SCB SING*SIN |
| 400452428 | SCB SG LTDACU*SIN |
| 300036368 | SCBACU*SIN |
| TZ | 10040387 | SCB TANZANI*DAR | v1/14147-ebbs-/casa/scbml-1.0/tz/pub/corp-fin/all |
| UG | 10041902 | SCB UGANDA*KAM | v1/14147-ebbs-/casa/scbml-1.0/ug/pub/corp-fin/all |
| VN | 10041530 | SCB HANOI*HNI | v1/14147-ebbs-/casa/scbml-1.0/vn/pub/corp-fin/all |
| ZM | 10041903 | SCB ZAMBIA*LUS | v1/14147-ebbs-/casa/scbml-1.0/zm/pub/corp-fin/all |
| MO | | | v1/14147-ebbs-/casa/scbml-1.0/mo/pub/corp-fin/all |
| AU | | | v1/14147-ebbs-/casa/scbml-1.0/au/pub/corp-fin/all |
| IQ | | | v1/14147-ebbs-/casa/scbml-1.0/iq/pub/corp-fin/all |
| BN | | | v1/14147-ebbs-/casa/scbml-1.0/bn/pub/corp-fin/all |
| DE | 400906330 | STAN CHART AG*FRA | v1/14147-ebbs-/casa/scbml-1.0/de/pub/corp-fin/all |
| JP | 10036382 | SCB TOKYO*TYO | v1/14147-ebbs-/casa/scbml-1.0/jp/pub/corp-fin/all |
| US | 7 | SCB NY*NY | v1/14147-ebbs-/casa/scbml-1.0/us/pub/corp-fin/all |
| NP | 400007847 | NEPAL GRINDLAYS*KTM | v1/14147-ebbs-/casa/scbml-1.0/np/pub/corp-fin/all |
| EG | 401036553 | SCB EGYPT*CAI | v1/14147-ebbs-/casa/scbml-1.0/eg/pub/corp-fin/all |
| AO | | | v1/14147-ebbs-/casa/scbml-1.0/ao/pub/corp-fin/all |
| CM | | | v1/14147-ebbs-/casa/scbml-1.0/cm/pub/corp-fin/all |
| FK | | | v1/14147-ebbs-/casa/scbml-1.0/fk/pub/corp-fin/all |
| GM | | | v1/14147-ebbs-/casa/scbml-1.0/gm/pub/corp-fin/all |
| JO | | | v1/14147-ebbs-/casa/scbml-1.0/jo/pub/corp-fin/all |
| LN | | | v1/14147-ebbs-/casa/scbml-1.0/ln/pub/corp-fin/all |
| SL | | | v1/14147-ebbs-/casa/scbml-1.0/sl/pub/corp-fin/all |
| ZW | | | v1/14147-ebbs-/casa/scbml-1.0/zw/pub/corp-fin/all |
| HK | 2 | SCB HONGKON*HKG | v1/14147-ebbs-/casa/scbml-1.0/hk/pub/corp-fin/all |

## EBBS RTA notification

- - InternalAccount RTA - Nostro Account get Debit/ Credit - CorporateFinancial RTA - Client Account get Debit / Credit

Confirmed with Deepak ,current DVP scope is external counterparty which account is held in SCB ,Ratan will only consume CorporateFinancial RTA which CreditDebitFlag=D ,if there is any cashflow only generate InternalAccount RTA will not be in scope.

## Booking Entity

Pilot countries : 6 countries to be agreed based on volumes

| FM CODE | volume | Country Code | FMID |
| --- | --- | --- | --- |
| SCB JAKARTA*JKT | 78 | ID | 8 |
| SCB HONGKON*HKG | 51 | HK | 2 |
| SCB China | 35 | CN | | FMID | FMCODE | BRANCH CODE | | --- | --- | --- | | 10020899 | SCB CHINA*NJG | 73 | | 10032025 | SCB CHINA*SZN | 73 | | 10036642 | SCB SHANGH*SHA | 73 | | 10062461 | SCB CHINA*XMN | 73 | | 10078716 | SCB CHINA*ZHU | 73 | | 235003861 | SCB CHINA*TIA | 73 | | 400001378 | SCB CHINA*BJG | 73 | | 400054708 | SCB GUANGZHOU*GZU | 73 | | 400054737 | SCB SUZHOU*SUZ | 73 | | 400054741 | SCB CHENGDU*CGD | 73 | | 400057714 | SCB QINGDAO*QDO | 73 | | 400075752 | SCB CN CHONGQING*CQG | 73 | | 400085753 | SCB CN HANGZHOU*HNZ | 73 | | 400090093 | SCB CHINA*NCG | 73 | | 400095464 | SCB CHINA DALIAN*DLN | 73 | | 400130178 | SCB CHINA HOHHOT*HHH | 73 | | 400130180 | SCB CHINA NINGBO*NGB | 73 | | 400185419 | SCB CN WUHAN*WUH | 73 | | 400193370 | SCBLXIAN*XIN | 73 | | 400209000 | SCB CN FOSHAN*FOS | 73 | | 400218197 | SCB CN JINAN BR*JNA | 73 | | 400220273 | SCB CN CHANGSHA*CGS | 73 | | 400229749 | SCB CN FUZHOU*FZH | 73 | | 400516442 | SCB CN ZHENGZHOU*ZZU | 73 | | 400516443 | SCB CN TAIYUAN*TYA | 73 | | 400667486 | SCB CN KMG*KMG | 73 | | 400677737 | SCB SHA FTU*FT2 | 73 | | 400683682 | SCB CN HRB*HRB | 73 | | 400798477 | SCB CN SYG*SYG | 73 | | 400899993 | SCB CN CHO*CHO | 73 | | 401053411 | SCB CHINA*HFI | 73 | |
| FMID | FMCODE | BRANCH CODE |
| 10020899 | SCB CHINA*NJG | 73 |
| 10032025 | SCB CHINA*SZN | 73 |
| 10036642 | SCB SHANGH*SHA | 73 |
| 10062461 | SCB CHINA*XMN | 73 |
| 10078716 | SCB CHINA*ZHU | 73 |
| 235003861 | SCB CHINA*TIA | 73 |
| 400001378 | SCB CHINA*BJG | 73 |
| 400054708 | SCB GUANGZHOU*GZU | 73 |
| 400054737 | SCB SUZHOU*SUZ | 73 |
| 400054741 | SCB CHENGDU*CGD | 73 |
| 400057714 | SCB QINGDAO*QDO | 73 |
| 400075752 | SCB CN CHONGQING*CQG | 73 |
| 400085753 | SCB CN HANGZHOU*HNZ | 73 |
| 400090093 | SCB CHINA*NCG | 73 |
| 400095464 | SCB CHINA DALIAN*DLN | 73 |
| 400130178 | SCB CHINA HOHHOT*HHH | 73 |
| 400130180 | SCB CHINA NINGBO*NGB | 73 |
| 400185419 | SCB CN WUHAN*WUH | 73 |
| 400193370 | SCBLXIAN*XIN | 73 |
| 400209000 | SCB CN FOSHAN*FOS | 73 |
| 400218197 | SCB CN JINAN BR*JNA | 73 |
| 400220273 | SCB CN CHANGSHA*CGS | 73 |
| 400229749 | SCB CN FUZHOU*FZH | 73 |
| 400516442 | SCB CN ZHENGZHOU*ZZU | 73 |
| 400516443 | SCB CN TAIYUAN*TYA | 73 |
| 400667486 | SCB CN KMG*KMG | 73 |
| 400677737 | SCB SHA FTU*FT2 | 73 |
| 400683682 | SCB CN HRB*HRB | 73 |
| 400798477 | SCB CN SYG*SYG | 73 |
| 400899993 | SCB CN CHO*CHO | 73 |
| 401053411 | SCB CHINA*HFI | 73 |
| SCB LONDON*LDN | 30 | GB | 10075222 |
| SCB KL*KUL | 16 | MY | 9 |
| SCBL*JBG | | ZA | 400032489 |

## Product

CCS

Currently our solution is to configured this product check logic in backend ,if any new product added in future ,there will be configure changed.

Murex and Stella should be covered.

Murex: 
Instrument_Common__ISDA_Taxonomy == "IRD|CS"

Stella:
Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FixedFloat"
Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis"
Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FixedFixed"
Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"

## Receive Cashflow Validation condition

- Currency
- Amount
- Payment Date

a. Check if currency /amount extracted from RTA equals to the ones query from Ratan

b. Check if payment date in Ratan <= value date in RTA<=payment date in Ratan+ 2 business day

if meet above a and b condition ,will treat this receive cashflow is the correct one , then find pay cashflow.

## Receive and Pay cashflow linkage

2026-06-26 Confirmed with Deepak

Murex :trade ID + payment date from the receive leg + payment type from receive cashflow(1st 6 characters match) to query the pay leg //**NOTE**: if payment type is null, will not include payment into the query

Stella : trade ID + major version + payment date from the receive leg + payment type from receive cashflow(1st 6 characters match) to query the pay leg

## DVP NSTP

Currently we have two DVP NSTP on production

| | Rule Id | Rule | Exception Code | Comment |
| --- | --- | --- | --- | --- |
| 1 | 7302643574521856000 | Instrument_Common__Murex_Product_Strategy in ("CCS_DVP", "CM_PMASIANFWDVP", "COM_AMES_DVP", "COM_BDF_DVP", "COM_BOE_DVP", "COM_JMUK_DVP", "COM_JMVF_DVP", "COM_LDN_DVP", "COM_OUTRGHT_DVP", "COM_RAND_DVP", "COM_SOUK_DVP", "COM_UBS_DVP", "COM_ZUR_DVP", "CR_RTM_CCS_DVP", "FX_PMTRF_DVP", "FX_TRF_DVP", "IR_AFR_DVP", "PAR FWD DVP", "PM_TRF_DVP", "PRC_OFFTAKE_DVP", "CM_PMASIANFWDP", "SGE_TRIPARTY_FW", "CCS_CORP_DVP", "CCS_FI_DVP") && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089") | DVP Strategy | 2026-06-09 Aligned during the call ,can keep the NSTP rule as is 2026-06-02 Current we can keep as is DVP NSTP rule 2026-04-20 Feedback from Deepak: 1 ) Existing NSTP rules to continue 2 ) Corporate- Both receive and pay cash flows to be NSTP 3 ) Interbank - as it will be nostro settlement, receipts can be sent as STP Deepak will check with Dinesh then come back 2026-03-20 Comment from Dinesh DVP rule to be updated as applicable only for 'Pay' so that the receive cashflows can be STP,rule may need to still be NSTP for specific countries. tbc with BAU Managers - Gunalan, Mehalai <Mehalai.Gunalan@[sc.com](http://sc.com)>; Leong, Weng Hien <WengHien.Leong@[sc.com](http://sc.com)>; Thomas, David George <Davidgeorge.Thomas@[sc.com](http://sc.com)>; Kumar, Babu <Babu.Kumar@[sc.com](http://sc.com)>; Joseph, Synthia <Synthia.Joseph@[sc.com](http://sc.com)> |
| 2 | 7207921568021745664 | Settlement_Method matches "(?i)^DVP$" | DVP | |

- - If a cashflow hits NSTP rule which the exception code in ('DVP Strategy', 'DVP'),then can be treated as cashfow has DVP exception. - In the future ,if user create a DVP exception rule , eg exception code ='DVP AAA' ,then system will not treat this as hit DVP exception.

## UI Indicator

User would like to add comment on pay cashflow when got RTA notification of receive cashflow on “Cashflow Detail” UI

1. When receive RTA notification of receive cashflow ,add comment on pay cashflow
2. Comment can be "DVP Received "like the format of exception code with green background

![image-2026-7-9_17-29-0.png](attachments/image-2026-7-9_17-29-0.png)

# Business User Case

| | Function | Scenario | Expected Result |
| --- | --- | --- | --- |
| 1 | Murex /Stella Cashflow+Scope entity+CCS+hit DVP exception+ EBBS RTA of Receive cashflow | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 | 2.C1 in ‘"Settled" status 3.Auto close DVP exception of C2 ,there is 'DVP Received' tag on the pay cashflow on the UI of 'Cashflow Details' in green background![image-2026-7-9_17-29-24.png](attachments/image-2026-7-9_17-29-24.png) |
| 2 | Murex /Stella Cashflow+not Scope entity+CCS+hit DVP exception+ EBBS RTA of Receive cashflow | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is not in 7 scope countries and not Africa country 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 | 2.C1 in "Settled "status 3.C2 still hit DVP exception if user not manually close the DVP exception |
| 3 | Murex /Stella Cashflow+Scope entity+not CCS+hit DVP exception+ EBBS RTA of Receive cashflow | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy != "IRD|CS"(Murex) or ISDA_Taxonomy not equals to Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 | 2.C1 in "Settled" status 3.C2 still hit DVP exception if user not manually close the DVP exception |
| 4 | Murex /Stella Cashflow+Scope entity+CCS+not hit DVP exception+ EBBS RTA of Receive cashflow not sure do we have this kind of scenario? | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 not hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 | 2.C1 in "Settled" status 3.C2 still in "Waiting" status if user not manually operate the cashflow |
| 5 | Murex /Stella Cashflow+Scope entity+CCS+hit DVP exception+ EBBS RTA of Pay cashflow | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status and hit DVP exception 2. User do the maker/checker on C2 and released from Ratan 3. Receive EBBS RTA notification of C2 | 2.C2 in "Settled" status 3.C1 is still in "Waiting" status if user not manually close the DVP exception |
| 6 | Murex/Stella Cashflow+Scope entity+CCS+ EBBS RTA of Receive cashflow(Pay not received in Ratan) | 1.Cashflow C1,C2 meet below conditions and C1 is received in Ratan ,C2 not received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1 "Waiting" status ,C2 should hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 4. C2 received in Ratan and in 'Waiting' status | 2.C1 in "Settled "status 3.C2 will not have DVP exception |
| 7 | Validation Condition check -Currency/Amount/Payment Date -1 | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 and meet below condition 1. Currency in RTA =Currency of C1 in Ratan 2. Amount in RTA=Amount of C1 in Ratan 3. Payment Date of C1 in Ratan <= Value Date in RTA<=Payment Date of C1 in Ratan+ 2 Business Day | 2.C1 in "Settled " status 3.Auto close DVP exception of C2 |
| 8 | Validation Condition check -Amount/Payment Date -2 | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 and meet one of the below condition 1. Amount in RTA !=Amount of C1 in Ratan 2. Value Date in RTA>Payment Date of C1 in Ratan+ 2 Business Day | 2.C1 in "Settled " status 3.C2 still hit DVP exception if user not manually close the DVP exception |
| 9 | One receive link to more than 1 pay cashflow-Split case | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User split pay cashflow into S1,S2,S3 child cashflows 3. User do the maker/checker on S1 4. User do the maker/checker on C1 and released from Ratan 5. Receive EBBS RTA notification of C1 | 2.Split child cashflow are in "Waiting" status and hit DVP exception 3.S1 in "Settled" status 4.Auto close DVP exception of S2,S3 |
| 10 | One receive link to more than 1 pay cashflow-non split case | 1.Cashflow C1,C2 meet below conditions and C1,C2,C3 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2,C3 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2,C3 in "Waiting" status ,and C2,C3 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. Receive EBBS RTA notification of C1 | 2.C1 in "Settled" status 3.C2,C3 still hit DVP exception if user not manually close the DVP exception |
| 11 | Withdrawal of Receive cashflow | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. C1 withdrawal comes 4. Receive EBBS RTA notification of original C1 | 2.C1 in "Settled" status 3.C1 in "Waiting" status 4.C2 still hit DVP exception if user not manually close the DVP exception |
| 12 | Withdrawal of Pay cashflow | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in "Waiting" status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. User do the maker/checker on C2 and released from Ratan 4. C2 withdrawal comes 5. Receive EBBS RTA notification of original C1 | 2.C1 in "Settled" status 3.C2 in "Settled" status 4.C2 in "Waiting" status 5.C2 still hit DVP exception if user not manually close the DVP exception |
| 13 | Amendment of Pay cashflow(trade id not changed) | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in 'Waiting' status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. C2 amendment happen ,new C3(original C2) received 4. Receive EBBS RTA notification of C1 | 2.C1 in ‘"Settled" status 3.C2 in "Cancelled" status ,C3 in "Waiting" status 4.Auto close DVP exception of C3 |
| 14 | Amendment of Receive cashflow(trade id not changed) | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in 'Waiting' status ,and C2 hit DVP exception 2. C1 amendment happen ,new C3(original C1) received 3. User do the maker/checker on C3 and released from Ratan 4. Receive EBBS RTA notification of C3 | 2.C1 in ‘"Cancelled" status 3.C3 in "Settled" status 4.Auto close DVP exception of C2 |
| 15 | Amendment of Pay cashflow(trade id changed) | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in 'Waiting' status ,and C2 hit DVP exception 2. User do the maker/checker on C1 and released from Ratan 3. C2 amendment happen ,new C3(original C2) received 4. Receive EBBS RTA notification of C1 | 2.C1 in ‘"Settled" status 3.C2 in "Cancelled" status ,C3 in "Waiting" status 4.C3 still hit DVP exception if user not manually close the DVP exception |
| 16 | Amendment of Receive cashflow(trade id changed) | 1.Cashflow C1,C2 meet below conditions and C1,C2 are received in Ratan 1. 1. Murex/Stella cashflow (both should be covered) 2. C1 is Receive,C2 is Pay 3. Booking entity FMID is in 7 scope countries 4. Instrument_Common__ISDA_Taxonomy == "IRD|CS"(Murex) or ISDA_Taxonomy in one of the four Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFloat" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:Basis" Instrument_Common__ISDA_Taxonomy=="InterestRate:CrossCurrency:FixedFixed" Instrument_Common__ISDA_Taxonomy =="InterestRate:CrossCurrency:FloatFloat"(Stella) 5. C1,C2 with the same tradeid/payment date (Murex),tradeid/major version/payment date(Stella) 6. C1,C2 in 'Waiting' status ,and C2 hit DVP exception 2. C1 amendment happen ,new C3(original C1) received 3. User do the maker/checker on C3 and released from Ratan 4. Receive EBBS RTA notification of C3 | 2.C1 in ‘"Cancelled" status 3.C3 in "Settled" status 4.C2 still hit DVP exception if user not manually close the DVP exception |

# Open questions

| | Questions | Answer | Status |
| --- | --- | --- | --- |
| 1 | IN corporate consume question: IN topic carries a very large data volume, which could potentially affect consumption for other queues. As confirmed with the Razor team, they consume all topics except the IN topic (v1/14147-ebbs-/casa/scbml-1.0/**in**/pub/corp-fin/all), which DVP is triggered by MT910 Can we apply the same approach? | 2026-07-16 2026-07-02 Waiting for Deepak and Dinesh to double confirm | |
| 2 | Currently we consume CorporateFinancial +D RTA ,as confrimed with Madhan, Country code in the CorporateFinancial RTA is identified of the account ![image-2026-6-26_11-17-51.png](attachments/image-2026-6-26_11-17-51.png) So, is the scope based on the booking-entity dimension, or on the country-code dimension in the received RTA? | 2026-07-02 Replied by Deepak 2026-06-26 Deepak will check with Razor and come back | |
| 3 | In the process ,it is correct to check the booking entity in 7 countries ? | 2026-07-02 Replied by Deepak 2026-06-26 if the above questioned answered ,then we can decide | |
| 4 | Because we will consume CorporateFinancial +D, but after extract RTA notification and get cashflow ,the direction is pay ,do you know any business case that pay cashflow trigger CorporateFinancial +D RTA ? ![image-2026-6-26_13-30-37.png](attachments/image-2026-6-26_13-30-37.png) ![image-2026-6-26_13-30-51.png](attachments/image-2026-6-26_13-30-51.png) add logic to filter pay cashflow when consume CorporateFinancial +D ,this is already covered in the process flow ,is that ok? | 2026-07-03 Waiting for Madhan's feedback 2026-06-26 Grace will drop an email then Deepak will help to follow up | |
| 5 | Find pay based on receive logic confirmation | 2026-06-26 Confirmed by Deepak | |
| 6 | Payment date ,any update? | 2026-07-02 2026-06-26 Deepak will help on this and come back | |
| 7 | Will cross border debit trigger EBBS RTA? | 2026-03-24 Confirmed with KEXIN, When the account opened in SCB ,will trigger EBBS RTA, no matter it is over-account or cross border debit | |
| 8 | Only internals (over-account) to be prioritized, what is the impact for Ratan? | 2026-03-20 No need to check settlement means=Over-Account in Ratan flow | |
| 9 | When a CCS /DVP trade booked ,is that the pay/receive cashflow with the same Settlement Method/Product_Strategy? And pay/receive cashflow will hit the same DVP exception? | 2026-03-20 Yes ,pay and receive with the same Settlement Method/Product_Strategy As Dinesh mentioned need to update existing DVP rule to support only pay cashflow ,so that receive will not hit DVP exception | |
| 10 | if a receive cashflow ,settlement means is over-account ,is that pay is over-account as well? | 2026-03-20 No,pay and receive may have different settlement means | |
| 11 | How to find the pay cashflow based on receive cashflow? can we use tradeid, tradeVersion, paymentDate, any other condition? | 2026-03-24 Checked with Kexin ,high level process in Razor when they receive RTA, find tag20(narration1-6),and get the receive cashflow id ,then use ccy ,amount ,value date to validate if it is the correct/same receive cashflow in Razor, then use contract id to find the pay cashflow and auto DVP 2026-03-20 It is OK ,but can check with Razor how they find the pay cashflow based on receive | |
| 12 | Is there any possibility that there are more than two pairs of pay/receive with the same payment date under a same trade id ? | 2026-03-24 Checked some data, found that there are more than one pair of pay/receive cashflow under the same trade id with the same payment date ,but there is only one pair of pay/receive under the same trade id /trade version/payment date 2026-03-20 Should consider ND CCS .need to be checked . For net resultant, if one of the cashflows is DVP, then net resultant should be considered as DVP | |
| 13 | Receive cashflow reached to release cutoff but not settled -Auto failed , generate accounting, will EBBS trigger RTA? if trigger, auto close DVP exception of the pay cashflow ,but is this expected to receive RTA notification from user perspective? if not trigger ,will not auto close DVP ,need user to manually close DVP exception | 2026-03-20 In this case ,EBBS will not trigger RTA ,so Ratan will not auto close DVP exception for pay cashflow ,need ops to manually close the DVP exception | |
| 14 | Not sure if EBBS will trigger RTA for pay cashflow? If Ratan receive SCB pay cashflow RTA ,what is the expectation ? if pay cashflow RTA trigger ,system will auto close DVP exception of receive cashflow, is this expected ? | 2026-03-20 Pay cashflow may trigger RTA notification ,when system receive pay RTA notification ,do nothing | |
| 15 | What is the auto DVP process in Razor? | 2026-02-25 Trade is booked as DVP settlement method Pay and receive are sent to different queues based on downstream feed (Hogan / EBBS), the receipt is updated as SETTLED, which triggers auto release of payment | |
| 16 | What the differences between the two samples? | 2026-02-25 a) EBBS Alert RTA, b) Swift(MT910, CAMT054) **RTA Types** Internal RTA - Nostro Account get Debit/ Credit (used only for SG) CorporateFinancial - Client Account get Debit / Credit (used for all non SG) Confirmation of Client account debit is also used to automate DVP since in some countries we do not get Internal RTA | |
| 17 | What the key information are from EBBS feed that could be used to link to DVP cashflows ? | 2026-02-25 Country, Value Date, CCY, Amount, Direction, Reference (in Narration 1 - 6). Value date is not part of criteria since in some africa countries the value date is different (cashflow VD is 25 Jan but client account debit is on 26 Jan) In some countries, same reference captured in 2 fields In some cases the field where the field 20 field is captured previously in a field (example Narration 2, but during SCPAY migration it changed to Narration 4) so we need to ensure to scan all Narration fields | |
| 18 | Are the notification from EBBS are all related to DVP? | 2026-02-25 They are not all related to DVP | |
| 19 | Is there any case that Razor receive notifications from EBBS more than one time for the same cashflow? | 2026-02-25 There is no duplication of same RTA observed in RAZOR BAU, but RAZOR has a logic to filter out duplicates based on Narration | |
| 20 | Brief introduce the workflow how to generate RTA? | 2026-05-26 Any credit or debit transaction will trigger RTA | |
| 21 | When will trigger CorporateFinacial ? | 2026-05-27 Confirmed with Nick ,no need to check 2026-05-26 Need check with cache system | |
| 22 | When will trigger InternalAccount ? | 2026-05-27 Confirmed with Nick ,no need to check 2026-05-26 Need check with cache system | |
| 23 | How to define if an account is internal account or corporate account ? | 2026-05-27 Confirmed with Nick ,no need to check 2026-05-26 Need check with cache system | |
| 24 | Is there any country account only generate corporate RTA or only generate internal RTA? what is the case? | 2026-05-27 Confirmed with Nick ,no need to check2026-05-26 Need check with cache system | |
| 25 | Withdraw event ,EBBS will trigger RTA or not ？ | 2026-05-20 Feedback from Madhankumar Hi Grace, With reference to real-time alert notifications for an account, all debit and credit transactions will indeed trigger notifications. Additionally, if you need to check specific transaction details, you can refer to the channel ID associated with each notification. 2026-05-15 Ask ebbs for help,waiting their response | |
| 26 | If withdraw trigger RTA , the creditdebit flag will be opposite? eg New--CorporateFinacial+D Withdraw-CorporateFinacial+C? | 2026-05-26 confrimed with Madhankumar,yes | |
| 27 | Is there any indicator in RTA to identify if it is a new event or withdraw event | 2026-05-26 Need to check specific RTA | |
| 28 | Is there any indicator to mention the pay cashflow is waiting for RTA to close the DVP after receive cashflow released to downstream | 2026-06-02 Confirmed with Deepak,we can ignore this first ,later if user have this kind of requirement ,then can further discuss 2026-04-10 Deepak mentioned will check and come back 2026-04-02 The effort is big ,what's the scenario for this requirement ? any business benefit? | |

# Future Enhancement

Below items not required in day1, please consider the solution to be able to extend with below functions.

| | Description | Comment |
| --- | --- | --- |
| 1 | More countries and products to be supported in future | This should be considered in the solution design |
| 2 | Cross border debit and client account held with external bank to be supported in future | Solution to consider support for cross border debit and MT910 |

# Related documentation

[Cash Settlements Day 2 - 2026 Prioritized list - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Cash+Settlements+Day+2+-+2026+Prioritized+list)

[Auto DVP Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Auto+DVP+Technical+Design)

DVP volume

Volume of hit DVP NSTP rule for last one year

<details>
<summary>Expand Details</summary>

| FMID | FMCODE | COUNT | CURRENCY |
| --- | --- | --- | --- |
| 5 | SCB DUBAI*DUB | 14110 | AED,CNH,USD,XAG,XAU,XG2,XPT,XU2,XU3 |
| 10075222 | SCB LONDON*LDN | 6245 | CHF,EUR,GBP,HKD,INO,JPY,KRO,NGX,PHO,PHP,USD,XAG,XAU,XG2,XG3,XG4,XG7,XPD,XPT,XRH,XU1,XU2,XU3,XU4,XU5,XU7,ZAR,ZMW |
| 2 | SCB HONGKON*HKG | 2957 | CNH,EUR,HAU,HKD,USD,XAG,XAU,XG2,XPD,XPT |
| 4 | SCB BOMBAY*MMB | 1352 | CHF,EUR,INO,INY,JPY,USD |
| 400452428 | SCB SG LTDACU*SIN | 1065 | AUD,CNH,EUR,JPY,THO,USD,XAG,XAU,XG7,XU1,XU5 |
| 400960089 | GIFT CITY TM*MUM | 882 | CHF,USD,XAU |
| 8 | SCB JAKARTA*JKT | 431 | CNH,IDO,IDR,JPY,USD |
| 10036428 | SCB MANILA*MNL | 110 | PHO,USD |
| 9 | SCB KL*KUL? | 72 | EUR,MYO,USD |
| 400677737 | SCB SHA FTU*FT2 | 56 | CNH,EUR,HKD,JPY,USD |
| 10036642 | SCB SHANGH*SHA | 55 | CNO,USD |
| 400032489 | SCBL*JBG | 44 | EUR,USD,ZAR |
| 10038345 | SCB TAIPEI*TPE | 30 | EUR,TWO |
| 6 | SCB BANGKOK*BKK | 27 | JPY,THO,USD |
| 400054741 | SCB CHENGDU*CGD | 24 | CNO,USD |
| 400075752 | SCB CN CHONGQING*CQG | 24 | CNO,HKD |
| 400193370 | SCBLXIAN*XIN | 12 | CNO,HKD |
| 400045551 | SCB DUBAI DFC*DUB | 6 | USD,XAU |
| 400018439 | SCB MAUR*PLO | 1 | USD |
| 400085753 | SCB CN HANGZHOU*HNZ | 1 | USD |
| 400906330 | STAN CHART AG*FRA | 1 | EUR |

**SELECT** entity_fmid, entity_fmcode , **COUNT**(*) **FROM** ratan_cashflow_lifecycle_service.ratan_stella_message_event_source rsmes **WHERE** cashflow_id **IN** (

**SELECT** **DISTINCT** entity_id **FROM** ratan_rule_service.ratan_rule_exception **WHERE** exception_code **IN** (**'DVP Strategy'**, **'DVP'**) **and** created_at > **'2025-07-01'**

) **GROUP** **BY** entity_fmid, entity_fmcode  ;

</details>

<details>
<summary>Expand Details</summary>

Murex:

eg Murex ,original trade id ='102256990' , looks C1-M00125257530 and C2-M00125696545 is a pair ,later , C2 withdrawal and C3 -M00126181149 comes， C1 and C3 is a pair, but the tradeid of C3 changed（108345837） ,so if we use tadeid of C1(102256990) ,will not find C3,original trade id not changed ,so maybe we need to use original trade id to find pay cashflow ,so we need to use trade version/original trade id /paymentdate of the receive cashflow to find pay cashflow

![image-2026-6-9_13-37-21.png](attachments/image-2026-6-9_13-37-21.png)

![image-2026-6-8_9-42-35.png](attachments/image-2026-6-8_9-42-35.png)

![image-2026-6-8_9-42-50.png](attachments/image-2026-6-8_9-42-50.png)

![image-2026-6-8_9-43-14.png](attachments/image-2026-6-8_9-43-14.png)

![image-2026-6-8_11-23-3.png](attachments/image-2026-6-8_11-23-3.png)

for stella, if amount amendment happen, major version not changed ,trade id not changed ,so maybe can use tradeid /major version/payment date of the receive cashflow to find pay cashflow

![image-2026-6-9_13-37-55.png](attachments/image-2026-6-9_13-37-55.png)

![image-2026-6-8_14-3-48.png](attachments/image-2026-6-8_14-3-48.png)

![image-2026-6-8_14-4-0.png](attachments/image-2026-6-8_14-4-0.png)

</details>

<details>
<summary>Expand Details</summary>

**SELECT** entity__counterparty_sci_fmid **FROM** cash_settlement_query_cn.cashflow_data *cd*

**WHERE** cashflow__pay_receive_indicator = **'Receive'**

**and** ssi__account__scb_nostro_account_type =**'Over-Account'**

**and** cashflow_index **in** (

**SELECT** entity_id **FROM** ratan_rule_service.ratan_rule_exception *rre* **WHERE** exception_code **IN** (**'DVP Strategy'**, **'DVP'**)

);

📎 [Copy of cashflow_data_202605210939.csv](attachments/Copy of cashflow_data_202605210939.csv)

SELECT entity__counterparty_sci_fmid, entity__counterparty_sci_fmcode FROM cash_settlement_query_cn.cashflow_data cd

WHERE cashflow__pay_receive_indicator = 'Receive'

and cashflow_index in (

SELECT entity_id FROM ratan_rule_service.ratan_rule_exception rre WHERE exception_code IN ('DVP Strategy', 'DVP')

);

📎 [cashflow_data_202605210952.csv](attachments/cashflow_data_202605210952.csv)

2.Netting Resultant

EBBS send Netting Resultant RTA

| Scenario | Netting Resultant | Murex_product_strategy | Pay/Receive | Component | Trade id | Murex_product_strategy | Pay/Receive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scenario 1 | N00000253220 | COM_RAND_DVP | Pay | M00125503871 | 107717841 | COM_RAND_DVP | Pay |
| M00125502947 | 107716069 | COM_RAND_DVP | Pay |
| Scenario 2 | N00000287213 | COM_OUTRGHT_DVP | Pay | M00125749322 | 107983169 | COM_OUTRGHT_DVP | Pay |
| M00125735098 | 107965331 | COM_OUTRGHT_DVP | Pay |
| M00125786937 | 108023067 | COM_OUTRGHT_DVP | Receive |
| Scenario 3 | N00000256555 | CR_RTM_CCS_DVP | Receive | M00124833580 | 106323276 | CR_RTM_CCS_DVP | Pay |
| M00124833551 | 106308411 | CR_RTM_CCS_DVP | Pay |
| M00124726540 | 106323275 | CR_RTM_CCS_DVP | Receive |
| M00124726534 | 106308410 | CR_RTM_CCS_DVP | Receive |
| Scenario 4 | N00000270708 | CCS_DVP | Receive | M00124725693 | 89905568 | CCS_DVP | Receive |
| M00124725691 | 89905539 | CCS_DVP | Receive |

Note:Some Netting resultant cashflow are netted by hundreds of component cashflow ,need to consider the performance .

3.Split Cashflow

EBBS send Split Cashflow RTA

</details>