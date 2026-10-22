import type { Page } from '@playwright/test';
import type { UiTarget } from '../catalog/ui-contracts.js';
import { inspectTarget } from '../components/target.js';

export async function inspectTargets(page: Page, targets: UiTarget[], captureUi: boolean) {
  return {
    targets: await Promise.all(targets.map(inspectTarget)),
    accessibilitySnapshot: captureUi ? await page.locator('body').ariaSnapshot() : null,
    snapshotScope: captureUi ? 'current DOM; may contain application data' : 'disabled',
  };
}

export async function componentCoverage(page: Page, targets: UiTarget[], includeIdentities: boolean) {
  const handles = [];
  for (const target of targets) {
    const inspection = await inspectTarget(target);
    if (inspection.count === 1 && inspection.visible) handles.push(await target.locator.elementHandle());
  }
  try {
    const controls = await page.evaluate(({ mapped, includeIdentities }) => {
      const selector = 'button,a[href],input:not([type="hidden"]),select,textarea,[role="button"],[role="link"],[role="tab"],[role="menuitem"],[role="checkbox"],[role="grid"]';
      return Array.from(document.querySelectorAll(selector)).filter(el =>
        el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden',
      ).map(el => {
        const labels = el instanceof HTMLInputElement ? Array.from(el.labels ?? []).map(label => label.textContent).join(' ') : '';
        const identity = el.getAttribute('aria-label') || el.getAttribute('data-testid') || el.id || labels ||
          (el.matches('button,a,[role="button"],[role="link"],[role="tab"],[role="menuitem"]') ? el.textContent?.trim() : null);
        return { type: el.getAttribute('role') || el.tagName.toLowerCase(),
          identifiable: Boolean(identity), identity: includeIdentities ? identity : null,
          mapped: mapped.some(target => target === el) };
      });
    }, { mapped: handles, includeIdentities });
    const identifiable = controls.filter(control => control.identifiable);
    return { discoveredVisibleControls: controls.length, identifiableControls: identifiable.length,
      controlsWithUniqueVisiblePomTarget: identifiable.filter(control => control.mapped).length,
      unidentifiableControls: controls.filter(control => !control.identifiable).length,
      unmapped: identifiable.filter(control => !control.mapped),
      limits: ['Counts cover visible light DOM controls in this page state only.',
        'The selected POM area defines mapped targets. Hidden states, virtual rows, and iframe contents remain outside this count.',
        'Element identity uses DOM attributes and labels. It does not compute the complete accessible name.'] };
  } finally { await Promise.all(handles.map(handle => handle?.dispose())); }
}
