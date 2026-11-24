---
type: Summary
description: "Records candidate auto-netting static access, validation, execution-key, STP, and rule-refresh controls."
doc_type: short
full_text: sources/KT-settlement-auto-netting-static-controls.md
---

> **Candidate/draft only:** These static controls and priorities remain source-specific proposals. Owner is unknown; `verified` is empty.

# Settlement auto-netting static controls

The selected requirement limits static-rule create/update to Data Ops and warns when booking entity is absent or the netting-ID exclusion is missing. CCIL and BIC types have separate settlement-method and counterparty predicates. The source distinguishes warnings from errors and manual from automatic rule types.

Bilateral grouping uses booking entity, counterparty, currency, and payment date. CCIL omits counterparty and maps its resultant to a named clearing counterparty. BIC adds SCI BIC-net attributes; SAL types add payment type. STP settings distinguish maker/checker, checker-only, and a disabled FULL_STP path. Resultant inheritance covers selected DVP, LIEN, and commodity flags; intent-to-clear remains open.

The requirement proposes refresh after rule changes, but also lists Pending Auto Netting among update exclusions. A no-refresh alternative remains in the clarification history. Priority, Clearing_Swift_Suppress behavior, and net-over-net exceptions also vary by source. The active [[summaries/KT-settlement-auto-netting]] describes the broader scheduled requirement. Existing [[concepts/auto-netting-rule-selection]] and [[concepts/cashflow-netting-grouping-and-outcomes]] cover rule precedence and grouping, not approval of these values.

## Canonical sections

- [Static rule access and validation](../../../records/candidates/settlement/KT-settlement-auto-netting-static-controls.md#static-rule-access-and-validation)
- [Execution-key and resultant mappings](../../../records/candidates/settlement/KT-settlement-auto-netting-static-controls.md#execution-key-and-resultant-mappings)
- [STP controls and inheritance](../../../records/candidates/settlement/KT-settlement-auto-netting-static-controls.md#stp-controls-and-inheritance)
- [Rule refresh boundary and contradiction](../../../records/candidates/settlement/KT-settlement-auto-netting-static-controls.md#rule-refresh-boundary-and-contradiction)
