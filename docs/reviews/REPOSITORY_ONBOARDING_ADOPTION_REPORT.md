---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
- Static evidence checks do not establish approved intent, deployed connectivity, or passing business behavior.
- Windows execution remains untested.
---

# Repository onboarding adoption

The skill makes existing repositories understandable through inspected source evidence without moving their implementation.
It maps responsibilities, components, interfaces, tests, and readiness gaps for coding agents.
Registry outputs remain proposals until the requested review and adoption occur.
This purpose supports the Workbench's context and relationship responsibilities.

The current consumers are external agents, CLI and MCP skill discovery, and workspace initialization.
The observable benefit is one distributed procedure with compatible proposals and checks for exact source evidence.
[Workspace tests](../../tests/test_workspace_layout.py) exercise discovery, resource availability, initialization, and forwarding.
[Evidence tests](../../tests/test_repository_onboarding.py) exercise source identity and consequential inspection boundaries.

## Scope and risk

The baseline source revision was `574c22c51d83a845d509d723bc862f2ee62af314`.
The review inspected callers, imports, catalog schemas, initialization, packaging, and agent adapters directly.
No usable project index was required.

Changed interfaces include skill instructions, staging contracts, static helpers, package resources, and native discovery aliases.
The runtime remains under `core/` with the installed name `ai_sdlc_workbench`.
Qualitative risk is moderate because evidence validation and distributed workspace resources affect agent conclusions.
Unrelated README and SDLC template changes remain outside this stage's commit.

## Findings and disposition

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Registry proposals used an incompatible envelope and fields. | [Loader](../../core/context/catalogs.py), [updated mapping](../../.agents/skills/repository-onboarding/references/registry-contracts.md) | Proposals could fail loading or lose relationship meaning. | unknown | Use integer version 1 and supported fields; validate proposals externally. |
| Distribution omitted the skill and its helpers. | [Scaffold](../../scaffold.json), [source manifest](../../MANIFEST.in) | Generated workspaces could not use the onboarding procedure. | unknown | Ship the canonical skill and preserve forwarding aliases. |
| Evidence checks accepted files absent from the declared commit. | [Validator](../../.agents/skills/repository-onboarding/scripts/validate_evidence.py), [regressions](../../tests/test_repository_onboarding.py) | Ignored or hidden changes could appear as exact source evidence. | unknown | Require tracked regular files and matching committed bytes. |
| Static Git inspection could invoke fsmonitor or refresh its index. | [Scanner](../../.agents/skills/repository-onboarding/scripts/scan_repo.py), [regressions](../../tests/test_repository_onboarding.py) | Read-only assessment could execute configured code or modify metadata. | unknown | Disable fsmonitor and optional writes; isolate inherited Git overrides. |
| Inventory included independent ignored checkouts. | [Scanner](../../.agents/skills/repository-onboarding/scripts/scan_repo.py), independent workflow evaluation | Other repositories contaminated stack and candidate results. | unknown | Apply repository boundaries and test ignored nested checkout exclusion. |
| Source status and review guidance conflicted with project contracts. | [Evidence contract](../../.agents/skills/repository-onboarding/references/readiness-and-evidence.md), [assessment template](../../.agents/skills/repository-onboarding/assets/assessment.template.md) | Source observations could be mistaken for knowledge approval. | unknown | Use observed claims and separate knowledge governance from static assessment. |

The procedure follows applicable repository instructions and preserves existing authorization.
It uses separate repository, service, capability, contract, source, and tool identities.
Drafts include contract and source proposals only when inspected evidence supports them.
Detailed component mappings remain skill-local artifacts.
Governed profiles use shipped knowledge templates, provenance, and append-only audit procedures.

## Validation evidence

| Check | Actual result |
| --- | --- |
| Skill structure | The skill-creator validator passed. |
| Runtime suite | All 132 tests passed, including 15 onboarding regressions. |
| Workspace validation | Status was VALID; nine documents passed with zero findings. |
| Final inventory | 381 files; Python build detected; 17 test candidates; zero candidate truncations. |
| Direct wheel build | Passed with existing build dependencies and no build isolation. |
| Source distribution | Built successfully; its wheel retained matching skill bytes and one scanner. |
| Installed wheel | External initialization and validation passed with zero findings. |
| Distributed resources | Skill bytes matched; aliases resolved; core runtime source remained absent. |
| Independent workflow | Registry proposals validated with one repository and zero tool grants. |
| Evidence controls | Changed citations failed; 13 unchanged claims passed despite unrelated modifications. |
| Documentation | Local links and report prose limits passed; full ASD review remains pending. |

The default isolated wheel build failed because restricted network access prevented retrieval of setuptools.
The successful build used the existing build environment with `--no-build-isolation`.
The runtime suite needed loopback permission for its local mock HTTP registry.
The external wheel environment reused local dependency libraries without network access.
Its imported Workbench runtime came from the installed wheel.

The independent assessment retained 21 claims and eight expected failures from changed-file citations.
It retained the original contaminated inventory instead of overwriting that evidence.
The final scanner excluded independent checkouts and identified the Workbench's Python source correctly.
The independent run did not execute target builds, tests, applications, network operations, or installers.

See [the retained validation record](../evidence/repository-onboarding-adoption.json) for commands, results, and evidence hashes.

## Measurable acceptance criteria

```gherkin
Scenario: Reject evidence absent from the source revision
  Given a report cites an ignored file outside the declared commit
  When the evidence helper validates the report
  Then validation returns a failure
  And zero claims receive knowledge approval

Scenario: Preserve read-only inspection
  Given a repository has an executable fsmonitor hook and a changed file timestamp
  When static inventory and evidence checks run
  Then the hook executes zero times
  And the Git index bytes and modification time remain unchanged

Scenario: Keep inventory repository-scoped
  Given a repository contains an ignored independent Java checkout
  When static inventory scans the repository root
  Then the independent checkout contributes zero manifest or contract candidates
  And its JVM stack does not classify the root repository

Scenario: Ship the onboarding procedure
  Given the built wheel is installed outside the source checkout
  When the installed command initializes and validates a workspace
  Then validation reports zero findings
  And skill discovery includes repository-onboarding
  And its helpers and templates match source bytes
  And the core directory contains zero Python runtime files
```

## Evidence limits and follow-up

The workflow assessment covers the Workbench and local synthetic regression fixtures.
It establishes no business repository readiness, runtime integration, or business approval.
Exact byte checks reject checkout transformations, including automatic CRLF conversion.
Windows forwarding was simulated through denied link creation; Windows execution remains untested.
Full ASD writing review remains pending.

Owner: unknown for platform verification and writing review.
Next action: perform those reviews before claiming Windows validation or complete ASD compliance.
