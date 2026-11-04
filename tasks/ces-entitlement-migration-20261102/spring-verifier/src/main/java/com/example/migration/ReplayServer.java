package com.example.migration;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Explicitly synthetic fixtures, served through real loopback HTTP to the two actual SDKs. */
public final class ReplayServer implements AutoCloseable {
    private final ObjectMapper mapper = new ObjectMapper();
    private final HttpServer server;
    private final String variant;

    public ReplayServer(String variant) throws IOException {
        if (!List.of("match", "missing", "extra", "failure", "empty", "malformed").contains(variant))
            throw new IllegalArgumentException("INVALID_REPLAY_VARIANT");
        this.variant = variant;
        server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", this::respond);
    }

    public void start() { server.start(); }
    public String origin() { return "http://127.0.0.1:" + server.getAddress().getPort(); }
    public void close() { server.stop(0); }

    private void respond(HttpExchange exchange) throws IOException {
        try (exchange) {
            String path = exchange.getRequestURI().getPath();
            Object response;
            int status = 200;
            if (path.startsWith("/ems2/account/") && exchange.getRequestMethod().equals("GET")) {
                String user = path.substring("/ems2/account/".length());
                response = Map.of("entitlementTypes", assignments(user));
            } else if (path.equals("/ems2/entitlements") && exchange.getRequestMethod().equals("POST")) {
                JsonNode request = mapper.readTree(exchange.getRequestBody());
                if (!request.isObject() || request.size() != 1) throw new IllegalArgumentException();
                String user = request.fieldNames().next();
                List<Map<String, Object>> grants = oldGrants(user);
                response = Map.of(user, Map.of("count", grants.size(), "entitlements", grants));
            } else if (path.startsWith("/ces/user/") && exchange.getRequestMethod().equals("GET")) {
                String user = path.substring("/ces/user/".length());
                if (!"Bearer synthetic-service-token".equals(exchange.getRequestHeaders().getFirst("Authorization"))) {
                    status = 401;
                    response = Map.of("error", "UNAUTHORIZED");
                } else if (variant.equals("failure") && user.equals("bob")) {
                    status = 503;
                    response = Map.of("error", "CONTROLLED_SERVICE_FAILURE");
                } else response = newRoles(user);
            } else {
                status = 404;
                response = Map.of("error", "UNKNOWN_ROUTE");
            }
            byte[] bytes = mapper.writeValueAsBytes(response);
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(status, bytes.length);
            exchange.getResponseBody().write(bytes);
        } catch (RuntimeException ignored) {
            // A malformed local fixture request closes without returning account or token details.
        }
    }

    private List<Map<String, Object>> assignments(String user) {
        if (variant.equals("empty") || variant.equals("malformed")) return List.of();
        return switch (user) {
            case "alice" -> List.of(assignment(1, "LEGACY_APP", 101, "READER"),
                assignment(1, "LEGACY_APP", 102, "EMPTY"), assignment(2, "LEGACY_DATA", 201, "GLOBAL"));
            case "bob" -> List.of(assignment(1, "LEGACY_APP", 101, "READER"));
            case "service.demo" -> List.of(assignment(3, "LEGACY_SYSTEM", 301, "SERVICE"));
            default -> throw new IllegalArgumentException("UNKNOWN_FIXTURE_ACCOUNT");
        };
    }

    private Map<String, Object> assignment(int entity, String name, int role, String roleName) {
        return Map.of("uniqueName", entity + "|" + name + "|" + role + "|" + roleName, "applicationName", "DEMO");
    }

    private List<Map<String, Object>> oldGrants(String user) {
        if (variant.equals("empty") || variant.equals("malformed")) return List.of();
        if (user.equals("service.demo")) return List.of(oldGrant(4, 3, "LEGACY_SYSTEM", 301, "SERVICE", 30, "SYSTEM", "query"));
        List<Map<String, Object>> grants = new ArrayList<>(List.of(
            oldGrant(1, 1, "LEGACY_APP", 101, "READER", 10, "TRADE", "view"),
            oldGrant(2, 1, "LEGACY_APP", 101, "READER", 10, "TRADE", "view"),
            oldGrant(3, 1, "LEGACY_APP", 101, "READER", 10, "TRADE", "export")));
        if (user.equals("alice")) grants.add(oldGrant(5, 2, "LEGACY_DATA", 201, "GLOBAL", 20, "DATA", "view"));
        return grants;
    }

    private Map<String, Object> oldGrant(int id, int entity, String entityName, int role, String roleName,
                                         int subject, String subjectName, String action) {
        return Map.of("id", id, "role", Map.of("id", role, "name", roleName, "entity", Map.of("id", entity, "name", entityName)),
            "subject", Map.of("id", subject, "name", subjectName), "action", Map.of("id", id, "name", action));
    }

    private List<Map<String, Object>> newRoles(String user) {
        if (variant.equals("empty")) return List.of();
        if (variant.equals("malformed")) return List.of(Map.of("appId", "demo-app", "appName", "DEMO",
            "appUID", "not-a-number", "entitlementName", "READER", "featureActionDtos", List.of()));
        if (user.equals("service.demo")) return List.of(role("SERVICE", List.of(grant("SYSTEM", "query"))));
        List<Map<String, Object>> pairs = new ArrayList<>(List.of(grant("TRADE", "view"), grant("TRADE", "view"), grant("TRADE", "export")));
        if (variant.equals("missing") && user.equals("bob")) pairs.remove(2);
        if (variant.equals("extra") && user.equals("bob")) pairs.add(grant("TRADE", "delete"));
        List<Map<String, Object>> roles = new ArrayList<>(List.of(role("READER", pairs)));
        if (user.equals("alice")) {
            roles.add(role("EMPTY", List.of()));
            roles.add(role("GLOBAL", List.of(grant("DATA", "view"))));
        }
        return roles;
    }

    private Map<String, Object> role(String name, List<Map<String, Object>> grants) {
        return Map.of("appId", "demo-app", "appName", "DEMO", "appUID", 1, "entitlementName", name, "featureActionDtos", grants);
    }

    private Map<String, Object> grant(String feature, String action) {
        return Map.of("features", Map.of("featureName", feature), "actions", Map.of("actionName", action));
    }
}
