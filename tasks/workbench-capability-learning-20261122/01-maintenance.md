# Self-Evolving Capability System

**No critical conclusions require user attention or action.**

The user supplied the [exact implementation directive](evidence/user-directive.txt) on 22 November 2026 in this Codex session.
The directive authorizes local Workbench implementation and fixture-based tests.
It protects production deployment and entitlement operations.

Baseline Workbench revision is `3ded0689336f7926e025d6545a9f5652c698446b`.
The deleted connector lockfile and untracked release-report source were present at entry.

## Workbench gap analysis

| Area | Reuse | Gap |
| --- | --- | --- |
| Runtime and configuration | Installed Python CLI, workspace declarations, existing JSON Schema validator, local atomic file helpers | Capability learning commands and local switches |
| Registry | Existing capability, contract, repository, service and tool catalogs | Scoped discovery and change records, reconciliation and revision history |
| Knowledge and experience | Canonical knowledge, governed transitions, retained sources and reviewed experience packets | Lightweight automatic capture and checkpoint-based semantic review |
| Agent discovery | Canonical Agent Skills folders and Claude discovery aliases | Learning skill and read-only ADO skill |
| Agent lifecycle | Installed Codex, Claude and Copilot hook adapters, explicit task bindings and advisory checks | Sanitized learning observations, extra lifecycle events and native verification |
| Integration | Granted ADO connector operations, release report, CES migration baselines and candidate records | Read-only artifact resolution and reusable CES classification with policy protection |
| Verification | Existing unit suite, wheel build, workspace validation, Git and task evidence | End-to-end fixture cases and capability-learning audit checks |

## Implementation plan

1. Extend the installed Python CLI and reuse its validation, path and atomic write helpers.
2. Keep revision history alongside the existing capability catalog. Reuse canonical contract and skill references.
3. Keep scratch observations and proposals in ignored local storage. Bind reviewed evidence to exact hashes.
4. Retrieve related capabilities by identity, category, applicability and terms before reconciliation.
5. Use a scoped revision journal to activate a validated change atomically and retain rollback history.
6. Allow automatic promotion for typed ADO artifact selection data with independent local checks.
7. Route executable content and CES policy through established review and governance.
8. Extend native adapters with bounded metadata capture and preserve explicit task checkpoints.
9. Package skills and current documentation. Verify ADO, CES and cross-session reuse with fixtures.
10. Run native checks where available, then run the unit suite, build the wheel and validate an initialized workspace.

The installed runtime and shared registry change. Invalid revisions can affect future sessions.
Strict validation, atomic promotion and isolated fixtures reduce that risk.

## Implemented outcome

The Workbench now captures minimized lifecycle events and accepts evidence-bound discoveries at task checkpoints.
The CLI reconciles scopes, holds conflicts, and stores promoted revisions in the existing registry area.
Earlier revisions remain available for audit and rollback. Existing provider grants remain the execution authority.

The ADO resolver reuses two granted artifact metadata reads. Its checks bind each result to an exact build and commit.
Local pipeline wrappers use shared templates. Their source does not establish the artifact naming and deployment rules.
Fixture discoveries extended one ADO skill across two branch conditions. A new process reused the selected rule.
Automatic promotion requires two matching builds with distinct commits and one artifact each.
The resolver reports metadata integrity. Artifact bytes, deployment mechanisms, and target approvals still need authorized evidence.

The CES foundation reuses the migration coverage replay and retained knowledge candidates.
CES discoveries preserve migration time, instance, environment, and application scope.
Protected proposals stay pending for canonical governance. Live entitlement state was outside validation.

Skill instructions remain reviewed source. The engine validates their identity and records the reviewed hash.
Typed ADO improvements change the skill's selection through scoped data.
The existing agent performs general semantic extraction at checkpoints. Native hooks supply lifecycle hints.

## Verification

- The complete Workbench suite passed 1,155 tests, including optional connector integration. Zero failures or skips.
- The wheel installed outside the checkout. A generated workspace completed learning, revision extension, and cross-session reuse.
- The two new skills passed structure validation. Workspace validation checked 119 knowledge documents with zero findings.
- Claude Code and the embedded Copilot runtime both dispatched six event classes in isolated macOS probes.
- Workbench-owned Claude and Copilot registrations were upgraded locally. Their configuration reports ready.
- Standalone Copilot CLI, cloud dispatch, native Windows, live ADO, and live CES were unverified.

[Validation evidence](evidence/validation.txt)

Current guidance is in [architecture](../../ARCHITECTURE.md#skills-and-adapters), [capability learning](../../docs/CAPABILITY_LEARNING.md),
[native hooks](../../docs/HOOKS.md#learning-capture), and the [CES domain skill](../../.agents/skills/ces-domain-capability/SKILL.md).

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```

## Skill lifecycle suggestion review

The user supplied the [exact suggestion](evidence/skill-lifecycle-suggestion.txt) for review on 22 November 2026.
The review compares it with committed Workbench revision `b04f3cf74`.
Use the six responsibilities as the model for the existing skill and Python engine.
The ADO fixture completed the proposed reuse sequence across CLI processes and two workspaces.
A separate probe confirmed that instruction-only updates fall outside the current promotion workflow.
The review record explains the gap and the smallest follow-up. [Review evidence](evidence/proposal-review.md)

## CES domain skill replacement

The user supplied the [exact request](evidence/ces-domain-skill-request-20261123.txt) in Codex on 23 November 2026.
Baseline Workbench revision is `9441e157f`.
The change affects CES skill routing, packaging, and the registry entry.
The existing scanner and evidence remain available for migration work.

The new CES domain skill covers effective access, data scope, integration contracts, and mixed-provider compatibility.
The registry resolves the existing capability ID to the new skill.
The scaffold ships the canonical skill and its Claude alias.
Migration review uses the relocated scanner and report guidance.
The scanner produces the existing report format and tool identifier.
[File relocation and source hashes](evidence/ces-skill-relocation-20261123.json)

Validation ran on macOS with Python 3.14.5.

- The full suite passed 1,155 tests with connector integration enabled and zero skips.
- The new skill passed the Agent Skills structure validator. Workbench validation checked 119 knowledge documents with zero findings.
- The wheel installed outside the source checkout. CLI discovery, the Claude alias, relative links, and an isolated scanner fixture passed.
- An independent read-only review traced a CES record-visibility question through application, entitlement, functional access, and data restrictions.

The wheel SHA-256 is `fac98c9efe09bf8af4dc86792ef6a5ac40257a5d0f22c1d154de57c6affedaff`.
The suite log at `.workbench/ces-domain-skill-validation/full-suite.log` has SHA-256
`683e2db700380f952c0f5f0320fca4960f1068045b63e23ffedc4f0db3bb7da1`.
The checks cover skill distribution and offline operation. Live CES and native client activation remain unverified for this change.

See the [CES domain skill](../../.agents/skills/ces-domain-capability/SKILL.md)
and its entry in [capability learning](../../docs/CAPABILITY_LEARNING.md#integration-examples).

## Standalone CES capability

The user supplied the [exact follow-up](evidence/ces-standalone-skill-request.txt) in this Codex session on 23 November 2026.
Baseline Workbench revision is `4301ebcee1de55e7ffc49375a08e38337d3f2dd4`.
The skill must package CES contracts, domain knowledge, workflows, and scripts.
Remove migration scan content from the skill and verify the package outside Workbench.

The package now contains CES response contracts, a domain model, investigation workflows, an offline inspector, and synthetic captures.
The inspector uses the Python standard library.
The active skill links resolve within its own folder.
The Workbench capability registry points to the same skill entry.
The change replaces one diagnostic tool and its supporting migration material with a CES capture inspector.
[Removed files and recovery revision](evidence/ces-standalone-skill-removals.json)

The response shapes follow four retained CES GET captures.
The evidence covers the application catalog and effective-user views.
[Captured API field mapping](../ces-entitlement-migration-20261102/03-output-mapping.md#operations-and-delivery)

- All 1,157 Workbench tests passed on macOS with connector integration enabled.
- The Agent Skills validator and Workbench validation passed. Workbench found zero issues in 119 knowledge documents.
- An installed wheel shipped all nine package files. CLI discovery, the Claude alias, and internal links passed in a fresh workspace.
- The inspector passed from a copied folder with Python isolated mode and site imports disabled.
- The independent walkthrough verified exact feature/action checks and compared assignment, grant, and data-section changes.

The offline checks cover captured responses. Data-policy interpretation and current CES enforcement need scoped evidence.
Current instructions are in [CES domain capability](../../.agents/skills/ces-domain-capability/SKILL.md)
and the [Workbench capability guide](../../docs/CAPABILITY_LEARNING.md#integration-examples).

## CES domain coverage and variables

The user supplied the [exact follow-up](evidence/ces-skill-enrichment-request-20261123.txt) in Codex on 23 November 2026.
Baseline Workbench revision is `39a10b1a2`.
Review relevant session decisions and retained tasks. Enrich the standalone CES skill and maintain its variable definitions separately.

The SDK session and retained fixture establish the assigned-role view and its role-specific grant shape.
The functional-profile session establishes the requested value checks, rejection cases, and timing convention.
The data-control design supplies decision points for tracing record and notification visibility.
These sources inform the skill's procedures. Current wire and policy details require evidence for the selected scope.

- Assigned roles and provenance. [SDK contract review](../single-ui-sdk-ces-migration-20261101/10-change-review.md#selected-compatibility-design)
- Profile values and account types. [Recorded clarifications](../ces-entitlement-migration-20261102/evidence/function-entitlement-20261117/user-clarifications.md) and [timing convention](../ces-entitlement-migration-20261102/evidence/function-entitlement-20261117/user-timing-target.md)
- Policy and consumer visibility. [Historical data-control design summary](../../knowledge/records/candidates/security/KT-ces-entitlement-control-20261115.md#query-and-notification-enforcement)

The skill adds assigned-role inspection and a role-attribution fixture.
The functional-profile guide distinguishes value, provisioning, and timing checks.
The variable template separates topic, service origin, routes, account, application, selectors, and evidence inputs.
Packaged tenant values are unset. Task values belong in a local copy.

All 1,158 Workbench tests passed on macOS with connector integration enabled.
The first attempt hit sandbox loopback errors. The rerun with local fixture access passed.
The passing log SHA-256 is `99f5b4e2b31e08c2879d62c1e997751feb824bbf34e18d03f6ae73397cecf2dd`.
The wheel, clean-workspace link checks, skill structure validation, and isolated Python commands passed.
Verification covers offline captures and documentation. Live CES and provisioning outcomes need scoped evidence.

[Updated CES skill](../../.agents/skills/ces-domain-capability/SKILL.md) · [Variable template](../../.agents/skills/ces-domain-capability/Workflows/variables.example.json)

## CES UAT origin and response schemas

The user supplied the [exact request](evidence/ces-uat-and-schema-request-20261123.txt) in Codex on 23 November 2026.
Baseline is `3d612a2c6`. The change covers the CES skill package and offline contract validation.

The previous skill contained route templates and prose field descriptions.
The update records the supplied host as a named UAT origin in the [variable template](../../.agents/skills/ces-domain-capability/Workflows/variables.example.json).
The [retained collection configuration](../ces-entitlement-migration-20261102/coverage/config.json#L31) and four HTTP captures use that host.
The active base URL remains an explicit task input.

Three Draft 2020-12 schemas cover the catalog, effective-user, and assigned-role response shapes.
The schema test accepted the four synthetic bodies and rejected an invalid body for each view.
Offline validation accepted two UAT catalogs, two effective-user bodies, and the retained assigned-role SDK fixture.
The inspector remains a separate standard-library tool for scoped comparisons.
See the [response contracts](../../.agents/skills/ces-domain-capability/Contracts/README.md).

All 1,159 Workbench tests passed with connector integration enabled on macOS.
The wheel installed outside the checkout and shipped the UAT origin and all three schemas.
The new workspace passed validation. Live endpoint behavior and service-wide schema guarantees remain unverified.
The full suite log SHA-256 is `2df36f06be9afe48416d1cc5ddaee643fa5c2a570c593b8c10c372e349f9c683`.

## CES domain facts and reusable tools

The user supplied the [exact follow-up](evidence/ces-domain-tools-refinement-request-20261123.txt) on 23 November 2026.
Baseline Workbench revision is `c5edb0322`. The scope is the standalone CES skill, its tests, and its Workbench guidance.

## Domain capability extraction refinement

The user supplied the [exact refinement request](evidence/domain-capability-extraction-request-20261123.md) on 23 November 2026.
The request references a shared conversation with the latest suggestions.
Baseline Workbench revision is `c5edb0322`.
Existing CES skill, inspector, domain-facts, and maintenance edits were present at entry.
The untracked release-report source was also present. Preserve these changes during refinement.

The [retained conversation selection](evidence/domain-capability-shared-suggestions-20261123.md) supplies the latest direction.
Use one extractor with domain-specific Contracts, Workflows, and Knowledge folders under `knowledge/integrations/`.
Keep workflows in Markdown. Scripts are optional. Retain meaningful failures and merge existing content.
The extractor uses ordinary agent tools without a hook or learning-engine prerequisite.

The change affects skill discovery, shipped guidance, and package distribution.
Incorrect extraction can overstate API guarantees or overwrite supported facts. Source bindings and isolated trials address that risk.
The [extractor](../../.agents/skills/domain-capability-extractor/SKILL.md) and its construction reference now define that workflow.
Root guidance routes extraction directly. Registry retrieval and reconciliation apply when independently relevant.
The scaffold ships the skill and creates its Claude discovery alias.
Existing CES edits remain separate from this refinement.

All 1,159 unit tests passed with connector integration enabled. No failures, errors, or skips occurred.
Skill structure, workspace validation, new relative links, and installed-wheel checks passed.
The wheel initialized outside the checkout with matching skill, reference, guide, and alias bytes.
An initial wheel check detected a guide edited after building. The rebuilt wheel passed.

An independent synthetic extraction preserved existing scoped content and three paired exchanges.
It retained uncertain causes, observation limits, and unfinished pagination and deployment steps.
Independent source review found one root routing conflict. The correction made registry learning conditional.
No actionable findings remained after review.
[Verification and trial evidence](evidence/domain-extractor-verification-20261123.json)

Current guidance changed in `AGENTS.md`, `ARCHITECTURE.md`, `docs/CAPABILITY_LEARNING.md`, `docs/EXPERIENCE_ASSETS.md`,
`docs/WORKSPACE_DESIGN.md`, `knowledge/README.md`, and `tasks/README.md`.
The workflow discovery became a shared instruction change. No runtime promotion or business-rule change was needed.
Validation covers offline behavior and one synthetic extraction. Full OpenAPI validation and live integrations remain unverified.

## CES capability under the extraction standard

The user supplied the [exact request](evidence/ces-new-standard-request-20261123.md) on 23 November 2026.
Baseline Workbench revision is `d6ca85c8a`.
The earlier CES facts and tool edits are now within the requested CES refinement scope.
Untracked release-report files remain outside this scope.
The affected consumers include CES skill discovery, the inspector command, response schemas, tests, registry links, and workspace packaging.
Preserve standalone CES use while consolidating contracts, workflows, and knowledge with source-bound evidence.

Incorrect schemas can overstate guarantees. Relocation can break tools and standalone discovery.
The real skill folder now contains the Contracts, Workflows, and Knowledge library.
`knowledge/integrations/ces/` links that folder without duplicating its maintained content.
The original inspector command forwards to the relocated implementation.
[Byte-preserving relocation and recovery bindings](evidence/ces-standard-relocation-20261123.json)

Four sanitized paired cases retain their original request and response bindings.
Catalog examples identify their selected rows and incomplete-body projection.
Large nested arrays retain bounded prefixes, with original lengths and exact selected ranges recorded.
The assigned-role example is a supplied body fixture, with no invented request, status, or capture date.
OpenAPI observation schemas separate field shapes from local inspector requirements.
[Inspected source bindings](evidence/ces-standard-source-review-20261123.json)

The eight focused CES tests and all 1,163 Workbench tests passed. No failures, errors, or skips occurred.
The OpenAPI document passed the official OpenAPI 3.1 schema. Embedded schemas and paired bodies passed separate JSON Schema checks.
The source archive built a wheel, which initialized outside the checkout with matching library bytes.
Six new command paths and six legacy command paths produced identical results from an isolated standalone folder.
Skill discovery, Claude alias, 47 local links, workspace validation, and offline source fingerprint checks passed.

Independent review found account identifiers in original provenance filenames. Portable references now use source IDs, hashes, and inventory locators.
The full source-path mapping remains in task evidence. None of 5,151 captured account identifiers appear in the portable library.
An early usage-trial manifest mislabeled all inputs synthetic. Its limited result and exact inputs remain retained.
The final independent trial used explicit evidence classes. Eight commands passed and all 26 input hashes remained unchanged.
It retained four comparison differences, a matching effective union, and unresolved profile assertions.
Final source review re-derived all four pairs after sampling. The catalog examples are 3,086 and 2,338 bytes.

Catalog A selects FLOWZERO. Catalog B and both effective-user captures select RATAN_ENTITLEMENT_RULE.
The library now states that these application scopes cannot be combined for reconciliation.
Current documentation changed in `docs/CAPABILITY_LEARNING.md` and this library's index, contracts, workflows, variables, and knowledge.
No new dependency or execution grant was added. The unrelated release-report source remains outside this change.
[Final verification, source hashes, and trial evidence](evidence/ces-standard-verification-20261123.json)

Validation covers retained observations, synthetic tool cases, and standalone distribution on macOS.
Live CES, provisioning, current consumer enforcement, and native Windows activation remain unverified.

## CES cleanup and real-response examples

The user supplied the [exact request](evidence/ces-legacy-duplication-real-examples-request-20261123.md) on 23 November 2026.
Baseline Workbench revision is `e72f75c55`.
The scope covers CES compatibility code, duplicate definitions, published examples, tests, and extractor guidance.
The unrelated release-report source remains outside this scope.
Real examples must retain domain values and observed structure, with narrowly scoped identity and credential redactions.

Removing active consumers can break tools or packaging. Over-redaction can erase useful domain information.
The completed cleanup and verification follow below.

## CES cleanup completion

The source comparison verified four HTTP pairs, the assigned-role body, and 90 scoped checks.
It preserved 453 domain string values and five nonstring values.
Fifteen private occurrences became seven stable aliases.
The portable library contained no checked account, owner, credential, or token values.

The obsolete `scripts/inspect_ces.py` wrapper was removed.
Tests and guidance now invoke `Workflows/tools/inspect_ces.py`.
Four synthetic command bodies moved to `tests/fixtures/ces/` without byte changes.
Published examples now use retained response bodies.
Local inspection schemas remain because they enforce required fields and nested input validation.
OpenAPI references shared feature/action and assigned-application observation schemas.

Examples retain application names, entitlement names, feature/action names, policy/profile names, data-scope values, response dates, and ITAM `51358`.
Account IDs, policy owners, profile owners, and Authorization values remain redacted.
Catalog projections record selected indexes, source counts, and half-open array ranges.
The extractor guidance now requires real examples when available and records narrow redactions and projections.

Nine focused CES tests and all 1,164 Workbench tests passed.
The full suite had zero failures, errors, or skips.
Both skill validators, OpenAPI checks, example schemas, regeneration, and 52 relative-link checks passed.
Workbench validation reported zero findings across 119 knowledge documents.
An independent standalone trial verified the documented commands and retained comparison limits.

The source archive, wheel, isolated installation, and fresh workspace passed final-byte checks.
All 21 CES files and extractor guidance matched the source.
The source archive retained the four test-only fixtures.
The installed copy excluded the retired wrapper and synthetic published bodies.
Existing Python dependencies supported runtime checks. No package download occurred.

[Cleanup inventory, source review, distribution, and trial](evidence/ces-cleanup-inventory-20261124.json) · [Complete unit results, gzip](evidence/ces-cleanup-unit-suite-20261124.txt.gz)

Live CES, provisioning, current enforcement, deployment, and native Windows remain unverified.
Independent task-evidence-growth edits appeared during work. They remain outside this cleanup.

The lightweight maintenance record follows ordinary Markdown under the task guide. Business-artifact lint does not apply to that format.
The capability checkpoint recorded `NO_CHANGE` for the existing CES capability. No new entitlement rule or execution grant was added.
