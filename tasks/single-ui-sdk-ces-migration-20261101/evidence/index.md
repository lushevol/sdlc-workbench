# SDK CES migration evidence

> **Resolve the SDK contract and artifact line before product implementation.**
> Action: complete the [living questions](../01-intake.md#answer-and-question-log).
> Consequence: permission mapping and consumer compatibility remain unresolved.
> Owner: unknown. Evidence: [current assessment](../01-intake.md).

The [current assessment](../01-intake.md) contains the update sequence and three coverage matrices.
No application code, Java build, live CES call, or business case execution forms part of this assessment.

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| SRC-USER-001 | Current investigation scope | [user-input.md](user-input.md) | 2026-11-01 message | `99c868591d697f0d499215583436abd16f0b87c95526da38b8f66dfcbe9a8fb9` | Assessment request; no detailed contract approval. |
| SRC-SDK-001 | Exact EMS2 paths and SDK edit map | [sdk-scope.md](sdk-scope.md) | SDK b0aa82005e7f14202f85f5ef583f25e42da9eeb3 | `3ce1de118a541e74a269897c82f510e6c33426c177453fa3f3ac22843fe6828a` | Source analysis; Java and business checks NOT_RUN. |
| SRC-CES-001 | CES client, authentication, and mapping limits | [ces-reference.md](ces-reference.md) | Auth dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2; BFF 134a340472f29d2a4136e07e516690de6a18e323 | `934014f5e1897af4fc393aef53ce5900c19b61e24ebf8044311a393c8861b9a5` | Source and sample evidence; no approved SDK mapping. |
| SRC-CONSUMERS-001 | Known consumers, versions, and assertions | [consumer-scope.md](consumer-scope.md) | Exact heads in consumer-sources.json | `e2257efb321f35a235bd7125ee84950a43245d3cf4067db476ea0ce33c7d01fa` | Search includes ignored checkouts. Deployment inventory remains incomplete. |
| SRC-API-001 | Static response structure and JSON pointers | [api-shape.json](api-shape.json) | 2026-11-01 inspection; original capture unknown | `d5e2579ca29af538fcd75047f55e82022e7f367b829c8d85edbb3c3890efc145` | One retained sample; no live execution. |
| SRC-FILES-001 | Exact inspected source hashes | [source-manifest.json](source-manifest.json) | 2026-11-01 inspection | `94f1381fecf7710b434e5cc6f79c868ed6fc06d6fa9cafe2e06a407738e4e0ec` | 63 source files; local identities only. |
| CHECK-LINT-001 | Requirement document validation | [intake-lint.json](intake-lint.json) | 2026-11-01 | `f279c0d3ed541950f084815694f0aba23f3013577412b3119b05e5099f610d92` | PASSED with four warnings; owner, review, unresolved content, and writing review remain open. |

Additional evidence: [workspace discovery](workspace-status.json) and [consumer source manifest](consumer-sources.json).
The [document checks](document-checks.json) record links, locators, source hashes, and final lint status.

## Validation

Command: `.venv/bin/ai-sdlc lint tasks/single-ui-sdk-ces-migration-20261101/01-intake.md`.
Result: PASSED, exit code 0, with four warnings.
Unknown ownership, pending business review, unresolved values, and pending ASD review are retained truthfully.
No runtime source changed. Runtime unit tests and wheel builds are not applicable to this documentation stage.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Document checks do not establish business verification or publication approval.
```
