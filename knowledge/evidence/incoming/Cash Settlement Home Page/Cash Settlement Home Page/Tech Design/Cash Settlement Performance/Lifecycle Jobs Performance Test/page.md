Story:  [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11222354](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11222354)

Backgroud

The following issues were found with the job during testing：

1.  In a distributed environment, machine resources cannot be fully utilized.

2. `moveStatus` data validation affects batch execution.

3. Performance issues, including database and memory overflow problems.

4. Queries on many unnecessary columns; `materializeJob` and `failJob` only care about `cashflowId`, `BusinessVersion`, `CashflowVersion`, and `MinorVersion`.

# Auto Materialize

## Round 1 - 100k:

#### Job information

| | |
| --- | --- |
| Job Name | Auto Materialize |
| Data Volume | 100k |
| Environment | stagiorchestrationng |
| Job URL | /v2/ratan/cashflow/auto/materialization |
| JVM options | -Xms2048m -Xmx8192m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | 1k |
| Page amount | 100 |
| Time cost for data loading(by condition) | 2.17 s |
| Total Time cost | 706.5 s （11 m 46.5 s） last PT：17 m 31.26 s |
| Max Memory Usage | 2.09G (26.1% of 8G) - No OOM |
| Max CPU Usage | 78% |
| Success rate | 100% （cashflowId starts with PTMJ） |

### Processing results：

1. The processing success rate was 100%
2. In a distributed environment, it saves approximately 6 minutes compared to before (last PT env: dev).
3. No OOM occurred

### Conclusion:

1. This batch version can replace the original online version.

CPU and memory screenshots

[View panel - Microservice - Application Component - Ratan Central Monitoring - Middleware & Microservice Level - Dashboards - Grafana](https://fmo-mfe-preprod.pi.dev.net:3000/d/cx9my9huvvnk0c/microservice-application-component?from=now-3h&to=now&timezone=browser&var-service_list=ratan-cashflow-lifecycle-service:0&var-host_list=uklvadrat0001a.pi.dev.net&var-host_list=uklvadrat0002a.pi.dev.net&var-host_list=uklvadrat0005a.pi.dev.net&var-host_list=uklvadrat0006a.pi.dev.net&var-datasource=de62pwk929vy8b&refresh=1m&viewPanel=panel-5)

CPU：

![image-2026-1-12_13-20-2.png](attachments/image-2026-1-12_13-20-2.png)

![image-2026-1-12_13-21-33.png](attachments/image-2026-1-12_13-21-33.png)

Memory：

![image-2026-1-12_13-20-29.png](attachments/image-2026-1-12_13-20-29.png)

GC Count：

![image-2026-1-12_13-20-49.png](attachments/image-2026-1-12_13-20-49.png)

# Auto Fail

## Round1 - 234k

#### Job information

| | |
| --- | --- |
| Job Name | Auto Fail |
| Data Volume | 234945 |
| Environment | staging |
| Job URL | /v1/cashflow/jobs/cashflows/autoFail |
| JVM options | -Xms2048m -Xmx8192m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | 1k |
| Page amount | 235 |
| Time cost for data loading(by condition) | 14.5 s |
| Total Time cost | 5890.5 s（98m10s） |
| Max Memory Usage | 1.76G（22% of 8G）- No OOM |
| Max CPU Usage | 90.7% |
| Success rate | 94.93%，（succ: 223028, data lose: 241） |

### Processing results：

1. All data was processed once, and no processing interruption occurred due to missing data.
2. No database query exceptions occurred, meaning there were no exceptions regarding excessively long database input parameters.
3. CPU resources are fully utilized, and memory usage remains largely unchanged.

### Conclusion:

1. This batch version can replace the original online version.
2. **When dealing with large datasets, fail job can process data smoothly and efficiently by using a batch processing approach.**

CPU and memory screenshots

[Microservice - Application Component - Ratan Central Monitoring - Middleware & Microservice Level - Dashboards - Grafana](https://fmo-mfe-preprod.pi.dev.net:3000/d/cx9my9huvvnk0c/microservice-application-component?from=2026-01-08T09:00:00.000Z&to=2026-01-08T11:59:59.000Z&timezone=browser&var-service_list=ratan-cashflow-lifecycle-service:0&var-host_list=uklvadrat0001a.pi.dev.net&var-host_list=uklvadrat0002a.pi.dev.net&var-host_list=uklvadrat0005a.pi.dev.net&var-host_list=uklvadrat0006a.pi.dev.net&var-datasource=de62pwk929vy8b&refresh=1m)

CPU：

![image-2026-1-12_10-51-39.png](attachments/image-2026-1-12_10-51-39.png)

![image-2026-1-12_10-53-13.png](attachments/image-2026-1-12_10-53-13.png)

Memory：

![image-2026-1-12_10-36-52.png](attachments/image-2026-1-12_10-36-52.png)

Gc Count:

GC count indirectly proves that memory usage is relatively stable.

![image-2026-1-12_10-38-58.png](attachments/image-2026-1-12_10-38-58.png)

# Auto Release

## Round1 - 1k

#### Job information

| | |
| --- | --- |
| Job Name | Auto Release Job |
| Data Volume | 1000 |
| Environment | dev |
| Job URL | /v2/cashflow/holding-release |
| JVM options | -Xms2048m -Xmx8192m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | 1k |
| Page amount | 1 |
| Time cost for data loading(by condition) | 0.04 s |
| Total Time cost | 42 s |
| Max Memory Usage | 1.40G（17.5% of 8G）- No OOM |
| Max CPU Usage | 92.5% |
| Success rate | 100% |

### Processing results：

### Conclusion:

1. This batch version can replace the original online version.

CPU Usage:

![image-2026-1-27_15-10-20.png](attachments/image-2026-1-27_15-10-20.png)

Memory：

![image-2026-1-27_15-10-56.png](attachments/image-2026-1-27_15-10-56.png)

GC Count：

![image-2026-1-27_15-11-23.png](attachments/image-2026-1-27_15-11-23.png)

## Round2 - 19k

#### Job information

| | |
| --- | --- |
| Job Name | Auto Release Job |
| Data Volume | 19024 |
| Environment | fmrp2 |
| Job URL | /v2/cashflow/holding-release |
| JVM options | -Xms2048m -Xmx8192m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | 1k |
| Page amount | 20 |
| Time cost for data loading(by condition) | 5.3 s |
| Total Time cost | 513 s （8m33s） |
| Max Memory Usage | 4.63G（57.8% of 8G）- No OOM |
| Max CPU Usage | 87.6% |
| Success rate | 100% |

### Conclusion:

1. This batch version can replace the original online version.

Lifecycle CPU Usage:  max 87.6%

![image-2026-1-29_10-9-48.png](attachments/image-2026-1-29_10-9-48.png)

Orchestration CPU Usage:  max 83.2%

![image-2026-1-29_10-15-56.png](attachments/image-2026-1-29_10-15-56.png)

Swift CPU Usage:  max 94.4%

![image-2026-1-29_10-14-39.png](attachments/image-2026-1-29_10-14-39.png)

## Round 3 - 20k

#### Job information

| | |
| --- | --- |
| Job Name | Auto Release Job |
| Data Volume | 20272 |
| Environment | staging |
| Job URL | /v2/cashflow/holding-release |
| JVM options | -Xms2048m -Xmx8192m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | 1k |
| Page amount | 21 |
| Time cost for data loading(by condition) | 0.7s |
| Total Time cost | 612s （ 10m 12s） |
| Max Memory Usage | 4.7G（ 58.75% of 8G）- No OOM |
| Max CPU Usage | 15.7% |
| Success rate | 100% |

### Conclusion:

Lifecycle CPU Usage:  max 15.7%

![image-2026-3-17_10-42-34.png](attachments/image-2026-3-17_10-42-34.png)

Orchestration CPU Usage:  max 25.8%

![image-2026-3-17_10-43-22.png](attachments/image-2026-3-17_10-43-22.png)

Swift CPU Usage:  max 24.2%

![image-2026-3-17_10-43-52.png](attachments/image-2026-3-17_10-43-52.png)