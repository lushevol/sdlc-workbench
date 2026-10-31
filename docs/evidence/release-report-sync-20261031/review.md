# Release report synchronization update

Source: [exact user request](user-input.md#exact-user-input), 31 October 2026.

The [release-confidence skill](../../../.agents/skills/release-confidence/SKILL.md) now requires synchronized maintained Markdown and HTML views.
The [reporting reference](../../../.agents/skills/release-confidence/references/reporting.md#keep-markdown-and-html-synchronized) defines shared metrics, scope, conclusions, evidence gaps, and actions.
The [runtime reference](../../../.agents/skills/release-confidence/references/runtime-log-evidence.md#collect-and-bind) requires operation correlation before a log event qualifies a path.
These rules remain independent of business domain, logging platform, test engine, and agent client.

The [release Markdown](../../../tasks/portal-background-session-20261019/10-release-confidence.md#runtime-log-evidence) now includes the HTML runtime observations, outcomes, limits, and actions.
The historical release hold, unit results, and 467-case totals retain their prior evidence scope.
The HTML pages retain their checked layout and bytes. This stage adds no application execution or UAT evidence.

The [validation record](validation.json) retains skill checks and links.
The [task synchronization checks](../../../tasks/portal-background-session-20261019/evidence/runtime-report-sync-20261031/validation.json) retain report claims and source hashes.
Prior validation records and manifests remain unchanged.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
