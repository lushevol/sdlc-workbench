# Knowledge wiki refresh

**Historical stage report.** This refresh describes revision `4c97d0d5f35bcb4f4b51c5bc7dc5f1c176f07a60` and its earlier 19-page wiki. Use the [current wiki workflow](../../.agents/skills/llm-wiki/SKILL.md) and [engine-selection report](LLM_WIKI_ROUTING_AND_CLEANUP_20261111.md) for present operation. Retain the results below as evidence of that refresh.

The wiki now follows CES migration knowledge version 6.
Its prior summaries used version 1.
The refresh updates the CES source summary, entitlement concept, living overview, and catalog.
The other 15 wiki pages retain their exact bytes.

Date: 10 November 2026, Asia/Singapore.
Owner: Workbench maintainer.
The user selected a refresh from existing Workbench knowledge records.
The [llm-wiki skill](../../.agents/skills/llm-wiki/SKILL.md) controls this workflow.

## Input scope and changes

The selected scope contains all 12 canonical structured domain records under `knowledge/`.
All records remain `candidate` and `draft`.
The [historical wiki index](https://github.com/lushevol/sdlc-workbench/blob/4c97d0d5f35bcb4f4b51c5bc7dc5f1c176f07a60/knowledge/wiki/index.md) links all 19 navigation pages.

Full SHA-256 comparisons found one changed record: [KT-ces-migration-parity](../../knowledge/candidates/security/KT-ces-migration-parity.md), version 6.
The other 11 record hashes match the [prior generation binding](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/generation.json).
Before this refresh, all 19 wiki hashes matched that binding.

The changed navigation preserves these intended boundaries:

- Each tile keeps its selected admission provider and application scope.
- Shared `hasPermission(code)` checks accept mapped EMS2 or CES grants without additional caller arguments.
- Accepted checks require a log identifying a provider that supplied a matching grant.
- CES role-owned saved-view and filter writes remain unavailable until their ownership rule is agreed.
- Existing EMS2 role-owned writes retain their established rules.
- Application-scoped `roleList` and `applicationId` fields do not select a scalar CES role.
- The RATAN mapping separates its CES authorization name, legacy team label, and CES application identifier.

Each affected wiki claim links its exact canonical definition.
The source record retains the original clarification sources and unresolved questions.

## Checks and review

The [refresh binding](../evidence/llm-wiki-refresh-20261110/refresh.json) records source identities, full hashes, page hashes, and actual check results.
It also retains the independent semantic review and retrieval answers.
Structural checks precede semantic lint and retrieval review.
The checks cover catalog coverage, reachability, source identities, local targets, heading anchors, and physical line locators.
Protected-byte comparisons cover canonical records, raw snapshots, the source manifest, and immutable audit events.

| Check | Actual result |
| --- | --- |
| Canonical summaries | 12/12 current identities and versions. |
| Page catalog and reachability | 19/19 pages. |
| Local destinations | 339 valid links, including 183 heading anchors and 30 physical line locators. |
| Workspace validation | `VALID`, with zero findings. |
| Protected bytes | All 14 governed documents, 462 raw inventory entries, 67 audit files, and 500 manifest records remain identical. |
| Semantic support | 12/12 records and 19/19 pages reviewed; zero remaining material findings. |
| Independent retrieval | Four questions reviewed, including an unsupported policy question and a proposed requirement. |
| Automated writing checks | Passed for all 19 wiki pages and this report. Complete ASD review remains pending. |

## Limits and unresolved decisions

Record navigation covers 12 of 12 selected records.
This denominator does not measure complete source ingestion or complete business knowledge.
The review reads canonical records. It does not independently reread every original snapshot.
External destinations remain unchecked.
The refresh establishes no business execution, deployment, migration acceptance, publication, or human approval.

CES scalar-role contracts, query visibility, role-query rules, and multiple-role exclusion policy remain unresolved.
Complete upper-application API compatibility still requires reviewed application, feature, action, and caller mappings.
Legacy restriction definitions and CES-only management-grant scope also remain unresolved.
Owners are unknown. Resolve these questions through the [canonical question table](../../knowledge/candidates/security/KT-ces-migration-parity.md#open-questions).

## Output review

```json
{
  "asd_review": "PENDING",
  "automated_check": "PASSED",
  "findings": [],
  "limitations": [
    "Automated checks do not check the complete approved dictionary or grammar rules."
  ],
  "reviewed_at": null,
  "reviewer": null,
  "standard": "ASD-STE100"
}
```
