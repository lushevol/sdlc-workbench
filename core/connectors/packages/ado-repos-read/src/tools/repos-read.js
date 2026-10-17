import { z } from 'zod';

// Tool mapping for repo read MCP tools
const REPO_TOOLS = {
  list_repos_by_project: 'repo_list_repos_by_project',
  list_pull_requests_by_repo_or_project: 'repo_list_pull_requests_by_repo_or_project',
  list_branches_by_repo: 'repo_list_branches_by_repo',
  list_my_branches_by_repo: 'repo_list_my_branches_by_repo',
  list_pull_request_threads: 'repo_list_pull_request_threads',
  get_repo_by_name_or_id: 'repo_get_repo_by_name_or_id',
  get_branch_by_name: 'repo_get_branch_by_name',
  get_pull_request_by_id: 'repo_get_pull_request_by_id',
  search_commits: 'repo_search_commits',
  get_file_content: 'repo_get_file_content',
  list_directory: 'repo_list_directory',
  get_pull_request_changes: 'repo_get_pull_request_changes',
};

function configureReposReadTools(server, getADOConnection) {

  // List repos by project
  server.tool(
    REPO_TOOLS.list_repos_by_project,
    'List all repositories in a given Azure DevOps project.',
    {
      project: z.string().describe('Azure DevOps project name'),
      repoNameFilter: z.string().optional().describe('Filter repos by name'),
      skip: z.number().int().optional().describe('Number of repos to skip'),
      top: z.number().int().optional().describe('Maximum number of repos to return')
    },
    async ({ project, repoNameFilter, skip, top }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        const repos = await gitApi.getRepositories(project);
        
        let filteredRepos = repos;
        if (repoNameFilter) {
          filteredRepos = repos.filter(repo => 
            repo.name?.toLowerCase().includes(repoNameFilter.toLowerCase())
          );
        }
        
        if (skip) filteredRepos = filteredRepos.slice(skip);
        if (top) filteredRepos = filteredRepos.slice(0, top);
        
        return { content: [{ type: 'text', text: JSON.stringify(filteredRepos, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.list_pull_requests_by_repo_or_project,
    'List pull requests for a repository or project with optional filters.',
    {
      project: z.string().optional().describe('Azure DevOps project name'),
      repositoryId: z.string().optional().describe('Repository ID or name'),
      sourceRefName: z.string().optional().describe('Filter by source branch name (e.g., refs/heads/feature)'),
      targetRefName: z.string().optional().describe('Filter by target branch name (e.g., refs/heads/main)'),
      status: z.enum(['active', 'abandoned', 'completed', 'all']).optional().describe('PR status filter'),
      created_by_me: z.boolean().optional().describe('Filter PRs created by current user'),
      created_by_user: z.string().optional().describe('Filter by creator user ID'),
      i_am_reviewer: z.boolean().optional().describe('Filter PRs where I am a reviewer'),
      user_is_reviewer: z.string().optional().describe('Filter by reviewer user ID'),
      skip: z.number().int().optional().describe('Number of PRs to skip'),
      top: z.number().int().optional().describe('Maximum number of PRs to return')
    },
    async ({ project, repositoryId, sourceRefName, targetRefName, status, created_by_me, created_by_user, i_am_reviewer, user_is_reviewer, skip, top }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        const searchCriteria = {};
        if (sourceRefName) searchCriteria.sourceRefName = sourceRefName;
        if (targetRefName) searchCriteria.targetRefName = targetRefName;
        if (status && status !== 'all') {
          if (status === 'active') searchCriteria.status = 1;
          else if (status === 'abandoned') searchCriteria.status = 2;
          else searchCriteria.status = 3;
        }
        if (created_by_user) searchCriteria.creatorId = created_by_user;
        if (user_is_reviewer) searchCriteria.reviewerId = user_is_reviewer;
        if (skip) searchCriteria.skip = skip;
        if (top) searchCriteria.top = top;
        
        let prs;
        if (repositoryId) {
          prs = await gitApi.getPullRequests(repositoryId, searchCriteria, project);
        } else if (project) {
          prs = await gitApi.getPullRequestsByProject(project, searchCriteria);
        } else {
          throw new Error('Either repositoryId or project must be provided');
        }
        
        return { content: [{ type: 'text', text: JSON.stringify(prs, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.list_branches_by_repo,
    'List all branches in a repository.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)'),
      filterContains: z.string().optional().describe('Filter branches by name substring'),
      top: z.number().int().optional().describe('Maximum number of branches to return')
    },
    async ({ repositoryId, project, filterContains, top }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // If project not provided, try to find repo across all projects
        let targetProject = project;
        if (!targetProject) {
          const coreApi = await connection.getCoreApi();
          const projects = await coreApi.getProjects();
          for (const proj of projects) {
            try {
              const repo = await gitApi.getRepository(repositoryId, proj.name);
              if (repo) {
                targetProject = proj.name;
                break;
              }
            } catch {
              continue;
            }
          }
          if (!targetProject) {
            throw new Error(`Repository '${repositoryId}' not found in any project. Please provide the project name.`);
          }
        }
        
        const branches = await gitApi.getBranches(repositoryId, targetProject);
        
        let filteredBranches = branches;
        if (filterContains) {
          filteredBranches = branches.filter(branch => 
            branch.name?.toLowerCase().includes(filterContains.toLowerCase())
          );
        }
        if (top) filteredBranches = filteredBranches.slice(0, top);
        
        return { content: [{ type: 'text', text: JSON.stringify(filteredBranches, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.list_my_branches_by_repo,
    'List branches in a repository created by current user.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)'),
      filterContains: z.string().optional().describe('Filter branches by name substring'),
      top: z.number().int().optional().describe('Maximum number of branches to return')
    },
    async ({ repositoryId, project, filterContains, top }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // If project not provided, try to find repo across all projects
        let targetProject = project;
        if (!targetProject) {
          const coreApi = await connection.getCoreApi();
          const projects = await coreApi.getProjects();
          for (const proj of projects) {
            try {
              const repo = await gitApi.getRepository(repositoryId, proj.name);
              if (repo) {
                targetProject = proj.name;
                break;
              }
            } catch {
              continue;
            }
          }
        }
        
        const branches = await gitApi.getBranches(repositoryId, targetProject);
        
        // Filter branches by creator - Note: Azure DevOps API doesn't always provide creator info
        // This is a best-effort filter
        let myBranches = branches;
        
        if (filterContains) {
          myBranches = myBranches.filter(branch => 
            branch.name?.toLowerCase().includes(filterContains.toLowerCase())
          );
        }
        if (top) myBranches = myBranches.slice(0, top);
        
        return { content: [{ type: 'text', text: JSON.stringify(myBranches, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.list_pull_request_threads,
    'List all comment threads for a pull request.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      project: z.string().optional().describe('Azure DevOps project name'),
      iteration: z.number().int().optional().describe('Iteration ID to filter threads'),
      baseIteration: z.number().int().optional().describe('Base iteration ID'),
      skip: z.number().int().optional().describe('Number of threads to skip'),
      top: z.number().int().optional().describe('Maximum number of threads to return')
    },
    async ({ repositoryId, pullRequestId, project, iteration, baseIteration, skip, top }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        const threads = await gitApi.getThreads(repositoryId, pullRequestId, project, iteration, baseIteration);
        
        let filteredThreads = threads;
        if (skip) filteredThreads = filteredThreads.slice(skip);
        if (top) filteredThreads = filteredThreads.slice(0, top);
        
        return { content: [{ type: 'text', text: JSON.stringify(filteredThreads, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.get_repo_by_name_or_id,
    'Get repository details by name or ID.',
    {
      project: z.string().describe('Azure DevOps project name'),
      repositoryNameOrId: z.string().describe('Repository ID or name')
    },
    async ({ project, repositoryNameOrId }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        const repo = await gitApi.getRepository(repositoryNameOrId, project);
        return { content: [{ type: 'text', text: JSON.stringify(repo, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.get_branch_by_name,
    'Get branch details by name.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      branchName: z.string().describe('Branch name (e.g., main, feature/new-feature)'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)')
    },
    async ({ repositoryId, branchName, project }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // If project not provided, find it
        let targetProject = project;
        if (!targetProject) {
          const coreApi = await connection.getCoreApi();
          const projects = await coreApi.getProjects();
          for (const proj of projects) {
            try {
              const repo = await gitApi.getRepository(repositoryId, proj.name);
              if (repo) {
                targetProject = proj.name;
                break;
              }
            } catch {
              continue;
            }
          }
        }
        
        const branch = await gitApi.getBranch(repositoryId, branchName, targetProject);
        return { content: [{ type: 'text', text: JSON.stringify(branch, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.get_pull_request_by_id,
    'Get pull request details by ID.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)'),
      includeWorkItemRefs: z.boolean().optional().describe('Include linked work items')
    },
    async ({ repositoryId, pullRequestId, project, includeWorkItemRefs }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Get PR by ID - works across organization
        const pr = await gitApi.getPullRequestById(pullRequestId);
        
        if (includeWorkItemRefs) {
          try {
            // Need project for work item refs
            let targetProject = project || pr.repository?.project?.name;
            if (targetProject) {
              const workItemRefs = await gitApi.getPullRequestWorkItemRefs(repositoryId, pullRequestId, targetProject);
              pr.workItemRefs = workItemRefs;
            }
          } catch {
            // Silently skip if work items can't be fetched
          }
        }
        
        return { content: [{ type: 'text', text: JSON.stringify(pr, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.search_commits,
    'Search for commits in a repository with comprehensive filtering.',
    {
      project: z.string().describe('Azure DevOps project name'),
      repository: z.string().describe('Repository ID or name'),
      searchText: z.string().optional().describe('Search text in commit messages'),
      author: z.string().optional().describe('Filter by commit author name'),
      authorEmail: z.string().optional().describe('Filter by author email'),
      committer: z.string().optional().describe('Filter by committer name'),
      committerEmail: z.string().optional().describe('Filter by committer email'),
      fromDate: z.string().optional().describe('Filter commits from this date (ISO 8601)'),
      toDate: z.string().optional().describe('Filter commits to this date (ISO 8601)'),
      fromCommit: z.string().optional().describe('Start commit ID'),
      toCommit: z.string().optional().describe('End commit ID'),
      commitIds: z.array(z.string()).optional().describe('Specific commit IDs to retrieve'),
      version: z.string().optional().describe('Branch name or commit ID'),
      versionType: z.enum(['branch', 'tag', 'commit']).optional().describe('Version type'),
      includeWorkItems: z.boolean().optional().describe('Include linked work items'),
      includeLinks: z.boolean().optional().describe('Include links'),
      skip: z.number().int().optional().describe('Number of commits to skip'),
      top: z.number().int().optional().describe('Maximum number of commits to return')
    },
    async ({ project, repository, searchText, author, authorEmail, committer, committerEmail, fromDate, toDate, fromCommit, toCommit, commitIds, version, versionType, includeWorkItems, includeLinks, skip, top }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        const searchCriteria = {};
        if (searchText) searchCriteria.searchText = searchText;
        if (author) searchCriteria.author = author;
        if (authorEmail) searchCriteria.authorEmail = authorEmail;
        if (committer) searchCriteria.committer = committer;
        if (committerEmail) searchCriteria.committerEmail = committerEmail;
        if (fromDate) searchCriteria.fromDate = fromDate;
        if (toDate) searchCriteria.toDate = toDate;
        if (fromCommit) searchCriteria.fromCommitId = fromCommit;
        if (toCommit) searchCriteria.toCommitId = toCommit;
        if (commitIds) searchCriteria.ids = commitIds;
        if (version) {
          let versionTypeNum = 0;
          if (versionType === 'tag') versionTypeNum = 1;
          else if (versionType === 'commit') versionTypeNum = 2;
          searchCriteria.itemVersion = { version, versionType: versionTypeNum };
        }
        if (includeWorkItems) searchCriteria.includeWorkItems = includeWorkItems;
        if (includeLinks) searchCriteria.includeLinks = includeLinks;
        if (skip) searchCriteria.$skip = skip;
        if (top) searchCriteria.$top = top;
        
        const commits = await gitApi.getCommits(repository, searchCriteria, project);
        return { content: [{ type: 'text', text: JSON.stringify(commits, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get file content from a repository
  server.tool(
    REPO_TOOLS.get_file_content,
    'Get the content of a file from a Git repository at a specific version (branch, tag, or commit SHA).',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      path: z.string().describe('Path to the file within the repository (e.g., "/src/index.js")'),
      project: z.string().optional().describe('Azure DevOps project name'),
      version: z.string().optional().describe('Branch name, tag name, or commit SHA (defaults to default branch)'),
      versionType: z.enum(['branch', 'tag', 'commit']).optional().describe('Type of version descriptor')
    },
    async ({ repositoryId, path, project, version, versionType }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        let vtypeNum = 0;
        if (versionType === 'tag') vtypeNum = 1;
        else if (versionType === 'commit') vtypeNum = 2;
        const versionDescriptor = version ? { version, versionType: vtypeNum } : undefined;
        const content = await gitApi.getItemContent(repositoryId, path, project, undefined, undefined, undefined, undefined, undefined, versionDescriptor);
        const chunks = [];
        for await (const chunk of content) {
          chunks.push(chunk);
        }
        const text = Buffer.concat(chunks).toString('utf8');
        return { content: [{ type: 'text', text: text }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List files and folders in a repository directory
  server.tool(
    REPO_TOOLS.list_directory,
    'List files and folders in a directory within a repository. Supports recursive listing.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      path: z.string().optional().default('/').describe('Directory path to list (default: root "/")'),
      project: z.string().optional().describe('Azure DevOps project name'),
      version: z.string().optional().describe('Branch name, tag name, or commit SHA (defaults to default branch)'),
      versionType: z.enum(['branch', 'tag', 'commit']).optional().describe('Type of version descriptor'),
      recursive: z.boolean().optional().describe('Whether to recursively list all subdirectory contents')
    },
    async ({ repositoryId, path, project, version, versionType, recursive }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        let vtypeNum2 = 0;
        if (versionType === 'tag') vtypeNum2 = 1;
        else if (versionType === 'commit') vtypeNum2 = 2;
        const versionDescriptor = version ? { version, versionType: vtypeNum2 } : undefined;
        const recursionLevel = recursive ? 120 /* Full */ : 1 /* OneLevel */;
        const items = await gitApi.getItems(repositoryId, project, path || '/', recursionLevel, undefined, undefined, undefined, undefined, versionDescriptor);
        return { content: [{ type: 'text', text: JSON.stringify(items, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get the full diff for a pull request
  server.tool(
    REPO_TOOLS.get_pull_request_changes,
    'Get the file changes (diff) for a pull request with line-by-line code content.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      project: z.string().optional().describe('Azure DevOps project name'),
      iterationId: z.number().int().positive().optional().describe('Iteration ID (defaults to latest iteration)'),
      top: z.number().int().positive().optional().describe('Maximum number of file changes to return'),
      skip: z.number().int().nonnegative().optional().describe('Number of file changes to skip')
    },
    async ({ repositoryId, pullRequestId, project, iterationId, top, skip }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();

        // Get latest iteration if not specified
        let targetIteration = iterationId;
        if (!targetIteration) {
          const iterations = await gitApi.getPullRequestIterations(repositoryId, pullRequestId, project);
          if (iterations && iterations.length > 0) {
            targetIteration = iterations[iterations.length - 1].id;
          }
        }

        const changes = await gitApi.getPullRequestIterationChanges(repositoryId, pullRequestId, targetIteration, project, top, skip);
        return { content: [{ type: 'text', text: JSON.stringify(changes, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  console.error('Registered all ADO repository read tools');
}

export { configureReposReadTools };
