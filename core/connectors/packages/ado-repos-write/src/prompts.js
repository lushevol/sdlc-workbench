import { z } from 'zod';

const msgCreateBranch = (args, repository, ctx) => {
  const repoId = repository || args.repository || '(required)';
  const sourceBranch = args.sourceBranch || ctx?.ado?.defaultBranch;
  const sourceLine = sourceBranch ? `\nSource branch: ${sourceBranch}` : '';
  const sourceParam = sourceBranch ? ` from sourceBranchName "${sourceBranch}"` : '';
  return `Create a new branch "${args.branchName}" in repository.\n\nRepository: ${repoId}${sourceLine}\n\nUse repo_create_branch with repositoryId "${repoId}" and branchName "${args.branchName}"${sourceParam}.`;
};

const msgManagePrReviewers = (args) =>
  `${args.action === 'add' ? 'Add' : 'Remove'} reviewers on PR.\n\nPR URL: ${args.prUrl}\nAction: ${args.action}\nReviewers: ${args.reviewers}\n\nParse the PR ID from the URL and use repo_update_pull_request_reviewers with action "${args.action}" and reviewerIdentifiers array. Reviewers are separated by semicolons (";"), not commas — display names may themselves contain a comma (e.g. "Surname, Firstname"), so split only on ";" and keep each identifier intact.`;

const msgCreatePrThread = (args) =>
  `Create a comment thread on a pull request file.\n\nPR URL: ${args.prUrl}\nFile: ${args.filePath}\nLine: ${args.line}\nComment: ${args.comment}\n\nParse the PR ID from the URL and use repo_create_pull_request_thread with filePath "${args.filePath}", rightFileStartLine ${args.line}.`;

const msgGetPrFileChanges = (args, repository) => {
  const repoId = repository || args.repository || '(required)';
  return `Get the file changes for PR #${args.pullRequestId}.\n\nRepository: ${repoId}\n\nUse repo_get_pull_request_changes with repositoryId "${repoId}" and pullRequestId ${args.pullRequestId}.`;
};

const msgVotePr = (args, repository) => {
  const repoId = repository || args.repository || '(required)';
  return `Cast a vote on PR #${args.pullRequestId}.\n\nRepository: ${repoId}\nVote: ${args.vote}\n\nUse repo_vote_pull_request with repositoryId "${repoId}", pullRequestId ${args.pullRequestId}, and vote "${args.vote}".`;
};

const msgUpdateThreadStatus = (args, repository) => {
  const repoId = repository || args.repository || '(required)';
  return `Update the status of thread #${args.threadId} on PR #${args.pullRequestId}.\n\nRepository: ${repoId}\nNew status: ${args.status}\n\nUse repo_update_pull_request_thread with repositoryId "${repoId}", pullRequestId ${args.pullRequestId}, threadId ${args.threadId}, status "${args.status}".`;
};

const msgReplyToComment = (args, repository) => {
  const repoId = repository || args.repository || '(required)';
  return `Reply to thread #${args.threadId} on PR #${args.pullRequestId}.\n\nRepository: ${repoId}\nContent: ${args.content}\n\nUse repo_reply_to_comment with repositoryId "${repoId}", pullRequestId ${args.pullRequestId}, threadId ${args.threadId}, content "${args.content}".`;
};

const msgPostPrComment = (args) => {
  const replyOrCreate = args.threadId ? `and use repo_reply_to_comment on threadId ${args.threadId}` : 'and use repo_create_pull_request_thread';
  return `Post a review comment on a pull request.\n\nPR URL: ${args.prUrl}\nFile: ${args.filePath}\nLine: ${args.line}\nComment: ${args.comment}\n\nParse the PR ID from the URL ${replyOrCreate} with the provided file and line details.`;
};

const msgGetIdentityIds = (args) =>
  `Look up Azure DevOps identity GUIDs for the provided identifiers.\n\nIdentifiers: ${args.identifiers}\n\nSplit only on semicolons (";") to get each identifier — display names may themselves contain a comma (e.g. "Surname, Firstname"), so a comma is part of a single identifier, not a separator. Use core_get_identity_ids with searchFilter set to each identifier to resolve their ADO identity IDs.`;

const msgCreatePr = (args, repository) => {
  const repo = repository || args.repository || '(required)';
  return `Create a new pull request:\n\nRepository: ${repo}\nSource: ${args.sourceBranch}\nTarget: ${args.targetBranch}\nTitle: ${args.title}\n\nPlease help me:\n1. Generate a detailed description based on changes\n2. Suggest appropriate reviewers\n3. Link related work items\n4. Add appropriate labels`;
};

const msgUpdatePullRequest = (args) => {
  const prLine = args.prUrl || `Repository: ${args.repository}`;
  const strategyLine = args.mergeStrategy ? `\nMerge strategy: ${args.mergeStrategy}` : '';
  const deleteLine = args.deleteSourceBranch ? `\nDelete source branch: ${args.deleteSourceBranch}` : '';
  const suffix = args.action === 'complete' ? ` using the ${args.mergeStrategy || 'merge'} strategy` : '';
  return `Update pull request using repo_update_pull_request:\n\n${prLine}\nAction: ${args.action}${strategyLine}${deleteLine}\n\nThis will ${args.action} the pull request${suffix}.`;
};

const MESSAGE_GENERATORS = {
  'create-branch': (args, ctx) => msgCreateBranch(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name, ctx),
  'manage-pr-reviewers': (args) => msgManagePrReviewers(args),
  'create-pr-thread': (args) => msgCreatePrThread(args),
  'get-pr-file-changes': (args, ctx) => msgGetPrFileChanges(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'vote-pull-request': (args, ctx) => msgVotePr(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'update-pr-thread-status': (args, ctx) => msgUpdateThreadStatus(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'reply-to-pr-comment': (args, ctx) => msgReplyToComment(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'post-pr-comment': (args) => msgPostPrComment(args),
  'get-identity-ids': (args) => msgGetIdentityIds(args),
  'create-pr': (args, ctx) => msgCreatePr(args, args.repository || ctx?.repositories?.find(r => r.isDefault)?.name),
  'update-pull-request': (args) => msgUpdatePullRequest(args),
};

const generateMessage = (name, args, ctx) => {
  const generator = MESSAGE_GENERATORS[name];
  return generator ? generator(args, ctx) : `Run the repository write tool for prompt: ${name}`;
};

export function configureReposWritePrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'create-branch',
      description: 'Create a new branch in a repository',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        branchName: z.string().describe('New branch name (e.g., feature/my-feature)'),
        sourceBranch: z.string().optional().describe('Source branch to branch from (defaults to default branch)')
      }
    },
    {
      name: 'manage-pr-reviewers',
      description: 'Add or remove reviewers on a pull request',
      args: {
        prUrl: z.string().describe('Pull request URL'),
        action: z.string().describe('Action to perform: add or remove'),
        reviewers: z.string().describe('Semicolon-separated list of reviewer identifiers (emails, employee IDs, or display names, e.g. "Surname, Firstname; jane.doe@company.com")')
      }
    },
    {
      name: 'create-pr-thread',
      description: 'Create a comment thread on a pull request',
      args: {
        prUrl: z.string().describe('Pull request URL'),
        filePath: z.string().describe('File path to comment on'),
        line: z.string().describe('Line number to comment on'),
        comment: z.string().describe('Comment text')
      }
    },
    {
      name: 'get-pr-file-changes',
      description: 'Get file changes for a pull request',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        pullRequestId: z.string().describe('Pull request ID')
      }
    },
    {
      name: 'vote-pull-request',
      description: 'Cast a vote on a pull request',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        pullRequestId: z.string().describe('Pull request ID'),
        vote: z.string().describe('Vote to cast: approve, approveWithSuggestions, waitForAuthor, reject, or reset')
      }
    },
    {
      name: 'update-pr-thread-status',
      description: 'Update the status of a pull request comment thread',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        pullRequestId: z.string().describe('Pull request ID'),
        threadId: z.string().describe('Thread ID to update'),
        status: z.string().describe('New status: active, fixed, wontFix, closed, byDesign, or pending')
      }
    },
    {
      name: 'reply-to-pr-comment',
      description: 'Reply to an existing pull request comment thread',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        pullRequestId: z.string().describe('Pull request ID'),
        threadId: z.string().describe('Thread ID to reply to'),
        content: z.string().describe('Reply text')
      }
    },
    {
      name: 'post-pr-comment',
      description: 'Post a review comment on a pull request',
      args: {
        prUrl: z.string().describe('Pull request URL'),
        filePath: z.string().describe('File path to comment on'),
        line: z.string().describe('Line number to comment on'),
        comment: z.string().describe('Comment text'),
        threadId: z.string().optional().describe('Existing thread ID to reply to (omit to create new thread)')
      }
    },
    {
      name: 'get-identity-ids',
      description: 'Look up Azure DevOps identity GUIDs for users',
      args: {
        identifiers: z.string().describe('Semicolon-separated list of identifiers (emails, employee IDs, or display names, e.g. "Surname, Firstname; jane.doe@company.com")')
      }
    },
    {
      name: 'create-pr',
      description: 'Create a new pull request with description and reviewers',
      args: {
        repository: z.string().optional().describe('Repository name or ID'),
        sourceBranch: z.string().describe('Source branch name'),
        targetBranch: z.string().describe('Target branch name (e.g., main)'),
        title: z.string().describe('PR title')
      }
    },
    {
      name: 'update-pull-request',
      description: 'Update pull request status, merge settings, or complete/abandon it',
      args: {
        prUrl: z.string().describe('Azure DevOps PR URL or PR ID'),
        action: z.string().describe('Action: complete, abandon, reactivate, or draft'),
        mergeStrategy: z.string().optional().describe('Merge strategy when completing: squash, merge, or rebase'),
        deleteSourceBranch: z.string().optional().describe('Delete source branch after merge (yes/no)'),
        repository: z.string().optional().describe('Repository name or ID')
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

  console.error(`Registered ${prompts.length} repository write prompts`);
}
