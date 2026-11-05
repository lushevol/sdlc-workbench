# Administration, onboarding, and release

Derived navigation, 6 November 2026.
**The linked records remain candidate/draft. Documented procedures do not establish current operating authority or completed release gates.**

## Onboarding connects several responsibilities

The onboarding model joins frontend assets, backend routing, authentication, entitlement setup, and Portal catalog records.
Tenant teams supply application files and API locations; platform responsibilities cover shared integration boundaries.
These role declarations need applicable owners and procedures before operational use.
See [onboarding responsibilities](../../../candidates/operations/KT-admin-and-onboarding.md#team-responsibilities-and-onboarding-sequence), candidate/draft, version 3.

Module Mapping connects a module name to an asset path.
Drawer Category groups tiles.
Tile Configuration connects presentation, container routes, and entitlement configuration.
Matching these records with application routes connects administration to [frontend composition](../../../candidates/architecture/KT-frontend-composition.md#documented-onboarding-sequence), candidate/draft, version 3.
See [catalog vocabulary](../../../candidates/operations/KT-admin-and-onboarding.md#purpose-and-component-vocabulary), candidate/draft, version 3.

## Administrative review and configuration promotion

The admin manual requires different maker and checker users before record activation.
Its `un-verified` status describes administrative records, separately from Workbench knowledge lifecycle states.
Per-record history supports the documented administrative review process.
Tenant isolation, activation propagation, rollback, and concurrent-edit behavior remain incompletely specified.
See [administrative review](../../../candidates/operations/KT-admin-and-onboarding.md#review-and-activation-workflow) and [open questions](../../../candidates/operations/KT-admin-and-onboarding.md#open-questions), candidate/draft, version 3.

The release flow describes exporting Development configuration as CSV and retaining it in a tenant-owned repository.
An ADO pipeline uploads those records to the Portal Admin service under the documented FMAA JWT procedure.
This is documented process intent, without an assertion that an upload or promotion succeeded.
The self-service proposal does not establish an exemption from production change controls.
See [configuration promotion](../../../candidates/operations/KT-release-operations.md#configuration-promotion), candidate/draft, version 2, and [administrative purpose](../../../candidates/operations/KT-admin-and-onboarding.md#purpose-and-component-vocabulary).

## Technical delivery and business activation

The release materials separate Portal releases, tenant releases, technical go-live, and business activation.
Configuration upload alone cannot establish routing, connectivity, sign-off, UVT, or business readiness.
Portal and tenant responsibilities remain distinct throughout that sequence.
See [technical and business activation](../../../candidates/operations/KT-release-operations.md#technical-and-business-activation), candidate/draft, version 2.

Analytics and performance also answer different questions.
Interaction events describe adoption and UI context; workload measurements support performance claims only within their evidence limits.
Historical draft targets cannot establish accepted current service limits.
See [observability purpose](../../../candidates/observability/KT-observability-and-performance.md#interaction-purpose-and-event-vocabulary) and [measurement intent](../../../candidates/observability/KT-observability-and-performance.md#frontend-measurement-intent), candidate/draft, version 2.

## Unresolved operating decisions

| Open boundary | Consequence | Owner and next action |
| --- | --- | --- |
| Release proposal states both 24-hour and 10-hour durations. | Standby and release-window planning remain uncertain. | Unknown; confirm one applicable duration. |
| Urgent-release rules mix explicit confirmation with proceeding after silence. | Required stakeholder agreement remains unclear. | Unknown; identify decision authority and required confirmations. |
| Checklist flags FMAA decommissioning. | The documented configuration-promotion authentication dependency needs review. | Unknown; confirm the replacement plan and governing checklist. |
| Analytics models differ on attribute limits and omit approved retention rules. | Collection and downstream compatibility boundaries remain unresolved. | Unknown; reconcile schemas and data policy. |

The [release questions](../../../candidates/operations/KT-release-operations.md#open-questions) and [observability questions](../../../candidates/observability/KT-observability-and-performance.md#open-questions) retain these uncertainties.
This page selects no missing policy and records no deployment or execution outcome.

## Canonical records and related topics

| Canonical record | Version | Source state |
| --- | --- | --- |
| [KT-admin-and-onboarding](../../../candidates/operations/KT-admin-and-onboarding.md) | 3 | candidate/draft |
| [KT-release-operations](../../../candidates/operations/KT-release-operations.md) | 2 | candidate/draft |
| [KT-frontend-composition](../../../candidates/architecture/KT-frontend-composition.md) | 3 | candidate/draft |
| [KT-observability-and-performance](../../../candidates/observability/KT-observability-and-performance.md) | 2 | candidate/draft |

Continue with [entitlements and CES migration](../entitlements-and-ces-migration/index.md) or [composition and interoperability](../portal-composition-and-interoperability/index.md).
Return to the [wiki index](../../index.md).
