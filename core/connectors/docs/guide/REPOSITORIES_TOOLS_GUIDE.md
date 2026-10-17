# Repository and Pull Request Tools Guide

## Overview
This document covers all 20 repository/PR tools and 4 PR review tools available in `@sc-node-mcp/ado` and `@sc-node-mcp/unified`.

## Example Environment
- **Organization**: sc-ado
- **Project**: YOUR_PROJECT
- **Repository**: your-repository-name
- **Repository URL**: https://dev.azure.com/sc-ado/YOUR_PROJECT/_git/your-repository-name
- **Test User**: Current authenticated user

> Replace `YOUR_PROJECT` and `your-repository-name` with values from your Azure DevOps environment.

---

## 📦 REPOSITORY OPERATIONS

### 1. repo_list_repos_by_project
**Test Query**: `List all repositories in project YOUR_PROJECT with -ui`
**Expected**: Returns list of all repositories with names, IDs, URLs
**Alternative**: `Show me repositories in YOUR_PROJECT with filter containing 'cib'`

**Parameters**:
```json
{
  "project": "YOUR_PROJECT",
  "repoNameFilter": "-ui",
  "skip": 0,
  "top": 10
}
```
**Response**:

```
Here are all repositories in project YOUR_PROJECT with "-ui" in their names:

example-app-ui
example-app-ui-module
example-app-ui-components
example-app-ui-forms
example-app-ui-landing
```

---

### 2. repo_get_repo_by_name_or_id
**Test Query**: `Get repository details for your-repository-name in project YOUR_PROJECT`
**Expected**: Full repository details including default branch, size, URLs

**Parameters**:
```json
{
  "project": "YOUR_PROJECT",
  "repositoryNameOrId": "your-repository-name"
}
```

**Response**:

```
Here are the repository details for example-app-repository in project YOUR_PROJECT:

Repository Name: example-app-repository
Repository ID: {repo-guid}
Project: YOUR_PROJECT
Default Branch: refs/heads/main
Size: 3,521,161 bytes
Web URL: https://dev.azure.com/sc-ado/YOUR_PROJECT/_git/example-app-repository
Remote URL: https://sc-ado@dev.azure.com/sc-ado/YOUR_PROJECT/_git/example-app-repository
SSH URL: git@ssh.dev.azure.com:v3/sc-ado/YOUR_PROJECT/example-app-repository
Created: 2025-01-19T22:30:03.297Z
Is Disabled: false
Is In Maintenance: false
Let me know if you need more details or want to perform another operation on this repository.
```

---

## 🌿 BRANCH OPERATIONS

### 3. repo_list_branches_by_repo
**Test Query**: `List all branches in repository your-repository-name`
**Expected**: Returns list of branches with names, commits, creators
**Alternative**: `Show branches containing 'feature' in your-repository-name`

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "filterContains": "feature",
  "top": 20
}
```

**Response**:

```
Here are all the branches in the repository your-repository-name (project: YOUR_PROJECT):

main
develop
25.11
bigfix/8168843
bugfix/10462520
bugfix/10759296
bugfix/11206979
bugfix/11206979-v1
bugfix/11210961
bugfix/11220930
bugfix/11239432
bugfix/11562336
bugfix/12345
bugfix/12345-v1
bugfix/9149725
catalyst/feature/25.2-staging
demo/agent1
feature/10736534
feature/10736534-v1
feature/10736534-v2
feature/11180198
feature/11239432
feature/12-grid-poc
feature/6866776-1
feature/7068744
feature/7090685-1
feature/7090685-2
feature/7090685-3
feature/7090685-5
feature/7235662
feature/7235662-1
feature/7238673
feature/7257404-1
feature/7654837-api
feature/7654939
feature/7654939-v1
feature/7722360-2
feature/7722360-workspace
feature/7966426-A
feature/8254060
feature/8370450-HMenu
feature/8797089
feature/8797089-V1
feature/8797089-v1
feature/8948658
feature/8951058
feature/8951058-trasanactionDetails
feature/8951058-v1
feature/9076219
feature/9076219-test
feature/9076219-v1
feature/9076641
feature/9374862
feature/9402997
feature/9402997-v1
feature/9822892
feature/ADO-6866776
feature/road-show-mock
nexus-scan
release/25.10
release/25.10.1
release/25.11
release/25.12
release/25.3
release/26.1
release/26.2
release/CatalystSIT
release/CatalystSIT.0
release/devops
release/devops1
release/devops2
release/devops3
release/devops4
release/mvp1
release/postCatalyst
If you need details for a specific branch, let me know!
```

---

### 4. repo_list_my_branches_by_repo
**Test Query**: `Show my branches in repository your-repository-name`
**Expected**: Returns only branches created by current user

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "filterContains": "my",
  "top": 10
}
```

**Response**:

```
Here are your branches in the your-repository-name repository:

main
develop
feature/test-mcp-branch
bugfix/12345
bugfix/12345-v1
bugfix/11562336
bugfix/11210961
bugfix/11206979
bugfix/11206979-v1
bugfix/11220930
bugfix/10759296
bugfix/10462520
bigfix/8168843
feature/10736534
```

---

### 5. repo_get_branch_by_name
**Test Query**: `Get details for branch main in repository your-repository-name`
**Expected**: Branch details including latest commit, creator, date

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "branchName": "main"
}
```

**Response**:

```
The main branch in example-app-repository exists. Its latest commit (ID: abc123def456789012345678901234567890abcd) was made by Developer Name on 2026-01-27 with the message "Merged PR 123456: code sync". The branch is up to date and is the base version.
```
---

### 6. repo_create_branch ⚠️ WRITE OPERATION
**Test Query**: `Create branch feature/add-validation from main in your-repository-name`
**Expected**: New branch created successfully with confirmation

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "branchName": "feature/test-mcp-branch",
  "sourceBranchName": "main"
}
```

**⚠️ WARNING**: This creates a real branch. Clean up after testing.

**Response**:

```
The branch feature/add-validation has been created from main in the your-repository-name repository. Let me know if you need to perform any further actions with this branch.
```

---

## 🔀 PULL REQUEST OPERATIONS

### 7. repo_list_pull_requests_by_repo_or_project
**Test Query**: `List all active pull requests in repository your-repository-name`
**Expected**: Returns active PRs with titles, authors, statuses
**Alternative**: `Show PRs in project YOUR_PROJECT where I am reviewer`

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "status": "active",
  "i_am_reviewer": true,
  "top": 10
}
```

**Response**:

```
Here are all active pull requests in the repository example-app-repository (project: YOUR_PROJECT):

PR #2383412
Title: feat: #11239432 - Example feature implementation
Author: U, Shiyamkumar
Source: feature/11239432 → Target: release/26.2
Created: 2026-01-30
Link: https://dev.azure.com/sc-ado/YOUR_PROJECT/_git/example-app-repository/pullrequest/2383412

PR #2182478
Title: DO_NOT_MERGE__ROAD_SHOW__This is for AI-MCP Code Review
Author: U, Shiyamkumar
Source: feature/road-show-mock → Target: develop
Created: 2025-11-11
Link: https://dev.azure.com/sc-ado/YOUR_PROJECT/_git/example-app-repository/pullrequest/2182478

PR #2157600
Title: DO_NOT_MERGE__ROAD_SHOW__This is for MCP Code Review
Author: U, Shiyamkumar
Source: feature/9076219-test → Target: develop
Created: 2025-11-05
Link: https://dev.azure.com/sc-ado/YOUR_PROJECT/_git/example-app-repository/pullrequest/2157600

Let me know if you need details or actions on any of these pull requests.
```

**Available Filters**:
- `status`: "active", "abandoned", "completed", "all"
- `created_by_me`: true/false
- `i_am_reviewer`: true/false
- `sourceRefName`: "refs/heads/feature"
- `targetRefName`: "refs/heads/main"

---

### 8. repo_get_pull_request_by_id
**Test Query**: `Get pull request 2383412 from repository your-repository-name`
**Expected**: Full PR details including title, description, reviewers, status
**Alternative**: `Get PR 2383412 with linked work items`

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "includeWorkItemRefs": true
}
```

**Response**:

```
Here are the details for pull request 2383412 from repository your-repository-name in project YOUR_PROJECT:

Title: feat: #11239432 - Example feature implementation

PR ID: 2383412

Status: Active

Author: U, Shiyamkumar (developer@example.com)

Source branch: feature/11239432

Target branch: release/26.2

Created: 2026-01-30T05:46:05Z

Reviewers: [YOUR_PROJECT]\ADO-Engineer-review (required)

Linked work items: #11239432

Description:
feat: #11239432 - Example feature implementation
<img src="https://dev.azure.com/sc-ado/YOUR_PROJECT/_apis/git/repositories/{repo-guid}/pullRequests/2383412/attachments/{attachment-id}.png" alt="Attachment">

Web URL: View PR

Let me know if you need more details or actions on this pull request.
```


---

### 9. repo_create_pull_request ⚠️ WRITE OPERATION
**Test Query**: `Create PR from feature/test-mcp-branch to develop in your-repository-name with title 'New Feature'`
**Expected**: New PR created with specified parameters

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "sourceRefName": "feature/new-feature",
  "targetRefName": "main",
  "title": "New Feature Implementation",
  "description": "This PR implements the new feature requested in #123",
  "isDraft": false,
  "labels": ["enhancement"],
  "workItems": [123, 456]
}
```

**Response**:

```
The pull request from feature/test-mcp-branch to develop in the example-app-repository repository (project YOUR_PROJECT) has been created with the title "New Feature".

You can view or manage the PR here:
https://dev.azure.com/sc-ado/YOUR_PROJECT/_git/example-app-repository/pullrequest/2386907
```

**⚠️ WARNING**: This creates a real PR. Use with caution.

---

### 10. repo_update_pull_request ⚠️ WRITE OPERATION
**Test Query**: `Update PR 2182478 in repository your-repository-name to change title to 'UPDATED: Test PR for MCP'`
**Expected**: PR updated with new properties
**Alternative**: `Complete PR 123 with squash merge and delete source branch`

**Parameters for Title Update**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "title": "Updated Title",
  "description": "Updated description"
}
```

**Parameters for Completion**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "status": "completed",
  "autoComplete": true,
  "deleteSourceBranch": true,
  "mergeStrategy": "squash"
}
```

**Available Options**:
- `status`: "active", "abandoned", "completed"
- `mergeStrategy`: "noFastForward", "squash", "rebase", "rebaseMerge"
- `autoComplete`: true/false
- `deleteSourceBranch`: true/false
- `transitionWorkItems`: true/false

**Response**:

```
The title of PR 2182478 in repository your-repository-name has been updated to "UPDATED: Test PR for MCP". If you need further changes or want to review the PR, let me know!
```
---

### 11. repo_update_pull_request_reviewers ⚠️ WRITE OPERATION
**Test Query**: `Add reviewer 1540326 to PR 2386907 in repo your-repository-name`
**Expected**: Reviewers added to PR successfully
**Alternative**: `Remove reviewer user3 from PR 123`

**Parameters for Adding**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "reviewers": ["user1-id", "user2-id"],
  "action": "add"
}
```

**Parameters for Removing**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "reviewers": ["user3-id"],
  "action": "remove"
}
```

**Response**:

```
Reviewer 1540326 (R3, Saravanan) has been successfully added to PR 2386907 in the repo your-repository-name. Let me know if you need to add more reviewers or perform other PR actions.
```

---

## 💬 COMMENT AND THREAD OPERATIONS

### 12. repo_list_pull_request_threads
**Test Query**: `List all comment threads for PR 2182478 in your-repository-name`
**Expected**: Returns all threads with comments, status, context

**Parameters**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "project": "YOUR_PROJECT",
  "top": 50
}
```
**Response**:

```
Here are all comment threads for PR 2182478 in the your-repository-name repository (project: YOUR_PROJECT):

Thread 15519583

Author: U, Shiyamkumar
Comment: "Policy status has been updated"
Date: 2025-11-11
Type: PolicyStatusUpdate
Status: Active
Thread 15519742 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/Landing.jsx, line 10
Comment: (deleted)
Status: Deleted
Thread 15519743 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/landing.services.js, line 7
Comment: (deleted)
Status: Deleted
Thread 15519744 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/utils.js, line 7
Comment: (deleted)
Status: Deleted
Thread 15519745 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/constants.js, line 20
Comment: (deleted)
Status: Deleted
Thread 15519746 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/landing.services.js, line 3
Comment: (deleted)
Status: Deleted
Thread 15519747 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/utils.js, line 1
Comment: (deleted)
Status: Deleted
Thread 15519748 (deleted)

Author: U, Shiyamkumar
File: /src/features/trade/landing/landing.styles.jsx, line 5
Comment: (deleted)
Status: Deleted
Thread 15523692

Author: R3, Saravanan
Comment: "🚨 Action Required: Commit Message Format 🚨 ..."
Date: 2025-11-12
Status: Active
Thread 15523693

Author: Microsoft.VisualStudio.Services.TFS
Comment: "R3, Saravanan joined as a reviewer"
Date: 2025-11-12
Type: ReviewersUpdate
Status: Active
Thread 15523694

Author: R3, Saravanan
Comment: "R3, Saravanan voted -5"
Date: 2025-11-12
Type: VoteUpdate
Status: Active
Let me know if you need details for any specific thread or comment.

```
---

### 13. repo_create_pull_request_thread ⚠️ WRITE OPERATION
**Test Query**: `Add comment 'Testing fixed MCP tool' to PR 2182478 in repo your-repository-name`
**Expected**: New comment thread created at specified location
**Alternative**: `Add general comment 'LGTM' to PR 123`

**Parameters for Line Comment**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "content": "Please review this change carefully",
  "filePath": "/src/index.js",
  "rightFileStartLine": 42,
  "rightFileEndLine": 42,
  "status": "active"
}
```

**Parameters for General Comment**:
```json
{
  "repositoryId": "your-repository-name",
  "pullRequestId": 123,
  "content": "LGTM! Great work on this PR.",
  "status": "active"
}
```

**Available Statuses**: "active", "fixed", "wontFix", "closed", "byDesign", "pending"

**Response**:

```
The comment "Testing fixed MCP tool" has been successfully added to PR 2182478 in the your-repository-name repository. Let me know if you need to add more comments or perform other actions.
```
---

## 🔍 COMMIT OPERATIONS

### 14. repo_search_commits
**Test Query**: `Search commits in your-repository-name for text 'bug fix' authored by john.doe@example.com`
**Expected**: Returns matching commits with details
**Alternative**: `List last 10 commits on main branch`

**Parameters for Search**:
```json
{
  "project": "YOUR_PROJECT",
  "repository": "your-repository-name",
  "searchText": "bug fix",
  "authorEmail": "john.doe@example.com",
  "top": 20
}
```

**Parameters for Branch History**:
```json
{
  "project": "YOUR_PROJECT",
  "repository": "your-repository-name",
  "version": "main",
  "versionType": "branch",
  "top": 10,
  "includeWorkItems": true
}
```

**Available Filters**:
- `searchText`: Text in commit message
- `author`: Author name
- `authorEmail`: Author email
- `committer`: Committer name
- `committerEmail`: Committer email
- `fromDate`: Start date (ISO 8601)
- `toDate`: End date (ISO 8601)
- `fromCommit`: Start commit ID
- `toCommit`: End commit ID
- `commitIds`: Array of specific commit IDs
- `version`: Branch/tag name or commit ID
- `versionType`: "branch", "tag", or "commit"
- `includeWorkItems`: Include linked work items
- `includeLinks`: Include links

**Response**:

```
Here are the commits in the YOUR_PROJECT project's example-app-repository repository authored by author@example.com containing the text ' fix':

Merge commit on 2025-12-08:

Message: "Merge pull request 2183078 from main into develop"
View Commit
Merge commit on 2025-11-24:

Message: "Merge pull request 2183078 from main into develop"
View Commit
Let me know if you need more details or want to see other commit authors.
```

---


## 🔗 COMMON USE CASES

### Use Case 1: Create and Review a Pull Request
```
1. Create branch: "Create branch feature/new-api from main in your-repository-name"
2. Create PR: "Create PR from feature/new-api to main in your-repository-name with title 'New API Implementation'"
3. Add reviewers: "Add reviewers alice and bob to PR 123"
4. Add comment: "Add comment 'Please review authentication logic' on line 50 of api/auth.js in PR 123"
5. Get PR details: "Show me PR 123 with linked work items"
```

### Use Case 2: Search and Analyze Commits
```
1. Search: "Search commits in your-repository-name by author 'John Doe' from 2026-01-01 to 2026-01-31"
2. Find PRs: "Find PRs containing commit abc123 in your-repository-name"
3. Get commit details: "Get commit abc123 in your-repository-name with linked work items"
```

### Use Case 3: Manage PR Comments
```
1. List threads: "List all comment threads for PR 123 in your-repository-name"
2. Reply: "Reply to thread 5 in PR 123 with 'Fixed in latest commit'"
3. Resolve: "Resolve thread 5 in PR 123"
4. List active: "Show active threads in PR 123"
```

### Use Case 4: Complete a Pull Request
```
1. Review status: "Get PR 123 from your-repository-name"
2. Add final comment: "Add comment 'All checks passed, ready to merge' to PR 123"
3. Complete: "Complete PR 123 with squash merge and delete source branch"
```

---

## 🚨 IMPORTANT NOTES

### API Differences from Microsoft's Implementation
1. **Parameter Names**: Our implementation uses camelCase (e.g., `repositoryId`) while Microsoft uses various conventions
2. **Error Handling**: All tools include consistent error handling with `isError: true` flag
3. **Optional Parameters**: Many parameters are optional for better usability
4. **Branch Names**: Can be provided with or without `refs/heads/` prefix (auto-detected)

### Testing Best Practices
1. **Start with Read Operations**: Test list/get operations first before write operations
2. **Use Test Repository**: Create a dedicated test repository for trying write operations
3. **Clean Up**: Delete test branches and PRs after testing
4. **Check Permissions**: Ensure your PAT has appropriate permissions for all operations
5. **Rate Limiting**: Azure DevOps has rate limits; space out tests if needed

### Required Permissions
Your Personal Access Token (PAT) must have:
- **Code (Read)**: For listing repos, branches, PRs, commits
- **Code (Write)**: For creating branches, PRs, comments
- **Code (Status)**: For updating PR status
- **Code (Contribute)**: For completing PRs and merging

---

## 🐛 TROUBLESHOOTING

### Common Issues

**Issue**: "Repository not found"
- **Solution**: Verify repository name/ID is correct and you have access

**Issue**: "Pull request not found"
- **Solution**: Check PR ID is valid and belongs to the specified repository

**Issue**: "Branch already exists"
- **Solution**: Use a different branch name or delete the existing branch first

**Issue**: "Insufficient permissions"
- **Solution**: Verify your PAT has the required Code permissions

**Issue**: "Cannot complete PR - policies not satisfied"
- **Solution**: Ensure all required reviewers have approved and build policies pass

**Issue**: "Thread not found"
- **Solution**: Verify thread ID exists and belongs to the specified PR

---

## 📝 NOTES FOR DEVELOPERS

### Tool Implementation Details
1. **Single Quotes**: All string literals use single quotes (project convention)
2. **Arrow Functions**: All handlers use arrow functions
3. **Error Handling**: Uses `error?.message || String(error)` pattern
4. **Template Literals**: Preferred over string concatenation
5. **Destructuring**: Used for function parameters

### Adding New Tools
1. Add tool name to `REPO_TOOLS` mapping object
2. Implement handler with proper Zod schema
3. Follow ES6+ conventions (ESM modules, async/await, Zod schemas — see existing tools in `packages/ado/src/tools/` for patterns)
4. Add JSDoc comments for exported functions
5. Update this guide with test cases
6. Update TOOLS_REFERENCE.md

---

