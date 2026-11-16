---
type: Summary
description: "Separates the candidate UTC runtime target from field-level local and UTC timestamp proposals."
doc_type: short
full_text: sources/INT-KT-indonesia-timezone-contract.md
---

# Indonesia timezone scope and field conversions

> **Source status:** Candidate/draft. Historical technical-design notes do not establish current runtime or field contracts.

One source targets UTC for JVM/OS and PostgreSQL behavior, including `LocalDateTime`, cron schedules, and database `now` or date functions. Its JVM example is spelled `-Duser,timezone=UTC`; this malformed text is not a verified command. The accepted service configuration and cron scope need confirmation. [UTC runtime target](../../../records/candidates/settlement/INT-KT-indonesia-timezone-contract.md#time-01--utc-runtime-target)

The field inventory distinguishes local audit, exception, net-trigger, and cutoff fields from upstream UTC timestamps. History effective/execution times and publication timestamps are listed as UTC, while cutoff/release fields are listed as local. Examples convert local UTC+7 input to UTC, but some also treat `Z`-suffixed values as local UTC+7 and reduce precision. Those examples conflict with ordinary `Z` semantics and do not establish accepted conversion rules. Blank service rows and linked images leave gaps. [Field-level distinctions](../../../records/candidates/settlement/INT-KT-indonesia-timezone-contract.md#time-02--field-level-timezone-distinctions) [Open questions](../../../records/candidates/settlement/INT-KT-indonesia-timezone-contract.md#open-questions)

Confirm per-service runtime settings, field ownership, conversion, and precision. Related regional design proposals: [[summaries/INT-KT-indonesia-regional-architecture]].
