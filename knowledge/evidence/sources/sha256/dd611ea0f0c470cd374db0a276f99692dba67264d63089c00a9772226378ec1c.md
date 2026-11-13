## Background

In Cash Settlement processing, some scenarios require trade information:

1. LMS feed generation 1. Entity LEID 2. Trader ID
2. Cashflow Blotter Query (Potential) 1. Instrument (BCS)

| Options | Option 1 Cashflow service query TDS3 directly through Data Ambassador on each cashflow event | Option 2 Continue with the trade service currently we are using to consume all trades from TDS3 |
| --- | --- | --- |
| PROs | 1. Only partial data will be within Payment world, no silver copy issue | 1. Independent with payment processing |
| CONs | 1. New dependency | 1. Silver copy of trade data 2. Large data storage |