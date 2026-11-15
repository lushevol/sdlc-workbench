---
type: KnowledgeTopic
id: INT-KT-ratan-cashflow-settlement-interfaces
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and Aspire 51282/page.md
  revision: sha256:e5adef13753c73d74db9eccc320dd293f0ad23bbdf47ae1b17d81e4a5a8efaab
  sha256: e5adef13753c73d74db9eccc320dd293f0ad23bbdf47ae1b17d81e4a5a8efaab
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and EBBS 14147/page.md
  revision: sha256:4123aceb92ef466be4758e11db873589b4f3e9622a4f1ac58a28ed3bd8d81483
  sha256: 4123aceb92ef466be4758e11db873589b4f3e9622a4f1ac58a28ed3bd8d81483
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and FMSGW 54949/page.md
  revision: sha256:232860caf94e82f0651a7424384f85d6bff51906522c35e82e33f221490a515a
  sha256: 232860caf94e82f0651a7424384f85d6bff51906522c35e82e33f221490a515a
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and FXU(MX-FXCASH) 40630/page.md
  revision: sha256:466c2b9b5f99556b638b48e172a3a1e80e940f5a4fee05127fbcdb967eef8ccb
  sha256: 466c2b9b5f99556b638b48e172a3a1e80e940f5a4fee05127fbcdb967eef8ccb
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and Murex 14165/page.md
  revision: sha256:bcdd139231ee996d3664313cc3c74c382810d7037fd04fdca2980bccae83d91a
  sha256: bcdd139231ee996d3664313cc3c74c382810d7037fd04fdca2980bccae83d91a
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and Murex KR 50216/page.md
  revision: sha256:1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936
  sha256: 1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and ENISIS 50157/page.md
  revision: sha256:a7c48470a31afa6b04d49ab9f306c8bc285cda1d29ae968a2c8b9742173f2ec0
  sha256: a7c48470a31afa6b04d49ab9f306c8bc285cda1d29ae968a2c8b9742173f2ec0
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and FMMIS-51406  CIS-31946  SSDR-51507 (DQSL) PacMan-51406 CNEDMp-50584/page.md
  revision: sha256:ae79d6652b996a76f5557d9580bfc74b1c7f0ecd60f6560efcfd27abc8ba376a
  sha256: ae79d6652b996a76f5557d9580bfc74b1c7f0ecd60f6560efcfd27abc8ba376a
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and OLTP/page.md
  revision: sha256:a8b78e9369f619db9ed5bbba7c78d543c40970cdace5bb4a87562ce415e070a1
  sha256: a8b78e9369f619db9ed5bbba7c78d543c40970cdace5bb4a87562ce415e070a1
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and Razor (MX-FXCASH)-40630/page.md
  revision: sha256:b29b8ceb98aec1bc887770342d9d29f98572aad4e4c4e89cec3444ff4afd6738
  sha256: b29b8ceb98aec1bc887770342d9d29f98572aad4e4c4e89cec3444ff4afd6738
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and SSI+ 50509/page.md
  revision: sha256:b6c7feb19f34aafa9178c93595b6297a96b9e3bb20aa6cb0756174f3cff936ec
  sha256: b6c7feb19f34aafa9178c93595b6297a96b9e3bb20aa6cb0756174f3cff936ec
- resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and TLM 20649/page.md
  revision: sha256:192581fc3b234f890bc2396d68b7360e61710fb134698c2ed96a26c9c7c16baf
  sha256: 192581fc3b234f890bc2396d68b7360e61710fb134698c2ed96a26c9c7c16baf
generated:
  by: agent:codex
  at: '2026-11-15T22:55:29+08:00'
verified: []
classification: settlement
scope: The selected RATAN cashflow, settlement, payment-accounting, and SSI interface descriptions in this source batch.
summary: These selected pages describe RATAN accounting, cashflow, settlement, and SSI interfaces. Current authority remains unconfirmed.
related:
- KT-settlement-cashflow-identity-and-stella-write-back
- KT-settlement-auto-netting
- KT-settlement-lms-feed
- KT-settlement-korea-trade-confirmation
open_questions:
- Which interface descriptions define current approved contracts and entity scope?
- Which date, status, and message rules apply to each system pair?
- Which source owner can confirm the differing schedules and payment-status conditions?
- Which Korea message types and design revisions use SFTP or FM Solace between RATAN and ENISIS?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PASSED
  reviewer: agent:codex
  reviewed_at: '2026-11-15T22:56:16+08:00'
  limitations:
  - Writing review does not establish source authority, current applicability, approval, or execution.
---

# RATAN cashflow and settlement interfaces

## Scope

This candidate groups selected RATAN cashflow, settlement, and payment-accounting interface descriptions.
It records source-described relationships and conditions, not current deployment or tested behavior.

## Summary

The pages describe RATAN cashflow, payment, and accounting interfaces.
Each source has a separate scope and unresolved authority limits.

## Documented knowledge

### Payment accounting and downstream reporting

- **Aspire:** RATAN sends payment-accounting messages to Aspire through a FileIT batch transfer. [Aspire path](../../../evidence/sources/sha256/e5adef13753c73d74db9eccc320dd293f0ad23bbdf47ae1b17d81e4a5a8efaab.md#L13-L14) [Batch route](../../../evidence/sources/sha256/e5adef13753c73d74db9eccc320dd293f0ad23bbdf47ae1b17d81e4a5a8efaab.md#L21)

- **EBBS:** The page describes real-time JSON accounting through central Solace. It lists `CN, MY, IN, SG, UK, DE, MU, AE, ID, PH, US, JP, ZA, HK, EG, NP, SA`. Current scope and date remain unknown. [EBBS path and scope](../../../evidence/sources/sha256/4123aceb92ef466be4758e11db873589b4f3e9622a4f1ac58a28ed3bd8d81483.md#L9-L23)

- **Cashflow queries:** FMMIS, CIS, PacMan, MarketUDP/SSDR, and CNEDMp call RATAN REST APIs. The page names no fields, access conditions, or deployment status. [Cashflow query consumers](../../../evidence/sources/sha256/ae79d6652b996a76f5557d9580bfc74b1c7f0ecd60f6560efcfd27abc8ba376a.md#L20-L26)

- **OLTP accounting:** The page proposes RATAN as the Korea accounting sender instead of Murex-KR. It gives the same cashflow scope as the Murex-KR feed. [OLTP path and scope](../../../evidence/sources/sha256/a8b78e9369f619db9ed5bbba7c78d543c40970cdace5bb4a87562ce415e070a1.md#L13-L20)

  The normal route sends accounting through KREDMI to OLTP. Acknowledgements return through KREDMI and Solace. The page states an EOD window of 11:30–12:30 KST and a KREDMI NACK. [Normal and EOD routes](../../../evidence/sources/sha256/a8b78e9369f619db9ed5bbba7c78d543c40970cdace5bb4a87562ce415e070a1.md#L34-L42)

  The source defines six status meanings:

  | Status | Source-described meaning |
  | --- | --- |
  | `HOLD` | Entry generated before value date; posting waits. |
  | `DISABLED` | `Sett Means = NOX` and account is `CCY UISUS` or `CCY UIDD`; OLTP receives no entry. |
  | `SENT` | Message sent; response pending. |
  | `SUCCESS` | OLTP consumed the message and returned ACK. |
  | `REJECTED` | OLTP returned an error code. |
  | `MISSING_INFO` | `SWIFT_SUPPRESSED` without Nostro, or a mandatory field is missing. |

  These statuses describe the source; their current scope remains unconfirmed. [OLTP statuses and conditions](../../../evidence/sources/sha256/a8b78e9369f619db9ed5bbba7c78d543c40970cdace5bb4a87562ce415e070a1.md#L13-L24)

- **TLM reconciliation:** TLM asks for accounting records already sent to OLTP, including ACKed, NACKed, and unanswered records. The page calls this a business agreement and limits `fmidList` to Korea entity `10036645`. [TLM query scope](../../../evidence/sources/sha256/192581fc3b234f890bc2396d68b7360e61710fb134698c2ed96a26c9c7c16baf.md#L13-L26)

  The filter requires task status `SENT`. Date fields convert to GMT and use `created_at >= startReleaseTime` and `< endReleaseTime`. The maximum interval is three days. Examples do not establish universal applicability. [TLM query example](../../../evidence/sources/sha256/192581fc3b234f890bc2396d68b7360e61710fb134698c2ed96a26c9c7c16baf.md#L33) [Maximum interval](../../../evidence/sources/sha256/192581fc3b234f890bc2396d68b7360e61710fb134698c2ed96a26c9c7c16baf.md#L44-L45)

### Cashflow and settlement processing

- **Murex cashflows:** MQ carries value dates T-1 through T+1. Batch SFTP carries T+2 through T+7 and excludes weekends and public holidays. Corrective files use SFTP regardless of date. [Murex cashflow windows](../../../evidence/sources/sha256/bcdd139231ee996d3664313cc3c74c382810d7037fd04fdca2980bccae83d91a.md#L9-L24)

  RATAN returns updated cashflow status to Murex 2.11. Separate MT and payment XML messages use MQ for MX conversion. Full decommission migration remains pending. [Murex status and conversion](../../../evidence/sources/sha256/bcdd139231ee996d3664313cc3c74c382810d7037fd04fdca2980bccae83d91a.md#L9-L24)

  Batch names include `YYYYMMDD`, sequence `XXX`, and payment count `ZZZZ`. The ending file is `FMRP_Murex_Payments_YYYYMMDD_END.csv`. Murex sends it daily, even without batch processing. [Batch file markers](../../../evidence/sources/sha256/bcdd139231ee996d3664313cc3c74c382810d7037fd04fdca2980bccae83d91a.md#L37-L43)

  Murex cannot regenerate a batch after processing issues. It holds transfers until RATAN returns ACK or NACK. The file patterns are `FMRP_Murex_Payments_YYYYMMDD_XXX_Ack.csv` and `FMRP_Murex_Payments_YYYYMMDD_XXX_Nack.csv`. A missing response for 30 minutes holds the process for Murex PSS investigation. [Murex response conditions](../../../evidence/sources/sha256/bcdd139231ee996d3664313cc3c74c382810d7037fd04fdca2980bccae83d91a.md#L98-L112)

- **Korea Murex payment path:** The Murex KR page describes MT and MxML input through MQ. RATAN converts them to MX and sends them to ENISIS over SFTP. The page also describes COMP status for payment STP. [Murex KR flow](../../../evidence/sources/sha256/1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936.md#L9-L13)

  The ENISIS page describes MxML input through MQ. RATAN generates MT and converts it to MX, except MT210. It sends MX and MT210 to ENISIS over FM Solace. These outbound channels differ; the pages do not explain which message, stage, or revision each covers. [ENISIS route](../../../evidence/sources/sha256/a7c48470a31afa6b04d49ab9f306c8bc285cda1d29ae968a2c8b9742173f2ec0.md#L9-L18) [Murex KR route](../../../evidence/sources/sha256/1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936.md#L9-L13)

  The Murex KR page describes four recovery cases:

  | Trigger | Source-described action |
  | --- | --- |
  | RATAN does not receive Murex input. | Murex emails Korea FMO. FMO investigates with PSS or development; staff draft MX in ENISIS or payment in OSCAR if recovery fails. |
  | Murex data is invalid. | RATAN returns no ACK. Murex emails FMO; staff draft manually if the system cannot resume. |
  | RATAN cannot generate Swift. | FMO monitors the MX exception blotter. After static-data correction or service recovery, FMO can replay; otherwise staff draft manually. |
  | ENISIS misses a message sent by RATAN over SFTP. | FMO downloads the Murex payment report from SSDR, extracts ENISIS MX, compares records, and drafts missing or failed payments. |

  The source describes these procedures; current ownership and applicability remain unconfirmed. [Murex KR recovery procedures](../../../evidence/sources/sha256/1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936.md#L65-L70)

  The ENISIS page separately describes FMO dashboard monitoring and SSDR reconciliation for missing acknowledgements or messages. It proposes an MX exception blotter with replay for RATAN exceptions. Manual drafting covers unresolved payments. Build and operating status are unstated. [ENISIS exception procedures](../../../evidence/sources/sha256/a7c48470a31afa6b04d49ab9f306c8bc285cda1d29ae968a2c8b9742173f2ec0.md#L60-L73)

- **FMSGW:** RATAN sends MT and MX settlement messages through Solace. The source lists MT countries `CN, MY, IN, SG, UK, DE, HK, TH, TW, US, ID, JP, MU, PH, UAE, ZA, TH`. The MX list is `MU, UK, CN, UAE, HK, SG, ZA, TW, MY, PH, TH, ID, IN, US, JP, DE`. Current scope is unknown. [FMSGW message route and scope](../../../evidence/sources/sha256/232860caf94e82f0651a7424384f85d6bff51906522c35e82e33f221490a515a.md#L9-L20)

- **FXU:** FXU queries cashflow status through the RATAN API. It sends JSON `FullUtilize` requests for SPOT, Forward, and SWAP products. The Solace route uses topics and queues between FXU and RATAN. [FXU interface](../../../evidence/sources/sha256/466c2b9b5f99556b638b48e172a3a1e80e940f5a4fee05127fbcdb967eef8ccb.md#L9-L27)

- **Razor:** RATAN sends SCBML V4.0 trade and event feeds, including `BOOKED` trades. Cashflow, status, ACK/NACK, affirmation, and failure feeds list London, Singapore, Hong Kong, Jersey, Egypt, and China 30 branches. Trade and event scope also names Taiwan, Germany, Malaysia, Thailand, Philippines, India, Sri Lanka, and Bangladesh. [Razor feed scope](../../../evidence/sources/sha256/b29b8ceb98aec1bc887770342d9d29f98572aad4e4c4e89cec3444ff4afd6738.md#L9-L28)

  Payment-status values include Released, Settled, Netted, Split, and CCPNetted for eligible payments. The source excludes UTIL trades and split/netting reversals and resultants. It states a 2M size limit. Utilization requests and ACK/NACK responses name Egypt, Nepal, and Saudi. [Razor payment-status conditions](../../../evidence/sources/sha256/b29b8ceb98aec1bc887770342d9d29f98572aad4e4c4e89cec3444ff4afd6738.md#L40-L42) [Razor utilization scope](../../../evidence/sources/sha256/b29b8ceb98aec1bc887770342d9d29f98572aad4e4c4e89cec3444ff4afd6738.md#L9-L28)

- **SSI+:** RATAN matches records using booking entity, counterparty code, currency, and CFI code. It attaches SSI data to cashflows and calls the SSI+ API in real time. SSI+ sends record-change notifications through Solace. [SSI matching and update flow](../../../evidence/sources/sha256/b6c7feb19f34aafa9178c93595b6297a96b9e3bb20aa6cb0756174f3cff936ec.md#L7-L15) [SSI API and notification channels](../../../evidence/sources/sha256/b6c7feb19f34aafa9178c93595b6297a96b9e3bb20aa6cb0756174f3cff936ec.md#L56-L60)

  The page assigns API and notification monitoring to SSI+ PSS. It assigns Solace subscription monitoring to RATAN PSS. It describes outage notices and response-time escalation; current ownership is unconfirmed. [SSI support procedure](../../../evidence/sources/sha256/b6c7feb19f34aafa9178c93595b6297a96b9e3bb20aa6cb0756174f3cff936ec.md#L56-L60)

## Connections

[Cashflow identity and Stella status write-back](KT-settlement-cashflow-identity-and-stella-write-back.md) covers related IDs, status events, and unresolved acknowledgement rules.
[Cash Settlement auto-netting](KT-settlement-auto-netting.md) covers netting rules and outcomes.
[Settlement cashflow feeds to LMS](KT-settlement-lms-feed.md) covers feed eligibility, account fields, and source-stack proposals.
[Korea trade confirmation](KT-settlement-korea-trade-confirmation.md) covers the distinct COMP gate and missing-confirmation diagnosis.

## Evidence limits

The sources describe different pairs, geographies, purposes, and dates. Do not combine them into one RATAN contract.
They do not establish current approval, configuration, deployment, or successful execution.
The selected pages establish no common current acceptance measure.

## Open questions

| Question | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Which current system contracts govern these feeds and API calls? | This candidate cannot establish active interface behavior. | unknown | Confirm exact contract revisions and owning teams. |
| Which entities, products, statuses, and dates apply to each exchange? | Scope differences could lead to incorrect cross-system assumptions. | unknown | Reconcile each source page with its applicable feed specification. |
| Which acknowledgement, retry, and exception rules apply to each flow? | Recovery behavior remains unresolved across the described interfaces. | unknown | Confirm the sender, receiver, acknowledgement, and retry condition for each message. |
| Which Korea message types and design revisions use SFTP or FM Solace between RATAN and ENISIS? | The selected pages describe different outbound channels and conversion paths. | unknown | Reconcile the approved contract by message type, stage, and revision. |
