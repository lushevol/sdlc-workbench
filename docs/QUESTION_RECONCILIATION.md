# Reconcile question answers and knowledge references

Use one living question document for each clarification scope.
The checker identifies missing answer propagation and stale source versions.
It does not answer business questions, change knowledge, or approve publication.

```sh
ai-sdlc --workspace PATH assurance questions --input questions-manifest.json
```

The input identifies selected question documents and consuming knowledge records.
Each document uses its retained workspace path and SHA-256.
Question headings use stable IDs. A question includes its deeper subsections.
Supported resolved statuses are `ANSWERED`, `ANSWERED_FROM_EVIDENCE`, and `RESOLVED`.

```json
{
  "schema_version": 1,
  "questions": [{
    "id": "KQ-ARCH-16",
    "document": {"path": "tasks/example/05-knowledge-questions.md", "sha256": "DOCUMENT_SHA256"},
    "consumers": [{
      "path": "knowledge/candidates/architecture/example.md",
      "sha256": "CONSUMER_SHA256",
      "version": 2,
      "applied_answer_sha256": "ANSWER_SECTION_SHA256"
    }]
  }]
}
```

Replace placeholders with exact lowercase SHA-256 values.
Use the checker output's `answer_sha256` after reviewing the answer and updating its consumer.
Link the consumer to the exact question heading in its living document.
Record the resulting consumer version and file hash.
These references support review. They cannot prove semantic agreement or source authority.

`ACTION_REQUIRED` identifies missing propagation, stale bindings, missing sources, or duplicate entry points.
`REFERENCES_COMPLETE` concerns the declared references only.
Unanswered policy remains unanswered.
Missing consumer declarations keep the scope unknown.
All results retain `verification: NOT_VERIFIED`.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
