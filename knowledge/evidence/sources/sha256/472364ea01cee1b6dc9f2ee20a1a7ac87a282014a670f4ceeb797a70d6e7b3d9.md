## Overview

The **Ratan Oct Service** is a unified GraphQL API that aggregates data from your DevOps ecosystem—including Azure DevOps, SonarQube, and Confluence—into a single, consistent interface. Instead of juggling multiple APIs and authentication schemes, developers interact with one endpoint to query and manipulate work items, code quality metrics, documentation, and more.

**API Base URL: **<u>[Ratan Oct Service](http://uklvadrtn006a.pi.dev.net:1218/graphql)</u>

## Confluence API

### Purpose & Main Functionalities

The Confluence API enables you to fetch detailed information about Confluence pages and spaces, including content in various formats (Markdown, HTML, XML), version history, and author details.

### Key Queries & Types

- **Query: `confluencePage(pageId: String!, contentFormats: [String])`** Retrieves a Confluence page by its ID, with selectable content formats.
- **Types:** - `ConfluencePage`: Page metadata, content, space, and version info - `ConfluenceContent`: Markdown, HTML, styled HTML, storage, XML - `ConfluenceSpaceInfo`: Space metadata - `ConfluenceVersion`: Versioning details - `ConfluenceUser`: User info

### Usage Example

Please set "confluencetoken" on the query headers.
`query {
confluencePage(pageId: "12345", contentFormats: ["markdown", "html"]) {
title
status
content {
markdown
html
}
space {
key
name
}
version {
number
by {
displayName
}
}
}
}
`
## SonarQube API

### Purpose & Main Functionalities

The SonarQube API provides access to code quality metrics for pull requests and branches, such as coverage, bugs, vulnerabilities, and code smells.

### Key Queries & Types

- **Query: `sonarqubePullRequest(prId: Int!, repo: String!)`** Fetches code quality metrics for a specific pull request.
- **Query: `sonarqubeBranch(branch: String!, repo: String!)`** Fetches metrics for a specific branch.
- **Types:** - `SonarqubeResult`: Contains `measures` - `SonarqubeMeasures`: Coverage, bugs, vulnerabilities, code smells, etc.

### Usage Example

Please set "sonarqubetoken" on the query headers.
`query {
sonarqubePullRequest(prId: 42, repo: "my-repo") {
measures {
coverage
new_bugs
new_vulnerabilities
new_code_smells
}
}
}
`
## Azure DevOps (ADO) API

### Purpose & Main Functionalities

The ADO API exposes a wide range of DevOps data and operations, including builds, releases, test cases, test plans, test runs, test suites, test points, and work items. It supports both querying and mutations for test management and release tracking.

### Key Queries & Types

- **Builds:** - `adoBuild(buildId: Int!)`: Fetch build details.
- **Releases:** - `adoRelease(id: Int!)`: Fetch release work item details. - `queryRatanReleaseIds(from: String, to: String)`: List release IDs in a date range.
- **Test Management:** - `adoTestCases(ids: [Int!]!)`: Fetch test cases. - `adoTestPlan(id: Int!)`: Fetch test plan. - `adoTestPoints(planId: Int!, suiteId: Int!)`: Fetch test points. - `adoTestRun(id: Int!)`: Fetch test run. - `adoTestSuite(testPlanId: Int!, testSuiteId: Int!)`: Fetch test suite. - `adoTestRunResults(testRunId: Int!)`: Fetch test run results.
- **Work Items:** - `queryWorkitemsByWiql(queryWiql: String!)`: Query work items using WIQL.
- **Types:** - `AdoBuild`, `AdoReleaseWorkItem`, `AdoTestCase`, `AdoTestPlan`, `AdoTestPoint`, `AdoTestRun`, `AdoTestSuite`, `WorkitemQueryResult`, etc.

### Usage Example

Please set "adotoken" on the query headers.
`query {
adoBuild(buildId: 1001) {
id
status
repo
url
buildNumber
result
startTime
finishTime
}
}
`
## Getting Started

1. Replace the API base URL placeholder with your actual endpoint.
2. Use the provided GraphQL queries as templates for your integration.
3. Refer to the schema for additional fields and mutations as needed.