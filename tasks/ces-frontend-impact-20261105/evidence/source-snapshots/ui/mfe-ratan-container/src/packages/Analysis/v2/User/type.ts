export interface OUD {
  userId?: string;
  emailId?: string;
  firstName?: string;
  lastName?: string;
  country?: string;
  fullName?: string;
  description?: string;
  title?: string;
  cn?: string;
}

export interface SessionUserType {
  sub?: string;
  id?: string;
  name?: string;
  userId?: string;
  emailId?: string;
  entitlements?: EntitlementsType;
  firstName?: string;
  lastName?: string;
  country?: string;
  fullName?: string;
  oud?: OUD;
  auth_time?: number;
}

export type EntitlementsType = Record<string, Record<string, string[]>>;
