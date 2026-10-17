import { z } from 'zod';
import { detectProxyFor, getConfig } from '@sc-node-mcp/core';

const VSSPS_HOST = 'vssps.dev.azure.com';
let _vsspsProxyPromise;

/** Test-only: reset the cached vssps proxy detection between test cases. */
export function clearVsspsProxyCache() {
  _vsspsProxyPromise = undefined;
}

// vssps.dev.azure.com is a different host from dev.azure.com, which is the only host the shared
// startup proxy auto-detection (packages/core/src/proxy.js) probes. Some users' network routes
// reach dev.azure.com fine but not vssps.dev.azure.com, causing ENOTFOUND here even though every
// other ADO tool works for them — so resolve a proxy specifically for this host, once per process.
function getVsspsProxy() {
  if (!_vsspsProxyPromise) {
    _vsspsProxyPromise = detectProxyFor(VSSPS_HOST, getConfig().HTTPS_PROXY);
  }
  return _vsspsProxyPromise;
}

// Swap HTTPS_PROXY to the vssps-specific proxy just for this call, then restore it — the shared
// azure-devops-node-api connection has no per-request proxy option, only a global env var one.
async function withVsspsProxy(fn) {
  const proxy = await getVsspsProxy();
  const previousUpper = process.env.HTTPS_PROXY;
  const previousLower = process.env.https_proxy;
  if (proxy) {
    process.env.HTTPS_PROXY = proxy;
    process.env.https_proxy = proxy;
  } else {
    delete process.env.HTTPS_PROXY;
    delete process.env.https_proxy;
  }
  try {
    return await fn();
  } finally {
    if (previousUpper === undefined) delete process.env.HTTPS_PROXY; else process.env.HTTPS_PROXY = previousUpper;
    if (previousLower === undefined) delete process.env.https_proxy; else process.env.https_proxy = previousLower;
  }
}

async function fetchIdentityPickerResults(connection, orgName, query) {
  const url = `https://${VSSPS_HOST}/${orgName}/_apis/IdentityPicker/Identities?api-version=7.0-preview.1`;
  const body = {
    query,
    identityTypes: ['user'],
    operationScopes: ['ims', 'source'],
    properties: ['DisplayName', 'Mail', 'SamAccountName', 'SignInAddress'],
    options: { MinResults: 5, MaxResults: 10 }
  };
  const response = await withVsspsProxy(() => connection.rest.create(url, body));
  return response.result?.results?.[0]?.identities || [];
}

// The legacy /_apis/identities endpoint only does exact-string matching (no fuzzy/partial search),
// so "Saravanan R" never matches a directory entry stored as "Raghavan, Saravanan". IdentityPicker
// (used by the ADO web UI's reviewer picker) supports fuzzy matching on name fragments, but only
// within "Surname, Firstname" comma-separated tokens — a plain two-word query without a comma
// returns zero matches, and swapping the two words only helps if they're tried in BOTH comma
// orders (the caller doesn't know which of the two words ADO stores as the surname).
async function resolveIdentityCandidates(connection, orgName, query) {
  const identities = await fetchIdentityPickerResults(connection, orgName, query);
  if (identities.length > 0 || query.includes(',')) return identities;

  const tokens = query.trim().split(/\s+/);
  if (tokens.length === 2) {
    const [a, b] = tokens;
    const swapped = await fetchIdentityPickerResults(connection, orgName, `${b}, ${a}`);
    if (swapped.length > 0) return swapped;
    return fetchIdentityPickerResults(connection, orgName, `${a}, ${b}`);
  }
  return identities;
}

// Tool mapping for repo write MCP tools
const REPO_TOOLS = {
  create_branch: 'repo_create_branch',
  create_pull_request: 'repo_create_pull_request',
  update_pull_request: 'repo_update_pull_request',
  update_pull_request_reviewers: 'repo_update_pull_request_reviewers',
  create_pull_request_thread: 'repo_create_pull_request_thread',
  vote_pull_request: 'repo_vote_pull_request',
  update_pull_request_thread: 'repo_update_pull_request_thread',
  reply_to_comment: 'repo_reply_to_comment',
};

function configureReposWriteTools(server, getADOConnection) {

  server.tool(
    REPO_TOOLS.create_branch,
    'Create a new branch in a repository.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      branchName: z.string().describe('New branch name (e.g., feature/new-feature)'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)'),
      sourceBranchName: z.string().optional().describe('Source branch name to branch from (defaults to default branch)'),
      sourceCommitId: z.string().optional().describe('Source commit ID to branch from')
    },
    async ({ repositoryId, branchName, project, sourceBranchName, sourceCommitId }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Find project if not provided
        let targetProject = project;
        if (!targetProject) {
          const coreApi = await connection.getCoreApi();
          const projects = await coreApi.getProjects();
          for (const proj of projects) {
            try {
              const repo = await gitApi.getRepository(repositoryId, proj.name);
              if (repo) {
                targetProject = proj.name;
                repositoryId = repo.id; // Use repo ID for operations
                break;
              }
            } catch {
              continue;
            }
          }
        }
        
        // Get repository to find default branch if needed
        const repo = await gitApi.getRepository(repositoryId, targetProject);
        
        // Determine source ref
        let sourceRef = sourceCommitId;
        if (!sourceRef && sourceBranchName) {
          const sourceBranch = await gitApi.getBranch(repositoryId, sourceBranchName, targetProject);
          sourceRef = sourceBranch.commit?.commitId;
        } else if (!sourceRef) {
          const defaultBranch = await gitApi.getBranch(repositoryId, repo.defaultBranch?.replace('refs/heads/', '') || 'main', targetProject);
          sourceRef = defaultBranch.commit?.commitId;
        }
        
        // Create branch using refs API
        const refUpdate = {
          name: `refs/heads/${branchName}`,
          oldObjectId: '0000000000000000000000000000000000000000',
          newObjectId: sourceRef
        };
        
        const result = await gitApi.updateRefs([refUpdate], repositoryId, targetProject);
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.create_pull_request,
    'Create a new pull request from a source branch to a target branch in an Azure DevOps repository, with optional title, description, draft mode, labels, and linked work items.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      sourceRefName: z.string().describe('Source branch (e.g., refs/heads/feature or feature)'),
      targetRefName: z.string().describe('Target branch (e.g., refs/heads/main or main)'),
      title: z.string().describe('PR title'),
      description: z.string().optional().describe('PR description'),
      isDraft: z.boolean().optional().describe('Create as draft PR'),
      labels: z.array(z.string()).optional().describe('Labels to add to PR'),
      workItems: z.array(z.number().int()).optional().describe('Work item IDs to link'),
      forkSourceRepositoryId: z.string().optional().describe('Source repository ID if fork')
    },
    async ({ repositoryId, sourceRefName, targetRefName, title, description, isDraft, labels, workItems, forkSourceRepositoryId }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Ensure refs have proper format
        const sourceRef = sourceRefName.startsWith('refs/') ? sourceRefName : `refs/heads/${sourceRefName}`;
        const targetRef = targetRefName.startsWith('refs/') ? targetRefName : `refs/heads/${targetRefName}`;
        
        const pullRequest = {
          sourceRefName: sourceRef,
          targetRefName: targetRef,
          title,
          description,
          isDraft: isDraft || false
        };
        
        if (forkSourceRepositoryId) {
          pullRequest.forkSource = { repository: { id: forkSourceRepositoryId } };
        }
        
        const pr = await gitApi.createPullRequest(pullRequest, repositoryId);
        
        // Add labels if provided
        if (labels && labels.length > 0) {
          await gitApi.createPullRequestLabel({ name: labels[0] }, repositoryId, pr.pullRequestId);
        }
        
        // Link work items if provided
        if (workItems && workItems.length > 0) {
          const workItemApi = await connection.getWorkItemTrackingApi();
          for (const workItemId of workItems) {
            const patch = [{
              op: 'add',
              path: '/relations/-',
              value: {
                rel: 'ArtifactLink',
                url: pr.artifactId,
                attributes: { name: 'Pull Request' }
              }
            }];
            await workItemApi.updateWorkItem(null, patch, workItemId);
          }
        }
        
        return { content: [{ type: 'text', text: JSON.stringify(pr, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.update_pull_request,
    'Update an existing pull request (title, description, status, completion settings).',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)'),
      title: z.string().optional().describe('New PR title'),
      description: z.string().optional().describe('New PR description'),
      status: z.enum(['active', 'abandoned', 'completed']).optional().describe('PR status'),
      autoComplete: z.boolean().optional().describe('Enable auto-complete'),
      deleteSourceBranch: z.boolean().optional().describe('Delete source branch after completion'),
      transitionWorkItems: z.boolean().optional().describe('Transition linked work items'),
      mergeStrategy: z.enum(['noFastForward', 'squash', 'rebase', 'rebaseMerge']).optional().describe('Merge strategy for completion')
    },
    async ({ repositoryId, pullRequestId, project, title, description, status, autoComplete, deleteSourceBranch, transitionWorkItems, mergeStrategy }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Get existing PR to find project if not provided
        let targetProject = project;
        if (!targetProject) {
          const pr = await gitApi.getPullRequestById(pullRequestId);
          targetProject = pr.repository?.project?.name;
        }
        
        // Get the existing PR
        const existingPr = await gitApi.getPullRequest(repositoryId, pullRequestId, targetProject);
        
        // Build update object with only provided fields
        const updatePr = {};
        if (title) updatePr.title = title;
        if (description !== undefined) updatePr.description = description;
        if (status) {
          if (status === 'active') updatePr.status = 1;
          else if (status === 'abandoned') updatePr.status = 2;
          else updatePr.status = 3;
        }
        
        // Handle completion settings
        if (autoComplete !== undefined || deleteSourceBranch !== undefined || transitionWorkItems !== undefined || mergeStrategy !== undefined) {
          let mergeStrategyNum;
          if (mergeStrategy === 'noFastForward') mergeStrategyNum = 2;
          else if (mergeStrategy === 'squash') mergeStrategyNum = 3;
          else if (mergeStrategy === 'rebase') mergeStrategyNum = 4;
          else if (mergeStrategy === 'rebaseMerge') mergeStrategyNum = 5;
          updatePr.completionOptions = {
            deleteSourceBranch: deleteSourceBranch || false,
            transitionWorkItems: transitionWorkItems || false,
            mergeStrategy: mergeStrategyNum
          };
        }
        
        if (autoComplete) {
          updatePr.autoCompleteSetBy = existingPr.createdBy;
        }
        
        const updated = await gitApi.updatePullRequest(updatePr, repositoryId, pullRequestId, targetProject);
        return { content: [{ type: 'text', text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.update_pull_request_reviewers,
    'Add or remove reviewers from a pull request using employee ID, email, or display name (fuzzy-matched, including "Surname, Firstname" order).',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      reviewerIdentifiers: z.array(z.string()).describe('Array of reviewer identifiers: employee IDs (e.g., ["1540326"]), emails (e.g., ["john.doe@company.com"]), or display names (e.g., ["Jane Smith"] or ["Smith, Jane"]) — each array element is one identifier, so a display name containing a comma is safe here'),
      action: z.enum(['add', 'remove']).describe('Action to perform'),
      project: z.string().optional().describe('Azure DevOps project name (auto-discovered if not provided)')
    },
    async ({ repositoryId, pullRequestId, reviewerIdentifiers, action, project }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Find project if not provided
        let targetProject = project;
        if (!targetProject) {
          const pr = await gitApi.getPullRequestById(pullRequestId);
          targetProject = pr.repository?.project?.name;
        }
        
        // Get organization name for API calls
        const orgName = connection.serverUrl.split('/').pop();
        
        const results = [];
        for (const reviewerIdentifier of reviewerIdentifiers) {
          try {
            let userId = null;
            let userName = null;
            
            // Check if identifier is an employee ID (numeric only)
            const searchIdentifier = /^\d+$/.test(reviewerIdentifier)
              ? `${reviewerIdentifier}@zone1.scb.net`
              : reviewerIdentifier;
            
            try {
              const candidates = await resolveIdentityCandidates(connection, orgName, searchIdentifier);
              if (candidates.length > 0) {
                userId = candidates[0].localId || candidates[0].entityId;
                userName = candidates[0].displayName || candidates[0].samAccountName;
              }
            } catch {
              // Identity lookup failed; handled as not-found below
            }
            
            if (!userId) {
              const convertedNote = searchIdentifier === reviewerIdentifier ? '' : ` (converted from ${reviewerIdentifier})`;
              results.push({ 
                identifier: reviewerIdentifier, 
                error: `User not found. Tried: ${searchIdentifier}${convertedNote}`, 
                action 
              });
              continue;
            }
            
            if (action === 'add') {
              const reviewer = await gitApi.createPullRequestReviewer(
                { id: userId },
                repositoryId,
                pullRequestId,
                userId,
                targetProject
              );
              results.push({ 
                identifier: reviewerIdentifier, 
                userId, 
                userName,
                reviewer: {
                  displayName: reviewer.displayName,
                  uniqueName: reviewer.uniqueName,
                  vote: reviewer.vote
                },
                action: 'added' 
              });
            } else {
              await gitApi.deletePullRequestReviewer(repositoryId, pullRequestId, userId, targetProject);
              results.push({ 
                identifier: reviewerIdentifier, 
                userId, 
                userName,
                action: 'removed' 
              });
            }
          } catch (err) {
            results.push({ identifier: reviewerIdentifier, error: err.message, action });
          }
        }
        
        return { content: [{ type: 'text', text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    REPO_TOOLS.create_pull_request_thread,
    'Create a new comment thread on a pull request.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      content: z.string().describe('Comment text'),
      filePath: z.string().optional().describe('File path for line comment'),
      rightFileStartLine: z.number().int().optional().describe('Start line number (right side)'),
      rightFileEndLine: z.number().int().optional().describe('End line number (right side)'),
      rightFileStartOffset: z.number().int().optional().describe('Start offset'),
      rightFileEndOffset: z.number().int().optional().describe('End offset'),
      status: z.enum(['active', 'fixed', 'wontFix', 'closed', 'byDesign', 'pending']).optional().describe('Thread status'),
      project: z.string().optional().describe('Azure DevOps project name')
    },
    async ({ repositoryId, pullRequestId, content, filePath, rightFileStartLine, rightFileEndLine, rightFileStartOffset, rightFileEndOffset, status, project }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Auto-discover project if not provided
        let targetProject = project;
        let targetRepositoryId = repositoryId;
        if (!targetProject) {
          try {
            const pr = await gitApi.getPullRequestById(pullRequestId);
            targetProject = pr.repository?.project?.name;
            
            // Also auto-discover repositoryId if it's a PR-only call
            if (!repositoryId || repositoryId === String(pullRequestId)) {
              targetRepositoryId = pr.repository?.id || pr.repository?.name;
            }
          } catch {
            throw new Error(`Could not find PR ${pullRequestId}. Please provide project and repositoryId parameters.`);
          }
        }
        
        const statusMap = { active: 1, fixed: 2, wontFix: 3, closed: 4, byDesign: 5, pending: 6 };
        const thread = {
          comments: [{ content, commentType: 1 }],
          status: status ? statusMap[status] : 1
        };
        
        if (filePath) {
          thread.threadContext = {
            filePath,
            rightFileStart: rightFileStartLine ? { line: rightFileStartLine, offset: rightFileStartOffset || 1 } : undefined,
            rightFileEnd: rightFileEndLine ? { line: rightFileEndLine, offset: rightFileEndOffset || 1 } : undefined
          };
        }
        
        const result = await gitApi.createThread(thread, targetRepositoryId, pullRequestId, targetProject);
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Vote on a pull request
  server.tool(
    REPO_TOOLS.vote_pull_request,
    'Cast a vote on a pull request (approve, approve with suggestions, wait for author, reject, or reset).',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      vote: z.enum(['approve', 'approveWithSuggestions', 'waitForAuthor', 'reject', 'reset']).describe('Vote to cast on the pull request'),
      project: z.string().optional().describe('Azure DevOps project name')
    },
    async ({ repositoryId, pullRequestId, vote, project }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();

        const voteMap = {
          approve: 10,
          approveWithSuggestions: 5,
          waitForAuthor: -5,
          reject: -10,
          reset: 0
        };

        // Get current user identity
        const pr = await gitApi.getPullRequest(repositoryId, pullRequestId, project);
        const reviewer = { vote: voteMap[vote], id: pr.createdBy?.id };
        const result = await gitApi.createPullRequestReviewer(reviewer, repositoryId, pullRequestId, pr.createdBy?.id, project);
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Update pull request thread status
  server.tool(
    REPO_TOOLS.update_pull_request_thread,
    'Update the status of an existing pull request comment thread (e.g., resolve, close, reactivate).',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      threadId: z.number().int().positive().describe('Thread ID to update'),
      status: z.enum(['active', 'fixed', 'wontFix', 'closed', 'byDesign', 'pending']).describe('New status for the thread'),
      project: z.string().optional().describe('Azure DevOps project name')
    },
    async ({ repositoryId, pullRequestId, threadId, status, project }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        const statusMap = { active: 1, fixed: 2, wontFix: 3, closed: 4, byDesign: 5, pending: 6 };
        const updatedThread = await gitApi.updateThread({ status: statusMap[status] }, repositoryId, pullRequestId, threadId, project);
        return { content: [{ type: 'text', text: JSON.stringify(updatedThread, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Reply to a PR comment thread
  server.tool(
    REPO_TOOLS.reply_to_comment,
    'Reply to a specific comment inside an existing pull request thread.',
    {
      repositoryId: z.string().describe('Repository ID or name'),
      pullRequestId: z.number().int().positive().describe('Pull request ID'),
      threadId: z.number().int().positive().describe('Thread ID to reply to'),
      content: z.string().describe('Reply comment text'),
      project: z.string().optional().describe('Azure DevOps project name')
    },
    async ({ repositoryId, pullRequestId, threadId, content, project }) => {
      try {
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        const comment = { content, commentType: 1 /* text */ };
        const result = await gitApi.createComment(comment, repositoryId, pullRequestId, threadId, project);
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Core identity resolution tool
  server.tool(
    'core_get_identity_ids',
    'Resolve Azure DevOps user identities (names, emails, or usernames) to their ADO identity IDs. Fuzzy-matched, including "Surname, Firstname" order. Call once per person — do not join multiple people into a single searchFilter. Useful for reviewer assignment and other identity-based operations.',
    {
      searchFilter: z.string().describe('A single search term for ONE person (e.g., display name like "Smith, Jane" or "Jane Smith", email address, or username) — do not pass multiple identifiers joined together')
    },
    async ({ searchFilter }) => {
      try {
        const connection = await getADOConnection();
        const orgName = connection.serverUrl.split('/').pop();
        const candidates = await resolveIdentityCandidates(connection, orgName, searchFilter);
        const value = candidates.map((identity) => ({
          id: identity.localId || identity.entityId,
          displayName: identity.displayName,
          mail: identity.mail,
          samAccountName: identity.samAccountName,
          signInAddress: identity.signInAddress,
          isLocal: Boolean(identity.localId)
        }));
        return { content: [{ type: 'text', text: JSON.stringify({ count: value.length, value }, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  console.error('Registered all ADO repository write tools');
}

export { configureReposWriteTools };
