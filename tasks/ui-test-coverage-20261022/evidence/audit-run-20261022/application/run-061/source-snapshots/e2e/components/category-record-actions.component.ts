import type { Locator } from '@playwright/test';
import { createCategoryRecordContracts, type UiTargets } from '../catalog/ui-contracts.js';
import { expectActionable } from './target.js';

export class CategoryRecordActions {
  readonly editMenuItem: Locator;
  readonly auditMenuItem: Locator;
  readonly targets: UiTargets;

  constructor(private readonly grid: Locator, readonly recordId: string) {
    const contracts = createCategoryRecordContracts(recordId);
    this.editMenuItem = grid.getByTestId(contracts.editMenuItem.identity);
    this.auditMenuItem = grid.getByTestId(contracts.auditMenuItem.identity);
    this.targets = {
      editMenuItem: { contract: contracts.editMenuItem, locator: this.editMenuItem },
      auditMenuItem: { contract: contracts.auditMenuItem, locator: this.auditMenuItem },
    };
  }

  async clickEditMenuItem(): Promise<void> {
    await expectActionable(this.targets.editMenuItem, this.grid);
    await this.editMenuItem.click();
  }

  async clickAuditMenuItem(): Promise<void> {
    await expectActionable(this.targets.auditMenuItem, this.grid);
    await this.auditMenuItem.click();
  }
}
