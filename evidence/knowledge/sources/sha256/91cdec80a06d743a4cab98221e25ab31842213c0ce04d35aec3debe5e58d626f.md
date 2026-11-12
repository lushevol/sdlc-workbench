# SOLUTION1(recommend)

## 1. Use the CONCURRENTLY option

```
CREATE INDEX CONCURRENTLY if not exists ratan_cashflow_scbml_history_active_status_idx ON ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history (cashflow_status, sub_status_event_type,active);
```

## 2. Failure handling

```
-- check invalid indexes
SELECT * FROM pg_indexes WHERE schemaname = 'ratan_cashflow_lifecycle_service' AND indexname LIKE '%invalid%';

-- delete invalid indexes
DROP INDEX CONCURRENTLY IF EXISTS ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history_active_status_idx;
```

## 3. Monitor index creation progress

```
-- View the progress of all indexes that are being created
SELECT * FROM pg_stat_progress_create_index;

-- Detailed monitoring queries
SELECT 
  p.pid, p.datname, p.usename, p.client_addr,
  p.query_start, now() - p.query_start AS duration,
  i.schemaname, i.indexrelname, i.command,
  i.phase, i.blocks_total, i.blocks_done,
  round(100 * i.blocks_done / NULLIF(i.blocks_total, 0), 2) AS progress_pct
FROM pg_stat_progress_create_index i
JOIN pg_stat_activity p ON i.pid = p.pid;
```

## **CONCURRENTLY option Reference:**

## 1.feature

1). Doesn't get an exclusive lock on the table
        2). The creation process is divided into two stages:
           a) First table scan: Create an index structure
           b)Second Table Scan: Captures data that has changed since the first scan
        3). May fail but doesn't break the table

4).Virtually no impact on read/write operations in production
        5). No maintenance window is required
        6). It is especially suitable for systems that are 7*24 hours runinng

## 2. limit

1). Can't be used for unique indexes (CONCURRENTLY doesn't guarantee uniqueness)
        2). It cannot be used for some complex cases of expression indexing
        3). Can't work with CREATE TABLE ... INCLUDING INDEXES together
        4). If it fails during the creation process, the "invalid" index will be left and needs to be cleaned manually

# SOLUTION 2

## 1. create temp table

CREATE TABLE ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history_v2(LIKE ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history INCLUDING all)

## 2. create index on temp table

CREATE INDEX if not exists ratan_cashflow_scbml_history_active_status_idx ON ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history_v2 (cashflow_status, sub_status_event_type,active);

## 3. check all indexes on temp table

select * from pg_catalog.pg_indexes where schemaname = 'ratan_cashflow_lifecycle_service' and tablename = 'ratan_cashflow_scbml_history_v2';

## 4. import data into temp table

INSERT INTO ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history_v2 SELECT * FROM ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history;

## 5. switch old table with temp table

ALTER TABLE ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history RENAME TO ratan_cashflow_scbml_history_bak;
ALTER TABLE ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history_v2 RENAME TO ratan_cashflow_scbml_history;

## 6. verify data consistence

select count(*) from ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history;

select count(*) fromratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history_v2;

## 7. check all indexes on switched table

select * from pg_catalog.pg_indexes where schemaname = 'ratan_cashflow_lifecycle_service' and tablename = 'ratan_cashflow_scbml_history';