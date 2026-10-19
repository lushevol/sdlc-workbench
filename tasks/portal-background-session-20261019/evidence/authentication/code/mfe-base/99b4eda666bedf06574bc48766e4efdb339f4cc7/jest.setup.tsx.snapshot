import React from "react";
import { TextEncoder, TextDecoder } from "text-encoding";
// @ts-ignore
if (typeof global.TextEncoder === "undefined") {
  // @ts-ignore
  global.TextEncoder = TextEncoder;
  // @ts-ignore
  global.TextDecoder = TextDecoder;
}
const mockComponent = (c) => {
  return <section>{c.children}</section>;
}
// Mock SystemJS
async function mockImport(name) {
  return Promise.resolve({
    __esModule: true,
    default: mockComponent,
    [name]: mockComponent,
    getRoot: mockComponent,
  });
}
// @ts-ignore
global.System = {
  // @ts-ignore
  import: jest.fn(mockImport),
};
// @ts-ignore
jest.mock("@scdevkit/webkit/elements/sc-button", () => {
  return {
    __esModule: true,
    default: (_props) => {},
  };
});
// @ts-ignore
jest.mock("@scdevkit/webkit/elements/sc-icon-card", () => {
  return {
    __esModule: true,
    default: (_props) => {},
  };
});

console.error = (...args) => { };
console.log = (...args) => { };
console.info = (...args) => { };
// @ts-ignore
jest.setTimeout(60000);
