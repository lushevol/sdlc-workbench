import { z } from 'zod';

export function configurePipelinePrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'run-pipeline',
      description: 'Run a pipeline',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        pipelineId: z.string().describe('Pipeline definition ID to run'),
        branchName: z.string().optional().describe('Branch to run the pipeline on')
      }
    },
    {
      name: 'list-pipeline-runs',
      description: 'List pipeline runs with optional filters',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        pipelineId: z.string().optional().describe('Pipeline definition ID to filter runs'),
        branchName: z.string().optional().describe('Branch name to filter runs'),
        statusFilter: z.string().optional().describe('Status filter: inProgress, completed, cancelling, all')
      }
    },
    {
      name: 'get-pipeline-status',
      description: 'Get the status of a specific build or pipeline run',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID to check status for')
      }
    },
    {
      name: 'cancel-pipeline',
      description: 'Cancel a running pipeline build',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID to cancel')
      }
    },
    {
      name: 'list-build-definitions',
      description: 'List pipeline/build definitions in a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        name: z.string().optional().describe('Filter by definition name'),
        repositoryId: z.string().optional().describe('Filter by repository ID')
      }
    },
    {
      name: 'get-builds',
      description: 'Get builds with optional branch, status, and result filters',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        branchName: z.string().optional().describe('Branch name to filter builds'),
        statusFilter: z.string().optional().describe('Status filter: inProgress, completed, cancelling, notStarted, all'),
        resultFilter: z.string().optional().describe('Result filter: succeeded, partiallySucceeded, failed, canceled, all')
      }
    },
    {
      name: 'list-work-item-pipelines',
      description: 'Find all pipeline runs linked to a specific work item',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        workItemId: z.string().describe('Work item ID to find associated pipeline runs for')
      }
    },
    {
      name: 'get-build-logs',
      description: 'Get the combined log output for all steps of a build',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID to retrieve logs for'),
        filter: z.string().optional().describe('Optional text to filter log output')
      }
    },
    {
      name: 'get-build-changes',
      description: 'Get commits and changesets associated with a build',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID to get associated changes for'),
        top: z.string().optional().describe('Maximum number of changes to return')
      }
    },
    {
      name: 'list-build-artifacts',
      description: 'List all published artifacts for a build',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID to list artifacts for')
      }
    },
    {
      name: 'get-pipeline-run',
      description: 'Get details of a specific pipeline run',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        pipelineId: z.string().describe('Pipeline definition ID'),
        runId: z.string().describe('Run ID to retrieve details for')
      }
    },
    {
      name: 'retry-pipeline-stage',
      description: 'Retry a specific stage in a pipeline run',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID containing the stage to retry'),
        stageName: z.string().describe('Name of the stage to retry'),
        forceRetryAllJobs: z.string().optional().describe('Set to "true" to force retry all jobs in the stage')
      }
    },
    {
      name: 'list-variable-groups',
      description: 'List variable groups (Library) for a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        groupName: z.string().optional().describe('Filter by variable group name')
      }
    },
    {
      name: 'get-variable-group',
      description: 'Get a specific variable group (Library) by ID',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        groupId: z.string().describe('Variable group ID')
      }
    }
  ];

  const messages = {
    'run-pipeline': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const branchLine = args.branchName ? `\nBranch: ${args.branchName}` : '';
      const branchParam = args.branchName ? ` and branchName "${args.branchName}"` : '';
      return `Trigger pipeline run.\n\nProject: ${project}\nPipeline ID: ${args.pipelineId}${branchLine}\n\nUse pipelines_run_pipeline with project "${project}" and pipelineId ${args.pipelineId}${branchParam}.`;
    },
    'list-pipeline-runs': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const filters = [
        args.pipelineId ? `pipelineId: ${args.pipelineId}` : null,
        args.branchName ? `branch: ${args.branchName}` : null,
        args.statusFilter ? `status: ${args.statusFilter}` : null
      ].filter(Boolean).join(', ');
      const filterLine = filters ? `\nFilters: ${filters}` : '';
      return `List pipeline runs in project "${project}".${filterLine}\n\nUse pipelines_list_runs with the specified filters.`;
    },
    'get-pipeline-status': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Get status of build ${args.buildId} in project "${project}".\n\nUse pipelines_get_build_status with project "${project}" and buildId ${args.buildId}.`;
    },
    'cancel-pipeline': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Cancel build ${args.buildId} in project "${project}".\n\nUse pipelines_cancel_run with project "${project}" and buildId ${args.buildId}.`;
    },
    'list-build-definitions': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const filters = [
        args.name ? `name: ${args.name}` : null,
        args.repositoryId ? `repositoryId: ${args.repositoryId}` : null
      ].filter(Boolean).join(', ');
      const filterLine = filters ? `\nFilters: ${filters}` : '';
      return `List build definitions in project "${project}".${filterLine}\n\nUse pipelines_get_build_definitions.`;
    },
    'get-builds': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const filters = [
        args.branchName ? `branch: ${args.branchName}` : null,
        args.statusFilter ? `status: ${args.statusFilter}` : null,
        args.resultFilter ? `result: ${args.resultFilter}` : null
      ].filter(Boolean).join(', ');
      const filterLine = filters ? `\nFilters: ${filters}` : '';
      return `Get builds in project "${project}".${filterLine}\n\nUse pipelines_get_builds with the specified filters.`;
    },
    'list-work-item-pipelines': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Find pipeline runs linked to work item ${args.workItemId} in project "${project}".\n\nUse pipelines_list_work_item_pipelines with project "${project}" and workItemId ${args.workItemId}.`;
    },
    'get-build-logs': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const filterLine = args.filter ? `\nFilter: ${args.filter}` : '';
      return `Get log output for build ${args.buildId} in project "${project}".${filterLine}\n\nUse pipelines_get_build_log with project "${project}" and buildId ${args.buildId}.`;
    },
    'get-build-changes': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const limitLine = args.top ? `\nLimit: ${args.top}` : '';
      return `Get commits associated with build ${args.buildId} in project "${project}".${limitLine}\n\nUse pipelines_get_build_changes with project "${project}" and buildId ${args.buildId}.`;
    },
    'list-build-artifacts': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `List published artifacts for build ${args.buildId} in project "${project}".\n\nUse pipelines_list_artifacts with project "${project}" and buildId ${args.buildId}.`;
    },
    'get-pipeline-run': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Get details of run ${args.runId} for pipeline ${args.pipelineId} in project "${project}".\n\nUse pipelines_get_run with project "${project}", pipelineId ${args.pipelineId}, and runId ${args.runId}.`;
    },
    'retry-pipeline-stage': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const force = args.forceRetryAllJobs === 'true' ? ' with forceRetryAllJobs: true' : '';
      return `Retry stage "${args.stageName}" in build ${args.buildId} in project "${project}"${force}.\n\nUse pipelines_retry_stage with project "${project}", buildId ${args.buildId}, and stageName "${args.stageName}".`;
    },
    'list-variable-groups': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const filterLine = args.groupName ? `\nFilter: name contains "${args.groupName}"` : '';
      const groupNameParam = args.groupName ? ` and groupName "${args.groupName}"` : '';
      return `List variable groups (Library) in project "${project}".${filterLine}\n\nUse pipelines_list_variable_groups with project "${project}"${groupNameParam}.`;
    },
    'get-variable-group': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Get variable group ${args.groupId} in project "${project}".\n\nUse pipelines_get_variable_group with project "${project}" and groupId ${args.groupId}.`;
    }
  };

  for (const prompt of prompts) {
    const callback = async (args) => {
      const ctx = getContext();
      const text = messages[prompt.name](args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text } }] };
    };
    server.prompt(prompt.name, prompt.description, prompt.args, callback);
  }

  console.error(`Registered ${prompts.length} pipeline prompts`);
}
