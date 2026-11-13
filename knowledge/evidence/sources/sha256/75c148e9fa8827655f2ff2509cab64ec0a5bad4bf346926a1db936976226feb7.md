# Background

- Murex cashflows would feed into Ratan Cash Settlement VD-7 Business days earlier. And Stella also generate and feed these cashflows into Ratan Cash Settlement. Which means 7 business days cashflows **overlapped**. In case duplicated payments / accountings / LMS etc, agreed with upstream and downstream, Ratan Cash Settlement would handle it.

#### Problems and Obstacles

- Accurate murex cancelled cashflow id list provided on Saturday.
- Stella cashflow id list provided on Sunday.
- Hence have to use portfolio to NSTP cashflows which may enlarge the in-scope cashflows.

## Approach to **Stop processing **In-Scope **Murex2.11 Cashflows **in advance

## Murex cashflow process flow