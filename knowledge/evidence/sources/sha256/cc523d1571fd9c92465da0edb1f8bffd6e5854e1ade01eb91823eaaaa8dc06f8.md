# AS-IS implementation

![image-2025-11-15_21-27-53.png](attachments/image-2025-11-15_21-27-53.png)

# Issue Reported

| Currency | Payment Date | Date from Netting Static | Auto netting date | CCY Calendar |
| --- | --- | --- | --- | --- |
| XAU | 2025-11-12 | VD-1 5AM | 2025-11-11 5AM | working day on 2025-11-11 |
| USD | 2025-11-12 | VD-1 5AM | 2025-11-10 5AM | USD holiday on 2025-11-11 |

| Event | System Date time | Trade | | Cashflow | Currency | Payment Date | Calculated auto netting date time | Cashflow State | Cashflow Sub State Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| New cashflow | 2025-11-07 4:00 | T1 | | C1 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting |
| C2 | USD | 2025-11-12 | 2025-11-10 5:00 | WAITING | Pending Auto Netting |
| New cashflow | 2025-11-10 3:00 | T2 | | C3 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting |
| C4 | USD | 2025-11-12 | 2025-11-10 5:00 | WAITING | Pending Auto Netting |
| Auto Netting job | 2025-11-10 5:00 | | | N1 | USD | 2025-11-12 | NA | WAITING | Pending Exception |
| | | C2 | USD | | NA | NETTED | |
| | | C4 | USD | | NA | NETTED | |
| New cashflow | 2025-11-10 7:00 | T3 | | C5 | XAU | | | | |
| | 2025-11-10 7:00 | C6 | USD | | | | |
| | 2025-11-10 7:15 | T4 | | C7 | XAU | | | | |
| | 2025-11-10 7:15 | | C8 | USD | | | | |
| Auto Netting job | 2025-11-10 7:30 | | | N2 | USD | 2025-11-12 | NA | WAITING | Pending Exception |
| | | C6 | USD | | NA | NETTED | |
| | | C8 | USD | | NA | NETTED | |
| Auto Netting job | 2025-11-11 5:00 | | | N3 | XAU | 2025-11-12 | NA | WAITING | Pending Exception |
| | | C1 | XAU | | NA | NETTED | |
| | | C3 | XAU | | NA | NETTED | |
| | | C5 | XAU | | NA | NETTED | |
| | | C7 | XAU | | NA | NETTED | |

# Solution Discussion

1. if there are high possibility that cashflow will be generated after the configured netting date time, should configure the netting date time to a later one.
2. Only skip Weekend, not holiday， 1. could resolve the issue user reported 2. potential issue: auto netting date time may fall into holiday - Dinesh confirmed it's acceptable, it OPS will take vacation on that day, they should manually net the cashflow without waiting for the system job. 3. release date time might be earlier than auto netting date time: | Cashflow | Currency | Payment Date | Date from Netting Static | Auto netting date (VD-1 without holiday) | Release Date(VD-1 BD) | | --- | --- | --- | --- | --- | --- | | C1 | XAU | 2025-11-12 | VD-1 5AM | 2025-11-11 5:00 | 2025-11-11 | | C2 | USD | 2025-11-12 | VD-1 5AM | 2025-11-11 5:00 | 2025-11-10 |
3. enhance the function to allow user to configure the system behavior after netting date time 1. move the post netting time cashflow to pending manual net for user to manual process 2. system auto net the post netting time cashflow | Event | System Date time | Cashflow | Currency | Payment Date | Calculated auto netting date time | Cashflow State | Cashflow Sub State Type | | --- | --- | --- | --- | --- | --- | --- | --- | | New cashflow | 2025-11-10 4:00 | C1 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | C2 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | C3 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | Auto Netting Job | 2025-11-11 5:00 | N1 | XAU | 2025-11-12 | | WAITING | Pending Exception | | | | C1 | XAU | | | NETTED | | | | | C2 | XAU | | | NETTED | | | | | C3 | XAU | | | NETTED | | | Withdrawal C1 and New C4 | 2025-11-11 6:00 | N1 | XAU | | | DEAD | | | C1 | XAU | | | CANCELLED | | | C2 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | C3 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | C4 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | Auto Netting Job | 2025-11-11 6:30 | N2 | XAU | 2025-11-12 | | WAITING | Pending Exception | | | | C2 | XAU | | | NETTED | | | | | C3 | XAU | | | NETTED | | | | | C4 | XAU | | | NETTED | | | Event | System Date time | Cashflow | Currency | Payment Date | Calculated auto netting date time | Cashflow State | Cashflow Sub State Type | | --- | --- | --- | --- | --- | --- | --- | --- | | New cashflow | 2025-11-10 4:00 | C1 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | C2 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | C3 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Auto Netting | | Auto Netting Job | 2025-11-11 5:00 | N1 | XAU | 2025-11-12 | | WAITING | Pending Exception | | | | C1 | XAU | | | NETTED | | | | | C2 | XAU | | | NETTED | | | | | C3 | XAU | | | NETTED | | | Withdrawal C1 and New C4 | 2025-11-11 6:00 | N1 | XAU | | | DEAD | | | C1 | XAU | | | CANCELLED | | | C2 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Netting | | C3 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Netting | | C4 | XAU | 2025-11-12 | 2025-11-11 5:00 | WAITING | Pending Netting |