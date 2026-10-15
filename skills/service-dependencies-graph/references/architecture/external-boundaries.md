# External boundary review

Review each protocol independently, then join identities through explicit evidence.
Keep raw values, normalized paths, source revision/fingerprint, owner component, and unresolved expressions.
Static, configuration, deployment, and runtime evidence describe different facts.

## HTTP and gateway routes

Retain method, path, authority, declared service alias, and supporting configuration chain.
Do not remove gateway prefixes without an explicit route or rewrite.
Resolve only compatible paths and methods with sufficient provider identity.
External authorities must survive normalization.

Nginx `location`, `rewrite`, and `proxy_pass` declarations require supported static parsing.
Jinja expressions and dynamic upstream names remain unresolved unless supplied bindings establish concrete identities.
IP-only upstreams cannot establish a repository service identity through address similarity.
A route template does not establish its active deployment.

GraphQL transport ownership does not establish field-level handlers.
WebSocket route resolution requires the supported upgrade configuration and exact rewritten endpoint.
Neither establishes a live connection.

## Messaging and data

Record topic direction only when a supported sender, listener, or route supplies it.
Keep cluster and environment identity separate from topic names.
Configuration-only values do not establish message flow.
Database access requires runtime client evidence.

Shared object names require matching datasource/schema identity before cross-repository dependency claims.
Never retain credentials or unredacted connection strings.

File API calls can identify repository-scoped file boundaries with unknown path identity.
They do not establish shared files or SFTP connections.
Selected SDK calls can identify external boundaries while provider identity remains unresolved.

## Packages and configuration

Direct npm and Maven declarations retain coordinates and scopes.
Exact local publishers can establish build dependency joins.
External packages remain external build boundaries.
Build dependencies do not establish runtime calls or compatible installed versions.

Exact ES value imports can establish `IMPORTS_MODULE` edges to in-scope npm producers.
These `MODULE` dependencies retain both source declarations and exclude type-only imports.
Duplicate producers remain ambiguous.
They do not establish compiler, bundler, version, deployment, or runtime behavior.

Profiles, environment references, deployment descriptors, and import maps can supply configuration variants.
They cannot select the active environment without observation.
Documentation-only relationships remain inferred.
Missing evidence cannot establish dependency absence.

Use [implemented limits](automated-analysis.md) and the [graph contract](graph-contract.md) before changing these rules.
