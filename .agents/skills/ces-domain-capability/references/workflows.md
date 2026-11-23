# CES investigation workflows

## Inspect a capture

1. Retain the request route, environment, result status, observation time, and source revision or capture digest.
2. Use a successful JSON body for the requested CES view. Keep request failures and incomplete collections visible in the investigation.
3. Run the matching command. Bind the catalog application to its capture metadata and the effective-user response to the request identity.
4. Check whether the reported counts match the expected definitions, assignments, or feature and action pairs.

## Explain an access difference

1. Identify the application, principal, feature, action, and affected data or resource.
2. Use the exact feature and action selector to check the returned functional grant. Inspect the applicable data sections for the same scope.
3. Trace the consumer's enforcement point and actual decision using scoped assertions or observations.
4. Report the expected decision, observed decision, supporting source, and unresolved conditions.

## Compare two effective-user captures

1. Confirm both captures refer to the same application and account. Record which environment and time each represents.
2. Compare assignment and effective permission sets. Use the source captures to investigate reported differences.
3. Treat detected data-section changes as a signal to inspect the approved policy and predicates.
4. Keep comparisons with absent records unassessed.

Run these examples from the skill folder with Python 3.10 or newer.

```sh
python3 scripts/inspect_ces.py catalog assets/catalog.json --app DEMO_REPORTS
python3 scripts/inspect_ces.py user assets/user-before.json --app DEMO_REPORTS --user demo-account
python3 scripts/inspect_ces.py user assets/user-before.json --app DEMO_REPORTS --user demo-account --feature Reports --action View
python3 scripts/inspect_ces.py compare assets/user-before.json assets/user-after.json --app DEMO_REPORTS --user demo-account
```

Commands read local files and print JSON summaries.
The paired selectors report a grant as `PRESENT`, `ABSENT`, or `UNASSESSED` in the captured response.
The comparison reports grants and assignments added or removed and identifies changed data sections by field.
Inspect user or comparison status before interpreting counts. A command can succeed with an absent record or an unassessed comparison.
Use the original approved captures when exact grant names or data values are necessary.
