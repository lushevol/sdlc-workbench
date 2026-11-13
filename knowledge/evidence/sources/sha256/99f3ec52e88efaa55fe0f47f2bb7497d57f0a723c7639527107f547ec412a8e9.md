## UAT testing follow up item

Got confirmation from user and config on UAT

Got confirmation from user and is config on UAT

Haven't got confirmation from user

| No | ADO | Reference | Static | Remark | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | [Story 9905158 [Tranche3] Static Data Setup](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9905158/) | **nostro** | **** | ** ** | ** ** |
| ~~**release cut off**~~ ~~select * from ratanone.ratan_static_cashflow_currency_cut_off where legal_entity_fmid = '400910415';~~ ~~version=3~~ ~~~~ | **** | ** 2025-09-01 ** **No need to do any change when go live** **![image-2025-9-1_15-16-31.png](attachments/image-2025-9-1_15-16-31.png)** | ** ** |
| **branch suspense bridge (equivalent to EBBS bridge suspense)** | ENTITY | Bridge Account information | | --- | --- | | Jersey | 123613180028890791098 | Branch Code:05 Ebbs nostro account:123613180028881491098 | **** | ** 2025-09-17 ** **Confirm with Balaji about the ebbs bridge account and ebbs nostro account** **![image-2025-9-17_9-56-32.png](attachments/image-2025-9-17_9-56-32.png)** **2025-08-01 ** **![image-2025-9-2_16-39-55.png](attachments/image-2025-9-2_16-39-55.png)** 2025-07-31 **![](https://confluence.global.standardchartered.com/download/attachments/3448355412/image-2025-8-26_10-7-38.png?version=1&modificationDate=1756174058000&api=v2)** | ** ** |
| ENTITY | Bridge Account information |
| Jersey | 123613180028890791098 |
| **entity level swift static** **JERSEY** select * from ratanone_swift_service.swift_static_data_sender_bic ssdsb ; select * from ratanone_swift_service.swift_static_data_correspondent_bic ssdcb ; | Entity | Branch code | FMID | Sender Bic | Field 53 BIC(Rule1) | Field 53 CCY to be used | Field 58 BIC(Rule2) | | --- | --- | --- | --- | --- | --- | --- | | JERSEY | 05 | 400910415 | SCBLJESHXXX | SCBLJESHXXX | | SCBLJESHXXX | ![image-2025-9-9_10-12-32.png](attachments/image-2025-9-9_10-12-32.png) **ZHENGZHOU&TAEYUAN** Entity level swift static update for TAEYUAN and ZHENGZHOU . | Entity | Branch code | FMID | Sender Bic | Field 53 BIC(Rule1) | Field 53 CCY to be used | Field 58 BIC(Rule2) | | --- | --- | --- | --- | --- | --- | --- | | ZHENGZHOU | 73 | 400516442 | SCBLCNSXZZH | SCBLCNSXGMO | CNY | SCBLCNSXGMO | | TAEYUAN | 73 | 400516443 | SCBLCNSXTAY | SCBLCNSXGMO | CNY | SCBLCNSXGMO | | **** | 2025-09-12 Sumita has replied the static for zhengzhou & taeyuan 2025-09-11 Need to confirm with Sumita about ZHENGZHOU and TAEYUAN ** 2025-08-29 ** **![image-2025-9-1_15-18-53.png](attachments/image-2025-9-1_15-18-53.png)** | UAT1 53 BIC-case1 ![image-2025-9-8_18-44-0.png](attachments/image-2025-9-8_18-44-0.png) ![image-2025-9-8_18-45-1.png](attachments/image-2025-9-8_18-45-1.png) **![image-2025-9-8_16-16-40.png](attachments/image-2025-9-8_16-16-40.png)** M00119946666 ![image-2025-9-8_18-47-19.png](attachments/image-2025-9-8_18-47-19.png) ![image-2025-9-8_18-46-1.png](attachments/image-2025-9-8_18-46-1.png) 53BIC case2 M00119949999 ![image-2025-9-9_10-43-0.png](attachments/image-2025-9-9_10-43-0.png) ![image-2025-9-9_10-44-47.png](attachments/image-2025-9-9_10-44-47.png) |
| Entity | Branch code | FMID | Sender Bic | Field 53 BIC(Rule1) | Field 53 CCY to be used | Field 58 BIC(Rule2) |
| JERSEY | 05 | 400910415 | SCBLJESHXXX | SCBLJESHXXX | | SCBLJESHXXX |
| Entity | Branch code | FMID | Sender Bic | Field 53 BIC(Rule1) | Field 53 CCY to be used | Field 58 BIC(Rule2) |
| ZHENGZHOU | 73 | 400516442 | SCBLCNSXZZH | SCBLCNSXGMO | CNY | SCBLCNSXGMO |
| TAEYUAN | 73 | 400516443 | SCBLCNSXTAY | SCBLCNSXGMO | CNY | SCBLCNSXGMO |
| **nstp , netting , swift suppression ** **1.Swift suppression--deliverable currencies** GBP,GHS,JOD,TRY,AUD,CHF,DKK,EUR,HKD,NZD,SEK,SGD,THB,THO,USD,ZAR,HUF, KES,PLN,AED,SAR,BWP,NOK,ZMK,MAD,ILS,PKR,NGN,UGX,TZS, Rule created on UAT:7374420229233111040 ![image-2025-9-19_14-25-11.png](attachments/image-2025-9-19_14-25-11.png) **2.Cashflow suppression--Metal currencies** Rule created on UAT:7369258354199584768 Metal Currencies XAU,XAG,XPD,XPT,XRH,XU5,XG2,XT3,XD3,XRU,XS9,XS5,XSD,XU6,XU7,XG5,XUC,XG3, XGC,XD1,XD2,XG1,XR1,XT1,XT2,XU1,XU2,XU3,XU4,XU8,XTN,XDN,XUD,XG4,XG6,XGF, XS6,XSF,XSI,XS4,XGI,XGA,XG7 ![image-2025-9-19_14-26-15.png](attachments/image-2025-9-19_14-26-15.png) **3.****Add Jersey FMID(400910415) to existing 'Non FMRP entities' cashflow suppression rule** **,** **SAUDI is keep as is** Rule id on UAT : 7369288575163731968 ![image-2025-9-19_14-25-55.png](attachments/image-2025-9-19_14-25-55.png) | **** | 2025-09-16 Pradeesh mentioned to use the below deliverable currencies for Jersey to create swift suppression rule ![image-2025-9-16_15-57-35.png](attachments/image-2025-9-16_15-57-35.png) 2025-09-02 Feedback from Clover ![image-2025-9-2_16-33-5.png](attachments/image-2025-9-2_16-33-5.png) 2025-09-01 Clover provide deliveryable ccy list ,double confirm 2025-08-29 waiting for Clover provide deliveriable ccy list 2025-08-27 Metal currencies list from Dinesh ![image-2025-8-29_11-39-21.png](attachments/image-2025-8-29_11-39-21.png) 2025-08-22 Waiting for user to provide metal ccy list and deliveriable ccy list 2025-08-15 Response from Pradeesh Swift suppression will be used for deliverable currencies and Cashflow suppression will be applied for Metal currencies in Jersey entity . Apart that there is no nstp and netting required. | |
| ~~**enable backed NSTP to prevent accounting cashflows from STP in absence of all netting static**~~ | ~~** **~~ | ~~** 2025-09-16 **~~ ~~**Confirmed with Lina ,no need for production**~~ | ** ** |
| **CPT Control** **![image-2025-9-19_15-20-38.png](attachments/image-2025-9-19_15-20-38.png)** | ** ** | **Need to update when go live** 2025-09-17 feedback from Lina Date previous Oct 12 2025, USD 1, XAU 1 Entity FMID 400910415 **![image-2025-9-17_10-1-14.png](attachments/image-2025-9-17_10-1-14.png)** | ** ** |
| 2 | [Story 9905654 [Tranche3] Entity setup in blotter](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9905654/) | Add tranche3 country into blotter ![image-2025-9-19_16-45-34.png](attachments/image-2025-9-19_16-45-34.png) - Cashflow Blotter Quick Search, Filters - Dashboard - Country drop down - Entity drop down - grouping blotter | **** | 2025-09-16 1.ZHENGZHOU&TAEYUAN is already on prod 2.There is no country for Jersey on prod ,so need to config country for jersey 3.The country of SAUDI on prod is SAUDI, confirm with Dinesh to keep as is, need to update the confluence page 2025-09-16 Confirmed with PO ,we can config the entities that already confirmed ,for the other four ,will create a new ADO for tracking （[10476997](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10476997/)） 2025-09-10 PO feedback manual entity should be filtered in Ratan waiting for PO to confirm | |
| 3 | ~~[Story 10476997* [Tranche3] Entity setup in blotter-FCBUSLANKA/HKGCT /GCT /SCBPLC](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/10476997/)~~ | ~~These four are waiting for users to confirm~~ ~~![image-2025-9-16_16-10-5.png](attachments/image-2025-9-16_16-10-5.png) ~~ | **** | ~~2025-09-19 Combined with above ~~ ~~ 2025-09-16 ~~ ~~Waiting for user to confirm the FMID~~ | |
| 4 | [Story 9920605 [Tranche 3] LMS filter](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9920605) | As part of the tranche 3 entity, the below entities needs to be filtered in Ratan and shouldn’t flow to LMS, as we don’t support this entity | **ENTITY** | **FMID** | | --- | --- | | JERSEY | 400910415 | ZHENGZHOU & TAEYUAN should flow to LMS | **** | | |
| **ENTITY** | **FMID** |
| JERSEY | 400910415 |
| 5 | ~~From Elena Wang~~ ~~Tranche3有个额外的cashflow suppression rule for manual entities哈~~ ~~select * from ratanone_rule_service.ratan_rule_engine rre where reason~~ ~~ = 'SAUDI cashflows from MUREX';~~ ~~Rule are created on UAT1~~ | ~~Entity__Booking_Entity_SCI_FMID == "400991880" && Data_Flow__Data_Source_System == "MUREX"~~ ~~![image-2025-9-16_7-3-19.png](attachments/image-2025-9-16_7-3-19.png)~~ | ~~** **~~ | ~~**2025-09-16 **~~ ~~**Confirmed with Lina ,no need for production**~~ ~~**Need to be created on production when go live **~~ ~~**![image-2025-8-26_10-33-33.png](attachments/image-2025-8-26_10-33-33.png)**~~ | ** ** |

# case 31 taeyuan:M00119946456

![image-2025-9-17_20-9-41.png](attachments/image-2025-9-17_20-9-41.png)

![image-2025-9-17_20-10-8.png](attachments/image-2025-9-17_20-10-8.png)

![image-2025-9-17_20-11-40.png](attachments/image-2025-9-17_20-11-40.png)

![image-2025-9-17_20-13-54.png](attachments/image-2025-9-17_20-13-54.png)

maker modify settlement means as below and submit

![image-2025-9-17_20-22-43.png](attachments/image-2025-9-17_20-22-43.png)

checker approve

![image-2025-9-17_20-24-2.png](attachments/image-2025-9-17_20-24-2.png)

![image-2025-9-17_20-24-42.png](attachments/image-2025-9-17_20-24-42.png)

![image-2025-9-17_20-25-41.png](attachments/image-2025-9-17_20-25-41.png)

CASE30 ZHENGZHOU

![image-2025-9-17_20-36-45.png](attachments/image-2025-9-17_20-36-45.png)

ADHOC SSI and submit

![image-2025-9-17_20-38-1.png](attachments/image-2025-9-17_20-38-1.png)

checker reject

![image-2025-9-17_20-47-7.png](attachments/image-2025-9-17_20-47-7.png)

MAKER SUBMIT

![image-2025-9-17_20-49-26.png](attachments/image-2025-9-17_20-49-26.png)

checker approve

![image-2025-9-17_20-52-12.png](attachments/image-2025-9-17_20-52-12.png)

maker modify and submit
![image-2025-9-17_20-58-30.png](attachments/image-2025-9-17_20-58-30.png)

checker approve

![image-2025-9-17_20-53-17.png](attachments/image-2025-9-17_20-53-17.png)

31 case zhengzhouM00119946000

maker submit

![image-2025-9-17_20-44-10.png](attachments/image-2025-9-17_20-44-10.png)

checkerreject

![image-2025-9-17_20-56-37.png](attachments/image-2025-9-17_20-56-37.png)

maker modify and submit

checker approve

![image-2025-9-17_21-1-22.png](attachments/image-2025-9-17_21-1-22.png)

![image-2025-9-17_21-3-54.png](attachments/image-2025-9-17_21-3-54.png)