# Independent repository setup

`repos/` holds independent business repositories for this Workbench.
The Workbench does not ignore this whole directory.
Its root Git excludes checkout directories inside category groups through `/repos/*/*/`.
Each checkout owns its Git metadata, ADO remote, branches, commits, and ignore rules.
Manage business changes through that repository's Azure DevOps (ADO) project.
Existing checkouts outside the workspace remain supported.

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

## Connect a repository after initialization

Initialization creates this guide and empty catalogs.
It does not clone repositories or copy business source from the Workbench checkout.
Obtain the repository's confirmed clone URL from ADO.
Use your existing Git authentication configuration.
Replace `PATH`, `ORG`, `PROJECT`, and `REPOSITORY` before running these commands.
The example repository and URL are placeholders.

```sh
git clone "https://dev.azure.com/ORG/PROJECT/_git/REPOSITORY" "PATH/repos/services/example-api"
git -C "PATH/repos/services/example-api" rev-parse --show-toplevel
git -C "PATH/repos/services/example-api" remote get-url origin
```

The reported Git root must identify the child checkout.
Keep existing directories and their local changes intact.
Inspect a supplied filesystem copy before connecting or replacing it with an ADO checkout.
A local `git init` does not restore its original history or establish its ADO identity.

Add an entry to `registry/repositories.yaml`:

```yaml
schema_version: 1
repositories:
  - id: example-api
    name: Example API
    primary_type: backend
    location: repos/services/example-api
    source_ids: [example-api-ado]
```

Add its technical source to `registry/sources.yaml`:

```yaml
schema_version: 1
sources:
  - id: example-api-ado
    type: git
    purpose: technical
    location: https://dev.azure.com/ORG/PROJECT/_git/REPOSITORY
    repository_id: example-api
    read_only: true
```

Merge these entries into the existing lists.
Preserve other records and retain existing evidence revisions.
Keep credentials outside URLs and tracked configuration.
Use a full commit ID when recording revision-specific evidence.
Registration describes the repository and does not grant executable operations.
Configure required tools separately in `registry/tools.yaml`.

Run `ai-sdlc --workspace PATH validate` after registration.

## Separate Git operations

Run business Git commands with `git -C` and the child checkout path.
Stage Workbench guides and catalogs by their exact paths from the Workbench root.
Review the staged diff before committing.
Do not use `git add repos/` or include business source in Workbench commits.
Do not stage independent clones as Git links without a separate submodule decision.
Commit and push business changes within their own repositories.
