# Technical Release Plan - Release date Nov. 15th

| Key Item Description | Spoker | Check List | Owner | Status |
| --- | --- | --- | --- | --- |
| EDMI engagement | @Bandi Anil Kumar Reddy | 1. Set up the solace queue (Nov. 15th) 1. uber flow 2. FXU flow(dummy request, dummy ack back) | @Fengke Wu | @Gopi scheduled a call, whether need PT? |
| Ratan deploy the message bridge | @Xinmiao Huang @Yonghua Li | 1. Set up new flow config to DB(uber flow, flow filter for only EG, NP, SA), shouldn't filter out scbml message which is EG, NP, SA 2. Deploy message bridge, check the connectivity to the new Queue is good | @Yonghua Li | |
| TDSX engagement to enable the publisher | @Rui Li | 1. Enable the publisher 2. Book 3 pilot trade(EG, NP, SA each has one) to Ratan | | |
| Ratan verification | @Xinmiao Huang | 1. Check the target topic "tdsx_uber_message_json_inbound" has such 3 uber messages 2. increase the topic partition from 6 to (same as group_inbound) | @Xinmiao Huang | |

# Pre-Business Release Checklist（NFR, Compatibility, Idempotence, Flexibility etc.）

| Item description | Sub Item | Owner | Status |
| --- | --- | --- | --- |
| No impact on SCBML entities(full regression testing) | | | |
| PT report(STP, Net and UnNet base on SCBML only, SCBML and Json, Json only) | | | |
| Invalid Uber message inbound(with errors), group service is able to filter it out | TDSXUberMessage.errors | | Waiting for @Prashanth Kalkunte Suresh Email: RE: UBER Adoption - Outstanding Issues |
| Uber schema version check for upgrade **Artifactory link**: [Index of maven-release/com/scb/sabre/fmrep/tdsx-proto-schema](https://artifactory.global.standardchartered.com/artifactory/maven-release/com/scb/sabre/fmrep/tdsx-proto-schema/) | tdsx.proto.version: tdsx prod: V7.10 (v7.10-RELEASE-20250822.2-3a3c47dc) foundation: v7.13-RELEASE-20250830.1-9e9be56c message-bridge: v7.13-RELEASE-20250830.1-9e9be56c | | |
| Schema upgrade by Upstream only, downstream is able to process successfully | 1. upstream add new attribute | | |
| | 2. Upstream remove field | | |
| | 3. Upstream change field type | | |
| | 4. Upstream change Array to single Value | | |
| | 5. Upstream change Single Value to Array | | |
| Schema upgrade by Ratan foundation, lifecycle service upgrade is required, other services upgrade is on demand. Domain services don't upgrade schema if it doesn't care expect no field missing. | 1. Add new field to schema 2. Remove field from schema 3. change the field type from schema | | |
| Same cashflow inbound in Uber but has been processed in SCBML type, uber cashflow should be filtered out, others in same group | | | Verified |
| ~~Same cashflow already been processed by Uber, then scbml inbound, there is no impact.~~ | | | |
| DB repo script review | 1. netting 2. orchestration(should in flyway) 3. message-bridge(only black list filter ) 4. static | @Chen Yang @Yonghua Li @Quill Li | |
| ~~property change~~ | ? | | |
| | | | |

# Business Release Plan - Release date Nov. 22nd

| Key Item Description | Spoker | Check List | Owner | Status |
| --- | --- | --- | --- | --- |
| check whether any messages stuck in EDMI SCBML and uber flow related topic | | | | |
| deploy db-repo | @Yonghua Li @Xinmiao Huang | 1. Enable the scbml filter rule, check the from the log to confirm no errors. 1. cashflow scbml should exclude EG NP SA 2. trade scbml should exclude EG NP SA 2. Mock scbml to verify the filter works.(EG, NP, SA scbml will be fitlered, others such as UK can be processed.) | @Yonghua Li | |
| Ratan deploy all services | @Xinmiao Huang | | | |
| restart message-bridge | All dev | | | |
| Check the lived EG, NP, SA cashflows | | 1. Keep monitoring whether the payments can be stp. 2. Ensure whether the cross message type net/unnet will happen | | |
| Ratan verification | All dev | | | |