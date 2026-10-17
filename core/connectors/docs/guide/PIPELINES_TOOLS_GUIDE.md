# Pipeline Tools Guide

This guide covers all pipeline-related tools for managing Azure DevOps pipelines (builds) from your MCP server.

> Replace project names, pipeline IDs, build IDs, and repository names below with values from your own Azure DevOps environment.

## Test Environment Setup

**Project**: YOUR_PROJECT (or your Azure DevOps project)  
**Pipeline ID**: Replace with your actual pipeline ID from Azure DevOps  
**Build ID**: Replace with actual build ID from pipeline runs  

## Tools Overview

### 1. pipelines_get_build_definitions
Get a list of pipeline definitions (build definitions) in a project.

**Test Query**: `List all pipeline definitions in YOUR_PROJECT`

**Parameters**:
- `project` (required): Project name or ID
- `name` (optional): Filter by pipeline name
- `repositoryId` (optional): Filter by repository
- `repositoryType` (optional): TfsGit, GitHub, or BitbucketCloud
- `top` (optional): Maximum number of results

**Expected Response**:
```json
[
  {
    "id": 123,
    "name": "My-Pipeline",
    "path": "\\Pipelines",
    "project": { "name": "YOUR_PROJECT" },
    "repository": {
      "id": "repo-guid",
      "name": "MyRepo",
      "type": "TfsGit"
    },
    "process": {
      "yamlFilename": "azure-pipelines.yml"
    }
  }
]
```


**Note**: This tool is essential for finding pipeline IDs before triggering runs. So basically we will pass the project and repo name. Like this `Get pipeline definitions of your-repository-name in YOUR_PROJECT and share me the pipelineId and all the details` 

---

### 2. pipelines_run_pipeline
Trigger/queue a new pipeline run from your local machine.

**Test Query**: `Run pipeline 3093 in YOUR_PROJECT on develop branch`

**Parameters**:
- `project` (required): Project name or ID
- `pipelineId` (required): Pipeline definition ID
- `branchName` (optional): Branch to run on (e.g., "main", "refs/heads/feature/my-branch")
- `templateParameters` (optional): Template parameters as key-value pairs
- `variables` (optional): Build variables with value and isSecret flag
- `stagesToSkip` (optional): Array of stage names to skip

**Example with Variables**:
```json
{
  "project": "YOUR_PROJECT",
  "pipelineId": 123,
  "branchName": "develop",
  "variables": {
    "environment": {
      "value": "staging",
      "isSecret": false
    },
    "apiKey": {
      "value": "secret-value",
      "isSecret": true
    }
  }
}
```

**Expected Response**:
```json
{
  "id": 789,
  "name": "20240131.1",
  "state": "inProgress",
  "createdDate": "2024-01-31T10:30:00Z",
  "pipeline": {
    "id": 123,
    "name": "My-Pipeline"
  },
  "resources": {
    "repositories": {
      "self": {
        "refName": "refs/heads/develop"
      }
    }
  }
}
```

**Response**: 
```
The pipeline 3093 ("my-app-npm-pipeline") has been successfully triggered in the YOUR_PROJECT project on the develop branch.

You can monitor the run here: https://dev.azure.com/sc-ado/YOUR_PROJECT/_build/results?buildId=10001234
Pipeline definition: https://dev.azure.com/sc-ado/YOUR_PROJECT/_build/definition?definitionId=3093
Let me know if you want to check the status or see logs for this run.
```

---

### 3. pipelines_list_runs
List pipeline runs with filtering by branch and status.

**Test Query**: `Show active pipelines in YOUR_PROJECT on main branch`

**Parameters**:
- `project` (required): Project name or ID
- `pipelineId` (optional): Specific pipeline ID to filter
- `branchName` (optional): Branch to filter by
- `statusFilter` (optional): "inProgress", "completed", "cancelling", or "all" (default)

**Use Cases**:
- List all active/running pipelines: `statusFilter: "inProgress"`
- List completed pipelines on a branch: `statusFilter: "completed", branchName: "main"`
- List all recent pipeline runs: `statusFilter: "all"`

**Expected Response**:
```json
[
  {
    "id": 789,
    "buildNumber": "20240131.1",
    "status": "inProgress",
    "result": null,
    "sourceBranch": "refs/heads/main",
    "definition": {
      "id": 123,
      "name": "My-Pipeline"
    },
    "queueTime": "2024-01-31T10:30:00Z",
    "startTime": "2024-01-31T10:31:00Z"
  }
]
```


---

### 4. pipelines_get_run
Get detailed information about a specific pipeline run.

**Test Query**: `Show details for pipeline run 789 in pipeline 123`

**Parameters**:
- `project` (required): Project name
- `pipelineId` (required): Pipeline ID
- `runId` (required): Run ID

**Expected Response**:
```json
{
  "id": 789,
  "name": "20240131.1",
  "state": "completed",
  "result": "succeeded",
  "createdDate": "2024-01-31T10:30:00Z",
  "finishedDate": "2024-01-31T10:45:00Z",
  "pipeline": {
    "id": 123,
    "name": "My-Pipeline"
  }
}
```


---

### 5. pipelines_get_build_status
Get the status of a specific build using build ID (alternative method).

**Test Query**: `Get status of build 789 in YOUR_PROJECT`

**Parameters**:
- `project` (required): Project name
- `buildId` (required): Build ID

**Expected Response**:
```json
{
  "id": 789,
  "buildNumber": "20240131.1",
  "status": "completed",
  "result": "succeeded",
  "sourceBranch": "refs/heads/main",
  "sourceVersion": "abc123def456",
  "queueTime": "2024-01-31T10:30:00Z",
  "startTime": "2024-01-31T10:31:00Z",
  "finishTime": "2024-01-31T10:45:00Z"
}
```


---

### 6. pipelines_get_builds
Get builds with comprehensive filtering options.

**Test Query**: `Show all failed builds in YOUR_PROJECT for pipeline 123`

**Parameters**:
- `project` (required): Project name
- `definitions` (optional): Array of pipeline IDs
- `branchName` (optional): Branch to filter
- `statusFilter` (optional): "inProgress", "completed", "cancelling", "notStarted", "all"
- `resultFilter` (optional): "succeeded", "partiallySucceeded", "failed", "canceled", "all"
- `top` (optional): Maximum number of results
- `buildIds` (optional): Array of specific build IDs

**Example - Find Failed Builds**:
```json
{
  "project": "YOUR_PROJECT",
  "definitions": [123],
  "resultFilter": "failed",
  "top": 10
}
```

**Expected Response**:
```json
[
  {
    "id": 788,
    "buildNumber": "20240131.1",
    "status": "completed",
    "result": "failed",
    "definition": {
      "id": 123,
      "name": "My-Pipeline"
    },
    "sourceBranch": "refs/heads/develop",
    "finishTime": "2024-01-31T09:45:00Z"
  }
]
```


---

### 7. pipelines_cancel_run
Cancel a running pipeline/build.

**Test Query**: `Cancel build 789 in YOUR_PROJECT`

**Parameters**:
- `project` (required): Project name
- `buildId` (required): Build ID to cancel

**Expected Response**:
```json
{
  "message": "Pipeline cancellation requested",
  "build": {
    "id": 789,
    "status": "cancelling"
  }
}
```


---

### 8. pipelines_retry_stage
Retry/restart a specific stage in a pipeline run.

**Test Query**: `Retry the Deploy stage in build 789`

**Parameters**:
- `project` (required): Project name
- `buildId` (required): Build ID
- `stageName` (required): Name of the stage to retry
- `forceRetryAllJobs` (optional): Force retry all jobs (default: false)

**Example**:
```json
{
  "project": "YOUR_PROJECT",
  "buildId": 789,
  "stageName": "Deploy",
  "forceRetryAllJobs": true
}
```

**Expected Response**:
```json
{
  "message": "Stage \"Deploy\" retry requested",
  "result": {
    "id": "Deploy",
    "name": "Deploy",
    "state": "pending"
  }
}
```


---

### 9. pipelines_list_work_item_pipelines
Find all pipeline runs linked to a specific work item. This is extremely useful for release work items to see which pipelines have been used.

**Test Query**: `Show all pipelines for release work item 12345`

**Parameters**:
- `project` (required): Project name
- `workItemId` (required): Work item ID to search for
- `top` (optional): Maximum number of builds to search (default: 50)

**Expected Response**:
```json
{
  "workItemId": 12345,
  "totalBuildsFound": 3,
  "builds": [
    {
      "buildId": 789,
      "buildNumber": "20240131.1",
      "definitionName": "My-Pipeline",
      "definitionId": 123,
      "status": "completed",
      "result": "succeeded",
      "sourceBranch": "refs/heads/release/v1.2.3",
      "sourceVersion": "abc123def456",
      "queueTime": "2024-01-31T10:30:00Z",
      "startTime": "2024-01-31T10:31:00Z",
      "finishTime": "2024-01-31T10:45:00Z",
      "url": "https://dev.azure.com/myorg/YOUR_PROJECT/_build/results?buildId=789",
      "webUrl": "https://dev.azure.com/myorg/YOUR_PROJECT/_build/results?buildId=789"
    }
  ]
}
```


---

## Common Workflows

### Workflow 1: Trigger a Pipeline from Local
```
1. Find your pipeline ID: "List all pipeline definitions in YOUR_PROJECT"
2. Trigger the pipeline: "Run pipeline 123 in YOUR_PROJECT on feature/my-branch"
3. Check status: "Show active pipelines in YOUR_PROJECT"
```

### Workflow 2: Monitor Active Pipelines
```
1. List active pipelines: "Show active pipelines in YOUR_PROJECT"
2. Get detailed status: "Get status of build 789 in YOUR_PROJECT"
3. If needed, cancel: "Cancel build 789 in YOUR_PROJECT"
```

### Workflow 3: Find Pipelines for a Release
```
1. Get release work item ID (e.g., 12345)
2. Find linked pipelines: "Show all pipelines for release work item 12345"
3. Review each pipeline's status and results
4. Click on the URL to view in browser
```

### Workflow 4: Retry Failed Pipeline Stage
```
1. Check build status: "Get status of build 789 in YOUR_PROJECT"
2. Identify failed stage (e.g., "Deploy")
3. Retry the stage: "Retry the Deploy stage in build 789"
```

### Workflow 5: Filter Pipelines by Branch
```
1. List all runs on specific branch: "Show completed pipelines on develop branch"
2. Filter by status: "Show active pipelines on main branch"
3. Check recent failures: "Show failed builds on release/v1.2.3 branch"
```

---

## Troubleshooting

### Issue: Pipeline not triggering
- Verify pipeline ID exists: Use `pipelines_get_build_definitions`
- Check permissions: Ensure your PAT has "Build (Read & Execute)" permissions
- Verify branch name: Use full ref format `refs/heads/branch-name`

### Issue: Cannot find work item pipelines
- Ensure work items are linked to builds (via commits or manual linking)
- Increase `top` parameter to search more builds
- Check if builds are in the correct project

### Issue: Stage retry not working
- Verify stage name is correct (case-sensitive)
- Ensure build is in a state that allows retry (completed or partially succeeded)
- Check if you have permissions to retry builds

---

## Additional Resources

- [Azure DevOps Build API Documentation](https://learn.microsoft.com/en-us/rest/api/azure/devops/build/)
- [Azure DevOps Pipelines API Documentation](https://learn.microsoft.com/en-us/rest/api/azure/devops/pipelines/)
- [Work Items and Builds Linking](https://learn.microsoft.com/en-us/azure/devops/pipelines/integrations/configure-pipelines-work-tracking)
