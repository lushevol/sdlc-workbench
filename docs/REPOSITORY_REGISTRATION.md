---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
---

# Single UI repository registration

Review date: 14 October 2026.
Workbench baseline: `4d8111e`.
Scope: Three supplied source directories, their declared interfaces, local catalog registration, and starter workspace isolation.
Status: Historical inventory stage before local Git initialization.
The [initial baseline stage](INITIAL_REPOSITORY_BASELINES.md) resolves local source revision binding.

The [user request](../knowledge/raw/2026-10-14-repository-registration/user-request.txt) directs updates for the added repositories.
The registration uses inspected filesystem bytes because the copies lack independent Git metadata.
Workbench Git revisions do not identify these business sources.

## Registered context

| Repository ID | Local source | Observed responsibility |
| --- | --- | --- |
| `single-ui-bff` | `repos/services/single-ui-bff` | Authentication, session, application administration, import-map, and analytics HTTP providers. |
| `mfe-base` | `repos/ui/mfe-base` | Frontend shell, shared exports, HTTP clients, administration screens, and dynamic containers. |
| `mfe-root-config` | `repos/ui/mfe-root-config` | Application registration, import-map loading, and frontend proxy declarations. |

The catalogs contain three repositories, two declared application services, four capability groups, and three filesystem sources.
Service and capability groupings describe observed implementation scope.
They do not establish approved business intent, named ownership, or deployed service identities.
The ignored `workspace.local.yaml` maps the three repository IDs to their local directories.

No executable resources or operation grants were added.
The contract registry remains empty because its records require exact source commit IDs.

## Candidate interfaces

[The candidate architecture](../knowledge/candidates/ARCH-single-ui-contracts.md) records eight interfaces with source references.

| Candidate | Observed boundary |
| --- | --- |
| `single-ui-base-module` | Root application registration and exported base lifecycles or shared interfaces. |
| `single-ui-container-props` | Dynamic container loading and supplied properties. |
| `single-ui-shared-http` | Shared HTTP helpers, `/api` prefix, and declared timeout. |
| `single-ui-sso-token-family` | Login, validation, logout, refresh, relogin, and token exchange declarations. |
| `single-ui-importmap-admin` | Import-map data, audit, create, update, and response envelope declarations. |
| `single-ui-active-importmap` | Active import-map response shape and potential loader compatibility. |
| `single-ui-category-tile-admin` | Category and tile administration route families. |
| `single-ui-analytics-proxy` | Analytics submission declarations and gateway proxy mediation. |

The candidate separates source facts, inferred compatibility, and unresolved relationships.
The active import-map provider-to-loader relationship remains unconfirmed.
The proxy names `ratan_backend_api_gateway`; direct BFF proxy directives are comments.
No retained observation establishes successful deployed routing or business behavior.

## Evidence and unresolved findings

Thirty business source snapshots retain exact selected file bytes or line ranges.
The raw manifest also records the directory inventory and user request.
Each `sha256:` revision identifies source bytes and does not represent a Git commit.
The [source checks](evidence/repository-registration-source-checks.json) compare snapshots, hashes, candidate references, and registered IDs.

| Finding | Evidence and consequence | Owner and next action |
| --- | --- | --- |
| Missing Git provenance | [Directory inventory](../knowledge/raw/2026-10-14-repository-registration/repository-inventory.json). Contract registration cannot bind declarations to original commits. | Owner unknown. Supply original checkouts and full commits, then compare cited files. |
| Unresolved gateway routing | Retained proxy declarations name an intermediary. Matching client and provider suffixes do not establish a deployed route. | Owner unknown. Supply active gateway configuration and retained request observations. |

[The provenance finding](../knowledge/findings/FND-single-ui-source-provenance.md) keeps the missing revision evidence open.
Six new audit events record the catalog and candidate changes.
Earlier snapshots, manifest records, and audit events remain unchanged.
No reviewer identity or business approval was supplied.

## Scope and risk

Caller inspection covered initialization, catalog loading, CLI dispatch, build configuration, and affected runtime assertions.
Previous initialization copied live catalogs and knowledge records.
The source workspace now contains project records, so this behavior could copy business evidence into new workspaces.

The scaffold now selects guides, schemas, templates, and illustrative catalog examples.
Initialization creates fresh configuration, six empty catalogs, and an empty raw manifest.
Wheel scaffolds and source distributions exclude live project configuration, catalogs, knowledge records, and snapshots.
One regression checks exclusions and unchanged source bytes.

Qualitative risk is moderate because initialization and distribution contents changed.
Business repositories and runtime execution grants remain unchanged.
Owner: Workbench maintainer. The named owner is unknown.
Next action: retain the empty starter contract while adding reviewed project context separately.

## Stage acceptance

```gherkin
Scenario: Register unversioned source copies
  Given three supplied source directories without independent Git metadata
  When the Workbench records their inspected source context
  Then the repository catalog contains three repository IDs
  And eight interface candidates reference retained source snapshots
  And the contract registry contains zero invented commit revisions

Scenario: Initialize a separate workspace
  Given a source workspace with registered project records and retained evidence
  When the installed ai-sdlc command initializes an empty directory
  Then all six new catalogs contain zero entries
  And the new raw manifest contains zero sources
  And no live candidate, finding, audit event, or source snapshot is copied
  And the original source bytes remain unchanged
```

## Validation

| Check | Result and evidence |
| --- | --- |
| Runtime regressions | PASSED: 77 tests. [Retained execution](evidence/repository-registration-tests.txt). |
| Snapshot and candidate checks | PASSED. [Retained source checks](evidence/repository-registration-source-checks.json). |
| Source workspace validation | VALID. Two candidate knowledge records and zero structural findings. |
| Distribution and standalone initialization | PASSED. [Package checks](evidence/repository-registration-packaging.json). |
| Documentation and staged diff | PASSED. Local links, changed prose limits, and whitespace checks passed. |

Checks used macOS and Python 3.14.5.
Business tests and deployments were not executed.
Windows execution and ASD writing review remain pending.
Original source commits remain the blocker for revisioned contract registration.
