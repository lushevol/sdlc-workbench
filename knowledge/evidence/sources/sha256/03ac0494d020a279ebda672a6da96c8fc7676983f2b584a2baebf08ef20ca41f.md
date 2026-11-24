# Background

Currently we are seeing MB is managing first level filter and routing post consumption on Solace queues, the purpose was to make the filter at the entrance of RATAN platform.

However it was mentioned MB should be a technical integration layer for routing but not managing any business logic filters but business domain service should do.

Below are the ones with filters configured for MB routes at current stage.

# Plan

| | MB filter | MB remove filter |
| --- | --- | --- |
| PROs | Filter centrally managed Low pressure on domain service Less log space Less Kafka space | Clear domain service boundary |
| CONs | MB maintain business logic | Higher pressure on domain service for additional filter, such as for BCS settlement flow, 99% of volume will be filtered More log space required More kafka space required |
| Changes required | NA | 1. Message Bridge to remove the Filter logic 1. Pass through on consumption 2. Headers carrier 2. Target topics need to be combined: 1. 1. 4, TDS3_All_Trade_Message_Process_In,Confirmation_Orchestration_Process_In,TDS3_Trade_Murex_Message_Process_In,TDS3_Trade_Message_Process_In 2. 2, Settlement_Orchestration_Process_In, Cash_Settlement_Group_Message_Inbound 3. 2, Settlement_Ssi_Notification_Event_In, Settlement_Ssi_Notification_Event_In_RT_Decom 4. 2, Settlement_Cashflow_Status_In, Cash_Settlement_Cashflow_Status_In 5. 2, Settlement_Receiver_Ack_Nack_In, Cash_Settlement_Receiver_Ack_Nack_In 3. Additional filters: 1. Integrate with the new config solution ?? 2. A SDK to be provided to each service to filter on 1. SCBML 2. UBER/JSON 3. Header 3. Group Service 1. Cashflow: consuming to new topic & Filter out BCS 2. Trade: self routing logic on sender 4. Trade service: self routing logic on sender & Filter on capture system 5. Trade control service: Filter on capture system 6. LMS Service: build filter on publishing based on BIC 7. BCS Cashflow Service: 1. Build filter on consuming cashflow scbml 2. build filter on publishing based on BIC for LMS |
| Conclusion | |