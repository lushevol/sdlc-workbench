# Offline CES assessment

The synthetic views are partly inconsistent. Their effective grant union matches, but four comparisons differ.
The UAT pairs support retained response structures. They do not verify a `function_entitlement` value or provisioning behavior.

## Synthetic consistency

Scope: `DEMO_REPORTS`, `demo-account`; role selectors: `appId=demo-reports`, `appUID=101`.
All successful commands exited zero. The catalog application and assigned-role account are caller-declared.

| Comparison: left to right | Status | Added | Removed |
| --- | --- | ---: | ---: |
| Catalog to assigned-role assignments | DIFFERENT | 1 | 1 |
| Catalog to effective assignments | DIFFERENT | 0 | 1 |
| Assigned-role to effective assignments | DIFFERENT | 0 | 1 |
| Catalog to attributed role grants | DIFFERENT | 0 | 2 |
| Assigned-role union to effective grants | MATCH | 0 | 0 |

`Added` means right-only. `Removed` means left-only.
The catalog assigns Reader and Editor. The role view assigns Reader and Unassigned Feature Set.
The effective view assigns Reader alone. The role view retains its explicit empty-grant assignment.
Both effective unions contain `Reports`/`View`. The catalog also attributes View and Edit to Editor.
Union equality cannot establish matching assignments, attribution, synchronization, or correct policy.

Observed inspector summaries:

- Catalog: three definitions, two accounts, three memberships, and three attributed grants.
- Assigned roles: two assignments, one without grants, and one grant. Reader and Reports/View are present.
- Effective user: one assignment and one grant. Reports/View is present; role attribution is unavailable.

## UAT pairs and evidence classes

| Input | Evidence class | Observed output and limit |
| --- | --- | --- |
| `catalog.json`, `roles.json`, `user-before.json` | Synthetic tool examples | Demonstrate deliberate local differences; establish no captured account parity. |
| Effective user A | Sanitized retained HTTP observation | HTTP 200; one matched record; five assignments; 47 effective grants. |
| Effective user B | Sanitized retained HTTP observation | HTTP 200; one matched record; seven assignments; 31 effective grants. |
| Catalog A | Sanitized retained HTTP observation, projected body | HTTP 200; three selected definitions from 40; application-002. |
| Catalog B | Sanitized retained HTTP observation, projected body | HTTP 200; two selected definitions from 74; application-001. |
| `assigned-role-body-fixture.json` | Sanitized supplied SDK body fixture | No retained request account, HTTP status, environment, or observation time. |

Effective A and B select application-001 and different accounts. They are not before/after snapshots.
Their request and response identities match, including the retained ITAM alias.
All four pairs retain UAT scope and HTTP Date headers from 3 November 2026.
Dates do not prove current deployment or independent retrieval time. Catalog subsets cannot prove absent memberships.

No literal `function_entitlement` key appears in the four packaged bodies.
The documented field locator and empty representation remain unresolved. Absence of that key does not establish CES-wide behavior.
Assignment-name counts and flattened grant counts do not establish exactly one functional profile.
The pairs provide no incompatible-assignment rejection, preserved reread, account-type binding, or provisioning sequence.
They cannot verify onboarding, switching, offboarding, re-onboarding, rename/deletion propagation, or non-functional-change isolation.
They establish neither immediate-read correctness nor five-second propagation conformance. Consumer enforcement remains unobserved.

## Check a sourced expected profile

First bind the capture to its application, account type, request, environment, and observation time.
Obtain the exact field pointer from the applicable contract. Obtain the expected profile independently from approved assignment evidence.
Preserve case and spaces. Store the expected JSON string locally; use null only with sourced empty-value semantics.

```sh
python3 ces-domain-capability/Workflows/tools/inspect_ces.py profile "$CAPTURE" --app "$CES_APPLICATION" --user "$CES_USER" --pointer "$PROFILE_POINTER" --expected "$EXPECTED_JSON"
```

The pointer is relative to one record, excluding the outer array index. Add `--itam-id` when independently known.
Retain input hashes, pointer source, expected-value source, and status. `MATCH` means captured-value equality only.
`DIFFERENT` preserves a discrepancy. `RECORD_ABSENT` and `VALUE_ABSENT` leave the assertion unassessed.
A matched explicit null does not establish CES's general empty-profile contract.
Preserve immediate-read and deadline outcomes separately. Five seconds is a sourced user test target, not an approved CES NFR.
No profile command ran because no independently sourced pointer and expected value were supplied.

All 26 supplied manifest hashes matched. No inputs changed; no network or provisioning actions occurred.
Eight body inspections succeeded. Earlier CLI-only failures and their corrections remain in `evidence.json`.
Only this skill copy and its manifest supplied evidence. Referenced originals were not reopened.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
