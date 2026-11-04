package com.example.migration;

import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class PermissionComparisonTest {
    @Test
    void exactRoleMapsPreserveEmptyRolesAndActionMultiplicity() {
        Map<String, Object> baseline = new LinkedHashMap<>();
        baseline.put("APP:reader", Map.of("trade", List.of("read", "read", "export")));
        baseline.put("APP:empty", Map.of());
        Map<String, Object> candidate = new LinkedHashMap<>();
        candidate.put("APP:empty", Map.of());
        candidate.put("APP:reader", Map.of("trade", List.of("read", "read", "export")));

        var result = PermissionComparison.compare(baseline, candidate);

        assertTrue(result.matches());
        assertEquals(List.of(), result.differences());
        assertEquals(2, metric(result, "roles").get("matched"));
        assertEquals(3, metric(result, "roleScopedPermissions").get("matched"));
        assertEquals(100.0, metric(result, "roleScopedPermissions").get("coveragePercent"));
        assertEquals(2, metric(result, "roleScopedPermissionDefinitions").get("matched"));
        assertEquals(Map.of("baseline", 1, "candidate", 1), result.metrics().get("duplicateOccurrences"));
    }

    @Test
    void missingEmptyRoleCannotHideBehindAnEmptyPermissionDenominator() {
        var result = PermissionComparison.compare(Map.of("APP:empty", Map.of()), Map.of());
        assertFalse(result.matches());
        assertEquals(1, metric(result, "roles").get("missing"));
        assertNull(metric(result, "roleScopedPermissions").get("coveragePercent"));
        assertTrue(result.differences().stream().anyMatch(d -> d.get("kind").equals("MISSING_ROLE")));
    }

    @Test
    void missingEmptySubjectRemainsADifference() {
        var result = PermissionComparison.compare(Map.of("APP:reader", Map.of("empty", List.of())),
            Map.of("APP:reader", Map.of()));
        assertFalse(result.matches());
        assertEquals(1, metric(result, "subjects").get("missing"));
        assertEquals(0, metric(result, "roles").get("missing"));
        assertTrue(result.differences().stream().anyMatch(d -> d.get("kind").equals("MISSING_SUBJECT")));
    }

    @Test
    void effectiveUnionCannotHidePermissionMovementBetweenRoles() {
        var result = PermissionComparison.compare(
            Map.of("APP:reader", Map.of("trade", List.of("read")), "APP:writer", Map.of()),
            Map.of("APP:reader", Map.of(), "APP:writer", Map.of("trade", List.of("read"))));
        assertFalse(result.matches());
        assertEquals(100.0, metric(result, "effectivePermissions").get("coveragePercent"));
        assertEquals(0.0, metric(result, "roleScopedPermissions").get("coveragePercent"));
        assertEquals(1, result.metrics().get("missingPermissionOccurrences"));
        assertEquals(1, result.metrics().get("additionalPermissionOccurrences"));
    }

    @Test
    void duplicateLossIsAContractDifferenceDespiteEqualUniquePermissions() {
        var result = PermissionComparison.compare(
            Map.of("APP:reader", Map.of("trade", List.of("read", "read", "export"))),
            Map.of("APP:reader", Map.of("trade", List.of("read", "export"))));
        assertFalse(result.matches());
        assertEquals(66.6667, metric(result, "roleScopedPermissions").get("coveragePercent"));
        assertEquals(100.0, metric(result, "roleScopedPermissionDefinitions").get("coveragePercent"));
        assertEquals(1, metric(result, "roleScopedPermissions").get("missing"));
    }

    @Test
    void reorderedActionsFailExactCompatibilityWithoutInventingMissingPermissions() {
        var result = PermissionComparison.compare(
            Map.of("APP:reader", Map.of("trade", List.of("read", "export"))),
            Map.of("APP:reader", Map.of("trade", List.of("export", "read"))));
        assertFalse(result.matches());
        assertEquals(100.0, metric(result, "roleScopedPermissions").get("coveragePercent"));
        assertEquals(0, metric(result, "roleScopedPermissions").get("missing"));
        assertEquals(0, metric(result, "roleScopedPermissions").get("additional"));
        assertEquals(1, result.metrics().get("actionSequenceMismatches"));
    }

    @Test
    void additionalPermissionsRemainVisibleWhenBaselineCoverageIsFull() {
        var result = PermissionComparison.compare(
            Map.of("APP:reader", Map.of("trade", List.of("read"))),
            Map.of("APP:reader", Map.of("trade", List.of("read", "delete"))));
        assertFalse(result.matches());
        assertEquals(100.0, metric(result, "roleScopedPermissions").get("coveragePercent"));
        assertEquals(1, metric(result, "roleScopedPermissions").get("additional"));
        assertEquals(1, metric(result, "effectivePermissions").get("additional"));
    }

    @Test
    void anotherEntityOrCaseVariantCannotSatisfyTheExpectedScope() {
        var result = PermissionComparison.compare(
            Map.of("APP:reader", Map.of("trade", List.of("read"))),
            Map.of("app:reader", Map.of("trade", List.of("read"))));
        assertFalse(result.matches());
        assertEquals(1, metric(result, "roles").get("missing"));
        assertEquals(1, metric(result, "roles").get("additional"));
        assertEquals(0.0, metric(result, "effectivePermissions").get("coveragePercent"));
    }

    @Test
    void validEmptyAssignmentsMatchWithoutClaimingOneHundredPercent() {
        var result = PermissionComparison.compare(Map.of(), Map.of());
        assertTrue(result.matches());
        assertEquals(true, result.metrics().get("validEmpty"));
        for (String key : List.of("roles", "subjects", "roleScopedPermissions", "effectivePermissions")) {
            assertNull(metric(result, key).get("coveragePercent"));
            assertEquals(true, metric(result, key).get("denominatorEmpty"));
        }
    }

    @Test
    void nullAndMalformedPayloadsCannotBecomeMatchingEmptyAssignments() {
        assertThrows(IllegalArgumentException.class, () -> PermissionComparison.compare(null, Map.of()));
        for (Map<String, Object> invalid : List.<Map<String, Object>>of(
            Map.of("reader", Map.of()),
            Map.of(":reader", Map.of()),
            Map.of("APP:", Map.of()),
            Map.of("APP:reader", List.of()),
            Map.of("APP:reader", Map.of("trade", "read")),
            Map.of("APP:reader", Map.of("trade", List.of(7))),
            Map.of("APP:reader", Map.of(" ", List.of("read"))),
            Map.of("APP:reader", Map.of("trade", List.of(" ")))
        )) {
            assertThrows(IllegalArgumentException.class, () -> PermissionComparison.compare(invalid, Map.of()));
            assertThrows(IllegalArgumentException.class, () -> PermissionComparison.compare(Map.of(), invalid));
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> metric(PermissionComparison.Comparison result, String name) {
        return (Map<String, Object>) result.metrics().get(name);
    }
}
