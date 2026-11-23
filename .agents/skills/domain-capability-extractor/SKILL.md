---
name: domain-capability-extractor
description: Extract and maintain reusable system integration capabilities from engineering sessions and retained evidence. Use for domain API contracts, paired request/response examples, detailed workflows, failure lessons, tools, and background knowledge.
---

# Domain capability extractor

Turn inspected engineering evidence into a domain library that another agent can use without the original conversation.
Use ordinary file, analysis, and editing tools. Extraction requires no hooks, learning engine, registry promotion, or experience packet.

## Output and discovery

Use `knowledge/integrations/<domain>/` by default. Honor an explicit project destination.
Read the existing domain index and matching files before writing. Reuse their identities and paths.

```text
knowledge/integrations/<domain>/
├── README.md
├── Contracts/       # APIs, schemas, paired examples, interface dependencies.
├── Workflows/       # Detailed Markdown procedures; optional scripts/ and tools/.
└── Knowledge/       # Background, architecture, conventions, decisions, limitations.
```

Create only files needed by supported discoveries. Do not scaffold empty folders or create another skill for each workflow.
Keep the README compact: domain purpose, applicability, linked contracts, workflows, knowledge, and material gaps.
Use relative links between the three folders. Keep each definition in one place.

## Extract and maintain

1. Identify the domain and requested scope from the current session, supplied history, and owning task.
2. Read relevant user clarifications, source revisions, API exchanges, commands, assertions, and existing domain files.
3. Classify each useful discovery as a contract, workflow, or knowledge item. One task can enrich all three.
4. Read the applicable sections of [construction.md](references/construction.md). Preserve technical detail and useful failures.
5. Merge matching operations, examples, scenarios, and facts. Preserve valid content and flag contradictory evidence with its scope.
6. Check schemas, paired cases, actionable steps, evidence links, and the index. Run applicable existing tools and tests.
7. Save completed files and task evidence as work progresses. Report changed capabilities, actual checks, and unresolved material gaps.

Extract useful contract observations and failure lessons even when the task is incomplete or unsuccessful.
Keep completion and verification limits explicit. A partial procedure must identify its unfinished steps.
When inspected evidence is insufficient, save supported content and ask only questions that materially affect the result.
Do not infer unseen session history or fill absent API fields, errors, policy, or successful results.

## Evidence and authority

Bind material claims and examples to precise source locators, revisions or hashes, observation dates, and applicable environments.
Separate observed behavior, documented requirements, inference, synthetic illustrations, and unknowns.
Use retained real responses for published examples when available. Follow the [paired-example rules](references/construction.md#paired-examples) for redaction and projections.
One observed response does not establish required fields, universal enums, omitted defaults, or behavior in other environments.
Keep meaningful failures and conflicting sources. A correction needs evidence; a suspected cause remains a hypothesis.
Use stable case identities. Repeated extraction should enrich existing files without duplicating content or erasing earlier conditions.

In Workbench, these files are technical integration references, outside canonical `knowledge/records/` and derived wiki ownership.
Link approved business rules by record identity and version. Route new business intent through existing knowledge governance.
Keep full execution history and implementation gaps in the owning task; retain reusable lessons here with exact evidence links.
Extraction does not establish publication, acceptance, deployed behavior, or permission to execute a documented workflow.

## Tools, configuration, and promotion

Every workflow has a detailed Markdown procedure. Add scripts only when they improve a supported, repeatable operation.
Place concrete step scripts under `Workflows/scripts/` and shared domain operations under `Workflows/tools/`, when needed.
Reuse existing connectors for transport, authentication, and grants. Do not build another generic client or execution engine.
Keep variable definitions, types, sources, allowed values, and safe placeholders separate from task-specific values.
Redact credentials, private identities, and sensitive values. Preserve useful domain values, response structure, and source bindings.
Keep private values in ignored configuration. Never repeat a mutation merely to obtain extraction evidence.

Keep domain-specific assets in the domain library. Promote shared guidance only when evidence supports a cross-domain benefit.
Use the existing shared asset and normal source review. Record the target, reason, checks, and before/after hashes in the task.
Do not make extraction depend on that promotion.
