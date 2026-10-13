# Provider plugin contract

A provider implements operations for one resource kind.
A workspace registers each resource instance separately.
A plugin can supply a connector through this provider interface.

## Package interface

Register a factory in the `ai_sdlc_workbench.providers` Python entry point group.
The entry point name must equal the provider ID.
The workspace `plugins` list enables that name explicitly.

The factory returns an object with these members:

```python
id: str
version: str
resource_kind: str
operations: dict[str, Operation]

def invoke(operation: str, resource: Resource,
           arguments: dict, context: Context) -> dict:
    ...
```

Import `Operation`, `Resource`, and `Context` from `ai_sdlc_workbench.models`.
The [example plugin](examples/hello-plugin/hello_provider.py) shows the interface.

## Operation contract

Each operation declares its name, description, input schema, and `mutating` flag.
Mark operations that can change external state as mutating.
The flag describes the operation; `allowed_operations` supplies the execution grant.
The workbench checks the grant and arguments before invoking a provider.
It retains denied calls and invalid arguments without invoking that provider.

Input schemas use objects with named properties and explicit unknown-field rules.
The validator supports types, required fields, enums, object properties, array items, and length or numeric bounds.
It does not implement the complete JSON Schema specification.
The registry rejects unsupported schema keywords before it loads resource operations.

Successful provider results use `status="SUCCEEDED"`.
Failures can use `FAILED`, `ERROR`, or `TIMEOUT`.
Result values must contain JSON data.
Do not return credential values or raw authentication headers.

## Resource contract

The resource supplies an ID, kind, provider ID, environment, configuration, and operation grants.
Provider configuration defines connection details and backend options.
Use environment variable names for credential references.
Resource configuration does not go into the public status response.
Action records retain its hash instead.

The provider owns validation of its configuration.
The workbench validates the shared resource structure and provider compatibility at startup.

## Execution context

`context.workspace_root` identifies the workspace directory.
`context.run_dir` identifies the action evidence directory.
`context.timeout_seconds` supplies the configured operation timeout.

Use `context.resolve_path(value)` for a registered resource path.
Use `context.confined_path(base, relative)` for a path within that resource.
Write retained output files into `context.run_dir`.
The workbench records their paths, sizes, and SHA256 hashes after execution.

The provider must implement its timeout and recovery behavior.
The workbench cannot stop arbitrary Python plugin code.
No remote runner, cancellation protocol, or rollback contract exists in this MVP.

## Evidence boundary

Retain exact source locators and revisions when the backend supplies them.
Keep observed results separate from inferred conclusions.
An operation result does not approve intent or establish behavior verification.

Skills describe the analysis procedure that uses these results.
The bundled skills remain independent of specific provider IDs.
Shared workspace procedures use `skills/<skill-id>/SKILL.md`.
Provider entry points do not automatically register skills.
