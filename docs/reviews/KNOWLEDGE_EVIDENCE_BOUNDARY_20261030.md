# Knowledge and evidence boundary review

No critical conclusions require user attention or action.

## Scope and priority reference

The user requested a recommendation about folder overlap.
The [preserved user input](../evidence/knowledge-evidence-boundary-20261030/user-input.md) is the high-priority scope reference.
This review concerns Workbench maintenance.
It does not authorize moving or deleting retained evidence.

## Recommendation

Keep the existing separation. Clarify folder ownership and reduce repeated task details.
Knowledge explains reusable business meaning. Evidence preserves the sources and observations that support or challenge that meaning.
Both can discuss the same subject without serving the same purpose.

| Location | Responsibility |
| --- | --- |
| `knowledge/` | Reusable domain rules, terms, requirements, architecture, and lifecycle-qualified candidates. |
| `evidence/knowledge/` | Source snapshots, provenance, governance findings, and immutable audit events. |
| `tasks/<task-id>/evidence/` | Investigation captures and execution results owned by a business task. |
| `docs/` | Workbench guides, maintenance reviews, and their supporting evidence. |

Candidates remain draft knowledge until the applicable review and publication gates pass.
An original source is evidence of its contents. Its storage location does not establish business authority or passing execution.

## Evidence-backed claims

Inspected tracked sources match Git revision `13f0e912ec0314c8bded2e0554518bf784697917`.
The inventory describes the current regular files under the two named roots.

| Claim | Class | Confidence and rationale | Evidence | Limit |
| --- | --- | --- | --- | --- |
| C1: The contracts already separate domain knowledge from supporting evidence. | Documented intent | High. Both folder guides state the boundary. | [Knowledge contract](../../knowledge/README.md#source-provenance-outside-knowledge), [evidence guide](../../evidence/knowledge/README.md), [workspace design](../WORKSPACE_DESIGN.md#folder-construction). | This does not establish semantic compliance for every document. |
| C2: The trees contain no identical files across their boundaries. | Observed execution | High. A Python scan compared SHA-256 values for 19 knowledge files and 156 evidence files. | [Inventory method and result](#inventory-method-and-result). | The scan does not detect semantic duplication. |
| C3: Some apparent overlap is original material plus a derived explanation. | Inspected records | High. The session topic combines two source versions and identifies conflicts. | [Session concepts](../../knowledge/candidates/security/KT-authentication-and-sessions.md#session-concepts-and-intended-lifecycle). | This is one inspected topic, not a complete semantic audit. |
| C4: Historical source identities resemble current knowledge paths. | Inspected records | High. The manifest separates `resource: knowledge/raw/...` from `snapshot: evidence/knowledge/sources/...`. | [Source manifest](../../evidence/knowledge/manifest.yaml), [source identity contract](../../knowledge/README.md#source-provenance-outside-knowledge). | A preserved identity is not a current storage locator. |
| C5: The session topic also contains detailed task disposition. | Inspected records | High. Its enhancement-status section includes P4/S4 backlog priorities and a proposed P3/S3 classification. | [Enhancement status](../../knowledge/candidates/security/KT-authentication-and-sessions.md#session-refresh-enhancement-status). | Domain scope and production-status qualifications remain useful knowledge. |

## Proposed refinements

1. Add a short folder-purpose table to the existing navigation guides.
   Explain that `evidence/knowledge/` means evidence supporting knowledge records.
2. Explain historical `resource` identities beside the manifest guidance.
   Use `snapshot` for current storage and preserve the stable identity.
3. Keep detailed task priorities, run results, and review disposition in the owning task.
   Retain reusable rules, production-status qualifications, and links in knowledge records.
4. Cite each retained source from derived knowledge instead of copying complete documents.
   Preserve the original bytes, revision, hash, and material disagreements.

Owner: Workbench maintainer. Next action: review these refinements before a separate maintenance change.
Qualitative risk is low for navigation changes.
Relocation has wider effects on source references, validation, initialization, and retained audit evidence.
The [evidence retention guide](../../evidence/knowledge/README.md) defines the required relocation safeguards.

## Inventory method and result

The scan used `Path.rglob('*')` for `knowledge/` and `evidence/`.
It selected regular files and excluded symbolic links.
It read each selected file and compared SHA-256 digest sets across the roots.

| Measure | Result |
| --- | --- |
| Knowledge files | 19 |
| Evidence files | 156 |
| Shared SHA-256 digest groups across the roots | 0 |

The scan excludes `docs/evidence/` and task evidence from its duplicate comparison.
It establishes byte comparison only. Similar meaning requires a separate content review.

## Scope and checks

The review inspected folder contracts, current inventory, manifest examples, and one domain topic with its original source.
It also inspected storage consumers in [initialization](../../core/workspace.py), [retrieval](../../core/providers/knowledge.py), and [validation](../../core/governance/validation.py).
CLI discovery returned `ai-sdlc: command not found` in the current shell.
No connector operation or business execution was needed for this folder recommendation.

Only this review and the preserved user input were added.
No existing evidence, knowledge record, source identity, or runtime behavior was changed.
Unrelated work remains outside this change.
Automated checks passed for 13 local links, heading anchors, whitespace, and final newlines.
Runtime tests and wheel builds were not run for this documentation-only recommendation.

## Writing checks

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
