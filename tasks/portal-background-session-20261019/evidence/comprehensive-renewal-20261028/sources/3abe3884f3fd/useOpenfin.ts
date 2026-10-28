import React from "react";
import * as fdc3 from "fdc3-2.1";
import * as openFinFdc3 from "openfin-fdc3";
import useDispatcher from "../../../hooks/dispathcer";
import { getEnv, getLocalStorage } from "../../../utils/common";
import { fdc3InitUtil } from "./util";

const CASHFLOW_CONTEXT_TYPE = "scb.fmptp.cashflows";
const TRADE_CONTEXT_TYPE = "scb.fmptp.trade.query";
const GENERAL_CONTEXT_TYPE = "scb.fmptp.general.parameters";
const TRADE_ID_FIELD = "Trade_Id";
const EQUALS_OPERATOR = "EQ";
const CASHFLOW_TILE_NAME = "cashflow_cn";
const TRADE_TILE_NAME = "trade";
const VIEW_LAUNCH_INTENT = "scb.ViewLaunch";

const openfinFdc3 = window.fdc3 || openFinFdc3;

export const waitTillLogin = (): Promise<boolean> =>
  new Promise((resolve) => {
    const getToken = () => {
      const ls = getLocalStorage();
      const token = ls.getItem("SET_TOKEN");
      return token;
    };

    if (getToken()) {
      resolve(true);
      return;
    }

    let count = 60 * 5; // timeout 5min
    const t = setInterval(() => {
      count--;
      if (getToken()) {
        resolve(true);
        clearInterval(t);
      }
      if (count < 0) {
        resolve(false);
        clearInterval(t);
      }
    }, 1000);
  });

const useOpenfin = () => {
  const { dispatchOpenTile } = useDispatcher();
  const [channelMessage, setChannelMessage] = React.useState<any>();
  const [intentListener, setIntentListener] = React.useState<any>();
  const handleExternalIntentListener = React.useCallback(
    (context: fdc3.Context) => {
      waitTillLogin().then((logined) => {
        if (logined) {
          if (context.type === CASHFLOW_CONTEXT_TYPE) {
            const search: {
              filters: { field: string; operator: string; values: any }[];
            } = {
              filters: [],
            };
            if (context.id?.tradeId) {
              search.filters.push({
                field: TRADE_ID_FIELD,
                operator: EQUALS_OPERATOR,
                values: context.id.tradeId,
              });
            } else if (context.filters) {
              search.filters = context.filters;
            }
            if (search.filters.length > 0) {
              dispatchOpenTile(search, CASHFLOW_TILE_NAME);
            }
          } else if (context.type === TRADE_CONTEXT_TYPE) {
            if (context.id?.tradeId) {
              const search = {
                intent: "ViewTradeDetails",
                context: {
                  tradeId: context.id.tradeId,
                },
              };
              dispatchOpenTile(search, TRADE_TILE_NAME);
            } else if (context.filters?.length) {
              const search = {
                intent: "SearchTrades",
                context: {
                  filters: context.filters,
                },
              };
              dispatchOpenTile(search, TRADE_TILE_NAME);
            }
          } else if (context.type === GENERAL_CONTEXT_TYPE) {
            dispatchOpenTile(context.parameters, context.target);
          }
        }
      });
    },
    []
  );

  const fdc3Init = React.useCallback(async () => {
    const intent = await openfinFdc3?.addIntentListener(
      VIEW_LAUNCH_INTENT,
      handleExternalIntentListener
    );

    setIntentListener(intent);
  }, [fdc3, openfinFdc3]);
  const clearListener = React.useCallback(() => {
    intentListener?.unsubscribe();
  }, [intentListener]);
  React.useEffect(() => {
    fdc3InitUtil(window.fin, fdc3, openfinFdc3, getEnv(), fdc3Init);
    return clearListener;
  }, []);
  const clearMessage = React.useCallback(
    () => setChannelMessage(undefined),
    [channelMessage]
  );
  return {
    channelMessage,
    clearMessage,
    fdc3Init,
    clearListener,
    setChannelMessage,
  };
};

export default useOpenfin;
