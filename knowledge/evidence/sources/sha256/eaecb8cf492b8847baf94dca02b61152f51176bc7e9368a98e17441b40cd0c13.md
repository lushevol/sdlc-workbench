# Background

# ADO

[Story 11137292 [Manual Rounding]](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11137292)

# Requirement Detail

- User must be able to add/decrease few cents to the cashflow amount for payment
- Control must be there to ensure the increase/decrease is less than USD 1， use the exchange rate from upstream(refer to existing authorization limit process)
- Settlement Accounting will ~~follow original cashflow amount ~~- follow the existing process: swift /accounting use the same updated amount
- [must align with Recon team] TLM? to check the possible break between trade/cashflow
- Cashflow state for the action? WAITING
- UI popup：design to be added, only the amount and ccy usd amount in the popup, ![image-2025-10-22_15-23-32.png](attachments/image-2025-10-22_15-23-32.png)
- maker/checker required