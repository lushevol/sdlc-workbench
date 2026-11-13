# Background

In the current BAU( CN/SG/IN/MY/AG/EG/NP/SA/LOANIQ) for the same client there can be multi Vostro setup from different dimensions, there was best matching logic defined to decide which SSI is the best to use for settlement.  
During UK cashflow migration Vostro static data review new requirement raised to adjust the best matching logic for UK entities.

| SSI ID | BranchId_Murex3Id | CFI_Code | Is_Default_SSI |
| --- | --- | --- | --- |
| 001 | SCB LONDON*LDN | *R**** | True |
| 002 | SCB LONDON*LDN | *R**** | False |
| 003 | SCB LONDON*LDN | ****** | True |
| 004 | Global | SR**** | True |
| 005 | Global | SR**** | False |
| 006 | Global | *R**** | True |

# Vostro Stamping in the BAU

There're 2 major steps for SSI stamping.

- **Query the Vostro from SSI+ ES**: We would try to query SSI+ ES API for one time only to get all possible Vostro If we got the cashflow booked with particular entity e.g. **SCB LONDON*LDN** & CFI Code as **SR******( Rates Swap) 1. BranchId_Murex3Id in (**SCB LONDON*LDN, Global) ** 2. CFI_Code in** ( SR****, *R****, ******)** 3. Other conditions like currency/counterparty FMID etc.
- **Run the best matching** : If there're multi Vostro returned from SSI+ best matching logic would decide which SSI is the best to use 1. **Filter by product hierarchy**: Keep the SSI with most detail granular level & drop the others. | SSI ID | BranchId_Murex3Id | CFI_Code | Is_Default_SSI | Filter Result | | --- | --- | --- | --- | --- | | 001 | SCB LONDON*LDN | *R**** | True | Dropped | | 002 | SCB LONDON*LDN | *R**** | False | Dropped | | 003 | SCB LONDON*LDN | ****** | True | Dropped | | 004 | Global | SR**** | True | Good to use | | 005 | Global | SR**** | False | Good to use | | 006 | Global | *R**** | True | Dropped | 2. **Filter by by Branch hierarchy & Primary/Secondary** | SSI ID | BranchId_Murex3Id | CFI_Code | Is_Default_SSI | Filter Result | | --- | --- | --- | --- | --- | | 004 | Global | SR**** | True | Good to use | | 005 | Global | SR**** | False | Dropped | The selection sequence of different combination of Branch & Primary/Secondary is as below. | Priority | Description | BranchId_Murex3Id | Is_Default_SSI | | --- | --- | --- | --- | | 1 | Country Specific + Primary | SCB LONDON*LDN | True | | 2 | Global + Primary | Global | True | | 3 | Country Specific + Secondary | SCB LONDON*LDN | False | | 4 | Global + Secondary | Global | False |

# Change scope

- No change on existing BAU ( CN/SG/IN/MY/AG/EG/NP/SA/LOANIQ)
- The new changes is to adjust the best matching logic for UK cashflow migration only: - If entity in CN(including HEFEI), SG, IN, MY, AG, EG, SA, NP or original source system=LOANIQ will go with original best matching logic - else (currently including UK, HK, TW, TAIPEI) will go with new best matching logic
- Any new entity/products onboarding would be assessed separately: Prime/Global Rates/New Cashflow Migration entities

# Best Matching for UK Cashflow Migration

1. **Branch VS Global**: Drop all the global SSI if there're UK specific Vostro. **Note**: For other case if there's only Global branches, system would keep all these Global branch SSI in step 1 & continue the step 2 & step 3 filtering. | SSI ID | BranchId_Murex3Id | CFI_Code | Is_Default_SSI | Filter Result | | --- | --- | --- | --- | --- | | 001 | SCB LONDON*LDN | *R**** | True | Good to use | | 002 | SCB LONDON*LDN | *R**** | False | Good to use | | 003 | SCB LONDON*LDN | ****** | True | Good to use | | 004 | Global | SR**** | True | Dropped | | 005 | Global | SR**** | False | Dropped | | 006 | Global | *R**** | True | Dropped |
2. **Filtering by product hierarchy**: Keep the SSI with most detail granular level & drop the others. e.g. for below 3 SSI keep the CFI Code *R**** only and drop the ******. | SSI ID | BranchId_Murex3Id | CFI_Code | Is_Default_SSI | Filter Result | | --- | --- | --- | --- | --- | | 001 | SCB LONDON*LDN | *R**** | True | Good to use | | 002 | SCB LONDON*LDN | *R**** | False | Good to use | | 003 | SCB LONDON*LDN | ****** | True | Dropped |
3. **Filtering by Primary/Secondary**: Take the primary SSI as high priority. e.g. eventually for the below cases SSI ID 001 is picked up & we have good unique stamping result. | SSI ID | BranchId_Murex3Id | CFI_Code | Is_Default_SSI | Filter Result | | --- | --- | --- | --- | --- | | 001 | SCB LONDON*LDN | *R**** | True | Good to use | | 002 | SCB LONDON*LDN | *R**** | False | Dropped |

![SSI Hierarchy Difference.jpg](attachments/SSI Hierarchy Difference.jpg)