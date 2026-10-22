import { expect, type Download, type Locator, type Page } from '@playwright/test';
import { expectUniqueVisible } from '../target.js';

/** Quote an attribute value without treating business identifiers as CSS syntax. */
export function cssValue(value: string): string {
  if (!value.trim()) throw new Error('A nonempty control identity is required.');
  return `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/[\n\r\f]/g, '\\a ')}"`;
}

/** MuiDialogV1 forwards a literal aria-labelledby that can differ from the generated title ID. */
export function namedDialogRoot(page: Page, title: string | RegExp): Locator {
  const text = typeof title === 'string'
    ? new RegExp(`^${title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?:$|\\s+-)`)
    : title;
  return page.locator('.MuiDialogTitle-root .MuiGrid-item').filter({ hasText: text })
    .locator('xpath=ancestor::*[@role="dialog"][1]');
}

/** Shared controls for source-defined and metadata-generated cashflow fields.
 * Portalled options require the opener's ARIA association or an explicit popup scope.
 * Missing, duplicate, hidden, and disabled targets fail before an interaction.
 */
export class CashflowControlScope {
  constructor(readonly page: Page, readonly root: Locator) {}

  scoped(root: Locator): CashflowControlScope { return new CashflowControlScope(this.page, root); }
  testId(id: string): Locator { return this.root.getByTestId(id); }
  button(name: string): Locator { return this.root.getByRole('button', { name, exact: true }); }
  link(name: string): Locator { return this.root.getByRole('link', { name, exact: true }); }
  tab(name: string): Locator { return this.root.getByRole('tab', { name, exact: true }); }
  menuItem(name: string): Locator { return this.root.getByRole('menuitem', { name, exact: true }); }
  label(name: string): Locator { return this.root.getByLabel(name, { exact: true }); }
  placeholder(name: string): Locator { return this.root.getByPlaceholder(name, { exact: true }); }

  /** Test IDs can identify either a native input or its toolkit wrapper. */
  field(id: string): Locator { return this.editable(this.testId(id)); }
  combobox(id: string): Locator {
    const wrapper = this.testId(id);
    return wrapper.getByRole('combobox').or(wrapper.and(this.page.getByRole('combobox')));
  }
  editable(target: Locator): Locator {
    const selector = 'input:not([type="hidden"]), textarea, [contenteditable="true"]';
    return target.locator(selector).or(target.and(this.page.locator(selector)));
  }

  async expectVisible(): Promise<void> { await expectUniqueVisible(this.root); }
  async actionable(target: Locator): Promise<void> {
    await this.expectVisible();
    await expectUniqueVisible(target);
    await expect(target).toBeEnabled();
    // aria-disabled can occur on wrapper controls outside native disabled elements.
    await expect(target).not.toHaveAttribute('aria-disabled', 'true');
  }
  async click(target: Locator): Promise<void> { await this.actionable(target); await target.click(); }
  async hover(target: Locator): Promise<void> { await this.actionable(target); await target.hover(); }
  async fill(target: Locator, value: string): Promise<void> {
    const input = this.editable(target);
    await this.actionable(input);
    await expect(input).toBeEditable();
    await input.fill(value);
  }
  async press(target: Locator, key: string): Promise<void> { await this.actionable(target); await target.press(key); }
  async check(target: Locator, checked = true): Promise<void> {
    await this.actionable(target);
    await target.setChecked(checked);
    await expect(target).toBeChecked({ checked });
  }

  async associatedPopup(opener: Locator): Promise<Locator> {
    await expect(opener).toHaveCount(1);
    const association = (await opener.getAttribute('aria-controls')) ?? (await opener.getAttribute('aria-owns'));
    if (!association?.trim()) throw new Error('The control has no associated popup. Supply an explicit popup scope.');
    const ids = association.trim().split(/\s+/);
    return this.page.locator(ids.map(id => `[id=${cssValue(id)}]`).join(', '));
  }

  async selectOption(opener: Locator, optionLabel: string, popup?: Locator): Promise<void> {
    await this.click(opener);
    let scope = popup ?? await this.associatedPopup(opener);
    // AntD virtual Select separates hidden accessibility options from clickable items.
    // Resolve its visible dropdown through the associated element, never through a page-wide option label.
    if (!popup) {
      const dropdown = this.page.locator('.ant-select-dropdown').filter({ has: scope }).filter({ visible: true });
      if (await dropdown.count() > 0) scope = dropdown;
    }
    await expectUniqueVisible(scope);
    const antItems = scope.locator('.ant-select-item-option');
    const option = await antItems.count() > 0
      ? antItems.filter({ hasText: new RegExp(`^${optionLabel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`) })
      : scope.getByRole('option', { name: optionLabel, exact: true });
    await expectUniqueVisible(option);
    await expect(option).toBeEnabled();
    await expect(option).not.toHaveAttribute('aria-disabled', 'true');
    await expect(option).not.toHaveClass(/(?:^|\s)ant-select-item-option-disabled(?:\s|$)/);
    await option.click();
  }

  async setSwitch(target: Locator, checked: boolean): Promise<void> {
    await this.actionable(target);
    await expect(target).toHaveAttribute('role', 'switch');
    const current = await target.getAttribute('aria-checked');
    if (!['true', 'false'].includes(current ?? '')) throw new Error('Switch has no definite aria-checked state.');
    if (current !== String(checked)) await target.click();
    await expect(target).toHaveAttribute('aria-checked', String(checked));
  }

  /** File inputs are intentionally hidden by upload widgets; uniqueness and enabled state still apply. */
  async upload(input: Locator, files: Parameters<Locator['setInputFiles']>[0]): Promise<void> {
    await this.expectVisible();
    await expect(input).toHaveCount(1);
    await expect(input).toHaveAttribute('type', 'file');
    await expect(input).toBeEnabled();
    await input.setInputFiles(files);
  }
  async download(trigger: Locator): Promise<Download> {
    await this.actionable(trigger);
    const result = this.page.waitForEvent('download');
    await trigger.click();
    return result;
  }
  async dragTo(source: Locator, destination: Locator): Promise<void> {
    await this.actionable(source);
    await this.actionable(destination);
    await source.dragTo(destination);
  }
}
