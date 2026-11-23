# CES functional profile checks

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
