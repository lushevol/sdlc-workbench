# Generic brownfield portability review

**Workbench supports generic adoption with explicit tool limits. Complete automatic extraction across arbitrary projects remains unsupported.**
Owner: Workbench maintainer.
Action: select tools through the [adoption boundary](../WORKSPACE_DESIGN.md#brownfield-adoption-boundary).
Consequence: unsupported extraction requires direct inspection and existing repository tools.
Evidence: [source assessment](#assessment) and [retained checks](#validation).

## Scope and reference

High-priority intent: [exact user input, 30 October 2026](../evidence/generic-brownfield-portability-20261030/user-input.md).
Scope: shared skills, runtime catalogs, workspace construction, onboarding, and shipped guidance.
This work is harness maintenance. It creates no business requirement, approval, or published knowledge.
Baseline: `840e8a9b727c4c7e95c88bc3276172c40e4d026b`.
Confidence: high for inspected contracts and controlled local checks.
Unseen technology stacks, native Windows execution, and live external integrations remain unverified.

## Assessment

| Area | Finding and consequence | Result, owner, and action |
| --- | --- | --- |
| Skills | Shared SDLC procedures use discovered sources and evidence. Specialized helpers have narrower coverage. | Generic procedures remain reusable. Maintainer: use the [project-fit rule](../../.agents/skills/service-dependencies-graph/SKILL.md#project-fit). |
| Functional components | [Catalog classifications](../../core/context/catalogs.py#L33) rejected otherwise valid project-defined asset kinds. | Fixed. Maintainer: use nonblank classifications; preserve provenance, references, and grants. |
| Onboarding | Six common stacks produced no manifest, entrypoint, or test hints. [Baseline probe](../evidence/generic-brownfield-portability-20261030/onboarding-baseline-probe.json) establishes this limit. | Fixed. Maintainer: inspect filename candidates before making semantic claims. |
| Construction | [Initialization](../../core/workspace.py#L83) creates empty catalogs and preserves existing repository locations. | Reusable. Maintainer: initialize an empty workspace beside existing assets. |
| Defaults | Shipped environment examples carried project, space, and ServiceNow API defaults. | Fixed in [.env.example](../../.env.example#L29). Maintainer: configure confirmed project values. |
| Guides | ADO wording implied a required source host. Root guidance linked omitted project fixtures. | Fixed. Maintainer: follow [host-neutral repository setup](../../repos/README.md). |
| Packaging | Generated workspaces omit runtime source, business checkouts, and live task evidence. | Confirmed through [wheel smoke assertions](../evidence/generic-brownfield-portability-20261030/wheel-smoke.json). |

No inspected gap demonstrated disruptive business-user impact.
These changes address adoption friction and misleading coverage expectations.
They do not establish production readiness for an adopting application.

## Changes and risk

Metadata classifications now accept custom nonblank strings across loader contracts, published schemas, and graph inventory.
Existing conventional values remain valid.
Custom values add no parser, connector, runtime relationship, or operation grant.
Full Git contract revisions, explicit Confluence read-only declarations, and reference checks remain required.

Onboarding now identifies Go, Rust, .NET, Ruby, PHP, and C/C++ filename hints.
Mixed repositories retain each module's hints.
The scanner reads no added source or manifest contents for these hints.
Ignored paths and independent nested checkouts retain their existing exclusions.

The adoption guide separates reusable components from specialized extraction, connectors, collectors, and client adapters.
Shared instructions retain this boundary for future maintenance.
Historical quotations remain intact. Root guides no longer require omitted project captures to explain those instructions.

Qualitative risk: low to medium.
Broader metadata types could expose downstream closed taxonomies.
Inspection found and corrected the duplicate graph inventory taxonomy.
The [graph regression](../../.agents/skills/service-dependencies-graph/tests/test_service_graph.py#L98) confirms unsupported extraction remains explicit.
Onboarding hints can include false candidates; direct inspection remains required.

## Maintenance behavior checks

These checks define this maintenance scope. They supply no business approval.

### MC-1: Preserve custom classifications and execution boundaries

```gherkin
Scenario: Register project-defined asset kinds
  Given valid catalogs with a cli repository, grpc contract, and jira source
  And the contract identifies a full Git commit
  When Workbench loads the catalogs
  Then it preserves all three classification values
  And it creates zero executable resources from those declarations
  And it rejects blank classifications and unknown references
```

### MC-2: Discover common brownfield layouts

```gherkin
Scenario: Inventory six stacks without reading candidate contents
  Given Go, Rust, .NET, Ruby, PHP, and C/C++ filename fixtures
  And a mixed repository includes ignored filename hints
  When the onboarding scanner inventories the fixtures
  Then each stack has manifest, entrypoint, and test candidates
  And the mixed repository retains every visible module's candidates
  And ignored hints remain absent
  And the repository's Git status remains unchanged
```

### MC-3: Initialize portable defaults

```gherkin
Scenario: Create a workspace without adopting tenant settings
  Given the installed Workbench wheel
  When Workbench initializes an empty workspace
  Then the workspace validates with zero executable resources
  And ADO_PROJECT, CONFLUENCE_SPACE_KEY, and SNOW_API_PATH are empty
  And business checkouts, live task evidence, and runtime source are absent
```

## Traceability

These matrices cover three maintenance behaviors.
Documentation and template updates support those behaviors and the explicit adoption boundary.
No business AC denominator exists for this harness maintenance stage.

### Behavior to test assertions

| Behavior | Direct assertion evidence |
| --- | --- |
| [MC-1](#mc-1-preserve-custom-classifications-and-execution-boundaries) | [Classification checks](../../tests/test_catalogs.py#L127), [reference and grant assertions](../../tests/test_catalogs.py#L144), [graph limit assertion](../../.agents/skills/service-dependencies-graph/tests/test_service_graph.py#L98). |
| [MC-2](#mc-2-discover-common-brownfield-layouts) | [Six-stack assertions](../../tests/test_repository_onboarding.py#L130), [mixed repository assertions](../../tests/test_repository_onboarding.py#L179). |
| [MC-3](#mc-3-initialize-portable-defaults) | [Tenant assertions](../../tests/test_workspace_layout.py#L352), [installed wheel assertions](../evidence/generic-brownfield-portability-20261030/wheel-smoke.json). |

Definition-to-assertion coverage: 3/3 maintenance behaviors.
This denominator excludes unsupported language semantics and business behavior.

### Behavior to changed implementation

| Behavior | Changed units |
| --- | --- |
| [MC-1](#mc-1-preserve-custom-classifications-and-execution-boundaries) | [Catalog loader](../../core/context/catalogs.py#L33), [repository schema](../../registry/repositories.schema.json), [contract schema](../../registry/contracts.schema.json), [source schema](../../registry/sources.schema.json), [graph inventory](../../.agents/skills/service-dependencies-graph/tools/repository_inventory.py). |
| [MC-2](#mc-2-discover-common-brownfield-layouts) | [Onboarding scanner](../../.agents/skills/repository-onboarding/scripts/scan_repo.py#L29). |
| [MC-3](#mc-3-initialize-portable-defaults) | [Environment defaults](../../.env.example#L29). |

Definition-to-change coverage: 3/3 maintenance behaviors.
The existing initializer remains required unchanged implementation.

### Changed implementation to test assertions

| Changed unit group | Direct assertions and retained execution |
| --- | --- |
| Catalog loader and three schemas | [Classification and schema assertions](../../tests/test_catalogs.py#L127), [focused execution](../evidence/generic-brownfield-portability-20261030/classification-checks.json). |
| Graph inventory | [Unsupported extraction assertion](../../.agents/skills/service-dependencies-graph/tests/test_service_graph.py#L98), [focused execution](../evidence/generic-brownfield-portability-20261030/classification-checks.json). |
| Onboarding scanner | [Candidate assertions](../../tests/test_repository_onboarding.py#L130), [focused execution](../evidence/generic-brownfield-portability-20261030/onboarding-regressions.json). |
| Environment defaults | [Empty tenant assertions](../../tests/test_workspace_layout.py#L352), [workspace execution](../evidence/generic-brownfield-portability-20261030/distribution-validation.txt). |

Change-to-assertion coverage: 4/4 changed runtime or configuration groups.
These links do not establish complete behavioral equivalence or business conformance.

## Remaining specialization

| Limit and consequence | Evidence | Owner and next action |
| --- | --- | --- |
| Graph extraction covers selected languages and frameworks. Empty results cannot establish absent relationships elsewhere. | [Extraction map](../../.agents/skills/service-dependencies-graph/SKILL.md#dependency-extraction-map). | Maintainer: inspect source directly or use existing project tools for unsupported scope. |
| Internal gRPC and DQSL recognition retain project-specific patterns. Generic protocol coverage remains incomplete. | [SDK constants](../../.agents/skills/service-dependencies-graph/tools/extract_grpc_dependencies.py#L22), [platform recognizer](../../.agents/skills/service-dependencies-graph/tools/build_graph.py#L1119). | Maintainer: treat these as specialized recognizers and inspect coverage. |
| Contracts currently require Git-backed source locators. Filesystem-only contracts cannot use this catalog form. | [Source requirements](../../core/context/catalogs.py#L54). | Maintainer: retain external specs as source evidence with explicit catalog limits. |
| Release Clinic retains upstream collector mappings. Arbitrary release systems require project-specific configuration or existing tools. | [Collector configuration](../RELEASE_CLINIC.md). | Adopting maintainer: supply confirmed streams, fields, endpoints, and credentials before collection. |
| Setup and native integrations have platform-specific requirements. This run establishes macOS evidence only. | [Setup limits](../SETUP.md). | Adopting maintainer: validate the actual target environment. |

These limits do not block generic workspace construction or manual evidence-led onboarding.
They block claims of complete automatic support for every brownfield project.

## Validation

- Complete suite: 687 passed; zero failures, errors, or skips. [Original output](../evidence/generic-brownfield-portability-20261030/unit-tests-complete.log).
- Optional Node integration ran against local fixtures with `WORKBENCH_CONNECTOR_INTEGRATION=1`.
- Wheel build passed using installed build dependencies. [Build output](../evidence/generic-brownfield-portability-20261030/wheel-build-local.log).
- Installed-wheel initialization, custom metadata, and mixed-stack inventory passed. [Smoke evidence](../evidence/generic-brownfield-portability-20261030/wheel-smoke.json).
- Six generated entrypoint documents have no missing local link targets. [Link results](../evidence/generic-brownfield-portability-20261030/entrypoint-links.json).
- Both changed skills passed the skill structure validator. [Check summary](../evidence/generic-brownfield-portability-20261030/validation-summary.json).

The first suite run encountered sandbox loopback restrictions and two opt-in integration skips.
The complete rerun resolved those conditions without narrowing the suite or weakening assertions.
The default isolated build could not download setuptools through the restricted proxy.
The successful build used installed setuptools through `--no-build-isolation`.
The first wheel smoke lacked prepared dependencies. The successful run used an isolated package with prepared dependency paths.
These original failures remain in the [evidence directory](../evidence/generic-brownfield-portability-20261030).
SDLC artifact lint requires template frontmatter and does not apply to these maintenance documents.
Its failed attempt remains in [authoring evidence](../evidence/generic-brownfield-portability-20261030/authoring-check.json).

Concurrent review-index maintenance remained outside this change's commit scope.
The complete suite and wheel smoke used the combined working tree.
The [validation summary](../evidence/generic-brownfield-portability-20261030/validation-summary.json) records hashes and evidence limits.
No live business service, target application build, or native Windows execution was verified.
No dependency declaration changed.
Authoring whitespace checks passed; original log whitespace remains preserved.

## Writing checks

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
