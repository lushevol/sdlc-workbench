# Summary of Changes Required

| # | Description | Details | Type | Done By | Required for Tranche1? |
| --- | --- | --- | --- | --- | --- |
| 1 | Bypass Validation Rule | Bypass EG/NP/SAUDI/LOANIQ/CN(FX), rest need validation Post MO Validation moved to FMRP, then not required? | | | No |
| 2 | LMS Feed Entity List Update | Blacklist includes: EG/NP/SAUDI/KL/TH/TW | Config | Dev Team (CR) | @Mingyang Zhong |
| 3 | [Murex Cash Migration Only] Entity list for the Batch Solution | H2 Adaptor whitelist includes: UK, DE (Set as default) [T-1, T+1] for group calculation H1 Adaptor whitelist includes: CN/SG/MY/IN [VD-1, VD+9] for group calculation only for Murex | Config | @Yang Chen |
| 4 | - BCS vs Strategic Routing - Entity whitelist for in scope entities (covered via Cashflow Suppression rule) - Entity whitelist setup to send to RAZOR or handle in RATAN (RATAN generates SWIFT & Accounting | Workflow whitelist: 1. EG/NP/SAUDI/LOANIQ (legacy flow) 2. Strategic flow (CN/SG/MY/IN/UK/DE) 3. ++CPT list(HK/TW/TH) | Config | @Yang Chen |
| 5 | SWIFT Generation Changes - Booking Entity FMID - Booking Entity SWIFT BIC (Sender BIC in SWIFT) - Field 53 SWIFT BIC (for LCY & Over Account) - Field 58 SWIFT BIC (for Flip MT202) - Receiver BIC (MT604/605) - Branch code mapping - Any other branch specific requirement on SWIFT | Need to be added for new entity [2025 Tranche 1 Go Live Readiness (Hongkong, Bangkok, Taipei, New York) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3222988926) | Config | @Mingyang Zhong |
| 6 | Currency Release Time | Need to be added for new entity | Config | @Yang Chen |
| 7 | NDS Auto Netting | Blacklist: TBD | Config | @Lina Feng |
| 8 | Pending Fixing STP/NSTP Control( in case new product have fixing events) | Blacklist: TBD | Config | No |
| 9 | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | Whitelist: CN/MY/IN/SG/LOANID old logic Rest: new logic | Config | No |
| 10 | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | NA | Config | No Exclude SGO/SGD change @Chongxuan Li |
| 11 | Settlement Accounting - Bridge Account # - EBBS Branch code & EBBS Transaction type - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | [2025 Tranche 1 Go Live Readiness (Hongkong, Bangkok, Taipei, New York) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3222988926) | Config | @Chongxuan Li @Guiling Wang |
| 12 | Include new branch in GUI Drop down - Cashflow Blotter - Dashboard | [2025 Tranche 1 Go Live Readiness (Hongkong, Bangkok, Taipei, New York) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3222988926) | Config | @Guiling Wang |
| 13 | Vostro SI Input Screen - Include New Settlement Means -NOX | | Config | @Guiling Wang @Chongxuan Li |
| 14 | Rounding - applicable for special currency/requirement only | | Config | | No |
| 15 | Nostro Static Setup | | Static | If volume high will be done by Dev Team (CR). Else Data Ops | @Yang Chen |
| 16 | Vostro Static Setup (Vostro to drive Nostro assignment) - Over-Account Clients to be created as Branch specific SSI | | Static | Data Ops | No, data ops to setup |
| 17 | Business Rules Setup - Cashflow Suppression - White List for in scope entities - Swift Suppression - Auto Debit by Agent - Nostros shared with other entity (example: China) - NSTP - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity - Netting Static - BIC Netting Static | [2025 Tranche 1 Go Live Readiness (Hongkong, Bangkok, Taipei, New York) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3222988926) | Static | Data Ops | @Chongxuan Li |
| 18 | Open Firewall for users in new location | | Config | Dev Team | Done |
| 19 | Downstream Engagement to determine additional requirements if any | | Analysis | Dev Team | No |
| 20 | UAT | | Testing | Settlement Ops | No |
| 21 | Regression Testing | | Testing | Dev Team | No |