import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.config.JWTConfigProperties;
import com.scb.sso.singleuibff.util.JwtTokenUtil;
import com.scb.fmoportal.auth.filter.AuthTokenFilter;
import com.scb.fmoportal.auth.properties.AuthProperties;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import java.nio.file.*;
import java.security.*;
import java.security.interfaces.*;
import java.util.*;

/** Ephemeral signed fixtures for an actual current-source client/SDK assertion chain. */
public class SignedCredentialBridge {
  public static void main(String[] args) throws Exception {
    var mapper=new ObjectMapper();Path dir=Path.of(args[1]);Files.createDirectories(dir);
    if(args[0].equals("issue")){
      var gen=KeyPairGenerator.getInstance("RSA");gen.initialize(2048);var pair=gen.generateKeyPair();
      Files.write(dir.resolve("private.der"),pair.getPrivate().getEncoded());Files.write(dir.resolve("public.der"),pair.getPublic().getEncoded());
      var algorithm=Algorithm.RSA512((RSAPublicKey)pair.getPublic(),(RSAPrivateKey)pair.getPrivate());var result=new LinkedHashMap<String,Object>();
      for(String subject:List.of("A","B")){
        String token=JWT.create().withIssuer("single-ui-bff").withSubject(subject).withClaim("id","bridge-"+subject).withClaim("oud","{}").withIssuedAt(new Date(System.currentTimeMillis()-1000)).withExpiresAt(new Date(System.currentTimeMillis()+900000)).sign(algorithm);
        result.put(subject,"Bearer "+token);
      }
      Files.writeString(dir.resolve("credentials.json"),mapper.writeValueAsString(result));
      System.out.println("Ephemeral signed credentials saved. No credential values emitted.");return;
    }
    String credential=mapper.readTree(Files.readString(Path.of(args[2]))).path("token").asText();String raw=credential.replace("Bearer ","");
    var props=new JWTConfigProperties();props.setPub(Base64.getEncoder().encodeToString(Files.readAllBytes(dir.resolve("public.der"))));props.setPrv(Base64.getEncoder().encodeToString(Files.readAllBytes(dir.resolve("private.der"))));
    var jwt=new JwtTokenUtil(props);boolean valid=jwt.validateToken(raw);jwt.handleIssuer(raw,"single-ui-bff");
    var p=new AuthProperties();p.setPub(props.getPub());var sdkJwt=new com.scb.fmoportal.auth.util.JwtTokenUtil(p,mapper);var filter=new AuthTokenFilter(new ArrayList<>(),p,mapper,sdkJwt);
    var req=new MockHttpServletRequest("GET","/synthetic/protected");req.addHeader("Single-UI-Authorization",credential);var response=new MockHttpServletResponse();var observed=new LinkedHashMap<String,Object>();observed.put("current_bff_jwt_valid",valid);
    filter.doFilter(req,response,(r,s)->{try{observed.put("sdk_authorization_subject",mapper.readTree((String)r.getAttribute("userInfo")).path("userId").asText());observed.put("protected_fixture_accepted",true);}catch(Exception e){throw new RuntimeException(e);}});
    observed.put("credential_sha256",HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(credential.getBytes(java.nio.charset.StandardCharsets.UTF_8))));observed.put("sdk_filter_status",response.getStatus());observed.put("limit","Actual current BFF verifier and SDK filter; synthetic servlet handler. No live business service or distributed revocation validation.");
    Files.writeString(Path.of(args[3]),mapper.writerWithDefaultPrettyPrinter().writeValueAsString(observed)+"\n");System.out.println("Validation saved without raw credentials.");
  }
}
