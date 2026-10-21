---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Runtime test contract

These tests protect capabilities that the Workbench currently ships.
They check observable results, retained records, external interfaces, and shipped contracts.
They do not establish business behavior coverage.

| Current consumer | Tests | Observable checks |
| --- | --- | --- |
| Workspace users | [Workspace layout](test_workspace_layout.py), [local configuration](test_workspace_v2.py) | Clean initialization, shipped guides, excluded runtime source, local paths, validation results, and source preservation. |
| Registry readers | [Catalogs](test_catalogs.py) | Valid identities, references, exact revisions, source declarations, and separate execution grants. |
| Knowledge reviewers | [Knowledge validation](test_knowledge_governance.py) | Required fields, measurable criteria, snapshot hashes, audit records, publication gates, and read-only validation. |
| Tool callers | [Core runtime](test_core.py) | Granted operations, argument rejection, retained outcomes, evidence hashes, and filesystem boundaries. |
| Provider maintainers | [Providers](test_providers.py) | Source reads, Git operations, retained command output, timeouts, log matches, bounded queries, and registry responses. |
| Robot test callers | [Robot provider](test_robot_provider.py) | Execution grants, suite confinement, separate statuses, native evidence, source identity, dry runs, failures, and timeouts. |
| Agent clients | [Interfaces](test_interfaces.py) | CLI outcomes, MCP protocol handling and shared operation results. |

The fixtures in [support.py](support.py) supply isolated resources for runtime tests.
They belong to the test suite and do not create product demonstrations.

## Removed duplication

Seven test methods were removed or consolidated.
Catalog tests retain the metadata execution boundary and catalog-count assertions from the removed layout test.
The catalog reference and identity tests replace the narrower layout regression.
The clean initialization test retains the removed guide and ignore-rule checks.
Two demo tests and two dashboard tests were removed with those product features.

The clean initialization test also rejects copied runtime modules, `src/`, and `tests/` in generated workspaces.
This check protects the boundary between the source distribution and generated workspace data.

## Stronger checks

The required-field test now uses a valid document body before removing one field.
The identity test now preserves complete catalogs before adding one invalid record.
Both tests first check that their unchanged fixtures are valid.
These changes prevent unrelated validation errors from satisfying the assertions.

Owner: Workbench maintainer. The named owner is unknown.
Next action: require a current consumer and observable assertion for each new test.

## Evaluate skill decisions

Use these evaluations when changing task summaries, behavior comparisons, setup readiness, or deployment evidence procedures.
Their current consumer is the maintainer of those shared skills.
The [case catalog](skill-evaluation-cases.json) contains seven synthetic requests derived from repeated user corrections.
It covers known answers, stale results, regression attribution, misleading passing assertions, review scope, setup readiness, and deployment evidence.
Synthetic records represent evaluation inputs. They establish no actual business policy, approval, or execution.

Prepare one case in a new external directory:

```sh
python tests/skill_evaluation.py --case current-results --output /tmp/workbench-current-results-trial
```

The [preparer](skill_evaluation.py) creates isolated inputs and two local Git revisions.
It records input hashes and listed skill document hashes in `evaluation-input.json`.
It refuses an existing output directory. Choose a new directory for each trial.
Use `--skills-root PATH` to evaluate another checkout or an initialized workspace.
The helper calls no model, external service, or business test runner.

Give an independent agent only that input manifest and its referenced fixture and skill files.
Ask the agent to execute the manifest's prompt within its stated boundaries.
Keep the [assessor rubric](skill-evaluation-rubric.json) outside the evaluating agent's context.
Save each completed response and requested artifact before evaluating another case.
Preserve command outputs when they support the response's claims.

Then assess each rubric criterion against the actual response and cited evidence.
Record `PASSED`, `FAILED`, or `NOT_ASSESSED` for each criterion with an evidence locator.
Recheck input hashes, repository status, selected branch, and index after each trial.
Retain consequential failures and scope violations. Refine guidance only when observed results justify the change.

Keep deterministic preparation checks separate from semantic assessment and ASD writing review.
Passing these cases does not establish general skill reliability or business behavior verification.
No automatic replay schedule, model dependency, or semantic grader is installed.
