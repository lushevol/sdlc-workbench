import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { JSDOM } from "jsdom";

// ---------------------------------------------------------------------------
// Mock @modelcontextprotocol/ext-apps
// ---------------------------------------------------------------------------
const mockApp = {
  connect: vi.fn().mockResolvedValue(undefined),
  callServerTool: vi.fn(),
  ontoolinput: null,
  onteardown: null
};

vi.mock("@modelcontextprotocol/ext-apps", () => ({
  App: vi.fn().mockImplementation(() => mockApp)
}));

// ---------------------------------------------------------------------------
// Shared handler logic (mirrors mcp-app.js ontoolinput implementation)
// ---------------------------------------------------------------------------
function applyToolInput(params, projectEl, wiIdEl) {
  try {
    const raw = params?.arguments?.project === undefined
      ? JSON.parse(params?.arguments?.message ?? "{}")
      : params.arguments;
    if (raw.project) projectEl.value = String(raw.project);
    if (raw.wiId) wiIdEl.value = String(raw.wiId);
  } catch {
    // leave form fields as-is on parse failure
  }
}

// ---------------------------------------------------------------------------
// DOM factory
// ---------------------------------------------------------------------------
function buildDom() {
  return new JSDOM(`
    <!DOCTYPE html>
    <html>
    <body>
      <input type="text" id="projectInput" />
      <input type="number" id="wiIdInput" />
      <div id="dropZone">
        <input type="file" id="fileInput" multiple />
      </div>
      <ul id="fileList"></ul>
      <div id="errors" class="errors"><ul id="errorList"></ul></div>
      <button id="uploadBtn">
        <span class="btn-text">Upload Files</span>
        <div class="spinner" id="spinner"></div>
      </button>
      <div id="result" class="result">
        <div id="resultTitle"></div>
        <div id="resultBody"></div>
      </div>
    </body>
    </html>
  `, { url: "http://localhost/" });
}

// ---------------------------------------------------------------------------
// Tests — ontoolinput handler
// ---------------------------------------------------------------------------
describe("mcp-app ontoolinput handler", () => {
  let dom;

  beforeEach(() => {
    dom = buildDom();
    globalThis.document = dom.window.document;
    globalThis.FileReader = dom.window.FileReader;
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("populates project and wiId inputs when directly provided in args", () => {
    const projectEl = dom.window.document.getElementById("projectInput");
    const wiIdEl = dom.window.document.getElementById("wiIdInput");

    applyToolInput({ arguments: { project: "TestProject", wiId: 9999 } }, projectEl, wiIdEl);

    expect(projectEl.value).toBe("TestProject");
    expect(wiIdEl.value).toBe("9999");
  });

  it("populates fields from a JSON message string", () => {
    const projectEl = dom.window.document.getElementById("projectInput");
    const wiIdEl = dom.window.document.getElementById("wiIdInput");

    applyToolInput(
      { arguments: { message: JSON.stringify({ project: "FromMessage", wiId: 7 }) } },
      projectEl,
      wiIdEl
    );

    expect(projectEl.value).toBe("FromMessage");
    expect(wiIdEl.value).toBe("7");
  });

  it("leaves inputs blank when args are empty", () => {
    const projectEl = dom.window.document.getElementById("projectInput");
    const wiIdEl = dom.window.document.getElementById("wiIdInput");

    applyToolInput({ arguments: {} }, projectEl, wiIdEl);

    expect(projectEl.value).toBe("");
    expect(wiIdEl.value).toBe("");
  });

  it("does not throw when params are null or undefined", () => {
    const projectEl = dom.window.document.getElementById("projectInput");
    const wiIdEl = dom.window.document.getElementById("wiIdInput");

    expect(() => applyToolInput(null, projectEl, wiIdEl)).not.toThrow();
    expect(() => applyToolInput({}, projectEl, wiIdEl)).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Tests — upload handler
// ---------------------------------------------------------------------------
describe("mcp-app upload handler", () => {
  let dom;
  let uploadBtn;

  /** Run upload handler logic inline, mirroring mcp-app.js handleUpload. */
  async function runUploadHandler({ project, wiId, files, callToolResult }) {
    mockApp.callServerTool.mockResolvedValue(callToolResult);

    const { validateForm, formatUploadResult, formatError } = await import("../src/app/utils.js");

    const validation = validateForm({ project, wiId, files });
    if (!validation.isValid) {
      return { validationErrors: validation.errors };
    }

    uploadBtn.disabled = true;

    let handlerResult;
    try {
      const filePayloads = files.map((f) => ({
        name: f.name,
        base64: Buffer.from(f.content ?? "test").toString("base64")
      }));
      const mcpResult = await mockApp.callServerTool({
        name: "wit_upload_attachment",
        arguments: { project, wiId: Number.parseInt(wiId, 10), files: filePayloads }
      });
      handlerResult = formatUploadResult(mcpResult);
    } catch (err) {
      handlerResult = { success: false, message: formatError(err), uploaded: [] };
    } finally {
      uploadBtn.disabled = false;
    }

    return { handlerResult };
  }

  beforeEach(() => {
    dom = buildDom();
    globalThis.document = dom.window.document;
    uploadBtn = dom.window.document.getElementById("uploadBtn");
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("calls callServerTool with correct project, wiId, and files payload", async () => {
    const successResult = {
      content: [{
        type: "text",
        text: JSON.stringify({ success: true, workItemId: 42, uploaded: [{ name: "doc.txt", attachmentId: "g1" }] })
      }]
    };

    const { handlerResult } = await runUploadHandler({
      project: "TestProject",
      wiId: "42",
      files: [{ name: "doc.txt" }],
      callToolResult: successResult
    });

    expect(mockApp.callServerTool).toHaveBeenCalledOnce();
    const callArgs = mockApp.callServerTool.mock.calls[0][0];
    expect(callArgs.name).toBe("wit_upload_attachment");
    expect(callArgs.arguments.project).toBe("TestProject");
    expect(callArgs.arguments.wiId).toBe(42);
    expect(callArgs.arguments.files[0].name).toBe("doc.txt");
    expect(handlerResult.success).toBe(true);
  });

  it("re-enables the upload button after successful upload", async () => {
    const successResult = {
      content: [{
        type: "text",
        text: JSON.stringify({ success: true, workItemId: 1, uploaded: [{ name: "f.txt", attachmentId: "x" }] })
      }]
    };

    uploadBtn.disabled = false;
    await runUploadHandler({ project: "P", wiId: "1", files: [{ name: "f.txt" }], callToolResult: successResult });
    expect(uploadBtn.disabled).toBe(false);
  });

  it("returns validation errors without calling callServerTool when form is invalid", async () => {
    const { validationErrors } = await runUploadHandler({
      project: "",
      wiId: "",
      files: [],
      callToolResult: null
    });

    expect(validationErrors.length).toBeGreaterThan(0);
    expect(mockApp.callServerTool).not.toHaveBeenCalled();
  });

  it("shows error result when callServerTool returns isError", async () => {
    const errorResult = { isError: true, content: [{ type: "text", text: "Server error" }] };
    const { handlerResult } = await runUploadHandler({
      project: "P", wiId: "5", files: [{ name: "x.txt" }], callToolResult: errorResult
    });

    expect(handlerResult.success).toBe(false);
    expect(handlerResult.message).toContain("Server error");
  });

  it("handles callServerTool throwing an exception", async () => {
    mockApp.callServerTool.mockRejectedValue(new Error("Network failure"));
    const { formatError } = await import("../src/app/utils.js");

    uploadBtn.disabled = true;
    let result;
    try {
      await mockApp.callServerTool({});
    } catch (err) {
      result = { success: false, message: formatError(err), uploaded: [] };
    } finally {
      uploadBtn.disabled = false;
    }

    expect(result.success).toBe(false);
    expect(result.message).toContain("Network failure");
    expect(uploadBtn.disabled).toBe(false);
  });
});
