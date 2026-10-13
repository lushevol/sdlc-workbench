# Context registry

`workspace.yaml` identifies the four registry files.
Registries declare resources and locations; their presence does not verify a relationship or source claim.
Keep existing repositories, documents, and engines in their current locations.

| File | Entries |
| --- | --- |
| `repositories.yaml` | Repository identity, name, location, and optional revision metadata. |
| `services.yaml` | Service identity, name, location, and optional `repository_id`. |
| `capabilities.yaml` | Capability identity, domain, source references, and optional `service_ids`. |
| `tools.yaml` | Executable resource records with provider, configuration, environment, and operation grants. |

Each file contains `schema_version: 1` and a list under its category name.
Each entry requires a unique `id` within its category.
When present, `repository_id` and `service_ids` must refer to registered entries.
Repository and service entries can contain `name` and `location` strings.
Locations can identify external assets; registering them does not copy those assets.

Tool entries follow the existing resource contract.
For example, register an external requirement directory through `knowledge.local`:

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
Use separate tool entries for domain knowledge, architecture sources, repositories, and the E2E engine.
Configured test suites use named command arrays through `testing.command`.
Keep credentials outside these files.

The runtime loads tools from this registry and any inline `resources` entries.
Duplicate resource IDs fail startup.
The status response shows catalog identities and counts; it omits tool connection configuration.
