1, Optimized items

| item name | before optimization | after optimization | remark |
| --- | --- | --- | --- |
| Using batch processing | 210 s | 52 s | 1000 cashflows are divided into 20 batches，make full use of all machine resources |
| Optimize the index of userTask table | 4000 ms | 2 ms | Use the cashflowId index, and delete invalid indexes |
| Optimize the index of camunda table | 1600 ms | 1-2 ms | Camunda task table query by index |
| JSON serialization/deserialization | 600 ms | 0 ms | Removed json serialization and deserialization of parsing exception collection |
| Transform frequent serialization | 450 ms | 8 ms | Remove the object serialization operation for each request |
| ProfileLimitation changed from single verification to batch verification | 700 ms per request | 150 ms for a batch of 50 requests | Changed from 1000 requests to 20 requests |

2, performance Analysis

Conclusion: The performance bottleneck is mainly the internal logic of camunda.

Comparing good and bad cases, we found that the time consumption was primarily in Camunda's complete operation, Furthermore, the holding-check operation took 1-6 seconds to complete the flow.

2.1，bad performance case :

AF7536600535 time taken: 10239 ms; AF7536600547 time taken: 9797 ms; AF7237600060  time taken：9518 ms

| | | AF7536600535 （bad） | AF7536600547（bad） | AF7237600060（bad） | AF7536600983（common） |
| --- | --- | --- | --- | --- | --- |
| Step | Service | Execute time | time taken(ms) | Execute time | time taken(ms) | Execute time | time taken(ms) | Execute time | time taken(ms) |
| Get Lock | | Sep 10, 2025 @ 11:29:59.478 | | Sep 10, 2025 @ 11:30:00.397 | | Sep 4, 2025 @ 19:34:11.257 | | Sep 9, 2025 @ 17:10:00.799 | |
| Query active task | | | | | | | | | |
| CashflowQueryServiceImpl.query | | | | | | | | | |
| Get latest SCBML message | | | | | | | | | |
| CashflowQueryServiceImpl.query | | | | | | | | | |
| Query active task | | | | | | | | | |
| Query active task | | | | | | | | | |
| Get latest SCBML message | | | | | | | | | |
| Call nstpException/approve | | | | | | | | | |
| Query active task | | | | | | | | | |
| Call nstpException/approve | | | | | | | | | |
| Query active task | | | | | | | | | |
| Query task for role （task start） | | Sep 10, 2025 @ 11:29:59.938 | sleep 1.5s | Sep 10, 2025 @ 11:30:00.701 | sleep 1.5s | Sep 4, 2025 @ 19:34:11.407 | sleep 1.5s | Sep 9, 2025 @ 17:10:01.392 | sleep 1.5s |
| Query CashflowUserTask by processBusinessKey | | Sep 10, 2025 @ 11:30:01.519 | 68 | Sep 10, 2025 @ 11:30:02.454 | 204 | Sep 4, 2025 @ 19:34:13.177 | 249 | Sep 9, 2025 @ 17:10:02.981 | 59 |
| CashflowQueryServiceImpl.query | lifecycle | | | Sep 10, 2025 @ 11:30:02.454 | 28 | Sep 4, 2025 @ 19:34:13.300 | 122 | | |
| Get latest SCBML message | orchestration | Sep 10, 2025 @ 11:30:01.561 | 41 | Sep 10, 2025 @ 11:30:02.455 | 31 | Sep 4, 2025 @ 19:34:13.301 | 123 | Sep 9, 2025 @ 17:10:03.105 | 124 |
| save user task done | | Sep 10, 2025 @ 11:30:01.580 | | Sep 10, 2025 @ 11:30:02.520 | | Sep 4, 2025 @ 19:34:13.330 | | Sep 9, 2025 @ 17:10:03.121 | |
| Request update/status | | | | | | | | | |
| start to spin status update for camunda | | | | | | | | | |
| end update/status | | | | | | | | | |
| call holding-check | | | | | | | | | |
| Post run holding-check | | | | | | | | | |
| Request update/status | | | | | | | | | |
| end update/status | | | | | | | | | |
| PublishEnrichedMessageService | orchestration | Sep 10, 2025 @ 11:30:02.246 | 148 | Sep 10, 2025 @ 11:30:03.033 | 113 | Sep 4, 2025 @ 19:34:14.920 | | Sep 9, 2025 @ 17:10:03.863 | 101 |
| Send domain event success | lifecycle | Sep 10, 2025 @ 11:30:03.590 | | Sep 10, 2025 @ 11:30:04.211 | | Sep 4, 2025 @ 19:34:15.795 | | | |
| message-event insert successfully | message-event | Sep 10, 2025 @ 11:30:03.599 | | Sep 10, 2025 @ 11:30:04.940 | | Sep 4, 2025 @ 19:34:15.541 | | Sep 9, 2025 @ 17:10:03.565 | |
| handleDomainEventForOpenSearch done | lifecycle | Sep 10, 2025 @ 11:30:04.243 | | | | Sep 4, 2025 @ 19:34:15.869 | | Sep 9, 2025 @ 17:10:03.778 | |
| message-event insert successfully | message-event | Sep 10, 2025 @ 11:30:05.567 | | Sep 10, 2025 @ 11:30:05.512 | | | | Sep 9, 2025 @ 17:10:03.865 | |
| Task completed | | Sep 10, 2025 @ 11:30:10.178 | 10239 | Sep 10, 2025 @ 11:30:10.499 | 9797 | Sep 4, 2025 @ 19:34:20.911 | 9518 | Sep 9, 2025 @ 17:10:04.801 | 3408 |
| Release lock | | Sep 10, 2025 @ 11:30:10.228 | | Sep 10, 2025 @ 11:30:10.507 | | Sep 4, 2025 @ 19:34:20.926 | | Sep 9, 2025 @ 17:10:04.808 | |