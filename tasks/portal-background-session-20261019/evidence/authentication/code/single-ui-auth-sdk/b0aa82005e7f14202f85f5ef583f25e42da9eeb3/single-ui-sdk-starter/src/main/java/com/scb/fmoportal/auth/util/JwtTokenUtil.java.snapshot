package com.scb.fmoportal.auth.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.fmoportal.auth.exception.JwtException;
import com.scb.fmoportal.auth.properties.AuthProperties;
import lombok.extern.slf4j.Slf4j;

import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.interfaces.RSAPublicKey;
import java.security.spec.X509EncodedKeySpec;
import java.util.*;

@Slf4j
public class JwtTokenUtil {
    private final String jwtIssuer = "single-ui-bff";
    private final String jwtIssuerEntitlement = "single-ui-bff-entitlement";
    private final JWTVerifier jwtVerifier;

    private final ObjectMapper objectMapper;

    public JwtTokenUtil(AuthProperties authProperties, ObjectMapper objectMapper) {
        try {
            this.objectMapper = objectMapper;
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            byte[] encodedForPublicKey = Base64.getMimeDecoder().decode(authProperties.getPub());
            RSAPublicKey rsaPublicKey = (RSAPublicKey) keyFactory.generatePublic(new X509EncodedKeySpec(encodedForPublicKey));

            Algorithm algorithm = Algorithm.RSA512(rsaPublicKey, null);
            jwtVerifier = JWT.require(algorithm).build();
        } catch (Exception e) {
            log.error("verify token failed, reason: {}", e.getMessage());
            throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - token is expired").build();
        }
    }

    public Optional<String> validateToken(String token) {
        DecodedJWT decodedJWT;
        try {
            decodedJWT = jwtVerifier.verify(token);
            if (!decodedJWT.getIssuer().equalsIgnoreCase(jwtIssuer)) {
                throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - invalid token").build();
            }
        } catch (Exception e) {
            log.error("verify token failed, reason: {}", e.getMessage());
            throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - token is expired").build();
        }
        Date max_age = decodedJWT.getClaim("max_age").asDate();
        Date now = new Date();
        if (Objects.nonNull(max_age) && max_age.before(now)) {
            throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - token is expired - reached absolute timeout").build();
        }
        String payload = decodedJWT.getPayload();
        String userData = new String(Base64.getMimeDecoder().decode(payload), StandardCharsets.UTF_8);
        return Optional.of(userData);
    }

    public String getEntitlementsToken(String token) {
        DecodedJWT decodedJWT;
        try {
            decodedJWT = jwtVerifier.verify(token);
            if (!decodedJWT.getIssuer().equalsIgnoreCase(jwtIssuerEntitlement)) {
                return null;
            }
            String payload = decodedJWT.getPayload();
            String userData = new String(Base64.getMimeDecoder().decode(payload), StandardCharsets.UTF_8);
            JsonNode userInfo = objectMapper.readValue(userData, JsonNode.class);
            if (Objects.nonNull(userInfo.get("entitlements"))) {
                return userInfo.get("entitlements").asText();
            }
        } catch (Exception e) {
            return null;
        }
        return null;
    }

    public void validateSession(String token, String sessionId, String url, List<JWTSessionData> jwtSessionDatas) {
        Date now = new Date();
        DecodedJWT decodedJWT;
        try {
            decodedJWT = jwtVerifier.verify(token);
            for (JWTSessionData jwtSessionData : jwtSessionDatas) {
                if (jwtSessionData.getSessionId().equals(sessionId)) {
                    throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - invalid token").build();
                } else if (jwtSessionData.getExpiredDate().before(now)) {
                    jwtSessionDatas.remove(jwtSessionData);
                }
            }
            Date expiredDate = decodedJWT.getExpiresAt();
            String[] urls = url.split("/");
            if (urls[urls.length - 1].equalsIgnoreCase("logout")) {
                JWTSessionData jwtSessionData = new JWTSessionData(sessionId, expiredDate);
                jwtSessionDatas.add(jwtSessionData);
            }
        } catch (Exception e) {
            log.error("verify token failed, reason: {}", e.getMessage());
            throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - token is expired").build();
        }
    }
}
