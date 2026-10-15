# Workbench registry proposal mapping

Read the destination workspace's `registry/README.md` and adjacent `*.schema.json` files before drafting catalogs.
The installed loader checks additional cross-reference and candidate restrictions.
Do not extend the runtime schema through onboarding output.

## Identity and field mapping

| Staged file | Supported fields and responsibility |
| --- | --- |
| `repositories.proposed.yaml` | Source identity; `primary_type`, responsibility, ownership, optional location, source IDs, and contract IDs. |
| `services.proposed.yaml` | Logical application identity; `repository_ids`, `deployment_repository_ids`, source IDs, and contract IDs. |
| `capabilities.proposed.yaml` | Business identity; `service_ids`, `repository_ids`, source IDs, and responsibility. |
| `contracts.proposed.yaml` | Interface identity; type, status, exact source locator, and supported asset references. |
| `sources.proposed.yaml` | Provenance identity; type, purpose, location, revision, repository ID, and read-only declaration. |
| `components.proposed.yaml` | Skill-local functional mapping; no canonical component catalog currently exists. |

Each catalog has exactly two envelope keys: integer `schema_version: 1` and its category list.
Use `repositories`, `services`, `capabilities`, `contracts`, or `sources` as the category.
Each entry needs a unique ID.
IDs contain at most 80 letters, digits, dots, underscores, or hyphens.
The first character must be a letter or digit.
All cross references must resolve across the proposed and existing declarations.
Several services can share one repository.
One service can use several repositories.

Use `ownership.team` and `ownership.contact` only when known.
Omit unknown optional fields and describe their review needs in the assessment.
Do not insert `review_required` as an owner identity.
Do not add `status: proposed`, `evidence_ids`, build commands, or component structures to catalog entries.
Keep those staging details in the assessment or structured claims.
Keep portable metadata in catalogs and machine paths in ignored `workspace.local.yaml` when possible.

Repository `primary_type` accepts `frontend`, `backend`, `library`, `integration`, `data`, `deployment`, or `testing`.
Repository and service links use `provides_contract_ids` and `consumes_contract_ids`.
Use service `repository_ids` for new records; `repository_id` exists only for legacy compatibility.
A catalog declaration does not prove deployment, call direction, or successful execution.

## Contract and source rules

Contract types are `http`, `graphql`, `messaging`, `ui`, `data`, and `deployment`.
A contract requires `id`, `type`, `status`, and `source`.
Its source requires `repository_id`, a relative file `path`, and a full hexadecimal Git `revision`.
Use a 40-character or 64-character commit ID from the inspected checkout.
Without an exact revision, retain the interface claim in the assessment instead of producing a catalog record.

Contract status accepts `documented` or `candidate`.
`documented` means an interface has a documented source; it does not mean approved or executed.
A candidate needs `documentation_gap` and must omit `verified_claims` or leave that list empty.
Retain consumer and provider citations separately before confirming a relationship across repositories.
A shared interface name alone does not establish connectivity.

Source types are `git`, `filesystem`, `xwiki`, `confluence`, `ado`, `email`, and `teams`.
A source requires `id`, `type`, `purpose`, and `location`.
Use `purpose: technical` for implementation evidence and `purpose: context` for business intent.
Use the actual access method; a local export is a filesystem source.
Sources default to read-only; Confluence records require explicit `read_only: true`.
Do not register credentials or tool execution grants as source metadata.

## Examples and validation

Use the destination workspace's `registry/examples/` for supported linked examples.
Those examples contain fictional assets and cannot establish discovered identities or evidence.
Keep catalog examples there instead of maintaining another schema example in this skill.

Initialize an isolated workspace with `ai-sdlc init` using its documented CLI arguments.
Place proposed declarations and required existing metadata into that workspace's catalogs.
Leave its executable tools empty.
Run `ai-sdlc --workspace <isolated-workspace> validate`.
Record missing references and schema failures in the assessment.
Do not change the live catalogs to make a proposal pass.

## Component proposals and later ingestion

`components.proposed.yaml` is a skill-local artifact with `schema_version: "1.0"`, `repository_id`, and `components`.
Each component uses a local `id`, responsibility, entrypoint paths, path patterns, contract references, tests, and claim IDs.
Use only inspected relationships and identify inferences in the referenced claims.
This format has no Workbench runtime loader and grants no canonical identity.
The evidence validator checks referenced claims; it does not validate this YAML artifact.

For an authorized profile, use `knowledge/templates/repository-profile.md` and the shipped knowledge schema.
Keep detailed component evidence in the body with exact source citations.
Preserve raw provenance before creating governed candidates.
Follow ingestion and governance procedures for candidate records, audit events, and required human review.
