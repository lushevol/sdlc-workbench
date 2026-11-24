# Functionality to demo:

- Cashflow data store in Ratan:
- Cashflow materialization:
- Netting/Un-Netting:

# User cases

| NO. | Description | Steps | Expected Result |
| --- | --- | --- | --- |
| 1 | Stella New & VD-7 | 1. Mock Stella new message with payment date as VD-7 2. Manually push new message to Ratan workflow 3. Load cashflow from cashflow blotter | 1. Ratan can store cashflow in database as 'Projected' cashflow 2. Display in cashflow blotter GUI. |
| 2 | Stella New & VD-5 | 1. Mock Stella new message with payment date as VD-5 2. Manually push new message to Ratan workflow 3. Load cashflow from cashflow blotter | 1. Ratan can store cashflow in database as 'Queued' cashflow 2. Display in cashflow blotter GUI. |
| 3 | Stella New & VD-4 | 1. Mock Stella new message with payment date as VD-4 2. Manually push new message to Ratan workflow 3. Load cashflow from cashflow blotter | 1. Ratan can store cashflow in database as 'Queued' cashflow 2. Display in cashflow blotter GUI. |
| 4 | Stella VD-7 and run materialization on VD-5 | 1. Cashflow imported on VD-7 as 'Projected' (022022112410, 022022112405) 2. Run the materialization job on VD-5 | 1. Ratan moves the status to 'Queued' on VD-5 |
| 5 | Stella New + Amendment (VD-4) | 1. Mock Stella new message with payment date as VD-4 2. Mock Stella Amendment message on same cashflow | 1. Display the amendment cashflow only and discard the new |
| 6 | Netting | 1. Mock component cashflows 2. Perform Netting from GUI | 1. Component cashflow moved to 'Netted' 2. Resultant cashflow created as 'Queued'. 3. Amount of netting resultant cashflow is sum of component cashflows 4. Same netting id for component & resultant cashflow |
| 7 | Un-Netting | 1. Perform the un-net from GUI | 1. Component cashflow status moved back to 'Queued' 2. Resultant cashflow status moved to 'Dead' |