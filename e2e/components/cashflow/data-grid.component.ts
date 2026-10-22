import { expect, type Locator, type Page } from '@playwright/test';
import { expectUniqueVisible } from '../target.js';
import { CashflowControlScope, cssValue } from './control-scope.js';

export type GridRegion = 'center' | 'left' | 'right';

/** AG Grid operations use Cashflow_Id row keys and field/col-id column keys.
 * Only rendered rows and columns can be targeted. No grid API or row index is assumed.
 * Library DOM selectors need runtime validation against the deployed AG Grid version.
 */
export class CashflowDataGrid extends CashflowControlScope {
  constructor(page: Page, root: Locator) { super(page, root); }

  row(rowId: string, region: GridRegion = 'center'): Locator {
    const container = region === 'center' ? '.ag-center-cols-container' : `.ag-pinned-${region}-cols-container`;
    return this.root.locator(`${container} [role="row"][row-id=${cssValue(rowId)}]`);
  }
  cell(rowId: string, columnId: string): Locator {
    return this.root.locator(`[role="row"][row-id=${cssValue(rowId)}] [role="gridcell"][col-id=${cssValue(columnId)}]`);
  }
  /** Nested preview/history grids can use generated row IDs. Identify those rows through an exact visible business cell. */
  rowByDisplayedCell(columnId: string, value: string, region: GridRegion = 'center'): Locator {
    const container = region === 'center' ? '.ag-center-cols-container' : `.ag-pinned-${region}-cols-container`;
    const exactText = new RegExp(`^${value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`);
    return this.root.locator(`${container} [role="row"]`).filter({
      has: this.page.locator(`[role="gridcell"][col-id=${cssValue(columnId)}]`).filter({ hasText: exactText }),
    });
  }
  cellInRow(row: Locator, columnId: string): Locator {
    return row.locator(`[role="gridcell"][col-id=${cssValue(columnId)}]`);
  }
  header(columnId: string): Locator {
    return this.root.locator(`[role="columnheader"][col-id=${cssValue(columnId)}]`);
  }
  rowCheckbox(rowId: string): Locator {
    return this.root.locator(`[role="row"][row-id=${cssValue(rowId)}] input[type="checkbox"]`);
  }
  headerCheckbox(columnId: string): Locator { return this.header(columnId).locator('input[type="checkbox"]'); }

  async selectRow(rowId: string, selected = true): Promise<void> { await this.check(this.rowCheckbox(rowId), selected); }
  async selectAll(columnId: string, selected = true): Promise<void> { await this.check(this.headerCheckbox(columnId), selected); }
  async sortColumn(columnId: string, shift = false): Promise<void> {
    const header = this.header(columnId);
    await this.actionable(header);
    await header.click({ modifiers: shift ? ['Shift'] : [] });
  }
  async expectSort(columnId: string, order: 'ascending' | 'descending' | 'none'): Promise<void> {
    await expect(this.header(columnId)).toHaveAttribute('aria-sort', order);
  }
  async openColumnMenu(columnId: string): Promise<void> {
    const header = this.header(columnId);
    await this.actionable(header);
    await header.hover();
    const trigger = header.locator('.ag-header-cell-menu-button');
    await this.click(trigger);
  }
  /** Filter editor types and option labels depend on the selected column metadata. */
  columnFilter(): CashflowControlScope {
    return this.scoped(this.root.locator('.ag-menu:visible'));
  }
  async openContextMenu(rowId: string, columnId: string): Promise<void> {
    const cell = this.cell(rowId, columnId);
    await this.actionable(cell);
    await cell.click({ button: 'right' });
  }
  async chooseContextMenuItem(name: string): Promise<void> {
    const menu = this.root.locator('.ag-context-menu:visible');
    await expectUniqueVisible(menu);
    await this.scoped(menu).click(menu.getByRole('menuitem', { name, exact: true }));
  }
  async doubleClickRow(rowId: string, columnId: string): Promise<void> {
    const cell = this.cell(rowId, columnId);
    await this.actionable(cell);
    await cell.dblclick();
  }
  async resizeColumn(columnId: string, deltaPixels: number): Promise<void> {
    if (!Number.isFinite(deltaPixels)) throw new Error('Column resize requires a finite pixel delta.');
    const handle = this.header(columnId).locator('.ag-header-cell-resize');
    await this.actionable(handle);
    const bounds = await handle.boundingBox();
    if (!bounds) throw new Error('Column resize handle has no visible bounds.');
    const x = bounds.x + bounds.width / 2;
    const y = bounds.y + bounds.height / 2;
    await this.page.mouse.move(x, y);
    await this.page.mouse.down();
    try { await this.page.mouse.move(x + deltaPixels, y, { steps: 8 }); }
    finally { await this.page.mouse.up(); }
  }
  async scroll(verticalPixels: number, horizontalPixels = 0): Promise<void> {
    if (![verticalPixels, horizontalPixels].every(Number.isFinite)) throw new Error('Grid scroll requires finite pixel offsets.');
    await this.expectVisible();
    const vertical = this.root.locator('.ag-body-viewport');
    await expectUniqueVisible(vertical);
    await vertical.evaluate((element, top) => { element.scrollTop = top; }, verticalPixels);
    if (horizontalPixels !== 0) {
      const horizontal = this.root.locator('.ag-body-horizontal-scroll-viewport');
      await expectUniqueVisible(horizontal);
      await horizontal.evaluate((element, left) => { element.scrollLeft = left; }, horizontalPixels);
    }
  }
  async expectCellText(rowId: string, columnId: string, text: string): Promise<void> {
    const cell = this.cell(rowId, columnId);
    await expectUniqueVisible(cell);
    await expect(cell).toHaveText(text);
  }
}
