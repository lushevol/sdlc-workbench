# Summary of Changes Required

| # | Description | Details | Type | Done By | Required for Hefie? | Released by |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bypass Validation Rule | Post MO Validation moved to FMRP, then not required? | | | Yes | @Xinmiao Huang |
| 2 | LMS Feed Entity List Update | Blacklist includes: EG/NP/SAUDI/KL/TH/TW | Config | Dev Team (CR) | No | |
| 3 | [Murex Cash Migration Only] Entity list for the Batch Solution | H2 Adaptor whitelist includes: UK, DE (Set as default) H1 Adaptor whitelist includes: CN/SG/MY/IN | Config | No | |
| 4 | - BCS vs Strategic Routing - Entity whitelist for in scope entities (covered via Cashflow Suppression rule) - Entity whitelist setup to send to RAZOR or handle in RATAN (RATAN generates SWIFT & Accounting | Workflow whitelist: 1. EG/NP/SAUDI/LOANIQ (legacy flow) 2. Strategic flow (CN/SG/MY/IN/UK/DE) | Config | Yes | @Mingyang Zhong |
| 5 | SWIFT Generation Changes - Booking Entity FMID - Booking Entity SWIFT BIC (Sender BIC in SWIFT) - Field 53 SWIFT BIC (for LCY & Over Account) - Field 58 SWIFT BIC (for Flip MT202) - Receiver BIC (MT604/605) - Branch code mapping - Any other branch specific requirement on SWIFT | Need to be added for new entity 1. SWIFT Field 20 | Entity | Entity Name(Murex 2.11) | Entity FMID | Branch code | | --- | --- | --- | --- | | Heifei | HEFEI | 401053411 | 73 | 1. Filed 53/58 customization mapping table. | Entity FMID | Entity Name(Murex 2.11) | Currency | 53 BIC (Rule1) | 58 BIC (Rule2) | | --- | --- | --- | --- | --- | | 401053411 | HEFEI | CNY | SCBLCNSXGMO | SCBLCNSXGMO | 1. Sender's BIC mapping table | Entity FMID | Entity Name(Murex 2.11) | Sender's BIC | | --- | --- | --- | | 401053411 | HEFEI | SCBLCNSXHFI | Country Code: CN | Config | Yes | @Mingyang Zhong |
| Entity | Entity Name(Murex 2.11) | Entity FMID | Branch code |
| Heifei | HEFEI | 401053411 | 73 |
| Entity FMID | Entity Name(Murex 2.11) | Currency | 53 BIC (Rule1) | 58 BIC (Rule2) |
| 401053411 | HEFEI | CNY | SCBLCNSXGMO | SCBLCNSXGMO |
| Entity FMID | Entity Name(Murex 2.11) | Sender's BIC |
| 401053411 | HEFEI | SCBLCNSXHFI |
| 6 | Currency Release Time | | Config | Yes | @Chen Yang |
| 7 | NDS Auto Netting | Blacklist: TBD | Config | No | |
| 8 | Pending Fixing STP/NSTP Control( in case new product have fixing events) | Blacklist: TBD | Config | No | |
| 9 | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | Whitelist: CN/MY/IN/SG/LOANID old logic Rest: new logic | Config | No | |
| 10 | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | NA | Config | No | |
| 11 | Settlement Accounting - Bridge Account # - EBBS Branch code & EBBS Transaction type - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | 1. eBBS static | Murex_Label | Entity FMID | Country | Posting Branch | Txn Type code | Dr Txn Code | Cr Txn Code | | --- | --- | --- | --- | --- | --- | --- | | HEIFEI | 401053411 | CN | 10000 | RTN | 100 | 200 | 1. eBBS Bridge account | LegalEntity | FMID | EBBS Bridge Account | | --- | --- | --- | | SCB CHINA*HFI | 401053411 | 560100000001910205 | | Config | Yes | @Chongxuan Li |
| Murex_Label | Entity FMID | Country | Posting Branch | Txn Type code | Dr Txn Code | Cr Txn Code |
| HEIFEI | 401053411 | CN | 10000 | RTN | 100 | 200 |
| LegalEntity | FMID | EBBS Bridge Account |
| SCB CHINA*HFI | 401053411 | 560100000001910205 |
| 12 | Include new branch in GUI Drop down - Cashflow Blotter - Dashboard | | LegalEntity | FMID | Country Code | | --- | --- | --- | | SCB CHINA*HFI | 401053411 | CHINA | | Config | Yes | @Guiling Wang |
| LegalEntity | FMID | Country Code |
| SCB CHINA*HFI | 401053411 | CHINA |
| 13 | Vostro SI Input Screen - Include New Settlement Means | | Config | No | |
| 14 | Rounding - applicable for special currency/requirement only | | Config | | No | |
| 15 | Nostro Static Setup | | Static | If volume high will be done by Dev Team (CR). Else Data Ops | No, data ops to setup | |
| 16 | Vostro Static Setup (Vostro to drive Nostro assignment) - Over-Account Clients to be created as Branch specific SSI | | Static | Data Ops | No, data ops to setup | |
| 17 | Business Rules Setup - Cashflow Suppression - White List for in scope entities - Swift Suppression - Auto Debit by Agent - Nostros shared with other entity (example: China) - NSTP - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity - Netting Static - BIC Netting Static | Cashflow suppression: - Non FMRP entities - China Precious Metal SWIFT Suppression: - Swift suppress for FCY BTB between 30 China intra entities (except FTU) NSTP - Murex 2.11 CRD CDS product - China Precious Metal - Murex 2.11 CRD RTRS product - CN AdhocNET except CURR/OPT | Static | Data Ops | No, data ops to setup | |
| 18 | Open Firewall for users in new location | | Config | Dev Team | Done | |
| 19 | Downstream Engagement to determine additional requirements if any | | Analysis | Dev Team | No | |
| 20 | UAT | | Testing | Settlement Ops | No | |
| 21 | Regression Testing | | Testing | Dev Team | No | |