import { describe, it, expect, vi, beforeEach } from "vitest";
import { readFileAsBase64, validateForm, formatUploadResult, formatError, formatFileSize } from "../src/app/utils.js";

// ---------------------------------------------------------------------------
// readFileAsBase64
// ---------------------------------------------------------------------------
describe("readFileAsBase64", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("resolves with base64 string stripped of the data URI prefix", async () => {
    const fakeDataUrl = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScAAAAAElFTkSuQmCC";
    const mockFile = { name: "test.png" };

    const mockReader = {
      onload: null,
      onerror: null,
      readAsDataURL: vi.fn(function () {
        this.onload({ target: { result: fakeDataUrl } });
      })
    };
    vi.stubGlobal("FileReader", vi.fn(function() { return mockReader; }));

    const result = await readFileAsBase64(mockFile);
    expect(result).toBe("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScAAAAAElFTkSuQmCC");
  });

  it("strips prefix for non-image MIME types", async () => {
    const fakeDataUrl = "data:text/plain;base64,SGVsbG8gV29ybGQ=";
    const mockFile = { name: "hello.txt" };

    const mockReader = {
      onload: null,
      onerror: null,
      readAsDataURL: vi.fn(function () {
        this.onload({ target: { result: fakeDataUrl } });
      })
    };
    vi.stubGlobal("FileReader", vi.fn(function() { return mockReader; }));

    const result = await readFileAsBase64(mockFile);
    expect(result).toBe("SGVsbG8gV29ybGQ=");
  });

  it("resolves with empty string when data URL has no comma (edge case)", async () => {
    const mockFile = { name: "oddfile.bin" };
    const mockReader = {
      onload: null,
      onerror: null,
      readAsDataURL: vi.fn(function () {
        this.onload({ target: { result: "no-comma-in-this-result" } });
      })
    };
    vi.stubGlobal("FileReader", vi.fn(function() { return mockReader; }));

    const result = await readFileAsBase64(mockFile);
    expect(result).toBe(""); // ?? "" fallback
  });

  it("rejects the promise when FileReader encounters an error", async () => {
    const mockFile = { name: "bad.bin" };
    const mockReader = {
      onload: null,
      onerror: null,
      readAsDataURL: vi.fn(function () {
        this.onerror();
      })
    };
    vi.stubGlobal("FileReader", vi.fn(function() { return mockReader; }));

    await expect(readFileAsBase64(mockFile)).rejects.toThrow("Failed to read file: bad.bin");
  });
});

// ---------------------------------------------------------------------------
// validateForm
// ---------------------------------------------------------------------------
describe("validateForm", () => {
  it("returns isValid true when all inputs are correct", () => {
    const result = validateForm({ project: "TestProject", wiId: "12345", files: [{}] });
    expect(result.isValid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  it("returns error when project is empty string", () => {
    const result = validateForm({ project: "", wiId: "12345", files: [{}] });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Project name is required.");
  });

  it("returns error when project is only whitespace", () => {
    const result = validateForm({ project: "   ", wiId: "12345", files: [{}] });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Project name is required.");
  });

  it("returns error when wiId is empty string", () => {
    const result = validateForm({ project: "TestProject", wiId: "", files: [{}] });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Work Item ID is required.");
  });

  it("returns error when wiId is 0", () => {
    const result = validateForm({ project: "TestProject", wiId: "0", files: [{}] });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Work Item ID must be a positive integer.");
  });

  it("returns error when wiId is a decimal", () => {
    const result = validateForm({ project: "TestProject", wiId: "12.5", files: [{}] });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("Work Item ID must be a positive integer.");
  });

  it("returns error when files array is empty", () => {
    const result = validateForm({ project: "TestProject", wiId: "12345", files: [] });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("At least one file must be selected.");
  });

  it("returns error when files is null", () => {
    const result = validateForm({ project: "TestProject", wiId: "12345", files: null });
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain("At least one file must be selected.");
  });

  it("accumulates multiple errors", () => {
    const result = validateForm({ project: "", wiId: "", files: [] });
    expect(result.isValid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(1);
  });
});

// ---------------------------------------------------------------------------
// formatUploadResult
// ---------------------------------------------------------------------------
describe("formatUploadResult", () => {
  it("returns success with uploaded file list on successful result", () => {
    const callResult = {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          workItemId: 123,
          project: "TestProject",
          uploaded: [{ name: "file.txt", attachmentId: "abc" }]
        })
      }]
    };
    const result = formatUploadResult(callResult);
    expect(result.success).toBe(true);
    expect(result.message).toContain("1 file");
    expect(result.message).toContain("#123");
    expect(result.uploaded).toHaveLength(1);
    expect(result.uploaded[0].name).toBe("file.txt");
  });

  it("uses plural 'files' when multiple files uploaded", () => {
    const callResult = {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          workItemId: 555,
          uploaded: [
            { name: "a.txt", attachmentId: "1" },
            { name: "b.png", attachmentId: "2" }
          ]
        })
      }]
    };
    const result = formatUploadResult(callResult);
    expect(result.success).toBe(true);
    expect(result.message).toContain("2 files");
  });

  it("returns failure with message when isError is true", () => {
    const callResult = { isError: true, content: [{ type: "text", text: "ADO API error" }] };
    const result = formatUploadResult(callResult);
    expect(result.success).toBe(false);
    expect(result.message).toBe("ADO API error");
    expect(result.uploaded).toHaveLength(0);
  });

  it("returns failure with fallback when isError true and content text is null", () => {
    const result = formatUploadResult({ isError: true, content: [{ type: "text", text: null }] });
    expect(result.success).toBe(false);
    expect(result.message).toBe("Upload failed with an unknown error.");
  });

  it("handles null callToolResult gracefully", () => {
    const result = formatUploadResult(null);
    expect(result.success).toBe(false);
  });

  it("handles success result with no uploaded key — uses ?? 0 and || [] fallbacks", () => {
    const callResult = {
      content: [{
        type: "text",
        text: JSON.stringify({ success: true, workItemId: 7 })
        // no 'uploaded' key → parsed.uploaded is undefined
      }]
    };
    const result = formatUploadResult(callResult);
    expect(result.success).toBe(true);
    expect(result.message).toContain("0 files");
    expect(result.uploaded).toEqual([]);
  });

  it("returns failure when result has no content", () => {
    const result = formatUploadResult({ isError: true });
    expect(result.success).toBe(false);
    expect(result.message).toBeTruthy();
  });

  it("returns failure on unparseable content", () => {
    const result = formatUploadResult({ content: [{ type: "text", text: "not json" }] });
    expect(result.success).toBe(false);
  });

  it("handles empty uploaded array gracefully", () => {
    const callResult = {
      content: [{
        type: "text",
        text: JSON.stringify({ success: true, workItemId: 1, uploaded: [] })
      }]
    };
    const result = formatUploadResult(callResult);
    expect(result.success).toBe(true);
    expect(result.uploaded).toHaveLength(0);
    expect(result.message).toContain("0 files");
  });
});

// ---------------------------------------------------------------------------
// formatError
// ---------------------------------------------------------------------------
describe("formatError", () => {
  it("returns the message for Error objects", () => {
    expect(formatError(new Error("something went wrong"))).toBe("something went wrong");
  });

  it("returns the string unchanged for string errors", () => {
    expect(formatError("network timeout")).toBe("network timeout");
  });

  it("returns fallback for null", () => {
    expect(formatError(null)).toBe("An unknown error occurred.");
  });

  it("returns fallback for undefined", () => {
    expect(formatError(undefined)).toBe("An unknown error occurred.");
  });

  it("returns JSON string for plain objects", () => {
    const result = formatError({ code: 500, msg: "fail" });
    expect(result).toContain("500");
  });
});

// ---------------------------------------------------------------------------
// formatFileSize
// ---------------------------------------------------------------------------
describe("formatFileSize", () => {
  it("formats bytes correctly", () => {
    expect(formatFileSize(512)).toBe("512 B");
  });

  it("formats kilobytes correctly", () => {
    expect(formatFileSize(2048)).toBe("2.0 KB");
  });

  it("formats megabytes correctly", () => {
    expect(formatFileSize(1_572_864)).toBe("1.5 MB");
  });
});
