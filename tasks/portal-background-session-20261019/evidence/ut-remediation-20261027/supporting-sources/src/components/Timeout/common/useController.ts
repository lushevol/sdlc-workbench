import React from "react";
import { useContext } from "../../../hooks/provider";
import useServices from "../../../services";
import { getJWTPayload, waitFor } from "../../../utils/common";
import { TimeoutProps } from "./interface";
import {
  getPendingRefreshToken,
  relogin,
  signal,
} from "../../../hooks/service";
import {
  currentSessionEpoch,
  invalidateSession,
} from "../../../utils/sessionEpoch";
import useAnalytics from "../../../analytics";
import { AnalyticsData } from "../../../analytics/model";
import useDispatcher from "../../../hooks/dispathcer";
const analyticsData: AnalyticsData = { container: "Base", tile: "Timeout" };

const useController = (props: TimeoutProps) => {
  const [store] = useContext();
  const { dispacthIsOnLogout } = useDispatcher();
  const [loading, setLoading] = React.useState(false);
  const [sessionEpoch] = React.useState(currentSessionEpoch);
  const [pendingAtMount] = React.useState(() => getPendingRefreshToken());
  const [waitingForRefresh, setWaitingForRefresh] = React.useState(
    Boolean(pendingAtMount)
  );
  const { ButtonEvent, ModalEvent } = useAnalytics();
  const { logout } = useServices();
  const timerPopup = React.useRef<any>(0);
  const mounted = React.useRef(true);
  const logoutStarted = React.useRef(false);
  const renewalPending = React.useRef(false);
  const clearAllTimeout = () => {
    clearTimeout(timerPopup.current);
    timerPopup.current = 0;
  };

  React.useEffect(() => {
    mounted.current = true;
    ModalEvent("open", { name: "session control", ...analyticsData });
    return () => {
      mounted.current = false;
      clearAllTimeout();
    };
  }, []);

  React.useEffect(() => {
    let active = true;
    const settled = () => {
      if (active && sessionEpoch === currentSessionEpoch()) {
        setWaitingForRefresh(false);
      }
    };
    pendingAtMount?.then(settled, settled);
    return () => {
      active = false;
    };
  }, [pendingAtMount, sessionEpoch]);

  const refreshExpiresAt = React.useMemo(() => {
    try {
      const payload = store.refreshToken
        ? getJWTPayload(store.refreshToken)
        : "";
      return payload &&
        typeof payload.exp === "number" &&
        Number.isFinite(payload.exp * 1000)
        ? payload.exp * 1000
        : 0;
    } catch {
      return 0;
    }
  }, [store.refreshToken]);
  const recoveryDeadline = refreshExpiresAt - 2000;

  React.useEffect(() => {
    clearAllTimeout();
    if (
      waitingForRefresh ||
      loading ||
      store.isOnLogout ||
      logoutStarted.current ||
      sessionEpoch !== currentSessionEpoch()
    )
      return;
    const remaining = recoveryDeadline - Date.now();
    if (remaining <= 0) {
      void continuLogout();
      return;
    }
    timerPopup.current = setTimeout(() => void continuLogout(), remaining);
    return clearAllTimeout;
  }, [
    recoveryDeadline,
    waitingForRefresh,
    loading,
    store.isOnLogout,
    sessionEpoch,
  ]);

  const canExtend =
    !waitingForRefresh &&
    !store.isOnLogout &&
    !logoutStarted.current &&
    sessionEpoch === currentSessionEpoch() &&
    recoveryDeadline > Date.now();

  const continuLogout = async () => {
    if (logoutStarted.current || sessionEpoch !== currentSessionEpoch()) return;
    logoutStarted.current = true;
    invalidateSession();
    const logoutEpoch = currentSessionEpoch();
    signal.getRefreshToken?.abort();
    signal.relogin?.abort();
    clearAllTimeout();
    dispacthIsOnLogout(true);
    setLoading(true);
    ButtonEvent("click", { name: "logout", ...analyticsData });
    ModalEvent("close", { name: "session control", ...analyticsData });
    await waitFor(1000);
    if (logoutEpoch !== currentSessionEpoch()) return;
    logout();
    if (mounted.current) props.setOpen(false);
  };

  const extend = async () => {
    if (renewalPending.current || !canExtend || recoveryDeadline <= Date.now())
      return;
    renewalPending.current = true;
    clearAllTimeout();
    setLoading(true);
    ButtonEvent("click", { name: "extend", ...analyticsData });
    try {
      await relogin();
      if (
        !mounted.current ||
        sessionEpoch !== currentSessionEpoch() ||
        logoutStarted.current
      )
        return;
      ModalEvent("close", { name: "session control", ...analyticsData });
      props.setOpen(false);
    } catch {
      // The service reports the failure. Keep usable recovery available.
    } finally {
      if (mounted.current && sessionEpoch === currentSessionEpoch()) {
        renewalPending.current = false;
        setLoading(false);
      }
    }
  };

  return {
    store,
    continuLogout,
    extend,
    clearAllTimeout,
    timerPopup,
    loading,
    canExtend,
  };
};

export default useController;
