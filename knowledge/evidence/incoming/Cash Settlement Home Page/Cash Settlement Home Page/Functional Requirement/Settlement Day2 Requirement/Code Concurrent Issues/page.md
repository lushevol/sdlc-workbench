# Issue points

| | service | point | service | comment |
| --- | --- | --- | --- | --- |
| 1 | ratan-cashflow-lifecycle-service | MessageHoldingServiceImpl.filterNettingResultantCashflowsV2 filteredHoldingMessageVos | | |
| 2 | MessageHoldingServiceImpl.filterRegularCashflowsV2 filteredData | | |
| 3 | MessageHoldingServiceImpl.releaseV2 successHoldingIds | | no concurrency point |
| 4 | ratan-cash-settlement-ssi-stamping-service | NostroRefreshCommand.scrollQueryAndPublish queryResult | | |
| 5 | | SsiExceptionCommand.scrollQueryAndPublish queryResult | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |