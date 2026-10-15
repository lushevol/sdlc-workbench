# Understanding responsibility

Understanding converts inspected source material into explicit engineering knowledge.
Keep raw evidence separate from authored explanations.
Record extracted facts, inferences, unresolved questions, and supporting source locators.
Use `KnowledgeTopic` for connected background, domain terms, workflows, and historical evolution.
Classify derived topics for retrieval and preserve source applicability limits.
Keep their project index under `knowledge/candidates/index.md` during investigation.

Draft new knowledge as a candidate before publication.
Use stable IDs for requirements, capabilities, services, contracts, and source references.
Describe expected behavior with measurable Gherkin acceptance criteria.
State preconditions, actions, observable results, and limits.
Do not infer approved intent from current code alone.

Record missing, ambiguous, conflicting, or stale evidence as findings.
Each finding needs evidence, a consequence, an owner, and a next action.
An agent can investigate a candidate through registered tools and exact source inspection.
Important requirements and decisions still require recorded human review before publication.

The [workspace design](../../docs/WORKSPACE_DESIGN.md) defines the folder and traceability contracts.
Agent reasoning supplies interpretation in this stage.
Automatic extraction and understanding remain future capabilities.
Keep justified runtime implementation under `core/`.
