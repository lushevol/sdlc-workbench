### Type of Access control

MFA/EMS2

### Access Groups

| Group Name | Description | Type of Access control | Owner | Status | Remarks |
| --- | --- | --- | --- | --- | --- |
| SGZ1-CentrifyRole-Users-UK-PROD-Ratan | To access RATAN ONE Unix servers | AD Group | 1500342-dev | | |
| SUZ1-USER-WEST_CM-RATAN_OPR | RATAN ONE Control-M Jobs | AD Group | Gevin | | |
| SUZ1-APP-WEBSSPROD-RATAN-PSS | For RATAN One Rundeck jobs | AD Group | Gevin | | |
| SGZ1-CentrifyRole-Comp-UK-PROD-Ratan | Centrify Unix computer user group | AD Group | | | |

### PID List

| PID Name | Description | Vaulted Yes/No | Vaulted(OneVault or Hashicorp) | Owner | Status | Remarks |
| --- | --- | --- | --- | --- | --- | --- |
| ratanrt | Linux -Prod server account | non interactive | | | | |
| ratansup | Linux -Prod server account，same group as ratanrt | Yes | OneVault | | | not in use |
| itrs | Linux -ITRS account | Yes | OneVault | | | |
| ratanprd_003 | DB account -Application | Yes | OneVault | | | 13 Jul 2024 all services interaction with ratanprd_001, this is not used anymore |
| ratanprd_001 | DB account -Application | Yes | Hashicorp | | | |
| ratanone_dmp | DB account -Readonly Prod | Yes | Hashicorp | | | |
| svc.ratanone.001 | AD account-DQSL API authentication connection by RATAN | Yes | Hashicorp | | | |
| srv.51358.ratanone.001 | OUD account for SOLACE | Yes | Hashicorp | | | |
| ratan_prod | OUD account for FMAA | Yes | Hashicorp | | | |
| ratan_edmi_prod | OUD account to connect Kong API | Yes | Hashicorp | | | |
| nginxadm | Linux - web team | Yes | OneVault | | | belong to Web BAU team |
| ~~nginx~~ | | ~~Yes~~ | ~~OneVault~~ | | | ~~seems not in use, pending checking~~ |
| ratan_archive | DB account -Application | Yes | Hashicorp | | | |
| ratan_ac_pss | DB account -Readonly Prod | Yes | Hashicorp | | | |
| ratan_ac_dmp | DB account -Readonly Prod | Yes | Hashicorp | | | |
| ratan_common | DB account -Application | Yes | Hashicorp | | | |
| ratan_com_pss | DB account -Readonly Prod | Yes | Hashicorp | | | |
| ratan_com_dmp | DB account -Readonly Prod | Yes | Hashicorp | | | |
| ratanone_id | Indonesia DB account -Application | Yes | Hashicorp | | | |
| ratanone_dmp | Indonesia DB account -Readonly Prod | Yes | Hashicorp | | | |
| ratanone_pss | Indonesia DB account -Readonly Prod | Yes | Hashicorp | | | |

### Certificate Type & Details

EJBCA / MSPKI

[Login - AppViewX](https://instacertclm.50962.app.standardchartered.com:31443/appviewx/login) to check cert info

| Group | Certificate Authority | Certificate Name | Issue Date | Expiry Date | Validity | Serial No | App Name | Host Name | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 51358 | Microsoft Enterprise | 51358-ratan | 7/16/2024 | 7/16/2026 | Valid | 56000053063FFEECD87C554936000000005306 | RATAN | uklvasapp590,uklvasapp591,uklvapapp590,uklvapapp590,uklvapapp591,uklvapapp676,uklvapapp591,uklvapapp676,uklvasapp676 | for RATAN integration with Enterprise Solace and Hashicorp where RATAN as client |
| ~~51358~~ | ~~Ejbca~~ | ~~[fmo-shell.gdc.standardchartered.com](http://fmo-shell.gdc.standardchartered.com)~~ | ~~4/27/2023~~ | ~~4/26/2025~~ | ~~Expired~~ | ~~6C265EC9587AE111~~ | ~~RATAN~~ | ~~uklvasapp676,uklvapapp591,uklvapapp590,uklvasapp591,uklvasapp590,uklvapapp676~~ | |
| ~~51358~~ | ~~Ejbca~~ | ~~[fmo-shell.gdc.standardchartered.com](http://fmo-shell.gdc.standardchartered.com)~~ | ~~8/23/2022~~ | ~~8/22/2024~~ | ~~Expired~~ | ~~660AFA9756AB3FD2~~ | ~~RATAN~~ | ~~uklvasapp676,uklvapapp591,uklvapapp590,uklvasapp591,uklvasapp590,uklvapapp676~~ | |
| 51358 | Microsoft Enterprise | [fmo-shell.gdc.standardchartered.com](http://fmo-shell.gdc.standardchartered.com) | 11/1/2024 | 11/1/2026 | Valid | 560000659E585CFC61BBC2C25500000000659E | RATAN | uklvasapp676,uklvapapp591,uklvapapp590,uklvasapp591,uklvasapp590,uklvapapp676 | RATAN https certificate where RATAN as server |
| ~~51358~~ | ~~Ejbca~~ | ~~[ratan.gdc.standardchartered.com](http://ratan.gdc.standardchartered.com)~~ | ~~7/22/2020~~ | ~~7/22/2022~~ | ~~Expired~~ | ~~5235992A220767EE~~ | ~~RATAN~~ | ~~uklvapapp676,uklvasapp676~~ | |
| 51358 | Microsoft Enterprise | [ratan-stella.gdc.standardchartered.com](http://ratan-stella.gdc.standardchartered.com) | 7/16/2024 | 7/16/2026 | Valid | 56000053050356DE4730E83F74000000005305 | RATAN | uklpapsab165a,uklpapsab166b,uklpapsab166a,uklpapsab165b,uklpapsab167b,uklpapsab167a | for RATAN integration with STELLA SDK where RATAN as client |