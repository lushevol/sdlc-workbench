# Java structure and configuration extraction

`extract_java_structure.py` reads declared Maven source roots through the shared source inventory.
It retains every parsed Java type, including configuration classes, implementation classes, records, and nested types.
It preserves existing class identities where available.
Additional type nodes retain exact source locations.

## Type relationships

`DEPENDS_ON_TYPE` records fields, parameters, and return types with exact local type identities.
`EXTENDS_TYPE` and `IMPLEMENTS_TYPE` record declared inheritance.
Generic arguments remain type dependencies.
They do not become inherited types.

`INJECTS` records explicit injection annotations and supported Spring constructor declarations.
Supported Lombok constructor declarations require the imported annotation and an eligible uninitialized field.
These edges establish injection declarations, not instantiated beans.

`CALLS_COMPONENT` records direct calls through a statically declared local receiver type.
Local variables, parameters, lambda parameters, and explicit `this` access retain lexical scope.
Calls to interfaces retain the interface as the target.
Multiple local implementations produce a diagnostic.
The extractor never selects a runtime implementation.

## Configuration relationships

`CONFIGURATION_SOURCE` identifies a source document and its declared profile context.
`CONFIGURATION_KEY` identifies a logical property key within one repository.
Spring relaxed punctuation supports matching camel case, hyphens, and underscores.
Profiles remain unselected.
Equal keys across profiles do not establish equal runtime values.

`DECLARES_CONFIG` retains YAML and properties key declarations.
`REFERENCES_CONFIG` records static placeholder key references.
`BINDS_CONFIG` records imported `ConfigurationProperties` fields and bounded nested property types.
`READS_CONFIG` records supported property getter calls, `Value` annotations, environment reads, and property conditions.

Generated Lombok accessors require the imported `Data` or `Getter` annotation.
Custom accessors require supported direct field use within one return expression.
Dynamic environment keys and unsupported accessors produce explicit gap records.

The extractor never retains configuration scalar values, annotation defaults, credentials, or token values.
It retains property names, profile labels, type names, source locations, and sanitized declarations.
A property binding does not establish a read.
A read does not establish an endpoint destination or active runtime value.

## Evidence limits

Typed analysis excludes reflection, runtime proxies, inferred `var` types, and unbounded method chains.
It does not prove control flow or runtime execution.
Nested configuration analysis stops at cycles and a bounded depth.
Dynamic property prefixes remain unresolved.
Properties continuation syntax remains unsupported and produces a diagnostic when recognized as an unsupported declaration.
Source roots outside declared module scope remain inventory limits.

The source ledger separates extracted declarations from unresolved syntax and identities.
Its counts describe inspected source forms, not complete runtime coverage.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
