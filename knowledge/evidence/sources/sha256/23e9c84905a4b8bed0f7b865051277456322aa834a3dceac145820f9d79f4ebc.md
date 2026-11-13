- [FMRP China Cash Settlement Delivery Plan](https://confluence.global.standardchartered.com/display/DSP/FMRP+China+Cash+Settlement+Delivery+Plan)
- [Functional Requirement](https://confluence.global.standardchartered.com/display/DSP/Functional+Requirement)
- [MX2.11 Decomm - Cash Settlement Business Workflow](https://confluence.global.standardchartered.com/display/DSP/MX2.11+Decomm+-+Cash+Settlement+Business+Workflow)
- [SFMRP - Cash Settlement Platform Architecture](https://confluence.global.standardchartered.com/display/DSP/SFMRP+-+Cash+Settlement+Platform+Architecture)
- [Quality Assurance](https://confluence.global.standardchartered.com/display/DSP/Quality+Assurance)
- [Leave Plans](https://confluence.global.standardchartered.com/display/DSP/Leave+Plans)
- [Strategic Cash Settlements Features](https://confluence.global.standardchartered.com/display/DSP/Strategic+Cash+Settlements+Features)
- [Settlement Hive](https://confluence.global.standardchartered.com/display/DSP/Settlement+Hive)
- [CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/CN+Retrospective)
- [Tech Design](https://confluence.global.standardchartered.com/display/DSP/Tech+Design)
- [CN Code Review Session](https://confluence.global.standardchartered.com/display/DSP/CN+Code+Review+Session)
- [Cash Settlement/BAU Hand Over](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3085545383)
- [2025 Target](https://confluence.global.standardchartered.com/display/DSP/2025+Target)
- [AI Discovery](https://confluence.global.standardchartered.com/display/DSP/AI+Discovery)
- [Ratan OpenFin & FDC3 Explore](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3270865431)
- [Documents](https://confluence.global.standardchartered.com/display/DSP/Documents)
- [RATAN - Data entitlement test cases](https://confluence.global.standardchartered.com/display/DSP/RATAN+-+Data+entitlement+test+cases)
- [2026 BRP Q3 On-Going Stories](https://confluence.global.standardchartered.com/display/DSP/2026+BRP+Q3+On-Going+Stories)
- [Other system related](https://confluence.global.standardchartered.com/display/DSP/Other+system+related)

Background

FMRP decision back then when the strategic stack was formalized its been concluded to have Razor as Strategic Cash settlements platform with analysis & understanding at that stage.

During BCS implementation there were various impediments identified by PO, FMO users & technology teams when solutioning various Settlements features which has called for re discussion on the direction to proceed with complex products and payment features to be built in the strategic its been decided by the Chief PO's that the right direction to proceed with Strategic stack is to build the Cash settlements Services in house that can potentially replace Razor processing

| SN | Impediments during BCS Execution | Strategic - Cash Settlements services |
| --- | --- | --- |
| 1 | Significant time spend on creation of technical portfolio setup, control governance documentation and ongoing monitoring. Ownership of the NSP is misaligned as PCT2 requires FO ownership but the NSP are purely post trade with no genuine trade booking. | Reduction in Murex License Cost |
| 2 | Razor imports the CF data as trade and not cashflow itself causing overhead in terms of number of references (ID's) created (STELLA Payment ID mapped to External ID, Razor trade ID & Razor CF ID) | Clear ownership of Post trade data sits within Post trade teams |
| 3 | Razor generates Trade Accounting for those cashflows which has to be suppressed at Aspire in contra having only to generate settlement accounting | Dedicated Payment Lake capturing every action, data & audit instead of cashflow |
| 4 | Established Cash functionalities already existing in Razor cannot be re used as the cash settlements workflow is isolated and needed rebuild on each of them (Ex: Netting, Split) | Elimination of NSP creation |
| 5 | No Flexibility in Payment Events definition for Amendments /updates | Cashflow inception is straight forward eliminating bottlenecks incurred when imported as trade |
| 6 | Payment Feature builds (like Net/Un Net) becomes complex in implementation & maintainability (build has to be shared between STELLA, RATAN & Razor) | Re use or extend already built services. |
| 7 | Removes payment exceptions where CP account codes aren’t tagged in Razor. (redundant exception activity | Data extraction is simpler/ can be at one source - Payment Lake instead of TDS3+ RATAN+ RAZOR |
| 8 | Added complexity in SCI and static maintenance overhead in SCI as Derivative only counterparties need to be tagged to Razor | Creates a single source of settlement system to FMSRE release timing rules (current design requires a staged released to allow for resolution of any Razor related exceptions) |
| 9 | Multiple logins required for FMO users to Razor and Ratan to resolve any Razor specific exceptions | |
| 10 | Annual swift upgrade impact to payment messages needs to be updated in multiple systems in todays design | |
| | | |

# Project Goal

1. Design and build a strategic settlement platform, which is an in-house built application to get rid of the dependency on the vendor product
2. It is supposed to solve the existing pain points
3. It should be stable and flexible enough to cover complicated business scenarios
4. A platform to be open sourced within TPT to benefit as many teams as possible

# Working Agreement

- Don't be afraid to ask for help
- Product Owner is available during core hours
- Be on time for meetings
- Define and adhere to ‘DONE’ criteria for stories/tasks

# Member for China Cash Settlement

8 story points is the capacity when a member can contribute for the whole sprint.

-1 when there is leave taken in the sprint.

| | **PSID** | **Name** | Contribution Rate | **Role** | **Leave Plan** | **Sprint 1** **(09 Jan - 20 Jan)** **8MD** | **Sprint 2** **(23 Jan - 03 Feb)** **8MD** | **Sprint 3** **(06 Feb - 17 Feb)** **8MD** | **Sprint 4** **(20 Feb - 03 Mar)** **8MD** | **Sprint 5** **(06 Mar - 17 Mar)** **8MD** | **Sprint 6** **(20 Mar - 31 Mar)** **8MD** | **Sprint 7** **(03 Apr - 14 Apr)** **7MD** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1490627 | Liam(50%) | 50% | Tech Chapter Lead | | 4 | 3 | 4 | 4 | 4 | 4 | 3.5 |
| 2 | 1481696 | Geoffrey | 100% | Deliver Lead | 26<sup>th</sup> - 27<sup>th</sup> Jan | 8 | 5 | 8 | 8 | 8 | 8 | 7 |
| 3 | 1480988 | Lina | 100% | Scrum master | | 8 | 6.5 | 8 | 0 | 0 | 0 | 0 |
| 4 | 1490623 | Wayne | 100% | BA | 26<sup>th</sup> - 27<sup>th</sup> Jan | 8 | 5 | 8 | 8 | 8 | 8 | 7 |
| 5 | 1662744 | Eric | 100% | Architect | 26<sup>th</sup> - 31<sup>st</sup> Jan | 8 | 2.5 | 8 | 8 | 8 | 8 | 7 |
| 6 | 1582024 | Lyn | 100% | BA | 26<sup>th</sup> - 27<sup>th</sup> Jan | 8 | 5 | 8 | 8 | 0 | 0 | 0 |
| 7 | 1490618 | Amy | 100% | Murex Dev | | 8 | 6.5 | 8 | 8 | 8 | 8 | 7 |
| 8 | 1639646 | Clover | 100% | Murex Dev/QA | | 8 | 6.5 | 8 | 8 | 8 | 8 | 7 |
| 9 | 1639796 | Lu, Shuai | 100% | UI engineer | | 8 | 6.5 | 8 | 8 | 8 | 8 | 7 |
| 10 | 1612086 | Wang, Guangqing | 100% | Backend Developer | | 8 | 6.5 | 8 | 8 | 8 | 8 | 7 |
| 11 | 1640671 | Eddie | 100% | Backend Developer | 26<sup>th</sup> - 27<sup>th</sup> Jan | 8 | 5 | 8 | 8 | 8 | 8 | 7 |
| 12 | | Zoey | 100% | Scrum master | | 0 | 0 | 0 | 8 | 8 | 8 | 7 |
| 13 | | Ma, Shimeng | 100% | QA | | 0 | 0 | 0 | 0 | 0 | 0 | 7 |
| 14 | | | | | | | | | | | | |

# 2022 Q4 Goal

**EXPAND: November update**

# Key Achievements

| | **Activity** | | **Status** |
| --- | --- | --- | --- |
| 1 | Cashflow Storage & Data Read/Write Splitting | | |
| 2 | Cashflow blotter load data from RATAN DB | [Ratan One](http://10.198.199.160:8453/) | |
| 3 | Cashflow Materialization Done | | |
| 4 | Cashflow Status Machine Done | | |
| 5 | Cashflow Netting & Un-netting supported | | |

# Key Action List

| | **Activity** | **Status** |
| --- | --- | --- |
| 1 | Workflow verification and preparation for the Q4 demo | |
| 2 | Real time recon with upstream solutioning | |
| 3 | Data query condition build for UI search | |

**EXPAND_END**

**EXPAND: September update**

# Key Achievements

| | **Activity** | Links for details | **Status** |
| --- | --- | --- | --- |
| 1 | Design done for technical architecture of strategic settlement process | **[SFMRP - Cash Settlement Architecture](https://confluence.global.standardchartered.com/display/DSP/SFMRP+-+Cash+Settlement+Platform+Architecture)** | |
| 2 | Basic principle defined and agreed on Ratan to take over STELLA actions for cashflows | **[Cashflow generation & settlement](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2530777788)** | |
| 3 | CPN business scenarios collection and analysis done | **[CPN Business Scenario](https://confluence.global.standardchartered.com/display/DSP/CPN+Business+Scenario)** | |
| 4 | Trade level SSI stamping dev done for FX Spot/Forward | **[SSI Stamping Tech Design-Egypt](https://confluence.global.standardchartered.com/display/DSP/SSI+Stamping+Tech+Design-Egypt)** | |

# Key Action List

| | **Activity** | Links for details | **Status** |
| --- | --- | --- | --- |
| 1 | Changes to be done on the overall technical architecture since the direction has been modified and confirmed | **[SFMRP - Cash Settlement Architecture](https://confluence.global.standardchartered.com/display/DSP/SFMRP+-+Cash+Settlement+Platform+Architecture)** | |
| 2 | Stella integration detailed design and review | **[Cashflow generation & settlement](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2530777788)** | |
| 3 | Cross product netting technical design | | |
| 4 | TPT Tech forum presentation | | |
| 5 | VAT presentation | | |

**EXPAND_END**

**EXPAND: August update**

# Key Achievements

| | **Activity** | Links for details | **Date** | **Status** |
| --- | --- | --- | --- | --- |
| 1 | Foundation & Infrastructure design | **[Foundation Service Mesh Platform](https://confluence.global.standardchartered.com/display/DSP/Foundation+Service+Mesh+Platform)** **[Cash Settlement Technical View](https://confluence.global.standardchartered.com/display/DSP/SFMRP+-+Cash+Settlement+Platform+Architecture?moved=true#SFMRPCashSettlementPlatformArchitecture-TechnicalView)** | 15<sup>th</sup> Aug | |
| 2 | We have agreed the co-development model | **[Co-development Guideline](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+Platform+-+Co-development+Guideline)** | 15<sup>th</sup> Aug | |
| 3 | Agreed on the status machine for payment lifecycle | **[Status Machine](https://confluence.global.standardchartered.com/display/DSP/CN+Cash+Settlement+Payment+Status+Machine#CNCashSettlementPaymentStatusMachine-StatusMachine)** | 16<sup>th</sup> Aug | |
| 4 | Agreed on the high level business processing flow with PO | **[Business Processing Flow](https://confluence.global.standardchartered.com/display/DSP/CN+Cash+Settlement+Payment+Status+Machine#CNCashSettlementPaymentStatusMachine-BusinessProcessingFlow)** | 18<sup>th</sup> Aug | |

# Key Action List

| | **Activity** | Links for details | **Status** |
| --- | --- | --- | --- |
| 1 | An high level design and workflow processing was proposed | **[Workflow View](https://confluence.global.standardchartered.com/display/DSP/SFMRP+-+Cash+Settlement+Platform+Architecture?moved=true#SFMRPCashSettlementPlatformArchitecture-WorkflowView)** | Awaiting Razor colleagues to provide their design on next catchup, which is on the workflow due to different ideas |
| 2 | Cross product netting analysis | | |
| 3 | Payment lake analysis and design | | |
| 4 | TPT Tech forum presentation | | |
| 5 | VAT presentation | | |

**EXPAND_END**