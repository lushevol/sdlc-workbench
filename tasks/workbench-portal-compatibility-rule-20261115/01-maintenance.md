# Portal backward compatibility review rule

> **No critical conclusions require user attention or action.**

## Request and scope

The user requested a mandatory Workbench review rule for changes affecting FMO Post Trade Portal (Markets Operations One).
The scope includes, in particular, `single-ui-bff` and `mfe-base`.

### Exact user input

Source and date are the user's Workbench chat message of 15 November 2026.

```text
I need to add a new rule: any changes involving FMO Post Trade Portal (Markets Operations One), especially single-ui-bff and mfe-base, must strictly prioritize backward compatibility. Ideally, downstream systems should see no change in behavior, allowing them to upgrade smoothly without needing any modifications or even noticing the change. This is a mandatory requirement for portal changes.\
\
If a smooth transition is genuinely impossible, we must minimize any API changes and clearly highlight the differences before and after, along with the resulting behavioral changes.\
\
The reason for this strict requirement is that a large number of systems currently depend on portal in production, and we want to avoid any breaking changes. Therefore, we need to be extremely cautious. Every time a change is made, our review process must cover two key areas:\
\
1\. Functional review:\
&#x20; ◦ Does it introduce any API breaking changes?\
&#x20; ◦ Does it introduce any data structure breaking changes?\
&#x20; ◦ Can downstream systems detect any change in behavior?\
2\. Performance review:\
&#x20; ◦ Does it cause any existing APIs to run slower?
```

## Affected scope and risk

- Workbench starts from baseline `845aa0e6e51deb96106f6f3b5158c63be1c6471f`.
- Contributors and reviewers use this rule when a change affects the portal, including changes outside the two named repositories.
- High compatibility risk applies to portal changes because many production systems depend on the portal.

## Current guidance

The [project guide](../../AGENTS.md#portal-backward-compatibility) makes the rule mandatory for all portal changes.
The [behavior review procedure](../../docs/BEHAVIOR_REVIEW.md#review-backward-compatibility) defines both reviews and the evidence for unavoidable changes.
The rule applies within Workbench review. The portal checkouts and application runtime are outside this documentation change.

## Verification

- All four added Markdown links resolve to their target headings in the source checkout.
- `.venv/bin/ai-sdlc --workspace "$PWD" validate` reports a valid workspace with zero findings.
- `.venv/bin/python -m unittest discover -s tests -p test_workspace_layout.py` passes all 23 tests, including initialization and package checks.
- Generated workspaces receive the procedure. The task source remains in the original checkout.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - This change defines a review procedure. Portal behavior and API performance require evidence from each candidate change.
```
