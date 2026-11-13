# Key Identifiers:  [https://confluence.global.standardchartered.com/display/FMRP/Key+Trade+Identifiers+and+Versions+-+Description+and+Scenarios](https://confluence.global.standardchartered.com/display/FMRP/Key+Trade+Identifiers+and+Versions+-+Description+and+Scenarios)

- Blade would book the packages trades as one contract, but will generate individual trade SCBML for each single trade in the same package
- Blade would populate the link id (RFQID) for the structure booking, this id would be available in each of the individual trade SCBML
- Stella will populate its own package id and enrich to each trade SCBML
- CDU have the plan to consolidate all individual trade SCBML and populate one confirmation document for the full package (combination of all individual trade SCBML with same package id) - TBC
- CDU will discuss with Stella the approach how CDU update the confirmation status back to Stella. - TBC

| Blade Source Package ID(RFQID) | Stella package ID | Trade ID | Trade SCBML | CDU Confirmation | Tracking Version | Trade Type | Cashflow ID | Cashflow SCBML | Payment Type | Currency | Amount | Pay/Receive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6c9a1f12-5899-490d-901b-036edbdfd75e | 65e2fda7-ef2d-48e2-93a7-0ad3073e67ce | 3375505333 | | TBC | 0 | NDF | 003375505334 | | Broker Fee | USD | 1000 | Pay |
| 3375505335 | | TBC | 0 | FX Swap | 003375505336 | | Broker Fee | USD | 1000 | Pay |
| TBC | 0 | FX Swap | 003375505337 | | Cashflow-NearLeg | JPY | 100190000 | Pay |
| TBC | 0 | FX Swap | 003375505339 | | Cashflow-NearLeg | GBP | 759357.96 | Receive |
| TBC | 0 | FX Swap | 003375505338 | | Cashflow-FarLeg | GBP | 759418.91 | Pay |
| TBC | 0 | FX Swap | 003375505340 | | Cashflow-FarLeg | JPY | 100190000 | Receive |