# Wiki comparison evidence

The single active compiled wiki is [knowledge/llm-wiki/](../../../knowledge/llm-wiki/wiki/index.md). Its pages retain candidate/draft source boundaries. Selecting that workspace does not publish or approve its knowledge.

The former expanded OpenKB benchmark and llm-wiki snapshots are consolidated into [wiki-comparison-snapshots-20261111.tar.gz](wiki-comparison-snapshots-20261111.tar.gz). Their original content bytes are preserved, including the prior exporter, graphs, logs, manifests, original OpenKB lint report, and archived instructions. The two expanded historical directories were removed after verification so they no longer appear as competing browsable wikis.

## Authorizing input

Source: user turn in the Workbench knowledge comparison Codex chat, 11 November 2026. Exact wording:

> OK, now safe remove duplicate llm wikis documents only keep authed one. The rule is openKB as primary llm-wiki if provide llm url and token other wise use llm-wiki-agent instead.

The earlier instruction to retain comparison materials remains satisfied by the archive, its manifest, and the comparison reports. The engine-selection rule is implemented by the active workflow; historical compilation provenance remains unchanged when the maintenance engine changes.

## Archive and verification

| Snapshot prefix | Original repository directory | Files | Original bytes |
| --- | --- | ---: | ---: |
| `openkb/` | `docs/reviews/benchmark-evidence/openkb/` | 107 | 879,932 |
| `llm-wiki/` | `docs/reviews/benchmark-evidence/llm-wiki/` | 28 | 689,351 |
| Total | Both historical snapshots | 135 | 1,569,283 |

The archive occupies 399,698 bytes. Its SHA-256 is `edd2ad1116b8d8d4127abe8e91bd9bca00b153ef88c81f4f4a4a4743d6a84f52`.

[The manifest](wiki-comparison-snapshots-20261111.manifest.json) maps every original repository path to an archive member, byte count, SHA-256, original file mode, and preservation reason. All 135 saved members were read back and their sizes and hashes matched the originals before removing the expanded directories. The archive was generated twice with normalized timestamps and owner metadata and produced identical bytes; the hidden `llm-wiki/graph/.gitkeep` member is included.

The original llm-wiki `inventory.json` remains inside the archive and still binds its 26 historical payload files. The broader archive manifest also covers that inventory and both original snapshot READMEs. No canonical source, active wiki document, or upstream source was removed through this consolidation.

## Historical member locators

Comparison-report links point to the manifest and name the exact archive member beside the link. For example, `openkb/wiki/concepts/session-activity-renewal.md` identifies the original OpenKB concept, while `llm-wiki/wiki/concepts/session-lifecycle.md` identifies the earlier, broader llm-wiki topic.

The original source copies in `openkb/wiki/sources/` are frozen comparison inputs inside the archive. The active `raw/` and `wiki/sources/` files remain links to canonical classified records rather than duplicated source files.

From the Workbench root, inspect a historical file without restoring a second wiki:

```sh
tar -tzf docs/reviews/benchmark-evidence/wiki-comparison-snapshots-20261111.tar.gz
tar -xOf docs/reviews/benchmark-evidence/wiki-comparison-snapshots-20261111.tar.gz openkb/wiki/concepts/session-activity-renewal.md
```

To inspect the entire snapshot, extract into a temporary directory outside the active knowledge workspace:

```sh
comparison_review_dir="$(mktemp -d /tmp/workbench-wiki-comparison.XXXXXX)"
tar -xzf docs/reviews/benchmark-evidence/wiki-comparison-snapshots-20261111.tar.gz -C "$comparison_review_dir"
```

Recovered snapshots preserve historical relative-link context and can contain outdated or unresolved claims. Use their original manifests and recorded source paths for provenance. They remain comparison evidence rather than live instructions or approved knowledge.

See the retained [benchmark and reassessment](../QMD_OPENKB_BENCHMARK_20261111.md), [direct llm-wiki comparison](../LLM_WIKI_DIRECT_COMPARISON_20261111.md), [migration record](../OPENKB_PRIMARY_MIGRATION_20261111.md), and [predefined questions](../KNOWLEDGE_BENCHMARK_QUESTIONS_20261111.json).
