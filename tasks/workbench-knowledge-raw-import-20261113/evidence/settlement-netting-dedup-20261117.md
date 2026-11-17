# Settlement netting source consolidation (17 November 2026)

## Decision

`knowledge/evidence/incoming/Cash Settlement Home Page/` is the proposed current source collection for the duplicated netting material. Owner authority and the effective date remain pending. The `settlement-netting` raw export remains retained as historical evidence. No raw file, retained snapshot, manifest row, audit event, or historical receipt was deleted or rewritten.

## Evidence

- Compared 55 settlement-netting documents with 884 Cash Settlement documents.
- 54 documents are byte-identical duplicates.
- One CCIL page is an older revision. The Cash Settlement revision adds the Stella CCIL test case at lines 158-165.
- Similarity and attachment details are in the ignored [full audit](../../.workbench/duplicate-netting-20261117/similarity/similarity-report.md).
- The complete 55-entry mapping is in [the alias map](settlement-netting-dedup-20261117.json).

## Applied updates

- All 55 `settlement-netting` selections are now `EXCLUDE`, each reason points to its Cash Settlement counterpart, and `sources verify` returns `READY`.
- Fourteen draft candidate records now bind to `source:cash-settlement-home-page/...`; `ai-sdlc --workspace . validate` returns `VALID`.
- The settlement processing ledger records the reviewed exclusion. The fresh plan has 55 unchanged items, zero process items, and zero review items.
- Wiki planning scoped 14 changed canonical records and 89 dependent outputs. The fallback `llm-wiki-agent` compile produced a handoff because no model URL/token is configured. A provenance-only review receipt then advanced the 14 candidate bindings in `knowledge/llm-wiki/source-manifest.json` and `.openkb/hashes.json`; all 89 derived outputs remained byte-identical and prior claim-level review evidence was retained. The [tracked rebind report](settlement-netting-wiki-rebind-20261117.md) records the hashes. `wiki.py verify` and the post-review plan pass.

## Limits and next action

The near-revision decision still needs owner confirmation if the older CCIL snapshot must remain independently applicable. Candidate records remain draft/candidate. Runtime model attestation for the requested GPT-6.1 Sol medium review is unavailable; the recorded review is limited to provenance and unchanged output bytes. Publication, approval, and production behavior remain unverified.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Similarity establishes byte and text overlap, not authority or approval.
  - Wiki compilation was not executed because the configured fallback engine has no model credentials; the manifest update records provenance only.
  - Candidate and wiki state do not establish publication or business execution.
```
