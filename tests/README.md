---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Runtime test contract

These tests protect capabilities that the Workbench currently ships.
They check observable results, retained records, external interfaces, and shipped contracts.
They do not establish business behavior coverage.

| Current consumer | Tests | Observable checks |
| --- | --- | --- |
| Workspace users | [Workspace layout](test_workspace_layout.py), [local configuration](test_workspace_v2.py) | Clean initialization, shipped guides, excluded runtime source, local paths, validation results, and source preservation. |
| Registry readers | [Catalogs](test_catalogs.py) | Valid identities, references, exact revisions, source declarations, and separate execution grants. |
| Knowledge reviewers | [Knowledge validation](test_knowledge_governance.py) | Required fields, measurable criteria, snapshot hashes, audit records, publication gates, and read-only validation. |
| Tool callers | [Core runtime](test_core.py) | Granted operations, argument rejection, retained outcomes, evidence hashes, and filesystem boundaries. |
| Provider maintainers | [Providers](test_providers.py) | Source reads, Git operations, retained command output, timeouts, log matches, bounded queries, and registry responses. |
| Agent clients | [Interfaces](test_interfaces.py) | CLI outcomes, MCP protocol handling and shared operation results. |

The fixtures in [support.py](support.py) supply isolated resources for runtime tests.
They belong to the test suite and do not create product demonstrations.

## Removed duplication

Seven test methods were removed or consolidated.
Catalog tests retain the metadata execution boundary and catalog-count assertions from the removed layout test.
The catalog reference and identity tests replace the narrower layout regression.
The clean initialization test retains the removed guide and ignore-rule checks.
Two demo tests and two dashboard tests were removed with those product features.

The clean initialization test also rejects copied runtime modules, `src/`, and `tests/` in generated workspaces.
This check protects the boundary between the source distribution and generated workspace data.

## Stronger checks

The required-field test now uses a valid document body before removing one field.
The identity test now preserves complete catalogs before adding one invalid record.
Both tests first check that their unchanged fixtures are valid.
These changes prevent unrelated validation errors from satisfying the assertions.

Owner: Workbench maintainer. The named owner is unknown.
Next action: require a current consumer and observable assertion for each new test.
