import { configureReviewTool } from './tools/review.js';
export { getRefactorInstructions } from './tools/review.js';

export function configureReviewTools(server, getADOConnection, options = {}) {
  configureReviewTool(server, getADOConnection, options);
}
