| # | Description | Type | Data | Done By |
| --- | --- | --- | --- | --- |
| 1 | LMS Feed Entity List Update | Config | Send to LMS | Dev Team (CR) |
| 2 | SWIFT Generation Changes - Booking Entity SWIFT BIC - Field 53 SWIFT BIC - Branch code mapping - Any other branch specific requirement on SWIFT | Config | - Booking Entity FMID: 401053411 - Booking Entity FMCODE: SCB CHINA*HFI - Booking Entity BIC: SCBLCNSXHFI (Sender BIC in SWIFT) - Field 53 BIC: SCBLCNSXGMO (LCY & Over-Account) - Field 58 in Flip MT202: SCBLCNSXGMO - Branch code: 73 - Assumption: No other branch specific requirement on SWIFT |
| 3 | Currency Release Time | Config | Follow China HO Release Time |
| 4 | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | Config | No new codes to be mapped |
| 5 | Settlement Accounting - Bridge Account # - EBBS Branch code - EBBS Transaction code - Any other branch specific requirement | Config | - Bridge Account # 560100000001910205 (TBC by Balaji) - EBBS branch code: 73 - EBBS Transaction code: Follow China - No other branch specific requirement |
| 6 | Include new branch in GUI Drop down - Cashflow Blotter - Dashboard | Config | |
| 7 | Nostro Static Setup | Static | Provided via Email | Data Ops / Dev Team (CR) |
| 8 | Vostro Static Setup (Vostro to drive Nostro assignment) | Static | - Existing SSI's which are Global will be auto picked up - Hefei branch specific SSI's will be required only for SUPPRESSXX (Nostro auto debit) or Over-Account clients. External Client SSI's not expected to be traded as of now - Open Issue: SSI created for Hefei branch flown into MX2.11 as a Global SSI | Data Ops |
| 9 | Business Rules Setup (Suppression / NSTP / Netting) | Static | - No NSTP - Swift Suppression: SCB Hefei to be added as a Counterparty + FCY - Weng Hien to raise to data ops SCH202G210A1190225096333 // Rule ID 7230060232576802816 Done - Existing Rules which have China Booking Entities: Sumi/WH Done via eOps SCH202G210A1200225022654 - Existing Rules which have China Entities as Counterparty: Sumi/WH Done via eOps SCH202G210A1200225022654 | Data Ops |
| 10 | Downstream Engagement to determine additional requirements if any | Analysis | | Dev Team |
| 11 | UAT | Testing | | Settlement Ops |
| 12 | Regression Testing | Testing | | Dev Team |