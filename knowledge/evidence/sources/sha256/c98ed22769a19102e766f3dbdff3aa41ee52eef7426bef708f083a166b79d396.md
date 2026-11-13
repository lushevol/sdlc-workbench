# Netting Function Flow

Version: 2026-09-11

## Purpose

This page explains how RATAN handles settlement netting from initial eligibility screening through execution and resultant cashflow handling.

## Editable Sources

- Markdown page source: `netting-function-flow-page-source-v20260911.md`
- GUI diagram source: `netting-function-flow-v10.drawio`
- Published Confluence page: `DSP / Netting Function Flow`

## Netting Universe

| Topic | Detail |
| --- | --- |
| Active catalogue types | IRS Auto, Bilateral Manual, Bilateral Adhoc, CCIL Guaranteed, CCIL Non-Guaranteed, Ben BIC, NDS Auto |
| Backlog | Bilateral Auto, CPN |
| Core business intent | Reduce gross settlements, save ops effort, lower nostro charges, and standardize automated cashflow handling |
| Execution rhythm | Rule-driven eligibility first, pending holding next, then scheduled or manual netting execution, followed by resultant cashflow processing |

## Operating Flow

1. Cashflows are received from Stella and Murex 2.1.
2. RATAN applies netting eligibility rules and routes eligible cashflows into the relevant pending states.
3. IRS leg aggregation, manual netting, or auto netting then determines the next path.
4. Scheduled auto-netting rules run by priority and execute only within the matched rule scope.
5. Resultant cashflows are created and processed for settlement or held in NSTP, depending on the netting outcome.
6. Single-cashflow and un-net scenarios follow exception or manual handling paths rather than re-entering auto netting.

## Main Netting Categories

| Netting Type | Typical Statuses | Core Conditions | Netting Key |
| --- | --- | --- | --- |
| IRS Netting | Pending Another Leg | Remaining leg must arrive before aggregation completes | Booking Entity FMID, Payment Date, Payment Currency, Counterparty FMID, Trade ID |
| Ben BIC Netting | WAITING, Pending Netting, Pending Auto Netting | Counterparty BIC Net Flag = Y, settlement method is not UTIL, splitting ID is blank | Booking Entity FMID, Payment Date, Payment Currency, Counterparty BIC Net Flag, Counterparty BIC Code |
| CCIL Netting | WAITING, Pending Netting, Pending Auto Netting | Settlement Method = CCIL, Counterparty BIC Net Flag is not Y, splitting ID is blank | Booking Entity FMID, Payment Date, Payment Currency |
| Bilateral Netting | PROJECTED, WAITING, READY, Pending Netting, Pending Auto Netting | Counterparty BIC Net Flag is not Y, Settlement Method is not CCIL or UTIL, splitting ID is blank | Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date |
| NDS Auto Netting | Pending Auto Netting | Typology-driven rule match on NDS child and resultant cashflows | ND Parent Trade ID, Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date |

## IRS Netting

- IRS aggregation is a distinct pre-netting step.
- The flow checks readiness from Stella and Murex.
- If another leg is still outstanding, the cashflow remains in WAITING / Pending Another Leg.
- When both legs are available, RATAN can continue to the auto-net path.

## Manual Netting Matrix

| # | Netting Type | Status Scope | Summary Condition | Key |
| --- | --- | --- | --- | --- |
| 1 | Ben BIC Netting | WAITING, Pending Netting, Pending Auto Netting | Booking entity and counterparty BIC-net criteria apply; splitting ID blank; settlement method not UTIL | Booking Entity FMID, Payment Date, Payment Currency, Counterparty BIC Net Flag, Counterparty BIC Code |
| 2 | CCIL Netting | WAITING, Pending Netting, Pending Auto Netting | Settlement Method = CCIL, non-BIC-net path, splitting ID blank | Booking Entity FMID, Payment Date, Payment Currency |
| 3 | Bilateral Netting | PROJECTED, WAITING, READY | Non-BIC-net and non-CCIL cashflows eligible for bilateral grouping | Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date |
| 4 | Bilateral Netting | WAITING, Pending Netting, Pending Auto Netting | CCIL-guaranteed style bilateral handling for the specified counterparty branch | Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date |

## Auto Netting Matrix

Priority is evaluated in ascending order. Once a cashflow matches a higher-precedence rule, it is held for that rule and does not continue to later rules.

| Priority | Netting Type | Netting Key | Resultant Mapping | Single Cashflow Swift Suppress | Description |
| --- | --- | --- | --- | --- | --- |
| 10 | SAL MTM Netting | Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date, Payment Type | Payment Type = SAL MTM Netting | Yes | Net Swap Agent MTM payments across trades |
| 20 | SAL Coupon Netting | Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date, Payment Type | Payment Type = SAL Coupon Netting | Yes | Net Swap Agent coupon payments across trades |
| 30 | Clearing_Swift_Suppress | Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date | Payment Type = Bilateral Netting | Yes | Special bilateral netting for clearing cashflows |
| 40 | CCIL Netting | Booking Entity FMID, Payment Date, Payment Currency | Counterparty FMID = 400021949, Counterparty FMCODE = CLEARING CORP*MMB, Settlement Method = Cash, Payment Type = CCIL Netting | No | Netting across CCIL counterparties |
| 50 | BIC Netting | Booking Entity FMID, Payment Date, Payment Currency, Counterparty BIC Net Flag, Counterparty BIC Code | Payment Type = Ben BIC Netting | No | Netting within the same BIC |
| 54 | NDS Auto Netting | ND Parent Trade ID, Booking Entity FMID, Counterparty FMID, Payment Currency, Payment Date | Payment Type = NDS Auto Netting | No | Net NDS child and resultant cashflows |

## Resultant and Exception Handling

- Resultant cashflows follow downstream settlement handling after successful netting.
- Single-cashflow outcomes are handled as exception scenarios rather than normal netting completion.
- Un-net cashflows do not re-enter auto-netting evaluation.
- Manual or exception handling remains relevant for cross-queue or ad-hoc client requests.

## Reference Appendices

The live Confluence page also retains these detailed reference sections:

- Full Auto Netting Rules Output
- Cashflow Dictionary
- Selected Rule Output
- IRS Aggregation Flow

These sections are reference-heavy and are better maintained from workbook or source-data refreshes rather than direct storage XML editing.

## Reading Guide

The sequence should be read as a common operating model rather than a strict single pipeline for every netting type. Each netting type shares the same broad stages, but applies different eligibility rules, matching keys, and execution controls.