# Web source modules and exported symbols

The skill extracts static ES value imports within each repository.
It keeps package imports separate from source module imports.
Imports establish source dependencies. They do not establish execution, invocation, or compiler success.

## Supported identities

Relative paths resolve against the importing file.
Extensionless imports require one matching source file or directory index.
Supported source extensions are `.ts`, `.tsx`, `.js`, and `.jsx`.
Multiple matching files remain ambiguous.
Imports cannot cross the analyzed repository boundary.

Local `tsconfig.json` and `jsconfig.json` declarations supply `baseUrl` and `paths` aliases.
The reader supports JSON comments, trailing commas, and local configuration inheritance.
External configuration packages remain unsupported.
Alias alternatives require one unique source target.
The extractor does not select build profiles or execute a compiler.

Named exports, default exports, aliases, and local re-exports retain exact source identities.
Barrel exports resolve to their original value declaration.
Conflicting star exports remain ambiguous.
Cycles and chains beyond 128 resolution steps cannot establish a unique symbol.
Namespace imports retain module evidence without inventing individual symbol usage.

## Canonical relationships

| Relationship | Meaning | Required evidence |
| --- | --- | --- |
| `IMPORTS_SOURCE` | A static declaration imports or re-exports a local module. | Import declaration and exact provider source. |
| `IMPORTS_SYMBOL` | An import binding identifies one exported value declaration. | Import declaration and original value declaration. |
| `EXPORTS_SYMBOL` | A source module declares an exported value. | Original exported value declaration. |

Existing component nodes are reused only when their exact source path matches.
Directory scopes cannot establish exact component identity.
Other source files receive `COMPONENT` nodes with `component_kind=SOURCE_MODULE`.
Exported values receive `COMPONENT` nodes with `component_kind=EXPORTED_SYMBOL`.
The symbol kind identifies the supported declaration form.
It does not prove that callers invoke the value.

Resolved joins retain their rule and evidence from both endpoints.
Merged imports retain all module spellings, bindings, and declaration kinds.
Source identities include repository and path. Equal basenames cannot merge different files.
Existing parent relationships remain unchanged.

## Exclusions and limits

Explicit type-only imports and exports do not create runtime value edges.
Known exported interfaces and type aliases also remain excluded from value joins.
Test files, test directories, and declaration files remain excluded.
Package imports use the separate npm extractor.

Dynamic `import()` and CommonJS `require()` remain explicit unsupported declarations.
Computed expressions, asset loaders, compiler plugins, and arbitrary generated module resolution remain unsupported.
The extractor does not inspect excluded packages to resolve aliases.

The declaration ledger records extracted, unresolved, and excluded items.
Statistics retain source counts, import counts, symbol counts, limits, and disposition counts.
Unresolved symbols remain separate from resolved module imports.
Inspect the consumer and provider evidence before reporting reuse.

## Validation

Run `test_web_structure.py` for source and symbol extraction regressions.
The tests cover aliases, barrels, collisions, cycles, exclusions, source boundaries, and evidence retention.
Run viewer regressions after changing relationship categories or inspection fields.
Rebuild the graph through the skill after integration changes.
