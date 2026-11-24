# CES functional profile checks

## Purpose and prerequisites

Compare a sourced functional profile value with an independent expected value and review scoped provisioning evidence.
Read the [source register](../Knowledge/sources.json), [variable guide](variables.md), and [response contracts](../Contracts/README.md).
The exact response field and empty representation remain unresolved. Obtain their scoped evidence before asserting a profile value.
The tool accepts a JSON Pointer relative to one effective-user record and an expected JSON string or `null` file.
Keep expected values in local private storage. The tool prints only `MATCH`, `DIFFERENT`, or an unassessed reason.

## Procedure and decision rules

Use the exact `function_entitlement` value from the response location established for the scoped contract.
Obtain the expected value from the approved assignment source independently of the response under test.
Check the exact profile name and preserve its case and spaces.
For an assigned account, verify one functional profile under the applicable account-type rule.
A missing response leaves the value unassessed. Confirm the empty wire representation for a present account without a profile.

| Investigation | Evidence to retain |
| --- | --- |
| Read or change an assignment | Record the account type, prior value, requested profile, response, and subsequent read. Cover onboarding, switching, offboarding, and re-onboarding. |
| Reject an incompatible assignment | Review the recorded request and rejection, then check that the reread preserves the original value. Cover both account-type directions on assigned and empty accounts. |
| Change a profile definition | Check that a rename reaches affected accounts. Check the confirmed empty value after deletion when no replacement exists. |
| Change non-functional access | Compare the functional value before and after changes that affect data scope or other non-functional entitlements. |
| Assess timing | Record the first scoped read separately from the elapsed time after change confirmation. Use the case's test target and report the service objective only when separately sourced. |

Review Generic, System, and Service coverage individually when those cases apply.
Preserve conflicting historical assignments as evidence gaps until their owners resolve them.
The workflow assesses evidence from supplied reads and provisioning results. It supplies no provisioning command.

1. Bind application, account type, request route, environment, and observation time to the effective-user capture.
2. Obtain the field locator and expected profile independently of that capture.
   Preserve case and spaces. Treat an empty-value assertion as unknown until its representation is sourced.
3. Export the expected value to a local JSON file. Use a string or explicit `null` only when justified by its source.
4. Run the command with the sourced pointer and expected-value file.
5. Retain the status, input hashes, source locator, and independent expected-value source in the owning task.
6. For change scenarios, compare the immediate read and deadline result separately. Preserve either failed observation.

```sh
python3 Workflows/tools/inspect_ces.py profile "$CAPTURE" --app "$CES_APPLICATION" --user "$CES_USER" --pointer "$PROFILE_POINTER" --expected "$EXPECTED_JSON"
```

Use `--itam-id` when the external application reference is independently known.
The pointer excludes the outer response-array index. JSON Pointer escapes are `~1` for `/` and `~0` for `~`.
This command compares the selected captured value. It does not discover the correct profile field or validate an assignment policy.
No profile field is added to the OpenAPI schemas from this workflow or its synthetic tool tests.

## Failure points, verification, and recovery

| Condition | Tool outcome | Required interpretation |
| --- | --- | --- |
| Effective-user record absent | `UNASSESSED`, `RECORD_ABSENT` | No value was assessed |
| Pointer target absent | `UNASSESSED`, `VALUE_ABSENT` | Missing differs from an explicit null value |
| Captured value differs from sourced expectation | `DIFFERENT` | Investigate the exact value and observation boundary in private evidence |
| Invalid pointer, wrong identity, or non-string expected value | Exit code 2 | Repair the evidence binding; preserve original inputs |

An explicit captured null can match an expected JSON null. This does not establish that CES uses null for an unassigned profile.
The 17 November user answer selected five seconds as a test target, with confirmation as the measurement convention.
It did not confirm a CES NFR. Later correctness cannot replace the separate immediate-read result.
No provisioning, rejection, propagation, or live recovery was executed by this workflow.
Use retained authorized provisioning evidence for those claims; never mutate access solely to enrich this library.
