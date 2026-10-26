import React from "react";
import { act, cleanup, renderHook } from "@testing-library/react";
import Provider from "../../../hooks/provider";
import { Workspace } from "../../../hooks/model/workspaces";
import useController from "./useController";

jest.mock("../../../analytics", () => () => ({
  ButtonEvent: jest.fn(), TileEvent: jest.fn(), TabEvent: jest.fn(), ModalEvent: jest.fn(),
}));

const workspace = (id: string): Workspace => ({ id, label: id, isActive: false, containers: [] });
const clickEvent = (id = "workspace-tab"): React.SyntheticEvent => {
  const container = document.createElement("div"); container.id = id;
  const span = document.createElement("span"); const button = document.createElement("button");
  container.appendChild(span); span.appendChild(button);
  return { target: button, stopPropagation: jest.fn() } as unknown as React.SyntheticEvent;
};
const open = (workspaces: Workspace[]) => renderHook(() => useController(), {
  wrapper: ({ children }) => <Provider data={{ workspaces, currentWorkspace: workspaces[0],
    entities: [], drawers: [], token: undefined }}>{children}</Provider>,
});

describe("Home workspace preservation during session changes", () => {
  beforeEach(() => { localStorage.clear(); sessionStorage.clear(); });
  afterEach(() => { cleanup(); localStorage.clear(); sessionStorage.clear(); });

  it("[DEL-15] preserves current workspace when a stale tab index is selected", () => {
    const first = workspace("workspace-a"); const second = workspace("workspace-b");
    const { result } = open([first, second]);
    expect(result.current.store.currentWorkspace?.id).toBe(first.id);
    act(() => result.current.handleChange(clickEvent(), 99));
    expect(result.current.store.currentWorkspace?.id).toBe(first.id);
    expect(result.current.store.workspaces?.map(item => item.id)).toEqual([first.id, second.id]);
  });

  it("[DEL-16] selects the next workspace after deleting the first selected workspace", () => {
    const first = workspace("workspace-a"); const second = workspace("workspace-b");
    const { result } = open([first, second]);
    act(() => result.current.remove(first)(clickEvent() as React.MouseEvent));
    expect(result.current.store.workspaces?.map(item => item.id)).toEqual([second.id]);
    expect(result.current.store.currentWorkspace?.id).toBe(second.id);
    expect(JSON.parse(localStorage.getItem("SET_WORKSPACES")!)).toEqual([second]);
  });

  it("[DEL-17] preserves previous-workspace selection after deleting a later selected workspace", () => {
    const first = workspace("workspace-a"); const second = workspace("workspace-b");
    const { result } = open([first, second]);
    act(() => result.current.handleChange(clickEvent(), 2));
    expect(result.current.store.currentWorkspace?.id).toBe(second.id);
    act(() => result.current.remove(second)(clickEvent() as React.MouseEvent));
    expect(result.current.store.workspaces?.map(item => item.id)).toEqual([first.id]);
    expect(result.current.store.currentWorkspace?.id).toBe(first.id);
    expect(JSON.parse(localStorage.getItem("SET_WORKSPACES")!)).toEqual([first]);
  });

  it("[DEL-18] replaces inaccessible saved descriptors with one blank workspace", () => {
    const unavailable: Workspace = { ...workspace("unavailable"), containers: [{
      id: "container-unavailable", container: "@fm/unavailable", module: "/unavailable", tile: "/unavailable",
      title: "Unavailable", emailSupport: "", panelId: "", tabId: "",
    }] };
    const { result } = open([unavailable]);
    expect(result.current.validateWorkspaceReady).toBe(true);
    expect(result.current.store.workspaces).toHaveLength(1);
    const restored = result.current.store.workspaces![0];
    expect(restored.id).not.toBe(unavailable.id);
    expect(restored.label).toBe("Workspace 1");
    expect(restored.containers).toEqual([]);
    expect(result.current.store.currentWorkspace?.id).toBe(restored.id);
  });
});
