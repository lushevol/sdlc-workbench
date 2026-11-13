##

## 1. Background

Due to the current policy situation in Indonesia, service data has been deployed in Indonesia.

In Tenant Mode:

- Indonesia-related UI packages are deployed to Indonesian servers as tenants on Post Trade Post.
- Opening an Indonesia tile loads its own container.js and cashflow-blotter.js, mfe-rules, nostro-static.js.
- Indonesian data is accessed through GDC -> ID nginx forwarding.
- Indonesia go-live will use independent CR processes and independent deployment pipelines.

## 2. Cash Settlement Platform

![](https://confluence.global.standardchartered.com/download/attachments/3602757038/image-2026-4-13_16-46-19.png?version=1&modificationDate=1776069980000&api=v2)

## 3. Nginx Flow

### 3.1 GDC - ID Nginx Mapping

| GDC Nginx Env | ID Nginx Env | Set GDC Nginx config | Note |
| --- | --- | --- | --- |
| Dev | STG | ``` # Indonisia location /api/idns/ { rewrite ^/api/idns/(.*)$ /api/$1 break; proxy_redirect off; proxy_set_header Host fmo-mfe-preprod.id.standardchartered.com; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-Proto https; proxy_set_header X-Forwarded-For $remote_addr; proxy_set_header X-Forwarded-Host $remote_addr; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "Upgrade"; proxy_ssl_server_name on; proxy_ssl_name fmo-mfe-preprod.id.standardchartered.com; proxy_ssl_verify off; proxy_pass https://indonisia; } location /static/idns/ { rewrite ^/static/idns/(.*)$ /$1 break; proxy_redirect off; proxy_set_header Host fmo-mfe-preprod.id.standardchartered.com; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-Proto https; proxy_set_header X-Forwarded-For $remote_addr; proxy_set_header X-Forwarded-Host $remote_addr; proxy_ssl_server_name on; proxy_ssl_name fmo-mfe-preprod.id.standardchartered.com; proxy_ssl_verify off; proxy_pass https://indonisia; } upstream indonisia { least_conn; server fmo-mfe-preprod.id.standardchartered.com:8453; } ``` ``` # Indonisia location /api/idns/ { rewrite ^/api/idns/(.*)$ /api/$1 break; proxy_redirect off; proxy_set_header Host uklvadrat0014a.pi.dev.net; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-Proto https; proxy_set_header X-Forwarded-For $remote_addr; proxy_set_header X-Forwarded-Host $remote_addr; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "Upgrade"; proxy_ssl_server_name on; proxy_ssl_name uklvadrat0014a.pi.dev.net; proxy_ssl_verify off; proxy_pass https://indonisia; } location /static/idns/ { rewrite ^/static/idns/(.*)$ /$1 break; proxy_redirect off; proxy_set_header Host uklvadrat0014a.pi.dev.net; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-Proto https; proxy_set_header X-Forwarded-For $remote_addr; proxy_set_header X-Forwarded-Host $remote_addr; proxy_ssl_server_name on; proxy_ssl_name uklvadrat0014a.pi.dev.net; proxy_ssl_verify off; proxy_pass https://indonisia; } upstream indonisia { least_conn; server 10.198.75.20:8453; } ``` | Websocket：http version 1.1 Root Cause: Nginx defaults to forwarding using HTTP/1.0, which does not support WebSocket Upgrade |
| FMRP1 | STG |

### 3.2  URLs Diff

| Type | GDC | ID |
| --- | --- | --- |
| API request | /api/ratan/.. /api/log/ | /api/idns/ratan/... /api/idns/log/ |
| Static JS module | /ratan_container/ratan_container.js /ratan_cashflow_blotter/ratan_cashflow_blotter.js /ratan_rules/ratan_rules.js /ratan_nostro_static/ratan_nostro_static.js | /static/idns/idns_container/idns_container.js /static/idns/idns_cashflow_blotter/idns_cashflow_blotter.js /static/idns/idns_rules/idns_rules.js /static/idns/idns_nostro_static/idns_nostro_static.js |

## 4. ID UI Design

##

### 4.1 ID Route

| Repo | Route |
| --- | --- |
| root-config | @fm/idns_container: "/static/idns/idns_container/idns_container.js", @fm/idns_cashflow_blotter": "/static/idns/idns_cashflow_blotter/idns_cashflow_blotter.js", @fm/idns_ratan_nostro_static: "/static/idns/idns_nostro_static/idns_nostro_static.js", @fm/idns_ratan_rules: "/static/idns/idns_rules/idns_rules.js" |
| ratan-container | /indonesia_cashflow_blotter_cn/*, /indonesia_rules_blotter/*, /indonesia_nostro_static_container/* |
| cashflow-blotter | Cashflow Blotter[ID]: indonesia_cashflow Grouping Blotter[ID]: indonesia_cashflow_group_management Cashflow Dashboard[ID]: indonesia_cashflow_dashboard Authorization Limits[ID]: indonesia_cashflow_authorization_limits BIC Netting Static[ID]: indonesia_cashflow_bic_netting_static_table Nostro Threshold Static[ID]: indonesia_cashflow_splitting_static Utilization Static[ID]: indonesia_cashflow_utilization_static_table |
| mfe-rules | Settlement NSTP Rules New[ID]: indonesia_new_nstp_rules Suppression Rules [Swift][ID]: indonesia_swift_suppression_rules Suppression Rules [Cashflow][ID]: indonesia_cashflow_suppression_rules Netting [ID]: indonesia_new_netting_rules |
| nostro-static | Nostro Static[ID]: indonesia_nostro_static |

### 4.2 Single Repo

Control webpack through environment variables and output GDC and ID packages

package.json  "build": "cross-env REGION=idns concurrently npm:build:*"()

| Changes | Solution | Snapshot | |
| --- | --- | --- | --- |
| Import third-party package | isIdns ? "@fm/idns_container" : "@fm/ratan_container"; This type of import * as RatanContainer from "@fm/ratan_container"; is typically not "bundled" in webpack, but rather "declared as an external dependency and injected at runtime.". | ![image-2026-7-22_14-36-48.png](attachments/image-2026-7-22_14-36-48.png) | |
| Webpack Bundle Name | isIdns ? "idns_container.js" : "ratan_container.js"; | ![image-2026-7-22_14-43-18.png](attachments/image-2026-7-22_14-43-18.png) | UI Repo | GDC JS Bundle | ID JS Bundle | ID Env URL | | --- | --- | --- | --- | | 51358-mfe-ratan-container | ratan_container.js | idns_container.js | [https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_container/idns_container.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_container/idns_container.js) | | 51358-mfe-cashflow-blotter | ratan_cashflow_blotter.js | idns_cashflow_blotter.js | [fmo-mfe-preprod.id.standardchartered.com:8453/idns_cashflow_blotter/idns_cashflow_blotter.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_cashflow_blotter/idns_cashflow_blotter.js) | | 51358-mfe-rules | ratan_rules.js | idns_rules.js | [fmo-mfe-preprod.id.standardchartered.com:8453/idns_rules/idns_rules.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_rules/idns_rules.js) | | 51358-mfe-nostro-static | ratan_nostro_static.js | idns_nostro_static.js | [fmo-mfe-preprod.id.standardchartered.com:8453/idns_nostro_static/idns_nostro_static.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_nostro_static/idns_nostro_static.js) | | |
| UI Repo | GDC JS Bundle | ID JS Bundle | ID Env URL |
| 51358-mfe-ratan-container | ratan_container.js | idns_container.js | [https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_container/idns_container.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_container/idns_container.js) |
| 51358-mfe-cashflow-blotter | ratan_cashflow_blotter.js | idns_cashflow_blotter.js | [fmo-mfe-preprod.id.standardchartered.com:8453/idns_cashflow_blotter/idns_cashflow_blotter.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_cashflow_blotter/idns_cashflow_blotter.js) |
| 51358-mfe-rules | ratan_rules.js | idns_rules.js | [fmo-mfe-preprod.id.standardchartered.com:8453/idns_rules/idns_rules.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_rules/idns_rules.js) |
| 51358-mfe-nostro-static | ratan_nostro_static.js | idns_nostro_static.js | [fmo-mfe-preprod.id.standardchartered.com:8453/idns_nostro_static/idns_nostro_static.js](https://fmo-mfe-preprod.id.standardchartered.com:8453/idns_nostro_static/idns_nostro_static.js) |
| Api prefix | isIdns ? "./.env.idns" : "./.env.global"; API_URL_PREFIX=/api/idns/ratan API_URL_PREFIX=/api/ratan process.env.API_URL_PREFIX | ![image-2026-7-22_14-55-17.png](attachments/image-2026-7-22_14-55-17.png) | |
| IndexedDB(holidayDB) | dbName storeName | ![image-2026-7-22_14-54-31.png](attachments/image-2026-7-22_14-54-31.png) | |
| Add ID storage | businessFieldsCashflowIndonesia | ![image-2026-7-22_14-52-32.png](attachments/image-2026-7-22_14-52-32.png) | |
| Less style | css-in-js style | src/ratancomponents/CustomRow/style.less src/ratancomponents/DataGrid/styles/aggird.less src/ratancomponents/CustomForm/style.less src/ratancomponents/QuickSearchComponents/style.less | ag-grid, ag-grid-angular, ag-grid-ng2, ag-grid-polymer, ag-grid-aurelia { display: block; } textarea[class^="ag-"]:disabled { color: var(--ag-disabled-foreground-color); background-color: var(--ag-input-disabled-background-color); border-color: var(--ag-input-disabled-border-color); } textarea[class^="ag-"]:focus { outline: none; box-shadow: var(--ag-input-focus-box-shadow); border-color: var(--ag-input-focus-border-color); } .group-item { margin: calc(var(--ag-grid-size) * 0.5) 0; } input[class^="ag-"][type="number"]:not( .ag-number-field-input-stepper )::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; } |
| Build | | | |

### 4.3 ID UI Dev

| No | Requirement | Process | |
| --- | --- | --- | --- |
| 1 | ID blotters - booking entity fmid in drop down list should only include ID | | |
| 2 | Dashboard[ID] status cards support open Cashflow Blotter[ID]/Grouping Blotter[ID] | | |
| 3 | Trade blotter - cashflow details button support redirect to GDC and ID based on trade booking entity | | |
| 4 | Global rule sync up from GDC to ID | | [Story 14080720 Indonesia Static Maintenance](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14080720) |
| 5 | ID timezone | | [Story 15226742 Timezone development](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15226742) |
| 6 | Post Trade Portal Tiles Develpoment | | [Story 16097694 Tiles new design and development](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/16097694) |
| 7 | ID view/filter new api url | | |
| 8 | ID netting preview and unnet still use GDC URL | | |

## 5. UI Services

| Service | Branch | Pipeline | FMRP1 Branch | PR | Release Pipeline | Change Points | ENV | IS deployed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 51358-mfe-admin-module | feature/13292993-id | [Pipelines - Run 20260717.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13613438&view=results) rollback: [Pipelines - Run 20260529.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12544397&view=results) | [release/v1.2.](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-admin-module?version=GBrelease/v1.2.2)6 | [Pull request 3394639: Add ID tiles - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-admin-module/pullrequest/3394639) | | add importmap and tiles for ID | GDC | Y |
| 51358-mfe-base | feature/idns | [Pipelines - Run 20260907.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14755776&view=results) | [release/v](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-admin-module?version=GBrelease/v1.2.2)2.2.1 | [Pull request 3394631: Feature/idns - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-base/pullrequest/3394631) | | add handle for ID api handle tiles | GDC | Y |
| 51358-mfe-trades | feature/pre-id | [Pipelines - Run 20260711.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13482474&view=results) | release/v1.16.7 | [Pull request 3394792: ID Change - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-trades/pullrequest/3394792) | | support skip to cashflow blotter id | GDC | |
| 51358-mfe-container | feature/pre-id old: feature/idns | [Pipelines - Run 20260916.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14995578&view=results) | release/v1.8.21.4 | [Pull requests - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-ratan-container/pullrequestcreate?sourceRef=feature/pre-id&targetRef=main&sourceRepositoryId=8891a091-7646-44ea-8a9b-0ff6e5ed7503&targetRepositoryId=8891a091-7646-44ea-8a9b-0ff6e5ed7503) | release pipeline: [Pipelines - Run 20260716.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13587530&view=results) [Pipelines - Run 20260713.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13504830&view=results) TODO:[Pipelines - Run 20260722.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13727898&view=results) | add prefix for url add route for ID enhance global style | ID | Y |
| 51358-mfe-cashflow-blotter | feature/idns | [Pipelines - Run 20260911.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14884983&view=results) | release/v1.48.6 | | | add prefix for url add route for ID | ID | Y |
| 51358-mfe-rules | [feature/](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=12441651&view=results)pre-id | [Pipelines - Run 20260916.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14995450&view=results) GDC：[Pipelines - Run 20260820.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14373680&view=results) waiting new: [Pipelines - Run 20260831.1 logs](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14607368&view=logs&j=2831d33e-84dd-5533-eda0-8105954f1bc8&t=95821634-ff70-5c13-fcfb-9d8a5d21f8ed) | release/v1.9.7 | [Pull requests - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-rules/pullrequestcreate?sourceRef=feature/pre-id&targetRef=main&sourceRepositoryId=7bb74439-c6a3-414f-b5ca-839f5dd86d24&targetRepositoryId=7bb74439-c6a3-414f-b5ca-839f5dd86d24) | [Pipelines - Run 20260824.3](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14447320&view=results) | add prefix for url add route for ID | ID GDC | Y |
| 51358-mfe-nostro-static | feature/idns | [Pipelines - Run 20260910.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=14865824&view=results) | release/v1.2.7 | [Pull requests - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-mfe-nostro-static/pullrequestcreate?sourceRef=feature/13292993-idns&targetRef=main&sourceRepositoryId=d4683f36-9281-4abc-a5e0-2894c693f46c&targetRepositoryId=d4683f36-9281-4abc-a5e0-2894c693f46c) | [Pipelines - Run 20260714.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13520898&view=results) TODO: [Pipelines - Run 20260722.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13728543&view=results) | add prefix for url add route for ID version guard | ID | Y |

### 5.1 ID Pipeline

| | | | |
| --- | --- | --- | --- |
| azure-pipelines-npm.yml | - name: deploymentLocation type: string displayName: deployment area "indonesia" or "global" default: global values: - global - indonesia deploymentLocation: ${{ parameters.deploymentLocation }} | ![image-2026-7-16_11-25-31.png](attachments/image-2026-7-16_11-25-31.png) | [Pipelines - Run 20260716.2](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=13587530&view=results) |