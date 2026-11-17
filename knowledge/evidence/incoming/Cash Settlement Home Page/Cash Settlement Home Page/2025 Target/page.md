[2025 High Level Backlog - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/2025+High+Level+Backlog)

# Yearly Target

- UK Cashflow migration from Murex 2.11 to RATAN
- Continuous Migration of Murex 2.11 cash settlements into Strategic Cash Settlements stack (RATAN) with 3 tranches - Tranche 1: BANGKOK, TAIPEI,OBU TAIPEI, HONG KONG, SCS HK - Tranche 2: MAURITIUS, DUBAI, JAKARTA, MANILA, TOKYO, JOBURG, PHILIP FCU, DIFC, NEWYORK - Tranche 3: JERSEY_BR
- Accounting with integration to Aspire
- FMRP business initiative - CN LNBR - UK Prime migration for PM and Rates - CN CCS Trade migration
- Hefei Branch Rollout
- Prime CPN
- FXO
- Swap Agent Day2
- FXU
- Auto Netting
- Strategic One Stop SSI stamping
- ISO 20022 MX onboarding
- Keystone

# Milestones

| Date | Milestone |
| --- | --- |
| 20 Jan 2025 | 430500 UK Cashflow Migration Go live (Murex Cash Settlements Migration 2024 including Precious Metals) |
| 22 Feb 2025 | 6469299 CN LNBR Go live (RATAN is Ready) |
| 3 Mar 2025 | 6469316 F2B: UK Prime PM Go Live (24 Feb Go Live) |
| 8 Mar 2025 | 6469344 F2B: CN CCS [CFETS 08 Mar] & Trade Migration [Aug] |
| Apr 2025 | F2B: UK Prime Rates Go Live |
| Apr 2025 | Hefei Branch Rollout |
| Q2 2025 | F2B: UK E-Precious +** PM NDF** + Trade Migration |
| Q2 2025 | Tranche 1 cashflow migration |
| Q2 2025 | Tranche 2 cashflow migration |
| Q2/Q3 2025 | F2B: Desk and Entity Setup (HK, TW, IN, LK, BD, SG, MY, TH, VN, UK) |
| Q3 2025 | F2B: Global Rates New Product (FRA) |
| Aug 2025 | CN CCS Trade Migration |
| Oct 2025 | F2B: FXO Go Live |
| Q3 2025 | Tranche 3 cashflow migration |
| | Prime CPN |
| | FXU |
| | Swap Agent Day2 |
| | Auto Netting |
| | Strategic One Stop SSI stamping |
| | Keystone |

# Q1 2025

## Sprints

| | Sprint | Sprint-0 (1.20-1.31) | Sprint-1（2.3-2.14) | Sprint-2 (2.17-2.28) | Sprint-3(3.3-3.14) (Current Sprint) | Sprint-4(3.17-3.28) | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | UK Post Care & Enhancement | F2B: Drop 4.0: CN Loan Depo Go Live | - [x] (RELEASED) Load 5k cashflows | 7177438 Data entitlement for TW/CN | | |
| 2 | | | UK Post Care - | - [x] (RELEASED) Dashboard auto refresh | 7477339 SSI Selection hierarchy - Tranche 1 to follow UK | | |
| 3 | | | Tranche 1 static data setup | - [x] (RELEASED) DB Usage enhancement | 6469344 CN CCS Go live [CFETS] | | |
| 4 | | | Tranche 1 Accounting design | - [x] (RELEASED) NSTP not displayed on cashflows | 6473089 Allow user who did netting to act as Checker | |
| 5 | | | | - [x] (RELEASED) ND IRS issue - Trade ID looked up RAZOR trade | 6472953 Enable NDS Auto Netting for SG (Dependency on Murex) | |
| 6 | | | | - [x] (RELEASED) SI hierarchy to follow new model for Stella Prime payments | Moving H1 entities to H2 model - Code & Config [32 MD] | |
| 7 | | | | - [x] (RELEASED) 7489431 [BIC Netting] Enable for Prime cashflow | 7147811 Tranche 1 - Update Vostro SI Settlement Means values | | |
| 8 | | | | - [x] UK Prime Rates Performance Testing | 7506417 Add entities to Dashboard & Blotter | | |
| 9 | | | | - [x] Tranche 1 UAT support on data loading/recon | 7402405 RATAN->Murex RELEASE Status Update Issue Fix - by batch | | |
| 10 | | | | | 7523847 [Trade SSI Stamping] Sync Up UK Prime trade SSI stamping best match with cashflow | | |
| 11 | | | | 7378233 MT605 Issue | | |
| 12 | | | | Tranche 1 Accounting implementation/UAT | | |
| 13 | | | | 7402457 housekeeping for Prod DB - Excessive growth in database space | | |
| 14 | | | | 7177927 fileIt setup | | |

To be Noticed

1. Review pre rules in Murex like suppression, netting, which are all supposed to be setup in RATAN
2. UAT cases should be reviewed more carefully from OPS/Dev team, we should get ourselves closely involved in the progress