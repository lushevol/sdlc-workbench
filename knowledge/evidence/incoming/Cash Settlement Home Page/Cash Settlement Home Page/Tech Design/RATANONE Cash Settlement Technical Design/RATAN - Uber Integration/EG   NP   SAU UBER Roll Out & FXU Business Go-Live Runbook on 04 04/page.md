# Release Work Item:

Release page link: [Release On 2026-04-04 CR: RATAN Settlement - FXU Biz Go-Live - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Release+On+2026-04-04+CR%3A+RATAN+Settlement+-+FXU+Biz+Go-Live)

# Release Date

2026-04-04

# Release Coordinators

| Team | Coordinators |
| --- | --- |
| TDSX | @Rui Li @Ray Guo PSS: SABRE [SABRE.PSS@sc.com](mailto:SABRE.PSS@sc.com) |
| RATAN | @Ruiheng Cao @Xinmiao Huang @Yonghua Li PSS: [RATAN_PSS_SME@sc.com](mailto:RATAN_PSS_SME@sc.com) |
| | |

# Runbook

| Steps | On Date | Start Time | Des. | Owner | Status | SQL Or Rule | Evidence | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | **Pre Release** |
| 1 | 2026-04-03 | | Book New Trade **UVT page**: [EG / NP / SAU: UBER UVT and FXU MVP UVT - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3673553968) | MO | | | | |
| ~~2~~ | 2026-04-04~~ ~~ | ~~9:00AM SGT(On Demand, time would be changed)~~ | ~~TDS3 stop publisher of SCBML trade, cashflow.~~ ~~TDSX stop publisher of Uber flow~~ | ~~TDS3 & TDSX~~ | ~~~~ | | | ~~Only stop EG, NP, SA - confirmed by ~~~~@Junwei Peng it is not possible.~~ ~~Sabre green zone is 12:00 PM SGT so not able to execute this step~~ |
| 3 | 2026-04-04 | 9:30AM SGT | Confirm no message back logs in EDMI topic & queue | RATAN PSS | | | ** ** | |
| 4 | 2026-04-04 | 9:45AMSGT | Confirm no pending groups for EG, NP, SA | RATAN PSS | | **Whether has group not 'COMPLTED'(expect no records):** select g.* from ratan_cashflow_group_management_service.ratan_cashflow_group g, ratan_cashflow_group_management_service.ratan_cashflow_group_message gm where gm.booking_entity_id in ('401036553', '400007847', '400991880') and g.status != 'COMPLETED' and g.id = gm.group_id ; **Whether has group message 'PENDING' (expect no "PENDING"):** select gm.status, count(status) from ratan_cashflow_group_management_service.ratan_cashflow_group_message gm where gm.booking_entity_id in ('401036553', '400007847', '400991880') group by gm.status ; | ** ** | If unexpected case happen, we need upstream to publish the specific data to let the group complete? Yes, refer to step 6 |
| 5 | 2026-04-04 | 10:00PM SGT | On demand option - if any message missing, we need upstream to publish/replay the specific cashflow to complete group | SABRE PSS | | ** ** | ** ** | @Zeyu Zhou help to add 1 more task for SABRE PSS , step will be shared by @Ankur Dutt |
| 6 | 2026-04-04 | 12:00AM SGT | On demand option - if lots of messages stuck in EDMI and continuous publishing, need SABRE PSS help to stop the publisher. | SABRE PSS | | ** ** | ** ** | @Zeyu Zhou help to add 1 more task for SABRE PSS to stop/start publisher in green window. |
| 6 | 2026-04-04 | 10:00AM SGT - 13:00AM SGT | Stop message bridge | RATAN PSS | | ** ** | ** ** | |
| | **Release** |
| 6 | 2026-04-04 | 10:00AM CST | Ratan installation | RATAN PSS | | Refer to AIG | ** ** | |
| ~~7~~ | 2026-04-04~~ ~~ | ~~11:00AM CST(On Demand)~~ | ~~TDS3 start publisher ~~ ~~TDSX start publisher~~ | ~~TDS3 &TDSX~~ | ~~~~ | | ~~** **~~ | |
| | **Post Release(UVT)** |
| 8 | 2026-04-04 - 2026-04-06 | | **UVT page**: [EG / NP / SAU: UBER UVT and FXU MVP UVT - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3673553968) | MO | | | | |