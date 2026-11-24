---
name: finalize-wiki-update
description: Complete a reviewed Workbench wiki update with consistent provenance, verification, and coordinated recovery of its two binding files.
---

# Finalize a wiki update

Input: selected source-before hashes, reviewed output receipt, actual engine result, and applicable recovery material.
Keep provenance completion, verification, and recovery in this operation.

## Reviewed completion in either engine

Native compilation records observed bindings and leaves an explicit pending review attempt.
ADE semantic edits also require reviewed completion before unchanged-input skipping is safe.
Use the same [review receipt contract](../llm-wiki/references/workflows.md#reviewed-completion-receipts) for either engine:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py review --receipt .workbench/wiki/RUN/review.json
```

Supply actual reviewer, mode, recipe, source-before hashes, reviewed output hashes, and semantic notes.
Include the summary, index, current dependents, former dependents, and affected explorations from the local plan.
Record supported unchanged summaries and dispositions for withdrawn claims.
Shared output review names all canonical sources whose claims it preserves.
The command checks structure and bytes, retains paired provenance before-images, and writes completion under the existing manifest.
It performs no model call and reads no credentials. Hash declarations do not authenticate a reviewer.
Run [check-wiki-health](../check-wiki-health/SKILL.md) and local planning afterward; report pending work separately.

## ADE provenance completion

This procedure may read/edit the two named provenance files in the selected KB root and `.openkb/`.
It requires no private configuration or authentication-file reads.
This is the Workbench exception to the upstream read-only skill's general state-file guidance.

On resume, inspect the receipt, both provenance files, paired before-images, and current source/output hashes before writing.
An already split pair is incomplete maintenance. Do not finish it by copying the latest source hash.
Restore both before-images only when their attempt matches and current files match that attempt's recorded before/after hashes.
If another writer changed either file, or ownership is uncertain, stop and reconcile without overwriting those changes.
Preserve semantic edits. Rebind and review changed source bytes before a fresh completion attempt.

Use `review --receipt` for coordinated provenance writes instead of manually advancing hashes.
The command preserves unrelated entries and rejects changed bytes, identity conflicts, and incomplete output scope.
Paired recovery material remains under ignored `.workbench/wiki/`.
The two replacements are not crash-atomic. Inspect an interrupted pair and reconcile ownership before retrying.
On failure, preserve semantic edits and inspect pending attempts and the diff.
Do not mark the batch complete or overwrite earlier successful work blindly.
Partial derived edits can remain; the direct compiler route does not provide native `add` batch rollback.

After verification passes, append one truthful `wiki/log.md` operation entry when needed.
Include actual ADE mode, source IDs/hashes, reviewed pages, review result, and supported unchanged dispositions.
Preserve original OpenKB compilation/import identity.
A retry checks the existing receipt/log before adding another entry.
Refresh the [native wiki graph](../llm-wiki/references/workflows.md#wiki-graph) when links changed and graph maintenance is in scope.

## Result and stop conditions

Return source scope, actual edits, source/output hashes, verification findings, completion disposition, and remaining knowledge limits.
Keep source and page changes visible when recovery leaves semantic edits for review.
Hashes identify reviewed bytes; they do not authenticate semantic correctness, human approval, or deployed behavior.
