This document is base on [FMRP - SSI Stamping Flow] and existing validation rule.

# Validation Rule

| Label | Name | Mandatory | Length | Format | Format Pattern | Scope |
| --- | --- | --- | --- | --- | --- | --- |
| 57a: Account With Institution/Account | accountWithInstitutionAccount | swiftType = MT103 and tradingCurrency = RUB | ?? | ?? | ?? | Vostro |
| 57a: Account With Institution/Address | accountWithInstitutionAddress | | 0 to 60. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,60}$ | Vostro |
| 57a: Account With Institution/BIC | accountWithInstitutionBic | swiftType = MT103 | 8 or 11. | Upper Case Alpahbet or number. | ^(([A-Z0-9]{8})|([A-Z0-9]{11}))$ | Vostro |
| 57a: Account With Institution/Country | accountWithInstitutionCity | | | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,}$ | Vostro |
| 57a: Account With Institution/Full Name | accountWithInstitutionName | | 0 to 35. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,35}$ | Vostro |
| 58a/59: Beneficiary Customer/Account | beneficiaryAccount | swiftType = MT103 or (swiftType = MT202 and settlementMeans = Over-Account) | 2 to 34. | Alphabet, number, space. | ^[A-Za-z0-9\s]{2,34}$ | Vostro |
| 58a/59:Beneficiary Customer/Address | beneficiaryAddress | swiftType = MT103 | 0 to 60. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,60}$ | Vostro |
| 58a/59:Beneficiary Customer/BIC | beneficiaryBic | swiftType = MT202 and beneficiaryName = "" | 8 or 11. | Upper Case Alpahbet or number, | ^(([A-Z0-9]{8})|([A-Z0-9]{11}))$ | Vostro |
| 58a/59:Beneficiary Customer/Country | beneficiaryCity | | | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,}$ | Vostro |
| 58a/59:Beneficiary Customer/Full Name | beneficiaryName | swiftType = MT202 and beneficiaryBic = "" | 0 to 35. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,35}$ | Vostro |
| 58a/59:Beneficiary Customer/Full Name1 | beneficiaryName2 | | 0 to 35. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,35}$ | Vostro |
| 58a/59:Beneficiary Customer/Charges | charges | swiftType = MT103 | | Only OUR/SHA/BEN | ^(OUR)|(SHA)|(BEN)$ | Vostro |
| eBBS information/Account | ebbsNostroAccount | TRUE | | | .{1,} | Nostro |
| 56a: Intermediary Institution/Address | intermediaryAddress | | 0 to 60. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,60}$ | Vostro |
| 56a: Intermediary Institution/BIC | intermediaryBic | | 8 or 11. | Upper Case Alpahbet or number. | ^(([A-Z0-9]{8})|([A-Z0-9]{11}))$ | Vostro |
| 56a: Intermediary Institution/Full Name | intermediaryName | | 0 to 35. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,35}$ | Vostro |
| 56a: Intermediary Institution/Country | intermediaryPostcode | | | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,}$ | Vostro |
| 56a: Intermediary Institution/Account | intermediaryAccount | | ?? | ?? | | Vostro |
| 50/52a: Ordering Institution/Account | orderCustomerAccount | swiftType = MT103 | 1 to 50. | Alphabet, number, space. | ^[A-Za-z0-9\s]{1,50}$ | Vostro |
| 50/52a: Ordering Institution/Address | orderCustomerAddress | swiftType = MT103 | 0 to 60. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,60}$ | Vostro |
| 50/52a: Ordering Institution/Country | orderCustomerCity | | | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,}$ | Vostro |
| 50/52a: Ordering Institution/Full Name | orderCustomerName | swiftType = MT103 | 0 to 70. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,70}$ | Vostro |
| 50/52a: Ordering Institution/BIC | orderCustomerBic | | ?? | ?? | | Vostro |
| 54a: Receiver's Correspondent/Address | receiversCorrespondentAddress | | 0 to 60. | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,60}$ | Vostro |
| 54a: Receiver's Correspondent/BIC | receiversCorrespondentBic | swiftType = MT103 & settlementMeans = NOS & coveredPayment = Y | 8 or 11. | Upper Case Alpahbet or number. | ^(([A-Z0-9]{8})|([A-Z0-9]{11}))$ | Vostro |
| 54a: Receiver's Correspondent/Country | receiversCorrespondentCity | | | Alphabet, number, space. | ^[A-Za-z0-9\s]{0,}$ | Vostro |
| 54a: Receiver's Correspondent/Full Name | receiversCorrespondentName | | 0 to 35. | Alphabet, number, space. | ^[\w\s]{0,35}$ | Vostro |
| 54a: Receiver's Correspondent/Account | receiversCorrespondentAccount | | ?? | ?? | | Vostro |
| 70: Remittance Inform/Line 1 | remittanceInformation1 | | 0 to 35. | | ^.{0,35}$ | Vostro |
| 70: Remittance Inform/Line 2 | remittanceInformation2 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 70: Remittance Inform/Line 3 | remittanceInformation3 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 70: Remittance Inform/Line 4 | remittanceInformation4 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 72: Sender To Reciever/Line 1 | senderToReceiver1 | | 0 to 35. | | ^.{0,35}$ | Vostro |
| 72: Sender To Reciever/Line 2 | senderToReceiver2 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 72: Sender To Reciever/Line 3 | senderToReceiver3 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 72: Sender To Reciever/Line 4 | senderToReceiver4 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 72: Sender To Reciever/Line 5 | senderToReceiver5 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 72: Sender To Reciever/Line 6 | senderToReceiver6 | | 0 to 33. | | ^.{0,33}$ | Vostro |
| 77: Purpose of Payment | popDubai | swiftType = MT103 & entity fmid = 5 & tradingCurrency != AED & settlementMeans = "NOS" & settlement account contains "MAIN" & beneficiary Bic != "SUPPRESSXXX" | 0 to 90 | | ^.{0,90}$ | Vostro |
| Settlement Account | settlementAccount | Always Mandatory | 0 to 20 | | ^.{0,20}$ | Vostro |
| Settlement Means | settlementMeans | Always Mandatory | | Only CLG/CLS SUSP/CPN SUSP/FATCASUS/FXBRREC/GBFXSUS/HKCT/HKNOTE/MMSUS/NOSCENT/Non-Nostro/Nostro/Over-Account/TBFXSUS/WMSUS allowed | ^(CLG)|(CLS SUSP)|(CPN SUSP)|(FATCASUS)|(FXBRREC)|(GBFXSUS)|(HKCT)|(HKNOTE)|(MMSUS)|(NOSCENT)|(Non-Nostro)|(NOS)|(Over-Account)|(TBFXSUS)|(WMSUS)$ | Vostro |
| SSI Type | ssiType | Always Mandatory | | Only Primary/Secondary allowed | ^(Primary)|(Secondary)$ | Vostro |
| Msg | swiftType | Always Mandatory | | Only MT103/MT103 SERIAL/MT202 | ^(MT103)|(MT103 SERIAL)|(MT202)$ | Vostro |
| Covered Payment | coveredPayment | | | Only Y/N | | Vostro |
| TPP | isThirdPartyPayment | | | Only Y/N | | Vostro |

## Legends

**Red ??** means not covered by SSI Stamping document nor in existing validation rules.
**Mandatory** means force to fill in, not allow empty value    
**Length** and **Format** means once fill in, should follow the rule

## Covered Payment

if Msg is MT103 and Settlement Means is NOS and Covered Payment is True (ticked from UI), then 54a: Receivers Correspondent BIC should be mandatory.
if Msg is MT103 and Settlement Means is NOS and 54a: Receivers Correspondent BIC filled with correct format, then Covered Payment checkbox should be always ticked (Manual Untick should be revert).

## Purpose of Payment

When popDubai is mandatory, it will appears on the form, otherwise it will hide.