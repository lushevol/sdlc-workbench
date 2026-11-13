# Knowledge graph projection

The graph connects retained knowledge, catalogs, sources, audits, and behavior-review declarations.
Markdown, YAML, source snapshots, and baseline records remain authoritative.
The generated graph provides navigation and bounded queries over those inputs.
It does not publish knowledge or infer missing business rules.

## Inputs and identities

Generator `2.3.0` adds the optional `KNOWLEDGE` dimension within graph schema `2.0.0`.
The `knowledge` envelope records extension version `1.0.0`, input hashes, counts, and limitations.
Legacy snapshots remain readable without that envelope.
New knowledge queries report `NOT_AVAILABLE` for legacy snapshots.

The projection reads these workspace inputs when present:

| Input | Projection |
| --- | --- |
| `knowledge/records/**/*.md` | Records, exact versions, lifecycle states, citations, related IDs, and acceptance criteria. |
| Configured catalogs | Repository, service, capability, contract, and source declarations. |
| `knowledge/evidence/manifest.yaml` | Exact source revisions, hashes, and retained snapshot status. |
| `knowledge/evidence/findings/**/*.md` | Governance findings and their declared subjects. |
| `knowledge/evidence/audit/**/*.yaml` | Immutable events and exact record targets. |
| `relationships/requirement-code/baselines/**/*.json` | Behavior, implementation, assertion, execution, and finding declarations. |

The installed layout resolver also supports legacy workspaces before explicit migration. Canonical discovery selects its resolved record root and does not combine records with evidence or derived wiki pages.

Workspace configuration, local repository mappings, and tool catalogs contribute fingerprints.
Private configuration values and execution grants are not copied into graph properties.
Raw source bodies, assertion text, commands, and result bodies remain in their owning evidence files.
Knowledge titles and declared identifiers support graph search.
Read the cited records for their complete meaning.

Record identities include the declared ID, version, and content hash.
Source identities include the resource, revision, and SHA-256.
Baseline identities retain their baseline and exact record metadata hash.
Repository catalog joins require an exact local path match against the source census.
Names alone cannot establish a join.
Missing and ambiguous references produce explicit unresolved nodes and diagnostics.

## Evidence boundaries

| Relationship | Meaning and limit |
| --- | --- |
| `CITES_SOURCE` | A record cites an exact source revision. Citation does not establish support or authority. |
| `RELATED_TO` | A declared navigation reference. It does not establish a dependency. |
| `HAS_CRITERION` | A record declares the criterion. It does not establish implementation. |
| `SAME_REPOSITORY_AS` | A catalog location matches a source graph repository. It does not establish deployment. |
| `SAME_RECORD_AS` | Baseline intent matches the exact current file hash. |
| `DECLARES_CRITERION` | Baseline behavior binds through exact intent metadata to a declared criterion. |
| `IMPLEMENTED_BY`, `ASSERTED_BY` | Retained baseline claims with their original grades and endpoint binding status. |
| `RETAINS_RESULT`, `DECLARES_ASSERTION_BINDING` | Declared execution links. Passing results do not establish complete business verification. |
| `RECORDS_EVENT_FOR` | An event targets the exact record version and hash. Git does not authenticate its actor. |

Governance state, evidence class, source freshness, binding status, and execution outcome remain separate fields.
Historical baselines without an exact current intent match receive no invented governance state.
Candidate records stay candidates.
No graph path establishes approval, causality, runtime execution, or semantic entailment.

## Build and query

Use the existing installed build command:

```sh
ai-sdlc --workspace PATH graph build
```

The build compares knowledge inventories before extraction and before publication.
Added, removed, or changed inputs abort publication and preserve the previous bundle.
Knowledge declarations reject escaping paths, symbolic links, duplicate identities, and oversized declaration inputs.
Each declaration is limited to four MiB; the input inventory permits at most 20,000 files.

Inspect the resource schema and coverage before querying:

```sh
ai-sdlc --workspace PATH resources
ai-sdlc --workspace PATH call service-dependencies coverage --args '{}'
ai-sdlc --workspace PATH call service-dependencies knowledge --args '{"type":"KNOWLEDGE_RECORD","limit":20}'
```

The direct skill runner exposes the same operations without Workbench action records:

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query --data-dir relationships/service-dependencies/generated knowledge --args '{"governance_state":"published","limit":20}'
```

Copy exact node IDs from results when using `references` or `paths`.

| Operation | Arguments and limits |
| --- | --- |
| `knowledge` | Optional text, type, record ID, owner, and governance state. `limit`: 1–200, default 60. |
| `references` | Required `node_id`; optional direction and governance state. `limit`: 1–200, default 60. |
| `paths` | Required `source` and `target`; optional direction and governance state. Depth: 1–6; results: 1–50; examined transitions: 1–2,000. |

Directions are `in`, `out`, or `both`.
Reference queries default to `both`; path queries default to `out`.
Path defaults are four edges, ten results, and 1,000 examined transitions.
Results retain canonical arrow direction when traversal follows an incoming edge.
Truncation reasons identify result, depth, and traversal limits.
A missing path cannot establish independence.

Lifecycle filters exclude records in other states, including intermediate path nodes.
Sources and catalogs retain no invented business lifecycle.
They remain available as neutral reference endpoints under a lifecycle filter.
Inspect evidence grades and record states along every returned path.

Coverage and new query results expose separate `knowledge_freshness`.
`CURRENT` means captured local input fingerprints match the present inventory.
It does not establish external source freshness, approved intent, or deployment applicability.
`STALE` identifies changed, added, or removed inputs.
`UNKNOWN` means the current inputs cannot be checked.

## Viewer and installation

The generated viewer opens its Knowledge tab when the extension exists.
Search and filter records, select an item, then inspect its direct references and evidence.
The complete record and relationship lists use pagination.
The diagram shows four relationships per page.
The Architecture tab retains the existing system, interface, data, and package views.

This delivery uses existing Python, PyYAML, and jsonschema dependencies.
It requires no graph database, server, API key, LLM, or startup download.
The viewer embeds its assets and makes no external asset requests.
Following source links can require access to their owning files or systems.
Graph queries read snapshots and cannot modify authoritative knowledge.
