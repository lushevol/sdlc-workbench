# **Introduction**

## **Background**

As a distributed system with microservice architecture, RATAN is serving Cash Settlement, Trade Control, BCS settlement flow with high concurrency and varies actions/events from cashflow and trade level.

Lock mechanism is required to guarantee no conflict of resource write operation.

| Time | Milestone | Lock evolving |
| --- | --- | --- |
| **2020** | RATAN TRF | No Lock built, no concurrency processing on same resource |
| **2021** | RATAN BCS Cash Settlement | Complicated settlement processing onboarded, and high concurrency appeared for different processing on same resource (cashflow), conflict occurred during processing. Concurrent business cases: 1. Cashflow workflow processing STP flow 2. User manual action for SI Exception handling 3. User netting/unnet action Issues: 1. Payments got released even the netting happened 2. ABA issue, maker A's input may overwrite B's. 3. Exception replay twice may lead to unnecessary re-processing Distributed lock implemented by Redis:** [RATAN ONE Distributed Lock on resource - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+ONE+Distributed+Lock+on+resource)** |
| **2023** | Strategic Cash Settlement for China | NA |
| **2024** | Strategic Cash Settlement for SG, MY, IN, AG, UK | Issues found as Section 1.2, several resolved |
| **2025** | Lock redesign started for resolving current issues | |

## **Problem Statement**

| | Type | Issue | Cases | Details |
| --- | --- | --- | --- | --- |
| 1 | **Issue** ** ** | Async processing caused race condition. Event driven processing carries re-entrance lock id. | Early Release by Users | Payment failed to be released, workaround is to "Re-Generate Swift" 1. (Process A) Lifecycle lock cashflow id 2. (Process A) Publish cashflow to workflow for releasing with lock process id 3. (Process B) Orchestration check the lock with lock process id, lock valid 4. (Process A) Released the lock 5. (Process B) Orchestration re-entrant the lock and extend the lock, which brought the lock back to live 6. (Process B) Orchestration release lock but failed because of owner is Lifecycle 7. Lock can only be expire with the setup TTL, but Swift service cannot release the payment as lock never released within the time window |
| Group handling messages from murex adaptor 1. 1. Payments 2. Force cancellation | Error logs for optimized lock on postgre SQL. 1. (Process A) Adaptor lock trade id 2. (Process A) Adaptor publish payment to Group Service with lock process id 3. (Process B) Adaptor publish force cancellation to Group Service with lock process id 4. (Process B) Group Service consume payments , re-entrant the lock and try to complete group 5. (Process C) Group Service consume cancellation, re-entrant the lock and try to complete group, but failed because of optimization lock on DB 6. (Process A) Adaptor Released the lock 7. (Process B&C) Group Service release lock but failed because of owner is Adaptor |
| 2 | **Issue** | No proper TTL control Lock expired before processing done | 1. Affirmation exception auto close, expected to be done in 2 seconds, which will block the high value exception close handling, but actually not because the lock expired in 2 seconds, another request acquired the lock which caused payment tech failure. Ideally second request would be dropped if the first one completed processing. | |
| 3 | **Issue** | Atomic on batch processing | Batch locking, if any component lock failure, the locked ones won't be released | 1. User net 1000 payments 2. Netting service try locking 1000 payments 3. Locked 10 but failed 11th because of other processing locked 4. Netting rejected, but the 10 payments will only be unlocked by expiry on TTL |
| 4 | **Risk** | Potential atomic issue | Extreme case there is a lock expired but re-entrant from client level, which will cause lock cannot be released by owner, risk is low but possible | |

# Design principles

| | Principle | |
| --- | --- | --- |
| 1 | **Atomic** | **Lock and Unlock process should be atomic** |
| 2 | **Clear responsibility / Re-entrance** | 1. **Lock owner** , owns 1. Lock creation 2. Lock extension when process is not completed 3. Renew and retry if re-entrant client reject the call 2. **Re-entrant lock client**, owns responsibility only of lock validation check, reject if lock expired or invalid |
| 3 | **No dead lock** | **Reasonable TTL setup & auto unlock on exceptional scenarios** |
| 4 | **Applicable only for synchronized process** | **Note no parallel processing allowed during the process unless the processing are all stateless. ** |

# Current Design

Original implementation: [RATAN ONE Distributed Lock on resource - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+ONE+Distributed+Lock+on+resource)

# Proposal Overview

## Common Practices

| | Current Practice with Redis | Redisson Practice |
| --- | --- | --- |
| **Lock Key** | E.G. cashflow id, trade id |
| **Re-Entrant Level** | Process Level | Thread level within JVM (Rewrite required for target - Client validation) |
| **Lock Auto Extension** | NO | (Watch Dog) Renewal every 10 seconds until (1) Unlock done or (2) Process/Thread shut down |
| **Atomic** | NO | Yes, with Lua script |
| **Retry** | NO | Yes, efficient by subscription |
| **No dead lock allowed** | Lock expiry supported |
| **Lock management** | Lock owner creation/deletion Client extend the lock | All managed by Lock owner, Creation/Deletion/Renewal |
| |
| **Proposal** | Continue with current practice, enhance as below: 1. Lock with Lua script 2. Add watch dog for lock extension | **** **Proposal 1 - Client validation required** - Lock enhancement required for passing down the process id | **** **Proposal 2 - No Client validation, process without lock is not safe** |

## Batch Lock

For Netting case, batch lock required to lock all the component payments. Redisson provides RedissonMultiLock for the case, with a list of RedissonLock.

However it is found the performance is not that good, especially for BIC netting, the component payment volume would be above 5000+, it behaves the same with current implementation as a loop, which is time consuming, finishing lock will cost 20+ seconds.

Also there would be watchdog blast that N lock will have N threads for lock renewal.

RedissonFasterMultiLock is potential a way but enhancement required to mutual exclusive with the single lock as currently the data structure is different.

| | RedissonMultiLock | RedissonFasterMultiLock |
| --- | --- | --- |
| Time Complexity | O (N) | O (1) |
| Network I/O | 2N | 2 |
| Lock Failure Cost | 2S (S is succeeded lock) | 1 |
| WatchDog (thread count) | N | 1 |
| Fit volume | <100 | >1000 |

## Potential extended issues on RATAN API:

Lock mechanism is aligned with the agreement we made. However, some open questions for API among services come out, when Interface A call interface B and both are POST, which may cause data not in sync between 2 services:

1. Client (B) Timeout but still processing, Parent (A) ended with failure
2. Parent (A) Crashed while Client B is still processing. We have never seen such case but possible

Through analysis, the impact won't be for single resource processing, but impact 1 to many batch processing which could cause data out of sync between services.

| | Cases | Lock creation by (A) | Lock re-entrant/validation by (B) | Issue 1 - Parent Crashed (Never Happened Yet) | Issue 2 - Client timeout (Happened for netting case) |
| --- | --- | --- | --- | --- | --- |
| 1 | Payment STP processing 1 to 1 processing | Camunda workflow | Lifecycle, SSI stamping service, Netting Service | √ When Camunda Crashed, message will be re-consumed, worst case is the payment will be tech failed, retryable by Reinstate. | √ Payment will be tech failed. Retryable by reinstate |
| 2 | Payment Maker/Checker 1 to 1 processing | Camunda workflow | Lifecycle, SSI stamping service, NSTP Service | √ Data out of sync between Netting Service/Lifecycle Service, but process level, payment could be checker not applicable but retryable by Reinstate. | √ Payment will be tech failed. Retryable by reinstate |
| 3 | Netting 1 to N processing | Netting Service | Lifecycle | × Data out of sync between Netting Service/Lifecycle Service, which would impact on | × Data out of sync between Netting Service/Lifecycle Service |

<details>
<summary>Expand Details</summary>

| | Cases | Lock creation by (A) | Lock re-entrant/validation by (B) | Potential issue | Solution |
| --- | --- | --- | --- | --- | --- |
| 1 | Payment STP processing | Camunda workflow | Lifecycle, SSI stamping service, Netting Service | Once Parent A fired the call to client B, parent went shut down, client B would operate on the resource without lock | This is a case never happened onto production, 2 cases may happen which would drive guidelines: 1. **Parent consumes an event**: **retriable and recoverable** as Parent A will re-consume the event and client B already completed the task 2. Parent is a user action: |
| 2 | Netting | Netting Service | Lifecycle | B timeout is still an issue to be solved | Idempotent API, once timeout, parent A still call the service to acquire the result of last call. Feign timeout/kafka rebalance to be configured properly |
| 3 | Payment Maker/Checker | Camunda workflow | Lifecycle, SSI stamping service, NSTP Service |

</details>

### Guidance of lock & Test

[Distribution lock test cases && Uber orchestration - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3301076122)

### Current Lock Summary

| | Business Flow | Lock Creation | Lock Extension | Unlock |
| --- | --- | --- | --- | --- |
| 1 | Workflow | Orchestration 360s | Lifecycle Netting NSTP SSI | Orchestration |
| 2 | Swift Generation | Swift 360s | Lifecycle | Swift |
| 3 | Auto Affirm | Orchestration 10s | Lifecycle | Orchestration |
| 4 | | | | |
| 5 | Maker Submit | Lifecycle 2s | | Lifecycle |
| 6 | Checker Approve | Lifecycle 2s | | Lifecycle |
| 7 | Manual Fail | Lifecycle 2s | | Lifecycle |
| 8 | Manual Reinstate | Lifecycle 2s | | Lifecycle |
| 9 | Net/Unnet | Netting 360s | Lifecycle | Netting |
| 10 | | | | |

# Appendix

## Technical Analysis

| | Relational DB | ZK (Curator) | REDIS (REDISSION) |
| --- | --- | --- | --- |
| Re-Entrant | × | × Need self implementation | √ Thread Level within JVM |
| Lock Expiry | × | × Unlock until session close | √ |
| Lock Extension | × | × Unlock until session close | √ |
| Lock Watcher | × | √ | √ |
| Un-Fair lock (RATAN usage) | √ | √ | √ |
| Fair lock (Not RATAN usage) | × | √ | √ |
| MultiLock | × | × Need self implementation | √ |
| Community Active Level | NA | Medium Not worth to create a cluster for lock, zk for kafka is going to decommission soon as well | High |
| | | | |

## Redisson Default Logic

![](https://geekdaxue.co/uploads/projects/shanshanerchuan-5wk01@cr0zqg/1c67594d64b094ddf110f03f66d3392a.png)

Advantage:

| Advantage | Ratan business support | Implemented by Redission |
| --- | --- | --- |
| High performance and atomic operation | Locking and Unlocking is atomic, all client interactions with Redis are implemented by LUA script | LUA script is atomic, Redis allow only one LUA script execute at the same time |
| Multiple lock type support | BaseLock / ReadWriteLock / FairLock / Multilock / RedLock / SpinLock | | Type | Applicable scenarios | | --- | --- | | RedissonLock | Base reentrant lock | | ReadWriteLock | high concurrency scenarios read lock > write lock | | RedissonMultiLock | Bulk lock multiple keys one time. Lock in the same transaction All succeed or all fail by one LUA script and keep the operation is atomic | | ~~RedissonRedLock~~ （Deprecated） | Solve the cluster environment single point failover issue. Lock write to master, but master node is down before it sync to slave node, slave node selected as master node, but lock missed, now a new request send to master, it can get lock as well. Redis client need send request to all Redis nodes, 1. Apply to high consistency scenarios. 2. Need deploy multi independent Redis node | | RedissonFairLock | No special requirement for processing efficient. Locks are processed in order | | RedissonSpinLock | 1. Lock occupied a shot time 2. High concurrency operation for one key CPU high usage if lock occupied a little long | |
| Type | Applicable scenarios |
| RedissonLock | Base reentrant lock |
| ReadWriteLock | high concurrency scenarios read lock > write lock |
| RedissonMultiLock | Bulk lock multiple keys one time. Lock in the same transaction All succeed or all fail by one LUA script and keep the operation is atomic |
| ~~RedissonRedLock~~ （Deprecated） | Solve the cluster environment single point failover issue. Lock write to master, but master node is down before it sync to slave node, slave node selected as master node, but lock missed, now a new request send to master, it can get lock as well. Redis client need send request to all Redis nodes, 1. Apply to high consistency scenarios. 2. Need deploy multi independent Redis node |
| RedissonFairLock | No special requirement for processing efficient. Locks are processed in order |
| RedissonSpinLock | 1. Lock occupied a shot time 2. High concurrency operation for one key CPU high usage if lock occupied a little long |
| Watch Dog | | |
| Lock notification | Support multiple mode to notify: listener / event notification / Pub-Sub | ------------Listener RLock lock = redissonClient.getLock("anyLock"); lock.addListener(new LockListener() { @Override public void onLocked(RLock l) { System.out.println("Lock acquired by " + l.getName()); } @Override public void onUnlocked(RLock l) { System.out.println("Lock released by " + l.getName()); } }); ----------------Event redissonClient.getEventListener().addEventListener(RLock.class, "lock:myLock", RLock.class, event -> { if (event instanceof LockStatusChangedEvent) { LockStatusChangedEvent lockEvent = (LockStatusChangedEvent) event; System.out.println("Lock status changed: " + lockEvent.getLockName() + " -> " + lockEvent.getState()); } }); --------------Redis Pub/Sub RTopic<String> topic = redissonClient.getTopic("myTopic"); topic.publish("lock:acquired"); topic.publish("lock:released"); topic.addListener(String.class, (channel, msg) -> { System.out.println("Received message: " + msg); }); |
| Flexibility | Support change config to control lock behavior and strategy | |
| Common solution for distribution lock | A lot of information can be learned online, easy to do tracking and troubleshooting | |

## Zookeeper (Reference)

Advantage

| | |
| --- | --- |
| Performance | Zookeep temporary node is in order, lock get and release one by one |
| Consistency | CP model, ZAB protocol to keep data consistency |

Disadvantage

| | |
| --- | --- |
| Network overhead | Frequently create or delete template node on ZK, generate a significant amount of network overhead High volume and high frequency operation will cause performance bottleneck (e.g. Frequent status update ) |
| Implement complication | Framework like ** Curator**, take some effort to learn and few reference |
| Batch support | ZK temporary nodes are in order so batch lock is not supported |

# Usage of lock starter

## ResourceLockManager

| Method | Return | Parameters |
| --- | --- | --- |
| run | void | key(String) - the lock primarty key waitTimeSeconds(long) - the max wait time try to lock, unit is second actionInProgress(String) - the description of key being locked commandNoReturn(CommandNoReturn) - the action should take when key is locked |
| run | void | keys(List<String>) - the lock primarty keys list waitTimeSeconds(long) - the max wait time try to lock, unit is second actionInProgress(String) - the description of key being locked commandNoReturn(CommandNoReturn) - the action should take when key is locked |
| get | T | key(String) - the lock primarty key waitTimeSeconds(long) - the max wait time try to lock, unit is second actionInProgress(String) - the description of key being locked command(Command<T>) - the action should take when key is locked, T is the specified class type you should return |
| get | T | keys(List<String>) - the lock primarty key waitTimeSeconds(long) - the max wait time try to lock, unit is second actionInProgress(String) - the description of key being locked command(Command<T>) - the action should take when key is locked, T is the specified class type you should return |

## ResourceLock

Note: If you use this class to lock and release lock,  pls confirm you should release lock in final blocker

e.g.

finally {

resourceLock.release(key, "xxxxx has been released")

}

| Method | Return | Parameters |
| --- | --- | --- |
| lock | void | key(String) - the lock primarty key waitTimeSeconds(long) - the max wait time try to lock, unit is second actionInProgress(String) - the description of key being locked |
| lock | void | keys(List<String>) - the lock primarty keys list waitTimeSeconds(long) - the max wait time try to lock, unit is second actionInProgress(String) - the description of key being locked |
| releaseLock | void | key(String) - the lock primarty key actionInProgress(String) - the description of key being locked |
| releaseLock | void | keys(List<String>) - the lock primarty key actionInProgress(String) - the description of key being locked |