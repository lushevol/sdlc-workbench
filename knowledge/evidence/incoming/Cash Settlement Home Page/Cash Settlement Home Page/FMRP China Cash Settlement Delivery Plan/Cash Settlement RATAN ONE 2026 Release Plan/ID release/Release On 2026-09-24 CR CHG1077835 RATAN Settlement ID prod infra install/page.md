# 1.3 Performance Test

| Item | Test Plan | Test Results |
| --- | --- | --- |
| | | |

# 1.4 Release Summary

| Squad | Release Date - [ ] DevOps | Release Scope - [ ] DM | Test Plan - [ ] QA | Test Summary - [ ] QA | Test Results Link - [ ] QA | Release Phase - [ ] DM | Test Progress - [ ] QA | Release Status - [x] Sign-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN | 2026-09-26 | | | - [x] **System Test** Reason if not to not: - [x] **Integration Test** Reason if not to not: - [x] **Acceptance Test ** Reason if not to not: - [x] **Regression Test** Reason if not to not: - [x] **Performance Test** Reason if not to not: | **Pls refer to Test Summary**: More Details pls refer to email: **QA Signoff:** **UAT signoff: ** | | | - [x] Delivery Manager Signoff - [x] QA Signoff - [x] User Signoff |

# 1.5 PIT

| No. | PIT Steps | Excepted Result | Results | Evidence screenshots |
| --- | --- | --- | --- | --- |
| | ulimit check | | | | |
| | database check, log check | 15 schemas are all there tables are there, query 3 tables as example `**log check script need to add to post build: ** cat /apps/ratanrt/bin/postgres/indonesia/logs/RTN_ID_Init_Script_ratanone_id.log` | | |
| | Kafka primary cluster status | /apps/ratanrt/utilities/kafka/live/bin/kafka-broker-api-versions.sh --bootstrap-server id279jxkgpjqq00:9092 | | |
| | redis primary cluster status | /apps/ratanrt/utilities/redis/live/src/redis-cli -h id279jxkgpjqq00 -p 6379 -a 'RatanOne' cluster nodes | awk '{split($2,a,"@"); hp=a[1]; st=(($3 ~ /fail|pfail|noaddr/ || $8!="connected")?"DOWN":"OK"); print hp, st}' | | |
| | ES cluster check | echo "cluster_status: $(curl -ks -u 'elastic:ratanone' '[https://](https://idlvaurat01.id.standardchartered.com:9200/_cluster/health?filter_path=status)[id279jxkgpjqq00.id.standardchartered.com](http://id279jxkgpjqq00.id.standardchartered.com):9200/_cluster/health?filter_path=status' | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')"; curl -ks -u 'elastic:ratanone' '[https://](https://idlvaurat01.id.standardchartered.com:9200/_cat/nodes?h=ip,port,node.role,master,name)[id279jxkgpjqq00.id.standardchartered.com](http://id279jxkgpjqq00.id.standardchartered.com):9200/_cat/nodes?h=ip,port,node.role,master,name' | awk '{print $1":"$2, "roles="$3, "master="$4, "name="$5}' | | |
| | kibana access successfully | [https://ratan-id-cluster.51358.id.app.standardchartered.com:5601/](https://ratan-id-cluster.51358.id.app.standardchartered.com:5601/) | | |
| | eureka access successfully, services get deployed, except message bridge, auth server package version is correct | [https://ratan-id-cluster.51358.id.app.standardchartered.com:8763](https://ratan-id-cluster.51358.id.app.standardchartered.com:8763/)/ | | |
| | chk openAPI | [https://](https://ratan-id-cluster.51358.id.app.standardchartered.com:8763/)[ratan-id-cluster.51358.id.app.standardchartered.com:](https://ratan-id-cluster.51358.id.app.standardchartered.com:8763/)8868[/v1/management/openapis](http://fmo-mfe-dev.uk.dev.net:8453/api/idns/ratan/v1/management/openapis) chk in es | | |

![image-2026-10-6_10-0-6.png](attachments/image-2026-10-6_10-0-6.png)