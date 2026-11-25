# Extract session lessons

## Choose the owner

| Learning | Durable destination |
| --- | --- |
| User requirements, clarifications, or decisions | Exact input and source in the owning task; business intent follows canonical governance. |
| Explicit project preferences | Relevant existing project instructions or guide, when authorized and applicable to future work. |
| Explicit personal preferences | Task evidence first; use the client's memory mechanism only after an explicit request to remember. |
| Inferred preferences | Task-local candidates with rationale and source; do not silently activate them as standing instructions. |
| Agent exploration and useful failures | Task evidence, with a scoped lesson linked from the relevant existing technical guide or workflow. |
| Integration contracts and background | The domain extractor's Contracts, Workflows, and Knowledge owners. |
| Repeatable successful procedures | Existing script or workflow; use an experience packet only when a packaged recipe is useful and authorized. |
| Scoped registry rules | Existing capability identity and Workbench checkpoint operations, when the supported schema fits. |

Do not force preferences or unrelated lessons into an unsupported registry category.
Do not create a packet or a new skill for every session.
Create only populated outputs with a demonstrated retrieval or execution use.
If no suitable reusable owner exists, keep a candidate in the task and identify the needed destination.

## Preserve preferences and user input

Capture the exact statement, source date, locator, and whether the preference is explicit or inferred.
Record the applicable project, domain, task type, conditions, and exceptions.
Keep a one-task workaround local unless the user establishes broader scope.
The latest explicit clarification governs only its stated scope; preserve the earlier source and explain the conflict.
When incompatible statements have unclear scope, retain both and identify the unresolved decision.
Do not treat an agent's proposal, user silence, or continuation as acceptance.
Do not rewrite global memory or personal instructions solely because session learning was requested.

For example, a preference to preserve caller APIs during migration applies to that migration scope.
A preference for a short response does not waive required evidence or checks.

## Reconstruct attempts

Record enough information to distinguish the useful lesson from the original transcript:

- Goal, trigger, prerequisites, inputs, source revision, environment, and relevant configuration.
- Action or command, exact observed result, and the assertion or evidence that supports it.
- Failed approaches, contradictory results, suspected causes, and supported recovery.
- The shortest supported procedure, expected output, verification scope, and unresolved steps.

Keep observed symptoms separate from suspected causes.
A workaround that passes once does not prove the cause or universal applicability.
Do not omit failures that change the recommended steps or conditions.
Keep detailed raw context in the owning task when reproduction or recovery needs it.
Summaries link that canonical evidence instead of copying logs into several outputs.

## Extract scripts and workflows

Read the original command chain and its inputs before generalizing it.
Preserve required ordering, working directory, errors, exit status, and expected outputs.
Replace task-specific values with named inputs without removing necessary domain constraints.
Use existing helpers, connectors, authentication, and execution grants.
For external operations, retain bounded deadlines, retry limits, and applicable recovery.
Document side effects and prerequisites before anyone reuses the procedure.

Verify useful positive and failure cases when the change requires execution.
Use offline or synthetic fixtures when appropriate and label their limits.
Retain untested steps as untested. Extraction alone does not establish a successful replay.
