import { realpathSync } from 'node:fs';
import { isAbsolute, relative, sep } from 'node:path';
import { createInterface } from 'node:readline';
import { pathToFileURL } from 'node:url';
import { z } from 'zod';
import { loadConfig } from './config.js';
import { validateConnectorConfig } from './server.js';
import { confinedEvidencePath, REPORT_READERS, ReportReader, validateReportArguments } from './release-readers.js';

const initSchema = z.object({ id: z.union([z.string(), z.number()]), operation: z.literal('init'),
  allowed_tools: z.array(z.string().min(1).max(256)).max(4096), run_dir: z.string().min(1),
  concurrency: z.number().int().min(1).max(32).default(6),
  request_timeout_seconds: z.number().min(0.01).max(3600).default(30),
  deadline_seconds: z.number().min(0.01).max(3600).default(300) }).strict();
const callSchema = z.object({ id: z.union([z.string(), z.number()]), operation: z.literal('call'),
  tool: z.string().min(1).max(256), arguments: z.record(z.unknown()).optional(), evidence_path: z.string().min(1) }).strict();

function error(id, code) {
  return { id, status: 'ERROR', code, message: 'The report connector operation failed.' };
}

export async function serveReleaseSession(workspaceRoot, connector, input, output) {
  if (!isAbsolute(workspaceRoot) || !['ado', 'sonar'].includes(connector)) throw new Error('Invalid session context.');
  const root = realpathSync(workspaceRoot);
  const config = loadConfig(root);
  Object.assign(process.env, config.env);
  let reader;
  let runDir;
  let allowed = new Set();
  let closing = false;
  const active = new Set();
  const seen = new Set();
  const claimedPaths = new Set();
  const write = payload => output.write(`${JSON.stringify(payload)}\n`);
  const lines = createInterface({ input, crlfDelay: Infinity });

  const handle = async request => {
    const id = request?.id ?? null;
    if (id === null || !['string', 'number'].includes(typeof id) || seen.has(id)) return write(error(id, 'INVALID_REQUEST'));
    seen.add(id);
    if (seen.size > 1000000) return write(error(id, 'REQUEST_LIMIT'));
    try {
      if (request.operation === 'init') {
        if (reader || closing) return write(error(id, 'ALREADY_INITIALIZED'));
        const values = initSchema.parse(request);
        if (!isAbsolute(values.run_dir)) return write(error(id, 'INVALID_PATH'));
        runDir = realpathSync(values.run_dir);
        const part = relative(root, runDir);
        if (!part || part === '..' || part.startsWith(`..${sep}`) || isAbsolute(part)) return write(error(id, 'INVALID_PATH'));
        validateConnectorConfig(connector, config);
        allowed = new Set(values.allowed_tools);
        reader = new ReportReader(connector, config, values);
        write({ id, status: 'SUCCEEDED', connector, endpoint: reader.base, metrics: { ...reader.metrics } });
      } else if (request.operation === 'close') {
        if (!reader) return write(error(id, 'NOT_INITIALIZED'));
        closing = true;
        await Promise.allSettled([...active]);
        const metrics = { ...reader.metrics };
        reader.close();
        write({ id, status: 'SUCCEEDED', metrics });
        lines.close();
      } else if (request.operation === 'call') {
        if (!reader || closing) return write(error(id, 'NOT_INITIALIZED'));
        const values = callSchema.parse(request);
        if (!allowed.has(values.tool)) return write(error(id, 'TOOL_NOT_GRANTED'));
        validateReportArguments(connector, values.tool, values.arguments);
        const destination = confinedEvidencePath(runDir, values.evidence_path);
        if (claimedPaths.has(destination)) return write(error(id, 'INVALID_PATH'));
        claimedPaths.add(destination);
        const result = await reader.read(values.tool, values.arguments, destination);
        write({ id, ...result });
      } else if (request.operation === 'list') {
        write({ id, status: 'SUCCEEDED', tools: Object.entries(REPORT_READERS)
          .filter(([, spec]) => spec.connector === connector).map(([name]) => ({ name, allowed: allowed.has(name) })) });
      } else write(error(id, 'INVALID_REQUEST'));
    } catch (failure) {
      const code = failure instanceof z.ZodError ? 'INVALID_ARGUMENT' :
        ['UNKNOWN_TOOL', 'INVALID_ARGUMENT', 'INVALID_PATH', 'DEADLINE_EXCEEDED', 'CANCELLED', 'RESPONSE_TOO_LARGE', 'REQUEST_FAILED'].includes(failure.code) ? failure.code : 'CONNECTOR_FAILURE';
      write(error(id, code));
    }
  };

  try {
    for await (const line of lines) {
      if (Buffer.byteLength(line) > 1024 * 1024) { write(error(null, 'REQUEST_TOO_LARGE'));continue; }
      let request;
      try { request = JSON.parse(line); } catch { write(error(null, 'INVALID_REQUEST'));continue; }
      if (request?.operation === 'init' || request?.operation === 'close') {
        await handle(request);
        if (closing) break;
      } else {
        const pending = handle(request);
        active.add(pending);
        pending.finally(() => active.delete(pending));
      }
    }
    await Promise.allSettled([...active]);
  } finally {
    reader?.close();
    input.pause();
  }
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length !== 4 || args[0] !== '--workspace' || args[2] !== '--connector') throw new Error('Invalid arguments.');
  await serveReleaseSession(args[1], args[3], process.stdin, process.stdout);
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  try { await main(); }
  catch { process.stdout.write(`${JSON.stringify(error(null, 'INVALID_CONFIGURATION'))}\n`);process.exitCode = 1; }
}
