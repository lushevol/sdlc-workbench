import { Buffer } from "buffer";
import { ActionType, IAction } from "../hooks/reducer/util/ActionType";
import { v4 } from "uuid";
import { getHooksBase } from "../hooks/HooksBase";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import duration from "dayjs/plugin/duration";
import { Entity } from "../hooks/model/root";
import { Workspace, firstWorkspace } from "../hooks/model/workspaces";
import { Tile } from "../components/Drawer/common/interface";
import { findTile } from "./drawer";
import { featureScopedEnabled } from "./featureFlagController";
dayjs.extend(utc);
dayjs.extend(duration);

export const getLocalStorage = (): Storage => {
  const { localStorage } = window;
  return localStorage;
};

export const getWindowOpen = (): Window["open"] => {
  const { open } = window;
  return open;
};

export const getSessionStorage = () => {
  const { sessionStorage } = window;
  return sessionStorage;
};
export interface JWTPayload {
  exp?: number;
  iat?: number;
  entitlements?: string;
  sub?: string;
  date?: unknown;
}
export const getJWTPayload = (token: string): JWTPayload | "" => {
  const payload = token.split(" ");
  if (payload && payload[1]) {
    const tokenParts: string[] = payload[1].split(".");
    return JSON.parse(Buffer.from(tokenParts[1], "base64").toString("utf8"));
  }
  return "";
};

export const storeData = (key: string, data: string): void => {
  getLocalStorage().setItem(key, data);
  getSessionStorage().setItem(key, data);
};

export const clearLocalStorage = (
  dispacth?,
  actionTypes?: ActionType[]
): void => {
  if (actionTypes && actionTypes.length > 0) {
    actionTypes.forEach((actionType) => {
      getLocalStorage().removeItem(actionType);
    });
  } else {
    getLocalStorage().clear();
  }
  getSessionStorage().clear();
  if (dispacth) {
    dispacth({
      type: ActionType.CLEAR,
      data: {},
    });
  }
};

export const clearStorageWhenLogout = (dispacth: React.Dispatch<IAction>) => {
  clearLocalStorage(dispacth, [
    ActionType.SET_TOKEN,
    ActionType.SET_USER,
    ActionType.SET_EXPIRED_TOKEN,
    ActionType.SET_ENTITIES,
  ]);
};

export const uuidv4 = () => {
  return v4();
};

export const showErrorMsg = (errorMsg: string) => {
  const { baseDispatch } = getHooksBase();
  baseDispatch({ type: ActionType.SET_ERRORMSG, data: { errorMsg } });
};

//This function is reported as code smell in Sonar Qube
//please replace all CommonUtil.show_error_msg to CommonUtil.showErrorMsg
export const show_error_msg = (errorMsg: string) => {
  showErrorMsg(errorMsg);
};

export const getHostName = () => {
  const { location } = window;
  const { hostname } = location;
  return hostname;
};

export const getLocation = () => {
  const { location } = window;
  return location;
};

export const getSurveyLink = () => {
  let surveyLink =
    "https://surveys.sc.com/jfe/preview/previewId/b35e7b90-467e-473f-9ff3-8b6a099569d5/SV_cUVyvBdVELMVr02?Q_CHL=preview&Q_SurveyVersionID=current";
  if (["PROD", "PRE-PROD"].includes(getEnv())) {
    surveyLink = "https://surveys.sc.com/jfe/form/SV_cUVyvBdVELMVr02";
  }
  return surveyLink;
};

const DOMAIN_ENV_MAP: Record<string, string> = {
  localhost: "LOCAL",
  "fmo-mfe-dev.uk.dev.net": "DEV",
  "fmo-mfe.uk.dev.net": "UAT",
  "uklvadapp1342.uk.dev.net": "UAT",
  "uklvadapp1344.uk.dev.net": "UAT",
  "uklvadapp1346.uk.dev.net": "UAT",
  "fmo-mfe-fmrp1.pi.dev.net": "UAT",
  "fmo-mfe-fmrp2.pi.dev.net": "UAT",
  "fmo-mfe-preprod.pi.dev.net": "PRE-PROD",
  "ratan-aws-app-fmo-mfe.ir.standardchartered.com": "EKS",
  "ratan-aws-sit-ns4-fmo-mfe.ir.standardchartered.com": "SIT",
};

export const getEnv = () => {
  const hostname = getHostName();
  return DOMAIN_ENV_MAP[hostname] ?? "PROD";
};

export const getSSOLink = () => {
  const enabledEntraSSO = featureScopedEnabled("ENABLE_ENTRA_SSO");

  if (enabledEntraSSO) {
    return getEntraSSOLink();
  } else {
    return getOneMfaSSOLink();
  }
};

export const getOneMfaSSOLink = () => {
  if (["LOCAL", "DEV", "SIT", "EKS"].includes(getEnv())) {
    return "https://test-mfaintig-stg.51318.app.standardchartered.com:443/openam/oauth2/realms/root/realms/sso/authorize?client_id=51358ratan&redirect_uri=https://fmo-mfe-dev.uk.dev.net:8453/mfa/callback&response_type=code";
  } else if (["UAT"].includes(getEnv())) {
    return "https://test-mfaintig-stg.51318.app.standardchartered.com:443/openam/oauth2/realms/root/realms/sso/authorize?client_id=51358ratanuat&redirect_uri=https://fmo-mfe.uk.dev.net:8453/mfa/callback&response_type=code";
  } else {
    return "https://mfaig.global.standardchartered.com/openam/oauth2/realms/root/realms/sso/authorize?client_id=51358ratan&redirect_uri=https://fmo-mfe.gdc.standardchartered.com:8453/mfa/callback&response_type=code";
  }
};

// NON PROD ids
const NON_PROD_TENANT_ID = "cd823f6b-31c5-4241-b504-3707cbc03fb7";
const NON_PROD_CLIENT_ID = "80c8b904-1b64-443b-a651-7548764d534d";

// PROD ids
const PROD_TENANT_ID = "b44900f1-2def-4c3b-9ec6-9020d604e19e";
const PROD_CLIENT_ID = "fd99d1e8-e543-4345-b5f0-208c94ffd39a";

export const getTenantId = () => {
  return getEnv() === "PROD" ? PROD_TENANT_ID : NON_PROD_TENANT_ID;
};

export const getClientId = () => {
  return getEnv() === "PROD" ? PROD_CLIENT_ID : NON_PROD_CLIENT_ID;
};

export const getEntraSSOLink = () => {
  const tenant_id = getTenantId();
  const client_id = getClientId();
  const callback = `${location.origin}/mfa/callback`;
  return `https://login.microsoftonline.com/${tenant_id}/oauth2/v2.0/authorize?client_id=${client_id}&response_type=code&redirect_uri=${callback}&response_mode=query&scope=openid+profile+offline_access+email`;
};

export const isNumber = (val: any) => {
  return (
    val &&
    val !== "" &&
    !isNaN(val as unknown as number) &&
    !isNaN(parseFloat(val)) &&
    isFinite(val)
  );
};

export const isDate = (val: any) => {
  if (isEmpty(val) || (isNumber(val) && val.toString().length !== 13)) {
    return false;
  }

  const result = new Date(val);
  return result instanceof Date && !isNaN(result.valueOf());
};

export const isValidationToFormateDate = (val: any) => {
  const result = new Date(val);
  const regez = /^\d{4}-\d{2}-\d{2}[T|\s]\d{2}:\d{2}:\d{2}/;
  if (
    !isEmpty(val) &&
    result instanceof Date &&
    !isNaN(result.valueOf()) &&
    regez.test(val)
  ) {
    return true;
  }
  return false;
};

// Format time
// Formats that do not need to be converted need to be excluded
// Possible parameter formats:
//   1. 1594006198764 (No conversion is required as may conflict with price)
//   2. 2020-02-02 (No conversion is required)
//   3. 2020-06-17T03:04:13Z
//   4. 2020-06-17 03:04:13
export const formatDate = (time: any, isAccurateToDay: boolean) => {
  if (isValidationToFormateDate(time) || isAccurateToDay) {
    const realTime = isNumber(time) ? parseInt(time) : time;
    let result = "";
    if (isAccurateToDay) {
      result = dayjs(realTime).format("YYYY MMM DD");
    } else {
      result = dayjs(realTime).format("YYYY-MM-DD HH:mm:ss");
    }
    return result !== "Invalid Date" ? result : time;
  }
  return time;
};

export const formatDateToISO = (time: any, isAccurateToDay: boolean) => {
  if (isValidationToFormateDate(time) || isAccurateToDay) {
    let newTime = "";
    try {
      const realTime = isNumber(time) ? parseInt(time) : time;
      if (isAccurateToDay) {
        newTime = dayjs.utc(realTime).format("YYYY MMM DD");
      } else {
        newTime = dayjs.utc(realTime).format();
      }
    } catch (error) {
      newTime = time;
    }

    return newTime;
  }
  return time;
};

export const isEmpty = (value: any) => {
  return (
    value === "" || value === null || value === undefined || value === "null"
  );
};

export const getDate = (date) => (date ? date.format("YYYY MMM DD") : "");

export const validateTile = (
  entities: Entity[] | [] | undefined,
  entity: string | string[] | undefined,
  subject: string | undefined
) => {
  if (entities?.length && entity && subject) {
    const entityIndex = entities.findIndex(
      (item: any) => item.name === entity || entity?.includes(item.name)
    );
    if (entityIndex >= 0) {
      const subjectIndex = entities[entityIndex].subjects.findIndex(
        (item: any) => item.name === subject || item.longName === subject
      );
      if (subjectIndex >= 0) {
        return true;
      }
    }
    /**
     * @author Tech
     * @description  X_RATANONE will release after MENU Contorl so add below code to control entity level
     *  */
    if (entity === "X_RATANONE") {
      const entityIndexEqSubject = entities.findIndex(
        (item: any) => item.name === subject
      );
      if (entityIndexEqSubject >= 0) {
        return true;
      }
    }
  }
  return false;
};

export const validateWorkspace = (workspaces, entities, drawers) => {
  let newWorkspaces = workspaces.reduce((result: any, workspace: Workspace) => {
    if (workspace.containers.length === 0) {
      result.push(workspace);
    } else {
      const tile: Tile = findTile(drawers, workspace);
      if (
        tile?.isTemplate ||
        validateTile(entities, tile?.entity, tile?.subject)
      ) {
        result.push(workspace);
      }
    }
    return result;
  }, []);
  if (newWorkspaces.length === 0) {
    newWorkspaces = [firstWorkspace()];
  }
  return newWorkspaces;
};

export const waitFor = (time = 2000) =>
  new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });

export const aOrb = <T = any, R = any>(a: T, b: R) => {
  return a ?? b;
};
