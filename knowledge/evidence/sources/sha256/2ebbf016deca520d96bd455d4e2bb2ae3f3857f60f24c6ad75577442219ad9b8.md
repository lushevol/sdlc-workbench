## Murex Vostro Screen

![image2022-10-26_14-25-48.png](attachments/image2022-10-26_14-25-48.png)

## BCS RATAN Vostro Screen

![image2022-10-27_15-43-21.png](attachments/image2022-10-27_15-43-21.png)

## CMS Account Holder

This tick box indicate CMS flag, which impact mt103/mt202/mt210/mtX92 on some of swift tags.

| | MT103_CMS | MT103 |
| --- | --- | --- |
| Header Block2- Receiver BIC | Account holder BIC (SWIFT_ACHL) | IF (FIN_COPY is blank) THEN Counterparty BIC OTHERWISE IF intermediary Code is NOT blank THEN intermediary Code OTHERWISE Account holder BIC (SWIFT_ACHL) |
| 26T - Transaction Type Code | NA | Applicable. value as :26T:TOF for AED payment |
| 53 - Sender's Correspondent | For China entity IF (CMS Account Number NOT blank) THEN **53a:line1= CMS Account number **line2= our entity BIC OTHERWISE 53a line1=entity swift code | not rely on CMS Account number |
| 56 | NA | Applicable |
| 57 - Account With Institution | CMS Flag don't impact mt103. only affect mt210 | not rely on CMS Flag |
| 72 - Sender to Receiver | IF CMS_FLAG=Y IF (entity=JAKARTA AND product in (NDF,IRS,CS,FXO)) THEN has special logic for different product on F72 OTHERWISE combination of SNDREC1~6 line1:SNDREC1 line2:SNDREC2 line3:SNDREC3 line4:SNDREC4 line5:SNDREC5 line6:SNDREC6 | IF CMS_FLAG <> Y IF (entity=JAKARTA AND CCY= IDR/IRO/IRY AND product in (NDF,IRS,CS,FXO)) THEN has special logic for different product on F72 OTHERWISE combination of SNDREC1~6 line1:SNDREC1 line2:SNDREC2 line3:SNDREC3 line4:SNDREC4 line5:SNDREC5 line6:SNDREC6 |
| 77b | CMS Flag only affect DUBAI entity | not rely on CMS Flag |

| | MT202_CMS | MT202 |
| --- | --- | --- |
| Header Block2- Receiver BIC | Our entity BIC | IF (FIN_COPY is blank) THEN Correspondent's BIC ( ie.Nostr filed 53 Corr.Code) OTHERWISE IF intermediary Code is NOT blank THEN intermediary Code OTHERWISE Account holder BIC (SWIFT_ACHL) |
| 53 - Sender's Correspondent | For China entity IF (CMS Account Number NOT blank) THEN **53a:line1= CMS Account number** line2= our entity BIC OTHERWISE 53a line1=our entity BIC | not rely on CMS Account number |
| 72 - Sender to Receiver | IF CMS_FLAG=Y IF (entity=JAKARTA AND product in (NDF,IRS,CS,FXO)) THEN has special logic for different product on F72 OTHERWISE combination of SNDREC1~6 line1:SNDREC1 line2:SNDREC2 line3:SNDREC3 line4:SNDREC4 line5:SNDREC5 line6:SNDREC6 | IF CMS_FLAG<>Y IF (entity=JAKARTA AND CCY= IDR/IRO/IRY AND product in (NDF,IRS,CS,FXO)) THEN hardcode :[72:/TTC/103](http://72/TTC/103) OTHERWISE combination of SNDREC1~6 line1:SNDREC1 line2:SNDREC2 line3:SNDREC3 line4:SNDREC4 line5:SNDREC5 line6:SNDREC6 |

## MT202 Field 58a: Beneficiary Institution

58 only applicable to mt202

Red highlights mean value come from murex GUI

| IF Beneficiary(58) is NOT populated IF ctp BIC is blank AND Beneficiary A/C is blank THEN 58D:Ctp LongName OTHERWISE line1 58D:Beneficiary A/C line2 Ctp LongName IF ctp BIC is NOT blank AND Beneficiary A/C is blank THEN 58A:Ctp BIC OTHERWISE line1 58A:Beneficiary A/C line2 Ctp BIC |
| --- |

| IF Beneficiary(58) is populated IF Beneficiary(58)'s BIC is blank AND Beneficiary A/C is blank THEN 58D:Beneficiary(58)'s LongName OTHERWISE line1 58D:Beneficiary A/C line2 Beneficiary(58)'s LongName IF Beneficiary(58)'s BIC is NOT blank AND Beneficiary A/C is blank THEN 58A:Beneficiary(58)'s BIC OTHERWISE line1 58A:Beneficiary A/C line2 Beneficiary(58)'s BIC |
| --- |

## Murex Product vs. CFI Code

IRD|IRS

IRD|CCS

IRD|LNBR

CURR|FXD|FXD

etc.