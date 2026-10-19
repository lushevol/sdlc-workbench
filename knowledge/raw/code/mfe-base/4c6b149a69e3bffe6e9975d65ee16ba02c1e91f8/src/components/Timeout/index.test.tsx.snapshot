import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import Root from ".";
import Provider from "../../hooks/provider";
import ThemeProvider from "../../theme";
import useController from "./common/useController";
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
const Comp = (props) => {
  const { timerPopup, clearAllTimeout, extend } = useController(props);
  React.useEffect(() => {
    extend();
    timerPopup.current = 1233;
    clearAllTimeout();
  }, [])
  return (<Root {...props} />);
};
describe("Timeout component", () => {
  it("Logout_Btn should be in the document", () => {
    global.window = Object.create(window);
    Object.defineProperty(window, 'setTimeout', {
      value: (f) => { f(); },
      writable: true
    });
    const part1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9";
    const part2 = "eyJlbnRpdGxlbWVudHMiOiJ7XCJGU1NfUEFZTUVOVFNfU0VSVklDRVNfVEg6RlNTX1BTX1NVUEVSX1VTRVJcIjp7XCJGU1MgUGF5bWVudHMgU2VydmljZXNcIjpbXCJNT0RVTEVfQ29udGFjdERldGFpbHNcIixcIkNPVU5UUllfVEhcIixcIk1PRFVMRV9DdXN0b21lclwiLFwiTU9EVUxFX0V4dGVybmFsQWNjb3VudFwiLFwiTU9EVUxFX0hvbGlkYXlcIixcIk1PRFVMRV9JbnRlcmVzdGVkUGFydHlcIixcIk1PRFVMRV9JbnRlcm5hbEFjY291bnRcIixcIk1PRFVMRV9SZXBvcnRzTWFuYWdlbWVudFwiLFwiTU9EVUxFX1J1bGVcIixcIk1PRFVMRV9UcmFuc2FjdGlvblwiXX0sXCJTU0lQTFVTOlNTSV9TVVBFUl9VU0VSXCI6e1wiU0VBUkNIXCI6W1wiV1JJVEVcIl0sXCJXT1JLUVVFVUVcIjpbXCJXUklURVwiXSxcIlZBTElEQVRJT05SVUxFU1wiOltcIldSSVRFXCJdLFwiU1RBVElDXCI6W1wiV1JJVEVcIl19LFwiQ0RVUFM6Rk1PX0ZYTU1fU3VwZXJVc2VyXCI6e1wiaW5ib3VuZGRvY3MuZXhwb3J0XCI6W1wiVFJVRVwiXSxcImJ1bGtwcmludGluZy52aWV3XCI6W1wiVFJVRVwiXSxcImluYm91bmRkb2NzLnVucGFpclwiOltcIlRSVUVcIl0sXCJzdGF0aWMuY3B0eS52aWV3XCI6W1wiVFJVRVwiXSxcInRyYWRlLmFmZmlybWF0aW9uLmFwcHJvdmVcIjpbXCJUUlVFXCJdLFwic3RhdGljLnJlZnN0YXRpYy52aWV3LnB1YmxpY1wiOltcIlRSVUVcIl0sXCJ0cmFkZS5hZmZpcm1hdGlvbi52aWV3XCI6W1wiVFJVRVwiXSxcInRyYWRlLkJ1bGtsb2FkXCI6W1wiVFJVRVwiXSxcInRyYWRlLmFmZmlybWF0aW9uLmNoYXNlclwiOltcIlRSVUVcIl0sXCJleGNlcHRpb25ibG90dGVyLnJlc3VibWl0XCI6W1wiRkFMU0VcIl0sXCJhZmZpcm1hdGlvbi52aWV3LnByaXZhdGVcIjpbXCJUUlVFXCJdLFwiaW5ib3VuZGRvY3MucGFpclwiOltcIlRSVUVcIl0sXCJkYXNoYm9hcmQuSUJkYXNib2FyZC52aWV3XCI6W1wiVFJVRVwiXSxcInRyYWRlLnRyYWRlZGV0YWlscy5pYm9idXBsb2FkXCI6W1wiVFJVRVwiXSxcInN0YXRpYy5jcHR5LnBha2lzdGFuXCI6W1wiRkFMU0VcIl0sXCJVc2VyQWNjZXNzTWdtdC5FZGl0XCI6W1wiVFJVRVwiXSxcImFmZmlybWF0aW9uLmV4cG9ydFwiOltcIlRSVUVcIl0sXCJzdGF0aWMucmVmc3RhdGljLmVkaXRcIjpbXCJUUlVFXCJdLFwic3RhdGljLnJlZnN0YXRpYy5yZWplY3RcIjpbXCJUUlVFXCJdLFwidHJhZGUuYWZmaXJtYXRpb24ucmVqZWN0XCI6W1wiVFJVRVwiXSxcImRpc3BhdGNoZmFpbHVyZS52aWV3XCI6W1wiVFJVRVwiXSxcInN0YXRpYy5jcHR5LnZpZXcucHVibGljXCI6W1wiVFJVRVwiXSxcImV4Y2VwdGlvbmJsb3R0ZXIuZXhwb3J0XCI6W1wiVFJVRVwiXSxcInN0YXRpYy5jcHR5LmVkaXRcIjpbXCJUUlVFXCJdLFwiZGlzcGF0Y2hmYWlsdXJlLnZpZXcucHJpdmF0ZVwiOltcIlRSVUVcIl0sXCJ0cmFkZS5kb2N1bWVudC52aWV3ZG9jdW1lbnRcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLnZpZXcucHVibGljXCI6W1wiVFJVRVwiXSxcInRzLmV4Y2VwdGlvbmJsb3R0ZXIudmlld1wiOltcIkZBTFNFXCJdLFwidHMuYXVkaXRsb2dzLnZpZXdcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLnZpZXcucHJpdmF0ZVwiOltcIlRSVUVcIl0sXCJ0cmFkZS5hZmZpcm1hdGlvbi5lZGl0XCI6W1wiVFJVRVwiXSxcInN0YXRpYy5yZWZzdGF0aWMucGFraXN0YW5cIjpbXCJGQUxTRVwiXSxcInN0YXRpYy5jcHR5LnJlamVjdFwiOltcIlRSVUVcIl0sXCJ0cmFkZS50cmFkZWRldGFpbHMuYXBwcm92ZVwiOltcIlRSVUVcIl0sXCJzdGF0aWMucmVmc3RhdGljLnZpZXdcIjpbXCJUUlVFXCJdLFwic3RhdGljLmNwdHkuZXhwb3J0XCI6W1wiVFJVRVwiXSxcInRyYWRlLmRvY3VtZW50LnJlc2VuZFwiOltcIlRSVUVcIl0sXCJhZmZpcm1hdGlvbi5lZGl0XCI6W1wiVFJVRVwiXSxcImJ1bGtwcmludGluZy52aWV3LnByaXZhdGVcIjpbXCJUUlVFXCJdLFwiZGFzaGJvYXJkLmFmZmlybWF0aW9uLnZpZXdcIjpbXCJUUlVFXCJdLFwidHJhZGUuUmV2aWV3Q2FzZS5FZGl0XCI6W1wiVFJVRVwiXSxcInRyYWRlLnRyYWRlZGV0YWlscy5pYnN0YXR1c1wiOltcIlRSVUVcIl0sXCJ0cmFkZS50cmFkZWRldGFpbHMucmVqZWN0XCI6W1wiVFJVRVwiXSxcImluYm91bmRkb2NzLnZpZXdcIjpbXCJUUlVFXCJdLFwiaW5ib3VuZGRvY3Mudmlldy5wcml2YXRlXCI6W1wiVFJVRVwiXSxcInRyYWRlLmRvY3VtZW50LmZvcmNlYWNrXCI6W1wiVFJVRVwiXSxcInRyYWRlLnRyYWRlZGV0YWlscy5yZXZhbGlkYXRlXCI6W1wiVFJVRVwiXSxcInRyYWRlLm1hdGNoLmlvLmFwcHJvdmVcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLnNjYm1sXCI6W1wiVFJVRVwiXSxcInRyYWRlLnRyYWRlZGV0YWlscy52aWV3LmV4cG9ydFwiOltcIlRSVUVcIl0sXCJ0cmFkZS5hZmZpcm1hdGlvbi5jcmVhdGVcIjpbXCJUUlVFXCJdLFwidHJhZGUuYWZmaXJtYXRpb24uaW52ZXN0aWdhdGVcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLm9ic3RhdHVzXCI6W1wiVFJVRVwiXSxcInRyYWRlLm1hdGNoLmlvLnZpZXdcIjpbXCJUUlVFXCJdLFwiZXhjZXB0aW9uYmxvdHRlci52aWV3XCI6W1wiVFJVRVwiXSxcImRpc3BhdGNoZmFpbHVyZS5leHBvcnRcIjpbXCJUUlVFXCJdLFwic3RhdGljLmNwdHkudmlldy5wcml2YXRlXCI6W1wiVFJVRVwiXSxcImluYm91bmRkb2NzLmVkaXRcIjpbXCJUUlVFXCJdLFwic3RhdGljLmNwdHkuYnVsa3VwbG9hZFwiOltcIlRSVUVcIl0sXCJzdGF0aWMucmVmc3RhdGljLmFwcHJvdmVcIjpbXCJUUlVFXCJdLFwic3RhdGljLnJlZnN0YXRpYy5leHBvcnRcIjpbXCJUUlVFXCJdLFwic3RhdGljLnJlZnN0YXRpYy5jcmVhdGVcIjpbXCJUUlVFXCJdLFwiYWZmaXJtYXRpb24udmlldy5wdWJsaWNcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLmVkaXRcIjpbXCJUUlVFXCJdLFwic3RhdGljLnJlZnN0YXRpYy52aWV3LnByaXZhdGVcIjpbXCJUUlVFXCJdLFwidHJhZGUuZG9jdW1lbnRyZXZpZXdcIjpbXCJUUlVFXCJdLFwiYWZmaXJtYXRpb24udmlld1wiOltcIlRSVUVcIl0sXCJkaXNwYXRjaGZhaWx1cmUudmlldy5wdWJsaWNcIjpbXCJUUlVFXCJdLFwiZGFzaGJvYXJkLk9iZGFzYm9hcmQudmlld1wiOltcIlRSVUVcIl0sXCJ0cmFkZS50cmFkZWRldGFpbHMuZ2VuZXJhdGVkb2NcIjpbXCJUUlVFXCJdLFwic3RhdGljLmNwdHkuYXBwcm92ZVwiOltcIlRSVUVcIl0sXCJzdGF0aWMucmVmc3RhdGljLmRlbGV0ZVwiOltcIlRSVUVcIl0sXCJzdGF0aWMucmVmc3RhdGljLmJ1bGt1cGxvYWRcIjpbXCJUUlVFXCJdLFwiYnVsa3ByaW50aW5nLmVkaXRcIjpbXCJUUlVFXCJdLFwiaW5ib3VuZGRvY3Mudmlldy5wdWJsaWNcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLmJ1bGtwcmludFwiOltcIkZBTFNFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLnJlbG9hZFwiOltcIlRSVUVcIl0sXCJkaXNwYXRjaGZhaWx1cmUuZWRpdFwiOltcIlRSVUVcIl0sXCJidWxrcHJpbnRpbmcudmlldy5wdWJsaWNcIjpbXCJUUlVFXCJdLFwiYnVsa3ByaW50aW5nLmV4cG9ydFwiOltcIlRSVUVcIl0sXCJ0cmFkZS50cmFkZWRldGFpbHMudmlld1wiOltcIlRSVUVcIl0sXCJ0cmFkZS50cmFkZWRldGFpbHMuaWJvYmRvd2xvYWRcIjpbXCJUUlVFXCJdLFwidHJhZGUudHJhZGVkZXRhaWxzLmV4cG9ydFwiOltcIlRSVUVcIl19fSIsIm1heF9hZ2UiOjE2OTQzOTU2OTMsInN1YiI6IjIwMDEyMDgiLCJhdXRoX3RpbWUiOjE2OTQzOTIwOTMsImlzcyI6InNpbmdsZS11aS1iZmYiLCJmdWxsTmFtZSI6IktoYWlydWwgQW5zaGFyMSIsImV4cCI6MTY5NDM5MzI1MywiaWF0IjoxNjk0MzkyMzUzLCJqdGkiOiJzaW5nbGUtdWktYmZmLWlkIn0";
    const part3 = "gMGrsRCXWq4p43qtfi5xIxUIbI3G22kEKjIs6-HqLXnsPt4TUGhT3dWtaO1cSR5gH4bKLRlFg2uIMaIVjj7_kGbxWqCmI8eqa0oVCAtf10bAtfne7pM1dUC5MnrYySE9PQiAqNlJyfvRyyd4DkrDEz4DCcQ7WpkiUjm6rFOi9tz0BC9s10p3bwuhaKaBz3C9GdCESqo48hGC96-fbaTMOz0jpXO9JTbJ89Kb8XyUWuRfXNryFFchTn2G-B4aaNoREORba1iWBCKma-NxoGW0cGgQIw6OCepp7PU4NmesVyDQZEnM7xHNxT35WjgX0VAmeN9EclHxCAi_ogvrS3C9fA"
    render(<Provider data={{ user: { id: "123" }, token: "123", theme: "dark", refreshToken: `Bearer ${part1}.${part2}.${part3}` }}>
      <ThemeProvider>
        <Comp setOpen={() => { }} />
      </ThemeProvider>
    </Provider>);
    expect(screen).toBeDefined();
    const Extend_Btn = screen.getByTestId("Extend_Btn");
    expect(Extend_Btn).toBeInTheDocument();
    Extend_Btn.click();
    fireEvent.click(Extend_Btn);
  });
  it("Hide_Btn should be in the document", () => {
    global.window = Object.create(window);
    Object.defineProperty(window, 'setTimeout', {
      value: (f) => { f(); },
      writable: true
    });
    render(<Provider data={{ user: { id: "123" }, token: "123", theme: "dark" }}>
      <ThemeProvider>
        <Comp setOpen={() => { }} />
      </ThemeProvider>
    </Provider>);
    expect(screen).toBeDefined();
    const Logout_Btn = screen.getByTestId("Logout_Btn");
    expect(Logout_Btn).toBeInTheDocument();
    Logout_Btn.click();
    fireEvent.click(Logout_Btn);
  });
});
