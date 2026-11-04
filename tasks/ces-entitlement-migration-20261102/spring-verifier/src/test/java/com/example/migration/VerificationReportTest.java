package com.example.migration;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class VerificationReportTest {
    @TempDir
    Path temporary;

    @Test
    void writesCompleteSelfContainedReportsWithUnknownScopeVisible() throws Exception {
        Map<String, Object> report = Map.of(
            "status", "INCOMPLETE", "mode", "replay", "migrationVerified", false,
            "scope", Map.of("populationComplete", false, "accountCount", 1),
            "metrics", Map.of("assessed", 0, "failed", 1),
            "gaps", List.of("Population unknown", "CES request unavailable"),
            "accounts", List.of(Map.of("userId", "account-a", "status", "ERROR", "errors", List.of("HTTP_401")))
        );
        VerificationReport.write(temporary, report);
        var json = new ObjectMapper().readTree(temporary.resolve("report.json").toFile());
        assertEquals("INCOMPLETE", json.path("status").asText());
        assertFalse(json.path("migrationVerified").asBoolean());
        assertEquals("HTTP_401", json.path("accounts").get(0).path("errors").get(0).asText());
        String html = Files.readString(temporary.resolve("report.html"));
        assertTrue(html.contains("Population unknown"));
        assertTrue(html.contains("HTTP_401"));
        assertFalse(html.contains("<script"));
        assertFalse(html.contains("https://"));
        assertTrue(Files.readString(temporary.resolve("report.md")).contains("INCOMPLETE"));
    }

    @Test
    void accountNamesPermissionsAndErrorsCannotInjectHtmlOrBreakMarkdownFences() throws Exception {
        String hostile = "</pre><script>alert('x')</script>```";
        Map<String, Object> report = Map.of(
            "status", hostile, "mode", "live", "gaps", List.of(hostile),
            "accounts", List.of(Map.of("userId", hostile, "status", "DIFFERENT", "comparison", Map.of("differences", List.of(hostile))))
        );
        VerificationReport.write(temporary, report);
        String html = Files.readString(temporary.resolve("report.html"));
        assertFalse(html.contains("<script>"));
        assertTrue(html.contains("&lt;script&gt;"));
        assertTrue(html.contains("&lt;/pre&gt;"));
        assertTrue(html.contains("Content-Security-Policy"));
        String markdown = Files.readString(temporary.resolve("report.md"));
        assertTrue(markdown.contains("````json"));
        assertTrue(markdown.contains("\\`\\`\\`"));
        assertTrue(new ObjectMapper().readTree(temporary.resolve("report.json").toFile()).path("status").asText().equals(hostile));
    }

    @Test
    void refusesToOverwriteExistingEvidence() throws Exception {
        Path existing = temporary.resolve("report.json");
        Files.writeString(existing, "original evidence");
        assertThrows(java.io.IOException.class, () -> VerificationReport.write(temporary, Map.of("status", "MATCH")));
        assertEquals("original evidence", Files.readString(existing));
        assertFalse(Files.exists(temporary.resolve("report.html")));
    }
}
