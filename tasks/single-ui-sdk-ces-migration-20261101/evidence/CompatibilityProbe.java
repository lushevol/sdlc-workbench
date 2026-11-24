import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.fmoportal.auth.properties.AuthProperties;
import com.scb.fmoportal.auth.services.AuthorizationService;
import com.scb.fmoportal.auth.services.implementation.AuthorizationImpl;
import org.springframework.http.HttpStatus;
import org.springframework.mock.http.client.MockClientHttpResponse;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestTemplate;

import java.lang.reflect.Proxy;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

/** One compiled caller exercises the unmodified baseline classes and the migrated classes in separate JVMs. */
public class CompatibilityProbe {
    public static void main(String[] args) throws Exception {
        String mode = args[0];
        ObjectMapper mapper = new ObjectMapper();
        AuthProperties properties = new AuthProperties();
        properties.setEntityList(List.of("LEGACY"));
        RestTemplate rest = new RestTemplate();
        MockRestServiceServer server = MockRestServiceServer.createServer(rest);
        AuthorizationService service;
        int requests;
        if (mode.equals("baseline")) {
            properties.setEms2Host("https://ems2.example");
            String account = "{\"entitlementTypes\":["
                + "{\"uniqueName\":\"1|LEGACY|11|ROLE_A\",\"applicationName\":\"APP\"},"
                + "{\"uniqueName\":\"1|LEGACY|12|ROLE_B\",\"applicationName\":\"APP\"},"
                + "{\"uniqueName\":\"1|LEGACY|13|EMPTY_ROLE\",\"applicationName\":\"APP\"}]}";
            String grants = "{\"user-1\":{\"count\":4,\"entitlements\":["
                + oldGrant(1, 11, "read") + "," + oldGrant(2, 11, "read") + ","
                + oldGrant(3, 11, "export") + "," + oldGrant(4, 12, "write") + "]}}";
            expect(server, "https://ems2.example/ems2/rest/account/user-1", "GET", account, false);
            expect(server, "https://ems2.example/ems2/rest/entitlements/entitlementList", "POST", grants, false);
            service = new AuthorizationImpl(rest, mapper, properties);
            requests = 2;
        } else {
            Object ces = AuthProperties.class.getMethod("getCes").invoke(properties);
            ces.getClass().getMethod("setBaseUrl", String.class).invoke(ces, "https://ces.example");
            Class<?> mappingClass = Class.forName("com.scb.fmoportal.auth.properties.AuthProperties$CesEntityMapping");
            Object mapping = mappingClass.getConstructor().newInstance();
            mappingClass.getMethod("setAppId", String.class).invoke(mapping, "app-1");
            mappingClass.getMethod("setAppName", String.class).invoke(mapping, "APP");
            mappingClass.getMethod("setEntityName", String.class).invoke(mapping, "LEGACY");
            ces.getClass().getMethod("setEntityMappings", List.class).invoke(ces, List.of(mapping));
            String roles = "[" + newRole("ROLE_A", "read", "read", "export") + ","
                + newRole("ROLE_B", "write") + "," + newRole("EMPTY_ROLE") + "]";
            expect(server, "https://ces.example/fmces/v1/entitlement/user/user-1", "GET", roles, true);
            Class<?> providerClass = Class.forName("com.scb.fmoportal.auth.services.FmaaTokenProvider");
            Object provider = Proxy.newProxyInstance(providerClass.getClassLoader(), new Class<?>[] {providerClass},
                (proxy, method, arguments) -> "test-token");
            service = (AuthorizationService) AuthorizationImpl.class.getConstructor(RestTemplate.class, ObjectMapper.class,
                AuthProperties.class, providerClass).newInstance(rest, mapper, properties, provider);
            requests = 1;
        }
        Map<String, Object> actual = service.getEntitlements("user-1");
        Map<String, Object> expected = Map.of("LEGACY:ROLE_A", Map.of("FEATURE", List.of("read", "read", "export")),
            "LEGACY:ROLE_B", Map.of("FEATURE", List.of("write")), "LEGACY:EMPTY_ROLE", Map.of());
        if (!expected.equals(actual)) throw new AssertionError("Legacy map differs: " + actual);
        server.verify();
        System.out.println("COMPATIBILITY_RESULT=" + mapper.writeValueAsString(Map.of("mode", mode,
            "permissions", actual, "httpRequests", requests, "assertionsPassed", true)));
    }

    private static String oldGrant(int id, int role, String action) {
        return "{\"id\":" + id + ",\"role\":{\"id\":" + role + "},"
            + "\"subject\":{\"id\":101,\"name\":\"FEATURE\"},"
            + "\"action\":{\"id\":" + id + ",\"name\":\"" + action + "\"}}";
    }

    private static String newRole(String name, String... actions) {
        java.util.ArrayList<String> grants = new java.util.ArrayList<>();
        for (String action : actions) grants.add("{\"features\":{\"featureName\":\"FEATURE\"},"
            + "\"actions\":{\"actionName\":\"" + action + "\"}}");
        return "{\"appId\":\"app-1\",\"appName\":\"APP\",\"entitlementName\":\"" + name
            + "\",\"featureActionDtos\":[" + String.join(",", grants) + "]}";
    }

    private static void expect(MockRestServiceServer server, String url, String method, String body, boolean bearer) {
        server.expect(request -> {
            if (!url.equals(request.getURI().toString()) || !method.equals(request.getMethod().name()))
                throw new AssertionError("Unexpected outbound request");
            if (bearer && !"Bearer test-token".equals(request.getHeaders().getFirst("Authorization")))
                throw new AssertionError("Missing caller bearer token");
        }).andRespond(request -> new MockClientHttpResponse(body.getBytes(StandardCharsets.UTF_8), HttpStatus.OK));
    }
}
