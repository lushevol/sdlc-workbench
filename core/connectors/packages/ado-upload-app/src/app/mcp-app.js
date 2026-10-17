import { App } from "@modelcontextprotocol/ext-apps";
import { readFileAsBase64, validateForm, formatUploadResult, formatError, formatFileSize } from "./utils.js";

const app = new App({ name: "ADO Upload App", version: "1.0.0" });

// ---------------------------------------------------------------------------
// DOM references (resolved after DOMContentLoaded)
// ---------------------------------------------------------------------------
let projectInput, wiIdInput, fileInput, fileList, uploadBtn, errorsEl, errorList, resultEl, resultTitle, resultBody, dropZone;

/** Currently selected files (kept in sync with the file picker and drop zone) */
let selectedFiles = [];

function initDom() {
  projectInput = document.getElementById("projectInput");
  wiIdInput = document.getElementById("wiIdInput");
  fileInput = document.getElementById("fileInput");
  fileList = document.getElementById("fileList");
  uploadBtn = document.getElementById("uploadBtn");
  errorsEl = document.getElementById("errors");
  errorList = document.getElementById("errorList");
  resultEl = document.getElementById("result");
  resultTitle = document.getElementById("resultTitle");
  resultBody = document.getElementById("resultBody");
  dropZone = document.getElementById("dropZone");
}

// ---------------------------------------------------------------------------
// File list rendering
// ---------------------------------------------------------------------------
function renderFileList() {
  fileList.innerHTML = "";
  for (const [index, file] of selectedFiles.entries()) {
    const li = document.createElement("li");

    const nameSpan = document.createElement("span");
    nameSpan.className = "file-name";
    nameSpan.textContent = file.name;

    const sizeSpan = document.createElement("span");
    sizeSpan.className = "file-size";
    sizeSpan.textContent = formatFileSize(file.size);

    const removeBtn = document.createElement("button");
    removeBtn.className = "remove-file";
    removeBtn.textContent = "×";
    removeBtn.setAttribute("aria-label", `Remove ${file.name}`);
    removeBtn.addEventListener("click", () => {
      selectedFiles.splice(index, 1);
      renderFileList();
    });

    li.append(nameSpan, sizeSpan, removeBtn);
    fileList.append(li);
  }
}

// ---------------------------------------------------------------------------
// Validation error display
// ---------------------------------------------------------------------------
function showErrors(errors) {
  errorList.innerHTML = "";
  for (const msg of errors) {
    const li = document.createElement("li");
    li.textContent = msg;
    errorList.append(li);
  }
  errorsEl.classList.add("visible");
}

function clearErrors() {
  errorsEl.classList.remove("visible");
  errorList.innerHTML = "";
}

// ---------------------------------------------------------------------------
// Result display
// ---------------------------------------------------------------------------
function showResult({ success, message, uploaded }) {
  resultEl.className = `result ${success ? "success" : "error"}`;
  resultTitle.textContent = success ? "Upload successful" : "Upload failed";
  resultBody.innerHTML = "";

  const msgP = document.createElement("p");
  msgP.textContent = message;
  resultBody.append(msgP);

  if (success && uploaded.length > 0) {
    const ul = document.createElement("ul");
    ul.className = "result-files";
    for (const f of uploaded) {
      const li = document.createElement("li");
      li.textContent = f.name;
      ul.append(li);
    }
    resultBody.append(ul);
  }
}

function clearResult() {
  resultEl.className = "result";
  resultTitle.textContent = "";
  resultBody.innerHTML = "";
}

// ---------------------------------------------------------------------------
// MCP App lifecycle hooks
// ---------------------------------------------------------------------------

/**
 * Called by the host when the tool is invoked (optionally with pre-fill args).
 * Args shape: { project?: string, wiId?: string|number }
 */
app.ontoolinput = (params) => {
  initDom();
  try {
    const raw = params?.arguments?.project === undefined
      ? JSON.parse(params?.arguments?.message ?? "{}")
      : params.arguments;
    // raw is now either the direct arguments object or a parsed message payload

    if (raw.project) projectInput.value = String(raw.project);
    if (raw.wiId) wiIdInput.value = String(raw.wiId);
  } catch {
    // Args not parseable — leave fields as-is
  }
};

app.onteardown = async () => ({});

// ---------------------------------------------------------------------------
// Main upload handler
// ---------------------------------------------------------------------------
async function handleUpload() {
  clearErrors();
  clearResult();

  const project = projectInput.value.trim();
  const wiId = wiIdInput.value.trim();

  const validation = validateForm({ project, wiId, files: selectedFiles });
  if (!validation.isValid) {
    showErrors(validation.errors);
    return;
  }

  // Enter loading state
  uploadBtn.disabled = true;
  uploadBtn.classList.add("loading");

  try {
    // Read all files as base64 in parallel
    const filePayloads = await Promise.all(
      selectedFiles.map(async (file) => ({
        name: file.name,
        base64: await readFileAsBase64(file)
      }))
    );

    // Call back to the MCP server tool
    const result = await app.callServerTool({
      name: "wit_upload_attachment",
      arguments: {
        project,
        wiId: Number.parseInt(wiId, 10),
        files: filePayloads
      }
    });

    showResult(formatUploadResult(result));
  } catch (err) {
    showResult({ success: false, message: formatError(err), uploaded: [] });
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.classList.remove("loading");
  }
}

// ---------------------------------------------------------------------------
// Wire up DOM events after content is loaded
// ---------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  initDom();

  // File input change
  fileInput.addEventListener("change", () => {
    selectedFiles = [...selectedFiles, ...Array.from(fileInput.files)];
    // Reset the input so the same file can be re-added if removed first
    fileInput.value = "";
    renderFileList();
  });

  // Drag-and-drop
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });
  dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    const dropped = Array.from(e.dataTransfer?.files ?? []);
    if (dropped.length > 0) {
      selectedFiles = [...selectedFiles, ...dropped];
      renderFileList();
    }
  });

  // Upload button
  uploadBtn.addEventListener("click", handleUpload);
});

await app.connect();
