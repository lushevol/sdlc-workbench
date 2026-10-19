import { render, screen } from "@testing-library/react";
import React from "react";
import Root from ".";
import Provider from "../../hooks/provider";
import ThemeProvider from "../../theme";
afterAll(() => {
  jest.clearAllMocks();
});
jest.mock("../../utils/common", () => {
  return {
    getJWTPayload: () => "JWT",
    storeData: jest.fn(),
    clearLocalStorage: jest.fn(),
    clearStorageWhenLogout: jest.fn(),
    uuidv4: () => "id",
    showErrorMsg: jest.fn(),
    show_error_msg: jest.fn(),
    getEnv: () => "LOCAL",
    getHostName: () => "localhost",
    getLocalStorage: () => ({
      setItem: (v) => { },
      getItem: () => undefined,
      clear: () => { }
    }),
    getSessionStorage: () => ({
      setItem: (v) => { },
      getItem: () => undefined,
      clear: () => { }
    }),
    waitFor: ()=>Promise.resolve(),
  }
});
jest.mock("../../hooks/service", () => {
  return {
    putService: async (path, data, signal = undefined) => { return Promise.resolve({}) },
    postService: async (path, data, signal = undefined) => { return Promise.resolve({}) },
    getService: async (path, signal = undefined) => { return Promise.resolve({}) },
    extendToken: async (path, signal = undefined) => { return Promise.resolve({}) },
    getRefreshToken: async (path, signal = undefined) => { return Promise.resolve({}) },
    relogin: async (path, signal = undefined) => { return Promise.resolve({}) }
  }
});
const Comp = () => {
  return (<Root setOpen={() => { }} />);
};


describe("Timeout component", () => {
  it("Logout_Btn should be in the document", () => {
    render(<Provider data={{ user: { id: "123" }, token: "123", theme: "dark" }}>
      <ThemeProvider>
        <Comp />
      </ThemeProvider>
    </Provider>);
    expect(screen).toBeDefined();
    const Extend_Btn = screen.getByTestId("Extend_Btn");
    expect(Extend_Btn).toBeInTheDocument();
    Extend_Btn.click();
  });
  it("Hide_Btn should be in the document", () => {
    render(<Provider data={{ user: { id: "123" }, token: "123", theme: "dark" }}>
      <ThemeProvider>
        <Comp />
      </ThemeProvider>
    </Provider>);
    expect(screen).toBeDefined();
    const Logout_Btn = screen.getByTestId("Logout_Btn");
    expect(Logout_Btn).toBeInTheDocument();
    Logout_Btn.click();
  });
});
