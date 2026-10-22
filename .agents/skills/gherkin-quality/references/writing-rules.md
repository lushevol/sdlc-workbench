# Gherkin UI writing rules

These rules apply to UI E2E specifications selected for this workflow.
Business scenarios retain implementation-independent behavior language.
The [manifest guide](../../../../docs/GHERKIN_QUALITY.md) defines machine fields and validation limits.

## Mandatory rules

| Rule | Required content | Review action |
| --- | --- | --- |
| GQ-01: Separate intent | Link the business behavior and criterion. Describe the outcome without relying on a control label. | Compare the linked intent with every UI assertion. |
| GQ-02: Name the actor | Identify the actor and relevant role, permission, entity, and state. | Resolve ambiguous pronouns and undefined terms. |
| GQ-03: Type the target | Use the actual component semantics for each UI reference. | Inspect accessibility, source, or an established page object. |
| GQ-04: Identify the target | Use an exact verified name, visible label, test ID, or stable identifier. | Read the cited identity and check its applicability. |
| GQ-05: Scope the target | Identify the page, dialog, panel, section, menu, row, or other distinguishing region. | Check uniqueness within the stated region. |
| GQ-06: Describe the action | State one concrete action, its target, and any required input. | Separate ordered actions and preserve meaningful keyboard or pointer differences. |
| GQ-07: Assert an observation | State the observed entity, observation point, comparison, and expected value or state. | Replace vague success statements with supported predicates. |
| GQ-08: Support expectations | Cite requirement or established behavior evidence for every expected result. | Keep draft and unknown expectations unverified. |
| GQ-09: Retain provenance | Give evidence exact paths, hashes, line ranges, and applicable revisions. | Inspect contents. A matching hash alone does not prove the claim. |
| GQ-10: Map automation | Identify exact framework bindings and inspect their assertions. | Check every mapped step and disclose unsupported boundaries. |
| GQ-11: Report gaps | Identify the affected scenario, step, missing information, consequence, owner, and next action. | Leave readiness unresolved until material gaps are resolved. |

The GQ identifiers name review rules. Checker finding codes remain the implementation's separate machine identifiers.
Do not infer semantic validation from matching these identifiers.
Start with Given conditions and end with Then assertions.
Use another When after an intermediate Then when the journey requires another ordered action.

## Component vocabulary

Use the actual application semantics. Similar appearance does not establish the same component type.
Extend this vocabulary when inspected application evidence requires another type.

| Component family | Supported terms | Distinguishing details |
| --- | --- | --- |
| Actions and navigation | button, icon button, link, menu, menu item, tab, tablist | Accessible name, containing region, and expanded or selected state when relevant. |
| Text entry | textbox, text input, textarea, search field, spinbutton | Label, input value, format, and applicable validation state. |
| Selection | combobox, dropdown, option, checkbox, radio button, switch | Parent control, option identity, checked state, and applicable selection count. |
| Dates | date picker | Field label, calendar scope, date format, timezone, and permitted range when established. |
| Containers and help | dialog, modal, tooltip, section, tabpanel, backdrop, drawer panel | Name, parent region, triggering control, and applicable visibility state. |
| Tables | table, data grid, row, column, cell | Table identity, stable row key, column heading, and expected cell value. |
| Content and feedback | label, text, heading, status indicator, notification, alert, toast, image, chip | Exact content, containing region, and applicable severity or state. |
| Hierarchies and lists | tree, tree item, list, list item | Parent container, stable item identity, and applicable expansion or selection state. |

Do not call a menu item a combobox option.
Do not call a decorative icon a button unless it has button semantics or verified interactive behavior.
A section with a click handler remains a section unless inspected semantics establish another type.
Use spinbutton for a numeric input when its inspected semantics support that role.
Identify an image by its exact alternative text or another verified stable identity.
Filling a field, replacing its value, and moving the mouse each count as one concrete interaction.
Moving a controlled clock is a fixture event when its evidence supports that classification.
An icon button still requires a verified accessible name or stable identifier.
Avoid generated CSS classes and positional selectors when a stable identity exists.
Explain unavoidable fragile selectors as maintenance warnings.

## Distinguish the three concepts

| Concept | Example | Evidence needed |
| --- | --- | --- |
| Business intent | User A requests continuation of an authenticated session. | Requirement, criterion, or clearly marked draft intent. |
| UI interaction | User A clicks the button labeled "Extend" inside the dialog named "Your session has been expired". | Actual component identity, type, location, and disambiguation. |
| UI observation | The dialog named "Your session has been expired" is no longer visible. | Supported expected UI state and an inspected visibility assertion. |
| Functional result | A subsequent authentication-validation request uses the installed token and returns `result: true`. | Supported predicate, request binding, response assertion, and execution for a passing claim. |

The [session fixture](../../../../docs/examples/gherkin-session/session.md) records source evidence and remaining limits.
The UI label does not establish the business rule.
The functional predicate establishes only its stated authentication-validation scope.
Do not infer downstream authorization or an extended lifetime from that predicate alone.

## Representative wording defects

These fragments illustrate writing rules. They do not define new business cases.

| Ambiguous fragment | Defect | Correction procedure |
| --- | --- | --- |
| `When User A clicks Extend` | Component type and scope are missing. | Inspect the control and state its verified type, exact identity, and region. |
| `When User A selects USD` | Parent control and option semantics are missing. | Identify the actual parent control and the verified option label. |
| `When User A enters the trade ID` | Field identity, location, and input value are missing. | Cite the field, give its containing form, and use concrete test data. |
| `When User A clicks Submit and closes the panel` | Two ordered actions share one step. | Write separate action steps with explicit targets. |
| `Then the operation succeeds` | No observable predicate is defined. | Cite the required outcome and assert its exact state or value. |
| `Then the session is extended because the dialog closed` | A UI observation is used as unsupported functional proof. | Keep separate UI and functional assertions with independent support. |

Never fill missing details from these examples without inspecting the application.
If the label or scope is unavailable, record the gap and keep the affected scenario unverified.

## Review coverage and boundaries

Evaluate the applicable dimensions against actual requirements and established application behavior.

| Dimension | Relevant variations |
| --- | --- |
| User and access | Authenticated, anonymous, expired, unauthorized, and changed permissions. |
| Data | Empty, one item, many items, duplicates, special characters, and supported boundary values. |
| Interaction | Pointer, keyboard, repeated activation, canceled actions, and disabled controls. |
| State and recovery | Loading, empty result, error, retry, partial completion, and navigation during an operation. |
| Concurrency | Parallel requests, competing updates, multiple tabs, and stale displayed state. |
| Environment | Supported viewport, locale, timezone, network interruption, and browser lifecycle conditions. |

These dimensions guide investigation. They do not create unsupported policies or promise exhaustive coverage.
Identify the relevant limits, test data, isolation, cleanup, and evidence for each selected case.
Explain exclusions that materially limit the named verification scope.

## Findings and readiness

Report each finding with a scenario ID, exact step location, rule, explanation, correction, and supporting or missing evidence.
Add the consequence, owner, and next action in human-facing reports.
Use `unknown` for an unavailable owner.

| State | Meaning |
| --- | --- |
| `FAIL` | A mandatory rule is violated. |
| `UNVERIFIED` | Required information, evidence support, review, or automation mapping is unresolved. |
| `WARNING` | Mandatory checks pass, but a maintainability or precision issue remains. |
| `PASS` | Required checks pass within the stated evidence and review limits. |

Recorded reviews are claims. The checker does not authenticate reviewers or grant business approval.
Automation readiness does not establish passing execution.
Preserve the checker findings when adding semantic findings. Do not replace either with a numerical score.

## Saved report metadata

Use the actual automated result in saved reports:

```yaml
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
