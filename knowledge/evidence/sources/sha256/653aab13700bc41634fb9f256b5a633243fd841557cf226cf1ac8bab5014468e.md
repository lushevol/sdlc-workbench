Story:  [Extra] Jobs optimization [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5856273](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5856273)

DOD, ensure jobs work for UK volume with 40,000 assumption of daily volume

1. Materialization job
2. Auto fail job
3. Auto release job for swift generation
4. Accounting job for EBBS feeds

# Auto Materialize

## Round 1 - 50k:

### V1

#### Job information

| | |
| --- | --- |
| Job Name | Auto Materialize |
| Data Volume | 50k |
| Environment | Dev |
| Job URL | /v1/ratan/cashflow/auto/materialization |
| JVM options | -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=1024m |

#### Result

| | |
| --- | --- |
| Page size | NA |
| Page amount | NA |
| Time cost for data process | 0.1635592s |
| Total Time cost | 790s |
| Max Memory Usage | 1.75G(87.3%) |
| Success rate | 5534 not materialized due to mocked data is invalid |

![image2024-10-20_12-32-53.png](attachments/image2024-10-20_12-32-53.png)

### V2

#### Job information

| | |
| --- | --- |
| Job Name | Auto Materialize |
| Data Volume | 50k |
| Environment | Dev |
| Job URL | /v2/ratan/cashflow/auto/materialization |
| JVM options | -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=1024m |

#### Result

| | |
| --- | --- |
| Page size | 2k |
| Page amount | 25 |
| Time cost for data loading(by condition) | 0.1635592s |
| Time cost for each page(query by ID + run lifecycle) | p1: 21.47(21.39s), p2: 15.85(15.81s), P3: 18.67(18.63s), P4: 15.96(15.93s), P5: 17.73(17.69s) P6: 14.65(14.61s), P7: 16.68(16.64s), P8: 15.23(15.2s), P9: 15.5(15.46s), P10: 16.03(16s) P11: 16.17(16.14s), P12: 15.62(15.57s), P13: 17.19(17.16s), P14: 17.59(17.54), P15: 16.26(16.22s) P16: 14.9(14.87s), P17: 13.17(13.13s), P18: 15.07(15.03s), P19: 15.5(15.45s), P20: 15.16(15.12s) P21: 16.58(16.55s), P22: 18.31(18.27s), P23: 16.53(16.49s), P24: 15.09(15.05s), P25: 15.04(15s) |
| Total Time cost | 406.13s |
| Max Memory Usage | 1.74G(87%) |
| Success rate | 5614 not materialized due to mocked data is invalid |

![image2024-10-20_11-22-53.png](attachments/image2024-10-20_11-22-53.png)

## Round 2 - 100k:

### V1:

#### Job information

| | |
| --- | --- |
| Job Name | Auto Materialize |
| Data Volume | 100k |
| Environment | Dev |
| Job URL | /v1/ratan/cashflow/auto/materialization |
| JVM options | -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | NA |
| Page amount | NA |
| Time cost for data process | |
| Total Time cost | No result |
| Max Memory Usage | 2G(100%) |
| Success rate | NA |

![image2024-10-23_14-30-36.png](attachments/image2024-10-23_14-30-36.png)

![image2024-10-23_14-32-10.png](attachments/image2024-10-23_14-32-10.png)

### V2:

#### Job information

| | |
| --- | --- |
| Job Name | Auto Materialize |
| Data Volume | 100k |
| Environment | Dev |
| Job URL | /v2/ratan/cashflow/auto/materialization |
| JVM options | -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=1024m |

#### Result:

| | |
| --- | --- |
| Page size | 2k |
| Page amount | 50 |
| Time cost for data loading(by condition) | 0.32s |
| Time cost for each page(query by ID + run lifecycle) | each page average time cost : 21s |
| Total Time cost | 17 m 31.26 s(1051.26) |
| Max Memory Usage | 1.99G(99.7%) - Handler dispatch failed: java.lang.OutOfMemoryError: Java heap space on page 48 |
| Success rate | 20450 not materialized due to mocked data is invalid |

![image2024-10-23_10-35-12.png](attachments/image2024-10-23_10-35-12.png)

# Conclusion:

1. Use **V2 **instead of V1 on production
2. Increate JVM to **-Xms3072m -Xmx6144m -XX:MaxMetaspaceSize=3072m**
3. API gateway will trigger** **circuitBreaker after 65s, whether need to extend to 30mins or change job to async mechanism TBC.

![image2024-10-24_11-17-41.png](attachments/image2024-10-24_11-17-41.png)

# Auto Fail

## Round1 - 50k

### V1

#### Job information

| | |
| --- | --- |
| Job Name | Auto Fail |
| Data Volume | 50k |
| Environment | Dev |
| Job URL | /v1/cashflow/jobs/cashflows/autoFail |
| JVM options | -Xms3072m -Xmx6144m -XX:MaxMetaspaceSize=3072m |

#### Result:

| | |
| --- | --- |
| Page size | NA |
| Page amount | NA |
| Time cost for data process | 3m13s |
| Total Time cost | 4m53.76 s |
| Max Memory Usage | 1.84G(31% of 6G) |

# Auto Release

## Round 1 - 50k:

### V1  - TBD

#### Job information

| | |
| --- | --- |
| Job Name | Auto Release |
| Data Volume | 50k |
| Environment | Dev |
| Job URL | /v1/cashflow/holding-release |
| JVM options | -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=1024m |

#### Result

| | |
| --- | --- |
| Page size | NA |
| Page amount | NA |
| Time cost for data process | 0.1635592s |
| Total Time cost | 790s |
| Max Memory Usage | 1.75G(87.3%) |
| Success rate | 5534 not materialized due to mocked data is invalid |

### V2

#### Job information

| | |
| --- | --- |
| Job Name | Auto Release |
| Data Volume | 50k(427resultant + 49573 gross) |
| Environment | Dev |
| Job URL | /v2/cashflow/holding-release |
| JVM options | -Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=1024m |

#### Result

| | |
| --- | --- |
| Page size | 2k |
| Page amount | 25 |
| Time cost for group lock filter | 5min37s(12.1s for resultant filter + 5mins 25s) |
| Time cost for each page(query by ID + run lifecycle) | ~2.7s for each page |
| Total Time cost | 6min49s |
| Max Memory Usage | < 900M |
| Success rate | 7095 filtered by group lock check, others 100% success |

![image2024-10-30_21-44-51.png](attachments/image2024-10-30_21-44-51.png)