ne

# Upstream connectivity

**E2E env:**

[SFMRP Environment - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/SFMRP+Environment)

[Stella Environments - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Stella+Environments)

**EDMI kibana**: password reach out to @Xinmiao Huang  or @Yonghua Li

[https://uklvadapp400.uk.standardchartered.com:5601/](https://uklvadapp400.uk.standardchartered.com:5601/)

**EDMI Dashboard: **password reach out to @Xinmiao Huang or @Yonghua Li

[http://10.198.38.42:3000/d/000000021/queue-level-basic-stats?var-timeRes=3m&orgId=1&from=now-1h&to=now&timezone=browser&var-router=ukxpiusol03a&var-vpn=FMEDMI2_GDCW_DEV&var-queue=q-51358-ratanone-uber-msg](http://10.198.38.42:3000/d/000000021/queue-level-basic-stats?var-timeRes=3m&orgId=1&from=now-1h&to=now&timezone=browser&var-router=ukxpiusol03a&var-vpn=FMEDMI2_GDCW_DEV&var-queue=q-51358-ratanone-uber-msg)

| Ratan Env | VPN | Blade | TDS3 index |
| --- | --- | --- | --- |
| DEV | QA2 | **Dev3** | sit |
| UAT4 | QA1 | **Dev7: [Markets](https://dev-dev7-dtp.apps.dtp-np.ocp.standardchartered.com/)** | fmrp1 |

# Service Metrics

| | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |
| | | | | | | | | | | |

# Workflow API Integration

| | Old URL | New URL | |
| --- | --- | --- | --- |
| 51358-ratan-cashflow-lifecycle-service @Xinmiao Huang | [http://ratan-cashflow-lifecycle-service/v1/ratan/cashflow/query](http://ratan-cashflow-lifecycle-service/v1/ratan/cashflow/query) | Keep Same | NA, lifecycle need enhance |
| [http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/lifecycle/update/status](http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/lifecycle/update/status) [http://ratan-cashflow-lifecycle-service](http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/lifecycle/update/status)/v2/ratan/lifecycle/update/status/batch/transactional [http://ratan-cashflow-lifecycle-service/v1/ratan/cashflow/user/status/update](http://ratan-cashflow-lifecycle-service/v1/ratan/cashflow/user/status/update) | /v2/ratan/camunda/lifecycle/status/move | Need confirm(lifecycle will response for the publishing work when joint debugging until workflow complete impmentation): 1. User action such as ResendToRazor, ReGenerateSwift, EarlyRelease, lifecycle will not do any data publishing except domain event. |
| [http://ratan-cashflow-lifecycle-service/v1/ratan/lifecycle/update/status](http://ratan-cashflow-lifecycle-service/v1/ratan/lifecycle/update/status) | /v2/ratan/camunda/lifecycle/status/move | Consolidate this to the only API for Camunda request. |
| ~~[http://ratan-cashflow-lifecycle-service/v1/ratan/lifecycle/update/status/batch](http://ratan-cashflow-lifecycle-service/v1/ratan/lifecycle/update/status/batch)~~ | Removed | |
| [http://ratan-cashflow-lifecycle-service/v1/cashflow/holding/disable](http://ratan-cashflow-lifecycle-service/v1/cashflow/holding/disable) | Keep same | NA |
| [http://ratan-cashflow-lifecycle-service/ratan/camunda/cashflow/preCheck](http://ratan-cashflow-lifecycle-service/ratan/camunda/cashflow/preCheck) | /v2/ratan/camunda/cashflow/preCheck | Need confirm: 1. Do not calculate cutoff in this API.(Currently do) 2. Do not auto materialize in this API.(Already not) 3. Do not publish message to “process_in” topic() 4. Should do mandatory fields check(FAILED) and data persistence if validation pass. |
| ~~[http://ratan-cashflow-lifecycle-service/v1/cashflow/cutoffs/calculate](http://ratan-cashflow-lifecycle-service/v1/cashflow/cutoffs/calculate)~~ | Removed | |
| ~~[http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/lifecycle/msgEventCheck](http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/lifecycle/msgEventCheck)~~ | Removed | |
| [http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/cashflow/stamp](http://ratan-cashflow-lifecycle-service/v1/ratan/camunda/cashflow/stamp) | /v2/ratan/camunda/cashflow/stamp | Need confirm: 1. Stamp should happen if any mandatory fields are missing. 2. Result should indicate whether still mandatory fields missing. 3. If still mandatory missing, workflow update cashflow with Techfail. |
| [http://ratan-cashflow-lifecycle-service/v1/cashflow/camunda/holding-check](http://ratan-cashflow-lifecycle-service/v1/cashflow/camunda/holding-check) | /v1/cashflow/camunda/holding | Need confirm: 1. Workflow to check if message can be released or not. 2. If release, call sub flow directly. 3. If not release, call lifecycle to save a holding record. |
| | [http://ratan-cashflow-lifecycle-service/v2/ratan/lifecycle/update/status/batch/transactional](http://ratan-cashflow-lifecycle-service/v2/ratan/lifecycle/update/status/batch/transactional) | `/v2/ratan/cashflow/init/move/status` | Used by Netting Service |
| | | | |
| 51358-ratan-rule-service @Chongxuan Li | ~~[http://ratan-rule-service/v1/nstpException/batchClose](http://ratan-rule-service/v1/nstpException/batchClose)~~ | Removed | |
| [http://ratan-rule-service/v1/nstpException/close](http://ratan-rule-service/v1/nstpException/close) | Keep Same | |
| [http://ratan-rule-service/v1/suppressionRule/check](http://ratan-rule-service/v1/suppressionRule/check) | Keep Same | |
| [http://ratan-rule-service/v1/swiftSuppressionRule/check](http://ratan-rule-service/v1/swiftSuppressionRule/check) | Keep Same | |
| [http://ratan-rule-service/v1/netting/rules/checkIrsRule](http://ratan-rule-service/v1/netting/rules/checkIrsRule) | Keep Same | |
| [http://ratan-rule-service/v1/netting/rules/checkNettingRule](http://ratan-rule-service/v1/netting/rules/checkNettingRule) | Keep Same | |
| [http://ratan-rule-service/v1/nstpRule/check](http://ratan-rule-service/v1/nstpRule/check) | Keep Same | |
| | | | |
| 51358-ratan-cash-settlement-ssi-stamping-service @Quill Li | ~~[http://ratan-cash-settlement-ssi-stamping-service/v1/stamping/cashflow/exception/batchClose](http://ratan-cash-settlement-ssi-stamping-service/v1/stamping/cashflow/exception/batchClose)~~ | Keep Same | |
| [http://ratan-cash-settlement-ssi-stamping-service/v1/stamping/cashflow/exception/close](http://ratan-cash-settlement-ssi-stamping-service/v1/stamping/cashflow/exception/close) | /v2/stamping/cashflow/exception/close | |
| [http://ratan-cash-settlement-ssi-stamping-service/v1/stamping/cashflow/enrich](http://ratan-cash-settlement-ssi-stamping-service/v1/stamping/cashflow/enrich) | /v2/stamping/cashflow/accounting/enrich | |
| | | | |
| 51358-ratan-cash-settlement-netting-service @Fengke Wu | [http://ratan-cash-settlement-netting-service/v1/netting/camunda/autoUnNet](http://ratan-cash-settlement-netting-service/v1/netting/camunda/autoUnNet) | Keep Same | |
| [http://ratan-cash-settlement-netting-service/v1/netting/camunda/checkPaymentDateForIRS](http://ratan-cash-settlement-netting-service/v1/netting/camunda/checkPaymentDateForIRS) | Keep Same | |
| [http://ratan-cash-settlement-netting-service/v1/netting/camunda/netForIRS](http://ratan-cash-settlement-netting-service/v1/netting/camunda/netForIRS) | Keep Same | |
| [http://ratan-cash-settlement-netting-service/v1/netting/camunda/checkPaymentDateForIRS](http://ratan-cash-settlement-netting-service/v1/netting/camunda/checkPaymentDateForIRS) | Keep Same | |
| [http://ratan-cash-settlement-netting-service/v1/netting/camunda/netForIRS](http://ratan-cash-settlement-netting-service/v1/netting/camunda/netForIRS) | Keep Same | |
| 51358-mfe-cashflow-blotter @Guiling Wang | /v1/ratan/cashflow/user/status/update | /v2/ratan/cashflow/move/status/user | |

# Schema Change use cases

| Case No. | Flow | Data Model | Case Description | Downstream Behavior | Downstream upgrade required | Core Logic |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | TDSX → Ratan | Proto Buffer → JSON | Upstream(TDSX) **add **new attribute "testField" and upgrade schema V2, downstream(Ratan) still use schema V1 | miss information in V1 processing no exceptions | If field is required then yes, otherwise nice to have | TDSXUberMessage tdsxUberMessage = TDSXUberMessage.parseFrom(byteArr); // Convert proto object to JSON String json = ProtobufUtils.toJson(tdsxUberMessage); |
| 2 | Upstream(TDSX) **remove **attribute "Netting_Id" and upgrade schema to V2, downstream(Ratan) still use schema V1 | upstream will not send this information no exceptions | No need |
| 3 | Upstream(TDSX) **change **attribute **type **from **String **to **Integer** and upgrade schema to V2, downstream(Ratan) still use schema V1 | miss information in V1 processing no exceptions | If field is required then yes, otherwise nice to have |
| 4 | Upstream(TDSX) **change **attribute **type **from **Integer **to **String **and upgrade schema to V2, downstream(Ratan) still use schema V1 | miss information in V1 processing Int value will change to 0(default) | If field is required then yes, otherwise nice to have |
| 5 | Upstream(TDSX) **change **attribute **type **from **Array **to **Single **and upgrade schema to V2, downstream(Ratan) still use schema V1 | No information loss, old schema array size is always 1 | No need |
| 6 | Upstream(TDSX) **change **attribute **type **from **Single **to **Array **and upgrade schema to V2, downstream(Ratan) still use schema V1 | Might have information loss, if array size greater than 1, only the last element will be picked no exceptions | If field is required then yes, otherwise nice to have |
| | Upgrade principal | **Only need to upgrade if any required fields change** |
| 7 | Ratan → Ratan | JSON → Proto Object → JSON | Upstream(Ratan domain client/producer) **add **new attribute "testField" and upgrade schema V2, downstream(Ratan domain server/consumer) still use schema V1 | miss information in V1 processing no exceptions | If field is required then yes, otherwise nice to have | Cashflow cashflowV1 = ProtobufUtils.toProtobuf(json, Cashflow.class); //... business handling String jsonV1 = ProtobufUtils.toJson(cashflowV1); |
| 8 | | | Upstream(Ratan domain client/producer) **remove **attribute "Netting_Id" and upgrade schema to V2, downstream(Ratan domain server/consumer) still use schema V1 | downstream will not send this information no exceptions | No need |
| 9 | | | Upstream(Ratan domain client/producer) **change **attribute **type **from **String **to **Integer** and upgrade schema to V2, downstream(Ratan domain server/consumer) still use schema V1 | No information loss | No need |
| 10 | | | Upstream(Ratan domain client/producer) **change **attribute **type **from **Integer **to **String **and upgrade schema to V2, downstream(Ratan domain server/consumer) still use schema V1 | miss information in V1 processing no exceptions | If field is required then yes, otherwise nice to have |
| 11 | | | Upstream(Ratan domain client/producer) **change **attribute **type **from **Array **to **Single **and upgrade schema to V2, downstream(Ratan domain server/consumer) still use schema V1 | No information loss, old schema array size is always 1 | No need |
| 12 | | | Upstream(Ratan domain client/producer) **change **attribute **type **from **Single **to **Array **and upgrade schema to V2, downstream(Ratan domain server/consumer) still use schema V1 | If array size is 1, then no information loss. else if greater than 1, has exception: Array must have size 1, but has size 2 | Required |
| | Upgrade pirncipal | **Group management service, lifecycle service upgrade are required for any schema change, others are on demand** |

# Test Cases

## Business case overview:

~~Case 1 Cashflow Pending Another Leg, The other one inbound and IRS Netting ~~

Case 2.1 Maker checker with MISSING_VOSTRO_ERRO and Pending Affirmation Exception, Early Release

1. holding check api issue
2. UI display issue (query service)
3. maker submit done but still can edit.

Case 2.2 Maker checker with MISSING_VOSTRO_ERRO and Pending Affirmation Exception, auto release

1. holding check api issue
2. UI display issue (query service)
3. maker submit done but still can edit.

Case 3 Bilateral netting

1. NetNew not publish to process in

Case 4 Manual UnNetting

C06810141006,C06810141007,N00000062632

1. query service component cashflow query empty result.

Case 5.1 Auto UnNetting - withdrawal inbound on netting resultant not post released

C06810141006,C06810141007,N00000062632

Case 5.2 Withdrawal inbound on netting resultant post released

C16810141024,C16810141023,N00000062638

Case 5.3 withdrawal inbound before new

Case 6 Cashflow Suppress/Manual Unsuppress

1. Unsuppress not publish to processs in

Case 7 Swift Suppress/Manual swift Unsuppress

1. Unsuppress not publish to processs in
2. pass value date accounting not sent UI not display (retest: ED6810140001)

Case 8 Manual Fail - orchestration

1. orchestration status update api need change

Case 9 Trade Validation Flow

Case 10 Trade Confirmation Flow

Case 11 SSI Refresh

Case 12 Materialize / Release Job

Case 13 bulk process - bulk exception handling

Case 14 Adhoc SSI

Case 15 Undo?

Case 16 UI Notification

Case 17 bulk manual operations

- [x] Materialize - Failed, Lifecycle need to know whether need to publish process-in
- [x] ReInstate
- [x] SettleAsGross
- [x] ReplayStatusWriteBack
- [x] ~~ResendToRazor~~
- [x] EarlyRelease
- [x] ManualAffirmed
- [x] Comment
- [x] ReGenerateSwift

Case 18 Net cross different message type.

## Blockers overview:

1. Separate flow has risks, the new workflow has same APIs, topics, how do the clients integrate with different orchestration? Need to confirm the principal and responsibility.
2. Uber adoption has to be implemented by all actions migrated to the restructured API.
3. The difference behavior between restructured API and legacy API.
4. Environment allocation for integration testing efficiency.

## Test details:

### Case 1: Cashflow Pending Another Leg, The other one inbound and IRS Netting

#### Sample Msg:

#### Test Steps:

| Step | | expected | Cashflow Id | Sample Message |
| --- | --- | --- | --- | --- |
| 1 | Publish Json to Cash_Settlement_Orchestration_Inbound_Uber_1 | WAITING + Pending Operator + Pending Another Leg | CH6800724451 | |
| 2. | Publish another Json with same trade id, they will be netted automatically | NETTED + NA + NA NETTED + NA + NA | CH6800724450(1afb0b65-7a44-11f0-b984-005056acac40) CH6800724451(1afb0b65-7a44-11f0-b984-005056acac40) N00000003845 | |
| 3 | Check netting resultant auto settled | SETTLED + NA + NA | N00000003845 | |

#### Evidence:

![image-2025-8-18_11-28-1.png](attachments/image-2025-8-18_11-28-1.png)

![image-2025-8-18_11-28-33.png](attachments/image-2025-8-18_11-28-33.png)

#### Critical Issue:

**"NetNew" message need to manual publish to Kafka topic which has gap.**

### Case 2 Maker checker with MISSING_VOSTRO_ERRO and Pending Affirmation Exception, Early Release

#### Sample Msg:

#### Test Steps:

| Step | Description | expected | Cashflow Id |
| --- | --- | --- | --- |
| 1 | Cashflow Inbound and hit SSI and NSTP rule | WAITING + Pending Exception + Pending Operator | C06810144246 |
| 2. | Maker submit | WAITING + Pending Exception + Pending Verification | C06810144246 |
| 3 | Checker Reject | WAITING + Pending Exception + Pending Operator | C06810144246 |

#### Evidence:

![image-2025-8-21_17-10-42.png](attachments/image-2025-8-21_17-10-42.png)

![image-2025-8-21_17-11-58.png](attachments/image-2025-8-21_17-11-58.png)

#### Critical Issue:

**Swift service call lifecycle legacy API which is not uber supported, need to call a certain lifecycle API.**

### Case 3 Bilateral netting

#### Critical Issue:

**UI is calling old netting API which is only support SCBML, need to call a certain Netting API.**

### Case 4 Manual UnNetting

#### Critical Issue:

**UI is calling old netting API which is only support SCBML, need to call a certain UnNetting API.**

### Case 5 Auto UnNetting - withdrawal inbound on netting resultant not post released

### Case 6 Cashflow Suppress/Manual Unsuppress

### Case 7 Swift Suppress/Manual Unsuppress

### Case 8 Manual Fail/Reinstate

### Case 9 Trade Validation Flow

Trade Id: CH6672555548

Sample message

![image-2025-9-4_14-4-20.png](attachments/image-2025-9-4_14-4-20.png)

![image-2025-9-4_14-14-50.png](attachments/image-2025-9-4_14-14-50.png)

## Action List

| Cashflow Action | Domain Client/UI | API provider | Comments |
| --- | --- | --- | --- |
| Comment | UI | lifecycle | |
| EarlyRelease | UI | lifecycle | |
| Hold | UI | lifecycle | |
| UnHold | UI | lifecycle | |
| ReGenerateSwift | UI | lifecycle | |
| ReInstate | UI | lifecycle | |
| ReplayStatusWriteBack | UI | lifecycle | |
| ResendToRazor | UI | lifecycle | |
| ManualAffirmed | UI | lifecycle | |
| ManualSuppress | UI | lifecycle | |
| ManualSwiftSuppress | UI | lifecycle | |
| ManualSwiftUnSuppress | UI | lifecycle | |
| ManualUnSuppress | UI | lifecycle | |
| Materialize | UI | lifecycle | Early materialize Auto materialize |
| SettleAsGross | UI | lifecycle | |
| Submit | UI | orchestration | |
| ApproveOnlyMaker | UI | orchestration | |
| Approve | UI | orchestration | Suppress, Unsuppress verify Multi exception approve |
| Reject | UI | orchestration | |
| Fail | UI | ?? | ?? |
| Net | UI netting | Netting | |
| UnNet | UI netting | Netting | |
| GenerateSwift | orchestration | | |
| CashflowStamped | orchestration | | |
| IsNettingEligible | orchestration | | |
| IsNstp | orchestration | | |
| IsNstpChecker | orchestration | | |
| NetNew | netting | | |
| New | lifecycle | | |
| NostroStamped | ssi stamping | | |
| PaymentDateUpdate | rule service | | |
| Release | swift lifecycle | | |
| RevertToQueued | orchestration group | | |
| SentToRazor | orchestration | | |
| Settle | swift lifecycle | | |
| SsiStamped | ssi stamping | | |
| Suppress | orchestration | | |
| SwiftSuppress | orchestration | | |
| SwiftUpdate | swift | | |
| TechFail | orchestration lifecycle | | |
| ValidateDirect | orchestration | | |
| VostroStamped | ssi stamping | | |
| WaitingAnotherLeg | netting | | |
| Withdrawal | lifecycle | | |
| AccountingUpdate | accounting service | | |
| Affirmed | rule netting | | |

## Open Items

| | | | |
| --- | --- | --- | --- |
| Q1 | How to handle with below topic: Cash_Settlement_Ssi_Notify_Orchestration_In Cash_Settlement_User_Task_Orchestration_In | | |
| Q2 | RevertToQueued(Group, orchestration, auto-netting?), Reinstate(UI) action who publish to process in, uber flow or legacy flow? | | |
| Q3 | UI need to call new flow and new flow will route SCBML to old flow？ then how to cover transactional operation? e.g. manual netting how to deal with the transactional and API? | | |
| Q4 | query service specific logic to handle domain events? | | |
| Q5 | batch job scan data, how to determine which flow to go? e.g. materialize, release | | |
| Q6 | ![image-2025-9-4_14-13-20.png](attachments/image-2025-9-4_14-13-20.png) | | |