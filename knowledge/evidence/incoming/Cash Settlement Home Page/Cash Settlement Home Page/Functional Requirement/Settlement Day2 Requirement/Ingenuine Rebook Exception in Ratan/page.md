# Problem Statement

A trade amendment triggers two downstream cashflow events:

1. Withdrawal of the original cashflow
2. Creation of a new cashflow

When the original cashflow has already been released from Ratan, operations users need to perform additional validation before releasing the withdrawal and new cashflows. To enforce this control, the expected behavior is:

- Generate a reversal exception for the withdrawal event
- Generate a rebook exception for the new cashflow event

However, there is currently no direct linkage between the original and new cashflows, so the system cannot reliably identify amendment-driven new cashflows for rebook exception generation.

As a workaround, system generates a rebook exception when another cashflow under the same trade ID(Original trade id for murex cashflow) and currency has already been released or settled, and its payment date is within **15** days of the new cashflow.

This approach provides partial coverage but may introduce false alert because it relies on proximity logic rather than explicit amendment lineage.

## false alert sample

- Swap
- ![image-2026-6-9_23-12-44.png](attachments/image-2026-6-9_23-12-44.png)

# Current Implementation

To reduce false alerts, we performed additional analysis and refined the rebook-exception logic. Under the updated logic, a rebook exception is generated only when another cashflow under the same Trade ID ( Original Trade ID for Murex cashflows) and with the same currency, has already been released or settled, and its payment date is within **5** days of the new cashflow.

Compared with the previous 15-day validation window, the 5-day window + CCY validation is expected to reduce rebook-exception volume by approximately 40%.

![image-2026-6-9_20-46-25.png](attachments/image-2026-6-9_20-46-25.png)

This change was deployed to the production environment on May 30, 2026. The rebook-exception volumes before and after the deployment are shown below.

| Date | Rebook Exception （Murex+Stella） |
| --- | --- |
| 20260504-20260508 | 656 (444+212) |
| 20260511-20260515 | 443 (329+114) |
| 20260518-20260522 | 501 (370+131) |
| 20260525-20260529 | 386 (346+40) |
| **20260530** | **change deployment** |
| 20260601-20260605 | 292 (277+15) |
| 20260608-20260612 | 134 (125+9) |
| 20260615-20260619 | 171 (146+25） |

# Potential Enhancement

- Add direction into the query criteria
- Consider to add trade event after uber enabled.