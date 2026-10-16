# Service dependency graph adoption

Date: 15 October 2026.
Scope: Import the supplied graph skill and generate evidence for local repositories.
The runtime now operates from the standalone Workbench package.
The [shared skill](../../.agents/skills/service-dependencies-graph/SKILL.md) uses installed commands and existing CLI/MCP grants.
The raw manifest retains the original skill bytes.
The [provenance record](../../core/relationships/graph/provenance.json) identifies imported sources and hashes.

## Scope and snapshot

The census contains nine repositories.
Eight repositories contribute canonical graph nodes.
The Robot test engine contributes inventory evidence only.
Static evidence does not establish deployment, passing business behavior, or complete codebase coverage.

| Field | Value |
| --- | --- |
| Generated at | `2026-10-15T03:50:11Z` |
| Graph SHA-256 | `2962d85700185c5e0f8ab116c30e39740a0bca7ccd0e4451958003a7c5069a73` |
| Manifest SHA-256 | `2c167621840e19c424eba6bad60c39558d186ac8643a10b3fbe0897ba3139c32` |
| Nodes | 961 |
| Edges | 1413 |
| Source evidence records | 1452 |
| Resolved repository relationship records | 3 |
| Unresolved boundaries | 679 |
| Source freshness | `CURRENT` |

The [machine receipt](../evidence/service-dependencies-adoption.json) retains exact revisions, dirty states, content fingerprints, and validation results.
The [viewer](../../relationships/service-dependencies/generated/relationship-viewer.html) and [coverage](../../relationships/service-dependencies/generated/analysis-coverage.json) share one manifest.
Generated bundles remain local and ignored.
Generated workspaces receive guides without Python source or live graph data.

## Repository coverage

| Repository | Kind | Status |
| --- | --- | --- |
| `nginx` | `INFRA` | `PARTIAL` |
| `single-ui-sdk-starter` | `SPRING` | `PARTIAL` |
| `ratan-auth-server` | `SPRING` | `PARTIAL` |
| `single-ui-bff` | `SPRING` | `PARTIAL` |
| `ratan-test-engine` | `UNKNOWN` | `UNSUPPORTED` |
| `mfe-base` | `WEB` | `PARTIAL` |
| `mfe-cashflow-blotter` | `WEB` | `PARTIAL` |
| `mfe-ratan-container` | `WEB` | `PARTIAL` |
| `mfe-root-config` | `WEB` | `SCANNED` |

`SCANNED` identifies extractor completion within supported syntax.
It does not establish complete semantic coverage.
`PARTIAL` records known layout, identity, template, or source limits.
Graph service nodes describe analysis roots and do not declare catalog services or deployments.

## Confirmed static evidence

Cashflow imports the exact Ratan Container package through `IMPORTS_MODULE`.
Ratan Container declares a remote Cashflow load through `LOADS_REMOTE`.
Ratan Container also declares a compatible BFF request through `CALLS_REST`.
Each resolved join retains consumer evidence, provider evidence, and a resolution rule.
The [relationship projection](../../relationships/service-dependencies/generated/repository-relationships.json) identifies canonical edges and source evidence.
Module imports do not establish installed versions, compiler resolution, or deployed connectivity.

The adaptation corrects grouped discovery, nginx extraction, and mixed Maven/npm classification.
It retains ambiguous upstream pools and missing module providers as unresolved boundaries.
Source changes during generation stop publication.
Failed validation preserves the prior snapshot.
Queries use captured, checksum-validated bytes.

## Findings and next actions

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Base module identity differs. | UI imports name `@fm/base`; base package declares `@fm/base-origin`. | The exact provider remains unresolved. | Unknown. | Supply the published module identity and supporting environment configuration. |
| Four copies lack independent Git metadata. | Both new UIs, auth, and nginx have null commits. | Fingerprints identify bytes without original revision history. | Unknown. | Supply original revisions for historical traceability. |
| Nginx templates need environment values. | Six `UNRESOLVED_NGINX_TEMPLATE` diagnostics retain source paths. | Concrete gateway joins remain unresolved. | Unknown. | Supply rendered configuration for the relevant environment. |
| SDK implementation uses a nested Maven layout. | Coverage records nested manifests and missing root Java source. | Current extraction omits runtime SDK dependencies. | Unknown. | Add module-aware extraction when an SDK boundary needs analysis. |
| Robot sources lack an extractor. | Test engine coverage is `UNSUPPORTED`. | Inventory does not establish test behavior or runtime dependencies. | Unknown. | Inspect assertions and execution through the test engine for verification. |
| Dynamic clients retain missing boundaries. | Coverage records unbound endpoints, parse errors, and unresolved URI diagnostics. | Extraction cannot establish every provider. | Unknown. | Inspect cited declarations before relying on affected paths. |

These limits prevent a claim that every dependency is known.
They do not establish repository independence.
No business source, existing approval, or service catalog identity changed.

## Acceptance checks

```gherkin
Scenario: Discover grouped repositories
  Given repositories exist under ui, services, and infra groups
  When the installed graph command builds a snapshot
  Then the census contains 9 repository records
  And the canonical graph contains 8 supported repositories

Scenario: Retain source uncertainty
  Given an imported module has no exact local package provider
  When extraction resolves module declarations
  Then the boundary resolution_status is UNRESOLVED
  And the number of invented provider joins is 0

Scenario: Preserve the prior snapshot
  Given a valid snapshot exists
  When validation fails or source bytes change during generation
  Then every prior published byte remains unchanged
```

These scenarios describe tool acceptance checks.
They do not approve business requirements.

## Validation record

The full suite passed 102 tests, including 24 graph adoption regressions.
The wheel build passed.
The [packaging check](../evidence/service-dependencies-packaging.json) initialized and built an external workspace from the wheel.
It confirmed available guides, schemas, templates, skills, and an exact module join.

Workspace validation returned `VALID`.
Coverage freshness returned `CURRENT`.
Viewer embedded JSON and JavaScript syntax checks passed.
Browser security policy blocked visual inspection of the local HTML viewer.
Visual review remains incomplete.

Retained command outputs are [tests](../evidence/service-dependencies-tests.txt), [wheel build](../evidence/service-dependencies-wheel-build.txt), and [graph build](../evidence/service-dependencies-graph-build.txt).

## Output review

```json
{
  "asd_review": "PENDING",
  "automated_check": "PASSED",
  "findings": [],
  "limitations": [
    "Automated checks do not check the complete approved dictionary or grammar rules."
  ],
  "reviewed_at": null,
  "reviewer": null,
  "standard": "ASD-STE100"
}
```
