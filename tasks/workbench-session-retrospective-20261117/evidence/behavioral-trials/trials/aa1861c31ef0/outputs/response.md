# Owner-decision view

The living file has 12 questions. Three contain recorded answers. Nine have blank answers and form seven scoped groups.
Grouping preserves each question's authority, actor, environment, version, and decision. [Living questions](../tasks/questions.md)

## Recorded answers

These answers remain exact. Their scope stays attached to the original question.

| ID | Scope | Exact recorded answer |
| --- | --- | --- |
| KQ-01 | policy · operator · UAT · v1 · renewal-scope | Mouse, keyboard, and scroll. |
| KQ-10 | maintenance · agent · local · v1 · recovery | Continue the saved payment recovery draft; retain accepted work. |
| KQ-11 | policy · agent · local · v1 · retention | No. Review consumers and provenance first. |

Confidence is high for these transcriptions. Their authority and scope come from the living file. [Recorded answers](../tasks/questions.md)

## Remaining decisions

Each answer field accepts another answer, “unknown,” or a named contact. Record the answering authority and date.

### 1. UAT input eligibility

**KQ-02, KQ-05, KQ-07 · owner:portal · policy · operator · UAT · v1 · renewal-scope**

Decide touch eligibility, qualifying keyboard and scroll inputs, and synthetic-event eligibility.
The source names mouse, keyboard, and scroll while refresh credentials remain usable.
These details determine renewal eligibility. KQ-01 remains answered. [Activity source](../sources/portal/activity.md)

Proposed options include eligible, excluded, or conditional eligibility. Specify qualifying events and conditions for each answer.

- KQ-02 touch answer __________
- KQ-05 keyboard and scroll answer __________
- KQ-07 synthetic events answer __________
- Authority and date __________

### 2. PROD touch eligibility

**KQ-03 · owner:portal · policy · operator · PROD · v1 · renewal-scope**

Decide whether PROD touch activity qualifies, including any conditions.
The supplied source leaves touch eligibility unresolved and supplies no production-adoption evidence.
The answer defines PROD intent. [Activity source](../sources/portal/activity.md)

Proposed options include eligible, excluded, or conditional eligibility.

Answer __________  
Authority and date __________

### 3. Touch implementation at ui-42

**KQ-04 · owner unknown · engineering · operator · UAT · v1 · renewal-scope**

Identify whether ui-42 implements touch renewal.
The historical local fixture exercised mouse activity with a controlled clock and stub issuer.
Touch implementation and UAT execution remain unverified. This limits conformance assessment. [Observation](../sources/portal/observation.md)

Proposed responses include implemented or absent, with exact source evidence, or an engineering contact for investigation.

Answer and evidence __________  
Engineering owner, authority, and date __________

### 4. Version 2 renewal delay

**KQ-06 · owner unknown · engineering · operator · UAT · v2 · renewal-timing**

Provide the v2 delay and its implementation evidence.
The inspected ui-42 delay is 5,000 ms. The supplied evidence gives no v2 value.
A missing value prevents a supported v2 timing conclusion. [Observation](../sources/portal/observation.md)

Proposed responses include an evidenced duration or a named engineering contact.

Answer and evidence __________  
Engineering owner, authority, and date __________

### 5. Candidate publication

**KQ-08 · owner:portal · publication · reviewer · UAT · v1 · publish**

Decide whether the identified candidate bytes may be published.
The fixture records candidate status and no human approval.
This decision controls publication authorization. [Selection](../selection.json), [Portal candidate](../knowledge/records/portal.md)

Proposed options include approve reviewed bytes, retain candidate status, or request specified changes.
Identify the bytes, review evidence, and any conditions in the answer.

Answer __________  
Approving authority and date __________

### 6. Effective UAT issuer configuration

**KQ-09 · owner unknown · engineering · service · UAT · v1 · issuer**

Provide the effective issuer configuration and relevant clock evidence.
Local evidence records a 15-minute YAML default and a 480-minute JVM override.
One UAT token lived 900 seconds. Effective UAT configuration and clock offset remain unknown.
These gaps limit environment conclusions. [Runtime evidence](../sources/operations/runtime.md)

Proposed responses include runtime-bound configuration evidence or a named issuer owner.

Answer and evidence __________  
Engineering owner, authority, and date __________

### 7. Late-arrival retention

**KQ-12 · owner:settlement · policy · operator · UAT · v1 · late-arrival**

Specify the retention duration.
The recovery source supplies no default. This prevents a complete late-arrival retention rule.
Retry uses the original reference. Repeating an accepted reference must prevent a second payment.
Those source-backed clauses need no new owner answer. [Recovery source](../sources/settlement/recovery.md)

Proposed options include a defined duration or a conditional duration with explicit conditions.

Answer __________  
Authority and date __________

## Handoff context and limits

Resume context points to the saved recovery draft and accepted work.
The checkpoint also retains an access-denial review item.
The grant source already specifies denial without a matching action grant. [Checkpoint](../tasks/checkpoint.json), [Recovery draft](../tasks/recovery-draft.md), [Grant source](../sources/access/grants.md)

All evidence is synthetic. Source statements support this decision view with high confidence.
Current business applicability, production adoption, and deployment completion remain unverified.
The original questions and answers remain preserved.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
