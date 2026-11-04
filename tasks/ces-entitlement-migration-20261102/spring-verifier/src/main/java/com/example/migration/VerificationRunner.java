package com.example.migration;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.env.Environment;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.time.Duration;
import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/** Runs every declared account, retaining each completed result before continuing. */
public final class VerificationRunner {
    static final String BASE = "b0aa82005e7f14202f85f5ef583f25e42da9eeb3";
    static final String HEAD = "fd9a157e260850b6d9efa10da3223950ea61133a";
    private final ObjectMapper mapper = new ObjectMapper();

    public int run(Environment environment) throws Exception {
        Path parent = Path.of(environment.getProperty("verification.output", "reports")).toAbsolutePath();
        Files.createDirectories(parent);
        Path output = parent.resolve(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss").withZone(java.time.ZoneOffset.UTC)
            .format(Instant.now()) + "-" + UUID.randomUUID().toString().substring(0, 8));
        Files.createDirectory(output);
        Files.createDirectory(output.resolve("accounts"));
        Map<String, Object> report = new LinkedHashMap<>();
        report.put("startedAt", Instant.now().toString());
        report.put("migrationVerified", false);
        report.put("scope", "Exact original SDK lookup output for the declared account list and configured entities");
        report.put("limits", List.of("This measures SDK-map parity; it does not certify all enterprise accounts or unassigned role definitions.",
            "Resolved data policies and real consumer authentication, logout, token renewal, and allowed/denied journeys need separate evidence.",
            "A completeness declaration records operator input; it does not authenticate its business authority."));
        report.put("gaps", new ArrayList<>(List.of("Complete role definitions beyond assigned accounts remain outside this measurement.",
            "Resolved data restrictions are not returned by either SDK map.", "Downstream business journeys are not executed by this command.")));
        List<Map<String, Object>> accounts = new ArrayList<>();
        report.put("accounts", accounts);
        ReplayServer replay = null;
        int exit;
        try {
            String mode = environment.getProperty("verification.mode", "replay");
            if (!List.of("replay", "live").contains(mode)) throw new IllegalArgumentException("INVALID_MODE");
            report.put("mode", mode);
            Path usersPath = Path.of(required(environment, "verification.users"));
            List<String> users = readUsers(usersPath);
            boolean complete = populationComplete(environment, mode);
            String inventorySource = populationSource(environment, mode);
            report.put("populationDeclaredComplete", complete);
            report.put("populationSource", inventorySource);
            report.put("populationFileSha256", sha256(usersPath));
            report.put("declaredAccounts", users);
            Path manifestPath = Path.of(environment.getProperty("verification.manifest", "lib/sdk-manifest.json"));
            Map<String, Object> manifest = mapper.readValue(manifestPath.toFile(), new TypeReference<>() {});
            Map<String, Object> baselineArtifact = artifact(manifest, "baseline", BASE);
            Map<String, Object> candidateArtifact = artifact(manifest, "candidate", HEAD);
            if (baselineArtifact.get("sha256").equals(candidateArtifact.get("sha256")))
                throw new IllegalArgumentException("SDK_ARTIFACTS_MUST_DIFFER");
            report.put("artifacts", Map.of("baseline", baselineArtifact, "candidate", candidateArtifact));
            report.put("artifactManifestSha256", sha256(manifestPath));
            Path mappingPath = Path.of(required(environment, "verification.ces.mappings-file"));
            List<Map<String, Object>> mappings = mapper.readValue(mappingPath.toFile(), new TypeReference<>() {});
            if (mappings.isEmpty()) throw new IllegalArgumentException("EMPTY_ENTITY_MAPPINGS");
            List<String> entities = mappings.stream().map(row -> row.get("entityName"))
                .map(value -> { if (!(value instanceof String name) || name.isBlank())
                    throw new IllegalArgumentException("INVALID_ENTITY_MAPPING"); return name; }).distinct().toList();
            report.put("mappingSha256", sha256(mappingPath));
            report.put("entities", entities);
            String baselineUrl;
            String candidateUrl;
            String baselineToken;
            String candidateToken;
            String accountPath;
            String entitlementPath;
            String cesPath;
            if (mode.equals("replay")) {
                replay = new ReplayServer(environment.getProperty("verification.replay.variant", "match"));
                replay.start();
                baselineUrl = replay.origin() + "/ems2";
                candidateUrl = replay.origin() + "/ces";
                baselineToken = "";
                candidateToken = "synthetic-service-token";
                accountPath = "/account/%s";
                entitlementPath = "/entitlements";
                cesPath = "/user/{userId}";
                report.put("fixture", "Built-in synthetic HTTP fixtures; both actual SDK jars execute against loopback HTTP.");
            } else {
                baselineUrl = required(environment, "verification.ems2.base-url");
                candidateUrl = required(environment, "verification.ces.base-url");
                baselineToken = environment.getProperty("SDK_VERIFY_EMS2_TOKEN", "");
                candidateToken = required(environment, "SDK_VERIFY_CES_TOKEN");
                accountPath = environment.getProperty("verification.ems2.account-path", "/ems2/rest/account/%s");
                entitlementPath = environment.getProperty("verification.ems2.entitlements-path", "/ems2/rest/entitlements/entitlementList");
                cesPath = environment.getProperty("verification.ces.assigned-roles-path", "/fmces/v1/entitlement/user/{userId}");
            }
            Duration connect = Duration.ofMillis(boundedMillis(environment, "verification.connect-timeout-ms", 10000));
            Duration read = Duration.ofMillis(boundedMillis(environment, "verification.read-timeout-ms", 15000));
            SdkBridge.Settings baseline = new SdkBridge.Settings(Path.of(environment.getProperty("verification.baseline.jar", "lib/ems2-sdk.jar")),
                (String) baselineArtifact.get("sha256"), baselineUrl, accountPath, entitlementPath, entities, List.of(), baselineToken, connect, read, false);
            SdkBridge.Settings candidate = new SdkBridge.Settings(Path.of(environment.getProperty("verification.candidate.jar", "lib/ces-sdk.jar")),
                (String) candidateArtifact.get("sha256"), candidateUrl, "", cesPath, entities, mappings, candidateToken, connect, read, true);
            int assessed = 0;
            int matches = 0;
            for (int index = 0; index < users.size(); index++) {
                String user = users.get(index);
                Map<String, Object> account = new LinkedHashMap<>();
                account.put("userId", user);
                account.put("startedAt", Instant.now().toString());
                try {
                    SdkBridge bridge = new SdkBridge();
                    SdkBridge.LookupResult old = bridge.lookup(baseline, user);
                    SdkBridge.LookupResult migrated = bridge.lookup(candidate, user);
                    account.put("baseline", mapper.convertValue(old, Map.class));
                    account.put("candidate", mapper.convertValue(migrated, Map.class));
                    if (!old.errors().isEmpty() || !migrated.errors().isEmpty()) {
                        account.put("status", "UNASSESSED");
                    } else {
                        var comparison = PermissionComparison.compare(old.permissions(), migrated.permissions());
                        account.put("comparison", mapper.convertValue(comparison, Map.class));
                        account.put("status", comparison.matches() ? "MATCH" : "DIFFERENT");
                        assessed++;
                        if (comparison.matches()) matches++;
                    }
                } catch (Exception error) {
                    account.put("status", "UNASSESSED");
                    account.put("error", "SDK_LOOKUP_OR_COMPARISON_FAILED");
                    account.put("errorCategory", error.getClass().getSimpleName());
                }
                account.put("finishedAt", Instant.now().toString());
                accounts.add(account);
                mapper.writerWithDefaultPrettyPrinter().writeValue(output.resolve("accounts/%05d.json".formatted(index + 1)).toFile(), account);
                report.put("metrics", accountMetrics(users.size(), assessed, matches, complete));
                report.put("status", "RUNNING");
                mapper.writerWithDefaultPrettyPrinter().writeValue(output.resolve("progress.json").toFile(), report);
            }
            report.put("status", verdict(users.size(), assessed, matches, complete));
            exit = assessed < users.size() || !complete ? 2 : matches < users.size() ? 1 : 0;
            if (!complete) ((List<String>) report.get("gaps")).add("The declared population is not confirmed complete by the operator's source record.");
        } catch (Exception error) {
            report.put("status", "INCOMPLETE");
            report.put("error", "CONFIGURATION_OR_STARTUP_FAILED");
            report.put("errorCategory", error.getClass().getSimpleName());
            exit = 2;
        } finally {
            if (replay != null) replay.close();
        }
        report.put("finishedAt", Instant.now().toString());
        report.put("exitCode", exit);
        VerificationReport.write(output, report);
        System.out.println("VERIFICATION_STATUS=" + report.get("status"));
        System.out.println("REPORT=" + output.resolve("report.html"));
        return exit;
    }

    static String verdict(int declared, int assessed, int matching, boolean complete) {
        if (declared <= 0 || assessed != declared || !complete) return "INCOMPLETE";
        return matching == declared ? "SCOPED_SDK_PARITY_PASS" : "DIFFERENCES";
    }

    static String populationSource(Environment environment, String mode) {
        return environment.getProperty("verification.population-source", mode.equals("replay")
            ? "Built-in synthetic fixture population; not enterprise users" : "").trim();
    }

    static boolean populationComplete(Environment environment, String mode) {
        return Boolean.parseBoolean(environment.getProperty("verification.population-complete",
            mode.equals("replay") ? "true" : "false")) && !populationSource(environment, mode).isEmpty();
    }

    static Map<String, Object> accountMetrics(int declared, int assessed, int matching, boolean complete) {
        Map<String, Object> metrics = new LinkedHashMap<>();
        metrics.put("declared", declared);
        metrics.put("assessed", assessed);
        metrics.put("matching", matching);
        metrics.put("unassessed", declared - assessed);
        metrics.put("assessedAccountPercent", declared == 0 ? null : 100.0 * assessed / declared);
        metrics.put("sdkParityPercent", !complete || assessed != declared || declared == 0 ? null : 100.0 * matching / declared);
        return metrics;
    }

    static List<String> readUsers(Path path) throws Exception {
        List<String> users = new ArrayList<>();
        LinkedHashSet<String> unique = new LinkedHashSet<>();
        for (String line : Files.readAllLines(path, StandardCharsets.UTF_8)) {
            String user = line.strip();
            if (user.isEmpty() || user.startsWith("#") || user.equals("userId")) continue;
            if (!user.matches("[A-Za-z0-9._@-]{1,200}") || !unique.add(user))
                throw new IllegalArgumentException("INVALID_OR_DUPLICATE_ACCOUNT");
            users.add(user);
        }
        if (users.isEmpty()) throw new IllegalArgumentException("EMPTY_ACCOUNT_POPULATION");
        return users;
    }

    private static Map<String, Object> artifact(Map<String, Object> manifest, String name, String expectedRevision) {
        Object entry = manifest.get(name);
        if (!(entry instanceof Map<?, ?> row) || !expectedRevision.equals(row.get("revision"))
            || !(row.get("sha256") instanceof String hash) || !hash.matches("[0-9a-f]{64}"))
            throw new IllegalArgumentException("SDK_MANIFEST_MISMATCH");
        return Map.of("revision", expectedRevision, "sha256", row.get("sha256"));
    }

    private static String required(Environment environment, String property) {
        String value = environment.getProperty(property, "");
        if (value.isBlank()) throw new IllegalArgumentException("MISSING_REQUIRED_CONFIGURATION");
        return value;
    }

    private static int boundedMillis(Environment environment, String name, int fallback) {
        int value = Integer.parseInt(environment.getProperty(name, Integer.toString(fallback)));
        if (value < 100 || value > 120000) throw new IllegalArgumentException("INVALID_TIMEOUT");
        return value;
    }

    static String sha256(Path path) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(path)));
    }
}
