## Problem statement

In current BAU, we have multiple challenges with BIC based netting:

- We will have lot of Give up counterparties onboarded to murex on daily basis and we will not have visibility of those counterparties. Settlements team will come to know only once the trades are booked and we will have mismatch on settlement amount where newly created counterparty not part of PAYSTP_NET Table.
- This allow user to manually net cash flows between multiple queues (Bilateral netting and BIC Based Netting) and we need to suppress all cash flows and arrange for manual payment via OSCAR.
- We have also noticed Swift BIC not getting captured in Murex system which is causing manual actions for team where we need to net cash flows in different queue and payment done out side murex.
- We also have significant risk where UDF tables not getting updated on time leading to Gross Net Issues.

With above existing pain points hence I was requesting that Ratan UDT should have Swift BIC as main criteria and not based on counterparty code or LEID.

| Entity Code | Family | Group | Type | Typology | Strategy | BIC |
| --- | --- | --- | --- | --- | --- | --- |
| SCB LONDON*LDN | CURR | FXD | FXD | ALL | ALL | BARCGB5G |

## Solutioning

1. Allow user to define Beneficiary BIC netting eligible list, as part of rule maintenance, through business rule profile (FMO_BR_APR & FMO_BR_MKR).
2. If cashflow satisfies Beneficiary BIC netting static, it will be moved to WAITING + Pending Netting status automatically. **EXPAND: Ben BIC Static** **EXPAND_END**
3. Control build to reduce operation risk, as it only allow cashflow on **Same BIC_Net Flag (Y) + ****Same Beneficiary BIC + ****Same Value Date + ****Same Currency +****Same Entity**, can be performed as BIC Netting.
4. For Ben BIC netting eligible cashflow, operation team can manually **Settle As Gross** if necessary.
5. If any amendment or withdrawal on Ben BIC component cashflow, netting resultant cashflow will be **auto un-netted** if it's not released yet.
6. There are **segregation **between Ben BIC Netting and CCIL Netting/Bilateral Netting
7. **Affirmation **details need to be filled in when validating netting resultant cashflow.
8. Netting Resultant cashflow parameter will follow Murex logic 1. Family/Group/Type/Typology/Strategy/Trade ID value will Inherit from component cashflow if the values are same, empty if value are different

## Demo Cases

| | Item | Scenario | Steps | Expected Behavior | Ready for Testing |
| --- | --- | --- | --- | --- | --- |
| 1 | Perform Netting | | | | |
| 2 | Maker-Checker Process | | | | |
| 3 | Settle as Gross | | | | |
| 4 | Deselect all when filter after select certain cashflow | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |

Open Questions:

1. BIC is the mediumusage as MXR from SCI