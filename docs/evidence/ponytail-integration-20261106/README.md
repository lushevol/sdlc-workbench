# Ponytail integration

No critical conclusions require user attention or action.

## Authority and result

The [preserved user request](user-input.md#exact-user-input) authorizes project installation and use for coding tasks.
This change maintains the Workbench harness.
Business intake and domain knowledge changes do not apply.

Ponytail is installed as a [shared coding skill](../../../.agents/skills/ponytail/SKILL.md).
[Project guidance](../../../AGENTS.md#coding-tasks-with-ponytail) selects `full` mode for coding tasks.
The user can request `lite`, `ultra`, or `off`.
Required scope, tests, evidence, security, accessibility, and authorization checks remain applicable.

## Source and scope

The installed skill preserves upstream revision `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`, dated 29 October 2026.
The upstream package version is `5.3.3`.
The [source record](../../../.agents/skills/ponytail/SOURCE.md) retains the skill hash and [MIT license](../../../.agents/skills/ponytail/LICENSE.md).

The integration includes coding guidance, a Claude discovery alias, distribution metadata, and the existing test inventory.
The [setup guide](../../SETUP.md#ponytail-coding-skill) explains installation and discovery.
The [dependency analysis](../../DEPENDENCIES.md#browser-assets-and-documentation) records the instruction-only boundary.
The existing runtime discovers shared skills and packages them into generated workspaces.
No additional runtime package, service, hook, installer, doctor prerequisite, or startup download is required.

Affected consumers: coding agents, CLI skill readers, Claude discovery, wheel packaging, initialization, and offline source fingerprints.
Qualitative risk: Low because the integration adds instructions and uses existing distribution paths.
Unrelated worktree content remains outside this change.

## Validation

The declared runtime inventory contains 883 tests.
The [complete runtime run](unit-tests.log) passed all 883 tests in 79.416 seconds.
It reported zero failures, errors, skips, and expected failures.
The command enabled available optional Node integrations through `WORKBENCH_CONNECTOR_INTEGRATION=1`.

The [wheel build](wheel-build.log) passed with installed build tools and `--no-build-isolation`.
The [external package check](package-check.json) passed 17 assertions using the built wheel.
Those assertions cover exact skill, source, and license bytes; CLI discovery; Claude discovery; empty catalogs; and workspace validation.
The [source workspace validation](workspace-validation.json) also passed without findings.
The [verification binding](verification.json) records commands, source hashes, artifact hashes, and document checks.

The first [sandbox run](unit-tests-sandbox.log) encountered 36 errors while binding local mock-server ports.
It reported 876 attempted tests and two optional Node skips.
A class setup error prevented seven declared tests from running.
The successful rerun allowed local networking and enabled the optional integrations.
No application code or test assertions changed for those environment errors.

The first package probe compared resolved and unresolved macOS temporary paths.
Its [retained diagnostic](package-check-path-error.json) confirms both paths resolve to the same canonical skill.
The corrected probe resolves both paths before comparison.

## Limits and maintenance

The package check uses existing interpreter dependencies with an isolated external target installation.
Native Windows execution and model adherence were not measured.
Existing tests cover the forwarding fallback when directory links are denied.
Connected package acquisition and a fresh complete offline bundle were not rerun.
Rebuild existing offline bundles from matching source because their fingerprints include shared skills.
Client discovery can require the next turn or a new session.

Owner: Workbench maintainer; the named owner is unknown.
Next action: use the installed skill for coding tasks and review source identity before deliberate updates.
No implementation blocker remains.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
