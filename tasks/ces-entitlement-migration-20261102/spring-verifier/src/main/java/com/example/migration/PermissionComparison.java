package com.example.migration;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Exact comparison of the SDK's entity:role -> subject -> action-list contract. */
public final class PermissionComparison {
    private PermissionComparison() {}

    public record Comparison(boolean matches, Map<String, Object> metrics,
                             List<Map<String, Object>> differences) {}

    private record Subject(String role, String subject) {}
    private record Permission(String role, String subject, String action) {}
    private record EffectivePermission(String entity, String subject, String action) {}
    private record Inventory(Map<String, Map<String, List<String>>> roles, Set<Subject> subjects,
                             Map<Permission, Integer> permissions, Set<EffectivePermission> effective,
                             int occurrences) {}

    /**
     * Accepts only successful, validated lookup maps. Callers must keep failed or unassessed
     * lookups outside this method; a swallowed upstream error is not a valid empty assignment.
     */
    public static Comparison compare(Map<String, Object> baseline, Map<String, Object> candidate) {
        Inventory expected = inventory(baseline, "baseline");
        Inventory actual = inventory(candidate, "candidate");
        List<Map<String, Object>> differences = new ArrayList<>();
        Set<String> expectedRoles = expected.roles().keySet();
        Set<String> actualRoles = actual.roles().keySet();
        for (String role : difference(expectedRoles, actualRoles)) {
            differences.add(diff("MISSING_ROLE", "role", role));
        }
        for (String role : difference(actualRoles, expectedRoles)) {
            differences.add(diff("ADDITIONAL_ROLE", "role", role));
        }
        for (Subject subject : difference(expected.subjects(), actual.subjects())) {
            differences.add(subjectDiff("MISSING_SUBJECT", subject));
        }
        for (Subject subject : difference(actual.subjects(), expected.subjects())) {
            differences.add(subjectDiff("ADDITIONAL_SUBJECT", subject));
        }
        int matchedOccurrences = 0;
        int missingOccurrences = 0;
        int additionalOccurrences = 0;
        Set<Permission> permissions = union(expected.permissions().keySet(), actual.permissions().keySet());
        for (Permission permission : permissions) {
            int before = expected.permissions().getOrDefault(permission, 0);
            int after = actual.permissions().getOrDefault(permission, 0);
            matchedOccurrences += Math.min(before, after);
            missingOccurrences += Math.max(0, before - after);
            additionalOccurrences += Math.max(0, after - before);
            if (before != after) {
                Map<String, Object> item = diff(before > after ? "MISSING_PERMISSION" : "ADDITIONAL_PERMISSION",
                    "role", permission.role());
                item.put("subject", permission.subject());
                item.put("action", permission.action());
                item.put("baselineCount", before);
                item.put("candidateCount", after);
                item.put("missingOccurrences", Math.max(0, before - after));
                item.put("additionalOccurrences", Math.max(0, after - before));
                differences.add(item);
            }
        }
        int sequenceMismatches = 0;
        Set<Subject> commonSubjects = intersection(expected.subjects(), actual.subjects());
        for (Subject subject : commonSubjects) {
            List<String> before = expected.roles().get(subject.role()).get(subject.subject());
            List<String> after = actual.roles().get(subject.role()).get(subject.subject());
            if (!before.equals(after)) {
                sequenceMismatches++;
                Map<String, Object> item = subjectDiff("ACTION_SEQUENCE_CHANGED", subject);
                item.put("baselineActions", before);
                item.put("candidateActions", after);
                differences.add(item);
            }
        }
        for (EffectivePermission permission : difference(expected.effective(), actual.effective())) {
            differences.add(effectiveDiff("MISSING_EFFECTIVE_PERMISSION", permission));
        }
        for (EffectivePermission permission : difference(actual.effective(), expected.effective())) {
            differences.add(effectiveDiff("ADDITIONAL_EFFECTIVE_PERMISSION", permission));
        }
        Map<String, Object> metrics = new LinkedHashMap<>();
        metrics.put("roles", metric(expectedRoles.size(), actualRoles.size(),
            intersection(expectedRoles, actualRoles).size()));
        metrics.put("subjects", metric(expected.subjects().size(), actual.subjects().size(),
            commonSubjects.size()));
        metrics.put("roleScopedPermissions", metric(expected.occurrences(), actual.occurrences(), matchedOccurrences));
        metrics.put("roleScopedPermissionDefinitions", metric(expected.permissions().size(), actual.permissions().size(),
            intersection(expected.permissions().keySet(), actual.permissions().keySet()).size()));
        metrics.put("effectivePermissions", metric(expected.effective().size(), actual.effective().size(),
            intersection(expected.effective(), actual.effective()).size()));
        Map<String, Object> duplicates = new LinkedHashMap<>();
        duplicates.put("baseline", expected.occurrences() - expected.permissions().size());
        duplicates.put("candidate", actual.occurrences() - actual.permissions().size());
        metrics.put("duplicateOccurrences", duplicates);
        metrics.put("comparedActionSequences", commonSubjects.size());
        metrics.put("actionSequenceMismatches", sequenceMismatches);
        metrics.put("validEmpty", expected.roles().isEmpty() && actual.roles().isEmpty());
        metrics.put("validEmptyPermissions", expected.occurrences() == 0 && actual.occurrences() == 0);
        metrics.put("missingPermissionOccurrences", missingOccurrences);
        metrics.put("additionalPermissionOccurrences", additionalOccurrences);
        metrics.put("comparisonBoundary", "Successful SDK maps only; role and subject keys, action multiplicity, and action order.");
        return new Comparison(differences.isEmpty(), Collections.unmodifiableMap(metrics), List.copyOf(differences));
    }

    private static Inventory inventory(Map<String, Object> input, String side) {
        if (input == null) throw invalid(side, "map is null");
        Map<String, Map<String, List<String>>> roles = new LinkedHashMap<>();
        Set<Subject> subjects = new LinkedHashSet<>();
        Map<Permission, Integer> permissions = new LinkedHashMap<>();
        Set<EffectivePermission> effective = new LinkedHashSet<>();
        int occurrences = 0;
        for (Map.Entry<?, ?> roleEntry : input.entrySet()) {
            if (!(roleEntry.getKey() instanceof String role) || role.isBlank()) {
                throw invalid(side, "role key is not a nonblank string");
            }
            int separator = role.indexOf(':');
            if (separator <= 0 || separator == role.length() - 1) {
                throw invalid(side, "role key must contain nonempty entity and role names");
            }
            if (!(roleEntry.getValue() instanceof Map<?, ?> rawSubjects)) {
                throw invalid(side, "role value is not a subject map");
            }
            String entity = role.substring(0, separator);
            Map<String, List<String>> subjectMap = new LinkedHashMap<>();
            for (Map.Entry<?, ?> subjectEntry : rawSubjects.entrySet()) {
                if (!(subjectEntry.getKey() instanceof String subject) || subject.isBlank()) {
                    throw invalid(side, "subject key is not a nonblank string");
                }
                if (!(subjectEntry.getValue() instanceof List<?> rawActions)) {
                    throw invalid(side, "subject value is not an action list");
                }
                List<String> actions = new ArrayList<>();
                subjects.add(new Subject(role, subject));
                for (Object rawAction : rawActions) {
                    if (!(rawAction instanceof String action) || action.isBlank()) {
                        throw invalid(side, "action is not a nonblank string");
                    }
                    actions.add(action);
                    permissions.merge(new Permission(role, subject, action), 1, Integer::sum);
                    effective.add(new EffectivePermission(entity, subject, action));
                    occurrences++;
                }
                subjectMap.put(subject, List.copyOf(actions));
            }
            roles.put(role, Collections.unmodifiableMap(subjectMap));
        }
        return new Inventory(Collections.unmodifiableMap(roles), subjects, permissions, effective, occurrences);
    }

    private static IllegalArgumentException invalid(String side, String reason) {
        // Do not echo permission payloads or account input into an exception message.
        return new IllegalArgumentException("Invalid " + side + " SDK permission map: " + reason);
    }

    private static Map<String, Object> metric(int expected, int actual, int matched) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("expected", expected);
        result.put("actual", actual);
        result.put("matched", matched);
        result.put("missing", expected - matched);
        result.put("additional", actual - matched);
        result.put("coveragePercent", expected == 0 ? null : Math.round(1000000.0 * matched / expected) / 10000.0);
        result.put("denominatorEmpty", expected == 0);
        return result;
    }

    private static Map<String, Object> diff(String kind, String field, Object value) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("kind", kind);
        result.put(field, value);
        return result;
    }

    private static Map<String, Object> subjectDiff(String kind, Subject subject) {
        Map<String, Object> result = diff(kind, "role", subject.role());
        result.put("subject", subject.subject());
        return result;
    }

    private static Map<String, Object> effectiveDiff(String kind, EffectivePermission permission) {
        Map<String, Object> result = diff(kind, "entity", permission.entity());
        result.put("subject", permission.subject());
        result.put("action", permission.action());
        return result;
    }

    private static <T> Set<T> difference(Set<T> left, Set<T> right) {
        Set<T> result = new LinkedHashSet<>(left);
        result.removeAll(right);
        return result;
    }

    private static <T> Set<T> intersection(Set<T> left, Set<T> right) {
        Set<T> result = new LinkedHashSet<>(left);
        result.retainAll(right);
        return result;
    }

    private static <T> Set<T> union(Set<T> left, Set<T> right) {
        Set<T> result = new LinkedHashSet<>(left);
        result.addAll(right);
        return result;
    }
}
