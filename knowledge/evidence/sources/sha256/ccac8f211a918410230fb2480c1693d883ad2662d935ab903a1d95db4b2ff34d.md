# Q4 2024

| # | Stream | System | Type | In ADO Backlog | ADO | MoSCoW | At Risk | Deliverable | DoD | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DE Go Live | RATAN | Story | Added | 5809387 | M | | DE: [Netting] Netting resultant cashflow inherit (CIS requirement) | Y | Done and release on Oct 19th |
| 2 | <u>Feature</u> | Present | <u>5967595</u> | <u>M</u> | | <u>DE UAT, Release & Post Care</u> | Y | |
| 3 | MX2.11 | <u>Feature</u> | | 5997126 | <u>M</u> | | <u>DE UAT, Release & Post Care</u> | Y | |
| 4 | FMSGW | <u>Feature</u> | | 5947775 , 5883014 | <u>M</u> | | <u>DE UAT, Release & Post Care</u> | | |
| 5 | UK Go Live | RATAN | Story | Added | 5967645 | M | | UK: Update Green Zone timings to meet TLM feed requirements | Y | In Analysis |
| 6 | Story | Added | 5765156 | M | | UK: [BIC Netting Static] Enhancement- Limit SWIFT BIC to 11 characters & Auto remove Space - Completed | Y | Done and release on Oct 05th |
| 7 | ~~Story~~ | ~~Added~~ | ~~5856575~~ | ~~M~~ | ~~Y~~ | ~~UK: BIC Netting - Update logic to use MAIN BIC ~~ | Y | Descoped due to risk of new issues |
| 8 | Story | Added | 5738149 | M | | UK: Prefix for Cash local agent sub account number | Y | Done and release on Nov 09th |
| 9 | ~~<u>Feature</u>~~ | ~~Present~~ | ~~<u>5967610</u>~~ | ~~<u>M</u>~~ | ~~Y~~ | ~~<u>UK: Set Vostro SI mandatory for precious metal receipts</u>~~ | ~~Y~~ | ~~12 failures seen in 2 weeks data testing~~ |
| 10 | Story | Added | 5907982 | M | | UK: For UK, for Cashflow CCY = CNH, send CCY as CNH in eBBS feed (don't convert to CNY) | Y | Done and release on Nov 09th |
| 11 | Story | Added | 5967647 | S | Y | Add FMCODE to Group Blotter | Y | Planning to release on Jan 2025 |
| 12 | Story | Added | 5997358 | M | | Waiting Fixing Flag handling for UK go live | Y | Planning to release on Jan 2025 |
| 13 | Story | Added | 5997360 | S | Y | Auto Suppress Zero amount cashflow & do not trigger SWIFT Error | Y | **Pending** |
| 14 | | | | | | [XTRA] Restrict 'Enter' in FMO Comments field | | |
| 15 | <u>Feature</u> | Present | <u>5937171</u> | <u>M</u> | | <u>UK New Features, UAT, Release & Post Care</u> | Y | 1 FTE Save from Ops side |
| 16 | MX2.11 | <u>Feature</u> | | 5713858 | <u>M</u> | | <u>UK UAT & Release</u> - <u>Refresh Env & load 3 days data (IMM & CDS roll dates)</u> | Y | |
| 17 | <u>Feature</u> | | 5691276 | <u>M</u> | | <u>RFR Auto Netting (with separate queue)</u> | Y | |
| 18 | <u>Feature</u> | | 4937584 | <u>M</u> | | <u>Waiting Fixing Flag handling for Realtime (Oct / Nov)</u> | Y | |
| 19 | <u>Feature</u> | | 5621331 | <u>M</u> | | UK NDS Cashflows to be excluded from Auto Netting and sent to RATAN | Y | |
| 20 | <u>Feature</u> | | 4816621 | <u>M</u> | | <u>Retain MLS CPN cashflows in MX2.11</u> | Y | |
| 21 | <u>Feature</u> | | 6004807 | <u>M</u> | | Automated Rollback solution for UK | Y | |
| 22 | Feature | | 6074927 | | | [NEW] Mx2.11 H2 Filter All London and SSTL Payments from Maker Queues with VD greater than Business Go live Date | Y | |
| 23 | FMSGW | <u>Feature</u> | | 5882994 | <u>M</u> | | <u>UK UAT & Release</u> | | |
| 24 | UK Phase 2 (Jan) | RATAN | <u>Feature</u> | Present | 5967597 | M | | RATAN Cash Settlements - RFR in strategic flow | Y | |
| 25 | <u>Feature</u> | Present | 5967599 | M | | RATAN Cash Settlements - Swap Agent in strategic settlement platform | Y | |
| 26 | <u>Feature</u> | Present | 5967601 | M | | RATAN Cash Settlements - LIEN processing in strategic settlement platform | Y | Raise TDS3 dependency in BRP |
| 27 | <u>Feature</u> | Present | 5967608 | M | | RATAN Cash Settlements - Pending fixing processing in strategic settlement platform | Y | |
| 28 | MX2.11 | <u>Feature</u> | | 5691290 | M | | Send RFR post netting to RATAN | Y | |
| 29 | <u>Feature</u> | | 4861227 | M | | Send Swap Agent post netting to RATAN with payment type identifiers | Y | |
| 30 | <u>Feature</u> | | 4937584 | M | | Update Pending Fixing Flag value as X | Y | |
| 31 | <u>Feature</u> | | 5986902 | M | | Send LIEN data to RATAN & TDS3 | Y | |
| 32 | <u>Feature</u> | | 6001960 | M | | HK and Taiwan Accounting feed Analysis | Y | |
| 33 | Prime Migration | RATAN | <u>Feature</u> | Added | 6101397 | M | | RATAN Cash Settlements - Trade SI Stamping for Prime trades | | |
| 34 | RATAN | <u>Feature</u> | Added | 4888196 | M | | RATAN Cash Settlements - PS4: Prime Trade Migration | Y | |
| 35 | RATAN | <u>Feature</u> | Added | 2300336 | ? | Y | CPN Analysis. No Capacity | N | |
| 36 | RATAN | Story | Added | 5967672 | M | | Update SGO to SGD ISO code mapping for both Payment SWIFT and Accounting | Y | Planning to release on Jan 2025 |
| 37 | *RAZOR* | | | | M | | Prime UAT Support | | |
| 38 | *RAZOR* | | | | | | Prime - New Events - what is the Dev Required? | | |
| 39 | *RAZOR* | | | | | | CPN Analysis + Design | | |
| 40 | FMSGW | | | 5947753 | | | Prime FIT / UAT Support | | |
| 41 | Global Rates | RATAN | <u>Feature</u> | Present | 5967613 | ? | Y | TBC on scope. No Capacity | N | Raise STELLLA dependencies in BRP |
| 42 | *RAZOR* | | | | | | Settlement Method Analysis | | |
| 43 | KTLO | RATAN | <u>Feature</u> | Present | <u>5780735</u> | <u>M</u> | | <u>RATAN Cash Settlements - KTLO Q4</u> | Y | |
| 44 | RATAN | Story | Present | 5855915 | M | | Mumbai Entity Release Cutoff update for INY | Y | Done and release on Nov 02th |
| 45 | RATAN | Story | Present | 5855842 | M | | Mumbai Entity: Add new CCIL client (Bandhan Bank) | Y | Done and release on Nov 02th |
| 46 | RATAN | Story | Present | 5586598 | M | | [SWIFT] Rounding logic to be applied for past generated cashflows | Y | Done and release on Oct 19th |
| 47 | Drop 4 LNBR | RATAN | Feature | Added | <u>5995951</u> | <u>M</u> | Y | <u>RATAN Cash Settlements - Drop 4 LN_BR</u> | Y | |
| 48 | RATAN | Story | Present | 4350456 | M | | Update CFI DYXXXX for LNBR | Y | **Pending** |
| 49 | RATAN | Story | Present | 5967659 | M | | LNBR UAT | Y | In Progress |
| 50 | RATAN | Feature | | 5952212 | | | [Cash Settlement][MXDECOMM - FMRP 4.0] Payment status update - Implement Stella API lock mechanism Drop3.1 | Y | |
| 51 | Drop 3 CN Trade Migration | RATAN | <u>Feature</u> | Present | <u>2633095</u> | <u>M</u> | | <u>Trade Migration Go Live</u> | Y | |
| 52 | ~~Drop 3.1~~ China Day 2 | RATAN | <u>Feature</u> | Present | <u>5967618</u> | | Y | <u>TBC</u> | | |
| 53 | Keystone | RATAN | <u>Feature</u> | Added | 6018325 | <u>M</u> | | <u>Keystone UAT Support</u> | | |
| 54 | ACE (Egypt, Nepal, Saudi) | RATAN | <u>Feature</u> | Added | 5997341 | <u>M</u> | | <u>Islamic UAT Support</u> | Y | |
| 55 | RAZOR | <u>Feature</u> | | | <u>M</u> | | <u>Islamic UAT Support</u> | | |
| 56 | Country Rollout | RATAN | <u>Feature</u> | Present | <u>4858340</u> | <u>M</u> | | <u>Analysis for HK & TW rollout for Accounting Model only</u> | Y | |
| 57 | FMSGW Roadmap | FMSGW | | | | | | Rollout RAZOR ALM (Not part of SFMRP funding) | | |
| 58 | | | | | | Kill Switch | | |