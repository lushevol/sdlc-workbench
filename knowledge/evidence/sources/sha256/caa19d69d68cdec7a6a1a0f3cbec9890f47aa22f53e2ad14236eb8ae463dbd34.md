#

# Repos/SDKs

| Item | Purpose | Mandatory |
| --- | --- | --- |
| mfe-root-config | basic foundation of MFE archtect | Yes |
| mfe-base | login page, home page, tiles containers, etc. | Yes |
| single-ui-bff | login, logout, session management. | Yes |
| services-properties | application properties | No |
| Authentication SDK | SDK for service authentication and authorization | Yes |

# Infra

| Item | Purpose | Mandatory | Alternative |
| --- | --- | --- | --- |
| DNS | Entry domain | Yes | |
| Nginx | Traffic proxies | No | Spring proxy |
| Postgresql | tiles, importmaps and categories data | No | Maintains in config |
| Elasticsearch | UI/Backend logs | No | |

# Services Connectivity

| Item | Purpose | Mandatory | Comments |
| --- | --- | --- | --- |
| EMS2 | User entitlements control | Yes | |
| OpenDJ | Account/Credential login | No | Only for non prod |
| OneMFA/Entra | Client SSO | Yes | |
| FMAA | tiles uploading | No | No need upload from API |

# Effort Estimation

This estimation is target to list down all works to be done from RATAN, as planned from FSS they are going to preparing the off board from now on and execution from Q3 till end of year.

![image-2026-5-27_13-9-1.png](attachments/image-2026-5-27_13-9-1.png)![image-2026-5-27_13-11-53.png](attachments/image-2026-5-27_13-11-53.png)

| Works | Estimation | Includes | Not includes |
| --- | --- | --- | --- |
| support & consultant | 10 MD | 1. guidance on architecture - 5MD 2. consultant on questions - 5MD | 1. create/maintains any documents in FSS |
| code base hand over | 10 MD | 1. upload code to FSS repos - 5MD 2. QA on code base - 5MD | 1. uncompleted features or features FSS doesn't used. 2. further commits on code base 3. active services issues handling |
| infra metrics handover | 5 MD | 1. infra servers/db/nginx basic information - 3MD 2. services launching scripts - 2MD | 1. delicate servers/db/nginx from ratan 2. login to ratan servers 3. certifications 4. infra |
| data handover | 2 MD | 1. FSS nginx config (non-prod & prod) - 1MD 2. FSS tiles configs (non-prod & prod) - 1MD | |
| Off boarding FSS | 15 MD | 1. consolidate FSS off boarding impacts. - 5MD 1. any function from portal or services rely on FSS. 2. entitlement control check. 2. clean FSS records & code & configs (non-prod & prod). - 5MD 3. update relavant documents, e.g. design, release calendar, OLA, etc. - 5MD | 1. No more supporting on portal for FSS users. |
| Total | 42MD | | |

Meanwhile, FSS request portal to continually support till fully off board,

## Support Estimation

| Task Area | Estimated Effort | Description | Notes |
| --- | --- | --- | --- |
| **New Onboarding Support** | 20 MD/request | - Guidance & Support & Review (code base setup, tile management, OLA, connectivity checks, intent reviewing, firewall, CR, etc.) - 10MD - Configuration change & supporting - 5MD - Performance Assurance (PT) - 2MD - Regression Testing - 3MD | - Regardless of the tiles count. |
| **New Tiles Onboarding Support** | 5 MD/request | - Guidance & Support & Review - 2MD - Configuration change & supporting - 2MD - Regression Testing - 1MD | |
| **Interoperability Integration** | 10MD/request | - Guidance - 1MD - Interop flow & contract definition - 2MD - development - 5MD - Functional testing - 2MD | |

## Existing Works

| Month | Scheduled Tasks | Scheduled ETA | FSS Delicate Portal Works | Extra ETA |
| --- | --- | --- | --- | --- |
| June | - CDUPS **2 tiles** on boarding - 8MD - FSS **11 tiles** on boarding - 10MD - PTS analysis - 2MD | 20MD - Full | - consulting & supporting - 10MD - code base handover - 10MD - infra metrics handover - 5MD | 25MD |
| July | - Interoperability Ratan ↔ CDUPS go live - 10MD - Entra roll out - 5MD - PTS analysis - 5MD | 20MD - Full |
| August | - PTS on boarding support - 10MD - FSS new tiles - 10MD | 20MD - Full |
| September | - PTS on boarding support - 5MD - CDUPS **4 tiles** on boarding - 5MD - VPA **1 tile** on boarding - 5MD - SSDR **2 tiles** on boarding - 5MD - FSS **2 tiles** on boarding - 5MD | 25MD - Overload |
| October | - FSS **2 tiles** on boarding - 10MD - CDUPS **4 tiles** on boarding - 5MD - PTS on boarding support - 5MD | 20MD - Full | - Data handover - 2MD - FSS off board - 15MD | 17MD |
| November | - SSDR **1 tile** on boarding - 5MD - PTS on boarding support - 15MD | 20MD - Full |
| December | - FSS **1 tile** on boarding - 10MD - PTS on boarding support - 10MD | 20MD - Full |