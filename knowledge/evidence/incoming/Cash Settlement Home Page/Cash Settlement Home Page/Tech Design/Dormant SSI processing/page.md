## **Background**

Record the last used date of SSIs unused for 24 months and feed status update to SSI+ to be marked as inactive.

## **API design**

Provide an API that allows SSI+ to access daily incremental data on the SSIs that have been used, which covers both BCS and FMPR flows.

| | FMRP API | New BCS API | Comments |
| --- | --- | --- | --- |
| Host | dev: [https://fmo-shell-dev.uk.dev.net:8453](https://fmo-mfe-dev.uk.dev.net/) uat: https://[fmo-shell.uk.dev.net](http://fmo-shell.uk.dev.net/):[8453](https://fmo-mfe-dev.uk.dev.net/) fmrp2: https://[fmo-shell-fmrp2.pi.dev.net:8453](http://fmo-shell-fmrp2.pi.dev.net/) prod: https://[fmo-shell.gdc.standardchartered.com](http://fmo-shell.gdc.standardchartered.com/):8453 | |
| Path | /api/v2/data/provider/query/cashflows | /api/v1/cashflows/ssi/{paymentDate} | |
| Method | POST | GET | |
| Header | FMAA-Token：“string” FMAA-UserId:"string" (sample: srv.ratan.001) FMAA-AppId:"string" (sample: RATAN_APP) | EMS2 Entity **RATAN_FUNC** with role **SYS_RO** |
| Request | {"queryCondition": "Select Cashflow.cashflow_id, Settlement_Instruction.SSI_Unique_Id from cash_settlement_query_cn.cashflow_data where Settlement_Instruction.SSI_Unique_Id != '' and cashflow.payment_date = :paymentDate"} (format sample: '2026-04-09') | PathVariable (format sample: 2026-04-09) | |
| Response | success code 200 [ { "Settlement_Instruction.SSI_Unique_Id": "46647941", "Cashflow.Cashflow_Id": "M00015700529" }, { "Settlement_Instruction.SSI_Unique_Id": "46647941", "Cashflow.Cashflow_Id": "M00015700530" } ] ![image-2026-7-6_17-28-49.png](attachments/image-2026-7-6_17-28-49.png) | success code 200 [ { "Cashflow.Cashflow_Id": "100021100919", "Settlement_Instruction.SSI_Unique_Id": "00003462" }, { "Cashflow.Cashflow_Id": "100021100920", "Settlement_Instruction.SSI_Unique_Id": "00003462" } ] error code 500 parameter payment date format error { "status": 500, "errorCode": "SERVICE_INTERNAL_ERROR", "errorMessage": "Failed to convert value of type 'java.lang.String' to required type 'java.sql.Date'; Failed to convert from type [java.lang.String] to type [@org.springframework.web.bind.annotation.PathVariable java.sql.Date] for value [2024-07-161]", "metadata": null } | |

## **Entity Relationship**

BCS:

##

**DB script**

Query sql:

select cs.cashflow_id, va.ssi_id

from ratanone_stamping_service.cashflow_stamping cs,

ratanone_stamping_service.stamped_vostro_account va

where cs.id = va.cashflow_stamping_id

and va.ssi_id != ''

and cs.payment_date = :paymentDate

and cs.state in ('STP_STAMPING_SHIPPED');

Create index:

CREATE INDEX if not exists cashflow_stamping_payment_date_idx ON ratanone_stamping_service.cashflow_stamping USING btree (payment_date);

Rollback:

DROP INDEX IF EXISTS ratanone_stamping_service.cashflow_stamping_payment_date_idx;

**PT:**

[Feature 11933199 [Dormant SSI processing] RATAN Cash Settlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11933199)

## **Past 2 years report query**

WITH t1 AS (
    SELECT
        cd.ssi__ssi_unique_id,
        MAX(cd.cashflow__payment_date) AS payment_date
    FROM cash_settlement_query_cn.cashflow_data cd
    WHERE cd.ssi__ssi_unique_id != ''
      AND cd.created_at >= DATE '2024-07-18'
      AND cd.created_at < DATE '2026-07-18'
    GROUP BY cd.ssi__ssi_unique_id
),
t2 AS (
    SELECT
        t.ssi__ssi_unique_id,
        MAX(t.cashflow__payment_date) AS payment_date
    FROM cash_settlement_query_cn.cashflow_data_backup_20june2026 t
    WHERE t.ssi__ssi_unique_id != ''
      AND t.created_at >= DATE '2024-07-18'
      AND t.created_at < DATE '2026-07-18'
    GROUP BY t.ssi__ssi_unique_id
),
t3 AS (
    SELECT
        t.ssi__ssi_unique_id,
        MAX(t.cashflow__payment_date) AS payment_date
    FROM cash_settlement_query_cn.cashflow_data_backup_3months_prior_31jan t
    WHERE t.ssi__ssi_unique_id != ''
      AND t.created_at >= DATE '2024-07-18'
      AND t.created_at < DATE '2026-07-18'
    GROUP BY t.ssi__ssi_unique_id
),
t4 AS (
    SELECT
        va.ssi_id AS ssi__ssi_unique_id,
        MAX(cs.payment_date) AS payment_date
    FROM ratanone_stamping_service.cashflow_stamping cs
    JOIN ratanone_stamping_service.stamped_vostro_account va
      ON [cs.id](http://cs.id) = va.cashflow_stamping_id
    WHERE cs.state = 'STP_STAMPING_SHIPPED'
      AND va.ssi_id != ''
      AND cs.created_at >= DATE '2024-07-18'
      AND cs.created_at < DATE '2026-07-18'
    GROUP BY va.ssi_id
),
all_rows AS (
    SELECT * FROM t1
    UNION ALL
    SELECT * FROM t2
    UNION ALL
    SELECT * FROM t3
    UNION ALL
    SELECT * FROM t4
)
SELECT
    ssi__ssi_unique_id as ssi_id,
    to_char(MAX(payment_date),'YYYY-MM-DD') AS payment_date
FROM all_rows
GROUP BY ssi__ssi_unique_id
ORDER BY payment_date;