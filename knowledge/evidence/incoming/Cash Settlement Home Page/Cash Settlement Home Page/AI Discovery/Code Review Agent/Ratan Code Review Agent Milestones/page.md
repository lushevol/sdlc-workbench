The Ratan Code Review Agent is an AI-powered tool designed to streamline pull request reviews by offering actionable suggestions and improvements based on recent code changes. Its primary goal is to help developers maintain high code quality and follow best practices.

## Performance Overview (Last 2 Weeks)

- Reviewed 100+ pull requests
- Average execution time: 30 seconds
- Task completion rate: 95%

## Capabilities

- **Code Review**: Analyses code changes and provides feedback on improvements, coding standards, and best practices.
- **Change Summary**: Summarizes key modifications in pull requests and their implications.
- **Related Work Items Summary**: Highlights associated work items to ensure all relevant tasks are addressed.
- **Static Metrics Aggregation**: Presents static code metrics to assess quality and maintainability.

## Milestones

### Completed Milestones

- 0.1: Local-only, reviews code changes.
- 0.2: Integrate Sonar for quality checks (Demo version).
- 0.3: Improve context and prompts for higher precision.
- 0.4: Add auto mode to scan all available PRs.
- 0.5: Generate PR descriptions and summarize related work items.

### Future Milestones

- 1.0: Standalone service, no personal machine needed. Fully refactored with LangGraph.
- 2.0: Visualized review results.
- 3.0: Custom prompts and workflow builder integration.
- 4.0: Add support for multiple programming languages.
- 5.0: Implement user feedback mechanisms for continuous improvement.

## Current Limitations & Solutions

### LLM Provider

Relies on the GitHub Copilot API, available only in VSCode, restricting execution to local developer environments. This dependency may cause inconsistencies in performance and availability.

**Follow up**: Integrate with AI Factory LLM API for broader accessibility.

### ADO Authentication

Uses ADO tokens for accessing pull requests and work items. Tokens are valid only when the owner is authenticated, which can interrupt operations if tokens expire, blocking agent running 7x24.

**Follow up**: Employ a robot account with a long-lived token or a token pool for uninterrupted access.

### Code Changes Data Source

Code changes are detected via local git diff comparisons, as ADO API does not provide this data.

**Follow up**: This approach may be unreliable. Still finding a proper solution.

### PR Event Subscription

Enables real-time updates on pull request activities, enhancing responsiveness and integration with CI/CD pipelines.

**Follow up**: Seek for ado team's support to implement a webhook for ADO events.

## Better Generation

- Provide clear, actionable instructions. [https://www.promptingguide.ai/](https://www.promptingguide.ai/)
- Ensure comprehensive project context and code guideline/preferences.
- Include essential comments for clarity.
- Generate precise PR titles and detailed descriptions.

## Better Reviewing

- Enhance context understanding by integrating documentation and comments for more relevant suggestions.
- Reference established coding standards and best practices to ensure consistent reviews.
- Clearly define the scope of each review to focus feedback.
- Leverage historical issues as a knowledge base for continuous improvement.

## Benchmarking Metrics

- accuracy
- precision
- recall
- F1 Score

## Observable

- feedback
- accept rate

## Next Steps

- AI Factory
- Observable & Testing
- Standalone Service
- ADO event notification