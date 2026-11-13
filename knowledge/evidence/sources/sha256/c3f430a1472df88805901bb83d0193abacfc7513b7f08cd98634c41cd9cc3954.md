# Background

- SCB London has started to deal as a RFI (Registered Foreign Institution) in Korea market with onshore / offshore counterparties
- As per regulation deals must be settled via a dedicated RFI Nostro account held with SCB Korea
- In productions deals are already being settled via RFI. To avoid settling to non RFI nostro, only RFI Nostro is currently setup in RATAN
- Multiple RFI portfolios can exist / be created in future

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11718757](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11718757)

- Stamp the RFI Nostro in RATAN based on **RFI portfolio** and **Currency** - RFI portfolio: - IR_SWP_KOR_NYRF_STL - IR_SWP_KOR_RFI_STL - IR_SWP_KOR_RFI - IR_SWP_KOR_NYRF
- Portfolio changes must update the Nostro selection - means if cashflow portfolio changed from Non-RFI to RFI portfolio, or vice versa, system should consider it as economic amendment and process the latest version of the cashflow
- On Swift, need to capture the RFI account number in the payment field 53 as well as in field 25 on MT210.
- No changes to Vostro stamping logic
- for RFI portfolio, vostro stamping should not overwrite Nostro stamping
- Logic to be kept agnostic of products
- Nostro selection logic change applied to - Cashflow SSI stamping - ~~trade SSI stamping~~
- consider to build a common solution, may need to support other special nostro stamping. - may need to stamp with additional attribute (portfolio / strategy / typology / any other FMRP attribute)

# Review History

| Date | Attendee | Requirement Sign off |
| --- | --- | --- |
| 2026-02-09 | Dinesh, Babu, Shiva | |

# Required Changes

1. add new fields in nostro static popup | | Field name | Field type | Mandatory? | display in list view? | Value | allow update? | comment | | --- | --- | --- | --- | --- | --- | --- | --- | | New | Nostro Type | dropdown | N | Y | RFI DEFAULT | N | when creating a new nostro, nostro value will be "DEFAULT", user can select the value in dropdown to change. | | New | Portfolio | text | will be mandatory if Nostro Type = RFI | Y | | Y | allow user to input multiple portfolio values | | Impacted | Primary | | will be disabled if Nostro Type = RFI | | | | | ![image-2026-1-26_17-33-8.png](attachments/image-2026-1-26_17-33-8.png)
2. update duplicate check to booking entity + ccy + settlement means + settlement account + nostro type
3. update nostro stamping logic 1. query nostro with Booking Entity + ccy + Portfolio 1. if single nostro match, stamp to the RFI nostro 2. if multiple nostro match, generate missing nostro exception, user can manually select the RFI from cashflow details 3. if no nostro match, continue with step b 2. follow as-is process
4. Change in adhoc SSI/lookup SI in split popup 1. user should be able to see the Nostro Type when select nostro 2. The Nostro type need to be added in cashflow details
5. **SI-Mismatch**: if settlement means/settlement account not matched between vostro and nostro, SI mismatch exception will be generated, user need to manually update vostro SI to process the cashflow.
6. Other impacted functions: 1. if cashflow portfolio changed from non-RFI to RFI or vice versa, system should consider it as economic changes 2. if there is any tech issue caused system failed to get the indicator to decide if the cashflow is RFI portfolio or not, consider it as economic change by default
7. RFI trade stamping to be covered in the trade stamping strategic solution de deployed seperately. 1. current trade stamping is product-related and CCS has not yet been enabled. 2. Once RFI logic enabled in settlement process, cashflow will stamp to the RFI nostro for in-scoped portfolios, trade will follow as-is BAU process.
8. MT210 need to capture the account number for tag25 (only for ISO ccy as KRW) 1. if ccy is KRW, MT210 need to generate tag25 with the account number from nostro 2. swift change need integration test with downstream.

# Business Use Case

| | Test Scenario | Test Steps | Expected Step |
| --- | --- | --- | --- |
| 1 | Create RFI nostro | 1. user create new nostro with nostro type = RFI 2. user is able to add multiple portfolio in one nostro record 3. Primary flag is disabled when RFI is selected 4. user cannot create 2 RFI record for same entity + ccy + settlement means + settlement account | |
| 2 | - RFI portfolio - KR ccy - SCB Pay - Vostro stamp to KRO OTH 1 Cashflow stamp to the RFI nostro (KRO OTH 1) | 1. nostro created for RFI portfolio 2. cashflow with RFI portfolio and KRO ccy sent to ratan 3. maker/checker release the cashflow | 1.nostro rule in save confirmed status 2.cashflow vostro stamped to KRO OTH 1 and nostro stamped to the RFI nostro 3. swift generated as expected |
| 3 | - RFI portfolio - KR ccy - SCB Receive Cashflow stamp to the RFI nostro (KRO OTH 1) | 1. nostro created for RFI portfolio 2. cashflow with RFI portfolio and KRO ccy sent to ratan 3. maker/checker release the cashflow | 1.nostro rule in save confirmed status 2.cashflow nostro stamped to the RFI nostro 3. swift generated as expected (tag25 added in the MT210) |
| 4 | - RFI portfolio - KR ccy - SCB pay - Vostro stamp to KRO MAIN Cashflow stamp to the RFI nostro (KRO OTH 1) with SI mismatch exception | 1. nostro created for RFI portfolio 2. cashflow with RFI portfolio and KRO ccy sent to ratan 3. maker/checker update the vostro settlement means/account and release the cashflow | 1.nostro rule in save confirmed status 2.cashflow vostro stamped to KRO MAIN and nostro stamped to the RFI nostro, SI mismatch exception generated 3. swift generated as expected |
| 5 | - RFI portfolio - KR ccy - SCB receive - Vostro stamp to KRO MAIN Cashflow stamp to the RFI nostro (KRO OTH 1) with SI mismatch exception | 1. nostro created for RFI portfolio 2. cashflow with RFI portfolio and KRO ccy sent to ratan 3. maker/checker update the vostro settlement means/account and release the cashflow | 1.nostro rule in save confirmed status 2.cashflow vostro stamped to KRO MAIN and nostro stamped to the RFI nostro, SI mismatch exception generated 3. swift generated as expected (tag25 added in the MT210) |
| 6 | - non RFI portfolio - KR ccy - SCB pay - Vostro stamp to KRO OTH 1 Cashflow stamp to the primary nostro (KRO MAIN) with SI mismatch exception | 1. nostro created for RFI portfolio 2. cashflow with non RFI portfolio and KRO ccy sent to ratan 3. maker/checker update the vostro settlement means/account and release the cashflow | 1.nostro rule in save confirmed status 2.cashflow vostro stamped to KRO OTH 1 and nostro stamped to the non-RFI nostro, SI mismatch exception generated 3. swift generated as expected |
| 7 | - non RFI portfolio - KR ccy - SCB receive - Vostro stamp to KRO MAIN Cashflow stamp to the KRO MAIN nostro static : notice to receive = N | 1. nostro created for RFI portfolio 2. cashflow with non RFI portfolio and KRO ccy sent to ratan 3. maker/checker release the cashflow | 1.nostro rule in save confirmed status 2.cashflow vostro stamped to KRO MAIN and nostro stamped to the RFI nostro 3. swift not generated as expected (notice to receive flag =N) |
| 8 | - non RFI portfolio - KR ccy - SCB receive - Vostro stamp to KRO MAIN Cashflow stamp to the KRO MAIN nostro static : notice to receive = Y | 1. nostro created for RFI portfolio 2. cashflow with non RFI portfolio and KRO ccy sent to ratan 3. maker/checker release the cashflow | 1.nostro rule in save confirmed status 2.cashflow vostro stamped to KRO MAIN and nostro stamped to the RFI nostro 3. swift generated as expected (tag25 added in the MT210) |
| 9 | Adhoc SSI allow user to see the nostro type in available nostro list, (user can select RFI nostro even for non-RFI portfolio) | 1. cashflow with KRO ccy sent to ratan 2. user manually edit nostro SI selection | 1. cashflow in WAITING status 2. nostro type field available in both list and form view |
| 10 | Cashflow changed from non-RFI to RFI portfolio is considered as economic amendment | 1. cashflow with non-RFI portfolio and KRO ccy sent to RATAN 2. maker/checker release the cashflow 3. user amend trade to RFI portfolio, withdrawal and new cashflow received in Ratan 4. maker/checker release the cashflow | 1. cashflow stamped to non-RFI nostro 2. cashflow in release or settled status 3. withdrawal and new event are in waiting status 4. withdrawal and new cashflow released |
| 11 | Cashflow changed from RFI to non-RFI portfolio is considered as economic amendment | 1. cashflow with RFI portfolio and KRO ccy sent to RATAN 2. maker/checker release the cashflow 3. user amend trade to non-RFI portfolio, withdrawal and new cashflow received in Ratan 4. maker/checker release the cashflow | 1. cashflow stamped to RFI nostro 2. cashflow in release or settled status 3. withdrawal and new event are in waiting status 4. withdrawal and new cashflow released |
| 12 | Cashflow changed from non-RFI portfolio to non-RFI portfolio is not considered as economic amendment | 1. cashflow with non-RFI portfolio and KRO ccy sent to RATAN 2. maker/checker release the cashflow 3. user amend trade to non-RFI portfolio, withdrawal and new cashflow received in Ratan | 1. cashflow stamped to non-RFI nostro 2. cashflow in release or settled status 3. withdrawal and new event are offset in group blotter |
| 13 | RFI cashflow hit swift_suppression rule before stamping, accounting generated with RFI nostro EBBS account | 1. cashflow with RFI portfolilo hit swift suppression rule | 1. cashflow moved to swift_suppressed, accounting generated with RFI nostro ebbs account |
| 14 | Non RFI cashflow hit swift_suppression rule before stamping, accounting generated with non RFI nostro EBBS account | 1. cashflow with RFI portfolilo hit swift suppression rule | 1. cashflow moved to swift_suppressed, accounting generated with non RFI nostro ebbs account |
| 15 | Trade will continue to stamp to the nostro matched with vostro SI | fixing/spot/forward/irs/swap trade message will follow as-is process | |

# Related Links