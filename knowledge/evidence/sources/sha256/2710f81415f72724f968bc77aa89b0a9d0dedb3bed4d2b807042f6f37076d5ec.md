# Background

Netting API request timeout happened in prod, we start to analyze this API. As we know BAU squad is working on the performance tuning with multi-thread transaction model. In most cases the solution works fine, but it couldn't cover the edge case to guarantee the transaction commit or rollback together. I spend some time to analyze the code and try to implement in another way.

# Code Structure

# Tuning points:

| SN. | | Benefit | Challenge | Solution | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Distributed lock could be in batch instead of 1 by 1 | Reduce time cost of redis read/write | batch lock should be in transactional | 1. Lua script execution 2. use Completable Future or Cyclic Barrier to lock in parallel, 1 fail, all release | |
| 2 | Query from DB at once | Reduce DB interaction, Reduce time cost and IO cost | 1. There is table join sql which is complicated. 2. query all data to memory to process, memory usage might be larger than before. | Spring data JPA, rely on JPQL and spring data projection | |
| 3 | Run status machine in parallel | Multi-thread processing in pure JVM, reduce time cost | - | CompletableFuture | |
| 4 | Save all for existing cashflows at once | Reduce DB interaction, Reduce time cost and IO cost | JPA saveAll() on insert/update operation is not efficient enough, need to implement manually | 1. Enabling batch operation with configuration: spring.jpa.properties.hibernate.jdbc.batch_size=100 spring.jpa.properties.hibernate.order_inserts=true 1. Use @Modifying or JdbcTemplate.batchUpdate() with native batch update sql | |
| 5 | Batch close exception instead of close 1 by 1 | reduce 2 exception close API time cost | Need code change on 1. SSI stamping service 2. NSTP service | JDBC batch update | |

# Testing result

As point 2 and 3 has been done locally, we got a round of test, result as below:

| Volume | 2300 cashflow netting | 2300 cashflow netting |
| --- | --- | --- |
| Env | DEV(after tuning) | UAT1(before tuning) |
| Stage | Time Cost | Time Cost |
| preprocess - Add lock for cashflowids | ~8.7s | first lock - Mar 12, 2025 @ 14:20:09.414 last release - Mar 12, 2025 @ 14:21:03.855 time cost: ~54.4s |
| core process - run lifecycle | ~22s |
| post process - release lock | ~3s |
| post process - close exceptions | close SSI exceptions: ~2s close NSTP exceptions: ~4s ~6s | close SSI exceptions: ~1s close NSTP exceptions: ~1.5s time cost: ~2.5s |
| Total Cost | ~39.7s | ~57s |
| Reference | Discover - Elastic | Discover - Elastic |

# ![image-2025-3-12_14-55-35.png](attachments/image-2025-3-12_14-55-35.png)

# Long Term Solution:

As our API is batch-oriented and no limitation to users, there is risk if there is a sudden data increase. For long term design, the prober solution could be

1. Combine netting and lifecycle to same application to avoid timeout between netting and lifecycle.
2. Netting API could be implemented in asynchronized mechanism, such as notification center.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Document Draft:

Current use case for batch update transactional :

UI → preview API → Lifecycle query API

UI → Net API → Lifecycle Batch status update API

UI → Unnet API → Lifecycle Batch status update API

Netting Service job → Net/API →Lifecycle Batch status update API

Workflow → Auto Unnet API → Lifecycle Batch status update API

Other functions related to batch status update API

Cashflow Ready + Pending Ack receive Ack(Release action) need batch update component cashflow sub status event type

Cashflow Settle action batch update component cashflow sub status event type

What's our solution?

Step 1:

migrate net/Unnet code from netting service to lifecycle, avoid timeout between netting and lifecycle

UI net/Unnet request → Lifecycle net/Unnet component

Step 2:

Restructure current batch status update API, tuning the performance and keep it done in a whole transaction.

1. Fetch required data in 1 single query.
2. data processing/calculation in pure memory.
3. data persistence in batch level.
4. post process stuff handling (CQRS, close exceptions, trigger STP by Kafka, etc.)

the 2nd task could be run in parallel with each cashflow.

Step 3:

Distributed lock on cashflow list.

Currently distributed lock is widely used by cash settlement in single cashflow level, but not very much cases with list lock, but our starter support lock on list with foreach mechanism which can be further optimized.

currently dev env lock 2.2k + need 12s

Option 1: lock cashflow ids in multi-threads to save some time.

Option 2: Lua script to set key in transactional can be more efficient.

Step 4:

As this API is for batch operation, with the request body lager, still suggest to consider do it asynchronously.  We want to propose notification center to cover similar use case in the future.