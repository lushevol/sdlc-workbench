# Context registry

`workspace.yaml` identifies the registry files.
Registries describe assets and relationships.
They do not verify source claims or actual execution.
Keep existing repositories, documents, and engines in their current locations.

| File | Entries |
| --- | --- |
| `repositories.yaml` | Repository identities, classification, responsibility, ownership, and provided or consumed contracts. |
| `services.yaml` | Logical services and their implementation or deployment repositories. |
| `capabilities.yaml` | Business capabilities and their service or repository links. |
| `contracts.yaml` | Interface contracts with exact source repository, path, and revision. |
| `sources.yaml` | Technical and context source locations. |
| `tools.yaml` | Executable resources with providers, configuration, environments, and operation grants. |

Each file contains `schema_version: 1` and a list under its category name.
The envelope version stays unchanged for compatibility.
Each entry requires a unique `id` within its category.
IDs use letters, digits, dots, underscores, or hyphens.
They start with a letter or digit and contain at most 80 characters.
Lists must contain unique values.

All declared cross references must identify registered entries.
The adjacent `*.schema.json` files describe the supported structure.
The loader also checks IDs, unique lists, cross references, and the restrictions below.

Old workspace files can omit `contracts` and `sources` registry paths.
Old repository, service, and capability entries can contain only an `id`.
The loader continues to accept the legacy service field `repository_id`.
New catalogs start empty.

## Repositories, services, and capabilities

Repository `primary_type` accepts `frontend`, `backend`, `library`, `integration`, `data`, `deployment`, or `testing`.
Use `responsibility` for a short description or `responsibilities` for a list.
Use `ownership: {team: ..., contact: ...}` for responsibility contacts.
Both ownership fields are optional.

Repository and service entries can declare `provides_contract_ids` and `consumes_contract_ids`.
These lists describe authored relationships.
They do not prove runtime calls.

Services can declare `repository_ids` and `deployment_repository_ids`.
Several repositories can implement one service.
Several services can share one repository.
The legacy `repository_id` is an additional repository reference when both forms appear.
Capabilities can declare `service_ids` and `repository_ids`.
Repositories, services, capabilities, and contracts can declare `source_ids` for registered provenance sources.

Optional `name`, `description`, and `location` fields contain nonempty text.
Locations can identify external assets.
Registration does not copy those assets or check their availability.

## Contracts

A contract requires `id`, `type`, `status`, and `source`.
Contract `type` accepts `http`, `graphql`, `messaging`, `ui`, `data`, or `deployment`.
Contract `status` accepts `documented` or `candidate`.
Use this source shape:

```yaml
source:
  repository_id: registered-repository
  path: contracts/interface.yaml
  revision: '1111111111111111111111111111111111111111'
```

The path must identify a relative file inside that repository.
The revision must contain a full Git commit ID with 40 or 64 hexadecimal characters.
Branches, tags, and abbreviated revisions do not identify an exact contract source.
The example commit ID is an invented placeholder.
The loader does not read that file or resolve the revision.

`documented` records an authored source declaration.
It does not establish actual execution or verification.

Candidate contracts require a nonempty `documentation_gap`.
Candidate `verified_claims` must be absent or empty.
Other contracts can contain authored `verified_claims` text.
The registry does not verify those claims.
Contracts can also declare `service_ids` and `repository_ids`.

## Sources

A source requires `id`, `type`, `purpose`, and `location`.
Source `type` accepts `git`, `filesystem`, `xwiki`, `confluence`, `ado`, `email`, or `teams`.
Source `purpose` accepts `technical` or `context`.
Technical sources can identify code, schemas, specifications, and configuration.
Context sources can identify requirements, decisions, discussions, and messages.
Sources can declare an optional `repository_id`, `revision`, and `ownership`.

`read_only` defaults to `true` when omitted.
Confluence sources must explicitly declare `read_only: true`.
The source catalog rejects provider configuration and operation grants.
Source metadata never creates an executable resource.
Keep credentials outside registry files.

## Tools

Tool entries follow the existing resource contract.
Register an external requirement directory through `knowledge.local`:

```yaml
schema_version: 1
tools:
  - id: business-requirements
    kind: knowledge
    provider: knowledge.local
    environment: local
    config:
      path: /absolute/path/to/existing/requirements
    allowed_operations: [list, search, read]
```

On Windows, use a quoted path such as `C:/Projects/ExistingSystem/requirements`.
Use separate tool entries for knowledge, repositories, and the E2E engine.
Configured test suites use named command arrays through `testing.command`.
Robot suites use named repository-relative paths through `testing.robot`.
Read [Robot testing](../docs/ROBOT_TESTING.md) for the separate interpreter and retained report contract.
The runtime merges tools with inline `resources` entries.
Duplicate resource IDs fail startup.

Status shows catalog identities and counts.
It omits tool connection configuration.

See [the illustrative registry](examples/README.md) for linked examples.
Those examples contain fictional settlement metadata.
