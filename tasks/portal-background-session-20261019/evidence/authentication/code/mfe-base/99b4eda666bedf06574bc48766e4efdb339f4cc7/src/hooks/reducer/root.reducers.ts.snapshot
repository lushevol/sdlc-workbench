import { RootModel } from "../model/root";
import { ActionType, IAction } from "./util/ActionType";

const root = (store: RootModel, action: IAction): RootModel => {
  switch (action.type) {
    case ActionType.SET_REFRESH_TOKEN:
      store.refreshToken = action.data.refreshToken;
      break;
    case ActionType.SET_IS_OPENFIN:
      store.isOpenFin = action.data.isOpenFin;
      break;
    case ActionType.SET_CLIENT_BUS:
      store.clientBus = action.data.clientBus;
      break;
    case ActionType.SET_TIME_TYPE:
      store.timeType = action.data.timeType;
      break;
    case ActionType.SET_ENTITIES:
      store.entities = action.data.entities;
      break;
    case ActionType.SET_ENTITLEMENTS_TOKEN:
      store.entitlementsToken = action.data.entitlementsToken;
      break;
    default:
      break;
  }
  return store;
};

export default root;
