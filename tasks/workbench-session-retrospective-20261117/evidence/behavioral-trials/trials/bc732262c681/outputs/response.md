# Owner-decision view

Twelve source rows form nine decision groups. Three rows have recorded answers. Nine rows remain unanswered across seven groups.

The groups coordinate review. Each question keeps its own answer scope. Reconciliation remains question-specific.
Every machine `Status` remains `UNKNOWN`, because the source has no Status field.
All evidence is synthetic. Confidence is high in the transcribed evidence and scope distinctions.
Remaining policy, implementation, and approval answers require their respective owners. [Living questions](../tasks/questions.md)

## Compact decision view

| Decision group | Source question IDs | Shared scope | Different scope or conflict | Consequence and owner |
| --- | --- | --- | --- | --- |
| DG-1 | KQ-01, KQ-02, KQ-05, KQ-07 | policy · operator · UAT · v1 · renewal-scope | Different event facets. KQ-01 alone has an answer. Touch, detailed keyboard/scroll eligibility, and synthetic events remain unanswered. | Define one complete UAT event policy for the [Portal candidate](../knowledge/records/portal.md). Owner `owner:portal`. [Source](../sources/portal/activity.md) |
| DG-2 | KQ-03 | policy · operator · PROD · v1 · renewal-scope | PROD scope requires its own answer. The source provides no adoption evidence. | Define PROD touch eligibility for the [Portal candidate](../knowledge/records/portal.md). Owner `owner:portal`. [Source](../sources/portal/activity.md) |
| DG-3 | KQ-04 | engineering · operator · UAT · v1 · renewal-scope | Local ui-42 mouse observations leave UAT touch implementation unverified. | Verify implementation and update [Portal gaps](../tasks/gaps.md). Affected record [Portal](../knowledge/records/portal.md). Owner `unknown`. [Source](../sources/portal/observation.md) |
| DG-4 | KQ-06 | engineering · operator · UAT · v2 · renewal-timing | v2 evidence is absent. The observed 5,000 ms delay describes ui-42. | Establish v2 timing for [Portal gaps](../tasks/gaps.md). Affected record [Portal](../knowledge/records/portal.md). Owner `unknown`. [Source](../sources/portal/observation.md) |
| DG-5 | KQ-08 | publication · reviewer · UAT · v1 · publish | Publication authority differs from event-policy authority. Human approval is absent. | Record the decision for exact [Portal candidate](../knowledge/records/portal.md) bytes. Owner `owner:portal`. [Publication declaration](../selection.json) |
| DG-6 | KQ-09 | engineering · service · UAT · v1 · issuer | Local defaults, overrides, and one UAT token sample have different evidence scopes. | Establish effective issuer configuration and clock offset in [environment gaps](../tasks/gaps.md). Affected record [Operations](../knowledge/records/operations.md). Owner `unknown`. [Source](../sources/operations/runtime.md) |
| DG-7 | KQ-10 | maintenance · agent · local · v1 · recovery | Recorded answer applies to resumption only. | Resume point is the [saved recovery draft](../tasks/recovery-draft.md). Preserve accepted work for the [Settlement candidate](../knowledge/records/settlement.md). Owner `maintainer`. [Checkpoint](../tasks/checkpoint.json) |
| DG-8 | KQ-11 | policy · agent · local · v1 · retention | Recorded answer requires consumer and provenance review. Inventory remains incomplete. | Retain meaningful failed traces and canonical payload references under the [Operations candidate](../knowledge/records/operations.md). Owner `maintainer`. [Source](../sources/operations/retention.md) |
| DG-9 | KQ-12 | policy · operator · UAT · v1 · late-arrival | Retention duration has no source default. | Define late-arrival retention for the [Settlement candidate](../knowledge/records/settlement.md). Owner `owner:settlement`. [Source](../sources/settlement/recovery.md) |

## Remaining answers

Options are proposals. Each answer field also accepts another answer, `unknown`, or a named contact.

| Group | Decision or evidence needed | Proposed response choices | Editable answer |
| --- | --- | --- | --- |
| DG-1 | Resolve KQ-02, KQ-05, and KQ-07 individually within one event policy. Keep KQ-01's recorded answer scoped to KQ-01. | Touch eligible/ineligible/conditional. Keyboard and scroll accept all inputs or a specified event/filter list. Synthetic inputs eligible/ineligible/conditional. Supply conditions and exclusions for each facet. | |
| DG-2 | Does PROD v1 policy allow touch renewal? Give effective scope and conditions. | Eligible / ineligible / conditional, with an authoritative policy reference. | |
| DG-3 | Does the UAT v1 ui-42 build implement touch renewal? Identify the engineering contact first. | Supported / unsupported / unknown. Supply exact code and build bindings. Any runtime claim needs retained touch assertions and results. | |
| DG-4 | What delay does UAT v2 use? Identify the engineering contact and exact v2 revision. | Provide the delay and units with code/configuration evidence, or identify the missing evidence and contact. | |
| DG-5 | May these candidate bytes be published? Identify reviewer authority and the exact reviewed revision or hash. | Approve exact reviewed bytes / request changes / defer with reviewer contact. | |
| DG-6 | What issuer configuration actually applies in UAT? Identify its service owner. | Provide effective configuration, override precedence, build/environment/time bindings, and clock offset evidence, or name the evidence owner. | |
| DG-9 | What late-arrival retention rule applies to UAT v1 operators? | Specify duration and units, retention start event, and conditions/exceptions, or provide an explicit alternative policy. | |

The activity source supports mouse, keyboard, and scroll renewal eligibility while refresh credentials remain usable.
It leaves the requested event details unresolved. Browser suspension recovery also remains unresolved outside these living rows. [Activity source](../sources/portal/activity.md)

Historical ui-42 execution used a controlled clock and stub issuer. It exercised mouse events locally.
UAT implementation, v2 timing, and production adoption require additional evidence. [Observation](../sources/portal/observation.md)

Local YAML specifies 15 minutes. The effective local JVM override is 480 minutes.
One UAT token lasted 900 seconds. Effective UAT issuer configuration and clock offset remain unknown. [Runtime evidence](../sources/operations/runtime.md)

The recovery source specifies original-reference retry and accepted-reference duplicate prevention.
Late-arrival retention remains an owner decision. The saved checkpoint still identifies recovery as unfinished. [Recovery source](../sources/settlement/recovery.md) [Checkpoint](../tasks/checkpoint.json)

## Original rows and recorded answers

The following source content is reproduced verbatim. Empty answer cells remain empty. [Original living document](../tasks/questions.md)

<details>
<summary>Show all 12 original rows</summary>

# Living questions

No machine Status column exists. Answers apply only to their exact question and scope.

| ID | Authority | Actor | Environment | Version | Decision | Question | Answer | Owner | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KQ-01 | policy | operator | UAT | v1 | renewal-scope | Which input events qualify? | Mouse, keyboard, and scroll. | owner:portal | sources/portal/activity.md |
| KQ-02 | policy | operator | UAT | v1 | renewal-scope | Do touch events qualify? |  | owner:portal | sources/portal/activity.md |
| KQ-03 | policy | operator | PROD | v1 | renewal-scope | Do touch events qualify in PROD? |  | owner:portal | sources/portal/activity.md |
| KQ-04 | engineering | operator | UAT | v1 | renewal-scope | Does ui-42 implement touch renewal? |  | unknown | sources/portal/observation.md |
| KQ-05 | policy | operator | UAT | v1 | renewal-scope | Which keyboard and scroll inputs qualify? |  | owner:portal | sources/portal/activity.md |
| KQ-06 | engineering | operator | UAT | v2 | renewal-timing | What delay does v2 use? |  | unknown | sources/portal/observation.md |
| KQ-07 | policy | operator | UAT | v1 | renewal-scope | Are synthetic input events eligible? |  | owner:portal | sources/portal/activity.md |
| KQ-08 | publication | reviewer | UAT | v1 | publish | May candidate bytes be published? |  | owner:portal | knowledge/records/portal.md |
| KQ-09 | engineering | service | UAT | v1 | issuer | What is effective issuer configuration? |  | unknown | sources/operations/runtime.md |
| KQ-10 | maintenance | agent | local | v1 | recovery | Where should resumed work start? | Continue the saved payment recovery draft; retain accepted work. | maintainer | tasks/checkpoint.json |
| KQ-11 | policy | agent | local | v1 | retention | May equal hashes be deleted without consumer review? | No. Review consumers and provenance first. | maintainer | sources/operations/retention.md |
| KQ-12 | policy | operator | UAT | v1 | late-arrival | How long must late arrivals be retained? |  | owner:settlement | sources/settlement/recovery.md |

</details>

## Checks and limits

Input hashes matched all 24 declared fixture files and the selected skill.
The original question files and recorded answers retain their input hashes.
This deliverable contains a proposed coordination view. The authorized output scope covers this view and its action log.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cover input preservation, source links, and question coverage.
  - Automated checks do not establish complete writing review.
  - Synthetic evidence does not establish business behavior.
```
