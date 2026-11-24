# Eight-area workbook structure

- Source: User message in the current Codex conversation.
- Date: 2026-11-18, Asia/Singapore.
- Scope: Migration expectations and functional entitlement lifecycle cases.

## Exact user input

Here is how I envision the test case spreadsheet being structured:\
\
1\. Tab 1 (Existing Accounts - Migration Consistency)\
&#x20; ◦ Do not include steps or status; simply state the expected outcome directly.\
&#x20; ◦ All users in the X-Rotation-1 Security Matrix Excel and their corresponding roles must match.\
&#x20; ◦ Once these users are onboarded to production, the functional_entitlement field must match the corresponding role listed.\
&#x20; ◦ List these data points and their expectations in the first tab.\
2\. Tab 2 (Service and Generic System Accounts - Migration Consistency)\
&#x20; ◦ These accounts and their corresponding roles are pulled from the runtime_func security matrix Excel.\
&#x20; ◦ For production, their function_entitlement must also match this data.\
&#x20; ◦ Tabs 1 and 2 cover existing accounts and mean that permissions must remain consistent with pre-migration states.\
3\. Tab 3 (Role Modification)\
&#x20; ◦ When a user changes from one role to another, their function_entitlement must change accordingly.\
&#x20; ◦ We require that function_entitlement changes dynamically with the user's actual permissions.\
4\. Tab 4 (New Functional Permission Grant)\
&#x20; ◦ For users who previously had only data permissions without a functional entitlement rule: when they acquire a functional entitlement, the field goes from empty to having a corresponding value.\
&#x20; ◦ Please provide an example using a user ID and their corresponding role.\
5\. Tab 5 (Functional Role Offboarding)\
&#x20; ◦ For users who previously had a functional role within the entitlement rules and are now offboarded (removed): the functional_entitlement field in this case should be empty.\
6\. Tab 6 (Account Separation)\
&#x20; ◦ General accounts and user accounts must not cross over.\
&#x20; ◦ System account functions should be bound to runtime_func, while user accounts should be bound to the original X-runtime roles.\
&#x20; ◦ These two sets of roles should not intersect.
7\. When the entitlement or role itself changes, for instance, if its name is changed or it is deleted outright, we expect any accounts with the corresponding functional entitlement field to be updated accordingly.\
8\. Conversely, if only other, non-functional entitlements change, it should not trigger an update.

## Source interpretation

The supplied filenames are `X_RATANONE_security_matrix_prod.xlsx` and `RATAN_FUNC_security_matrix_prod.xlsx`.
Use those matrices for the first two tabs. Preserve both historical account-type conflicts for resolution.
The established API field is `function_entitlement`; the latest message also uses `functional_entitlement`.
Retain the established identifier and state this naming interpretation in the workbook.
Items 7 and 8 add role-definition change and non-functional-change areas.
This request specifies expected behavior. It does not authorize CES execution or production mutations.
