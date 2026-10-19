import React from "react";
import { useContext } from "../../../hooks/provider";
import useServices from "../../../services";
import { getJWTPayload, waitFor } from "../../../utils/common";
import { TimeoutProps } from "./interface";
import { relogin } from "../../../hooks/service";
import useAnalytics from "../../../analytics";
import { AnalyticsData } from "../../../analytics/model";
import useDispatcher from "../../../hooks/dispathcer";
const analyticsData: AnalyticsData = { container: "Base", tile: "Timeout" };

const useController = (props: TimeoutProps) => {
  const [store] = useContext();
  const { dispacthIsOnLogout } = useDispatcher();
  const [loading, setLoading] = React.useState(false);
  const { ButtonEvent, ModalEvent } = useAnalytics();
  const { logout } = useServices();
  const timerPopup = React.useRef<any>(0);
  const clearAllTimeout = () => {
    if (timerPopup.current) {
      clearTimeout(timerPopup.current);
    }
  };

  React.useEffect(() => {
    ModalEvent("open", { name: "session control", ...analyticsData });
  }, []);

  React.useEffect(() => {
    if (!store.refreshToken) {
      return;
    }

    const payload = getJWTPayload(store.refreshToken);
    if (payload != "" && typeof payload.exp !== "undefined") {
      const diff = 1000 * payload.exp - new Date().getTime() - 2000;
      timerPopup.current = setTimeout(() => {
        continuLogout();
      }, diff);
    }

    return () => {
      clearAllTimeout();
    };
  }, [store.refreshToken]);

  const continuLogout = async () => {
    dispacthIsOnLogout(true);
    setLoading(true);
    ButtonEvent("click", { name: "logout", ...analyticsData });
    ModalEvent("close", { name: "session control", ...analyticsData });
    await waitFor(1000);
    await logout();
    clearAllTimeout();
    props.setOpen(false);
  };

  const extend = async () => {
    setLoading(true);
    ButtonEvent("click", { name: "extend", ...analyticsData });
    ModalEvent("close", { name: "session control", ...analyticsData });
    await relogin();
    clearAllTimeout();
    props.setOpen(false);
  };

  return {
    store,
    continuLogout,
    extend,
    clearAllTimeout,
    timerPopup,
    loading,
  };
};

export default useController;
