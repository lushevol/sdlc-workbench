15th switch to H2

March

Case 1:  VD after  H2

| | Send Date | Group | MxSystemDate | VD | Status | Adaptor Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| Realtime (H1) | 10th (Monday) | C1 C1 SNTR C2 INIT C3 INIT | 10th | 18th(Tue) | PENDING | MxSystemDate <= VD <= MxSystemDate+9 C1 C2 C3 in same group |
| Switch to model 2 | | | | | | |
| Realtime (H2) | 17th(Monday) | C2 C1 SNTR C2 SNTR C3 INIT | 17th | 18th(Tue) | PENDING | Find C2 already in group C1/C2/C3, cashflow count = 2 |
| Realtime (H2) | 17th(Monday) | C3 C1 SNTR C2 SNTR C3 SNTR | 17th | 18th(Tue) | COMPLETED | Find C2 already in group C1/C2/C3, cashflow count = 3 |

Case 2: H1  MxSystemDate+9 = H2

| | Send Date | Group | MxSystemDate | VD | Status | Adaptor Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| Realtime (H1) | 6th (Thursday) | C1 C1 SNTR C2 INIT C3 INIT | 6th(Thursday) | 15th(Saturday) | PENDING | MxSystemDate <= VD <= MxSystemDate+9 C1 C2 C3 in same group |
| Realtime (H1) | 14th(Friday) | C2 C1 SNTR C2 SNTR C3 INIT | 14th | 15th(Saturday) | PENDING | Find C2 already in group C1/C2/C3, cashflow count = 2 |
| Switch to model 2 | | | | | | |
| Realtime (H2) | 15th(Saturday) | C3 C1 SNTR C2 SNTR C3 SNTR | 15th | 15th(Saturday) | COMPLETED | Find C2 already in group C1/C2/C3, cashflow count = 3 |

Case 3:  VD = H2

| | Send Date | Group | MxSystemDate | VD | Status | Adaptor Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| Realtime (H1) | 6th | C1 C1 SNTR C2 INIT C3 INIT | 17th(Monday) | 17th | PENDING | MxSystemDate <= VD <= MxSystemDate+9 C1 C2 C3 in same group |
| Switch to model 2 | | | | | | |
| Realtime (H2) | 15th(Friday) | C2 C1 SNTR C2 SNTR C3 INIT | 17th | 17th | PENDING | Find C2 already in group C1/C2/C3, cashflow count = 2 |
| Realtime (H2) | 15th(Saturday) | C3 C1 SNTR C2 SNTR C3 SNTR | 17th | 17th | COMPLETED | Find C2 already in group C1/C2/C3, cashflow count = 3 |

Case 4:  CNCL after H2 go-live date

| | Send Date | Group | MxSystemDate | VD | Status | Adaptor Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| Realtime (H1) | 10th (Monday) | C1 C1 SNTR C2 INIT C3 INIT C4 INIT | 10th | 19th | PENDING | MxSystemDate <= VD <= MxSystemDate+9 C1 C2 C3 in same group |
| Realtime (H1) | 15th(Friday) | C2 C1 SNTR C2 SNTR C3 INIT C4 INIT | 17th | 17th | PENDING | Find C2 already in group C1/C2/C3/C4 cashflow count = 2 |
| Switch to model 2 | | | | | | |
| Realtime (H2) | 15th(Saturday) | C4 C1 SNTR C2 SNTR C4 SNTR C3 CNCL | 17th | 17th | COMPLETED | Find C2 already in group C1/C2/C3/C4 cashflow count = 4 C3 found in C1/C2/C3/C4 , send force complete to group |