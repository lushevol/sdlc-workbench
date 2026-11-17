# Functionality to demo:

- Cashflow data store in Ratan:
- Cashflow materialization:

# User cases

| NO. | Description | Steps | Expected Result |
| --- | --- | --- | --- |
| 1 | Stella New & VD-7 | 1. Mock Stella new message with payment date as VD-7 2. Manually push new message to Ratan workflow 3. Load cashflow from cashflow blotter | 1. Ratan can store cashflow in database as 'Projected' cashflow 2. Display in cashflow blotter GUI. |
| 2 | Stella New & VD-5 | 1. Mock Stella new message with payment date as VD-5 2. Manually push new message to Ratan workflow 3. Load cashflow from cashflow blotter | 1. Ratan can store cashflow in database as 'Queued' cashflow 2. Display in cashflow blotter GUI. |
| 3 | Stella New & VD-4 | 1. Mock Stella new message with payment date as VD-4 2. Manually push new message to Ratan workflow 3. Load cashflow from cashflow blotter | 1. Ratan can store cashflow in database as 'Queued' cashflow 2. Display in cashflow blotter GUI. |
| 4 | Stella VD-7 and run materialization on VD-5 | 1. Mock Stella new message with payment date as VD-7 2. Manually push new message to Ratan workflow 3. Run the materialization job on VD-5 | 1. Ratan store the cashflow as 'Projected' on VD-7 2. Ratan move the status to 'Queued' on VD-5 |
| | Stella New + Amendment (VD-4) | 1. Mock Stella new message with payment date as VD-4 2. Mock Stella Amendment message on same cashflow | 1. Display the amendment cashflow only and discard the new |
| 5 | Netting Status Moving | 1. Mock component cashflows 2. Run the netting API manually | 1. Component cashflow moved to 'Netted' 2. Resultant cashflow created as 'Queued'. |