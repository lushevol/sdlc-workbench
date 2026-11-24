/**
 * Utility functions for the ADO Work Item File Upload MCP App.
 */

/**
 * Read a File object and resolve with its base64-encoded content
 * (without the data URI prefix, e.g. without "data:image/png;base64,").
 *
 * @param {File} file - Browser File object
 * @returns {Promise<string>} Raw base64 string
 */
export function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target.result;
      // dataUrl format: "data:<mime>;base64,<content>"
      const base64 = dataUrl.split(",")[1] ?? "";
      resolve(base64);
    };
    reader.onerror = () => reject(new Error(`Failed to read file: ${file.name}`));
    reader.readAsDataURL(file);
  });
}

/**
 * Validate the upload form inputs.
 *
 * @param {{ project: string, wiId: string, files: FileList|File[] }} params
 * @returns {{ isValid: boolean, errors: string[] }}
 */
export function validateForm({ project, wiId, files }) {
  const errors = [];

  if (!project?.trim()) {
    errors.push("Project name is required.");
  }

  const parsedWiId = Number.parseInt(wiId, 10);
  if (!wiId || wiId.toString().trim() === "") {
    errors.push("Work Item ID is required.");
  } else if (!Number.isInteger(Number(wiId)) || parsedWiId <= 0) {
    errors.push("Work Item ID must be a positive integer.");
  }

  if (!files || files.length === 0) {
    errors.push("At least one file must be selected.");
  }

  return { isValid: errors.length === 0, errors };
}

/**
 * Format the result of a callServerTool response for display.
 *
 * @param {Object} callToolResult - The result from app.callServerTool()
 * @returns {{ success: boolean, message: string, uploaded: Array }}
 */
export function formatUploadResult(callToolResult) {
  if (callToolResult?.isError) {
    const message =
      callToolResult?.content?.[0]?.text || "Upload failed with an unknown error.";
    return { success: false, message, uploaded: [] };
  }

  try {
    const text = callToolResult?.content?.[0]?.text || "{}";
    const parsed = JSON.parse(text);
    if (parsed.success) {
      const count = parsed.uploaded?.length ?? 0;
      return {
        success: true,
        message: `Successfully uploaded ${count} ${count === 1 ? "file" : "files"} to work item #${parsed.workItemId}.`,
        uploaded: parsed.uploaded || []
      };
    }
    return { success: false, message: parsed.message || "Upload failed.", uploaded: [] };
  } catch {
    return { success: false, message: "Unexpected response from server.", uploaded: [] };
  }
}

/**
 * Format an error value into a human-readable string.
 *
 * @param {Error|string|unknown} error
 * @returns {string}
 */
export function formatError(error) {
  if (!error) return "An unknown error occurred.";
  if (error instanceof Error) return error.message;
  if (typeof error === "string") return error;
  return JSON.stringify(error);
}

/**
 * Format a file size in bytes as a human-readable string (e.g. "1.2 MB").
 *
 * @param {number} bytes
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
