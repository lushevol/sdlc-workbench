---
type: Summary
description: "Separates RATAN business-data visibility from tile access and records conflicting role, country-scope, and system-path proposals."
doc_type: short
full_text: sources/KT-ratan-data-entitlement-and-access.md
---

> **Candidate/draft only:** Historical role and country tables do not define an effective permission policy or current CES enforcement.

# RATAN Access and Data Entitlement Boundaries

The processing guide describes cashflow visibility by user profile, location, and permitted entities. This business-data boundary is distinct from portal entry and tile admission [[concepts/portal-entry-and-tile-authorization]], and from SDK entitlement retrieval [[concepts/entitlement-retrieval]]. These concepts do not supply the missing RATAN data policy.

The role guide marks several business-rule roles removed, while the processing guide lists them as new. Historical Global Business Services country tables also disagree. Blank role-country entries remain unknown; they do not grant wildcard access. The request table maps business functions to subjects, but RATAN_NOSTRO_BLOTTER labels both Nostro Static and BIC Netting Static.

A January 2026 checklist describes CES UI tiles without RATAN data feeds. A May checklist separately proposes FMCES restrictions and system integrations. SSDR is described with system, user, and country fields, while TLM, FMMIS, EOD, and CIS have system-only request paths whose equivalent user-country checks are unspecified. The materials do not prove current grants, deployed checks, or test results.

## Canonical sections

- [Need-to-know visibility](../../../records/candidates/operations/KT-ratan-data-entitlement-and-access.md#need-to-know-visibility)
- [Function-role inventory](../../../records/candidates/operations/KT-ratan-data-entitlement-and-access.md#function-role-inventory)
- [Request subjects and tiles](../../../records/candidates/operations/KT-ratan-data-entitlement-and-access.md#request-subjects-and-tiles)
- [Historical country-scope conflict](../../../records/candidates/operations/KT-ratan-data-entitlement-and-access.md#historical-country-scope-conflict)
- [Role-country matrix limits](../../../records/candidates/operations/KT-ratan-data-entitlement-and-access.md#role-country-matrix-limits)
- [Data-entitlement integration checklist](../../../records/candidates/operations/KT-ratan-data-entitlement-and-access.md#data-entitlement-integration-checklist)
