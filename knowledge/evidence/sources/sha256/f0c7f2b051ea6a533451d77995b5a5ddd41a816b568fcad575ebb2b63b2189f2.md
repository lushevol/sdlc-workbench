#

# Background

- The Suspension logic(part of) that cashflows not settled in Ratan Settlement marked as status: SUSPENDED by Stella would move to Ratan Settlement. - [SUSPENDED vs PROJECTED cashflow status in Ratan - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SUSPENDED+vs+PROJECTED+cashflow+status+in+Ratan) - [Stella cashflow logic for SUSPENDED vs PROJECTED - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Stella+cashflow+logic+for+SUSPENDED+vs+PROJECTED)
- After movement, in-scope cashflows will be marked as status: PROJECTED by Stella and status: **RATAN_SUSPENDED /CASHFLOW_SUPPRESSED** by Ratan Settlement.
- Uber adoption for all entities

# Test Cases for Uber testing(Dinesh)

| **Time** | **Action** | **Message Format** | **Action Party** | **Status** | **Trade Id** |
| --- | --- | --- | --- | --- | --- |
| 5*th* Aug – 7*th* Aug | Book a test CCS with notational USD 1 vs GBP, VD 10*th* Aug, Trade Id: 8640993952 | SCBML | MO | | 8640993952 |
| 5*th* Aug – 7*th* Aug | Release the USD leg notational (MT202), cashflow Id: 008640993953,008640993954 | SCBML | Settlement OPS | | |
| 8*th* Aug | Change implementation for enabling UBER for all entity | UBER | Application team | | |
| 8*th* Aug | Eco amend the notional to USD 2 | UBER | MO | | |
| 8*th* Aug | Release the USD leg notational on both cancellation and rebook (MT192 for USD 1 and MT202 for USD 2) | UBER | Settlement OPS | | |
| 8*th* Aug | Cancel the CCS | UBER | MO | | |
| 8*th* Aug | Release the USD leg notational for cancellation (MT192 for USD 2) | UBER | Settlement OPS | | |

# Test Cases for Suspension logic movement(Elena)

| No. | Scenarios | Pre-Movement | Post-Movement | **Production Trade Reference** | Test By | Test Date | Result | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC1 | **New Trade Booking** - **Portfolio Hierarchy** - |Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|FXO* - **Taxonomy**: - ForeignExchange:Swap | Stella: SUSPENDED Ratan Settlement: SUSPENDED | Stella: PROJECTED Ratan Settlement: - **RATAN_SUSPENDED** | 8285805957 | | 2026-08-08 | | - **Trade Id**: 8648205001 cashflow: **CASHFLOW_SUPPRESSED **as expectation. because - booking entity: 10075222 - SCB LONDON*LDN - ctpty: 300037151 - CAASH*ROLL ![image-2026-8-8_16-21-46.png](attachments/image-2026-8-8_16-21-46.png) Trade Cancellation ![image-2026-8-8_16-23-30.png](attachments/image-2026-8-8_16-23-30.png) |
| TC2 | **New Trade Booking** - **Portfolio Hierarchy** - |Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Rates* - **Taxonomy**: - ForeignExchange:Forward - **ctpty** - ~~**300010953 - IRS SECTION*LDN **~~ - **10036642 - SCB SHANGH*SHA** | Stella: SUSPENDED Ratan Settlement: SUSPENDED | Stella: PROJECTED Ratan Settlement: - **RATAN_SUSPENDED** - ~~**CASHFLOW_SUPPRESSED**~~ - ~~**ctpty: 300010953 - IRS SECTION*LDN**~~ | - ~~8613660539 with ctpty **300010953 - IRS SECTION*LDN**~~ - **8594727573 with ctpty **10036642 - SCB SHANGH*SHA | | 2026-08-08 | | **Trade Id**: 8648205010 cashflow: **RATAN_SUSPENDED **as expectation. ![image-2026-8-8_16-24-28.png](attachments/image-2026-8-8_16-24-28.png) Trade Cancellation ![image-2026-8-8_16-24-48.png](attachments/image-2026-8-8_16-24-48.png) |
| ~~TC3~~ | ~~**New Trade Booking**~~ - ~~**Portfolio Hierarchy**~~ - ~~|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Commodities*~~ - ~~**Taxonomy**:~~ - ~~ForeignExchange:Spot~~ - ~~ForeignExchange:Forward~~ - ~~ForeignExchange:Swap~~ | ~~Stella: SUSPENDED~~ ~~Ratan Settlement: SUSPENDED~~ | ~~Stella: PROJECTED~~ ~~Ratan Settlement:~~ - **~~RATAN_~~SUSPENDED** | | | | | |
| ~~TC4~~ | ~~**Trade Migration**~~ - ~~**Past VD aggregated cashflows**~~ | ~~Stella: SUSPENDED~~ ~~Ratan Settlement: SUSPENDED~~ | ~~No change~~ | | | | | |
| ~~TC5~~ | ~~**New Trade Booking**~~ - ~~PreAllocation ~~ | ~~Stella: SUSPENDED~~ ~~Ratan Settlement: SUSPENDED~~ | ~~No change~~ | | | | | |
| | | | | | | | | |
| | | | | | | | | |