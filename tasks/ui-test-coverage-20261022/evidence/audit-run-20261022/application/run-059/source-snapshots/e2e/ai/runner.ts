import { chromium, type Page } from '@playwright/test';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import { browserLaunchOptions } from '../browser-config.js';
import { createActions, createPom, describeActions, executeAction, targetsForArea, type Area, type Pom } from '../catalog/actions.js';
import { componentCoverage, inspectTargets } from '../support/discovery.js';
import { extendSessionAndVerifyAuthentication } from '../flows/session-extension.flow.js';
import { installPortalFixture, fixturePrefix, fixtureCredentials, type PortalFixture } from '../fixtures/portal.fixture.js';
import { checkSourceContracts } from '../support/source-quality.js';
import { sha256 } from '../support/results.js';

export type Step = { command: 'inspect' | 'action' | 'run' | 'validate'; id?: string; area?: Area };
const areas = ['portal', 'login', 'category'] as const;
const root = fileURLToPath(new URL('../../', import.meta.url));
class RunnerInputError extends Error { override name = 'RunnerInputError'; }
export function validateSteps(value: unknown): Step[] {
  if (!Array.isArray(value) || value.length === 0 || value.length > 50) throw new RunnerInputError('Supply 1 to 50 sequence steps.');
  for (const step of value) {
    if (!step || typeof step !== 'object' || Object.keys(step).some(key => !['command', 'id', 'area'].includes(key))) throw new RunnerInputError('Invalid step fields.');
    if (!['inspect', 'action', 'run', 'validate'].includes(step.command)) throw new RunnerInputError('Unsupported sequence command.');
    if (step.area !== undefined && !areas.includes(step.area)) throw new RunnerInputError('Unsupported UI area.');
    if (['action', 'run'].includes(step.command) && typeof step.id !== 'string') throw new RunnerInputError('Action and flow steps require an ID.');
  }
  return value as Step[];
}

type Environment = { page: Page; pom: Pom; fixture?: PortalFixture; captureUi: boolean; allowSessionChange: boolean;
  workspaceName: string; refreshCredentialSha256?: string };
export async function executeSteps(steps: Step[], environment: Environment) {
  // Every step receives the same page and context. Failure stops dependent steps.
  validateSteps(steps);
  const actions = createActions(environment.pom);
  for (const step of steps) {
    if (step.command === 'action' && !actions.has(step.id!)) throw new RunnerInputError(`Unknown action: ${step.id}`);
    if (step.command === 'run' && step.id !== 'session-extension') throw new RunnerInputError(`Unknown flow: ${step.id}`);
    if ((step.command === 'run' || (step.command === 'action' && actions.get(step.id!)?.risk === 'session-state-change')) &&
      !environment.allowSessionChange) throw new RunnerInputError('Session actions require --allow-session-change.');
  }
  const results: unknown[] = [];
  for (const step of steps) {
    const area = step.area ?? 'portal';
    const targets = targetsForArea(environment.pom, area);
    let result: { status: string; [key: string]: unknown };
    try {
      if (step.command === 'action') result = await executeAction(actions, step.id!, environment.allowSessionChange);
      else if (step.command === 'run') result = await extendSessionAndVerifyAuthentication(environment.pom.portal, {
        scope: environment.fixture ? 'synthetic-fixture' : 'configured-application', workspaceName: environment.workspaceName,
        releaseRenewal: environment.fixture?.releaseRenewal,
        refreshCredentialSha256: environment.fixture ? sha256(fixtureCredentials.refresh) : environment.refreshCredentialSha256,
      });
      else {
        const inspection = await inspectTargets(environment.page, targets, environment.captureUi);
        const coverage = await componentCoverage(environment.page, targets, environment.captureUi);
        const rootTarget = inspection.targets.find(target => target.contract.id === `${area}.root`);
        const validationStatus = !rootTarget?.visible || rootTarget.count !== 1 || inspection.targets.some(target => target.count > 1)
          ? 'failed' : inspection.targets.some(target => target.count === 0 || !target.visible) ? 'unverified' : 'passed';
        result = { command: step.command, area, status: step.command === 'validate' ? validationStatus : 'passed',
          ...inspection, coverage,
          validationScope: 'Current-state inspection only. Absent controls remain unverified; this does not pass all area contracts.' };
      }
    } catch (error) {
      result = { command: step.command, id: step.id ?? null, area, status: 'failed',
        error: error instanceof Error ? error.name : 'UnknownError',
        observations: { sessionValid: null },
        limits: ['The operation failed before its named postconditions were established.'] };
    }
    results.push(result);
    if (result.status === 'failed') break;
  }
  return results;
}

function parseArguments(args: string[]) {
  const positional: string[] = [];
  const options: Record<string, string | boolean> = {};
  const flags = ['fixture', 'allow-session-change', 'capture-ui'];
  const valued = ['url', 'prefix', 'out', 'area', 'steps-file', 'workspace', 'refresh-sha256'];
  for (let i = 0; i < args.length; i++) {
    const token = args[i]!;
    if (!token.startsWith('--')) { positional.push(token); continue; }
    const key = token.slice(2);
    if (Object.hasOwn(options, key)) throw new RunnerInputError(`Duplicate option: ${key}`);
    if (flags.includes(key)) options[key] = true;
    else if (valued.includes(key) && args[i + 1] && !args[i + 1]!.startsWith('--')) options[key] = args[++i]!;
    else throw new RunnerInputError(`Unknown or incomplete option: ${key}`);
  }
  return { positional, options };
}

export async function main(args: string[]) {
  const { positional, options } = parseArguments(args);
  const command = positional[0];
  const prefix = typeof options.prefix === 'string' ? options.prefix : fixturePrefix;
  if (command === 'actions' && positional[1] === 'list' && positional.length === 2) {
    return { status: 'passed', actions: describeActions(prefix) };
  }
  if (command === 'validate' && !options.url && !options.fixture && positional.length === 1) {
    const check = spawnSync(process.execPath, [path.join(root, 'e2e/scripts/check-traceability.mjs')], { encoding: 'utf8', cwd: root });
    const sourceQuality = await checkSourceContracts();
    return { status: check.status === 0 && sourceQuality.status === 'passed' ? 'passed' : 'failed', validationScope: 'Static traceability and source contracts; no browser started.',
      sourceQuality,
      traceability: check.stdout ? JSON.parse(check.stdout) : null };
  }
  let steps: Step[];
  if (command === 'sequence' && typeof options['steps-file'] === 'string' && positional.length === 1) {
    steps = validateSteps(JSON.parse(await readFile(options['steps-file'], 'utf8')));
  } else if (['inspect', 'validate', 'action', 'run'].includes(command ?? '')) {
    if (positional.length !== (['action', 'run'].includes(command!) ? 2 : 1)) throw new RunnerInputError('Unexpected positional arguments.');
    steps = validateSteps([{ command, ...(positional[1] ? { id: positional[1] } : {}),
      ...(options.area ? { area: options.area } : {}) }]);
  } else throw new RunnerInputError('Use actions list, inspect, action ID, run session-extension, sequence --steps-file FILE, or validate.');
  if (options.fixture && options.url) throw new RunnerInputError('Choose --fixture or --url.');
  if (!options.fixture && !options.url) throw new RunnerInputError('Browser commands require --fixture or an explicit --url.');
  if (options.url && !options.prefix) throw new RunnerInputError('Configured applications require the actual --prefix value.');
  if (options.url) {
    const target = new URL(String(options.url));
    if (!['http:', 'https:'].includes(target.protocol) || target.username || target.password) throw new RunnerInputError('Use an HTTP URL without embedded credentials.');
  }
  const output = path.resolve(String(options.out ?? `e2e/results/${Date.now()}`));
  await mkdir(output, { recursive: true, mode: 0o700 });
  const browser = await chromium.launch(browserLaunchOptions());
  const context = await browser.newContext({ serviceWorkers: 'block' });
  const page = await context.newPage();
  let fixture: PortalFixture | undefined;
  let tracing = false;
  try {
    if (options.fixture) {
      await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
      tracing = true;
      fixture = await installPortalFixture(page);
    } else await page.goto(String(options.url));
    const results = await executeSteps(steps, { page, pom: createPom(page, prefix), fixture,
      captureUi: Boolean(options.fixture || options['capture-ui']), allowSessionChange: Boolean(options['allow-session-change']),
      workspaceName: String(options.workspace ?? 'WS-A'),
      refreshCredentialSha256: typeof options['refresh-sha256'] === 'string' ? options['refresh-sha256'] : undefined });
    const statuses = results.map(value => (value as { status: string }).status);
    const result = { status: statuses.includes('failed') ? 'failed' : statuses.includes('unverified') ? 'unverified' : 'passed',
      scope: fixture ? 'synthetic-fixture' : 'configured-application', results,
      evidence: { summary: path.join(output, 'result.json'), trace: tracing ? path.join(output, 'trace.zip') : null },
      limits: ['Separate CLI invocations create isolated contexts. Use sequence for dependent actions.',
        'Synthetic execution does not update canonical business readiness or execution states.'] };
    await writeFile(path.join(output, 'result.json'), `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 });
    return result;
  } finally {
    await fixture?.cleanup();
    if (tracing) await context.tracing.stop({ path: path.join(output, 'trace.zip') });
    await context.close();
    await browser.close();
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).then(result => {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    if (result.status === 'failed' || result.status === 'unverified') process.exitCode = 1;
  }).catch(error => {
    // Do not emit Playwright call logs, response bodies, storage, or raw credentials.
    process.stderr.write(`${JSON.stringify({ status: 'failed', error: error instanceof Error ? error.name : 'UnknownError',
      message: error instanceof RunnerInputError ? error.message : 'The operation failed. Inspect the named target and preconditions.' })}\n`);
    process.exitCode = 1;
  });
}
