import { RootModel } from "../model/root";
import { ActionType, IAction } from "./util/ActionType";

const root0 = (store: RootModel, action: IAction): RootModel => {
  switch (action.type) {
    case ActionType.SET_TOKEN:
      store.token = action.data.token;
      store.isOnLogout = false;
      break;
    case ActionType.SET_USER:
      store.user = action.data.user;
      break;
    case ActionType.SET_ERRORMSG:
      store.errorMsg = action.data.errorMsg;
      break;
    case ActionType.SET_IS_LOADING:
      store.isLoading = action.data.isLoading;
      break;
    case ActionType.SET_THEME:
      store.theme = action.data.theme;
      break;
    case ActionType.SET_EXPIRED_TOKEN:
      store.expiredIn = action.data.expiredIn;
      store.iat = action.data.iat;
      if (!store.userLoginTime) {
        store.userLoginTime = action.data.userLoginTime;
      }
      break;
    case ActionType.SET_DRAWER:
      store.drawer = action.data.drawer;
      break;
    case ActionType.SET_IS_ON_LOGOUT:
      store.isOnLogout = action.data.isOnLogout;
      break;
    case ActionType.CLEAR:
      store.user = undefined;
      store.token = undefined;
      store.refreshToken = undefined;
      store.expiredIn = undefined;
      store.iat = undefined;
      store.userLoginTime = undefined;
      store.errorMsg = undefined;
      store.isOnLogout = false;
      break;
    default:
      break;
  }
  return store;
};

export default root0;
