import axios, { AxiosRequestConfig } from "axios";
import { errorHandler } from "./util/error.response.handler";
import { successHandler } from "./util/succes.response.handler";
import { requestHandler } from "./util/success.request.handler";

export const config: AxiosRequestConfig = {
  headers: {
    "Content-Type": "application/json",
    "Cache-Control": "no-store",
    "X-XSS-Protection": "1;mode:block",
    "X-Content-Type-Options": "nosniff",
    Accept: "application/json, text/plain",
    // "Frontend-Version": "mfe",
  },
  timeout: 60000,
};
const service = axios.create(config);
service.interceptors.request.use(requestHandler);
service.interceptors.response.use(successHandler, errorHandler);

export default service;
