import { configureTestPlanTools } from './tools/testplans.js';

export function configureTestPlanToolsModule(server, getADOConnection) {
  configureTestPlanTools(server, getADOConnection);
}
