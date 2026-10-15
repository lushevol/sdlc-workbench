package com.scb.sso.singleuibff.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.scb.sso.singleuibff.config.EntraConfigProperties;
import com.scb.sso.singleuibff.exceptions.JwtException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;
import org.springframework.util.StringUtils;

import java.io.InputStream;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.KeyFactory;
import java.security.interfaces.RSAPrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.time.Instant;
import java.util.Base64;
import java.util.Date;
import java.util.Map;
import java.util.UUID;

@Slf4j
@RequiredArgsConstructor
public class ClientAssertionGenUtil {

    private static final long ASSERTION_TTL_SECONDS = 300; // 5 minutes

    private final EntraConfigProperties entraConfigProperties;

    private volatile Algorithm algorithm;
    private volatile String certificateThumbprint;

    public String generateClientAssertion() {
        String clientId = entraConfigProperties.getClientId();
        String tokenEndpoint = entraConfigProperties.getEntraTokenEndpoint();
        if (!StringUtils.hasText(clientId) || !StringUtils.hasText(tokenEndpoint)) {
            throw JwtException.builder().message("Missing client assertion configuration").build();
        }
        Instant now = Instant.now();
        return JWT.create()
            .withIssuer(clientId)
            .withSubject(clientId)
            .withAudience(tokenEndpoint)
            .withHeader(Map.of("x5t", getCertificateThumbprint()))
            .withJWTId(UUID.randomUUID().toString())
            .withIssuedAt(Date.from(now))
            .withNotBefore(Date.from(now))
            .withExpiresAt(Date.from(now.plusSeconds(ASSERTION_TTL_SECONDS)))
            .sign(getAlgorithm());
    }

    private Algorithm getAlgorithm() {
        Algorithm local = algorithm;
        if (local != null) {
            return local;
        }
        synchronized (this) {
            if (algorithm == null) {
                RSAPrivateKey privateKey = loadPrivateKey(entraConfigProperties.getClientKeyPath());
                algorithm = Algorithm.RSA256(null, privateKey);
            }
            return algorithm;
        }
    }

    private RSAPrivateKey loadPrivateKey(String keyPath) {
        if (!StringUtils.hasText(keyPath)) {
            throw JwtException.builder().message("Client key path is blank").build();
        }
        try {
            byte[] keyBytes = readKeyBytes(keyPath);
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            return (RSAPrivateKey) keyFactory.generatePrivate(new PKCS8EncodedKeySpec(keyBytes));
        } catch (Exception e) {
            log.error("Failed to load client private key from path: {}", keyPath, e);
            throw JwtException.builder().message("Unable to load client private key").build();
        }
    }

    private String getCertificateThumbprint() {
        String local = certificateThumbprint;
        if (local != null) {
            return local;
        }
        synchronized (this) {
            if (certificateThumbprint == null) {
                certificateThumbprint = loadCertificateThumbprint(entraConfigProperties.getClientCertPath());
            }
            return certificateThumbprint;
        }
    }

    private String loadCertificateThumbprint(String certPath) {
        if (!StringUtils.hasText(certPath)) {
            throw JwtException.builder().message("Client cert path is blank").build();
        }
        try {
            byte[] certDerBytes = readCertificateBytes(certPath);
            byte[] digest = MessageDigest.getInstance("SHA-1").digest(certDerBytes);
            return Base64.getUrlEncoder().withoutPadding().encodeToString(digest);
        } catch (Exception e) {
            log.error("Failed to load client certificate from path: {}", certPath, e);
            throw JwtException.builder().message("Unable to load client certificate").build();
        }
    }

    private byte[] readKeyBytes(String keyPath) throws Exception {
        String keyText = readKeyText(keyPath);
        String sanitized = keyText
            .replace("-----BEGIN PRIVATE KEY-----", "")
            .replace("-----END PRIVATE KEY-----", "")
            .replace("-----BEGIN RSA PRIVATE KEY-----", "")
            .replace("-----END RSA PRIVATE KEY-----", "")
            .replaceAll("\\s", "");
        return Base64.getDecoder().decode(sanitized);
    }

    private String readKeyText(String keyPath) throws Exception {
        URI uri = URI.create(keyPath);
        Path filePath = Path.of(uri);
        if (Files.exists(filePath)) {
            return Files.readString(filePath, StandardCharsets.UTF_8);
        }
        ClassPathResource resource = new ClassPathResource(keyPath);
        if (resource.exists()) {
            try (InputStream inputStream = resource.getInputStream()) {
                return new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
            }
        }
        throw new IllegalArgumentException("Client key path not found: " + keyPath);
    }

    private byte[] readCertificateBytes(String certPath) throws Exception {
        byte[] rawBytes = readResourceBytes(certPath);
        String asText = new String(rawBytes, StandardCharsets.UTF_8);
        if (asText.contains("BEGIN CERTIFICATE")) {
            String sanitized = asText
                .replace("-----BEGIN CERTIFICATE-----", "")
                .replace("-----END CERTIFICATE-----", "")
                .replaceAll("\\s", "");
            return Base64.getDecoder().decode(sanitized);
        }
        return rawBytes;
    }

    private byte[] readResourceBytes(String resourcePath) throws Exception {
        URI uri = URI.create(resourcePath);
        Path filePath = Path.of(uri);
        if (Files.exists(filePath)) {
            return Files.readAllBytes(filePath);
        }
        ClassPathResource resource = new ClassPathResource(resourcePath);
        if (resource.exists()) {
            try (InputStream inputStream = resource.getInputStream()) {
                return inputStream.readAllBytes();
            }
        }
        throw new IllegalArgumentException("Client cert path not found: " + resourcePath);
    }

}
