# Background

There's design agreement between Murex & RATAN that the original trade id would retain the same during the whole trade lifecycle( trade booking or market events), RATAN is rely on this agreement to group the cashflows belong to the same booking. But there's exception case which is breaking this agreement when there's special market event 'Counterparty Assignment' performed in Murex 2.11.

# Good production booking with agreed model

| **Murex Event** | **Original Trade Id** | **Trade ID** | **Payments** | **Payment Snapshot** | **RATAN Process** |
| --- | --- | --- | --- | --- | --- |
| New booking | 99434373 | 99434373 | 112877123 | '112877123' | 112877123 is the only payment under the original trade 112877123 |
| |
| Trade C&R | 99434373 | 99706143 | 113352621 | '112877123','**113352621**' | **113352621 **is the additional payment under the original trade 112877123 |
| |
| Trade C&R | 99434373 | 99713131 | 113363859 | 112877123','113352621','**113363859**','**113369339**' | **113363859 **and **113369339 **are the additional payments under the original trade 112877123 |
| 113369339 | 112877123','113352621','**113363859**','**113369339**' |

# New exception case with special market event Counterparty Assignment

| **Murex Event** | **Original Trade Id** | **Trade ID** | **Payments** | **Payment Snapshot** | **RATAN Process** |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| |
| | | | | | |
| |
| | | | | | |
| | |