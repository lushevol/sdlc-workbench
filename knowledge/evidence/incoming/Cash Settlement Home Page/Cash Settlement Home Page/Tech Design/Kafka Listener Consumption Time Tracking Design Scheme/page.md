story: [Story 11472308: [0608_Proposed] RATAN business monitor--central monitoring - Boards](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11472308)

design: [Ratan Central Monitoring - PSS Requirement - 2026 Phase 1 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+Central+Monitoring+-+PSS+Requirement+-+2026+Phase+1)

1，Backgroud

2，Analysis

2.1，group service

| topic name | Business | source | comment |
| --- | --- | --- | --- |
| Cash_Settlement_Group_Message_Inbound | scbml cashflow | 1, MB 2, adapor service(when message from murex, change to scbml) | CashflowInboundListener scbml |
| TDS3_Trade_Message_Process_In | stell trade | | TDS3DefaultTradeInboundListener |
| TDS3_Trade_Murex_Message_Process_In | murex trade | | TDS3MurexTradeInboundListener |
| cash_settlement_cashflow_domain_events | | | CashflowDomainEventListener |
| Cash_Settlement_Cashflow_Status_Response_In | stell ack | | CashflowStatusSyncUpAckListener |
| tdsx_uber_message_json_inbound | | MB | TdsxUberMessageListener uber |
| Cash_Settlement_Mxg_Group_Complete_Event | murex , adaptor service | | MxgGroupCompleteListener |

3，Design

| **Zero Intrusion** | No modification to any existing Listener source code |
| --- | --- |

| **Full Coverage** | One codebase automatically applies to all existing/future Listeners |
| --- | --- |

| **Extensible** | Tracking string format, Header Key, and output method can all be independently extended |
| --- | --- |

| **Testable** | Each component has a single responsibility, facilitating unit testing |
| --- | --- |

| **Disabled** | Interceptor activation can be controlled via configuration switches, without affecting business logic |
| --- | --- |

Why Choose RecordInterceptor?

| Solution | Advantages | Disadvantages |

| **Spring Kafka RecordInterceptor** ✅ | Native Spring support; no need to modify any Listeners; always obtains the complete `ConsumerRecord` (including headers); automatically adapts to all new Listeners | Requires Spring Kafka 2.3+ |

| Spring AOP Aspect | Framework independent | Some Listener method signatures lack the `ConsumerRecord` parameter, making it impossible to directly retrieve headers; requires writing pointcuts for each signature, resulting in high maintenance costs |

| Kafka's native ConsumerInterceptor | Decoupled from the framework | Cumbersome registration; not managed by the Spring container; cannot inject Spring Beans |

| Modifying each Listener | Intuitive | Highly intrusive; requires adding logic every time a new Listener is added; violates the Open/Closed Principle |

**Conclusion:** `RecordInterceptor` is the best choice for Spring Kafka. The extension point, designed specifically for this scenario, is non-intrusive, fully automated, and easy to test, making it the preferred solution.

ConsumerRecord arrives -->

* add KafkaConsumerTimingInterceptor  implements RecordInterceptor<K,V>         (Transmit the original record (without modification))*

*                  1→ Extract trackingId from header*

*                  2→ Building log trace strings  →    .#|#.ms_in#ratan-cash-settlement-group-management-service_**businessDescription**#${trackingId}#Timer#end#1750063879234*

*                  3→ [log.info](http://log.info)(trace string)*

Listener.handleMessage() / onMessage() / mxgGroupComplete() / CashflowInboundListener / TdsxUberMessageListener / ...