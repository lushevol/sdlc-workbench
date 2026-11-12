# Incremental knowledge update proposal

Source: user message in the owning Codex conversation, 12 November 2026.
Priority: explicit user goal for knowledge update efficiency.

## Exact user input

> I want my knowledge base updates to only detect incremental updates from source files, reducing token consumption and increasing efficiency. how to optimize

Implementation authorization, same conversation, 12 November 2026:

> good, implement them

This authorizes the file-level implementation below. Section-level processing remains deferred as proposed.
See [the implementation and validation result](incremental-implementation.md) for the completed stage.

## Review scope

Inspect current incremental detection and propose the smallest complete improvement.
Keep implementation changes separate from this proposal review.
Use [the lifecycle contract](../../KNOWLEDGE_LIFECYCLE.md) for stage ownership and existing engine controls.

## Current source inspection

| Stage | Existing behavior | Optimization gap |
| --- | --- | --- |
| Source refresh | Reuses unchanged source revisions and reviewed selections when source, policy, and context hashes match. | Feed its changed and affected-record inventory downstream instead of rereading all sources. |
| Filtered source view | Emits all current kept pages. | Add explicit planned-file selection while preserving omissions and exact provenance. |
| Canonical knowledge | Refresh identifies records directly citing modified or missing source revisions. | Add bounded dependency expansion and successful-processing receipts, including supported no-change outcomes. |
| Wiki compilation | The bridge invokes native compilation for every selected unique canonical record. | Skip completed unchanged bindings before any semantic model call; support exact record selection. |

Evidence: [source decision reuse](../../../core/ingestion/sources.py#L410), [direct affected-record lookup](../../../core/ingestion/sources.py#L323),
[full kept-view emission](../../../core/ingestion/sources.py#L552), and [unconditional bridge compilation](../../../.agents/skills/llm-wiki/scripts/wiki.py#L213).

## Bounded wiki binding check

An independent reader checked local JSON metadata, hashes, aliases, and output existence on 12 November 2026.
The check used standard-library reads, without engine commands, model calls, configuration reads, or secret access.

- Twelve manifest sources and twelve native registry entries were present.
- All twelve canonical hashes matched their manifest bindings; registry document names matched.
- Both aliases resolved to the canonical original for each source; twelve expected summaries existed.
- The wiki also contained 34 concept pages, 39 entity pages, and six explorations.

These results establish current binding agreement and expected-summary existence only.
They do not establish structural validity, semantic accuracy, reviewed output hashes, or a completed processing recipe.

## Recommended implementation order

1. Create a deterministic update plan before semantic work.
   Reuse refresh results for new, modified, missing, reused, and directly affected canonical records.
   Include invalidated policy/context bindings and unfinished attempts. Return compact counts and queued paths to the agent.
   Keep full unchanged inventories on disk rather than placing them in model context.
2. Add exact planned-file selection to filtered views and wiki compilation.
   Review complete changed source pages first. Load only relevant prior records, definitions, exceptions, and affected dependent pages.
   New or changed meaning can require bounded topic discovery beyond declared links. Broaden review when relationships are incomplete.
3. Track successful processing separately from observed hashes.
   A refresh or source selection does not prove canonical extraction or wiki maintenance finished.
   Reuse selection and wiki manifests. Add compact canonical processing receipts for outputs and supported no-change outcomes.
   Bind receipts to input identities/hashes, relevant policy/context, processor recipe, target starting hashes, and checked outputs.
   Keep incomplete attempts retryable. Commit success only after the stage's actual review and integrity requirements pass.
4. Add a safe unchanged-source guard to the existing wiki bridge before its semantic compiler call.
   Check canonical identity/hash, both aliases, registry/manifest agreement, completed review receipts, and expected outputs.
   Missing outputs, partial generation, mismatched bindings, relevant recipe changes, or unfinished work require scoped repair or review.
   Compare requested canonical scope with recorded bindings so new records remain visible.
5. Preserve explicit propagation boundaries.
   After source re-selection, unchanged selected meaning can produce a supported no-change receipt without rewriting canonical knowledge.
   Changed canonical meaning updates affected summaries, prior and new concepts/entities, contradictions, links, and index entries.
   Review withdrawn claims on former dependents, even when a new compiler plan omits those pages.
   Invalidate affected saved explorations when relevant. Preserve stale qualifications until authorized regeneration.

Local hashing can inspect all files without sending their contents to an LLM.
Skip semantic work for unchanged completed inputs. Keep local integrity checks for their applicable scope.
Literal zero model invocation on an unchanged run requires running the local planner before starting an agent session.
An already running ADE session still has routing overhead.

Use existing storage and engines; add metadata rather than copied document trees.
Bootstrap from existing manifests and receipts. Missing completion evidence requires scoped review, not automatic global recompilation.
Do not make every global index change invalidate every source; track only relevant dependencies and shared-page updates.

## Later optimization for large documents

Start with file-level increments. They preserve the existing complete-source review rule and minimize implementation changes.
Consider section-level hashing only when measurements show that a few large changed documents dominate input tokens.
Use heading-aware diffs, surrounding definitions, exceptions, governing context, and changed references when selecting those sections.
Preserve original full-file SHA-256 and exact source ranges as authoritative provenance.
Any normalized or section fingerprint is an optimization key, never a replacement for the retained raw hash.
This later mode requires an explicit processing-policy change and its own negative-case checks.

## Proposed verification

| Case | Required observable result |
| --- | --- |
| Identical successful rerun | No document content sent for semantic processing; zero additional semantic model calls. |
| One source changes | Process that source and its supported affected closure. Preserve unrelated canonical and wiki outputs. |
| Only excluded source content changes | Reassess selection; no downstream intent processing unless relevance or context changes. |
| Selected meaning remains unchanged | Record supported no change and current provenance; avoid unnecessary canonical or wiki rewrites. |
| Policy or governing context changes | Reassess affected decisions despite unchanged source bytes. |
| New or missing source | Discover new scope; preserve missing-source history and unresolved consequences. |
| Failure, partial output, split bindings, or concurrent change | Resume or reconcile affected work; never treat observed hashes alone as successful completion. |
| A source withdraws a claim | Review prior dependent pages and remove or qualify unsupported derived claims. |

Measure scanned/changed/reused files, selected bytes, actual semantic calls, provider token usage when available, elapsed time, and retries.
Do not claim a token-saving percentage without measured before/after runs.
Use existing tests for source races, binding consistency, provider failures, and retained per-source success.
Add focused no-op and affected-scope regressions when implementing incremental execution.

## Limits and next decision

Confidence is high for the inspected source behavior. No performance benchmark or model compilation ran during this review.
Local reference targets and Markdown anchors passed review checks. The staged diff must also pass whitespace checks before commit.
This document proposes implementation. Runtime commands, skills, source decisions, canonical knowledge, and wiki state remain unchanged.
The recommended next stage is file-level incremental planning, scoped views, processing receipts, and safe wiki skipping.
Section-level processing can follow measured evidence of remaining token cost.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
