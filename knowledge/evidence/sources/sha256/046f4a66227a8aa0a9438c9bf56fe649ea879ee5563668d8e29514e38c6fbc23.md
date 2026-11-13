# 1. Identify the problem

Issue After Feb.16th team released db index creation for netting related functions, but on Monday PSS still found DB CPU usage has high occupy.

With the enhancement we have done on 16th Feb, we can see the peak times reduces significantly from production data, peak for netting have gone.

| **Date** | **High CPU peak times (>90%)** **(S****can tool every 30 s) ** |
| --- | --- |
| Tue Feb 04 | 124 |
| Wed Feb 05 | 208 |
| Thu Feb 06 | 297 |
| Mon Feb 17 | 27 |

Other peaks as below:

![image2025-2-18_14-9-8.png](attachments/image2025-2-18_14-9-8.png)

Detailed CPU usage:

![image2025-2-18_14-46-54.png](attachments/image2025-2-18_14-46-54.png)

# 2. Investigation

## 2.1 Reproduce problem

After analysis according to the timeline, we suppose the high usage might be caused by batch file processing, so we generate batch file with 1000 payments for testing.

![image2025-2-18_14-19-6.png](attachments/image2025-2-18_14-19-6.png)

## 2.2. Define Test Steps and execution:

**EXPAND: Steps**

**Test case 1: **

1. Stop group service

2. Send 500 cashflow, CPU > 90% (Identify adaptor issue)

3. Stop orchestration, start group, CPU > 90%(Identify group issue)

4. Start orchestration, stop rule-service

5. Start up orchestration, CPU > 90%

**Conclusion**:

1. adaptor, group has issue,
2. not rule-service issue
3. workflow, message event, lifecycle may have issue.

Fix adaptor and group issue, run test case 2

**Test case 2:** 
1. Stop orchestration, message-event stopped, rule-service stopped

2. Start up lifecycle

3. Send 500 cashflow

4. Start up lifecycle, Start up orchestration, CPU > 90%

**Conclusion:**

1. not message-event issue
2. orchestration, lifecycle may have issue

**Test case 3: **  
1. Stop orchestration, message-event stopped, rule-service stopped, lifecycle stopped

2. Send 500 cashflow

3. Start up orchestration

4. CPU < 30%

**Conclusion**:

1. Not orchestration issue,
2. it is lifecycle issue

There are only 2 API being called during the inbound flow

1. precheck
2. cashflow status update

Then we decide to test on API level

**Test case 4: **  (lifecycle status update API test)

1. Stop orchestration

2. 5 batch update, 200 per one

3. Call status update

4. CPU < 30%

**Conclusion**: not status update issue, it is precheck API issue.

Then check all DB operation in code, and then check which table has sequence scan

**EXPAND_END**

## 2.3 Locate Problem:

2 main contributors found:

**-- static service CREATE INDEX if not exists ratan_static_cashflow_currency_holiday_iso_currency_code_idx ON ratanone.ratan_static_cashflow_currency_holiday USING btree (iso_currency_code, version, ratan_label);**

**-- lifecycle service CREATE INDEX if not exists ratan_stella_message_event_source_originating_trade_id_idx ON ratan_cashflow_lifecycle_service.ratan_stella_message_event_source USING btree (originating_trade_id);**

# 3. Fix The Problem

## 3.1 Ratan batch testing:

![image2025-2-18_14-35-33.png](attachments/image2025-2-18_14-35-33.png)

## 3.2 Ratan self PT pre/post index creation

Period 1 before indexing: 5000 payments with one batch, db cpu reaches 90

Period 2 after indexing:    4X PT, 30k payments in an hour, we can see db cpu is below 60%.

![image2025-2-18_16-23-42.png](attachments/image2025-2-18_16-23-42.png)

# 4. Appendix

## 4.1 During testing, run query to check which table still has sequence scan:

![image2025-2-18_14-29-4.png](attachments/image2025-2-18_14-29-4.png)

## 4.2 SQL to query out sequence scan rate:

```sql
select
	*
from
	(
	select
		round(cast(coalesce(idx_scan, 0) as numeric)/ cast ((seq_scan + coalesce(idx_scan, 0)) as numeric), 4) as index_scan_percentage,
		*
	from
		pg_stat_user_tables
	where
		n_live_tup > 100000
		and seq_scan > 10
	order by
		seq_scan desc ) a
order by
	a.index_scan_percentage asc;
```

## 4.3 Create index according to the result:

```sql
-- group service
CREATE INDEX if not exists idx_cashflow_group_mxg_trade_id ON ratan_cashflow_group_management_service.ratan_cashflow_group USING btree (mxg_trade_id);
CREATE INDEX if not exists idx_status_sync_blocking_queue_cfid_bizversion ON ratan_cashflow_group_management_service.ratan_cashflow_status_sync_up_blocking_queue USING btree (cashflow_id, business_version);
CREATE INDEX if not exists idx_status_sync_blocking_queue_exceptionId ON ratan_cashflow_group_management_service.ratan_cashflow_status_sync_up_blocking_queue USING btree (exception_id);

-- static service
CREATE INDEX if not exists ratan_static_cashflow_currency_holiday_iso_currency_code_idx ON ratanone.ratan_static_cashflow_currency_holiday USING btree (iso_currency_code, version, ratan_label);

-- adaptor service
CREATE INDEX if not exists mxg_cashflow_cancel_record_trn_original_id_status_idx ON rantan_mxg_cashflow_adaptor.mxg_cashflow_cancel_record USING btree (trn_original_id, flow_id, status);

-- lifecycle service
CREATE INDEX if not exists ratan_stella_message_event_source_trade_id_idx ON ratan_cashflow_lifecycle_service.ratan_stella_message_event_source USING btree (settlement_date);
CREATE INDEX if not exists ratan_stella_message_event_source_originating_trade_id_idx ON ratan_cashflow_lifecycle_service.ratan_stella_message_event_source USING btree (originating_trade_id);
CREATE INDEX if not exists ratan_stella_message_event_source_trade_id_major_idx ON ratan_cashflow_lifecycle_service.ratan_stella_message_event_source USING btree (trade_id, major_version);

-------------------- rollback --------------------
-- group service
DROP INDEX if exists idx_cashflow_group_mxg_trade_id;
DROP INDEX if exists idx_status_sync_blocking_queue_cfid_bizversion;
DROP INDEX if exists idx_status_sync_blocking_queue_exceptionId;

-- static service
DROP INDEX if exists ratan_static_cashflow_currency_holiday_iso_currency_code_idx;

-- adaptor service
DROP INDEX if exists mxg_cashflow_cancel_record_trn_original_id_status_idx;

-- lifecycle service
DROP INDEX if exists ratan_stella_message_event_source_trade_id_idx;
DROP INDEX if exists ratan_stella_message_event_source_originating_trade_id_idx;
DROP INDEX if exists ratan_stella_message_event_source_trade_id_major_idx;
```