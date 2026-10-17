import { z } from 'zod';

function configureSprintsTools(server, getADOConnection) {

  // List all iterations in a project
  server.tool(
    'work_list_iterations',
    'List all iterations (sprints) defined in an Azure DevOps project.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      depth: z.number().int().nonnegative().optional().describe('Depth of child nodes to retrieve (default: all)')
    },
    async ({ project, depth }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const iterations = await witApi.getClassificationNode(project, 1 /* Iterations */, undefined, depth);
        return { content: [{ type: 'text', text: JSON.stringify(iterations, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Create new iterations in a project
  server.tool(
    'work_create_iterations',
    'Create new sprint iterations in an Azure DevOps project.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      iterations: z.array(z.object({
        name: z.string().describe('Name of the iteration (e.g., "Sprint 1")'),
        startDate: z.string().optional().describe('Start date in ISO 8601 format (e.g., "2026-04-21")'),
        finishDate: z.string().optional().describe('Finish date in ISO 8601 format (e.g., "2026-05-04")')
      })).describe('Array of iterations to create')
    },
    async ({ project, iterations }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const results = [];
        for (const iter of iterations) {
          const node = { name: iter.name, attributes: {} };
          if (iter.startDate) node.attributes.startDate = iter.startDate;
          if (iter.finishDate) node.attributes.finishDate = iter.finishDate;
          const created = await witApi.createOrUpdateClassificationNode(node, project, 1 /* Iterations */);
          results.push(created);
        }
        return { content: [{ type: 'text', text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List iterations assigned to a specific team
  server.tool(
    'work_list_team_iterations',
    'List sprint iterations assigned to a specific team in a project.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      team: z.string().describe('Team name or ID'),
      timeframe: z.enum(['past', 'current', 'future']).optional().describe('Filter iterations by timeframe')
    },
    async ({ project, team, timeframe }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const teamContext = { project, team };
        const iterations = await workApi.getTeamIterations(teamContext, timeframe);
        return { content: [{ type: 'text', text: JSON.stringify(iterations, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Assign iterations to a team
  server.tool(
    'work_assign_iterations',
    'Assign existing project iterations to a specific team.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      team: z.string().describe('Team name or ID'),
      iterations: z.array(z.object({
        id: z.string().describe('Iteration GUID to assign to the team')
      })).describe('Array of iteration objects with their GUIDs')
    },
    async ({ project, team, iterations }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const teamContext = { project, team };
        const results = [];
        for (const iter of iterations) {
          const assigned = await workApi.postTeamIteration({ id: iter.id }, teamContext);
          results.push(assigned);
        }
        return { content: [{ type: 'text', text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get capacity for all teams in an iteration
  server.tool(
    'work_get_iteration_capacities',
    'Get capacity breakdown for all teams in a project iteration.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      iterationId: z.string().describe('Iteration GUID')
    },
    async ({ project, iterationId }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const coreApi = await connection.getCoreApi();
        const teams = await coreApi.getTeams(project);
        const results = [];
        for (const team of teams) {
          try {
            const teamContext = { project, team: team.name };
            const capacities = await workApi.getCapacitiesWithIdentityRefAndTotals(teamContext, iterationId);
            results.push({ team: team.name, capacities });
          } catch {
            // Skip teams that error
          }
        }
        return { content: [{ type: 'text', text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get capacity for a specific team in an iteration
  server.tool(
    'work_get_team_capacity',
    'Get capacity for a specific team in a specific sprint iteration.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      team: z.string().describe('Team name or ID'),
      iterationId: z.string().describe('Iteration GUID')
    },
    async ({ project, team, iterationId }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const teamContext = { project, team };
        const capacities = await workApi.getCapacitiesWithIdentityRefAndTotals(teamContext, iterationId);
        return { content: [{ type: 'text', text: JSON.stringify(capacities, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Update a team member's capacity for an iteration
  server.tool(
    'work_update_team_capacity',
    "Update a team member's activity capacity for a sprint.",
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      team: z.string().describe('Team name or ID'),
      iterationId: z.string().describe('Iteration GUID'),
      teamMemberId: z.string().describe('Team member identity ID (GUID)'),
      activities: z.array(z.object({
        name: z.string().describe('Activity name (e.g., "Development", "Testing")'),
        capacityPerDay: z.number().nonnegative().describe('Hours per day for this activity')
      })).describe('List of activities with capacity per day'),
      daysOff: z.array(z.object({
        start: z.string().describe('Start date of days off in ISO 8601 format'),
        end: z.string().describe('End date of days off in ISO 8601 format')
      })).optional().describe('Optional list of days-off date ranges')
    },
    async ({ project, team, iterationId, teamMemberId, activities, daysOff }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const teamContext = { project, team };
        const patch = { activities };
        if (daysOff) patch.daysOff = daysOff;
        const updated = await workApi.updateCapacityWithIdentityRef(patch, teamContext, iterationId, teamMemberId);
        return { content: [{ type: 'text', text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get team settings
  server.tool(
    'work_get_team_settings',
    'Get team settings including default iteration, backlog iteration, and default area path.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      team: z.string().optional().describe('Team name or ID (uses default team if not provided)')
    },
    async ({ project, team }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const teamContext = { project, team };
        const settings = await workApi.getTeamSettings(teamContext);
        return { content: [{ type: 'text', text: JSON.stringify(settings, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );
}

export { configureSprintsTools };
