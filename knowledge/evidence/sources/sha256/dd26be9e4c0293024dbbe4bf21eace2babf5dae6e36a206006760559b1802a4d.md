**Current process:**

****

**Proposal process:**

Question:

1. How to check the order of businessVersion + minorVersion ?
2. If retryNum > 3, throw exception or ?
3. Delay time ?

### Statistics of table "ratanone_cashflow_service__cqrs_cashflow_events":

- #### Records count: 811340
- #### Total DB size: 2301 MB
- #### Different event type calculations are following:

| Event type | Each event size (kB) | Contains SCBML | Records count | Records percent |
| --- | --- | --- | --- | --- |
| CashflowCreationEvent | 5.36 | Yes | 139540 | 17.20% |
| CashflowAmendEvent | 5.76 | Yes | 276965 | 34.13% |
| CashflowHoldInRatan | 1.14 | No | 34005 | 4.19% |
| CashflowSkipped | 1.14 | No | 50264 | 6.19% |
| CashflowStatusUpdateEvent | 1.14 | No | 310566 | 38.28% |

- #### If all CashflowHoldInRatan, CashflowSkipped, CashflowStatusUpdateEvent include SCBML to size as CashflowAmendEvent (5.76 kB), then DB size will increase **59%**, DB size=**3658.6 MB**