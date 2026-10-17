import { spawn } from 'node:child_process';
import { realpathSync } from 'node:fs';
import { isAbsolute } from 'node:path';
import { pathToFileURL } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js';
import { loadConfig } from './config.js';
import { CONNECTORS, createConnectorServer, validateConnectorConfig } from './server.js';

const ERROR_MESSAGE = 'The connector request failed. Check configuration, access, and tool arguments.';

async function restartWithEnvironment(input, args, env) {
  const output = await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [process.argv[1], ...args], {
      cwd: args[1], env, stdio: ['pipe', 'pipe', 'inherit'],
    });
    let stdout = '';
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.on('error', reject);
    child.on('close', code => {
      if (code === 0) resolve(stdout);
      else reject(new Error('The connector process failed.'));
    });
    child.stdin.on('error', reject);
    child.stdin.end(input);
  });
  process.stdout.write(output);
}

export async function executeRequest(request, workspaceRoot) {
  if (!request || typeof request !== 'object' || Array.isArray(request) ||
      !CONNECTORS.includes(request.connector) || !['list', 'call'].includes(request.operation)) {
    return { status: 'ERROR', code: 'INVALID_REQUEST', message: 'The connector request is invalid.' };
  }
  if (request.operation === 'call' &&
      (typeof request.tool !== 'string' || !request.tool ||
       (request.arguments !== undefined && (!request.arguments ||
        typeof request.arguments !== 'object' || Array.isArray(request.arguments))))) {
    return { status: 'ERROR', code: 'INVALID_REQUEST', message: 'The tool request is invalid.' };
  }

  let client;
  let server;
  try {
    const config = loadConfig(workspaceRoot);
    Object.assign(process.env, config.env);
    process.env.WORKBENCH_CONNECTOR_WORKSPACE = config.workspaceRoot;
    process.chdir(config.workspaceRoot);
    if (request.operation === 'call') validateConnectorConfig(request.connector, config);
    server = await createConnectorServer(request.connector, config);
    client = new Client({ name: 'workbench-connector-bridge', version: '1.0.0' });
    const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
    await server.connect(serverTransport);
    await client.connect(clientTransport);
    if (request.operation === 'list') {
      const response = await client.listTools();
      return { status: 'SUCCEEDED', tools: response.tools };
    }
    const result = await client.callTool({ name: request.tool, arguments: request.arguments || {} });
    if (result.isError) return { status: 'ERROR', code: 'TOOL_ERROR', message: ERROR_MESSAGE };
    return { status: 'SUCCEEDED', result };
  } catch {
    return { status: 'ERROR', code: 'CONNECTOR_ERROR', message: ERROR_MESSAGE };
  } finally {
    await client?.close().catch(() => {});
    await server?.close().catch(() => {});
  }
}

async function main() {
  // Tool diagnostics must not corrupt the single JSON response on stdout.
  console.log = (...args) => console.error(...args);
  let response;
  try {
    const args = process.argv.slice(2);
    if (args.length !== 2 || args[0] !== '--workspace' || !isAbsolute(args[1])) {
      throw new Error('An absolute workspace path is required.');
    }
    let input = '';
    for await (const chunk of process.stdin) {
      input += chunk;
      if (Buffer.byteLength(input) > 8 * 1024 * 1024) throw new Error('The request is too large.');
    }
    const config = loadConfig(args[1]);
    // Node reads additional CA certificates only at process startup.
    if (config.env.NODE_EXTRA_CA_CERTS && config.env.NODE_EXTRA_CA_CERTS !== process.env.NODE_EXTRA_CA_CERTS) {
      await restartWithEnvironment(input, args, config.env);
      return;
    }
    response = await executeRequest(JSON.parse(input), args[1]);
  } catch {
    response = { status: 'ERROR', code: 'INVALID_REQUEST', message: 'The connector request is invalid.' };
  }
  process.stdout.write(`${JSON.stringify(response)}\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  await main();
}
