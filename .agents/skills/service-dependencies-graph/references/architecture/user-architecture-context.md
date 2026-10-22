# User architecture clarifications

Use architecture context when a user explains roles, layers, or relationships that static extraction cannot establish.
Keep supplied intent separate from source facts, resolved provider matches, and runtime verification.
Do not encode project names or project-specific routing rules in skill tools.

## Input and publication

The normal build reads `relationships/service-dependencies/architecture-context.json` when that file exists.
Use `build --context PATH` to select another workspace-local file.
An explicitly selected file must exist.
The input uses schema version `1.0.0`.
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

## Viewer and interpretation

The viewer displays supplied context in a separate `USER_REPORTED` section.
Layers follow their supplied order.
Subjects outside those layers remain visible below them.
Relationships retain source-to-target direction and evidence references.
Notes preserve conflicts and boundaries.
Search and repository filters apply only to this context section.
Adjacent subjects remain visible when a relationship matches the selected repository.
The source panel links captured bytes and original workspace files.

Annotations never add canonical nodes or edges.
They never create highest-priority resolved repository links.
They never override extracted identities, configuration, or unresolved boundaries.
Use source extraction or a separate source investigation to establish those facts.
