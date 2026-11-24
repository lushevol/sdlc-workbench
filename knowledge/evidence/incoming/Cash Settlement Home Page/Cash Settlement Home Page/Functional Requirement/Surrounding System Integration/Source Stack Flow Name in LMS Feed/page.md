#

# Background

As part of strategic approach to distinguish the different types of trade workflow that go through SABRE, new field Source_Stack_Flow_Name was introduced and contains one of the following values:

RATAN will consume the value to dispatch the cashflow to different settlement process

- **BCSSTELLA **- BCS Flow
- NativeSTELLA (this will not flow to RATAN)
- **FMRPSTELLA**: FMRP Flow
- **FMRPSTELLA-LOANIQ** : FMRP Flow

# Specifications

Current Process

| Cashflow Data Source | Stack Flow Value | Settlement Process | Trade Original Source System | Netting Resultant Source Value | Netting Resultant Stack Value | Swift/Accounting | Source Value sent to LMS | Tag20 Prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BCSSTELLA→ Stella | BCSSTELLA | BCS | TBC | null | null | RAZOR | STELLA | EQ |
| Blade→ Stella | FMRPSTELLA | FMRP | Blade | if component are the same, derive the value if not, set to null | null | RATAN | FMRP | DV |
| Blade | null | null | RAZOR (For EGNPSA) | NA | FX |
| LOANIQ→ Stella | FMRPSTELLA-LOANIQ | FMRP | LOANIQ | LOANIQ | null | RAZOR | LOANIQ | LQ |
| Murex | null | FMRP | null | null | null | RATAN | FMRP | DV |

Stack field: /scb:SCBML/scb:header/scb:originationDetails/scb:messageSender/scb:messageSender[@systemScheme="[http://www.sc.com/coding-scheme/stack-flow](http://www.sc.com/coding-scheme/stack-flow)"]

Data source field in LMS feed: /scb:SCBML/scb:header/scb:originationDetails/scb:messageSender/scb:messageSender systemScheme='[http://www.sc.com/coding-scheme/system-1-0](http://www.sc.com/coding-scheme/system-1-0)']

**Proposal 1**: get stack field value and set to the data source field to LMS - Confirmed with LMS team to implement this one

| Cashflow Data Source | Stack Flow Value | Settlement Process | Netting Resultant Stack Value | Swift/Accounting | Source Value sent to LMS | Tag20 Prefix |
| --- | --- | --- | --- | --- | --- | --- |
| BCSSTELLA→ Stella | BCSSTELLA | BCS | | RAZOR | STELLA | EQ |
| Blade→ Stella | FMRPSTELLA | FMRP | FMRPSTELLA | RATAN | FMRPSTELLA | DV |
| RAZOR (For EGNPSA) | NA | FX |
| LOANIQ→ Stella | FMRPSTELLA-LOANIQ | FMRP | FMRPSTELLA-LOANIQ | RATAN | FMRPSTELLA-LOANIQ | LQ |
| Murex | FMRPMUREX | FMRP | if component are the same, derive the parent value if not, set the value to FMRPSTELLA | RATAN | FMRPSTELLA FMRPMUREX | DV |

**EXPAND: Proposal 2 - rejected**

**Proposal 2**: add stack field value to LMS feed

| Cashflow Data Source | Stack Flow Value | Settlement Process | Netting Resultant Stack Value | Swift/Accounting | Source Value sent to LMS | Stack flow value in LMS feed | Tag20 Prefix |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BCSSTELLA→ Stella | BCSSTELLA | BCS | | RAZOR | Stella | BCSSTELLA | EQ |
| Blade→ Stella | FMRPSTELLA | FMRP | FMRPSTELLA | RATAN | FMRP | FMRPSTELLA FMRP | DV |
| RAZOR (For EGNPSA) | NA | | FX |
| LOANIQ→ Stella | FMRPSTELLA-LOANIQ | FMRP | FMRPSTELLA-LOANIQ | RATAN | LOANIQ | FMRPSTELLA-LOANIQ | LQ |
| Murex | MUREX | FMRP | if component are the same, derive the parent value if not, set the value to FMRPSTELLA | RATAN | FMRP | FMRPSTELLA MUREX | DV |

Netting derive logic:

**EXPAND_END**

# Deployment

Considering there might be the case that user net cashflow before the change and release it after.

It’s better to deploy the change in 2 releases:

1. Deploy the change to derive stack value in netting service
2. Change the data source value from LMS feed in next release

# Integration Test Case

| Stack Flow Value | Test Step | Expected Result | Test Data | Status | Comment |
| --- | --- | --- | --- | --- | --- |
| FMRPSTELLA | 1. cashflow received in Ratan and SI stamped 2. maker/checker approve the transaction 3. swift sent and cashflow moved to Released status 4. Withdrawal event received and released | 1.new message sent to LMS with source field value set to "FMRPSTELLA" 2. withdrawal message sent to LMS with source field value set to "FMRPSTELLA" | ~~006148455905 new event sent to LMS~~ 006148455910 new event sent to LMS 006148455910 withdrawal sent to LMS~~ ~~ | New and Withdrawal is received as expected | test DB refreshed, rebook another cashflow for withdrawal event |
| FMRPSTELLA -LOANIQ | 1. cashflow received in Ratan and SI stamped 2. maker/checker approve the transaction 3. cashflow sent and status moved to Released | 1. message sent to LMS with source field value set to "FMRPSTELLA -LOANIQ" | 006164794767 new event sent to LMS | New is received as expected | currently there is no withdrawal event for LOANIQ cashflow |
| FMRPMUREX | 1. cashflow received in Ratan and SI stamped 2. maker/checker approve the transaction 3. swift sent and cashflow moved to Released status 4. Withdrawal event received and released | 1. message sent to LMS with source field value set to "FMRPMUREX" 2. withdrawal message sent to LMS with source field value set to "FMRPMUREX" | M01737519205 new event sent to LMS M01737519205 Withdrawal event sent to LMS | New and withdrawal is received as expected | |
| STELLA | 1. cashflow received in Ratan and SI stamped | 1. message sent to LMS with source field value set to "STELLA" | 104838976010 new event sent to LMS 005565870127 ew event sent to LMS | New is received as expected New is received as expected | @Kaiyuan Xue Can you please book a debit cashflow to confirm if the Tag20 PREFIX is fine? |
| FMRPSTELLA -LOANIQ | 1. 2 cashflow received in Ratan and SI stamped 2. user net the cashflow 3. maker/checker approve the netting resultant cashflow 4. swift sent and cashflow moved to Released status | 1. message sent to LMS with source field value set to "FMRPSTELLA -LOANIQ" | (net 006164794768,006164794768) N00000037098 new event sent to LMS | New is received as expected | |
| FMRPMUREX | 1. 2 cashflow received in Ratan and SI stamped 2. user net the cashflow 3. maker/checker approve the netting resultant cashflow 4. swift sent and cashflow moved to Released status | 1. message sent to LMS with source field value set to "FMRPMUREX" | (M01737519206/M01737519207) N00000037066 new event sent to LMS | New is received as expected | no withdrawal event for netting resultant cashflow after released |
| FMRPSTELLA | 1. 2 cashflow received in Ratan and SI stamped (component have different stack) 2. user net the cashflow 3. maker/checker approve the netting resultant cashflow 4. swift sent and cashflow moved to Released status | 1. new message sent to LMS with source field value set to "FMRPSTELLA | (M01737519209/ 006148455906 ) N00000037131 new event sent to LMS | New is received as expected | no withdrawal event for netting resultant cashflow after released |
| FMRP | Mock cashflow message with source value set to FMRP | | 106148455910 new event sent to LMS | New is received as expected | |
| LOANIQ | Mock cashflow message with source value set to LOANIQ | | 106164794767 new event sent to LMS | New is received as expected | |

Questions:

1. if LMS value is backward compatible? yes, FMRP/LOANIQ will also mapped in LMS, no dependency on Ratan release time.
2. test env: both SIT/UAT are OK from LMS, will send sample for the connectivity testing.
3. general release plan - LMS will release the change prior.