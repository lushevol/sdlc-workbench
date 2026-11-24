# Work Item Tools Guide

## Overview
This document covers all 26 Azure DevOps work item tools available in `@sc-node-mcp/ado` and `@sc-node-mcp/unified`.

---

## Example Environment
- **Project**: YOUR_PROJECT
- **Team**: YOUR_TEAM
- **Example Work Items**: #12345, #12346, #12347

> Replace `YOUR_PROJECT`, `YOUR_TEAM`, and work item IDs with values from your Azure DevOps environment.

---

## ✅ READ OPERATIONS (Safe to Test)

### 1. wit_list_projects
**Test Query**: `List all Azure DevOps projects`
**Expected**: Returns list of all projects including YOUR_PROJECT
**Response**: 

```
Here are all Azure DevOps projects in your organization:

AMEQPR
GDCWQPR
CCIBQPR
Platform SRE
TECHSIMQPR
FMREG
PROPERTYQPR
BANKINGQPR
ADO Adoption
ReleaseManagement
ADO Support
DevFactory Support
YOUR_PROJECT_DO_NOT_USE
CCQPR
TechObsGovForum
MRC
MAG
YOUR_PROJECT
CATALYSTQPR
TRADEQPR_DO_NOT_USE
CABMQPR
Task Management
```
---

### 2. wit_get_work_item
**Test Query**: `Show me the details about work item #12345`
**Expected**: Full details of work item including fields, relations, comments
**Alternative Test**: `Get work item 12346`
**Response**: 
```
Here are the details for work item #12345:

Title: Tech - Standard width for Dashboard widget Page
Type: Story
Project: YOUR_PROJECT
State: In Test
Assigned To: Alice Johnson
Created By: Ethan Kim (2026-01-05)
Last Changed By: Bob Smith (2026-01-30)
Story Points: 13
Priority: 1
Tags: 1-ICND 2026; 2-Trade Common; 4-Modernization / Upgrades
```
---

### 3. wit_my_work_items
**Test Query**: `List my work items`
**Expected**: Work items assigned to current user
**Alternative**: `Show me top 5 work items assigned to me`
**Response**: 

```
Here are your current work items:

Tech | IC | Trade UI - Exploring the MCP Server with NodeJS

Type: Story | State: Dev Done | Project: YOUR_PROJECT | Sprint: Lexus 25.09 Sprint B
Tech | IC | Trade UI - Extend Deployment Script for Imperva S3 - Phase 2

Type: Story | State: Dev Done | Project: YOUR_PROJECT | Sprint: Lexus 25.10 Sprint B
Enable Advice download in OAF Transaction Detail page

Type: Story | State: Prioritized | Project: YOUR_PROJECT | Sprint: Your Sprint B
Enable Advice download in EXOTB Transaction Detail page

Type: Story | State: Prioritized | Project: YOUR_PROJECT | Sprint: Your Sprint B
Enable Advice download in IMOTB Transaction Detail page

Type: Story | State: Prioritized | Project: YOUR_PROJECT | Sprint: Your Sprint B
Ember lazy load engines

Type: Feature | State: Completed | Project: YOUR_PROJECT
[DESOPS] My Transactions Widget | Skeletal loading of UI is not seen when user click on Refresh button

Type: Bug | State: Done | Project: YOUR_PROJECT | Sprint: UDS SPRINT 52
[DESOPS] FFG | Column Customisation menu reset functionality not resetting the searched column

Type: Story | State: In Development | Project: YOUR_PROJECT
Let me know if you want details or actions on any specific work item.
```
---

### 4. wit_get_work_items_batch_by_ids
**Test Query**: `Batch retrieve work items 12345, 12346, 12347`
**Expected**: Details of all three work items
**Response**: 
```
Here are the details for the requested work items:

12345

Title: Tech - Standard width for Dashboard widget Page
State: In Test
Assigned To: Alice Johnson
Iteration: YOUR_PROJECT\Your Team\Your Sprint B
Story Points: 13
Description: Standard width for Dashboard widget Page, so that all widgets will be the same size in all laptop resolutions.
Tags: 1-ICND 2026; 2-Trade Common; 4-Modernization / Upgrades
Work Item Link
12346

Title: Tech | IC | Trade UI - Exploring the MCP Server with NodeJS
State: Dev Done
Assigned To: Bob Smith
Iteration: YOUR_PROJECT\DCS-Lexus (SQUAD)\Lexus 25.09 Sprint B
Story Points: 8
Description: Investigate the features, architecture, and capabilities of the MCP server for Azure DevOps.
Tags: 1-ICND 2025; 2-OAT; 4-Modernization / Upgrades
Work Item Link
12347

Title: Tech | IC | Trade UI - Extend Deployment Script for Imperva S3 - Phase 2
State: Dev Done
Assigned To: Bob Smith
Iteration: YOUR_PROJECT\DCS-Lexus (SQUAD)\Lexus 25.10 Sprint B
Story Points: 3
Description: Extend Deployment Script for Imperva S3 to support the movement of Akami Net Storage to Imperva S3 Bucket deployment.
Tags: 1-ICND 2025; 2-OAT; 4-Modernization / Upgrades
Work Item Link
Let me know if you need more details or a specific field from any of these work items.
```
---

### 5. wit_list_work_item_comments
**Test Query**: `List comments for work item 12345`
**Expected**: All comments on the work item with full details (author, date, text, mentions)
**Alternative**: `Show comments for work item 12346 in project YOUR_PROJECT`
**Response**: 
```
Here are the comments for work item 12345:

1. Test Comments for MCP.
  - Author: Bob Smith  
  - Date: 2026-01-30  
  - View: https://dev.azure.com/sc-ado/0fec05a6-bc9e-48c2-9392-b4bd1475e676/_apis/wit/workItems/12345/comments/16936886

2. @Alice Johnson As confirmed with @Bob Smith, 1400px has been set as a maximum width for the dashboard widget page.  
  cc @Ethan Kim @Kengond, Sunil  
  - Author: Carol Lee  
  - Date: 2026-01-30  
  - View: https://dev.azure.com/sc-ado/0fec05a6-bc9e-48c2-9392-b4bd1475e676/_apis/wit/workItems/12345/comments/16934837

3. @Ling, Gordon Jun Jie  
  I tested the trade dashboard page at various widths (1200px, 1300px, and 1400px) to determine a suitable standard size. I noticed some alignment issues in the UDS component at 1200px and 1300px, while everything displays correctly at 1400px.  
  PFA: 12345_Dashboard_page.docx  
  Please share your feedback on selecting the standard width.  
  cc @Dana Patel @Bob Smith @Ethan Kim  
  - Author: Carol Lee  
  - Date: 2026-01-19  
  - View: https://dev.azure.com/sc-ado/0fec05a6-bc9e-48c2-9392-b4bd1475e676/_apis/wit/workItems/12345/comments/16786320

4. Copied from #11281911  
  - Author: Ethan Kim  
  - Date: 2026-01-05  
  - View: https://dev.azure.com/sc-ado/0fec05a6-bc9e-48c2-9392-b4bd1475e676/_apis/wit/workItems/12345/comments/16649741
```

---

### 6. wit_get_work_item_type
**Test Query**: `Get work item type 'Task' for project YOUR_PROJECT`
**Expected**: Task type definition with fields and states
**Alternative Test**: `Get work item type 'Bug' for YOUR_PROJECT`
**Alternative Test**: `Get work item type 'User Story' for YOUR_PROJECT`
**Response**: 

```
The work item type 'Task' for project YOUR_PROJECT is defined as follows:

Name: Task
Reference Name: Microsoft.VSTS.WorkItemTypes.Task
Description: Tracks work that needs to be done.
States: Open, In Progress, On Hold, Done, Cancelled
Required fields: Title, State, Area ID, Iteration ID, On Hold
Default State: Open
Transitions: Tasks can move between all states (Open, In Progress, On Hold, Done, Cancelled)
More details: Work Item Type: Task
Let me know if you need the full field list or XML form details.

The work item type 'Bug' for project YOUR_PROJECT is defined as follows:

Name: Bug
Reference Name: Microsoft.VSTS.WorkItemTypes.Bug
Description: Describes a divergence between required and actual behavior, and tracks the work done to correct the defect and verify the correction.
States: Open, Prioritized, In Analysis, Ready For Development, In Development, On Hold, Dev Done, In Test, Ready For Release, Done, Cancelled, No Fix Required
Required fields: Title, State, Area ID, Iteration ID, Value Area, Application ID, Impacted Environment, Steps to Reproduce, Phase Detected, Test Phase, Help Needed, System Info
Default State: Open
Transitions: Bugs can move between all states listed above
More details: Work Item Type: Bug
Let me know if you need the full field list or XML form details.

The work item type 'User Story' for project YOUR_PROJECT is defined as follows:

Name: User Story
Reference Name: Microsoft.VSTS.WorkItemTypes.UserStory
Description: Tracks an activity the user will be able to perform with the product.
States: Open, Prioritized, In Analysis, Ready For Development, In Development, On Hold, Dev Done, In Test, Ready For Release, Done, Cancelled
Required fields: Title, State, Area ID, Iteration ID, Value Area
Default State: Open
Transitions: User Stories can move between all states listed above
More details: Work Item Type: User Story
Let me know if you need the full field list or XML form details.
```
---

### 7. wit_list_backlogs
**Test Query**: `List available backlogs for project YOUR_PROJECT team Your Team`
**Expected**: Available backlogs (e.g., Stories, Features)
**Note**: First get team list: `List teams for project YOUR_PROJECT` (use wit_list_teams)
**Response**: 
```
Available backlogs:
- Epic (id: Microsoft.EpicCategory, hidden)
- Initiative (id: Custom.0a4b1be9-8fa6-4d57-b2a6-4b5bdca581b1, hidden)
- Feature (id: Microsoft.FeatureCategory)
- Story (id: Microsoft.RequirementCategory)
- Tasks (id: Microsoft.TaskCategory)
```
---

### 8. wit_list_backlog_work_items
**Prerequisites**: Need backlog ID from wit_list_backlogs (e.g., Microsoft.RequirementCategory)
**Test Query**: `List work items in backlog Microsoft.RequirementCategory for project YOUR_PROJECT team Your Team`
**Expected**: Work items in specified backlog
**Response**: 
```
Here are the work items in the backlog Microsoft.RequirementCategory (Stories) for project YOUR_PROJECT, team Your Team:

10649830
10649868
11201259
11201285
11201309
11240642
11281996
11282004
11282006
11282066
12345
11030625
11030746 
```
**Note**: Use backlog IDs from tool #7 above

---

### 9. wit_list_teams
**Test Query**: `List teams for project YOUR_PROJECT`
**Expected**: All teams in the project including Your Team
**Response**: 
```
Here are the teams for the Azure DevOps project "YOUR_PROJECT":

DCS-AJEYA (SQUAD)
Digital Channel Solutions (RF)
Trade-Others (APP)
Cash - FI Clearing (HIVE)
Trade-Proton (SQUAD)
Trade-Rose (SQUAD)
Your Team
Trade - Trade Risk-Fraud and AML (RF)
Trade - Incremental Change (RF)
DCS-MAZDA (SQUAD)
CASH-TheHawk (SQUAD)
```

---

### 10. wit_list_iterations
**Test Query**: `List iterations for project YOUR_PROJECT team Your Team`
**Expected**: All iterations with paths, names, and start/finish dates
**Response**: 
```
Here are the iterations for project YOUR_PROJECT, team Your Team:

Abarth 25.07 Sprint B: 2025-06-09 to 2025-06-20
Abarth 25.08 Sprint A: 2025-06-23 to 2025-07-04
```

---

### 11. wit_get_work_items_for_iteration
**Prerequisites**: Need iteration path from a work item
**Test Query**: `Get work items for iteration [ITERATION_PATH] in project YOUR_PROJECT team Your Team`
**Note**: Get iteration from work item #12345 first
**Response**: 
```
Here are the work items for iteration YOUR_PROJECT\Your Team\Your Sprint B in project YOUR_PROJECT, team Your Team:

Story: Tech - Standard width for Dashboard widget Page
State: In Test
Assigned to: Alice Johnson
View Work Item

Bug: Notify Icon is not getting disabled after clicking it
State: In Test
Assigned to: R, Gowthamrishi
View Work Item

Story: Global filters should not be cleared when predefined filter is applied
State: Cancelled
Assigned to: Alice Johnson
View Work Item

Story: Retain filter values when returning from target pages to Trade Dashboard
State: In Test
Assigned to: Alice Johnson
View Work Item

Story: Enable Advice download in ELC Bills Transaction Detail page
State: Prioritized
Assigned to: Bob Smith
View Work Item

Story: Enable Advice download in EXOTB Transaction Detail page
State: Prioritized
Assigned to: Bob Smith
View Work Item

Story: Enable Advice download in IMOTB Transaction Detail page
State: Prioritized
Assigned to: Bob Smith
View Work Item
```
---

### 10. wit_list_iterations ✨ NEW
**Test Query**: `List iterations for project YOUR_PROJECT team Your Team`
**Expected**: All iterations with paths and dates
**Response**: 
```
Here are the available backlogs (iteration categories) for project YOUR_PROJECT, team Your Team:

Feature (id: Microsoft.FeatureCategory)
Initiative (id: Custom.c8b92d97-6ec5-46dd-b4b1-09cebd05617e)
Epic (id: Microsoft.EpicCategory)
Story (id: Microsoft.RequirementCategory)
Tasks (id: Microsoft.TaskCategory)
If you need to list the actual iteration paths (sprints), let me know!
```

---

### 11. wit_get_work_items_for_iteration
**Prerequisites**: Need iteration path from a work item
**Test Query**: `Get work items for iteration YOUR_PROJECT\Your Team\Your Sprint B in project YOUR_PROJECT team Your Team`
**Note**: Get iteration from work item #12345 first or use wit_list_iterations
**Response**: 
```
Here are the work items for iteration YOUR_PROJECT\Your Team\Your Sprint B in project YOUR_PROJECT, team Your Team:

Story: Tech - Standard width for Dashboard widget Page
State: In Test
Assigned to: Alice Johnson
View Work Item

Bug: Notify Icon is not getting disabled after clicking it
State: In Test
Assigned to: R, Gowthamrishi
View Work Item

Story: Global filters should not be cleared when predefined filter is applied
State: Cancelled
Assigned to: Alice Johnson
View Work Item

Story: Retain filter values when returning from target pages to Trade Dashboard
State: In Test
Assigned to: Alice Johnson
View Work Item

Story: Enable Advice download in ELC Bills Transaction Detail page
State: Prioritized
Assigned to: Bob Smith
View Work Item

Story: Enable Advice download in EXOTB Transaction Detail page
State: Prioritized
Assigned to: Bob Smith
View Work Item

Story: Enable Advice download in IMOTB Transaction Detail page
State: Prioritized
Assigned to: Bob Smith
View Work Item

If you need more details or a specific field for any work item, let me know!
```
---

### 12. wit_get_query
**Prerequisites**: Need query ID (queries may not exist)
**Test Query**: `Get query [QUERY_ID] from project YOUR_PROJECT`
**Expected**: Query definition or "query not found"
**Response**: 
```
The query with ID c0b01591-26e6-40cd-85e1-e06bda29c8da from project YOUR_PROJECT is named "TLP Active" and is located at My Queries/FFG/TLP Active. It was created and last modified by Bob Smith. You can view or edit the query in Azure DevOps using this link:
https://dev.azure.com/sc-ado/web/qr.aspx?pguid=0fec05a6-bc9e-48c2-9392-b4bd1475e676&qid=c0b01591-26e6-40cd-85e1-e06bda29c8da
```
---

### 12. wit_get_query
**Prerequisites**: Need query ID (queries may not exist)
**Test Query**: `Get query c0b01591-26e6-40cd-85e1-e06bda29c8da from project YOUR_PROJECT`
**Expected**: Query definition or "query not found"
**Response**: 
```
The query with ID c0b01591-26e6-40cd-85e1-e06bda29c8da from project YOUR_PROJECT is named "TLP Active" and is located at My Queries/FFG/TLP Active. It was created and last modified by Bob Smith. You can view or edit the query in Azure DevOps using this link:
https://dev.azure.com/sc-ado/web/qr.aspx?pguid=0fec05a6-bc9e-48c2-9392-b4bd1475e676&qid=c0b01591-26e6-40cd-85e1-e06bda29c8da
```
---

### 13. wit_get_query_results_by_id
**Prerequisites**: Need valid query ID
**Test Query**: `Get results for query [QUERY_ID] in project YOUR_PROJECT`
**Expected**: Work items matching the query
**Response**: 
```
Here are the results for query c0b01591-26e6-40cd-85e1-e06bda29c8da in project YOUR_PROJECT:

Navigating back to Trade Dashboard — Assigned to Kengond, Sunil. State: Prioritized.
Library upgrades for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Vulnerability fixes for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Library upgrades for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Library upgrades for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Let me know if you need details for any specific work item.
```
---

### 13. wit_get_query_results_by_id
**Prerequisites**: Need valid query ID
**Test Query**: `Get results for query c0b01591-26e6-40cd-85e1-e06bda29c8da in project YOUR_PROJECT`
**Expected**: Work items matching the query
**Response**: 
```
Here are the results for query c0b01591-26e6-40cd-85e1-e06bda29c8da in project YOUR_PROJECT:

Navigating back to Trade Dashboard — Assigned to Kengond, Sunil. State: Prioritized.
Library upgrades for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Vulnerability fixes for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Library upgrades for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Library upgrades for TLP repos — Assigned to Teja, Aripirala Balarka. State: Prioritized.
Let me know if you need details for any specific work item.
```
---

### 14. wit_list_work_item_pull_requests
**Test Query**: `List pull requests for work item 12345`
**Expected**: All PRs linked to the work item (may be empty if none linked)
**Response**: 
```
Work item 12345 has 2 linked pull requests:

PR #2385233 - Linked on 2026-01-30 at 09:57:37 UTC
PR #2383487 - Linked on 2026-01-30 at 05:57:51 UTC
Both pull requests were linked on January 30, 2026.
```

---

### 15. wit_list_work_item_commits
**Test Query**: `List commits for work item 12345`
**Expected**: All commits linked to the work item (may be empty if none linked)
**Response**:
```
Here are the commits linked to work item 12345:

Commit ID: 7b22d4169b950067055d14c02ed1d92ce8f25b4b (Authorized: 2026-01-30 09:57 UTC)
Commit ID: 838e3207319c8ab46b5e61be89ef200336b7ef17 (Authorized: 2026-01-30 09:14 UTC)
Commit ID: e5d7816307dc4e786bcd9d5ba8b15dfecb24472a (Authorized: 2026-01-30 05:56 UTC)
Commit ID: d6017670424705b91c80336cfcde1d78fc2d6a9a (Authorized: 2026-01-30 09:30 UTC)
Commit ID: 1a7fff79206700841e2598f571ff47b4ad166bc9 (Authorized: 2026-01-30 11:22 UTC)
If you need more details about any specific commit, let me know!
```
---

## ⚠️ WRITE OPERATIONS (Test Carefully - Makes Changes!)

### 16. wit_add_work_item_comment
**Test Query**: `Add comment "Testing comment from MCP" to work item 12345`
**Expected**: Comment added successfully AND visible when listing comments
**⚠️ WARNING**: This will actually add a comment to the work item!
**Response**: 
```
The comment "Testing comment from MCP" has been successfully added to work item 12345. If you need to verify or add more comments, let me know!
```
---

### 17. wit_update_work_item
**Test Query**: `Update work item #12345 - Add tag "MCP-Test"`
**JSON Patch Example**:
```json
{
  "id": 12345,
  "patch": [
    {
      "op": "add",
      "path": "/fields/System.Tags",
      "value": "MCP-Test"
    }
  ]
}
```
**Alternative**: `Update work item 12345 to add description "Updated via MCP"`
**⚠️ WARNING**: This will modify the work item!

---

### 17. wit_update_work_item
**Test Query**: `Update work item #12345 - Add tag "MCP-Test"`
**JSON Patch Example**:
```json
{
  "id": 12345,
  "patch": [
    {
      "op": "add",
      "path": "/fields/System.Tags",
      "value": "MCP-Test"
    }
  ]
}
```
**Alternative**: `Update work item 12345 to add description "Updated via MCP"`
**⚠️ WARNING**: This will modify the work item!

**Response**: 
```
Work item #12345 has been updated with the tag "MCP-Test". The change is complete.
```
---

### 18. wit_create_work_item
**Test Query**: `Create a SUBTASK in project YOUR_PROJECT with title "Test Task from MCP" and description "This is a test task"`
**JSON Patch Example**:
```json
{
  "project": "YOUR_PROJECT",
  "type": "Task",
  "patch": [
    {
      "op": "add",
      "path": "/fields/System.Title",
      "value": "Test Task from MCP Tool"
    },
    {
      "op": "add",
      "path": "/fields/System.Description",
      "value": "This is a test task created via MCP tool"
    }
  ]
}
```
**⚠️ WARNING**: This will create a new work item!
**Response**: 
```
A new SUBTASK has been created in project YOUR_PROJECT with the title "Test Task from MCP" and description "This is a test task".

You can view or edit it here:
https://dev.azure.com/sc-ado/0fec05a6-bc9e-48c2-9392-b4bd1475e676/_workitems/edit/12025714
```
---

### 18. wit_create_work_item
**Test Query**: `Create a SUBTASK in project YOUR_PROJECT with title "Test Task from MCP" and description "This is a test task"`
**JSON Patch Example**:
```json
{
  "project": "YOUR_PROJECT",
  "type": "Task",
  "patch": [
    {
      "op": "add",
      "path": "/fields/System.Title",
      "value": "Test Task from MCP Tool"
    },
    {
      "op": "add",
      "path": "/fields/System.Description",
      "value": "This is a test task created via MCP tool"
    }
  ]
}
```
**⚠️ WARNING**: This will create a new work item!
**Created Work Item ID**: 12025714
**Response**: 
```
A new SUBTASK has been created in project YOUR_PROJECT with the title "Test Task from MCP" and description "This is a test task".

You can view or edit it here:
https://dev.azure.com/sc-ado/0fec05a6-bc9e-48c2-9392-b4bd1475e676/_workitems/edit/12025714

Let me know if you need to update or link this work item!
```
---

### 19. wit_add_child_work_items
**Prerequisites**: Need parent and child work item IDs
**Test Query**: `Add work item [CHILD_ID] as child of work item [PARENT_ID]`
**Example**: `Add work item 12025719 as child of work item 12025714`
**⚠️ WARNING**: This will create parent-child relationship!
**Response**: 
```
Work item 12025719 has been successfully added as a child of work item 12025714. No further action is needed.
```
---

### 19. wit_add_child_work_items
**Prerequisites**: Need parent and child work item IDs
**Test Query**: `Add work item 12025719 as child of work item 12025714`
**⚠️ WARNING**: This will create parent-child relationship!
**Response**: 
```
Work item 12025719 has been successfully added as a child of work item 12025714. No further action is needed.
```
---

### 20. wit_work_items_link
**Test Query**: `Link work item 12025719 to work item 12025714 with link type 'System.LinkTypes.Related'`
**Available Link Types**:
- `System.LinkTypes.Related` - Generic relation
- `System.LinkTypes.Dependency-Forward` - This depends on target
- `System.LinkTypes.Dependency-Reverse` - Target depends on this
- `System.LinkTypes.Hierarchy-Forward` - Parent-child
**⚠️ WARNING**: This will create a link between work items!
**Response**:
```
Work item 12025719 has been successfully linked to work item 12025714 with the link type 'System.LinkTypes.Related'. No further action is needed.
```

---

### 21. wit_update_work_items_batch
**Test Query**: `Update work items 12345 and 12346 to add tag "Batch-Test"`
**JSON Example**:
```json
{
  "updates": [
    {
      "id": 12345,
      "patch": [{"op": "add", "path": "/fields/System.Tags", "value": "Batch-Test"}]
    },
    {
      "id": 12346,
      "patch": [{"op": "add", "path": "/fields/System.Tags", "value": "Batch-Test"}]
    }
  ]
}
```
**⚠️ WARNING**: This will modify multiple work items!
**Response**: 
```
Both work items 12025719 and 12025714 have been successfully updated with the tag "Batch-Test".

12025719: View in Azure DevOps
12025714: View in Azure DevOps
```
---

### 21. wit_update_work_items_batch
**Test Query**: `Update work items 12025719 and 12025714 to add tag "Batch-Test"`
**JSON Example**:
```json
{
  "updates": [
    {
      "id": 12025719,
      "patch": [{"op": "add", "path": "/fields/System.Tags", "value": "Batch-Test"}]
    },
    {
      "id": 12025714,
      "patch": [{"op": "add", "path": "/fields/System.Tags", "value": "Batch-Test"}]
    }
  ]
}
```
**⚠️ WARNING**: This will modify multiple work items!
**Response**: 
```
Both work items 12025719 and 12025714 have been successfully updated with the tag "Batch-Test".

12025719: View in Azure DevOps
12025714: View in Azure DevOps
No errors were reported. Let me know if you need to verify or perform further actions.
```

---

## 📊 Test Results Summary

### Total Tools: 21
### Success Count: 21 / 21
### Failed Count: 0 / 21
### Skipped Count: 0 / 21

---

