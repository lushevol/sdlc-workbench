---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-ssi-form-validation",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-85922e06ef72466af62b7be6",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/SSI Stamping Notification/Adhoc SI/page.md",
      "revision": "sha256:168a6b94aa27cbb4c8eaf70b3af2da1f453da208e036090de1e000175e9be3e2",
      "sha256": "168a6b94aa27cbb4c8eaf70b3af2da1f453da208e036090de1e000175e9be3e2",
      "snapshot": "knowledge/evidence/sources/sha256/168a6b94aa27cbb4c8eaf70b3af2da1f453da208e036090de1e000175e9be3e2.md"
    },
    {
      "id": "SRC-a9ddc4cb9e33456363257e26",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/SSI Validation Rule for UI Form/page.md",
      "revision": "sha256:7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff",
      "sha256": "7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff",
      "snapshot": "knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md"
    },
    {
      "id": "SRC-233fb8a6609ed65875103b53",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/SSI Stamping Notification/FMRP - SSI Stamping Flow/page.md",
      "revision": "sha256:dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28",
      "sha256": "dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28",
      "snapshot": "knowledge/evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:47:40.798282+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "SSI form validation and adhoc correction controls",
  "summary": "The form requires settlement account, settlement means, SSI type, message type and eBBS Nostro account.",
  "related": [],
  "open_questions": [
    "Resolve all question-mark field limits/formats and supplied regex differences.",
    "Confirm NOS versus Nostro normalization, message-type and current Swift dictionary applicability.",
    "Confirm effective Dubai purpose taxonomies/defaults and region scope.",
    "Resolve the conflicting initial READY adhoc transitions and checker rejection semantics."
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Automated checks do not establish complete writing review.",
    "Retained intent does not establish current approval, execution or rollout."
  ]
}
---
# SSI form validation and adhoc correction controls

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

SSI form validation and adhoc correction controls. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The form requires settlement account, settlement means, SSI type, message type and eBBS Nostro account.

## Documented knowledge

### Mandatory form fields

The form requires settlement account, settlement means, SSI type, message type and eBBS Nostro account. SSI type allows Primary/Secondary. Message type allows MT103, MT103 SERIAL and MT202. Settlement-account maximum is20 characters, although its length pattern permits zero while mandatory forbids blank. Settlement-means prose says Nostro while regex says NOS. Do not infer normalization. Mandatory means nonempty; optional populated fields still meet their length/format constraints. Question-mark entries remain undefined.

[Source 9, lines 19-19](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L19-L19) [Source 9, lines 45-57](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L45-L57)

### Conditional beneficiary and ordering fields

MT103 requires field57 BIC, beneficiary account/address/charges, and ordering account/address/name. MT103 plus RUB requires field57 account, whose length/format remain unknown. MT202 with Over-Account also requires beneficiary account. For MT202, missing beneficiary name requires BIC; missing BIC requires name. Beneficiary account length is2–34; ordering account is1–50. Ordering name maximum is70. Charges allow OUR/SHA/BEN. Explicitly constrained BICs require8 or11 uppercase alphanumeric characters. Intermediary account, ordering BIC and receiver-correspondent account retain unknown specifications.

[Source 9, lines 7-34](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L7-L34)

### Optional formats and line lengths

The table generally permits letters, digits and whitespace in addresses/names, with address maximum60 and most names maximum35. Receiver-correspondent name uses a different regex accepting word characters, so underscore behavior is unresolved. Field70 and72 first lines allow35 characters; subsequent lines allow33. Field70 has four lines;72 has six. Those lines allow arbitrary characters subject to length. The source regexes are recorded specifications, without verified Swift-wire conformance.

[Source 9, lines 8-44](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L8-L44)

### Covered and serial payment controls

For MT103 plus NOS, ticking Covered Payment makes field54 BIC mandatory. A correctly formatted field54 BIC forces the checkbox selected and reverses manual unticking. The main design allows manual or candidate-selected inputs for MT103, NOS and field54. Both input routes use maker/checker handling and documented payment-method enrichment. Adhoc/Vostro-exception input cannot populate54 and56 together; entering one disables the other.

[Source 9, lines 59-62](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L59-L62) [Source 7, lines 112-129](../../../../knowledge/evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L112-L129) [Source 7, lines 133-148](../../../../knowledge/evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L133-L148)

### Dubai purpose predicate

The purpose field appears only when mandatory: MT103, entity FMID5, non-AED currency, NOS, account containing MAIN, and beneficiary BIC not SUPPRESSXXX. Maximum length is90. The mapping proposes IRP for listed IRS taxonomies and FDA for other derivative payments, with maker/checker handling like70/72. Effective regional/product applicability remains unconfirmed.

[Source 9, lines 45-45](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L45-L45) [Source 9, lines 64-66](../../../../knowledge/evidence/sources/sha256/7a8b712550c0de49ca426d16eb880ba6ee4d88e519777ad071d1361143af60ff.md#L64-L66) [Source 7, lines 94-94](../../../../knowledge/evidence/sources/sha256/dcda0030ded419ffb15b4b0a093b369a9a99d16dfd3cf87745718e5324450d28.md#L94-L94)

### Adhoc transition conflict

The WAITING table sends maker adhoc input from Pending Operator to Pending Verification. Approval returns READY and clears exception/substates; rejection returns Pending Operator with AdhocSI. Its first READY row instead retains READY with Pending Exception/Pending Verification after maker action. The later READY table initially retains READY and adds AdhocSI with blank substates; maker input then enters Pending Verification. Approval/rejection both retain READY and blank substates there. These presentations do not define one consistent initial READY transition; do not merge them.

[Source 5, lines 1-24](../../../../knowledge/evidence/sources/sha256/168a6b94aa27cbb4c8eaf70b3af2da1f453da208e036090de1e000175e9be3e2.md#L1-L24)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Resolve all question-mark field limits/formats and supplied regex differences.
- Confirm NOS versus Nostro normalization, message-type and current Swift dictionary applicability.
- Confirm effective Dubai purpose taxonomies/defaults and region scope.
- Resolve the conflicting initial READY adhoc transitions and checker rejection semantics.
