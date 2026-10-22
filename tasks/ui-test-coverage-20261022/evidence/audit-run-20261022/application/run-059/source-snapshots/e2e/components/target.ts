import { expect, type Locator } from '@playwright/test';
import type { UiTarget } from '../catalog/ui-contracts.js';

export interface TargetInspection {
  readonly contract: UiTarget['contract'];
  readonly count: number;
  readonly visible: boolean | null;
  readonly enabled: boolean | null;
  readonly available: boolean;
  readonly reason: 'ready' | 'not-found' | 'ambiguous' | 'hidden' | 'disabled';
}

export async function inspectTarget(target: UiTarget): Promise<TargetInspection> {
  const count = await target.locator.count();
  if (count !== 1) {
    return { contract: target.contract, count, visible: null, enabled: null,
      available: false, reason: count === 0 ? 'not-found' : 'ambiguous' };
  }
  const visible = await target.locator.isVisible();
  const enabled = await target.locator.isEnabled();
  return { contract: target.contract, count, visible, enabled, available: visible && enabled,
    reason: !visible ? 'hidden' : !enabled ? 'disabled' : 'ready' };
}

export async function expectUniqueVisible(locator: Locator): Promise<void> {
  await expect(locator).toHaveCount(1);
  await expect(locator).toBeVisible();
}

export async function expectActionable(target: UiTarget, scope?: Locator): Promise<void> {
  if (scope) await expectUniqueVisible(scope);
  await expectUniqueVisible(target.locator);
  await expect(target.locator).toBeEnabled();
}

export const assertUniqueVisibleEnabled = expectActionable;
