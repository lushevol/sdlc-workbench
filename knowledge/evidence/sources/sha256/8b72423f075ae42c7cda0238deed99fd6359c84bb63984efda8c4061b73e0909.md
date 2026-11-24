| [Feature 4069981 Business Feature - MO Trade validation and associated workflow changes](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/4069981) | High Level: [MO Validation - Design - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/MO+Validation+-+Design)Detailed: [MO Trade Review Process - Episode 2 - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/MO+Trade+Review+Process+-+Episode+2) |
| --- | --- |
| [Feature 7703895 Business Feature - FMRP should move all trades which do not require confirmation to NONCONFIRMED status](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7703895) | [MO Validation - Design - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/MO+Validation+-+Design) |

New Trade Booking+Cancel/Withdrawal+New

| **Trade process** | **Business Event** | **Trade ID** | **Major Version** | **Trade Status** | | **Available in Blotter** | **Cashflow Id** | **Major Version** | **Message State** | **Cashflow Events** | **Cashflow Status** | **Exception** | **Available Action** | **Pay/Receive** | **Amount** | **Currency** | **Value Date** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| New Trade booking | Trade | 123 | 1 | BOOKED | No | C1 | 1 | HOLD | New | NA | | | Pay | 100 | USD | 5/10/2024 |
| | | | | | | | | | | | | | | | | |
| Auto validated by rule | Trade | T1 | 1 | TOBESENT | | | | | | | | | | | | |
| | | | | | YES | C1 | 1 | HOLD | New | NA | | | Pay | 100 | USD | 5/10/2024 |
| Trade amendment | Trade | T1 | 2 | BOOKED | | | | | | | | | | | | |
| | | | | | No | C1 | 2 | CLOSED | Withdrawal | NA | | | Pay | 100 | USD | 5/10/2024 |
| | | | | | | No | C2 | 1 | | New | | | | | | | |
| Trade amendment auto validated | Trade | T1 | 2 | TOBESENT | | | | | | | | | | | | | |
| | | | | | | Yes | C1 | 2 | CLOSED | Withdrawal | NA | | | Pay | 100 | USD | 5/10/2024 |
| | | | | | | Yes | C2 | 1 | | New | | | | | | | |