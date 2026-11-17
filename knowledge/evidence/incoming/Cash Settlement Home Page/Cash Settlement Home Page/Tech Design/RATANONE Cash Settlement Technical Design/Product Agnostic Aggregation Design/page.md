# Business Background

[[Draft]Product Agnostic Aggregation based on Normalized Payment Schedule - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/%5BDraft%5DProduct+Agnostic+Aggregation+based+on+Normalized+Payment+Schedule)

# UBER Message

## UBER Message sample

### It will stamp normalizedPaymentSchedule element when we call TDSX API with original Uber message (so far only support : IRS, CCS, LNBR and FRA). Below screenshot is the sample.

![image-2026-8-12_9-48-10.png](attachments/image-2026-8-12_9-48-10.png)

### If the cashflow is not in above taxonomies, then Uber message will not stamp normalizedPaymentSchedule node even call TDSX API.

📎 [out_8751171913_FXSpot.json](attachments/out_8751171913_FXSpot.json)

### Enhance existed IRS rule for product agnostic aggregation

- existed IRS rule for Stella - Data_Flow__Data_Source_System matches "(?i)^Stella$" && Instrument_Common__ISDA_Taxonomy in ("InterestRate:IRSwap:FixedFloat","InterestRate:IRSwap:OIS","InterestRate:IRSwap:FloatFloat","InterestRate:IRSwap:Basis","InterestRate:IRSwap:FixedFixed") && Cashflow__Payment_Type in ("Coupon/Fixed","Coupon/Float") && Cashflow__Cashflow_Event_Type not matches "(?i)Withdrawal" && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "")
- add Entity__Booking_Entity_SCI_FMID and Entity__Counterparty_SCI_FMID limition - Entity__Booking_Entity_SCI_FMID in ("300011345", "10038345") && Entity__Counterparty_SCI_FMID in ("10055390", "10037780", "10023033", "205001936") - ~~Cashflow__Cashflow_Event_Reason not in ("Reversal", "Rebook") ~~? Withdrawal == Reversal

# V2 process before workflow after group-service

## Business scenario

📎 [Aggregation Trade Cashflow Events_2026_09_23_v1.xlsx](attachments/Aggregation Trade Cashflow Events_2026_09_23_v1.xlsx)

## Rules set up

### Trade level

- **<u>Data_Flow__Data_Sender matches "(?i)^Stella$" && Instrument_Common__ISDA_Taxonomy in ("InterestRate:IRSwap:FixedFloat","InterestRate:IRSwap:OIS","InterestRate:IRSwap:FloatFloat","InterestRate:IRSwap:Basis","InterestRate:IRSwap:FixedFixed") && Entity__Booking_Entity_SCI_FMID in ("300011345", "10038345") && Entity__Counterparty_SCI_FMID in ("10055390", "10037780", "10023033", "205001936")</u>**

### Cashflow level

- **<u>Cashflow__Payment_type not matches "(?i)Fee" </u>**
- **<u>Cashflow__Is_Cashflow_SettleAsGross != true && Cashflow__Aggregate_Status in ("Pending_Aggregate","Auto_Aggregated")</u>**

## High level

### Benefit

1. Keep all existed Group process
2. Aggregation base on final cashflows info(such as some fields stamp and rounding).

### Disadvantage

1. Cashflow count need calculate from group and aggregation services.

## Tigger cashflow aggregate before Group-Service

### Aggregation Service workflow

#### Basic logic

#### DB desgin

##### ratan_cashflow_aggregation_service.ratan_cashflow_aggregate_records

##### ratan_cashflow_aggregation_service.ratan_cashflow_aggregate_records_history

##### ratan_cashflow_aggregation_service.ratan_group_inbound_messages

##### ratan_cashflow_aggregation_service.ratan_cashflow_aggregate_outbound

#### Open question

1. How to handle historic cashflows?
2. How to process it when A1 is netted + released with other cashflow and c1 rebook c1' come? Allow c1' flow into Ratan or c1' aggregate with other cashflows first?
3. Is it write back to stella for Aggregation?
4. Could aggregated resultant cashflow do netting with Murex cashflows?

# Trigger Aggregation after Group-service process

## Business scenario

📎 [Aggregation Trade Cashflow Events_2026_09_23_v1.xlsx](attachments/Aggregation Trade Cashflow Events_2026_09_23_v1.xlsx)

## High Level

### Benefit

1. It can fetch all cashflows from original UBER message.
2. Aggregated cashflow will be stored in Group service.

### Disadvantage

1. Break Group service receive cashflows sequence
2. Disable Non Eco process, will generate new cashflows once non eco message arrive.

## Base Logic