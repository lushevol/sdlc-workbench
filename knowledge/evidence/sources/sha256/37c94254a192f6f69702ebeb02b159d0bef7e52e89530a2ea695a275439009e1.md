# Background

There would be new currency onboarding from TP system during the BAU, there're some currency related static data are maintained in RATAN local. This document is capturing the static data we need to review & decide if any new/update required.

# Currency Cutoff

Static data to control the cashflow release date/time, cashflow post this cutoff would start the swift generation and can't touched by settlement ops any more.

Data lookup key: Legal Entity/Currency
![image2024-6-13_17-10-53.png](attachments/image2024-6-13_17-10-53.png)

# Nostro Static Data

Nostro is one of mandatory static data for settlement process and we have to create the Nostro data for the new onboarding currency.

# PM Currency List

It's used to identify if the currency is precious metal, if yes it would drive the MT604/MT605/MT692 generation. Right now the data is hardcode PM currency list provided by Murex 2.11 colleagues, 
The list is maintained in the swift generation document [FMRP Swift Generation - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)

# Booking Currency → ISO Code mapping

For both Swift/Accounting the currency has to be converted to ISO Code instead of the original booking currency, there's one hardcoded booking currency → Currency ISO Code mapping provided by Murex 2.11 colleagues.

The data is maintained in accounting function document [Cash Settlement - Accounting - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+Accounting)

# Rounding Logic

RATAN is building the tactical rounding logic for cashflow migration H1 release( SG/MY/IN), need to check if the new onboarded currency is available in the current rounding config. Details can be found in [Rounding Rule - Tactical solution for H1 2024 Cashflow Migration - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Rounding+Rule+-+Tactical+solution+for+H1+2024+Cashflow+Migration)