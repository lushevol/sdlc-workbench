import { type Locator, type Page } from '@playwright/test';
import { CashflowControlScope, cssValue, namedDialogRoot } from './control-scope.js';

/** Date variables and regular-expression flags use page portals outside their rule. */
export class CashflowQueryValuePopup extends CashflowControlScope {
  readonly dayType = this.combobox('custom-day-type-select');
  readonly dayOffset = this.field('custom-day-value-select');
  readonly timeType = this.combobox('custom-time-type-select');
  readonly timeOffset = this.field('custom-time-value-input');
  readonly currentDateButton = this.button('Current Date');
  readonly lastBusinessDayButton = this.button('Last Business Day');
  readonly nextBusinessDayButton = this.button('Next Business Day');
  readonly currentTimeButton = this.button('Current Time');
  readonly setButton = this.button('Set');
  readonly ignoreCaseCheckbox = this.root.getByRole('checkbox', { name: 'Ignore Case', exact: true });
}

// Identities come from RatanFilterBuilder and ViewSelector in mfe-ratan-container.
// Repeated query controls require a caller-selected rule/group scope.
export class CashflowQueryRule extends CashflowControlScope {
  readonly fieldSelector = this.testId('custom-field-selector');
  readonly operatorSelector = this.root.locator('.rule-operators');
  readonly valueSelector = this.testId('custom-value-selector');
  readonly textValue = this.field('text-input');
  readonly numberValues = this.field('multiple-input-number');
  readonly textArea = this.field('textarea-input');
  readonly regularExpression = this.field('regexp-input');
  readonly regularExpressionOptions = this.testId('regexp-icon');
  readonly dateVariable = this.testId('open-popover');
  readonly dateRange = this.testId('datePicker-rangePicker');
  readonly dateTime = this.field('datetime-local');
  readonly time = this.testId('time-picker');
  readonly dateWithTime = this.testId('datePicker-timePicker');
  readonly switchValue = this.testId('switch-type');
  readonly checkboxValue = this.testId('checkbox-type');
  readonly radioValues = this.testId('radio-type');
  readonly autocomplete = this.testId('customAntDValueEditor-autoComplete');
  readonly fallbackValue = this.field('customAntDValueEditor-Input');
  readonly removeButton = this.root.locator('button.rule-remove');

  // Some field types render repeated inputs. Supply an exact input locator from this scope.
  valueInput(testId: string): Locator { return this.field(testId); }
  multipleDates(type: 'date' | 'datetime' | 'time'): Locator { return this.field(`multiple-date-picker-${type}`); }

  /** Supply the observed popup root when several builder instances can open overlays. */
  relativeDatePopup(observedRoot: Locator): CashflowQueryValuePopup {
    return new CashflowQueryValuePopup(this.page, observedRoot);
  }
  regularExpressionPopup(observedRoot = this.page.getByTestId('regexp-flags').filter({ visible: true })): CashflowQueryValuePopup {
    return new CashflowQueryValuePopup(this.page, observedRoot);
  }
  calendar(observedRoot: Locator): CashflowControlScope { return this.scoped(observedRoot); }
}

export class CashflowQueryGroup extends CashflowControlScope {
  readonly header = this.root.locator(':scope > .ruleGroup-header');
  readonly addRuleButton = this.header.locator('.ruleGroup-addRule');
  readonly addGroupButton = this.header.locator('.ruleGroup-addGroup');
  readonly removeButton = this.header.locator('.ruleGroup-remove');
  readonly combinator = this.header.locator('.ruleGroup-combinators');

  ruleAt(index: number): CashflowQueryRule {
    requireIndex(index);
    return new CashflowQueryRule(this.page, this.root.locator(':scope > .ruleGroup-body > .rule').nth(index));
  }

  groupAt(index: number): CashflowQueryGroup {
    requireIndex(index);
    return new CashflowQueryGroup(this.page, this.root.locator(':scope > .ruleGroup-body > .ruleGroup').nth(index));
  }
}

export class CashflowSearchBuilder extends CashflowControlScope {
  readonly newFilterButton = this.testId('new-filter-btn');
  readonly searchFilters = this.placeholder('Search filters');
  readonly filterName = this.label('Filter Name');
  readonly privateCheckbox = this.root.getByRole('checkbox', { name: 'Private', exact: true });
  readonly duplicateButton = this.root.getByTitle('Duplicate this filter', { exact: true });
  readonly deleteButton = this.testId('/advanced_search/preview_dialog/delete_btn');
  readonly saveButton = this.testId('/advanced_search/preview_dialog/save_or_create_btn');
  readonly searchButton = this.testId('/advanced_search/preview_dialog/search_btn');
  readonly query = new CashflowQueryGroup(this.page, this.root.locator('.queryBuilder.ruleGroup, .queryBuilder > .ruleGroup'));

  constructor(page: Page, root = namedDialogRoot(page, 'Custom Search')) {
    super(page, root);
  }

  savedFilter(name: string): Locator {
    // ListItemButton uses a titled child, not a stable record-id attribute.
    return this.root.getByRole('button').filter({ has: this.root.getByTitle(name, { exact: true }) });
  }
}

export class CashflowViewBuilder extends CashflowControlScope {
  readonly searchFields = this.field('searchField');
  readonly viewName = this.field('viewName');
  readonly targetRoles = this.testId('filterNameTargetRoleSelect');
  readonly privateCheckbox = this.root.getByRole('checkbox', { name: 'Is Private', exact: true });
  readonly saveButton = this.testId('customView-save-btn');
  readonly removeButton = this.testId('customView-remove-btn');
  readonly closeButton = this.testId('setBtn');
  readonly availableFields = this.root.locator('.group-data');
  readonly displayedFields = this.root.locator('.result-data');

  constructor(page: Page, root = namedDialogRoot(page, 'View Builder')) {
    super(page, root);
  }

  category(name: string): Locator {
    // Source anchors have no href and therefore no link role.
    return this.root.locator('.group a').filter({ has: this.root.getByText(name, { exact: true }) });
  }

  availableField(fieldId: string, sourceIndex: number): Locator {
    requireIndex(sourceIndex);
    return this.availableFields.locator(`[data-rbd-draggable-id=${cssValue(`${fieldId}-${sourceIndex}`)}]`);
  }

  displayedField(columnId: string): Locator {
    return this.displayedFields.locator(`[data-rbd-draggable-id=${cssValue(columnId)}]`);
  }

  removeFieldButton(columnId: string): Locator {
    return this.displayedField(columnId).getByTitle('Delete', { exact: true });
  }

  showFieldNameButton(fieldId: string, sourceIndex: number): Locator {
    return this.availableField(fieldId, sourceIndex).getByTestId('show-field-name');
  }

  // react-beautiful-dnd supports keyboard lifting and dropping.
  async moveFieldWithKeyboard(field: Locator, direction: 'ArrowLeft' | 'ArrowRight' | 'ArrowUp' | 'ArrowDown', count = 1): Promise<void> {
    requireIndex(count);
    await this.press(field, 'Space');
    for (let step = 0; step < count; step++) await this.press(field, direction);
    await this.press(field, 'Space');
  }
}

function requireIndex(index: number): void {
  if (!Number.isSafeInteger(index) || index < 0) throw new Error('Index must be a nonnegative integer.');
}
