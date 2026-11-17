# Owner decisions

Twelve source question rows form nine decision groups. Seven groups need follow-up. Three rows contain recorded answers.

Grouping is a coordination aid. Each source question keeps its answer scope and reconciliation entry.
All machine `Status` values remain `UNKNOWN`, because the source has no such field.

## Decision view

| Decision group | Source question IDs | Shared scope | Different scope or conflict | Consequence and owner |
| --- | --- | --- | --- | --- |
| DG-1 | KQ-01, KQ-02, KQ-05, KQ-07 | Policy; operator; UAT; v1; renewal eligibility. | KQ-01 answers activity categories. Touch, input details, and synthetic-event eligibility remain open. | `owner:portal` defines eligible activity for [Portal candidate](../knowledge/records/portal.md). [Draft requirement](../sources/portal/activity.md). |
| DG-2 | KQ-03 | Policy; operator; PROD; v1; renewal eligibility. | PROD scope requires its own answer. Touch eligibility remains unspecified. | `owner:portal` defines PROD touch eligibility for [Portal candidate](../knowledge/records/portal.md). [Draft requirement](../sources/portal/activity.md). |
| DG-3 | KQ-04 | Engineering; operator; UAT; v1; ui-42 touch implementation. | Engineering authority and environment differ from the retained local mouse observation. | Owner `unknown`. Obtain exact touch-path evidence before asserting UAT implementation for [Portal candidate](../knowledge/records/portal.md). [Local observation](../sources/portal/observation.md). |
| DG-4 | KQ-06 | Engineering; operator; UAT; v2; renewal delay. | Version v2 differs from the ui-42 evidence. | Owner `unknown`. Obtain version-bound timing evidence for [Portal candidate](../knowledge/records/portal.md). [Historical evidence](../sources/portal/observation.md). |
| DG-5 | KQ-08 | Publication; reviewer; UAT; v1; candidate publication. | Publication authority requires an explicit decision on exact candidate bytes. | `owner:portal` decides the permitted transition for [Portal candidate](../knowledge/records/portal.md). [Recorded candidate status](../selection.json). |
| DG-6 | KQ-09 | Engineering; service; UAT; v1; effective issuer configuration. | The token sample leaves configuration and clock offset unknown. | Owner `unknown`. Identify the issuer owner and obtain effective configuration for [Operations candidate](../knowledge/records/operations.md). [Environment evidence](../sources/operations/runtime.md). |
| DG-7 | KQ-10 | Maintenance; agent; local; v1; recovery restart. | Recorded answer applies to the saved recovery draft. | `maintainer`. Resume location is [checkpoint](../tasks/checkpoint.json) and [recovery draft](../tasks/recovery-draft.md). Affected record is [Settlement candidate](../knowledge/records/settlement.md). |
| DG-8 | KQ-11 | Policy; agent; local; v1; evidence retention. | Recorded answer requires consumer and provenance review. The inventory remains incomplete. | `maintainer`. Apply the recorded constraint to [Operations candidate](../knowledge/records/operations.md). [Retention instruction](../sources/operations/retention.md). |
| DG-9 | KQ-12 | Policy; operator; UAT; v1; late-arrival retention. | Recovery source leaves the duration unresolved and supplies no default. | `owner:settlement` defines retention for [Settlement candidate](../knowledge/records/settlement.md). [Recovery source](../sources/settlement/recovery.md). |

## Editable follow-up

Options below remain proposals. Every field also accepts another answer, `unknown`, or a named contact.

- **DG-1 — owner:portal.** Specify one complete UAT v1 eligibility rule. Touch options include eligible, excluded, or conditional. Specify qualifying keyboard/scroll inputs and synthetic-event treatment. Preserve KQ-01's recorded answer.
  **Answer** `Touch: ___; keyboard: ___; scroll: ___; synthetic events: ___; conditions: ___`
- **DG-2 — owner:portal.** Specify PROD v1 touch eligibility. Options include eligible, excluded, or conditional. Record applicable conditions and authority.
  **Answer** `___`
- **DG-3 — owner unknown.** Identify the responsible engineer. Supply ui-42 touch handling and UAT applicability evidence, or record unavailable evidence.
  **Answer / contact / evidence** `___`
- **DG-4 — owner unknown.** Identify the responsible engineer. Supply the UAT v2 revision, configured delay, units, and supporting source.
  **Answer / contact / evidence** `___`
- **DG-5 — owner:portal.** Options include authorize publication of identified bytes, hold, or request specified revisions. Record reviewer authority and scope.
  **Decision / candidate hash / reviewer / date** `___`
- **DG-6 — owner unknown.** Identify the issuer owner. Supply effective UAT configuration, build, capture time, and clock-offset evidence.
  **Answer / contact / evidence** `___`
- **DG-9 — owner:settlement.** Specify duration, unit, retention start event, applicable conditions, and authority. An explicit conditional rule is another option.
  **Answer** `___`

## Investigation limits

Confidence is high in the recorded text and its stated limits. Remaining policy choices require owner answers.

The draft supports mouse, keyboard, and scroll eligibility while refresh credentials remain usable. It specifies no fixed session duration.
It supplies no production-adoption evidence. [Activity requirement](../sources/portal/activity.md).

The ui-42 evidence covers historical local mouse activity, a controlled clock, and a stub issuer.
Its 5,000 ms implementation delay leaves UAT touch behavior and v2 timing unverified. [Observation](../sources/portal/observation.md).

One UAT token lived 900 seconds. Effective issuer configuration and UAT clock offset remain unknown. [Runtime evidence](../sources/operations/runtime.md).

Settlement recovery remains absent from its candidate record. The saved progress summary conflicts with that record and checkpoint.
Recovery requires further source review. [Settlement candidate](../knowledge/records/settlement.md), [checkpoint](../tasks/checkpoint.json), [progress](../tasks/progress.md).

These inputs are synthetic. This handoff establishes no business execution, publication, or deployment result.

## Original living questions

The following source text preserves every question, owner, source path, and exact recorded answer.
Source paths in this verbatim copy resolve from the fixture root. [Living question file](../tasks/questions.md).

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

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cover source hashes, question IDs, preserved answers, and local links.
  - Automated checks do not establish complete writing review.
```
