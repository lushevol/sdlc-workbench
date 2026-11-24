# Background

As current Murex booking model MO would place or remove Lien on the trade level and there's dedicate payment NSTP exception in Murex BAU generated on back of trade Lien. In cashflow migration when RATAN start to receive & handle the Murex payments, the similar settlement exception control with trade Lien is required in RATAN.

# Murex 2.11 Lien Trades Volume

- **Total Lien trade volume is 519 since 2009** 1. By Murex product | **Family** | **Group** | **Trade Count** | | --- | --- | --- | | IRD | LN_BR | 328 | | IRD | CS | 112 | | IRD | IRS | 41 | | IRD | CF | 30 | | IRD | OSWP | 6 | | CRD | CDS | 2 | 2. By booking date | **Trade Date** | **Trade Count** | | --- | --- | | 2009 | 14 | | 2013 | 7 | | 2014 | 13 | | 2017 | 107 | | 2018 | 127 | | 2019 | 131 | | 2020 | 41 | | 2021 | 19 | | 2022 | 12 | | 2023 | 31 | | 2024 | 17 | 3. Struct Trades or Standalone | **Booking Model** | **Trade Count** | | --- | --- | | Structure Trade | 515 | | Standalone | 4 |
- ****The volume of Murex live Lien trade is 24 **** | **Trade Date** | **Family** | **Group** | **Trade Count** | | --- | --- | --- | --- | | 2020 | IRD | LN_BR | 1 | | 2021 | IRD | LN_BR | 1 | | 2022 | IRD | LN_BR | 5 | | IRD | IRS | 1 | | 2023 | IRD | LN_BR | 6 | | 2024 | IRD | LN_BR | 9 | | IRD | CS | 1 |

# Settlement Requirement with Lien for RATAN

1. **Lien placement**: When Lien is placed on a trade, underlying cashflows(all payment types including interest, notional & others) must be NSTP in RATAN with 'Lien' exceptions
2. **Lien Removal**: When Lien is removed from a trade, underlying cashflow can be STP( if no other exception populated)

# How RATAN link the Murex cashflow to Murex Trades

Note: The Murex cashflows & trades are populated as separate business objects & handled as separate data flow.

# Business Scenarios

- **Lien is added on trade booking: **All cashflows would generate **Lien **Exception. ![image2024-10-28_16-11-59.png](attachments/image2024-10-28_16-11-59.png)
- **Lien is added during middle lifecycle: **Cashflows post Lien update would generate **Lien **exception. ![image2024-10-29_19-16-47.png](attachments/image2024-10-29_19-16-47.png)
- **Lien is removed before maturity: **Cashflow post Lien remove **won't **generate **Lien **exception.** ![image2024-10-28_16-10-7.png](attachments/image2024-10-28_16-10-7.png) **

# Appendix