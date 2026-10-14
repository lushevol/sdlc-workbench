import { uuidv4 } from "../../utils/common";

export interface Container {
  id: string;
  container: string;
  module: string;
  tile: string;
  title: string;
  subtitle?: string;
  parameters?: Object;
  emailSupport: string;
  panelId: string;
  tabId: string;
  leftPosition?: string;
  topPossition?: string;
}

export interface Workspace {
  id: string;
  label: string;
  isActive: boolean;
  containers: Container[] | [];
}

export const firstWorkspace = () => ({
  id: uuidv4(),
  label: "Workspace 1",
  isActive: false,
  containers: [],
});
