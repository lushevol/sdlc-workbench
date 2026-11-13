# Knowledge layout consolidation design

- Status: completed and validated
- Date: 2026-11-13 (Asia/Singapore)
- Scope: `knowledge/` and `evidence/knowledge/` ownership, overlap, consumers, and consolidation
- High-priority references: [original request](../evidence/knowledge-layout-assessment-20261113/user-input.md), then [design-first clarification](../evidence/knowledge-layout-assessment-20261113/design-first.md)
- Inspected source revision: `88efb69a56541fa214f0ac9593a81335a8b4a9b7`
- Existing unrelated work: untracked `core/release-report/`; preserved and excluded
- Implementation authorization: [start migration](../evidence/knowledge-layout-assessment-20261113/implementation-request.md)
- Operation: coordinated runtime, layout, provenance and documentation migration; completed with retained recovery evidence

## Recommendation

Consolidate under one `knowledge/` parent, with three explicit children: `records/`, `evidence/`, and the existing `llm-wiki/`.
The benefit is one discoverable knowledge workspace and a clearer processing pipeline. There is no demonstrated cross-tree storage duplication to remove.
Keep canonical intent, supporting evidence, and derived navigation distinct within that parent.
This changes the current physical layout contract; it does not change business meaning, publication gates, or evidence retention.

```text
knowledge/
├── README.md                       # Ownership and processing contract.
├── index.md                        # One entry point to all three areas.
├── records/                        # Canonical business intent and navigation.
│   ├── candidates/                 # Preserve classifications and candidate states.
│   ├── requirements/
│   ├── architecture/
│   ├── decisions/
│   └── repository-profiles/
├── evidence/                       # Existing evidence/knowledge/ contents.
│   ├── README.md
│   ├── incoming/                   # Ignored, replaceable complete exports.
│   ├── sources/                    # Retained original bytes and revisions.
│   ├── manifest.yaml               # Same source identities and hashes.
│   ├── selections/                 # Source filtering decisions.
│   ├── processing/                 # Reviewed canonical processing receipts.
│   ├── findings/                   # Governance issues, not business rules.
│   ├── audit/                      # Existing immutable events plus new events.
│   └── migration-20261020/          # Preserve existing relocation/recovery material.
└── llm-wiki/                       # Existing single derived workspace.
    ├── raw/                        # Relative aliases to records/, not raw exports.
    ├── wiki/                       # Existing summaries, concepts, entities, index.
    └── ...                         # Existing bindings, native state and ignores.
```

The general workspace `evidence/` directory may continue to serve its other consumers; only its knowledge-specific subtree is in scope.
Business investigation and execution evidence stays under its owning task. Reusable schemas/templates stay under `core/knowledge/`.
Optional plans, generated filtered views, caches, and routine diagnostics stay in ignored working storage.

## What actually overlaps

A SHA-256 inventory found **zero byte-identical regular-file groups shared between the two trees**.
The scan did not follow symlinks or read credential configuration. Counts below exclude `.DS_Store`.

| Current content | Observed inventory | Meaning |
| --- | --- | --- |
| Canonical domain records | 13, all candidates | Curated intent with citations and unresolved limits. |
| Retained original source payloads | 144, all distinct by SHA-256 | Evidence for claims, including older revisions. |
| Derived source summaries | 13 | Short interpretations of canonical records; not duplicate authority. |
| Wiki aliases | 26 relative symlinks | Two engine-facing links for each canonical record; no copied payload. |
| Governance history | 79 immutable YAML events | Exact-byte review/transition history. |
| Governance findings | 2 | Issues tracked outside canonical intent. |
| Selections / processing receipts | 2 / 2 | Different source-preparation and completion contracts. |
| Ignored incoming source pages | 55 | All match retained originals: 806,546 bytes shared within evidence. Replaceable inbox and retained history have different lifecycles. |

Total regular-file inventory: `knowledge/` has 125 files / 1,359,157 bytes; `evidence/knowledge/` has 291 files / 4,321,561 bytes.
These are local inventory totals, including ignored non-secret artifacts; they are not an approved cleanup list.
The scan establishes byte identity, not absence of semantic repetition across prose.

For a representative chain, [the Netting canonical topic](../../knowledge/records/candidates/settlement/KT-settlement-auto-netting.md) synthesizes five original sources and preserves conflicting rules.
[Its wiki summary](../../knowledge/llm-wiki/wiki/summaries/KT-settlement-auto-netting.md) explicitly identifies itself as derived candidate material.
Their shared subject is intentional. [The existing index](../../knowledge/index.md) already links records, source manifest, findings, and audit events across the current split.

## Options considered

| Option | Benefit | Cost and disposition |
| --- | --- | --- |
| Keep current split and improve navigation | Smallest change; existing consumers continue unchanged. | Two physical roots remain. Suitable if navigation is the only problem. |
| `knowledge/{records,evidence,llm-wiki}` | One parent, with an explicit canonical boundary and one wiki. | Recommended consolidation; requires coordinated runtime and provenance migration. |
| Put `knowledge/evidence/` beside current candidate/requirement folders | Fewer record moves. | Still requires consumer changes, and the parent remains ambiguous for recursive canonical scanning. |
| Put all contents into one flat tree | Fewer apparent categories. | Reject: sources, drafts, receipts, mutable imports, and immutable events have different ownership and lifecycle rules. |

## Consumer contract

Only `knowledge/records/` supplies canonical domain documents to validation, ingestion, normal knowledge retrieval, and canonical graph projection.
`knowledge/evidence/` is accessed through the source, provenance, findings, audit, and processing operations that own those artifacts.
The wiki continues to consume selected canonical records through relative aliases. It does not ingest the evidence tree as approved intent.
Snapshot confinement must forbid snapshots inside `records/` while allowing the evidence sibling; workspace confinement and exact-byte hashing remain required.

| Consumer | Current dependency inspected | Required design change |
| --- | --- | --- |
| Validator | [validation.py](../../core/governance/validation.py):190–233, 248–297 | Change canonical root and evidence paths together. Keep schema, hash, confinement, and governance checks. |
| Knowledge provider | [knowledge.py](../../core/providers/knowledge.py):64–94 | Resolve canonical storage to `records/`; prevent evidence/wiki from entering ordinary domain retrieval. Preserve explicit supported provider configurations. |
| Source preparation | [sources.py](../../core/ingestion/sources.py):26, 90–145, 327–392 | Resolve manifest/selections/snapshots/inbox beneath the new evidence root; find dependents only within canonical records. |
| Incremental processing | [incremental.py](../../core/ingestion/incremental.py):46–55, 233–259, 440–459 | Use new record/receipt paths; classify old bindings as requiring migration/review rather than asserting completion. |
| Ingestion checkpoints | [harness.py](../../core/ingestion/harness.py):120–144, 190–200 | Preserve historical checkpoints; make new baselines use the new roots and retained history. |
| Service graph | [knowledge_projection.py](../../.agents/skills/service-dependencies-graph/tools/knowledge_projection.py):110–200, 376–389, 482 | Keep canonical records, findings, sources, and events separately typed; prevent evidence Markdown becoming canonical nodes. |
| Wiki bridge | [wiki.py](../../.agents/skills/llm-wiki/scripts/wiki.py):204–247, 351, 394, 599, 664–685 | Preserve the wiki location/pages; update canonical discovery, aliases, origin paths, and checked completion bindings. |
| Init and distribution | [workspace.py](../../core/workspace.py):93–127; [scaffold.json](../../scaffold.json):38–47 | Generate the consolidated empty layout; package guides, not live source snapshots or project records. |
| Agent instructions and ignores | [AGENTS.md](../../AGENTS.md), architecture/design/lifecycle guides, affected skills, [.gitignore](../../.gitignore):8–23 | Explain the new canonical boundary consistently; keep incoming exports, secrets, and runtime state ignored. |

Use one small shared layout resolver for the two fixed supported layouts instead of adding independently configurable paths for every operation.
New initialization should create the consolidated layout. Existing workspaces must remain usable until explicitly migrated.
Resolve the layout from the unique active source manifest location; both manifest locations present is an ambiguous migration state requiring diagnostics/recovery, never automatic union or precedence.
A consolidated layout must also contain its canonical `records/` directory; report incomplete layouts instead of falling back silently.
The compatibility route must read the existing tree, not copy it into a second authoritative tree or create broad directory aliases.
CLI/MCP operation names and business record/source identities remain stable; the intended filesystem paths change through the migration.

## Migration and recovery design

1. Record the selected layout, exact worktree/source revision, affected files, source/record/audit hashes, existing receipt bindings, and authorized scope. Exclude unrelated work. Use one migration locator map rather than duplicate full payload inventories.
2. Update and check path consumers in an isolated fixture before relocating live content. Do not temporarily weaken checks so mixed storage passes.
3. Relocate canonical folders and the knowledge evidence subtree using the old-to-new map. Preserve every retained source and prior audit event byte. Keep source `id`, `resource`, `revision`, and `sha256` unchanged; update active `snapshot` locators and necessary operational bindings only. A historical `resource` string is an identity, not a path to mass-rewrite.
4. Repair active Markdown links, registry/provider references, wiki aliases, and ignore rules. Preserve previous manifest bytes and existing relocation material. Append an actual relocation event with its supporting map; do not rewrite prior events, frozen receipts, or historical reports.
5. Where active canonical Markdown links must change, its full file hash also changes. Review those final bytes and use the existing supported governance procedure for required successor/review/transition evidence. Do not reuse approval for an old hash. Candidate status does not become approved during migration.
6. Replan source processing against the new paths. Rebind or re-establish current receipts only after their source selections, dependencies, output bytes, and required reviewed checkpoints agree. Reconcile wiki origins/relative links through the existing bridge and verify outputs; moving files alone does not establish semantic completion.
7. Build a fresh graph/checkpoint for the migrated layout. Retain earlier baselines as historical evidence. Remove the old active directory only after all migration checks pass and the locator map provides historical recovery. No payload deduplication or history cleanup is part of this change.

Recovery restores the coherent prior manifest, paths, and dependent bindings using the migration map and pre-migration revision.
Prior immutable history remains intact; any events already appended during the attempted migration remain truthful history and require corrective follow-up rather than deletion.
Migration must have a clear interruption/recovery procedure because moving both roots and updating bindings is not inherently crash-atomic.

## Required validation before implementation delivery

- Canonical record IDs, states, source identities, retained source count, and historical audit hashes reconcile with the migration baseline; every path-only change is explained.
- Evidence and wiki content never enter canonical validation/retrieval as business records. Snapshot bytes and workspace confinement checks remain effective.
- Existing legacy workspaces and new empty consolidated workspaces operate through the same supported CLI/MCP contracts; ambiguous or incomplete layouts produce actionable diagnostics.
- Source refresh, selection verification, incremental plans/completion, ingestion checkpoints, and protected source/history tests pass for their affected contracts.
- Wiki aliases resolve to the same record IDs; native structure, source/output bindings, and reviewed completion are checked through the existing bridge. No model compilation is required solely to move a path when the supported rebind operation can preserve verified output.
- Graph projection keeps the expected canonical identities and separately typed provenance; no duplicate authority or dangling active locators appears.
- Applicable complete unit suites, wheel/scaffold checks, and installed empty-workspace checks pass after implementation. No tests are waived because this is a directory change.

## Outcome, confidence, and next action

**Feasible, with moderate migration risk:** one physical parent can preserve all three lifecycle boundaries. High confidence in the layout assessment and lack of cross-tree exact duplicates; migration correctness remains unverified until implementation and the checks above.
Current stage is completed harness migration. Canonical states, versions, business prose, and publication disposition are preserved.
Implementation was authorized by [the migration request](../evidence/knowledge-layout-assessment-20261113/implementation-request.md). The coordinated migration and final delivery checks are complete. Use [the consolidated index](../../knowledge/index.md) for records, evidence and the wiki; knowledge review and publication decisions remain separate.

The design-stage probe could not use the default system Python. Implementation checks use the existing project `.venv` and isolated `.venv-openkb` runtimes; neither requires dependency installation or model calls.


## Implementation evidence and disposition

- [Exact migration authorization](../evidence/knowledge-layout-assessment-20261113/implementation-request.md)
- [Old-to-new locator and hash map](../evidence/knowledge-layout-assessment-20261113/relocation-map.json)
- [Original manifest bytes](../evidence/knowledge-layout-assessment-20261113/manifest-before.yaml)
- [Origin-only wiki relocation receipt](../evidence/knowledge-layout-assessment-20261113/wiki-relocation-receipt.json)
- [Exact Git proof for source/output locator changes](../evidence/knowledge-layout-assessment-20261113/wiki-locator-proof-receipt.json)
- [Final validation and source/test bindings](../evidence/knowledge-layout-assessment-20261113/validation.json)
- [New immutable relocation event](../../knowledge/evidence/audit/AUD-20261113-knowledge-layout-relocation-v1.yaml)

The map contains the pre-edit hashes and the path-repair checkpoint hashes. Its active manifest after-hash precedes registration of the two migration-evidence sources, avoiding a self-referential final manifest hash. All 556 prior source records were reconciled with only their applicable snapshot locators changed. The final manifest also records authorization and relocation evidence as two new sources.

All 144 retained original payloads and 79 earlier audit events retain their original bytes. Both old processing receipts retain their exact bytes under `knowledge/evidence/migration-20261113/processing/`; active processing queues require new reviewed completion rather than reused invalid paths.
All 13 canonical records retain their IDs, versions, metadata, candidate/draft states and business prose. Their only changes are Markdown local destination strings. The same exact Git comparison proved locator-only changes in 46 derived wiki pages.
Wiki relocation preserves existing semantic recipes, review actors/times, missing receipts and pending attempts. It changes observed source/output hashes only where exact prior Git bytes match the existing observation and the complete diff passes the local-destination proof. Prior-stale observations reject rebinding.

| Check | Current result |
| --- | --- |
| Workspace validation | `VALID`; 15 documents, zero findings. |
| Source verification | Portal 85 pages and Netting 55 pages; zero binding findings; one existing HOLD page per collection remains review-required. |
| Source processing plans | Portal: review 1 / process 80 / unchanged 4. Netting: review 1 / process 41 / unchanged 13. No semantic completion inferred from relocation. |
| Ingestion checkpoint | `PASSED`; 13 selected records, 372 local links, 173 line fragments, one new relocation event, zero findings. This is explicitly a post-relocation baseline. |
| Wiki structure/bindings | Verified 13 linked canonical sources; zero structural findings. Default-recipe plan: 12 unchanged and one recipe mismatch for Netting; prior recipe IDs remain intact. |
| Service dependency graph | Rebuilt and validated: 9,440 nodes, 23,243 edges, 11 repositories. Static declarations do not prove runtime relationships. |
| Core focused regressions | 99 passed; source-hash corruption and evidence-alias rejection probes also passed. |
| Packaging regressions | 30 passed, including sdist → wheel → clean workspace. |
| Complete unit suite | 1,067 run: 1,065 passed, zero failures/errors, two optional connector integrations skipped. Final source includes all review corrections. |
| Wheel and installed workspace | Built wheel `bb8b522a19304411fc97490e544ecbffc189c4b4bb22edfb546caa98f18276fc`; installed outside the checkout and initialized an empty consolidated workspace: `VALID`, zero documents/findings. |

The first full run exposed a missing sdist include, old-path fixtures, and standalone import-denial handling; those defects were corrected. Mock HTTP server errors in that run were sandbox `socket.bind` denials. A later full run passed 1,060 tests with two optional connector integrations disabled. Subsequent independent review tightened code-literal exclusion, absolute-path rejection, and baseline alias handling in the locator proof; the final 1,067-test run and matching wheel include those corrections. The two optional Node connector tests are outside this layout change and require explicit connector integration configuration.

Pre-migration preservation is established by the original map hashes, exact prior Git blobs, and archived manifest. The new harness baseline is not presented as a pre-edit checkpoint. No business publication, deployed behavior, model compilation, or live external connector verification is claimed.

## Scoped implementation traceability

These are harness layout contracts from the approved design. They define no new business behavior. The matrices establish inspected links and assertions; they are not a percentage claim of business conformance.

| Contract → test/assertion | Inspected assertion evidence |
| --- | --- |
| L1: Resolve one layout; reject ambiguity/incompleteness | `test_knowledge_layout`: existing roots and incomplete/dual layout tests. |
| L2: Initialize and package only the empty consolidated workspace | `test_workspace_layout`: clean initialization, project exclusion, full sdist/wheel initialization. |
| L3: Keep evidence/wiki outside canonical validation/retrieval/projection | `test_knowledge_layout` consumer exclusion and snapshot rejection; graph consolidated projection test; independent corruption/evidence-alias probes. |
| L4: Preserve source filtering, planning, completion and checkpoint contracts | Consolidated refresh → selection → plan → receipt → skip/view/checkpoint assertions, plus explicit legacy suites. |
| L5: Preserve retained sources, old audits, original receipts and canonical meaning | Live relocation assertions for every mapped file; 144 source payloads, 79 prior events and two receipt hashes; 13 exact metadata/prose comparisons. |
| L6: Rebind wiki paths without inventing semantic review | OpenKB relocation/proof tests: legacy/unified paths, stale hashes, missing receipts, pending attempts, idempotence, conflicts, rollback, prose/code-literal/absolute-path rejection and alias handling. |

| Contract → code change | Implementing boundary |
| --- | --- |
| L1 | `core/knowledge_layout.py`; standalone wiki/graph fallback selectors. |
| L2 | `core/workspace.py`, `scaffold.json`, `MANIFEST.in`, `.gitignore`. |
| L3 | Governance validator, canonical provider and graph projection canonical roots. |
| L4 | Source preparation, incremental processing and ingestion harness root resolution. |
| L5 | Relocation map, active locator repairs, archived original manifest/receipts and new relocation event. |
| L6 | Wiki canonical discovery, `relocate` operation and exact Git/local-destination proof. |

| Changed unit → direct test/assertion | Classification |
| --- | --- |
| Shared layout resolver → root selection and ambiguity/incomplete assertions | Runtime compatibility. |
| Initializer/scaffold/sdist manifest → clean workspace and distribution assertions | Supporting maintenance. |
| Validator/provider/graph roots → evidence/wiki exclusion and confinement assertions | Consequential trust boundary. |
| Sources/planner/harness → consolidated pipeline plus legacy fixture assertions | Runtime compatibility. |
| Wiki aliases/binding writer/proof → stale/conflict/rollback/code/prose/absolute-path/alias assertions | Consequential provenance boundary. |
| Canonical/source/audit/receipt locator migration → exact-byte reconciliation and source identity/prose assertions | Path-only maintenance. |
| Guides/task navigation/wiki page links → destination checks, canonical checkpoint and native wiki lint | Navigation maintenance; no business meaning change. |

Denominators: six scoped layout contracts mapped to implementation and inspected assertions. Five have unit/integration assertions; L5 additionally uses the live exact-byte reconciliation. Execution outcomes are reported separately above. Test-only legacy fixtures preserve old-layout coverage; unchanged business sources and existing governance gates remain required dependencies. No unsupported additional business behavior was found in the path-only canonical comparison.
