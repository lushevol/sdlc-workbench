import { featureScopedEnabledFactor } from "./featureFlagController";

import { getEnv } from "./common";
jest.mock("./common", () => {
  const actual = jest.requireActual("./common");
  return {
    ...actual,
    getEnv: jest.fn(() => "local"),
    getLocalStorage: () => ({
      setItem: (v) => { },
      getItem: () => undefined,
      clear: () => { }
    }),
    uuidv4: () => "id",
  };
});


describe("pilot feature flag controller", () => {
  beforeEach(() => {
    // Reset URL query parameters
    delete (window as any).location;
    (window as any).location = { search: "" };
    localStorage.clear();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

   // ==================== URL search params priority ====================
  describe("URL search params priority", () => {
    it("should return true when URL param is 'true'", () => {
      (window as any).location = { search: "?ENABLE_ENTRA_SSO=true" };
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: false, dev: false, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(true);
    });

    it("should return true when URL param is '1'", () => {
      (window as any).location = { search: "?ENABLE_ENTRA_SSO=1" };
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: false, dev: false, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(true);
    });

    it("should return true when URL param is 'yes'", () => {
      (window as any).location = { search: "?ENABLE_ENTRA_SSO=yes" };
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: false, dev: false, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(true);
    });

    it("should return true when URL param is 'y'", () => {
      (window as any).location = { search: "?ENABLE_ENTRA_SSO=y" };
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: false, dev: false, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(true);
    });

    it("should return false when URL param is 'false'", () => {
      (window as any).location = { search: "?ENABLE_ENTRA_SSO=false" };
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: true, "pre-prod": true, prod: true },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });

    it("should return false when URL param is '0'", () => {
      (window as any).location = { search: "?ENABLE_ENTRA_SSO=0" };
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: true, "pre-prod": true, prod: true },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });
  });

   // ==================== configuration file ====================
  describe("feature config", () => {
    it("should return false when feature flag does not exist in config", () => {
      const featureFlagEnabled = featureScopedEnabledFactor<"ENABLE_ENTRA_SSO">({});
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });

    it("should return true when local env is true", () => {
      (getEnv as jest.Mock).mockReturnValue("local");
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(true);
    });

    it("should return false when uat env is false", () => {
      (getEnv as jest.Mock).mockReturnValue("uat");
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });

    it("should return false when pre-prod env is false", () => {
      (getEnv as jest.Mock).mockReturnValue("pre-prod");
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });

    it("should return false when prod env is false", () => {
      (getEnv as jest.Mock).mockReturnValue("prod");
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });

    it("should return false when env is not in config", () => {
      (getEnv as jest.Mock).mockReturnValue("unknown-env");
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: true, dev: true, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(false);
    });

    it("should return true when env is in config and enabled", () => {
      (getEnv as jest.Mock).mockReturnValue("dev");
      const featureFlagEnabled = featureScopedEnabledFactor({
        ENABLE_ENTRA_SSO: { local: false, dev: true, uat: false, "pre-prod": false, prod: false },
      });
      expect(featureFlagEnabled("ENABLE_ENTRA_SSO")).toBe(true);
    });
  });
});