# @sc-node-mcp/ado-core

Shared Azure DevOps connection factory used by all `@sc-node-mcp/ado-*` sub-packages.

## Usage

```js
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
```

## Configuration

Set `AZURE_DEVOPS_PAT` and `AZURE_DEVOPS_ORG_URL` via environment variable, CLI arg, or `config.json`.
