import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// ---------------------------------------------------------------------------
// Module mocks
// ---------------------------------------------------------------------------
vi.mock("@modelcontextprotocol/ext-apps/server", () => ({
  registerAppTool: vi.fn(),
  registerAppResource: vi.fn(),
  RESOURCE_MIME_TYPE: "text/html;profile=mcp-app"
}));

vi.mock("fs/promises", () => ({
  readFile: vi.fn().mockResolvedValue("<html>Test UI</html>")
}));

// ---------------------------------------------------------------------------
// Imports
// ---------------------------------------------------------------------------
import { registerAppTool, registerAppResource, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";
import { configureUploadTools, configureUiResource } from "../src/tools.js";

// ---------------------------------------------------------------------------
// Mock ADO connection factory
// ---------------------------------------------------------------------------
function buildMockWitApi() {
  return {
    createAttachment: vi.fn(),
    updateWorkItem: vi.fn()
  };
}

function buildMockConnection(witApi) {
  return {
    getWorkItemTrackingApi: vi.fn().mockResolvedValue(witApi)
  };
}

/** Build a mock MCP server that captures tool registrations. */
function buildMockServer() {
  const handlers = {};
  return {
    tool: vi.fn((name, _desc, _schema, handler) => { handlers[name] = handler; }),
    handlers,
    connect: vi.fn()
  };
}

// ---------------------------------------------------------------------------
// Tests — tool registration
// ---------------------------------------------------------------------------
describe("configureUploadTools — registration", () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it("registers wit_upload_attachment_ui via registerAppTool with correct metadata", () => {
    const server = buildMockServer();
    configureUploadTools(server, vi.fn());

    expect(registerAppTool).toHaveBeenCalledOnce();
    const [, toolName, config] = registerAppTool.mock.calls[0];
    expect(toolName).toBe("wit_upload_attachment_ui");
    expect(config._meta.ui.resourceUri).toBe("ui://ado-upload-ui");
    expect(config._meta.ui.visibility).toContain("app");
  });

  it("registers wit_upload_attachment via server.tool", () => {
    const server = buildMockServer();
    configureUploadTools(server, vi.fn());

    expect(server.tool).toHaveBeenCalledOnce();
    const [name] = server.tool.mock.calls[0];
    expect(name).toBe("wit_upload_attachment");
  });

  it("configureUiResource registers UI resource with correct URI and MIME type and handler returns HTML", async () => {
    const server = buildMockServer();
    configureUiResource(server);

    expect(registerAppResource).toHaveBeenCalledOnce();
    const [, name, uri, , handler] = registerAppResource.mock.calls[0];
    expect(name).toBe("ADO Upload UI");
    expect(uri).toBe("ui://ado-upload-ui");
    expect(RESOURCE_MIME_TYPE).toBe("text/html;profile=mcp-app");

    // Invoke handler to cover lines in tools.js
    const result = await handler({ href: "ui://ado-upload-ui" });
    expect(result.contents[0].mimeType).toBe(RESOURCE_MIME_TYPE);
    expect(result.contents[0].text).toBe("<html>Test UI</html>");
    expect(result.contents[0].uri).toBe("ui://ado-upload-ui");
  });
});

// ---------------------------------------------------------------------------
// Tests — wit_upload_attachment_ui handler
// ---------------------------------------------------------------------------
describe("wit_upload_attachment_ui handler", () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = buildMockServer();
    let uiHandler;
    registerAppTool.mockImplementationOnce((_s, _name, _config, handler) => { uiHandler = handler; });
    configureUploadTools(server, vi.fn());
    server.__uiHandler = uiHandler;
  });

  it("returns project and wiId when pre-filled", async () => {
    const result = await server.__uiHandler({ project: "MyProject", wiId: 999 });
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.project).toBe("MyProject");
    expect(parsed.wiId).toBe("999");
  });

  it("returns empty strings when no args provided", async () => {
    const result = await server.__uiHandler();
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.project).toBe("");
    expect(parsed.wiId).toBe("");
  });
});

// ---------------------------------------------------------------------------
// Tests — wit_upload_attachment handler
// ---------------------------------------------------------------------------
describe("wit_upload_attachment handler", () => {
  let witApi, getADOConnection, server;

  beforeEach(() => {
    vi.clearAllMocks();
    witApi = buildMockWitApi();
    const connection = buildMockConnection(witApi);
    getADOConnection = vi.fn().mockResolvedValue(connection);
    server = buildMockServer();
    configureUploadTools(server, getADOConnection);
  });

  afterEach(() => { vi.clearAllMocks(); });

  async function invokeUpload(args) {
    const handler = server.handlers["wit_upload_attachment"];
    return handler(args);
  }

  it("uploads a single file and links it to the work item", async () => {
    witApi.createAttachment.mockResolvedValue({
      id: "guid-screenshot.png",
      url: "https://dev.azure.com/sc-ado/_apis/wit/attachments/guid-screenshot.png"
    });
    witApi.updateWorkItem.mockResolvedValue({ id: 12345 });

    const result = await invokeUpload({
      project: "TestProject",
      wiId: 12345,
      files: [{ name: "screenshot.png", base64: Buffer.from("pngdata").toString("base64") }]
    });

    expect(result.isError).toBeFalsy();
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.success).toBe(true);
    expect(parsed.workItemId).toBe(12345);
    expect(parsed.uploaded).toHaveLength(1);
    expect(parsed.uploaded[0].name).toBe("screenshot.png");

    expect(witApi.createAttachment).toHaveBeenCalledOnce();
    expect(witApi.updateWorkItem).toHaveBeenCalledOnce();

    const [, patch] = witApi.updateWorkItem.mock.calls[0];
    expect(patch).toHaveLength(1);
    expect(patch[0].op).toBe("add");
    expect(patch[0].value.rel).toBe("AttachedFile");
  });

  it("uploads multiple files and creates one relation patch entry per file", async () => {
    witApi.createAttachment.mockImplementation(async (_h, _stream, fileName) => ({
      id: `guid-${fileName}`,
      url: `https://dev.azure.com/sc-ado/_apis/wit/attachments/guid-${fileName}`
    }));
    witApi.updateWorkItem.mockResolvedValue({ id: 99 });

    const result = await invokeUpload({
      project: "TestProject",
      wiId: 99,
      files: [
        { name: "file1.txt", base64: Buffer.from("aaa").toString("base64") },
        { name: "file2.pdf", base64: Buffer.from("bbb").toString("base64") },
        { name: "file3.csv", base64: Buffer.from("ccc").toString("base64") }
      ]
    });

    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.success).toBe(true);
    expect(parsed.uploaded).toHaveLength(3);
    expect(witApi.createAttachment).toHaveBeenCalledTimes(3);

    const [, patch] = witApi.updateWorkItem.mock.calls[0];
    expect(patch).toHaveLength(3);
  });

  it("returns isError when createAttachment throws", async () => {
    witApi.createAttachment.mockRejectedValue(new Error("ADO 404: Not Found"));

    const result = await invokeUpload({
      project: "BadProject",
      wiId: 1,
      files: [{ name: "doc.txt", base64: "dGVzdA==" }]
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("ADO 404");
  });

  it("returns isError when updateWorkItem throws", async () => {
    witApi.createAttachment.mockResolvedValue({ id: "abc", url: "https://example.com/abc" });
    witApi.updateWorkItem.mockRejectedValue(new Error("Permission denied"));

    const result = await invokeUpload({
      project: "TestProject",
      wiId: 5,
      files: [{ name: "notes.txt", base64: "dGVzdA==" }]
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("Permission denied");
  });
});
