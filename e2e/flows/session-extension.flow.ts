import { expect, type Page, type Request } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import type { PortalPage } from '../pages/portal.page.js';
import { assertion, sha256, type AssertionResult, type ExecutionScope } from '../support/results.js';

export type SessionExtensionOptions = {
  scope: ExecutionScope;
  workspaceName: string;
  releaseRenewal?: () => void;
  timeoutMs?: number;
  refreshCredentialSha256?: string;
};

export async function extendSessionAndVerifyAuthentication(portal: PortalPage, options: SessionExtensionOptions) {
  const page = portal.page;
  const assertions: AssertionResult[] = [];
  const requests: Request[] = [];
  const origin = new URL(page.url()).origin;
  const timeout = options.timeoutMs ?? 10000;
  const matches = (request: Request, path: string) =>
    request.method() === 'POST' && request.url() === `${origin}${path}`;
  const observe = (request: Request) => { if (matches(request, '/api/auth/v2/sso/relogin')) requests.push(request); };
  const dialog = portal.sessionTimeoutDialog;
  let responseWait: ReturnType<Page['waitForResponse']> | undefined;
  let predicate = 'session-preconditions';
  let renewalReleased = false;
  const releaseRenewal = () => {
    if (renewalReleased) return;
    renewalReleased = true;
    options.releaseRenewal?.();
  };
  try {
    if (options.refreshCredentialSha256 && !/^[a-f0-9]{64}$/.test(options.refreshCredentialSha256)) {
      throw new Error('The expected refresh fingerprint must be a SHA-256 value.');
    }
    await dialog.expectVisible();
    page.on('request', observe);
    responseWait = page.waitForResponse(response => response.request() === requests[0] &&
      matches(response.request(), '/api/auth/v2/sso/relogin'), { timeout });
    // Attach a rejection handler before an action can fail or a response can time out.
    void responseWait.catch(() => {});
    predicate = 'extend-click';
    await dialog.clickExtendButton();
    predicate = 'dialog-closed';
    await dialog.expectAbsent();
    assertions.push(assertion('dialog-closed', true, 'absent'));
    predicate = 'one-relogin-request';
    await expect.poll(() => requests.length, { timeout }).toBeGreaterThan(0);
    const requestRefresh = await requests[0]!.headerValue('single-ui-refresh');
    const refreshObservation = { expectedSha256: options.refreshCredentialSha256 ?? null,
      requestSha256: requestRefresh ? sha256(requestRefresh) : null };
    assertions.push(options.refreshCredentialSha256
      ? assertion('refresh-credential', refreshObservation.requestSha256 === options.refreshCredentialSha256, refreshObservation)
      : { id: 'refresh-credential', status: 'unverified', actual: refreshObservation });
    releaseRenewal();
    predicate = 'renewal-accepted';
    const renewal = await responseWait;
    assertions.push(assertion('renewal-accepted', renewal.status() === 200, renewal.status()));
    const renewed = await renewal.headerValue('single-ui-authorization');
    // Token installation may follow the response event. Poll the independent storage observation.
    predicate = 'installed-access';
    if (renewal.status() === 200 && renewed) {
      await expect.poll(async () => (await page.evaluate(() => localStorage.getItem('SET_TOKEN'))) === renewed, { timeout }).toBe(true);
    }
    const installed = await page.evaluate(() => localStorage.getItem('SET_TOKEN'));
    assertions.push(assertion('installed-access', Boolean(renewed && installed === renewed && renewal.status() === 200), {
      responseSha256: renewed ? sha256(renewed) : null, installedSha256: installed ? sha256(installed) : null,
    }));
    predicate = 'workspace-visible';
    await portal.expectWorkspaceTabVisible(options.workspaceName);
    assertions.push(assertion('workspace-visible', true, options.workspaceName));
    const probeId = randomUUID();
    const validationWait = page.waitForResponse(response => matches(response.request(), '/api/auth/v2/sso/validate') &&
      response.request().headers()['x-workbench-pom-probe'] === probeId, { timeout });
    void validationWait.catch(() => {});
    // Fixed, read-only authentication predicate. No caller-supplied JavaScript or endpoint.
    predicate = 'validation-result';
    await page.evaluate(async ({ timeoutMs, probeId }) => {
      await fetch('/api/auth/v2/sso/validate', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Workbench-POM-Probe': probeId },
        body: JSON.stringify({ singleUIAuthorization: localStorage.getItem('SET_TOKEN') }),
        signal: AbortSignal.timeout(timeoutMs),
      });
    }, { timeoutMs: timeout, probeId });
    const validation = await validationWait;
    const payload = validation.request().postDataJSON() as { singleUIAuthorization?: string };
    const body: unknown = await validation.json();
    const result = typeof body === 'object' && body !== null && 'result' in body ? body.result : undefined;
    const tokenMatches = Boolean(installed && payload.singleUIAuthorization === installed);
    assertions.push(assertion('validation-request-token', tokenMatches, {
      requestSha256: payload.singleUIAuthorization ? sha256(payload.singleUIAuthorization) : null,
      installedSha256: installed ? sha256(installed) : null,
    }));
    assertions.push(assertion('validation-result', validation.status() === 200 && result === true,
      { httpStatus: validation.status(), result: typeof result === 'boolean' ? result : null,
        resultType: typeof result }));
    assertions.push(assertion('one-relogin-request', requests.length === 1, requests.length));
    return {
      flow: 'session-extension', scope: options.scope,
      status: assertions.some(value => value.status === 'failed') ? 'failed'
        : assertions.some(value => value.status === 'unverified') ? 'unverified' : 'passed', assertions,
      observations: { dialogClosed: true, sessionValid: tokenMatches && validation.status() === 200 && result === true },
      limits: ['Authentication validation does not establish token lifetime or downstream authorization.',
        'Request counts cover the flow observation window only.',
        'Refresh comparison requires an independently observed or fixture-defined credential fingerprint.'],
    };
  } catch (error) {
    assertions.push(assertion(predicate, false, { error: error instanceof Error ? error.name : 'UnknownError' }));
    return { flow: 'session-extension', scope: options.scope, status: 'failed', assertions,
      observations: { sessionValid: null },
      limits: ['The flow stopped before all independent predicates were established.'] };
  } finally {
    releaseRenewal();
    page.off('request', observe);
  }
}
