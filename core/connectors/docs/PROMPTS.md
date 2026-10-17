# MCP Prompts Reference

This document provides a comprehensive reference for all available MCP (Model Context Protocol) prompts in the SC Node MCP server.

## Overview

Prompts are reusable templates that provide structured workflows for common Azure DevOps, Confluence, Messaging, Nexus IQ, and SonarQube operations. They guide users through complex tasks by generating contextual messages with best practices and recommendations.

**Total Prompts Available**: 117

Prompts are now **distributed across packages** — each standalone package ships its own prompts so they are available regardless of whether you use the unified server or a single-service install. Context auto-fill (via `~/.sc-node-mcp-context.json`) works in standalone package installs, not just the unified server.

**Categories:**
- Work Item Management (20 prompts)
- Pull Requests (11 prompts)
- Branches & Repositories (11 prompts)
- Confluence Documentation (15 prompts)
- Messaging & File Upload (3 prompts)
- Nexus IQ (1 prompt)
- Pipelines (14 prompts)
- Search (2 prompts)
- Sprint & Capacity (8 prompts)
- Test Plans (9 prompts)
- Repository Enhancements (6 prompts)
- Advanced Work Items (5 prompts)
- Core (1 prompt)
- SonarQube (8 prompts)
- Context Management (3 prompts)

## Prompt Distribution

Each package now ships its own `configureXxxPrompts()` function and registers its prompts directly. The unified server delegates to each package and adds a small set of unified-only prompts on top.

| Package | Prompts | Notes |
|---------|---------|-------|
| `@sc-node-mcp/ado` | ~87 | All ADO-related prompts (work items, PRs, branches, pipelines, sprints, test plans, etc.) |
| `@sc-node-mcp/confluence` | 15 | Confluence page and space management, search, comments, and labels prompts |
| `@sc-node-mcp/messaging` | 2 | `send-email`, `teams-send-message` |
| `@sc-node-mcp/nexus` | 1 | `nexus-vulnerability-scan` |
| `@sc-node-mcp/sonar` | 8 | SonarQube project health, quality gate, issues, hotspots, and metrics prompts |
| `@sc-node-mcp/unified` | 4 (unified-only) | `set-context`, `switch-context`, `list-contexts`, `upload-attachment-ui` — plus all the above via delegation |

Standalone installs (e.g. `@sc-node-mcp/ado` without the unified server) will receive all prompts relevant to that package. Context auto-fill (`~/.sc-node-mcp-context.json`) is read by the shared `@sc-node-mcp/core` context module and works in any package install.

## Usage

Prompts can be invoked through the MCP client (VS Code extension) by selecting them from the prompt menu. Each prompt accepts specific arguments that customize the generated workflow.

---

## Work Item Management Prompts

### 1. create-work-item
**Description**: Create a new work item (User Story, Bug, Task, Feature, or Epic)

**Arguments**:
- `project` (required): Azure DevOps project name
- `title` (required): Work item title
- `type` (optional): Work item type: User Story, Bug, Task, Feature, Epic (defaults to User Story)
- `description` (optional): Work item description

**Example Usage**:
```
Prompt: create-work-item
Arguments:
  - project: "TTOQPR"
  - title: "Add login functionality"
  - type: "User Story"
  - description: "Users should be able to log in with email"
```

**Generated Workflow**:
- Guides format based on type (user stories: As a [user]..., bugs: steps to reproduce, tasks: delivery steps)
- Acceptance criteria template
- Estimated effort planning
- Tags or labels suggestions

---

### 2. my-work
**Description**: Show all work items assigned to me

**Arguments**: None

**Generated Workflow**:
- Lists work items by ID and title
- Groups by state (Active, New, Resolved, Closed)
- Shows priority and iteration
- Displays work item type

---

### 4. sprint-planning
**Description**: Help plan the current sprint by listing backlog items

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name

**Generated Workflow**:
- Lists current backlog items
- Shows items in current iteration
- Identifies high-priority items
- Suggests capacity planning based on team velocity

---

### 5. get-multiple-work-items
**Description**: Get details of multiple work items by IDs

**Arguments**:
- `workItemIds` (required): Comma-separated work item IDs

**Generated Workflow**:
- Retrieves full details including title, state, type
- Shows assigned to and priority
- Displays iteration and area path
- Includes description and acceptance criteria
- Shows recent comments and history

---

### 6. update-multiple-work-items
**Description**: Update multiple work items in a single batch operation

**Arguments**:
- `workItemIds` (required): Comma-separated work item IDs
- `updateType` (required): Type of update (state/assignee/iteration/tags)
- `value` (required): New value to set

**Generated Workflow**:
- Applies same update to all specified work items efficiently
- Batch operation for performance

---

### 7. find-work-items-by-iteration
**Description**: Find all work items in a specific iteration

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `iteration` (required): Iteration path

**Generated Workflow**:
- Groups by work item type
- Groups by state
- Groups by assigned to
- Includes story points and effort estimates

---

### 8. run-work-item-query
**Description**: Execute a saved work item query by ID

**Arguments**:
- `project` (required): Azure DevOps project name
- `queryId` (required): Query ID or path

**Generated Workflow**:
- Returns query results with work item IDs
- Shows titles and states
- Displays assigned to
- Shows priority

---

### 9. get-query
**Description**: Get details of a saved work item query by ID or path

**Arguments**:
- `project` (required): Azure DevOps project name
- `queryId` (required): Query ID (GUID) or path

**Generated Workflow**:
- Uses `wit_get_query` to retrieve the named query
- Returns query name, path, WIQL text, and column configuration

---

### 10. get-work-item-links
**Description**: Get parent, child, and related work items linked to a work item

**Arguments**:
- `id` (required): Work item ID

**Generated Workflow**:
- Uses `wit_get_work_item_links` to expand relations on the work item
- Groups linked items into parent, child, and related buckets

---

### 11. query-by-url
**Description**: Get work items from a saved query URL or project+queryId

**Arguments**:
- `url` (optional): Full ADO query URL
- `project` (optional): Azure DevOps project name (if not passing url)
- `queryId` (optional): Query ID (if not passing url)

**Generated Workflow**:
- Uses `wit_query_by_url` to parse the query URL (or use project+queryId directly)
- Returns the resolved work items
- Dashboard links are rejected with a message pointing to `get-dashboard-work-items`

---

### 12. get-dashboard-work-items
**Description**: Get work items from query-backed widgets on a dashboard URL or project+dashboardId

**Arguments**:
- `url` (optional): Full ADO dashboard URL
- `project` (optional): Azure DevOps project name (if not passing url)
- `dashboardId` (optional): Dashboard ID (if not passing url)

**Generated Workflow**:
- Uses `wit_get_dashboard_work_items` to enumerate the dashboard's widgets
- Resolves work items for any query-backed widgets (Query Tile, Chart for a Query, etc.)
- Non-query widgets (Markdown, burndown charts, etc.) are skipped

---

## Work Item Comments

### 9. view-work-item-comments
**Description**: View all comments on a work item

**Arguments**:
- `workItemId` (required): Work item ID

**Generated Workflow**:
- Shows comment text
- Displays author
- Shows timestamp
- Highlights mentions or attachments

---

### 10. add-work-item-comment
**Description**: Add a comment to a work item

**Arguments**:
- `workItemId` (required): Work item ID
- `comment` (required): Comment text

**Generated Workflow**:
- Posts comment visible to all users with access

---

## Work Item Relationships

### 11. add-child-items
**Description**: Add child work items to a parent work item

**Arguments**:
- `parentId` (required): Parent work item ID
- `childIds` (required): Comma-separated child work item IDs

**Generated Workflow**:
- Creates parent-child relationships in work item hierarchy

---

### 12. link-related-work-items
**Description**: Create a relationship between work items

**Arguments**:
- `sourceId` (required): Source work item ID
- `targetId` (required): Target work item ID
- `linkType` (optional): Link type (Related/Dependency/Parent)

**Generated Workflow**:
- Creates specified link type between work items
- Default link type is "Related"

---

### 13. list-work-item-pull-requests
**Description**: List all pull requests linked to a specific work item

**Arguments**:
- `workItemId` (required): Work item ID
- `project` (optional): Azure DevOps project name

**Generated Workflow**:
- Uses `wit_list_work_item_pull_requests` to retrieve PR relationships
- Returns PR IDs, titles, repositories, statuses, and URLs

---

### 14. list-work-item-commits
**Description**: List all commits associated with a specific work item

**Arguments**:
- `workItemId` (required): Work item ID
- `project` (optional): Azure DevOps project name

**Generated Workflow**:
- Uses `wit_list_work_item_commits` to retrieve commit history
- Returns commit IDs, messages, authors, dates, and repository names

---

### 15. get-work-item
**Description**: Get full details of a single work item by ID

**Arguments**:
- `id` (required): Work item ID
- `project` (optional): Azure DevOps project name

**Generated Workflow**:
- Uses `wit_get_work_item` to fetch the work item
- Returns title, state, type, assignee, priority, iteration, and all fields

---

### 16. update-work-item
**Description**: Update fields of an existing work item

**Arguments**:
- `id` (required): Work item ID
- `title` (optional): New title
- `state` (optional): New state
- `assignedTo` (optional): Assignee email or display name
- `description` (optional): New description

**Generated Workflow**:
- Uses `wit_update_work_item` to apply field updates
- Returns updated work item with all fields

---

### 17. get-work-item-type
**Description**: Get the schema and field definitions for a work item type

**Arguments**:
- `project` (required): Azure DevOps project name
- `type` (required): Work item type name (e.g., Bug, User Story, Task)

**Generated Workflow**:
- Uses `wit_get_work_item_type` to retrieve type schema
- Returns field definitions, states, transitions, and allowed values

---

## Pull Request Management

### 15. create-pr
**Description**: Create a new pull request with description and reviewers

**Arguments**:
- `repository` (required): Repository name or ID
- `sourceBranch` (required): Source branch name
- `targetBranch` (required): Target branch name (e.g., main)
- `title` (required): PR title

**Generated Workflow**:
- Generates detailed description based on changes
- Suggests appropriate reviewers
- Links related work items
- Adds appropriate labels

---

### 16. my-prs
**Description**: Show all pull requests I created or need to review

**Arguments**:
- `repository` (optional): Repository name or ID

**Generated Workflow**:
- Shows PRs where I am the creator
- Shows PRs where I am a reviewer
- Groups by status (Active, Completed, Abandoned)

---

### 17. review-pr
**Description**: Review a pull request with automated code quality checks

**Arguments**:
- `prUrl` (required): Azure DevOps PR URL

**Generated Workflow**:
- Checks ES6 syntax compliance (arrow functions, template literals, destructuring)
- Identifies string literals that should be constants
- Finds unused imports and variables
- Identifies missing JSDoc comments
- Scans for security vulnerabilities
- Checks accessibility issues
- Detects code duplication
- Posts comments directly on PR with 🤖 Co-pilot Assisted Review prefix

---

### 18. analyze-pr-diff
**Description**: Analyze PR changes and suggest improvements

**Arguments**:
- `prUrl` (required): Azure DevOps PR URL

**Generated Workflow**:
- Analyzes code complexity
- Identifies potential bugs or issues
- Evaluates performance considerations
- Highlights security concerns
- Points out best practice violations
- Suggests refactoring opportunities

---

### 19. update-pull-request
**Description**: Update pull request settings including status, merge strategy, and source branch deletion

**Arguments**:  
- `prUrl` (required): Azure DevOps PR URL or PR ID
- `repository` (optional): Repository name or ID
- `mergeStrategy` (optional): Merge strategy (squash/merge/rebase)
- `deleteSourceBranch` (optional): Delete source branch after merge (yes/no)

**Generated Workflow**:
- Uses `repo_update_pull_request` to update PR settings
- Applies merge strategy and branch deletion preferences
- Returns updated PR details

---

## PR Reviewers

### 20. manage-pr-reviewers
**Description**: Add or remove reviewers on a pull request

**Arguments**:
- `prUrl` (required): Azure DevOps PR URL or PR ID
- `action` (required): Action to perform: add or remove
- `reviewers` (required): Semicolon-separated reviewer emails, employee IDs, or display names (e.g. `"Surname, Firstname; jane.doe@company.com"`) — use `;`, not `,`, since display names can themselves contain a comma
- `repository` (optional): Repository name or ID

**Generated Workflow**:
- Uses `repo_update_pull_request_reviewers` to apply the change
- Adds reviewers who can approve or comment, or removes existing reviewers

---

## PR Threads

### 21. view-pr-threads
**Description**: View all comment threads in a pull request

**Arguments**:
- `prUrl` (required): Azure DevOps PR URL

**Generated Workflow**:
- Shows thread location (file and line)
- Displays comments in each thread
- Shows thread status (active/resolved)
- Lists participants

---

### 22. create-pr-thread
**Description**: Create a new comment thread in a pull request

**Arguments**:
- `prUrl` (required): Azure DevOps PR URL
- `filePath` (required): File path to comment on
- `line` (required): Line number
- `comment` (required): Comment text

**Generated Workflow**:
- Creates new discussion thread at specified location

---

### 23. get-pull-request
**Description**: Get full details of a specific pull request

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID
- `project` (optional): Azure DevOps project name

**Generated Workflow**:
- Uses `repo_get_pull_request_by_id` to fetch the PR
- Returns title, description, source/target branches, status, reviewers, and work items

---

### 24. post-pr-comment
**Description**: Post a comment to a pull request

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID
- `comment` (required): Comment text to post
- `project` (optional): Azure DevOps project name

**Generated Workflow**:
- Uses `mcp_sc-mcp_post_pr_comment` to post a comment on the PR
- Returns the thread ID and comment ID of the posted comment

---

### 25. delete-pr-review-comments
**Description**: Delete all automated co-pilot review comments from a pull request

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID
- `project` (optional): Azure DevOps project name

**Generated Workflow**:
- Uses `mcp_sc-mcp_delete_all_pr_review_comments` to remove all 🤖 Co-pilot Assisted Review comments
- Returns count of deleted comments

---

## Branch Management

### 26. create-branch
**Description**: Create a new feature or bugfix branch

**Arguments**:
- `repository` (required): Repository name or ID
- `branchName` (required): New branch name (e.g., feature/new-feature)
- `sourceBranch` (optional): Source branch to branch from

**Generated Workflow**:
- Creates branch from specified or default branch
- Confirms naming conventions:
  - `feature/*` for new features
  - `bugfix/*` for bug fixes
  - `hotfix/*` for production fixes

---

### 27. list-all-branches
**Description**: List all branches in a repository

**Arguments**:
- `repository` (required): Repository name or ID
- `filter` (optional): Filter branches by name substring

**Generated Workflow**:
- Shows branch name
- Displays last commit date
- Shows last commit message
- Indicates behind/ahead status

---

### 28. list-my-branches
**Description**: List branches I created in a repository

**Arguments**:
- `repository` (required): Repository name or ID
- `filter` (optional): Filter branches by name substring

**Generated Workflow**:
- Shows only branches where I am the creator

---

### 29. get-branch-details
**Description**: Get detailed information about a specific branch

**Arguments**:
- `repository` (required): Repository name or ID
- `branchName` (required): Branch name

**Generated Workflow**:
- Shows latest commit information
- Displays creator and creation date
- Lists branch policies
- Shows associated pull requests

---

## Repository Management

### 30. get-repository-details
**Description**: Get detailed information about a repository

**Arguments**:
- `project` (required): Azure DevOps project name
- `repository` (required): Repository name or ID

**Generated Workflow**:
- Shows repository URL
- Displays default branch
- Shows size
- Displays last commit date
- Shows fork information (if applicable)

---

### 31. list-project-repositories
**Description**: List all repositories in a project

**Arguments**:
- `project` (required): Azure DevOps project name
- `filter` (optional): Filter repositories by name

**Generated Workflow**:
- Lists repository name and ID
- Shows size
- Displays default branch
- Shows last update

---

### 32. search-commits
**Description**: Search for commits in a repository with filters

**Arguments**:
- `repository` (required): Repository name or ID
- `searchTerm` (optional): Search term (author/message)
- `fromDate` (optional): Start date (YYYY-MM-DD)
- `toDate` (optional): End date (YYYY-MM-DD)

**Generated Workflow**:
- Shows commit ID and message
- Displays author and date
- Lists changed files
- Shows related work items

---

## Team and Project Management

### 33. list-all-projects
**Description**: List all projects in the Azure DevOps organization

**Arguments**: None

**Generated Workflow**:
- Lists project name and ID
- Shows project state
- Displays description
- Shows last update date

---

### 34. list-project-teams
**Description**: List all teams in a project

**Arguments**:
- `project` (required): Azure DevOps project name

**Generated Workflow**:
- Shows team name and ID
- Displays team description
- Shows number of members

---

### 35. list-team-iterations
**Description**: List all iterations for a team

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name

**Generated Workflow**:
- Shows iteration name and path
- Displays start and end dates
- Indicates current/future/past status

---

## Backlog Management

### 36. view-backlog
**Description**: View backlog items for a team

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `backlogLevel` (optional): Backlog level

**Generated Workflow**:
- Shows backlog items by priority
- Displays story points
- Shows state
- Lists assigned to
- Displays iteration

---

## Messaging & File Upload

### 37. upload-attachment-ui
**Description**: Open the interactive file upload panel to attach files to an Azure DevOps work item

**Arguments**:
- `project` (optional): Azure DevOps project name — pre-fills the UI
- `wiId` (optional): Work item ID to attach files to — pre-fills the UI

**Example Usage**:
```
Prompt: upload-attachment-ui
Arguments:
  - project: "TBQPR"
  - wiId: "12345"
```

**Generated Workflow**:
- Invokes `wit_upload_attachment_ui` to open the embedded VS Code panel
- UI provides drag-and-drop file picker with project/WI ID fields
- On submit, calls `wit_upload_attachment` to upload files as AttachedFile relations
- Supports multiple files in a single operation
- Works entirely within VS Code — no browser needed

---

### 38. send-email
**Description**: Send an email via Outlook with recipients, subject, and body

**Arguments**:
- `to` (required): Comma-separated recipient email addresses
- `subject` (required): Email subject line
- `body` (required): Email body content (supports HTML)
- `cc` (optional): Comma-separated CC recipients
- `bcc` (optional): Comma-separated BCC recipients

**Example Usage**:
```
Prompt: send-email
Arguments:
  - to: "john@example.com,jane@example.com"
  - subject: "Sprint Review Meeting"
  - body: "<h2>Sprint Review</h2><p>Join us tomorrow at 2 PM</p>"
  - cc: "manager@example.com"
```

**Generated Workflow**:
- Sends email via your logged-in Outlook session
- No SMTP configuration needed
- Works on macOS and Windows
- Supports HTML formatting

---

### 38. teams-send-message
**Description**: Send a direct message or group chat via Microsoft Teams using the native Teams desktop app (no webhook required)

**Arguments**:
- `to` (required): Comma-separated recipient email addresses
- `message` (required): Message body text
- `title` (optional): Optional title prepended to the message

**Example Usage**:
```
Prompt: teams-send-message
Arguments:
  - to: "john@example.com,jane@example.com"
  - message: "Sprint review is at 2 PM today in the main conference room."
  - title: "Sprint Review Reminder"
```

**Generated Workflow**:
- Opens Microsoft Teams desktop app via `msteams://` deep link
- Sends message to specified recipients
- No webhook or API setup required
- Works on macOS and Windows

---

## Confluence Integration

### 41. my-confluence-pages
**Description**: List my recent Confluence pages

**Arguments**:
- `spaceKey` (optional): Confluence space key

**Generated Workflow**:
- Lists page title
- Shows last modified date
- Displays space
- Provides page URL

**Note**: Confluence credentials are optional. If not provided, only Azure DevOps tools will be registered.

---

### 42. search-confluence
**Description**: Search Confluence pages using CQL

**Arguments**:
- `cql` (required): CQL query string
- `limit` (optional): Max results to return

**Example Usage**:
```
Prompt: search-confluence
Arguments:
  - cql: "type=page AND space.key=\"CITGOLD\" AND text~\"trade finance\""
  - limit: "10"
```

**Generated Workflow**:
- Executes CQL search via `confluence_search`
- Returns matching pages with titles, spaces, URLs, and last modified dates

---

### 43. update-confluence-page
**Description**: Update the content of a Confluence page

**Arguments**:
- `pageId` (required): Confluence page ID (numeric string)
- `body` (required): New page body in Confluence Storage Format (XHTML)
- `title` (optional): New page title — keeps existing title if omitted

**Example Usage**:
```
Prompt: update-confluence-page
Arguments:
  - pageId: "12345678"
  - title: "Updated Title"
  - body: "<p>New content here</p>"
```

**Generated Workflow**:
- Fetches current page version via `confluence_get_page_id`
- Updates page content and optional title via `confluence_update_page`
- Returns updated page URL and version number

---

### 44. get-confluence-page-id
**Description**: Look up a Confluence page ID from its URL

**Arguments**:
- `pageUrl` (required): Full Confluence page URL

**Example Usage**:
```
Prompt: get-confluence-page-id
Arguments:
  - pageUrl: "https://confluence.global.standardchartered.com/display/CC/MyPage"
```

**Generated Workflow**:
- Resolves page metadata from URL via `confluence_get_page_id`
- Returns page ID, title, space, version, and URLs

---

### 45. read-confluence-page
**Description**: Read the full content of a Confluence page from its URL

**Arguments**:
- `pageUrl` (required): Full Confluence page URL (Cloud or Server-style)

**Example Usage**:
```
Prompt: read-confluence-page
Arguments:
  - pageUrl: "https://confluence.global.standardchartered.com/display/CC/Architecture"
```

**Generated Workflow**:
- Fetches full page content via `confluence_read_page`
- Returns page title, storage-format body, version, space, and web URL
- Supports both Cloud-style (`/wiki/spaces/SPACE/pages/{id}`) and Server-style (`/display/SPACE/Title`) URLs

---

### 46. create-confluence-page
**Description**: Create a new Confluence page under a parent page

**Arguments**:
- `parentPageUrl` (required): Full URL of the parent Confluence page
- `title` (required): Title for the new page
- `body` (optional): Page body in Confluence Storage Format (XHTML) — defaults to empty page

**Example Usage**:
```
Prompt: create-confluence-page
Arguments:
  - parentPageUrl: "https://confluence.global.standardchartered.com/display/CC/Sprints"
  - title: "Sprint 42 Notes"
  - body: "<p>Sprint goals and outcomes here.</p>"
```

**Generated Workflow**:
- Resolves parent page ID from URL
- Creates new page under the parent via `confluence_create_page`
- Returns new page ID, title, and web URL

---

### 47. get-confluence-page
**Description**: Get a Confluence page by its numeric ID

**Arguments**:
- `pageId` (required): Confluence page numeric ID

**Example Usage**:
```
Prompt: get-confluence-page
Arguments:
  - pageId: "123456789"
```

**Generated Workflow**:
- Fetches page via `confluence_get_page` using the numeric ID
- Returns view, storage, and export_view body formats
- export_view captures rendered tab content not visible in storage format

---

### 48. find-confluence-page
**Description**: Find a Confluence page by space key and exact title

**Arguments**:
- `spaceKey` (required): Confluence space key (e.g., TEAM)
- `title` (required): Exact page title to search for

**Example Usage**:
```
Prompt: find-confluence-page
Arguments:
  - spaceKey: "TEAM"
  - title: "Architecture Overview"
```

**Generated Workflow**:
- Searches for the page via `confluence_find_page`
- Returns page ID, title, space, version, and web URL

---

### 49. get-confluence-page-children
**Description**: List child pages of a Confluence page by its ID

**Arguments**:
- `pageId` (required): Confluence page numeric ID
- `limit` (optional): Maximum number of children to return

**Example Usage**:
```
Prompt: get-confluence-page-children
Arguments:
  - pageId: "123456789"
  - limit: "25"
```

**Generated Workflow**:
- Fetches child pages via `confluence_get_page_children`
- Returns list of child page IDs, titles, and web URLs

---

### 50. list-confluence-spaces
**Description**: List all Confluence spaces (global spaces by default)

**Arguments**:
- `limit` (optional): Maximum number of spaces to return

**Example Usage**:
```
Prompt: list-confluence-spaces
```

**Generated Workflow**:
- Fetches spaces via `confluence_list_spaces`
- Returns space keys, names, descriptions, and types

---

### 51. get-confluence-space
**Description**: Get details of a Confluence space by its key

**Arguments**:
- `spaceKey` (required): Confluence space key (e.g., TEAM)

**Example Usage**:
```
Prompt: get-confluence-space
Arguments:
  - spaceKey: "TEAM"
```

**Generated Workflow**:
- Fetches space details via `confluence_get_space`
- Returns space key, name, description, homepage, and metadata

---

### 52. delete-confluence-page
**Description**: Delete a Confluence page by ID (title confirmation required)

**Arguments**:
- `pageId` (required): Confluence page numeric ID
- `title` (required): Exact page title — must match to confirm deletion

**Example Usage**:
```
Prompt: delete-confluence-page
Arguments:
  - pageId: "123456789"
  - title: "Old Sprint Notes"
```

**Generated Workflow**:
- Verifies title matches via `confluence_get_page` before deleting
- Deletes page via `confluence_delete_page` only if title matches exactly
- Returns confirmation of deletion

---

### 53. add-confluence-comment
**Description**: Add a page-level comment to a Confluence page

**Arguments**:
- `pageId` (required): Confluence page numeric ID
- `body` (required): Comment body in Confluence Storage Format (XHTML)

**Example Usage**:
```
Prompt: add-confluence-comment
Arguments:
  - pageId: "123456789"
  - body: "<p>Great work on this documentation!</p>"
```

**Generated Workflow**:
- Adds comment via `confluence_add_comment`
- Returns comment ID and web URL

---

### 54. get-confluence-labels
**Description**: Get all labels on a Confluence page

**Arguments**:
- `pageId` (required): Confluence page numeric ID

**Example Usage**:
```
Prompt: get-confluence-labels
Arguments:
  - pageId: "123456789"
```

**Generated Workflow**:
- Fetches labels via `confluence_get_labels`
- Returns list of label names and prefixes on the page

---

### 55. add-confluence-label
**Description**: Add a label to a Confluence page

**Arguments**:
- `pageId` (required): Confluence page numeric ID
- `label` (required): Label name to add (lowercase, no spaces)

**Example Usage**:
```
Prompt: add-confluence-label
Arguments:
  - pageId: "123456789"
  - label: "architecture"
```

**Generated Workflow**:
- Adds label via `confluence_add_label`
- Returns updated label list for the page

---

## Nexus IQ

### 47. nexus-vulnerability-scan
**Description**: Scan local npm dependencies for security vulnerabilities using Nexus IQ

**Arguments**:
- `applicationId` (required): Nexus IQ application ID (format: `ITAM__ENV__REPO_NAME`)
- `pattern` (optional): Scan pattern — `scan` (default, pipeline-aligned), `scan-fix` (scan + auto-fix), `deep-scan` (exhaustive, all deps), `deep-scan-fix` (exhaustive + auto-fix)

**Example Usage**:
```
Prompt: nexus-vulnerability-scan
Arguments:
  - applicationId: "51855__DCDAQPR__51855-ui-platform"
  - pattern: "scan"
```

**Generated Workflow**:
- Reads local `package.json` and `node_modules` (auto-installs dependencies first)
- Submits npm components to Nexus IQ for policy evaluation via `nexus_scan_vulnerabilities`
- Generates HTML, JSON, and Markdown reports in `nexus-report/`; HTML opens in browser automatically
- Returns structured vulnerability report with Critical/High/Medium/Low severity breakdown
- When `scan-fix` or `deep-scan-fix` pattern used, calls `nexus_fix_vulnerabilities` to remediate actionable vulnerabilities

---

## Pipelines

### 1. run-pipeline
**Description**: Trigger a pipeline run with optional branch, variables, and parameters

**Arguments**:
- `project` (required): Azure DevOps project name
- `pipelineId` (required): Pipeline definition ID to run
- `branchName` (optional): Branch to run the pipeline on

**Example Usage**:
```
Prompt: run-pipeline
Arguments:
  - project: "DDCPQPR"
  - pipelineId: "123"
  - branchName: "feature/my-feature"
```

**Generated Workflow**:
- Queues the pipeline run via `pipelines_run_pipeline`
- Returns the Run ID, state, and web URL to monitor progress

---

### 2. list-pipeline-runs
**Description**: List pipeline runs with optional filters for branch and status

**Arguments**:
- `project` (required): Azure DevOps project name
- `pipelineId` (optional): Pipeline ID to filter runs
- `branchName` (optional): Branch name to filter runs
- `statusFilter` (optional): Status filter — inProgress, completed, cancelling, all

**Example Usage**:
```
Prompt: list-pipeline-runs
Arguments:
  - project: "DDCPQPR"
  - pipelineId: "123"
  - statusFilter: "completed"
```

**Generated Workflow**:
- Lists runs filtered by pipeline, branch, and status
- Shows run IDs, build numbers, states, and start/finish times

---

### 3. get-pipeline-status
**Description**: Get the status of a specific build/pipeline run by build ID

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build ID to get status for

**Example Usage**:
```
Prompt: get-pipeline-status
Arguments:
  - project: "DDCPQPR"
  - buildId: "456"
```

**Generated Workflow**:
- Fetches build details via `pipelines_get_build_status`
- Returns status, result, source branch, commit, queue/start/finish times, and requestedBy

---

### 4. cancel-pipeline
**Description**: Cancel a running pipeline or build

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build/Run ID to cancel

**Example Usage**:
```
Prompt: cancel-pipeline
Arguments:
  - project: "DDCPQPR"
  - buildId: "789"
```

**Generated Workflow**:
- Sends cancellation request via `pipelines_cancel_run`
- Confirms the cancellation was requested and shows updated build status

---

### 5. list-build-definitions
**Description**: List pipeline/build definitions for a project with optional filters

**Arguments**:
- `project` (required): Azure DevOps project name
- `name` (optional): Filter definitions by name
- `repositoryId` (optional): Filter by repository ID

**Example Usage**:
```
Prompt: list-build-definitions
Arguments:
  - project: "DDCPQPR"
  - name: "CI"
```

**Generated Workflow**:
- Retrieves definitions via `pipelines_get_build_definitions`
- Shows definition IDs, names, repositories, default branches, and creation dates

---

### 6. get-builds
**Description**: Get builds with filters for branch, status, result, and definition

**Arguments**:
- `project` (required): Azure DevOps project name
- `branchName` (optional): Branch name to filter builds
- `statusFilter` (optional): Status — inProgress, completed, cancelling, notStarted, all
- `resultFilter` (optional): Result — succeeded, partiallySucceeded, failed, canceled, all

**Example Usage**:
```
Prompt: get-builds
Arguments:
  - project: "DDCPQPR"
  - branchName: "main"
  - resultFilter: "failed"
```

**Generated Workflow**:
- Fetches builds via `pipelines_get_builds`
- Shows build IDs, numbers, definition names, status, result, and time details

---

### 7. list-work-item-pipelines
**Description**: Find all pipeline runs linked to a specific work item

**Arguments**:
- `project` (required): Azure DevOps project name
- `workItemId` (required): Work item ID to find associated pipelines

**Example Usage**:
```
Prompt: list-work-item-pipelines
Arguments:
  - project: "DDCPQPR"
  - workItemId: "11681009"
```

**Generated Workflow**:
- Searches recent builds via `pipelines_list_work_item_pipelines`
- Returns all builds linked to the work item with IDs, numbers, statuses, and Azure DevOps URLs

---

### 8. get-pipeline-run
**Description**: Get the details of a specific pipeline run by run ID

**Arguments**:
- `project` (required): Azure DevOps project name
- `pipelineId` (required): Pipeline definition ID
- `runId` (required): Pipeline run ID

**Generated Workflow**:
- Uses `pipelines_get_run` to fetch run details
- Returns run state, result, created/finish times, and triggered by information

---

### 9. retry-pipeline-stage
**Description**: Retry a failed or skipped stage in a pipeline run

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build/run ID
- `stageName` (required): Name of the stage to retry
- `retryFailed` (optional): Retry only failed jobs within the stage (yes/no)

**Generated Workflow**:
- Uses `pipelines_retry_stage` to re-trigger the specified stage
- Returns the updated run status and stage information

---

### 10. list-variable-groups
**Description**: List variable groups (Library) for a project

**Arguments**:
- `project` (required): Azure DevOps project name or ID
- `groupName` (optional): Filter by variable group name

**Generated Workflow**:
- Uses `pipelines_list_variable_groups` to list the project's Library variable groups
- Optionally filters by group name

---

### 11. get-variable-group
**Description**: Get a specific variable group (Library) by ID

**Arguments**:
- `project` (required): Azure DevOps project name or ID
- `groupId` (required): Variable group ID

**Generated Workflow**:
- Uses `pipelines_get_variable_group` to retrieve the group's variables and settings

---

## Search

### 1. search-code
**Description**: Search for code text across Azure DevOps repositories

**Arguments**:
- `searchText` (required): Text or code pattern to search for
- `project` (optional): Limit search to a specific project
- `repository` (optional): Limit search to a specific repository
- `branch` (optional): Limit search to a specific branch

**Example Usage**:
```
Prompt: search-code
Arguments:
  - searchText: "getUserById"
  - project: "TBQPR"
  - repository: "my-api"
  - branch: "main"
```

**Generated Workflow**:
- Uses `search_code` to search across ADO repositories
- Returns matching file paths, repository names, and code snippets in context

---

### 2. search-work-item
**Description**: Search Azure DevOps work items by free text with optional filters

**Arguments**:
- `searchText` (required): Text to search in work item titles, descriptions, and comments
- `project` (optional): Limit search to a specific project
- `workItemType` (optional): Filter by work item type (e.g., Bug, Task)
- `state` (optional): Filter by state (e.g., Active, Closed)

**Example Usage**:
```
Prompt: search-work-item
Arguments:
  - searchText: "login bug"
  - workItemType: "Bug"
  - state: "Active"
```

**Generated Workflow**:
- Uses `search_workitem` to search work items
- Returns work item IDs, titles, types, states, and assignees

---

## Sprint & Capacity

### 1. list-project-sprints
**Description**: List all sprint iterations defined in an Azure DevOps project

**Arguments**:
- `project` (required): Azure DevOps project name

**Generated Workflow**:
- Uses `work_list_iterations` to retrieve the full iteration tree
- Returns sprint names, paths, and start/finish dates

---

### 2. create-sprints
**Description**: Create one or more new sprint iterations in a project

**Arguments**:
- `project` (required): Azure DevOps project name
- `name` (required): Sprint name (e.g., Sprint 42)
- `startDate` (optional): Start date in YYYY-MM-DD format
- `endDate` (optional): End date in YYYY-MM-DD format

**Generated Workflow**:
- Uses `work_create_iterations` to create the sprint
- Returns the new sprint path and ID

---

### 3. list-team-sprint-iterations
**Description**: List sprint iterations assigned to a specific team

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `timeframe` (optional): Filter by past, current, or future

**Generated Workflow**:
- Uses `work_list_team_iterations`
- Returns iteration names, paths, dates, and timeframe classification

---

### 4. assign-sprint-to-team
**Description**: Assign an existing project iteration to a team

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `iterationId` (required): Iteration GUID to assign

**Generated Workflow**:
- Uses `work_assign_iterations` to assign the iteration
- Confirms successful assignment

---

### 5. get-sprint-capacities
**Description**: Get per-member capacity details for a sprint iteration

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `iterationId` (required): Iteration GUID

**Generated Workflow**:
- Uses `work_get_iteration_capacities`
- Returns display name, activity, capacity per day, and days off for each member

---

### 6. get-team-capacity
**Description**: Get the total team capacity summary (activity totals, days off) for a sprint

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `iterationId` (required): Iteration GUID

**Generated Workflow**:
- Uses `work_get_team_capacity`
- Returns total capacity per activity, team days off, and working days

---

### 7. update-team-capacity
**Description**: Update a team member's daily capacity hours and activities for a sprint

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name
- `iterationId` (required): Iteration GUID
- `teamMemberId` (required): Team member identity GUID
- `activityName` (required): Activity name (e.g., Development)
- `hoursPerDay` (required): Capacity hours per day

**Generated Workflow**:
- Uses `work_update_team_capacity`
- Confirms the capacity update was applied

---

### 8. get-team-settings
**Description**: Get team settings including sprint cadence and working days

**Arguments**:
- `project` (required): Azure DevOps project name
- `team` (required): Team name

**Generated Workflow**:
- Uses `work_get_team_settings`
- Returns default iteration, area path, working days, and bug behaviour setting

---

## Test Plans

### 1. list-test-plans
**Description**: List all test plans in an Azure DevOps project

**Arguments**:
- `project` (required): Azure DevOps project name
- `filterActivePlans` (optional): Return only active test plans (yes/no)

**Generated Workflow**:
- Uses `testplan_list_test_plans`
- Returns plan IDs, names, states, iteration paths, and dates

---

### 2. create-test-plan
**Description**: Create a new test plan in an Azure DevOps project

**Arguments**:
- `project` (required): Azure DevOps project name
- `name` (required): Test plan name
- `iteration` (required): Iteration path (e.g., MyProject/Sprint 42)
- `startDate` (optional): Start date YYYY-MM-DD
- `endDate` (optional): End date YYYY-MM-DD

**Generated Workflow**:
- Uses `testplan_create_test_plan`
- Returns the new plan ID, root suite ID, and web URL

---

### 3. list-test-suites
**Description**: List all test suites in a test plan

**Arguments**:
- `project` (required): Azure DevOps project name
- `planId` (required): Test plan ID

**Generated Workflow**:
- Uses `testplan_list_test_suites`
- Returns suite hierarchy with IDs, names, types, and parent relationships

---

### 4. create-test-suite
**Description**: Create a new test suite inside a test plan

**Arguments**:
- `project` (required): Azure DevOps project name
- `planId` (required): Test plan ID
- `parentSuiteId` (required): Parent suite ID
- `name` (required): Test suite name

**Generated Workflow**:
- Uses `testplan_create_test_suite`
- Returns the new suite ID and name

---

### 5. add-test-cases-to-suite
**Description**: Add existing test case work items to a test suite

**Arguments**:
- `project` (required): Azure DevOps project name
- `planId` (required): Test plan ID
- `suiteId` (required): Test suite ID
- `testCaseIds` (required): Comma-separated test case work item IDs

**Generated Workflow**:
- Uses `testplan_add_test_cases_to_suite`
- Confirms all test cases were added

---

### 6. list-test-cases
**Description**: List all test cases in a test suite

**Arguments**:
- `project` (required): Azure DevOps project name
- `planId` (required): Test plan ID
- `suiteId` (required): Test suite ID

**Generated Workflow**:
- Uses `testplan_list_test_cases`
- Returns work item IDs, titles, priorities, assigned testers, and execution outcomes

---

### 7. create-test-case
**Description**: Create a new test case work item with optional steps

**Arguments**:
- `project` (required): Azure DevOps project name
- `title` (required): Test case title
- `priority` (optional): Priority (1=Critical, 2=High, 3=Medium, 4=Low)
- `steps` (optional): Brief description of test steps (AI will structure them)

**Generated Workflow**:
- Uses `testplan_create_test_case`
- Structures steps as action/expectedResult pairs
- Returns the new work item ID

---

### 8. update-test-case-steps
**Description**: Replace all test steps on an existing test case

**Arguments**:
- `project` (required): Azure DevOps project name
- `testCaseId` (required): Test case work item ID
- `steps` (required): New test steps as plain text (AI will structure them)

**Generated Workflow**:
- Uses `testplan_update_test_case_steps`
- Structures each step as action/expectedResult and confirms the update

---

### 9. show-build-test-results
**Description**: Show all test run results associated with a specific build

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build ID to fetch test results for

**Generated Workflow**:
- Uses `testplan_show_test_results_from_build_id`
- Returns test run names, totals (passed/failed/skipped), failed test names, and pass rate

---

## Repository Enhancements

### 1. get-file-content
**Description**: Get the content of a specific file from an Azure DevOps repository

**Arguments**:
- `repository` (required): Repository name or ID
- `filePath` (required): File path (e.g., /src/index.js)
- `branch` (optional): Branch name (defaults to default branch)

**Generated Workflow**:
- Uses `repo_get_file_content`
- Returns the full file content as text

---

### 2. list-repo-directory
**Description**: List files and folders at a given path in a repository

**Arguments**:
- `repository` (required): Repository name or ID
- `path` (optional): Directory path (e.g., /src)
- `branch` (optional): Branch name
- `recursive` (optional): List all files recursively (yes/no)

**Generated Workflow**:
- Uses `repo_list_directory`
- Returns file and folder names with their types

---

### 3. get-pr-file-changes
**Description**: Get all file changes in a pull request across all iterations

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID

**Generated Workflow**:
- Uses `repo_get_pull_request_changes`
- Returns all changed files with change type (add/edit/delete/rename) and file paths

---

### 4. vote-pull-request
**Description**: Cast a vote on a pull request

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID
- `vote` (required): approve, approveWithSuggestions, waitForAuthor, reject, reset

**Generated Workflow**:
- Uses `repo_vote_pull_request`
- Confirms the vote was recorded

---

### 5. update-pr-thread-status
**Description**: Update the status of a PR comment thread

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID
- `threadId` (required): Thread ID to update
- `status` (required): active, fixed, wontFix, closed, byDesign, pending

**Generated Workflow**:
- Uses `repo_update_pull_request_thread`
- Confirms the thread status was updated

---

### 6. reply-to-pr-comment
**Description**: Post a reply to an existing PR comment thread

**Arguments**:
- `repository` (required): Repository name or ID
- `pullRequestId` (required): Pull request ID
- `threadId` (required): Thread ID to reply to
- `content` (required): Reply text

**Generated Workflow**:
- Uses `repo_reply_to_comment`
- Confirms the reply was posted

---

## Advanced Work Items

### 1. unlink-work-item
**Description**: Remove one or more relation links from a work item

**Arguments**:
- `workItemId` (required): Work item ID
- `relationUrls` (required): Comma-separated relation URLs to remove (use `wit_get_work_item` to find them)

**Generated Workflow**:
- First uses `wit_get_work_item` to confirm current relations
- Uses `wit_work_item_unlink` to remove specified links
- Confirms each removal

---

### 2. link-work-item-to-pr
**Description**: Link a work item to a pull request as an artifact link

**Arguments**:
- `workItemId` (required): Work item ID
- `pullRequestId` (required): Pull request ID
- `repositoryId` (required): Repository name or ID
- `projectId` (required): Azure DevOps project name

**Generated Workflow**:
- Uses `wit_link_work_item_to_pull_request`
- Creates an artifact link on the work item pointing to the PR

---

### 3. update-work-item-comment
**Description**: Update the text of an existing comment on a work item

**Arguments**:
- `project` (required): Azure DevOps project name
- `workItemId` (required): Work item ID
- `commentId` (required): Comment ID to update
- `text` (required): New comment text

**Generated Workflow**:
- Uses `wit_update_work_item_comment`
- Confirms the comment was updated

---

### 4. list-work-item-revisions
**Description**: List the full revision history of a work item

**Arguments**:
- `workItemId` (required): Work item ID
- `top` (optional): Maximum number of revisions to return

**Generated Workflow**:
- Uses `wit_list_work_item_revisions`
- Returns revision number, date, changed fields, and author for each revision

---

### 5. get-work-item-attachment
**Description**: Download a work item attachment and return its content as base64

**Arguments**:
- `project` (required): Azure DevOps project name
- `attachmentId` (required): Attachment GUID (from work item relations)

**Generated Workflow**:
- Uses `wit_get_work_item_attachment`
- Returns attachment content as base64 for decoding and saving

---

## Pipeline Enhancements

### 8. get-build-logs
**Description**: Get all log lines for a build with optional text filter

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build ID
- `filter` (optional): Filter logs to lines containing this text

**Generated Workflow**:
- Uses `pipelines_get_build_log`
- Returns log output grouped by log section

---

### 9. get-build-changes
**Description**: List commits and changesets associated with a pipeline build

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build ID
- `top` (optional): Maximum number of changes to return

**Generated Workflow**:
- Uses `pipelines_get_build_changes`
- Returns commit IDs, messages, authors, timestamps, and repositories

---

### 10. list-build-artifacts
**Description**: List published artifacts from a build

**Arguments**:
- `project` (required): Azure DevOps project name
- `buildId` (required): Build ID

**Generated Workflow**:
- Uses `pipelines_list_artifacts`
- Returns artifact names, IDs, resource types, and download URLs

---

## Core

### 1. get-identity-ids
**Description**: Look up Azure DevOps identity GUIDs for one or more users by email or display name

**Arguments**:
- `identifiers` (required): Semicolon-separated email addresses or display names to look up (e.g. `"Surname, Firstname; jane@example.com"`) — use `;`, not `,`, since display names can themselves contain a comma

**Example Usage**:
```
Prompt: get-identity-ids
Arguments:
  - identifiers: "john@example.com;jane@example.com"
```

**Generated Workflow**:
- Uses `core_get_identity_ids` to resolve identities
- Returns display name, email, and identity GUID for each identifier
- GUIDs are needed for capacity (`work_update_team_capacity`), reviewer, and team member tools

---

## SonarQube

### 1. sonar-search-projects
**Description**: Search or list SonarQube projects by name or key

**Arguments**:
- `query` (optional): Filter text — project name or key substring

**Example Usage**:
```
Prompt: sonar-search-projects
Arguments:
  - query: "my-service"
```

**Generated Workflow**:
- Calls `sonar_search_projects` with optional query filter
- Returns a table of project names, keys, last analysis dates, and quality gate statuses

---

### 2. sonar-get-branches
**Description**: List all analysed branches for a SonarQube project

**Arguments**:
- `projectKey` (required): SonarQube project key

**Example Usage**:
```
Prompt: sonar-get-branches
Arguments:
  - projectKey: "my-service"
```

**Generated Workflow**:
- Calls `sonar_get_branches` for the specified project
- Returns branch names, types, quality gate statuses, and last analysis dates

---

### 3. sonar-get-quality-gate
**Description**: Check the quality gate pass/fail status for a SonarQube project branch or pull request

**Arguments**:
- `projectKey` (required): SonarQube project key
- `branch` (optional): Branch name
- `pullRequest` (optional): Pull request ID (mutually exclusive with branch)

**Example Usage**:
```
Prompt: sonar-get-quality-gate
Arguments:
  - projectKey: "my-service"
  - branch: "main"
```

**Generated Workflow**:
- Calls `sonar_get_quality_gate_status` for the project and branch/PR
- Returns overall PASSED/FAILED status and individual condition details

---

### 4. sonar-get-issues
**Description**: Search for bugs, vulnerabilities, and code smells in a SonarQube project

**Arguments**:
- `projectKey` (required): SonarQube project key
- `types` (optional): Comma-separated: BUG, VULNERABILITY, CODE_SMELL
- `severities` (optional): Comma-separated: BLOCKER, CRITICAL, MAJOR, MINOR, INFO
- `branch` (optional): Branch name

**Example Usage**:
```
Prompt: sonar-get-issues
Arguments:
  - projectKey: "my-service"
  - types: "BUG,VULNERABILITY"
  - severities: "BLOCKER,CRITICAL"
```

**Generated Workflow**:
- Calls `sonar_get_issues` with filters for type and severity
- Returns issues grouped by type and severity with file paths and remediation effort

---

### 5. sonar-get-hotspots
**Description**: List security hotspots in a SonarQube project that require manual review

**Arguments**:
- `projectKey` (required): SonarQube project key
- `branch` (optional): Branch name
- `status` (optional): TO_REVIEW or REVIEWED (defaults to TO_REVIEW)

**Example Usage**:
```
Prompt: sonar-get-hotspots
Arguments:
  - projectKey: "my-service"
  - status: "TO_REVIEW"
```

**Generated Workflow**:
- Calls `sonar_get_hotspots` for the project
- Returns hotspots grouped by security category with vulnerability probability and file locations

---

### 6. sonar-get-measures
**Description**: Retrieve code quality metrics (coverage, bugs, vulnerabilities, code smells, tech debt) for a SonarQube project

**Arguments**:
- `component` (required): SonarQube project key
- `metricKeys` (optional): Comma-separated metric keys (defaults to standard set)
- `branch` (optional): Branch name

**Example Usage**:
```
Prompt: sonar-get-measures
Arguments:
  - component: "my-service"
  - branch: "main"
```

**Generated Workflow**:
- Calls `sonar_get_measures` to fetch quality metrics
- Returns a metrics dashboard: coverage, duplication, lines of code, issue counts, tech debt, and A–E ratings

---

### 7. sonar-project-health
**Description**: Get a full code quality health report for a SonarQube project: quality gate, key metrics, and open issues

**Arguments**:
- `projectKey` (required): SonarQube project key
- `branch` (optional): Branch name

**Example Usage**:
```
Prompt: sonar-project-health
Arguments:
  - projectKey: "my-service"
  - branch: "main"
```

**Generated Workflow**:
- Calls `sonar_get_quality_gate_status` for overall pass/fail
- Calls `sonar_get_measures` for coverage, duplication, bug count, tech debt
- Calls `sonar_get_issues` filtered to BLOCKER/CRITICAL severity
- Returns a health dashboard with all three data sets combined

---

### 8. sonar-security-review
**Description**: Get a security-focused review of a SonarQube project: vulnerabilities, security hotspots, and security rating

**Arguments**:
- `projectKey` (required): SonarQube project key
- `branch` (optional): Branch name

**Example Usage**:
```
Prompt: sonar-security-review
Arguments:
  - projectKey: "my-service"
  - branch: "main"
```

**Generated Workflow**:
- Calls `sonar_get_measures` for security rating and hotspot coverage
- Calls `sonar_get_issues` filtered to VULNERABILITY type
- Calls `sonar_get_hotspots` for unreviewed security hotspots
- Returns a security review with vulnerabilities grouped by severity and hotspots by category

---

## Context Management

### 1. set-context
**Description**: Guided workflow to set up the active workspace context (project, team, default repo, Nexus app ID, Confluence space key)

**Arguments**:
- `name` (required): Context name (e.g., my-service)
- `project` (optional): Azure DevOps project name
- `team` (optional): Team name
- `defaultRepo` (optional): Default repository name
- `nexusAppId` (optional): Nexus IQ application ID for the default repo (format: `ITAM__ENV__REPO_NAME`)
- `confluenceSpaceKey` (optional): Default Confluence space key (e.g., PLAT)

**Example Usage**:
```
Prompt: set-context
Arguments:
  - name: "my-service"
  - project: "TBQPR"
  - team: "DCS-Abarth (SQUAD)"
  - confluenceSpaceKey: "PLAT"
```

**Generated Workflow**:
- Uses `ctx_set` to create or update the named context
- Sets the new context as active
- Once set, other tools auto-fill project/team/repo arguments from the active context
- Use `ctx_get` to verify the active context at any time
- Use `ctx_switch` to swap between saved contexts

---

### 2. switch-context
**Description**: Switch the active workspace context to a previously saved context by name

**Arguments**:
- `name` (required): Context name to switch to (use `list-contexts` to see available names)

**Example Usage**:
```
Prompt: switch-context
Arguments:
  - name: "payments-service"
```

**Generated Workflow**:
- Calls `ctx_switch` with the specified context name
- All subsequent tool calls auto-fill arguments from the switched context
- Use `ctx_get` to confirm the switch was successful

---

### 3. list-contexts
**Description**: List all saved workspace contexts with their project, team, and workspace path details

**Arguments**: None

**Example Usage**:
```
Prompt: list-contexts
```

**Generated Workflow**:
- Calls `ctx_list` to show all stored contexts
- The currently active context is marked with ✓
- Shows project, team, and workspace paths for each context
- Use `switch-context` (or `ctx_switch` directly) to change the active context

---

## Best Practices

1. **Use Specific Arguments**: Always provide required arguments for accurate results
2. **Naming Conventions**: Follow branch naming conventions (feature/*, bugfix/*, hotfix/*)
3. **PR Reviews**: Use automated review prompts to maintain code quality
4. **Work Item Linking**: Link PRs to work items for traceability
5. **Batch Operations**: Use batch update prompts for efficiency when updating multiple items

## Related Documentation

- [Tools Reference](./TOOLS_REFERENCE.md) - Complete list of available MCP tools
- [Work Items Guide](guide/WORKITEMS_TOOLS_GUIDE.md) - Detailed work item tool usage
- [Repositories Guide](guide/REPOSITORIES_TOOLS_GUIDE.md) - Repository and PR management
- [PR Review Guide](./PR_REVIEW.md) - Automated PR review system

---

**Last Updated**: June 8, 2026
