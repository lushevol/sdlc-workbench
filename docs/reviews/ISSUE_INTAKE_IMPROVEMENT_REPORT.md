---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Procedure instructions do not enforce an agent's question selection or semantic reasoning.
  - Artifact lint does not establish source authority, implementation approval, or passing business execution.
---

# Issue intake improvement

The portal incident exposed an intake gap before diagnosis.
The existing defect form requested exact revisions but did not distinguish investigation readiness from implementation approval.
Its fields did not guide iterative questions about browser lifecycle and session conditions.

The [defect template](../../knowledge/templates/sdlc/defect-report.md) now supports immediate intake with explicit unknowns.
The [analysis skill](../../.agents/skills/analyze-requirement/SKILL.md) selects a template before discovery and diagnosis.
The [catalog guide](../../knowledge/templates/sdlc/README.md#selection-and-handoff) directs unexpected behavior to that template.

## Scope and qualitative risk

Owned changes include those three guides, the real intake, and this review report.
The work starts from `621096a7aa0d09f4239a02c09af0b59e866e7832`.
Concurrent browser and verification changes remain outside this stage.
The untracked `TODO` remains outside this stage.

Qualitative risk is low because the change affects authoring guidance and template content.
Affected consumers include analysis agents, artifact authors, sample lint tests, and generated workspace users.
Package copying must preserve the changed template, skill, and navigation guide.

The existing seven defect headings and authoring envelope remain compatible.
No runtime validator, schema, dependency, or workflow engine change is required.
Readiness values describe an agent procedure. They are not a new enforced runtime state machine.

The real intake is an authoring artifact under `docs/reviews/`.
It is not a governed knowledge record or publication event.
No raw evidence, manifest record, or audit event changes belong to this stage.

## Intake behavior

The procedure records known facts and existing answers before asking focused questions.
It searches existing indexes, linked requirements, prior answers, and cited source bytes before asking for recorded intent.
The intake records applicable criterion IDs, source hashes, conflicts, and search limits.
Pending publication review does not erase documented user intent.
Each question records its answer source, status, resolution owner, consequence, and next action.
Separate hypotheses retain supporting evidence, missing checks, and scope limits.
The procedure uses small question rounds and avoids repeated answered questions without conflicting evidence.

Readiness names the investigation scope and its limits.
It requires expected and observed behavior, environment, timing, actions, impact, and an evidence plan.
A proposed expectation can support local investigation when policy authority remains unknown.
An unknown PROD revision does not block authorized local source inspection.
Implementation approval, business review, and publication remain separate decisions.

Applicable reproduction fields cover tab visibility, browser sleep, device sleep, session policy, network, VPN, and SSO.
The fields also record revisions, controls, mocks, instrumentation, and untested differences.
Unrelated issue types need only applicable fields with explicit reasons for exclusions.

## Real incident assessment

The populated [portal intake](PORTAL_SESSION_DEFECT_INTAKE.md) validates the procedure against retained incident evidence.
It records the reported PROD symptom separately from the demonstrated local failure.
It preserves the answered environment, browser, action sequence, elapsed time, and missing extension opportunity.
The first policy question missed the existing renewal requirement and raw replies.
The corrected intake links that intent and records the latest three answers.
The reporter confirms an awake device, connected network, and active use of another Edge tab.
The reporter describes nearly all users and nearly every occurrence. Measured counts remain unavailable.

The local timeline shows freeze, late refresh, automatic logout selection, HTTP 401, and authentication clear.
Run 001's Sign In capture phase remains unresolved.
The refresh callback ran 1,018,349 milliseconds after its target.
Automatic logout selection occurred before the refresh response.
The logout HTTP request occurred afterward.
The proposed regression therefore counts premature logout decisions and state transitions.
A request-only assertion would miss the demonstrated ordering defect.

The [existing execution report](PORTAL_BACKGROUND_SESSION_REPRODUCTION.md) owns the retained execution description.
This stage performs no new portal reproduction and changes no business runtime.
The local evidence does not establish PROD causation or approved session policy.

## Source and interface inspection

| Inspected source | Finding and implication |
| --- | --- |
| `core/schemas/sdlc-artifact.schema.json` | Existing defect sections support additional intake content. No schema extension is needed. |
| `core/artifact_lint.py` | Existing lint checks all fenced Gherkin blocks, including defect regression scenarios. |
| `tests/test_artifact_lint.py` | Tests consume documented samples directly and check all 37 samples together. |
| `scaffold.json`, `setup.py`, `core/workspace.py` | Packaging copies canonical templates and skills. Initialization creates aliases and guides without runtime source. |
| `tests/test_workspace_layout.py` | Existing tests cover shipped skills, package boundaries, and alias fallback. |
| Raw execution manifest and snapshots | All 51 retained local execution files match their manifest hashes. |
| Exact source snapshots and repositories | Six inspected MFE/BFF files match their exact Git revision bytes. The retained root source also matches its manifest. |

The MFE source revision is `f025513f696476a9cc8162681410cbd21e029bcb`.
The root source revision is `83091d85beff5306ca0cd643955d8ea6ed0a2d93`.
The BFF source revision is `85d7cc03eb12710d6facf581987fd4ae24fc9844`.
These identify local inspected source. They do not identify PROD deployments.
The real intake resolves each retained source through its source table and existing raw manifest.

## Validation observations

The [knowledge review checks](../evidence/portal-session-harness-20261019/knowledge-first-intake.json) cover the latest intake correction.
Four source hashes match. All 492 tracked raw and audit files remain unchanged.
Artifact lint and workspace validation pass. Local links and selected prose checks pass.
These checks do not repeat the earlier runtime suite or establish approval.

Build validation used an isolated source copy of the baseline plus this stage's owned changes.
It excluded concurrent changes and used existing installed build dependencies.
The wheel installation used `--no-deps --no-index` outside this checkout.

| Check | Actual result | Evidence limit |
| --- | --- | --- |
| Artifact lint tests | 51 tests passed. All 37 documented samples are covered. | Tests check supported authoring structure, not agent question quality. |
| Workspace layout tests | 18 tests passed. | Tests cover existing package and initialization boundaries. |
| Installed-wheel focused tests | The same 51 artifact tests and 18 layout tests passed against the installed wheel. | The full runtime suite was not repeated for these documentation changes. |
| Real intake normal lint | PASSED; one artifact; zero errors; four warnings. | Owner, business review, unresolved content, and writing review remain pending. |
| Real intake strict lint | FAILED as expected; exit code 1; four warnings; zero errors. | Pending owner decisions prevent strict handoff readiness. |
| Source workspace validation | VALID; 13 governed documents; zero findings. | Authoring documents use separate artifact lint. |
| Wheel build | Passed with `--no-build-isolation`; SHA256 below. | No connected installation or new platform test was needed for unchanged dependencies. |
| Installed initialization | Generated workspace is VALID with zero governed documents and zero findings. | A clean workspace contains no approved business knowledge. |
| Shipped content | Template, skill, and catalog guide match source bytes. Alias, guides, and schemas are present. | Existing Windows alias fallback was exercised through tests, not a Windows host. |
| Package boundary | Generated workspace excludes Python runtime source, `pyproject.toml`, and runtime tests. | Runtime remains installed in the package. |
| Source evidence | Manifest hashes and inspected exact source bytes match. | Hashes do not establish policy authority, reviewer identity, or PROD parity. |
| Documentation | Local links, selected prose limits, and owned diff checks pass. | Full ASD writing review remains pending. |

Wheel SHA256: `ecdfde2ad0635db2602a729c84e8805590f14c6f382e62d99b2a7fabb27e14ea`.
The build used `ai_sdlc_workbench-0.1.0-py3-none-any.whl`.

Relevant command forms are shown below.
Wheel and installed checks ran in isolated temporary directories outside the shared checkout.

```sh
python -m unittest discover -s tests -p test_artifact_lint.py -v
python -m unittest discover -s tests -p test_workspace_layout.py -v
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
ai-sdlc lint docs/reviews/PORTAL_SESSION_DEFECT_INTAKE.md
ai-sdlc lint docs/reviews/PORTAL_SESSION_DEFECT_INTAKE.md --strict
ai-sdlc --workspace . validate
git diff --check -- .agents/skills/analyze-requirement knowledge/templates/sdlc/defect-report.md knowledge/templates/sdlc/README.md docs/reviews/PORTAL_SESSION_DEFECT_INTAKE.md docs/reviews/ISSUE_INTAKE_IMPROVEMENT_REPORT.md
```

## Measurable regression criteria

These criteria describe the authoring procedure.
Source inspection and the populated intake support their review.
No workflow runner or Gherkin step definitions execute these scenarios.

```gherkin
Feature: Start source-backed intake with scoped investigation readiness

  Scenario: Start a new reported defect
    Given the request reports unexpected behavior with four previously answered details
    When the analysis procedure starts
    Then exactly 1 existing defect template is selected before discovery
    And all 4 supplied answers have source locators before new questions are recorded
    And exactly 0 answered details are requested again without conflicting evidence

  Scenario: Start a requested behavior
    Given the request describes a new required behavior
    When the analysis procedure starts
    Then exactly 1 existing requirement template is selected before discovery
    And each material unknown has an answer status and resolution owner

  Scenario: Investigate safely without a deployed revision
    Given expected and observed behavior, environment, timing, actions, impact, and an evidence plan are recorded
    And the deployed PROD revision and approved session policy are unknown
    And local evidence collection is authorized
    When readiness is assessed for local source inspection
    Then exactly 1 READY_WITH_LIMITS decision names the local scope
    And exactly 0 implementation approvals are inferred from that decision
    And the unavailable PROD revision does not block that local inspection

  Scenario: Use existing intent before asking for policy
    Given the knowledge index links a candidate requirement and two original user replies
    And publication review remains pending
    When the author reviews intent before asking policy questions
    Then all 3 linked sources have recorded locators and hashes
    And exactly 0 requests ask the user to repeat that recorded intent

  Scenario: Keep new background regression intent pending
    Given the known requirement separates browser suspension from its renewal fixtures
    When the author records new background recovery criteria
    Then every criterion has explicit Given, When, and measurable Then steps
    And exactly 0 policy-dependent criteria are presented as approved behavior
    And every unresolved policy question has a source status, owner, and next action
```

## Remaining decisions and integration risks

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Recorded intent resolves Q-005; publication review remains pending | Known renewal behavior can guide local fixtures without establishing approval | unknown | Trace refresh credential availability and effective configuration |
| Q-006 reports widespread frequent logout without measured counts | Severity, priority, and ownership remain unassessed | unknown | Obtain measured impact and responsible owners when available |
| Q-007 confirms awake device and connected network | Device sleep and disconnection no longer explain the reported conditions | unknown | Inspect tab suspension; retain unknown VPN and SSO state |
| Both retained runs lack a valid foreground portal control | The local comparison remains incomplete | unknown | Review and execute paired local controls |
| Readiness resides in procedure text | Agents can still omit material questions despite valid artifact structure | unknown | Review each intake semantically before implementation handoff |
| Concurrent chats share the checkout | Combined validation can include unrelated stages | unknown | Integrate each scoped commit and validate the combined result |
| Business and ASD reviews remain pending | This stage establishes no approval or complete ASD compliance | unknown | Record actual reviewers and decisions when reviews occur |
