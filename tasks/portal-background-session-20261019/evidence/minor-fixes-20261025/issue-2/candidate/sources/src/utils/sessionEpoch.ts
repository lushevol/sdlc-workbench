let epoch = 0;

export interface SessionRequestConfig {
  url?: string;
  sessionEpoch?: number;
}

export const currentSessionEpoch = () => epoch;

export const invalidateSession = () => {
  epoch += 1;
};

export const isFreshLogin = (url = "") =>
  /\/auth\/v[23]\/sso\/login(?:[?#]|$)/.test(url);

export const isStaleSessionRequest = (config?: SessionRequestConfig) =>
  typeof config?.sessionEpoch === "number" && config.sessionEpoch !== epoch;
