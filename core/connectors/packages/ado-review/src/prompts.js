import { z } from 'zod';

export function configureReviewPrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'review-pr',
      description: 'Review a pull request and post automated code quality comments',
      args: {
        prUrl: z.string().describe('Azure DevOps Pull Request URL')
      }
    },
    {
      name: 'analyze-pr-diff',
      description: 'Analyze the diff of a pull request for insights and potential issues',
      args: {
        prUrl: z.string().describe('Azure DevOps Pull Request URL')
      }
    },
    {
      name: 'delete-pr-review-comments',
      description: 'Delete all AI-generated review comments from a pull request',
      args: {
        prUrl: z.string().describe('Azure DevOps Pull Request URL')
      }
    }
  ];

  const messageGenerators = {
    'review-pr': (args) =>
      `Review pull request: ${args.prUrl}\n\nPerform automated code quality review and post comments directly on the PR with 🤖 Co-pilot Assisted Review prefix.`,
    'analyze-pr-diff': (args) =>
      `Analyze the changes in pull request: ${args.prUrl}\n\nUse repo_pr_diff to get the diff, then provide insights on code complexity, potential bugs, performance considerations, and security concerns.`,
    'delete-pr-review-comments': (args) =>
      `Delete all AI-generated review comments from pull request: ${args.prUrl}\n\nUse delete_all_pr_review_comments to remove all comments with the 🤖 Co-pilot Assisted Review: prefix.`
  };

  for (const prompt of prompts) {
    const callback = async (args) => {
      getContext();
      const text = messageGenerators[prompt.name](args ?? {});
      return { messages: [{ role: 'user', content: { type: 'text', text } }] };
    };
    server.prompt(prompt.name, prompt.description, prompt.args, callback);
  }

  console.error(`Registered ${prompts.length} review prompts`);
}
