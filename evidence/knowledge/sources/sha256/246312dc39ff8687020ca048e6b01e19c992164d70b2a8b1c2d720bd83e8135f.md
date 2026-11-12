# 1.CCIL Cashflow

2. CCIL Netting

Changes

| Module | Function | Description |
| --- | --- | --- |
| ~~static data service ~~ | ~~new static data table~~ | ~~refer to [CCIL Netting - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CCIL+Netting)~~ |
| murex adaptor | identify the CCIL cashflow | - identify CCIL( **ccy=INO & family=IRS & group =IRD & fmid==4 and (counterparty in static data list or counterparty is ****400021949** )) - query static data DB in mxg, if hint, then set tag <scbextn:settlementMethod settlementMethodScheme="http://www.sc.com/coding-scheme/settlementMethod">CCIL</scbextn:settlementMethod> |
| rule service | add new NSTP rule for settlement method | - Settlement_Method = "CCIL" - if matched then Waiting+IsNettingEligible |
| netting service | netting review netting | - netting review change. allow different counterparties for (settlemenet method =CCIL) - netting change. netting resultant cashflow settlement method change to CASH Principle: 1. New controller for CCIL netting and preview 2. Reuse on the service layer for netting function without building new netting logic |
| frontend | add new logic model for Settlement_Method | - filter add settlement method value, drop-down (CASH / CCIL Netting) - identify normal netting and & CCIL netting - for CCIL netting, settlement method = CCIL & with the same entity/value date/currency and status is waiting+pending netting - normal netting can not be netted with CCIL netting cashflow |