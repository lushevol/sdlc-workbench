## Key difference Comparison

| Functionalities | BCS/EG cash settlement | Strategic cash settlement |
| --- | --- | --- |
| Cashflow Golden Source | TDS3 | RATAN (Postgre SQL) |
| Cashflow Creation | FMRP STELLA | MUREX 2.11, FMRP STELLA, RATAN |
| Cashflow Lifecycle | FMRP STELLA | RATAN |
| Cashflow Materialization | FMRP STELLA | RATAN |
| Netting (CPN) | FMRP STELLA | RATAN |
| Fail/Reinstate | FMRP STELLA | RATAN |
| Products scope | BCS products + EG FX | CN IRS, CCS, Loan&Deposit, NDF |
| Exception handling | One by one on Exception blotter | All in one go on cashflow detail page |
| Function entitlement | Different tiles via different EMS2 entities, transition in progress to CN | Only 1 EMS2 entity (X_RATANONE), different tiles control via different subjects |

## Overall Design

## Workflow

## Service boundary

| Service | Responsibility | Functions provided to UI | Documentation |
| --- | --- | --- | --- |
| Murex adaptor | 1. Transformation from MXML to SCBML 2. Transformation to align the group management strategy. 3. CFI mapping maintenance | NA | [Ratan MxML->SCBML Adaptor - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Ratan+MxML-%3ESCBML+Adaptor) [CN Settlement - Murex2.11 Technical Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex2.11+Technical+Design) [CN Settlement - MxML mapping to SCBML - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+MxML+mapping+to+SCBML) |
| Cashflow Group Management Service | 1. Group the cashflow events from upstream, only publish to workflow when the whole group arrive 2. Manual force STP when group is not ready because of message lost 3. [Future scope]Non-economic change mapping handling 4. Cashflow status write back to upstream 5. Trade validation event consumption, STP the whole group in PTV 6. Trade confirmation event consumption, STP the cashflow stuck in CF blotter, auto close pending affirmation exception 7. Cashflow standardization, enrich the required information from surrounding systems. 8. Uber message consumption, batch cashflow processing in a single message. | 1. Group management data query 2. Force STP when leg missing case happened (rare case) 3. Cashflow resend if CF blotter missed the payment. | [Ratan processing on cashflow events - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Ratan+processing+on+cashflow+events) |
| Camunda workflow | 1. STP processing, orchestrate all the microservices 1. STP from upstream 2. Exception auto close 2. Maker/Checker APIs for those orchestration processing required, currently multiple exception handling, it need to orchestrate rule service and ssi service for exception fixing 3. Technical exception handling, move to tech fail status on the cashflow | 1. Multiple exception maker API 2. Multiple exception checker API | Please see the workflow as diagram below the table |
| Cashflow Lifecycle Service | 1. Cashflow data storage for processing (Write DB) 1. Cashflow persistence on STELLA/Murex messages 2. Cashflow creation base on request 3. Reversal and Rebook tagging on cashflows, which is for NSTP processing 2. Cashflow status machine for status movement 1. Single cashflow change 2. Batch cashflow change as a transaction 3. Support UI status movement without services orchestration 1. Hold/Unhold 2. Fail/Reinstate 3. Swift suppression/Undo Swift suppression 4. Cashflow suppression/Undo Cashflow suppression 5. Early materialization | 1. Hold/Unhold 2. Fail/Reinstate 3. Swift suppression/Undo Swift suppression 4. Cashflow suppression/Undo Cashflow suppression 5. Early materialization | [Status Machine - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Status+Machine) |
| Rule Service | 1. Rule management 1. Cashflow suppression 2. Swift suppression 3. Netting static 4. IRS checking 5. Profile limits 6. NSTP rules 2. Rule execution 3. Exception handling on NSTP exceptions | 1. Cashflow suppression rules configuration 2. Swift suppression rules configuration 3. Netting eligibility rules configuration 4. Profile limit configuration 5. NSTP rules configuration | [Ratan Rule Service Technical Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Ratan+Rule+Service+Technical+Design) |
| Netting Service | 1. Netting processing 1. component cashflows validation 2. resultant cashflow generation 2. Un-net process 1. all impacted cashflows validation 2. request to revert status 3. [Future] Split process 1. Threshold check 2. Calculation on the split cashflow generation 4. [Future] Auto netting | 1. Netting action 2. Un-net action | [Netting Service Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Netting+Service+Design) |
| SSI stamping service | 1. Vostro stamping 2. Nostro stamping 3. Exception generation + Handling 4. SSI update handling | NA | [FMRP - SSI Stamping Flow - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/FMRP+-+SSI+Stamping+Flow) |
| Query Service | 1. Event driven cashflow data storage for query purpose (Read DB) 1. Cashflow creation 2. Cashflow data update 2. API for UI to query data 3. GraphQL supported for cashflow details query, combining: 1. Cashflow details 2. Trade details 3. Exception details 4. Exception stashing data 5. SSI candidates (Vostro + Nostro) | 1. Cashflow blotter query 2. Cashflow blotter notification 3. Cashflow details query 4. External API to RATAN EOD and SSDR | [GraphQL Used For Front End In RATAN - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/GraphQL+Used+For+Front+End+In+RATAN) [GraphQL Proposal - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/GraphQL+Proposal) |
| Murex Batch Service | 1. Process Murex payments batch file 2. Process Murex pending fixing flag batch file | NA | |
| Static data service (Common) | Additionally support FX spot rates querying. | NA | |
| Trade service (Common) | Additionally consume Murex trade confirmation. | NA | |
| Stella Ambassador (Common) | Additionally support higher version STELLA API on strategic cashflow management | NA | |
| Message Bridge (Common) | Additional support for MQ. | NA | |
| FX utilization Service | 1. Persist UTIL cashflow to database 2. Consume fxu request message from Razor FXU to perform utilize action, and ack to razor FXU 3. EOD Auto Utilization, auto Pastdue. | NA | [FXU Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Technical+Design) |

## External Interfaces

MQ

| Source system | Target System | Purpose | Publish end | Consume end | Dev config | Prod config |
| --- | --- | --- | --- | --- | --- | --- |
| Murex | Ratan | 1. Cashflow publishing 2. Ack on released status | CF.MXG.RATAN.RQST | CF.MXG.RATAN.RQSTIN | Host 10.198.198.93 Port 8212 Channel UKMXGCLNTS2 Queue manager UKFM02S1 User ukmxgmq | Host Port 8212 Channel Queue manager User ukmxgmq |
| Ratan | Murex | 1. Ack on cashflow consuming 2. Released status | CF.RATAN.MXG.RESP | CF.RATAN.MXG.RESPIN |

Solace please refer to the ASRM, we are reusing the same connections with BAU.

## Table structure

| Service name | Description | Tables | Table purpose |
| --- | --- | --- | --- |
| ratan-cash-settlement-lms-service | | lms_message lms_outbox_events lms_raw_message lms_trade ratan_lms_scbml_history | this table used for storage message send status for downstream this table used for storage per event record in one cashflow this table used for storage lms service received message and sent out message this table used for storage trade information ratan_lms_scbml_history, this table won’t used any longer, will be removed |
| ratan-cash-settlement-netting-service | | t_cashflow t_request | maintain all cashflows information with the latest maintain all casfhflow update audit history |
| ratan-cash-settlement-orchestration | STP workflow base on camunda framework | ratan_cashflow_multiple_exception ratan_cashflow_user_task | Record all technical exceptions in STP workflow Record user task in STP workflow, like maker task & checker task |
| ratan-cash-settlement-query-service | | cashflow_data cashflow_data_history t_event | cashflow_data: record cashflow scbml cashflow_data_history : record cashflow_data_history t_event : record received event message from cashflow lifecycle service |
| ratan-cash-settlement-ssi-stamping-service | | cashflow_stamping cashflow_stamping_exception cashflow_stamping_legacy_exception cashflow_status_snapshot maker_checker_request raw_message stamped_nostro_account stamped_vostro_account stamping_outbox_events trade_stamping_message | cashflow_stamping: record cashflow stamping info cashflow_stamping_exception: record cashflow stamping exception cashflow_stamping_legacy_exception: record stamping exception reason cashflow_status_snapshot : record cashflow status_snapshot maker_checker_request: record maker checker request data raw_message : record cashflow scbml stamped_nostro_account: record cashflow nostro_account stamped_vostro_account: record cashflow vostro_account stamping_outbox_events: record received event trade_stamping_message: record trade stamping info |
| ratan-cash-settlement-group-management-service | | ratan_cashflow_group ratan_cashflow_group_history ratan_cashflow_group_message ratan_cashflow_group_message_history ratan_cashflow_mapping ratan_cashflow_mapping_history ratan_cashflow_rounding_config ratan_cashflow_status_sync_up_blocking_queue ratan_inbound_message ratan_trade ratan_trade_history | 1. All cashflow message with same trade id + major version should be treated as a cashflow group. 2. Cashflow group audit table. 3. Persist cashflow message after receive any cashflows from upstream, message can be delivered only after all message arrived in the same group. 4. Cashflow group message audit table |
| ratan-cashflow-lifecycle-service | The cashflow main service, provide the main business interface. Persist the cashflow information and status change. | lms_message | |
| ratan_cashflow_affirmation_status | Maintain all cashflow affirmation status |
| ratan_cashflow_cutoff_info | Maintain all cashflow cut-off date, involve queue/netting/ccy cut off |
| ratan_cashflow_holding_message | Persist the cashflows holding in ratan as the queued cut off date in future |
| ratan_cashflow_razor_stella_status_blocking_queue | The queue to manage STELLA status write back |
| ratan_cashflow_scbml_history | Persist all cashflows status and sub-status |
| ratan_cashflow_scbml_message | Record the latest message for each cashflow |
| ratan_cashflow_scheduler_job_record | Record the scheduler job impact cashflows and execution status triggered by Control-m |
| ratan_minor_version_history | Record the response and status from razor |
| ratan_stella_message_event_source | Persist the received cashflows from upstream |
| ratanone_cashflow_service__cqrs_cashflow_events | Record the event from cashflow like creation, amendment, ssi notification, sendToRazor, status update |
| razor_acknack_event_source | Record the acknowloge response from razor |
| razor_cashflow_status_event_source | Record the status update from downstream, like released, settled |
| ratan-exception-platform | | rep_exception rep_exception_history | 1. Persist all exceptions published by domain services. 2. Exception audit table for tracking the exception change history. |
| rantan_mxg_cashflow_adaptor | | mxg_cashflow_inbound | Record PayMent Info from murex |
| | | mxg_cashflow_history | Record PayMent Info history |
| | | mxg_cashflow_message | Record PayMent history message |
| | | static_data_cfi_code | Maintain CFI Code static data |
| | | mxg_cashflow_exception | Discarded |
| | | mxg_cashflow_group | Record Payment group |
| | | mxg_cashflow_group_message | Record Payment group Histories |
| ratan-cash-settlement-fx-utilization-service | | ratan_fx_cashflow_brief_info ratan_fx_cashflow_utilization_history ratan_fx_accounting_send_failed_info ratan_fx_utilization_response_failed_info | 1. fx cashflow main table 2. fx utilization audit table 3. fx publish accounting msg and fx utilization response failure table |

## Exception handling

[Exception Handling - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Exception+Handling)

## Aggregation