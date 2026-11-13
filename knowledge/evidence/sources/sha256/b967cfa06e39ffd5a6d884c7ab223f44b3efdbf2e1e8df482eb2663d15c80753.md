# Background

There're some BAU scenarios that MO would perform trade amendment to update the non economic trade attributes, according to the strategy FMRP design Stella cashflow generation behavior is as below.

- Stella will withdrawal the C1, C2 and create new C3, C4.
- All these cashflow id & events would be sent down to TDS3->Ratan.

| | ## Stella |
| --- | --- |
| **FO/MO Action** | **Trade Event** | **Trade Action** | **Trade Id** | **Trade Major Version** | **Cashflow ID** | **Cashflow Event** |
| New Trade Booking | Trade | Book | T1 | V1 | C1 | New |
| C2 | New |
| Non Economic Amendment | Trade | Update | T1 | V2 | C1 | Withdrawal |
| C2 | Withdrawal |
| C3 | New |
| C4 | New |

# Problem Statement

The non economic cashflows C3, C4 will impact the settlement process as settlement ops don't expect any settlement activities on the non economic trade amendment.

| | ## Stella | | ## Ratan Cashflow Blotter |
| --- | --- | --- | --- |
| **FO/MO Action** | **Trade Event** | **Trade Action** | **Trade Id** | **Trade Major Version** | **Cashflow ID** | **Cashflow Event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Status** |
| New Trade Booking | Trade | Book | T1 | V1 | C1 | New | C1 | New | SETTLED |
| C2 | New | C2 | New | SETTLED |
| Non Economic Amendment | Trade | Update | T1 | V2 | C1 | Withdrawal | C1 | Withdrawal | SETTLED |
| C2 | Withdrawal | C2 | Withdrawal | SETTLED |
| C3 | New | C3 | New | PROJECTED |
| C4 | New | C4 | New | PROJECTED |

# Proposed solution

- Discard the non economic cashflow C3, C4 in Ratan, these won't be visible for settlement ops.
- Only the cashflows(C5, C6 below) from trade economic trade amendment would be taken for settlement process.

| | ## Stella | | ## Ratan Cashflow Blotter |
| --- | --- | --- | --- |
| **FO/MO Action** | **Trade Event** | **Trade Action** | **Trade Id** | **Trade Major Version** | **Cashflow ID** | **Cashflow Event** | **Cashflow ID** | **Cashflow Event** | **Cashflow Status** |
| New Trade Booking | Trade | Book | T1 | V1 | C1 | New | C1 | New | SETTLED |
| C2 | New | C2 | New | SETTLED |
| Trade Non Economic Amendment | Trade | Update | T1 | V2 | C1 | Withdrawal | C1 | New | SETTLED |
| C2 | Withdrawal | C2 | New | SETTLED |
| C3 | New | | | |
| C4 | New | | | |
| Trade Economic Amendment | Trade | Update | T1 | V3 | C3 | Withdrawal | C1 | Withdrawal | WAITING |
| C4 | Withdrawal | C2 | Withdrawal | WAITING |
| C5 | New | C5 | New | PROJECTED |
| C6 | New | C6 | New | PROJECTED |

# Integration with Stella & CDU

- Ratan only update the status to the active cashflows (C3, C4 after the non eco amendment)
- CDU will always take the latest trade id + Trade version for the confirmation status notification regardless it's eco or non eco trade amendment, Ratan would follow this principle to drive the cashflow STP.

| | ## Stella | | ## Ratan Cashflow Blotter | | ## CDU |
| --- | --- | --- | --- | --- | --- |
| **FO/MO Action** | **Trade Event** | **Trade Action** | **Trade Id** | **Trade Major Version** | **Cashflow ID** | **Cashflow Event** | **Cashflow Status** | **Cashflow ID** | **Cashflow Event** | **Cashflow Status** | **Expected CDU Confirmation Identifier** | **Trade Event** | **Trade Action** | **Trade Id** | **Trade Version** |
| New Trade Booking | Trade | Book | T1 | V1 | C1 | New | PROJECTED | C1 | New | PROJECTED | T1 + V1 | Trade | Book | T1 | V1 |
| C2 | New | PROJECTED | C2 | New | PROJECTED |
| Trade Non Economic Amendment | Trade | Update | T1 | V2 | C1 | Withdrawal | PROJECTED | C1 | New | SETTLED | T1 + V2 | Trade | Update | T1 | V2 |
| C2 | Withdrawal | PROJECTED | C2 | New | SETTLED |
| C3 | New | PROJECTED->SETTELD | | | | |
| C4 | New | PROJECTED->SETTELD | | | | |
| Trade Economic Amendment | Trade | Update | T1 | V3 | C3 | Withdrawal | SETTLED | | | | | Trade | Update | T1 | V3 |
| C4 | Withdrawal | SETTLED | | | | |
| C5 | New | PROJECTED | C5 | New | PROJECTED | T1 + V3 |
| C6 | New | PROJECTED | C6 | New | PROJECTED | |