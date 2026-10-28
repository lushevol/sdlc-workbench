# Architecture instructions and investigated relationships

Use architecture context when a user supplies initial roles, layers, or relationship hints.
Follow [instruction investigation](initial-instruction-investigation.md) before creating the final graph.
Keep supplied intent separate from source facts, resolved provider matches, and runtime verification.
Do not encode project names or project-specific routing rules in skill tools.

## Input and publication

The normal build reads `relationships/service-dependencies/architecture-context.json` when that file exists.
Use `build --context PATH` to select another workspace-local file.
An explicitly selected file must exist.
Use schema version `1.1.0` for investigated relationships integrated into the graph.
Version `1.0.0` remains supported for legacy annotations.
The skill validates the contract in `tools/architecture_context.py`.
Unknown fields, unsupported versions, duplicate IDs, and unknown references stop publication.
Paths must remain within the workspace.
Each cited file must match its declared SHA-256.

The build captures input and evidence bytes before extraction.
It compares input and evidence again before publication.
Changed evidence stops publication and preserves the previous bundle.
These checks do not authenticate the person who supplied a clarification.

Published artifacts include:

- `architecture-context.json`: exact applied input bytes.
- `architecture-context-provenance.json`: input locator, checksum, source identities, and explicit limits.
- `architecture-context-sources/`: exact cited evidence bytes.

The manifest records each artifact checksum.
Queries validate saved input, references, provenance, and source snapshots.
Portable queries do not require access to the original evidence files.
The `coverage` operation returns architecture context separately from canonical extraction coverage.
Its context freshness compares current input and evidence bytes with saved fingerprints.
Missing or changed files produce `STALE` context freshness.
Missing local files do not invalidate the captured bundle.

## Contract

All top-level arrays are required.
Use empty arrays when no item applies.
Every record requires a unique `id` across the complete document.
IDs start with a letter and contain letters, digits, periods, underscores, colons, or hyphens.
Every claim record requires at least one known `source_ids` entry.

| Array | Required record fields | Meaning |
| --- | --- | --- |
| `sources` | `id`, `path`, `sha256`, `revision`, `kind` | Workspace-local evidence identity and exact bytes. |
| `layers` | `id`, `label`, `order`, `description`, `source_ids` | Supplied hierarchy with unique positive order numbers. |
| `subjects` | `id`, `repository`, `label`, `role`, `layer_id`, `status`, `description`, `source_ids` | Supplied responsibility or explicit boundary. |
| `relationships` | `id`, `source`, `target`, `kind`, `description`, `source_ids` | Directed relationship between known subject IDs. |
| `notes` | `id`, `subject_ids`, `description`, `source_ids` | Clarification, conflict, or limit for known subjects. |

Source `kind` accepts `USER_CLARIFICATION` or `SOURCE_REVIEW`.
Source `revision` identifies the evidence version.
Use the actual revision or recorded clarification identifier.
Never substitute the Workbench revision for a business repository revision.
Source-review evidence can document code agreement, conflicts, and missing support.
It does not establish runtime verification.

Subject `repository` accepts an exact captured `repo:` ID or `null`.
The build rejects unknown repository IDs.
Subject `layer_id` accepts a known layer ID or `null`.
Subject `status` accepts `USER_REPORTED` or `OUT_OF_SCOPE`.
Use `OUT_OF_SCOPE` for boundaries deliberately excluded from the present investigation.
A subject without a repository binding does not establish a discovered provider.
Relationship `kind` describes the supplied relationship in stable project terminology.
It does not reuse canonical resolution status.
An empty note `subject_ids` array describes the complete context.

## Investigated contract, version 1.1.0

Version `1.1.0` requires the preceding arrays and an `investigations` array.
Each relationship requires exactly one investigation.
Each subject can provide `node_id` to bind an exact existing canonical node.
The node must belong to the subject's declared repository.
Without an explicit binding, a unique repository root supplies the anchor.
Unbound subjects become explicit `ARCHITECTURE_BOUNDARY` nodes, not discovered providers.

| Investigation field | Meaning |
| --- | --- |
| `id`, `relationship_id` | Unique investigation identity and its relationship reference. |
| `status` | `SUPPORTED`, `INFERRED`, `CONFLICTED`, `UNVERIFIED`, or `OUT_OF_SCOPE`. |
| `family` | `api`, `data`, `shared`, `configuration`, or `structure`. |
| `rationale` | Conclusion, reasoning, and material limits from source investigation. |
| `source_refs` | Exact citations: `source_id`, `line`, and `end_line`. |
| `canonical_edge_ids` | Existing edges to enrich instead of duplicating extracted facts. |

The build checks source hashes and captured line ranges.
Supported relationships require source-review evidence covering each bound repository endpoint.
Reused edges must match the directed endpoints and retain their original assertion and resolution fields.
These checks establish structural consistency. The agent remains responsible for the source interpretation.
Claims without sufficient evidence retain an uncertain assessment.

The graph stores review metadata in `properties.architecture_claims` on affected edges.
New reviewed edges use `REVIEWED_RELATIONSHIP` and retain the specific relationship kind in their properties.
Only `SUPPORTED` new edges use assertion status `CONFIRMED`.
New reviewed edges retain provider status `UNRESOLVED`, including supported source declarations.
Source support does not establish active deployment or runtime behavior.
Existing matched edges retain their separate provider resolution evidence.

The main architecture diagram includes investigated relationships and ordered layer lanes.
Labels and filters distinguish investigation results from provider matching.
Inspectors show rationales, source ranges, revisions, and hashes.
Queries and repository projections retain the integrated canonical relationships.
The original instructions remain available in a collapsed evidence section below the graph.

Source changes make freshness stale.
Reinvestigate changed claims before updating source hashes or regenerating their final dispositions.
The deterministic build does not perform AI reasoning or refresh investigation conclusions.

## Legacy annotations, version 1.0.0

For version `1.0.0`, the viewer displays supplied context in a separate `USER_REPORTED` section.
Layers follow their supplied order.
Subjects outside those layers remain visible below them.
Relationships retain source-to-target direction and evidence references.
Notes preserve conflicts and boundaries.
Search and repository filters apply only to this context section.
Adjacent subjects remain visible when a relationship matches the selected repository.
The source panel links captured bytes and original workspace files.

Legacy annotations never add canonical nodes or edges.
They never create highest-priority resolved repository links.
They never override extracted identities, configuration, or unresolved boundaries.
Use source extraction or a separate source investigation to establish those facts.
