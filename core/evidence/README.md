# Evidence responsibility

The `core/store.py` implementation retains resource action records and result hashes.
Hashes identify retained bytes; they do not establish business approval or actual execution authenticity.
Keep observations, inferences, and unresolved claims separate.
The [behavior evidence guide](../../docs/BEHAVIOR_REVIEW.md) describes implemented contract, source freshness, and declared assertion-binding checks.
The `core/assurance.py` implementation preserves immutable baselines and compares their declared dependencies.
Its business verification result always remains `NOT_VERIFIED`.
The [review index](../../docs/REVIEW_INDEX.md) also reconciles retained browser inventories and original Jest JSON records.
Those imports do not authenticate execution. Broader native formats, approval authentication, and complete semantic behavior verification remain outside these deterministic checks.
