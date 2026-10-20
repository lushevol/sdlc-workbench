---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Native Windows setup and external repository access require checks on the target computer.
---

# Independent repository setup

`repos/` holds independent business repositories for this Workbench.
The Workbench does not ignore this whole directory.
Its root Git excludes checkout directories inside category groups through `/repos/*/*/`.
Each checkout owns its Git metadata, ADO remote, branches, commits, and ignore rules.
Manage business changes through that repository's Azure DevOps (ADO) project.
Existing checkouts outside the workspace remain supported.

## Quick setup on another computer

Install Workbench through [the setup guide](../docs/SETUP.md).
Activate its Python environment before using the commands below.
Use the same portable checkout paths on each computer.

| Step | New project workspace | Existing project on another computer |
| --- | --- | --- |
| Prepare Workbench | Run `ai-sdlc init "PATH" --name "Team workspace"` in an empty target directory. | Restore the tracked project workspace through its own Git repository or approved transfer process. |
| Restore business source | Clone each confirmed repository URL into its grouped directory. | Clone confirmed upstreams, restore Git bundles, or transfer supplied filesystem copies. |
| Connect records | Add repository, source, service, capability, contract, and required tool records. | Keep the existing linked catalogs and their evidence records together. |
| Configure this computer | Create private settings and install each repository's dependencies. | Recreate private settings and dependencies for this computer. |
| Check setup | Run the checks under [Validate the connections](#validate-the-connections). | Run the same checks and compare restored commit IDs. |

Replace `PATH` with the workspace directory, such as `C:/Work/team-workspace` or `/Users/you/Work/team-workspace`.
The quoted Git and CLI commands work in PowerShell and macOS Terminal.
Use an existing workspace directly; initialization requires an empty directory.
Initialization creates empty catalogs and does not restore another project's registrations or evidence.

## Placement

Use a stable directory for each registered repository.
The current workspace uses these groups:

| Group | Repository responsibility |
| --- | --- |
| `ui/` | Frontend applications and shared UI modules. |
| `services/` | Backend and integration services. |
| `libraries/` | Shared libraries and SDKs. |
| `infra/` | Deployment and infrastructure configuration. |
| `testing/` | Independent test engines and suites. |

Register each checkout separately, including several checkouts within one group.
Keep portable workspace-relative paths in `registry/repositories.yaml`.
Use ignored `workspace.local.yaml` for machine-specific path overrides.

The root `.gitignore` keeps this guide and files directly inside each group visible.
It excludes each group's checkout directories from parent Git status and staging.
For a checkout directly under `repos/`, add its exact directory to the root `.gitignore`.
For example, exclude `/repos/example-api/` when using that custom placement.
Parent ignore rules do not control a child repository's own Git operations.

## Clone and register repositories

Initialization creates this guide and empty catalogs.
It does not clone repositories or copy business source from the Workbench checkout.
Obtain the repository's confirmed clone URL from ADO.
Use your existing Git authentication configuration.

Replace `PATH`, `ORG`, `PROJECT`, `API_REPOSITORY`, and `WEB_REPOSITORY` before running these commands.
The two repository names and URLs are placeholders.
Use each project's confirmed URL; repositories can belong to different ADO projects or organizations.

```sh
git clone "https://dev.azure.com/ORG/PROJECT/_git/API_REPOSITORY" "PATH/repos/services/example-api"
git clone "https://dev.azure.com/ORG/PROJECT/_git/WEB_REPOSITORY" "PATH/repos/ui/example-web"
git -C "PATH/repos/services/example-api" rev-parse --show-toplevel
git -C "PATH/repos/services/example-api" remote get-url origin
git -C "PATH/repos/services/example-api" rev-parse HEAD
```

The reported Git root must identify the child checkout.
Repeat the identity checks for every repository.
Select the agreed branch or commit within each checkout before recording evidence.
Keep existing directories and their local changes intact.
Inspect a supplied filesystem copy before connecting or replacing it with an ADO checkout.
A local `git init` does not restore its original history or establish its ADO identity.

Add entries to `registry/repositories.yaml`:

```yaml
schema_version: 1
repositories:
  - id: example-api
    name: Example API
    primary_type: backend
    location: repos/services/example-api
    source_ids: [example-api-ado]
  - id: example-web
    name: Example web application
    primary_type: frontend
    location: repos/ui/example-web
    source_ids: [example-web-ado]
```

Add their technical sources to `registry/sources.yaml`:

```yaml
schema_version: 1
sources:
  - id: example-api-ado
    type: git
    purpose: technical
    location: https://dev.azure.com/ORG/PROJECT/_git/API_REPOSITORY
    repository_id: example-api
    read_only: true
  - id: example-web-ado
    type: git
    purpose: technical
    location: https://dev.azure.com/ORG/PROJECT/_git/WEB_REPOSITORY
    repository_id: example-web
    read_only: true
```

Merge these entries into the existing lists.
Preserve other records and retain existing evidence revisions.
Keep credentials outside URLs and tracked configuration.
Use a full commit ID when recording revision-specific evidence.
Registration describes the repository and does not grant executable operations.

For a supplied copy, retain its filesystem source identity until its upstream and revision are confirmed.
Do not replace historical source records with a newly discovered URL.

## Link repositories, services, and capabilities

Use catalog IDs to connect the registered assets.
The following declarations illustrate the two example repositories above.
They establish no actual application connection.

Add services to `registry/services.yaml`:

```yaml
schema_version: 1
services:
  - id: example-api-service
    name: Example API service
    repository_ids: [example-api]
    source_ids: [example-api-ado]
  - id: example-web-service
    name: Example web service
    repository_ids: [example-web]
    source_ids: [example-web-ado]
```

Add the shared business responsibility to `registry/capabilities.yaml`:

```yaml
schema_version: 1
capabilities:
  - id: example-workflow
    name: Example workflow
    service_ids: [example-api-service, example-web-service]
    repository_ids: [example-api, example-web]
    source_ids: [example-api-ado, example-web-ado]
```

A service can list several implementation repositories under `repository_ids`.
Use `deployment_repository_ids` for separately registered deployment repositories.
Several services can reference the same repository.
Register each SDK and test repository with its own repository ID.

Record inspected interfaces in `registry/contracts.yaml`.
Use the same contract ID in each provider's `provides_contract_ids` and each consumer's `consumes_contract_ids`.
Each contract needs its source repository ID, relative file path, and full Git commit ID.
Use `status: candidate` and `documentation_gap` when interface documentation remains incomplete.
Read [the registry contracts](../registry/README.md#contracts) and [linked examples](../registry/examples/README.md) before adding contracts.
Preserve existing contract revisions when restoring a project.

## Configure executable tools

Configure required tools separately in `registry/tools.yaml`.
Tool IDs identify executable resources and can differ from repository IDs.
This example grants local Git inspection for the API checkout:

```yaml
schema_version: 1
tools:
  - id: example-api-git
    kind: repository
    provider: repository.git
    environment: local
    config:
      path: repos/services/example-api
    allowed_operations: [status, diff]
```

Repeat the tool entry with a distinct ID and path for each required checkout.
The Git provider requires independent `.git` metadata at its configured path.
Keep tool paths relative to the workspace where possible.

For an existing external checkout, create ignored `workspace.local.yaml`:

```yaml
schema_version: 1
repository_paths:
  example-api: 'C:/Projects/example-api'
```

Use that computer's actual path; macOS can use `/Users/you/Projects/example-api`.
Only registered repository IDs can appear in this mapping.
Also set the corresponding tool's `config.path` to that checkout.
`repository_paths` changes catalog locations only; it does not change tool paths or grants.
Review command paths, interpreter paths, and connector bridge paths when restoring existing tools.
Keep credentials in private configuration, such as the workspace root `.env`.

## Configure the applications

Install each repository's toolchain and dependencies through its own setup guide.
Workbench setup installs only Workbench dependencies.
Use each repository's required Node, Java, Python, and package manager versions.
Recreate `.venv` and `node_modules` on the target computer.

| Application connection | Configuration to confirm with the project maintainer |
| --- | --- |
| Frontend to frontend | Development ports, module names, import maps, and shared module URLs. |
| Frontend to API | API base URLs, proxy routes, authentication settings, and browser origin rules. |
| Service to SDK | Exact dependency coordinates, version, and approved artifact repository. |
| Service to service | Endpoint URLs, certificates, secrets, and required external dependencies. |
| Test engine to applications | Interpreter, named suites, environment files, credentials, and target endpoints. |

Keep local values in the owning repository's supported private configuration.
Follow [Robot setup](../docs/ROBOT_TESTING.md) for the supported test provider.
Follow [connector setup](../docs/CONNECTORS.md) for external Workbench tools and exact grants.
Catalog links do not configure application URLs, install packages, or start services.

## Validate the connections

Run these commands after registration and local configuration:

```sh
ai-sdlc --workspace "PATH" doctor --profile core
ai-sdlc --workspace "PATH" validate
ai-sdlc --workspace "PATH" status
ai-sdlc --workspace "PATH" call example-api-git status
```

Use the actual tool ID when checking an existing project.
`validate` checks record structure and references; it does not check clone availability or application connectivity.
The Git status operation checks the configured checkout.
Run each application's documented local check after its dependencies and environment are ready.
Retain business test results under the owning task when business verification is required.

## Preserve a project for another computer

Keep portable paths, confirmed credential-free clone URLs, and linked catalogs in the tracked project workspace.
Retain the associated knowledge, evidence, relationships, and task records when moving an existing project.
Do not restore live catalogs alone when they reference omitted project records.
Record each checkout's selected branch and full commit ID in the project handoff.
Publish authorized business commits through their own repositories before cloning them elsewhere.

### Transfer a Git checkout without an upstream

Use a Git bundle when the required commits are unavailable from a confirmed upstream.
Replace `TRANSFER` with an existing transfer directory outside the checkout.
Use absolute paths for `PATH` and `TRANSFER` in the transfer commands.
Run these commands on the source computer:

```sh
git -C "PATH/repos/services/example-api" status --short
git -C "PATH/repos/services/example-api" rev-parse HEAD
git -C "PATH/repos/services/example-api" bundle create "TRANSFER/example-api.bundle" --all
git -C "PATH/repos/services/example-api" bundle verify "TRANSFER/example-api.bundle"
```

A bundle preserves referenced Git history, including local branches and tags.
It excludes uncommitted changes, untracked files, ignored files, Git LFS payloads, and separate submodule repositories.
Inspect those items and preserve required files separately through the approved transfer process.
Keep private configuration separate from tracked source.
Follow repository-specific LFS or submodule transfer instructions when applicable.

Transfer the bundle and restore it into a new checkout on the target computer:

```sh
git clone "TRANSFER/example-api.bundle" "PATH/repos/services/example-api"
git -C "PATH/repos/services/example-api" rev-parse HEAD
git -C "PATH/repos/services/example-api" branch --all
```

Select the recorded branch or commit and compare the restored commit ID with the handoff.
The clone's `origin` initially identifies the bundle file.
Set it to the confirmed upstream URL when that URL becomes available:

```sh
git -C "PATH/repos/services/example-api" remote set-url origin "CONFIRMED_CLONE_URL"
```

Repeat this process for each independent repository.
Keep bundles outside Workbench commits.

### Transfer a filesystem copy

Transfer the supplied source through the approved process into its registered relative path.
Preserve hidden source files and record the archive hash in the project handoff.
Recreate machine environments and private settings separately.
Compare the transferred source before registering a different upstream revision.
Do not invent a clone URL or use the parent Workbench Git history as the copy's revision.

On the target computer, repeat [validation](#validate-the-connections) after restoring all required checkouts and settings.

## Separate Git operations

Run business Git commands with `git -C` and the child checkout path.
Stage Workbench guides and catalogs by their exact paths from the Workbench root.
Review the staged diff before committing.
Do not use `git add repos/` or include business source in Workbench commits.
Do not stage independent clones as Git links without a separate submodule decision.
Commit and push business changes within their own repositories.
