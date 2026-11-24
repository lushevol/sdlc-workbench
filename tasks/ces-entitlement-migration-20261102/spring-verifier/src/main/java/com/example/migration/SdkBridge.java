package com.example.migration;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Proxy;
import java.net.URI;
import java.net.URLClassLoader;
import java.net.http.HttpClient;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Executes the actual SDK artifacts; response audits expose failures hidden by the legacy API. */
public final class SdkBridge {
    private static final String PACKAGE = "com.scb.fmoportal.auth.";
    private static final int MAX_RESPONSE_BYTES = 8 * 1024 * 1024;
    private final ObjectMapper mapper = new ObjectMapper();

    public record Settings(Path jar, String expectedSha256, String baseUrl,
                           String userRolesEndpoint, String entitlementsEndpoint,
                           List<String> entities, List<Map<String, Object>> mappings,
                           @com.fasterxml.jackson.annotation.JsonIgnore String token, Duration connectTimeout, Duration readTimeout,
                           boolean candidate) {
        @Override public String toString() {
            return "SdkSettings[jar=" + jar + ", candidate=" + candidate + ", token=REDACTED]";
        }
    }

    public record LookupResult(Map<String, Object> permissions, List<Map<String, Object>> requests,
                               List<String> errors, String jarSha256) {}

    public LookupResult lookup(Settings settings, String userId) throws Exception {
        List<Map<String, Object>> requests = new ArrayList<>();
        ResponseAudit audit = new ResponseAudit(settings, userId);
        String jarHash = "";
        try {
            if (settings.jar() == null || !Files.isRegularFile(settings.jar())) {
                throw new VerificationFailure("ARTIFACT_NOT_FOUND");
            }
            jarHash = sha256(Files.readAllBytes(settings.jar()));
            if (settings.expectedSha256() == null || !settings.expectedSha256().matches("[a-fA-F0-9]{64}")) {
                throw new VerificationFailure("ARTIFACT_IDENTITY_MISSING");
            }
            if (!jarHash.equalsIgnoreCase(settings.expectedSha256())) {
                throw new VerificationFailure("ARTIFACT_SHA256_MISMATCH");
            }
            validateSettings(settings, userId);
            URI origin = URI.create(settings.baseUrl());
            HttpClient client = HttpClient.newBuilder()
                .connectTimeout(settings.connectTimeout())
                .followRedirects(HttpClient.Redirect.NEVER).build();
            JdkClientHttpRequestFactory factory = new JdkClientHttpRequestFactory(client);
            factory.setReadTimeout(settings.readTimeout());
            RestTemplate rest = new RestTemplate(factory);
            rest.getInterceptors().add((request, body, execution) -> {
                Map<String, Object> event = new LinkedHashMap<>();
                event.put("method", request.getMethod().name());
                event.put("path", redactedPath(request.getURI(), userId));
                requests.add(event);
                try {
                    if (!sameOrigin(origin, request.getURI()) || request.getURI().getRawQuery() != null
                        || request.getURI().getRawFragment() != null || request.getURI().getRawUserInfo() != null) {
                        throw new VerificationFailure("UNEXPECTED_REQUEST_DESTINATION");
                    }
                    String stage = audit.stage(request.getMethod(), request.getURI());
                    event.put("stage", stage);
                    if (!settings.candidate() && hasText(settings.token())) {
                        String token = settings.token();
                        request.getHeaders().set(HttpHeaders.AUTHORIZATION,
                            token.startsWith("Bearer ") || token.startsWith("Basic ") ? token : "Bearer " + token);
                    }
                    if (settings.candidate() && !("Bearer " + settings.token()).equals(
                        request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION))) {
                        throw new VerificationFailure("CALLER_TOKEN_NOT_USED");
                    }
                    ClientHttpResponse response = execution.execute(request, body);
                    try {
                        HttpStatusCode status = response.getStatusCode();
                        event.put("status", status.value());
                        byte[] bytes = response.getBody().readNBytes(MAX_RESPONSE_BYTES + 1);
                        event.put("responseBytes", bytes.length);
                        event.put("responseSha256", sha256(bytes));
                        if (bytes.length > MAX_RESPONSE_BYTES) {
                            throw new VerificationFailure("RESPONSE_LIMIT_EXCEEDED");
                        }
                        if (!status.is2xxSuccessful()) {
                            throw new VerificationFailure("HTTP_" + status.value());
                        }
                        audit.inspect(stage, bytes);
                        if (!audit.errors.isEmpty()) {
                            throw new VerificationFailure("INVALID_RESPONSE");
                        }
                        return new BufferedResponse(response, bytes);
                    } catch (IOException | RuntimeException failure) {
                        response.close();
                        throw failure;
                    }
                } catch (Exception failure) {
                    String code = failure instanceof VerificationFailure vf ? vf.code : "TRANSPORT_FAILURE";
                    audit.errors.add(code);
                    event.put("error", code);
                    // The old SDK logs caught exceptions. Never pass response bodies, tokens, or raw causes to it.
                    throw new IOException("SDK_VERIFY_" + code);
                }
            });
            try (URLClassLoader loader = new URLClassLoader(
                new java.net.URL[]{settings.jar().toUri().toURL()}, SdkBridge.class.getClassLoader())) {
                Class<?> propertyType = loader.loadClass(PACKAGE + "properties.AuthProperties");
                if (propertyType.getClassLoader() != loader) {
                    throw new VerificationFailure("SDK_CLASSLOADER_COLLISION");
                }
                audit.bindSdkTypes(loader, mapper);
                Object properties = propertyType.getConstructor().newInstance();
                propertyType.getMethod("setEntityList", List.class).invoke(properties, settings.entities());
                propertyType.getMethod("setConnectTimeout", Duration.class).invoke(properties, settings.connectTimeout());
                propertyType.getMethod("setReadTimeout", Duration.class).invoke(properties, settings.readTimeout());
                Class<?> serviceType = loader.loadClass(PACKAGE + "services.implementation.AuthorizationImpl");
                Object service;
                if (settings.candidate()) {
                    Object ces = propertyType.getMethod("getCes").invoke(properties);
                    Class<?> cesType = ces.getClass();
                    cesType.getMethod("setBaseUrl", String.class).invoke(ces, settings.baseUrl());
                    cesType.getMethod("setUserEntitlementsEndpoint", String.class)
                        .invoke(ces, settings.entitlementsEndpoint());
                    Class<?> mappingType = loader.loadClass(PACKAGE + "properties.AuthProperties$CesEntityMapping");
                    List<Object> mappings = new ArrayList<>();
                    for (Map<String, Object> mapping : settings.mappings()) {
                        mappings.add(mapper.convertValue(mapping, mappingType));
                    }
                    cesType.getMethod("setEntityMappings", List.class).invoke(ces, mappings);
                    Class<?> providerType = loader.loadClass(PACKAGE + "services.FmaaTokenProvider");
                    Object provider = Proxy.newProxyInstance(loader, new Class<?>[]{providerType},
                        (proxy, method, args) -> {
                            if (method.getName().equals("getToken")) return settings.token();
                            if (method.getName().equals("toString")) return "CallerTokenProvider";
                            if (method.getName().equals("hashCode")) return System.identityHashCode(proxy);
                            if (method.getName().equals("equals")) return proxy == args[0];
                            throw new UnsupportedOperationException("TOKEN_PROVIDER_METHOD");
                        });
                    service = serviceType.getConstructor(RestTemplate.class, ObjectMapper.class, propertyType, providerType)
                        .newInstance(rest, mapper, properties, provider);
                } else {
                    propertyType.getMethod("setEms2Host", String.class).invoke(properties, settings.baseUrl());
                    propertyType.getMethod("setUserRolesEndpoint", String.class).invoke(properties, settings.userRolesEndpoint());
                    propertyType.getMethod("setEntitlementEndpoint", String.class).invoke(properties, settings.entitlementsEndpoint());
                    service = serviceType.getConstructor(RestTemplate.class, ObjectMapper.class, propertyType)
                        .newInstance(rest, mapper, properties);
                }
                Object returned = serviceType.getMethod("getEntitlements", String.class).invoke(service, userId);
                Map<String, Object> permissions = checkedMap(returned);
                audit.finish();
                if (requests.isEmpty()) audit.errors.add("NO_HTTP_REQUEST");
                return new LookupResult(permissions, List.copyOf(requests), List.copyOf(audit.errors), jarHash);
            }
        } catch (VerificationFailure failure) {
            audit.errors.add(failure.code);
        } catch (InvocationTargetException failure) {
            audit.errors.add("SDK_INVOCATION_FAILURE");
        } catch (ReflectiveOperationException | LinkageError failure) {
            audit.errors.add("SDK_LOAD_OR_API_FAILURE");
        } catch (IOException | IllegalArgumentException failure) {
            audit.errors.add("CONFIGURATION_OR_ARTIFACT_FAILURE");
        }
        return new LookupResult(Map.of(), List.copyOf(requests), List.copyOf(audit.errors), jarHash);
    }

    private static void validateSettings(Settings settings, String userId) throws VerificationFailure {
        if (!hasText(userId) || userId.indexOf('\r') >= 0 || userId.indexOf('\n') >= 0) {
            throw new VerificationFailure("INVALID_USER_ID");
        }
        URI base;
        try { base = URI.create(settings.baseUrl()); }
        catch (RuntimeException failure) { throw new VerificationFailure("INVALID_BASE_URL"); }
        if (!("https".equalsIgnoreCase(base.getScheme()) || "http".equalsIgnoreCase(base.getScheme()))
            || base.getHost() == null || base.getRawUserInfo() != null || base.getRawQuery() != null
            || base.getRawFragment() != null) throw new VerificationFailure("INVALID_BASE_URL");
        if (settings.connectTimeout() == null || settings.readTimeout() == null
            || settings.connectTimeout().isNegative() || settings.connectTimeout().isZero()
            || settings.readTimeout().isNegative() || settings.readTimeout().isZero()) {
            throw new VerificationFailure("INVALID_TIMEOUT");
        }
        if (hasText(settings.token()) && (settings.token().indexOf('\r') >= 0 || settings.token().indexOf('\n') >= 0)) {
            throw new VerificationFailure("INVALID_TOKEN");
        }
        if (settings.candidate() && (!hasText(settings.token()) || settings.token().startsWith("Bearer ")
            || settings.mappings() == null || settings.mappings().isEmpty())) {
            throw new VerificationFailure("CANDIDATE_TOKEN_OR_MAPPINGS_MISSING");
        }
        if (!validEndpoint(settings.entitlementsEndpoint())
            || (settings.candidate() && !settings.entitlementsEndpoint().contains("{userId}"))
            || (!settings.candidate() && (!validEndpoint(settings.userRolesEndpoint())
                || !settings.userRolesEndpoint().contains("%s")))) {
            throw new VerificationFailure("INVALID_ENDPOINT");
        }
    }

    private static boolean validEndpoint(String endpoint) {
        return hasText(endpoint) && endpoint.startsWith("/") && !endpoint.startsWith("//")
            && !endpoint.contains("?") && !endpoint.contains("#");
    }

    private static Map<String, Object> checkedMap(Object value) throws VerificationFailure {
        if (!(value instanceof Map<?, ?> roles)) throw new VerificationFailure("INVALID_SDK_OUTPUT");
        Map<String, Object> result = new LinkedHashMap<>();
        for (Map.Entry<?, ?> role : roles.entrySet()) {
            if (!(role.getKey() instanceof String key) || !hasText(key) || !(role.getValue() instanceof Map<?, ?> subjects)) {
                throw new VerificationFailure("INVALID_SDK_OUTPUT");
            }
            Map<String, Object> copied = new LinkedHashMap<>();
            for (Map.Entry<?, ?> subject : subjects.entrySet()) {
                if (!(subject.getKey() instanceof String name) || !hasText(name)
                    || !(subject.getValue() instanceof List<?> actions)
                    || actions.stream().anyMatch(action -> !(action instanceof String text) || !hasText(text))) {
                    throw new VerificationFailure("INVALID_SDK_OUTPUT");
                }
                copied.put(name, List.copyOf(actions));
            }
            result.put(key, copied);
        }
        return result;
    }

    static String sha256(byte[] bytes) {
        try { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)); }
        catch (Exception impossible) { throw new IllegalStateException("SHA256_UNAVAILABLE"); }
    }

    static boolean sameOrigin(URI left, URI right) {
        return left.getScheme() != null && right.getScheme() != null && left.getHost() != null && right.getHost() != null
            && left.getScheme().equalsIgnoreCase(right.getScheme()) && left.getHost().equalsIgnoreCase(right.getHost())
            && effectivePort(left) == effectivePort(right);
    }

    private static int effectivePort(URI uri) {
        return uri.getPort() >= 0 ? uri.getPort() : "https".equalsIgnoreCase(uri.getScheme()) ? 443 : 80;
    }

    private static String redactedPath(URI uri, String userId) {
        return uri.getPath() == null ? "" : uri.getPath().replace(userId, "{userId}");
    }

    private static boolean hasText(String value) { return value != null && !value.isBlank(); }

    private static final class VerificationFailure extends IOException {
        final String code;
        VerificationFailure(String code) { super(code); this.code = code; }
    }

    private record BufferedResponse(ClientHttpResponse delegate, byte[] bytes) implements ClientHttpResponse {
        @Override public HttpStatusCode getStatusCode() throws IOException { return delegate.getStatusCode(); }
        @Override public String getStatusText() throws IOException { return delegate.getStatusText(); }
        @Override public HttpHeaders getHeaders() { return delegate.getHeaders(); }
        @Override public InputStream getBody() { return new ByteArrayInputStream(bytes); }
        @Override public void close() { delegate.close(); }
    }

    /** Package-visible for tests of malformed data and masked-failure boundaries. */
    static final class ResponseAudit {
        final Settings settings;
        final String userId;
        final Set<String> errors = new LinkedHashSet<>();
        final Map<Long, String> assignedRoles = new HashMap<>();
        Map<String, JavaType> payloadTypes = Map.of();
        ObjectMapper schemaMapper;
        boolean baselineHadAssignments;
        int accountRequests;
        int entitlementRequests;

        ResponseAudit(Settings settings, String userId) { this.settings = settings; this.userId = userId; }

        void bindSdkTypes(ClassLoader loader, ObjectMapper mapper) throws ClassNotFoundException {
            schemaMapper = mapper;
            if (settings.candidate()) {
                payloadTypes = Map.of("CES_ASSIGNED_ROLES", mapper.getTypeFactory().constructCollectionType(
                    List.class, loader.loadClass(PACKAGE + "entity.CesRole")));
            } else {
                payloadTypes = Map.of(
                    "EMS2_ACCOUNT", mapper.constructType(loader.loadClass(PACKAGE + "entity.Ems2Role")),
                    "EMS2_ENTITLEMENTS", mapper.getTypeFactory().constructMapType(Map.class,
                        mapper.constructType(String.class), mapper.constructType(loader.loadClass(PACKAGE + "entity.EntitlementList"))));
            }
        }

        String stage(HttpMethod method, URI uri) throws VerificationFailure {
            String path = uri.getPath();
            String basePath = URI.create(settings.baseUrl()).getPath();
            if (settings.candidate()) {
                String expected = basePath + settings.entitlementsEndpoint().replace("{userId}", userId);
                if (method != HttpMethod.GET || !expected.equals(path)) throw new VerificationFailure("UNEXPECTED_SDK_REQUEST");
                entitlementRequests++;
                return "CES_ASSIGNED_ROLES";
            }
            String accountPath = basePath + String.format(settings.userRolesEndpoint(), userId);
            if (method == HttpMethod.GET && accountPath.equals(path)) {
                accountRequests++;
                return "EMS2_ACCOUNT";
            }
            if (method == HttpMethod.POST && (basePath + settings.entitlementsEndpoint()).equals(path)) {
                entitlementRequests++;
                return "EMS2_ENTITLEMENTS";
            }
            throw new VerificationFailure("UNEXPECTED_SDK_REQUEST");
        }

        void inspect(String stage, byte[] body) {
            try {
                JsonNode json = new ObjectMapper().readTree(body);
                if (json == null) { errors.add("EMPTY_JSON_RESPONSE"); return; }
                switch (stage) {
                    case "EMS2_ACCOUNT" -> account(json);
                    case "EMS2_ENTITLEMENTS" -> baselineGrants(json);
                    case "CES_ASSIGNED_ROLES" -> candidateRoles(json);
                    default -> errors.add("UNEXPECTED_RESPONSE_STAGE");
                }
                if (errors.isEmpty() && payloadTypes.containsKey(stage)) {
                    try {
                        // Deserialize every row, including unselected applications, before either legacy API can mask failure.
                        schemaMapper.readValue(body, payloadTypes.get(stage));
                    } catch (Exception failure) {
                        errors.add("SDK_RESPONSE_DESERIALIZATION_FAILURE");
                    }
                }
            } catch (Exception failure) { errors.add("INVALID_JSON_RESPONSE"); }
        }

        void account(JsonNode json) {
            JsonNode types = json.get("entitlementTypes");
            if (!json.isObject() || types == null || !types.isArray()) { errors.add("INVALID_ACCOUNT_RESPONSE"); return; }
            baselineHadAssignments = !types.isEmpty();
            Set<String> keys = new HashSet<>();
            for (JsonNode type : types) {
                String[] fields = type.path("uniqueName").asText("").split("\\|", -1);
                if (fields.length < 4 || !hasText(fields[1]) || !hasText(fields[3])) {
                    errors.add("INVALID_ACCOUNT_ASSIGNMENT"); continue;
                }
                try {
                    Long.parseLong(fields[0]);
                    long roleId = Long.parseLong(fields[2]);
                    if (selectedEntity(fields[1])) {
                        String key = fields[1] + ":" + fields[3];
                        String prior = assignedRoles.putIfAbsent(roleId, key);
                        if ((prior != null && !prior.equals(key)) || !keys.add(key)) errors.add("AMBIGUOUS_BASELINE_ASSIGNMENT");
                    }
                } catch (NumberFormatException failure) { errors.add("INVALID_ACCOUNT_ASSIGNMENT"); }
            }
        }

        void baselineGrants(JsonNode json) {
            if (!json.isObject() || json.size() != 1 || !json.has(userId)) { errors.add("BASELINE_USER_MISMATCH"); return; }
            JsonNode data = json.get(userId), rows = data.get("entitlements"), count = data.get("count");
            if (rows == null || !rows.isArray() || count == null || !count.isIntegralNumber()
                || count.asLong() < 0 || count.asLong() != rows.size()) { errors.add("INCOMPLETE_BASELINE_GRANTS"); return; }
            Map<String, String> subjectNames = new HashMap<>();
            for (JsonNode row : rows) {
                JsonNode roleId = row.path("role").get("id"), subjectId = row.path("subject").get("id");
                if (!integral(row.get("id")) || !integral(roleId) || !integral(subjectId)
                    || !text(row.path("subject"), "name") || !text(row.path("action"), "name")) {
                    errors.add("INVALID_BASELINE_GRANT"); continue;
                }
                long id = roleId.asLong();
                if (!assignedRoles.containsKey(id)) errors.add("UNASSIGNED_BASELINE_ROLE");
                String identity = id + ":" + subjectId.asLong();
                String oldName = subjectNames.putIfAbsent(identity, row.path("subject").path("name").asText());
                if (oldName != null && !oldName.equals(row.path("subject").path("name").asText())) {
                    errors.add("AMBIGUOUS_BASELINE_SUBJECT");
                }
            }
        }

        void candidateRoles(JsonNode json) {
            if (!json.isArray()) { errors.add("INVALID_CES_ASSIGNED_ROLE_RESPONSE"); return; }
            Set<String> outputRoles = new HashSet<>();
            for (JsonNode role : json) {
                if (!text(role, "appId") || !text(role, "appName")) { errors.add("INVALID_CES_ROUTING_IDENTITY"); continue; }
                for (Map<String, Object> rawMapping : settings.mappings()) {
                    JsonNode mapping = new ObjectMapper().valueToTree(rawMapping);
                    if (!mapping.path("appId").asText().equals(role.path("appId").asText())
                        || !mapping.path("appName").asText().equals(role.path("appName").asText())
                        || !selectedEntity(mapping.path("entityName").asText())) continue;
                    if (!text(role, "entitlementName")) { errors.add("INVALID_CES_ROLE_NAME"); continue; }
                    String name = role.path("entitlementName").asText();
                    JsonNode aliases = mapping.path("roleMappings");
                    if (aliases.isObject() && !aliases.isEmpty() && !aliases.has(name)) continue;
                    JsonNode grants = role.get("featureActionDtos");
                    if (grants == null || !grants.isArray()) { errors.add("INCOMPLETE_CES_ROLE_GRANTS"); continue; }
                    String outputRole = mapping.path("entityName").asText() + ":" + aliases.path(name).asText(name);
                    if (!outputRoles.add(outputRole)) errors.add("AMBIGUOUS_CES_ROLE_MAPPING");
                    Map<String, String> outputSubjects = new HashMap<>();
                    for (JsonNode grant : grants) {
                        JsonNode feature = grant.path("features"), action = grant.path("actions");
                        if (!text(feature, "featureName") || !text(action, "actionName")) {
                            errors.add("INVALID_CES_GRANT"); continue;
                        }
                        nestedApplication(role, feature.path("applicationDto"));
                        nestedApplication(role, action.path("applicationDto"));
                        String featureName = feature.path("featureName").asText();
                        JsonNode features = mapping.path("featureNames");
                        if (features.isArray() && !features.isEmpty()) {
                            boolean included = false;
                            for (JsonNode permitted : features) if (featureName.equals(permitted.asText())) included = true;
                            if (!included) continue;
                        }
                        String outputSubject = mapping.path("subjectMappings").path(featureName).asText(featureName);
                        String previous = outputSubjects.putIfAbsent(outputSubject, featureName);
                        if (previous != null && !previous.equals(featureName)) errors.add("AMBIGUOUS_CES_SUBJECT_MAPPING");
                    }
                }
            }
        }

        private void nestedApplication(JsonNode role, JsonNode nested) {
            if (nested.isMissingNode() || nested.isNull()) return;
            if (!role.path("appName").asText().equals(nested.path("appName").asText())
                || (role.hasNonNull("appUID") && !role.get("appUID").equals(nested.get("appUID")))) {
                errors.add("CES_GRANT_APPLICATION_MISMATCH");
            }
        }

        private boolean selectedEntity(String entity) {
            return settings.entities() == null || settings.entities().isEmpty() || settings.entities().contains(entity);
        }

        private static boolean integral(JsonNode node) { return node != null && node.isIntegralNumber(); }
        private static boolean text(JsonNode node, String field) {
            return node != null && node.path(field).isTextual() && hasText(node.path(field).asText());
        }

        void finish() {
            if (settings.candidate()) {
                if (entitlementRequests != 1) errors.add("UNEXPECTED_CES_REQUEST_COUNT");
                if (accountRequests != 0) errors.add("CANDIDATE_EMS2_REQUEST");
            } else {
                if (accountRequests != 1) errors.add("UNEXPECTED_BASELINE_ACCOUNT_REQUEST_COUNT");
                if (entitlementRequests != (baselineHadAssignments ? 1 : 0)) errors.add("UNEXPECTED_BASELINE_GRANT_REQUEST_COUNT");
            }
        }
    }
}
