import { z } from 'zod';

const msgSearchCommits = (args, repository) => {
  const repoLine = repository ? `\nRepository: ${repository}` : '';
  const termLine = args.searchTerm ? `\nSearch term: ${args.searchTerm}` : '';
  const fromLine = args.fromDate ? `\nFrom: ${args.fromDate}` : '';
  const toLine = args.toDate ? `\nTo: ${args.toDate}` : '';
  return `Search commits in a repository.${repoLine}${termLine}${fromLine}${toLine}\n\nUse repo_search_commits with the provided filters.`;
};

const msgListBranches = (args, repository, tool) => {
  const repoLine = repository ? `\nRepository: ${repository}` : '';
  const filterLine = args.filter ? `\nFilter: ${args.filter}` : '';
  const repoParam = repository ? ` with repositoryId "${repository}"` : '';
  return `List branches in a repository.${repoLine}${filterLine}\n\nUse ${tool}${repoParam}.`;
};

const msgGetBranchDetails = (args, repository) => {
  const repoId = repository || args.repository || '(required)';
  return `Get details for branch "${args.branchName}".\n\nRepository: ${repoId}\n\nUse repo_get_branch_by_name with repositoryId "${repoId}" and branchName "${args.branchName}".`;
};

const msgGetRepoDetails = (project, repository) => {
  const projLine = project ? `\nProject: ${project}` : '';
  const repoLine = repository ? `\nRepository: ${repository}` : '';
  return `Get repository information.${projLine}${repoLine}\n\nUse repo_get_repo_by_name_or_id with the provided project and repositoryNameOrId.`;
};

const msgListProjectRepos = (args, project) => {
  const projLine = project ? `\nProject: ${project}` : '';
  const filterLine = args.filter ? `\nFilter: ${args.filter}` : '';
  const projParam = project || args.project || '(required)';
  const filterParam = args.filter ? ` and repoNameFilter "${args.filter}"` : '';
  return `List all repositories in a project.${projLine}${filterLine}\n\nUse repo_list_repos_by_project with project "${projParam}"${filterParam}.`;
};

const msgGetFileContent = (args, repository, contextBranch) => {
  const repoId = repository || args.repository || '(required)';
  const branch = args.branch || contextBranch || '(default branch)';
  const resolvedBranch = args.branch || contextBranch;
  const versionParam = resolvedBranch ? `, version "${resolvedBranch}"` : '';
  return `Get the content of file "${args.filePath}" from repository.\n\nRepository: ${repoId}\nBranch: ${branch}\n\nUse repo_get_file_content with repositoryId "${repoId}", path "${args.filePath}"${versionParam}.`;
};

const msgListDirectory = (args, repository) => {
  const repoId = repository || args.repository || '(required)';
  const pathLine = args.path ? `\nPath: ${args.path}` : '\nPath: / (root)';
  const branchLine = args.branch ? `\nBranch: ${args.branch}` : '';
  const recursiveLine = args.recursive === 'true' ? '\nRecursive: yes' : '';
  return `List directory contents in a repository.\n\nRepository: ${repoId}${pathLine}${branchLine}${recursiveLine}\n\nUse repo_list_directory with the provided parameters.`;
};

const MESSAGE_GENERATORS = {
  'search-commits': (args, ctx) => msgSearchCommits(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'list-all-branches': (args, ctx) => msgListBranches(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name, 'repo_list_branches_by_repo'),
  'list-my-branches': (args, ctx) => msgListBranches(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name, 'repo_list_my_branches_by_repo'),
  'get-branch-details': (args, ctx) => msgGetBranchDetails(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'get-repository-details': (args, ctx) => msgGetRepoDetails(args.project || ctx?.ado?.project, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'list-project-repositories': (args, ctx) => msgListProjectRepos(args, args.project || ctx?.ado?.project),
  'get-file-content': (args, ctx) => {
    const defaultRepo = ctx?.repositories?.find(r => r.isDefault);
    return msgGetFileContent(args, args.repository || defaultRepo?.name, defaultRepo?.defaultBranch || ctx?.ado?.defaultBranch);
  },
  'list-repo-directory': (args, ctx) => msgListDirectory(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'get-pull-request': (args, ctx) => {
    const repo = args.repositoryId || ctx?.repositories?.find(r => r.isDefault)?.name || '(required)';
    const includeWI = args.includeWorkItems === 'yes' ? 'Include linked work items.' : '';
    return `Get details of pull request ${args.pullRequestId} in repository "${repo}" using repo_get_pull_request_by_id.\n\n${includeWI}\n\nReturn:\n- PR title, description, and status\n- Source and target branches\n- Created by and creation date\n- Reviewers and their vote status\n- Linked work items (if requested)`;
  },
  'my-prs': (args) => {
    const repoLine = args.repository ? `in repository "${args.repository}"` : 'across all repositories';
    return `Show all pull requests ${repoLine} where:\n- I am the creator\n- I am a reviewer\n\nGroup by status (Active, Completed, Abandoned).`;
  },
  'view-pr-threads': (args) =>
    `View all comment threads in pull request: ${args.prUrl}\n\nShow:\n- Thread location (file and line)\n- Comments in each thread\n- Thread status (active/resolved)\n- Participants`,
};

const generateMessage = (name, args, ctx) => {
  const generator = MESSAGE_GENERATORS[name];
  return generator ? generator(args, ctx) : `Run the repository read tool for prompt: ${name}`;
};

export function configureReposReadPrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'search-commits',
      description: 'Search commits in a repository',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        searchTerm: z.string().optional().describe('Text to search in commit messages'),
        fromDate: z.string().optional().describe('Start date (ISO 8601)'),
        toDate: z.string().optional().describe('End date (ISO 8601)')
      }
    },
    {
      name: 'list-all-branches',
      description: 'List all branches in a repository',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        filter: z.string().optional().describe('Filter branches by name substring')
      }
    },
    {
      name: 'list-my-branches',
      description: 'List branches created by the current user',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        filter: z.string().optional().describe('Filter branches by name substring')
      }
    },
    {
      name: 'get-branch-details',
      description: 'Get details for a specific branch',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        branchName: z.string().describe('Branch name (e.g., main, feature/my-feature)')
      }
    },
    {
      name: 'get-repository-details',
      description: 'Get repository information',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        repository: z.string().optional().describe('Repository name or ID')
      }
    },
    {
      name: 'list-project-repositories',
      description: 'List all repositories in a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        filter: z.string().optional().describe('Filter repositories by name')
      }
    },
    {
      name: 'get-file-content',
      description: 'Get the content of a file from a repository',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        filePath: z.string().describe('Path to the file (e.g., /src/index.js)'),
        branch: z.string().optional().describe('Branch name or commit SHA (defaults to default branch)')
      }
    },
    {
      name: 'list-repo-directory',
      description: 'List files and folders in a repository directory',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        path: z.string().optional().describe('Directory path (default: root "/")'),
        branch: z.string().optional().describe('Branch name or commit SHA'),
        recursive: z.string().optional().describe('Set to "true" to list recursively')
      }
    },
    {
      name: 'get-pull-request',
      description: 'Get full details of a pull request by ID',
      args: {
        repositoryId: z.string().optional().describe('Repository name or ID'),
        pullRequestId: z.string().describe('Pull request ID'),
        includeWorkItems: z.string().optional().describe('Include linked work items (yes/no)')
      }
    },
    {
      name: 'my-prs',
      description: 'Show all pull requests I created or need to review',
      args: {
        repository: z.string().optional().describe('Repository name or ID (optional)')
      }
    },
    {
      name: 'view-pr-threads',
      description: 'View all comment threads in a pull request',
      args: {
        prUrl: z.string().describe('Azure DevOps PR URL')
      }
    }
  ];

  for (const prompt of prompts) {
    const callback = async (args) => {
      const ctx = getContext();
      return { messages: [{ role: 'user', content: { type: 'text', text: generateMessage(prompt.name, args ?? {}, ctx) } }] };
    };
    server.prompt(prompt.name, prompt.description, prompt.args, callback);
  }

  console.error(`Registered ${prompts.length} repository read prompts`);
}
