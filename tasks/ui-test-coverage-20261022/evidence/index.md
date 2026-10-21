---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# UI coverage evidence

> **Critical conclusions: Review required before business acceptance**
>
> **All 521 new cases remain NOT_RUN.**
> Action: Bind reviewed assertions and fixtures before execution. Consequence: Business verification remains unsupported.
> Owner: unknown. Evidence: [case inventory](case-inventory.json) and [execution binding](../test-cases.md#execution-binding).
>
> **Draft source conflicts remain open.**
> Action: Resolve the applicable entry and integration policies. Consequence: Affected business acceptance remains blocked.
> Owner: unknown. Evidence: [knowledge decisions](knowledge-inspection.md#open-rule-decisions).

Start with the [intake](../intake.md) and [canonical case navigation](../test-cases.md#coverage-navigation).
The inventory counts 521 definitions across 46 groups.
It records 336 implementation characterizations, 23 documented draft expectations, and 162 proposals.
Counts do not prove independent rule coverage or exhaustive combinations.

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| UI-EV-001 | Case identities, coverage counts, and execution states | [case-inventory.json](case-inventory.json) | 2026-10-22; exact source revisions appear in the manifest. | `0706e6e0f587dce6b8a60045cda3803a0eaf3e4142ed24263e6b10c9ce8abeb6` | 521 definitions; all NOT_RUN. Definitions remain in the canonical catalog. |
| UI-EV-002 | Exact source hashes and retained source identities | [source-manifest.json](source-manifest.json) | 2026-10-22; exact source revisions appear in the manifest. | `34c25939eea1cee69410043fec22abf1f007f3c43d0d3848e66697b11c6966dc` | 124 source files; implementation and draft-source authority remain distinct. |
| UI-EV-003 | UI source and inspected assertion scope | [ui-source-inspection.md](ui-source-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `ece95bfbc0719307783708c38b0d017c384d3383d63195623c63f09e6885f5bc` | 156 source-derived UI cases. Conditional hook coverage is explicitly proposed. |
| UI-EV-004 | UI source-byte receipt | [ui-source-inspection.json](ui-source-inspection.json) | 2026-10-22; exact source revisions appear in the manifest. | `b72056ade9c8798369dada96d38927599ab42f35eccbe2d36ad0c7fd095406ae` | Inspected source hashes and baseline checks. No business execution. |
| UI-EV-005 | Authentication and session source scope | [session-source-inspection.md](session-source-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `b7a1d819f9ddf998ab0f061147a19f48757d81230665d8fb28588f4e34d3c1e6` | 144 source-derived UI cases. Timings characterize local code. |
| UI-EV-006 | BFF administration boundaries | [admin-boundary-inspection.md](admin-boundary-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `aa9ff5337ea325d0880b7a8bb794f60e566277ff3b96423cec76a82e3093156a` | 97 boundary cases. DDL limits require a prepared-schema fixture. |
| UI-EV-007 | Draft domain intent, conflicts, and prior-run limits | [knowledge-inspection.md](knowledge-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `5defcf79f4aa1abc36f1dac7c5cd5c2fd13dd1d9caf90a8b4cbb84bd1a82eca6` | 52 domain cases. Business source approval remains unrecorded. |
| UI-EV-008 | Quality probes, shared fields, and assertion limits | [crosscut-inspection.md](crosscut-inspection.md) | 2026-10-22; exact source revisions appear in the manifest. | `85b3b46814d5862057f1b0dd874fb84fc5f60b5fb4fde5c9bfc5a4c642653407` | 72 UI quality and boundary cases. Proposed policy remains unapproved. |
| UI-EV-009 | Registered local resources and schemas | [workspace-status.json](workspace-status.json) | 2026-10-22; exact source revisions appear in the manifest. | `7e2d1428b83ebc67ab0d30b8eaa6e0b3e8c8706daff9775d55637a4e78057c80` | Local discovery succeeded. No external connector call occurred. |
| UI-EV-010 | Staging retention reconciliation | [authoring-cleanup.json](authoring-cleanup.json) | 2026-10-22; exact source revisions appear in the manifest. | `5f4636122ba68500edb79034366b5dfa478f87e45b0ff1eef395bc6806cc68e5` | Only new generated inputs were removed after canonical reconciliation. |

## Validation

The [document checks](document-checks.json) retain lint, links, IDs, Gherkin, inventory, and source-hash results.
Lint warnings retain unknown owners, pending review, unresolved policies, and pending ASD review.
Document validation does not execute business scenarios.
Existing snapshots, task histories, source repositories, and audit events remain unchanged.

## Resume

Review the proposed and draft expectations before business acceptance.
Bind each selected case to its actual browser, fixture, executable assertion, and source revision.
Keep the current case IDs stable.
Save every completed execution immediately under this evidence directory.
Record actual results and material limits separately from the case definitions.
