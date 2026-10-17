# Evidence responsibility

The `core/store.py` implementation retains resource action records and result hashes.
Hashes identify retained bytes; they do not establish business approval or actual execution authenticity.
Keep observations, inferences, and unresolved claims separate.
The [behavior evidence guide](../../docs/BEHAVIOR_REVIEW.md) describes implemented contract, source freshness, and declared assertion-binding checks.
The `core/assurance.py` implementation preserves immutable baselines and compares their declared dependencies.
Its business verification result always remains `NOT_VERIFIED`.
Approval authentication, native result importing, and complete behavior evidence validation require further implementation.
