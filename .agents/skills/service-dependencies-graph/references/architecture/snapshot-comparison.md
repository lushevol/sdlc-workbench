# Compare dependency snapshots

Compare two saved graph bundles through the existing checksum-verified snapshot loader.
The operation performs no build, clone, network request, application change, or knowledge publication.

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH compare \
  --baseline OLD_BUNDLE --candidate NEW_BUNDLE
```

The installed Workbench command provides the same comparison.

```sh
ai-sdlc --workspace PATH graph compare --baseline OLD_BUNDLE --candidate NEW_BUNDLE
```

Use `--skip-current-check` only when comparing saved evidence without current source inspection.
The result marks unchecked freshness explicitly.

## Read the differences

The result identifies both manifests, graph hashes, generator versions, and saved source counts.
It reports added, removed, changed, and unchanged nodes, edges, evidence, repositories, and investigated claims.
Changed records retain both versions and their direct source evidence.
All referenced identities remain bound to their saved snapshot hashes.

Repository coverage changes can reflect extraction scope or omitted context.
The separate `source_inventory` comparison checks source-selection fingerprints through the existing inventory contract.
It includes source hashes, independent Git revisions, dirty states, classification, and configured source roots.
Do not equate a coverage change with changed business code.

The result lists direct static consumers of changed edges, targets, or evidence.
Containment edges do not establish consumer impact.
Transitive reachability, dynamic calls, deployment, and user consequences remain unexamined.
Affected static consumers require source review before a business impact claim.

## Inspect freshness and scope

Current source and architecture-context freshness reuse the coverage query and its inventory exclusions.
Each snapshot reports `knowledge_freshness` separately for its selected knowledge projection input bytes.
Changed knowledge inputs mark that field `STALE`, even when repository sources remain `CURRENT`.
An unchanged saved comparison remains `UNCHANGED` when only current knowledge inputs have changed.
Skipping the current check marks saved knowledge projection freshness `NOT_CHECKED`.
Legacy snapshots without a knowledge projection report `NOT_AVAILABLE`.
Knowledge freshness does not establish source authority, business applicability, approval, or execution.
Investigated claims with changed cited files receive explicit reinvestigation actions.
The result preserves stale sources without changing their previous assessments.
A source-only candidate has a different architecture context scope from an investigated snapshot.
Removed claims then describe omitted context. They do not disprove relationships.

Initial instruction freshness requires a captured source fingerprint.
If the saved context did not capture that file, its historical freshness remains `UNKNOWN`.
A present instruction file alone cannot establish unchanged historical instructions.

Contract and test-case relationships require exact supported identities.
Existing snapshots do not supply those joins, so the result marks them unavailable.
Do not infer joins from names, repository proximity, or shared requirements.

## Validation limits

Bundle checks reject changed artifact bytes, duplicate identities, dangling graph references, and unsafe artifact paths.
Saved differences remain distinct from source freshness and semantic review.
Checksum identity does not authenticate an actor, approval, or build process.
A changed graph does not establish a broken dependency or release blocker.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
