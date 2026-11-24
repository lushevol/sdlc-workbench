# Background

Strategic Cash settlement is running on production for almost 2 years. Mostly the application is running smoothly, but undeniable there are some technical debts make our application faces a lot of challenges.

- Hard to expand new logic in status machine, and not support transactional status update very well. High risk to modify the current code.
- Deep coupling between microservices, the boundary is not clear enough, e.g. orchestration-service and lifecycle-service.
- Performance Issue occurred sometimes, need deep analysis on system bottleneck.
- Deep coupling with SCBML, there is a lot of disadvantages of using xml data format - Verbosity - Parsing Complexity - Limited Readability - Performance issue - Lack of Flexibility - Limited Data Types support

# Purpose of Design

Considering the current tech debts, Raise several high level topics and break them down according to the priority, each high level topic should have a complete detail design.

Tech debt page:

[Technical Debt - FMRP China Cash Settlement - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Technical+Debt+-+FMRP+China+Cash+Settlement)

# Main topics

| | Topic | Owner | Problem Statement |
| --- | --- | --- | --- |
| 1 | State machine Restructure | @Xinmiao Huang | |
| 2 | Workflow optimization | @Xinmiao Huang | |
| 3 | Function Domain segregation | @Xinmiao Huang | |
| 4 | SCBML Decommission | @Xinmiao Huang | |
| 5 | Distributed lock issues | @Chen Yang | |
| 6 | Strategic SSI | @Quill Li | |
| 7 | Open search Integration | @Ruiheng Cao | |

# Topic 1: State machine Restructure

## Break down tasks

| Task No. | Description |
| --- | --- |
| 1 | Restructuring lifecycle service |
| 2 | Remove all useless table and clean up the related code |
| 3 | isBeforeValueDate is useless, can be removed and use isAfterValueDate instead |
| 4 | |
| | |

1. Table Analysis ![image-2025-5-13_16-51-0.png](attachments/image-2025-5-13_16-51-0.png)
2. Status machine Logic ![image-2025-5-13_17-14-48.png](attachments/image-2025-5-13_17-14-48.png)

3. State Machine new UML

4. Change suggestions:

- Close All NSTP and SSI exceptions is not required, or final consistency is ok, workflow will natively close exceptions if any new cashflow inbound or reinstate
- Auto release job has issue if message didn't consumed by workflow successfully but status in lifecycle stable is already released2Razor.
- Cashflow Stamping fields move to standardization service, by default stamping all required attributes from surrounding systems, if reinstate, lifecycle only call standardization service for specific attributes.
- STP actions mostly covered by command, manual actions mostly covered by command + handler
- Data persistence will happen in postprocess method, process method can be run in parallels.
- Batch status update transactional cases: - Netting(use JdbcTemplate for batch update on status and netting id, Net New do the insert only) - UnNetting(Use JdbcTemplate for batch update on status and netting id). - Component status update(Use JdbcTemplate for batch update on Status and netting id)).

# Topic 2: Workflow Optimization

Change suggestion

- Precheck will only do the data validation and persistence, if validation failed, workflow move status to TechFail.
- Move cutoff calculation to 2-1 beginning in case TechFail result in cutoff missing and need to check every next step.
- Auto Materialization(materialize directly check) move from lifecycle precheck to workflow
- Remove "Publish Post Process" from sent to Razor flow
- remove Swift service distributed lock for swift generation, swift status write back to lifecycle should be final consistency.
- Auto UnNet checking from netting service instead of lifecycle service.

![image-2025-5-14_14-47-6.png](attachments/image-2025-5-14_14-47-6.png)

![image-2025-5-14_10-36-39.png](attachments/image-2025-5-14_10-36-39.png)

![image-2025-5-14_10-49-6.png](attachments/image-2025-5-14_10-49-6.png)

# Topic 3 - Function Domain segregation

1. Cashflow Stamping move to Standardization Service

# Topic 4 - SCBML Decommission