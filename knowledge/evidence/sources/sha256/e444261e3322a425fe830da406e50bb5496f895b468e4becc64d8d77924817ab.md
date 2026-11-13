[Story 13292989 Netting ID and Splitting ID prefix change to configurable](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13292989)

1.Analyze msg: find the diff between no netting/spliting and yes ...

| ACTION | RULE |
| --- | --- |
| Spliting | getAmountSplitRule(entityFmId, nostrolAgent, currency) |
| Netting | orchestration call ratan-rule-servicecheckIrsRule |

2.Analize code:

| action | service | sub action | | ut |
| --- | --- | --- | --- | --- |
| Spliting | netting lifecycle | autoSplit manualSplit unsplit -- 1 unNetAndUnSplitCashflowsWithLock (moveStatus) splitWithdrawal | | |
| Netting | nettingCashFlow--netOrAffirm --generateResultantCashflowId // callLifecycleToNet--batchUpdateStatus unNetCashFlow -- 2 unNetAndUnSplitCashflowsWithLock (moveStatus) | hard code | |

3.Plan

| DATA CENTER PREFIX | SPLITING | NETTING | ORIGIN CODE | example | NOTE |
| --- | --- | --- | --- | --- | --- |
| GDC | S | N | S -- Utils.getCashFlowId(Constant.SPLIT_CASHFLOW_PREFIX, 11, String.valueOf(cashflowIdSeq)); N -- Utils.getCashFlowId("N", 11, String.valueOf(cashflowIdSeq)); | length.size = 12 S00050110905 N00000001832 | select nextval('cashflow_id_seq') |
| ID | SID | NID | | length.size should keep 12 SID000062866 | will this affect the amount of cashflow? |

![image-2026-5-14_13-34-38.png](attachments/image-2026-5-14_13-34-38.png)![image-2026-5-18_9-31-39.png](attachments/image-2026-5-18_9-31-39.png)