# Evidence worksheets and examples

Use these worksheets in batch notes.
They explain which evidence a claim needs and what remains unknown.

## Evidence classes

| Class | What it establishes | What it does not establish |
| --- | --- | --- |
| Documented intent | A source records a rule, proposal, or rationale. | Current approval, implementation, or deployment. |
| Inspected implementation | Exact code contains the described branch or state change. | Effective production settings or business approval. |
| Deployment evidence | A named environment uses recorded artifacts and configuration. | Every behavior or future deployment. |
| Observed execution | Retained results show specific assertions under recorded conditions. | Unasserted behavior or execution against different bytes. |
| Inference | A stated consequence follows under named assumptions. | An observed defect or approved requirement. |
| Unknown | Available evidence cannot determine the answer. | Permission to fill the gap from intuition. |

Keep knowledge governance state separate from these evidence classes.
An investigated document can contain unknown deployment behavior.
An OKF `verified` review does not mean that business tests passed.

## Claim worksheet

Create one row per important claim.
Keep the worksheet small enough to inspect every cited range.

| ID | Claim | Class | Exact source and locator | Why these lines support it | Limit or owner question |
| --- | --- | --- | --- | --- | --- |
| C-1 | Write one supported sentence. | Choose one class above. | Record revision, hash, and range. | Identify the actual predicate or statement. | State uncertainty and owner. |

Completion check for each row:

1. Open the source and read the cited range.
2. Read surrounding setup, conditions, call sites, and error handling when they affect meaning.
3. Confirm that the cited bytes match the source manifest.
4. Explain the support without relying on the source's filename or symbol name.
5. Restrict the claim when the evidence covers only part of it.

A working link proves that a destination exists.
It does not prove that the destination supports the claim.
Keep unresolved conflicting statements with their separate dates, revisions, and applicability.
Code can resolve an implementation question while leaving intended policy unresolved.
A source that omits a retry rule does not establish that retries are forbidden.

## Feature worksheet

Use this worksheet when the task asks how a feature works.
Trace actual callers and providers rather than relying on directory names.

| Field | Required detail |
| --- | --- |
| Trigger | User action, request, timer, callback, or imported call. |
| Inputs | Relevant arguments, configuration, token fields, or persisted data. |
| Conditions | Exact guards, branches, limits, and precedence. |
| Path | Caller → helper → provider → state or persistence effect. |
| Result | Observable return, response, event, or state change. |
| Failure | Rejection, fallback, cleanup, retry, or unavailable dependency. |
| Evidence | Pinned source revisions and useful retained locators. |
| Limit | Missing consumer, deployment setting, dependency, or execution. |

Inspect only relevant boundaries and name the omitted ones.
Search results and source indexes locate evidence; they do not replace reading it.
If repository HEAD changes, compare cited file bytes with the pinned revision.
Unrelated documentation commits need not invalidate unchanged implementation evidence.

## Assertion and execution worksheet

| Criterion | Fixture | Invocation | Assertion | Mocks or omitted boundaries | Result and matching bytes | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| AC identifier | Conditions and values. | Actual tested call. | Exact expected predicate. | Controlled collaborators. | Result path, revision, environment, source hashes. | Inspected, executed, partial, stale, or unavailable. |

Read setup, invocation, and assertion together.
Follow imported Robot keywords or test helpers that supply the actual assertion.
A constant `true` assertion does not establish persistence.
A request count does not establish successful server renewal.
A displayed Sign In control does not establish global token revocation.
A wait timeout supplies an upper waiting bound, not a minimum elapsed lifetime.

Compare every executed source hash with the final implementation revision.
Both an old result and a matching result can say `PASSED`.
Use only the matching result for a current execution claim.
Preserve the stale result and state why it cannot support that claim.
Disclose transforms, mocks, commands, environment, and missing dependencies beside controlled results.

Write `NOT_RUN` when a runner or environment is unavailable.
Write `NOT_VERIFIED` when required behavior lacks adequate assertion-backed execution.
Do not install dependencies or invoke external systems merely to avoid these statuses.
Execution follows the actual task's authorization and owning repository instructions.

## Worked reasoning example

This teaching example models the parser question encountered during the completed investigation.
It is not a source record or a claim about every deployed parser.

```ts
const enabled = ["true", "1", "yes", "y"].includes(value.toLowerCase());
```

| Proposed claim | Assessment |
| --- | --- |
| The supplied parser accepts `true` and `yes`. | Supported by the listed values. |
| The supplied parser accepts uppercase `TRUE`. | Supported by lowercasing before comparison. |
| Production enables this feature. | Unknown without effective configuration and deployment evidence. |
| Users may override the feature in production. | Unknown policy; parser capability does not grant permission. |

The correct implementation answer can coexist with an unresolved business decision.
Ask about the business decision only after inspecting the relevant implementation.

## Citation and audit examples

A timing claim needs timing derivation and display code.
Entitlement rendering in the same file cannot substantiate that claim.
A blacklist test needs its setup, validation call, and outcome assertion.
Retain a safe complete range or several connected ranges when private fixtures require exclusions.

For an excerpt of original lines 68–72, physical `#L4` means original line 71.
Use `#L4` on that excerpt link and record `source_start_line: 68` in its manifest record.
Use `#L71` only when the linked snapshot contains at least 71 physical lines.
The harness checks physical bounds; the reader checks semantic support.

Finish wording, review metadata, and file endings before recording final hashes.
A single extra newline changes a document hash.
After an immutable event exists, a correction needs a new event rather than an overwritten event.
Reconcile a review's summary, findings, resolution, limits, and reviewed hash before retaining it.

## Retrieval worksheet

Choose representative questions from the user's actual scope.
Use questions that require relationships, exceptions, or unresolved boundaries.

| Question or new requirement | Starting topic | Supported answer and citations | Missing decision or evidence |
| --- | --- | --- | --- |
| A real project question. | Index link or topic ID. | Explain the supported answer. | Name the unknown and owner. |

The reader must reach the evidence through the classified index.
The reader must identify missing evidence instead of inventing an answer.
A realistic new requirement should expose related features, affected contracts, and unresolved policy.
Judge usefulness by those answers and gaps, not by file counts.
State the evaluating agent and model only when known.
Testing with one capable agent does not establish reliability for weaker models.
