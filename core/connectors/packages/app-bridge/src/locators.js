/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { By, locateWith } from 'selenium-webdriver';
import { z } from 'zod';

/** Simple (non-relative) Selenium locator strategies. */
export const SIMPLE_STRATEGIES = ['id', 'css', 'xpath', 'name', 'className', 'tagName', 'linkText', 'partialLinkText'];

/** Selenium 4 relative locator spatial relations. */
export const RELATIONS = [
  'above',
  'below',
  'toLeftOf',
  'toRightOf',
  'straightAbove',
  'straightBelow',
  'straightToLeftOf',
  'straightToRightOf',
  'near'
];

/** Anchor locator used as the reference element for a relative locator. Always simple (non-relative). */
const anchorSchema = z.object({
  using: z.enum(SIMPLE_STRATEGIES).describe('Locator strategy for the anchor element'),
  value: z.string().min(1).describe('Locator value for the anchor element')
});

/**
 * Shared locator schema used by every app-bridge tool that targets an element.
 * Supports all standard Selenium locator strategies plus Selenium 4 relative locators
 * (using: "relative" + relation + anchor). Used consistently across all tools so a single
 * mental model covers every capability.
 */
export const locatorSchema = z
  .object({
    using: z
      .enum([...SIMPLE_STRATEGIES, 'relative'])
      .describe('Locator strategy. Use "relative" together with relation/anchor for Selenium 4 relative locators.'),
    value: z
      .string()
      .min(1)
      .describe('Locator value. For "relative", the base tag name or CSS selector of the elements being searched for.'),
    relativeStrategy: z
      .enum(['css', 'tagName'])
      .optional()
      .describe('How to interpret "value" when using is "relative" (default: css)'),
    relation: z.enum(RELATIONS).optional().describe('Required when using is "relative" — spatial relation to the anchor'),
    anchor: anchorSchema
      .optional()
      .describe('Required when using is "relative" — the reference element the relation is measured against'),
    index: z
      .number()
      .int()
      .nonnegative()
      .optional()
      .default(0)
      .describe('0-based index to disambiguate when the locator matches multiple elements')
  })
  .superRefine((data, ctx) => {
    if (data.using === 'relative') {
      if (!data.relation) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: 'relation is required when using is "relative"', path: ['relation'] });
      }
      if (!data.anchor) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: 'anchor is required when using is "relative"', path: ['anchor'] });
      }
    }
  });

/**
 * Build a simple (non-relative) Selenium By locator.
 * @param {string} using
 * @param {string} value
 * @returns {import('selenium-webdriver').By}
 */
function simpleBy(using, value) {
  switch (using) {
    case 'id':
      return By.id(value);
    case 'css':
      return By.css(value);
    case 'xpath':
      return By.xpath(value);
    case 'name':
      return By.name(value);
    case 'className':
      return By.className(value);
    case 'tagName':
      return By.tagName(value);
    case 'linkText':
      return By.linkText(value);
    case 'partialLinkText':
      return By.partialLinkText(value);
    default:
      throw new Error(`Unsupported locator strategy "${using}"`);
  }
}

/**
 * Resolve a validated locator object into a Selenium By/RelativeBy instance usable with
 * driver.findElement()/findElements().
 * @param {Object} locator - A locator object matching locatorSchema.
 * @returns {import('selenium-webdriver').By}
 */
export function resolveBy(locator) {
  if (locator.using !== 'relative') {
    return simpleBy(locator.using, locator.value);
  }

  const base = locateWith(simpleBy(locator.relativeStrategy || 'css', locator.value));
  const anchorBy = simpleBy(locator.anchor.using, locator.anchor.value);

  switch (locator.relation) {
    case 'above':
      return base.above(anchorBy);
    case 'below':
      return base.below(anchorBy);
    case 'toLeftOf':
      return base.toLeftOf(anchorBy);
    case 'toRightOf':
      return base.toRightOf(anchorBy);
    case 'straightAbove':
      return base.straightAbove(anchorBy);
    case 'straightBelow':
      return base.straightBelow(anchorBy);
    case 'straightToLeftOf':
      return base.straightToLeftOf(anchorBy);
    case 'straightToRightOf':
      return base.straightToRightOf(anchorBy);
    case 'near':
      return base.near(anchorBy);
    default:
      throw new Error(`Unsupported relation "${locator.relation}"`);
  }
}

/**
 * Build a short, human-readable description of a locator for error messages.
 * @param {Object} locator
 * @returns {string}
 */
export function describeLocator(locator) {
  if (locator.using === 'relative') {
    return `relative(${locator.relativeStrategy || 'css'}="${locator.value}" ${locator.relation} anchor[${locator.anchor.using}="${locator.anchor.value}"])`;
  }
  return `${locator.using}="${locator.value}"`;
}

/**
 * Find all elements matching a locator.
 * @param {import('selenium-webdriver').WebDriver} driver
 * @param {Object} locator
 * @returns {Promise<import('selenium-webdriver').WebElement[]>}
 */
export async function findAll(driver, locator) {
  return driver.findElements(resolveBy(locator));
}

/**
 * Find a single element matching a locator, disambiguating multiple matches via locator.index.
 * Throws a clear error if no element matches or the index is out of range.
 * @param {import('selenium-webdriver').WebDriver} driver
 * @param {Object} locator
 * @returns {Promise<import('selenium-webdriver').WebElement>}
 */
export async function findOne(driver, locator) {
  const elements = await findAll(driver, locator);
  const index = locator.index ?? 0;

  if (elements.length === 0) {
    throw new Error(`No element found for locator ${describeLocator(locator)}`);
  }
  if (index >= elements.length) {
    throw new Error(
      `Locator ${describeLocator(locator)} matched ${elements.length} element(s); index ${index} is out of range`
    );
  }
  return elements[index];
}
