# Direct ADE wiki maintenance

Use this procedure after the bridge selects llm-wiki-agent and the user authorizes compilation or maintenance. Read the original agent's semantic workflow, then apply this Workbench contract to the shared OpenKB-format files. A printed handoff alone performs no compilation.

## Author complete native-format pages

Native OpenKB compiler prompts ask for body text because native code writes frontmatter. Direct ADE file authoring must create or retain the complete frontmatter below. These Workbench layout and metadata rules take precedence over the original agent's different page types and folders. Original upstream files remain unchanged.

Summary at `wiki/summaries/<source-name>.md`:

```yaml
---
type: Summary
description: One sentence describing this source's contribution.
doc_type: short
full_text: sources/<source-name>.md
---
```

Concept at `wiki/concepts/<slug>.md`:

```yaml
---
type: Concept
description: One sentence describing this focused topic.
sources: [summaries/<source-name>.md]
---
```

Entity at `wiki/entities/<slug>.md`:

```yaml
---
type: Product
description: One sentence identifying this named thing.
sources: [summaries/<source-name>.md]
---
```

Use the actual supported, capitalized entity subtype, such as `Organization` or `Product`. Preserve additional valid fields on existing pages. Saved explorations use the existing `query:` frontmatter. Replace illustrative names and descriptions with the inspected source and actual content. Add a document title, source-status note, meaningful body and wiki-relative links; register each page in the corresponding index section. Keep exact canonical criterion links beside important rules.

## Prepare and perform semantic work

1. Select canonical records and validate them through Workbench. Reject conflicting IDs, duplicate filenames, paths outside the workspace, and the reserved derived subtree. Raw/full-text aliases must be relative symlinks to the selected canonical records; a conflicting alias is an error. Use canonical ingestion/governance to resolve source changes.
2. In a new ignored `.workbench/wiki/<run-id>/` directory, retain the before-images of `source-manifest.json` and `.openkb/hashes.json`. Record each selected source's path, full-file SHA-256, ID, version, status and governance state, plus the previous binding and affected summary/page hashes. Capture the source hash **before** semantic work, after any authorized canonical change.
3. Read each selected source fully. Maintain its summary, relevant concepts/entities, contradictions and index using the original agent's semantic steps. Keep `raw/` and `wiki/sources/` immutable. Do not infer implementation or approval from intended rules. Keep unrelated pages and imported compilation provenance intact.
4. Review the changed claims against their canonical sections. Record the reviewed page paths/hashes, source-before hashes, actual mode `llm-wiki-agent/ADE` and a short review note in the run receipt. If a source changed but its summary did not, record why no semantic page change was needed, such as a metadata-only source change. An unexplained unchanged summary is not completed maintenance.

Hash a selected source or output without displaying its content:

```sh
python3 -c "import hashlib,pathlib,sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())" PATH
```

## Complete provenance after review

This authorized procedure may read/edit only the two named provenance files under `.openkb/` and the KB root; it does not require reading private configuration or authentication files. It is the Workbench-specific exception to the upstream read-only skill's general state-file guidance.

1. Finish all semantic edits first. With other wiki compilers stopped, compare each source's current hash with its recorded before-hash and each reviewed page with its receipt hash. Stop if either changed; investigate and review again. Confirm relative aliases point to that source and all expected summaries exist.
2. Run native local structural checks before changing bindings. From the workspace root on POSIX:

   ```sh
   .venv-openkb/bin/python -c "from pathlib import Path; from openkb.lint import run_structural_lint; print(run_structural_lint(Path('knowledge/llm-wiki')))"
   ```

   On Windows use `.venv-openkb\Scripts\python.exe` with the same arguments. All six categories must report zero findings. This explicit KB path uses no global default or model call. Full bridge verification can still report stale source bindings at this point; that is expected after a source change.
3. For **each reviewed source only**, replace its entry in `source-manifest.json` → `sources`, matching `doc_name`. Set `origin` to the workspace-relative canonical path and `sha256` to the source-before hash; copy `id`, `version`, `status` and `governance_state` from the source. Preserve unrelated entries and all top-level imported engine/version/revision/archive provenance. The following shape is illustrative:

   ```json
   {"doc_name":"<source-name>","origin":"knowledge/candidates/<classification>/<source-name>.md","id":"<canonical-id>","sha256":"<source-before-sha256>","version":1,"status":"draft","governance_state":"candidate"}
   ```

4. In `.openkb/hashes.json`, remove prior entries whose `doc_name` is this source name. Add the reviewed source hash as the key with this value, preserving unrelated entries and rejecting any hash/filename collision:

   ```json
   {"name":"<source-name>.md","doc_name":"<source-name>","type":"md","path":"raw/<source-name>.md","raw_path":"raw/<source-name>.md","source_path":"wiki/sources/<source-name>.md"}
   ```

5. Recheck source/output receipt hashes and run the bridge's `verify`. If writing either state file or verification fails, restore **both provenance before-images**, preserve semantic edits for inspection, and report incomplete maintenance. The two file writes are not crash-atomic; keep their matched before-images until completion. Never advance hashes to hide unfinished semantic work.
6. After successful verification, append one truthful operation entry to `wiki/log.md`: actual ADE mode, source IDs/hashes, reviewed pages, review result and any no-semantic-change disposition. Keep the original OpenKB compilation/import identity. A retry of an already completed run checks the existing receipt/log; it does not invent another compilation. Refresh the original wiki graph when page links change and graph maintenance is in scope.

Report source scope, actual edits, source integrity, native structural findings and unresolved knowledge limits. The receipt and hashes record reviewed bytes; they do not authenticate semantic correctness, human approval or deployed behavior.
