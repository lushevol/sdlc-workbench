Subject updated to 1) APPNAME-XXXXX

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Zhenzhen Liu | 2026-09-10 | | | |

### **Description **

- Currently, when Orchestration decides a cashflow is ready to be settled, it publishes the SCBML to a Kafka topic. Swift Service consume it, generates the MT message, and immediately sends it to Downstream. There is no checker between "generate" and "send". LMC is shorter for Last Mile Checker.
- ### Common Checks | **1** | **Duplicate send Checker** | Based on (CashflowID + BusineesVersion + EventType +MessageType) to check if there is existing record in Last Mile Check data result table | #### ***<u>Last Mile Check</u>*** | #### **Block** | `SELECT` `id, cashflow_id, business_version, tracking_id, lmc_sub_status, check_status` `FROM` `lmc_check_result` `WHERE` `cashflow_id = :cashflowId` ` ``AND` `event_type = :eventType` ` ``AND` `business_version = :businessVersion` ` ``AND` `message_type = :messageType` ` ``AND` `lmc_sub_status ``IN` `(``'SENT'``, ``'FORCE_RELEASED'``, ``'PENDING_CONFIRMATION'``)` `ORDER` `BY` `created_at ``DESC` | | --- | --- | --- | --- | --- | --- | | **2** | **Economic Checker** | system will check the individual Swift economic details matches it's original Cashflow economic details or not. (bookingEntityFmid + counterpartyFmid + paymentAmount + paymentCurrency + paymentDate ) | #### ***<u>Last Mile Check</u>*** | #### **Block** | `SELECT` `DISTINCT` `cashflow_id, business_version, tracking_id, lmc_sub_status` `FROM` `lmc_check_result` `WHERE` `booking_entity_fmid = :bookingEntityFmid` ` ``AND` `counterparty_fmid = :counterpartyFmid` ` ``AND` `payment_amount = :paymentAmount` ` ``AND` `payment_currency = :paymentCurrency` ` ``AND` `payment_date = :paymentDate` ` ``AND` `trade_id ``IS` `NOT` `DISTINCT` `FROM` `CAST``(:tradeId ``AS` `TEXT)` ` ``AND` `cashflow_id <> :excludeCashflowId` ` ``AND` `lmc_sub_status ``IN` `(``'SENT'``, ``'FORCE_RELEASED'``, ``'PENDING_CONFIRMATION'``)` |

### **Main Flow Diagram **

![v33.png](attachments/v33.png)

### **Tables**

List the function related tables and description

| # | Table Name | Description |
| --- | --- | --- |
| 1 | ratanone_last_mile_check.lmc_check_result | Main table for LMC |
| 2 | ratanone_last_mile_check.lmc_check_result_checker | All LMC status records of main table |
| 3 | ratanone_last_mile_check.lmc_check_result_suspicious_ref | Relevant suspicious cashflow ID record of main table |

### **Jobs**

List the function related jobs and description

| # | Job Name | Description |
| --- | --- | --- |
| 1 | Job name | Short description for job |
| 2 | | |

### **Topic/queue/service related **

List the function related topic queue service and description

| # | Name | Description |
| --- | --- | --- |
| 1 | name | Short description |
| 2 | | |

### **Main Tools **

List the function introduced Tools

| Tools Name | Description |
| --- | --- |
| Tool name | Short description |

### **Issue**

- List the related issue links or you can insert "Content by Label" macro, then all KB with same label would show here

### **Related articles **

- [Last Mile Checker - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Last+Mile+Checker)