| | Categories | Detailed Function | Comment |
| --- | --- | --- | --- |
| 1 | All current Ratan business feature | Murex msg format, additional fields? | |
| 2 | | Murex integration MQ + Batch? | |
| 3 | | Fixing batch for rates product which may pending fixing | |
| 4 | | SWIFT Generation Changes - Booking Entity FMID(mandatory for each entity) - Booking Entity SWIFT BIC (Sender BIC in SWIFT) (mandatory for each entity) - Field 53 SWIFT BIC (for LCY & Over Account) (mandatory for each entity) - Field 58 SWIFT BIC (for Flip MT202) (mandatory for each entity) - Receiver BIC (MT604/605) - Branch code mapping (mandatory for each entity) - Any other branch specific requirement on SWIFT | |
| 5 | | Vostro SI Input Screen - Include New Settlement Means? | Nothing special |
| 6 | | Currency Release Time (mandatory for each entity) | |
| 7 | | NDS Auto Netting | |
| 8 | | Pending Fixing STP/NSTP Control( in case new product have fixing events) | |
| 9 | | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | Nothing special |
| 10 | | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | |
| 11 | | Settlement Accounting - Bridge Account # (mandatory for each entity) - EBBS Branch code & EBBS Transaction type (mandatory for each entity) - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | |
| 12 | | Rounding - applicable for special currency/requirement only | Keep without decimal |
| 13 | | Nostro Static Setup (mandatory for each entity) | Korea data management team. |
| 14 | | Vostro Static Setup (Vostro to drive Nostro assignment) - Over-Account Clients to be created as Branch specific SSI | |
| 15 | | Business Rules Setup - Cashflow Suppression - White List for in scope entities - Swift Suppression - Auto Debit by Agent - Nostros shared with other entity (example: China) - NSTP - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity - Netting Static - BIC Netting Static | Data entitlement, potentially Korea entity fmid is a mandatory condition for rule setup from Korea data static team. Yeon Su to advise on: NSTP/Netting/suppression rules |
| 16 | Open Firewall for users in new location | | |
| 17 | TDS3 dependency | Trade confirmation status (TDS3?) | |
| 18 | | NDS auto netting | |
| 19 | | LIEN | |
| 20 | | Integration | |
| 21 | TLM dependency | | |
| 22 | LMS dependency | | |
| 23 | Korea customized features? | MT/MX? | |
| 24 | | Ensis integration by solace? | |
| 25 | | Accounting? | |
| 26 | | Korea language issue? Require to support in SSI, SCI, cashflow data? | |
| 27 | | OUR payments, TPP | manually key in by OSCAR 1. TPP 2. Decimal diff |