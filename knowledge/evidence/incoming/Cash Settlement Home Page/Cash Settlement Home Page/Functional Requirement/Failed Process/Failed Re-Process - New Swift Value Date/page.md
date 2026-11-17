# Background:

Cashflows re-instate from 'FAILED' status will generate exception 'Re-Instate' and pending for Maker/Checker to re-process cashflow & fix this exception, Maker/Checker will select the '**Swift Value Date**'(Settlement_Instruction.Value_Date) as part of exception fix.

# Re-Instate & Excetpion:

- FMO Ops can right click on the 'FAILED' cashflow from cashflow blotter and perform action 'Re Instate'.
- Cashflow will go to 'QUEUED' status and run through the 'Netting client Check'/'Exception Check' process.
- As the result of 'Exception Check' there'll be dedicated exception 'Cashflow Re-Instate' generated.
- This is Maker/Checker exception and default as Maker's exception ('Pending Operator') when exception populated.

# Maker/Checker fix exception:

- Maker/Checker dual blind select required to decide the new '**Swift Value Date**'.
- Both Maker/Checker have 2 options to select the '**Swift Value Date'**. - The current cashflow 'Value Date' ( Cashflow.Payment_Date ): This will copy the cash flow 'Value Date' to the '**Swift Value Date**'. - User select new date: User can select any date as the '**Swift Value Date**'. ![New Swift Value Date.jpg](attachments/New Swift Value Date.jpg)
- After maker's submit the cashflow exceptions will move to Checker's page. When Checker try to submit the new date, system will verify Maker/Checker input. In case Maker's input is different with Checker's, system will populate warning message to Checker.
- With the system warning message and ff Checker consider his input is the correct one, checker can reject maker's input, cashflow exceptions will move back to Maker's page.