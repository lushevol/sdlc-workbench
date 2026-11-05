import { CommonUtil } from "../../Root/import";
import { getUser } from "../../ratanutils/authenticator";

type Env = "local" | "dev" | "uat" | "pre-prod" | "prod" | "sit";

// env:
// if no env present, then feature is enable for all. Recommend to remove it as it's always return true.
// env allows single Env or multiple, e.g. "dev, uat, prod"
// NOT ALLOW to conflict with each other, otherwise will failed
// users:
// entitlements:
// if users and entitlements are both present, then have to match them both.
// if either one present, then have to match the one.
// if neither present, then feature is enable for all entitlements and all users.
type PilotFeaturesType<T extends string> = {
  [feature in T]?: {
    [env in Env]:
      | boolean
      | {
          users?: string[];
          entitlements?: string[];
        };
  };
};

const cachedFeatureFlagMap = new Map<string, boolean>();

export const featureScopedEnabledFactor = <T extends string>(
  PilotFeatures: PilotFeaturesType<T>
) => {
  cachedFeatureFlagMap.clear();
  return (f: T): boolean => {
    if (cachedFeatureFlagMap.has(f)) return cachedFeatureFlagMap.get(f)!;
    const hasFeatureFlag = Object.keys(PilotFeatures).includes(f);
    if (!hasFeatureFlag) {
      cachedFeatureFlagMap.set(f, false);
      return false;
    }
    const featureConfig = PilotFeatures[f];
    // feature: {} means enable all
    if (!Object.keys(featureConfig!).length) {
      cachedFeatureFlagMap.set(f, true);
      return true;
    }
    const curUser = getUser();
    const curEnv = CommonUtil.getEnv()?.toLowerCase();
    const settingsOfCurrentEnv = featureConfig![curEnv];
    if (typeof settingsOfCurrentEnv === "boolean") {
      cachedFeatureFlagMap.set(f, settingsOfCurrentEnv);
      return settingsOfCurrentEnv;
    }
    const { users, entitlements } = settingsOfCurrentEnv || {};
    const userPassed = users?.length ? users.includes(curUser.id) : true;
    const entitlementPassed = entitlements?.length
      ? entitlements.every((et) => curUser.entitlements.includes(et))
      : true;
    const enabled = userPassed && entitlementPassed;
    cachedFeatureFlagMap.set(f, enabled);
    return enabled;
  };
};
