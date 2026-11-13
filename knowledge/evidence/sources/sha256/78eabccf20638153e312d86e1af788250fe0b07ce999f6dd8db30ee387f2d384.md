Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta | 2026-01-28 | @Yunzhe Ta @Jie Cai | 2026-01-29 | |

### Description:

This is for hashicorp integration following bank policy. HashiCorp Vault is an integrated **secrets management solution** that provides programmatic & dynamic access to the credentials at run time.

| Application Name | Control-M Job Name | Description |
| --- | --- | --- |
| RATAN | RATAN_FULL_HCV(parent folder) | for monthly enable hashicorp, VIP and clusters on all servers **(Mar, Jul, Nov**) |
| | RAT_HCV_CHECK | check all hashicorp account rotate info |
| | RAT_HCV_REFRESH | refresh all hashicorp account to Redis |
| | RAT_HCV_ROTATE | rotate all hashicorp account |
| | RAT_RESTART_ALL_SERV_HCV | Restart VIP and the whole clusters from ARK servers |
| | RAT_STOP_ALL_SERV_HCV | Stop all services on whole cluster |

**![image-2026-1-30_9-19-56.png](attachments/image-2026-1-30_9-19-56.png)**

**All Hashicorp accounts:**

**DB **ratanone_ratanprd_003 ratanprd_003
**DB **ratanone_ratanprd_001 ratanprd_001
**DB **ratanone_ratanone_dmp ratanone_dmp
**AD **svc.ratanone.001
**OUD **srv.51358.ratanone.001
**OUD **ratan_prod
**OUD **ratan_edmi_prod

### E2E Data Flow:

RATAN implements a secure, two-phase credential lifecycle:

**(1)  ****rotate **— the ratan_hashicorp_all.sh script calls HashiCorp Vault’s native `POST /v1/{mount}/rotate-role/{role}` API to *force Vault to invalidate existing credentials and generate brand-new, cryptographically random *for each configured DB/AD/OUD role — this is an authoritative, upstream change that immediately revokes old secrets in the target systems (e.g., PostgreSQL `ALTER USER`, AD reset);

**(2) ****refresh **— in refresh mode, the same script first retrieves the *newly rotated* credentials via Vault’s `GET /v1/{mount}/static-cred/{role}` endpoint, then securely pushes them to RATAN’s own internal `POST /v1/hashicorp/refresh` API, which hot-updates components without restarting the application

### Connection details:

### Interface Specification:

![image-2026-1-30_8-54-59-1.png](attachments/image-2026-1-30_8-54-59-1.png)

### Interface team contact:

### OLA:

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.