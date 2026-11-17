Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta | 2026-01-13 | | | |

### **Description **

For the FX deals which are booked in FM booking system(S2BX, BLADE) tend to make a payment to Transaction Banking Client(Trade Services, Cash Management, or Security Services) account by intervention of CMO/Trade/Securities OPS. This is known as FX Utilization.

In the current environment, prior to settlement/value date, the client will instruct TB on how to ‘**utilize**’ the settlement currency amount.  Transaction Banking Operations (Trade Services, Cash Management, or Security Services) then login into SCPAY/FX Util to retrieve the deal, and apply payment instructions by link with AA code. Once claimed, the utilization details will be updated to RATAN.

- RATAN would publish bridge and util accounting to EBBS on real time base.
- SWIFT will be generated in Transaction Banking systems, which would send util accounting to PSGL
- Utilization accounting recon will be performed in TLM.

Ratan also opens API for BLADE and FXU for remaining amount query. -day2

- In FXU, remaining amount will be used for further utilization.
- In Blade, remaining amount will be used for booking reverse trade.

In short, the settlement has been performed from other systems, but **accounting **needs to perform from Ratan via FXU process

### **Main Flow Diagram**

- Cashflow received from Ratan, there is util account validation service rule checking, according to booking entity +counterparty to identify if util cashflow, if so, no swift to generate but pending accounting. ** **
- User can trigger request from FXU(support by Razor) to query via trade id and check the cashflows in Ratan via Grafql
- User can trigger utilization request to Ratan and trigger accounting on VD ,and send same to EBBS
- Ratan would return utilization status back to FXU
- Ratan returns utilization status back to TDS3 for lock amendment by Stella API call
- Past due if no utilization is done and accounting by past due account as EOD auto utilization(day2)
- Partial accounting might be introduced on day2

**![image-2026-1-13_10-21-15.png](attachments/image-2026-1-13_10-21-15.png)**

**![image-2026-1-13_10-22-32.png](attachments/image-2026-1-13_10-22-32.png)**

**FXU function flow:**

![image-2026-1-13_10-24-27.png](attachments/image-2026-1-13_10-24-27.png)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratan_fx_cashflow_brief_info | cashflow data main table |
| 2 | ratan_fx_cashflow_utilization_history | utilization record table |
| 3 | ratan_fx_accounting_send_failed_info | accounting failed retry table |
| 4 | ratan_fx_utilization_response_failed_info | utilization ack failed retry table |

### **Jobs**

List the function related jobs and description

| # | Job Name | Cron | TimeZone | Description |
| --- | --- | --- | --- | --- |
| 1 | EGAutoUtilizeScheduler | 0 30 16-18 * * ? | GMT | auto utilize & pastdue job for EG |
| 2 | SAAutoUtilizeScheduler | 0 30 16-18 * * ? | GMT | auto utilize & pastdue job for SA |
| 3 | NPAutoUtilizeScheduler | 0 15 15-17 * * ? | GMT | auto utilize job for NP |
| 4 | AccountingFailedJobRetry | 0 0/5 * * * * | | account failed retry job |
| 5 | UtilizeResponseFailedJobRetry | 30 0/5 * * * * | | utilize response failed retry job |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Type | Name | Description |
| --- | --- | --- | --- |
| 1 | Topic | cash_settlement_cashflow_domain_events | domain event topic for cashflow upsert |
| 2 | Topic | Cash_Settlement_FXU_Request_In | manual utilization request topic |
| 3 | Topic | Cash_Settlement_FXU_Ack | manual utilization response top |
| 4 | Topic | Cash_Settlement_FXU_Accounting_Event | accounting event out topic |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here

### **Related articles **

- [FXU Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Technical+Design)
- [FXU - RATAN analysis - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+-+RATAN+analysis)