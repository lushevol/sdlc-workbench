# Function Breakdown

| Function Type | Function Name | New building | Effort Estimation | Comment |
| --- | --- | --- | --- | --- |
| Static Data | EBBS Account | N | NA | |
| Bridge Account | Y | Analysis: 8 Dev & Test: 12 UI : TBD | |
| Aspire Accounting (HK/TW) | Accounting Entries generation | Y | Analysis: 16 Dev & Test: 12 | 1. Accounting stamping ( cashflow VS underlying static data) 2. File format is BCDF, TBC the cashflows eligible for accounting feeding |
| Integration - EOD | Y | Analysis: 8 Dev & Test: 8 DevOps & Test: 12 | 1. EOD schedule by entity 2. Feeding data by BCDF file |
| EBBS Accounting(UK,SG/IN) | Accounting Entries generation -EOD | Y | Analysis: 16 Dev & Test: 12 | 1. Accounting stamping ( cashflow VS underlying static data) 2. File format is BCDF, TBC the cashflows eligible for accounting feeding |
| Integration - EOD Feeding | Y | Analysis: 8 Dev & Test: 8 DevOps & Test: 12 | 1. EOD schedule by entity 2. Feeding data by BCDF file |
| Sum | Analysis: 56 Dev & Testing: 76 | |

# EBBS feeding approach

- EOD approach by entity
- Realtime feeding by single payment