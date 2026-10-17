import { z } from "zod";
import fs from 'node:fs/promises';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

/**
 * Load code review instructions from the configured file path.
 * Reads the file at `codeReviewGuideFile` directly.
 *
 * If no file path is configured, returns a notice prompting the user to set
 * `CODE_REVIEW_GUIDE_FILE`.
 *
 * @param {string} [codeReviewGuideFile] - Full path to the review guidelines file (e.g. /path/to/CODE_REVIEW_GUIDE.md)
 * @returns {Promise<string>} Review instruction text or a configuration notice
 */
async function getRefactorInstructions(codeReviewGuideFile) {
  if (!codeReviewGuideFile) {
    return 'No review guidelines configured. Set `CODE_REVIEW_GUIDE_FILE` to the full path of your review guidelines file (e.g. /path/to/CODE_REVIEW_GUIDE.md).';
  }

  try {
    return await fs.readFile(codeReviewGuideFile, 'utf8');
  } catch {
    return `Could not load review guidelines from \`${codeReviewGuideFile}\`. Ensure the file exists.`;
  }
}

const execFileAsync = promisify(execFile);

// Git ref names are NOT restricted to shell-safe characters, so PR branch names
// must be validated before ever reaching a subprocess call.
const SAFE_REF_NAME = /^(?!-)(?!.*\.\.)[A-Za-z0-9._/-]+$/;

function assertSafeRefName(name, label) {
  if (!SAFE_REF_NAME.test(name)) {
    throw new Error(`Refusing to run git commands against unsafe ${label} ref name: ${name}`);
  }
  return name;
}

/**
 * Run git via execFile (argument array, no shell) so branch/ref names can never
 * be interpreted as shell syntax, regardless of their content.
 */
async function runGit(args, cwd) {
  const env = { ...process.env, GIT_SSL_NO_VERIFY: 'true' };
  return execFileAsync('git', args, { cwd, env });
}

const STALE_TEMP_REPO_MS = 6 * 60 * 60 * 1000; // 6 hours

/**
 * Remove leftover clone dirs from a prior run that was killed before its own
 * `finally` cleanup could run. Non-fatal: normal runs clean up themselves.
 */
async function pruneStaleTempRepos(tempReposDir) {
  let entries;
  try {
    entries = await fs.readdir(tempReposDir);
  } catch {
    return;
  }
  const now = Date.now();
  await Promise.all(entries.map(async (entry) => {
    const match = entry.match(/^pr(?:review|diff)-\d+-(\d+)$/);
    if (!match || now - Number(match[1]) < STALE_TEMP_REPO_MS) return;
    try {
      await fs.rm(path.join(tempReposDir, entry), { recursive: true, force: true });
    } catch { /* non-fatal */ }
  }));
}

/**
 * PR Review Tool: Automated Azure DevOps PR review utilities.
 *
 * ## Tool Prompts and Usage
 *
 * 1. Check PR for String Literals and Code Issues
 *    - Prompt: `Check PR <PR_URL>`
 *    - Checks all files modified in a PR for string literals in variable or object assignments and suggests moving them to a constants file. Also checks for hex color codes, equality checks, quote style, unused variables, and refactor suggestions. Posts comments directly in the Azure DevOps PR.
 *    - Parameters: <PR_URL> (Azure DevOps Pull Request URL)
 *
 * 2. Review PR Details
 *    - Prompt: `Review PR <PR_URL>`
 *    - Reviews a pull request by providing its Azure DevOps PR URL. Returns PR details including status, reviewers, branches, and description.
 *    - Parameters: <PR_URL> (Azure DevOps Pull Request URL)
 *
 * 3. Get PR Diff
 *    - Prompt: `PR Diff <PR_URL>`
 *    - Gets the diff of a pull request by providing its Azure DevOps PR URL. Shows the full file diffs between source and target branches.
 *    - Parameters: <PR_URL> (Azure DevOps Pull Request URL)
 *
 * Notes:
 * - The tool is context-aware and avoids false positives (e.g., does not comment on string-to-constant in constants.js, checks for variable usage in template literals, and detects multi-line nested ifs).
 * - Comments are posted directly to the PR in Azure DevOps for actionable feedback.
 *
 * TODO: When the 'repo_review_pr' tool is called, Copilot will always analyze the diff, generate actionable suggestions, and use the 'post_pr_comment' tool to post comments in the PR, without need of another prompt.
 */

/**
 * Configure PR review tools for the MCP server.
 * 
 * IMPORTANT: All review analysis and suggestions are performed by Copilot (the AI), not by code logic.
 * These tools only fetch diffs and PR context for Copilot to process.
 * 
 * @param {Object} server - MCP server instance
 * @param {Function} getADOConnection - Function to get Azure DevOps connection
 * @param {Object} [options={}] - Optional configuration
 * @param {string} [options.codeReviewGuideFile] - Full path to the review guidelines file (e.g. /path/to/CODE_REVIEW_GUIDE.md)
 */
function configureReviewTool(server, getADOConnection, options = {}) {
  const { codeReviewGuideFile } = options;
  // =============================================================
  // PR Review Tool Configuration
  // =============================================================
  // NOTE: All review analysis, suggestions, and posting of comments are ALWAYS
  // performed by Copilot (the AI) and not by any code logic in this repo.
  // No review logic is present in this codebase; tools only fetch diff and
  // context for Copilot to process.
  // =============================================================  

  const DELETION_SUCCESS = (count, prId) => `Deleted ${count} AI review comment(s) from PR ${prId}.`;
  const THREAD_REPLY_SUCCESS = (threadId, prId) => `Replied to thread ${threadId} in PR ${prId}.`;
  const NEW_THREAD_SUCCESS = (prId, filePath, line) => `Posted new comment thread in PR ${prId} on ${filePath} at line ${line}.`;
  
  // Tool to post a comment on a PR (new thread or reply to existing thread) post_pr_comment
  server.tool(
    "post_pr_comment",
    "Post a comment on a PR. Usage: 'Post PR Comment <PR_URL> <filePath> <line> <commentText> [threadId]'. If threadId is omitted, creates a new thread.",
    {
      prUrl: z.string().url().describe("Azure DevOps Pull Request URL"),
      filePath: z.string().describe("File path in the PR (relative to repo root)"),
      line: z.number().int().positive().describe("Line number in the file (1-based)"),
      commentText: z.string().describe("Comment text to post"),
      threadId: z.number().int().positive().optional().describe("Thread ID to reply to (optional)")
    },
    async ({ prUrl, filePath, line, commentText, threadId }) => {
      try {
        // Always use the generic prefix for all file types
        const prefix = "🤖 Co-pilot Assisted Review: ";
        let finalCommentText = commentText;
        // Remove any existing prefix to avoid duplicates
        if (finalCommentText.startsWith(prefix)) {
          finalCommentText = finalCommentText.slice(prefix.length);
        }
        const prefixedCommentText = prefix + finalCommentText;
        // Parse PR URL
        const match = prUrl.match(/dev\.azure\.com\/(.+?)\/(.+?)\/_git\/(.+?)\/pullrequest\/(\d+)/);
        if (!match) {
          return { content: [{ type: "text", text: "Invalid Azure DevOps PR URL format." }], isError: true };
        }
        const [, , project, repoId, prId] = match;
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        if (threadId) {
          // Reply to an existing thread
          const comment = { content: prefixedCommentText, commentType: 1 };
          await gitApi.createComment(comment, repoId, Number(prId), threadId, project);
          return { content: [{ type: "text", text: THREAD_REPLY_SUCCESS(threadId, prId) }] };
        } else {
          // Create a new thread
          const thread = {
            comments: [{ content: prefixedCommentText, commentType: 1 }],
            status: "active",
            threadContext: {
              filePath: filePath.startsWith("/") ? filePath : "/" + filePath,
              rightFileStart: { line: line, offset: 1 },
              rightFileEnd: { line: line, offset: 1 }
            }
          };
          await gitApi.createThread(thread, repoId, Number(prId), project);
          return { content: [{ type: "text", text: NEW_THREAD_SUCCESS(prId, filePath, line) }] };
        }
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );


  // Tool to delete all AI review comments from a PR
  server.tool(
    "delete_all_pr_review_comments",
    "Delete all AI-generated review comments from a PR. Usage: 'Delete all PR review comments <PR_URL>'",
    {
      prUrl: z.string().url().describe("Azure DevOps Pull Request URL")
    },
    async ({ prUrl }) => {
      try {
        // Parse PR URL
        const match = prUrl.match(/dev\.azure\.com\/(.+?)\/(.+?)\/_git\/(.+?)\/pullrequest\/(\d+)/);
        if (!match) {
          return { content: [{ type: "text", text: "Invalid Azure DevOps PR URL format." }], isError: true };
        }
        const [, , project, repoId, prId] = match;
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        // Get all threads for the PR
        const threads = await gitApi.getThreads(repoId, Number(prId), project);
        
        let deletedCount = 0;
        const errors = [];

        // Iterate through threads and delete AI-generated comments
        for (const thread of threads) {
          if (thread.comments && thread.comments.length > 0) {
            for (const comment of thread.comments) {
              // Check if comment is AI-generated and not already deleted
              if (comment.content &&
                  comment.content.includes('🤖 Co-pilot Assisted Review:') &&
                  !comment.isDeleted) {
                try {
                  await gitApi.deleteComment(repoId, Number(prId), thread.id, comment.id, project);
                  deletedCount++;
                } catch (err) {
                  errors.push(`Failed to delete comment ${comment.id} in thread ${thread.id}: ${err.message}`);
                }
              }
            }
          }
        }

        const resultMessage = DELETION_SUCCESS(deletedCount, prId);
        const errorMessage = errors.length > 0 ? `\n\nErrors:\n${errors.join('\n')}` : '';

        return { content: [{ type: "text", text: resultMessage + errorMessage }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // =============================================================
  // repo_review_pr Tool - Automated PR Review
  // =============================================================
  // NOTE FOR MAINTAINERS AND USERS:
  // - Copilot (AI) will ALWAYS analyze the diff and post actionable suggestions
  //   as PR comments directly on the corresponding lines in Azure DevOps
  // - This is the DEFAULT behavior - suggestions are posted automatically
  //   without requiring additional prompts or permission
  // - To prevent posting comments, explicitly state: "Do not post comments in the PR"
  // - All suggestions MUST strictly follow the refactor guidelines:
  //   * For *.js/*.jsx files: copilot-refactor-instructions-js.md
  //   * For *.java files: copilot-refactor-instructions-java.md
  // - Each comment MUST reference the specific standard number
  // - When posting comments, DO NOT include line numbers in the comment text
  //   (the PR API handles line association)
  // =============================================================
  server.tool(
    "repo_review_pr",
    "Review PR <PR URL>. Posts suggestions as PR comments on the corresponding lines. Loads review guidelines from the file path set in CODE_REVIEW_GUIDE_FILE; if not configured, includes a notice to set it. All suggestions are posted automatically without requiring permission.",
    {
      prUrl: z.string().url().describe("Azure DevOps Pull Request URL")
    },
    async ({ prUrl }) => {
      try {
        const match = prUrl.match(/dev\.azure\.com\/(.+?)\/(.+?)\/_git\/(.+?)\/pullrequest\/(\d+)/);
        if (!match) {
          return { content: [{ type: "text", text: "Invalid Azure DevOps PR URL format." }], isError: true };
        }
        const [, , project, repoId, prId] = match;
        
        console.log(`Reviewing PR ${prId} from project ${project}, repo ${repoId}`);
        
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        const pr = await gitApi.getPullRequestById(Number(prId), project, repoId);
        if (!pr) {
          return { content: [{ type: "text", text: `Pull request ${prId} not found.` }], isError: true };
        }
        
        console.log(`PR Status: ${pr.status}, Title: ${pr.title}`);
        console.log(`Source: ${pr.sourceRefName}, Target: ${pr.targetRefName}`);
        
        // Clone repo and print diff
        const repoUrl = pr.repository.remoteUrl;
        if (!/^https?:\/\//i.test(repoUrl)) {
          throw new Error(`Unexpected repository URL: ${repoUrl}`);
        }
        const sourceBranch = assertSafeRefName(pr.sourceRefName.replace(/^refs\/heads\//, ''), 'source branch');
        const targetBranch = assertSafeRefName(pr.targetRefName.replace(/^refs\/heads\//, ''), 'target branch');
        
        // Create tempRepos directory in src folder
        const tempReposDir = path.resolve(process.cwd(), 'src', 'tempRepos');
        await fs.mkdir(tempReposDir, { recursive: true });
        await pruneStaleTempRepos(tempReposDir);
        
        // Use specific directory for this PR review
        const tempDir = path.join(tempReposDir, `prreview-${prId}-${Date.now()}`);
        
        try {
          console.log(`Cloning repo for review to ${tempDir}`);
          
          // Clone the entire repository without depth limitations
          await runGit(['clone', repoUrl, tempDir]);
          
          // Fetch all branches to ensure we have both source and target
          await runGit(['fetch', '--all'], tempDir);
          
          // Check what branches we actually have
          const { stdout: localBranches } = await runGit(['branch', '-a'], tempDir);
          console.log(`Available branches: ${localBranches}`);
          
          // Ensure we're on the target branch
          await runGit(['checkout', targetBranch], tempDir);
          
          // Get the merge base to find the actual diff
          let mergeBase;
          try {
            const { stdout: mergeBaseOutput } = await runGit(['merge-base', `origin/${targetBranch}`, `origin/${sourceBranch}`], tempDir);
            mergeBase = mergeBaseOutput.trim();
            console.log(`Merge base: ${mergeBase}`);
          } catch (mergeError) {
            console.log(`Could not find merge base, using direct diff: ${mergeError.message}`);
            mergeBase = `origin/${targetBranch}`;
          }
          
          const { stdout: changedFiles } = await runGit(['diff', '--name-status', `${mergeBase}...origin/${sourceBranch}`], tempDir);
          console.log(`Changed files for review: ${changedFiles}`);
          
          if (!changedFiles.trim()) {
            return { content: [{ type: "text", text: `No changes found between ${targetBranch} and ${sourceBranch} branches for PR ${prId}.` }] };
          }
          
          // Print the full diff for all changed files
          let fileDiffs = [];
          const fileList = [];
          for (const line of changedFiles.split('\n').filter(Boolean)) {
            const [status, ...fileParts] = line.split(/\s+/);
            const file = fileParts.join(' ');
            fileList.push(`[${status}] ${file}`);
            const { stdout: fileDiff } = await runGit(['diff', `${mergeBase}...origin/${sourceBranch}`, '--', file], tempDir);
            fileDiffs.push(`--- [${status}] ${file} ---\n${fileDiff}`);
          }

          // Load review guidelines once (not per-language)
          const refactorInstructions = await getRefactorInstructions(codeReviewGuideFile);

          const header = `**PR ${prId} Review:**\nTitle: ${pr.title}\nSource: ${sourceBranch}\nTarget: ${targetBranch}\nFiles changed: ${fileDiffs.length}\n\n**File List:**\n${fileList.join('\n')}`;
          // Always include the refactor instructions at the top for reference
          return { content: [{ type: "text", text: `### Code Review Guidelines:\n\n${refactorInstructions}\n\n${header}\n\n**Full Diffs:**\n\n${fileDiffs.join('\n\n')}` }] };

        } finally {
          // Clean up temp directory
          try {
            await fs.rm(tempDir, { recursive: true, force: true });
          } catch (cleanupError) {
            console.log(`Review cleanup error: ${cleanupError.message}`);
          }
        }
      } catch (error) {
        console.error(`PR review error: ${error.message}`);
        return { content: [{ type: "text", text: `Error reviewing PR ${prUrl}: ${error?.message || String(error)}` }], isError: true };
      }
    }
  );

  // Get PR diff by URL (by cloning and comparing branches)
  server.tool(
    "repo_pr_diff",
    "Get the diff of a pull request by providing its Azure DevOps PR URL. Usage: 'PR Diff <PR_URL>'",
    {
      prUrl: z.string().url().describe("Azure DevOps Pull Request URL")
    },
    async ({ prUrl }) => {
      try {
        const match = prUrl.match(/dev\.azure\.com\/(.+?)\/(.+?)\/_git\/(.+?)\/pullrequest\/(\d+)/);
        if (!match) {
          return { content: [{ type: "text", text: "Invalid Azure DevOps PR URL format." }], isError: true };
        }
        const [, , project, repoId, prId] = match;
        
        console.log(`Processing PR ${prId} from project ${project}, repo ${repoId}`);
        
        // Get PR details to find source/target branches and repo URL
        const connection = await getADOConnection();
        const gitApi = await connection.getGitApi();
        
        const pr = await gitApi.getPullRequestById(Number(prId), project, repoId);
        if (!pr) {
          return { content: [{ type: "text", text: `Pull request ${prId} not found.` }], isError: true };
        }
        
        console.log(`PR Status: ${pr.status}, Title: ${pr.title}`);
        console.log(`Source: ${pr.sourceRefName}, Target: ${pr.targetRefName}`);
        
        const repoUrl = pr.repository.remoteUrl;
        if (!/^https?:\/\//i.test(repoUrl)) {
          throw new Error(`Unexpected repository URL: ${repoUrl}`);
        }
        const sourceBranch = assertSafeRefName(pr.sourceRefName.replace(/^refs\/heads\//, ''), 'source branch');
        const targetBranch = assertSafeRefName(pr.targetRefName.replace(/^refs\/heads\//, ''), 'target branch');
        
        // Create tempRepos directory in src folder
        const tempReposDir = path.resolve(process.cwd(), 'src', 'tempRepos');
        await fs.mkdir(tempReposDir, { recursive: true });
        await pruneStaleTempRepos(tempReposDir);
        
        // Use specific directory for this PR
        const tempDir = path.join(tempReposDir, `prdiff-${prId}-${Date.now()}`);
        
        try {
          console.log(`Cloning repo to ${tempDir}`);
          
          // Clone the entire repository without depth limitations
          await runGit(['clone', repoUrl, tempDir]);
          
          // Fetch all branches to ensure we have both source and target
          await runGit(['fetch', '--all'], tempDir);
          
          // Check what branches we actually have
          const { stdout: localBranches } = await runGit(['branch', '-a'], tempDir);
          console.log(`Available branches: ${localBranches}`);
          
          // Ensure we're on the target branch
          await runGit(['checkout', targetBranch], tempDir);
          
          // Get the merge base to find the actual diff
          let mergeBase;
          try {
            const { stdout: mergeBaseOutput } = await runGit(['merge-base', `origin/${targetBranch}`, `origin/${sourceBranch}`], tempDir);
            mergeBase = mergeBaseOutput.trim();
            console.log(`Merge base: ${mergeBase}`);
          } catch (mergeError) {
            console.log(`Could not find merge base, using direct diff: ${mergeError.message}`);
            mergeBase = `origin/${targetBranch}`;
          }
          
          // Get list of changed files using the merge base
          const { stdout: changedFiles } = await runGit(['diff', '--name-status', `${mergeBase}...origin/${sourceBranch}`], tempDir);
          
          if (!changedFiles.trim()) {
            await fs.rm(tempDir, { recursive: true, force: true });
            return { content: [{ type: "text", text: `No changes found between ${targetBranch} and ${sourceBranch} branches for PR ${prId}.` }] };
          }
          
          const fileDiffs = [];
          const fileList = [];
          for (const line of changedFiles.split('\n').filter(Boolean)) {
            const [status, ...fileParts] = line.split(/\s+/);
            const file = fileParts.join(' ');
            fileList.push(`[${status}] ${file}`);
            
            // Get the full diff for this file using merge base
            const { stdout: fileDiff } = await runGit(['diff', `${mergeBase}...origin/${sourceBranch}`, '--', file], tempDir);
            fileDiffs.push(`--- [${status}] ${file} ---\n${fileDiff}`);
          }
          
          const header = `**PR ${prId} Diff:**\nSource: ${sourceBranch}\nTarget: ${targetBranch}\nFiles changed: ${fileDiffs.length}\n\n**File List:**\n${fileList.join('\n')}`;
          return { content: [{ type: "text", text: `${header}\n\n**Full Diffs:**\n\n${fileDiffs.join('\n\n')}` }] };
          
        } finally {
          // Clean up
          try {
            await fs.rm(tempDir, { recursive: true, force: true });
          } catch (cleanupError) {
            console.log(`Cleanup error: ${cleanupError.message}`);
          }
        }
      } catch (error) {
        console.error(`PR diff error: ${error.message}`);
        return { content: [{ type: "text", text: `Error processing PR ${prUrl}: ${error?.message || String(error)}` }], isError: true };
      }
    }
  );
}

export { getRefactorInstructions, configureReviewTool };
