---
type: Summary
description: "Summarizes candidate settlement network controls, Indonesia isolation, identity migration, and API alternatives."
doc_type: short
full_text: sources/KT-settlement-security-p3.md
---

# Settlement security P3

> **Source status:** Candidate/draft. Historical security and migration options do not establish current identity, access, or deployment contracts.

The historical settlement design describes internal active/passive services, TLS messaging, vaulted secrets, firewall allowlists, Nginx/API-gateway access, and FMAA token checks. It excludes external clients in that settlement scope; it does not decide other portal products. [Historical network and access design](../../../records/candidates/security/KT-settlement-security-p3.md#historical-network-and-access-design)

Migration proposals target Entra identity and Indonesia data/session isolation, with CES migration as a prerequisite for new ServiceNow entitlement onboarding. Other designs move entitlement checks among BFF, gateway, and auth service, embed entitlement data in tokens, or relocate token endpoints. These are alternatives requiring caller-compatibility review; no endpoint removal or consumer change is authorized here. [Identity and Indonesia isolation objectives](../../../records/candidates/security/KT-settlement-security-p3.md#identity-and-indonesia-isolation-objectives) [Entitlement and API migration alternatives](../../../records/candidates/security/KT-settlement-security-p3.md#entitlement-and-api-migration-alternatives)

Illustrative EMS2-subject/CES-feature mappings are not full grants. Confirm effective identity, external-user scope, Indonesia isolation, entitlement mapping, and backward-compatible API behavior. See [[concepts/entitlement-retrieval]] and [[concepts/ems2-to-ces-permission-mapping]].
