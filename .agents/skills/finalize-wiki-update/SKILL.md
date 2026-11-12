---
name: finalize-wiki-update
description: Complete a reviewed Workbench wiki update with consistent provenance, verification, and coordinated recovery of its two binding files.
---

# Finalize a wiki update

Input: selected source-before hashes, reviewed output receipt, actual engine result, and applicable recovery material.
Keep provenance completion, verification, and recovery in this operation.

## Native OpenKB completion

The bridge advances each source's registry and manifest after compilation succeeds and source bytes remain unchanged.
Use [check-wiki-health](../check-wiki-health/SKILL.md) to verify resulting source bindings and structure.
Recheck reviewed source/output hashes and report native semantic review findings separately.
On failure, inspect the per-source results and diff before retrying. Do not mark the batch complete or overwrite earlier successful work blindly.
Partial derived edits can remain; the direct compiler route does not provide native `add` batch rollback.

## ADE provenance completion

This procedure may read/edit the two named provenance files in the selected KB root and `.openkb/`.
It requires no private configuration or authentication-file reads.
This is the Workbench exception to the upstream read-only skill's general state-file guidance.

On resume, inspect the receipt, both provenance files, paired before-images, and current source/output hashes before writing.
An already split pair is incomplete maintenance. Do not finish it by copying the latest source hash.
Restore both before-images only when their attempt matches and current files match that attempt's recorded before/after hashes.
If another writer changed either file, or ownership is uncertain, stop and reconcile without overwriting those changes.
Preserve semantic edits. Rebind and review changed source bytes before a fresh completion attempt.

1. Finish semantic edits. Stop other wiki compilers while completing bindings.
   Compare current sources with their starting hashes and reviewed pages with receipt hashes.
   Stop on either mismatch, investigate, and review again.
   Confirm both relative aliases and all expected summaries.
2. Run [local structural checks](../check-wiki-health/SKILL.md#check-before-advancing-bindings) before changing provenance.
   All six native categories must have zero findings.
   Full verification can still report stale bindings before completion; record that expected condition.
3. Prepare the `source-manifest.json` after-image. Replace each reviewed source's entry by `doc_name` in that prepared data.
   Set `origin` to its workspace-relative canonical path and `sha256` to its source-before hash.
   Copy canonical `id`, `version`, `status`, and `governance_state` without promotion.
   Preserve unrelated entries and imported engine/version/revision/archive metadata.
   Keep the current files unchanged while preparing both after-images.
4. Prepare the `.openkb/hashes.json` after-image. Remove previous entries for that source's `doc_name` in that prepared data.
   Add its reviewed source hash as the key with the existing native entry shape:

   ```json
   {"name":"<source-name>.md","doc_name":"<source-name>","type":"md","path":"raw/<source-name>.md","raw_path":"raw/<source-name>.md","source_path":"wiki/sources/<source-name>.md"}
   ```

   Replace illustrative values. Preserve unrelated entries and reject hash or filename collisions.
5. Recheck source/output hashes and confirm both current provenance files still match this attempt's starting state.
   Record both intended after-image hashes in the receipt before replacing either file.
   Write the two prepared provenance files, recheck source/output hashes, and run full [wiki verification](../check-wiki-health/SKILL.md).
   If either write or verification fails, check recovery ownership as described above, then restore **both provenance before-images** when safe.
   Preserve semantic edits for inspection. Never restore whole files over unrelated concurrent changes.
   Report incomplete maintenance. Never advance hashes to hide unfinished work.
   These two writes are not crash-atomic; retain their matched before-images until completion.
6. After verification passes, append one truthful `wiki/log.md` operation entry.
   Include actual ADE mode, source IDs/hashes, reviewed pages, review result, and supported unchanged dispositions.
   Preserve original OpenKB compilation/import identity.
   A retry checks the existing receipt/log before adding another entry.
   Refresh the [native wiki graph](../llm-wiki/references/workflows.md#wiki-graph) when links changed and graph maintenance is in scope.

## Result and stop conditions

Return source scope, actual edits, source/output hashes, verification findings, completion disposition, and remaining knowledge limits.
Keep source and page changes visible when recovery leaves semantic edits for review.
Hashes identify reviewed bytes; they do not authenticate semantic correctness, human approval, or deployed behavior.
