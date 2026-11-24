****

# **0 Illustration**

Utilize Action, Utilize Status and Utilize Account Task Type in Utilize scope.

| **Name** | **Enum Value** | **Description** | ** ** |
| --- | --- | --- | --- |
| Util_Type | Manual: EARLY-FULL-UTIL EARLY-PART-UTIL VDATE-FULL-UTIL VDATE-PART-UTIL PADU-FULL-UTIL PADU-PART-UTIL EARLY-FULL-REV EARLY-PART-REV VDATE-FULL-REV VDATE-PART-REV PADU-FULL-REV PADU-PART-REV Auto: VDATE-AUTO-UTIL PADU-AUTO-UTIL VDATE-PASTDUE-UTIL PADU-PASTDUE-UTIL PADU-PASTDUE-REV | Utilize request example: { "Utilization": { "Utilization_Id": "2870476", "Orig_Utilization_Id": null, **"Util_Type": "PADU-FULL-UTIL",** "AACode_Comments": "FX", "Util_Payment_Ref": "test", "Maker_ID": "1556878", "Checker_ID": "1465419", "Trade": { "Trade_Id": "7150113118", "Trade_Lake_Trade_Major_Version": "1", "Swap_Leg_ID": "", "Exchanged_Currency1_Payment_Amount_Currency": "USD", "Exchanged_Currency1_Util_Amount": "75000" } } } | Util_Type Utilize Action mapping: EARLY_PART_UTIL("EARLY-PART-UTIL", PartialUtilize), EARLY_PART_REV("EARLY-PART-REV", PartialReverse), EARLY_FULL_UTIL("EARLY-FULL-UTIL", FullUtilize), EARLY_FULL_REV("EARLY-FULL-REV", FullReverse), VDATE_PART_UTIL("VDATE-PART-UTIL", PartialUtilize), VDATE_PART_REV("VDATE-PART-REV", PartialReverse), VDATE_FULL_UTIL("VDATE-FULL-UTIL", FullUtilize), VDATE_FULL_REV("VDATE-FULL-REV", FullReverse), PADU_PART_UTIL("PADU-PART-UTIL", PartialUtilize), PADU_PART_REV("PADU-PART-REV", PartialReverse), PADU_FULL_UTIL("PADU-FULL-UTIL", FullUtilize), PADU_FULL_REV("PADU-FULL-REV", FullReverse), // Ratan Defined Status VDATE_AUTO_UTIL("VDATE-AUTO-UTIL", AutoUtilize), PADU_AUTO_UTIL("PADU-AUTO-UTIL", AutoUtilize), VDATE_PASTDUE_UTIL("VDATE-PASTDUE-UTIL", Pastdue), PADU_PASTDUE_UTIL("PADU-PASTDUE-UTIL", Pastdue), PADU_PASTDUE_REV("PADU-PASTDUE-REV", PastdueReverse); |
| Utilize Action | FullUtilize PartialUtilize AutoUtilize FullReverse PartialReverse Pastdue PastdueReverse | | |
| Utilize Status | READY FULLY_UTILIZED PARTIALLY_UTILIZED PASTDUE | | |
| Utilize Account Task Type | UTILIZE PASTDUE | | UTILIZE used for action: FullUtilize PartialUtilize AutoUtilize FullReverse PartialReverse PASTDUE used for action: Pastdue PastdueReverse |

# **1 FXU Scope Cashflow Onboard**

Ratan identify FXU cashflows by Settlement_Method field in cashflow data from upstream system. But now the field can not be stamped correctly in upstream systems. So Ratan need to stamp the field itself with UTIL by static config data in BookingEntityFMID and CounterpartyFMID pair to work around.

FXU Scope Cashflows will skip suppression rule check and directly move to READY status when there are no Nostro Exceptions.

FXU Scope Cashflows will skip SSI Vostro stamping and swift generation because the payment happen in SCPAY directly.

## **1.1 FXU Settlement Method Stamping**

****

## **1.2 Workflow Gateway For UTIL Flow**

**     **New workflow for cashflow with Settlement_Method='UTIL'.

![image-2026-4-14_16-26-31.png](attachments/image-2026-4-14_16-26-31.png)

## **1.3 Status Machine For FXU**

### **1.3.1 Utilization Cashflow Status Machine**

### **1.3.2 Status Derive**

| **Source Cashflow Status** | **Source Cashflow Sub Status** | **Source Cashflow Sub Status Type** | **Action** | **Target Cashflow Status** | **Target Cashflow Sub Status** | **Target Cashflow Sub Status Type** | ** ** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| READY | NA | NA | **FullUtilize** | UTILIZED | NA | NA | |
| READY | NA | NA | **PartialUtilize** | PARTIALLY_UTILIZED | NA | NA | |
| READY | NA | NA | **AutoUtilize** | UTILIZED | NA | NA | |
| READY | NA | NA | **Pastdue** | PASTDUE | Pastdue | NA | |
| PARTIALLY_UTILIZED | NA | NA | **FullUtilize** | UTILIZED | NA | NA | |
| ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ | ~~**PartialUtilize**~~ | ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ | |
| PARTIALLY_UTILIZED | NA | NA | **FullReverse** | READY | NA | NA | |
| ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ | ~~**PartialReverse**~~ | ~~PARTIALLY_UTILIZED~~ | ~~NA~~ | ~~NA~~ | |
| PARTIALLY_UTILIZED | NA | NA | Pastdue | PARTIALLY_UTILIZED | Pastdue | NA | |
| PARTIALLY_UTILIZED | NA | NA | **Withdrawal** | ERROR | NA | NA | |
| PARTIALLY_UTILIZED | Pastdue | NA | **FullUtilize** | UTILIZED | NA | NA | |
| PARTIALLY_UTILIZED | Pastdue | NA | **FullReverse** | READY | NA | NA | |
| PARTIALLY_UTILIZED | Pastdue | NA | **PartialUtilize** | PARTIALLY_UTILIZED | NA | NA | add on 4.1 |
| PARTIALLY_UTILIZED | Pastdue | NA | **PartialReverse** | PARTIALLY_UTILIZED | NA | NA | add on 4.1 |
| PARTIALLY_UTILIZED | Pastdue | NA | **Withdrawal** | ERROR | Pastdue | NA | |
| UTILIZED | NA | NA | **FullReverse** | READY | NA | NA | |
| UTILIZED | NA | NA | **PartialReverse** | PARTIALLY_UTILIZED | NA | NA | |
| UTILIZED | NA | NA | **Withdrawal** | ERROR | NA | NA | |
| PASTDUE | Pastdue | NA | **FullUtilize** | UTILIZED | NA | NA | |
| PASTDUE | Pastdue | NA | **PartialUtilize** | PARTIALLY_UTILIZED | NA | NA | |
| PASTDUE | Pastdue | NA | **Withdrawal** | CANCELLED | NA | NA | |

## **1.4 SSI Stamping**

When cashflow Settlement_Method is 'UTIL',  ssi stamping will skip all vostro validation and stamping process.

### 1.4.1 Workflow ssi stamping

When Settlement Method is UTIL ssi service will request fxu static config to get the settlement means and settlement account.

### 1.4.2 Adhoc ssi stamping

1. GUI will skip vostro validation for maker and checker when the cashflow Settlement_method='UTIL'
2. When Checker approve an adhoc ssi action, ssi service will skip all vostro validation and setup new Nostro when Settlement_method='UTIL'.

## **1.5 Block Swift Generation(Not Implement)**

Hard block for Swift Generation when Cashflow Settlemnt_Method='UTIL'.

Not implement because:

1. UTIL is a different way from GROSS in Workflow.
2. Swift Service only support Settlement Means with Nos or Over-Account, but in FXU scope the settlement means always be FXBRREC or FXBRREC-M

```
public class SwiftMessageHandler {
	public List<BaseSwiftGenerator> handlePayment(CashFlowDataBean cashFlowDataBean) {    
   		if("UTIL".equals(cashFlowDataBean.getVostroSettlementMethod()) {
            log.warn("Cashflow {} is a utility settlement, no MT generation will be performed.",
                cashFlowDataBean.getCashflowId());
            return Collections.EMPTY_LIST;    
        }
		...
	}
}
```

# **2 Utilization Service Design**

## **2.1 FXU Cashflow Onboard Utilization Service**

- **Initial**

- **Updating**

## **2.2 Processing Design**

**Key Points**

- **Core Logic Control** - All utilization types(Full/Partial/Pastdue/Reverse) have the same core logic with different action and validator chain. - Actions - FullUtilize - PartialUtilize - FullReverse - PartailReverse - Pastdue - PastdueReverse - Validator Chain - Utilize validator chain - Pastdue validator chain - Reverse validator chain - Core logic - Calculate remaining amount - Status move - Save utilize history - Generate accounting event
- **Trade level transaction control** - Ratan→Stella - Block status sync up - Ratan Domain Services - Controlled by cashflow level distribute lock and db transaction.

### **2.2.1 Overall Utilization Logic flow**

### **2.2.2 Hard Block For Trade Amendment**

There is a long process chain with three  separate systems(FXU, Stella, Ratan) on utilize action. We need to handle in transaction on each utilize request between Stella and Ratan and also need to handle in transaction between domain services(Utilization, Lifecycle, Accounting) in Ratan.

We need to create a separate distribute transaction operation space for each utilize request to guarantee consistency.

#### ~~**2.2.2.1 Design Concept**~~

#### ~~**2.2.2.2 Distribute Lock flow**~~

Hard Block when request arrives.

#### **2.2.2.3 Status Sync Up From Domain Event**

This proposal is to reuse the existing status sync up flow.

We use this way because:

1. It's heavy to hard dependency upstream system, and they are not stable enough as we want.
2. Concurrent operation is low probability.
3. Ratan have distribute lock to handle the concurrent operation and prevent next step when any ERROR occur

So finally we decide to take this option to sync up Utilize, PartiallyUtilize, Unutilize action to Stella.

Stella Design Ref: [Cashflow UTILIZATION & PARTIALLY-UTILIZED status for RATAN - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3565997533)

### 2.2.3 Core Utilization Logic

There are 12 manual and 5 auto util type for utilization action:

> **INFO**
> Manual:
> - EARLY-FULL-UTIL
> - EARLY-PART-UTIL
> - VDATE-FULL-UTIL
> - VDATE-PART-UTIL
> - PADU-FULL-UTIL
> - PADU-PART-UTIL
> - EARLY-FULL-REV
> - EARLY-PART-REV
> - VDATE-FULL-REV
> - VDATE-PART-REV
> - PADU-FULL-REV
> - PADU-PART-REV
> Auto:
> - VDATE-AUTO-UTIL
> - PADU-AUTO-UTIL
> - VDATE-PASTDUE-UTIL
> - PADU-PASTDUE-UTIL
>
> - PADU-PASTDUE-REV

The difference between manual and auto utilization action is the trigger source. The manual action is trigger by user from Razor FXU system and the auto utilization is trigger by Ratan auto job. So the underlying logic is almost the same between manual and auto utilization.

The core logic contains below common steps:

1. Validator for request data quality and business legitimacy.
2. Calculator and update remaining amount.
3. Cashflow status move.
4. Generate utilization history.
5. Generate and publish accounting data.

The **PastdueReverse **action is special, it happens when:

1. any manual utilization action happened and there are pastdue accounting data existing meanwhile, PastdueReverse happened as an additional action.
2. trade cancelled and there are pastdue accounting data existing meanwhile, PastdueReverse happened as an independent action.
3. manually change settlement method from UTIL to GROSS and there are pastdue accounting data existing meanwhile, PastdueReverse happened as an independent action.

#### **2.2.3.1 Utilization Logic Flow**

#### **2.2.3.2 Utilization Logic Dependency**

#### **2.2.3.3 Pastdue Logic For Get Pastdue Account**

| Entity | Pastdue Account(Ebbs Nostro Account) | Accounting System |
| --- | --- | --- |
| NEPAL | 09285266713 | EBBS |
| SAUDI | 09700236201 | EBBS |
| EGYPT | 09500031601 | EBBS |

Pastdue account together with Nostro

CCY:  ALL

Settlement Means: FXBRREC

Settlement Account: PASTDUE

Account: {pastdue account}

![image-2025-12-17_10-56-29.png](attachments/image-2025-12-17_10-56-29.png)

#### **2.2.3.4 Pastdue Reverse When Cashflow CANCELLED**

When Trade CANCELLED happened after Pastdue, but before any other utilization actions, the pastdue accounting should be reversed.

#### **2.2.3.5 Pastdue Reverse When Utilize And Reverse Actions**

Pastdue will happen at EOD on value date, also, Utilize & Reverse actions are both allowed after value date. When Utilize or Reverse action happen after EOD, the pastdue accounting should be reversed at the same time.

#### **2.2.3.6 Pastdue Reverse When Settlement Method Change**

**Ref to chapter 2.2.4**

**EXPAND: FXU_accounting_event**

**EXPAND_END**

#### ~~**2.2.3.7 Auto Utilize Response**~~

UtilizationResp:

```
{
  "Utilization_Id": "fxu.7419987178642673665",
  "Trade": {
    "Trade_Id": "7111011225",
    "Trade_Lake_Trade_Major_Version": 1,
    "Swap_Leg_ID": "",
    "Exchanged_Currency1_Payment_Amount_Currency": "EGO",
    "Exchanged_Currency1_Util_Amount": "476.19",
    "Exchanged_Currency1_Remaining_Amount": 0,
    "Exchanged_Currency2_Payment_Amount_Currency": "USD",
    "Exchanged_Currency2_Util_Amount": "100.0",
    "Exchanged_Currency2_Remaining_Amount": 0
   }
}
```

- Proposal1: Utilization Service + Query Service + FXU （Prefer）

- Proposal2: Utilization Service + Lifecycle Service

- Proposal3: Utilization Service

#### **2.2.3.8 Failed Retry**

Two failed scenarios should have a retry

1. When manual utilize ack and auto utilize response failed to FXU because Kafka unavailable.
2. When account event message send failed because Kafka unavailable

Ratan should retry the failed response base on PostgreSQL.

#### **2.2.3.9 Business Scenarios**

**
📎 [FXU Data cases.xlsx](attachments/FXU Data cases.xlsx)
**

#### **2.2.3.10 External System Key Generator**

The external system key is a unique field for accounting data. It's generated by Utilization Service and passed to Accounting Service because the utilize reversal action is identify by this field in accounting service.

There is also a limitation of external_system_key length which is less than 50.

external_system_key generate rule list below:

| Type | Rule | Example |
| --- | --- | --- |
| Manual Utilization | fxu.{utilizationId}.{cashflowId} | fxu.67160289441.006716028950 |
| Auto Utilization | fxu.{snowflakeId}.{cashflowId} | fxu.7411613250391826432.006716028951 |
| Pastdue | fxu.{snowflakeId}.{cashflowId} | fxu.7411614508675489792.006716028950 |

#### **2.2.3.11 Accounting Event Message Definition**

**EXPAND: FXU_accounting_event**

UTILIZE:

```java
{
	"requestList": [
					{
						"externalKey": "123456-cf01",
						"isReverse": false,
						"originalExternalKey": null,
                        "cashflowInfo": {
								"cashflowId": "cf01",
								"cashflowBusinessVersion": "0",
								"cashflowVersion": "0",
								"cashflowMinorVersion": "6",
								"cashflowStatus": "UTILIZED",
								"cashflowSubStatusType": "",
								"action": "PartialReverse",
								"cashflowEvent": "NEW",
								"cashflowRowData": "UBER message",
								"currency": "USD",
								"bookingFmid": "400007847",
								"amount": "100",
								"tradeOriginalSourceSystemName": "Stella",
								"fxuRequestInfo": {
											"paymentReference": "12345678",
											"areaCode": "ac123",
											"makerId": "maker",
											"checkerId": "checker",
											"utilizationStatus": "Early Partial Utilized",
											"requestAmount": "30"
													}
								
										}
                    },
					{
					    "externalKey": "123456-cf01",
						"isReverse": true,
						"originalExternalKey": "654321-cf01",
						"cashflowInfo": {
								"cashflowId": "cf01",
								"cashflowBusinessVersion": "0",
								"cashflowVersion": "0",
								"cashflowMinorVersion": "4",
								"cashflowStatus": "UTILIZED",
								"cashflowSubStatusType": "",
								"action": "PartialReverse",
								"cashflowEvent": "NEW",
								"cashflowRowData": null,
								"currency": "USD",
								"bookingFmid": "400007847",
								"amount": "100",
								"tradeOriginalSourceSystemName": "Stella",
								"fxuRequestInfo": {
											"paymentReference": "12345678",
											"areaCode": "ac123",
											"makerId": "maker",
											"checkerId": "checker",
											"utilizationStatus": "Early Partial Utilized",
											"requestAmount": "30"
													}
								
										}
					}
					]
}


```
PASTDUE:
```
{
  "requestList": [
    {
      "externalKey": "fxu.7420510631204438020.020011576157",
      "isReverse": false,
      "originalExternalKey": "",
      "cashflowInfo": {
        "cashflowId": "020011576157",
        "cashflowBusinessVersion": "0",
        "cashflowVersion": "0",
        "cashflowMinorVersion": "5",
        "cashflowStatus": "PASTDUE",
        "cashflowSubStatusType": "NA",
        "action": "Pastdue",
        "cashflowEvent": "New",
        "cashflowRowData": "xxxxxxx",
        "comment": "",
        "currency": "EUR",
        "bookingFmid": "401036553",
        "amount": "8.01",
        "tradeOriginalSourceSystemName": "S2BX",
        "fxuRequestInfo": {
          "paymentReference": "",
          "areaCode": "",
          "makerId": "System",
          "checkerId": "System",
          "utilizationStatus": "VDATE-PASTDUE-UTIL",
          "requestAmount": "8.01",
          "pastDueAccountNumber": "09500031601"
        }
      }
    },
    {
      "externalKey": "fxu.7420510631204438020.657378537980",
      "isReverse": false,
      "originalExternalKey": "",
      "cashflowInfo": {
        "cashflowId": "657378537980",
        "cashflowBusinessVersion": "0",
        "cashflowVersion": "0",
        "cashflowMinorVersion": "5",
        "cashflowStatus": "PASTDUE",
        "cashflowSubStatusType": "NA",
        "action": "Pastdue",
        "cashflowEvent": "New",
        "cashflowRowData": "xxxxxx",
        "comment": "",
        "currency": "USD",
        "bookingFmid": "401036553",
        "amount": "1.01",
        "tradeOriginalSourceSystemName": "S2BX",
        "fxuRequestInfo": {
          "paymentReference": "",
          "areaCode": "",
          "makerId": "System",
          "checkerId": "System",
          "utilizationStatus": "VDATE-PASTDUE-UTIL",
          "requestAmount": "1.01",
          "pastDueAccountNumber": "09500031601"
        }
      }
    }
  ]
}
```

UTILIZE & PASTDUE REVERSE:

```
{
  "requestList": [
    {
      "externalKey": "fxu.7420032846321106944.000036012744",
      "isReverse": true,
      "originalExternalKey": "fxu.7420032476840673280.000036012744",
      "cashflowInfo": {
        "cashflowId": "000036012744",
        "cashflowBusinessVersion": "0",
        "cashflowVersion": "0",
        "cashflowMinorVersion": "7",
        "cashflowStatus": "UTILIZED",
        "cashflowSubStatusType": "NA",
        "action": "PastdueReverse",
        "cashflowEvent": "New",
        "cashflowRowData": "xxx",
        "comment": "",
        "currency": "USD",
        "bookingFmid": "400991880",
        "amount": "100.0",
        "tradeOriginalSourceSystemName": "Blade",
        "fxuRequestInfo": {
          "paymentReference": "",
          "areaCode": "",
          "makerId": "1642375",
          "checkerId": "1376381",
          "utilizationStatus": "VDATE-PART-UTIL",
          "requestAmount": "100.0",
          "pastDueAccountNumber": null
        }
      }
    },
    {
      "externalKey": "fxu.7420032846363049984.000036012743",
      "isReverse": true,
      "originalExternalKey": "fxu.7420032476840673280.000036012743",
      "cashflowInfo": {
        "cashflowId": "000036012743",
        "cashflowBusinessVersion": "0",
        "cashflowVersion": "0",
        "cashflowMinorVersion": "7",
        "cashflowStatus": "UTILIZED",
        "cashflowSubStatusType": "NA",
        "action": "PastdueReverse",
        "cashflowEvent": "New",
        "cashflowRowData": "xxx",
        "comment": "",
        "currency": "SAR",
        "bookingFmid": "400991880",
        "amount": "375.16",
        "tradeOriginalSourceSystemName": "Blade",
        "fxuRequestInfo": {
          "paymentReference": "",
          "areaCode": "",
          "makerId": "1642375",
          "checkerId": "1376381",
          "utilizationStatus": "VDATE-PART-UTIL",
          "requestAmount": "375.16",
          "pastDueAccountNumber": null
        }
      }
    },
    {
      "externalKey": "fxu.71110113011.000036012744",
      "isReverse": false,
      "originalExternalKey": "",
      "cashflowInfo": {
        "cashflowId": "000036012744",
        "cashflowBusinessVersion": "0",
        "cashflowVersion": "0",
        "cashflowMinorVersion": "7",
        "cashflowStatus": "UTILIZED",
        "cashflowSubStatusType": "NA",
        "action": "FullUtilize",
        "cashflowEvent": "New",
        "cashflowRowData": "xxx",
        "comment": "",
        "currency": "USD",
        "bookingFmid": "400991880",
        "amount": "100.0",
        "tradeOriginalSourceSystemName": "Blade",
        "fxuRequestInfo": {
          "paymentReference": "1",
          "areaCode": "FX",
          "makerId": "1642375",
          "checkerId": "1376381",
          "utilizationStatus": "VDATE-PART-UTIL",
          "requestAmount": "100.0",
          "pastDueAccountNumber": null
        }
      }
    },
    {
      "externalKey": "fxu.71110113011.000036012743",
      "isReverse": false,
      "originalExternalKey": "",
      "cashflowInfo": {
        "cashflowId": "000036012743",
        "cashflowBusinessVersion": "0",
        "cashflowVersion": "0",
        "cashflowMinorVersion": "7",
        "cashflowStatus": "UTILIZED",
        "cashflowSubStatusType": "NA",
        "action": "FullUtilize",
        "cashflowEvent": "New",
        "cashflowRowData": "xxxx",
        "comment": "",
        "currency": "SAR",
        "bookingFmid": "400991880",
        "amount": "375.16",
        "tradeOriginalSourceSystemName": "Blade",
        "fxuRequestInfo": {
          "paymentReference": "1",
          "areaCode": "FX",
          "makerId": "1642375",
          "checkerId": "1376381",
          "utilizationStatus": "VDATE-PART-UTIL",
          "requestAmount": "375.16",
          "pastDueAccountNumber": null
        }
      }
    }
  ]
}
```

**EXPAND_END**

### 2.2.4 Manual Settlement Method Update

[Story 11834223 [FXU] Move from Utilization to Gross settlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11834223)

This design is related to settlement method field value change in bidirectional with value GROSS and UTIL in cashflows.

While settlement method=UITL means these cashflows belongs to FXU scope and GROSS means they are in GROSS scope.

This is utilization scope requirement, so the entry point build in utilization service.

The key points contains:

- This function takes effective **immediately **in **trade level** after manual action.
- Utilization pastdue accounting reversal when UTIL to GROSS when they are existing.
- Batch process in trade level.
- Inherit - **Settlement method** **inherit: ****"Withdrawal"** event's settlement method **inherit **the latest '**New**' event's value to support the settlement method keep consistent when amendment or cancel action happens. - **Status inherit: "New" **event's **status inherit ERROR **when there exist cashflows belong to the same trade with** **current status is ERROR and history status contains UTILIZED/PARTIALLY_UTILIZED to stop the flow.

**High Level Flow**

**Detail Flow**

- GROSS → UTIL then Withdraw with GROSS event

if not utilization → CANCELLED()

if utilized → ERROR()

- GROSS → UTIL then Amendment with GROSS event

if not utilization → old cashflow to CANCELLED + new cashflow settlement method stamp to GROSS(Manual change settlement method again if necessary)()

if utilized → old cashflow to ERROR with settlement method UTIL + new cashflow to READY with settlement method GROSS (Do not support settlement method change because cashflow settlement method not consistent and ERROR status)()

Comment: new cashflows may STP and released, that's not expected!!!

Proposal Solution1: new cashflow also to ERROR state when there have utilized + ERROR cashflows exists in the same trade.

- UTIL → GROSS then Withdraw with GROSS event

if not released → CANCELLED()

if released → WAITTING(Reversal)()

- UTIL → GROSS then Amendment with UTIL event

if not released → old cashflow to CANCELLED + new cashflow settlement method stamp to UTIL(Manual change settlement method again if necessary)()

if released → old cashflow to WAITTING(Reversal) with settlement method GROSS + new cashflow to READY with settlement method UTIL(Do not support settlement method change because cashflow settlement method not consistent)()

Open points:

- How to handle distribute transaction between CashflowStamped and RevertToQueued status move? (do not consider this edge scenario now.)

## **2.3 Module Design**

### **2.3.1 Module Structure**

### **2.3.2 Validator Chain**

- UtilizeValidatorChain

- ReverseUtilizationChain
- PastdueUtilizationChain
- PastduReverseUtilizationChain

### **2.3.3 Remaining Amount Calculator**

- UtilizeRemainingAmountCalculator
- ReverseRemainingAmountCalculator
- PastdueRemainingAmountCalculator
- PastdueReverseRemainingAmountCalculator

## **2.4 DB Table**

- ratan_fx_cashflow_utilization_history

Create new table.

```
-- ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history definition

-- Drop table

-- DROP TABLE ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history;

CREATE TABLE ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history (
	id bigserial NOT NULL,
	trade_id text NOT NULL,
	trade_major_version int4 NOT NULL,
	cashflow_id text NOT NULL,
	cashflow_state text NOT NULL,
	business_version text NULL,
	cashflow_version text NULL,
	minor_version text NULL,
	payment_date date NULL,
	utilize_date date NULL,
	utilize_action text NULL,
	currency varchar(10) NULL,
	payment_amount numeric NULL,
	utilize_amount numeric NULL,
	remaining_amount numeric NULL,
	utilize_id text NOT NULL,
	origin_utilize_id text NULL,
	accounting_task_id text NULL,
	create_at timestamp NULL,
	update_at timestamp NULL,
	accounting_send_status int2 NULL DEFAULT 0,
	external_key text NULL,
	CONSTRAINT ratan_fx_cashflow_utilization_history_pk PRIMARY KEY (id)
);
CREATE INDEX ratan_cashflow_utilization_history_accounting_task_id_idx ON ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history (accounting_task_id);
CREATE INDEX ratan_cashflow_utilization_history_cashflow_id_idx ON ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history (cashflow_id);
CREATE INDEX ratan_cashflow_utilization_history_trade_id_idx ON ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history (trade_id);
CREATE INDEX ratan_cashflow_utilization_history_utilize_id_idx ON ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_utilization_history (utilize_id);
```

- ratan_fx_cashflow_brief_info (Utilization Service)

Create new table.

```
-- ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_brief_info definition

-- Drop table

-- DROP TABLE ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_brief_info;

CREATE TABLE ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_brief_info (
	id bigserial NOT NULL,
	trade_id text NOT NULL,
	trade_major_version int4 NOT NULL,
	cashflow_id text NOT NULL,
	cashflow_state text NOT NULL,
	business_version text NULL,
	cashflow_version text NULL,
	minor_version text NULL,
	value_date date NOT NULL,
	settlement_method text NULL,
	settlement_means text NULL,
	settlement_account text NULL,
	country_code varchar(10) NULL,
	currency varchar(10) NULL,
	payment_type varchar(20) NULL,
	payment_amount numeric NULL,
	remaining_amount numeric NULL,
	pastdue_job_done int4 NULL,
	create_at timestamp NULL,
	update_at timestamp NULL,
	booking_entity_fmid text NULL,
	counterparty_fmid text NULL,
	pastdue_external_key text NULL,
	CONSTRAINT ratan_fx_cashflow_brief_info_pk PRIMARY KEY (id),
	CONSTRAINT ratan_fx_cashflow_brief_info_un UNIQUE (trade_id,trade_major_version,cashflow_id),
	CONSTRAINT ratan_fx_cashflow_brief_info_un_cashflow_id UNIQUE (cashflow_id)
);
CREATE INDEX ratan_fx_cashflow_brief_info_country_code_idx ON ratan_cash_settlement_fx_utilization_service.ratan_fx_cashflow_brief_info (country_code,value_date,settlement_means);
```

- ratan_fx_accounting_send_failed_info

Create new table

```sql
-- ratan_cash_settlement_fx_utilization_service.ratan_fx_accounting_send_failed_info definition

-- Drop table

-- DROP TABLE ratan_cash_settlement_fx_utilization_service.ratan_fx_accounting_send_failed_info;

CREATE TABLE ratan_cash_settlement_fx_utilization_service.ratan_fx_accounting_send_failed_info (
	utilize_id text NULL,
	accounting_event_data text NULL,
	send_status int2 NULL,
	id bigserial NOT NULL,
	external_key text NULL,
	trade_id text NULL,
	CONSTRAINT ratan_fx_accounting_send_failed_info_pk PRIMARY KEY (id)
);
CREATE INDEX ratan_fx_accounting_send_failed_info_send_status_idx ON ratan_cash_settlement_fx_utilization_service.ratan_fx_accounting_send_failed_info USING btree (send_status);
```

## **2.5 Open API**

### **2.5.1 Cashflows Query API**

Reuse the existing cashflows api for GUI in Query Service and only support tradeId and s2bxId parameters.

### **2.5.2 Find Curerncy2 API**

This interface supports finding currencyt2 and util amount2 by currency1 and util amount1. It's useful when user do partially utilization, this interface will return the util amount2 which apply Ratan's rounding rule config.

| URL | {nginx}/[api/ratan/v1/fx/utilization/trade/getCurrency2ByCurrency1](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/fx/utilization/trade/getCurrency2ByCurrency1) |
| --- | --- |
| Method | POST |
| Content-Type | application/json |
| Auth Action | - RATAN_STRATEGIC_CASHFLOW_BLOTTER:ACCESS_FMO_POST_TRADE_PORTAL - RATAN_FUNC:Query:Ratan_Function_Cashflow |
| Request | { "tradeId": "6721092670", "tradeLakeTradeMajorVersion":1, "swapLegId": "", // Near|Far|”” "exchangedCurrency1PaymentAmountCurrency": "USD", "exchangedCurrency1UtilAmount": 10000 } |
| Response | Response: { "status": 200, "message": "OK", "data": { "tradeId": "6721092670", "tradeLakeTradeMajorVersion": "1", "swapLegId": "", "exchangedCurrency1PaymentAmountCurrency": "USD", "exchangedCurrency1UtilAmount": 10000, "exchangedCurrency2PaymentAmountCurrency": "EGO", "exchangedCurrency2UtilAmount": 35000.00 } } Invalid TradeId: { "status": 400, "message": "Could not find any data, requested trade id may not in util scope.", "data": **null** } Trade cancelled: { "status": 400, "message": "Trade is cancelled.", "data": **null** } Trade contains error cashflow: { "status": 400, "message": "Trade contains error cashflow.", "data": **null** } Settlement method is not UTIL: { "status": 400, "message": "Settlement method is not UTIL.", "data": **null** } Invalid Currency1: { "status": 400, "message": "Can not find another currency.", "data": **null** } Ratan server error: { "status": 500, "message": "Ratan internal error.", "data": null } |

### **2.5.3 ****Utilize Request API**

This is the entry point that receive utilization request from Razor FXU system through Solace.

[FXU Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Technical+Design#FXUTechnicalDesign-FXURequest/Response)

### 2.5.4 Manual Settlement Method Update API

```
POST {nginx_host}/v1/utilization/cashflow/settlementMethod/stamping
Req:
{   
    "trades": [
         {
            "tradeId": "123",
            "cashflowIds": ["007300894620", "007300894621"]
         },
         {
            "tradeId": "456",
            "cashflowIds": ["007300894623", "007300894624"]
         },
         {
            "tradeId": "789",
            "cashflowIds": ["007300894625", "007300894626"]
         },
         {
            "tradeId": "112",
            "cashflowIds": ["007300894627", "007300894628"]
         }     
    ],
	"settlementMethod": "GROSS|UTIL",
    "comment": ""
}

Resp:
 [
        {
          "tradeId": "123",
          "cashflowIds": ["007300894620", "007300894621"],
          "success": true, 
          "errorMessage": "" 
       },
       {
          "tradeId": "456",
          "cashflowIds": ["007300894623", "007300894624"] 
          "success": true,
	      "errorMessage": "" 
       },
        {
          "tradeId": "789",
          "cashflowIds": ["007300894625", "007300894626"]  
          "success": false,
	      "errorMessage": "Action not allowed." 
       } ,
        {
          "tradeId": "112",
          "cashflowIds": ["007300894627", "007300894628"]  
          "success": false,
	      "errorMessage": "Action not allowed." 
       } 
]
```

## **2.6 Inner API**

### **2.6.1 Remaining Amount**

| URL | {Utilization Service Domain}/v1/utilization/cashflow/remainingAmount |
| --- | --- |
| Method | POST |
| Content-Type | application/json |
| Request | [ "006697383077", "006697383076", "006697380550", "006697380549", "006697104840" ] |
| Response | { "006697383076": 0.00, "006697380549": 375.16, "006697380550": 100.0, "006697383077": 0.0, "006697104840": 1000.0 } |

# **3 Static Service**

## **3.1 Utilize Query Config API（For Group Service**）

| | |
| --- | --- |
| URL | /v1/static/utilizeConfig |
| Method | GET |
| Content-Type | application/json |
| Response | [ { "id": "", "booking_entity_fmid": "xxxx", "counterparty_fmid": "xxxx", "is_auto": true/false, "settlement_means": "FXBREREC" } ] |

## **3.2 Utilize Static Data Setup API （For FE）**

| | Query |
| --- | --- |
| URL | /v1/static/utilizationEligibleRule?page=0&size=50 |
| Method | GET |
| Content-Type | application/json |
| Response | { pageNo: 0, pageSize: 50, totalPages: 3, totalHits: 124, result: [ { id: xxx, dataStatus: "ADD_PENDING", createdAt: "2025-09-18T08:54:45Z", updatedAt: "2025-09-18T08:54:45Z", makerId: "1632737", checkerId: "System", counterpartyFmId: "400703596", counterpartyFmCode: "PROFUTURO PR F 1*LIM", entityFmId: "400703598", entityFmCode: "SCB BOMBAY*MMB", autoUtil: "yes/no" }, ] } |

| | Create |
| --- | --- |
| URL | /v1/static/utilizationEligibleRule |
| Method | POST |
| Content-Type | application/json |
| Payload | { "counterpartyFmId": "1", "counterpartyFmCode": "1", "entityFmId": "10036642", "entityFmCode": "SCB SHANGH*SHA", "autoUtil": "yes" } |
| Response | { "result": "success", "recordId": "xxxx" } |

| | Delete |
| --- | --- |
| URL | /v1/static/utilizationEligibleRule/{id} |
| Method | DELETE |
| Content-Type | application/json |
| Response | { "result": "success", "recordId": "xxxx" } |

| | Approve |
| --- | --- |
| URL | /v1/static/utilizationEligibleRule/{id}/confirm |
| Method | POST |
| Content-Type | application/json |
| Response | { "result": "success", "recordId": "xxxx" } |

| | Reject |
| --- | --- |
| URL | /v1/static/utilizationEligibleRule/{id}/cancel |
| Method | POST |
| Content-Type | application/json |
| Response | { "result": "success", "recordId": "xxxx" } |

| | Audit |
| --- | --- |
| URL | /v1/static/utilizationEligibleRule/audit?page=0&size=50&entityId=765 |
| Method | GET |
| Content-Type | application/json |
| Response | { "pageNo": 0, "pageSize": 50, "totalPages": 1, "totalHits": 2, "results": [ { "id": "457a3f1a-0fb7-4e0e-8ddc-a1e8cc73cbe7", "utilizationEntityId": 780, "dataStatus": "UPDATE_PENDING", "userId": "1622463", "snapshot": { "id": 780, "counterpartyFmId": "xxxxx", "counterpartyFmCode": "xxxx", "entityFmId": "xxxx", "entityFmCode": "xxxxx", "autoUtil"： "xx", "dataStatus": "UPDATE_PENDING", "makerId": "1622463", "checkerId": "System", "createdAt": "2025-09-18T15:20:29Z", "updatedAt": "2025-09-18T15:20:29Z" }, "createdAt": "2025-09-18T15:20:29Z" } ] } |
| | |

## **3.3 Utilize Config Table**

1. ratan_fxu_config

| Field | Data Type | Not Null | Description | Primary Key |
| --- | --- | --- | --- | --- |
| id | text | Y | | Y |
| booking_entity_fmid | text | Y | | |
| booking_entity_fmcode | text | Y | | |
| counterparty_fmid | text | Y | | |
| counterparty_fmcode | text | Y | | |
| is_auto_utilize | text | Y | true, false | |
| settlement_means | text | Y | FXBRREC, FXBRREC-M | |
| settlement_account | text | Y | FXBRREC FXBRREC-M | |
| created_at | timestamp without time zone | Y | | |

# **4 Task List**

| Domain Service | Backend Task | Frontend Task | Dependency |
| --- | --- | --- | --- |
| cash-settlement-group-management-service | 1、setup Remaining_Amount and Settement_Method when entity is configured | no | UTIL Static data |
| cash-settlement-orchestration | 1、Settement_Method=UTIL skip Suppression check Netting rule check SSI /NSTP check 1. Bypass below rule check for Settlement Method = UTIL 1. Suppression Rule 2. Netting Rule 3. Swift Suppression Rule 4. NSTP Rule 2. Avoid publishing to swift service for UTIL payment | no | |
| cashflow-lifecycle-service | 1、New status Derive for FXU Action | no | |
| cash-settlement-ssi-stamping-service | 1、SSI Stamping skip VostroStamp 2、Adhoc SSI skip Vostro validation and stamp | 1、Skip Missing Voistro validation when Settlement_Method='UTIL' | UTIL Static data |
| ratanone-swift-service | 1、Double intercept for Settement_Method = UTIL | no | |
| ratanone-query-service | 1、New Query API for FXU | no | |
| cash-settlement-accounting-service | 1、CommonValidator、UtilizeValidator 2、DistributeLock with Cashflow Stella Ambassandor 3、Utilize Domain maintain 4、Manual Utilize Utilize Request Handle 5、Auto Utilize Auto Utilize DataFecher Auto Utilize Process 6、Accounting Accounting Task Generator 7、Utilize ACK/NACK/Auto Utilize ACK to FXU | no | |
| ratanone-static-data-service | 1、New Interface for GroupService & SSI Stamping Service to Get Utilize configuration 2、New Interface for GUI to CURD Utilize static data | 1、CURD for Utilize configuration | |
| cash-settlement-netting-service | 1、Intercept for netting when Settement_Method = UTIL | 1、Intercept for netting/unnet when Settement_Method = UTIL | |

# Open Point

1. when we send ack to FXU? if rejected from ebbs?