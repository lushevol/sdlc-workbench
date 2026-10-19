import React from "react";
import ReactDOMClient from "react-dom/client";
import singleSpaReact from "single-spa-react";
import App from "./App";

const lifecycles = singleSpaReact({
  React,
  ReactDOMClient,
  rootComponent: App,
  errorBoundary(err) {
    // Customize the root error boundary for your microfrontend here.
    return <span>{err.message}</span>;
  },
});

export const { bootstrap, unmount } = lifecycles;
const rootElement = window.single_spa_container_id;
type RootProps = Record<string, unknown>;

export const render = (rootComp: Element, props: RootProps) => {
  const root = ReactDOMClient.createRoot(rootComp);
  root.render(<App {...props} />);
};
export const check = (rootComp: Element | undefined, props: RootProps) => {
  if (rootComp) {
    render(rootComp, props);
  }
};
export function MountComponent(props: RootProps) {
  return Promise.resolve().then(() => {
    check(rootElement, props);
  });
}
export const mount = rootElement ? MountComponent : lifecycles.mount;

export * as Provider from "./hooks/provider";
export * as Service from "./hooks/service";
export * as Reduces from "./hooks/reducer";
export * as ActionType from "./hooks/reducer/util/ActionType";
export * as Hooks from "./hooks";
export * as CommonUtil from "./utils/common";
export * as ChannelUtil from "./utils/drawer";
export * as LoginUtil from "./utils/login";
export * as LocaleUtil from "./utils/locale";
export * as ErrorBoundry from "./components/ErrorBoundry";
export * as Loader from "./components/Loader";
export * as PageLoader from "./components/Loader/PageLoader";
export * as LoaderProps from "./components/Loader/common/type";
export * as Drawer from "./components/Drawer";
export * as ThemeConfig from "./theme/Config";
export * as ThemeUtil from "./theme/config/utils";
export * as ThemeProvider from "./theme/Provider";
export * as Splash from "./components/Splash";
export * as ReactRouterDom from "react-router-dom";
export * as Dispatcher from "./hooks/dispathcer";
export * as Time from "./components/Time";
export * as LoadingButton from "./components/LoadingButton";
export * as LoadingButtonProps from "./components/LoadingButton/interface";
export * as Input from "./components/Input";
export * as Snackbar from "./components/Snackbar";
export * as Dialog from "./components/Dialog";
export * as Label from "./components/Label";
export * as SearchCondition from "./components/SearchCondition";
export * as SearchConditionContainer from "./components/SearchConditionContainer";
export * as BuilderButton from "./components/BuilderButton";
export * as SearchInput from "./components/SearchInput";
export * as DateRangePicker from "./components/DateRangePicker";
export * as DatePicker from "./components/DatePicker";
export * as DateTimePicker from "./components/DateTimePicker";
export * as TimePicker from "./components/TimePicker";
export * as SearchGrid from "./components/SearchGrid";
export * as ToggleButton from "./components/ToggleButton";
export * as SearchButton from "./components/SearchButton";
export * as Button from "./components/Button";
export * as ExtendService from "./hooks/service/util/extend";
export * as Analytics from "./analytics";
export * as Version from "./components/Version";
export * as Select from "./components/Select";
export * as ResetButton from "./components/ResetButton";
export * as Services from "./services";
export * as ScWebkit from "./components/ScWebkit";
export * as ReactWrapper from "./utils/ReactWrapper";
