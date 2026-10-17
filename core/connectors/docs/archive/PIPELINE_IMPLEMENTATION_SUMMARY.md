> ⚠️ **ARCHIVED** — This document is archived and may be outdated. It captures the implementation notes from when pipeline tools were first added. Current documentation is in [docs/guide/PIPELINES_TOOLS_GUIDE.md](../guide/PIPELINES_TOOLS_GUIDE.md) and [docs/TOOLS_REFERENCE.md](../TOOLS_REFERENCE.md).

# Pipeline Tools Implementation Summary

## Overview
Successfully implemented comprehensive Azure DevOps pipeline management tools for the MCP server. These tools enable triggering, monitoring, canceling, and linking pipelines with work items directly from your local environment.

## Files Created/Modified

### New Files
1. **[packages/ado/src/tools/pipelines.js](../../packages/ado/src/tools/pipelines.js)** - Complete pipeline tools implementation
2. **[docs/guide/PIPELINES_TOOLS_GUIDE.md](../guide/PIPELINES_TOOLS_GUIDE.md)** - Comprehensive usage guide with examples

### Modified Files
1. **[packages/ado/src/tools.js](../../packages/ado/src/tools.js)** - Registered pipeline tools
2. **[docs/TOOLS_REFERENCE.md](docs/TOOLS_REFERENCE.md)** - Added pipeline tools reference

## Implemented Tools

### 1. **pipelines_run_pipeline** - Trigger Pipelines Locally ✅
Trigger/queue a new pipeline run from your local machine with:
- Branch selection
- Custom variables (including secrets)
- Template parameters
- Stage skipping

**Example**: 
```
"Run pipeline 123 in TBQPR on feature/new-feature branch with environment=staging"
```

### 2. **pipelines_list_runs** - List Active Pipelines ✅
Get list of pipeline runs filtered by:
- Branch name
- Status (inProgress, completed, cancelling, all)
- Specific pipeline ID
- Project-wide view

**Example**:
```
"Show active pipelines in TBQPR on main branch"
```

### 3. **pipelines_cancel_run** - Cancel Running Pipelines ✅
Stop a running pipeline/build.

**Example**:
```
"Cancel build 789 in TBQPR"
```

### 4. **pipelines_retry_stage** - Restart Pipeline Stages ✅
Retry/restart a specific stage in a pipeline run with option to force retry all jobs.

**Example**:
```
"Retry the Deploy stage in build 789"
```

### 5. **pipelines_list_work_item_pipelines** - Link Work Items to Pipelines ✅
**This is the complex feature you requested!**

Find all pipeline runs that used a specific release work item. When you provide a release work item ID, it will:
1. Search through recent builds
2. Check which builds have that work item linked
3. Return all pipeline links with detailed information

**Example**:
```
"Show all pipelines for release work item 11681009"
```

**Response includes**:
- Build ID and build number
- Pipeline name and ID
- Status and result
- Branch and commit
- Queue/start/finish times
- Direct URL links to view in Azure DevOps

### Supporting Tools

6. **pipelines_get_build_definitions** - List all pipelines in a project
7. **pipelines_get_run** - Get specific pipeline run details
8. **pipelines_get_build_status** - Get build status by build ID
9. **pipelines_get_builds** - Comprehensive build search with filters

## How to Use

### Quick Start
1. Restart your VS Code MCP extension to load the new tools
2. Try: `"List all pipeline definitions in TBQPR"`
3. Trigger a pipeline: `"Run pipeline <ID> in <PROJECT> on <BRANCH>"`

### Main Workflows

#### Workflow 1: Trigger Pipeline from Local
```
1. "List all pipeline definitions in TBQPR"
2. "Run pipeline 123 in TBQPR on feature/my-branch"
3. "Show active pipelines in TBQPR"
```

#### Workflow 2: Monitor Active Pipelines
```
1. "Show active pipelines in TBQPR"
2. "Get status of build 789 in TBQPR"
3. "Cancel build 789 in TBQPR" (if needed)
```

#### Workflow 3: Find Pipelines for Release (Your Complex Requirement!)
```
1. "Show all pipelines for release work item 11681009"
   → Returns all pipeline links that used this work item
2. Click URLs to view detailed pipeline runs
3. Check deployment status and results
```

#### Workflow 4: Retry Failed Stages
```
1. "Get status of build 789 in TBQPR"
2. "Retry the Deploy stage in build 789"
```

## Key Features

✅ **Trigger from Local** - Run pipelines without opening Azure DevOps  
✅ **Branch-Specific** - Filter and run on specific branches  
✅ **Active Pipeline Monitoring** - See what's currently running  
✅ **Cancel/Retry** - Stop or restart pipelines and stages  
✅ **Work Item Linking** - Find all pipelines used in a release  
✅ **Comprehensive Filtering** - By status, result, branch, definition  

## Architecture Highlights

- **Pattern Consistency**: Follows same patterns as workItems.js and repos.js
- **Error Handling**: Proper try-catch with `isError` flag
- **Zod Validation**: All parameters validated with Zod schemas
- **Azure DevOps API**: Uses both Build API and Pipelines API
- **REST API Fallback**: Uses REST API for stage retry (not in typed SDK)

## Next Steps for Testing

1. Update `config.json` with PAT that has "Build (Read & Execute)" permissions
2. Test basic listing: `"List all pipeline definitions in TBQPR"`
3. Test triggering: `"Run pipeline <ID> in <PROJECT>"`
4. Test work item linking: `"Show all pipelines for release work item <ID>"`
5. Update testing status in [docs/guide/PIPELINES_TOOLS_GUIDE.md](../guide/PIPELINES_TOOLS_GUIDE.md)

> ✅ All items above have been completed as part of the initial pipeline tools release.

## Technical Notes

### API Methods Used
- `getBuildApi().getDefinitions()` - List pipelines
- `getPipelinesApi().runPipeline()` - Trigger runs
- `getPipelinesApi().listRuns()` - List runs
- `getBuildApi().getBuilds()` - Search builds
- `getBuildApi().updateBuild()` - Cancel builds
- `getBuildApi().getBuildWorkItemsRefs()` - Get linked work items
- REST API PATCH - Retry stages

### Branch Handling
The tools automatically normalize branch names:
- Input: `"main"` → `"refs/heads/main"`
- Input: `"refs/heads/develop"` → Kept as-is

### Status/Result Mapping
Maps friendly names to Azure DevOps enum values:
- `"inProgress"` → 1 (BuildStatus.InProgress)
- `"completed"` → 2 (BuildStatus.Completed)
- `"succeeded"` → 2 (BuildResult.Succeeded)
- `"failed"` → 8 (BuildResult.Failed)

## Documentation

All tools are documented in:
- **Quick Reference**: [docs/TOOLS_REFERENCE.md](docs/TOOLS_REFERENCE.md)
- **Detailed Guide**: [guides/PIPELINES.md](guides/PIPELINES.md)

Each tool includes:
- Description and purpose
- Required/optional parameters
- Example queries (natural language)
- JSON parameter examples
- Expected responses
- Common workflows
- Troubleshooting tips

---

**Status**: ✅ Implementation Complete  
**Date**: 31 January 2026  
**Ready for Testing**: Yes
