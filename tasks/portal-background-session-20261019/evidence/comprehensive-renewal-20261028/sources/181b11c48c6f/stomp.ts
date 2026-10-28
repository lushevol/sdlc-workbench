import { CommonUtil } from "Import/index";
import { logger } from "Import/ratanutils";
import _get from "lodash/get";
import _set from "lodash/set";
import SockJS from "sockjs-client";
import Stomp, { Client, Frame, Message, Subscription } from "stompjs";

import { CASHFLOW_NOTIFICATION_SUBSCRIPTIONS } from "../../../services";

const getRatanToken = () => {
  const { getLocalStorage } = CommonUtil;
  return getLocalStorage().getItem("SET_TOKEN");
};
interface ISocketClientConnectStatus {
  reConnetctTime: number;
  updateTime: number;
}

interface ISocketClient {
  client: Client;
  status: ISocketClientConnectStatus;
  subscriptions: Map<string, Subscription>;
  destoryClient: () => void;
}

export const socketClientStore = new Map<string, ISocketClient>();

export const getUid = (url: string, id: string) => `${url}@${id}`;

export function socketClientFactory(url: string, id: string): ISocketClient {
  const uid = getUid(url, id);
  const socketClientExisted = socketClientStore.get(uid);

  if (socketClientExisted) {
    return socketClientExisted;
  } else {
    const client = Stomp.over(new SockJS(url, undefined, { timeout: 1000 }));
    client.heartbeat.outgoing = 3000;
    client.heartbeat.incoming = 25000;
    const socketClientNew = {
      client,
      status: {
        reConnetctTime: 0,
        updateTime: Date.now(),
      },
      subscriptions: new Map(),
      destoryClient: () => {
        try {
          client.disconnect(() => {
            socketClientStore.delete(uid);
          });
        } catch (error) {
          socketClientStore.delete(uid);
        }
      },
    };
    socketClientStore.set(uid, socketClientNew);
    return socketClientNew;
  }
}

export const updateSocketClientReconnetctTime = (
  uid: string,
  reConnetctTime: number
) => {
  const socketClientExisted = socketClientStore.get(uid);
  if (socketClientExisted) {
    _set(socketClientExisted, "status.reConnetctTime", reConnetctTime);
    _set(socketClientExisted, "status.updateTime", Date.now());
  }
};

export const getSocketClientConnectStatus = (uid: string) => {
  const socketClientExisted = socketClientStore.get(uid);
  return _get(socketClientExisted, "status");
};

export const subscribeSocketNotification = (props: {
  url: string;
  id: string;
  topic?: {
    destination: string;
    callback: (message: Record<string, object>) => void;
  };
  onConnected?: (frame: Frame | undefined) => void;
  onError?: (frame: Frame | string, cb: () => void) => void;
}) => {
  const { url, id = "", topic, onConnected, onError } = props;
  const uid = getUid(url, id);
  const { client, subscriptions, destoryClient } = socketClientFactory(url, id);
  const token = getRatanToken() || "";
  const header = {
    "Single-UI-Authorization": token,
  };
  client.connect(
    header,
    (frame) => {
      if (topic) {
        const subsciptionExisted = subscriptions.get(topic.destination);
        if (subsciptionExisted) subsciptionExisted.unsubscribe();
        const subscription = client.subscribe(
          topic.destination,
          (message: Message) => {
            topic.callback(JSON.parse(message.body));
            message.ack();
          }
        );
        subscriptions.set(topic.destination, subscription);
      }
      const status = getSocketClientConnectStatus(uid);
      if (status) {
        if (status.reConnetctTime <= 5) {
          updateSocketClientReconnetctTime(uid, 0);
        }
      }
      onConnected?.(frame);
    },
    (frame) => {
      const status = getSocketClientConnectStatus(uid);
      if (status) {
        const { reConnetctTime } = status;
        destoryClient();
        if (reConnetctTime < 5) {
          setTimeout(() => {
            subscribeSocketNotification(props);
            updateSocketClientReconnetctTime(uid, reConnetctTime + 1);
          }, reConnetctTime * 1000);
        } else {
          const errorMessage = `Message: Websocket Error, Path: ${url}`;
          logger.warn(errorMessage);

          const reconnect = () => {
            subscribeSocketNotification(props);
            updateSocketClientReconnetctTime(uid, 0);
          };
          onError?.(frame, reconnect);
        }
      }
    }
  );
  return destoryClient;
};

export const subscribeCashflowNotification = (
  topic: string,
  id: string,
  callback: (message: Record<string, object>) => void,
  onConnected: (frame: Frame | undefined) => void,
  onError: (frame: Frame | string, cb: () => void) => void
) => {
  const url = CASHFLOW_NOTIFICATION_SUBSCRIPTIONS;
  return subscribeSocketNotification({
    url,
    id,
    topic: {
      destination: topic,
      callback,
    },
    onConnected,
    onError,
  });
};
