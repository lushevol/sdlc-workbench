# Agent guidance review and simplification

**The root guide is 55.2% smaller. Mandatory rules, all heading anchors, and original user authority remain preserved.**

- Work type: Workbench maintenance.
- Date: 13 November 2026 (Asia/Singapore).
- Source: user message in this Codex chat, high-priority reference.
- Baseline: `55bc74d19113ee7b051ffc5f721eb2d34251121f`.
- Scope: `AGENTS.md`, current agent entry adapters, their referenced procedures, and affected distribution/navigation contracts.
- Excluded: unrelated `core/connectors/yarn.lock`, untracked `core/release-report/`, and the separate ADO skills assessment.

## Exact user input

> Review the agents we just recorded, and check for content that are expired, duplicate, or no longer usable. Make it more efficiency.

### Follow-up assurance request

- Source: user message in the same Codex chat, 13 November 2026 (Asia/Singapore).
- Priority: high; review commit `e2a8054ea95165030d714b11c4c855dacc9e96f9` for regressions and material rule loss.

> double confirm your change won't introduce side effect and make things become worse.

The follow-up checks compare exact committed endpoints and current protected consumers.
They cannot guarantee future model adherence or replace missing live-client evidence.

## Intended outcome and authority

Treat “agents” as the repository's `AGENTS.md` and its connected current agent guidance.
Remove unsupported current instructions and repeated explanations only after checking their owners, consumers, and retained authority.
Keep one concise entry guide with explicit routes to maintained procedures.
Preserve unique behavioral requirements, referenced heading contracts, protected evidence, upstream agent instructions, and unrelated edits.

## Affected scope and risk

Agent instruction loading, native adapters, workspace initialization, package resources, and linked heading anchors can consume these guides.
Qualitative risk is moderate: aggressive shortening can silently remove a required rule or break instruction discovery.
Inspect source requirements and consumer contracts before editing. Record before/after coverage and actual validation here.

## Findings and changes

| Finding | Result and evidence |
| --- | --- |
| Duplicate always-loaded procedures | Reduced [AGENTS.md](../../AGENTS.md) from 539 to 221 lines and 42,969 to 19,234 bytes. Detailed procedures now have mandatory links to existing maintained owners. |
| Stale knowledge layout instructions | Corrected four lines in [the task guide](../README.md#update-knowledge-after-clarification). Canonical restrictions now name `knowledge/records/`; retained sources and audits use `knowledge/evidence/`. |
| Historical quotations mixed with active procedure | All nine exact quotations remain in existing original captures. The [authority bindings](evidence/authority-bindings.json) retain their hashes and all 33 prior authority links. No duplicate archive was added. |
| Necessary apparent duplication | Retained native skill aliases and upstream wiki instructions. Initialization consumes the aliases; the wiki compiler and incremental recipe consume its native schema. |
| Unusable commands or discovery claims | The connected-guide audit established no expired command or broken discovery rule. Client-specific adapters remain available. |

All 25 existing headings remain in the same order, including source anchors used by other guides.
Root policy still requires migration compatibility, honest identity mappings, impact-based priority, default Ponytail, scoped commits, writing rules, and bounded dependency acquisition.
Independent semantic review found no material requirement loss. Linked procedures remain mandatory for their applicable scope.
The [changes record](evidence/changes.json) binds both edited guides to their original revisions and current hashes.
It records content reduction without deleting files, relocating evidence, or changing source authority.

## Verification and limits

The [validation record](evidence/validation.json) records actual checks and inspected scope.

- All 28 affected workspace tests pass. Current workspace validation reports zero findings.
- All 91 local links in the two edited guides resolve in the source checkout.
- The wheel builds without dependency acquisition. An isolated installed import initializes and validates an empty workspace outside this checkout.
- Installed initialization copies both revised guides exactly. Its 83 procedure links resolve; eight historical links remain explicitly source-checkout-only.
- The generated workspace contains no project task history, business records, runtime source copies, or runtime tests.
- Protected sources, audit events, canonical records, upstream wiki inputs, aliases, and unrelated local changes remain unchanged.

The byte reduction concerns the root entry guide. It does not measure model tokens, semantic adherence, or elapsed workflow time.
Detailed procedures still require reading when their scope applies. No live agent-client session or business scenario was executed.
Current documentation updates are limited to the root guide and the stale task-guide statements.
No critical conclusions require user attention or action.

## Follow-up assurance outcome

**No introduced regression was found in the inspected scope. Live model adherence remains unverified.**

The [assurance record](evidence/assurance.json) compares exact commits `55bc74d19` and `e2a8054ea`.
Its change fingerprint is `9eae2822e860fce9970b4ff5a2565f67a912ca8c151ef1c7c53cdf7c8b8f33c4`.
Two independent reviews found no lost requirement or broken consumer contract.
They traced removed rules to retained root text or mandatory maintained owners.

- All 82 workspace and hook tests pass, with zero failures.
- Paired installed initialization produces 392 matching paths and 38 matching alias links.
- Only the two intended guide files differ after excluding the generated workspace UUID.
- Baseline and candidate workspaces both validate with the same empty catalogs and zero knowledge documents.
- Across the reviewed commits, runtime code, skills, adapters, package manifests, wiki inputs, and all 245 protected files remain byte-identical.
- All 25 heading contracts and the source, publication, retention, compatibility, priority, and test requirements remain available.

The paired baseline uses exact prior guide bytes with the unchanged installed initializer and remaining scaffold resources.
The review added no changes to either guide after `e2a8054ea`.
These checks found no regression. Future model behavior remains unverified.
No live agent session, native Windows execution, or business deployment was performed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review or live agent adherence.
```
