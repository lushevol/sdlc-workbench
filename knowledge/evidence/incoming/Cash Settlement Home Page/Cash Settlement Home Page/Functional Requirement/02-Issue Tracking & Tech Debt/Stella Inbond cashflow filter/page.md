# Background

Normally the new cashflow generation would be driven by trade events that the cashflow events and major version would be increased, RATAN would take these as business change on cashflow and consume these new cashflows. But there're some other scenarios the cashflows would be updated without trade events, most common case as below.

1. Status update driven by RATAN
2. Stella cashflow expiry

# Problem

There's some confusion caused by these

Production cases:

- New cashflow + Expiry + Withdrawal: There're 2 new event while only one withdrawal event, the withdrawal can only offset one new event.
- ![image2024-11-13_10-30-26.png](attachments/image2024-11-13_10-30-26.png)