# Knowledge standards

Use the Workbench profile of [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
Upstream OKF requires `type`. This profile adds mandatory domain fields and governance checks.

Keep original sources unchanged. Record each source revision in `raw/manifest.yaml`.
Keep derived candidates in `candidates/`. Keep accepted documents in the relevant domain directory.
Store governance findings in `findings/` and audit events in `audit/`.

Ingestion classifies original materials and connects their meaning across project topics.
Use `KnowledgeTopic` for background, terms, workflows, and historical explanations.
Keep source classification separate from derived topic classification.
Classification alone does not establish source authority or current applicability.
The [ingestion skill](../.agents/skills/ingest-knowledge/SKILL.md) supports review and ingestion modes.

## Document contract

Each instantiated Markdown document starts with YAML frontmatter.
Required fields are `type`, `id`, `version`, `owner`, `governance_state`, `status`,
`sources`, `generated`, and `verified`. Use a positive integer for `version`.
Use a stable ID with letters, digits, dots, underscores, or hyphens.

Keep OKF `status` as `draft`, `stable`, or `deprecated`. Use `governance_state`
for `candidate`, `investigated`, `verified`, `published`, `contested`, `stale`, or `superseded`.
These fields have separate meanings. Extra OKF extension fields are permitted.

Each `sources` entry requires `resource`, `revision`, and lowercase hexadecimal `sha256`.
The three values must match a raw manifest record.
`generated` requires `by` and `at`. Each `verified` entry requires `by` and `at`.

Quote each timestamp. Use ISO 8601 with a timezone, for example `"2026-10-14T00:00:00Z"`.
An empty `verified` list is permitted for a candidate. Verification must follow generation.

The [schemas](schemas/) define required domain fields. The [templates](templates/)
show complete illustrative records. Each domain also requires these level-two body headings:

| Type | Required fields and body headings |
| --- | --- |
| `KnowledgeTopic` | Classification, scope, summary, related IDs, and open questions; body: Scope, Summary, Documented knowledge, Connections, Evidence limits, Open questions. |
| `Requirement` | Description, Rationale, Acceptance criteria |
| `Architecture` | Scope, Components, Interfaces, Dependencies, Decisions |
| `Decision` | Context, Options, Decision, Rationale, Consequences |
| `RepositoryProfile` | Purpose, Scope, Responsibility, Components, Contracts, Dependencies, Languages, Entry points, Validation commands; frontmatter also requires `repository_id` |
| `GovernanceFinding` | Subject, Evidence, Proposed action, Resolution; frontmatter also requires `category` and `severity` |

Required headings must occur outside Markdown code fences and contain text.
Keep structured frontmatter and body content consistent during human review.
The structural checker does not compare their meaning.

Classified drafts use `candidates/<classification>/` and retain the normal candidate lifecycle.
An ingested project's `candidates/index.md` lists its topics, purposes, review states, and evidence limits.
This project-specific index is navigation and does not grant approval.
The reusable `index.md` remains a generic guide for new workspaces.
Only reviewed knowledge with the required evidence can support a source-of-truth claim.

Requirements need at least one actionable acceptance criterion. Each criterion has
`id`, `given`, `when`, `then`, and `measure`. Start the clauses with `Given`, `When`,
and `Then`. A measure has `metric`, `operator`, numeric `value`, and `unit`.
Operators are `equals`, `at_least`, `at_most`, `less_than`, and `greater_than`.

Use an observable count, duration, size, or numeric code. Human review must confirm
that the clauses and measurement describe the intended behavior.

## Raw source manifest

`raw/manifest.yaml` contains `schema_version: 1` and a `sources` list.
Each record requires `id`, `resource`, `revision`, `sha256`, `ingested_at`, and `classification`.
Classify sources as `business`, `architecture`, `decision`, `implementation`,
`deployment`, or `verification`. Use `unknown` or `mixed` when review cannot assign one class.

Retain each prior revision. A stable source ID may occur once per revision.
One resource and revision must have one recorded hash.
Keep resource names at their original locations. A resource name does not grant tool access.

An optional `snapshot` is a path relative to the workspace. It must stay within
the workspace and cannot contain `..`. Validation hashes snapshot bytes without
normalization. It never opens or fetches the external `resource` value.
Without a snapshot, validation checks the recorded reference only.

## Review gates

A candidate may omit audit events. Each other state requires a matching transition
event for its current ID, version, state, and full Markdown file SHA256.
Verified and published records also need a verifier entry with a matching `verified`
transition event.
Both records must identify the same actor, timestamp, ID, version, and current file hash.

Published requirements and decisions also need a human approval event for the
current file hash. Declare the human actor as `human:<id>`. The approval actor
must also occur in `verified` and its matching verification audit event.
Approval must follow that actor's verification. Publication must follow approval.

AI generation or validation never supplies human approval.

Review the final bytes, including frontmatter. Record the final file hash in review
and publication events. A file change requires a new review and matching audit evidence.

Events contain `id`, `item_id`, `item_version`, `actor`, `at`, `action`, `from_state`,
`to_state`, `content_sha256`, `reason`, and nonempty `evidence` source references.
Use `action: transition` for state changes and `action: approval` for human review.
Each event filename is its ID plus `.yaml`. Append a new file for each event.

Do not change or delete earlier event files. Use Git review to check audit changes.

The main path is `untracked` → `candidate` → `investigated` → `verified` → `published`.
An active item may become `contested` or `stale`. A contested or stale item may
return to `investigated` or become `superseded`. A published item may become
`superseded`. A superseded item has no next state.

Approval events start from `verified` and keep that state or authorize `published`.
Publication must follow verification and human approval in timestamp order.

`ai-sdlc --workspace PATH validate` checks structure, source declarations, available
snapshot hashes, and recorded gates. It reads files and returns findings.
It does not edit source files, promote candidates, create audit records, or grant approval.
It cannot establish factual truth, source authority, reviewer identity, or historical
append-only integrity. Human review must assess those matters and apply ASD-STE100.
The shared ingestion skill guides agent-assisted synthesis.
The runtime does not extract meaning or investigate source quality automatically.
