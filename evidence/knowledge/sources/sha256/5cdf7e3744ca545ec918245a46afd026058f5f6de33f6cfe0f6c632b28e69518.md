| Product_ISDA | Cashflow Type | Payment taxonomy | Schedule_Date | Schedule_Currency |
| --- | --- | --- | --- | --- |
| any | Additional Payments | Additional_Payment.Additional_Party_Payment_type | Additional_Payment.Additional_Party_Payment_Date | Additional_Payment.Additional_Party_Payment_Amount_Currency |
| IRS (deliverable/ND), CCS (deliverable/ND) | Coupons | Coupon/<Fixed/Float> | Swap_Instrument.IR_Leg.First_Leg.Periodic_Cash_Flow.Periodic_Adjusted_Interest_Payment_Date | coalesce (Swap_Instrument.IR_Leg.First_Leg.Cash_Settlement_Currency, Swap_Instrument.IR_Leg.First_Leg.Notional_Amount_Currency) |
| | Coupons | Coupon/<Fixed/Float> | Swap_Instrument.IR_Leg.Second_Leg.Periodic_Cash_Flow.Periodic_Adjusted_Interest_Payment_Date | coalesce (Swap_Instrument.IR_Leg.Second_Leg.Cash_Settlement_Currency, Swap_Instrument.IR_Leg.Second_Leg.Notional_Amount_Currency) |
| CCS (deliverable/ND) - non MTM | Principal | <Initial/Final/Amortization>Exchange/Fixed | Swap_Instrument.IR_Leg.First_Leg.Periodic_Cash_Flow.Periodic_Notional_Exchange_Date | coalesce (Swap_Instrument.IR_Leg.First_Leg.Cash_Settlement_Currency, Swap_Instrument.IR_Leg.First_Leg.Notional_Amount_Currency) |
| | | <Initial/Final/Amortization>Exchange/Fixed | Swap_Instrument.IR_Leg.Second_Leg.Periodic_Cash_Flow.Periodic_Notional_Exchange_Date | coalesce (Swap_Instrument.IR_Leg.Second_Leg.Cash_Settlement_Currency, Swap_Instrument.IR_Leg.Second_Leg.Notional_Amount_Currency) |
| | Amortizing | AmortizationExchange/Fixed | Swap_Instrument.IR_Leg.First_Leg.Step_Schedule.Notional_Amortization_Schedule_Date | |
| | | AmortizationExchange/Float | Swap_Instrument.IR_Leg.Second_Leg.Step_Schedule.Notional_Amortization_Schedule_Date | |
| | | | | |

### Tech Design

For Expected Payment Count, we need to compare current payment data with trade scheduled payment for both payment currency and payment date.

Only when the trade.Schedule_Currency = Cashflow.Payment_Currency and trade.Schedule_Date = Cashflow.Payment_Date, it can be taken into expected payment count calculation.

For IRS and CCS, we need to compare both leg, if any leg schedule matches with current payment, it should be taken into expected payment count calculation.

### Business Case

## Step 3: Auto Netting

| Cashflow ID | Payment Date | Currency | Expected Payment Count | Actual Payment Count | Cashflow In the Same Group | Cashflow Status |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | 2025 Sep 15 | USD | 4 | 1 | C01 | Pending Another Leg |
| C02 | 2025 Sep 15 | USD | 4 | 2 | C01, C02 | Pending Another Leg |
| C03 | 2025 Sep 15 | USD | 4 | 3 | C01, C02, C03 | Pending Another Leg |
| C04 | 2025 Sep 15 | USD | 4 | 4 | C01, C02, C03, C04 | Netted |

Netting by key:

Same trade ID + Payment Date +Payment Currency + Entity + Counterparty

## Step 4: Aggregation Resultant Cashflow can be Netted