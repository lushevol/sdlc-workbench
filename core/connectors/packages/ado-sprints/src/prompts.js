import { z } from 'zod';

export function configureSprintsPrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'sprint-planning',
      description: 'List backlog levels for a team to support sprint planning',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name')
      }
    },
    {
      name: 'list-project-sprints',
      description: 'List all sprint iterations in a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name')
      }
    },
    {
      name: 'create-sprints',
      description: 'Create new sprint iterations in a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        name: z.string().describe('Sprint name (e.g., Sprint 42)'),
        startDate: z.string().optional().describe('Start date YYYY-MM-DD'),
        endDate: z.string().optional().describe('End date YYYY-MM-DD')
      }
    },
    {
      name: 'list-team-sprint-iterations',
      description: 'List sprint iterations assigned to a team',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        timeframe: z.string().optional().describe('Filter: past, current, or future')
      }
    },
    {
      name: 'assign-sprint-to-team',
      description: 'Assign an existing project iteration to a team',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        iterationId: z.string().describe('Iteration GUID to assign')
      }
    },
    {
      name: 'get-sprint-capacities',
      description: 'Get per-member capacity details for a sprint',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        iterationId: z.string().describe('Iteration GUID')
      }
    },
    {
      name: 'get-team-capacity',
      description: 'Get total team capacity summary for a sprint',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        iterationId: z.string().describe('Iteration GUID')
      }
    },
    {
      name: 'update-team-capacity',
      description: "Update a team member's daily capacity hours for a sprint",
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        iterationId: z.string().describe('Iteration GUID'),
        teamMemberId: z.string().describe('Team member identity GUID'),
        activityName: z.string().describe('Activity name (e.g., Development)'),
        hoursPerDay: z.string().describe('Capacity hours per day')
      }
    },
    {
      name: 'get-team-settings',
      description: 'Get team settings including sprint cadence and working days',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name')
      }
    },
    {
      name: 'list-team-iterations',
      description: 'List all iterations for a team',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name')
      }
    }
  ];

  const messages = {
    'sprint-planning': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      return `List available backlog levels for sprint planning.\n\nProject: ${project}\nTeam: ${team}\n\nUse wit_list_backlogs with project "${project}" and team "${team}".`;
    },
    'list-project-sprints': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `List all sprint iterations in project "${project}".\n\nUse work_list_iterations with project "${project}".`;
    },
    'create-sprints': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const dates = [
        args.startDate ? 'startDate: ' + args.startDate : null,
        args.endDate ? 'finishDate: ' + args.endDate : null
      ].filter(Boolean).join(', ');
      const dateLine = dates ? ' (' + dates + ')' : '';
      const startPart = args.startDate ? ', startDate "' + args.startDate + '"' : '';
      const endPart = args.endDate ? ', finishDate "' + args.endDate + '"' : '';
      return `Create sprint "${args.name}" in project "${project}"${dateLine}.\n\nUse work_create_iterations with project "${project}" and iterations array containing name "${args.name}"${startPart}${endPart}.`;
    },
    'list-team-sprint-iterations': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      const timeframePart = args.timeframe ? ' (' + args.timeframe + ')' : '';
      const timeframeParam = args.timeframe ? ', and timeframe "' + args.timeframe + '"' : '';
      return `List sprint iterations for team "${team}" in project "${project}"${timeframePart}.\n\nUse work_list_team_iterations with project "${project}", team "${team}"${timeframeParam}.`;
    },
    'assign-sprint-to-team': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      return `Assign iteration ${args.iterationId} to team "${team}" in project "${project}".\n\nUse work_assign_iterations with project "${project}", team "${team}", and iterations [{id: "${args.iterationId}"}].`;
    },
    'get-sprint-capacities': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      return `Get per-member capacity for iteration ${args.iterationId}, team "${team}", project "${project}".\n\nUse work_get_team_capacity with project "${project}", team "${team}", and iterationId "${args.iterationId}".`;
    },
    'get-team-capacity': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      return `Get capacity summary for team "${team}" in iteration ${args.iterationId}, project "${project}".\n\nUse work_get_team_capacity with project "${project}", team "${team}", and iterationId "${args.iterationId}".`;
    },
    'update-team-capacity': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      return `Update capacity for member ${args.teamMemberId} in iteration ${args.iterationId}, team "${team}", project "${project}".\n\nActivity: ${args.activityName}, ${args.hoursPerDay} hrs/day.\n\nUse work_update_team_capacity with project "${project}", team "${team}", iterationId "${args.iterationId}", teamMemberId "${args.teamMemberId}", and activities [{name: "${args.activityName}", capacityPerDay: ${args.hoursPerDay}}].`;
    },
    'get-team-settings': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team;
      const teamPart = team ? ' and team "' + team + '"' : '';
      return `Get team settings for project "${project}"${teamPart}.\n\nUse work_get_team_settings with project "${project}"${teamPart}.`;
    },
    'list-team-iterations': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const team = args.team || ctx?.ado?.team || '(required)';
      return `List all iterations for team "${team}" in project "${project}":\n\nInclude:\n- Iteration name and path\n- Start and end dates\n- Current/future/past status`;
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
}
