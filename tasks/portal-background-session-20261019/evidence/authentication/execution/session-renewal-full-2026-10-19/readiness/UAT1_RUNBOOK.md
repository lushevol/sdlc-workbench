# Proposed UAT1 session extension check

This plan selects UAT1 from the user's instruction.
The proposal grants no operations and has not executed business tests.
The canonical catalogs and timeout remain unchanged.

## Scope

Run only `BAU-UI-RP-LOGIN-001-006` from `Tests/ratan/workspace/ui/BAU-UI-RP.robot`.
Robot still executes the suite setup and its imported initialization.
The filter excludes the cashflow creation case and every other test.
The existing login cases have exact suffixes `001` through `006`.
This proposal selects suffix `006` only.

The selected case waits for the expired-session prompt.
It selects Extend, opens MO Rules, and checks LIVE.
These assertions provide limited evidence of access after extension.
They do not establish complete verification of any acceptance criterion.

## Private inputs

Create this ignored file only when the approved values are available:

`/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace/.workbench/private/uat1.robot.variables.yaml`

Supply these variable names through that private YAML file:

- `SECRET`
- `USERNAME_MO`
- `PASSWORD_MO`
- `LOGIN_URL`
- `MARKETS_OPERATIONS_ONE`
- `SECURITY_SOURCE`

Supply `TEST_PORTAL_URL` and `TEST_PORTAL_CERTIFICATE_ENDPOINT` only when the approved setup uses portal certificate retrieval.
The `SECRET` binding selects the private environment configuration identifier.
The suite resolves `Tests/ratan/data/env_${ENV}_${SECRET}.yaml`.
Confirm that the resolved file belongs to UAT1.
The fixed command overrides the source default `stg` with `--variable ENV:uat1`.
The root `.env` alone does not bind Robot scalar variables.
No private values or endpoint URLs were read for this proposal.

## Readiness gates

1. Prepare the pinned Browser wrapper dependencies and compatible browser binaries.
2. Confirm the UAT1 URL, account permissions, private variable file, and certificate source.
3. Review suite setup effects before any external call.
4. Identify deployed application revisions and backend revisions.
5. Record the human reviewer and acceptance-criterion review.
6. Confirm that the output directory is fresh.
7. Activate only `list` and `run` for this resource after readiness passes.

Owner for each open gate: unknown.
The deployed UAT1 relationship to pilot commit `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8` remains unknown.
The local Java launcher has no runtime.
This limits local BFF execution; hosted UAT1 browser execution does not depend on that launcher.
The missing local Jest runner also limits separate source-test execution.

## Proposed configuration

Read `uat1-proposed-workspace/workspace.yaml` for the fixed command.
It contains one named suite and no execution grant.
The proposal sets its separate workspace timeout to 1800 seconds.
The current canonical timeout is 30 seconds.
The selected case allows 960 seconds for the prompt.

Run discovery after readiness and activation:

```sh
.venv/bin/ai-sdlc --workspace '/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace' status
.venv/bin/ai-sdlc --workspace '/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace' call uat1-session-extension list
```

Run the fixed named command only after the declared readiness gates pass:

```sh
.venv/bin/ai-sdlc --workspace '/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace' call uat1-session-extension run --args '{"suite":"session-extend-001-006"}'
```

These commands are proposed and were not used to run the business scenario.
The current empty grant rejects `list` and `run` calls.
The fixed command has no arbitrary suite or argument input.
Retain Robot output in the configured ignored directory.
Use a fresh output directory and proposal revision for each later run.
Keep native Robot results private until their logs receive a disclosure review.
Retain matching source, deployed revision, configuration, assertion, and execution evidence.

## Criterion limits

| Criterion | Missing assertion |
| --- | --- |
| AC-1 | Mouse activity causes successful renewal. |
| AC-2 | Keyboard activity causes successful renewal. |
| AC-3 | Scroll activity causes successful renewal. |
| AC-4 | Four hours of activity cause zero elapsed-time-only SSO prompts. |
| AC-5 | Pending renewal causes zero premature successful closures. |
| AC-6 | Successful renewal causes exactly one closure after completion. |
| AC-7 | Rejected renewal causes zero successful closures and permits retry. |

Every criterion remains `NOT_VERIFIED`.
A passing selected case must not change that verdict without the missing assertions and evidence.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

## Observed configuration blocker

The proposed workspace failed the actual CLI status check.
The inspected workspace schema limits `timeout_seconds` to 300.
The provider permits 3600, but that does not override schema validation.
The scenario permits 960 seconds for the prompt.
The proposed 1800-second timeout therefore needs a resolved supported contract before activation.
Read `proposed-UAT1-schema-validation.json` and `UAT1_TIMEOUT_FINDING.json` for retained evidence.
The earlier eight checks cover proposal invariants only.
They do not establish successful CLI loading.
No business test was executed.

```yaml
standard: ASD-STE100
automated_check: FAILED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

## Configuration check after the schema correction

The corrected schema permits a maximum timeout of 3600 seconds.
The proposed 1800-second workspace now passes the actual CLI status check.
A separate list attempt returned `DENIED`, as expected from the empty grant.
No provider operation or business test ran.
The earlier failure remains retained as historical evidence.
Read `proposed-UAT1-after-fix-verification.json` for command outputs and schema provenance.
Browser, private inputs, deployed revisions, and human review still prevent business verification.
The canonical workspace timeout remains 30 seconds.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
