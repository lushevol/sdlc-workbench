# Business Events:

| Business Event | Applicable for Egypt | Applicable for CN & Onward |
| --- | --- | --- |
| Trade | Y | Y |
| Amendment | Y | Y |
| Withdrawal | Y | Y |
| Termination | N | Y |
| Partial Termination | N | Y |
| Novation | N | Y |
| Expiry | N | Y |
| Allocation | N | Y |
| Close Out | N | Y |

# Stella Business Events & Actions impact cashflow:

Cashflow Amendment event can be Withdrawal&New if the previous cashflow event is settled in Ratan.

| Business Event | Action | Pre Trade Status | Target Trade Status | CDU Confirmation | Cashflow Events | Sample Cashflows |
| --- | --- | --- | --- | --- | --- | --- |
| Trade | Book | TOBESENT/SENT | TOBESENT | | New | |
| | Update(Economic) | TOBESENT/SENT | TOBESENT | | 1. New → Amendment 2. New ( Cashflow Partial update) | |
| | Update(Non-Economic) | TOBESENT/SENT | | | | |
| | Cancel | TOBESENT/SENT | TOBESENT | | 1. New → Withdrawal 2. New → Amendment → Withdrawal | |
| Amendment | Book (Economic) | AFFIRMED/CONFIRMED | TOBESENT | | 1. New → Amendment 2. New ( Cashflow Partial update) | |
| | Book (Non-Economic) | AFFIRMED/CONFIRMED | TOBESENT | | New | |
| | Update (Economic) | TOBESENT/SENT | TOBESENT | | 1. New → Amendment → Amendment 2. New → Amendment 3. New | |
| | Update (Non-Economic) | | | | | |
| | Cancel | TOBESENT/SENT | TOBESENT | | 1. New →Amendment ->Withdrawal 2. New → Withdrawal | |
| Withdrawal | Book | AFFIRMED/CONFIRMED | TOBESENT | | 1. New→ Withdrawal 2. New → Amendment → Withdrawal | |
| | Undo (Revive) | TOBESENT/SENT | TOBESENT | | 1. New→ Withdrawal → Amendment 2. New → Amendment → Withdrawal → Amendment | Trade ID: 3860748027 |
| Termination | Book | | TOBESENT | | Withdrawal/New | |
| | Undo | TOBESENT/SENT | TOBESENT | | Withdrawal/New | |
| Partial Termination | Book | | | | Amendment/New/Withdrawal | |
| | Undo | | | | | |
| Close Out | Book | | | | | |
| | Update | | | | | |
| | Cancel | | | | | |
| Expiry | Book | | | | | |
| Novation | Book | | | | | |
| Allocation | Book | | | | | |

# Trade Events Scenarios

- 3860748027 ![image2023-5-11_12-15-49.png](attachments/image2023-5-11_12-15-49.png)![image2023-5-11_12-18-49.png](attachments/image2023-5-11_12-18-49.png)