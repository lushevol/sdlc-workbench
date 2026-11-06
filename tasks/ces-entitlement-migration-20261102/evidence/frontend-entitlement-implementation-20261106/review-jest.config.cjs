const c=require("../../frontend-tests/container-jest.config.cjs");
const path=require("path");
module.exports={...c,rootDir:path.resolve(__dirname,"../../../.."),testMatch:[path.join(__dirname,"review-role-delete.ces.test.tsx")],testEnvironment:"jsdom",moduleDirectories:[path.resolve(__dirname,"../../../../repos/ui/mfe-base/node_modules"),path.resolve(__dirname,"../../../../repos/ui/mfe-ratan-container/node_modules")]};
