# Background

The ideal clearing booking model

- Trade booked with bilateral counterparty but FO/MO/System know this is clearing trades which would be cleared( novated to clearing counterparty), there suppose be clearing indicator( e.g. UDF clearing_status in Murex 2.11)
- With this clearing indicator, original payment from original trades( with bilateral counterparty) **won't be STP**, but waiting for the later novation( original payments with bilateral counterparty would be cancelled).
- After Novation, there would be payment generated facing clearing counterparty( form the novated trade).
- Clearing team would net these post novated payments, no settlement required but just accounting.

# Murex Problem & Limitation

Murex problem

- For SWAPWIRE trades, there's no clearing flag( **the indicator reminder every team no bilateral settlement is allowed**) on trade on the booking
- It depends on subsequent event to correct the trade adding the clearing flag, this can take 2 hours. Problem is when the payment is generated from the original trades, Murex won't be able to send the clearing status to RATAN( it's not available on the trade).
- Even for the trade which booked with clearing status, Murex have tech limitation( concern from PSS not allowing adding new fields to payment message) which they can't include the clearing indicator on payment.
- After the original payment sent to RATAN, even Murex updated the clearing status indicator( which is UDF) there's Murex limitation they won't be able to send the update to RATAN( by additional payment event). Similar like the non eco trade amendment they can't guarantee the latest info are sent to RATAN, the data between Murex & RATAN are not in sync.

| **Row Labels(SRC_SYSTEM)** | **Comments** | **Novation to Clearing House** |
| --- | --- | --- |
| | Manual booking | |
| ASTROID | Only Beta trades booking (MUMBAI only) | No |
| BLADE | Only Beta trades booking | No |
| CFETS | First version has clearing status (CHINA HO and HONGKONG only) | Yes |
| Hurricane | NDF - No Alpha impact (no Alpha payment) | Yes |
| ION | First version has clearing status | Yes |
| LIMITHUB | Both alpha and Batea in the same package for client clearing | No |
| LYNX | NDF - No Alpha impact (no Alpha payment) | Yes |
| PACMAN | Only Beta trades booking | No |
| RTNS | NDF - No Alpha impact (no Alpha payment) | Yes |
| SWAPSWIRE | First version does not have clearing status, following modify message update it | Yes |
| TRAIANATRM | First version has clearing status | No |

# Detail cases which have risk - If no clearing status available in RATAN

- Trade only novated on VD-1 1. Trade booked with bilateral client A, first payment C1 is T+5. Payment sent to RATAN without any clearing status indicator 2. Payment C1 is STP in RATAN, waiting for cutoff which is VD-1 3. Cutoff approaching on VD-1, payment C1 auto released with client A as bilateral settlement 4. MO Novated the trade after the payment settled as bilateral, reversal of C1 & new C2(with clearing counterparty) populated 5. Settlement team need to recall the C1 with client A which is very risky, the escalation would be more serious if settlement ops fail to recall the payment in 10 days.

# Potential Solution to mitigate the risk

- **Approach 1- Consume the clearing status by some approach** 1. Trade booked with bilateral client A, first payment C1 is T+5. Payment sent to RATAN without any clearing status indicator. - **Additional control that RATAN get the clearing status indicator & NSTP C1, Eric again propose RATAN to consume the clearing status from TDS3 trades. This is a design call to align.** 2. Payment C1 is NSTP in RATAN, won't be auto release 3. MO Novated the trade after the payment settled as bilateral, C1 would be cancelled & C2(with clearing counterparty) generated 4. RATAN would have netting rule to stop C2 as pending netting, given all these clearing counterparty are known and won't have so many( around 20 clearing counterparty only).
- **Approach 2- Define NSPT rule with source system name( for these source system which are doing clearing), this need to proved by the data that there won't be much normal trades which don't need clearing with same source system( e.g. if there're many normally trades with SWAPSWIRE which don't need stopped as NSTP, this solution won't work). ** 1. Trade booked with bilateral client A, first payment C1 is T+5. Payment is stopped by NSTP rule(** source system is SWAPSWIRE**)**.** 2. Payment C1 is NSTP in RATAN, won't be auto release 3. MO Novated the trade after the payment settled as bilateral, C1 would be cancelled & C2(with clearing counterparty) generated 4. RATAN would have netting rule to stop C2 as pending netting, given all these clearing counterparty are known and won't have so many( around 20 clearing counterparty only).