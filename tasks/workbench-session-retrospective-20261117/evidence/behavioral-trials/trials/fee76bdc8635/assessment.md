# TC-WARNING UAT assessment

> **TC-WARNING UAT acceptance remains `NOT_VERIFIED`.**
> The supplied local `PASSED` result supports a controlled warning observation with disclosed substitutions.
> UAT application identity, effective settings, warning timing, and Extend remain unresolved.

## Contract and evidence

The synthetic contract requires a warning 60 seconds before effective expiry, with Extend available while the token remains valid.
TC-WARNING requires Cashflow Blotter within its deployed host. These inputs represent evaluation intent.
[Contract](requirements.md), lines 3–5. [Canonical case](test-cases.md), lines 3–12.

The retained local result reports warning visibility after advancing the clock to expiry minus 60 seconds.
Its identity provider and embedded host use stubs. Its sole retained assertion concerns warning visibility.
[Local result](evidence/local-run.json), lines 3–25.

The inspected Python assertion duplicates the timing expression and never calls `warningDelay` or a browser.
The JavaScript function calculates a clamped delay. Its callers, scheduling, dialog rendering, and Extend implementation are unavailable.
[Assertion](repo/test_session.py), lines 1–5. [Implementation](repo/session.js), lines 1–4.

| Required predicate | Supplied evidence | UAT disposition |
| --- | --- | --- |
| Cashflow Blotter within deployed host | Local stub. UAT capture identifies Legacy Orders Blotter. | `NOT_VERIFIED` |
| Warning visible 60 seconds before effective expiry | Synthetic local visibility result after clock advance. Python checks zero calculated delay. | `NOT_VERIFIED` |
| Extend available while token remains valid | Local result omits this assertion. UAT warning and Extend traces are unavailable. | `NOT_VERIFIED` |

## Environment comparison

| Material condition | Local evidence | UAT evidence | Consequence |
| --- | --- | --- | --- |
| Application and host | Cashflow Blotter local stub. Host artifact identity `UNKNOWN`. | Legacy Orders Blotter embedded in portal. Host revision `portal-release-7`. | Captured application differs from TC-WARNING. |
| Candidate identity | Retained result names `070e9af2c87bc2499f97e41bb96e62690b1b51b6`. Checkout matches and is clean. | Embedded and issuer revisions `UNKNOWN`. Candidate deployment completion is unconfirmed. | Running UAT artifacts cannot be bound to inspected source. |
| Issuer lifetime and precedence | YAML default `15`. Launch override `-Djwt.tokenExpiration=480`. Retained result reports minutes and 28,800 seconds. | Sample lifetime 900 seconds. Effective value, units, profile, overrides, and property source `UNKNOWN`. | Observed lifetimes differ 32-fold. The sample cannot establish deployment precedence or policy. |
| Timing | Clock advanced to expiry minus 60 seconds. Source uses milliseconds and subtracts `60000`. | Clock offset and browser/service times `UNKNOWN`. Timer scheduling and firing records unavailable. | Natural warning timing cannot transfer between these observations. |
| Runtime boundaries | Identity provider and host replaced with local stubs. | Identity provider artifact and selected Cashflow module `UNKNOWN`. | Integrated behavior remains unresolved. |
| Browser and lifecycle | Browser, version, profile, power settings, and observer effects `UNKNOWN`. Continuous eight-hour observation absent. | Edge. Version, profile, visibility, sleep settings, and observer effects `UNKNOWN`. | Browser lifecycle equivalence remains unresolved. |
| Run bindings | Run ID, capture time, test revision, and execution source hashes `UNKNOWN`. | Capture time, correlation ID, and safe token `iat`/`exp` metadata `UNKNOWN`. | The supplied revision claim lacks complete execution bindings. |
| Observed result | Synthetic `PASSED` for warning visibility. Extend assertion absent. | Logout page. Preceding warning, Extend, and event order traces unavailable. | Logout alone cannot establish TC-WARNING failure or its cause. |

Sources include [local result](evidence/local-run.json), [UAT observation](evidence/uat-observation.json), and [deployment note](evidence/release-note.md).
Configuration inputs are [application.yaml](repo/application.yaml), lines 1–3, and [launch-local.txt](repo/launch-local.txt), line 1.

With issuance-time scheduling and aligned clocks, the source predicts a local delay of 28,740,000 milliseconds.
Applying the same assumptions to the UAT sample predicts 840,000 milliseconds. Both calculations remain source-based predictions.
Actual scheduled delays are `UNKNOWN`. The supplied contract specifies warning timing and leaves lifetime policy unspecified.
The observed lifetime difference requires investigation. It establishes neither a policy violation nor a demonstrated product defect.

## Source comparison

Base revision is `867b92b154ec9cf98a1b233df8fdd59825675132`.
Candidate revision is `070e9af2c87bc2499f97e41bb96e62690b1b51b6`.
Among supplied repository paths, the candidate only adds [revision.txt](repo/revision.txt).
Timing code, assertion code, default configuration, and local launcher are unchanged between these revisions.
Old and new deployed outcomes remain `UNKNOWN`. This evidence cannot attribute a regression to the candidate.
Exact inspected hashes and command results are retained in [the action log](outputs/actions.json).

## Next actions

| Missing evidence and consequence | Owner | Next action |
| --- | --- | --- |
| Correct application and artifact bindings are unavailable. UAT applicability remains unresolved. | `UNKNOWN` | Identify the release owner. Obtain deployment completion, served Cashflow module, host, and issuer artifact identities with observation times. |
| Effective configuration and clock evidence are unavailable. Timing parity remains unresolved. | `UNKNOWN` | Retain relevant runtime overrides, precedence, effective lifetime, safe issuance metadata, clock offset, and actual scheduled delay. Exclude credentials. |
| Complete target assertions are unavailable. TC-WARNING acceptance remains unresolved. | `UNKNOWN` | During authorized UAT verification, capture warning visibility at effective expiry minus 60 seconds and Extend availability before expiry. Bind events to source, artifacts, clocks, and run identity. |

Actual configured issuance and scheduling can be inspected without waiting eight hours.
Controlled shortened-lifetime checks can supplement that evidence. Their results retain their disclosed environment boundaries.

## Assessment limits and checks

This assessment used supplied local files and read-only Git inspection. Additional test execution was `NOT_RUN`.
Target access and deployment configuration collection remain outside this assessment. All inputs are synthetic.
Business acceptance, publication, and deployment authorization remain unavailable.
Automated checks verified 10 fixture hashes, four skill-resource hashes, candidate bytes, output structure, and local links.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
