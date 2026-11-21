---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks cover local links, command availability, and diff formatting.
---

# Workbench testing mechanism

**No critical conclusions require user attention or action.**

## Request and scope

User input from this conversation, 21 November 2026.

> Now let's focus on the testing um engine of this workbench project. Um in my opinion, testing are too part one is UI testing, another one is HI testing. So testing should be the stronger harness of each release change. So when the requirement it's calm. We have a roughly test case on it. Test case is described by natural language. Then it should be translated into a jerking grammar. then it can be translated into test scraps. Test scraps is working on playwright and API testing I I'm not sure I have no idea what it's gonna be And once the design is concrete, then we have more test cases. We can adjust the previous test cases, then updated. And finally when the code is completed, then the um the re the the verification harness should be all the test cases set up before. discuss it with me on the testing mechanism I just said, sort out it, polish, and um we need to come out to a final solution.

Scope covers design discussion and a proposal for harness maintenance. Implementation awaits a subsequent request.
This proposal interprets “HI testing” as direct API testing, based on the later reference to API testing.

## Proposed design

Keep one case catalog per task and one resolved case list per release candidate.
Workbench should assemble the list, run configured suites or import their CI results, and reconcile each required case.
Executable tests remain with their current repository owners. [Canonical case rules](../../tasks/README.md#canonical-gherkin-test-cases).

| Stage | Work | Output |
| --- | --- | --- |
| Requirement intake | Write rough cases in plain language. Convert supported expectations to business Gherkin. Flag unanswered questions. | Stable case IDs in `06-test-cases.md`, linked to acceptance criteria. |
| Design refinement | Revise established cases. Add relevant positive, negative, boundary, failure, recovery, and regression cases. | Reviewed case versions, test data, expected outcomes, and required test levels and environments. |
| Test automation | Reuse or draft native scripts from the cases. Review each setup, action, and observable assertion against the design. | Exact runner selectors, assertion bindings, and any missing automation. |
| Code review | Compare base and candidate behavior. Add cases for newly discovered changes and confirm the impacted regression scope. | The required case list for the candidate, with exact definition revisions and bindings. |
| Release verification | Run the required cases on the candidate. Reconcile every planned result and retain evidence as each case finishes. | Case results, uncovered behavior, and the verification decision. |

During design, record the UI controls, API operations, setup data, and cleanup needed to make each case reproducible.
Prepare runnable assertions before product code where the interface permits. For a defect, use the same case on both builds.
An early failure must demonstrate the expected missing or incorrect behavior. Setup errors remain separate.
Use the same case ID for a refinement of the same behavior. Version material definition changes.
Use a new ID for a distinct behavior. Record who agreed to withdraw a required case and why.
Keep earlier run evidence tied to its original definition. Resolve the current list again if candidate scope changes.

Use Gherkin for observable behavior and generate starter script code where the bindings are known.
Review AI-drafted scripts in the test repository. Inspect every expected outcome and its executable assertion.
Leave unknown bindings visible until the team resolves them. [Gherkin quality guide](../../docs/GHERKIN_QUALITY.md).

### UI and API coverage

| Path | What the test proves | Runner choice |
| --- | --- | --- |
| UI | A user can complete the required journey and observe its actual result. | Playwright with existing page and component objects. Reuse existing Robot browser cases where they already cover the journey. |
| API | The service responds correctly to a direct request, including response fields, errors, and observable state changes. | Reuse Robot or service-native tests. Use Playwright Test's browser-free `request` fixture for new HTTP coverage without an existing runner. |

Use API cases for service rules and data variations. Use browser cases for outcomes that depend on rendering or user interaction.
Require both paths when the behavior crosses both contracts and each path has a distinct observable outcome.
Record the reason when a path does not apply.
Treat an API call used to prepare browser data as setup. Count a direct API case when it asserts API behavior.
[Playwright API testing](https://playwright.dev/docs/api-testing).

### Example

Illustrative requirement. A user can save a display preference and see it after reloading the application.

```gherkin
Scenario: TC-001 retains the saved display preference
  Given a user whose display preference is Standard
  When the user saves the Compact preference
  And the user reloads the application
  Then the display preference shown is Compact
```

Bind `TC-001` to a browser test that asserts the displayed value after reload.
Add `TC-002` to save through the API and read back the stored value.
Add `TC-003` when the design specifies invalid-value handling. Assert the documented error and the previously stored value.
[Gherkin reference](https://cucumber.io/docs/gherkin/reference/).

## Candidate verification

The release list contains every required case from the included changes and their impacted regressions.
Fast pull request runs can select subsets. The release check accounts for every required instance.
For each instance, capture the case revision, assertion bindings, runner selector, data variant, environment, and candidate build.
When a release spans services, bind the relevant deployed artifact identities.

Each required instance needs a retained passing result for its selected build, environment, and assertions.
Store the original runner result, normalized outcome, expected and actual values, attempts, and artifact references.
Mark cases without matching passes as outstanding. Preserve failed, skipped, blocked, missing, stale, and expected-failure outcomes.
Flag a later retry pass alongside the earlier failure. Review the failed attempt before accepting the case.
Save completed cases as they finish. Reuse existing run-level metadata and durable artifacts. [Case evidence rules](../../tasks/README.md#save-case-evidence-and-resume-checkpoints).

Keep unit tests as a separate required check. Run the full applicable candidate unit suite.
Use the three existing coverage views for acceptance criteria to tests, criteria to code, and code changes to tests.
Show the required case count, matching passes, and outstanding cases with impact, owner, and next action.
Resolve missing assertions and untraced business changes before claiming complete verification.
For a blocked required environment, keep verification incomplete. Record any release exception as a separate decision.
[Unit test principle](../../PRINCIPLE.md#10-delivery-requires-passing-unit-tests) · [Coverage procedure](../../docs/BEHAVIOR_REVIEW.md#coverage-output-for-requirements-and-defects).

## Current support and implementation scope

| Current capability | Consequence for the proposal |
| --- | --- |
| The Gherkin checker validates UI definitions and bindings. | Keep the current UI checks. Review direct API assertions against the case and designed contract. |
| Root Playwright has synthetic, local application, and deployed checks. The default command selects synthetic tests. | Select a suite that exercises the required boundary. Bind deployed claims to the served candidate. |
| The independent Robot engine covers UI and API. Its registered Workbench resource exposes offline smoke only. | Use approved direct or CI runs, or configure the relevant existing resource and grant. |
| Workbench provides runner planning, preflight, and a shared review index. The ledger imports browser inventory and Jest JSON. | Extend result ingestion for the first needed native formats. Reconcile the expected inventory independently of suite exit status. |

[Gherkin quality](../../docs/GHERKIN_QUALITY.md#use-the-workflow) · [Playwright suites](../../e2e/README.md#select-and-run-tests) · [Robot execution](../../docs/ROBOT_TESTING.md#run-ratan-business-cases-directly) · [Preflight](../../docs/TEST_PREFLIGHT.md) · [Review index](../../docs/REVIEW_INDEX.md#reconcile-retained-runner-records).

Start with one representative change with a browser journey and a direct API contract.
Use its current cases and existing runner outputs. Add required-case selection and reconciliation to the existing review workflow.
Demonstrate a complete pass, a failed assertion, and detection of omitted and stale results.
Use an isolated environment and a known candidate for the pilot.
Expand to another runner only when an actual release needs that result format.

The Workbench maintainer owns the integration proposal. The relevant test owner reviews case bindings.
The release owner reviews outstanding evidence and any exception.
The main design risk is treating runner success as complete coverage. Reconcile each required case explicitly to address it.
Reviewed Workbench source at `5a6012b9c` and the independent Robot checkout at `9f83897`.
Current guides were assessed. The proposal remains in this maintenance record pending review.
This was a static review. Implementation and live execution remain pending.

## Checks

Verified ten local links and anchors, the Gherkin code fence, and diff whitespace.
Confirmed five installed command entry points for Gherkin validation, test planning, preflight, coverage, and the case ledger.
