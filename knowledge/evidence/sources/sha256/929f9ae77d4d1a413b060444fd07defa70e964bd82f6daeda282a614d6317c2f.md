Currently we've the following flows:

- Trade SSI stamping, which is invoked by CDUPS, we receive SCBML and return enriched SCBML
- Cashflow SSI stamping, which is triggered by caumuda workflow
- SSI change notify, including vostro/nostro change nofity.
- If SSI stamp failed, exceptions will be generated (for cashflow only)

The interaction of services are shown as bellow diagram:

# SSI stamping and best match

Bellow is current SSI stamping flow, which basically query candidate vostros and do best matching, the stamping process is considered success if unique vostro/nostro found.

We've already unified the stamping logic of both trade and cashflow, however there're some limitations of current implementation:

- The response format differs between cashflow and trade, thus different logic must be maintained
- The program need to parse necessary information from SCBML, for different type of trade, the xpath is also different

As a result, the though the stamping logic is same, the code is partially reused and we're still maintaining two different APIs.

# Ad-hoc SSI stamping

# SSI update notification

**ANCHOR: ssi-notify-scbml**

If SSI stamp failed, cashflow will be NSTP with exceptions. During that time if SSI or nostro changed, it's possible that those failed cashflow will success to re-stamp.

Therefore, we've SSI update flow as bellow, which will try the best to re-stamp failed cashflows if nostro or vostro changed:

## Nostro notification

Example of nostro notification event:

```java
{
  "nostroPayload": {
    "id": "df6ea634-673c-465f-a258-3b6e67af04f7",
    "legalEntity": "SCB HONGKON*HKG",
    "legalEntityFmId": "2",
    "settlementCurrency": "HKD",
    "ebbsNostroAccount": "2387251800289042910098",
    "settlementMeans": "NOX",
    "settlementAccount": "HKD BCS",
    "sendersCorrespondent53Swift": "SCBLHKHHXXX",
    "sendersCorrespondent53Fullname": "test",
    "sendersCorrespondent53Address": "",
    "sendersCorrespondent53City": "",
    "sendersCorrespondent53Postcode": "",
    "sendersCorrespondent53Account": "44709412560",
    "noticeToReceive": "N",
    "currencyPair": "",
    "dataStatus": "SAVE_CONFIRMED",
    "makerId": "1593571",
    "checkerId": "1434424",
    "tlmSetId": "",
    "nostroStaticId": 10003674,
    "primaryFlag": false,
    "startDate": "2025-05-15",
    "endDate": "9999-12-30",
    "dataVersion": 2,
    "createdAt": "2025-05-15T09:21:47.687236",
    "updatedAt": "2025-05-15T09:27:42.280607"
  },
  "eventType": "INSERT"
}
```

Impacted cashflows computation algorithm NA1(for missing nostro):

- Find record from cashflow_stamping_legacy_exception with code in ('MISSING_VOSTRO_ERROR', 'MISSING_NOSTRO_ERROR', 'MULTI_VOSTRO_ERROR', 'VALIDATE_BENE_INFO') and status='ACTIVE'
- join cashflow_stamping with cashflow_id and filter by party1_fm_id, currency, start_date, end_date, which are extracted from event payload
- filter updated_at >=current_date -6
- exclude ad-hoc ssi stamping: if stamped_nostro_account record found with cashflow_id
- exclude pending approval ad-hoc ssi stamping record: if find record in maker_checker_request and it's not closed

```sql
select
	csle.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping_legacy_exception csle,
	cash_settlement_ssi_cn.cashflow_stamping cs
where
	csle.ssi_exception in ('MISSING_VOSTRO_ERROR', 'MISSING_NOSTRO_ERROR', 'MULTI_VOSTRO_ERROR', 'VALIDATE_BENE_INFO')
	and csle.status = 'ACTIVE'
	and cs.party1_fm_id = :party1FmId
	and cs.currency = :currency
	and cs.payment_date >= :startDate
	and cs.payment_date <= :endDate
	and cs.cashflow_id = csle.cashflow_id
	and cs.updated_at >= current_date-6
except
select
	csle1.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping_legacy_exception csle1,
	cash_settlement_ssi_cn.cashflow_stamping cs1,
	cash_settlement_ssi_cn.stamped_nostro_account sna
where
	csle1.ssi_exception in ('MISSING_VOSTRO_ERROR', 'MISSING_NOSTRO_ERROR', 'MULTI_VOSTRO_ERROR', 'VALIDATE_BENE_INFO')
	and csle1.status = 'ACTIVE'
	and cs1.party1_fm_id = :party1FmId
	and cs1.currency = :currency
	and cs1.payment_date >= :startDate
	and cs1.payment_date <= :endDate
	and cs1.cashflow_id = csle1.cashflow_id
	and cs1.updated_at >= current_date-6
	and cs1.cashflow_id = sna.cashflow_stamping_id
except
select
	csle2.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping_legacy_exception csle2,
	cash_settlement_ssi_cn.cashflow_stamping cs2,
	cash_settlement_ssi_cn.maker_checker_request mcr
where
	csle2.ssi_exception in ('MISSING_VOSTRO_ERROR', 'MISSING_NOSTRO_ERROR', 'MULTI_VOSTRO_ERROR', 'VALIDATE_BENE_INFO')
	and csle2.status = 'ACTIVE'
	and mcr.cashflow_id = cs2.cashflow_id
	and mcr.state != 'AUTO_CLOSED'
	and cs2.party1_fm_id = :party1FmId
	and cs2.currency = :currency
	and cs2.payment_date >= :startDate
	and cs2.payment_date <= :endDate
	and cs2.cashflow_id = csle2.cashflow_id
	and cs2.updated_at >= current_date-6
```

NA2(for good stamped):

- Find cashflow_stamping by party1_fm_id, currency, filter updated_at >=current_date -6
- exclude ad-hoc ssi stamping

```sql
select
	cs.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping cs,
	cash_settlement_ssi_cn.stamped_nostro_account sna
where
	cs.party1_fm_id = :party1FmId
	and cs.currency = :currency
	and cs.cashflow_id = sna.cashflow_stamping_id
	and cs.updated_at >= current_date-6
except
select
	cs.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping_legacy_exception csle,
	cash_settlement_ssi_cn.cashflow_stamping cs,
	cash_settlement_ssi_cn.maker_checker_request mcr
where
	csle.ssi_exception in ('MISSING_VOSTRO_ERROR', 'MISSING_NOSTRO_ERROR', 'MULTI_VOSTRO_ERROR', 'VALIDATE_BENE_INFO', 'SETTLEMENT_ACCOUNT_OR_MEANS_MISMATCH_EXCEPTION', 'ADHOC_SSI_EXCEPTION')
	and mcr.cashflow_id = cs.cashflow_id
	and mcr.state != 'AUTO_CLOSED'
	and cs.party1_fm_id = :party1FmId
	and cs.currency = :currency
	and cs.payment_date >= :startDate
	and cs.payment_date <= :endDate
	and cs.cashflow_id = csle.cashflow_id
	and cs.updated_at >= current_date-6
```

NA3(for good stamped):

- Find cashflow_stamping by nostroStaticId, and payment_date in the start_date, end_date, filter updated_at >=current_date -6
- Exclude pending ad-hoc ssi stamping

```sql
select
	cs.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping cs,
	cash_settlement_ssi_cn.stamped_nostro_account sna
where
	sna.account_catalogs->>'nostroStaticId' = :nostroStaticId
	and cs.cashflow_id = sna.cashflow_stamping_id
	and cs.updated_at >= current_date-6
	and cs.payment_date >= :startDate
	and cs.payment_date <= :endDate
except
select
	cs.cashflow_id
from
	cash_settlement_ssi_cn.cashflow_stamping_legacy_exception csle,
	cash_settlement_ssi_cn.cashflow_stamping cs,
	cash_settlement_ssi_cn.stamped_nostro_account sna,
	cash_settlement_ssi_cn.maker_checker_request mcr
where
	csle.ssi_exception in ('MISSING_VOSTRO_ERROR', 'MISSING_NOSTRO_ERROR', 'MULTI_VOSTRO_ERROR', 'VALIDATE_BENE_INFO', 'SETTLEMENT_ACCOUNT_OR_MEANS_MISMATCH_EXCEPTION', 'ADHOC_SSI_EXCEPTION')
	and mcr.cashflow_id = cs.cashflow_id
	and mcr.state != 'AUTO_CLOSED'
	and sna.cashflow_stamping_id = cs.cashflow_ids
	and sna.account_catalogs->>'nostroStaticId' = :nostroStaticId
	and cs.payment_date >= :startDate
	and cs.payment_date <= :endDate
	and cs.cashflow_id = csle.cashflow_id
	and cs.updated_at >= current_date-6
```

| Type | INSERT | UPDATE | DELETE |
| --- | --- | --- | --- |
| missing nostro | NA1 | NA1 | No impact |
| good stamped | NA2 | NA3 | NA3 |

## Vostro notification

Impacted cashflows algorithm **getImpactCashflowIdsByCondition**:

- If it's global, then query cashflow_exception with status='ACTIVE', party2_fm_id, currency with value from event payload, and cfiCode with like condition( using PG underscore like)
- if it's not global, add party1_fm_id condition
- filter records with updated_at >=current_date -6

```sql
select
	csle.*
from
	cashflow_stamping_legacy_exception csle,
	cashflow_stamping cs
where csle.ssi_exception = :ssiException     -- :ssiException
	and csle.status = :status				 -- ACTIVE
	and csle.cashflow_id = cs.cashflow_id
	and cs.currency = :currency              -- :currency
	and cs.cfi_code like :cfiCode            -- :cfiCode
	and cs.party2_fm_id = :party2FmId        -- :party2FmId
	and cs.updated_at >= current_date - 6
	and cs.party1_fm_code = :party1FmCodes   -- applies iff it's not Global
```

**getImpactCashflowIdsBySsiId**:

```sql
select
	csle.*
from
	cashflow_stamping_legacy_exception csle,
	cashflow_stamping cs,
	stamped_vostro_account sva
where csle.ssi_exception = :ssiException
	and csle.status = :status
	and csle.cashflow_id = cs.cashflow_id
	and sva.cashflow_stamping_id = cs.cashflow_id
	and sva.ssi_id = :ssiId
	and cs.updated_at >= current_date - 6
```

For vostro change:

| Type | INSERT | UPDATE | DELETE |
| --- | --- | --- | --- |
| missing nostro | getImpactCashflowIdsByCondition |
| missing vostro |
| multiple vostro | getImpactCashflowIdsByCondition | getImpactCashflowIdsBySsiId | getImpactCashflowIdsBySsiId |
| mismatch | N/A |
| no exception | getImpactCashflowIdsBySsiId |

# Camunda and SSI Stamping

Cashflow SSI stamping is triggered by camunda workflow, as shown bellow:

![image-2025-4-22_16-41-39.png](attachments/image-2025-4-22_16-41-39.png)