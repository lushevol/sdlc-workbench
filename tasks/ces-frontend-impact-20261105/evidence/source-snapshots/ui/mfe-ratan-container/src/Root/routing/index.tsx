import React, { ReactElement, Suspense } from "react";
import { ReactRouterDom, Splash } from "../import";
import { APPLICATION_MENU, ContainerProps } from "./common/interface";
const { Routes, Route } = ReactRouterDom;
import useController from "./common/useController";
import TradeBlotter from "../import/TradeBlotter";
import CashflowBlotter from "../import/CashFlow";
import CashflowBlotterCN from "../import/CashFlowCN";
import Exception from "../import/Exception";
import Rule from "../import/Rule";
import AuthorizationLimits from "../import/AuthorizationLimits";
import NostroStatic from "../import/NostroStatic";
const Routing: React.FC<ContainerProps> = (
  props: ContainerProps
): ReactElement => {
  useController(props);
  return (
    <Suspense fallback={<Splash />}>
      <Routes>
        <Route
          path={APPLICATION_MENU.TRADE_BLOTTER}
          element={<TradeBlotter {...props} />}
        ></Route>
        <Route
          path={APPLICATION_MENU.CASHFLOW_BLOTTER}
          element={<CashflowBlotter {...props} />}
        ></Route>
        <Route
          path={APPLICATION_MENU.CASHFLOW_BLOTTER_CN}
          element={<CashflowBlotterCN {...props} />}
        ></Route>
        <Route
          path={APPLICATION_MENU.EXCEPTIONS_BLOTTER}
          element={<Exception {...props} />}
        ></Route>
        <Route
          path={APPLICATION_MENU.RULES_BLOTTER}
          element={<Rule {...props} />}
        ></Route>
        <Route
          path={APPLICATION_MENU.AUTHORIZATION_LIMITS_CONTAINER}
          element={<AuthorizationLimits {...props} />}
        ></Route>
        <Route
          path={APPLICATION_MENU.NOSTRO_STATIC_CONTAINER}
          element={<NostroStatic {...props} />}
        ></Route>
        <Route path="*" element={<></>}></Route>
      </Routes>
    </Suspense>
  );
};

export default Routing;
