package com.scb.sso.singleuibff.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.TokenExpiredException;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.scb.sso.singleuibff.config.JWTConfigProperties;
import com.scb.sso.singleuibff.exceptions.JwtException;
import lombok.AllArgsConstructor;
import org.springframework.util.StringUtils;

import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.*;

import static com.scb.sso.singleuibff.util.Constant.*;

@AllArgsConstructor
public class JwtTokenUtil {

    private final Algorithm algorithm;
    private final JWTVerifier jwtVerifier;
    private JWTConfigProperties jwtConfigProperties;

    public JwtTokenUtil(JWTConfigProperties jwtConfigProperties) {
        this.jwtConfigProperties = jwtConfigProperties;

        try {
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");

            byte[] keyByte = Base64.getMimeDecoder().decode(jwtConfigProperties.getPrv());
            RSAPrivateKey rsaPrivateKey = (RSAPrivateKey) keyFactory.generatePrivate(new PKCS8EncodedKeySpec(keyByte));

            keyByte = Base64.getMimeDecoder().decode(jwtConfigProperties.getPub());
            RSAPublicKey rsaPublicKey = (RSAPublicKey) keyFactory.generatePublic(new X509EncodedKeySpec(keyByte));
            algorithm = Algorithm.RSA512(rsaPublicKey, rsaPrivateKey);
            jwtVerifier = JWT.require(algorithm).build();
        } catch (Exception e) {
            throw JwtException.builder().message("token is expired - error occurred while generating algorithm").build();
        }
    }

    public String generateToken(String userName, Map<String, String> payload) {
        Date expireAt = new Date(System.currentTimeMillis() + jwtConfigProperties.getTokenExpiration() * 60 * 1000);
        return doGenerateToken(userName, payload, expireAt, JWT_ISSUER);
    }

    public String generateReToken(String userName, Map<String, String> payload) {
        Date expireAt = new Date(System.currentTimeMillis() + 24000 + jwtConfigProperties.getReTokenExpiration() * 60 * 1000);
        return doGenerateToken(userName, payload, expireAt, JWT_ISSUER_REFRESH);
    }

    public String generateEntitlementToken(String userName, Map<String, String> payload) {
        Date expireAt = new Date(System.currentTimeMillis() + 12 * 60 * 60 * 1000);
        return doGenerateToken(userName, payload, expireAt, JWT_ISSUER_ENTITLEMENT);
    }

    private String doGenerateToken(String subject, Map<String, String> payload, Date expiresAt, String Issuer) {
        return JWT.create()
            .withIssuer(Issuer)
            .withExpiresAt(expiresAt)
            .withSubject(subject)
            .withIssuedAt(new Date())
            .withJWTId(JWT_ID)
            .withPayload(payload)
            .sign(algorithm);
    }

    public String doGenerateTokenWithAuthTime(String subject, Map<String, String> payload) {
        return JWT.create()
            .withIssuer(JWT_ISSUER)
            .withExpiresAt(new Date(System.currentTimeMillis() + jwtConfigProperties.getTokenExpiration() * 60 * 1000))
            .withSubject(subject)
            .withIssuedAt(new Date())
            .withJWTId(JWT_ID)
            .withPayload(payload)
            .withClaim(USER_LOGIN_TIME_KEY, new Date())
            .withClaim(ABSOLUTE_IDLE, new Date(System.currentTimeMillis() + jwtConfigProperties.getAbsoluteExpiration() * 60 * 1000))
            .sign(algorithm);
    }

    public boolean validateToken(String token) {
        try {
            DecodedJWT decodedJWT = jwtVerifier.verify(token);
            Date maxAge = decodedJWT.getClaim(ABSOLUTE_IDLE).asDate();
            Date now = new Date();
            if (Objects.nonNull(maxAge) && maxAge.before(now)) {
                throw JwtException.builder().message("token is expired - reached idle timeout").build();
            }
            return true;
        } catch (TokenExpiredException e) {
            throw JwtException.builder().message("token is expired - reached idle timeout").build();
        }
    }

    public Date getExpirationDate(String token) {
        if (Objects.isNull(token)) {
            return null;
        }
        DecodedJWT decodedJWT = JWT.decode(token);
        return decodedJWT.getExpiresAt();
    }

    public Date getMaxAge(String token) {
        if (Objects.isNull(token)) {
            return null;
        }
        DecodedJWT decodedJWT = JWT.decode(token);
        return decodedJWT.getClaim(ABSOLUTE_IDLE).asDate();
    }

    private String getIssuer(String token) {
        if (Objects.isNull(token)) {
            return null;
        }
        DecodedJWT decodedJWT = JWT.decode(token);
        return decodedJWT.getIssuer();
    }

    public String retrieveUserInfoFromToken(String token) {
        if (!validateToken(token)) {
            throw JwtException.builder().message("token is expired").build();
        }
        return retrieveUserInfo(token);
    }

    private String retrieveUserInfo(String token) {
        DecodedJWT decodedJWT = JWT.decode(token);
        String payload = decodedJWT.getPayload();
        return new String(Base64.getDecoder().decode(payload), StandardCharsets.UTF_8);
    }

    public void handleIssuer(String token, String issuer) {
        if (!Objects.requireNonNull(getIssuer(token)).equalsIgnoreCase(issuer)) {
            throw JwtException.builder().message("invalid token").build();
        }
    }

    public void handleIssuerAnalytics(String token, String issuer1, String issuer2) {
        if (!Objects.requireNonNull(getIssuer(token)).equalsIgnoreCase(issuer1)
            && !Objects.requireNonNull(getIssuer(token)).equalsIgnoreCase(issuer2)) {
            throw JwtException.builder().message("invalid token").build();
        }
    }

    public String retrieveHeaderToken(String inputHeaderValue) {
        if (!StringUtils.hasLength(inputHeaderValue)) {
            throw JwtException.builder().message("Invalid format").build();
        }
        String[] headerValue = inputHeaderValue.split(HEADER_JWT_TOKEN_VALUE_PREFIX);
        if (headerValue.length == 2) {
            return headerValue[1];
        }
        throw JwtException.builder().message("Invalid format").build();
    }

}
