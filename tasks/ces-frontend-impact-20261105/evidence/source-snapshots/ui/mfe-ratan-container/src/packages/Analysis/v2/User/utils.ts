import { EntitlementsType, SessionUserType } from "./type";
import { Hooks } from "../import";
import { MonitorUser } from "./index";
import { encode } from "../Storage/crypto";
const { getHooks } = Hooks;

const X_RATANONE = "X_RATANONE";

export const getUserId = () => {
  const hooks = getHooks();
  const { id, oud } = (hooks?.store?.user ?? {}) as SessionUserType;
  const { userId } = oud ?? {};

  return userId ?? id ?? "";
};

export const getUserName = () => {
  const hooks = getHooks();
  const { oud } = (hooks?.store?.user ?? {}) as SessionUserType;
  const { firstName, lastName } = oud ?? {};
  return `${firstName} ${lastName}`;
};

export const getUserEmail = () => {
  const hooks = getHooks();
  const { oud } = (hooks?.store?.user ?? {}) as SessionUserType;
  const { emailId } = oud ?? {};
  return emailId ?? "";
};

export const getUserCountry = () => {
  const hooks = getHooks();
  const { oud } = (hooks?.store?.user ?? {}) as SessionUserType;
  const { country } = oud ?? {};
  return country ?? "";
};

export const getUserProfile = () => {
  const hooks = getHooks();
  const { entitlements } = (hooks?.store?.user ?? {}) as SessionUserType;
  return (
    (entitlements ? extractProfileBySubject(entitlements, X_RATANONE) : "") ??
    ""
  );
};

let cachedMonitorUserMap = new Map<string, MonitorUser>();
export const getCachedMonitorUser = () => {
  const userId = getUserId();
  const hasCachedUser = cachedMonitorUserMap.has(userId);
  if (!hasCachedUser) cachedMonitorUserMap.set(userId, new MonitorUser());
  return cachedMonitorUserMap.get(userId) as MonitorUser;
};

export const getTimeZone = () => {
  return Intl.DateTimeFormat().resolvedOptions().timeZone;
};

export const getTimeZoneOffset = () => {
  return new Date().getTimezoneOffset() / 60 + "";
};

export const getUserAgent = () => {
  return navigator.userAgent;
};

export const getLanguage = () => {
  return navigator.language;
};

export const extractProfileBySubject = (
  entitlements: EntitlementsType,
  subject: string
) => {
  const name = Object.keys(entitlements).find((k) => k.includes(subject));
  if (name) return name.split(":")[1];
  else return name;
};

export const getBrowserFingerprint = () => {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  if (ctx) {
    ctx.font = "14px Arial";
    ctx.fillStyle = "#ccc";
    ctx.fillText("hello, ratanone", 2, 2);
  }
  return window.btoa(canvas.toDataURL("image/jpeg"));
};

export const getUID = () => {
  const id = getUserId();
  return encode(id);
};
