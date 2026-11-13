# AI SDLC Workbench assessment

Date: 2026-11-07 (Asia/Singapore).
Source baseline: `a8e3fdd14a5a779f9af90969650a5a6211f61fbb`.

**The Workbench provides a strong foundation for evidence-led AI engineering. Reliable lifecycle execution and measurable outcomes need further proof.**
No immediate user decision is required.
This assessment does not establish a product failure, release hold, or deployment authorization.

## Scope and source priority

The [exact user input](user-input.md#exact-user-input) controls this assessment.
This is harness assessment, so business-task intake does not apply.

Inspect current architecture, runtime, assertions, knowledge records, evaluation evidence, and adoption limits.
Separate implemented capability, documented intent, observed execution, and inference.
The source revision above applies to repository sources below, unless another revision is explicitly recorded.

Affected scope: this assessment and its supporting evidence.
Risk: low; documentation changes only.
Existing untracked files remain outside this change.
No business repository, runtime code, domain meaning, or execution grant changes.

## What the project does well

| ID | Strength and evidence | Class and confidence | Practical value and limit |
| --- | --- | --- | --- |
| S1 | Separate intent, implementation, execution, and approval. The [session gap record](../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md#scope-and-source-facts) demonstrates this in actual investigations. | Inspected records; HIGH. | Prevents passing mocks or current code from becoming approved policy. This does not prove deployed behavior. |
| S2 | Preserve existing repositories and separate asset identities. The [adoption boundary](../../WORKSPACE_DESIGN.md#brownfield-adoption-boundary) supports independent layouts and many-to-many relationships. | Documented contracts and inspected tests; HIGH. | Fits brownfield systems without source migration. Specialized extraction retains explicit limits. |
| S3 | Share tool grants, schema validation, and action retention across interfaces. See [runtime](../../../core/runtime.py), lines 24–34 and 68–104. | Inspected implementation; HIGH. | Gives agents consistent execution boundaries and reviewable results. Hashes do not authenticate an actor or establish truth. |
| S4 | Generate AC-to-case, AC-to-change, and change-to-case matrices. See [coverage implementation](../../../core/review_coverage.py), lines 45–76 and 100–112. | Inspected implementation; HIGH. | Separates denominators, freshness, assertion bindings, and passing execution. Complete links do not establish semantic conformance. |
| S5 | Test consequential boundaries and evaluate agent decisions. See [runtime assertions](../../../tests/test_core.py), lines 34–68 and 217–244, and [skill trials](../../../tests/README.md#evaluate-skill-decisions). | Inspected assertions and historical execution; HIGH within those bounds. | Checks permissions, evidence hashes, filesystem escapes, and misleading verification claims. General agent reliability remains unproved. |

The two retained semantic evaluations contain seven synthetic cases and 33 assessed criteria in total.
The [first evaluation](../../reviews/skill-workflow-evaluation.json) records five cases and 21 criteria.
The [second evaluation](../../reviews/setup-deployment-skill-evaluation.json) records two cases and 12 criteria.
These are historical results at their recorded revisions, not current-skill execution results.

## What still needs work

These priorities concern improvement order. They are not product incident severities or release decisions.
Owners below identify roles; named accountable people remain unknown.

| ID | Gap, evidence, and confidence | Consequence | Owner and next action |
| --- | --- | --- | --- |
| G1 | Lifecycle gates and recovery remain agent procedures. [Architecture](../../../ARCHITECTURE.md#core-workflow), lines 343–349, explicitly excludes executable phase gates and a durable runner. HIGH; documented implementation boundary. | An agent can omit a required stage without the runtime preventing its next operation. No such misuse was demonstrated here. | Workbench maintainer. Select one current workflow and add only justified persistent checkpoints and transition checks. |
| G2 | Traceability validity does not establish behavior correctness. [Behavior review](../../BEHAVIOR_REVIEW.md#interpret-the-result) retains `NOT_VERIFIED` and declared assertion bindings. HIGH; inspected contract and implementation. | Reviewers must still establish semantic support, correct assertions, actual execution, and deployment applicability. | Task reviewer and application owners. Demonstrate one real change from approved intent through UAT evidence and knowledge reconciliation. |
| G3 | Canonical knowledge has not reached publication. All 12 canonical domain records remain candidate/draft, with unknown topic owners. See [current topic states](../../../knowledge/candidates/index.md), lines 18–20 and 95–97. HIGH; current frontmatter inventory and index agree. | Agents have useful context, but these records cannot supply an approved domain baseline. Validation success cannot remove this limit. | Domain owners, currently unknown. Assign owners and complete review for one bounded topic. |
| G4 | Freshness handling and knowledge maintenance remain substantially manual. [Ingestion](../../../core/ingestion/README.md), lines 21–32, excludes automatic source synchronization. HIGH; documented runtime boundary. | Relevant source changes can require repeated manual discovery and review. Actual staleness frequency was not measured. | Knowledge steward. Add a source-change review queue only for active sources with demonstrated maintenance demand. |
| G5 | AI evaluation is small and manually assessed. The [evaluation procedure](../../../tests/README.md#evaluate-skill-decisions) installs no automatic replay or semantic grader. HIGH for scope; productivity benefit UNKNOWN. | Existing trials cannot establish current general reliability, improvement against prior skills, or reduced engineering effort. | Workbench maintainer. Repeat affected cases at current hashes. Measure unsupported claims, reviewer corrections, time, and cost. |
| G6 | Adoption evidence remains narrower than the generic foundation. See [extractor limits](../../WORKSPACE_DESIGN.md#brownfield-adoption-boundary), [platform limits](../../SETUP.md#root-playwright-pom-harness), and [connector limits](../../CONNECTORS.md#analyze-postgresql-data). HIGH for documented limits. | Unsupported syntax needs direct inspection. Local fixtures cannot establish native Windows readiness or company service access. | Adopting team. Complete an unrelated brownfield pilot and native Windows setup, offline, and authorized service checks. |
| G7 | Some optional integrations disable certificate validation. See [Vault session](../../../core/release-clinic/plugins/test/dtp-tda-service/service/vault_client.py), line 79, and [web helper](../../../core/connectors/packages/web/scripts/search-ddg.py), lines 36–38. HIGH; inspected source. | These paths lack server certificate validation. No attack, production exposure, or user disruption was demonstrated. | Integration maintainer and security owner. Add verified certificate handling and private CA support before broader use of affected paths. |

The current local trust boundary also matters for future shared deployment.
[Governance validation](../../../core/governance/README.md), lines 22–24, does not authenticate reviewers.
[Plugin loading](../../../core/registry.py) imports trusted Python rather than isolating untrusted extensions.
Authenticated approval and plugin isolation require a demonstrated shared or untrusted deployment consumer.
They are not prerequisites for the documented trusted local use case.

## Recommended next increment

Complete one real, bounded SDLC workflow using existing components.
Bind approved intent, measurable criteria, changed code, inspected assertions, actual execution, and deployment identity.
Include remote UAT evidence when the selected workflow requires it.
Reconcile intended knowledge and independent gaps after the change.

Record manual intervention, reviewer corrections, unsupported claims, elapsed effort, and model cost.
Compare these outcomes against a declared baseline.
The [existing pilot proposal](../../reviews/LLM_WIKI_AGENT_INTEGRATION_20261105.md#proposed-bounded-pilot) already proposes related measurements.
Its proposal does not establish achieved savings.

Use that evidence to select the smallest valuable automation.
Prioritize recurring review work, trustworthy evidence bindings, and workflow recovery over additional framework breadth.
Treat a dedicated UI and general orchestration as conditional expansion choices.

## Local verification

The [validation record](validation.json) retains exact commands, counts, environment, hashes, and execution limits.
Workspace validation returned `VALID`, with 14 documents and zero findings.
This checks contracts, not domain correctness.

The declared harness inventory contains 883 tests.
The initial configured run encountered sandbox restrictions on local fixture servers.
It reported 876 tests, 37 errors, zero assertion failures, and seven unrun cases.
The [compressed original output](unit-tests-sandbox.log.gz) preserves that result.
This environment limit does not establish a product defect or passing status.
The permitted rerun passed all 883 tests in 78.274 seconds.
It reported zero failures, errors, skips, or expected failures.
The [compressed passing output](unit-tests-passed.log.gz) preserves the complete result.
No code or assertions changed between these runs.

Meaningful inspected assertions include the following:

- [Operation and filesystem boundaries](../../../tests/test_core.py), lines 34–68 and 217–244.
- [Publication content bindings](../../../tests/test_knowledge_governance.py), lines 153–177.
- [Empty generated workspace boundaries](../../../tests/test_workspace_layout.py), lines 240–259.
- [Standalone CLI invocation](../../../tests/test_interfaces.py), lines 28–45.

No wheel build, native Windows run, live connector call, business E2E execution, or production inspection was performed.
No numerical maturity score is assigned. This assessment has no calibrated scoring model.

## Assessment limits

Confidence is HIGH for the cited implementation boundaries and current record states.
Confidence is MEDIUM for improvement ordering because adoption cost and business value were not measured.
The recommended increment is an inference from those boundaries, not an approved implementation requirement.
A bounded inspection cannot establish that all other project capabilities or outcome measurements are absent.

## Output review

[Document checks](document-checks.json) validate local links, heading anchors, JSON evidence, and retained log hashes.
They do not establish ASD grammar compliance or business correctness.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
