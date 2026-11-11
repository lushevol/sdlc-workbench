# Knowledge Tools Benchmark and Compilation Reassessment

- Date: 11 November 2026
- Repository: Workbench
- Corpus: 12 candidate/draft knowledge records in `knowledge/candidates/`

Subsequent adoption: OpenKB is now the active engine at `knowledge/llm-wiki/`. The llm-wiki output and exporter assessed below, together with the original OpenKB benchmark snapshot, are preserved byte-for-byte in the [comparison archive](benchmark-evidence/README.md). Historical links below name the exact archive member recorded in the manifest.

## Result

The retained OpenKB compilation is more detailed and better organized for topic navigation than the current llm-wiki output. For the user's priority of a rich compiled knowledge base, OpenKB is the stronger demonstrated option. The earlier blanket recommendation that llm-wiki-agent was "enough" was not established by this benchmark and is withdrawn.

The current llm-wiki run is principally a source export with a small synthesis layer. It was not an equivalent semantic-compilation trial against OpenKB. A working graph, complete source-record coverage, and lower installation overhead do not establish equivalent compilation quality.

QMD is the local source retriever in this setup. With embeddings enabled, hybrid retrieval improved F1 from `0.667` to `0.778` at a reported mean of `15 ms`; full reranking reached `0.806` at about `5.4 s`. OpenKB is the slower answer synthesizer and returned source-linked answers with candidate and evidence limits. These measure different jobs, so their latency figures are not an apples-to-apples ranking.

For practical use, QMD hybrid is the best measured retrieval tradeoff on this fixture. Full reranking adds a small F1 gain at much higher latency. Use OpenKB when a synthesized answer with cross-page context is useful. OpenKB's answers are useful for exploration, but its lint findings still need correction before relying on the wiki as a clean reference layer.

## Compilation Quality Reassessment — 11 November 2026

Source: user feedback in the current Codex chat, preserved verbatim:

> I have checked the results from OpenKB, the compiled outcomes are more details and well organized than llm-wiki-agent, how you say llm-wiki-agent is enough ???

Inspection of the saved artifacts supports this feedback:

| Dimension | Current llm-wiki output | Retained OpenKB output |
| --- | --- | --- |
| Source inputs | 12 candidate/draft records | The same 12 source hashes |
| Source treatment | 12 exported record bodies with rewritten links and provenance | 12 retained full-text sources plus 12 synthesized summaries |
| Concept organization | 4 broad concept pages | 33 focused concept pages |
| Entity organization | 1 service-responsibility page | 39 entity pages |
| Catalog | Predominantly a list of technical page slugs | Grouped summaries, concepts, entities, and explorations with descriptions |
| Compilation performed | Deterministic source export plus five broad derived topic pages | Model-based summary, concept, and entity compilation |

The source equality check compared each llm-wiki source page's `workbench_sha256` with the corresponding archived OpenKB source SHA-256: all 12 matched. Raw source word counts are unsuitable for comparing synthesis effort because llm-wiki strips the original YAML frontmatter while OpenKB's retained full-text sources include it.

Concrete differences:

- The [former llm-wiki entitlement concept](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`llm-wiki/wiki/concepts/entitlements-and-ces-migration.md`) provides four core bullets. OpenKB separates [permission mapping](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/ems2-to-ces-permission-mapping.md`), [per-tile provider selection](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/per-tile-provider-selection.md`), [provider-union permission checks](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/permission-check-provider-union.md`), and [role multiplicity](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/ces-role-multiplicity.md`). Its provider-union page includes a truth table, acceptance criterion, and admission/ownership boundaries.
- The [former llm-wiki session concept](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`llm-wiki/wiki/concepts/session-lifecycle.md`) provides four core bullets and an unresolved-boundaries paragraph. OpenKB provides focused pages for [activity renewal](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/session-activity-renewal.md`), [expiry-prompt recovery](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/session-expiry-prompt-recovery.md`), and [token timing policies](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/concepts/token-lifecycle-and-timeout-policy.md`), exposing details otherwise buried in the exported records.
- The [former Workbench exporter](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`llm-wiki/implementation/wiki.py`) reads candidate bodies, strips frontmatter, rewrites links, and writes the body under native metadata. The [preserved operation log](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`llm-wiki/wiki/log.md`) explicitly records these exports as having no LLM invocation. Export coverage therefore does not establish that semantic ingestion was completed.

Page counts show granularity, not accuracy. OpenKB still has the structural and semantic findings recorded below, including repeated links to a missing release-governance concept and ambiguous CES field descriptions. These need source-backed correction; they do not invalidate its observed organizational advantage. This reassessment inspected representative content and the complete input/page inventory; it is not a claim-level correctness audit of every generated page.

The [original llm-wiki ingestion workflow](../../.agents/skills/llm-wiki/upstream/AGENTS.md) also requires summaries, concept/entity extraction, and contradiction review. The current result shows that our executed llm-wiki workflow fell short of the desired compilation depth; it does not prove that the upstream framework cannot achieve it. That capability would require a comparable semantic compilation using the same inputs, stated model and budget, and a common quality rubric.

**Revised recommendation:** use the saved OpenKB output as the quality baseline for detailed compilation. Current llm-wiki is a lightweight source-navigation layer whose adequacy for that richer goal remains unproven. Evaluate factual fidelity, meaningful topic coverage, organization, contradiction handling, and link validity separately from setup cost and retrieval latency.

## Setup

- QMD `2.8.3`, collection `candidates`, 14 indexed Markdown files (12 candidate records plus two navigation files). The `embeddinggemma-300M-Q8_0.gguf` model (318 MB) was downloaded for the benchmark and removed afterward.
- OpenKB `0.5.0rc2.dev3+gff54396e5`, 12 source records, 12 summaries, 33 concepts, and 39 entities.
- The OpenKB raw input was a symlink to `knowledge/candidates`; the archived compiled snapshot retains full-text source copies as `openkb/wiki/sources/` members.
- The full original OpenKB output is retained as comparison evidence under the archive member prefix `openkb/wiki/`; see the [archive and recovery guide](benchmark-evidence/README.md).
- OpenKB used `deepseek/deepseek-v4-flash`. The available `CHATBOT_OPENAI_*` endpoint was configured to `api.deepseek.com` with model `deepseek-v4-flash`; no usable OpenAI API credential was exposed to the OpenKB CLI. The API credential was not written to project files.
- The six predefined question areas and expected QMD source files are recorded in [the fixture](KNOWLEDGE_BENCHMARK_QUESTIONS_20261111.json).

## QMD Retrieval

Results from `qmd bench docs/reviews/KNOWLEDGE_BENCHMARK_QUESTIONS_20261111.json`:

| Backend | P@k | R@1 | R@3 | R@5 | MRR | F1 | Mean latency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BM25 | 0.667 | 0.500 | 0.667 | 0.667 | 1.000 | 0.667 | 2 ms |
| Vector | 0.750 | 0.417 | 0.750 | 0.833 | 0.917 | 0.778 | 229 ms |
| Hybrid | 0.750 | 0.500 | 0.750 | 0.833 | 1.000 | 0.778 | 15 ms |
| Full | 0.750 | 0.500 | 0.750 | 0.833 | 1.000 | 0.806 | 5,439 ms |

The benchmark index recorded 149 embedded chunks across all 14 documents. The first vector query took 1,293 ms while subsequent queries took about 15 ms, so the vector mean includes model initialization. Full mean latency includes QMD's reranking/generation path and is dominated by model work. These are the rounded timings reported by QMD's benchmark, not end-to-end application measurements.

Runtime note: the sandboxed process could not initialize the Metal backend, and `QMD_FORCE_CPU=1` reported that no CPU-only llama.cpp binary was packaged. The scoring run completed with host Metal access. One shader compilation warning appeared on the first query; the benchmark then completed all six queries.

## OpenKB Questions

All six DeepSeek-backed queries completed and are retained as archive members under `openkb/wiki/explorations/`. The saved answers link to wiki sources and retain candidate, draft, or missing-execution qualifications.

| Question area | Wall time | Saved answer |
| --- | ---: | --- |
| Session renewal and retry | 15.0 s | [Exploration](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/explorations/how-should-the-portal-preserve-an-active-session-across-refr.md`) |
| CES permission mapping | 11.9 s | [Exploration](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/explorations/what-candidate-mapping-rules-map-ems2-roles-and-entitlements.md`) |
| Frontend layers and ownership | 18.6 s | [Exploration](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/explorations/what-are-the-portal-frontend-composition-layers-and-ownershi.md`) |
| Release responsibilities | 11.7 s | [Exploration](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/explorations/which-responsibilities-belong-to-portal-and-tenant-teams-for.md`) |
| Interoperability contract | 13.2 s | [Exploration](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/explorations/what-candidate-interoperability-contract-and-openfin-fdc3-co.md`) |
| Observability and performance | 14.9 s | [Exploration](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/explorations/what-telemetry-and-performance-or-capacity-evidence-exists-f.md`) |
| **Mean / range** | **14.2 s / 11.7-18.6 s** | **6/6 completed** |

This was a source and governance review, not a blinded answer-accuracy study: no independent answer key or scoring rubric was applied. OpenKB latency includes a remote model call; it should not be compared directly with QMD's local retrieval latency.

## Limits and Next Steps

- The six-question sample is small and covers candidate knowledge only. It does not establish completeness, approved policy, production behavior, or business acceptance.
- The same-day OpenKB lint report found 14 broken links to the missing `concepts/release-window-governance` page and semantic consistency issues, including the CES field-count conflict and session-timeout contradictions. See [the lint report](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/reports/lint_20261111_144834.md`).
- QMD and OpenKB were initially uninstalled after comparison. OpenKB was subsequently reinstalled as the primary wiki engine; QMD and its index/model cache remain removed. The original benchmark snapshot remains historical evidence.
- Fix the broken and contradictory OpenKB pages, then repeat the six questions with an explicit answer rubric and a shared timing protocol.
