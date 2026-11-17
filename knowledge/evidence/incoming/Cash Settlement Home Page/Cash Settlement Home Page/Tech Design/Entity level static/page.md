[FXU - RATAN analysis - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+-+RATAN+analysis)

# Background

For each entity onboarding, a bunch of configurations and static data to be setup to separate domains, which is costing massive effort on it.

1. Too many configuration to be uploaded as below table, which may even lead to manual error
2. No validation as they are completely manual checked
3. Slow speed to market, CR required for onboarding, at least 2 weeks

| **#** | **Description** | **Table** | **Type** | **Domain** | **Key** | **Comment** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bypass Validation Rule | ratanone.ratan_rule_engine | DB Static | Rule engine | | This will be dropped by new MO validation |
| 2 | Nostro Static Setup (mandatory for each entity) | ratanone.ratan_static__cashflow_nostro | Static | Static Data | Entity FMID + CCY + Settlement Means + Settlement Method | Self Serviced |
| 3 | Currency Release Time (mandatory for each entity) | ratanone.ratan_static_cashflow_currency_cut_off | DB Static | Static Data | Entity FMID + CCY | Can be made self-service |
| 4 | LMS Feed Exclusion Entity List Update | | Service Config | LMS | Entity FMID | Can be merged into 1 table to maintain Booking Entity Information, as well as self-service |
| 5 | SWIFT Generation Changes | ratanone_swift_service.swift_static_data_sender_bic ratanone_swift_service.swift_static_data_correspondent_bic | DB Static | Swift Service | Entity FMID |
| 6 | ratanone-static-data-service: Branch Code Mapping | | Config | Static Data | Entity FMID |
| 7 | Settlement Accounting | ratanone.ratan_static__cashflow_ebbs_txn_code ratanone.ratan_static__cashflow_ebbs_bridge_account | DB Static | Accounting service | Entity FMID |
| 8 | Include new branch in GUI Drop down | | UI Config | Cashflow Blotter | Entity FMID |
| 9 | STP White List | | Config | Workflow | Entity FMID |
| | | | | | |

# Proposal

Maintain 1 Table for above except for Nostro Static:

| ** ** | **Type** | **Possible Value** | **Comment** | **Nature** |
| --- | --- | --- | --- | --- |
| 1 | Booking Entity FMID | 300089409 | To cover above item 8, Include new branch in GUI Drop down | Data |
| 2 | Booking Entity FMCODE | SCB MNL FCD*MNL |
| 3 | Workflow Flag | Strategic/Legacy/CPT | To cover above item 9, STP White List | Config / Dev |
| 4 | LMS Filter | true/false | To cover above item 4, LMS Feed Entity White List | Config / Dev |
| 5 | Branch Code | 59 | To cover above item 6, ratanone-static-data-service: Branch Code Mapping | Data |
| 6 | country | PH | To cover above item 7 Settlement Accounting ratanone.ratan_static__cashflow_ebbs_txn_code ratanone.ratan_static__cashflow_ebbs_bridge_account | Data |
| 7 | posting_branch | 100 |
| 8 | txn_type_code | RTO |
| 9 | txn_dr_code | 478 |
| 10 | txn_cr_code | 378 |
| 11 | ebbs_bridge_account | 78653775888 |
| 12 | currency | PHP | To cover above item 5 ratanone_swift_service.swift_static_data_correspondent_bic ratanone_swift_service.swift_static_data_sender_bic | Data |
| 13 | Correspondent BIC | SCBLPHMMXXX |
| 14 | Sender BIC | SCBLPHMMXXX |

# Additional thinking

Common static for key/value, like below:

1. BIC netting static
2. FXU static
3. Profile limit