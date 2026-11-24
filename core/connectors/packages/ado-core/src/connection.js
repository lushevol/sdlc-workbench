import * as azdev from 'azure-devops-node-api';
import { getConfig } from '@sc-node-mcp/core';

export async function getADOConnection() {
  const { AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PAT } = getConfig();
  const authHandler = azdev.getPersonalAccessTokenHandler(AZURE_DEVOPS_PAT);
  return new azdev.WebApi(AZURE_DEVOPS_ORG_URL, authHandler);
}
