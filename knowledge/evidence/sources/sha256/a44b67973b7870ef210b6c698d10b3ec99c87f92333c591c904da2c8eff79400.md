#

# Performance Testing Result

| Queried Filter | Underlining Filters | Page Size 1000 | Page Size 5000 | 1000 vs 5000 Scaling Factor | Page Size 5000 + VD in [T, T+10] | + VD vs without VD Scaling Factor |
| --- | --- | --- | --- | --- | --- | --- |
| 90% Response Time (ms) | 90% Response Time (ms) | 90% Response Time (ms) |
| Default Filters | Cashflow State = WAITING VD between [T, T+5] | 195.00 | 161.00 | 0.82 | | |
| Only WAITING | Cashflow State = WAITING | 893.00 889.00 934.00 | 3418.00 3584.00 3510.00 | 3.9 | 116.70 118.50 105.30 | 0.033 |
| INDIA | Entity FMCODE in [....] VD = ... | 147.00 | 126.00 | 0.85 | | |
| NDF LONDON | Entity FMID = ... Murex Product Typology = ... Cashflow State NOTIN [...] | 851.00 1319.00 1337.00 | 923.00 1336.00 1351.00 | 1.14 | 291.10 435.90 440.10 | 0.315 |
| COMM CHECKER | Sub State = Pending Verification Is Commodity = true Entity FMID IN [...] | 237.00 69.00 99.00 | 175.00 115.00 100.00 | 1.5 | 88.60 81.70 101.40 | 0.502 |
| UK COMMODITY | Entity FMID = ... Cashflow State NOTIN [...] Is Commodity = true | 22305.00 22412.00 22481.00 | 25233.00 25393.00 26159.00 | 1.20 | 5352.30 11862.00 18592.90 | 0.4 |
| DRV KL LDN COM | Entity FMID = ... Cashflow State in [...] Is Commodity = true Counterparty FMID NOTIN [...] VD NOTIN [...] | 3376.00 3272.00 2415.00 | 2978.00 1791.00 1887.00 | 0.87 | | |
| PAYDOL UK | Entity FMID = ... Cashflow State NOTIN [...] Is Commodity = false Counterparty FMID NOTIN [...] Murex Product Typology NOTIN [...] ISDA Taxonomy NOTIN [...] | 6607.00 9372.00 26920.00 | 26927.00 9883.00 10179.00 | 4 | 6910.90 8411.40 3349.50 | 0.256 |
| UK NON COMMODITY | Entity FMID = ... Cashflow State NOTIN [...] Is Commodity = false Counterparty FMID NOTIN [...] Murex Product Typology NOTIN [...] ISDA Taxonomy NOTIN [...] | 45731.00 17463.00 34051.00 | 18604.00 35079.00 35221.00 | 2.05 | 6773.20 10910.80 10971.70 | 0.364 |
| DRV ASA SETTS | Entity FMID in [...] Cashflow State in [...] | 513.00 113.00 125.00 | 436.00 147.00 422.00 | 1.3 | 135.80 149.00 150.80 | 0.30 |
| WAITING + VD 15 | Cashflow State IN [WAITING] VD between [T, T+15] | 72.00 74.00 86.00 | 105.00 109.00 103.00 | 1.4 | | |
| Overall Scaling Factor | | | | 1.5 | | 0.3 |

# Conclusion

1. Comparing with 1000 loading, 5000 is 5x larger but with less expecting round time, the overall time slowness than 1000 is 1.5, which is more efficiency.
2. In Cashflow Blotter query case, blotter loading performed 1000 page size before UK volume (we have increased it from 500 once a time). As UK users requires, we increased the page size to 5000, the expecting response time increased. ***So the SLA "user action turn around time" should be change correspondingly***.

![image-2025-2-25_9-57-9.png](attachments/image-2025-2-25_9-57-9.png)

**          Max: 7.5 seconds (Cashflow Blotter Loading)**

**          Avg: 3 seconds**

Explaining: with 5000 size reached the scaling of 1.5 times, the max should go from 5 to 7.5 (5*1.5), and avg go from 2 to 3 (2*1.5).

# Suggestion

1. Different filters results to different responding time, response time various with filters.
2. Query on indexed fields will make the response even fast, there are cases which will make the query more slower, 1. If queried fields contains not indexed fields. (most impacted) 2. If query operators contains NOTIN, !=, LIKE. 3. If queried fields is indexed but the values distribution take a large amount, DB will give up using Index. (e.g. if 90% cashflow in db are suppressed, then filter with suppressed will not trigger index).
3. We consider query on filters with all indexed fields and with valid operators (=, IN, BET) as recommended valid queries, otherwise they are invalid queries. 1. Valid queries should be in NFR scope. 2. Invalid queries, as case various, we can't predict how much time it will cost. The response time is not guaranteed.
4. If we added all filters with VD limits, the improvement is obviously. Overall 3x times faster than those without VD limits.

# Performance Testing on 20250412 Release

**Target Env**: Staging

**Total Volume**: 1357121

**VD**: 0318

**VD Volume**: 84141

**User Concurrency**: 50

**Target TPS**: 1

| Queried Filter | Underlining Filters | Legacy Response | Ultra Response |
| --- | --- | --- | --- |
| 90% Response Time (ms) | 90% Response Time (ms) |
| Default Filters | Cashflow State = WAITING VD = 20250318 | 3212.00 | 2282.00 |
| INDIA | Entity FMCODE in [....] VD = 20250318 | 291.20 | 169.40 |
| NDF LONDON | Entity FMID = ... Murex Product Typology = ... Cashflow State NOTIN [...] VD = 20250318 | 2833.00 2384.10 3210.10 | 1235.60 2081.70 2027.40 |
| COMM CHECKER | Sub State = Pending Verification Is Commodity = true Entity FMID IN [...] VD = 20250318 | 129.70 1167.10 329.20 | 88.00 54.40 482.00 |
| UK COMMODITY | Entity FMID = ... Cashflow State NOTIN [...] Is Commodity = true VD = 20250318 | 1602.12 1230.00 2491.00 | 1504.40 1575.00 1626.00 |
| DRV KL LDN COM | Entity FMID = ... Cashflow State in [...] Is Commodity = true Counterparty FMID NOTIN [...] VD = 20250318 | 2013.01 2891.01 2931.00 | 1502.50 2713.50 2333.20 |
| PAYDOL UK | Entity FMID = ... Cashflow State NOTIN [...] Is Commodity = false Counterparty FMID NOTIN [...] Murex Product Typology NOTIN [...] ISDA Taxonomy NOTIN [...] VD = 20250318 | 1853.20 2930.11 2811.02 | 1777.40 3101.00 3195.10 |
| UK NON COMMODITY | Entity FMID = ... Cashflow State NOTIN [...] Is Commodity = false Counterparty FMID NOTIN [...] Murex Product Typology NOTIN [...] ISDA Taxonomy NOTIN [...] VD = 20250318 | 1823.10 3419.22 3519.01 | 1701.70 3304.00 3427.00 |
| DRV ASA SETTS | Entity FMID in [...] Cashflow State in [...] VD = 20250318 | 1230.11 3952.11 2699.35 | 196.00 4232.20 2456.80 |
| WAITING + VD 15 | Cashflow State IN [WAITING] VD = 20250318 | 1911.01 3920.51 2501.30 | 2318.10 4105.20 2336.80 |
| ACCOUNTING ERROR + VD+-1 | Cashflow Accounting Status in ["SENT", "REJECTED", "MISSING_INFO"] and VD in [T-1, T+1] | 90.22 | 38.50 |
| ERROR + VD+2 | Cashflow State = "Error" and VD in [T, T+2] | 120.23 | 63.00 |
| FAILED + VD Today | Cashflow State = "FAILED" and VD = T (CURRENT_DATE) | 901.65 | 648.50 |
| HOLD + VD+2 | Cashflow State = "HOLD" and VD in [T, T+2] | 90.77 | 77.80 |
| QUEUED + VD+2 | Cashflow State = "QUEUED" and VD in [T, T+2] | 125.60 | 54.40 |
| SWIFT ERROR + VD+-1 | Cashflow Swift Status in [ "Ratan Internal Error", "FMSGW Error", "AMH Error", "MX Generation Error", "FMSRE Error", "SCPAY Error"] and VD in [T-1, T+1] | 157.33 | 77.50 |
| WAITING + VD Today | Cashflow State = "WAITING" and VD = T (CURRENT_DATE) | 952.23 | 56.90 |
| GROUP ERROR | Dashboard Status = "ERROR" | 305.55 | 248.00 |
| GROUP PENDING | Dashboard Status = "PENDING" and Dashboard Group Status in ["PENDING", "PENDING_PRE_GROUP"] | 302.22 | 207.60 |
| GROUP PENDING VALIDATION + VD Today | Dashboard Status = "PENDING" and Dashboard Group Status = "PENDING_TRADE_VALIDATION" and VD <= T+1 | 196.88 | 139.50 |

## Conclusion

Regarding to legacy query performance, new ultra query doesn't create performance shortcoming, the overall scale factor is around 5%.

# Appendix

Ultra Cashflow Query

[https://uklvadrtn006a.pi.dev.net:8081/performance-test/1744185925071/report/index.html](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1744185925071/report/index.html)

![image-2025-4-9_17-21-34.png](attachments/image-2025-4-9_17-21-34.png)

Legacy Cashflow Query

TODO

Jmeter Script

📎 [RATAN_ADVANCED_SEARCH_PT.jmx](attachments/RATAN_ADVANCED_SEARCH_PT.jmx)