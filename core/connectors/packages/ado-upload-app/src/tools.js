import { z } from "zod";
import { registerAppTool, registerAppResource, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";
import { Readable } from "stream";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { readFile } from "fs/promises";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Register the two upload tools on the given MCP server.
 *
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 * @param {() => Promise<import('azure-devops-node-api').WebApi>} getADOConnection
 */
export function configureUploadTools(server, getADOConnection) {
  // -------------------------------------------------------------------------
  // Tool 1 — wit_upload_attachment_ui
  // Opens the embedded UI panel; AI can pre-fill project / wiId via args.
  // -------------------------------------------------------------------------
  registerAppTool(
    server,
    "wit_upload_attachment_ui",
    {
      description:
        "Opens an interactive UI panel to upload one or more files to an Azure DevOps work item as attachments. " +
        "Optionally pre-fill the project name and work item ID.",
      inputSchema: {
        project: z.string().optional().describe("Azure DevOps project name to pre-fill in the UI (optional)"),
        wiId: z.number().optional().describe("Work item ID to pre-fill in the UI (optional)")
      },
      _meta: {
        ui: {
          resourceUri: "ui://ado-upload-ui",
          visibility: ["model", "app"]
        }
      }
    },
    async ({ project = "", wiId = "" } = {}) => ({
      content: [
        {
          type: "text",
          text: JSON.stringify({
            project: String(project),
            wiId: String(wiId),
            message: "Select a project, enter the work item ID, and choose files to upload."
          })
        }
      ]
    })
  );

  // -------------------------------------------------------------------------
  // Tool 2 — wit_upload_attachment
  // Headless upload — called programmatically by the UI or directly by the AI.
  // -------------------------------------------------------------------------
  server.tool(
    "wit_upload_attachment",
    "Upload one or more files to an Azure DevOps work item as attachments. " +
    "Each file must be provided as a base64-encoded string together with its filename.",
    {
      project: z.string().min(1).describe("Azure DevOps project name"),
      wiId: z.number().int().positive().describe("Work item ID"),
      files: z
        .array(
          z.object({
            name: z.string().min(1).describe("File name including extension"),
            base64: z.string().min(1).describe("Base64-encoded file content (no data URI prefix)")
          })
        )
        .min(1)
        .describe("Files to upload")
    },
    async ({ project, wiId, files }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        // Upload each file and collect attachment references
        const uploaded = [];
        for (const file of files) {
          const buffer = Buffer.from(file.base64, "base64");
          const stream = Readable.from(buffer);
          const attachmentRef = await witApi.createAttachment(
            {},         // customHeaders
            stream,     // contentStream
            file.name,  // fileName
            undefined,  // uploadType (simple attachment)
            project     // project
          );
          uploaded.push({ name: file.name, id: attachmentRef.id, url: attachmentRef.url });
        }

        // Patch the work item — add AttachedFile relation for every uploaded file
        const patch = uploaded.map((att) => ({
          op: "add",
          path: "/relations/-",
          value: {
            rel: "AttachedFile",
            url: att.url,
            attributes: { comment: "Uploaded via ADO Upload MCP App" }
          }
        }));

        await witApi.updateWorkItem({}, patch, wiId, project);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  success: true,
                  workItemId: wiId,
                  project,
                  uploaded: uploaded.map((a) => ({ name: a.name, attachmentId: a.id }))
                },
                null,
                2
              )
            }
          ]
        };
      } catch (error) {
        return {
          content: [{ type: "text", text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );
}

/**
 * Register the UI resource that serves the bundled single-file HTML app.
 *
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureUiResource(server) {
  registerAppResource(
    server,
    "ADO Upload UI",
    "ui://ado-upload-ui",
    {},
    async (uri) => {
      // Use built HTML from dist if it exists, otherwise fall back to src for dev
      let htmlPath = join(__dirname, "..", "dist", "src", "app", "index.html");
      try {
        await readFile(htmlPath, "utf-8");
      } catch {
        // Fallback to src for local dev
        htmlPath = join(__dirname, "..", "src", "app", "index.html");
      }
      const htmlContent = await readFile(htmlPath, "utf-8");
      return {
        contents: [
          {
            uri: uri.href,
            mimeType: RESOURCE_MIME_TYPE,
            text: htmlContent
          }
        ]
      };
    }
  );
}
