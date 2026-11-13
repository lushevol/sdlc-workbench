# Background

Uber development has already been completed, we need to prove.

1. Uber adoption has no performance impact on existing SCBML flow. - Must to have
2. Uber message performance is better than SCBML message. – Nice to have.

Performance testing scope

| SN. | Description |
| --- | --- |
| 1 | Settlement STP flow |
| 2 | Netting/UnNetting |
| | |

Round 1 - without message bridge

Data volume:

Murex - 7000

Stella - 7000

Uber - 100(cashflow 200)

Settlement STP Time Cost

Avg                            Max                            Min                         Total

00:00:03.401777  00:00:14.553234  00:00:01.474934  13737

```sql
select
	*
from
	(
	select
		count(1)
	from
		ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history rcsh
	where
		cashflow_id like 'M01XMX%'
		and create_time >= '2025-11-21 04:50:00'
		and active = 'ACTIVE') as murex_cashflow,
	(
	select
		count(1)
	from
		ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history ready
	where
		cashflow_id like '1XSA%'
		and create_time >= '2025-11-21 04:50:00'
		and active = 'ACTIVE') as stella_cashflow,
	tr
(
	select
		count(1)
	from
		ratan_cashflow_group_management_service.ratan_cashflow_group_message rcgm,
		ratan_cashflow_lifecycle_service.ratan_cashflow_scbml_history hi
	where
		rcgm.trade_id like '1UN%'
		and rcgm.created_at > '2025-11-21 04:50:00'
		and rcgm.cashflow_id = hi.cashflow_id
		and hi.active = 'ACTIVE') as uber_message;
```

```sql
count|count|count|
-----+-----+-----+
 6773| 6967|  200|
```