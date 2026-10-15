import { registerApplication, start } from "single-spa";
import {
  constructApplications,
  constructRoutes,
  constructLayoutEngine,
} from "single-spa-layout";
import microfrontendLayout from "./microfrontend-layout.html";
import json from "../package.json";

const root = () => {
  const routes = constructRoutes(microfrontendLayout);
  const applications = constructApplications({
    routes,
    loadApp({ name }) {
      return System.import(name);
    },
  });
  const layoutEngine = constructLayoutEngine({ routes, applications });
  applications.forEach((mfe) => {
    mfe.customProps = {
      publicUrl: `/`,
      version: json.version,
    };
    registerApplication(mfe);
  });
  layoutEngine.activate();
  start();
};
root();
export default root;
