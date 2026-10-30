# Stage 6 verification: dependency snapshot comparison

**Six retained claims require source reinvestigation before reuse as current architecture evidence.**
Owner: unknown for architecture review; Workbench maintainer for the comparison tool.
Action: inspect each changed citation before updating its previous assessment.
Consequence: stale source evidence cannot support a current relationship claim.
Evidence: [current source comparison](GRAPH-REAL-003-current-source-delta.json).

Authorization: [exact implementation request](../user-input.md).
This stage adds read-only comparison through the canonical dependency graph skill.
It does not change business source, existing graph bytes, investigated context, or publication state.

## Real cases

| Case | Setup and observable result | Evidence |
| --- | --- | --- |
| GRAPH-REAL-001 | The retained graph has stale sources in two repositories and seven cited files. | [Current coverage query](GRAPH-REAL-001-current-freshness.json) |
| GRAPH-REAL-002 | Comparing the retained graph with itself reports zero saved differences. Current source staleness remains visible. | [Unchanged comparison](GRAPH-REAL-002-unchanged.json) |
| GRAPH-REAL-003 | Comparing retained and fresh source graphs identifies exact source changes and direct static consumers. | [Current source comparison](GRAPH-REAL-003-current-source-delta.json) |

Each completed case saved its evidence before the next case started.
The [verification script](verify_snapshot_delta.py) checks real bundles without synthetic graph changes.
The [verification receipt](verification-receipt.json) binds that script and implementation through SHA-256 values.

Both canonical graphs passed the existing semantic validation and relationship projection checks.
The [baseline validation](baseline-validation.json) and [candidate validation](candidate-validation.json) retain exact arguments and results.
The fresh source inventory matched current fingerprints after extraction.
The original graph remained unchanged.

| Saved identity | Baseline | Candidate |
| --- | --- | --- |
| Nodes | 6517 | 6518 |
| Edges | 17836 | 17866 |
| Architecture context | Investigated, with stale cited files | Source only |
| Current source freshness | STALE | CURRENT |
| Manifest | [Baseline identity](baseline-manifest.json) | [Candidate identity](candidate-manifest.json) |

The source inventory identifies `ratan-auth-server` and `single-ui-bff` changes.
Eight extraction coverage records differ because source and architecture context scope differ.
These are separate denominators.
The comparison retains 63 added, 33 removed, and 437 changed edge records.
It lists 128 direct static source nodes for follow-up inspection.

These counts include scope differences. They do not measure business impact.

## Preserved limits and failed checks

The candidate deliberately excludes the stale investigated context.
All 23 omitted claims retain `CONTEXT_SCOPE_DIFFERENCE` interpretation.
Their omission does not disprove the relationships.
The tool reports six stale claim assessments with exact source references and next actions.
Historical instruction freshness remains `UNKNOWN` because the retained context captured no instruction-file fingerprint.

The first comparison assertion incorrectly equated all repository coverage changes with source changes.
Its [failed receipt](GRAPH-REAL-003-current-source-delta-attempt01.json) remains available.
The implementation now reports source inventory changes separately from extraction coverage changes.
The corrected comparison asserts both denominators.

The first focused test setup supplied a relative source path to the lower-level builder.
That builder resolves source paths from the process directory.
The fixture now supplies its explicit temporary source root.
No application behavior changed through either fixture correction.

The candidate bundle remains under `.workbench/conversation-graph-source-20261030/`.
The retained baseline remains under `relationships/service-dependencies/generated/`.
This evidence directory retains manifests, exact changed records, validation results, and source identities.
The comparison requires those complete local bundles for reproduction.
It does not copy complete unchanged bundles into task evidence.

Static changes cannot establish active deployments, dynamic calls, broken dependencies, or user consequences.
Direct static consumers do not establish transitive impact.
Existing snapshots contain no supported contract or test-case joins, so these links remain unavailable.
Missing joins do not establish absent tests.
No business suite, application service, external network, or authenticated session executed during this stage.

```yaml
standard: ASD-STE100
automated_check: FAILED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
