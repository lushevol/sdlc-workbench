# ORM mappings and SQL column references

`extract_orm_details.py` adds detail without replacing the legacy database extractor.
All facts describe source declarations.
They do not establish executed queries, active profiles, or database reachability.
Entity and repository evidence retains annotation names and type signatures.
It excludes type bodies, field initializers, and default method implementations.

## JPA mappings

The extractor requires imported or qualified Jakarta or Javax persistence annotations.
It retains entity identities, table declarations, column annotations, and Spring Data repository bindings.
Repository bindings include declared method names and the imported base repository type.
Inherited CRUD methods remain framework declarations.
They do not prove application calls.

Literal annotation names and unique static string constants can establish declared names.
Schema-only table annotations retain the qualified entity name as a logical boundary.
The extractor does not convert class names to guessed physical table names.
Unnamed column annotations retain field names and an unknown physical name.
Dynamic names, ambiguous constants, and ambiguous entity imports retain diagnostics.

`ENTITY` and `COLUMN` nodes supply mapping details.
`MAPS_TO_TABLE`, `MAPS_TO_COLUMN`, and `USES_ENTITY` describe declarative relationships.
These relationships do not create `READS` or `WRITES` claims.
Unknown datasource identities remain explicit.
Table and column identities include repository and schema scope.
Unresolved logical table identities also retain source scope.

## SQL references

The extractor reads native Spring repository queries and typed JDBC template calls.
It also reads literal MyBatis mapper statements under discovered resource roots.
Standalone migration files do not establish runtime query dependencies.
Dynamic mapper branches and included fragments retain unresolved diagnostics.

Supported statements include simple `SELECT`, `INSERT`, `UPDATE`, and `DELETE` forms.
References distinguish projections, predicates, assignments, insert columns, grouping, sorting, and returned columns.
`REFERENCES_COLUMN` records these roles and the statement kind.
It does not establish column access during execution.

Native query declarations and typed JDBC calls retain their declaring method, line, arity, and deferred context.
API traces use this context to exclude column references from unrelated repository methods.
Column references and entity mappings remain declaration context within those traces.

Mapper statements require an exact Java namespace and unique method declaration for method attribution.
The graph retains both Java and XML evidence for supported bindings.
Missing declarations, overloaded methods, and unknown source owners retain explicit limits.
XML statement identifiers alone do not establish a Java method binding.

Qualified identifiers and unique table aliases can establish declared column scope.
Unqualified columns remain ambiguous when multiple tables could supply them.
Projection labels and parameter names do not create columns.
SQL wildcards retain a diagnostic instead of an invented column set.
Nested queries, unions, window expressions, table functions, and dynamic identifiers retain explicit limits.

The extractor reuses an existing unqualified table only when its name and source declaration match.
Schema-qualified references remain separate when the legacy node lacks schema identity.
Matching names do not establish a shared physical database.

## Validation

Focused regressions cover constants, unknown naming, import ambiguity, schema separation, aliases, SQL roles, and dynamic syntax.
They also check nested modules, mapper statements, JDBC receiver typing, and retained legacy metadata.

```sh
python -m unittest discover -s .agents/skills/service-dependencies-graph/tests -p test_orm_details.py -v
```
