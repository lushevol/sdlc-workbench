# Requirement

1. New -code, type
2. withdrawal - also stamp- or should directly cancel?
3. All trade level, cashflow level and fixing notice level activities will trigger Uber message generation. 1. Trade booking & market event 2. Trade status update 3. Fixing & re-fixing 4. New cashflow generation & cashflow status update
4. **Latest & Full **trade/fixing notice/cashflow/**schedule** information should be captured in the Uber message. 1. When new trade booking & market event performed, the underlying cashflows should be fully captured in the Uber message. No missing or wrong cashflows. And for current business event, **there should be identifier shows which cashflows are published by this business event**. (No, check the trade tracking version and cashflow version) 2. When there’s new Uber generating from trade status update, the Uber message would capture all the latest status of trade/fixing notice/cashflows within the same parent trade. 3. When there’s fixing & re-fixing, there should be unique correlation id for fixing notice, schedule & underlying cashflow ( used to link the cashflow with fixing notice). 4. When there’s new Uber generating cashflow status update, the Uber message would capture all the latest status of trade/fixing notice/cashflows within the same parent trade. 5. **Exception Handling ** 1. SLA, how long will it take to resolve the error 2. who is taking care of the exception → Middle Office 3. Latest version of trade and cashflow 4. Introduce error message into Uber? 5. Current production failure and turn around time
5. Technical** Sequence identifier** 1. Latest version in trade version x and cashflow also with version x 2. Uber message generation timestamp
6. Settlement Instruction, can it be included in protobuff?- To be checked with Olexiy
7. Adhoc query for Uber message (Trade ID + Asof Time)

# Settlement Business Scenario

1. Settlement Process - Cashflow Processing
2. Settlement Process - Eco/Non-Eco Amendment information
3. Settlement Process - Need to query Trade Fields
4. Settlement Process - SSI Stamping for trade and cashflow
5. Settlement Process - Trade Validation and Confirmation

- ## Cashflow Processing

| | Trade ID | Cashflow ID | Business Event | Sequence | Count | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | T1 | C1 | New | 1 | 5 | |
| 2 | T1 | C2 | New | 2 | 5 | |
| 3 | T1 | C3 | New | 3 | 5 | |
| 4 | T1 | C4 | New | 4 | 5 | |
| 5 | T1 | C5 | New | 5 | 5 | Exception |

- ## Non-Eco Amendment Control

| | Trade ID | Cashflow ID | Business Event | Sequence | Count | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | T1 | C1 | New | 1 | 2 | |
| 2 | T1 | C2 | New | 2 | 2 | |
| 3 | T1 | C1 | Withdrawal | 1 | 4 | |
| 4 | T1 | C2 | Withdrawal | 2 | 4 | Exception, may have duplicate payment |
| 5 | T2 | C3 | New | 3 | 4 | |
| 6 | T2 | C4 | New | 4 | 4 | |

- ## MO Trade Validation

| | Trade ID | Cashflow ID | Business Event | PENDING_TRADE_VALIDATION | Sequence | Count | Exception |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | T1 | C1 | New | Yes | 1 | 5 | |
| 2 | T1 | C2 | New | Yes | 2 | 5 | |
| 3 | T1 | C3 | New | Yes | 3 | 5 | |
| 4 | T1 | C4 | New | Yes | 4 | 5 | |
| 5 | T1 | C5 | New | Yes | 5 | 5 | Exception |

1. Trade confirmation (Trade and cashflow business version/event are matched)