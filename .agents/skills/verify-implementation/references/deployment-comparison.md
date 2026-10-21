# Compare deployment conditions before acceptance

Use this procedure when verification depends on a named environment, deployed configuration, or environment-specific failure.
It supplies an agent check, not a core-enforced gate or a deployment tool.
Keep the comparison in the existing stage record and evidence index.
For harness maintenance, use the existing maintenance report without creating a business task.

## Define the conclusion and inputs

Name the target environment, behavior predicates, canonical cases, and required execution level.
Read existing setup records and results before collecting more evidence.
Link each case definition, assertion source, and original execution separately using the [shared handoff](behavior-review.md#keep-one-evidence-handoff).
Select conditions that can change those predicates. Do not require unrelated configuration parity.

Before execution, record the following bindings:

| Binding | Required evidence |
| --- | --- |
| Source | Exact implementation and test revisions, relevant file hashes, local changes, transformations, and build inputs. |
| Running components | Observed artifact or build identities for the host, embedded application, and relevant services; origin and observation time. |
| Case conditions | Selected case, inputs, assertion IDs, fixtures, substituted boundaries, runner, and actual application navigation. |
| Configuration | Relevant defaults, profile, build-time substitutions, runtime overrides, units, precedence, and effective values with their sources. |
| Observation | Run/action ID, capture time, clocks, uncertainty, instrumentation, and retained logs or captures. |

A repository revision or healthy endpoint alone does not identify the running artifact.
Inspect the served module when host and embedded applications deploy independently.
Record unresolved cache, routing, or module-version differences instead of assuming the checked-out module was served.

## Compare relevant configuration

Use one row per material value or condition. Add rows to the existing record rather than creating another summary.

| Input or condition | Intended value and authority | Actual local value and evidence | Actual target value and evidence | Disposition and affected predicate |
| --- | --- | --- | --- | --- |
| Record the setting or condition. | Link approved intent, or mark unresolved. | Link exact source and runtime observation separately. | Link target observation, or mark unknown. | Record matched, different, or unknown; name the limited conclusion. |

Trace each material setting from its default through applicable bindings to the actual launcher or deployment path.
Inspect the framework's precedence and selected profile before deciding which source wins.
Do not infer effective values from a checked-in YAML file, deployment template, or environment variable alone.
Separate intended launch instructions from evidence that the identified process used them.
An observed issued value can confirm that value while leaving its configuration source unknown.

For sessions and timers, use the [timing worksheet](browser-investigation.md#verify-timing-inputs-and-deployment-settings).
It defines lifetime arithmetic, units, clock checks, scheduling evidence, and separate actual-lifetime and shortened-lifetime checks.
Bind safe credential metadata to the issuing component, environment, observation time, and run.
Exclude raw tokens, cookies, signing keys, passwords, and unrelated process or environment values.
Inspect only the relevant configuration fields. Redact sensitive values before retaining output.

Use existing authorized CLI or MCP operations to collect target evidence.
Discover resources with `ai-sdlc --workspace PATH status`, then inspect each resource's `list` schema and grants.
Use the [connector procedure](../../connectors/SKILL.md#discover-and-use-tools) for external connector operations.
Reuse authorized access. Missing access limits target claims while independent local checks continue.
Do not broaden grants or modify deployment settings merely to make environments match.

## Reconcile each result

After execution, compare observed conditions with the recorded setup.
Bind every result to the implementation, assertions, running components, effective settings, and case inputs actually used.
Preserve interrupted runs, setup failures, mismatches, and contradictory observations.
If a relevant artifact or setting changed during execution, identify the affected interval or mark that result inconclusive.
Recheck these bindings before reusing an earlier pass after configuration or deployment changes.

Apply these dispositions to each requested conclusion:

| Available evidence | Permitted disposition |
| --- | --- |
| Local execution passes under disclosed local settings. | Report those local predicates passed. Keep target acceptance separate. |
| Only shortened clocks, injected expiry, or mocked services pass. | Report the controlled branch result and omitted boundaries. |
| Target values or artifact identities are unavailable. | Keep target parity and affected target behavior `NOT_VERIFIED`. |
| Relevant local and target conditions differ. | State the difference and affected predicate. Do not transfer the local pass to the target. |
| Relevant conditions match, but target assertions did not run. | Report supported condition matches. Keep target behavior `NOT_VERIFIED`. |
| Actual target assertions pass with matching retained bindings. | Use `VERIFIED` only for those predicates within that environment and evidence scope. |

Configuration equality alone cannot establish correct behavior or approved policy.
A difference alone cannot establish a defect without applicable intent and an affected behavior.
Do not erase a useful local mechanism result because target evidence remains unavailable.

For each blocked acceptance claim, name its consequence, owner, missing evidence, and next action.
Mark an unknown owner explicitly. Request only the material missing evidence or decision.
Keep business approval and knowledge publication separate from technical verification.
