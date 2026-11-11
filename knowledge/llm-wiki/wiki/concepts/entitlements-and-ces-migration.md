---
title: "Entitlements and CES migration"
type: concept
tags: [candidate-derived, security]
sources: [wb-candidate-security-kt-sdk-and-entitlements, wb-candidate-security-kt-ces-migration-parity, wb-candidate-operations-kt-admin-and-onboarding]
workbench_status: candidate-derived
---

# Entitlements and CES migration

This topic separates Portal entry, tile admission, and application data permission while preserving the candidate migration mapping from EMS2 concepts to CES concepts.

## Core model

- Portal entry, tile visibility and launch, and application data permissions are separate decisions. [[wb-candidate-security-kt-sdk-and-entitlements]]
- The migration compares roles to entitlements, entities to applications, subjects to features, and actions to actions within application scope. [[wb-candidate-security-kt-ces-migration-parity]]
- Entitlement definitions, account assignments, effective permissions, and unresolved differences require separate coverage denominators. [[wb-candidate-security-kt-ces-migration-parity]]
- Each tile selects its configured provider independently; a shared permission check does not choose a scalar CES role for role-owned writes. [[wb-candidate-security-kt-ces-migration-parity]]

## Open boundaries

Multiple-role ownership, legacy data restrictions, complete upper-application mappings, CES-only management scope, and deployed parity remain unresolved. The candidate records establish intended comparison boundaries, not confirmed permission equivalence. [[wb-candidate-security-kt-ces-migration-parity]]
