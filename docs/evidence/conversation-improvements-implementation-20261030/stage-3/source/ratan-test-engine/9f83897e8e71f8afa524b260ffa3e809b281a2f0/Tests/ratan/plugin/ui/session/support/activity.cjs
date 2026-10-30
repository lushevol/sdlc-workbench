'use strict';
const { assert, claims, promptSelector, sleep, tokenSummary, waitUntil } = require('./common.cjs');
const { retain } = require('./session.cjs');
const { emitActivity, protectedRequest } = require('./browser.cjs');

async function assertActivityRenewsSession(kind, page) {
  return retain(page, `activity-${kind}`, async (state, result) => {
    if (kind === 'scroll') {
      assert.ok(state.config.scrollSelector, 'Configure a scrollable portal-document element.');
      await page.locator(state.config.scrollSelector).hover();
    }
    // Login and pointer setup can schedule mouse renewal. Exclude it from every activity assertion window.
    await sleep(6000);
    await waitUntil(() => state.inFlight.size === 0, 10000, 'Setup renewal must finish before the activity assertion window.');
    const baselineAccess = await page.evaluate(() => localStorage.getItem('SET_TOKEN'));
    result.activityBaselineAccess = tokenSummary(baselineAccess);
    assert.ok(claims(baselineAccess).exp * 1000 - Date.now() >= 30000, 'AC-1–AC-3 require at least 30 seconds before access expiry.');
    const initialCount = state.renewals.length;
    const initialActivity = await page.evaluate(() => ({ ...window.__sessionE2e.activity }));
    const started = Date.now();
    let emitted = 0;
    while (Date.now() - started < 15000) {
      await emitActivity(page, state, kind, emitted++);
      await sleep(100);
    }
    const accepted = state.renewals.slice(initialCount).filter(item => item.time <= started + 15000);
    const activity = await page.evaluate(() => window.__sessionE2e.activity);
    const eventName = { mouse: 'mousemove', keyboard: 'keydown', scroll: 'scroll' }[kind];
    const trustedEvents = activity[eventName] - initialActivity[eventName];
    assert.ok(trustedEvents >= Math.floor(emitted / 2), 'The portal document must receive repeated trusted activity events.');
    assert.ok(accepted.length > 0, 'At least one successful renewal must finish within the 15-second continuous-activity interval.');
    assert.ok(accepted.some(item => item.access.exp > claims(baselineAccess).exp), 'Renewal must move the access expiry forward.');
    assert.equal(await page.locator(promptSelector).isVisible(), false, 'Activity must not produce an expiry prompt.');
    await waitUntil(() => state.inFlight.size === 0, 10000, 'All activity renewals must settle before the protected request.');
    const installedAccess = await page.evaluate(() => localStorage.getItem('SET_TOKEN'));
    assert.ok(installedAccess, 'Activity must install a renewed access token before the protected request.');
    result.protectedRequest = await protectedRequest(page, state, installedAccess);
    result.assertions.push({ kind, emitted, trustedEvents, intervalMs: 100, elapsedMs: Date.now() - started, successfulRenewals: accepted.length });
  });
}

module.exports = { assertActivityRenewsSession };
