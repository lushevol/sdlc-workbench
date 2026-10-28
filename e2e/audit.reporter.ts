import type { Reporter, FullConfig, Suite, TestCase, TestResult, FullResult, TestStep } from '@playwright/test/reporter';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { auditCaseId, digest } from './support/audit-fixture.js';

const workspace = fileURLToPath(new URL('../', import.meta.url));
const executionClaim = (scope: string) => scope === 'SYNTHETIC_HARNESS' ? 'NOT_RUN'
  : scope === 'CONFIGURED_APPLICATION' ? 'CONFIGURED_APPLICATION_ASSERTIONS' : 'LOCAL_CONTROLLED_ASSERTIONS';
const save = (file: string, content: unknown) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(content, null, 2)}\n`, { mode: 0o600 });
};
function sourceFiles(directory: string): string[] {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) return ['results', 'playwright-report', 'test-results', 'validation'].includes(entry.name) ? [] : sourceFiles(file);
    return /\.(?:ts|mjs|js|json)$/.test(entry.name) ? [file] : [];
  });
}
const git = (...args: string[]) => {
  try { return execFileSync('git', args, { cwd: workspace, encoding: 'utf8' }).trim(); }
  catch { return null; }
};
function steps(value: TestStep[]): unknown[] {
  return value.map(step => ({ title: step.title, category: step.category, location: step.location,
    durationMs: step.duration, error: step.error ?? null, steps: steps(step.steps) }));
}
function walkFiles(directory: string): string[] {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? walkFiles(file) : [file];
  });
}

export default class AuditReporter implements Reporter {
  private output: string;
  private startedAt = new Date().toISOString();
  private completed: Record<string, unknown> = {};
  private planned: { caseId: string; testId: string; title: string; source: unknown }[] = [];
  private scope = process.env.E2E_AUDIT_SCOPE ?? 'SYNTHETIC_HARNESS';
  private sourceHashes: { path: string; sha256: string; snapshotPath: string }[] = [];
  private excludedSources: Set<string>;
  constructor(options: { output?: string; excludedSources?: string[] }) {
    this.output = path.resolve(options.output ?? process.env.E2E_AUDIT_OUTPUT!);
    this.excludedSources = new Set((options.excludedSources ?? []).map(file => path.resolve(file)));
  }

  onBegin(config: FullConfig, suite: Suite) {
    if (fs.existsSync(path.join(this.output, 'run-inputs.json'))) throw new Error('Audit output already contains a run. Choose a new directory to preserve prior evidence.');
    this.planned = suite.allTests().map(test => ({ caseId: auditCaseId(test.id, test.title), testId: test.id,
      title: test.title, source: test.location }));
    const sources = [...sourceFiles(path.join(workspace, 'e2e')), path.join(workspace, 'package.json'), path.join(workspace, 'package-lock.json')]
      .filter(file => !this.excludedSources.has(path.resolve(file)));
    this.sourceHashes = sources.map(file => {
      const relative = path.relative(workspace, file);
      const bytes = fs.readFileSync(file);
      const snapshotPath = path.join(this.output, 'source-snapshots', relative);
      fs.mkdirSync(path.dirname(snapshotPath), { recursive: true });
      fs.writeFileSync(snapshotPath, bytes, { flag: 'wx', mode: 0o600 });
      return { path: relative, sha256: digest(bytes), snapshotPath };
    });
    save(path.join(this.output, 'run-inputs.json'), {
      schemaVersion: 1, startedAt: this.startedAt, sourceRevision: git('rev-parse', 'HEAD'),
      worktreeStatus: git('status', '--short'), platform: process.platform, architecture: process.arch,
      nodeVersion: process.version, workers: config.workers, scope: this.scope,
      target: config.metadata.executionTarget ?? null,
      fixture: process.env.E2E_AUDIT_FIXTURE ?? 'Controlled source-shaped DOM and routed service responses.',
      command: process.argv, sourceHashes: this.sourceHashes,
      planned: this.planned, canonicalBusinessExecution: executionClaim(this.scope),
      limits: ['Per-case scope and assertion mappings determine the supported execution claim. A title or screenshot does not establish a canonical business pass.'],
    });
    this.progress();
  }

  onTestBegin(test: TestCase, result: TestResult) {
    const id = auditCaseId(test.id, test.title, result.retry);
    save(path.join(this.output, 'cases', id, 'started.json'), { caseId: id, testId: test.id,
      title: test.title, source: test.location, startedAt: result.startTime.toISOString(),
      status: 'RUNNING', scope: this.scope, canonicalBusinessExecution: 'NOT_YET_ESTABLISHED' });
  }

  onTestEnd(test: TestCase, result: TestResult) {
    const id = auditCaseId(test.id, test.title, result.retry);
    const directory = path.join(this.output, 'cases', id);
    const attachments = result.attachments.map((attachment, index) => {
      if (!attachment.path || !fs.existsSync(attachment.path)) return { name: attachment.name, contentType: attachment.contentType, unavailable: true };
      const original = attachment.path;
      const existing = path.resolve(original).startsWith(`${directory}${path.sep}`);
      const target = existing ? original : path.join(directory, 'attachments', `${String(index + 1).padStart(3, '0')}-${path.basename(original)}`);
      if (!existing) { fs.mkdirSync(path.dirname(target), { recursive: true }); fs.copyFileSync(original, target); }
      return { name: attachment.name, contentType: attachment.contentType,
        originalPath: original, retainedPath: target, sha256: digest(fs.readFileSync(target)), copiedBytesUnchanged: true };
    });
    const framesFile = path.join(directory, 'frames.json');
    const frames = fs.existsSync(framesFile) ? JSON.parse(fs.readFileSync(framesFile, 'utf8')) : null;
    const scope = frames?.scope ?? test.annotations.find(annotation => annotation.type === 'audit-scope')?.description ?? 'SYNTHETIC_HARNESS';
    const record = { caseId: id, testId: test.id, title: test.title, source: test.location,
      startedAt: result.startTime.toISOString(), endedAt: new Date().toISOString(), durationMs: result.duration,
      expectedStatus: test.expectedStatus, actualStatus: result.status, outcome: test.outcome(),
      assertionsSatisfied: result.status === test.expectedStatus, scope,
      canonicalIdsMentioned: [...test.title.matchAll(/\b[A-Z]+(?:-[A-Z]+)*-\d+\b/g)].map(match => match[0]),
      canonicalBusinessExecution: executionClaim(scope), errors: result.errors, assertionSteps: steps(result.steps),
      annotations: test.annotations,
      frames: frames ? { path: framesFile, sha256: digest(fs.readFileSync(framesFile)), count: frames.frames.length, captureStatus: frames.captureStatus } : null,
      screenshotGap: !frames ? (test.title.startsWith('missing source checkout') ? 'NOT_APPLICABLE: This source validation case has no UI.' : 'No named screenshot frames were retained.') : null,
      attachments, limits: scope === 'SYNTHETIC_HARNESS' ? ['Passing harness checks do not establish actual React, BFF, or business behavior.']
        : ['The recorded assertions and environment binding limit the supported business result.'],
    };
    save(path.join(directory, 'result.json'), record);
    const files = walkFiles(directory).filter(file => path.basename(file) !== 'artifact-manifest.json');
    save(path.join(directory, 'artifact-manifest.json'), { caseId: id, savedAt: new Date().toISOString(),
      artifacts: files.map(file => ({ path: file, bytes: fs.statSync(file).size, sha256: digest(fs.readFileSync(file)) })) });
    this.completed[id] = { caseId: id, title: test.title, actualStatus: result.status, outcome: test.outcome(),
      result: path.join(directory, 'result.json'), sha256: digest(fs.readFileSync(path.join(directory, 'result.json'))),
      screenshotFrames: frames?.frames.length ?? 0, screenshotGap: record.screenshotGap };
    this.progress();
  }

  onEnd(result: FullResult) {
    const records = Object.values(this.completed) as { actualStatus: string; screenshotFrames: number }[];
    const sourceDrift = this.sourceHashes.filter(source => {
      const current = path.join(workspace, source.path);
      return !fs.existsSync(current) || digest(fs.readFileSync(current)) !== source.sha256;
    }).map(source => ({ path: source.path, beforeSha256: source.sha256,
      snapshotPath: source.snapshotPath, limit: 'Review affected test dependencies before reusing this run.' }));
    save(path.join(this.output, 'run-result.json'), { startedAt: this.startedAt, endedAt: new Date().toISOString(),
      runnerStatus: result.status, scope: this.scope, canonicalBusinessExecution: executionClaim(this.scope),
      plannedTests: this.planned.length, completedTests: records.length,
      statuses: Object.fromEntries([...new Set(records.map(item => item.actualStatus))].map(status => [status, records.filter(item => item.actualStatus === status).length])),
      screenshotFrames: records.reduce((count, record) => count + record.screenshotFrames, 0),
      incompleteTests: this.planned.filter(test => !this.completed[test.caseId]), cases: Object.values(this.completed) });
    save(path.join(this.output, 'source-integrity.json'), { checkedAt: new Date().toISOString(),
      retainedSourceFiles: this.sourceHashes.length, sourceDrift,
      status: sourceDrift.length ? 'SOURCE_CHANGED_DURING_RUN' : 'SOURCE_UNCHANGED_DURING_RUN' });
    this.progress();
  }

  private progress() {
    save(path.join(this.output, 'progress.json'), { updatedAt: new Date().toISOString(), plannedTests: this.planned.length,
      completedTests: Object.keys(this.completed).length, cases: Object.values(this.completed),
      remaining: this.planned.filter(test => !this.completed[test.caseId]),
      resume: 'Read the completed per-case results and artifact hashes. Run only missing cases in a new audit output directory.' });
    const lines = ['# UI audit evidence', '', '**Use each case scope and assertion mapping before claiming a canonical business result.**', '',
      `Execution scope: ${this.scope}.`, '',
      `Completed cases: ${Object.keys(this.completed).length} of ${this.planned.length}.`, '',
      ...Object.values(this.completed).map(value => {
        const item = value as { caseId: string; title: string; actualStatus: string; result: string };
        return `- [${item.title}](cases/${item.caseId}/result.json): ${item.actualStatus}.`;
      }), '',
      'writing_review:', '  standard: ASD-STE100', '  automated_check: NOT_RUN', '  asd_review: PENDING',
      '  reviewer: null', '  reviewed_at: null', '  limitations:',
      '    - Automated checks do not check the complete approved dictionary or grammar rules.', ''];
    fs.writeFileSync(path.join(this.output, 'index.md'), lines.join('\n'));
  }
}
