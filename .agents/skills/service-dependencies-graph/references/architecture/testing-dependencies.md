# Testing dependency declarations

`extract_testing_dependencies.py` operates only when its caller explicitly selects a testing repository.
The registry can establish this scope through `primary_type: testing`.
Python syntax alone does not establish testing scope.
Every generated node and relationship retains `dependency_scope=TESTING`.
Static declarations do not establish test execution, passing assertions, or business behavior.

## Python clients

The extractor reads Python syntax without importing or executing repository code.
Imported `requests` functions and directly constructed `Session` receivers can establish HTTP declarations.
Imported aliases and unique session fields remain supported.
Reassigned imports, shadowed receivers, and uncertain control-flow bindings cannot establish client identity.

Inline literal HTTP destinations retain sanitized transport paths.
Authentication information, query strings, fragments, and marked credential paths are omitted.
Variable destinations remain symbolic.
The extractor does not read configuration values or follow environment bindings.
Evidence includes safe call signatures instead of complete argument lists.

Explicitly imported `psycopg2.connect` and `psycopg.connect` calls establish database client declarations.
Explicitly imported `Minio` construction establishes an object storage client declaration.
Connection arguments, endpoint configuration, usernames, passwords, and keys are omitted.
These declarations retain unknown destination identities.
MinIO construction does not establish object transfers or network calls.

Namespace URLs, fixture strings, comments, and untyped method names do not establish dependencies.
Unsupported Python syntax retains a parse diagnostic.
Arbitrary wrappers, generated code, general receiver typing, and callback execution remain outside the supported analysis.

## Robot imports

Robot Settings sections can establish library and resource imports.
The extractor retains the first import target and omits library constructor arguments.
An exact included local file can establish a source-backed import relationship.
Missing files, dynamic paths, and external library identities remain unresolved boundaries.

Robot keyword bodies do not establish HTTP requests through this extractor.
Imported resources do not prove that their keywords execute.
Dynamic import keywords and variable expansion require separate supported analysis.
Robot variables and fixture URLs do not create API calls.

## Validation

Focused tests check imported clients, sessions, scope boundaries, credentials, Robot imports, and source exclusions.
They also check namespace strings, shadowed identities, dynamic destinations, and parse diagnostics.

```sh
python -m unittest discover -s .agents/skills/service-dependencies-graph/tests -p test_testing_dependencies.py -v
```
