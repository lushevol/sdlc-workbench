# CES investigation workflows

## Purpose and prerequisites

Inspect retained CES JSON, attribute grants, compare two snapshots, or reconcile three views without contacting CES.
Use Python 3.10 or newer. The inspector uses the standard library and prints counts or statuses without account values.
Bind source requests, application, account, environment, observation boundary, and completeness before interpreting the results.
Use the [contracts](../Contracts/README.md), [source register](../Knowledge/sources.json), and [variable guide](variables.md).
Export response bodies into private local files. Paired-case envelopes must not be passed as response bodies.

## Inspect a capture

Take application, account, grant, and evidence inputs from the task's [variable file](variables.md).

1. Retain the request route, environment, result status, observation time, and source revision or capture digest.
2. Use a successful JSON body for the requested CES view. Keep request failures and incomplete collections visible in the investigation.
3. Run the matching command. Bind the catalog application to its capture metadata and the effective-user response to the request identity.
4. Check whether the reported counts match the expected definitions, assignments, or feature and action pairs.

## Explain an access difference

1. Identify the application, principal, feature, action, and affected data or resource.
2. Use the exact feature and action selector to check the returned functional grant. Inspect the applicable data sections for the same scope.
3. Trace the consumer's enforcement point and actual decision using scoped assertions or observations.
4. Report the expected decision, observed decision, supporting source, and unresolved conditions.

## Attribute a grant to an entitlement

1. Confirm the captured assigned-role request identifies the expected account and environment.
2. Select the CES application and use its internal UID when the request evidence identifies it.
3. Check the entitlement with the exact feature/action pair. Retain explicit empty grants as an assignment with no listed grants.
4. Check the effective-user view separately when the question concerns what the account can do.

## Compare two effective-user captures

1. Confirm both captures refer to the same application and account. Record which environment and time each represents.
2. Compare assignment and effective permission sets. Use the source captures to investigate reported differences.
3. Treat detected data-section changes as a signal to inspect the approved policy and predicates.
4. Keep comparisons with absent records unassessed.

## Reconcile catalog, assigned roles, and effective access

1. Bind a complete catalog and assigned-role body to the same application's captured requests.
   Catalog application and assigned-role account identity are caller-declared because their bodies omit those bindings.
2. Match the effective-user account and application. Supply `--itam-id` when that identity is independently known.
3. Run `reconcile` with the three body paths, exact account, application, and optional assigned-role application identifiers.
4. Read each comparison separately. Assignment names, role-attributed grants, and the effective grant union answer different questions.
5. Use the original sources to explain differences. Do not infer synchronization, denial, or policy correctness from set equality.

`added` means present on the right side but absent on the left. `removed` means present only on the left.
The command compares catalog memberships for the selected account against assigned roles and effective assignments.
It compares role-attributed catalog grants against assigned-role grants, then compares the assigned-role union against effective grants.
A matching union can coexist with different assignments or role attribution. Inspect every comparison.
An absent effective record makes effective comparisons unassessed; catalog-to-role differences remain available.

## Commands and outputs

Run these synthetic examples from the skill folder.

```sh
python3 Workflows/tools/inspect_ces.py catalog Contracts/examples/catalog.json --app DEMO_REPORTS
python3 Workflows/tools/inspect_ces.py user Contracts/examples/user-before.json --app DEMO_REPORTS --user demo-account
python3 Workflows/tools/inspect_ces.py user Contracts/examples/user-before.json --app DEMO_REPORTS --user demo-account --feature Reports --action View
python3 Workflows/tools/inspect_ces.py assigned-role Contracts/examples/roles.json --app DEMO_REPORTS --entitlement 'Report Reader' --feature Reports --action View
python3 Workflows/tools/inspect_ces.py compare Contracts/examples/user-before.json Contracts/examples/user-after.json --app DEMO_REPORTS --user demo-account
python3 Workflows/tools/inspect_ces.py reconcile Contracts/examples/catalog.json Contracts/examples/roles.json Contracts/examples/user-before.json --app DEMO_REPORTS --user demo-account
```

Commands read local files and print JSON summaries.
The paired selectors report a grant as `PRESENT`, `ABSENT`, or `UNASSESSED` in the captured response.
The assigned-role command reports account scope as `CALLER_DECLARED`.
Use `--app-id` for the string role-view identifier or `--app-uid` for the numeric UID when the capture supplies them.
The comparison reports grants and assignments added or removed and identifies changed data sections by field.
Inspect user or comparison status before interpreting counts. A command can succeed with an absent record or an unassessed comparison.
Use the original approved captures when exact grant names or data values are necessary.
The synthetic reconciliation deliberately produces assignment differences with a matching effective union.
The retained effective-user UAT cases concern different accounts. They cannot be used as a two-snapshot account comparison.

## Decision rules and verification

Check the command status before interpreting grants or counts. `MATCH` establishes local equality within the supplied evidence only.
Grant `PRESENT` and `ABSENT` describe a matched body. They do not establish consumer enforcement or data visibility.
Stop when request identity, completeness, source age, or observation boundaries do not support the intended conclusion.
Use the same account and application for `compare`; bind each snapshot's time and environment independently.
For `reconcile`, retain all five comparison results and the source bindings. Do not report only the matching union.
The tool accepts local JSON up to 16 MiB and rejects duplicate keys, nonfinite numbers, and ambiguous identities.
Exit code 2 reports invalid arguments or evidence. Exit code 0 can still report absent or unassessed evidence.

## Failure points and recovery

| Observed controlled case | Outcome | Recovery and limit |
| --- | --- | --- |
| Wrong account or conflicting nested application | Inspector rejects the input | Reopen request evidence; select the correct body. Do not rewrite the captured identity |
| Duplicate JSON keys or entitlement names | Inspector rejects ambiguous evidence | Retain the original failure and obtain an unambiguous export |
| Absent effective record | Effective comparisons remain `UNASSESSED` | Check request scope and completeness; do not convert absence into an explicit denial |
| Matching effective union with assignment differences | Separate comparisons retain the differences | Inspect role attribution and source observation boundaries |
| `--itam-id` supplied to `user` during offline usage | Invalid-arguments exit code 2 | That flag belongs to `reconcile` and `profile`; retain ITAM request binding separately for `user` |
| Process substitution supplied as a body path during offline usage | Regular-local-file error, exit code 2 | Export the body into a private regular JSON file before inspection |

These failures come from local negative fixtures or offline usage trials. They are not captured CES HTTP errors.
The current test source and execution are bound in the owning task's verification evidence.
No service error payload or successful live recovery was supplied for the four UAT pairs.
Commands perform no mutations. Keep source files immutable and save corrected inputs as new evidence.
Repeat only the relevant local inspection after repairing its input binding.

## Related knowledge

Use the [domain model](../Knowledge/domain-model.md) to distinguish assignments, effective grants, and data restrictions.
Use [domain facts](../Knowledge/domain-facts.md) for observed counts, supported shapes, and source limitations.
