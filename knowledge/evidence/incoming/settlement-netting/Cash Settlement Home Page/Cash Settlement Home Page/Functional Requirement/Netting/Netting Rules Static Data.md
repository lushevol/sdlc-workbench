# Netting Rule Category & Scope

There would be multi netting static data rules defined in Ratan and driving the cashflow netting process.

- Netting eligibility rule: Rules to determine the cashflow is eligible for netting and holding as NSTP. Settlement ops will filter these pending netting cashflows and manually perform netting.
- ~~Potential netting rule: Cashflows won't be NSTP but would have separate Ratan→Razor release cutoff time. Removed from CN Day 1 Scope.~~
- ~~Auto netting rule: Cashflows to be holding in 'auto netting pool' and wait for EOD auto netting job to perform the netting without user manual intervention. Netting resultant cashflow still need review & approval as part of multi excetion process. ~~Removed from CN Day 1 Scope.~~~~
- ~~These rules will be maintained in different tiles from GUI. ~~Removed from CN Day 1 Scope.~~~~

# Netting Rule Structure & Key attributes

- Netting Rule: Rule would be defined with the below fix attributes. | Attribute | Operator | Logical Model Field | Can be Blank? | Sample | Optional | | --- | --- | --- | --- | --- | --- | | Booking Entity FM Code | IS | Entity.Booking_Entity_SCI_FMCODE | | SCB SHANGH*SHA, SCB CN CHO*CHO | | | Client FM Code | IS | Entity.Counterparty_SCI_FMCODE | | BARCLAYS FX*LDN | | | Product Type | IS/IN | Instrument_Common.ISDA_Taxonomy | Y | InterestRate:CrossCurrency:Basis | |
- ~~Auto Netting Rule: Rule would be defined with the below fix attributes. Not for Day 1 Scope.~~ | Attribute | Operator | Logical Model Field | Can be Blank? | Sample | | --- | --- | --- | --- | --- | | Booking Entity FMID/FM Code | IS | Entity.Booking_Entity_SCI_FMID Entity.Booking_Entity_SCI_FMCODE | | | | Portfolio | IS | | Y | | | Client FMID/FM Code | IS | Entity.Counterparty_SCI_FMID Entity.Counterparty_SCI_FMCODE | | 10036739 BARCLAYS FX*LDN | | Product Type? | IS/IN | Instrument_Common.CFI_Code Instrument_Common.ISDA_Taxonomy | Y | SRACCP InterestRate:CrossCurrency:Basis | | Currency | IS/IN | Cashflow.Payment_Currency | Y | USD | | Currency Pair | IS/IN | | Y | | | Auto Netting Shifter | IS | | | VD-5/VD-4/VD-3/VD-2/VD-1 |
- ~~Potential Netting Rule. Not for CN Day 1.~~ | Attribute | Operator | Logical Model Field | Can be Blank? | Sample | | --- | --- | --- | --- | --- | | Booking Entity FMID/FM Code | IS | Entity.Booking_Entity_SCI_FMID Entity.Booking_Entity_SCI_FMCODE | | | | Portfolio | IS | | Y | | | Client FMID/FM Code | IS | Entity.Counterparty_SCI_FMID Entity.Counterparty_SCI_FMCODE | | 10036739 BARCLAYS FX*LDN | | Product Type? | IS/IN | Instrument_Common.CFI_Code Instrument_Common.ISDA_Taxonomy | Y | SRACCP InterestRate:CrossCurrency:Basis | | Currency | IS/IN | Cashflow.Payment_Currency | Y | USD/Blank | | Currency Pair | IS/IN | | Y | USD/TRY |

# Netting Rule Execution & Exception Fix: