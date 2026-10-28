# Deterministic graph skill optimization

**Critical conclusion:** The graph skill now searches dependency-shaped patterns before AI review.
Review candidates through the `patterns` query before interpreting unresolved relationships.

High-priority source: [exact user request](../evidence/graph-instruction-integration-20261028/user-input-20261028-optimize-skill.txt), 28 October 2026.

## Result

The skill now includes broader contract files in its source inventory.
It scans GraphQL schemas, protobuf files, modern JavaScript modules, HTML, EJS, and build configuration.

The build runs a bounded deterministic pattern census.
It records endpoint, configuration, messaging, database, module, gateway, and GraphQL-schema candidates.
Each candidate retains a repository, path, line, pattern, value, and review status.
Sensitive values are redacted. Robot interpolation and non-contract JSON remain excluded.

Literal SystemJS import-map entries now become canonical remote-load edges.
Exact local package identities resolve those edges when available.
Unknown modules remain unresolved boundaries.

## Coverage comparison

Both snapshots use the same current repository sources.
The baseline is the previous generated graph before this optimization.

| Dimension | Baseline | Optimized |
| --- | ---: | ---: |
| Repositories | 9 | 9 |
| Nodes | 6,507 | 6,517 |
| Edges | 17,818 | 17,836 |
| Evidence records | 17,981 | 17,998 |
| Inventoried source files | Not captured | 3,458 |
| Deterministic pattern candidates | 0 | 9,451 |
| Pattern scan files | 0 | 2,068 |
| Resolved import-map loads | 0 | 4 |

The graph count increase is deliberate and bounded.
Pattern candidates remain outside canonical edges until source review confirms their semantics.
The optimized graph includes four resolved import-map links and their unresolved remote boundaries.

## Operating procedure

Run the normal build after adding or changing repositories.
Read `analysis-coverage.json` and `coverage-declarations.json` before interpreting absence.
Use the `patterns` query to filter deterministic candidates by repository or family.
Review exact source lines before promoting an unresolved candidate into architecture context.

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query \
  --data-dir relationships/service-dependencies/generated patterns \
  --args '{"family":"HTTP_ENDPOINT","limit":100}'
```

## Scope and limitations

The pattern census provides high recall, not semantic precision.
It does not prove runtime execution, deployment, provider identity, or active configuration.
Typed extractors and exact identity joins remain canonical relationship sources.
AI review is still required for ambiguous candidates and unsupported dynamic expressions.

No business repository source changed. Generated graph output remains ignored.
The unresolved `core/release-report/` directory remains outside this stage.

## Validation

The [validation receipt](../evidence/graph-instruction-integration-20261028/optimization-validation.json) records the build, queries, tests, and checksums.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
