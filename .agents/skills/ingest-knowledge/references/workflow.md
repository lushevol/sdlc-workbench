# Ingestion workflow and harness

Use these checkpoints in order.
Keep batch notes in ignored working storage until a report needs retention.

## 1. Define the scope

Input: the user's request, workspace instructions, and available materials.

1. Inspect worktree changes and preserve work from other tasks.
2. Record the mode, source paths, project questions, and requested outputs.
3. Record permitted external access and business execution from the actual task.
4. Name evidence limits, owners, and missing inputs without guessing.

Output: a short scope statement and question list.
Completion: each planned output answers a requested project question.
Do not import materials merely because they exist.
Derive only reusable business-domain knowledge, including technical explanations of business-system behavior or responsibilities.
Exclude Workbench maintenance, logs, raw sources, code copies, fixtures, execution results, reports, and intermediate files from `knowledge/`.

## 2. Protect the originals

Input: selected source locations and the current workspace.

1. Run the harness `start` command before editing raw sources, knowledge, or audit records.
2. Inventory source paths, hashes, titles, available dates, revisions, and authority.
3. Identify empty pages, duplicate content, missing attachments, and unread files.
4. For ingestion, reuse originals under `evidence/knowledge/sources/`. Append new records to `evidence/knowledge/manifest.yaml`.
5. Register an actual source collection through the supported catalog contract when needed.

Output: the baseline checkpoint, inventory, and source manifest additions for ingestion.
Completion: every source used for a derived record has an exact manifest reference and permitted retention.

Original Markdown needs no Workbench frontmatter.
For an export without original revision metadata, use `sha256:<digest>` and state that limitation.
Do not initialize Git merely to identify supplied files.
Pasted documents use filesystem provenance; links do not establish remote retrieval.
If a retained original changed, recover its predecessor before deriving new claims.
Add a separate snapshot for changed source content.
When full-file retention would expose secrets, retain permitted contiguous excerpts and record the omitted scope.
Record original source ranges and hashes without rewriting the original file.
Keep credentials, tokens, and unnecessary personal examples out of synthesized knowledge.

## 3. Read and trace the evidence

Input: protected sources and the project questions.

1. Read source contents, including cited ranges and relevant surrounding conditions.
2. Fill the claim worksheet in [the evidence guide](evidence.md).
3. For implementation questions, trace callers, providers, configuration, state, and failure paths at exact revisions.
4. Inspect assertion setup, invocation, expected predicates, mocks, and imported test keywords.
5. Resolve code questions from code; ask the user for remaining intent or policy.

Output: supported claims, conditional inferences, and consequential unresolved findings.
Completion: each important claim has inspected support and an explicit evidence class.

Missing environments limit execution; they do not block a static baseline.
Missing attachments remain missing; filenames cannot establish their contents.
Keep excluded secrets and unavailable dependencies beside the affected claim.
A branch name, class name, or comment cannot replace its actual predicate.

## 4. Draft the connected knowledge

Input: supported claims and recorded unknowns.

| Type | Choose when |
| --- | --- |
| `KnowledgeTopic` | Explaining background, terms, workflows, or historical evolution. |
| `Architecture` | Explaining components, responsibilities, interfaces, and dependencies. |
| `Requirement` | Recording confirmed intended behavior with measurable acceptance criteria. |
| `Decision` | Recording an actual choice, alternatives, rationale, and consequences. |
| `RepositoryProfile` | Describing an inspected repository's responsibilities and entry points. |
| `GovernanceFinding` | Retaining a consequential unresolved issue for investigation. |

Copy the selected shipped knowledge template and follow its schema.
Group by project question; one source can support several topics.
Several sources can support one topic.
Preserve each source's revision, applicability, purpose, and uncertainty.

Save new concept drafts under `knowledge/candidates/<classification>/` with stable IDs.
Save `GovernanceFinding` records under `evidence/knowledge/findings/`, outside the domain knowledge base.
Keep logs, assertions, execution captures, and investigation reports under the owning task.
Keep harness checkpoints in ignored working storage or retained task evidence.
Use `governance_state: candidate`, `status: draft`, and `verified: []`.
Mark an unavailable owner `unknown`.
Reuse unchanged records; increment a version when its content or scope changes.
Preserve unresolved predecessor knowledge and findings.

Create `knowledge/candidates/index.md` with topic purpose, state, links, and evidence limits.
Keep the reusable `knowledge/index.md` free from live project records.
Use declared registry IDs only where the inspected relationship supports them.
Declarations do not prove runtime integration or execution permission.

Requirements need matching structured criteria and readable Gherkin scenarios.
Separate business thresholds from controlled test fixtures.
If a required business limit is unknown, retain the question instead of inventing a number.
Keep unsupported criteria outside the confirmed acceptance list and state incomplete scope.

Review mode produces the requested findings and proposed topic map here.
It creates no source registrations or governed records automatically.

## 5. Prepare the final content

Input: drafted outputs and a harness plan.

1. Reconcile descriptions, tables, metadata, scenarios, finding status, and review summaries.
2. Finish writing and formatting, including trailing whitespace and file endings.
3. Perform applicable writing checks and set their actual result.
4. Keep `asd_review: PENDING`, `reviewer: null`, and `reviewed_at: null` without a complete ASD review.
5. Run the harness with `--phase prepare` and fix its failed checks.
6. Perform semantic review using the claim worksheet and cited contents.

Output: final proposed bytes and a `PREPARED` checkpoint.
Completion: structural and evidence checks pass within the preparation scope, and remaining decisions are explicit.

Preparation can defer a selected record's missing transition event.
The report keeps the actual workspace validation result and names deferred findings.
Preparation cannot supply verification or human approval.
After a content correction, create a new prepared checkpoint and repeat the affected review.

## 6. Append the audit events

Input: final proposed bytes and actual review evidence.

1. Compute hashes after all content, metadata, and formatting changes.
2. Create new files under `evidence/knowledge/audit/` using the shipped contract and permitted lifecycle transitions.
3. Bind each event to its final item path, ID, version, hash, and exact evidence sources.
4. Record only actual actors, times, reviews, and approvals.
5. Preserve existing events, including events that need correction.

Output: new immutable event files and unchanged prepared document bytes.
Completion: each changed governed record has a current event, as required by this project's instructions.
The base validator permits unaudited candidates; the harness checks this stricter project rule.

Use `previous_event_id` when a new event corrects an earlier event.
An explicit correction chain can preserve an earlier hash and bind its replacement to current bytes.
Do not change document text or writing metadata after creating its event.
If that occurs, prepare a new version and event without rewriting the earlier event.
Use [the governance skill](../../govern-knowledge/SKILL.md) for a requested state change or publication.

## 7. Check usefulness and hand off

Input: prepared documents, new events, and retained evidence.

1. Run the final harness check with `--seal` pointing to the prepared checkpoint.
2. Ask an independent reader to answer representative project questions from the classified index.
3. Ask the reader to locate context for one realistic new requirement.
4. Repair unsupported answers and record unresolved gaps.
5. Report actual checks, scope, generated paths, findings, and owner decisions.

After a document repair, repeat preparation, append required correction events, and run final validation again.

Output: a final check report and a retrieval result with explicit limits.
Completion: selected questions have supported answers or clearly identified gaps.
Publication and business execution remain separate outcomes.

If delegation is unavailable, perform the retrieval exercise yourself and disclose that limitation.
Do not claim that an independent reader or a smaller model ran when it did not.
Follow the owning project's validation and commit instructions.

## Harness commands

The installed module owns deterministic checking under the single Workbench runtime.
It does not perform automatic source ingestion or semantic classification.
Use the same Python environment that provides `ai-sdlc`.
From this source checkout, `.venv/bin/python` can replace `python` when that environment is available.

Copy [the plan template](../assets/check-plan.yaml) into the batch directory.
Replace document paths and keep machine locations in ignored storage.

| Plan field | Meaning |
| --- | --- |
| `schema_version` | Use `1`. |
| `documents` | Selected output Markdown paths, relative to the workspace. Include the project index. |
| `repositories` | Declared repository ID to local checkout path, for exact Git comparisons. |
| `executions` | Retained passing JSON results used by this batch's execution claims. |
| Execution `result` | Workspace-relative retained result path. |
| Execution `repository_id` | Repository ID from the plan's mapping. |
| Execution `revision` | Expected full Git commit ID. |

Empty repository mappings and execution lists are valid for document-only work.
When citing code, supply the repositories needed to compare captured bytes.
Missing repository mappings remain explicit unchecked scope.
Execution JSON needs `status: PASSED` and nonempty `source_sha256` file-to-hash entries.
Other result formats require manual inspection; do not relabel them as compatible executions.
Keep failed and stale results as history without selecting them as passing support.

`start` captures existing raw files, manifest history, audit bytes, and governed document hashes.
`check` reuses Workbench validation and adds retention, locator, execution-hash, and prepared-content checks.
The first source addition can replace an empty manifest list with a populated list.
Existing source records and nonempty manifest prefixes must remain unchanged.
Physical `#L1-L5` fragments refer to lines inside the linked snapshot.
Original source ranges belong in source metadata and the surrounding explanation.
Unsupported heading fragments and external destinations remain unchecked limits.

| Result | Required response |
| --- | --- |
| `PREPARED` | Review these bytes, then append required events and run the final check. |
| `PASSED` | Report the passed deterministic scope and remaining semantic or execution limits. |
| `FAILED` | Read findings, repair the affected input, and write a new checkpoint report. |
| `NOT_RUN` | State why the harness was unavailable and list manual checks performed. |

| Failure | Repair |
| --- | --- |
| Raw or manifest history changed | Recover original bytes and append a new snapshot or record. |
| Existing audit changed | Restore the event and add a new correction event. |
| Link or line range missing | Find the correct retained source and repair the citation. |
| Execution hash differs | Mark the result stale; rerun permitted checks against final code. |
| Prepared content changed | Create a new prepared checkpoint and repeat the affected review. |
| Changed record lacks an event | Append its required current event after final preparation. |
| Required decision missing | Ask the user or owner; keep the affected claim unresolved. |

Never fix a check by weakening the claim silently or editing retained evidence to match it.
State any intentional scope reduction in the handoff.
