- Existing MX2.11 SSI's will be re-used by RATAN
- RATAN will fetch the SSI's based on the CFI code stamped on the Cashflows; In SSI+, existing Security ID's need to be updated with the CFI code
- Since SSI's are not maintained at CFI code equivalent level, the CFI code updated in SSI+ will be different (example: XFXXXX across FX SPOT, FORWARD and SWAP products)
- For BLADE / CFETS / S2BX Trades, the CFI code will be stamped by STELLA on the Cashflows
- For MX2.11 Cashflows, RATAN has to do the CFI Code stamping. The First 2 characters of the CFI code that was stamped on MX2.11 trades in TDS3 will be maintained within RATAN for this purpose

# Vostro Statistics:

- The full list of Murex 2.11 Vostro SSI: The top 2 are 'Alert' SSI which are used for all applications, the remaining are Murex 2.11 specific securities.
- SSI assigned for CN payments with year 2022.
- Key Vostro attributes: 1. Swift Types for Murex 2.11 SSI( Security with Murex name) 2. There's no placeholder for field 58/59 for Murex 2.11 Vostro SSI. 3. Settlement Method( Murex Securities): 4. Branch id: There're some SSI missing branch info in ES. ![image2023-5-4_17-8-53.png](attachments/image2023-5-4_17-8-53.png) ![image2023-5-4_17-9-25.png](attachments/image2023-5-4_17-9-25.png) 5. Settlement Account/Means: The value of these 2 fields are blank for 98.8% Murex 2.11 SSI. 6. Cover payment flag: To explore if the Spare1 can help.
- CN trades using 'MXG BLANK'

Vostro Query Conditions in FMRP

![SSI_Query.jpg](attachments/SSI_Query.jpg)

# Branch identifiers in SSI+

- ![image2022-12-2_13-50-58.png](attachments/image2022-12-2_13-50-58.png)