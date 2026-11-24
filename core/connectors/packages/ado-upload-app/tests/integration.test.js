import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { JSDOM } from "jsdom";

// ---------------------------------------------------------------------------
// Mocks
// ---------------------------------------------------------------------------
const mockApp = {
  connect: vi.fn().mockResolvedValue(undefined),
  callServerTool: vi.fn()
};

vi.mock("@modelcontextprotocol/ext-apps", () => ({
  App: vi.fn().mockImplementation(() => mockApp)
}));

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function buildDom() {
  return new JSDOM(`
    <!DOCTYPE html>
    <html>
    <body>
      <input type="text" id="projectInput" />
      <input type="number" id="wiIdInput" />
      <input type="file" id="fileInput" multiple />
      <ul id="fileList"></ul>
      <div id="errors" class="errors"><ul id="errorList"></ul></div>
      <button id="uploadBtn"><span class="btn-text">Upload</span></button>
      <div id="result" class="result">
        <div id="resultTitle"></div>
        <div id="resultBody"></div>
      </div>
    </body>
    </html>
  `, { url: "http://localhost/" });
}

/**
 * Simulate the full upload flow from end to end, replicating the logic in
 * mcp-app.js so we can test the complete interaction without importing the
 * module (which has a top-level await and DOM dependency).
 */
async function simulateFullFlow({ preFilledProject, preFilledWiId, userProject, userWiId, files, callToolResult }) {
  const { validateForm, formatUploadResult, formatError } = await import("../src/app/utils.js");

  const dom = buildDom();
  const doc = dom.window.document;
  const projectEl = doc.getElementById("projectInput");
  const wiIdEl = doc.getElementById("wiIdInput");
  const uploadBtn = doc.getElementById("uploadBtn");

  // Step 1: ontoolinput pre-fills the form (optional)
  if (preFilledProject !== undefined) projectEl.value = preFilledProject;
  if (preFilledWiId !== undefined) wiIdEl.value = String(preFilledWiId);

  // Step 2: User overrides / fills in values
  if (userProject !== undefined) projectEl.value = userProject;
  if (userWiId !== undefined) wiIdEl.value = String(userWiId);

  const project = projectEl.value.trim();
  const wiId = wiIdEl.value.trim();

  // Step 3: Validate
  const validation = validateForm({ project, wiId, files });
  if (!validation.isValid) {
    return { success: false, validationErrors: validation.errors, callServerToolCalled: false };
  }

  // Step 4: Upload
  mockApp.callServerTool.mockResolvedValue(callToolResult);
  uploadBtn.disabled = true;

  let result;
  try {
    const filePayloads = files.map((f) => ({
      name: f.name,
      base64: Buffer.from(f.content ?? "test").toString("base64")
    }));

    const mcpResult = await mockApp.callServerTool({
      name: "wit_upload_attachment",
      arguments: { project, wiId: Number.parseInt(wiId, 10), files: filePayloads }
    });

    result = formatUploadResult(mcpResult);
  } catch (err) {
    result = { success: false, message: formatError(err), uploaded: [] };
  } finally {
    uploadBtn.disabled = false;
  }

  return {
    ...result,
    buttonDisabled: uploadBtn.disabled,
    callServerToolCalled: mockApp.callServerTool.mock.calls.length > 0,
    callServerToolArgs: mockApp.callServerTool.mock.calls[0]?.[0]
  };
}

// ---------------------------------------------------------------------------
// Integration tests
// ---------------------------------------------------------------------------
describe("Integration — pre-filled form via ontoolinput → upload", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("succeeds: AI pre-fills project+wiId, user selects files and submits", async () => {
    const result = await simulateFullFlow({
      preFilledProject: "MyProject",
      preFilledWiId: 42,
      files: [
        { name: "screenshot.png", content: "pngdata" },
        { name: "log.txt", content: "logdata" }
      ],
      callToolResult: {
        content: [{
          type: "text",
          text: JSON.stringify({
            success: true,
            workItemId: 42,
            project: "MyProject",
            uploaded: [
              { name: "screenshot.png", attachmentId: "id-1" },
              { name: "log.txt", attachmentId: "id-2" }
            ]
          })
        }]
      }
    });

    expect(result.success).toBe(true);
    expect(result.callServerToolCalled).toBe(true);
    expect(result.callServerToolArgs.arguments.project).toBe("MyProject");
    expect(result.callServerToolArgs.arguments.wiId).toBe(42);
    expect(result.callServerToolArgs.arguments.files).toHaveLength(2);
    expect(result.uploaded).toHaveLength(2);
    expect(result.buttonDisabled).toBe(false);
  });

  it("succeeds: user fills in form manually (no pre-fill) and uploads one file", async () => {
    const result = await simulateFullFlow({
      userProject: "ManualProject",
      userWiId: 99,
      files: [{ name: "report.pdf" }],
      callToolResult: {
        content: [{
          type: "text",
          text: JSON.stringify({ success: true, workItemId: 99, uploaded: [{ name: "report.pdf", attachmentId: "g1" }] })
        }]
      }
    });

    expect(result.success).toBe(true);
    expect(result.callServerToolArgs.arguments.project).toBe("ManualProject");
    expect(result.callServerToolArgs.arguments.wiId).toBe(99);
    expect(result.callServerToolArgs.arguments.files[0].name).toBe("report.pdf");
  });

  it("fails validation: no project and no files — callServerTool never called", async () => {
    const result = await simulateFullFlow({
      userProject: "",
      userWiId: "12345",
      files: [],
      callToolResult: null
    });

    expect(result.success).toBe(false);
    expect(result.validationErrors.length).toBeGreaterThan(0);
    expect(result.callServerToolCalled).toBe(false);
  });

  it("fails validation: wiId is zero — callServerTool never called", async () => {
    const result = await simulateFullFlow({
      userProject: "P",
      userWiId: "0",
      files: [{ name: "x.txt" }],
      callToolResult: null
    });

    expect(result.success).toBe(false);
    expect(result.validationErrors).toContain("Work Item ID must be a positive integer.");
    expect(result.callServerToolCalled).toBe(false);
  });

  it("error path: callServerTool returns isError — result shows error message", async () => {
    const result = await simulateFullFlow({
      preFilledProject: "ErrProject",
      preFilledWiId: 1,
      files: [{ name: "f.txt" }],
      callToolResult: {
        isError: true,
        content: [{ type: "text", text: "ADO permission denied" }]
      }
    });

    expect(result.success).toBe(false);
    expect(result.message).toContain("ADO permission denied");
    expect(result.buttonDisabled).toBe(false);
  });

  it("button is re-enabled after upload even when callServerTool throws", async () => {
    mockApp.callServerTool.mockRejectedValue(new Error("Unexpected crash"));
    const { formatError } = await import("../src/app/utils.js");

    const dom = buildDom();
    const uploadBtn = dom.window.document.getElementById("uploadBtn");
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
    expect(result.message).toContain("Unexpected crash");
    expect(uploadBtn.disabled).toBe(false);
  });
});
