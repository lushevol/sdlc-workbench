# Verify a local change

Required capabilities: `knowledge.read`, `repository.diff`, `testing.run`.
Optional capabilities: `logs.search`, `database.query`, `discovery.instances`.

1. Identify the requirement, repository, comparison refs, and execution environment.
2. Read the exact requirement and retain its source hash.
3. Inspect the repository diff for the selected refs.
4. Identify the assertions that evaluate the requested behavior.
5. Run the configured test suite and retain its action ID.
6. Inspect the result and retained output files.
7. Collect relevant logs or database rows when the workflow requires them.
8. Report differences with evidence, consequence, owner, and next action.

Keep test inspection separate from actual execution.
Keep demonstration fixtures separate from service observations.
Do not claim `VERIFIED` from an action status alone.
Missing evidence leaves the behavior unresolved.
