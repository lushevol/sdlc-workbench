# Setup and E2E readiness

Use this procedure when the user requests setup, restoration, or readiness for a named test workflow.
Keep the requested runner and application scope.
Use existing Workbench diagnostics and repository commands; do not add another readiness runtime.
Default repository onboarding remains static.
Apply existing authorization before running installations, applications, browser launches, tests, or external reads.

## Keep one current view

Reuse the existing assessment or active task summary.
For maintenance without a task, use one setup summary in the selected output directory.
Link detailed logs and earlier reports instead of copying their complete outputs.
Capture the selected workspace, source checkout, test repository, revisions, checkout changes, platform, and interpreter.
Record the requested environment, browser, suite, configuration profile, and available execution authorization.

Use one row per required boundary:

| Boundary | Required evidence |
| --- | --- |
| Workbench core | Doctor `core_status`, workspace validation, selected runtime path, and actual result. |
| Resource and grants | Discovered resource, provider, configured executable path, suite, and applicable operation or tool grants. |
| Runner dependencies | Selected repository environment, package and library checks, variables present, and required browser assets. |
| Browser launch | Actual selected-browser smoke result, runtime versions, retained artifacts, and cleanup result. |
| Application path | Running components, resolved frontend modules, API destination, required dependencies, and observed responses. |
| Selected suite | Canonical case definitions, inspected assertions, exact tested revisions, native result files, and per-case outcomes. |

For each row, record the observed status, evidence link, owner, blocked action, and next action.
Use `not-run`, `unknown`, or the actual failed result when execution evidence is absent.
Mark an unknown owner explicitly.
State which next operation can proceed and which boundary prevents the requested E2E claim.
Do not turn an optional missing feature into a blocker for an unrelated operation.
Do not describe an absent required feature as optional to obtain readiness.

## Check the selected installation

Start with [the setup guide](../../../../docs/SETUP.md#start-setup).
Distinguish a source checkout from a generated workspace before selecting installation commands.
Generated workspaces contain no runtime source, `pyproject.toml`, connector source, or root Node dependencies.
Do not run source installation commands there.
Use the installed environment's executable when `ai-sdlc` is absent from `PATH`.

```sh
ai-sdlc --workspace "PATH" doctor --profile core
ai-sdlc --workspace "PATH" doctor --profile all
ai-sdlc --workspace "PATH" validate
ai-sdlc --workspace "PATH" status
```

Replace `PATH` with the selected workspace.
Retain the exact command, exit code, report, runtime identity, and time.
Inspect feature results and `core_status` when the full doctor exits nonzero.
The full profile includes unsupported integrations, so its aggregate `INCOMPLETE` does not identify every feature as unusable.
Doctor inspects prerequisites; it performs no business tests, browser launch, or service calls.
Workspace validation checks contracts; it does not establish compatible libraries or passing assertions.

Use [setup check mode](../../../../docs/SETUP.md#start-setup) for diagnosis before reinstalling packages.
Resolve only prerequisites needed by the selected operation.
For restricted installation, follow [the offline procedure](../../../../docs/SETUP.md#install-without-package-registry-access).
Core bundles, optional browser bundles, and independent repository caches have different consumers.
Check target platform, architecture, interpreter, source fingerprint, profile, and retained hashes before restoration.
Do not copy `.venv` or `node_modules` between platforms.
Keep unavailable target-platform execution explicit.

## Select and prove the runner

Discover the actual resource and inspect its `list` result before choosing a registered suite.
Use [Robot execution guidance](../../../../docs/ROBOT_TESTING.md) for `testing.robot` resources.
Relative interpreter, suite, and variable-file paths resolve from the configured test repository.
Repository metadata overrides do not repair executable tool paths.
Keep private inputs in the repository's approved ignored variable file or environment.
Record required variable names and presence without their values.

Package metadata does not establish library imports, Browser library initialization, or browser asset compatibility.
Use the owning test repository's documented checks for those boundaries.
A Robot dry run can import libraries but executes no keyword assertions.
An offline framework smoke establishes its own assertions only.
Neither result establishes the selected live suite's business behavior.

For browser investigation tooling, follow [the browser guide](../../../../docs/BROWSER_INVESTIGATIONS.md#install-explicitly).
Root Node installation does not install this optional environment or Robot's Browser assets.
Browser doctor `READY` establishes package and executable presence only.
When authorized, run the selected browser's controlled smoke and retain its result before claiming launch readiness.
Use a new evidence directory and preserve failed output and cleanup limits.
The credential-free browser fixture does not establish application login or E2E business coverage.
Keep Robot as the selected business runner when that is the requested workflow.
Playwright investigation evidence cannot substitute for executing that Robot suite.

For connectors, inspect the exact schema and per-tool grants through [the connector procedure](../../connectors/SKILL.md#discover-and-use-tools).
Discovery requires no service credentials or external requests.
Perform a scoped external read only when the requested workflow authorizes it.
Do not use messaging, uploads, or other external writes as generic setup probes.

## Check the actual application path

Read existing repository setup guides before asking for information already recorded there.
Start with [application setup guidance](../../../../repos/README.md#configure-the-applications) and each owning repository's recorded startup procedure.
Inspect an existing workspace project guide before reconstructing frontend or BFF setup.

Check required components, public assets, frontend configuration, module resolution, API proxy rules, and backend dependencies.
Bind observations to the actual browser origin and network destination.
A listening port or standalone component pass does not establish the embedded application's request path.
Record substituted dependencies and unavailable identity, database, or network boundaries beside each affected claim.
Keep credentials, raw tokens, private settings, and unnecessary response bodies out of reports.

Execute the selected suite only after its required boundaries support that operation.
Use a scoped timeout that covers the defined case duration and cleanup.
Save each completed case through the owning task's evidence procedure before further execution or handoff.
Link definitions, assertion source, and retained execution separately.
Report passed, failed, errored, skipped, and not-run cases without counting skipped cases as passes.
Refresh the same current view after repairs; preserve meaningful failed and contradictory evidence.
Claim E2E readiness only for the environment, application path, and asserted cases actually exercised.
