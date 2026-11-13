# Background

Currently vostro is not mandatory for SCB receive cashflow, but for some precious metal ccy, vostro info are required in swift generation which will lead to the cashflow stuck in swift generation error. User expect to enhance the stamping validation to avoid such cases.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5510918](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5510918)

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6473001](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/6473001)

# Requirement Details

1. **Auto Stamping** - **ASI-IS:** Vostro is mandatory for SCB Pay cashflow and optional for all SCB receive cashflow - **TO-BE:** For SCB receive cashflow with currency in (‘XAU’,‘XAG’,'XPD','XPT'), vostro will be mandatory which is the same as SCB pay cashflow
2. **Manually update SSI** - **AS-IS:** When user add adhoc SSI from cashflow details UI and submit the change, system will apply below validation: 1. Mandatory field in vostro/nostro 2. vostro settlement means/settlement account should be the same as nostro settlement means/settlement account - **TO-BE: ** 1. For SCB pay cashflow, keep the same validation as above 2. For SCB receive cashflow with PM currency in (‘XAU’,‘XAG’,'XPD','XPT'), apply the same validation as above 3. For SCB receive cashflow with settlement means = "Over-Account", apply the same validation as above ~~if mandatory field not added in vostro, popup soft warning: vostro info required to generate swift, are you sure to proceed?~~ 4. For other SCB receive cashflow except item b,c, 1. bypass as-is vostro mandatory validation 2. if vostro SSI Type is null, auto populate the vostro settlement means/settlement account to the same as nostro