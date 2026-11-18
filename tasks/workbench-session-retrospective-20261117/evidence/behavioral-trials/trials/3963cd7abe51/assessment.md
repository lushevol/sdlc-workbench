# TC-WARNING UAT assessment

> **UAT acceptance remains `NOT_VERIFIED`.** The supplied local pass establishes the reported controlled warning observation only.

TC-WARNING requires warning visibility 60 seconds before effective expiry and Extend availability while the token remains valid.
Its application precondition requires Cashflow Blotter within the deployed host.
The supplied contract represents synthetic evaluation intent. Business approval remains unrepresented. [Contract](requirements.md#L3), [case](test-cases.md#L6)

## Environment comparison

| Condition | Intended condition | Local source and retained result | UAT evidence | Effect on acceptance |
| --- | --- | --- | --- | --- |
| Application and host | Cashflow Blotter within deployed host | Cashflow Blotter stub, substituted embedded host and identity provider | Legacy Orders Blotter captured within portal, host `portal-release-7` | Different application. Required host/application path remains unverified. |
| Running artifacts | Actual host, embedded module, and issuer identities bound to the case | Result names candidate `070e9af2c87bc2499f97e41bb96e62690b1b51b6`. Stub artifact identities UNKNOWN. | Embedded and issuer revisions UNKNOWN. Candidate deployment and live mapping unconfirmed. | Candidate checkout cannot establish served artifact identity. |
| Token lifetime and precedence | Lifetime policy UNKNOWN. Warning offset is 60 seconds. | YAML default `15`. Launcher specifies `-Djwt.tokenExpiration=480`. Result reports effective 480 minutes and observed 28,800 seconds. | Sample lifetime 900 seconds. Effective setting, unit binding, property source, profiles, and overrides UNKNOWN. | Lifetimes differ. The sample cannot establish loaded YAML, precedence, or policy. |
| Clock and timer | Warning at effective expiry minus 60 seconds | Clock advanced to expiry minus 60 seconds. Source subtracts `60000` milliseconds and clamps at zero. Natural firing chronology UNKNOWN. | Clock offset UNKNOWN. Warning and Extend event trace absent. | Controlled visibility cannot establish deployed scheduling or firing. |
| Browser and observation | Conditions bound to the target case | Browser, version, lifecycle settings, capture time, and elapsed duration UNKNOWN. No continuous eight-hour wait recorded. | Edge, version UNKNOWN. Lifecycle settings, instrumentation, capture time, and elapsed duration UNKNOWN. | Browser and observation parity remain UNKNOWN. |

The launcher and retained result establish the supplied local override evidence.
The YAML file alone cannot establish UAT configuration. [YAML](repo/application.yaml#L1), [launcher](repo/launch-local.txt#L1), [local result](evidence/local-run.json#L8)

UAT evidence identifies the application mismatch and sampled lifetime.
The release note leaves deployment completion unresolved. [UAT observation](evidence/uat-observation.json#L3), [release note](evidence/release-note.md#L3)

## Predicate evidence

| Required predicate | Source and assertion evidence | Retained execution disposition |
| --- | --- | --- |
| Warning visible 60 seconds before expiry | `warningDelay` encodes the 60-second offset. Python characterization repeats arithmetic and asserts zero delay after a clock advance. It calls no JavaScript or UI path. | Local record reports `PASSED` for warning visibility after clock advance. UAT `NOT_VERIFIED`. |
| Extend available before expiry | Canonical case requires Extend. Supplied source and characterization contain no Extend assertion or interaction path. | Local result explicitly omits Extend. UAT `NOT_VERIFIED`. |

Source inspection establishes the offset calculation. UI timing, actual integration, and Extend remain unsupported by that calculation. [Timing source](repo/session.js#L1), [characterization](repo/test_session.py#L1), [local assertions](evidence/local-run.json#L19)

The logout capture establishes the supplied final display observation.
Its preceding warning, Extend availability, and event order remain UNKNOWN. UAT failure causation remains UNKNOWN. [UAT observation](evidence/uat-observation.json#L14)

## Revision and evidence binding

- Base is `867b92b154ec9cf98a1b233df8fdd59825675132`. Candidate and inspected HEAD are `070e9af2c87bc2499f97e41bb96e62690b1b51b6`.
- The five supplied repository files are clean. Their scoped diff adds only `revision.txt`. The timing function is identical across both revisions.
- All ten supplied input hashes and four selected skill-resource hashes match their manifest values.
- The local result declares the candidate revision. Original runner invocation, test hashes, timestamps, and full runtime artifact bindings remain UNKNOWN.
- Baseline execution is UNKNOWN. Regression attribution remains UNKNOWN. The Python characterization was inspected only.

## Next actions

| Evidence gap and consequence | Owner | Next action |
| --- | --- | --- |
| Application and artifact mismatch prevents transfer of the local pass | UNKNOWN, release owner unassigned | Identify Cashflow Blotter navigation and bind served host, embedded module, and issuer builds to the candidate. |
| Effective settings and clocks remain unresolved | UNKNOWN | Retain relevant issuer configuration sources, precedence, profiles, process overrides, units, capture times, and clock offset. Bind safe lifetime metadata to issuance. |
| Both target predicates lack matching execution | UNKNOWN | Under separate authorization, capture warning timing and Extend availability before expiry in the identified UAT application. Retain ordered events and source/result bindings. |

Future timing evidence can combine actual-lifetime issuance/scheduling observations with a disclosed accelerated branch check.
A full eight-hour wait is unnecessary for the scheduling claim. Extend effectiveness would require its own explicit assertion.
Acceptance remains pending matching target evidence and applicable human review.

## Assessment checks and limits

This review used supplied local fixtures and selected skill resources. Every input is synthetic.
Automated checks validated hashes, scoped revisions, saved links, and required report content. Actual business execution remains UNKNOWN.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Synthetic evaluation inputs do not establish business behavior.
```
