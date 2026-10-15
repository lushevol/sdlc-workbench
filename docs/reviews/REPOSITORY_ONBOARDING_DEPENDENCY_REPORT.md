---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
implementation_status: COMPLETE
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
- Static checks do not prove complete discovery, effective permissions, deployed connectivity, or business behavior.
- Windows execution remains untested.
---

# Repository onboarding dependency reporting

The skill now makes critical external relationships prominent in repository assessments.
Reports identify provided operations, permission controls, outbound call conditions, messaging, data access, and configuration bindings.
They also cover identity, trust, storage, network, platform, operations, frontend, business providers, and engineering delivery.
The user approved [the implementation plan](REPOSITORY_ONBOARDING_DEPENDENCY_PLAN.md) in this chat.

The current consumers are agents preparing assessments and engineers reviewing integration risks.
The observable benefit is explicit dependency evidence, conditions, consequences, and unresolved questions before general readiness conclusions.
The [investigation guide](../../.agents/skills/repository-onboarding/references/external-dependencies.md) defines all 16 coverage families.
The [assessment template](../../.agents/skills/repository-onboarding/assets/assessment.template.md) places critical relationships after purpose and before readiness.

## Scope and compatibility

The baseline source revision was `308fcb2c58f4facb5efcd8d667ef538c748aa169`.
The validated helper revision is `95abccdfa2ca671a667ed71215c52a7a4fbc00ae`.
The final guidance revision is `3ee09d9b05828293af37018a2523e60d5b0d741c`.
The review inspected helper callers, tests, packaging, initialization, and catalog boundaries before implementation.
Changed interfaces comprise skill guidance, assessment templates, the local report profile, static helpers, and their regressions.
Qualitative risk is moderate because compatibility and evidence handling affect agent conclusions.

New assessments select `dependency_profile: "external-dependencies/1"` while retaining `schema_version: "1.0"`.
Legacy reports remain valid without claiming the stronger profile checks.
The profile requires field-specific claim references, evidence statuses, unresolved reasons, review actions, and all-family coverage.
The helper validates structure and exact source citations; it cannot decide semantic truth or discovery completeness.
Detailed dependency records remain local staging artifacts.
Canonical catalogs and graph extraction keep their existing ownership boundaries.

## Findings and disposition

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| A generic dependency table omitted important relationship details. | [Updated template](../../.agents/skills/repository-onboarding/assets/assessment.template.md) | Permissions, triggers, and failure consequences could remain hidden. | unknown | Use the critical summary and dedicated dependency sections. |
| Discovery guidance covered too few engineering dependency kinds. | [Dependency guide](../../.agents/skills/repository-onboarding/references/external-dependencies.md) | gRPC, LDAP, infrastructure, and operational relationships could escape review. | unknown | Review every family and retain scope limits. |
| Reports lacked structured dependency checks. | [Evidence contract](../../.agents/skills/repository-onboarding/references/readiness-and-evidence.md), [validator](../../.agents/skills/repository-onboarding/scripts/validate_evidence.py) | Missing fields or unsupported certainty could pass citation checks. | unknown | Select the dependency profile and inspect supporting claims. |
| Profile conflict support accepted one citation repeated twice. | [Conflict regression](../../tests/test_onboarding_dependency_profile.py) | One source observation could appear as conflicting evidence. | unknown | Require two distinct citations for conflicting support. |
| Filename inventory missed profile, deployment, interface, and migration candidates. | [Scanner](../../.agents/skills/repository-onboarding/scripts/scan_repo.py), [regressions](../../tests/test_repository_onboarding.py) | Relevant configuration and declared boundaries needed extra manual discovery. | unknown | Use expanded candidates and disclose truncation. |
| One evaluated attribute labeled candidate UI linkage as observed. | Retained pre-review assessment and source path comparison | A reviewer could mistake equal paths for a confirmed relationship. | unknown | Keep the linkage inferred and apply the clarified evidence guidance. |

Missing authorization evidence remains unknown; it does not establish public access.
Observed protocols cannot establish observed permissions, activation, or production connectivity.
The helper rejects missing claims, unsupported certainty, incompatible coverage references, and undeclared profile extensions.
Inventory remains filename and safe metadata discovery.
It does not parse configuration values, execute target code, or extract dependency graphs.

## Validation evidence

| Check | Actual result |
| --- | --- |
| Skill structure | The skill-creator validator passed. |
| Runtime suite | All 151 tests passed, including 16 profile tests and 18 onboarding tests. |
| Workspace validation | Status was VALID; nine documents passed with zero findings. |
| Wheel build | Passed with installed build tools and no build isolation. |
| Installed wheel | External initialization and validation passed with zero findings. |
| Distributed resources | All nine onboarding resources matched source bytes; aliases, schemas, templates, and core guides remained available. |
| Generated workspace boundary | Runtime Python source, runtime tests, and package metadata remained absent. |
| Independent workflow | 48 claims and 27 relationships passed evidence and profile validation across all 16 families. |
| Documentation | Local links, prose limits, and diff checks passed; full ASD review remains pending. |

The first runtime suite failed because the sandbox denied a local mock HTTP server.
The successful run used the required loopback permission.
The default isolated build failed because restricted network access prevented setuptools retrieval.
The successful build used installed build tools with `--no-build-isolation`.

The external wheel check reused existing dependency libraries through a local path file.
Its Workbench runtime imported from the installed wheel outside this checkout.
An initial smoke script checked a nonexistent guide path; the corrected check used the shipped responsibility guide.
These checks establish distribution behavior within the tested macOS environment.
The last source change clarified guidance; executable helper code matches the passing runtime suite.

## Independent workflow assessment

The isolated assessment uses a committed Java and TypeScript fixture with configuration and deployment files.
The evaluating agent received the skill, raw source, and a realistic assessment request.
The initial evaluation received no intended findings or suspected defects.
Target builds, tests, applications, installers, and network operations remain unexecuted.

The scanner enumerated all 18 tracked files without warnings or truncation.
The report identified operation-specific permissions and conditional HTTP/gRPC calls.
It kept equal topic names on separate broker bindings.
It preserved unknown JMS providers, dormant Solace invocation, LDAP consumers, migration activation, and configuration resolution.

The first helper run rejected a duplicate claim reference.
The evaluator corrected that reference and retained the failed output.
Manual review then found one candidate linkage labeled as observed.
The evaluator preserved the earlier report and changed that attribute to inferred.
The guide now explains that a caveat cannot make an inferred value observed.
These corrections establish neither complete semantic accuracy nor business approval.

Nested UI manifests require manual inspection because automatic package metadata describes the repository root.
The evaluator found the nested UI manifest and inspected it directly.
This inventory limit did not block the assessment.
The guide requires manifest inspection rather than treating scanner stack signals as exhaustive.

See [the validation record](../evidence/repository-onboarding-dependencies.json) for commands, results, source identities, and retained artifact hashes.
Raw fixture bytes, earlier reports, helper outputs, and logs remain in the ignored evaluation directory identified there.

## Measurable acceptance criteria

```gherkin
Scenario: Preserve compatibility without implying stronger checks
  Given a valid legacy report without dependency extension keys
  When the evidence helper validates its exact source citations
  Then validation exits with status 0
  And the output states that dependency profile structure was not checked

Scenario: Reject unsupported permission certainty
  Given an observed authorization attribute references only an inferred claim
  When the evidence helper validates the dependency profile
  Then validation exits with status 1
  And the output identifies that authorization attribute

Scenario: Reject repeated conflict citations
  Given a conflicting attribute cites a claim with one repeated source range
  When the evidence helper validates the dependency profile
  Then validation exits with status 1
  And relabeling the repeated citation kind does not change that result

Scenario: Preserve dependency resources in distribution
  Given the built wheel is installed outside the source checkout
  When the installed command initializes and validates a workspace
  Then validation reports zero findings
  And all nine onboarding resources match source bytes
  And the generated core directory contains zero Python runtime files
```

## Remaining limits

The helper cannot check whether family details cover every semantic requirement or whether cited sources support each stated value.
Agents must read citations and review technology-specific details.
Synthetic fixtures establish no business repository readiness or production connectivity.
Windows execution and full ASD writing review remain pending.

Owner: unknown for platform verification and writing review.
Next action: complete those reviews before claiming Windows validation or full ASD compliance.
