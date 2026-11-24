# Service Deployment Strategy

## Option-1 Maintain 1 profile with VIP

## Option-2 Two profiles for 2 clusters

| | Pros | Cons |
| --- | --- | --- |
| Option-1 | 1. Infra switch is transparent for domain applications 2. Only maintain 1 profile 3. Real Active-Passive model | 1. 6 servers for each cluster need 6 VIPs 2. Apps to infra connectivity is available to only 1 DC at same time, so switch step should be 1. Stop primary DC apps. 2. Check all primary DC services are down. 3. Switch VIPs. 4. Start backup DC apps. 5. Check all backup DC services are up. |
| Option-2 | 1. No additional VIPs required 2. Two DCs are totally isolated | 1. Need to maintain 2 profiles separately. 2. CD script needs to be revised to support 1 CD deploy 2 profiles. 3. Could be Active-Active, need to manual avoid message racing(MB startup should be restricted). |

# Kafka Fail-Over Solution

## Option-1 Self developed sync up tool

## Option-2 Mirror Maker 2

Mirror Maker 2 (MM2) is Kafka's built-in solution for replicating data between Kafka clusters. Built on Kafka Connect, it provides continuous, reliable replication for disaster recovery, data migration, and multi-datacenter architectures.

![](https://developers.redhat.com/sites/default/files/fig5-mm2-migration-simple.jpg)

![](https://developers.redhat.com/sites/default/files/fig8-topic-mm2-offset-sync_1.jpg)

**Reference: **

[KIP-382: MirrorMaker 2.0 - Apache Kafka - Apache Software Foundation](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/95650722/KIP-382+MirrorMaker+2.0)

[Kafka MirrorMaker 2: Complete Guide to Cluster Replication | KLogic](https://klogic.io/blog/kafka-mirrormaker2-guide/)

## Option-3 Real time recon between producer and consumer after DR

Step A: Only if DR happen, then to recon between key producer and consumer to see if there is anything missed.

**Topic Category**

| Category | Topic List |
| --- | --- |
| Level 1 | Cash_Settlement_Group_Message_Inbound tdsx_uber_message_json_inbound Cash_Settlement_Orchestration_Inbound Cash_Settlement_Orchestration_Process_In cash_settlement_cashflow_domain_events Cash_Settlement_Orchestration_Swift_Out Cash_Settlement_Mxg_Inbound Cash_Settlement_FXU_Request_In Cashflow_Realm_Process_Out Cash_Settlement_Swift_Process_Out Cash_Settlement_FXU_Ack Swift_MX_FMSGW_Out Cash_Settlement_EBBS_Process_Out_ID Settlement_Stamping_Internal_Ssi_Event_In_cn Settlement_Ssi_Notification_Event_In_RT_Decom |
| Level 2 | TDS3_Trade_Message_Process_In TDS3_Trade_Murex_Message_Process_In Cash_Settlement_Mxg_Group_Complete_Event Cash_Settlement_User_Task_Orchestration_In Cash_Settlement_Orchestration_Approval_Check Cash_Settlement_Orchestration_Hold_Check Cash_Settlement_Receiver_Ack_Nack_In Settlement_Stamping_Internal_Ssi_Event_In_cn Settlement_Ssi_Notification_Event_In_RT_Decom Cash_Settlement_EBBS_Ack_Nack |
| Level 3 | Cash_Settlement_Cashflow_Status_Response_In Cash_Settlement_Orchestration_Post_Holding_Check Cash_Settlement_OLA_Breaking_Exception_Record_In Cash_Settlement_Release_Response_Process_In Cash_Settlement_FXU_Accounting_Event Cash_Murex_Settlement_Batch_FIXING_Task Ratan-Mxg-Cashflow-Adaptor-Murex-Ack |
| Useless(exist bcoz of code reuse) | Mx_Mt_Payment_In_Internal Mx_Mt_Payment_In Swift_MX_FMSGW_Ack Cash_Murex_Settlement_Batch_Task_Next Cash_Murex_Settlement_Batch_Task Cash_Settlement_Ssi_Notify_Orchestration_In |

**Scenario Analysis**

**Scenario-1 Message persist by producer and consumer directly(Normal case)**

**Scenario-2 Message persist by producer and only trigger consumer process**

Step B: Trigger message replay to specific topic if there is any message identified.