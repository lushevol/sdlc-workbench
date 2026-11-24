# Ratan AI Code Review Agent: Overview & Updates

This document provides an overview of the Ratan AI Code Review Agent, including its mechanism, recent enhancements, initial findings, and our roadmap for the future.

## How It Works

The agent is designed to automate the initial pass of a code review, catching common issues and allowing developers to focus on more complex logic. Here is the step-by-step workflow:

1. **Scan Repositories**: The agent continuously scans all 51358-ratan and mfe repositories in Azure DevOps (ADO).
2. **Identify New PRs**: It fetches all pull requests (PRs) created within the last two weeks.
3. **Filter for Actionable PRs**: The list is narrowed down to PRs that have recent human-raised updates but have not yet received a review.
4. **Fetch Code Changes**: Using the ADO API, the agent retrieves the specific code changes (git diff) for each targeted PR.
5. **Prepare for AI Review**: It filters out automatically generated or irrelevant files (e.g., package-lock.json, build artifacts) to focus the analysis.
6. **AI-Powered Review**: The filtered code is sent to a Large Language Model (LLM) with a carefully designed set of instructions. The AI reviews the code for potential bugs, style inconsistencies, and performance improvements, then outputs a structured result.
7. **Log & Comment**: The agent posts the AI's feedback as a comment directly on the PR in ADO and logs the results in our database for tracking and analysis.
8. **Feedback Loop**: Any replies made to the agent's comment are automatically forwarded to our development team. This is crucial for helping us improve the system!

## Recent Enhancements

We've recently rolled out several key updates to improve the agent's reliability and intelligence:

1. **Enhanced Reliability**: Migrated from local git diff generation to using the official Azure DevOps API, ensuring more stable and secure data retrieval.
2. **Always-On Service**: Deployed the agent as a persistent service on a dedicated VM, enabling continuous, automated reviews without manual intervention.
3. **Improved Scalability**: Exposed the core LLM as a standardized OpenAI-compatible API, making it easier to maintain and integrate with other tools in the future.
4. **Comprehensive File Analysis**: Updated the logic to scan file-by-file instead of as a single large block. This guarantees full coverage for large PRs without hitting context window limits.
5. **Smarter AI**: Significantly optimized the prompts sent to the AI, resulting in more accurate and relevant feedback.
6. **Focused Reviews**: Added logic to filter out unsupported file types, reducing noise and focusing the agent on the code it understands best.

## Initial Findings & Performance

The agent is still in its Proof of Concept (POC) phase, but early results are promising.

- **Coverage**: In the last two weeks, the agent has automatically reviewed 128 pull requests.
- **Impact**: It has successfully identified several potential issues, including potential null pointer risks, and opportunities for refactoring.
- **Important Note**: Please treat the agent's feedback as a helpful "first pass" review. It is a supplement, not a replacement, for thorough human code review. 🧑‍💻

## How You Can Help Us Improve

To make this tool truly effective, we need your active participation. Here’s what we ask from all development teams:

- **Engage with the Feedback**: Please don't just ignore the agent's comments. Set the status after checked the list. - ![image-2025-9-19_11-0-54.png](attachments/image-2025-9-19_11-0-54.png) - Pending → I'm fixing, will update later. - Resolved → Reported bugs fixed. - Won't Fix → Reported bugs can be all ignore.
- **Provide Constructive Criticism**: If a suggestion is incorrect or not useful, please reply directly to the comment on the PR. This is the most valuable data we can get to improve the agent's accuracy.
- **Improve Release Visibility**: Please create release-to-main PRs at least 4 days ahead of the release date. This gives the agent (and your teammates!) enough time to review what's changing.

## Next Steps & Roadmap

We are actively working on the next phase of development. Our key priorities are:

- **Smarter Context**: Ingest historical ratan issue descriptions and team-specific review instructions to provide more tailored and insightful feedback.
- **Easier Feedback**: Implement a one-click feedback mechanism on comments to make providing input even faster.
- **Continued Optimization**: Continuously refine the workflow and prompts to reduce inaccuracies and improve the quality of suggestions.
- **Model Upgrades**: Evaluate and upgrade to more powerful underlying AI models as they become available.