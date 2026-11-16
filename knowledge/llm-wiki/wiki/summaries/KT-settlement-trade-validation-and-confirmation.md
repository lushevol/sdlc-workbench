---
type: Summary
description: "Summarizes candidate trade-validation visibility, source-specific states, bypass scopes, and affirmation exceptions."
doc_type: short
full_text: sources/KT-settlement-trade-validation-and-confirmation.md
---

# Settlement trade validation and confirmation

> **Source status:** Candidate/draft. Status matrices and migration milestones do not establish current implementation or release.

The proposal holds unvalidated cashflows outside the settlement GUI and resumes matching flows after trade validation. Correlation differs by source, using trade IDs/major versions for Stella and internal IDs for Murex. [Validation gates visibility](../../../records/candidates/settlement/KT-settlement-trade-validation-and-confirmation.md#validation-gates-visibility)

Accepted state lists differ between Murex cashflows, other sources, and Stella/Murex parent trades. Bypass scope also depends on named entities and product taxonomies; a dated migration plan retains manual exception handling and marks a later auto-validation milestone tentative. Do not merge these states or bypasses into one universal allowlist. [Source-specific accepted validation states](../../../records/candidates/settlement/KT-settlement-trade-validation-and-confirmation.md#source-specific-accepted-validation-states) [Validation bypass and migration conditions](../../../records/candidates/settlement/KT-settlement-trade-validation-and-confirmation.md#validation-bypass-and-migration-conditions)

Confirmation proposals let specified affirmative states close Pending Confirmation/Affirmation; removing the only exception permits STP. Cancellation withdrawal is a separate bypass. Product-specific FX, fixing, netting, clearing, and Islamic conditions remain distinct. Version ordering and special-product decisions remain open. [Confirmation exception handling](../../../records/candidates/settlement/KT-settlement-trade-validation-and-confirmation.md#confirmation-exception-handling) [Product-specific affirmation proposal](../../../records/candidates/settlement/KT-settlement-trade-validation-and-confirmation.md#product-specific-affirmation-proposal)

See [[summaries/KT-settlement-cashflow-blotter-actions]] and proposed [[summaries/KT-settlement-multi-exception-control]].
