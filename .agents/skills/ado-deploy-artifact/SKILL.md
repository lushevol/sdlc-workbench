---
name: ado-deploy-artifact
description: Resolve a published Azure DevOps build artifact by exact application, pipeline, Git ref, and commit. Use when identifying release or rollback inputs before a separately authorized deployment.
---

# Resolve an Azure DevOps deployment artifact

1. Identify the target application and environment from the task and its approved deployment procedure.
2. Resolve the project ID, repository ID, pipeline definition ID, build ID, Git ref, and commit SHA.
   Use the release work item's linked pipeline run or an explicitly selected build.
   Inspect the pipeline definition and any shared template at the relevant revisions.
   A local wrapper may leave artifact publication rules in a shared template.
3. Discover the registered ADO resource and its exact grants. Use the existing connector procedure.
   This resolver requires `report_builds` and `report_build_artifacts`. [Connector procedure](../connectors/SKILL.md)
4. Resolve the artifact from the workspace root. Use the name supplied by the release evidence where available.

```sh
ai-sdlc --workspace . learning ado-resolve --resource RESOURCE --project PROJECT_ID --pipeline-id PIPELINE_ID --build-id BUILD_ID --repository-id REPOSITORY_ID --source-ref FULL_REF --source-commit COMMIT_SHA --artifact-name ARTIFACT_NAME
```

The resolver checks the successful build and its exact selectors before it inspects the published artifact metadata.
Omit `--artifact-name` to try the scoped capability rule or list safe names for explicit selection.
If it returns `SELECTION_REQUIRED`, resolve the intended name from the release evidence.
Verify retrieved rules by exact organization, project, repository, pipeline, and ref.
Use the approved deployment procedure to confirm byte integrity, target eligibility, and any approval needed for execution.
The resolver reports `METADATA_ONLY` for its read-only result.

Treat a repeatable publication convention as a candidate at the task checkpoint.
Use the returned evidence references from separate completed builds and commits in the same scope.
Record the observed artifact names and the proposed rule separately.
Submit the candidate against `ado-deploy-artifact` so future conditions improve the same capability.
Pass each projected receipt path with `learning checkpoint --ado-observation PATH`.
Repeat the flag for an independent result and include the task with `--task PATH`.
Follow the shared learning and review policy. [Session learning registry mode](../learn-from-sessions/references/capability-registry.md)
