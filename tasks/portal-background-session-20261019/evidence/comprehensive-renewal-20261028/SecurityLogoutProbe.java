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
import java.util.*;
import static org.mockito.Mockito.*;

/** Isolated actual-controller probe. No HTTP service, production credentials, or network calls. */
public class SecurityLogoutProbe {
  static void set(Object o, String name, Object value) throws Exception {
    var f = o.getClass().getDeclaredField(name); f.setAccessible(true); f.set(o, value);
  }
  static void reject(JwtAuthenticationController controller, String credential,
      String id, boolean acquisition, String output) throws Exception {
    var response = new MockHttpServletResponse();
    org.springframework.http.ResponseEntity<?> result;
    if (acquisition) {
      var input = new RequestOfJWT(); input.setSingleUIAuthorization(credential);
      result = controller.refreshtoken(input,response);
    } else {
      var request = new MockHttpServletRequest();
      if (credential != null) request.addHeader("Single-UI-Refresh",credential);
      result = controller.relogin(new RequestOfRelogin(),request,response);
    }
    var row = new LinkedHashMap<String,Object>();
    row.put("case_id",id); row.put("status",result.getStatusCode().value());
    row.put("issued_access",response.getHeader("Single-UI-Authorization")!=null);
    row.put("issued_refresh",response.getHeader("Single-UI-Refresh")!=null);
    row.put("assertions_passed",result.getStatusCode().value()==401 &&
      response.getHeader("Single-UI-Authorization")==null && response.getHeader("Single-UI-Refresh")==null);
    Files.writeString(Path.of(output,id+"-credential-case.json"),new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(row)+"\n");
  }
  public static void main(String[] args) throws Exception {
    var mapper = new ObjectMapper();
    var generator = KeyPairGenerator.getInstance("RSA"); generator.initialize(2048);
    var pair = generator.generateKeyPair();
    var props = new JWTConfigProperties();
    props.setPrv(Base64.getEncoder().encodeToString(pair.getPrivate().getEncoded()));
    props.setPub(Base64.getEncoder().encodeToString(pair.getPublic().getEncoded()));
    props.setTokenExpiration(15); props.setReTokenExpiration(225); props.setAbsoluteExpiration(60);
    var jwt = new JwtTokenUtil(props);
    var algorithm = Algorithm.RSA512((RSAPublicKey)pair.getPublic(),(RSAPrivateKey)pair.getPrivate());
    var rows = new ArrayList<Map<String,Object>>();
    for (boolean expired : new boolean[]{false,true}) {
      String sid = "synthetic-security-" + expired;
      var deny = new HashSet<String>();
      var repo = mock(ApplicationSessionRepo.class);
      when(repo.save(any(ApplicationSession.class))).thenAnswer(i -> {
        ApplicationSession s = i.getArgument(0); deny.add(s.getSessionId()); return s;
      });
      when(repo.findBySessionId(anyString())).thenAnswer(i -> deny.contains(i.getArgument(0))
        ? Optional.of(ApplicationSession.builder().sessionId(i.getArgument(0)).build()) : Optional.empty());
      var session = new SessionServiceImplementation(repo);
      var controller = new JwtAuthenticationController();
      set(controller,"jwtTokenUtil",jwt); set(controller,"objectMapper",mapper);
      set(controller,"sessionService",session); set(controller,"httpSession",new MockHttpSession());
      var cat = mock(ApplicationCategoryService.class); when(cat.getDrawers()).thenReturn(Optional.of(List.of()));
      set(controller,"applicationCategoryService",cat);
      var tile = mock(TileAuthorizationService.class); var ems = new Ems2Result(); ems.setEntities(List.of());
      when(tile.getEntitlements(anyString(),anyList())).thenReturn(ems); set(controller,"tileAuthorizationService",tile);
      var admin = mock(AdminModuleUtil.class); when(admin.getDrawer(anyList(),anyList())).thenReturn(List.of());
      set(controller,"adminModuleUtil",admin);
      var filter = mock(AuthFilterExecutor.class); when(filter.filterDrawersRaw(anyString(),anyList())).thenReturn(List.of());
      set(controller,"authFilterExecutor",filter);
      var now = System.currentTimeMillis();
      String access = JWT.create().withIssuer("single-ui-bff").withSubject("synthetic-user")
        .withClaim("id",sid).withClaim("oud","{}").withIssuedAt(new Date(now-60000))
        .withExpiresAt(new Date(expired ? now-10000 : now+60000)).sign(algorithm);
      String refresh = jwt.generateReToken("synthetic-user",Map.of("id",sid,"oud","{}"));
      if (!expired) {
        String expiredRefresh = JWT.create().withIssuer("single-ui-bff-refresh").withSubject("synthetic-user")
          .withClaim("id",sid).withClaim("oud","{}").withIssuedAt(new Date(now-60000))
          .withExpiresAt(new Date(now-10000)).sign(algorithm);
        String foreignIssuer = JWT.create().withIssuer("foreign-test-issuer").withSubject("synthetic-user")
          .withClaim("id",sid).withExpiresAt(new Date(now+60000)).sign(algorithm);
        String future = JWT.create().withIssuer("single-ui-bff-refresh").withSubject("synthetic-user")
          .withClaim("id",sid).withNotBefore(new Date(now+60000)).withExpiresAt(new Date(now+120000)).sign(algorithm);
        String unsigned = JWT.create().withIssuer("single-ui-bff-refresh").withSubject("synthetic-user")
          .withClaim("id",sid).withExpiresAt(new Date(now+60000)).sign(Algorithm.none());
        reject(controller,"Bearer "+expiredRefresh,"RN-S011",false,args[0]);
        reject(controller,"Bearer "+refresh.substring(0,refresh.lastIndexOf('.')+1)+(refresh.charAt(refresh.lastIndexOf('.')+1)=='A'?'B':'A')+refresh.substring(refresh.lastIndexOf('.')+2),"RN-S012",false,args[0]);
        reject(controller,"Bearer "+access,"RN-S013",false,args[0]);
        reject(controller,"Bearer "+jwt.generateEntitlementToken("synthetic-user",Map.of("id",sid)),"RN-S014",false,args[0]);
        reject(controller,"Bearer "+foreignIssuer,"RN-S015",false,args[0]);
        reject(controller,"Bearer "+unsigned,"RN-S016",false,args[0]);
        reject(controller,"Bearer malformed.two","RN-S017",false,args[0]);
        String expiredAccess = JWT.create().withIssuer("single-ui-bff").withSubject("synthetic-user")
          .withClaim("id",sid).withExpiresAt(new Date(now-10000)).sign(algorithm);
        reject(controller,"Bearer "+expiredAccess,"RN-S018",true,args[0]);
        reject(controller,"Bearer "+refresh,"RN-S019",true,args[0]);
        reject(controller,"Bearer "+future,"RN-S020",false,args[0]);
        reject(controller,null,"RN-S021",false,args[0]);
      }
      var input = new RequestOfJWT(); input.setSingleUIAuthorization("Bearer "+access);
      var logout = controller.logout(input,new MockHttpServletResponse());
      var request = new MockHttpServletRequest(); request.addHeader("Single-UI-Refresh","Bearer "+refresh);
      var response = new MockHttpServletResponse();
      var renewal = controller.relogin(new RequestOfRelogin(),request,response);
      var row = new LinkedHashMap<String,Object>();
      row.put("case_id",expired?"RN-S002":"RN-S001"); row.put("expired_access",expired);
      row.put("logout_status",logout.getStatusCode().value()); row.put("logout_result",logout.getBody().isResult());
      row.put("blacklist_entries",deny.size()); row.put("relogin_status",renewal.getStatusCode().value());
      row.put("relogin_result",renewal.getBody().isResult());
      row.put("new_access_issued",response.getHeader("Single-UI-Authorization")!=null);
      row.put("expected_relogin_status",401); row.put("security_assertion_passed",renewal.getStatusCode().value()==401);
      rows.add(row);
      Files.writeString(Path.of(args[0],expired?"expired-logout-case.json":"valid-logout-case.json"),mapper.writerWithDefaultPrettyPrinter().writeValueAsString(row)+"\n");
    }
    System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(rows));
  }
}
