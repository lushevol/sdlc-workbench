---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Knowledge documentation structure and content review

**The overall structure makes sense. Keep one canonical knowledge layer, one compiled wiki, and the existing engine-selection rule. Correct the project-selection instructions and unsupported generated architecture claims before the next maintenance run. Then complete the fallback procedure and reduce documentation drift.**

Status: remediation in progress under the [follow-up authorization](../evidence/knowledge-documentation-review-20261111/user-input.md#remediation-authorization). Findings below describe the review baseline; the remediation ledger records each later fix and verification. Baseline: `01750558bbce9413921568917bd0cc4f2694a403` on `codex/ces-gap-clarification-20261109`. A concurrent documentation commit, `edafad4dc`, added an independent initial-ingestion review; it did not change the reviewed knowledge guides or wiki.

Authorizing input: [exact user request](../evidence/knowledge-documentation-review-20261111/user-input.md), 11 November 2026.

Review scope: current knowledge management guides, shared skill instructions and integration references, generated wiki organization and source traceability, and historical review navigation. Remediation preserves canonical knowledge and original upstream packages.

## Remediation ledger

| Finding | Status | Change and verification |
| --- | --- | --- |
| F1 | RESOLVED | Root, bridge and nested instructions translate upstream commands through the project-scoped launcher. Independent forward check from `/private/tmp` selected this wiki, returned 12 indexed documents, and found no launch ambiguity. Skill validation and both upstream source locks pass. |
| F2 | PENDING | Generated responsibility claims. |
| F3 | PENDING | Fallback authoring and provenance completion. |
| F4 | PENDING | Reserved storage exception. |
| F5 | PENDING | Standalone claim traceability. |
| F6 | PENDING | Historical navigation and policy. |
| F7 | PENDING | Focused content and detail preservation. |
| F8 | PENDING | Procedure ownership and examples. |

## What makes sense

The current layers have useful, separate responsibilities:

| Layer | Current owner and role | Assessment |
| --- | --- | --- |
| Canonical intent | `knowledge/candidates/` and reviewed domain directories; [knowledge standards](../../knowledge/README.md). | Keep. IDs, versions, sources and review/publication gates belong here. |
| Source evidence and governance | `evidence/knowledge/`; task evidence for implementation, deployment and conformance gaps. | Keep. Generated text cannot establish source authority or approval. |
| Derived knowledge wiki | [Wiki index](../../knowledge/llm-wiki/wiki/index.md); summaries, concepts, entities and saved explorations. | Keep one copy. The richer OpenKB pages are useful for discovery. |
| Engine and maintenance | [Workbench bridge](../../.agents/skills/llm-wiki/SKILL.md) and [procedures](../../.agents/skills/llm-wiki/references/workflows.md). | Keep explicit URL/token selection, with current-session llm-wiki-agent fallback. |
| Wiki graph | [Native OpenKB viewer](../../knowledge/llm-wiki/output/visualize/graph.html). | Keep for page navigation. Its links are untyped wikilinks. |
| Engineering evidence graph | [Service graph skill](../../.agents/skills/service-dependencies-graph/SKILL.md). | Keep separate. Its Knowledge tab projects governed records and evidence. |

Source files are linked instead of duplicated. The wiki index clearly states candidate/draft limits. Current top-level setup, dependency and workspace-design guides agree on the engine rule. Neither a new wiki nor another knowledge product is needed to address these findings.

## Inventory and content shape

The [review inventory](../evidence/knowledge-documentation-review-20261111/review-metrics.json) binds all 91 derived pages and 12 canonical input files to their SHA-256 values.

| Content | Files | Whitespace-separated words |
| --- | ---: | ---: |
| Canonical candidate records | 12 | 23,474 |
| Derived summaries | 12 | 9,895 |
| Concepts | 34 | 34,121 |
| Entities | 39 | 31,623 |
| Saved explorations | 6 | 3,270 |
| Total derived pages | 91 | 78,909 |

The derived text is about 3.36 times the canonical corpus by this measure. This is an indicator of reading and maintenance cost, not proof of waste or better quality. A comparison of concept/entity paragraphs of at least 35 words found no exact duplicates after whitespace normalization; the repetition identified below concerns overlapping narratives. Sixteen of 34 concepts declare just one summary source. Single-source concepts can still be useful, but their creation should depend on a recurring question or a distinct reusable topic.

The retained native graph contains 85 nodes and 1,468 directed links: 12 summaries, 34 concepts and 39 entities. It excludes the six explorations and canonical/raw source aliases. Preserve this scope statement next to the graph link. Graph density does not measure factual correctness or domain completeness.

## Findings and recommended adjustments

### F1 — Make project-scoped launch instructions explicit

Priority: high, before the next operator run. Owner: Workbench maintainer.

The unchanged [OpenKB skill](../../.agents/skills/openkb/SKILL.md#first-find-where-the-kb-lives), lines 35–59, directs the agent to run bare `openkb status`. Its lookup searches parent directories and then a global default. The current runtime is isolated in `.venv-openkb/`, and the active KB is nested under Workbench. In the local check, the bare command was unavailable on `PATH`; invoking the isolated native command from the project root selected a different, pre-existing sibling KB and then failed at a denied lock write. No global configuration changed. The bridge's project-scoped `run status` selected the correct wiki.

The root [wiki rules](../../AGENTS.md#primary-knowledge-wiki) already direct agents to the bridge, which reduces the risk. The missing part is an explicit translation of upstream discovery and command examples. Document that Workbench operations always start through:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py run status
```

Keep upstream files unchanged. Put the project-selection rule and command translations in Workbench-owned instructions, including the nested wiki guide. Do not instruct users to fix this by setting a global KB.

### F2 — Correct generated responsibility claims and unsupported coupling

Priority: high, before using these pages as architecture references. Owner: knowledge maintainer; domain review remains separate.

The summary layer generally retains the principal source distinctions and open questions. Two inspected concept/entity areas contain stronger claims than their sources support:

| Generated claim | Source comparison | Recommended correction |
| --- | --- | --- |
| [Portal entity](../../knowledge/llm-wiki/wiki/entities/fmo-post-trade-portal.md#what-it-is), line 17, delegates portal authentication and entitlement retrieval to the SDK. [SDK concept](../../knowledge/llm-wiki/wiki/concepts/single-ui-sdk-authentication.md#boundary-with-portal-access), line 58, makes SDK authentication the prerequisite supplying portal-entry identity. | [Authentication responsibilities](../../knowledge/candidates/security/KT-authentication-and-sessions.md#authentication-responsibilities), lines 205–207, assigns UI exchange, user information, entitlement retrieval and token issuance to the BFF. [SDK responsibility](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#integration-purpose-and-responsibility-boundary), lines 374–376, describes JWT validation in downstream Spring applications. [Architecture limits](../../knowledge/candidates/architecture/ARC-portal-service-relationships.md#portal-and-sdk-boundaries), lines 133–136, keeps adoption conditional and unconfirmed. | Distinguish BFF login/token responsibilities from downstream SDK validation and entitlement helper APIs. Preserve the source's design/adoption limits. |
| [MFE Base entity](../../knowledge/llm-wiki/wiki/entities/mfe-base.md#http-and-token-handling), line 71, says provider-union permission checks consume the HTTP interceptor because accepted grants require logging. | [FE-COMPAT-AC-004](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004), lines 274–297, specifies union results and provider-source logs. It establishes no interceptor or transport dependency. | Remove that dependency claim, or label it as an implementation question requiring separate evidence. |

These are derived-content findings against the canonical records, not a new production architecture assessment. Native format checks cannot detect either error.

### F3 — Complete the fallback authoring and provenance procedure

Priority: medium; required before the next fallback compilation after a canonical change. Owner: Workbench maintainer.

The [fallback procedure](../../.agents/skills/llm-wiki/references/workflows.md#compile-canonical-records), lines 27–33, tells the ADE agent to maintain pages and log source IDs/hashes. It does not define the completion transaction for `source-manifest.json` and `.openkb/hashes.json`. The [launcher](../../.agents/skills/llm-wiki/scripts/wiki.py), lines 227–238, advances both during native compilation; lines 252–264 reject stale bindings. An agent can follow the prose and still leave verification failing after an authorized source edit. This is a procedure gap; existing unchanged bindings currently verify.

New-page instructions also conflict. The generated [wiki schema](../../knowledge/llm-wiki/wiki/AGENTS.md#frontmatter-managed-by-code--do-not-emit-it-in-generated-content), lines 39–44, assumes code owns frontmatter and tells generated content to omit it. The [original fallback format](../../.agents/skills/llm-wiki/upstream/AGENTS.md#page-format), lines 45–54, uses different page types. Preserving existing metadata is clear; creating valid new pages in direct-agent mode is not.

Add a Workbench-owned fallback contract with complete native-format page examples and explicit precedence for the shared layout. Define: source scope and before-hash; semantic edits and changed-page review; unchanged-source check; relative-link reconciliation; binding/registry update; index/log reconciliation; local verification. Record the actual agent mode. Advance hashes only after the semantic work is complete; changing hashes alone must never count as compilation. A guarded completion helper could implement this later without changing either upstream package.

### F4 — State the derived-wiki exception in the primary storage contract

Priority: medium. Owner: documentation maintainer.

[Knowledge standards](../../knowledge/README.md), lines 10–15 and 45–47, describes `knowledge/` as canonical domain Markdown with the full governance contract. Lines 179–183 says validation rejects other artifacts. The [README folder table](../../README.md#create-a-workspace), line 114, says the same. These statements omit the reserved subtree that contains source aliases, native page metadata, local state and HTML.

The scoped exception is already explicit in [AGENTS](../../AGENTS.md#primary-knowledge-wiki), lines 208–210, and [workspace design](../WORKSPACE_DESIGN.md), lines 209–217. Add that exception to the primary standards and folder table/tree. Explain that Workbench validates canonical records while the bridge validates the derived format and bindings. Keep the exception limited to `knowledge/llm-wiki/`.

### F5 — Make important claims traceable from a standalone page

Priority: medium. Owner: knowledge maintainer.

Concept/entity frontmatter generally lists whole summaries. Exact canonical IDs, versions and hashes are available in the [source manifest](../../knowledge/llm-wiki/source-manifest.json), but an important rule often takes several hops to inspect. A concrete locator was damaged in the [admin summary](../../knowledge/llm-wiki/wiki/summaries/KT-admin-and-onboarding.md#empty-subject-tile-clarification), line 40: `KT sdk and entitlements#ui empty subject ac 001` is plain text instead of a navigable criterion link.

Add a compact source-and-status note to important standalone pages, and direct canonical links beside critical rules and criteria. Repair the damaged locator to [UI-EMPTY-SUBJECT-AC-001](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001). Keep native metadata intact and source hashes in the manifest. Repeat the candidate/draft qualifier near the top where a page could otherwise read as approved policy; do not rely only on the index preamble.

### F6 — Distinguish historical reports from current operating instructions

Priority: medium. Owner: documentation maintainer.

The old [adoption report](LLM_WIKI_ADOPTION_20261105.md), lines 3–5 and 25–31, reads as current and says upstream tools were not installed. The [refresh report](LLM_WIKI_REFRESH_20261110.md), lines 3–17, still describes the previous wiki. Three local links in these reports target removed `knowledge/wiki/` paths: adoption lines 5 and 44; refresh line 17.

The [benchmark report](QMD_OPENKB_BENCHMARK_20261111.md), lines 7 and 94, says OpenKB is now active/primary without the explicit URL/token condition. Lines 11–17 call the archived comparison output “current.” The [direct comparison](LLM_WIKI_DIRECT_COMPARISON_20261111.md), line 7, describes a removed comparison workspace in present tense; its deletion note appears only at line 36.

Add a short historical/superseded banner with a current-policy link. Bind historical outputs to their original revision or retained archive locator. Use the existing [migration report banner](OPENKB_PRIMARY_MIGRATION_20261111.md) as the pattern. Preserve benchmark results and historical claims; do not restore duplicate wikis to satisfy obsolete links. State which old lint findings were repaired so that a historical failure is not mistaken for the current state.

### F7 — Reduce overlapping narratives while preserving useful detail

Priority: low, after correctness and maintenance gaps. Owner: knowledge maintainer.

The [portal entity](../../knowledge/llm-wiki/wiki/entities/fmo-post-trade-portal.md#session-renewal) grows to 346 lines and repeats session criteria, permissions, onboarding and release narratives. [Application ownership](../../knowledge/llm-wiki/wiki/concepts/application-ownership.md#admin-module-and-catalog-administration) repeats substantial catalog, release and interoperability details. These topics already have focused concept pages. The schema describes concepts as cross-document synthesis, while 16 of 34 currently cite one summary.

Use each page type for a distinct job: summaries explain one source; concepts own focused cross-source rules and conflicts; entities identify a named thing, its responsibilities, interfaces and related topics; explorations preserve requested answers. Keep useful single-source topics when they support a recurring question. Trim entity overviews by linking to the detailed concept rather than repeating its whole narrative. Preserve detailed material and contradictory evidence until its current consumers are checked.

Minor polish can follow: the release summary starts at an H2 without a document title, and the portal-purpose summary has two “Related concepts” sections. These do not block retrieval.

### F8 — Give repeated policy one owner and correct small examples

Priority: low. Owner: documentation maintainer.

Credential routing, fallback layout, immutable links and graph rules recur in README, AGENTS, SETUP, DEPENDENCIES, WORKSPACE_DESIGN and several skill entrypoints. Current active guides largely agree, but each repetition adds another place to maintain.

Keep engine/layout details in the bridge; caller skills need only their trigger, authorization boundary and completion check. Keep installation commands in SETUP, package/network facts in DEPENDENCIES and architectural responsibilities in WORKSPACE_DESIGN. Link to these owners from short overviews.

Also correct two examples: [wiki procedures](../../.agents/skills/llm-wiki/references/workflows.md#compile-canonical-records), line 24, uses nonexistent `knowledge/confirmed`, while accepted records belong in relevant domain directories. Use a real selected directory or an explicit placeholder. The [template guide](../../core/knowledge/templates/README.md#supported-knowledge-records), line 13, sends every template to candidates; exempt governance findings, which belong under `evidence/knowledge/findings/`.

## Suggested documentation hierarchy

| Entry or document | Keep here |
| --- | --- |
| `knowledge/index.md` | Short task choices: find canonical knowledge, browse candidates, open the compiled wiki, review governance. |
| `knowledge/README.md` | Canonical contract, lifecycle, evidence rules and the reserved derived-subtree exception. |
| `.agents/skills/llm-wiki/SKILL.md` | Engine rule, project-scoped entry and links to exact procedures. |
| Bridge workflow reference | Compilation, fallback authoring/provenance, query, validation, graph and failure recovery. |
| Individual knowledge skills | Scope, trigger, handoff and completion criteria for ingestion, query, governance and release sync. |
| `knowledge/llm-wiki/wiki/index.md` | Browse summaries, concepts, entities and explorations; visible status and graph links. |
| SETUP / DEPENDENCIES / WORKSPACE_DESIGN | Installation / package and access needs / architecture and ownership. |
| Current review plus historical archive | Decisions, evidence, measured limits and supersession links. Avoid using historical reports as the operator manual. |

## Order of work and completion criteria

1. Correct F1–F2: all operator examples select this KB; sampled BFF/SDK and permission claims match cited canonical scope.
2. Complete F3–F5: an authorized no-credential maintenance run can create/update a page and finish with truthful current bindings; contracts and critical citations are unambiguous.
3. Repair F6: old outputs remain recoverable through frozen locators, and current policy is visible before historical results.
4. Optimize F7–F8: reduce reading/repetition cost while preserving the detail users found useful in OpenKB.

Reuse the [six benchmark questions](KNOWLEDGE_BENCHMARK_QUESTIONS_20261111.json) for a future semantic acceptance review. Score claim correctness, intent-versus-implementation separation, candidate qualifiers, exact citation support, conflict handling and answer usefulness. Record retrieval and synthesis time separately. Document volume, source coverage, passing schema checks and graph link counts cannot substitute for that review.

## Checks and limits

- Bridge `verify`: all 12 canonical source bindings remain current; all six native structural categories have zero findings.
- Workbench validation: `VALID`, 14 canonical/governance documents, zero findings.
- Project-scoped status: correct Workbench wiki, 12 indexed documents.
- Local management-document target check: 400 Markdown targets across 20 guides/reports/diagram documents; three missing file targets, all in F6. The [link audit](../evidence/knowledge-documentation-review-20261111/link-audit.json) records the checked document set and missing locators. Historical heading anchors and external URLs were not checked.
- Review output checks: all 39 local report targets and their referenced heading anchors resolve; evidence JSON parses; diff whitespace checks pass. The `automated_check` field concerns these new review outputs, not a finding-free corpus or complete writing compliance.
- Inventory: 91 derived pages and their hashes recorded; native embedded graph JSON parsed without regeneration.
- Semantic review: all 12 summaries compared with canonical records; selected material concept/entity assertions inspected. This is not a sentence-by-sentence audit of the approximately 79,000-word derived corpus, a reread of all original raw exports, or live business verification.

No model-provider calls were needed. Original upstream packages, canonical records and generated wiki pages were not edited. These checks establish the present structural state and support the cited findings; they do not certify every generated claim. Writing review remains `PENDING`.
