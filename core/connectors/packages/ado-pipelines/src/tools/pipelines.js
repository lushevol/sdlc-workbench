import { z } from 'zod';

// Tool mapping for pipeline-related MCP tools
const PIPELINE_TOOLS = {
  run_pipeline: 'pipelines_run_pipeline',
  list_runs: 'pipelines_list_runs',
  get_run: 'pipelines_get_run',
  cancel_run: 'pipelines_cancel_run',
  retry_stage: 'pipelines_retry_stage',
  get_build_definitions: 'pipelines_get_build_definitions',
  get_builds: 'pipelines_get_builds',
  get_build_status: 'pipelines_get_build_status',
  list_work_item_pipelines: 'pipelines_list_work_item_pipelines',
  get_build_log: 'pipelines_get_build_log',
  get_build_changes: 'pipelines_get_build_changes',
  list_artifacts: 'pipelines_list_artifacts',
  list_variable_groups: 'pipelines_list_variable_groups',
  get_variable_group: 'pipelines_get_variable_group',
};

function configurePipelineTools(server, getADOConnection) {

  // List pipeline definitions (build definitions)
  server.tool(
    PIPELINE_TOOLS.get_build_definitions,
    'Retrieves a list of build/pipeline definitions for a given project.',
    {
      project: z.string().describe('Project ID or name to get build definitions for'),
      name: z.string().optional().describe('Name of the build definition to filter'),
      repositoryId: z.string().optional().describe('Repository ID to filter build definitions'),
      repositoryType: z.enum(['TfsGit', 'GitHub', 'BitbucketCloud']).optional().describe('Type of repository to filter build definitions'),
      top: z.number().int().optional().describe('Maximum number of build definitions to return')
    },
    async ({ project, name, repositoryId, repositoryType, top }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        const definitions = await buildApi.getDefinitions(
          project,
          name,
          repositoryId,
          repositoryType,
          undefined, // queryOrder
          top
        );
        return { content: [{ type: 'text', text: JSON.stringify(definitions, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Run/trigger a pipeline
  server.tool(
    PIPELINE_TOOLS.run_pipeline,
    'Trigger/queue a new pipeline run. You can specify branch, variables, and other parameters.',
    {
      project: z.string().describe('Project ID or name to run the pipeline in'),
      pipelineId: z.number().int().positive().describe('ID of the pipeline definition to run'),
      branchName: z.string().optional().describe('Branch name to run the pipeline on (e.g., "refs/heads/main" or "main")'),
      templateParameters: z.record(z.string(), z.string()).optional().describe('Template parameters as key-value pairs'),
      variables: z.record(z.string(), z.object({
        value: z.string().describe('Value of the variable'),
        isSecret: z.boolean().optional().describe('Whether the variable is a secret')
      })).optional().describe('Build variables as key-value pairs'),
      stagesToSkip: z.array(z.string()).optional().describe('Array of stage names to skip')
    },
    async ({ project, pipelineId, branchName, templateParameters, variables, stagesToSkip }) => {
      try {
        const connection = await getADOConnection();
        const pipelinesApi = await connection.getPipelinesApi();
        
        // Build the run request
        const runRequest = {
          templateParameters,
          variables,
          stagesToSkip
        };

        // Add branch/repository resources if specified
        if (branchName) {
          const normalizedBranch = branchName.startsWith('refs/') 
            ? branchName 
            : `refs/heads/${branchName}`;
          
          runRequest.resources = {
            repositories: {
              self: {
                refName: normalizedBranch
              }
            }
          };
        }

        const pipelineRun = await pipelinesApi.runPipeline(runRequest, project, pipelineId);
        
        return { content: [{ type: 'text', text: JSON.stringify(pipelineRun, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List pipeline runs
  server.tool(
    PIPELINE_TOOLS.list_runs,
    'List pipeline runs for a specific pipeline or project. Can filter by branch and status.',
    {
      project: z.string().describe('Project ID or name'),
      pipelineId: z.number().int().positive().optional().describe('Pipeline ID to filter runs (optional)'),
      branchName: z.string().optional().describe('Branch name to filter runs (e.g., "refs/heads/main" or "main")'),
      statusFilter: z.enum(['inProgress', 'completed', 'cancelling', 'all']).optional().default('all').describe('Status filter for pipeline runs')
    },
    async ({ project, pipelineId, branchName, statusFilter }) => {
      try {
        const connection = await getADOConnection();
        
        if (pipelineId) {
          // Use Pipelines API for specific pipeline
          const pipelinesApi = await connection.getPipelinesApi();
          const runs = await pipelinesApi.listRuns(project, pipelineId);
          
          let filteredRuns = runs;
          
          // Filter by branch if specified
          if (branchName) {
            const normalizedBranch = branchName.startsWith('refs/') 
              ? branchName 
              : `refs/heads/${branchName}`;
            filteredRuns = runs.filter(run => 
              run.resources?.repositories?.self?.refName === normalizedBranch
            );
          }
          
          // Filter by status
          if (statusFilter !== 'all') {
            filteredRuns = filteredRuns.filter(run => {
              const state = run.state?.toLowerCase();
              if (statusFilter === 'inProgress') return state === 'inprogress';
              if (statusFilter === 'completed') return state === 'completed';
              if (statusFilter === 'cancelling') return state === 'cancelling';
              return true;
            });
          }
          
          return { content: [{ type: 'text', text: JSON.stringify(filteredRuns, null, 2) }] };
        } else {
          // Use Build API for all builds in project
          const buildApi = await connection.getBuildApi();
          
          // Map status filter to Build API status enum values
          let buildStatusFilter = undefined;
          if (statusFilter === 'inProgress') buildStatusFilter = 1; // InProgress
          else if (statusFilter === 'completed') buildStatusFilter = 2; // Completed
          else if (statusFilter === 'cancelling') buildStatusFilter = 32; // Cancelling
          
          const normalizedBranch = branchName && !branchName.startsWith('refs/') 
            ? `refs/heads/${branchName}` 
            : branchName;
          
          const builds = await buildApi.getBuilds(
            project,
            undefined, // definitions
            undefined, // queues
            undefined, // buildNumber
            undefined, // minTime
            undefined, // maxTime
            undefined, // requestedFor
            undefined, // reasonFilter
            buildStatusFilter, // statusFilter
            undefined, // resultFilter
            undefined, // tagFilters
            undefined, // properties
            undefined, // top
            undefined, // continuationToken
            undefined, // maxBuildsPerDefinition
            undefined, // deletedFilter
            undefined, // queryOrder
            normalizedBranch, // branchName
            undefined, // buildIds
            undefined, // repositoryId
            undefined  // repositoryType
          );
          
          return { content: [{ type: 'text', text: JSON.stringify(builds, null, 2) }] };
        }
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get specific pipeline run
  server.tool(
    PIPELINE_TOOLS.get_run,
    'Get details of a specific pipeline run.',
    {
      project: z.string().describe('Project ID or name'),
      pipelineId: z.number().int().positive().describe('Pipeline ID'),
      runId: z.number().int().positive().describe('Run ID')
    },
    async ({ project, pipelineId, runId }) => {
      try {
        const connection = await getADOConnection();
        const pipelinesApi = await connection.getPipelinesApi();
        const run = await pipelinesApi.getRun(project, pipelineId, runId);
        return { content: [{ type: 'text', text: JSON.stringify(run, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get build status (alternative method using Build API)
  server.tool(
    PIPELINE_TOOLS.get_build_status,
    'Get the status of a specific build/pipeline run using build ID.',
    {
      project: z.string().describe('Project ID or name'),
      buildId: z.number().int().positive().describe('Build ID to get status for')
    },
    async ({ project, buildId }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        const build = await buildApi.getBuild(project, buildId);
        return { content: [{ type: 'text', text: JSON.stringify(build, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get all builds (comprehensive)
  server.tool(
    PIPELINE_TOOLS.get_builds,
    'Get builds/pipeline runs with various filters including branch, status, and definition.',
    {
      project: z.string().describe('Project ID or name'),
      definitions: z.array(z.number().int()).optional().describe('Array of build definition IDs to filter'),
      branchName: z.string().optional().describe('Branch name to filter builds'),
      statusFilter: z.enum(['inProgress', 'completed', 'cancelling', 'notStarted', 'all']).optional().describe('Status filter'),
      resultFilter: z.enum(['succeeded', 'partiallySucceeded', 'failed', 'canceled', 'all']).optional().describe('Result filter'),
      top: z.number().int().optional().describe('Maximum number of builds to return'),
      buildIds: z.array(z.number().int()).optional().describe('Array of specific build IDs to retrieve')
    },
    async ({ project, definitions, branchName, statusFilter, resultFilter, top, buildIds }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        
        // Map status filter
        let buildStatus = undefined;
        if (statusFilter === 'inProgress') buildStatus = 1;
        else if (statusFilter === 'completed') buildStatus = 2;
        else if (statusFilter === 'cancelling') buildStatus = 32;
        else if (statusFilter === 'notStarted') buildStatus = 8;
        
        // Map result filter
        let buildResult = undefined;
        if (resultFilter === 'succeeded') buildResult = 2;
        else if (resultFilter === 'partiallySucceeded') buildResult = 4;
        else if (resultFilter === 'failed') buildResult = 8;
        else if (resultFilter === 'canceled') buildResult = 32;
        
        const normalizedBranch = branchName && !branchName.startsWith('refs/') 
          ? `refs/heads/${branchName}` 
          : branchName;
        
        const builds = await buildApi.getBuilds(
          project,
          definitions,
          undefined, // queues
          undefined, // buildNumber
          undefined, // minTime
          undefined, // maxTime
          undefined, // requestedFor
          undefined, // reasonFilter
          buildStatus,
          buildResult,
          undefined, // tagFilters
          undefined, // properties
          top,
          undefined, // continuationToken
          undefined, // maxBuildsPerDefinition
          undefined, // deletedFilter
          undefined, // queryOrder
          normalizedBranch,
          buildIds
        );
        
        return { content: [{ type: 'text', text: JSON.stringify(builds, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Cancel a pipeline run
  server.tool(
    PIPELINE_TOOLS.cancel_run,
    'Cancel a running pipeline/build.',
    {
      project: z.string().describe('Project ID or name'),
      buildId: z.number().int().positive().describe('Build/Run ID to cancel')
    },
    async ({ project, buildId }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        
        // Update the build to cancel it
        const updatedBuild = await buildApi.updateBuild(
          { status: 32 }, // 32 = Cancelling status
          project,
          buildId
        );
        
        return { 
          content: [{ 
            type: 'text', 
            text: JSON.stringify({ 
              message: 'Pipeline cancellation requested',
              build: updatedBuild 
            }, null, 2) 
          }] 
        };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Retry/restart a pipeline stage
  server.tool(
    PIPELINE_TOOLS.retry_stage,
    'Retry/restart a specific stage in a pipeline run.',
    {
      project: z.string().describe('Project ID or name'),
      buildId: z.number().int().positive().describe('Build ID to retry'),
      stageName: z.string().describe('Name of the stage to retry'),
      forceRetryAllJobs: z.boolean().optional().default(false).describe('Whether to force retry all jobs in the stage')
    },
    async ({ project, buildId, stageName, forceRetryAllJobs }) => {
      try {
        const connection = await getADOConnection();
        const orgUrl = connection.serverUrl;
        
        // Get PAT from config
        const { getConfig } = await import('@sc-node-mcp/core');
        const config = getConfig();
        const token = config.AZURE_DEVOPS_PAT;
        
        // Use REST API to update stage (not available in typed API)
        const endpoint = `${orgUrl}/${project}/_apis/build/builds/${buildId}/stages/${stageName}?api-version=7.1-preview.1`;
        
        const body = {
          forceRetryAllJobs,
          state: 'retry' // Retry the stage
        };
        
        const response = await fetch(endpoint, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Basic ${Buffer.from(`:${token}`).toString('base64')}`
          },
          body: JSON.stringify(body)
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to retry stage: ${response.status} ${errorText}`);
        }
        
        const result = await response.json();
        
        return { 
          content: [{ 
            type: 'text', 
            text: JSON.stringify({ 
              message: `Stage "${stageName}" retry requested`,
              result 
            }, null, 2) 
          }] 
        };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List pipelines that used a specific work item
  server.tool(
    PIPELINE_TOOLS.list_work_item_pipelines,
    'Find all pipeline runs that are linked to a specific work item (useful for release work items).',
    {
      project: z.string().describe('Project ID or name'),
      workItemId: z.number().int().positive().describe('Work item ID to find associated pipelines'),
      top: z.number().int().optional().default(50).describe('Maximum number of builds to return')
    },
    async ({ project, workItemId, top }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        
        // Get all recent builds
        const builds = await buildApi.getBuilds(
          project,
          undefined, // definitions
          undefined, // queues
          undefined, // buildNumber
          undefined, // minTime
          undefined, // maxTime
          undefined, // requestedFor
          undefined, // reasonFilter
          undefined, // statusFilter
          undefined, // resultFilter
          undefined, // tagFilters
          undefined, // properties
          top
        );
        
        // For each build, check if it has the work item linked
        const buildsWithWorkItem = [];
        
        for (const build of builds) {
          try {
            // Get work items for this build
            const workItems = await buildApi.getBuildWorkItemsRefs(project, build.id);
            
            // Check if our work item is in the list
            const hasWorkItem = workItems.some(wi => wi.id === String(workItemId));
            
            if (hasWorkItem) {
              buildsWithWorkItem.push({
                buildId: build.id,
                buildNumber: build.buildNumber,
                definitionName: build.definition?.name,
                definitionId: build.definition?.id,
                status: build.status,
                result: build.result,
                sourceBranch: build.sourceBranch,
                sourceVersion: build.sourceVersion,
                queueTime: build.queueTime,
                startTime: build.startTime,
                finishTime: build.finishTime,
                url: build._links?.web?.href || `${connection.serverUrl}/${project}/_build/results?buildId=${build.id}`,
                webUrl: build._links?.web?.href
              });
            }
          } catch (error) {
            // Continue if we can't get work items for a build
            console.error(`Could not get work items for build ${build.id}:`, error.message);
          }
        }
        
        return { 
          content: [{ 
            type: 'text', 
            text: JSON.stringify({
              workItemId,
              totalBuildsFound: buildsWithWorkItem.length,
              builds: buildsWithWorkItem
            }, null, 2) 
          }] 
        };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get full build log output
  server.tool(
    PIPELINE_TOOLS.get_build_log,
    'Retrieve the combined log output for all steps of a specific build.',
    {
      project: z.string().describe('Project ID or name'),
      buildId: z.number().int().positive().describe('Build ID to retrieve logs for')
    },
    async ({ project, buildId }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        const logs = await buildApi.getBuildLogs(project, buildId);
        if (!logs || logs.length === 0) {
          return { content: [{ type: 'text', text: `No logs found for build ${buildId}.` }] };
        }
        // Fetch each log and concatenate
        const logTexts = [];
        for (const log of logs) {
          const logContent = await buildApi.getBuildLogLines(project, buildId, log.id);
          logTexts.push(`--- Log ${log.id} (${log.type || 'step'}) ---\n${logContent.join('\n')}`);
        }
        return { content: [{ type: 'text', text: logTexts.join('\n\n') }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get commits/changesets associated with a build
  server.tool(
    PIPELINE_TOOLS.get_build_changes,
    'Get the commits and changesets associated with a specific build.',
    {
      project: z.string().describe('Project ID or name'),
      buildId: z.number().int().positive().describe('Build ID'),
      top: z.number().int().positive().optional().describe('Maximum number of changes to return')
    },
    async ({ project, buildId, top }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        const changes = await buildApi.getBuildChanges(project, buildId, undefined, top, true);
        return { content: [{ type: 'text', text: JSON.stringify(changes, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List published artifacts for a build
  server.tool(
    PIPELINE_TOOLS.list_artifacts,
    'List all published artifacts for a given build.',
    {
      project: z.string().describe('Project ID or name'),
      buildId: z.number().int().positive().describe('Build ID to list artifacts for')
    },
    async ({ project, buildId }) => {
      try {
        const connection = await getADOConnection();
        const buildApi = await connection.getBuildApi();
        const artifacts = await buildApi.getArtifacts(project, buildId);
        return { content: [{ type: 'text', text: JSON.stringify(artifacts, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List variable groups (Library) for a project
  server.tool(
    PIPELINE_TOOLS.list_variable_groups,
    'List variable groups (Library) for a project, optionally filtered by name.',
    {
      project: z.string().describe('Project ID or name'),
      groupName: z.string().optional().describe('Filter by variable group name'),
      top: z.number().int().optional().describe('Maximum number of groups to return')
    },
    async ({ project, groupName, top }) => {
      try {
        const connection = await getADOConnection();
        const taskAgentApi = await connection.getTaskAgentApi();
        const groups = await taskAgentApi.getVariableGroups(project, groupName, undefined, top);
        return { content: [{ type: 'text', text: JSON.stringify(groups, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get a specific variable group (Library) by ID
  server.tool(
    PIPELINE_TOOLS.get_variable_group,
    'Get a specific variable group (Library) by ID, including its variables.',
    {
      project: z.string().describe('Project ID or name'),
      groupId: z.number().int().positive().describe('Variable group ID')
    },
    async ({ project, groupId }) => {
      try {
        const connection = await getADOConnection();
        const taskAgentApi = await connection.getTaskAgentApi();
        const group = await taskAgentApi.getVariableGroup(project, groupId);
        return { content: [{ type: 'text', text: JSON.stringify(group, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );
}

export { PIPELINE_TOOLS, configurePipelineTools };
