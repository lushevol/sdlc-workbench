import { describe, it, expect } from 'vitest';
import { By } from 'selenium-webdriver';
import { locatorSchema, resolveBy, describeLocator, findAll, findOne, SIMPLE_STRATEGIES, RELATIONS } from '../src/locators.js';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

describe('locatorSchema', () => {
  it('accepts every simple locator strategy', () => {
    for (const using of SIMPLE_STRATEGIES) {
      const result = locatorSchema.safeParse({ using, value: 'x' });
      expect(result.success).toBe(true);
    }
  });

  it('applies a default index of 0', () => {
    const result = locatorSchema.parse({ using: 'id', value: 'foo' });
    expect(result.index).toBe(0);
  });

  it('rejects an empty value', () => {
    const result = locatorSchema.safeParse({ using: 'id', value: '' });
    expect(result.success).toBe(false);
  });

  it('rejects a relative locator missing relation', () => {
    const result = locatorSchema.safeParse({
      using: 'relative',
      value: 'input',
      anchor: { using: 'id', value: 'x' }
    });
    expect(result.success).toBe(false);
  });

  it('rejects a relative locator missing anchor', () => {
    const result = locatorSchema.safeParse({ using: 'relative', value: 'input', relation: 'below' });
    expect(result.success).toBe(false);
  });

  it('accepts a valid relative locator', () => {
    const result = locatorSchema.safeParse({
      using: 'relative',
      value: 'input',
      relation: 'below',
      anchor: { using: 'id', value: 'email' }
    });
    expect(result.success).toBe(true);
  });
});

describe('resolveBy', () => {
  it.each(SIMPLE_STRATEGIES)('resolves the "%s" simple locator strategy', (using) => {
    const by = resolveBy({ using, value: 'x' });
    expect(by).toBeInstanceOf(By);
  });

  it('throws for an unsupported simple strategy', () => {
    expect(() => resolveBy({ using: 'bogus', value: 'x' })).toThrow(/Unsupported locator strategy/);
  });

  it.each(RELATIONS)('resolves a relative locator with relation "%s"', (relation) => {
    const by = resolveBy({ using: 'relative', value: 'input', relation, anchor: { using: 'id', value: 'email' } });
    expect(by).toBeDefined();
  });

  it('throws for an unsupported relation', () => {
    expect(() =>
      resolveBy({ using: 'relative', value: 'input', relation: 'bogus', anchor: { using: 'id', value: 'x' } })
    ).toThrow(/Unsupported relation/);
  });

  it('defaults relativeStrategy to css', () => {
    const by = resolveBy({ using: 'relative', value: 'input', relation: 'above', anchor: { using: 'id', value: 'x' } });
    expect(by).toBeDefined();
  });

  it('supports relativeStrategy tagName', () => {
    const by = resolveBy({
      using: 'relative',
      value: 'input',
      relativeStrategy: 'tagName',
      relation: 'above',
      anchor: { using: 'id', value: 'x' }
    });
    expect(by).toBeDefined();
  });
});

describe('describeLocator', () => {
  it('describes a simple locator', () => {
    expect(describeLocator({ using: 'css', value: '#a' })).toBe('css="#a"');
  });

  it('describes a relative locator', () => {
    const desc = describeLocator({
      using: 'relative',
      value: 'input',
      relation: 'below',
      anchor: { using: 'id', value: 'email' }
    });
    expect(desc).toBe('relative(css="input" below anchor[id="email"])');
  });
});

describe('findAll / findOne', () => {
  it('findAll delegates to driver.findElements with the resolved By', async () => {
    const element = createMockElement();
    const driver = createMockDriver({ findElements: resolvedWith([element]) });
    const result = await findAll(driver, { using: 'id', value: 'x', index: 0 });
    expect(result).toEqual([element]);
  });

  it('findOne returns the element at the given index', async () => {
    const el0 = createMockElement();
    const el1 = createMockElement();
    const driver = createMockDriver({ findElements: resolvedWith([el0, el1]) });
    const result = await findOne(driver, { using: 'id', value: 'x', index: 1 });
    expect(result).toBe(el1);
  });

  it('findOne defaults to index 0', async () => {
    const el0 = createMockElement();
    const driver = createMockDriver({ findElements: resolvedWith([el0]) });
    const result = await findOne(driver, { using: 'id', value: 'x' });
    expect(result).toBe(el0);
  });

  it('findOne throws when no elements match', async () => {
    const driver = createMockDriver({ findElements: resolvedWith([]) });
    await expect(findOne(driver, { using: 'id', value: 'x', index: 0 })).rejects.toThrow(/No element found/);
  });

  it('findOne throws when the index is out of range', async () => {
    const driver = createMockDriver({ findElements: resolvedWith([createMockElement()]) });
    await expect(findOne(driver, { using: 'id', value: 'x', index: 5 })).rejects.toThrow(/out of range/);
  });
});

/** Small helper to build a resolved-promise stub. */
function resolvedWith(value) {
  return () => Promise.resolve(value);
}
