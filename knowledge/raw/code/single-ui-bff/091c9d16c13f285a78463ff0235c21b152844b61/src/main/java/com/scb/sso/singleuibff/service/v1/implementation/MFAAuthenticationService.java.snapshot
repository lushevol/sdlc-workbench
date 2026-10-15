package com.scb.sso.singleuibff.service.v1.implementation;

import com.auth0.jwt.JWT;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.Maps;
import com.scb.sso.singleuibff.config.MFAConfigProperties;
import com.scb.sso.singleuibff.dto.mfa.ResponseMFA;
import com.scb.sso.singleuibff.dto.request.RequestOfAuthenticate;
import com.scb.sso.singleuibff.exceptions.AuthenticationException;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import static com.scb.sso.singleuibff.util.Constant.MFA_RELATED_CODE;

/**
 * @deprecated
 */
@Slf4j
@AllArgsConstructor
public class MFAAuthenticationService {

    private RestTemplate restTemplate;

    private ObjectMapper objectMapper;

    private MFAConfigProperties mfaConfigProperties;

    public Map<String, String> authenticate(RequestOfAuthenticate authenticationRequest) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
        headers.setAll(mfaConfigProperties.getHeaders());

        LinkedMultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("client_id", authenticationRequest.getClientId());
        map.add("grant_type", mfaConfigProperties.getGrantType());
        map.add("code", authenticationRequest.getCode());
        map.add("redirect_uri", mfaConfigProperties.getRedirectUri());

        HttpEntity<LinkedMultiValueMap<String, String>> request = new HttpEntity<>(map, headers);
        String url = authenticationRequest.getIss() + mfaConfigProperties.getAccessToken();
        try {
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                ResponseMFA responseMFA = objectMapper.readValue(response.getBody(), ResponseMFA.class);
                DecodedJWT decode = JWT.decode(responseMFA.getIdToken());
                authenticationRequest.setUsername(Objects.isNull(decode.getClaim("name")) ? null : decode.getClaim("name").asString());
                return initPayloadMFA(decode);
            } else {
                log.error("MFA authenticate failed, status: {}", response.getStatusCode());
                throw AuthenticationException.builder().code(MFA_RELATED_CODE)
                    .message("MFA authenticate failed.").build();
            }
        } catch (Exception e) {
            log.error("Error while getting response from MFA at endpoint {}", url, e);
            throw AuthenticationException.builder().code(MFA_RELATED_CODE).message("MFA authenticate failed.").build();

        }
    }

    private Map<String, String> initPayloadMFA(DecodedJWT decode) {
        HashMap<String, String> resultMap = Maps.newHashMap();
        final String country = "country";
        final String locale = "locale";
        final String fullName = "full_name";
        final String givenName = "given_name";
        final String familyName = "family_name";
        final String email = "email";
        resultMap.put("userId", Objects.isNull(decode.getClaim("name")) ? null : decode.getClaim("name").asString());
        resultMap.put("lastName", Objects.isNull(decode.getClaim(familyName)) ? null : decode.getClaim(familyName).asString());
        resultMap.put("firstName", Objects.isNull(decode.getClaim(givenName)) ? null : decode.getClaim(givenName).asString());
        resultMap.put("fullName", Objects.isNull(decode.getClaim(fullName)) ? null : decode.getClaim(fullName).asString());
        resultMap.put("emailId", Objects.isNull(decode.getClaim(email)) ? null : decode.getClaim(email).asString());
        resultMap.put(locale, Objects.isNull(decode.getClaim(locale)) ? null : decode.getClaim(locale).asString());
        resultMap.put(country, Objects.isNull(decode.getClaim(country)) ? null : decode.getClaim(country).asString());
        return resultMap;
    }

}
