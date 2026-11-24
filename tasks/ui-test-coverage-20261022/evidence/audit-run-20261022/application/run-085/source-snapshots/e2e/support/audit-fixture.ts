import { test as base, expect, type Page, type TestInfo } from '@playwright/test';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

export type AuditScope = 'SYNTHETIC_HARNESS' | 'ACTUAL_APPLICATION_LOCAL_SERVICES' | 'CONFIGURED_APPLICATION';
type AuditOptions = { auditScope: AuditScope; auditFixture: string };
export const auditEnabled = () => Boolean(process.env.E2E_AUDIT_OUTPUT);
export function auditOutput(): string {
  if (!process.env.E2E_AUDIT_OUTPUT) throw new Error('E2E_AUDIT_OUTPUT is required for durable audit capture.');
  return path.resolve(process.env.E2E_AUDIT_OUTPUT);
}
export function auditCaseId(testId: string, title: string, retry = 0): string {
  const slug = title.replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-|-$/g, '').toLowerCase().slice(0, 75);
  return `${slug}-${createHash('sha256').update(testId).digest('hex').slice(0, 12)}-attempt-${retry + 1}`;
}
export const digest = (bytes: Buffer | string) => createHash('sha256').update(bytes).digest('hex');
export async function saveAuditJson(file: string, value: unknown): Promise<void> {
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
}

type Frame = {
  sequence: number; phase: string; capturedAt: string; path: string; sha256: string;
  claim: string; step: string; url: string; viewport: unknown; scope: AuditScope;
  method: 'Playwright Page.screenshot'; limits: string[];
  canonicalStep: number | null;
  targetPageLabel: string;
  observationsBefore: Record<string, unknown>;
  observationsAfter: Record<string, unknown>;
  sameImageAsSequence: number | null;
};

type StepCaptureOptions = { targetPage?: Page | (() => Page); pageLabel?: string };

export type CanonicalStep = {
  number: number; keyword: string; text: string; line: number;
  status: 'PENDING' | 'RUNNING' | 'PASSED' | 'FAILED' | 'NOT_EXECUTED';
  startedAt?: string; endedAt?: string; frameSequences: number[];
};
type CanonicalCase = { caseId: string; path: string; sha256: string; steps: CanonicalStep[] };
const catalogPath = path.resolve('tasks/ui-test-coverage-20261022/test-cases.md');

export async function canonicalSteps(caseId: string): Promise<CanonicalCase> {
  const bytes = await readFile(catalogPath);
  const lines = bytes.toString('utf8').split(/\r?\n/);
  let inCase = false;
  let inGherkin = false;
  const steps: CanonicalStep[] = [];
  for (const [index, line] of lines.entries()) {
    if (line.startsWith('#### ')) {
      if (inCase) break;
      inCase = line.trim() === `#### ${caseId}`;
    }
    if (!inCase) continue;
    if (line.trim() === '```gherkin') { inGherkin = true; continue; }
    if (line.trim() === '```') { inGherkin = false; continue; }
    const match = inGherkin && /^\s*(Given|When|Then|And|But)\s+(.+)$/.exec(line);
    if (match) steps.push({ number: steps.length + 1, keyword: match[1], text: match[2],
      line: index + 1, status: 'PENDING', frameSequences: [] });
  }
  if (!steps.length) throw new Error(`No canonical Gherkin steps for ${caseId}`);
  return { caseId, path: catalogPath, sha256: digest(bytes), steps };
}

export class AuditCapture {
  private frames: Frame[] = [];
  private gaps: { phase: string; capturedAt: string; error: string }[] = [];
  private sequence = 0;
  private canonical: CanonicalCase | null = null;
  private activeStep: number | null = null;
  private pageLabels = new Map<Page, string>();
  private observers = new Map<Page, () => Promise<Record<string, unknown>>>();
  readonly caseId: string;
  readonly directory: string | null;

  constructor(readonly page: Page, readonly testInfo: TestInfo, readonly scope: AuditScope, readonly fixture: string) {
    this.caseId = auditCaseId(testInfo.testId, testInfo.title, testInfo.retry);
    this.directory = auditEnabled() ? path.join(auditOutput(), 'cases', this.caseId) : null;
    this.pageLabels.set(page, 'PRIMARY');
  }

  labelPage(page: Page, label: string): void {
    if (!label.trim()) throw new Error('An audit page label cannot be empty.');
    this.pageLabels.set(page, label);
  }

  observePage(page: Page, observer: () => Promise<Record<string, unknown>>): void {
    this.observers.set(page, observer);
  }

  private async observations(page: Page): Promise<Record<string, unknown>> {
    const browser = await page.evaluate(() => {
      const active = document.activeElement;
      return { nowMs: Date.now(), visibility: document.visibilityState,
        focus: active ? { tag: active.tagName, id: active.id, role: active.getAttribute('role'),
          ariaLabel: active.getAttribute('aria-label'), placeholder: active.getAttribute('placeholder'),
          testId: active.getAttribute('data-testid'), rowId: active.closest('[data-id]')?.getAttribute('data-id') ?? null,
          field: active.closest('[data-field]')?.getAttribute('data-field') ?? null } : null };
    });
    try { return { browser, ...(await this.observers.get(page)?.() ?? {}) }; }
    catch (error) { return { browser, observationError: error instanceof Error ? error.name : 'UnknownError' }; }
  }

  async defineCase(caseId: string): Promise<readonly CanonicalStep[]> {
    if (this.canonical) throw new Error('A test attempt can bind only one canonical case.');
    this.canonical = await canonicalSteps(caseId);
    this.testInfo.annotations.push({ type: 'canonical-case', description: caseId });
    await this.persist();
    return this.canonical.steps;
  }

  /** Execute the exact canonical step, then retain its live visible state immediately. */
  async step<T>(number: number, operation: () => Promise<T>, options: StepCaptureOptions = {}): Promise<T> {
    if (!this.canonical) throw new Error('Call audit.defineCase before audit.step.');
    if (this.activeStep !== null) throw new Error('Canonical steps cannot overlap or nest.');
    const expected = this.canonical.steps.find(step => step.status !== 'PASSED');
    if (!expected || expected.number !== number || expected.status !== 'PENDING')
      throw new Error(`Canonical steps must run once in order; expected ${expected?.number ?? 'end'}, received ${number}.`);
    this.activeStep = number;
    expected.status = 'RUNNING';
    expected.startedAt = new Date().toISOString();
    await this.persist();
    const target = () => typeof options.targetPage === 'function' ? options.targetPage() : options.targetPage ?? this.page;
    const capturePage = () => {
      const selected = target();
      if (options.pageLabel) this.labelPage(selected, options.pageLabel);
      return selected;
    };
    try {
      const value = await base.step(`${number}. ${expected.keyword} ${expected.text}`, operation);
      const framesBeforeCapture = expected.frameSequences.length;
      await this.capture(`step-${String(number).padStart(2, '0')}`,
        `Visible state after step ${number}: ${expected.keyword} ${expected.text}`,
        `${this.canonical.path}:${expected.line}`, capturePage());
      if (this.directory && expected.frameSequences.length === framesBeforeCapture)
        throw new Error(`Required screenshot missing for canonical step ${number}.`);
      expected.status = 'PASSED';
      return value;
    } catch (error) {
      expected.status = 'FAILED';
      await this.capture(`step-${String(number).padStart(2, '0')}-failure`,
        `Visible state when step ${number} failed. Later steps did not execute.`,
        `${this.canonical.path}:${expected.line}`, capturePage());
      throw error;
    } finally {
      expected.endedAt = new Date().toISOString();
      this.activeStep = null;
      await this.persist();
    }
  }

  async finish(): Promise<void> {
    if (!this.canonical) return;
    const missing = this.canonical.steps.filter(step => step.status === 'PENDING' || step.status === 'RUNNING');
    for (const step of missing) step.status = 'NOT_EXECUTED';
    await this.persist();
    if (this.testInfo.status === 'passed' && missing.length)
      throw new Error(`${missing.length} canonical steps did not execute. A complete case result requires every step.`);
  }

  async capture(phase: string, claim: string, step = 'Named test assertion at the corresponding source location', targetPage: Page = this.page): Promise<void> {
    if (!this.directory) return;
    const sequence = ++this.sequence;
    const safePhase = phase.replace(/[^a-zA-Z0-9-]+/g, '-').toLowerCase();
    const filename = `${String(sequence).padStart(3, '0')}-${safePhase}.png`;
    try {
      await mkdir(this.directory, { recursive: true });
      const file = path.join(this.directory, filename);
      const targetPageLabel = this.pageLabels.get(targetPage) ?? `PAGE-${this.pageLabels.size + 1}`;
      this.labelPage(targetPage, targetPageLabel);
      const observationsBefore = await this.observations(targetPage);
      await targetPage.screenshot({ path: file, fullPage: true, animations: 'disabled', timeout: 10000 });
      const observationsAfter = await this.observations(targetPage);
      const sha256 = digest(await readFile(file));
      const previous = [...this.frames].reverse().find(frame => frame.sha256 === sha256 && frame.targetPageLabel === targetPageLabel);
      const frame: Frame = { sequence, phase, capturedAt: new Date().toISOString(), path: file,
        sha256, claim, step, url: targetPage.url(), targetPageLabel, observationsBefore, observationsAfter,
        sameImageAsSequence: previous?.sequence ?? null,
        viewport: targetPage.viewportSize(), scope: this.scope, method: 'Playwright Page.screenshot', canonicalStep: this.activeStep,
        limits: ['The screenshot establishes visible state only. It does not prove request, storage, timing, or business results.',
          ...(this.scope === 'SYNTHETIC_HARNESS' ? ['The browser rendered a controlled fixture. The real MFE and BFF were not executed.'] : [])] };
      this.frames.push(frame);
      if (this.activeStep !== null) this.canonical?.steps[this.activeStep - 1].frameSequences.push(sequence);
      await saveAuditJson(path.join(this.directory, filename.replace('.png', '.json')), frame);
      await this.testInfo.attach(`${phase} (${this.scope})`, { path: file, contentType: 'image/png' });
    } catch (error) {
      this.gaps.push({ phase, capturedAt: new Date().toISOString(), error: error instanceof Error ? error.name : 'UnknownError' });
    }
    await this.persist();
  }

  async record(name: string, observations: unknown): Promise<void> {
    if (!this.directory) return;
    const filename = `${name.replace(/[^a-zA-Z0-9-]+/g, '-').toLowerCase()}.json`;
    await saveAuditJson(path.join(this.directory, filename), { recordedAt: new Date().toISOString(),
      caseId: this.caseId, scope: this.scope, observations });
  }

  async persist(): Promise<void> {
    if (!this.directory) return;
    await saveAuditJson(path.join(this.directory, 'frames.json'), {
      caseId: this.caseId, testId: this.testInfo.testId, title: this.testInfo.title,
      scope: this.scope, fixture: this.fixture, source: this.testInfo.file,
      browserVersion: this.page.context().browser()?.version() ?? null,
      captureStatus: this.gaps.length ? 'INCOMPLETE' : this.frames.length ? 'CAPTURED' : 'NO_FRAMES',
      frames: this.frames, captureGaps: this.gaps,
      canonical: this.canonical,
      completeStepEvidence: this.canonical ? this.canonical.steps.every(step =>
        step.status === 'PASSED' && step.frameSequences.length > 0) : false,
      canonicalBusinessStatus: this.scope === 'SYNTHETIC_HARNESS' ? 'NOT_RUN' : 'LOCAL_CONTROLLED_ASSERTIONS',
    });
  }
}

export const test = base.extend<AuditOptions & { audit: AuditCapture }>({
  auditScope: ['SYNTHETIC_HARNESS', { option: true }],
  auditFixture: ['Source-shaped controlled DOM and routed responses; no actual MFE or BFF execution.', { option: true }],
  audit: async ({ page, auditScope, auditFixture }, use, testInfo) => {
    const audit = new AuditCapture(page, testInfo, auditScope, auditFixture);
    testInfo.annotations.push({ type: 'audit-scope', description: auditScope });
    testInfo.annotations.push({ type: 'audit-fixture', description: auditFixture });
    try { await use(audit); }
    finally {
      await audit.capture(testInfo.status === testInfo.expectedStatus ? 'final-result' : 'failure-result',
        testInfo.status === testInfo.expectedStatus ? 'The final visible state after the named test assertions.' : 'The visible state when the test failed.',
        `Test source: ${testInfo.file}:${testInfo.line}`);
      await audit.persist();
      await audit.finish();
    }
  },
});
export { expect };
