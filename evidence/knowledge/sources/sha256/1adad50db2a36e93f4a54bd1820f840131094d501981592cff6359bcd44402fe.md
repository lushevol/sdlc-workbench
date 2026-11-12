- [Auto Un-Net - Trade market event](https://confluence.global.standardchartered.com/display/DSP/Auto+Un-Net+-+Trade+market+event)
- [Beneficiary BIC Netting](https://confluence.global.standardchartered.com/display/DSP/Beneficiary+BIC+Netting)
- [Business User Case](https://confluence.global.standardchartered.com/display/DSP/Business+User+Case)
- [CCIL Netting](https://confluence.global.standardchartered.com/display/DSP/CCIL+Netting)
- [CPN Business Scenario](https://confluence.global.standardchartered.com/display/DSP/CPN+Business+Scenario)
- [CPN Tech Design - Draft for now](https://confluence.global.standardchartered.com/display/DSP/CPN+Tech+Design+-+Draft+for+now)
- [Cashflow Auto Netting- 2024](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Auto+Netting-+2024)
- [IRS Fix Leg & Floating leg payment handling](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2726685251)
- [NDS Auto Netting](https://confluence.global.standardchartered.com/display/DSP/NDS+Auto+Netting)
- [Netting Rules Static Data](https://confluence.global.standardchartered.com/display/DSP/Netting+Rules+Static+Data)
- [Netting Service - GUI & API intergration](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2594781981)
- [Netting Story Board](https://confluence.global.standardchartered.com/display/DSP/Netting+Story+Board)
- [Product Agnostic model to identify all cashflows for a specific value date to support Auto Aggregation](https://confluence.global.standardchartered.com/display/DSP/Product+Agnostic+model+to+identify+all+cashflows+for+a+specific+value+date+to+support+Auto+Aggregation)
- [Settlement Netting Validation/Generation](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2386165321)
- [[Draft] Auto Aggregation based on Normalized Payment Schedule](https://confluence.global.standardchartered.com/display/DSP/%5BDraft%5D+Auto+Aggregation+based+on+Normalized+Payment+Schedule)

| Netting Type | Netting Criteria | TP systems | Further Netting | Comment |
| --- | --- | --- | --- | --- |
| IRS Netting - Auto | - IRS Cashflows - 2 Cashflows on same VD - Netting key: Value Date/Currency/Entity FMID/Counterparty FMID | - Stella | - Bilateral Netting - Manual -**NA now given netting id in rule** - Bilateral Netting - Adhoc - **Available** - CCIL Netting Guaranteed - Manual - **NA now given netting id in rule** - CCIL Netting Non Guaranteed- Manual -**NA now given netting id in rule** - Ben BIC Netting - Manual - **NA now given netting id in rule** - Bilateral Netting - Auto(In Backlog) - TBC - CPN(in Backlog) - TBC | |
| Bilateral Netting - Manual | - **Netting rule: Component cashflow netting id == blank** - Netting key: Value Date/Currency/Entity FMID/Counterparty FMID | - Stella - Murex 2.11 | NA | |
| Bilateral Netting - Adhoc | - **Component cashflow netting id can have value** - Netting key: Value Date/Currency/Entity FMID/Counterparty FMID | - Stella - Murex 2.11 | NA | |
| Bilateral Netting - Auto(In Backlog) | - Auto Netting rule - Netting key: Value Date/Currency/Entity FMID/Counterparty FMID | | NA | |
| CCIL Netting Guaranteed - Manual | - **Netting rule: Component cashflow netting id == blank** - Settlement Method == CCIL - Counterparty FMID == 400021949 - Product == IRS - Currency == INO - Netting key: Value Date/Currency/Entity FMID/Counterparty FMID | - Murex 2.11 - Stella - NA | NA | |
| CCIL Netting Non Guaranteed- Manual | - **Netting rule:Component cashflow netting id == blank** - Settlement Method == CCIL - Counterparty FMID not 400021949 - Product == IRS - Currency == INO - Netting key: Value Date/Currency/Entity FMID | - Murex 2.11 - Stella - NA | NA | |
| Ben BIC Netting - Manual | - **Netting rule: Component cashflow netting id == blank** - Ben BIC Static - Netting key: Value Date/Currency/Entity FMID/Ben BIC | - Stella - Murex 2.11 | NA | |
| NDS Netting - Auto | - Product Scope: Typology in (NDS, NDS Fixing, NDIRS, NDCF, NDFRA, ND CDS Fixing, ND CDS and ND-Convert) - VD = Business VD Today, Tomorrow & Day After - Netting key: Value Date/Currency/Entity FMID/Counterparty FMID/NID | - Murex 2.11 - Stella - NA | NA | |
| CPN(in Backlog) | | | | |

Changes for Netting on 'IRS Netting' cashflows

- Only allow the netting on resultant cashflow when it's from IRS netting, the revised netting pre-check would as below - This is the common pre-check logic cross all netting types - When component cashflow id is starting with 'N' and the netting id is not blank, only if the payment type =='IRS Netting' can pass the netting pre-check and any other payment types would be rejected
- To make the netting on 'IRS Netting' available for all netting types? Not problem for Murex 2.11 booking but would impact Stella booking - For current TP/entity/product status: Make is available for 'Bilateral Netting - Adhoc' only: **Already supported, no further change** - For long term netting process when onboarding more Stella entity/products: Make it available for all netting types | Netting Type | Problem/ Change | | --- | --- | | Bilateral Netting - Manual | 1. Rule update to add 'IRS Netting' as exception case | | Bilateral Netting - Adhoc | NA | | Bilateral Netting - Auto(In Backlog) | 1. TBC | | CCIL Netting Guaranteed - Manual | 1. Rule update to add 'IRS Netting' as exception case 2. Settlement method of 'IRS Netting' resultant cashflow, inherit from component cashflows | | CCIL Netting Non Guaranteed- Manual | 1. Rule update to add 'IRS Netting' as exception case 2. Settlement method of 'IRS Netting' resultant cashflow, inherit from component cashflows | | Ben BIC Netting - Manual | 1. Rule update to add 'IRS Netting' as exception case 2. BIC stamping on 'IRS Netting' resultant cashflow, need to check if there's new query when netting resultant cashflow published to workflow | | CPN(in Backlog) | TBC |
- Lifecycle change: Pending Netting cashflow can't be un-neted(manual or auto by withdrawal on component).
- To apply the same for 'NDS Fixing Netting'?