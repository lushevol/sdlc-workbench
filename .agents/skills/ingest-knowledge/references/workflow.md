# Ingestion workflow and harness

The [ingestion orchestrator](../SKILL.md) selects reusable operations.
These stable checkpoints route to their owners; read only the operations needed for the requested scope.
Keep working notes and checkpoint reports in ignored storage until retained evidence is required.

## 1. Define the scope

Record the requested mode, project questions, materials, output paths, and actual access limits.
Review mode produces findings and a topic proposal without source registration or governed changes.
Only ingest materials within the actual request.

## 2. Protect the originals

Use [capture-knowledge-sources](../../capture-knowledge-sources/SKILL.md) for baseline capture, retained revisions, and provenance.
For complete exports, [prepare-knowledge-sources](../../prepare-knowledge-sources/SKILL.md) coordinates capture and selection.
The [source command reference](source-preparation.md) retains CLI and selection contracts.

## 3. Read and trace the evidence

Use [retrieve-knowledge-evidence](../../retrieve-knowledge-evidence/SKILL.md), then [extract-knowledge-claims](../../extract-knowledge-claims/SKILL.md).
The [evidence worksheets](evidence.md) define claim, feature, assertion, and retrieval evidence.
Use [resolve-knowledge-questions](../../resolve-knowledge-questions/SKILL.md) for remaining material uncertainty after investigation.

## 4. Draft the connected knowledge

Use [compose-knowledge-records](../../compose-knowledge-records/SKILL.md) for domain candidates and connected navigation.
Keep actual implementation, deployment, observations, and intent-to-reality gaps outside canonical intent.
Review-only scope ends with the requested findings and proposed topic map.

## 5. Prepare the final content

Use [prepare-knowledge-transition](../../prepare-knowledge-transition/SKILL.md) for final bytes and a `PREPARED` checkpoint.
Use [review-knowledge-claims](../../review-knowledge-claims/SKILL.md) for semantic review before appending final-byte events.
A content correction requires new preparation and affected review.
Preparation does not supply human approval or passing business execution.

## 6. Append the audit events

Use [record-knowledge-audit](../../record-knowledge-audit/SKILL.md) for new immutable events bound to final bytes.
Each changed governed record needs its required current event.
The base validator permits unaudited candidates; the ingestion harness checks the stricter project rule.
Do not edit prepared document bytes after recording their event.
Use new preparation and correction events for later corrections.

## 7. Check usefulness and hand off

Use [check-knowledge-integrity](../../check-knowledge-integrity/SKILL.md) for the final sealed harness check.
Use [evaluate-knowledge-retrieval](../../evaluate-knowledge-retrieval/SKILL.md) for representative questions and one realistic new requirement.
Repeat affected preparation, semantic review, audit correction, and final checks after content repairs.
Report outputs, exact source scope, actual checks, findings, owners, and unresolved decisions.
For registered collection plans, record successful results with [sources complete](source-preparation.md#record-canonical-processing-completion).
This receipt records processing completion; it supplies no publication approval.
Keep canonical publication, wiki freshness, and business execution as separate outcomes.
Follow the owning project's validation and commit instructions.

## Harness commands

```sh
python -m ai_sdlc_workbench.ingestion.harness start --workspace . --output .workbench/ingestion/batch/baseline.json
python -m ai_sdlc_workbench.ingestion.harness check --workspace . --baseline .workbench/ingestion/batch/baseline.json --plan .workbench/ingestion/batch/plan.yaml --phase prepare --output .workbench/ingestion/batch/prepared.json
python -m ai_sdlc_workbench.ingestion.harness check --workspace . --baseline .workbench/ingestion/batch/baseline.json --plan .workbench/ingestion/batch/plan.yaml --seal .workbench/ingestion/batch/prepared.json --output .workbench/ingestion/batch/final.json
```

Choose a new batch directory for a new run. Output paths must be unused.
The harness writes requested checkpoint reports; it does not run business tests or publish knowledge.
If unavailable, report `NOT_RUN` and the actual manual checks performed.

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
When `--seal` is supplied, the report records that checkpoint's exact SHA-256 for downstream completion checks.
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
