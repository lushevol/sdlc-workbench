# SCT

| HKCS Test Guide | S/N | Testing Scope | Responsible Team: | Detailed Execution Steps | Test Evidence | Test Status | Sent to LMS? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.1 | Single Credit Transfer (Sell Side) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I604BKCHHKH0XGSIN}{3:{108:RXL2309262976804}}{4: :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:260925 :20:DV60M00128901997 :21:DV60M00128901997 :23:TRANSFER :32F:FOZ10, :82A:SCBLHKH0XXX :87A:BKCHHKH0XXX :88A:BKCHHKH0XXX :[72:/ACC/SCRTRF](http://72/ACC/SCRTRF) -} | ![image-2026-9-29_13-52-47.png](attachments/image-2026-9-29_13-52-47.png) ![image-2026-9-29_13-56-28.png](attachments/image-2026-9-29_13-56-28.png) | |
| 1.2 | GBS Deriv Setts | - GBSDerivSetts to release MT604. | |
| 1.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | |
| 1.4 | CTMU | - On VD, CTMU to receive MT606 Completion Advice - On VD, CTMU to receive MT608 EOD Balance Statement with correct balance | |
| 2 | 2.1 | Single Credit Transfer (Buy Side) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I605BKCHHKH0XGSIN}{3:{108:RXL2309262976867}}{4: :20:DV60M00128901999 :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:260925 :21:DV60M00128901999 :23:TRANSFER :32F:FOZ10, :82A:BKCHHKH0XXX :87A:BKCHHKH0XXX :88A:SCBLHKH0XXX :[72:/ACC/SCRTRF](http://72/ACC/SCRTRF) -} | |
| 2.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | |
| 2.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | |
| 2.4 | CTMU | - On VD, CTMU to receive MT607 Completion Advice - On VD, CTMU to receive MT608 EOD Balance Statement with correct balance | |
| 3 | 3.1 | Physical Withdrawal | CTMU | 1. CTMU PM to send Load Out (Appendix E ) Email to BOC HK at least 3 days before physical withdrawal. 2. Designated vault advises booking # and details via email. 3. CTMU PM sends Appendix F to BOC HK on email 4. CTMU PM sends MT604 to BOC HK with time and date of email in #4 and expect to receive MT699. 5. VD: CTMU expect to receive MT606 Completion Advice once withdrawal has completed. | | | |
| 4 | 4.1 | Physical Deposit | CTMU | 1. CTMU PM to send Load In (Appendix C) Email to BOC HK at least 2 day before physical deposit. 2. Designated vault advises booking # and details via email. 3. CTMU PM to send Appendix D - Template of Security Transport of Physical form to Designated vault by email. 4. CTMU PM sends MT605 to BOC HK with time and date of email in #4 and expect to receive MT699. 5. CTMU PM sends MT699 to test for Change on Security Transport (refer to #8) to change Security Transport details. 6, Expect to receive MT699 Confirmation Advice on Change of Security Personnel. 7. VD: CTMU expect to receive MT607 Completion Advice once deposit has completed. | | | |
| 5 | 5.1 | Real Time Balance Enquiry | CTMU | - CTMU to Send MT699 for Balance Enquiry and expect to receive MT699 response with the expected balance | | | |
| 6 (A) | 6.A.1 | Cancellation - SCT (Sell) | Middle Office | - Middle Office to book test trade | | | |
| 6.A.2 | GBS Deriv Setts | - GBSDerivSetts to release MT604. | | | |
| 6.A.3 | Middle Office | - Middle Office to cancel test trade upon release of MT604. | | | |
| 6.A.4 | GBS Deriv Setts | - GBSDerivSetts to release MT692 Request for Cancellation | | | |
| 6.A.5 | CTMU | - CTMU expect to receive MT696 Cancellation Advice '- On VD, no expected changes in balances. | | | |
| 6 (B) | 6.B.1 | Cancellation - SCT (Sell) | Middle Office | - Middle Office to book test trade | | | |
| 6.B.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605. | | | |
| 6.B.3 | CTMU | - CTMU to sight MT699 Match Advice before value date. | | | |
| 6.B.4 | Middle Office | - Middle Office to cancel test trade upon CTMU's confirmation on MT699 receipt | | | |
| 6.B.5 | GBS Deriv Setts | - Before VD, GBSDerivSetts to release MT692 Request for Cancellation upon CTMU's request. | | | |
| 6.B.6 | CTMU | - CTMU expect to receive MT696 Cancellation Advice '- On VD, no expected changes in balances. | | | |
| 6 (C ) | 6.C.1 | Cancellation - Deposit | CTMU | 1. CTMU PM to send Load In (Appendix C) Email to BOC HK 3 days before physical deposit. 2. Designated vault advises booking # and details via email. 3. CTMU PM to send Appendix D - Template of Security Transport of Physical form to Designated vault by email. 4. CTMU PM sends MT605 to BOC HK with time and date of email in #4 and expect to receive MT699. 5. CTMU PM sends MT692 to Request for Cancellation of Deposit 6. Expect to receive MT696 confirming Cancellation is successfully processed. | | | |
| 6(D) | 6.D.1 | Cancellatiion - Withdrawal | CTMU | 1. T: CTMU PM to send Load Out (Appendix E ) Email to BOC HK at least 2 days before physical withdrawal. 2. T: Designated vault advises booking # and details via email. 3. CTMU sends Appendix F on email to BOC HK. 4. T: CTMU PM sends MT604 to BOC HK with time and date of email in #4 and expect to receive MT699. 5. T+1: CTMU sends MT692 for cancellation 6. Expect to receive MT696 confirming Cancellation is successfully processed. | | | |
| 7 | 7.1 | Change of Security Transport | CTMU | Full Acceptance 1. CTMU PM to send Load In (Appendix C) Email to BOC HK 3 days before physical deposit. 2. Designated vault advises booking # and details via email. 3. CTMU PM to send Appendix D - Template of Security Transport of Physical form to Designated vault by email. 4. Prior to VD, CTMU PM sends MT699 for Change on Security Transport and expect to receive MT699 Confirmation Advice in return. 5. VD: CTMU expect to receive MT607 Completion Advice once deposit has completed. | | | |
| 8 | 8.1 | Monthly Report Download | CTMU | - Successfully download monthly fee report from SI's File Transfer Gateway (FTG) | | | |
| 9 (A) | 9.A.1 | Fee payment to SI | CTMU | - Receipt of Fee Advices from BOC HK | | | |
| 9.A.2 | Middle Office | - CTMU to instruct Middle Office to book fees into Murex for payment | | | |
| 9.A.3 | GBS Deriv Setts | - Release payment of fees to SI and Designated Vault via HKD Chats | | | |
| 9 (B) | 9.B.1 | Fee payment to Designated Vault | CTMU | - Receipt of Fee Advices from BOC HK | | | |
| 9.B.2 | Middle Office | - CTMU to instruct Middle Office to book fees into Murex for payment | | | |
| 9.B.3 | GBS Deriv Setts | - Release payment of fees to SI and Designated Vault via HKD Chats | | | |
| 10 | 10.1 | Daily statement of unallocated PM account | CTMU | - Successfully received the MT608 daily statement of unallocated PM account | | | |
| 11 | 10.1 | Daily statement of unallocated PM account 01 Oct Holiday | CTMU | - Expect to not receive any return response. | | | |

# DVP

| HKCS Test Guide | S/N | Testing Scope | Responsible Team: | Detailed Execution Steps | Test Evidence | Test Status | Sent to LMS? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.1 | DvP Transfer (by Paying DP = SCB ) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I604BKCHHKH0XGSIN}{3:{108:RXL2409262979671}}{4: :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:260928 :20:DV60M00128902005 :21:DV60M00128902005 :23:TRANSFER :32F:FOZ10, :82A:SCBLHKH0XXX :87A:BKCHHKH0XXX :88A:BKCHHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/HKD341434,90/ -} | | |
| 1.2 | GBS Deriv Setts | - GBSDerivSetts to release MT604 on DVP terms | |
| 1.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | |
| 1.4 | HK Cash | - By VD, HK Cash team to confirm receipt of Credit Advice pacs.009 from RTGS | |
| 1.4 | CTMU | - On VD, CTMU to receive MT606 Completion Advice - On VD, CTMU to receive MT608 EOD Balance Statement with correct balance | |
| 2 | 2.1 | DvP Transfer (by Receiving DP = SCB ) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I605BKCHHKH0XGSIN}{3:{108:RXL2409262979670}}{4: :20:DV60M00128902007 :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:260928 :21:DV60M00128902007 :23:TRANSFER :32F:FOZ15, :82A:BKCHHKH0XXX :87A:BKCHHKH0XXX :88A:SCBLHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/USD65286,00/ -} | | |
| 2.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | |
| 2.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | |
| 2.4 | HK Cash | - By VD, HK Cash team to receive HKCS Payment Notification (pain.001) from RTGS '- On VD, HK Cash team to receive debit advice (camt.054) from RTGS | |
| 2.5 | CTMU | - On VD, CTMU to receive MT607 Completion Advice - On VD, CTMU to receive MT608 EOD Balance Statement with correct balance | |
| 3 | 3.1 | DvP Transfer (by Paying DP = SCB ) Forward Date | Middle Office | - Middle Office to book test trade | | | |
| 3.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | | | |
| 3.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | | | |
| 3.4 | HK Cash | - By VD, HK Cash team to receive HKCS Payment Notification (pain.001) from RTGS - On VD, HK Cash team to receive debit advice (camt.054) from RTGS | | | |
| 3.5 | CTMU | - On VD, CTMU to receive MT607 Completion Advice - On VD, CTMU to receive MT608 EOD Balance Statement with correct balance | | | |
| 4 | 4.1 | DvP Transfer (by Receiving DP = SCB ) Forward Date | Middle Office | - Middle Office to book test trade | | | |
| 4.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | | | |
| 4.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | | | |
| 4.4 | HK Cash | - By VD, HK Cash team to receive HKCS Payment Notification (pain.001) from RTGS '- On VD, HK Cash team to receive debit advice (camt.054) from RTGS | | | |
| 4.5 | CTMU | - On VD, CTMU to receive MT607 Completion Advice - On VD, CTMU to receive MT608 EOD Balance Statement with correct balance | | | |

# Cancellation

| HKCS Test Guide | S/N | Testing Scope | Responsible Team: | Detailed Execution Steps | Test Evidence | Test Status | Sent to LMS? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.1 | Cancellation on DvP Transfer (by Paying DP = SCB ) (by Sending DP via MT692 to HKCS before successful match) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I604BKCHHKHHXGSIN}{3:{108:jycMPshw5VrpbvrA}}{4: :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:260930 :20:DV60M00128902015 :21:DV60M00128902015 :23:TRANSFER :32F:FOZ30, :82A:SCBLHKH0XXX :87A:BKCHHKH0XXX :88A:BKCHHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/HKD1024304,70/ -} {1:F01SCBLHKH0AXXX0000000000}{2:I692BKCHHKHHXGSIN}{3:{108:Hey4hZ1gd4Ozz5z3}}{4: :20:CANCM00128902015 :21:DV60M00128902015 :11S:604 260928 :[79:/HONGKONG/UNALLGOLD995+](http://79/HONGKONG/UNALLGOLD995+) :30:260930 :20:DV60M00128902015 :21:DV60M00128902015 :23:TRANSFER :32F:FOZ30, :82A:SCBLHKH0XXX :87A:BKCHHKH0XXX :88A:BKCHHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/HKD1024304,70/ -} | ![image-2026-9-29_14-25-11.png](attachments/image-2026-9-29_14-25-11.png)![image-2026-9-29_14-24-39.png](attachments/image-2026-9-29_14-24-39.png) | |
| 1.2 | GBS Deriv Setts | - GBSDerivSetts to release MT604 on DVP terms | |
| 1.3 | Middle Offfice | - Middle Office to cancel test trade once MT604 is released | |
| 1.4 | GBS Deriv Setts | - GBSDerivSetts to confirm reversal MT692 is released from Ratan | |
| 1.5 | CTMU | - CTMU to sight MT696 Cancellation Advice | |
| 2 | 2.1 | Cancellation on DvP Transfer (by Paying DP = SCB ) (After successfully matched and before submitted to RTGS) | Middle Office | - T: Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I604BKCHHKHHXGSIN}{3:{108:PqSZX1gA8nSh7UF7}}{4: :26C:/HONGKONG/UNALLGOLD995+ :30:261002 :20:DV60M00128902023 :21:DV60M00128902023 :23:TRANSFER :32F:FOZ25, :82A:SCBLHKH0XXX :87A:BKCHHKH0XXX :88A:BKCHHKH0XXX :72:/ACC/DVPTRF /OCMT/USD108810,00/ -} | | |
| 2.2 | GBS Deriv Setts | - T: GBSDerivSetts to release MT604 on DVP terms | | |
| 2.3 | CTMU | - T+1: Before VD, CTMU to sight incoming MT699 of HAU match advice | | |
| 2.4 | Middle Office | - T+1: Middle Office to cancel test trade upon CTMU sighting of MT699 | | |
| 2.5 | GBS Deriv Setts | - T+1: GBSDerivSetts to confirm reversal MT692 is released from Ratan | | |
| 2.6 | CTMU | - T+1: CTMU to sight MT696 Cancellation Advice | | |
| 2.7 | CTMU | - T+2: CTMU to check with BOC HK that they have received MT699 Pending Match Advice | | |
| 2.8 | HK Cash | - On VD, HK Cash team to confirm no credit advice from RTGS received | | |
| 3 | 3.1 | Cancellation on DvP Transfer (by Paying DP = SCB ) (After submitted to RTGS and before successful settlement) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I604BKCHHKHHXGSIN}{3:{108:mMzy3z8eqDN1bLwe}}{4: :26C:/HONGKONG/UNALLGOLD995+ :30:261006 :20:DV60M00128902025 :21:DV60M00128902025 :23:TRANSFER :32F:FOZ10, :82A:SCBLHKH0XXX :87A:CCBQHKA0XXX :88A:CCBQHKA0XXX :72:/ACC/DVPTRF /OCMT/EUR37962,50/ -} | | |
| 3.2 | GBS Deriv Setts | - GBSDerivSetts to release MT604 on DVP terms | | |
| 3.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | | |
| 3.4 | HK Cash | - Before VD, HK Cash team to confirm receipt of Credit Advice pacs.009 from RTGS - HK Cash team to notify Middle Office to cancel test trade. | | |
| 3.5 | Middle Office | - Middle Office to cancel test trade | | |
| 3.6 | GBS Deriv Setts | - GBSDerivSetts to confirm reversal MT692 is released from Ratan | | |
| 3.7 | CTMU | - CTMU to sight MT696 Cancellation Advice | | |
| 3.8 | CTMU | - CTMU to confirm with CCB Asia receipt of: i) Cancellation advice camt.021 from RTGS ii) MT699 Rejection Advice | | |
| 4 | 4.1 | Cancellation on DvP Transfer (by Receiving DP = SCB ) (After submitted to RTGS and before successful settlement) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I605BKCHHKHHXGSIN}{3:{108:xDvxASixJoi2Ch03}}{4: :20:DV60M00128902027 :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:261001 :21:DV60M00128902027 :23:TRANSFER :32F:FOZ18, :82A:CCBQHKA0XXX :87A:CCBQHKA0XXX :88A:SCBLHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/EUR68332,49/ -} | | |
| 4.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | | |
| 4.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | | |
| 4.4 | HK Cash | - Before VD, HK Cash team to receive HKCS Payment Notification (pain.001) from RTGS - HK Cash team to notify Middle Office to cancel test trade. | | |
| 4.5 | Middle Office | - Middle Office to cancel test trade | | |
| 4.6 | GBS Deriv Setts | - GBSDerivSetts to confirm reversal MT692 is released from Ratan | | |
| 4.7 | HK Cash | - HK Cash team to confirm receipt of cancellation advice camt.021 from RTGS | | |
| 4.8 | CTMU | - CTMU to sight MT696 Cancellation Advice | | |
| 5 | 5.1 | Cancellation on DvP Transfer via camt.056 (by Receiving DP = SCB ) (After submitted to RTGS and before successful settlement) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I605BKCHHKHHXGSIN}{3:{108:WkFQwYlgKW7uDgrY}}{4: :20:DV60M00128902029 :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:261002 :21:DV60M00128902029 :23:TRANSFER :32F:FOZ20, :82A:CCBQHKA0XXX :87A:CCBQHKA0XXX :88A:SCBLHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/HKD682943,40/ -} | | |
| 5.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | | |
| 5.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | | |
| 5.4 | HK Cash | - Before VD, HK Cash team to receive HKCS Payment Notification (pain.001) from RTGS | | |
| 5.5 | HK Cash | - HK Cash team to initiate camt.056 cancellation to RTGS | | |
| 5.6 | HK Cash | - HK Cash team confirm receipt of cancellation advice camt.029 | | |
| 5.7 | CTMU | - Receive MT699 rejection advice | | |
| 6 | 6.1 | Cancellation on DvP Transfer via eiMBT (by Receiving DP = SCB ) (After submitted to RTGS and before successful settlement) | Middle Office | - Middle Office to book test trade | {1:F01SCBLHKH0AXXX0000000000}{2:I605BKCHHKHHXGSIN}{3:{108:Mayh9YRxSWK0koHL}}{4: :20:DV60M00128902031 :[26C:/HONGKONG/UNALLGOLD995+](http://26C/HONGKONG/UNALLGOLD995+) :30:261005 :21:DV60M00128902031 :23:TRANSFER :32F:FOZ10, :82A:CCBQHKA0XXX :87A:CCBQHKA0XXX :88A:SCBLHKH0XXX :[72:/ACC/DVPTRF](http://72/ACC/DVPTRF) /OCMT/USD43524,00/ -} | | |
| 6.2 | GBS Deriv Setts | - GBSDerivSetts to release MT605 on DVP terms | | |
| 6.3 | CTMU | - CTMU to sight incoming MT699 of HAU match advice | | |
| 6.4 | HK Cash | - Before VD, HK Cash team to receive HKCS Payment Notification (pain.001) from RTGS | | |
| 6.5 | HK Cash | - HK Cash team to initiate cancellation request via eiMBT and confirm cancellation processed. | | |
| 6.6 | HK Cash | - HK Cash team confirm receipt of cancellation advice camt.029 | | |
| 6.7 | CTMU | - Receive MT699 rejection advice | | |
| 6.8 | GBS Deriv Setts | - No requirment to release MT692 | | |
| 8 | 8.1 | DvP Transfer (by Paying DP = SCB ) Trigger cancellation via HKCS Bank Cutoff in HKCS (Test for Pending Match) | Middle Office | - Middle Office to book test trade | | | |
| 8.2 | GBS Deriv Setts | - GBSDerivSetts to release MT604 on DVP terms | | | |
| 8.3 | CTMU | - CTMU to inform UBS HK this is a test for pending match and UBS HK to send in MT605 for different amount against SCB HK. | | | |
| 8.4 | CTMU | - On VD, CTMU to receive MT699 rejection advice. | | | |