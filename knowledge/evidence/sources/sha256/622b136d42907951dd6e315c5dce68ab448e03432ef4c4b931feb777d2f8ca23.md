# Background

- The aggregation on cashflows under the **same** trade would happen in Murex2.11 which is not implemented in Stella - cashflows generator of FMRP Flow.
- As a supplement, Ratan Settlement System introduced IRS Netting & CCS Auto Netting to do Auto Aggregation which limits to specific Taxonomies(IRS & CCS).
- We have already foresee the above supplementary approach could no longer satisfy the auto aggregation requirement since additional Taxonomies(e.g. InterestRate:LoanDeposit) introduced in FMRP Flow.
- Also even for IRS, we found a new model - there are multiple cashflows in second leg which isn't supported by current IRS Netting. - details, pls refer to [Story 15005868 [FMRP 8.0 India Rates] IRS trade - second leg with multiple cashflows](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15005868).
- Hence we work with upstream / data modeling team to introduce Normalized Payment Schedule to support strategical Product Agnostic Aggregation.

# Requirement in ADO

- [Story 14618546 [2026 BRP Q3 RatanSett Enhancement] Product Agnostic Aggregation based on Normalized Payment Schedule](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14618546)

# Requirement Details

**Note**: Elena: 4th Aug, Newest version of User Cases, pls refer to attached excel.
📎 [analysis.xlsx](attachments/analysis.xlsx)

- Sheet: - Happy User Cases - Negative User Cases - Historical Data-User Cases

# Happy User Cases

![image-2026-7-27_11-7-42.png](attachments/image-2026-7-27_11-7-42.png)

![image-2026-7-27_11-9-7.png](attachments/image-2026-7-27_11-9-7.png)

![image-2026-7-27_11-9-46.png](attachments/image-2026-7-27_11-9-46.png)

![image-2026-7-27_11-10-25.png](attachments/image-2026-7-27_11-10-25.png)

# Negative User Cases

![image-2026-7-27_11-12-55.png](attachments/image-2026-7-27_11-12-55.png)

# Historical Data-User Cases

![image-2026-7-27_11-13-45.png](attachments/image-2026-7-27_11-13-45.png)