---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Evidence index

> **Critical conclusions: Controlled helpers expose frontend compatibility gaps.**
> Action: review the [required changes](../05-impact-analysis.md#proposed-change).
> Consequence: mapped permissions can fail existing page and action checks.
> Owner: unknown. Evidence: [probe summary](contract-probe-summary.json).

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| USER-001 | Current analysis request | [Exact input](user-input.md#exact-user-input) | 2026-11-05 | a6e329a6323d9542c584481140f1ffbce9773cd4e8b19ef22c55971c7d802097 | High-priority scope; no application edits requested. |
| BFF-001 | Provider contract comparison | [BFF analysis](bff-contract-analysis.md) | 834b4155232222347220e47139a502ee43a9cbdf → 267081800cc28b6af0f8e080fa67c2d5f14d3a26 | [Per-file manifest](source-manifest.json) | 53 changed paths; source and assertions inspected. |
| BASE-001 | Shell consumers | [Base analysis](mfe-base-analysis.md) | 66c6411ade58e4d134e381c2baee8ad3f76a8dbf plus preserved local edits | [Source hashes](mfe-base-source-hashes.json) | Workspace, deep links, shared models, profiles, and configuration. |
| CONTAINER-001 | Shared permission consumers | [Container analysis](mfe-ratan-container-analysis.md) | Filesystem snapshot; no independent Git | [Source hashes](container-source-hashes.json) | Application scope, mixed sources, and role-dependent consumers. |
| PROBES-001 | Actual helper observations | [Canonical cases](../06-test-cases.md); [assertions](contract-probes.cjs); [summary](contract-probe-summary.json) | 2026-11-05 | [Source-bound summary](contract-probe-summary.json) | Four expected diagnostic observations; synthetic payloads; no browser or live CES. |
| PROBE-01 | Workspace and deep-link mismatch | [Result](PROBE-01.json) | 2026-11-05 | cbe0eb7a283a62ba51af04cf1599359cfb0eb27562991a8b1fb2f43f02fe78fe | Legacy accepted; reconstructed CES rejected; saved workspace replaced. |
| PROBE-02 | Application-name mismatch | [Result](PROBE-02.json) | 2026-11-05 | abdf15d8487ecfa4714540c0bed877c898c5f9aa3f2ac8fa13c9934d868acdc3 | Same action grant returns true for legacy and false for CES. |
| PROBE-03 | Mixed source masking | [Result](PROBE-03.json) | 2026-11-05 | 97def21c5f1fce499bd4a1c750e91ef200d51bc794695e1faa0a74bd0e39e1dd | Legacy early return masks CES grant in the fixture. |
| PROBE-04 | Repeated name overwrite | [Result](PROBE-04.json) | 2026-11-05 | b0a7a2811f622e5fefee99d4b5bf724ebdab48d86a6d8923be16b2f5a501d9d3 | Later entity removes earlier action during normalization. |
| GRAPH-001 | Graph applicability | [Coverage excerpt](graph-coverage.json) | Snapshot 2026-11-03T16:10:12Z | 1af788b0e2d60512b9ff3a032c5e6e05d257e902764e3b6443b9cd966df15e9f | STALE for current BFF; direct source used. |
| SOURCES-001 | Exact bytes and non-Git retention | [Source manifest](source-manifest.json) | 2026-11-05 | cc93ccf675468373c9dc44c96e647732b8b10e1a7421f67ed128acf0f0e32ad4 | Three repository identities; 20 source snapshots. |
| CHECKS-001 | Document and evidence validity | [Validation](validation.json) | 2026-11-05 | Recorded in validation | Schema, links, locators, source and snapshot hashes; ASD review remains pending. |
