package com.example.migration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Map;

/** Local, self-contained output. All source values are rendered as escaped text. */
public final class VerificationReport {
    private VerificationReport() {}

    public static void write(Path outputDir, Map<String, Object> report) throws IOException {
        if (report == null) throw new IllegalArgumentException("Report is required");
        Files.createDirectories(outputDir);
        for (String name : List.of("report.json", "report.html", "report.md")) {
            if (Files.exists(outputDir.resolve(name))) {
                throw new IOException("Report output already exists; select a new run directory");
            }
        }
        ObjectMapper mapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
        String json = mapper.writeValueAsString(report) + "\n";
        String html = html(report, mapper);
        String markdown = markdown(report, mapper);
        atomicWrite(outputDir.resolve("report.json"), json);
        atomicWrite(outputDir.resolve("report.html"), html);
        atomicWrite(outputDir.resolve("report.md"), markdown);
    }

    private static String html(Map<String, Object> report, ObjectMapper mapper) throws IOException {
        StringBuilder out = new StringBuilder("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">")
            .append("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")
            .append("<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src 'unsafe-inline'\">")
            .append("<title>EMS2 to CES SDK verification</title><style>")
            .append("body{font:16px/1.5 system-ui,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#18222d}")
            .append("h1,h2,h3{line-height:1.25}table{border-collapse:collapse;width:100%;margin:1rem 0}")
            .append("th,td{border:1px solid #cbd5df;padding:.55rem;text-align:left;vertical-align:top;overflow-wrap:anywhere}")
            .append("pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f8;padding:1rem;border:1px solid #d8dfe5}")
            .append(".verdict{border-left:5px solid #245c8c;padding:.5rem 1rem;background:#edf4fa}")
            .append("details{margin:1rem 0}summary{cursor:pointer;font-weight:600}.limit{color:#4b5563}")
            .append("</style></head><body><h1>EMS2 to CES SDK verification</h1>");
        Object status = report.getOrDefault("status", report.getOrDefault("verdict", "UNKNOWN"));
        out.append("<div class=\"verdict\"><p><strong>Result: ").append(escape(status)).append("</strong></p>")
            .append("<p>Mode: ").append(escape(report.getOrDefault("mode", "UNKNOWN"))).append("</p>")
            .append("<p>Complete migration verified: ").append(escape(report.getOrDefault("migrationVerified", false)))
            .append("</p></div><p class=\"limit\">Percentages apply only to their declared populations and predicates. ")
            .append("Zero denominators, failed reads, and unassessed scope do not establish full migration coverage.</p>");
        appendSection(out, "Scope", report.get("scope"), mapper);
        appendSection(out, "Metrics", report.get("metrics"), mapper);
        appendSection(out, "Open gaps and evidence limits", report.get("gaps"), mapper);
        List<?> accounts = report.get("accounts") instanceof List<?> list ? list : List.of();
        out.append("<h2>Account outcomes</h2><table><thead><tr><th>Account</th><th>Status</th></tr></thead><tbody>");
        for (Object raw : accounts) {
            if (raw instanceof Map<?, ?> account) {
                out.append("<tr><td>").append(escape(account.get("userId"))).append("</td><td>")
                    .append(escape(account.get("status"))).append("</td></tr>");
            } else {
                out.append("<tr><td colspan=\"2\">").append(escape(raw)).append("</td></tr>");
            }
        }
        out.append("</tbody></table>");
        int number = 0;
        for (Object raw : accounts) {
            out.append("<h3>Account ").append(++number).append("</h3>");
            if (raw instanceof Map<?, ?> account) {
                out.append("<p>Account: ").append(escape(account.get("userId"))).append("; status: ")
                    .append(escape(account.get("status"))).append("</p>");
                appendSection(out, "Comparison and exact differences", account.get("comparison"), mapper);
                appendSection(out, "Source errors", account.get("errors"), mapper);
            }
            out.append("<details><summary>Complete account evidence</summary><pre>")
                .append(escape(mapper.writeValueAsString(raw))).append("</pre></details>");
        }
        out.append("<details><summary>Complete report and source bindings</summary><pre>")
            .append(escape(mapper.writeValueAsString(report))).append("</pre></details>")
            .append("<p><a href=\"report.json\">Complete JSON report</a> · <a href=\"report.md\">Markdown report</a></p>")
            .append("</body></html>\n");
        return out.toString();
    }

    private static void appendSection(StringBuilder out, String title, Object value,
                                      ObjectMapper mapper) throws IOException {
        out.append("<h2>").append(escape(title)).append("</h2><pre>")
            .append(escape(mapper.writeValueAsString(value))).append("</pre>");
    }

    private static String markdown(Map<String, Object> report, ObjectMapper mapper) throws IOException {
        StringBuilder out = new StringBuilder("---\nwriting_review:\n  standard: ASD-STE100\n")
            .append("  automated_check: NOT_RUN\n  asd_review: PENDING\n  reviewer: null\n  reviewed_at: null\n")
            .append("  limitations:\n    - Automated checks do not check the complete approved dictionary or grammar rules.\n")
            .append("---\n\n# EMS2 to CES SDK verification\n\n");
        out.append("**Result: ").append(markdownText(report.getOrDefault("status", report.getOrDefault("verdict", "UNKNOWN"))))
            .append(".**\n\nMode: ").append(markdownText(report.getOrDefault("mode", "UNKNOWN")))
            .append(". Complete migration verified: ").append(markdownText(report.getOrDefault("migrationVerified", false)))
            .append(".\n\nPercentages apply only to declared scope. Failed reads and zero denominators do not establish complete coverage.\n\n");
        appendMarkdownSection(out, "Scope", report.get("scope"), mapper);
        appendMarkdownSection(out, "Metrics", report.get("metrics"), mapper);
        appendMarkdownSection(out, "Open gaps and evidence limits", report.get("gaps"), mapper);
        List<?> accounts = report.get("accounts") instanceof List<?> list ? list : List.of();
        int number = 0;
        for (Object account : accounts) {
            appendMarkdownSection(out, "Account " + (++number), account, mapper);
        }
        appendMarkdownSection(out, "Complete source bindings and result", report, mapper);
        return out.toString();
    }

    private static void appendMarkdownSection(StringBuilder out, String title, Object value,
                                               ObjectMapper mapper) throws IOException {
        String json = mapper.writeValueAsString(value);
        String fence = "`".repeat(Math.max(3, longestBacktickRun(json) + 1));
        out.append("## ").append(title).append("\n\n").append(fence).append("json\n")
            .append(json).append("\n").append(fence).append("\n\n");
    }

    private static int longestBacktickRun(String text) {
        int longest = 0;
        int current = 0;
        for (int i = 0; i < text.length(); i++) {
            current = text.charAt(i) == '`' ? current + 1 : 0;
            longest = Math.max(longest, current);
        }
        return longest;
    }

    private static String markdownText(Object value) {
        return escape(value).replace("\\", "\\\\").replace("\r", "\\r").replace("\n", "\\n")
            .replace("*", "\\*").replace("_", "\\_").replace("`", "\\`")
            .replace("[", "\\[").replace("]", "\\]").replace("|", "\\|");
    }

    private static String escape(Object value) {
        return String.valueOf(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;");
    }

    private static void atomicWrite(Path target, String content) throws IOException {
        Path temporary = Files.createTempFile(target.getParent(), ".verification-", ".tmp");
        try {
            Files.writeString(temporary, content, StandardCharsets.UTF_8);
            try {
                Files.move(temporary, target, StandardCopyOption.ATOMIC_MOVE);
            } catch (AtomicMoveNotSupportedException exception) {
                Files.move(temporary, target);
            }
        } finally {
            Files.deleteIfExists(temporary);
        }
    }
}
