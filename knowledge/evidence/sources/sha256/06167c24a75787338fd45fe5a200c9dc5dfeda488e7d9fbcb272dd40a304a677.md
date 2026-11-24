# Background

- Murex cashflows would feed into Ratan Cash Settlement VD-7 Business days earlier. And Stella also generate and feed these cashflows into Ratan Cash Settlement. Which means 7 business days cashflows **overlapped**. In case duplicated payments / accountings / LMS etc, agreed with upstream and downstream, Ratan Cash Settlement would handle it.

# PROD Approach

## Principle: Cancel Murex2.11 Cashflows and Settle Stella Cashflows.

- **NSTP** In-Scope<u>** **</u>**Murex2.11** Cashflows(VD Next Monday / Tuesday) in advance, Then they would be **CANCELLED naturally along with 'Trade Cancellation' post migration.**
- **NSTP** In-Scope **Stella **Cashflows(VD Next Monday / Tuesday) during Migration Weekend and **un-NSTP them after Recon PASS.**
- Hence Ratan Settlement would be able to **support subsequence market events on Stella cashflows.**

## Approach to **NSTP **In-Scope **Murex2.11 Cashflows **in advance

#### Problems and Obstacles

- Potential dup payment from last Migration(HKTW-Rates) - e.g. NDS Fixing - how to NSTP Murex2.11 NDS Fixing cashflows in advance and waiting them to be cancelled along with Trade Cancellation. - Murex2.11 would generate brand new FXD trades for NDIRS / NDCCS trades - different Trade Id / original Trade Id from parent trade - usually on VD-2 and no precise conditions to NSTP NDS Fixing cashflows in advance. They would be STP'd directly - e.g. M00124568264 - ![image-2026-4-21_12-7-0.png](attachments/image-2026-4-21_12-7-0.png) - ![image-2026-4-21_12-6-18.png](attachments/image-2026-4-21_12-6-18.png) - Stella use a different approach on NDIRS / NDCCS trades which is 'generating cashflows with deliverable ccy directly'. - Hence Murex FXD trades would **not be migrated** to Stella(blade) and would be** **cancelled directly post-migration - (**New info** to Cash Settlement Team after HKTW-Rates Migration go-live on 16th Nov 2025).

#### Approaches

- | No. | NSTP Criteria | Obstacles | Solution Steps | | --- | --- | --- | --- | | Approach1 **Picked on 2026-01-26 ** | Cancelled Trade Id List | - Final Cancellation Trade Id List only available on **Migration Weekend** - **Saturday** - Draft Version on Friday Night - Murex cashflows may be already STP'd by then. | 1. NSTP **Murex2.11** cashflows by following Criteria, **Create **the rule on **VD(Next Mon.)-6** 1. **Data Source System = MUREX** 2. **Payment Date in (Next Mon. , Next Tue.)** 3. **In-Scope Portfolio** 2. On Migration Weekend - **Saturday**, **update **above NSTP rule to criteria - **Data Source System = MUREX** - **Payment Date in (Next Mon. , Next Tue.)** - ~~**In-Scope Portfolio**~~ - **Cancelled Trade Id List (Original Trade Id List – update on 28th April 2026)** 3. **Cashflow Suppression & Un-Suppression **cashflows which hit above NSTP rule to** narrow down **to the **real In-Scope** cashflows. - Note: Would delay some payment to Saturday / Sunday which are supposed on Friday, **agreed **with users during last Migration (HKTW Rates on 2025-11-16) 4. **Disable **above NSTP rule on Migration Weekend - **Sunday before Murex Cancellation flow feeding in** | | ~~Approach2~~ **Dropped on 2026-01-26 ** | ~~Portfolio~~ | - ~~Would block Payment of out-of-scope Murex cashflows~~ - ~~pls refer to page [11 Murex211 Exception/Exclusion Rule - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3507903952)~~ | NA | | ~~Approach3~~ **Dropped on 2026-01-26** | ~~original Trade Id List or Typology: NDS Fixing~~ | - ~~Would block Payment of out-of-scope Murex cashflows~~ - ~~May Miss some In-Scope cashflows~~ | NA |

- - **EXPAND: Approach2 Sample** FMRP7.0 Trade Migration UAT with COBE Date: 2025-12-26 | Streams | By Portfolio | By Trade Id List | | --- | --- | --- | | FXO | 856 ![image-2026-1-16_11-51-7.png](attachments/image-2026-1-16_11-51-7.png) | 299 ![image-2026-1-16_14-12-0.png](attachments/image-2026-1-16_14-12-0.png) | | ASEN | 684 ![image-2026-1-16_17-45-33.png](attachments/image-2026-1-16_17-45-33.png) **Not use taxonomy as condition to filter?** | 361 ![image-2026-1-16_17-43-58.png](attachments/image-2026-1-16_17-43-58.png) Resultant cf no included if different Trade Id. | **EXPAND_END**

## Approach to **NSTP **In-Scope **Stella Cashflows **during Migration weekend

- | No. | NSTP Criteria | Solution Steps | Rule Sample | | --- | --- | --- | --- | | Approach1** ** | Portfolio | 1. NSTP **Stella** cashflows by following Criteria, **Created **on Migration weekend - **Saturday**. 1. **Data Source System in (Stella, Ratan)** 2. **Payment Date in (Next Mon. , Next Tue.)** 3. **In-Scope Portfolio** 2. **Disable **On Migration Weekend - **Sunday after Recon PASS**, 3. **Cashflow Suppression & Un-Suppression **cashflows which hit above NSTP rule. So Stella cashflows would be **processed as normal BAU behavior**(e.g. STP'd). | ![image-2026-1-26_12-55-20.png](attachments/image-2026-1-26_12-55-20.png) ![image-2026-1-26_13-11-0.png](attachments/image-2026-1-26_13-11-0.png) |

# **Note**

- **The Approach is for Trade Migration on PROD.**
- **Approach for Murex Cashflows would be different while UAT / DR phase since Murex cashflows already there while securing prod dump.** - **What's done already done, e.g. released / settled**