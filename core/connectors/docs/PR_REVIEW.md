# PR Review Feature Guide

## Overview

The MCP server provides fully automated, AI-driven PR review capabilities for Azure DevOps. All review analysis and actionable comments are performed by Copilot (the AI), strictly following your team's coding standards. This system streamlines code review, reduces manual effort, and enforces consistent standards across your codebase.


## Key Features

- **Automated Analysis:** The server analyzes Azure DevOps pull request diffs, identifies code quality issues, and enforces refactor guidelines.
- **Actionable Comments:** It posts direct, actionable comments on PRs, helping teams improve code quality and maintain standards.
- **String Literal Checks:** Scans for string literals in assignments and suggests moving them to constants files for maintainability.
- **Automated Checks:** Runs additional automated checks to catch common mistakes and ensure best practices.
- **Customizable Guidelines:** Provide your team's coding standards in a single guidelines file; the tool loads it automatically.
- **Integration:** All review actions are performed via the MCP protocol, allowing seamless integration with editors and automation tools.
- **No Backend Review Logic:** All review analysis and comment generation is performed by Copilot (the AI). The server only fetches diffs and posts comments.
- **Threaded Comments:** Supports posting new comment threads and replying to existing threads in PRs.
- **Opt-Out Option:** By default, all suggestions are posted as PR comments. To only show review feedback in chat (not as PR comments), explicitly request this in your prompt.

## Customizing PR Review Standards

Create a `CODE_REVIEW_GUIDE.md` file anywhere on your machine and set the `CODE_REVIEW_GUIDE_FILE` environment variable (or `codeReviewGuideFile` in `config.json`) to its full path.

This single file applies to **all file types** reviewed in the PR. Include any coding standards, style rules, and best practices your team wants enforced.

**Example:**
```
CODE_REVIEW_GUIDE_FILE=/path/to/CODE_REVIEW_GUIDE.md
```

The tool will load `/path/to/CODE_REVIEW_GUIDE.md` for every PR review.

If no file path is configured, the review still runs but includes a notice reminding you to configure `CODE_REVIEW_GUIDE_FILE`.

## Available Review Tools

### 1. Automated PR Review
**Tool:** `repo_review_pr`  
**Usage:** `Review PR https://dev.azure.com/org/proj/_git/repo/pullrequest/123`

This tool performs a comprehensive analysis of a pull request and automatically posts comments on specific lines where improvements are needed. Review guidelines are loaded from the file path set in `CODE_REVIEW_GUIDE_FILE` when configured. All file types in the PR are reviewed.

### 2. Get PR Diff
**Tool:** `repo_pr_diff`  
**Usage:** `PR Diff https://dev.azure.com/org/proj/_git/repo/pullrequest/123`

Retrieves the complete diff of a pull request for manual inspection or integration with other tools.

### 3. Post PR Comments (New Thread or Reply)
**Tool:** `post_pr_comment`  
**Usage:** `Post PR Comment <PR_URL> <filePath> <line> <commentText> [threadId]`

Posts a comment on a specific line in a PR. If `threadId` is omitted, creates a new thread; if provided, replies to an existing thread. All AI-generated review comments use this tool.

### 4. Delete All PR Review Comments
**Tool:** `delete_all_pr_review_comments`
**Usage:** "Delete all PR review comments https://dev.azure.com/org/proj/_git/repo/pullrequest/123"

This tool removes all AI-generated review comments from a pull request. It identifies comments by the "🤖 Co-pilot Assisted Review:" prefix and deletes them from all threads in the PR. This is useful when:
- You want to re-run an automated review with updated guidelines
- Previous review comments are no longer relevant
- You need to clean up before a fresh review cycle

**Note:** Only AI-generated comments (those with the Co-pilot prefix) are deleted. Manual comments from human reviewers remain untouched.

## Workflow Example

1. **Start Review:** Use `repo_review_pr` to automatically analyze and comment on a PR
2. **Get Details:** Use `repo_pr_diff` to examine specific changes in detail
3. **Add Custom Comments:** Use `post_pr_comment` to add additional feedback
4. **Clean Up (Optional):** Use `delete_all_pr_review_comments` to remove all AI comments if you need to re-run the review
5. **Follow Up:** Use standard PR management tools to resolve threads and complete the review

## Best Practices

1. **Configure Guidelines:** Create a `CODE_REVIEW_GUIDE.md` file with your team's standards and set the `CODE_REVIEW_GUIDE_FILE` environment variable to its full path. This single file applies to all file types reviewed in the PR — see [Customizing PR Review Standards](#customizing-pr-review-standards) above.
2. **Review Automation:** Use automated reviews as a first pass, followed by human review for complex logic
3. **Consistent Standards:** Ensure all team members understand the guidelines to maintain consistency
4. **Iterative Improvement:** Regularly update guidelines based on common issues found in reviews
5. **Language-Specific Rules:** Ensure rules are appropriate for the target language and only apply to files with matching extensions

## Integration with Azure DevOps

The PR review tools are fully integrated with Azure DevOps:
- All review comments are posted directly to the PR, associated with the correct file and line.
- Supports both new comment threads and replies to existing threads.
- All actions are logged and visible in the PR timeline.
- Follows Azure DevOps conventions for thread management and review workflows.
- No backend review logic: all analysis and comment generation is performed by Copilot (the AI).
