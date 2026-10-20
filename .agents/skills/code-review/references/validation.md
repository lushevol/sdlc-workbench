# Validation and evidence

Read this reference before executing checks or reporting test, coverage, security, licensing, or analyzer conclusions.
Use repository instructions and existing tooling for the selected review scope.
Use [integration guidance](integrations.md) when evidence requires external systems.

## Establish execution identity

Record the repository, selected baseline, reviewed revision, and relevant worktree content identity.
Record staged and unstaged differences when either affects the review.
Include untracked source or tests when they belong to the requested scope.
Treat binary files and unavailable content as explicit review limits.

Bind each result to its command, working directory, configuration, tool version, environment, time, and exit code.
Retain output when the report requires reproducible execution evidence.
Redact credentials and sensitive values before retaining output.
State when a result came from existing evidence rather than a new execution.

Reuse earlier evidence only when its relevant identities and inputs still match.
A prior passing step does not validate changed source, tests, dependencies, configuration, or commands.
Do not skip review from a branch name or an unbound session checklist.

## Select meaningful checks

Inspect package scripts, build configuration, CI definitions, and repository guidance before choosing commands.
Prefer existing, installed tools and targeted tests that exercise the changed behavior.
Read assertions and fixtures before using a passing test as behavior evidence.
Expand checks when failures, interface effects, or unresolved risks justify broader execution.
Record unavailable platforms and external dependencies with the claims they limit.

Existing test execution can be appropriate during a review.
Review alone does not authorize generating tests, changing assertions, or modifying application source.
When the user requests fixes, add tests for confirmed defects or consequential behavior when appropriate.
Preserve existing test conventions and avoid unrelated changes.

Repository commands can execute arbitrary project code and contact external systems.
Inspect unfamiliar commands before execution.
Use isolated local fixtures where supported.
Do not run destructive checks or shared-environment operations without authorization for those effects.
Use existing authorization without asking for redundant approval.

## Preserve failures and limits

Keep the actual command exit code and useful error output.
Do not discard stderr or convert an execution failure into a missing-tool message.
Inspect structured tool results alongside process status.
Some analyzers use nonzero exit codes for findings; apply their documented exit semantics.
Distinguish command completion from the behavior or policy assertion being assessed.

| Status | Meaning |
| --- | --- |
| `PASSED` | The stated check executed and satisfied its explicit criterion. |
| `FAILED` | The check executed and demonstrated an unmet criterion. |
| `ERROR` | An execution or infrastructure problem prevented a reliable check result. |
| `SKIPPED` | A selected check was omitted; record the specific reason. |
| `NOT_RUN` | No execution was attempted for this check. |
| `UNAVAILABLE` | The required tool, evidence, platform, credential, or access was unavailable. |

Use `NOT_APPLICABLE` only when the check does not apply, with a scope-specific reason.
Do not classify an unavailable scanner, empty response, or skipped test as passing.
Report partial results when remaining checks fail or become unavailable.
State the consequence of each material validation gap.

## Compare baseline failures

When a check fails, determine whether the reviewed change caused the failure when practical.
Use matching commands, configuration, dependencies, and environments for baseline comparisons.
Use an isolated temporary checkout when baseline execution would otherwise replace user files.
Do not reset, stash, switch, or clean the user's checkout to create a baseline.
Record differences that prevent a fair comparison.

A baseline failure does not excuse a newly introduced failure.
An unchanged failure can remain a review limit without becoming a new defect finding.
Separate failing assertions from setup, dependency, and infrastructure failures.
After an authorized fix, rerun the relevant checks against the final content identity.

## Coverage and test quality

Compare coverage only when the tool, metric, test selection, source scope, and configuration are compatible.
Identify whether the metric measures lines, branches, functions, or another unit.
Bind baseline and candidate reports to their exact source and test identities.
Report missing coverage as unavailable evidence rather than zero or an invented delta.

Coverage does not establish assertion quality or requirement satisfaction.
Inspect meaningful assertions, failure paths, mock behavior, and relevant production boundaries.
Apply thresholds only when repository policy or the requested review defines them.
Do not generate tests solely to increase coverage during a review.

## Vulnerabilities and dependencies

Use existing dependency manifests, lockfiles, resolved versions, and available scanners.
Distinguish direct dependencies, transitive dependencies, development dependencies, and shipped runtime components.
Confirm the affected version range, advisory identity, source date, and relevant usage.
State exploitation prerequisites and reachability limits when they affect the conclusion.

Use current authoritative advisory sources when making current vulnerability claims.
Record the advisory source and retrieval time.
State stale database dates and offline evidence limits.
Do not claim that an offline scan establishes the absence of current vulnerabilities.

Disclose required network access and relevant data transmission before using an unfamiliar external scanning service.
Use network access only within granted access and user authorization.
Do not install scanners, refresh dependencies, or add startup downloads as an incidental review action.
An update recommendation requires compatibility evidence and appropriate current sources.

## Licenses

Inspect declared license metadata and license files for the exact resolved package version.
Record missing, conflicting, or compound license declarations.
Apply the organization's supplied policy to the relevant usage and distribution model.
Do not invent a universal allowlist, prohibited-license policy, or legal conclusion.
Identify unresolved legal questions and their decision owner when available.
Mark an unknown owner explicitly.

## SonarQube and other remote analyzers

Discover the available tools and exact grants through [integration guidance](integrations.md).
Confirm the project identity, branch or pull request, analyzed revision, analysis time, and completion status.
Check whether the analysis includes the relevant files and current configuration.
Treat results from another revision as historical evidence with an explicit freshness limit.
Do not describe them as the reviewed revision's result.

Distinguish existing issues from issues introduced by the selected comparison.
Distinguish server policy status from independently reviewed behavior.
Remote analysis can upload source and execute configured build steps.
Run it only within the authorized scope and access grants.

If remote analysis is unavailable, continue appropriate local review and record the missing evidence.
Local heuristics do not replace SonarQube analysis or reproduce its quality gate.
Do not invent tool names, project keys, findings, or scan results.
