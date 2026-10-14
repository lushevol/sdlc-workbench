import React from "react";
import { postService } from "../hooks/service";
import { useContext } from "../hooks/provider";
import {
  AnalyticsButtonOrTabOrSwitchEventType,
  AnalyticsData,
  AnalyticsDropDownEventType,
  AnalyticsTileOrModalEventType,
  AnalyticsType,
} from "./model";

const useAnalytics = () => {
  const [store] = useContext();
  const post = (data: AnalyticsType) => {
    postService("/analytics/v1/fmo/print", data).catch((e) => console.error(e));
  };
  const singleUIAuthorization = store.refreshToken ?? store.token;
  const TileEvent = (
    event: AnalyticsTileOrModalEventType,
    analyticsData: AnalyticsData
  ) => {
    const data: AnalyticsType = {
      singleUIAuthorization,
      key: "tile",
      event,
      ...analyticsData,
    };
    post(data);
  };

  const ModalEvent = (
    event: AnalyticsTileOrModalEventType,
    analyticsData: AnalyticsData
  ) => {
    const data: AnalyticsType = {
      singleUIAuthorization,
      key: "modal",
      event,
      ...analyticsData,
    };
    post(data);
  };

  const TabEvent = (
    event: AnalyticsButtonOrTabOrSwitchEventType,
    analyticsData: AnalyticsData
  ) => {
    const data: AnalyticsType = {
      singleUIAuthorization,
      key: "tab",
      event,
      ...analyticsData,
    };
    post(data);
  };

  const ButtonEvent = (
    event: AnalyticsButtonOrTabOrSwitchEventType,
    analyticsData: AnalyticsData
  ) => {
    const data: AnalyticsType = {
      singleUIAuthorization,
      key: "button",
      event,
      ...analyticsData,
    };
    post(data);
  };

  const SwitchEvent = (
    event: AnalyticsButtonOrTabOrSwitchEventType,
    analyticsData: AnalyticsData
  ) => {
    const data: AnalyticsType = {
      singleUIAuthorization,
      key: "switch",
      event,
      ...analyticsData,
    };
    post(data);
  };

  const DropDownEvent = (
    event: AnalyticsDropDownEventType,
    analyticsData: AnalyticsData
  ) => {
    const data: AnalyticsType = {
      singleUIAuthorization,
      key: "dropdown",
      event,
      ...analyticsData,
    };
    post(data);
  };
  return {
    TileEvent,
    ModalEvent,
    TabEvent,
    ButtonEvent,
    DropDownEvent,
    SwitchEvent,
  };
};

export default useAnalytics;
