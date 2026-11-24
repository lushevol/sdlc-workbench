**Reuirment**

This part is to record the requirments confusion and clarified requirments in work.

| id | requirments confusion | clarified requirments | Sumbit Person | comment |
| --- | --- | --- | --- | --- |
| 1 | when maker/checker fix exception and enter the comment, where to display the comment entered? | The comment would be displayed in the cashflow audit table. | | ![comment.png](attachments/comment.png) |
| 2 | Do Netting Preview need to add the columns ' Fixing Rate 'and' Notional '? | is not available in the cashflow yet | | |
| 3 | IRS netting--when Murex send a cash have netted, how to handle？ | Murex will handle it, CN need not concerned. | | |
| 4 | For Cash flow Sub State Type and Cashflow Sub State. It should be State or Status? DB and requirement is status. DB: ![image2023-7-6_13-51-35.png](attachments/image2023-7-6_13-51-35.png) Requirement: ![image2023-7-6_13-53-12.png](attachments/image2023-7-6_13-53-12.png) | | @Ming Ni | ![image2023-7-6_13-49-21.png](attachments/image2023-7-6_13-49-21.png)![image2023-7-6_13-50-4.png](attachments/image2023-7-6_13-50-4.png) |

**Issue**

This part is to record the errors encountered and solutions.

| id | description | solution | comment |
| --- | --- | --- | --- |
| 1 | GUI pop up "ACTION_DENIED"; response 403 | user permission is wrong | |
| 2 | [https://fmo-mfe-dev.uk.dev.net:8453/api/ratan/v1/cashflow/currency/holiday](https://fmo-mfe-dev.uk.dev.net:8453/api/ratan/v1/cashflow/currency/holiday) | static data enterface, contact BAU | |
| 3 | cashflow details page, click [https://fmo-mfe.uk.dev.net:8453/api/ratan/bff/v1/counterparties](https://fmo-mfe.uk.dev.net:8453/api/ratan/bff/v1/counterparties) return 400 | the CN path is correct, but BAU has issue | |