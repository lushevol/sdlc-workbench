---
type: Summary
description: "Summarizes candidate entity configuration consolidation and RDM holiday message ingestion proposals."
doc_type: short
full_text: sources/INT-KT-entity-and-reference-data-design.md
---

# Entity and holiday reference-data design

> **Source status:** Candidate/draft. Proposed tables and feed routes do not establish current configuration or authoritative calendars.

The consolidation proposal places selected onboarding values in one entity table but excludes Nostro static. It lists FMID/FMCODE, workflow, LMS filtering, branch/country, accounting, currency, and BIC fields. Strategic, Legacy, and CPT examples are not approved defaults. Possible BIC-netting, FXU, and profile-limit extensions are ideas only, and the entity filter does not supersede a separate LMS filter proposal. [STATIC-01](../../../records/candidates/settlement/INT-KT-entity-and-reference-data-design.md#static-01--entity-configuration-consolidation-proposal)

The holiday design separates raw messages from structured records and proposes duplicate keys from center, event date, event name, and file type. Ordinary holidays/weekends use Solace or FileIT paths; special holidays have a separate Solace route. Sample IDs and dates do not define a calendar. Correction, deletion, and special-holiday precedence remain unspecified. [STATIC-02](../../../records/candidates/settlement/INT-KT-entity-and-reference-data-design.md#static-02--rdm-holiday-input-and-duplicate-key)

Confirm ownership, allowed onboarding fields, sender-side filters, correction handling, and calendar precedence. See [[summaries/KT-day2-manual-entity-settlement]], [[summaries/INT-KT-ratan-reference-and-control-interfaces]], and proposed [[summaries/KT-rule-service-p3]].
