// The original XRATANONE test spies on this mocked store boundary.
// Other focused tests provide their own Hooks factory and store fixtures.
const path = require("path");
jest.mock(path.resolve(__dirname, "../../../repos/ui/mfe-ratan-container/src/Root/import"), () => ({
  Hooks: { getHooks: jest.fn(() => ({ store: {} })) },
}));

// Entitlement decision logging is a separate HTTP boundary from permission evaluation.
jest.mock(path.resolve(__dirname, "../../../repos/ui/mfe-ratan-container/src/ratanutils/logger"), () => ({
  logger: { info: jest.fn() },
}));
