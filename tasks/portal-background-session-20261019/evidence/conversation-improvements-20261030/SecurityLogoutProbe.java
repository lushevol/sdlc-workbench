import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.config.JWTConfigProperties;
import com.scb.sso.singleuibff.controller.v2.JwtAuthenticationController;
import com.scb.sso.singleuibff.dto.ems2.v2.Ems2Result;
import com.scb.sso.singleuibff.dto.request.RequestOfJWT;
import com.scb.sso.singleuibff.dto.request.RequestOfRelogin;
import com.scb.sso.singleuibff.entity.ApplicationSession;
import com.scb.sso.singleuibff.repository.ApplicationSessionRepo;
import com.scb.sso.singleuibff.service.v1.ApplicationCategoryService;
import com.scb.sso.singleuibff.service.v1.implementation.SessionServiceImplementation;
import com.scb.sso.singleuibff.service.v2.authorization.TileAuthorizationService;
import com.scb.sso.singleuibff.service.v2.filter.AuthFilterExecutor;
import com.scb.sso.singleuibff.util.AdminModuleUtil;
import com.scb.sso.singleuibff.util.JwtTokenUtil;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.mock.web.MockHttpSession;
import java.nio.file.*;
import java.security.*;
import java.security.interfaces.*;
import java.time.Instant;
import java.util.*;
import static org.mockito.Mockito.*;

/** One source-bound controller case. No HTTP server, network, or production credentials. */
public class SecurityLogoutProbe {
  static void set(Object target, String name, Object value) throws Exception {
    var field = target.getClass().getDeclaredField(name);
    field.setAccessible(true);
    field.set(target, value);
  }

  public static void main(String[] args) throws Exception {
    if (args.length != 3 || !Set.of("RN-S001", "RN-S002").contains(args[0])) {
      throw new IllegalArgumentException("Expected case ID, full revision, and new output path");
    }
    String caseId = args[0];
    boolean expired = caseId.equals("RN-S002");
    Path destination = Path.of(args[2]);
    var mapper = new ObjectMapper();
    var generator = KeyPairGenerator.getInstance("RSA");
    generator.initialize(2048);
    var pair = generator.generateKeyPair();
    var props = new JWTConfigProperties();
    props.setPrv(Base64.getEncoder().encodeToString(pair.getPrivate().getEncoded()));
    props.setPub(Base64.getEncoder().encodeToString(pair.getPublic().getEncoded()));
    props.setTokenExpiration(15);
    props.setReTokenExpiration(225);
    props.setAbsoluteExpiration(60);
    var jwt = new JwtTokenUtil(props);
    var algorithm = Algorithm.RSA512((RSAPublicKey)pair.getPublic(), (RSAPrivateKey)pair.getPrivate());
    String sessionId = "synthetic-paired-" + caseId;
    var deniedSessions = new HashSet<String>();
    var repository = mock(ApplicationSessionRepo.class);
    when(repository.save(any(ApplicationSession.class))).thenAnswer(call -> {
      ApplicationSession session = call.getArgument(0);
      deniedSessions.add(session.getSessionId());
      return session;
    });
    when(repository.findBySessionId(anyString())).thenAnswer(call -> {
      String id = call.getArgument(0);
      return deniedSessions.contains(id)
          ? Optional.of(ApplicationSession.builder().sessionId(id).build()) : Optional.empty();
    });
    var controller = new JwtAuthenticationController();
    var servletSession = new MockHttpSession();
    set(controller, "jwtTokenUtil", jwt);
    set(controller, "objectMapper", mapper);
    set(controller, "sessionService", new SessionServiceImplementation(repository));
    set(controller, "httpSession", servletSession);
    var category = mock(ApplicationCategoryService.class);
    when(category.getDrawers()).thenReturn(Optional.of(List.of()));
    set(controller, "applicationCategoryService", category);
    var entitlements = new Ems2Result();
    entitlements.setEntities(List.of());
    // This fixture adapts only the renamed entitlement collaborator API.
    // The application controller, JWT checks, session service, and assertions are identical inputs.
    var tile = mock(TileAuthorizationService.class, call -> {
      if (call.getMethod().getName().equals("getEntitlements")) return entitlements;
      if (call.getMethod().getName().equals("getAuthorization")) {
        return call.getMethod().getReturnType().getMethod("legacy", Ems2Result.class)
            .invoke(null, entitlements);
      }
      return RETURNS_DEFAULTS.answer(call);
    });
    set(controller, "tileAuthorizationService", tile);
    var admin = mock(AdminModuleUtil.class, call -> {
      if (Set.of("getDrawer", "getAuthorizedDrawer").contains(call.getMethod().getName())) return List.of();
      return RETURNS_DEFAULTS.answer(call);
    });
    set(controller, "adminModuleUtil", admin);
    var filter = mock(AuthFilterExecutor.class);
    when(filter.filterDrawersRaw(anyString(), anyList())).thenReturn(List.of());
    set(controller, "authFilterExecutor", filter);

    long now = System.currentTimeMillis();
    String access = JWT.create().withIssuer("single-ui-bff").withSubject("synthetic-user")
        .withClaim("id", sessionId).withClaim("oud", "{}")
        .withIssuedAt(new Date(now - 1_200_000))
        .withExpiresAt(new Date(expired ? now - 600_000 : now + 600_000)).sign(algorithm);
    String refresh = jwt.generateReToken("synthetic-user", Map.of("id", sessionId, "oud", "{}"));
    boolean refreshValidBeforeLogout = jwt.validateToken(refresh);
    jwt.handleIssuer(refresh, "single-ui-bff-refresh");
    var logoutInput = new RequestOfJWT();
    logoutInput.setSingleUIAuthorization("Bearer " + access);
    var logout = controller.logout(logoutInput, new MockHttpServletResponse());
    var replayRequest = new MockHttpServletRequest();
    replayRequest.addHeader("Single-UI-Refresh", "Bearer " + refresh);
    var replayResponse = new MockHttpServletResponse();
    var replay = controller.relogin(new RequestOfRelogin(), replayRequest, replayResponse);

    var assertions = new LinkedHashMap<String, Boolean>();
    assertions.put("refresh_valid_before_logout", refreshValidBeforeLogout);
    assertions.put("logout_http_200", logout.getStatusCode().value() == 200);
    assertions.put("logout_result_true", logout.getBody() != null && logout.getBody().isResult());
    assertions.put("replay_http_401", replay.getStatusCode().value() == 401);
    assertions.put("zero_access_credentials", replayResponse.getHeader("Single-UI-Authorization") == null);
    boolean passed = assertions.values().stream().allMatch(Boolean::booleanValue);
    var row = new LinkedHashMap<String, Object>();
    row.put("case_id", caseId);
    row.put("revision", args[1]);
    row.put("observed_at", Instant.now().toString());
    row.put("expired_access", expired);
    row.put("logout_status", logout.getStatusCode().value());
    row.put("logout_result", logout.getBody() != null && logout.getBody().isResult());
    row.put("servlet_session_invalidated", servletSession.isInvalid());
    row.put("blacklist_entries", deniedSessions.size());
    row.put("session_id_revoked", deniedSessions.contains(sessionId));
    row.put("relogin_status", replay.getStatusCode().value());
    row.put("relogin_result", replay.getBody() != null && replay.getBody().isResult());
    row.put("new_access_issued", replayResponse.getHeader("Single-UI-Authorization") != null);
    row.put("new_refresh_issued", replayResponse.getHeader("Single-UI-Refresh") != null);
    row.put("assertions", assertions);
    row.put("status", passed ? "PASSED" : "FAILED");
    row.put("assertion_scope", expired
        ? "Canonical zero-access security proposal; identical supplemental 401 assertion on both revisions"
        : "Canonical observed logout, 401 replay rejection, and zero-access predicates");
    // CREATE_NEW prevents replacement of an earlier completed case.
    Files.writeString(destination, mapper.writerWithDefaultPrettyPrinter().writeValueAsString(row) + "\n",
        StandardOpenOption.CREATE_NEW);
    System.out.println(mapper.writeValueAsString(row));
    System.exit(passed ? 0 : 2);
  }
}
