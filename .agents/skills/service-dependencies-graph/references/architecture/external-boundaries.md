# Repository external boundary extraction

Review each protocol independently, then join identities through explicit evidence.
Keep raw values, normalized paths, revision/fingerprint, owner component, and unresolved expressions.
Static, configuration, deployment, and runtime evidence describe different facts.
One cannot silently replace another.

## REST, HTTP, and gateways

Inspect supported Spring mappings, Feign clients, Java URI calls, frontend clients, and proxy declarations.
Retain method, path, authority, service alias, and supporting configuration chain.
Do not remove a gateway prefix without an explicit route or rewrite.
External authorities must survive normalization.

Supported nginx parsing retains locations, rewrites, proxy targets, and upstream declarations.
Proxy URI prefix replacement preserves the unmatched request suffix.
Dynamic Jinja expressions remain unresolved without concrete bindings.
IP-only identities and multiple/empty upstream pools cannot establish unique repository providers.

A route template does not establish its active deployment.
Timeouts, retries, headers, and request/response types require direct evidence when relevant.
Generated contract files cannot replace a bound runtime caller or provider.
Unsupported rewrite chains remain explicit limits.

## GraphQL and WebSocket

Inspect selected client endpoints and annotated resolver fields.
Keep operation names, transport, endpoint, and field-level handlers distinct.
Transport ownership cannot establish resolver invocation.
Schema-only fields and generated types remain insufficient alone.

Supported WebSocket resolution requires static paths, upgrade configuration, and declared upstream identity.
Unknown providers and dynamic endpoints remain unresolved.
Neither declarations nor static joins establish live connections.
Do not merge distinct methods or protocols by matching labels.

## Messaging and files

Record message direction only when supported senders, listeners, or routes supply it.
Keep topic names separate from cluster and environment identity.
Configuration-only values cannot establish message flow.
Consumer groups do not identify providers.

Conditional or dynamic endpoints require explicit variants or unresolved records.
File API calls can identify repository-scoped file boundaries with unknown path identity.
They cannot establish shared files or SFTP connections.
A package dependency alone cannot establish an instantiated transfer client.

## Database and platforms

Runtime clients and queries determine supported data-access claims.
Datasource configuration identifies connection or migration scope without table-level execution proof.
Shared table names require matching datasource/schema identity before cross-repository joins.
Never retain credentials or unredacted connection strings.

Selected SDK calls can identify external boundaries with unresolved provider identities.
Generic generated stubs, tracing configuration, and platform names remain insufficient alone.
An external data-lake name cannot establish Elasticsearch or another engine.
Keep inferred platform findings explicit.

## MFE and internal packages

Literal remote imports and exact published module names can establish composition joins.
Import maps remain configuration evidence; observed browser traces supply separate runtime evidence.
Direct npm/Maven declarations retain coordinates and scopes.
Exact local publishers can establish build dependencies.

ES value imports can establish `IMPORTS_MODULE` edges to in-scope npm producers.
These `MODULE` edges retain evidence from both sides and exclude type-only imports.
Namespaces control scanning and cannot prove aliases.
Missing providers remain unresolved; duplicate producers remain ambiguous.

Build and module edges do not establish compiler, bundler, version, deployment, or runtime behavior.
Package boundaries remain distinct from API targets in the viewer.
Browser events, storage keys, and interoperability contracts require dedicated support or direct source review.
Do not invent their graph relationships from names.

## Configuration and failure evidence

Inspect profiles, environment references, deployment descriptors, import maps, and CI configuration when they bind identities.
These can establish configuration variants without selecting the active environment.
Secret keys remain references, never values.
Unknown values and conflicting routes remain diagnostics or unresolved boundaries.

Documentation-only relationships remain inferred.
Missing evidence cannot establish dependency absence.
Read [implemented limits](automated-analysis.md) and the [graph contract](graph-contract.md) before extending extraction.
