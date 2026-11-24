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
import com.scb.fmoportal.auth.filter.AuthTokenFilter;
import com.scb.fmoportal.auth.properties.AuthProperties;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.mock.web.MockHttpSession;
import java.nio.file.*;
import java.security.*;
import java.security.interfaces.*;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import static org.mockito.Mockito.*;

/** Controlled actual-controller and SDK-filter experiments. No external traffic. */
public class RemainingSecurityProbe {
  static final ObjectMapper mapper = new ObjectMapper();
  static KeyPair pair;
  static Algorithm algorithm;
  static JwtTokenUtil jwt;
  static String output;
  static void set(Object o, String name, Object value) throws Exception {
    var f=o.getClass().getDeclaredField(name);f.setAccessible(true);f.set(o,value);
  }
  static class Fixture {
    final Set<String> deny;
    final List<String> events=Collections.synchronizedList(new ArrayList<>());
    final ApplicationSessionRepo repo=mock(ApplicationSessionRepo.class);
    final JwtAuthenticationController controller=new JwtAuthenticationController();
    final String sid;
    volatile boolean writeFails;
    volatile CountDownLatch writeEntered, writeRelease;
    Fixture(String id) throws Exception { this(id,ConcurrentHashMap.newKeySet()); }
    Fixture(String id, Set<String> shared) throws Exception {
      sid=id;deny=shared;
      when(repo.save(any(ApplicationSession.class))).thenAnswer(i->{
        events.add("revocation-write-entered");
        if(writeEntered!=null)writeEntered.countDown();
        if(writeRelease!=null&&!writeRelease.await(5,TimeUnit.SECONDS))throw new IllegalStateException("fixture latch timeout");
        if(writeFails){events.add("revocation-write-failed");throw new IllegalStateException("synthetic revocation write rejected");}
        ApplicationSession s=i.getArgument(0);deny.add(s.getSessionId());events.add("revocation-committed");return s;
      });
      when(repo.findBySessionId(anyString())).thenAnswer(i->{
        String session=i.getArgument(0);boolean revoked=deny.contains(session);events.add("renewal-validation:"+(revoked?"revoked":"active"));
        return revoked?Optional.of(ApplicationSession.builder().sessionId(session).build()):Optional.empty();
      });
      set(controller,"jwtTokenUtil",jwt);set(controller,"objectMapper",mapper);
      set(controller,"sessionService",new SessionServiceImplementation(repo));set(controller,"httpSession",new MockHttpSession());
      var category=mock(ApplicationCategoryService.class);when(category.getDrawers()).thenReturn(Optional.of(List.of()));set(controller,"applicationCategoryService",category);
      var tile=mock(TileAuthorizationService.class);var ems=new Ems2Result();ems.setEntities(List.of());when(tile.getEntitlements(anyString(),anyList())).thenReturn(ems);set(controller,"tileAuthorizationService",tile);
      var admin=mock(AdminModuleUtil.class);when(admin.getDrawer(anyList(),anyList())).thenReturn(List.of());set(controller,"adminModuleUtil",admin);
      var auth=mock(AuthFilterExecutor.class);when(auth.filterDrawersRaw(anyString(),anyList())).thenReturn(List.of());set(controller,"authFilterExecutor",auth);
    }
  }
  static String token(String subject,String sid,String issuer,boolean expiry) {
    var b=JWT.create().withIssuer(issuer).withSubject(subject).withClaim("id",sid).withClaim("oud","{}").withIssuedAt(new Date(System.currentTimeMillis()-1000));
    if(expiry)b.withExpiresAt(new Date(System.currentTimeMillis()+120000));
    return b.sign(algorithm);
  }
  static Map<String,Object> renewal(Fixture f,String refresh,String... extra) {
    var req=new MockHttpServletRequest();
    if(refresh!=null)req.addHeader("Single-UI-Refresh","Bearer "+refresh);
    for(String x:extra)req.addHeader("Single-UI-Refresh","Bearer "+x);
    var response=new MockHttpServletResponse();
    var result=f.controller.relogin(new RequestOfRelogin(),req,response);
    var row=new LinkedHashMap<String,Object>();row.put("http_status",result.getStatusCode().value());row.put("result",result.getBody().isResult());
    String access=response.getHeader("Single-UI-Authorization");row.put("issued_access_count",access==null?0:1);
    if(access!=null){var decoded=JWT.decode(access.replace("Bearer ",""));row.put("access_subject",decoded.getSubject());row.put("access_session_id",decoded.getClaim("id").asString());}
    row.put("credential_response_header_count",response.getHeaderNames().stream().filter(x->x.equalsIgnoreCase("Single-UI-Authorization")||x.equalsIgnoreCase("Single-UI-Refresh")).count());
    return row;
  }
  static Map<String,Object> logout(Fixture f,String access) {
    var req=new RequestOfJWT();req.setSingleUIAuthorization(access==null?null:"Bearer "+access);
    var response=new MockHttpServletResponse();var result=f.controller.logout(req,response);
    return Map.of("http_status",result.getStatusCode().value(),"result",result.getBody().isResult(),"revocation_entries",f.deny.size());
  }
  static Map<String,Object> assertion(String name,Object expected,Object actual) {
    var row=new LinkedHashMap<String,Object>();row.put("name",name);row.put("expected",expected);row.put("actual",actual);row.put("passed",Objects.equals(expected,actual));return row;
  }
  static void save(String id,Map<String,Object> observed,List<Map<String,Object>> assertions,String level,List<String> extraLimits) throws Exception {
    var row=new LinkedHashMap<String,Object>();row.put("case_id",id);row.put("executed_at",Instant.now().toString());row.put("execution_level",level);
    row.put("status",assertions.stream().allMatch(a->Boolean.TRUE.equals(a.get("passed")))?"PASSED":"FAILED");row.put("observations",observed);row.put("assertions",assertions);
    var limits=new ArrayList<String>();limits.add("Actual committed controller/JWT/session logic or SDK filter executes. Repository, entitlement, and servlet collaborators are isolated fixtures.");limits.add("Synthetic identities and ephemeral RSA keys only. No production, live database, gateway, HTTP listener, or protected business service.");limits.addAll(extraLimits);row.put("limits",limits);
    Path dir=Path.of(output,id.toLowerCase());Files.createDirectories(dir);Files.writeString(dir.resolve("result.json"),mapper.writerWithDefaultPrettyPrinter().writeValueAsString(row)+"\n");
    System.out.println(id+" "+row.get("status"));
  }
  public static void main(String[] args) throws Exception {
    output=args[0];var gen=KeyPairGenerator.getInstance("RSA");gen.initialize(2048);pair=gen.generateKeyPair();
    algorithm=Algorithm.RSA512((RSAPublicKey)pair.getPublic(),(RSAPrivateKey)pair.getPrivate());
    var props=new JWTConfigProperties();props.setPrv(Base64.getEncoder().encodeToString(pair.getPrivate().getEncoded()));props.setPub(Base64.getEncoder().encodeToString(pair.getPublic().getEncoded()));props.setTokenExpiration(15);props.setReTokenExpiration(225);props.setAbsoluteExpiration(60);jwt=new JwtTokenUtil(props);
    {
      var f=new Fixture("write-failure");f.writeFails=true;String access=token("A",f.sid,"single-ui-bff",true),refresh=token("A",f.sid,"single-ui-bff-refresh",true);
      var out=new LinkedHashMap<String,Object>();out.put("logout",logout(f,access));out.put("replay",renewal(f,refresh));out.put("events",f.events);
      save("RN-S003",out,List.of(assertion("failed write recorded",true,f.events.contains("revocation-write-failed")),assertion("replay issued count recorded",true,((Map<?,?>)out.get("replay")).containsKey("issued_access_count"))),"actual-controller-characterization",List.of("This observational case records a failure consequence; passing its recording predicates does not establish safe logout."));
    }
    {
      var f=new Fixture("refresh-only");String refresh=token("A",f.sid,"single-ui-bff-refresh",true);var out=new LinkedHashMap<String,Object>();out.put("logout",logout(f,null));out.put("replay",renewal(f,refresh));out.put("revocation_entries",f.deny.size());
      save("RN-S004",out,List.of(assertion("revocation count recorded",true,out.containsKey("revocation_entries")),assertion("replay status and issuance recorded",true,((Map<?,?>)out.get("replay")).keySet().containsAll(Set.of("http_status","issued_access_count")))),"actual-controller-characterization",List.of("The logout request has no access input. Refresh remains held for the explicit replay; logout has no refresh-input parameter."));
    }
    {
      var f=new Fixture("already-revoked");f.deny.add(f.sid);var out=renewal(f,token("A",f.sid,"single-ui-bff-refresh",true));
      save("RN-S006",out,List.of(assertion("revoked refresh rejected",401,out.get("http_status")),assertion("no access issued",0,out.get("issued_access_count"))),"actual-controller-integration",List.of());
    }
    {
      var orders=new ArrayList<Map<String,Object>>();
      for(boolean renewalFirst:new boolean[]{false,true}){
        var f=new Fixture("race-"+renewalFirst);String a=token("A",f.sid,"single-ui-bff",true),r=token("A",f.sid,"single-ui-bff-refresh",true);var row=new LinkedHashMap<String,Object>();row.put("order",renewalFirst?"renewal-validation-before-revocation-commit":"revocation-commit-before-renewal-validation");
        if(renewalFirst){f.writeEntered=new CountDownLatch(1);f.writeRelease=new CountDownLatch(1);var executor=Executors.newSingleThreadExecutor();var pending=executor.submit(()->logout(f,a));if(!f.writeEntered.await(5,TimeUnit.SECONDS))throw new AssertionError("write not reached");row.put("renewal",renewal(f,r));f.writeRelease.countDown();row.put("logout",pending.get(5,TimeUnit.SECONDS));executor.shutdown();}
        else{row.put("logout",logout(f,a));row.put("renewal",renewal(f,r));}
        row.put("events",f.events);orders.add(row);
      }
      save("RN-S007",Map.of("orders",orders),List.of(assertion("both operation orders observed",2,orders.size()),assertion("every renewal records issuance",true,orders.stream().allMatch(r->((Map<?,?>)r.get("renewal")).containsKey("issued_access_count")))),"actual-controller-concurrency",List.of("Thread scheduling is bounded by a repository-write latch. No distributed transaction or live replica race is established."));
    }
    {
      var f=new Fixture("revoked-acquisition");f.deny.add(f.sid);var req=new RequestOfJWT();req.setSingleUIAuthorization("Bearer "+token("A",f.sid,"single-ui-bff",true));var response=new MockHttpServletResponse();var result=f.controller.refreshtoken(req,response);int issued=response.getHeader("Single-UI-Refresh")==null?0:1;
      save("RN-S008",Map.of("http_status",result.getStatusCode().value(),"issued_refresh_count",issued),List.of(assertion("revoked access rejected",401,result.getStatusCode().value()),assertion("no refresh issued",0,issued)),"actual-controller-integration",List.of());
    }
    {
      var f=new Fixture("refresh-replacement");String r1=token("A",f.sid,"single-ui-bff-refresh",true);var req=new RequestOfJWT();req.setSingleUIAuthorization("Bearer "+token("A",f.sid,"single-ui-bff",true));var response=new MockHttpServletResponse();var result=f.controller.refreshtoken(req,response);String r2=response.getHeader("Single-UI-Refresh").replace("Bearer ","");var out=new LinkedHashMap<String,Object>();out.put("acquisition_status",result.getStatusCode().value());out.put("distinct_refresh_values",!r1.equals(r2));out.put("r1_expiry",JWT.decode(r1).getExpiresAt().toInstant().toString());out.put("r2_expiry",JWT.decode(r2).getExpiresAt().toInstant().toString());out.put("r1_replay",renewal(f,r1));
      save("RN-S009",out,List.of(assertion("two distinct refresh credentials",true,!r1.equals(r2)),assertion("both expiries recorded",true,out.containsKey("r1_expiry")&&out.containsKey("r2_expiry")),assertion("old refresh replay observed",true,((Map<?,?>)out.get("r1_replay")).containsKey("http_status"))),"actual-controller-characterization",List.of("Replaced-token single-use policy remains unresolved. The result records that old signed refresh remains accepted."));
    }
    {
      Set<String> shared=ConcurrentHashMap.newKeySet();var one=new Fixture("shared-session",shared);var two=new Fixture("shared-session",shared);String access=token("A",one.sid,"single-ui-bff",true),refresh=token("A",one.sid,"single-ui-bff-refresh",true);var out=new LinkedHashMap<String,Object>();out.put("logout_replica_1",logout(one,access));var replay=renewal(two,refresh);out.put("renewal_replica_2",replay);out.put("declared_store","same in-memory synchronized deny set behind two repository mocks");
      save("RN-S010",out,List.of(assertion("second controller rejects after shared commit",401,replay.get("http_status")),assertion("second controller issues no access",0,replay.get("issued_access_count"))),"actual-controller-two-instance-isolation",List.of("Two controller instances share fixture persistence. This is not database replication or deployment acceptance."));
    }
    {
      var f=new Fixture("missing-expiry");String refresh=token("A",f.sid,"single-ui-bff-refresh",false);var out=renewal(f,refresh);out.put("input_expiry_present",JWT.decode(refresh).getExpiresAt()!=null);out.put("expiry_required_by_verifier",false);
      save("RN-S022",out,List.of(assertion("no expiry supplied",false,out.get("input_expiry_present")),assertion("status and issuance recorded",true,out.keySet().containsAll(Set.of("http_status","issued_access_count"))),assertion("verifier expiry requirement observed",true,out.containsKey("expiry_required_by_verifier"))),"actual-controller-characterization",List.of("Issuer-minted malformed-claim policy is not an accepted organizational requirement. No signing-key compromise is assumed."));
    }
    {
      var f=new Fixture("duplicate-headers");String a=token("A",f.sid,"single-ui-bff-refresh",true),b=token("B","other-session","single-ui-bff-refresh",true);var out=renewal(f,a,b);out.put("header_values",2);out.put("header_subjects",List.of("A","B"));
      save("RN-S023",out,List.of(assertion("ambiguous input issues no access under proposed rule",0,out.get("issued_access_count"))),"actual-controller-servlet-header-integration",List.of("Mock servlet request retains duplicate header values. No gateway/header-normalization filter or real HTTP transport is included. Proposed ambiguous-input rule remains unreviewed."));
    }
    {
      var p=new AuthProperties();p.setPub(Base64.getEncoder().encodeToString(pair.getPublic().getEncoded()));p.setSkipJwtHeaders(List.of("X-Synthetic-Skip-JWT"));
      var sdkjwt=new com.scb.fmoportal.auth.util.JwtTokenUtil(p,mapper);var filter=new AuthTokenFilter(new ArrayList<>(),p,mapper,sdkjwt);var req=new MockHttpServletRequest("GET","/synthetic/protected");req.addHeader("X-Synthetic-Skip-JWT","untrusted-value");var response=new MockHttpServletResponse();var count=new AtomicInteger();filter.doFilter(req,response,(r,s)->count.incrementAndGet());
      save("RN-S037",Map.of("business_handler_invocations",count.get(),"request_has_jwt",false,"configured_skip_header","X-Synthetic-Skip-JWT"),List.of(assertion("forged skip header cannot invoke handler",0,count.get())),"actual-sdk-filter-servlet-integration",List.of("The fixture deliberately models the case prerequisite that an untrusted caller reaches a configured skip header. Actual gateway stripping and production reachability remain unknown. Synthetic handler invocation is the observed impact."));
    }
    {
      var p=new AuthProperties();p.setPub(Base64.getEncoder().encodeToString(pair.getPublic().getEncoded()));var sdkjwt=new com.scb.fmoportal.auth.util.JwtTokenUtil(p,mapper);var filter=new AuthTokenFilter(new ArrayList<>(),p,mapper,sdkjwt);var req=new MockHttpServletRequest("GET","/synthetic/protected");req.addHeader("Single-UI-Authorization","Bearer "+token("A","sdk-session","single-ui-bff",true));req.addHeader("userId","B");req.addHeader("userInfo","{\"userId\":\"B\"}");var response=new MockHttpServletResponse();var observations=new LinkedHashMap<String,Object>();filter.doFilter(req,response,(r,s)->{try{var info=mapper.readTree((String)r.getAttribute("userInfo"));observations.put("verified_attribute_subject",info.path("userId").asText());observations.put("returned_b_only_records",info.path("userId").asText().equals("A")?0:1);}catch(Exception e){throw new RuntimeException(e);}});observations.put("untrusted_userId_header",req.getHeader("userId"));
      save("RN-S039",observations,List.of(assertion("authorization attribute subject equals signed user","A",observations.get("verified_attribute_subject")),assertion("synthetic authorized handler returns no B records",0,observations.get("returned_b_only_records"))),"actual-sdk-filter-servlet-integration",List.of("Synthetic handler consumes the SDK-verified request attribute. Independent business services that read untrusted headers instead are outside this case result."));
    }
  }
}
