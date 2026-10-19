package com.scb.sso.singleuibff.service.v1.implementation;

import com.auth0.jwt.JWT;
import com.auth0.jwt.interfaces.Claim;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.config.EntraConfigProperties;
import com.scb.sso.singleuibff.dto.entra.ResponseEntra;
import com.scb.sso.singleuibff.dto.request.RequestOfAuthenticate;
import com.scb.sso.singleuibff.exceptions.AuthenticationException;
import com.scb.sso.singleuibff.service.v1.EntraAuthenticationService;
import com.scb.sso.singleuibff.util.ClientAssertionGenUtil;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import static com.scb.sso.singleuibff.util.Constant.ENTRA_RELATED_CODE;

@Slf4j
@AllArgsConstructor
public class EntraAuthenticationServiceImpl implements EntraAuthenticationService {

    private RestTemplate restTemplate;

    private ObjectMapper objectMapper;

    private EntraConfigProperties entraConfigProperties;

    private ClientAssertionGenUtil clientAssertionGenUtil;

    public Map<String, String> authenticate(RequestOfAuthenticate authenticationRequest) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        LinkedMultiValueMap<String, String> entraRequestBody = new LinkedMultiValueMap<>();
        entraRequestBody.add("client_id", entraConfigProperties.getClientId());
        entraRequestBody.add("grant_type", entraConfigProperties.getGrantType());
        entraRequestBody.add("client_assertion_type", entraConfigProperties.getClientAssertionType());
        entraRequestBody.add("client_assertion", clientAssertionGenUtil.generateClientAssertion());
        entraRequestBody.add("scope", entraConfigProperties.getScope());
        entraRequestBody.add("code", authenticationRequest.getCode());
        entraRequestBody.add("redirect_uri", entraConfigProperties.getRedirectUri());

        HttpEntity<LinkedMultiValueMap<String, String>> request = new HttpEntity<>(entraRequestBody, headers);
        String url = entraConfigProperties.getEntraTokenEndpoint();
        try {
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                ResponseEntra responseEntra = objectMapper.readValue(response.getBody(), ResponseEntra.class);
                DecodedJWT decode = JWT.decode(responseEntra.getIdToken());
                authenticationRequest.setUsername(Objects.isNull(decode.getClaim("userId")) ? null : decode.getClaim("userId").asString());
                return initPayloadMFA(decode);
            } else {
                log.error("Entra authenticate failed, status: {}", response.getStatusCode());
                throw AuthenticationException.builder().code(ENTRA_RELATED_CODE)
                    .message("Entra authenticate failed.").build();
            }
        } catch (Exception e) {
            log.error("Error while getting response from Entra at endpoint {}", url, e);
            throw AuthenticationException.builder().code(ENTRA_RELATED_CODE).message("Entra authenticate failed.").build();

        }
    }

    private Map<String, String> initPayloadMFA(DecodedJWT decode) {
        HashMap<String, String> resultMap = new HashMap<>();
        List<String> claimKeys = List.of(
            "userId",
            "lastName",
            "firstName",
            "fullName",
            "emailId",
            "locale",
            "country"
        );
        for (String claimKey : claimKeys) {
            resultMap.put(claimKey, getClaimAsString(decode, claimKey));
        }
        return resultMap;
    }

    private String getClaimAsString(DecodedJWT decode, String claimKey) {
        Claim claim = decode.getClaim(claimKey);
        return Objects.isNull(claim) ? null : claim.asString();
    }

}
