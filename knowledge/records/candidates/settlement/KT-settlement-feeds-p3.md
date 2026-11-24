---
type: KnowledgeTopic
id: KT-settlement-feeds-p3
version: 3
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Backward
    Workflow Design/page.md
  revision: sha256:2c590a56cbacc8d67569b9b51033f8c93ca921f8b18fc8dfeb52a5dfdef125c6
  sha256: 2c590a56cbacc8d67569b9b51033f8c93ca921f8b18fc8dfeb52a5dfdef125c6
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Ratan - LMS feed/page.md
  revision: sha256:ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8
  sha256: ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Settlement Accounting for Aspire Tech design/page.md
  revision: sha256:3e590bff0dba8a3f78409d039f29504997675464b6f05c0baee7eef4a6f8a74f
  sha256: 3e590bff0dba8a3f78409d039f29504997675464b6f05c0baee7eef4a6f8a74f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Swift Generation & Settlement Accounting Tech
    design/Korea Accounting - OLTP/page.md
  revision: sha256:b52a48f1b57aea90c69cc72ba6b53f91174318e523b9d0e195eb7f38bac95d65
  sha256: b52a48f1b57aea90c69cc72ba6b53f91174318e523b9d0e195eb7f38bac95d65
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Swift Generation & Settlement Accounting Tech
    design/Korea Swift - Enisis/page.md
  revision: sha256:063a7540f6ac6217447951dfd897775c5e77508e9710a5298c6c8bb391704efd
  sha256: 063a7540f6ac6217447951dfd897775c5e77508e9710a5298c6c8bb391704efd
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Swift Generation & Settlement Accounting Tech
    design/page.md
  revision: sha256:f669575b4c1dd607ecf658b75aa9a5bd03bfc1123e8519ebfa2027757e5a6770
  sha256: f669575b4c1dd607ecf658b75aa9a5bd03bfc1123e8519ebfa2027757e5a6770
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Trade Information Tech Design/page.md
  revision: sha256:dd611ea0f0c470cd374db0a276f99692dba67264d63089c00a9772226378ec1c
  sha256: dd611ea0f0c470cd374db0a276f99692dba67264d63089c00a9772226378ec1c
generated:
  by: agent:sol_complete_sources
  at: '2026-11-16T07:55:20.538353+00:00'
verified: []
scope: Historical selected-source design for settlement feeds p3.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which feed variant, local calendar/date boundary, retry contract, and storage schema
  are approved by downstream?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
previous_version: 2
previous_content_sha256: acc3916fc616460e13279cd3ff7fe889cb5c7fbf73fdb68f56a5c38d83f6ae94
---
# Settlement feeds p3

## Scope

Historical selected-source design for settlement feeds p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Status write-back contract

Razor returns ACK/NACK, RELEASED, and SETTLED status information.
RATAN updates cashflow status and synchronizes STELLA or Murex.
The adaptor example batches netted components and sends a single gross cashflow ID.
Its payload carries Cashflow__Cashflow_State, nullable Cashflow__Netting_Id, and Cashflow__Cashflow_Id array.

The state examples cover RELEASED or SETTLED; they do not define an ACK/NACK payload.

Sources: [original lines 1–9](../../../evidence/sources/sha256/2c590a56cbacc8d67569b9b51033f8c93ca921f8b18fc8dfeb52a5dfdef125c6.md#L1-L9), [original lines 15–35](../../../evidence/sources/sha256/2c590a56cbacc8d67569b9b51033f8c93ca921f8b18fc8dfeb52a5dfdef125c6.md#L15-L35).

### LMS and trade information

The proposed stack-flow identifiers distinguish default Murex/Stella and LoanIQ feeds.
The source requires LMS alignment and does not establish no-risk compatibility.
Trade information supplies entity LEID and trader ID for LMS.
Instrument data for cashflow-blotter querying is only potential scope.

Sources: [original lines 1–6](../../../evidence/sources/sha256/ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8.md#L1-L6), [original lines 3–6](../../../evidence/sources/sha256/dd611ea0f0c470cd374db0a276f99692dba67264d63089c00a9772226378ec1c.md#L3-L6).

### EBBS and Aspire publication variants

The EBBS principle generates feeds from events, holds until value date, publishes directly when due, and limits retries to three for specified error codes.
Withdrawal reverses the New direction.
The Aspire design instead publishes batch files after value-date 22:05 local time.
Its Control-M schedule runs every 30 minutes from 22:05 to 02:05 and selects payment_date <= current date with creation before 22:00.

It calls for one workday file and a 03:30 empty-file job.
The after-midnight date interpretation and EBBS/Aspire storage-column choice remain unresolved.
Direct and batch publication are separate design variants.

Sources: [original lines 9–17](../../../evidence/sources/sha256/3e590bff0dba8a3f78409d039f29504997675464b6f05c0baee7eef4a6f8a74f.md#L9-L17), [original lines 23–27](../../../evidence/sources/sha256/3e590bff0dba8a3f78409d039f29504997675464b6f05c0baee7eef4a6f8a74f.md#L23-L27), [original lines 9–13](../../../evidence/sources/sha256/f669575b4c1dd607ecf658b75aa9a5bd03bfc1123e8519ebfa2027757e5a6770.md#L9-L13).

### Korea accounting task differences

EBBS and OLTP use payment date as system date, while bridge-account selection differs.
Validation checks stamped accounts; OLTP disables a task when settlementMeans is NOX and settlementAccount contains UUID or UISUS.
EBBS Request_info and OLTP ExtColumn2 hold their distinct JSON messages.
Reversal flips account/direction; OLTP also flips TransData.

EBBS retries absent responses or TXN99999/TEC0004 three times at four-minute intervals.
OLTP has no retry and Korean tasks are excluded from that retry job.
Both variants use hourly SOD processing from 06:00 through 18:00 and generate missing message JSON before processing.
Acknowledgements arrive on distinct topics, are saved, and update task status.

The Enisis/Enisis-named Swift fragment retains the old connection while adding logic; it supplies no new wire contract.

Sources: [original lines 11–40](../../../evidence/sources/sha256/b52a48f1b57aea90c69cc72ba6b53f91174318e523b9d0e195eb7f38bac95d65.md#L11-L40), [original lines 53–72](../../../evidence/sources/sha256/b52a48f1b57aea90c69cc72ba6b53f91174318e523b9d0e195eb7f38bac95d65.md#L53-L72), [original lines 1–4](../../../evidence/sources/sha256/063a7540f6ac6217447951dfd897775c5e77508e9710a5298c6c8bb391704efd.md#L1-L4).

### Reversal and reinstatement limits

The selected EBBS note distinguishes reinstate and SwiftUnSuppressed reversal tags.
Its stated filter combines reversal flag reinstate with last published balance below zero.
It does not define every downstream reversal, retry, or idempotency rule.

Sources: [original lines 17–21](../../../evidence/sources/sha256/f669575b4c1dd607ecf658b75aa9a5bd03bfc1123e8519ebfa2027757e5a6770.md#L17-L21).

### Historical write-back downstream version

The write-back design specifically names STELLA or Murex2.11 as downstream synchronization targets.
Its source-specific qualifier leaves other Murex versions outside this fragment's documented contract.
[Selected original lines 1–9](../../../evidence/sources/sha256/2c590a56cbacc8d67569b9b51033f8c93ca921f8b18fc8dfeb52a5dfdef125c6.md#L1-L9) [Selected original lines 15–35](../../../evidence/sources/sha256/2c590a56cbacc8d67569b9b51033f8c93ca921f8b18fc8dfeb52a5dfdef125c6.md#L15-L35)

### Proposed LMS identifier migration

The proposed identifiers retain these source-specific mappings.

| Upstream | Original source | Current MessageSender | Proposed Stack Flow |
| --- | --- | --- | --- |
| Murex/Stella | MUREX/STELLA | FMRP, default | FMRPSTELLA, default |
| LoanIQ | LOANIQ | LOANIQ | FMRPSTELLA-LOANIQ |

The source requires LMS alignment. Its no-risk statement remains a technical claim without compatibility execution evidence.
[Selected original lines 1–6](../../../evidence/sources/sha256/ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8.md#L1-L6)

### Korean accounting selection and validation conditions

The EBBS initialization uses one bridge account per entity. OLTP instead chooses its bridge account by currency.
Reversal and netted/split task initialization follow the corresponding normal-task rules.
EBBS validation additionally checks that its JSON fields are populated after Nostro and bridge stamping.

The OLTP JSON proposal calls for additional 53 BIC and receiver-BIC logic. Its selected text leaves that mapping unspecified.
The SOD job selects Hold tasks whose payment_date is at most current_date.
EBBS generates missing Request_info before processing. OLTP checks ExtColumn2 and generates its missing JSON before processing.
[Selected original lines 11–40](../../../evidence/sources/sha256/b52a48f1b57aea90c69cc72ba6b53f91174318e523b9d0e195eb7f38bac95d65.md#L11-L40) [Selected original lines 53–72](../../../evidence/sources/sha256/b52a48f1b57aea90c69cc72ba6b53f91174318e523b9d0e195eb7f38bac95d65.md#L53-L72)

### Reinstatement trigger and reversal tags

A reinstate action after FAILED status produces reversal tag reinstate in the selected design.
An approval after SWIFT_SUPPRESSED status produces tag SwiftUnSuppressed.
The stated filter selects reversal flag reinstate together with last published balance below zero.

These source-specific predicates leave other reversal and idempotency decisions unresolved.
[Selected original lines 9–13](../../../evidence/sources/sha256/f669575b4c1dd607ecf658b75aa9a5bd03bfc1123e8519ebfa2027757e5a6770.md#L9-L13) [Selected original lines 17–21](../../../evidence/sources/sha256/f669575b4c1dd607ecf658b75aa9a5bd03bfc1123e8519ebfa2027757e5a6770.md#L17-L21)

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which feed variant, local calendar/date boundary, retry contract, and storage schema are approved by downstream?
