import { vi } from 'vitest';

// Stub process.exit to prevent unhandled rejection errors during tests
// This is needed because src/index.js calls process.exit(1) on errors
// and gets imported by config tests
const originalExit = process.exit;
process.exit = vi.fn((code) => {
  // Don't actually exit during tests
  // But keep the original behavior available if needed
  if (process.env.NODE_ENV !== 'test') {
    originalExit(code);
  }
});
