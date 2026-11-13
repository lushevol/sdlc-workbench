# Background

There's new business function onboarding to Murex 2.11 which would using the swap agent clear service for the payments, there would be hybrid payment & accounting model required means not all payments would be settled( only accounting required).

The basic requirement is as below

- Trade would generate initial & final principal payments which would require bilateral payment
- Interim coupon & interim principal won't go with bilateral payment with bilateral client but would be settled by the swap agent service, these payments would be suppressed in settlement platform & only accounting required.

# Booking Model

There're limitation by Murex which they can't book one trade to cater for the requirement to generate the required principal & interim coupon, Murex has to split the booking into 3 trades within the same package.

- Trade 1: Mainly generating the interim coupon but as Murex, but as **Murex limitation** they would generate dummy principal payments. | Flow Type | Value Date | Amount | LTI ID | Strategy | Typology | Settlement Requirement | | --- | --- | --- | --- | --- | --- | --- | | Initial Principal (**dummy**) | T+2(Start date +2) | 100mio | 123456 | SWAP_AGENT | Vanilla X-ccy swap | No Settlement, Accounting only | | Interim Coupon 1 | 3M+2 | 2mio | 123456 | SWAP_AGENT | Vanilla X-ccy swap | No Settlement, Accounting only | | Interim Coupon 1 | 6M+2 | 2mio | 123456 | SWAP_AGENT | Vanilla X-ccy swap | No Settlement, Accounting only | | Interim Coupon 1 | 9M+2 | 2mio | 123456 | SWAP_AGENT | Vanilla X-ccy swap | No Settlement, Accounting only | | Final Principal ( **dummy**) | 12M+2(Maturity +2) | (-1) 100mio | 123456 | SWAP_AGENT | Vanilla X-ccy swap | No Settlement, Accounting only |
- Trade 2: To generate the initial & final principal payments which need actual settlement with client( bilateral settlement). | Flow Type | Value Date | Amount | LTI ID | Strategy | Typology | Settlement Requirement | | --- | --- | --- | --- | --- | --- | --- | | Initial Principal (Bilateral Settlement) | T(Start date) | 100mio | 123456 | SWAP_AGENT | RFR CCS MTM Fixing | Bilateral Settlement | | Interim Principal 1 | 3M | 10 mio | 123456 | SWAP_AGENT | RFR CCS MTM Fixing | No Settlement, Accounting only | | Interim Principal 1 | 6M | 10 mio | 123456 | SWAP_AGENT | RFR CCS MTM Fixing | No Settlement, Accounting only | | Final Principal (Bilateral Settlement) | 12M(Maturity) | (-1) 100mio | 123456 | SWAP_AGENT | RFR CCS MTM Fixing | Bilateral Settlement |
- Trade 3: This is to resolve the problem with trade 1 which Murex generate the additional dummy payments( suppose not be settled), Murex would book opiate payments from trade 3 to knock off the 2 dummy payments from trade 1. | Flow Type | Value Date | Amount | LTI ID | Strategy | Typology | Settlement Requirement | | --- | --- | --- | --- | --- | --- | --- | | Initial Principal (**Dummy**) | T+2(Start Date+2) | 100mio | 123456 | SWAP_AGENT | RFR CCS MTM Fixing | No Settlement, Accounting only | | Final Principal (**Dummy**) | 12M+2(Maturity+2) | (-1) 100mio | 123456 | SWAP_AGENT | RFR CCS MTM Fixing | No Settlement, Accounting only |

# Function Requirement for Murex & RATAN

- Settle the initial & final principal from trade 2 as bilateral
- Bypass settlement for all the other payments & generate accounting only
- All the payments would generate accounting on Main Nostro account
- No netting required for these payments

# Proposed solution

Murex is saying there's limitation they can't handle these requirement within Murex and proposing to send all these payment to RATAN.

- They don't have the capacity to assign different Vostro on same entity/counterparty/currency, means they need to assign 'SUPPRESSXXX' on trade 1&2 and assign normal Vostro on trade 2.

# Open questions

# RATAN Potential Change

- Consume the Swap Agent settle & Swap Agent non settle flag from Murex 2.11
- Define the swift suppression rule for the Swap Agent non settle cashflows