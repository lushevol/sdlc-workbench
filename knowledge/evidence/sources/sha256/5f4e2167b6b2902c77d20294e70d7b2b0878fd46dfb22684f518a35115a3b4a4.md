1. **WIKI** : [Cashflow Events Control - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Events+Control)
2. **Topic：** | Topic | Cash_Settlement_Group_Message_Inbound（upstream-inbound.topic） | TDS3_Trade_Message_Process_In（tds3-trade-inbound） | TDS3_Trade_Murex_Message_Process_In（tds3-trade-murex-inbound） | | --- | --- | --- | --- | | cashflowinfo | 从scbml获取cashflowInfo businessEvent: New, Withdrawal countSeq:batchId_seq_count/seq_count | 从scbml获取TradeInfo 更新ratan_trade TradeValidatedEvent: 1. 更新所有的group by tradeId的isTradeValidated=true； 2. 获取PENDING_TRADE_VALIDATION的groups | 从scbml获取TradeInfo 更新ratan_trade TradeValidatedEvent: 1. 更新所有的group by tradeId的isTradeValidated=true； 2. 获取PENDING_TRADE_VALIDATION的groups | | event | MessageInboundEvent: build&save CashflowGroupMessage(ratan_cashflow_group_message) status=PENDING key fields: businessEvent: New, Withdrawal batchId:batchId/major_version Duplication check(CashflowGroupMessage): tradeId, majorVersion, batchId,businessVersion, cashflowId build&save CashflowGroup(ratan_cashflow_group) getCashflowGroup：batchId， tradeId， majorVersion status:PENDING isLocked = true（trade， <major_version） tradeId&major 有 PENDING, PENDING_TRADE_VALIDATION， 当前的group的status更新为PENDING_PRE_GROUP else PENDING_TRADE_VALIDATION group.isTradeValidated=true, 状态更新成ready groupGroupReadyEvent | | | | TradeValidatedEvent | // Should ignore the ERROR offset and trade validation update? if (groupMessageList.size() > cashflowGroupMessage.getCashflowCnt()) { log.info("All group message has been arrived already for group: {}, change the current message: {} status to ERROR.", cashflowGroup.getAggregateRootId(), cashflowGroupMessage.getAggregateRootId()); cashflowGroupMessage.changeToError(cashflowGroupMessageRepository); return; } | | | | | ![image-2025-10-28_16-29-1.png](attachments/image-2025-10-28_16-29-1.png) | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |

![image-2025-10-29_1-3-45.png](attachments/image-2025-10-29_1-3-45.png)

PENDING->
        ->小版本存在pending => group：status=PENDING_PRE_GROUP
        ->noPreviousGroupPending（PENDING, PENDING_TRADE_VALIDATION）& group：status=PENDING_PRE_GROUP & is_trade_validated=false->PENDING_TRADE_VALIDATION
        ->is_trade_validated=true => group：status=READY
        ->noPendingMessage =>group：status=COMPLETED
        READY,
        COMPLETED,
        PENDING_TRADE_VALIDATION,

topic(trade)
** 1.=> groups/trade is_trade_validated=true**
   => group:status=READY
   => publish GroupReadyEvent
        => !OFFSET： cashflowGroupMessage：status=END
        => send groupmessage to topic:Cash_Settlement_Orchestration_Inbound
        => noPendingMessage
           => groups:status=COMPLETED
           => unLockPrevious
           => publish GroupCompletedEvent
                => FXStatusWriteBackEventHandler ： cashflowGroupMessage：cashflowStatus=SUSPENDED=>
                => GroupCompletedEventHandler ：
                    => find next UN-COMPLETED groups
                    => NoPreviousGroupPending&PENDING_PRE_GROUP.equals(nextGroup.getStatus())
                    =>enablePendingPreGroup
                       ** =>groups/trade is_trade_validated=true**
                        =>group：status=PENDING_TRADE_VALIDATION

![image-2025-10-29_21-40-59.png](attachments/image-2025-10-29_21-40-59.png)![image-2025-10-29_21-41-29.png](attachments/image-2025-10-29_21-41-29.png)

group：

![image-2025-10-29_21-46-24.png](attachments/image-2025-10-29_21-46-24.png)

![image-2025-10-29_21-45-34.png](attachments/image-2025-10-29_21-45-34.png)