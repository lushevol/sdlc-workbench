import { getHooksBase } from "../../HooksBase";
import { ActionType } from "../../reducer/util/ActionType";
import {
  currentSessionEpoch,
  isStaleSessionRequest,
  SessionRequestConfig,
} from "../../../utils/sessionEpoch";

const pending = new Set<SessionRequestConfig>();
let epoch = currentSessionEpoch();

const synchronizeSession = () => {
  const current = currentSessionEpoch();
  if (epoch !== current) {
    pending.clear();
    epoch = current;
  }
};

const publishLoading = () => {
  getHooksBase().baseDispatch({
    type: ActionType.SET_IS_LOADING,
    data: { isLoading: pending.size > 0 },
  });
};

export const startRequestLoading = (
  request: SessionRequestConfig,
  showLoading: boolean
) => {
  synchronizeSession();
  if (showLoading) pending.add(request);
  publishLoading();
};

export const finishRequestLoading = (request?: SessionRequestConfig) => {
  synchronizeSession();
  if (isStaleSessionRequest(request)) return;
  if (request) pending.delete(request);
  publishLoading();
};
