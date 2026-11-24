# GraphQL source documents

The adapter records imported `gql` tagged templates through a TypeScript AST.
Supported direct providers are `@apollo/client`, `@apollo/client/core`, `graphql-tag`, and `graphql-request`.
Named import aliases and the `graphql-tag` default import retain their source identities.
Shadowed bindings, comments, tests, and type-only imports do not produce document facts.

`GRAPHQL_DOCUMENT` records describe source declarations.
`DECLARES_GRAPHQL_DOCUMENT` links each document to its source module.
`SELECTS_GRAPHQL_FIELD` links literal documents to sanitized `GRAPHQL_FIELD_SELECTION` records.
Selection paths describe document shape, including response aliases.
Arguments, variable defaults, and literal values stay excluded.

Template substitutions retain partial document metadata and an unresolved diagnostic.
The adapter does not guess substituted operation names, field names, arguments, or document structure.
Other imported `gql` bindings retain candidate documents with unresolved tag providers.
These candidates do not establish GraphQL library semantics.

Fragment names remain visible.
The adapter does not expand fragment spreads into field selections.
Limits bound source size, token count, selection count, and nesting depth.
Unsupported documents retain explicit ledger dispositions.

Document declarations do not establish API invocation, transport, provider identity, or schema validity.
Existing valid named-operation and transport facts keep their identities.
The legacy operation-name matcher excludes template substitutions from named operations.

The viewer includes documents in the API family and Outbound APIs view.
Declaration and selection labels remain separate from API call labels.
These repository-local declarations do not create resolved links between repositories.
