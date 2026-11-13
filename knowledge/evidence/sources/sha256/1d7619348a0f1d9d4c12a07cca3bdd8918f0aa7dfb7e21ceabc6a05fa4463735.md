# Project Scan Cost Estimation

This estimation calculates the cost to fully review all codebases in the provided repo list using the same LLM review algorithm as PR reviews.

## Algorithm Recap

- Token count = repos code character length / 4
- Review input tokens per repo = repos code token count + 1000
- Review output tokens per repo = 900
- Cost per token ≈ $0.00000926 (Cluade-4-Sonnet)
- Final cost = base cost × (0.75 + 0.25 + 0.18) = base cost × 1.18

## Repo Data Summary

- Number of repos: 90
- Total repo code character count: 173,156,375
- Total repo code token count: 43,289,093.75
- Total reviewable token count (Removed not eligible for review): 18,867,521.8

## Calculation

- Total input tokens: 18,867,521.8 + 80,000 = 18,947,521.8
- Total output tokens: 900 × 80 = 72,000
- Total tokens: 18,947,521.8 + 72,000 = 19019521.8
- Estimated cost: 43,460,093.75 × $0.00000926 = $176.12
- Final cost (with supporting/foundation/cloud engineering): $176.12 × 1.18 ≈ $207.8

## Summary Table

| Item | Value |
| --- | --- |
| Number of repos | 80 |
| Total code char count | 173,156,375 |
| Total code token count | 43,289,093.75 |
| Total input tokens | 43,379,093.75 |
| Total output tokens | 72,000 |
| Total tokens | 19019521.8 |
| Estimated cost | $207.8 |

## Detailed Repo Cost Table

| Repo Name | Size (chars) | Token Count | Cost (USD) |
| --- | --- | --- | --- |
| 51358-mfe-admin-module | 54241 | 13560.25 | 0.125567915 |
| 51358-mfe-authorization-limits | 1276298 | 319074.5 | 2.9546298699999998 |
| 51358-mfe-base | 5605487 | 1401371.75 | 12.976702405 |
| 51358-mfe-cashflow | 5064501 | 1266125.25 | 11.724319815 |
| 51358-mfe-cashflow-blotter | 3847099 | 961774.75 | 8.906034185 |
| 51358-mfe-exception | 2043689 | 510922.25 | 4.731140035 |
| 51358-mfe-nostro-static | 1360253 | 340063.25 | 3.148985695 |
| 51358-mfe-ratan-config-management | 5418 | 1354.5 | 0.012542669999999999 |
| 51358-mfe-ratan-container | 5070228 | 1267557 | 11.737577819999998 |
| 51358-mfe-ratan-graphql-java-poc | 2543 | 635.75 | 0.005887045 |
| 51358-mfe-ratan-graphql-ui-poc | 4997 | 1249.25 | 0.011568054999999999 |
| ~~51358-mfe-ratan-starter~~ | ~~24774388~~ | ~~6193597~~ | ~~57.35270822~~ |
| ~~51358-mfe-root-config~~ | ~~11315435~~ | ~~2828858.75~~ | ~~26.195232025~~ |
| 51358-mfe-rule-core | 5418 | 1354.5 | 0.012542669999999999 |
| 51358-mfe-rules | 1983589 | 495897.25 | 4.592008535 |
| 51358-mfe-template-container | 1015719 | 253929.75 | 2.351389485 |
| 51358-mfe-template-tiles | 1360934 | 340233.5 | 3.15056221 |
| 51358-mfe-trades | 5824711 | 1456177.75 | 13.484205965 |
| 51358-ratan-agents | 24061 | 6015.25 | 0.055701215 |
| 51358-ratan-cashflow-lifecycle-service | 3189161 | 797290.25 | 7.382907715 |
| 51358-ratan-cash-settlement-accounting-service | 794173 | 198543.25 | 1.838510495 |
| 51358-ratan-cash-settlement-batch-service | 336646 | 84161.5 | 0.7793354899999999 |
| 51358-ratan-cash-settlement-fx-utilization-service | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratan-cash-settlement-group-management-service | 1221518 | 305379.5 | 2.82781417 |
| 51358-ratan-cash-settlement-lms-service | 1145868 | 286467 | 2.65268442 |
| 51358-ratan-cash-settlement-netting-service | 1187326 | 296831.5 | 2.7486596899999998 |
| 51358-ratan-cash-settlement-nstp-service | 2543 | 635.75 | 0.005887045 |
| 51358-ratan-cash-settlement-orchestration | 300635 | 75158.75 | 0.6959700249999999 |
| 51358-ratan-cash-settlement-query-service | 1525762 | 381440.5 | 3.5321390299999997 |
| 51358-ratan-cash-settlement-ssi-stamping-service | 3809361 | 952340.25 | 8.818670715 |
| 51358-ratan-cash-settlement-swift-service | 2651 | 662.75 | 0.006137065 |
| 51358-ratan-central-monitoring | 2761 | 690.25 | 0.006391714999999999 |
| ~~51358-rataneod-enduser-megaview~~ | ~~5061456~~ | ~~1265364~~ | ~~11.717270639999999~~ |
| ~~51358-ratan-eod-hcp-tool~~ | ~~51563~~ | ~~12890.75~~ | ~~0.11936834499999999~~ |
| ~~51358-ratan-eod-report-converter~~ | ~~92205~~ | ~~23051.25~~ | ~~0.21345457499999998~~ |
| ~~51358-rataneod-stella-data-handler~~ | ~~217444~~ | ~~54361~~ | ~~0.50338286~~ |
| 51358-ratan-ever-telligent-engine-service | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratan-exception-platform | 449752 | 112438 | 1.04117588 |
| 51358-ratan-market-workflow-service | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratan-mxg-cashflow-adaptor | 936466 | 234116.5 | 2.16791879 |
| 51358-ratanone-ado-templates | 184488 | 46122 | 0.42708971999999995 |
| ~~51358-ratanone-ansible~~ | ~~3312579~~ | ~~828144.75~~ | ~~7.668620385~~ |
| ~~51358-ratanone-api-auto-test-cases~~ | ~~1342131~~ | ~~335532.75~~ | ~~3.1070332649999997~~ |
| 51358-ratanone-api-gateway | 232740 | 58185 | 0.5387930999999999 |
| 51358-ratanone-api-hub | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratanone-audit-trial | 169323 | 42330.75 | 0.39198274499999997 |
| 51358-ratanone-auth-server | 275604 | 68901 | 0.63802326 |
| ~~51358-ratanone-autotest-api-cn~~ | ~~48989225~~ | ~~12247306.25~~ | ~~113.410055875~~ |
| ~~51358-ratanone-auto-test-cases~~ | ~~4520~~ | ~~1130~~ | ~~0.010463799999999999~~ |
| 51358-ratanone-backend-deployment | 2655 | 663.75 | 0.006146324999999999 |
| 51358-ratanone-business-functions | 46608 | 11652 | 0.10789752 |
| 51358-ratanone-ca-control-service | 569304 | 142326 | 1.3179387599999999 |
| 51358-ratanone-capacity-monitor | 140935 | 35233.75 | 0.32626452499999997 |
| 51358-ratanone-cashflow-service | 3070257 | 767564.25 | 7.107644955 |
| 51358-ratanone-command | 41108 | 10277 | 0.09516501999999999 |
| 51358-ratanone-config-server | 73872 | 18468 | 0.17101368 |
| 51358-ratanone-confirmation-orchestration | 94269 | 23567.25 | 0.21823273499999998 |
| 51358-ratanone-controlm | 148132 | 37033 | 0.34292557999999995 |
| 51358-ratanone-data-ambassador | 819847 | 204961.75 | 1.897945805 |
| 51358-ratanone-data-provider-external-client | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratanone-data-provider-internal-client | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratanone-db-repository | 45780 | 11445 | 0.1059807 |
| 51358-ratanone-db-rest | 127134 | 31783.5 | 0.29431521 |
| 51358-ratanone-devops | 2308 | 577 | 0.0053430199999999995 |
| 51358-ratanone-eureka-server | 57776 | 14444 | 0.13375144 |
| 51358-ratanone-exception-service | 448888 | 112222 | 1.03917572 |
| 51358-ratanone-external-component-simulator | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratanone-field-management | 4997 | 1249.25 | 0.011568054999999999 |
| 51358-ratanone-foundation | 1902635 | 475658.75 | 4.404600025 |
| 51358-ratanone-frontend-deployment | 2655 | 663.75 | 0.006146324999999999 |
| 51358-ratanone-grpc-api | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratanone-helm | 2193 | 548.25 | 0.005076794999999999 |
| 51358-ratanone-internal-component-simulator | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratanone-kafka-monitor | 2651 | 662.75 | 0.006137065 |
| 51358-ratanone-message-bridge | 661466 | 165366.5 | 1.5312937899999999 |
| 51358-ratanone-message-event | 465494 | 116373.5 | 1.07761861 |
| 51358-ratanone-notification-service | 208686 | 52171.5 | 0.48310809 |
| 51358-ratanone-opensearch-agent | 2761 | 690.25 | 0.006391714999999999 |
| ~~51358-ratanone-performancetest-api~~ | ~~607119~~ | ~~151779.75~~ | ~~1.405480485~~ |
| 51358-ratanone-query-service | 659494 | 164873.5 | 1.52672861 |
| 51358-ratanone-recon-service | 2651 | 662.75 | 0.006137065 |
| 51358-ratanone-rule-service | 2651169 | 662792.25 | 6.137456234999999 |
| 51358-ratanone-security-matrix | 246429 | 61607.25 | 0.5704831349999999 |
| 51358-ratanone-service | 51790 | 12947.5 | 0.11989385 |
| 51358-ratanone-settlement-orchestration | 217533 | 54383.25 | 0.5035888949999999 |
| 51358-ratanone-stamping-service | 1629918 | 407479.5 | 3.77326017 |
| 51358-ratanone-static-data-service | 1489021 | 372255.25 | 3.447083615 |
| 51358-ratanone-stella-ambassador | 446801 | 111700.25 | 1.034344315 |
| 51358-ratanone-suppression-service | 1753395 | 438348.75 | 4.059109425 |
| 51358-ratanone-swift-service | 3246899 | 811724.75 | 7.516571184999999 |
| 51358-ratanone-tech-share | 2208 | 552 | 0.00511152 |
| ~~51358-ratanone-test-case-portal~~ | ~~1303737~~ | ~~325934.25~~ | ~~3.018151155~~ |
| 51358-ratanone-trade-control-service | 309932 | 77483 | 0.7174925799999999 |
| 51358-ratanone-trade-service | 1397496 | 349374 | 3.2352032399999997 |
| 51358-ratanone-vendor-package | 30975 | 7743.75 | 0.071707125 |
| ~~51358-ratanone-yangjian~~ | ~~614486~~ | ~~153621.5~~ | ~~1.42253509~~ |
| 51358-ratan-rule-service | 1453088 | 363272 | 3.36389872 |
| 51358-ratan-service-gui-bff | 584931 | 146232.75 | 1.354115265 |
| 51358-ratan-service-properties | 2193 | 548.25 | 0.005076794999999999 |
| 51358-ratan-task-service | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratan-test-helper-api | 2761 | 690.25 | 0.006391714999999999 |
| 51358-ratan-test-helper-ui | 5418 | 1354.5 | 0.012542669999999999 |
| Total | 173156375 | *43289093.75 - 24421572 = *18,867,521.8 | *400.857008125 - 224.82 = ***176.037** |

## Conclusion

To fully review all codebases in all ratan repo list using the same LLM review algorithm, the estimated cost would be approximately **$207.8** (one-time, not monthly), assuming linear scaling and the same pricing as PR review estimation.