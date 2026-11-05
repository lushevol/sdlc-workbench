# Wiki mode procedures

## Generate or refresh

1. Read the owning workspace instructions and preserve unrelated edits.
2. Declare the selected record set, output directory, evidence directory, and requested questions.
3. Capture the source inventory before editing derived navigation.
4. Read the existing wiki index and overview, when present.
5. Read each selected canonical record in full and inspect its source locators and unresolved questions.
6. Write one source-summary page per selected record.
7. Create or update supported entity and concept explanations across those records.
8. Reconcile the living overview and page catalog.
9. Run health checks, review claim support, and retain compact generation evidence.

Record each canonical path, ID, version, lifecycle, status, and full-file SHA-256 in the external inventory.
Record the upstream skill revision and actual generated page hashes in the same run binding.
Reuse source files at their canonical locations.
Raw snapshots remain evidence behind the selected records; counting them does not establish that they were read.

For refresh, compare complete hashes without truncation.
Follow inbound wiki references to identify affected overviews, entities, concepts, and saved syntheses.
For a deleted or superseded source, preserve its historical identity and label affected navigation before proposing removal.
Do not silently substitute a candidate successor for an applicable published predecessor.
An unchanged input set needs no content rewrite.

Use the supported layout in [the skill entrypoint](../SKILL.md#use-the-supported-wiki-layout).
Navigation pages need no new governance events when canonical records remain unchanged.
If synthesis requires a new rule or changed meaning, stop that change and use the normal knowledge procedure.
Continue other supported pages without filling the unknown.

## Page content

| Page | Useful content |
| --- | --- |
| Source summary | Canonical ID, version, lifecycle, concise summary, key rules, exceptions, open questions, and connected records. |
| Entity | Intended responsibilities, boundaries, collaborators, and unresolved authority or interface questions. |
| Concept | A supported cross-source explanation, relevant conditions, conflicting statements, and links to related concepts. |
| Overview | How the topics fit together, where to start, and which uncertainties limit engineering use. |
| Saved synthesis | The exact question, supported answer, evidence classes, citations, source states, and material limits. |
| Index | Every generated page, its purpose, declared record coverage, and navigation to canonical evidence. |

Label pages as derived navigation.
State actual source lifecycle and status near the top.
Use target-language domain terms where helpful while retaining stable record IDs.
Every consequential claim needs an exact canonical citation.
Read any original evidence used to extend a claim beyond the canonical record.
Do not fabricate quotations or duplicate entire source documents.

## Query

Read the index, relevant wiki pages, and their canonical records.
Inspect cited original sources when the answer requires source authority or details omitted from the record.
Explain intended behavior separately from implementation or observed execution.
Use independent task gaps and exact engineering evidence for actual behavior.

Answer with claim-level citations, source states, confidence, and meaningful unknowns.
Do not treat wiki link density or an inferred relationship as proof.
Save an answer only when the user's request includes reusable synthesis or saving.

## Structural health

Check the following without making model API calls:

- Every generated page has meaningful content and a catalog entry.
- Every selected canonical record has a source summary and an exact identity binding.
- Local links and heading or physical line locators resolve within the selected workspace.
- Every page is reachable from the wiki index; missing references remain explicit.
- Source hashes match the captured inventory; changed inputs invalidate current freshness claims.
- Existing raw snapshots, manifest records, governed records, and audit files retain their protected bytes.
- The wiki contains Markdown navigation only, without unsupported frontmatter or working artifacts.

Keep the health report outside `knowledge/`.
Report missing evidence and unsupported checks explicitly.
Structural health does not establish semantic support or publication approval.

## Semantic lint

After structural health, review representative claims and connections against their exact canonical sources.
Check contradictions, stale synthesis, unresolved applicability, missing exceptions, and unsupported additional behavior.
For complete semantic review, inspect all consequential wiki claims and disclose omitted original-source scope.
Preserve confirmed user clarifications and existing unanswered questions.
Add links to the existing living question document instead of creating competing policy answers.

Use an independent reader for representative retrieval questions when available.
Include a question that has no supported answer and a realistic proposed requirement.
Retain the reader's answers and limits without treating them as business verification.
Only adopt recurring changes into existing skills after their evidence and workflow ownership are clear.

## Graph navigation

Use the existing graph skill's knowledge, references, and bounded paths operations after inspecting resource grants.
Read graph freshness, record lifecycle, endpoint identities, evidence grades, and truncation limits.
An unrebuilt graph may omit new navigation while preserving its prior canonical-record snapshot.
Do not overwrite graph artifacts with the upstream `{nodes, edges, built}` format.
Community and hub suggestions can guide review, but cannot define policy or authorize page creation.
