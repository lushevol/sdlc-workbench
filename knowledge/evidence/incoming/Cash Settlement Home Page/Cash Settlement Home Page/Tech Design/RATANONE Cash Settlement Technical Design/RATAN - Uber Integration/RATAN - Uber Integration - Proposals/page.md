| | Options | Flow | Standardization Service inbound (Group) | Standardization Service outbound | Effort | Risk to Current Flow | PROs | CONs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Current BAU Flow | FMRP + Murex | SCBML | SCBML | - | - | - | - |
| 2 | Strategic RATAN Settlement Data Model principle | FMRP | UBER | Strategic RATAN data model (JSON) | **Medium** Many services to be updated | High | 1. Strategic movement in one go, single strategic data model in RATAN 2. Get rid of SCBML completely in RATAN processing flow | Higher risk on full migration, potentially impacts Murex flow. |
| Murex | SCBML |
| 3 | Murex flow no impact principle | FMRP | UBER | Strategic RATAN data model (JSON) | **Medium +** Effort of above option + effort of managing 2 workflows | Medium | Minimal risk for Murex flow | 1. 2 workflows to be managed 2. Both SCBML and JSON exist in Ratan data model |
| Murex | SCBML | SCBML |
| 4 | Smallest change principle | FMRP | UBER | Strategic RATAN data model (JSON), additionally add SCBML | **Small** Only change Group & Camunda msg extraction | Low | 1. Only Group Service and Camunda are mandatory and sensitive on UBER/JSON 2. All other services remain the same, support one by one migration | Duration will be long for getting rid of SCBML eventually |
| Murex | SCBML |

Standardization (Group):

1. Group management for Murex
2. Cashflow Attributes Stamping
3. Trade validation/confirmation control

Lifecycle:

1. Status movement
2. Data persistence
3. Validation

Workflow:

1. Business flow routing
2. Status movement trigger point 1. Processing workflow determination, 1. currently lifecycle is responsible like materialization, revert to queued 2. cashflows post netting/un-net 2. Current withdrawal driven auto Unnet is a circle workflow, optimization needed to resolve it

| Phase | Summary | Purpose and Testing Scope |
| --- | --- | --- |
| 1 | New workflow UBER front to back process New version of all APIs | Build capability of processing UBER 1. EG, NP, SA 2. FXO |
| 2 | Integration 1. Historical SCBML data 2. Murex SCBML data | Historical data and Murex Data compatibility All entities |
| 3 | Open Search Build for extract from new data model + integration with front end | |
| 4 | Production go live rehearsal by a clear cutover | Ensure no events lost during transition of topic |
| | | |

# Uber Low Level Integration

###

| | Business Case | Expectation | Blocker & Concerns |
| --- | --- | --- | --- |
| 1 | Workflow STP process | 1. Independent workflow for Uber for EG/NP/SA 2. Keep existing flow for rest of the payments 3. Expect to optimize the workflow with below principle 1. Business flow routing, simplify lifecycle responsibility 2. Status movement trigger point 4. A consist lifecycle status update API to integrate with. 2 APIs for same action is not expected. 5. Lifecycle service - except the status update API, other related API e.g. cutoff calculation, holding check, cashflow stamping need a new version API or only support JSON in current API need to be clarified. | 1. Workflow is being updated by 2 squads, new workflow means large effort of keep the changes and regression 2. Domain service need to separate a new API for only two different points 1. Message deserialization by message type. 2. lifecycle status update different API invoke for different message type 3. The concern is we create a lot of duplicate code and maintain effort is double. |
| 2 | Rule service - exception checker approve | Rule service doesn't know either fmid or message type, it's not able to know which API to call. Expect a consist lifecycle API to integrate with. 2 APIs for same action is not expected. | 1. Currently BAU only live the new API by business function level, e.g. auto netting use new API, but other nettings use legacy API, which is only support SCBML. 2. If Uber integrate with new API, which means the scope is not only uber enabling, it's new API migration, which need more effort |
| 3 | Rule service -confirmation flow(group→rule→1. Lifecycle; 2. Orchestration) | 1. rule call lifecycle with action Affirmed, expect the lifecycle API is same 2. rule service publish event to orchestration complete user task expected a certain topic to publish | 1. Currently BAU only live the new API by business function level, e.g. Affirm action in auto netting flow is using new API, but in confirmation flow is using legacy API, which is only support SCBML. 2. There is complete user task topic for each workflow, but rule service doesn't know which flow to go |
| 4 | Manual Netting IRS auto Netting NDS auto Netting, etc. | 1. Netting provide 2 different APIs, UI manual netting, orchestration and scheduled job expected a certain API to call the backend service. 2. Expect only 1 lifecycle API to receive netting request, 2 APIs for same action is too complicated. | 1. The netting operation may triggered from multi client, then all netting clients need to identify which API to invoke, which is more complicated and maintenance effort is too large. 2. Uber implementation on lifecycle service can only use the new API |
| 5 | UI batch action to Lifecycle service directly non-transactional | 1. Expect a certain lifecycle API to call, otherwise UI need additional logic to determine which API to call by entity fmid 2. If the action need to publish message to workflow, need a certain topic to publish | 1. Uber implementation on lifecycle service can only use the new API 2. Need to confirm whether we have to keep two APIs, if so, we need to define the responsibility who should determine the correct API & topic to go. |
| 6 | SSI refresh(vostro refresh + nostro refresh) | 1. Expect a certain topic to publish the impact cashflows | 1. Not able to know the cashflow message type from SSI prospective, can only get the fmid, if check by fmid, then the historical data for EG, NP, SA need a one time migration, need confirmation on this. |
| 7 | Multi-exception handling/ Bulk exception handling | 1. UI need a certain API to call | 1. Orchestration will provide two APIs for UI, 1 is for EG, NP, SA, 1 is for others. UI is not able to know which API to call unless checking with FmId. |
| 8 | BAU live actions on new API 1. NetNew 2. Net 3. Affirmed 4. UnNet 5. RevertToQueued | 1. Require same behavior on old API and new API, e.g. NewNew action in old API lifecycle is responsible for publish new message to Process in topic, but in new API, lifecycle is not doing this, that need to be aligned. | 1. If all actions migrate to new API, domain service need to do the message publishing work which need more effort include failure retry etc. which need more effort. 2. If keep two APIs, domain service still need |

Summarize:

| | Issue Categories | Workaround & Solution | Disadvantages |
| --- | --- | --- | --- |
| 1 | Lifecycle new and old APIs exists at same time, domain service need to check which API to invoke, same logic everywhere. | 1. **Solution**: the check logic implement in lifecycle service and provide a new status update API for domain services, lifecycle determine which internal API to call | 1. The new API is only a proxy to cover old and new API, eventually should be removed, it is a tactical solution. and it is not a completely isolation |
| 2 | Workflow is not stable for Uber adoption, keep changing on new features | 1. **Solution**: Choose a stable version as code base and migrate all new changes before UAT. | 1. Under risk if any change missing to merge. 2. Regression won't cover the new flow with new data model |
| 3 | If domain service doesn't care about the message type then can't determine which API to call or which topic to publish | 1. **Solution**: lifecycle API add a flag to response, domain service add additional check which flow to go | 1. Tactical logic will exist everywhere and intrude business code(Add new flag to response). |
| 4 | UI to backend service which has two version API, need additional check | 1. **Solution1**: UI call different backend API by checking the fmid is in uber scope or not. 2. **Solution2**: Lifecycle provide a compatible API | 1. **Solution1, **Uber integration expected transparent to UI. Bring additional UI effort. 2. **Solution2**, the new API is only a proxy to cover old and new API, eventually should be removed, it is a tactical solution. and it is not a completely isolation |

### Uber Flow and Legacy Flow Isolation

### Why separate a new workflow?

1. Minimize the impact scope from orchestration change prospective.
2. Freedom degree to restructure workflow according to 2.0 design diagram.
3. Compared with supporting both SCBML and JSON format in 1 service, two service reduces the complexity.
4. Use 1 workflow means all existing API should support both SCBML and JSON even though we provide a new version, then all domain services API will be message type agnostic, regression scope is huge?

### Open Issues:

1. Single Cashflow operation from non-inbound flow, need to additional check which workflow to go, how to define the responsibility to do the judgement, such as: 1. UI request Proposal 1, 3.a 2. Trade confirmation flow Proposal 4 3. ~~LIEN flow(Murex is not in scope)~~
2. Batch operation across message type, need to additional check which workflow to go, how to define the responsibility to do the judgement, such as: 1. Non-transactional 1. (Reinsate, EarlyRelease)UI request Proposal 1, 3.b 2. (Release, Materialize) Scheduled job Proposal 5 3. SSI refresh Proposal 6 2. Transactional 1. Netting/Unnetting(UI, Scheduled job, orchestration) Proposal 2, Proposal 5 2. Splitting/Unsplitting(UI, Scheduled job, orchestration) Proposal 2, Proposal 5 3. Component status update
3. Lifecycle restructured API is not applied all actions, not clearly sure whether we can use new API for Uber implementation. Currently(after Aug 23th release) live actions are: 1. NetNew 2. Net 3. Affirmed 4. UnNet 5. RevertToQueued
4. RevertToQueued, NetNew action in new API will not publish message to process_in topic any more, BAU did the change and currently domain service need to publish itself.
5. Cashflow stamping, holding-check, cutoff calculation APIs should be kept same because workflow not change currently, need to rollback and disable the stamping from group service.

### Proposal

1. UI → Lifecycle: lifecycle responsible for publish to correct workflow
2. UI → Netting: UI need to check the select cashflow booking entity list, if uber scope need to call netting service V2 API.(Cashflow is uber scope but SCBML indicate it's historical data, resultant should be JSON)
3. UI → Orchestration: UI need to check the select cashflow booking entity list, if uber scope need to call netting service V2 API.(Cashflow is uber scope but SCBML indicate it's historical data, handling with SCBML or handling with JSON are both ok, but suggest to convert real time) 1. single multi-exception handling 2. bulk multi-exception handling
4. Trade confirmation flow(Group→Rule→1. Lifecycle; 2. Orchestration): lifecycle return with message type then rule can determine which flow to go
5. Scheduled job: Materialize, Release, AutoNetting - lifecycle responsible for publish to correct workflow;
6. SSI refresh(SSI → Orchestration): Orchestration provide sub flow in new service, consume the event and status update, then determine handle by itself or publish to legacy flow according to status update response.

### Upstream Delivery plan

- UAT ready prerequisite : - EDMI topic created start date: 2025-08-14 - TDSX Enable publisher

- Prod release: - TDSX release frequency - Quarterly - Once we are ready for UAT and planned release date, need to agree with upstream and plan a TDSX release date before RATAN.

### BAU all actions delivery plan

No plan. Need to agreement with Nick?