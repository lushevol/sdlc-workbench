---
artifact_kind: change-request
id: SESSION-PAIRED-VERIFICATION-20261030
version: 1
status: draft
owner: unknown
source_refs: [USER-20261030-GOAL]
related_ids: [RN-S001, RN-S002, RN-R020]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Paired session verification stage

> **The completed experiment retains an inherited expired-access logout failure.**
> Action: review the logout contract and verify the actual server consequence.
> Consequence: the proposed zero-access security assertion remains failed.
> Owner: unknown authentication and security owners. Evidence: [paired comparison](paired-comparison.json).

## Request and source facts

- Requester: current chat user; identity is not independently authenticated.
- Request source: [exact user instruction](user-input.md).
- Current baseline: BFF `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`, committed on 27 October 2026.
- Compared candidate: BFF `134a340472f29d2a4136e07e516690de6a18e323`, committed on 30 October 2026.
- Supported rationale: compare the same consequential assertions across actual application revisions.
- Evidence limit: local controller integration cannot establish production reachability or protected business impact.
- Entry route: bounded exploration, using existing canonical cases and retained execution evidence.
- Actual chronology: both supplied implementations precede this successor verification stage.

## Stage boundary and readiness

- Stage: paired local logout and refresh replay verification.
- Frozen intake: [original intake](../../01-intake.md), Workbench revision `840e8a9b727c4c7e95c88bc3276172c40e4d026b`.
- Intake SHA-256: `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`.
- Canonical catalog SHA-256: `5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037`.
- Compared implementation: the exact BFF revisions above; local business edits are excluded.
- Readiness: `READY` for this bounded local experiment only.
- Assessor and date: Codex agent, 30 October 2026, Asia/Singapore.
- Rationale: source revisions, canonical assertions, offline dependencies, and local authorization are available.
- Prior boundary: [previous checkpoint](../remaining-execution-20261029/stage-checkpoint.json) permits local probes without application changes.
- Blocked actions: production claims, application fixes, deployment, and business acceptance remain outside this stage.
- Resolution owner: unknown authentication owner; inspect actual endpoint behavior before production applicability claims.
- Intake integrity result: `PASSED`; intake and catalog bytes match their entry hashes. See [validation](validation.json).

## Proposed change

| Aspect | Current baseline | Proposed addition | Basis |
| --- | --- | --- | --- |
| Logout evidence | Earlier controller probe covers one BFF revision. | Repeat identical assertions on both pinned revisions. | [User instruction](user-input.md) |
| Failure classification | Current BFF revision lacks matching replay evidence. | Classify inherited behavior or regression through paired results. | [RN-S001](../../06-test-cases.md#rn-s001), [RN-S002](../../06-test-cases.md#rn-s002) |
| Unavailable contracts | Stale-response and protected-operation evidence has limits. | Name unresolved contracts and preserve their dispositions. | [Previous inventory](../remaining-execution-20261029/aggregate/final-inventory.json) |

## Scope and affected artifacts

| Artifact ID | Exact version | Effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| BFF baseline | `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a` | Export and compile selected source. | Retained source manifest | Low; checkout remains unchanged. | unknown |
| BFF candidate | `134a340472f29d2a4136e07e516690de6a18e323` | Export and compile selected source. | Retained source manifest | Low; checkout remains unchanged. | unknown |
| [RN-S001](../../06-test-cases.md#rn-s001) | Frozen catalog hash above | Reuse definition unchanged. | Per-case execution | Local assertion confidence only. | unknown |
| [RN-S002](../../06-test-cases.md#rn-s002) | Frozen catalog hash above | Reuse proposed security assertion unchanged. | Per-case execution | Policy remains proposed. | unknown |

## User impact

| Actor and journey | Trigger | Before and after | Consequence | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Synthetic signed-in user | Logout, then retained refresh replay | Observe both revisions with valid and expired access. | An issued access credential demonstrates local revocation failure. | No production or protected endpoint claim. | unknown authentication owner | Review paired results. |

## System impact

| Path | Consumer | Effect | Risk | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Logout controller | Refresh replay controller | Actual RSA and session-service path runs locally. | Mock persistence excludes replicas and database behavior. | Selected exact sources; servlet mocks. | unknown authentication owner | Verify actual deployment contract separately. |

## Options and consequences

| Option | Consequence | Evidence or inference | Required decision |
| --- | --- | --- | --- |
| Execute the paired local experiment. | Establish source-bound outcome and inheritance. | Exact revisions and identical assertions. | Authorized by [user input](user-input.md). |
| Claim production closure now. | Unsupported target and business assertions would remain. | No target evidence exists. | Not authorized or supported. |

## Proposed acceptance and validation

| Criterion | Canonical definition | Validation | Current result | Evidence |
| --- | --- | --- | --- | --- |
| [RN-S001](../../06-test-cases.md#rn-s001) | Existing observed case | Logout succeeds; replay returns 401; no access is issued. | PASSED on both revisions | [Comparison](paired-comparison.json) |
| [RN-S002](../../06-test-cases.md#rn-s002) | Existing proposed security case | Record logout outcome; require no replay access; observe HTTP 401. | FAILED on both revisions | [Comparison](paired-comparison.json) |

## Implementation and release proposal

- Implementation scope: new probe, runner, results, and comparison within this evidence directory.
- Proposed release: none; this experiment does not recommend a release.
- Estimate: unknown; compilation uses available offline verification dependencies.
- Reversal: remove only newly generated scratch exports; retain claim-bearing evidence.

### Bounded exploration

- Goal: save four revision-by-case results and compare each asserted observable.
- Boundaries: no business-source changes, credentials, network access, production tests, or deployments.
- Permitted edits: this evidence directory and its task evidence-index entry.
- Owner: Codex executes; accountable application owner remains unknown.
- Authorization: [current user instruction](user-input.md), with the retained local verification boundary.
- Stop condition: four results, or a retained compilation or execution blocker.
- Artifact disposition: preserve per-case results, meaningful failures, source hashes, logs, and comparison.

`READY` covers this exploration only. It does not establish approved security policy or business acceptance.

## Sources and evidence limits

| Source | Locator | Revision or hash | Authority and limit |
| --- | --- | --- | --- |
| User intent | [Preserved input](user-input.md) | SHA-256 recorded in execution manifest | Authorizes local goal verification. |
| Canonical cases | [Case catalog](../../06-test-cases.md) | Frozen hash above | RN-S002 remains proposed security behavior. |
| Earlier execution | [Original probe](../comprehensive-renewal-20261028/SecurityLogoutProbe.java) | SHA-256 recorded in comparison | Local actual-controller evidence; no HTTP server. |
| Dependency cache | Workbench `.workbench/current-bff-audit/` | Each used jar and cache class is hashed. | Public verification dependencies; production equivalence remains unestablished. |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Production request and revocation contract remains unavailable. | No target evidence in this stage. | Production applicability cannot be established. | unknown authentication owner | Supply the deployed endpoint and store contract. |
| Protected mutation endpoint remains unnamed. | [Combination summary](../remaining-execution-20261029/combinations/combination-summary.json) | Durable commit assertions remain unavailable. | unknown business-service owner | Name an authorized endpoint and commit observation. |

## Stage evidence and completion

| Stage | Required evidence | Record | Current result | Remaining blocker |
| --- | --- | --- | --- | --- |
| Impact analysis | Exact caller paths and boundaries | This record | Local scope established | Production applicability unavailable |
| Code review | Paired source and assertion inspection | [Source inspection](paired-source-inspection.json) | Selected methods match | Whole BFF migration remains unassessed |
| E2E expansion | Canonical inventory and explicit assertions | [Shared probe](SecurityLogoutProbe.java), [execution](paired-execution.json) | Four local cases completed; two failed | No real server in this stage |
| Browser execution | Actual target browser journey | Outside stage | NOT_RUN | Requires separate endpoint and environment contract |

## Requested decision and actual disposition

- Requested decision: complete and verify planned improvements using real cases.
- Authorized decision owner: current chat user for this local verification request.
- Actual decision: execute this bounded experiment.
- Decision reference: [preserved instruction](user-input.md).
- Implementation status: probe and evidence only; application source remains unchanged.
- Intent review: RN-S001 is observed behavior; RN-S002 remains proposed security behavior.
- Execution outcome: four local cases completed; two passed and two failed. See [report](02-paired-verification-report.md).
- Business acceptance: pending; this stage cannot establish acceptance or deployment authorization.
