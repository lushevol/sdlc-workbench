# Requirements and skill map

> **Review requirements before choosing enhancements.** This table is the next discussion surface, ahead of the provisional optimization plan.
> **All 49 retained input excerpts are accounted for.** The 22 rows consolidate related requests; they are not priority rankings.
> Skill ownership identifies existing responsibilities. It does not establish reliable execution or an approved change.

## Scope and reading guide

Authority: [latest table request](01-maintenance.md#requirements-table-clarification-17-november-2026).
Sources: [49 retained inputs](evidence/selected-inputs.md), the [408-input retrospective inventory](evidence/session-inventory.json), and the linked clarifications below.
This table accounts for the retained excerpts individually. It does not claim an individual classification of all 408 inputs.

Problems and focus areas are working interpretations of the requests. Desired results and preferences are source-backed paraphrases.
Historical concerns are not findings that every current skill remains defective.
The [source map](#source-map) preserves each retained input's primary requirement row. An input can also inform other rows.

| Area | Meaning |
| --- | --- |
| Problem | The friction or risk behind the request. |
| Desired result | The observable value the work should deliver. |
| Preference | How the user wants work performed or presented. |
| Focus | What the user pays attention to when judging the result. |

## Requirements table

| Problems behind the inputs | Results wanted | Preferences | Focus |
| --- | --- | --- | --- |
| **R01 · Adoption:** Setup takes effort and assumes the current project environment. | A ready-to-use workbench for other brownfield systems. | Simple startup, complete missing-prerequisite guidance, and generic shared components. | Practical adoption and portability. |
| **R02 · Investigation:** Agents ask questions that available knowledge can answer. | Supported answers before human escalation. | Investigate first; reuse known answers; cite sources and confidence. | Useful investigation and less supervision. |
| **R03 · Decisions:** Inputs and answers become scattered or forgotten. | Durable requirements and an efficient clarification loop. | Preserve exact input; batch questions in one editable document; reconcile returned answers. | Decision continuity and answer authority. |
| **R04 · Knowledge intake:** Raw exports and task evidence obscure intended behavior; filtering gets skipped. | A relevant source-to-knowledge pipeline with clear intent boundaries. | Filter first; preserve intended behavior; keep actual gaps separate; update knowledge after clarification. | Processing order, source completeness, and correct knowledge meaning. |
| **R05 · Recovery:** Interruptions and quota outages strand work and unfinished threads. | Resume unfinished work without losing verified results. | Save evidence immediately; reuse checkpoints; preserve the worker settings requested for that dispatch. | Durable progress and actual resumption. |
| **R06 · Case definitions:** Ambiguous or duplicated cases weaken verification. | One precise, reusable definition for each behavior. | Canonical Gherkin, explicit assertions, unambiguous entities, and links from consumers. | Test meaning and traceability. |
| **R07 · Test evidence:** Blocked cases, conflicting statuses, and repeated screenshots reduce trust. | Complete case execution with a faithful review record. | Resolve blockers; reconcile results; retain genuine screenshots for each step. | Execution completeness and authentic step evidence. |
| **R08 · Coverage:** Test totals hide missing requirements and changed behaviors. | Detect important issues before release and expose SDLC coverage. | Separate AC-to-test, AC-to-code, and code-change-to-test mappings; inspect actual assertions. | Behavioral coverage and pre-release detectability. |
| **R09 · Reporting:** Verbose reports and opaque metrics hide the decision. | See the conclusion, failures, risks, and required attention immediately. | Essential information first; explain metrics; highlight failed checks and reasons; use clear tables. | Decision usefulness and reader effort. |
| **R10 · Unit tests:** Delivery confidence can overlook applicable test failures. | All applicable candidate unit tests pass before delivery. | Resolve failures without weakened assertions or unnecessary application changes. | Release discipline and meaningful passing evidence. |
| **R11 · Verification:** Reviews and tooling completion can lack tangible proof. | Demonstrate correctness and useful improvement through observable cases. | Verify changes one by one; use authorized E2E evidence where useful. | Real consequences and verified improvement. |
| **R12 · Environment evidence:** Local results can be mistaken for UAT evidence. | Assess the named environment using matching operational evidence. | Collect remote logs during UAT; retain local-first checks as local evidence. | Environment fidelity and operational observability. |
| **R13 · Connectors:** Analysis can assume access that the real environment forbids. | Useful log and database analysis through permitted access. | Read-only Kibana Console/KQL and PostgreSQL; explain log field mappings. | Connector usability and access boundaries. |
| **R14 · Evidence growth:** Unnecessary artifacts and copied sources increase maintenance effort. | A smaller, understandable collection that preserves necessary evidence. | Review before cleanup; classify material; link raw files instead of duplicating them. | Storage cost, provenance, and reviewability. |
| **R15 · Skill structure:** Large skills are difficult to reuse and verify independently. | Small reusable operations coordinated by parent skills. | Split major steps into reusable units; keep parent orchestrators; review design first. | Composability and verifiability. |
| **R16 · Reprocessing:** Unchanged knowledge consumes repeated model effort. | Incremental updates driven by actual source changes. | Detect changed inputs and reuse completed unchanged work. | Token consumption and processing efficiency. |
| **R17 · Completion:** The user must repeatedly ask for continuation, status, and remaining scope. | Authorized work continues until genuine input is needed, with progress visible. | Keep questions and progress in files; show completed work, remaining scope, and supported ETA limits. | Completion, transparency, and throughput. |
| **R18 · Semantic preservation:** Corrections can remove useful meaning; isolated patches allow recurrence. | Preserve justified facts and prevent related failures. | Retain qualified observations; investigate root cause and similar edits; add systemic prevention. | Semantic fidelity and regression prevention. |
| **R19 · Collaboration:** Design or review requests can become premature implementation. | Agree the requirements and approach before changing the system when requested. | Requirements first, then skill mapping and joint review; respect the authorized phase. | Collaboration and scope control. |
| **R20 · Documentation:** Incremental task reports compete with current system documentation. | A maintained, integrated view across lifecycles and domains. | Keep history in tasks; update stable current docs rather than adding competing documents. | Documentation ownership and discoverability. |
| **R21 · Compatibility:** Migration can break callers or invent an invalid old-role equivalent. | Smooth upgrades with every unavoidable incompatibility exposed. | Preserve upper APIs; inspect data, behavior, and performance; show exact file/line/snippet evidence. | Consumer compatibility and faithful role semantics. |
| **R22 · Tool quality:** Integration can replace native strengths or declare weak output sufficient. | One integrated wiki with detailed, organized, useful output. | Preserve upstream content and native graph; test predefined questions; follow configured engine selection. | Native capabilities and demonstrated output quality. |

## Requirement-to-skill map

Read this table after the requirements table. It maps responsibility without selecting an enhancement.
Existing guidance is not the same as observed reliable behavior.
Shared responsibilities need the active workflow, relevant runtime, and client adapters as applicable.

| Requirement | Main existing owner | Supporting owners or controls | Boundary to review together |
| --- | --- | --- | --- |
| R01 | [repository-onboarding](../../.agents/skills/repository-onboarding/SKILL.md) | [connectors](../../.agents/skills/connectors/SKILL.md); setup, installer, and offline procedures. | Skills assess prerequisites; installation and native-platform readiness need actual target evidence. |
| R02 | [query-knowledge](../../.agents/skills/query-knowledge/SKILL.md); [resolve-knowledge-questions](../../.agents/skills/resolve-knowledge-questions/SKILL.md) | [analyze-requirement](../../.agents/skills/analyze-requirement/SKILL.md); evidence retrieval and applicability. | Known-answer investigation already exists. Check where actual use still repeats questions. |
| R03 | [resolve-knowledge-questions](../../.agents/skills/resolve-knowledge-questions/SKILL.md) | [analyze-requirement](../../.agents/skills/analyze-requirement/SKILL.md); task records; [govern-knowledge](../../.agents/skills/govern-knowledge/SKILL.md). | Preserve exact answers and scope. Grouping must not merge different authorities or contexts. |
| R04 | [prepare-knowledge-sources](../../.agents/skills/prepare-knowledge-sources/SKILL.md); [ingest-knowledge](../../.agents/skills/ingest-knowledge/SKILL.md) | [classify-knowledge-change](../../.agents/skills/classify-knowledge-change/SKILL.md); capture, selection, and claim review. | Filtering, canonical coverage, and intended-versus-actual classification are distinct responsibilities. |
| R05 | Active workflow: [manage-knowledge-lifecycle](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md) or [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md) | Task checkpoints; transition/wiki recovery; native client adapters. | Checkpoint guidance exists. Actual cross-session dispatch and requested settings need independent evidence. |
| R06 | [gherkin-quality](../../.agents/skills/gherkin-quality/SKILL.md) | [analyze-requirement](../../.agents/skills/analyze-requirement/SKILL.md); [validate-sdlc-documents](../../.agents/skills/validate-sdlc-documents/SKILL.md). | Definition quality, executable bindings, and passing execution remain separate. |
| R07 | [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md) | [gherkin-quality](../../.agents/skills/gherkin-quality/SKILL.md); browser evidence procedures; selected test runner/reporter. | Genuine captures and consistent statuses can require adapter or reporter fixes, beyond skill wording. |
| R08 | [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md) | [impact-analysis](../../.agents/skills/impact-analysis/SKILL.md); [gherkin-quality](../../.agents/skills/gherkin-quality/SKILL.md); coverage procedures. | Inspect the three actual mappings. Case counts, links, or line coverage cannot prove equivalence. |
| R09 | Report owner: [release-confidence](../../.agents/skills/release-confidence/SKILL.md), [release-clinic](../../.agents/skills/release-clinic/SKILL.md), or [manage-knowledge-lifecycle](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md) | Shared output standard; selected report renderer. | Ownership follows the report. Separate confidence, failed behavior, recommendation, and required human action. |
| R10 | [release-confidence](../../.agents/skills/release-confidence/SKILL.md) | [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md); owning repository's applicable tests. | A narrower suite or weaker assertion cannot turn an applicable failure into a pass. |
| R11 | [code-review](../../.agents/skills/code-review/SKILL.md); [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md) | Existing behavioral evaluation cases; active workflow owner. | Compare the same baseline/candidate trigger. A local reproduction cannot establish production frequency. |
| R12 | [release-confidence](../../.agents/skills/release-confidence/SKILL.md); [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md) | [connectors](../../.agents/skills/connectors/SKILL.md); runtime-log and deployment comparison procedures. | Bind logs and assertions to the actual build, environment, configuration, and time. |
| R13 | [connectors](../../.agents/skills/connectors/SKILL.md) | Configured read-only resource operations, grants, and private workspace settings. | Verify actual access mode and field semantics. Discovery or catalog metadata cannot prove access. |
| R14 | Shared task and evidence-retention contract | [capture-knowledge-sources](../../.agents/skills/capture-knowledge-sources/SKILL.md); [llm-wiki](../../.agents/skills/llm-wiki/SKILL.md); active workflow. | Review consumers and provenance before cleanup. Preserve meaningful failures, snapshots, and recovery material. |
| R15 | Parent skills: [ingest-knowledge](../../.agents/skills/ingest-knowledge/SKILL.md), [govern-knowledge](../../.agents/skills/govern-knowledge/SKILL.md), [llm-wiki](../../.agents/skills/llm-wiki/SKILL.md) | [manage-knowledge-lifecycle](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md); shared-skill packaging and discovery. | Reusable operations already exist. Identify actual coupling before splitting further or adding another coordinator. |
| R16 | [ingest-knowledge](../../.agents/skills/ingest-knowledge/SKILL.md); [llm-wiki](../../.agents/skills/llm-wiki/SKILL.md) | [prepare-knowledge-sources](../../.agents/skills/prepare-knowledge-sources/SKILL.md); incremental runtime plans and receipts. | Reuse must preserve affected dependencies and semantic quality; receipt activity is not new conversion. |
| R17 | [manage-knowledge-lifecycle](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md) for knowledge; active owner elsewhere. | [analyze-requirement](../../.agents/skills/analyze-requirement/SKILL.md); task progress, question, and checkpoint rules. | Scope blockers locally. Separate accepted distinct work from refreshes before reporting progress or ETA. |
| R18 | [review-knowledge-claims](../../.agents/skills/review-knowledge-claims/SKILL.md); [maintain-wiki-content](../../.agents/skills/maintain-wiki-content/SKILL.md) | [classify-knowledge-change](../../.agents/skills/classify-knowledge-change/SKILL.md); [check-wiki-health](../../.agents/skills/check-wiki-health/SKILL.md). | Claim-removal controls already exist. Check their actual decisions before adding duplicate instructions. |
| R19 | Active workflow owner and task authorization rules | [ponytail](../../.agents/skills/ponytail/SKILL.md) for coding scope; existing review-only routes. | Design-first applies where requested. Existing execution authorization does not require repeated confirmation. |
| R20 | Shared documentation and task-ownership contract | [validate-sdlc-documents](../../.agents/skills/validate-sdlc-documents/SKILL.md); active workflow owner. | Structural validation cannot establish semantic synchronization across current documents. |
| R21 | [code-review](../../.agents/skills/code-review/SKILL.md); [impact-analysis](../../.agents/skills/impact-analysis/SKILL.md) | [ces-migration-scan](../../.agents/skills/ces-migration-scan/SKILL.md) for its specialized scope; [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md). | Preserve actual consumer contracts and performance. Escalate role meaning that cannot fit the old scalar contract. |
| R22 | [llm-wiki](../../.agents/skills/llm-wiki/SKILL.md); [maintain-wiki-content](../../.agents/skills/maintain-wiki-content/SKILL.md) | [openkb](../../.agents/skills/openkb/SKILL.md); [query-knowledge](../../.agents/skills/query-knowledge/SKILL.md); [evaluate-knowledge-retrieval](../../.agents/skills/evaluate-knowledge-retrieval/SKILL.md). | Native graph, engine selection, freshness, detail, and factual support need separate checks. |

`evaluate-harness` remains a proposal in the [earlier plan](06-optimization-plan.md#stage-1--add-a-narrowly-scoped-evaluation-skill).
It does not currently exist and is not a confirmed requirement or mapped existing owner.
The earlier five-skill shortlist does not cover this complete requirement set.

## Scope qualifications

- R03: Latest explicit answers govern intended meaning within their applicable scope. They do not supply publication or deployment approval.
- R04: The [1 November clarification](../workbench-knowledge-intent-boundary-20261101/evidence/knowledge-intent-boundary-20261101/user-input.md#exact-user-input) distinguishes intended knowledge from independent implementation gaps.
- R05: [U0351](evidence/selected-inputs.md#u0351) requested `GPT-6 luna Max` for those resumed threads. It establishes no universal model default.
- R07: Repeated screenshots do not prove separate steps occurred. Missing captures remain explicit gaps, not reconstructed evidence.
- R10: [U0170](evidence/selected-inputs.md#u0170) favored avoiding application changes in that task. Preserve meaningful tests rather than forcing green results.
- R14: Review-first cleanup remains scoped authority. Linking raw inputs does not authorize deleting protected historical payloads.
- R19: This request selects requirements, skill mapping, and joint review before enhancements. No new implementation selection is implied.
- R21: Portal compatibility covers APIs, data structures, downstream-observable behavior, and performance. CES-specific decisions retain their separate scope.
- R21: [U0406](evidence/selected-inputs.md#u0406) prioritizes settings actually used by applications and excludes unrelated dashboard issues from that migration scope.
- R21: [U0410](evidence/selected-inputs.md#u0410) requests two simple role-schema options: a primary role or searchable tags. Neither option is selected here.
- R21: Those two schema proposals should contain only necessary fields, without versioning. This is a scoped preference, not a universal schema rule.
- R22: [U0398](evidence/selected-inputs.md#u0398) selects OpenKB with explicit LLM URL and token; otherwise use llm-wiki-agent.
- R22: [U0375](evidence/selected-inputs.md#u0375) preserves upstream content and its native graph. A dependency graph is not a substitute.

## Source map

Each retained input has one primary row below. The input's original text, date, source locator, and hash remain unchanged.
This index establishes traceability and accounting. It does not prove every interpretation is correct.

| Requirement | Primary retained inputs |
| --- | --- |
| R01 | [U0011](evidence/selected-inputs.md#u0011), [U0218](evidence/selected-inputs.md#u0218). |
| R02 | [U0024](evidence/selected-inputs.md#u0024), [U0152](evidence/selected-inputs.md#u0152). |
| R03 | [U0111](evidence/selected-inputs.md#u0111), [U0114](evidence/selected-inputs.md#u0114), [U0357](evidence/selected-inputs.md#u0357). |
| R04 | [U0029](evidence/selected-inputs.md#u0029), [U0264](evidence/selected-inputs.md#u0264), [U0323](evidence/selected-inputs.md#u0323), [U0326](evidence/selected-inputs.md#u0326). |
| R05 | [U0054](evidence/selected-inputs.md#u0054), [U0340](evidence/selected-inputs.md#u0340), [U0351](evidence/selected-inputs.md#u0351), [U0352](evidence/selected-inputs.md#u0352). |
| R06 | [U0068](evidence/selected-inputs.md#u0068). |
| R07 | [U0098](evidence/selected-inputs.md#u0098), [U0100](evidence/selected-inputs.md#u0100). |
| R08 | [U0139](evidence/selected-inputs.md#u0139), [U0150](evidence/selected-inputs.md#u0150). |
| R09 | [U0142](evidence/selected-inputs.md#u0142), [U0147](evidence/selected-inputs.md#u0147), [U0191](evidence/selected-inputs.md#u0191), [U0202](evidence/selected-inputs.md#u0202). |
| R10 | [U0170](evidence/selected-inputs.md#u0170). |
| R11 | [U0187](evidence/selected-inputs.md#u0187), [U0217](evidence/selected-inputs.md#u0217). |
| R12 | [U0221](evidence/selected-inputs.md#u0221). |
| R13 | [U0228](evidence/selected-inputs.md#u0228). |
| R14 | [U0255](evidence/selected-inputs.md#u0255), [U0378](evidence/selected-inputs.md#u0378). |
| R15 | [U0271](evidence/selected-inputs.md#u0271). |
| R16 | [U0275](evidence/selected-inputs.md#u0275). |
| R17 | [U0298](evidence/selected-inputs.md#u0298), [U0331](evidence/selected-inputs.md#u0331), [U0361](evidence/selected-inputs.md#u0361), [U0368](evidence/selected-inputs.md#u0368). |
| R18 | [U0300](evidence/selected-inputs.md#u0300), [U0302](evidence/selected-inputs.md#u0302). |
| R19 | [U0304](evidence/selected-inputs.md#u0304). |
| R20 | [U0312](evidence/selected-inputs.md#u0312). |
| R21 | [U0348](evidence/selected-inputs.md#u0348), [U0400](evidence/selected-inputs.md#u0400), [U0406](evidence/selected-inputs.md#u0406), [U0410](evidence/selected-inputs.md#u0410). |
| R22 | [U0375](evidence/selected-inputs.md#u0375), [U0385](evidence/selected-inputs.md#u0385), [U0396](evidence/selected-inputs.md#u0396), [U0398](evidence/selected-inputs.md#u0398). |

The latest planning, skills-first, and table requests also inform R09, R15, and R19.
Their exact text remains in the [owning record](01-maintenance.md#scope-and-method).
The separately retained intent clarification supports R04. Neither supplement changes the frozen historical excerpt count.

## Joint review record

Current state: draft requirements and candidate ownership map. No new priorities, targets, or enhancements are selected.
Use the stable requirement ID when correcting a problem, desired result, preference, focus, or skill owner.
Record future answers here with their exact source and date. Do not infer answers from continuation messages.

| Review item | Current recorded answer |
| --- | --- |
| Requirement wording and missing themes | No new answer recorded. |
| Proposed ownership corrections | No new answer recorded. |
| First requirements to improve | Not selected. |
| Evidence needed before changing a skill | Not selected for individual rows. |
| New skill responsibility | Not selected; `evaluate-harness` remains a candidate. |

After this review, inspect the chosen skills against agreed requirements and representative cases.
Then record narrow enhancement options, affected files, expected outcomes, and measurements beside their requirement IDs.
Reuse the existing [plan](06-optimization-plan.md) where supported. Revise its scope and numerical targets from the reviewed requirements.

## Checks and limits

The [table checks](evidence/requirements-table-checks.json) record row accounting, source coverage, current skill links, and document checks.
The source excerpts remain the evidence; this matrix supplies no new business policy, execution result, or implementation authorization.
No skill, runtime, business repository, knowledge record, or wiki content changed for this table.
Named enhancement owners remain unknown until selected. Joint review of this requirements synthesis remains pending.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
