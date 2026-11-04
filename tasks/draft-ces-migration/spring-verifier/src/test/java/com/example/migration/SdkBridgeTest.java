package com.example.migration;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class SdkBridgeTest {
    @TempDir Path temporary;

    @Test
    void mismatchedArtifactCannotExecuteOrReturnAPassingEmptyResult() throws Exception {
        Path jar = temporary.resolve("wrong.jar");
        Files.writeString(jar, "artifact bytes");
        SdkBridge.Settings configured = settings(false, jar, "0".repeat(64));
        SdkBridge.LookupResult result = new SdkBridge().lookup(configured, "user-a");
        assertEquals(List.of("ARTIFACT_SHA256_MISMATCH"), result.errors());
        assertEquals(SdkBridge.sha256(Files.readAllBytes(jar)), result.jarSha256());
        assertTrue(result.requests().isEmpty());
        assertTrue(result.permissions().isEmpty());
    }

    @Test
    void missingArtifactRemainsAnError() throws Exception {
        SdkBridge.LookupResult result = new SdkBridge().lookup(
            settings(false, temporary.resolve("absent.jar"), "0".repeat(64)), "user-a");
        assertEquals(List.of("ARTIFACT_NOT_FOUND"), result.errors());
        assertTrue(result.requests().isEmpty());
    }

    @Test
    void credentialsAreExcludedFromSettingsSerializationAndText() throws Exception {
        SdkBridge.Settings settings = settings(true, temporary.resolve("sdk.jar"), "0".repeat(64));
        assertFalse(settings.toString().contains("synthetic-service-token"));
        ObjectMapper mapper = new ObjectMapper();
        var fields = mapper.getSerializationConfig().introspect(mapper.constructType(SdkBridge.Settings.class)).findProperties();
        assertTrue(fields.stream().noneMatch(field -> field.getName().equals("token")));
    }

    @Test
    void accountRowsIgnoredByLegacySdkStillInvalidateCompleteness() {
        SdkBridge.ResponseAudit audit = audit(false);
        audit.inspect("EMS2_ACCOUNT", bytes("{\"entitlementTypes\":[{\"uniqueName\":\"\"}]}"));
        assertTrue(audit.errors.contains("INVALID_ACCOUNT_ASSIGNMENT"));
    }

    @Test
    void wrongUserCannotSatisfyBaselineEvenThoughLegacySdkSelectsFirstObject() {
        SdkBridge.ResponseAudit audit = audit(false);
        audit.inspect("EMS2_ENTITLEMENTS", bytes("{\"another-user\":{\"count\":0,\"entitlements\":[]}}"));
        assertTrue(audit.errors.contains("BASELINE_USER_MISMATCH"));
    }

    @Test
    void incompleteCountAndUnassignedRoleCannotProduceParity() {
        SdkBridge.ResponseAudit mismatch = audit(false);
        mismatch.inspect("EMS2_ENTITLEMENTS", bytes("{\"user-a\":{\"count\":3,\"entitlements\":[]}}"));
        assertTrue(mismatch.errors.contains("INCOMPLETE_BASELINE_GRANTS"));

        SdkBridge.ResponseAudit unassigned = audit(false);
        unassigned.inspect("EMS2_ACCOUNT", bytes(account()));
        unassigned.inspect("EMS2_ENTITLEMENTS", bytes(grants(999)));
        assertTrue(unassigned.errors.contains("UNASSIGNED_BASELINE_ROLE"));
    }

    @Test
    void emptyAccountsAndConfirmedEmptyRoleAssignmentsRemainValid() {
        SdkBridge.ResponseAudit emptyAccount = audit(false);
        emptyAccount.inspect("EMS2_ACCOUNT", bytes("{\"entitlementTypes\":[]}"));
        assertTrue(emptyAccount.errors.isEmpty());
        assertFalse(emptyAccount.baselineHadAssignments);

        SdkBridge.ResponseAudit emptyRole = audit(false);
        emptyRole.inspect("EMS2_ACCOUNT", bytes(account()));
        emptyRole.inspect("EMS2_ENTITLEMENTS", bytes("{\"user-a\":{\"count\":0,\"entitlements\":[]}}"));
        assertTrue(emptyRole.errors.isEmpty());
        assertEquals("LEGACY:reader", emptyRole.assignedRoles.get(11L));
    }

    @Test
    void aggregateCesResponseCannotMasqueradeAsEmptyAssignedRoles() {
        SdkBridge.ResponseAudit audit = audit(true);
        audit.inspect("CES_ASSIGNED_ROLES", bytes("[{\"user_data\":{\"user_id\":\"user-a\"},\"entitlements\":{}}]"));
        assertTrue(audit.errors.contains("INVALID_CES_ROUTING_IDENTITY"));
    }

    @Test
    void selectedRoleMustHaveGrantArrayButUnselectedApplicationsNeedNot() {
        SdkBridge.ResponseAudit selected = audit(true);
        selected.inspect("CES_ASSIGNED_ROLES", bytes("[{\"appId\":\"app-1\",\"appName\":\"APP\",\"entitlementName\":\"reader\"}]"));
        assertTrue(selected.errors.contains("INCOMPLETE_CES_ROLE_GRANTS"));

        SdkBridge.ResponseAudit unselected = audit(true);
        unselected.inspect("CES_ASSIGNED_ROLES", bytes("[{\"appId\":\"another-app\",\"appName\":\"OTHER\"}]"));
        assertTrue(unselected.errors.isEmpty());
    }

    @Test
    void duplicateMappedRoleAndConflictingApplicationAreRejected() {
        String empty = "{\"appId\":\"app-1\",\"appName\":\"APP\",\"entitlementName\":\"reader\",\"featureActionDtos\":[]}";
        SdkBridge.ResponseAudit duplicate = audit(true);
        duplicate.inspect("CES_ASSIGNED_ROLES", bytes("[" + empty + "," + empty + "]"));
        assertTrue(duplicate.errors.contains("AMBIGUOUS_CES_ROLE_MAPPING"));

        SdkBridge.ResponseAudit mismatch = audit(true);
        mismatch.inspect("CES_ASSIGNED_ROLES", bytes("[{\"appId\":\"app-1\",\"appName\":\"APP\",\"entitlementName\":\"reader\",\"featureActionDtos\":[{\"features\":{\"featureName\":\"trade\",\"applicationDto\":{\"appName\":\"OTHER\"}},\"actions\":{\"actionName\":\"view\"}}]}]"));
        assertTrue(mismatch.errors.contains("CES_GRANT_APPLICATION_MISMATCH"));
    }

    @Test
    void dtoDeserializationFailureCannotBecomeAnEmptySuccessForSelectedOrUnselectedRoles() throws Exception {
        for (String application : List.of("app-1", "unselected-app")) {
            SdkBridge.ResponseAudit audit = typedAudit(true);
            audit.inspect("CES_ASSIGNED_ROLES", bytes("[{\"appId\":\"" + application
                + "\",\"appName\":\"APP\",\"entitlementName\":\"reader\",\"appUID\":\"not-a-number\",\"featureActionDtos\":[]}]"));
            assertEquals(java.util.Set.of("SDK_RESPONSE_DESERIALIZATION_FAILURE"), audit.errors);
        }
        SdkBridge.ResponseAudit legitimateEmpty = typedAudit(true);
        legitimateEmpty.inspect("CES_ASSIGNED_ROLES", bytes("[]"));
        assertTrue(legitimateEmpty.errors.isEmpty());
    }

    @Test
    void baselineFieldsUnusedByOutputStillMustDeserializeIntoSdkDtos() throws Exception {
        SdkBridge.ResponseAudit audit = typedAudit(false);
        audit.inspect("EMS2_ACCOUNT", bytes(account()));
        audit.inspect("EMS2_ENTITLEMENTS", bytes(grants(11).replace("\"action\":{", "\"action\":{\"id\":\"not-a-number\",")));
        assertEquals(java.util.Set.of("SDK_RESPONSE_DESERIALIZATION_FAILURE"), audit.errors);
    }

    @Test
    void originGuardSeparatesSchemeHostAndEffectivePort() {
        assertTrue(SdkBridge.sameOrigin(URI.create("https://service.example/base"), URI.create("https://SERVICE.example:443/path")));
        assertFalse(SdkBridge.sameOrigin(URI.create("https://service.example"), URI.create("http://service.example")));
        assertFalse(SdkBridge.sameOrigin(URI.create("https://service.example"), URI.create("https://other.example")));
        assertFalse(SdkBridge.sameOrigin(URI.create("https://service.example"), URI.create("https://service.example:8443")));
    }

    private SdkBridge.ResponseAudit audit(boolean candidate) {
        return new SdkBridge.ResponseAudit(settings(candidate, temporary.resolve("sdk.jar"), "0".repeat(64)), "user-a");
    }

    private SdkBridge.ResponseAudit typedAudit(boolean candidate) throws Exception {
        SdkBridge.ResponseAudit audit = audit(candidate);
        // The typed fixtures isolate the bridge boundary; the executable replay binds the actual SDK DTO classes.
        ClassLoader dtoLoader = new ClassLoader() {
            @Override public Class<?> loadClass(String name) throws ClassNotFoundException {
                return switch (name) {
                    case "com.scb.fmoportal.auth.entity.CesRole" -> TypedCandidateRole.class;
                    case "com.scb.fmoportal.auth.entity.Ems2Role" -> TypedAccount.class;
                    case "com.scb.fmoportal.auth.entity.EntitlementList" -> TypedEntitlementList.class;
                    default -> super.loadClass(name);
                };
            }
        };
        audit.bindSdkTypes(dtoLoader, new ObjectMapper());
        return audit;
    }

    @com.fasterxml.jackson.annotation.JsonIgnoreProperties(ignoreUnknown = true)
    public record TypedCandidateRole(Long appUID) {}
    @com.fasterxml.jackson.annotation.JsonIgnoreProperties(ignoreUnknown = true)
    public record TypedAccount(List<Map<String, Object>> entitlementTypes) {}
    @com.fasterxml.jackson.annotation.JsonIgnoreProperties(ignoreUnknown = true)
    public record TypedEntitlementList(int count, List<TypedEntitlement> entitlements) {}
    @com.fasterxml.jackson.annotation.JsonIgnoreProperties(ignoreUnknown = true)
    public record TypedEntitlement(TypedAction action) {}
    @com.fasterxml.jackson.annotation.JsonIgnoreProperties(ignoreUnknown = true)
    public record TypedAction(Long id) {}

    private SdkBridge.Settings settings(boolean candidate, Path jar, String hash) {
        return new SdkBridge.Settings(jar, hash, "https://service.example", "/ems2/rest/account/%s",
            candidate ? "/fmces/v1/entitlement/user/{userId}" : "/ems2/rest/entitlements/entitlementList",
            List.of("LEGACY"), List.of(Map.of("appId", "app-1", "appName", "APP", "entityName", "LEGACY")),
            "synthetic-service-token", Duration.ofSeconds(2), Duration.ofSeconds(3), candidate);
    }

    private static byte[] bytes(String text) { return text.getBytes(StandardCharsets.UTF_8); }
    private static String account() { return "{\"entitlementTypes\":[{\"uniqueName\":\"1|LEGACY|11|reader\"}]}"; }
    private static String grants(long role) {
        return "{\"user-a\":{\"count\":1,\"entitlements\":[{\"id\":1,\"role\":{\"id\":" + role
            + "},\"subject\":{\"id\":21,\"name\":\"trade\"},\"action\":{\"name\":\"view\"}}]}}";
    }
}
