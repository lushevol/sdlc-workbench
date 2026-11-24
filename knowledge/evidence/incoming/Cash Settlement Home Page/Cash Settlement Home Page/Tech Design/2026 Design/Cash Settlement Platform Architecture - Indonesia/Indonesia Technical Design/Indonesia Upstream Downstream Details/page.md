# Surrounding System list

| | Application | SPOC | Integration Type | Comments |
| --- | --- | --- | --- | --- |
| 1 | ENTRA | | API | Firewall not required, not applicable to ID |
| 2 | Stella | Zhou, Hong | SDK | |
| 3 | SSI+ | Patha, Praveen Kumar/1, Prateek/Jitendra Kumar | API, Message | Already provided by Bhuyan, Jitendra Kumar |
| 4 | RDM | Wong, Kelvin Song Hui | API, Message | Firewall not required, ID access RDM API via Kong gateway |
| 5 | MDS | uBawa, Amarnath Balakrishnan | API | |
| 6 | SCI | Wang, Jojo Xue/S, Praveen Bharathi | API | Firewall not required, Ratan→DQSL rt→SCI→BPSI F5 |
| 7 | TDS3 | Dutt, Ankur | API | |
| 8 | Murex2.11 | Liu, Junlin/Ren, Eric Shiyi | Message | Firewall not required, connect to IBMMQ directly for DR, vip information |
| 9 | FM Swift Gateway | Ji, Xiatong | Message | Firewall not required, Ratan→FM Solace→FMSGW→AMH |
| 10 | Ebbs ID | Sargunam, Chandramohan | Message | Firewall not required, Ratan→Central Solace→EBBS ID |
| 11 | DQSL | Wang, Hallie/Zhipeng/Jeady | API | already provided, need double confirm |
| 12 | TLM | Udani, Megha/Saminathan, Rajkannan | API | Firewall not required, TLM→ DQSL service→ Ratan |
| 13 | FMMIS | Lv, Wenjie/Gao, Jing | API | will be decommission? confirmed by Wenjie that they will use SSDR OSV for dashboard |
| 14 | SSDR | Zhang, Cherry Ying | API | Firewall not required, SSDR→ DQSL service→ Ratan |
| 15 | UDP | Feng, Jerry Bin | API | Already provided by Jerry |
| 16 | AMH | Manoharan,Kannan/Gouthaman, Vinoth | Message | Firewall not required, Ratan→FM Solace→FMSGW→AMH |
| 17 | FM Solace | C, Daniel Sebastian | Message | Already provided by Daniel |
| 18 | LMS | Kumar Suriamoorti, Kishor | Message | Firewall not required |
| 19 | TDSX | Li, Rui | | Firewall not required, Not applicable to ID now |
| 20 | FMAA | Balaji, Ts/Biradar, Shivaraj | API | Will be provided by |
| 21 | KONG | | API | **Manifest** |
| 22 | Hashicorp | | API | already have details |
| 23 | IBMMQ | Liu, Junlin/Ren, Eric Shiyi | Message | already have details |
| 24 | EMS2 | Balaji, Ts/Biradar, Shivaraj | API | Will be provided by |
| 25 | EMS3(CES) | Balaji, Ts/Biradar, Shivaraj | API | Will be provided by |
| 26 | ENTERPRISE_SOLACE | Arjunan, Arul Kumar | Message | **Manifest** |
| 27 | ENTERPRISE_SOLACE_EBBS | Arjunan, Arul Kumar | Message | **Manifest** |
| 28 | CDU PS | | API | Firewall not required, not applicable to ID |
| 29 | CIS | | API | Firewall not required, not applicable to ID |
| 30 | FXU | | API | Firewall not required, not applicable to ID for now |

example command: timeout 5 bash -c 'cat < /dev/null > /dev/tcp/[sabre-prod-cloud-global.gdc.standardchartered.com](http://sabre-prod-cloud-global.gdc.standardchartered.com)/31050' && echo "TCP_OK" || echo "TCP_FAIL"

| PROD | Method | system | Description | Source | Destination Host（PROD） （What we used in config file) | Destination Port（PROD） （What we used in config file) | Need to open firewall by NSSR or Manifest | Connection Hosts （PROD） (spoc provided to open firewall, include IP, VIP) | Connection Port（PROD） (spoc provided to open firewall) | TCP | host（STG） | port（STG） | SPOC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| up stream | api call | SSI | query on this | RATAN new SRACK servers with subnet 10.29.40.128/26; 10.29.32.128/26; 10.125.4.0/25; 10.124.4.0/25 | 10.193.230.157:9200,10.193.230.158:9200 | 9200 | NSSR | | | | 10.198.37.147,10.198.37.148 | 9200 | Patha, Praveen Kumar/1, Prateek |
| TDS3 | Trade query on LIEN, NDS | TDS3_ENV: tlprod TDS3_ACCOUNT: ${FMAA_ACCOUNT} [https://sabre-prod-cloud-global.gdc.standardchartered.com](https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-tdsx-service/prod/auth/TDSXQuery) 10.4.162.236 | 443 | | | | | | Dutt, Ankur |
| Stella | Stella cashflow status write back | STELLA_ENV: prod STELLA_ACCOUNT: RATAN_PROD [uklpapsab165a.gdc.standardchartered.com](http://uklpapsab165a.gdc.standardchartered.com):9093, [uklpapsab166a.gdc.standardchartered.com](http://uklpapsab166a.gdc.standardchartered.com):9093, [uklpapsab167a.gdc.standardchartered.com](http://uklpapsab167a.gdc.standardchartered.com):9093· [uklpapsab165b.gdc.standardchartered.com](http://uklpapsab165b.gdc.standardchartered.com):9093, [uklpapsab166b.gdc.standardchartered.com](http://uklpapsab166b.gdc.standardchartered.com):9093, [uklpapsab167b.gdc.standardchartered.com](http://uklpapsab167b.gdc.standardchartered.com):9093 | 9093 | | | | | | zhou, hong pss: SABRE PSS <S[ABREPSS@sc.com](mailto:ABREPSS@sc.com)> devops: [SABREDevOps@exchange.standardchartered.com](mailto:SABREDevOps@exchange.standardchartered.com) |
| TDSX | | [sabre-prod-cloud-global.gdc.standardchartered.com](http://sabre-prod-cloud-global.gdc.standardchartered.com) | 31050 | | | TCP_FAIL | [https://](https://sabre-dev-cloud-global.uk.standardchartered.com/fmrp-tdsx-service/stage/auth/TDSXQuery)[sabre-dev-cloud-global.uk.standardchartered.com](http://sabre-dev-cloud-global.uk.standardchartered.com) | 31068 | li, Rui |
| SABRE | | [https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-fx-fxcs/prod/rate/{date}/OFFICIAL_EOD/USD](https://sabre-prod-cloud-global.gdc.standardchartered.com/fmrp-fx-fxcs/prod/rate/%7Bdate%7D/OFFICIAL_EOD/USD) | 443 | | | | | | |
| MDS | | [https://mds-api.gdc.standardchartered.com](https://mds-api.gdc.standardchartered.com) | 443 | | | TCP_FAIL | [https://dev-cloud-1.uk.standardchartered.com](https://dev-cloud-1.uk.standardchartered.com) | 30758 | uBawa, Amarnath Balakrishnan |
| DQSL | legal entity query FM code | [api-dqslrt.gdc.standardchartered.com](http://api-dqslrt.gdc.standardchartered.com) [dqsl.gdc.standardchartered.com](http://dqsl.gdc.standardchartered.com) | 443 | | | | | | Wang, Hallie |
| FMAA | services account authentication | [https://fmaaprod.gdc.standardchartered.com/v1/fmaa/oauth2](https://fmaaprod.gdc.standardchartered.com/v1/fmaa/oauth2) | | | | | | | Balaji, Ts/Biradar, Shivaraj |
| KONG | | [https://gateway.51242.app.standardchartered.com](https://gateway.51242.app.standardchartered.com/) | 443/8443 | Manifest | `- sourceitam: 51358 sourceinfra: LAN destinationitam: 51242 destinationinfra: LAN destinationservice: FD` | | | | | |
| RDM (Used KONG api to cover) | | | | | | | | | Wong, Kelvin, Song Hui |
| Hashicorp | For application call Hashicorp API to retrieve account details. Hashicorp firewall is opened during VM setup as mentioned by network team. But in case anything missed, we need to raise firewall request to make sure connection works | [https://vault.global.standardchartered.com:8200](https://vault.global.standardchartered.com:8200) | 8200 | NSSR | 10.4.38.167 10.95.202.147 10.95.202.148 10.92.202.142 10.92.202.143 | 8200 | | | | |
| middleware | IBMMQ | MUREX | 10.4.195.209 | 8210 | | | | | [ukfm02p1-0.50974.app.standardchartered.com](http://ukfm02p1-0.50974.app.standardchartered.com) | 8233 | Liu, Junlin/Ren, Eric Shiyi |
| ENTERPRISE_SOLACE (REAL TIME) | RDM | [smfs://vpn-rd-data-p1-0-a-prd.51080.app.standardchartered.com:55443,](smfs://vpn-rd-data-p1-0-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-rd-data-p1-0-b-prd.51080.app.standardchartered.com:55443) [smfs://vpn-rd-data-p1-0-b-prd.51080.app.standardchartered.com](smfs://vpn-rd-data-p1-0-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-rd-data-p1-0-b-prd.51080.app.standardchartered.com:55443) | [55443](smfs://vpn-rd-data-p1-0-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-rd-data-p1-0-b-prd.51080.app.standardchartered.com:55443) | **Manifest** | `- sourceitam: 51358 sourceinfra: LAN destinationitam: 51080 destinationinfra: LAN destinationservice: FD` | | TCP_FAIL | smfs://[vpn-rd-data-p1-0-a-0.51080.app.standardchartered.com](http://vpn-rd-data-p1-0-a-0.51080.app.standardchartered.com)[,](smfs://hk-np1.fs-solace.dev.net:55443,smfs://hk-np2.fs-solace.dev.net:55443) [vpn-rd-data-p1-0-b-0.51080.app.standardchartered.com](http://vpn-rd-data-p1-0-b-0.51080.app.standardchartered.com) | [55443](smfs://ukxpiusol12av1.uk.standardchartered.com:55443,smfs://ukxpiusol3av1.uk.standardchartered.com:55443) | |
| EMS3(CES) | data entitlement query | [https://fmcesprod.gdc.standardchartered.com](https://fmcesprod.gdc.standardchartered.com) | 443 | NSSR | | | TCP_FAIL | [https://fmcesuat.gdc.standardchartered.com](https://fmcesuat.gdc.standardchartered.com) | 443 | Balaji, Ts/Biradar, Shivaraj |
| EMS2(Sabre) | functional entitlement query | [https://sabre-prod-ems2.gdc.standardchartered.com](https://sabre-prod-ems2.gdc.standardchartered.com:16443) | [16443](https://sabre-prod-ems2.gdc.standardchartered.com:16443) | NSSR | | | TCP_FAIL | [https://uklvauems01a.uk.standardchartered.com](https://uklvauems01a.uk.standardchartered.com:16443) | [16443](https://uklvauems01a.uk.standardchartered.com:16443) | Balaji, Ts/Biradar, Shivaraj |
| FM SOLACE | Uber flow/ Send Swift Msg( MT/MX)/Trade/ Cashflow/FXU/ SSI+ /BPMI/ Razor Status write back (loanIQ)/CDU PS Trade/ BCS Confirmation | [smfs://ukxpipsol12av1.uk.standardchartered.com](smfs://ukxpipsol12av1.uk.standardchartered.com:55443,smfs://ukxpipsol12bv1.uk.standardchartered.com:55443) [smfs://ukxpipsol12bv1.uk.standardchartered.com](smfs://ukxpipsol12av1.uk.standardchartered.com:55443,smfs://ukxpipsol12bv1.uk.standardchartered.com:55443) | [55443](smfs://ukxpipsol12av1.uk.standardchartered.com:55443,smfs://ukxpipsol12bv1.uk.standardchartered.com:55443) | NSSR | | **Environment** | ** HostName ** | **IP and Port** | | --- | --- | --- | | Prod | [ukxpipsol12av1.uk.standardchartered.com](http://ukxpipsol12av1.uk.standardchartered.com/) | 10.193.68.50:55443 | | DR | [ukxpipsol12bv1.uk.standardchartered.com](http://ukxpipsol12bv1.uk.standardchartered.com/) | 10.192.82.50:55443 | | Prod HA | [ukxpipsol12av2.uk.standardchartered.com](http://ukxpipsol12av2.uk.standardchartered.com/) [ukxpipsol12bv2.uk.standardchartered.com](http://ukxpipsol12bv2.uk.standardchartered.com/) | 10.193.68.52:55443 10.192.82.52:55443 | | Country | Tagged to Service | Hostname | Environment | DC | Management IP | Domain of Management IP | Domain VIP | | --- | --- | --- | --- | --- | --- | --- | --- | | UK | FM SOLACE | ukxpipsol01a | Prod | ARK | 10.4.14.139 | <u>[ukxpipsol01a-mgmt.uk.standardchartered.com](http://ukxpipsol01a-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12av1.uk.standardchartered.com](http://ukxpipsol12av1.uk.standardchartered.com/)</u> | | UK | FM SOLACE | ukxpipsol02a | Prod | ARK | 10.4.14.140 | <u>[ukxpipsol02a-mgmt.uk.standardchartered.com](http://ukxpipsol02a-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12av2.uk.standardchartered.com](http://ukxpipsol12av2.uk.standardchartered.com/)</u> | | UK | FM SOLACE | ukxpipsol01b | Prod - DR | WF | 10.192.42.239 | <u>[ukxpipsol01b-mgmt.uk.standardchartered.com](http://ukxpipsol01b-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12bv1.uk.standardchartered.com](http://ukxpipsol12bv1.uk.standardchartered.com/)</u> | | UK | FM SOLACE | ukxpipsol02b | Prod - DR | WF | 10.192.42.243 | <u>[ukxpipsol02b-mgmt.uk.standardchartered.com](http://ukxpipsol02b-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12bv2.uk.standardchartered.com](http://ukxpipsol12bv2.uk.standardchartered.com/)</u> | | | TCP_FAIL | [smfs://ukxpiusol12av1.uk.standardchartered.com,](smfs://ukxpiusol12av1.uk.standardchartered.com:55443,smfs://ukxpiusol3av1.uk.standardchartered.com:55443) [smfs://ukxpiusol3av1.uk.standardchartered.com](smfs://ukxpiusol12av1.uk.standardchartered.com:55443,smfs://ukxpiusol3av1.uk.standardchartered.com:55443) | 55443 | C, Daniel Sebastian |
| **Environment** | ** HostName ** | **IP and Port** |
| Prod | [ukxpipsol12av1.uk.standardchartered.com](http://ukxpipsol12av1.uk.standardchartered.com/) | 10.193.68.50:55443 |
| DR | [ukxpipsol12bv1.uk.standardchartered.com](http://ukxpipsol12bv1.uk.standardchartered.com/) | 10.192.82.50:55443 |
| Prod HA | [ukxpipsol12av2.uk.standardchartered.com](http://ukxpipsol12av2.uk.standardchartered.com/) [ukxpipsol12bv2.uk.standardchartered.com](http://ukxpipsol12bv2.uk.standardchartered.com/) | 10.193.68.52:55443 10.192.82.52:55443 |
| Country | Tagged to Service | Hostname | Environment | DC | Management IP | Domain of Management IP | Domain VIP |
| UK | FM SOLACE | ukxpipsol01a | Prod | ARK | 10.4.14.139 | <u>[ukxpipsol01a-mgmt.uk.standardchartered.com](http://ukxpipsol01a-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12av1.uk.standardchartered.com](http://ukxpipsol12av1.uk.standardchartered.com/)</u> |
| UK | FM SOLACE | ukxpipsol02a | Prod | ARK | 10.4.14.140 | <u>[ukxpipsol02a-mgmt.uk.standardchartered.com](http://ukxpipsol02a-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12av2.uk.standardchartered.com](http://ukxpipsol12av2.uk.standardchartered.com/)</u> |
| UK | FM SOLACE | ukxpipsol01b | Prod - DR | WF | 10.192.42.239 | <u>[ukxpipsol01b-mgmt.uk.standardchartered.com](http://ukxpipsol01b-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12bv1.uk.standardchartered.com](http://ukxpipsol12bv1.uk.standardchartered.com/)</u> |
| UK | FM SOLACE | ukxpipsol02b | Prod - DR | WF | 10.192.42.243 | <u>[ukxpipsol02b-mgmt.uk.standardchartered.com](http://ukxpipsol02b-mgmt.uk.standardchartered.com/)</u> | <u>[ukxpipsol12bv2.uk.standardchartered.com](http://ukxpipsol12bv2.uk.standardchartered.com/)</u> |
| ENTERPRISE_SOLACE_EBBS | EBBS and RDM | [smfs://vpn-cb-transactions-p1-1-a-prd.51080.app.standardchartered.com](smfs://vpn-cb-transactions-p1-1-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-cb-transactions-p1-1-b-prd.51080.app.standardchartered.com:55443) [smfs://vpn-cb-transactions-p1-1-b-prd.51080.app.standardchartered.com](smfs://vpn-cb-transactions-p1-1-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-cb-transactions-p1-1-b-prd.51080.app.standardchartered.com:55443) | [55443](smfs://vpn-cb-transactions-p1-1-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-cb-transactions-p1-1-b-prd.51080.app.standardchartered.com:55443) | **Manifest** | `- sourceitam: 51358 sourceinfra: LAN destinationitam: 51080 destinationinfra: LAN destinationservice: FD` | | TCP_FAIL | [smfs://vpn-cb-transactions-p1-stg.51080.app.standardchartered.com](smfs://vpn-cb-transactions-p1-stg.51080.app.standardchartered.com) | [55443](smfs://vpn-cb-transactions-p1-1-a-prd.51080.app.standardchartered.com:55443,smfs://vpn-cb-transactions-p1-1-b-prd.51080.app.standardchartered.com:55443) | |
| down stream | | FMDP and EOD servers | existing GDC downstream as source group of policy **CIB_FM_CJ_51358_EPG_SVR_IN** | 10.4.162.0/24, 10.5.160, 10.5.142.0/24, 10.4.142.0/24, 10.4.162.0/24, 10.4.139.0/24 | Add RATAN new SRACK servers with subnet 10.29.40.128/26; 10.29.32.128/26; 10.125.4.0/25; 10.124.4.0/25 into the destination group **CIB_FM_CJ_51358_EPG** of policy **CIB_FM_CJ_51358_EPG_SVR_IN** | 8453 | NSSR | | | | | | |
| CDU PS | 10.4.206.0/24 | 8453 | | | | | | |
| CIS | 10.193.231.0/24 | 8453 | | | | | | |
| FSS | 10.5.178.32, 10.5.178.34 | 8453 | | | | | | |
| SSI+ | 10.4.39.240 | 8453 | | | | | | |
| LoanIQ | 10.4.40.115 | 8453 | | | | | | |
| FXU | 10.192.226.91, 10.192.227.220, 10.192.227.212, 10.192.227.210, 10.192.227.162, 10.4.178.17, 10.192.226.61, 10.192.227.221, 10.192.227.213, 10.192.227.211, 10.192.227.163, 10.4.178.26 | 8453 | | | | | | |
| DB servers | | Hashicorp | Hashicorp for DB servers: Hashicorp source group of policy **CIB_FM_CJ_51358_EPG_SVR_IN** | Add below into **CIB_FM_CJ_51358_EPG_SVR_SRC_GRP** 10.92.202.0/24 10.95.202.0/24 | Add RATAN new SRACK DB servers with subnet 10.29.46.128/25; 10.29.38.128/25; 10.125.2.0/24; 10.124.2.0/24 into the destination group **CIB_FM_CJ_51358_EPG** of policy **CIB_FM_CJ_51358_EPG_SVR_IN** | 6524 | | | | | | |
| control-m | | | No extra actions as long as new servers added into destination groups with above steps | | | 7006 | | | | | | |
| DBA health check server | | | | no change | Add RATAN new SRACK DB servers with subnet 10.29.46.128/25; 10.29.38.128/25; 10.125.2.0/24; 10.124.2.0/24 into the destination group **CIB_FM_CJ_51358_EPG_SSH_SVR_DST_GRP** | 22 | | | | | | |

For GDCW brown applications if there is no specific network segmentation added on the application, we can use pseudo application 98503 for GDCW.

**Manifest need to update in 98503 firewall_mf.yml**
- sourceitam: 98503 #GDCW
    sourceinfra: LAN
    destinationitam: 51358 #RATAN SRACK
    destinationinfra: LAN
    destinationservice: FD

**Manifest need to update in 51358 firewall_mf.yml**
`- sourceitam: 51358
sourceinfra: LAN
destinationitam: 98503
destinationinfra: LAN
destinationservice: FD`