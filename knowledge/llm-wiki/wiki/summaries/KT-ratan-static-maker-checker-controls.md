---
type: Summary
description: "Summarizes candidate BIC and netting static maker-checker lifecycle and rule-refresh boundaries."
doc_type: short
full_text: sources/KT-ratan-static-maker-checker-controls.md
---

# BIC and netting static control intent

> **Source status:** Candidate/draft. The retained source intent awaits authority and applicability confirmation.

The BIC static design assigns maker and checker profiles, prevents leading or trailing spaces, and uses pending and confirmed states. Checker approval activates additions and updates; rejected updates keep the previous version, while approved deletions remain audit-only. These are source-specific lifecycle descriptions, not verified controls. [BIC static lifecycle](../../../records/candidates/operations/KT-ratan-static-maker-checker-controls.md#bic-static-lifecycle)

Netting static uses the same named profiles. Makers define AND conditions and a reason; automatic rules add schedule, resultant STP level, and netting type. Checker approval makes a new rule effective, and maker/checker identities must differ. Refresh behavior varies by create, disable, update, and manual/automatic conversion. The update passage both includes and excludes tagged Pending Auto Netting cashflows, so the conflict remains open. [Netting rule creation](../../../records/candidates/operations/KT-ratan-static-maker-checker-controls.md#netting-rule-creation) [Automatic-rule refresh boundaries](../../../records/candidates/operations/KT-ratan-static-maker-checker-controls.md#automatic-rule-refresh-boundaries)

No current profile export, execution, deployment, or publication is established. See proposed [[summaries/KT-rule-service-p3]] and [[concepts/auto-netting-rule-selection]].
