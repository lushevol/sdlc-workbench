---
type: Concept
description: "How candidate amendment classes affect cashflow identity, status, downstream publication, and release controls."
sources:
  - summaries/INT-KT-cashflow-amendment-and-release-controls.md
  - summaries/KT-settlement-non-economic-amendments.md
  - summaries/KT-settlement-amendment-reversal-rebook-exceptions.md
  - summaries/KT-settlement-cashflow-identity-and-stella-write-back.md
---

> **Candidate synthesis:** Supporting records retain distinct source scopes and unresolved rules. Owner review and implementation evidence remain absent.

# Cashflow amendment classification and release

The source set distinguishes non-economic replacement, economic or key-field change, and amendment after release. One design compares booking entity, counterparty, currency, amount, value date, and pay/receive; when all six match, originals remain active while replacements receive new identities. It routes later status updates to replacement identities. Separate sources propose economic classifications and additional reversal/rebook checks after release.

These rules do not form one settled state machine. The order of key-field checks versus manual-touch/release checks remains open. The release controls also differ between January and October, including allowed actions and cutoff wording. The released-amendment proposal reports no direct original-to-replacement link, which limits reliable rebook identification. Do not infer one identity, exception, or publication rule across all products and versions.

The six-field design retains original settlement IDs for Razor, LMS, and the EOD API, while Stella updates target replacement IDs. This separation must remain producer-specific. [Identity treatment](../../../records/candidates/settlement/KT-settlement-non-economic-amendments.md#settlement-identity-and-external-status-identity)

The released-amendment record includes a dated tagging change from ten days to five days for the same trade ID. Calendar, boundaries, authority, and rollout remain unresolved. NDS and IRS examples retain separate release and settlement predicates. [Dated tagging](../../../records/candidates/settlement/KT-settlement-amendment-reversal-rebook-exceptions.md#dated-pre-cab-rebook-tagging-entry) [NDS scope](../../../records/candidates/settlement/KT-settlement-amendment-reversal-rebook-exceptions.md#nds-post-release-scope-boundary)

January separates workflow publication at `READY+NA+NA` from SWIFT generation at `READY+NA+PendingAck`. October retains a READY-only downstream gate and near-cutoff net/split restriction. These source-specific controls need precedence and boundary decisions. [January gates](../../../records/candidates/settlement/INT-KT-cashflow-amendment-and-release-controls.md#ctrl-01--proposed-layered-release-validation) [October controls](../../../records/candidates/settlement/INT-KT-cashflow-amendment-and-release-controls.md#ctrl-04--october-release-control-intent)

The summary pages below preserve their exact conditions and conflicts. This concept establishes no approved mapping, deployed behavior, or successful reconciliation.

## Source records

- [[summaries/INT-KT-cashflow-amendment-and-release-controls]] covers candidate economic/key-field classification and READY gates.
- [[summaries/KT-settlement-non-economic-amendments]] covers six-field comparison and identity treatment.
- [[summaries/KT-settlement-amendment-reversal-rebook-exceptions]] covers released amendment exception proposals.
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back]] covers source IDs and status write-back questions.
