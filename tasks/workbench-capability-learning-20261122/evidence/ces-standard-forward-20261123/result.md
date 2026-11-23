# CES offline evidence assessment

> The synthetic views disagree on assignments and role attribution. Their effective grant union matches.

Scope: `DEMO_REPORTS`, `demo-account`, offline inspection on 23 November 2026.
All demo bodies are synthetic, including examples carrying UAT metadata.
Seven inspector commands completed with exit code `0`.
[Command evidence](evidence.json) preserves their exact stdout and paired-example observations.

## Three-view consistency

| View | Exact observed summary | Conclusion and limit |
| --- | --- | --- |
| [Catalog](ces-domain-capability/Contracts/examples/catalog.json) | `CATALOG_PRESENT`; 3 entitlements, 2 accounts, 3 assignments, 3 role grants; application `CALLER_DECLARED` | The selected account belongs to Report Reader and Report Editor. These define Reports/View and Reports/Edit. Definitions and memberships do not establish effective enforcement. |
| [Assigned roles](ces-domain-capability/Contracts/examples/roles.json) | `ASSIGNMENTS_PRESENT`; 2 assignments, 1 without grants, 1 role grant; account `CALLER_DECLARED` | Report Reader attributes Reports/View. Unassigned Feature Set remains assigned despite its empty grant array. Its name does not mean assignment absence. |
| [Effective user](ces-domain-capability/Contracts/examples/user-before.json) | `PRESENT`; 1 assignment, 1 effective grant; attribution `UNAVAILABLE`; data sections `data_entitlements`, `data_profiles` | Report Reader and Reports/View are returned. Exact selectors return View `PRESENT`, Edit `ABSENT`. This describes the body, without proving actual allow or deny decisions. |

The effective body contains `Region: ["Example East"]` and empty `data_profiles`.
No `data_policies` section is present. These facts do not establish record visibility or policy precedence.

`reconcile` returned `COMPARED`, with effective-user status `PRESENT`.
All five comparisons follow. Added means present only on the right; removed means present only on the left.

| Comparison | Status | Added | Removed | Exact difference |
| --- | --- | ---: | ---: | --- |
| Catalog → assigned-role assignments | DIFFERENT | 1 | 1 | Add Unassigned Feature Set; remove Report Editor |
| Catalog → effective assignments | DIFFERENT | 0 | 1 | Remove Report Editor |
| Assigned-role → effective assignments | DIFFERENT | 0 | 1 | Remove Unassigned Feature Set |
| Catalog → attributed role grants | DIFFERENT | 0 | 2 | Remove Report Editor's Reports/View and Reports/Edit |
| Assigned-role union → effective grants | MATCH | 0 | 0 | Both contain only Reports/View |

A matching union does not establish overall consistency, synchronization, or policy correctness.
Catalog application and role-account identities require independent request bindings.
Their environment, observation time, completeness, and compatible capture boundaries remain unproved.

Sources: [reconciliation rules](ces-domain-capability/Workflows/inspect-captures.md#reconcile-catalog-assigned-roles-and-effective-access),
[view contracts](ces-domain-capability/Contracts/README.md), and [access concepts](ces-domain-capability/Knowledge/domain-model.md).

## Paired UAT examples and function_entitlement

The packaged envelopes describe successful GET responses with HTTP status `200`.

| Packaged example | Exact body observation | Boundary |
| --- | --- | --- |
| [Effective A](ces-domain-capability/Contracts/examples/effective-user-a-uat-pair.json) | application-001/account-001; 5 assigned names; 47 flattened grants | Complete single-record example; HTTP Date 3 November 2026, 05:33:51 GMT |
| [Effective B](ces-domain-capability/Contracts/examples/effective-user-b-uat-pair.json) | application-001/account-002; 7 assigned names; 31 flattened grants | Different account; HTTP Date 3 November 2026, 05:33:42 GMT |
| [Catalog A](ces-domain-capability/Contracts/examples/catalog-a-uat-pair.json) | application-002; 3 selected rows, source indexes 0, 1, 3 | Incomplete projection of declared 40 originals; HTTP Date 05:33:19 GMT |
| [Catalog B](ces-domain-capability/Contracts/examples/catalog-b-uat-pair.json) | application-001; 2 selected rows, source indexes 0, 1 | Incomplete projection of declared 74 originals; HTTP Date 05:30:46 GMT |

No packaged response body contains a `function_entitlement` key.
This observation does not establish profile absence because its response locator remains unresolved.
The examples support structural checks and request/response identity matching.
They support no executed assertion about:

- A specific profile value, exactly one functional profile, or the unassigned wire value.
- Incompatible-assignment rejection, original-value preservation, or either account-type direction.
- Generic, System, or Service account behavior.
- Onboarding, switching, offboarding, re-onboarding, rename, deletion, or non-functional-change invariance.
- Immediate-read correctness, propagation deadlines, or live enforcement.

Assignment-name counts and data-profile arrays do not prove functional-profile cardinality.
Different accounts cannot establish a before-and-after profile transition.
Catalog projections cannot establish absent memberships.
HTTP Date headers do not establish independent retrieval times or current deployment.

The [source register](ces-domain-capability/Knowledge/sources.json) identifies original UAT sources under `http_sources`.
All four reference revision `31e508f75443916633cb196d013129ad82a65974` and `/examples/0`.
Each envelope retains exact source hashes and request/response locators.
Those originals were not opened during this assessment.

## Checking a sourced expected profile

Use the [functional-profile procedure](ces-domain-capability/Workflows/functional-profile.md).

1. Bind the body to application, account, account type, request, environment, and observation time.
2. Obtain the scoped response JSON Pointer and an independent approved assignment expectation.
3. Save the expected value as one JSON string, preserving case and spaces.
4. Use JSON `null` only when an independent source establishes that empty representation.
5. Run from the copied skill root:

```sh
python3 Workflows/tools/inspect_ces.py profile "$CAPTURE" --app "$CES_APPLICATION" --user "$CES_USER" --pointer "$PROFILE_POINTER" --expected "$EXPECTED_JSON"
```

The pointer starts inside one effective-user record and excludes the outer array index.
Use `~1` for slash and `~0` for tilde.
Add `--itam-id` only when independently sourced.
Pass the response body, without its paired-case envelope.

Report `MATCH`, `DIFFERENT`, or the exact unassessed reason.
`RECORD_ABSENT` and `VALUE_ABSENT` are distinct; missing differs from explicit null.
Exit code `2` identifies invalid evidence or arguments.
Retain input hashes, the pointer source, independent expectation, and observation boundary.

No profile command ran: neither a sourced pointer nor an independent expected value was supplied.
The register's `functional_profile_user_sources` records the 17 November requirements.
Its referenced clarification uses revision `73917a552bcaf0b6f4b20625c0a21cb22e86baa5`, lines 6–34.
The timing source uses that revision, lines 6–20.
These are registered references, rather than inspected original user answers.

Exactly-one-profile and rejection checks are requirements, without execution evidence.
Five seconds after CES confirmation is the selected test target; the CES NFR remains unconfirmed.
Keep the immediate read separate from deadline results.
Provisioning, propagation, acceptance, and deployment remain unassessed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks comprise seven successful local inspector commands.
  - Automated checks do not establish complete writing review.
```
