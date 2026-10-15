# Bidirectional Impact Analysis

Use the same canonical graph for both planning and regression review.

## Requirement to code

Normalize the requirement into business nouns and actions. Match business-capability, page, application, service, and component explanations, then traverse both `BUSINESS` and `RUNTIME` relationships. Results are candidate impact, not a promise that every reachable file must change. Prioritize direct matches, short paths, public interfaces, persisted data, Kafka topics, and unresolved external frontiers.

When an authoritative business Wiki is available, use it to enrich terminology and retain its document/section provenance. The local graph and source remain authoritative for technical relationships. If no Wiki is available, label semantic mappings as inferred rather than inventing citations.

## Code to requirements

Map changed files to node `source_paths`, including wildcards. Traverse toward pages, capabilities, applications, services, APIs, data, and consumers. Report business and runtime impact independently. A broad wildcard match should trigger source inspection before assigning high confidence.

For independent checkouts, select the manifest repository explicitly:

```sh
.venv/bin/python .claude/skills/service-dependencies-graph/tools/analyze_impact.py --repository service-name --base-ref main --head-ref feature
.venv/bin/python .claude/skills/service-dependencies-graph/tools/analyze_impact.py --repo-ref service-one=main..feature --repo-ref service-two=main..feature
```

Omitting `--head-ref` compares the selected base to the worktree, including untracked paths. Rename/deletion paths remain workspace-relative; invalid repositories/refs fail explicitly. Results list examined and unexamined repositories. The harness repository is never an implicit substitute.

Exact source matches take precedence over ancestor wildcards. Incoming runtime dependencies propagate impact; containment is terminal navigation context. Outgoing reads/dependencies are context and do not make their other callers affected. Explicit write-to-reader and publication-to-consumer paths can propagate within resolved graph boundaries. Requirement seeds and inferred edges remain candidates. Unresolved frontiers come from boundary edge status and retain the edge, reason and evidence; an external node alone is not unresolved.

## Reporting

Include input mode, seed nodes and match reason, affected repositories, business impact, runtime impact, traversal paths, unresolved frontiers, and test areas suggested by affected public contracts. Distinguish direct, indirect, inferred, unresolved, and unknown findings. Missing graph edges are uncertainty, not proof of no impact.
