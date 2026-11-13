# 1. Design Diagram

# 2. Service Changes

| Services | Changes | Comment |
| --- | --- | --- |
| Group service | 1. Change FXUSettlementCommand 2. Lookup static data by new API, query conditon is booking fmid /counparty fmid / currency/ family / group | Any exception then set settlement as UNKNOWN |
| Lifecycle service | Change precheck API, add a validation for settlement method | If settlementMethod = UNKNOWN, update status to TechFail |
| Ssi service | Change | |
| Static data service | 1. Provide a new API for new table query 2. Update static data table 3. Cache data | |