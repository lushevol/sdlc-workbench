1 Conclusion

uat2 maker

| case | cashflowId rows | interface | condition one | condition two | condition three | condition four | max (second) | min (second) | average (second) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000 cashflows in a single batch and verify the checker under 50 core threads | 1000 | maker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | | | 90 | | |
| backend 20 batches, and verify the maker under 50 core threads and 4 database connections | 1000 | maker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | backend divided into 20 batches, with 50 cashflows in each batch | | 55 | | |
| frontend and backend 20 batches, and verify the maker under 50 core threads and 4 database connections | 1000 | maker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | | 45 | | |
| frontend and backend 20 batches, and verify the maker under 50 core threads and 4 database connections | 1000 | maker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 50 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | | 17 | | |
| frontend and backend 20 batches, and verify the maker under 50 core threads and 4 database connections | 1000 | maker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 50 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | | 21 | | |

uat2 checker

| case | cashflowId rows | interface | condition one | condition two | condition three | condition four | max (second) | min (second) | average (second) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 cashflows in a single batch and verify the checker under 20 core threads | 100 | checker | app thread pool: core thread size: 20 max thread size: 50 queue capacity: 10000 | | | | 22.84 | | |
| 1000 cashflows in a single batch and verify the checker under 20 core threads | 1000 | checker | app thread pool: core thread size: 20 max thread size: 50 queue capacity: 10000 | | | | 210 | | |
| 1000 cashflows in a single batch and verify the checker under 50 core threads | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | | | | 132 | | |
| frontend 2 batches, and verify the checker under 50 core threads and 4 database connections | 100 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | frontend divided into 2 batches, with 50 cashflows in each batch | | 18.68 | | |
| frontend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | frontend divided into 20 batches, with 50 cashflows in each batch | | 72 | 13.18 | 41.93 |
| frontend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | frontend divided into 20 batches, with 50 cashflows in each batch | | 72 | 17.58 | 44.73 |
| backend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | backend divided into 20 batches, with 50 cashflows in each batch | | 90 | | |
| frontend and backend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 20 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | | 90 | | |
| frontend and backend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 50 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | | 72 | 14.44 | |
| frontend and backend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 50 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | two query user task | 52 | 12.24 | |
| frontend and backend 20 batches, and verify the checker under 50 core threads and 4 database connections | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 50 | frontend and backend divided into 20 batches, with 50 cashflows in each batch | three query user task | 59 | | |

Performance bottleneck:

1 task.complete

------------------------------------------------------------------------------------------------------------------------

1.2 case 1

core thread size: 20

max thread size: 50

queue capacity: 10000

| Test rows | fetch cashflow infomation | checkLimitationsBatch | checker |
| --- | --- | --- | --- |
| 2 | 548ms | 999ms | 7.84s |
| 100 | 3. 14s | 324ms | 22.84s |
| 1000 | 22.83s | 1.64s (max, first request) | 3.5m |

1.3 case 2

core thread size: 50

max thread size: 50

queue capacity: 10000

| Test rows | fetch cashflow infomation | checkLimitationsBatch | checker |
| --- | --- | --- | --- |
| 1000 | 34.87s | 657ms | 2.2m |

1.4 case 3

Condition 1:

app thread pool

core thread size: 50

max thread size: 50

queue capacity: 10000

Condition 2:

db thread pool
minimumIdle: 4maximumPoolSize: 10

Condition 3:
The browser simulates the submission of checkers in batches, divided into 17 batches, with 50 cashflows in each batch.

result:

The verification results are an average of 43 seconds and a maximum of 56 seconds. The detailed results are as follows：

![image-2025-8-26_19-34-15.png](attachments/image-2025-8-26_19-34-15.png)

1.5 case 4

Condition 1:

app thread pool

core thread size: 50

max thread size: 50

queue capacity: 10000

Condition 2:

db thread pool
minimumIdle: 4maximumPoolSize: 20

Condition 3:
The browser simulates the submission of checkers in batches, divided into 17 batches, with 50 cashflows in each batch.

![image-2025-8-29_10-43-40.png](attachments/image-2025-8-29_10-43-40.png)

average : 41.93s， max:  72s

1.6  condition same to 1.5

![image-2025-9-1_13-31-38.png](attachments/image-2025-9-1_13-31-38.png)

1.7  condition same to 1.5 but 100 cashflowIds

![image-2025-9-1_13-39-8.png](attachments/image-2025-9-1_13-39-8.png)

1.8 backend batch maker

![image-2025-9-2_18-56-34.png](attachments/image-2025-9-2_18-56-34.png)

1.9 backend batch checker

![image-2025-9-2_19-0-28.png](attachments/image-2025-9-2_19-0-28.png)

1.9.1 frontend and backend  batch maker

![image-2025-9-3_9-27-44.png](attachments/image-2025-9-3_9-27-44.png)

1.9.2 frontend and backend  batch checker

![image-2025-9-3_9-32-51.png](attachments/image-2025-9-3_9-32-51.png)

1.9.3 frontend and backend  batch maker

![image-2025-9-3_11-2-42.png](attachments/image-2025-9-3_11-2-42.png)

1.9.4 frontend and backend  batch maker ， db maxpoosize:50

![image-2025-9-3_11-15-49.png](attachments/image-2025-9-3_11-15-49.png)

1.9.5 frontend and backend  batch maker ， db maxpoosize:50

![image-2025-9-4_19-31-11.png](attachments/image-2025-9-4_19-31-11.png)

1.9.6 frontend and backend  batch checker， db maxpoosize:50

![image-2025-9-4_19-35-30.png](attachments/image-2025-9-4_19-35-30.png)

1.9.7 batch maker

![image-2025-9-10_11-26-28.png](attachments/image-2025-9-10_11-26-28.png)

1.9.8 batch checker

![image-2025-9-10_11-32-19.png](attachments/image-2025-9-10_11-32-19.png)

conclusion: The main performance bottleneck is still in the checker interface, followed by the acquisition of cashflow information interface

2 Evidence

2.1

core thread size: 50

a) [https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows](https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows)

![image-2025-8-22_13-23-6.png](attachments/image-2025-8-22_13-23-6.png)

34.87s

b) [https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/profileLimitation/checkLimitationsBatch](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/profileLimitation/checkLimitationsBatch)

![image-2025-8-22_13-24-7.png](attachments/image-2025-8-22_13-24-7.png)

657.41ms

c) [https://uklvadapp1344.uk.dev.net:8453/api/ratan/v2/camunda/task/NSTPSSI/checker](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v2/camunda/task/NSTPSSI/checker)

![image-2025-8-22_13-28-17.png](attachments/image-2025-8-22_13-28-17.png)

2.2m

2.2

core thread size: 50

db min thread size: 4, max: 20

a) [https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows](https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows)

![image-2025-8-28_18-27-11.png](attachments/image-2025-8-28_18-27-11.png)

b) [https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/profileLimitation/checkLimitationsBatch](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/profileLimitation/checkLimitationsBatch)

![image-2025-8-28_18-28-45.png](attachments/image-2025-8-28_18-28-45.png)

c) [https://uklvadapp1344.uk.dev.net:8453/api/ratan/v2/camunda/task/NSTPSSI/checker](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v2/camunda/task/NSTPSSI/checker)

2.6m

2.3

There are two operations for the checker interface.

One is ProfileLimitCheck, which calls the original checkLimitation/{profile}/{currency}/{amount} single verification interface, which takes about **300 milliseconds** on average,

and the other is the checkerOperate operation, which takes about **6.7 seconds** on average, that is, a checker operation takes about** 7 seconds**.

A checker operation needs to call the following method and number of times:

| service method | call times | total time taken(ms) |
| --- | --- | --- |
| checkUserLimitBasedProfileAccess Most of your time is spent on cashFlowApiClient.getCashFlows（711） | 1 | 829 |
| | | |
| statusUpdateService.getLatestSCBMLMessage | 3 | 120 |
| userTaskService.queryActiveTask | 3 | 534 |
| userTaskService.queryDeadTask | 1 | |
| taskService.complete | 1 | 4336 |
| commonServiceCaller.execute | 1 | 163 |
| userTaskService.save | 3 | |
| authServerClient.getUserEntitlement | 1 | 100 |
| total time | 6742 |

In summary, the performance bottleneck is mainly reflected in three places.

One is checkUserLimitBasedProfileAccess. This method is to verify each cashflowId separately;

the second is queryActiveTask, which does not index when querying the table according to the cashflowId;

the third is taskService.complete, which is the most time-consuming.

3 Improvement plan

~~3.1 Change a single ProfileLimitCheck to call the batch limitCheck interface.~~

~~3.2 Add a cashflowId query index to the user table, modify the corresponding query code, and use cashflowId as the first query condition.~~

~~CREATE INDEX idx_ratan_cashflow_user_task_cid_bt_bv_active~~
~~    ON ratan_cashflow_user_task (cashflow_id, business_type, business_version, active);~~

![image-2025-9-3_10-3-45.png](attachments/image-2025-9-3_10-3-45.png)

3.3 Optimize taskService.complete method.

this is the underlying logic of camunda.

During the execution of the complete method, CompleteTaskListener will be called. When this class is executed, sleep 1.5 seconds first, and then access userTask and getLatestSCBMLMessage and other operations.

When approve, it is only responsible for saving task data, etc., and changes the camuda operation to asynchronous, especially the camuda complete operation.

Alternatively, change the complete method to asynchronous, but communicate with joay to change the code logic from asynchronous to synchronous.

3.4 Optimize [stmcn/v1/cashflows](https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows) api

This interface takes about 30 seconds to query 1,000 cashflowIds. After the performance of this API is improved, the user experience can be improved, and the approve operation will be much smoother.

3.5 Optimize db pool  — complete

Orchestration uses the direct connection method of the database, and the total report too many connections is reported in pt.
 Modify the database connection method, change the direct connection method to HikariDataSource, and set the minimum number of connections to 4 and the maximum number of connections to 10.

3.6 Optimize json parse  — complete

The parseExceptionListRequest method has code to parse json, but it is time-consuming to serialize and deserialize repeatedly.
The getEntitlement method uses new ObjectMapper(). This object is thread-safe and does not need to be created repeatedly in the method.

parseExceptionListRequest

3.7 lifecycle get cashflow

As the concurrency increases, the time to get cashflow from lifecycle also increases.

![image-2025-8-29_11-12-35.png](attachments/image-2025-8-29_11-12-35.png)

3.8 Optimize camunda table

uat2

ACT_RU_TASK :  60.9w

ACT_RU_VARIABLE: 2471.3W

ACT_RU_EXECUTION: 907W

ACT_HI_TASKINST: 3.6W

ACT_HI_VARINST： 466.7W

ACT_HI_ACTINST: 148.9W

ACT_HI_DETAIL: 890.1W

ACT_GE_BYTEARRAY：1762W

4 base info

4.1 thread pool info

core thread size: 20（50）

max thread size: 50

queue capacity : 10000

a, fetch cashflow infomation

[https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows](https://uklvadapp1344.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows)

b, checkLimitationsBatch（rule-service）

[https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/profileLimitation/checkLimitationsBatch](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/profileLimitation/checkLimitationsBatch)

c, checker（foundation）

[https://uklvadapp1344.uk.dev.net:8453/api/ratan/v2/camunda/task/NSTPSSI/checker](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v2/camunda/task/NSTPSSI/checker)

![image-2025-8-28_17-22-47.png](attachments/image-2025-8-28_17-22-47.png)