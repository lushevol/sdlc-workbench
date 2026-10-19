package com.scb.sso.singleuibff.controller.v2;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.dto.ems2.v2.Action;
import com.scb.sso.singleuibff.dto.ems2.v2.Ems2Result;
import com.scb.sso.singleuibff.dto.ems2.v2.Entity;
import com.scb.sso.singleuibff.dto.ems2.v2.Subject;
import com.scb.sso.singleuibff.dto.request.RequestOfAnalytics;
import com.scb.sso.singleuibff.dto.request.RequestOfAuthenticate;
import com.scb.sso.singleuibff.dto.request.RequestOfAuthenticateEntra;
import com.scb.sso.singleuibff.dto.request.RequestOfJWT;
import com.scb.sso.singleuibff.dto.request.RequestOfRelogin;
import com.scb.sso.singleuibff.dto.response.ResponseOfAuthenticate;
import com.scb.sso.singleuibff.exceptions.AuthenticationException;
import com.scb.sso.singleuibff.exceptions.JwtException;
import com.scb.sso.singleuibff.exceptions.RecordNotFoundException;
import com.scb.sso.singleuibff.service.v1.*;
import com.scb.sso.singleuibff.service.v1.implementation.MFAAuthenticationService;
import com.scb.sso.singleuibff.service.v1.implementation.OUDAuthenticationService;
import com.scb.sso.singleuibff.service.v2.AuthorizationService;
import com.scb.sso.singleuibff.util.AdminModuleUtil;
import com.scb.sso.singleuibff.util.JwtTokenUtil;
import com.scb.sso.singleuibff.util.OudUtil;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;
import java.util.stream.Collectors;

import static com.scb.sso.singleuibff.util.Constant.*;

@Slf4j
@RestController
public class JwtAuthenticationController {

    @Autowired
    private OUDAuthenticationService oudAuthenticationService;
    @Autowired
    private MFAAuthenticationService mfaAuthenticationService;
    @Autowired
    private EntraAuthenticationService entraAuthenticationService;
    @Autowired
    private AuthorizationService authorizationService;
    @Autowired
    private JwtTokenUtil jwtTokenUtil;
    @Autowired
    private ObjectMapper objectMapper;
    @Autowired
    private OudUtil oudUtil;
    @Autowired
    private HttpSession httpSession;
    @Autowired
    private SessionService sessionService;
    @Autowired
    private AnalyticService analyticService;
    @Autowired
    private ApplicationCategoryService applicationCategoryService;
    @Autowired
    private AdminModuleUtil adminModuleUtil;

    private void hanldeAnalytics(RequestOfAuthenticate request, HttpServletRequest httpServletRequest) {
        RequestOfAnalytics requestOfAnalytics = new RequestOfAnalytics();
        requestOfAnalytics.setKey("button");
        requestOfAnalytics.setEvent("click");
        requestOfAnalytics.setContainer("Base");
        requestOfAnalytics.setTile("Login");
        if (StringUtils.isBlank(request.getCode())) {
            requestOfAnalytics.setName("normal login");
            analyticService.insertData(requestOfAnalytics, request.getUsername(), oudUtil.getIp(httpServletRequest));
        } else {
            // If the "iss" and "client_id" claim are blank, it indicates the authentication
            // is from Entra SSO, otherwise it is from MFA.
            Boolean isEntraSSO = StringUtils.isBlank(request.getIss()) && StringUtils.isBlank(request.getClientId());
            if (isEntraSSO) {
                requestOfAnalytics.setName("entra sso login");
            } else {
                requestOfAnalytics.setName("sso login");
            }
            analyticService.insertData(requestOfAnalytics, request.getUsername(), oudUtil.getIp(httpServletRequest));
        }
    }

    private Map<String, Object> buildEntities(HttpServletResponse response, String username,
        String oudString, String sessionId) throws JsonProcessingException, RecordNotFoundException {
        List<Map<String, Object>> applicationCategories = applicationCategoryService.getDrawers().get();
        final List<String> ems2Entities = adminModuleUtil.getEntityFromApplicationCategory(applicationCategories);
        Ems2Result ems2Result = authorizationService.getEntitlements(username, ems2Entities);
        List<Entity> entities = ems2Result.getEntities();
        List<Map<String, Object>> drawers = adminModuleUtil.getDrawer(applicationCategories, entities);
        String jsonString = buildEntitlementString(entities);
        Map<String, String> userInfoPayload = new HashMap<>();
        userInfoPayload.put("oud", oudString);
        userInfoPayload.put(SESSION_ID, sessionId);
        Map<String, String> entitlementsPayload = new HashMap<>();
        entitlementsPayload.put("entitlements", jsonString);
        final String entitlementsToken = jwtTokenUtil.generateEntitlementToken(username, entitlementsPayload);
        final String token = jwtTokenUtil.doGenerateTokenWithAuthTime(username, userInfoPayload);
        response.setHeader(HEADER_JWT_TOKEN, HEADER_JWT_TOKEN_VALUE_PREFIX.concat(token));
        Map<String, Object> returnObject = new HashMap<>();
        returnObject.put("entities", entities);
        returnObject.put("token", token);
        returnObject.put("entitlementsToken", entitlementsToken);
        returnObject.put("drawers", drawers);
        return returnObject;
    }

    private String buildEntitlementString(List<Entity> entities) throws JsonProcessingException {
        Map<String, Object> entitlements = new HashMap<>();
        entities.stream().forEach(entity -> {
            String entityRole = entity.getName() + ":" + entity.getRoleName();
            Map<String, Object> action = new HashMap<>();
            List<Subject> subjects = entity.getSubjects();
            subjects.stream().forEach(subject -> {
                List<String> actions = subject.getActions().stream().map(Action::getName).collect(Collectors.toList());
                action.put(subject.getName(), actions);
            });
            entitlements.put(entityRole, action);
        });
        return objectMapper.writeValueAsString(entitlements);
    }

    private String retrieveToken(String inputHeaderValue) {
        if (StringUtils.isEmpty(inputHeaderValue)) {
            throw JwtException.builder().message("jwtToken is empty, validation failed.").build();
        }
        String[] headerValue = inputHeaderValue.split(HEADER_JWT_TOKEN_VALUE_PREFIX);
        if (headerValue.length == 2) {
            return headerValue[1];
        }
        throw JwtException.builder().message("jwtToken is empty, validation failed.").build();
    }

    private void clearCookie(HttpServletResponse response) {
        Cookie sessionCookie = new Cookie("JSESSIONID", "");
        sessionCookie.setMaxAge(0);
        sessionCookie.setPath("/");
        sessionCookie.setHttpOnly(true);
        sessionCookie.setSecure(true);
        sessionCookie.setAttribute("SameSite", "Strict");
        response.addCookie(sessionCookie);
    }

    @PostMapping(value = "v2/sso/login")
    public ResponseEntity<ResponseOfAuthenticate> authenticate(@RequestBody RequestOfAuthenticate request,
        HttpServletRequest httpServletRequest, HttpServletResponse response) throws JsonProcessingException {
        try {
            request.setHostName(httpServletRequest.getServerName());
            Map<String, String> oud;
            if (StringUtils.isBlank(request.getCode())) {
                oud = oudAuthenticationService.authenticate(request);
            } else {
                oud = mfaAuthenticationService.authenticate(request);
            }
            if (Objects.isNull(oud.get("fullName"))) {
                oud.put("fullName", request.getUsername());
            }
            final String oudString = objectMapper.writeValueAsString(oud);
            Map<String, Object> returnObject = buildEntities(response, request.getUsername(), oudString, httpSession.getId());
            final List<Entity> entities = (List<Entity>) returnObject.get("entities");
            final String jwtToken = (String) returnObject.get("token");
            final String entitlementsToken = (String) returnObject.get("entitlementsToken");
            final List<Map<String, Object>> drawers = (List<Map<String, Object>>) returnObject.get("drawers");
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            hanldeAnalytics(request, httpServletRequest);
            clearCookie(response);
            return ResponseEntity.ok(
                ResponseOfAuthenticate.builder().entitlementsToken(entitlementsToken).oud(oudString).result(true).drawers(drawers)
                    .entities(entities)
                    .userInfo(userInfo).build());
        } catch (AuthenticationException exception) {
            log.info("login failed, reason: {}", exception.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                ResponseOfAuthenticate.builder().result(false)
                    .errorMessage(
                        "AuthenticationException: ".concat(exception.getCode()).concat(" - ").concat(exception.getMessage()))
                    .build());
        } catch (Exception e) {
            log.info("login failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                ResponseOfAuthenticate.builder().result(false).errorMessage("AuthenticationException: ".concat(e.getMessage())).build());
        }
    }

    @PostMapping(value = "v3/sso/login")
    public ResponseEntity<ResponseOfAuthenticate> authenticateEntra(@RequestBody RequestOfAuthenticateEntra request,
        HttpServletRequest httpServletRequest, HttpServletResponse response) throws JsonProcessingException {
        try {
            request.setHostName(httpServletRequest.getServerName());
            // convert Entra-specific request to the common RequestOfAuthenticate
            RequestOfAuthenticate authRequest = new RequestOfAuthenticate();
            authRequest.setUsername(request.getUsername());
            authRequest.setPassword(request.getPassword());
            authRequest.setCode(request.getCode());
            authRequest.setHostName(request.getHostName());
            authRequest.setEntities(request.getEntities());

            Map<String, String> userInfoMap;
            if (StringUtils.isBlank(authRequest.getCode())) {
                userInfoMap = oudAuthenticationService.authenticate(authRequest);
            } else {
                userInfoMap = entraAuthenticationService.authenticate(authRequest);
            }
            if (Objects.isNull(userInfoMap.get("fullName"))) {
                userInfoMap.put("fullName", request.getUsername());
            }
            final String oudString = objectMapper.writeValueAsString(userInfoMap);
            Map<String, Object> returnObject = buildEntities(response, authRequest.getUsername(), oudString, httpSession.getId());
            final List<Entity> entities = (List<Entity>) returnObject.get("entities");
            final String jwtToken = (String) returnObject.get("token");
            final String entitlementsToken = (String) returnObject.get("entitlementsToken");
            final List<Map<String, Object>> drawers = (List<Map<String, Object>>) returnObject.get("drawers");
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            // reuse analytics helper by passing the converted auth request
            hanldeAnalytics(authRequest, httpServletRequest);
            clearCookie(response);
            return ResponseEntity.ok(
                ResponseOfAuthenticate.builder().entitlementsToken(entitlementsToken).oud(oudString).result(true).drawers(drawers)
                    .entities(entities)
                    .userInfo(userInfo).build());
        } catch (AuthenticationException exception) {
            log.info("entra login failed, reason: {}", exception.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                ResponseOfAuthenticate.builder().result(false)
                    .errorMessage(
                        "AuthenticationException: ".concat(exception.getCode()).concat(" - ").concat(exception.getMessage()))
                    .build());
        } catch (Exception e) {
            log.info("entra login failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                ResponseOfAuthenticate.builder().result(false).errorMessage("AuthenticationException: ".concat(e.getMessage())).build());
        }
    }

    @PostMapping(value = "v2/sso/validate")
    public ResponseEntity<ResponseOfAuthenticate> checkTokenValidity(@RequestBody RequestOfJWT requestOfJWT,
        HttpServletResponse response) {
        try {
            String jwtToken = retrieveToken(requestOfJWT.getSingleUIAuthorization());
            boolean result = jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuer(jwtToken, JWT_ISSUER);
            Date expirationDate = jwtTokenUtil.getExpirationDate(jwtToken);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.validateSession(payload.get(SESSION_ID));
            final String userName = payload.get("sub");
            final String oudString = payload.get("oud");
            final String sessionId = payload.get(SESSION_ID);
            final Map<String, Object> returnObject = buildEntities(response, userName, oudString, sessionId);
            final List<Entity> entities = (List<Entity>) returnObject.get("entities");
            final String entitlementsToken = (String) returnObject.get("entitlementsToken");
            final List<Map<String, Object>> drawers = (List<Map<String, Object>>) returnObject.get("drawers");
            clearCookie(response);
            return ResponseEntity
                .ok(ResponseOfAuthenticate.builder().entitlementsToken(entitlementsToken).oud(oudString).result(result).drawers(drawers)
                    .entities(entities)
                    .userInfo(userInfo).expiration(expirationDate).build());
        } catch (Exception e) {
            log.info("token validate failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ResponseOfAuthenticate.builder().result(false).errorMessage("TOKEN_INVALID_EXPIRED - ".concat(e.getMessage())).build());
        }
    }

    @PostMapping(value = "v2/sso/extend")
    public ResponseEntity<ResponseOfAuthenticate> extend(@RequestBody RequestOfJWT requestOfJWT, HttpServletResponse response) {
        try {
            String jwtToken = retrieveToken(requestOfJWT.getSingleUIAuthorization());
            boolean result = jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuer(jwtToken, JWT_ISSUER);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.validateSession(payload.get(SESSION_ID));
            String userName = payload.get("sub");
            payload.remove("exp");
            payload.remove("iat");
            String newJwtToken = jwtTokenUtil.generateToken(userName, payload);
            Date newExpirationDate = jwtTokenUtil.getExpirationDate(newJwtToken);
            Date maxAge = jwtTokenUtil.getMaxAge(newJwtToken);
            if (Objects.nonNull(maxAge) && newExpirationDate.after(maxAge)) {
                newJwtToken = jwtTokenUtil.doGenerateTokenWithAuthTime(userName, payload);
                newExpirationDate = jwtTokenUtil.getExpirationDate(newJwtToken);
            }
            response.setHeader(HEADER_JWT_TOKEN, HEADER_JWT_TOKEN_VALUE_PREFIX.concat(newJwtToken));
            return ResponseEntity.ok(ResponseOfAuthenticate.builder().result(result).expiration(newExpirationDate).build());
        } catch (Exception e) {
            log.info("token extend failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ResponseOfAuthenticate.builder().result(false).errorMessage("TOKEN_INVALID_EXPIRED - ".concat(e.getMessage())).build());
        }
    }

    @PostMapping(value = "v2/sso/refreshtoken")
    public ResponseEntity<ResponseOfAuthenticate> refreshtoken(@RequestBody RequestOfJWT requestOfJWT,
        HttpServletResponse response) {
        try {
            String jwtToken = retrieveToken(requestOfJWT.getSingleUIAuthorization());
            boolean result = jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuer(jwtToken, JWT_ISSUER);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, Object> payload = objectMapper.readValue(userInfo, HashMap.class);
            String userName = (String) payload.get("sub");
            sessionService.validateSession((String) payload.get(SESSION_ID));
            Map<String, String> userInfoPayload = new HashMap<>();
            userInfoPayload.put("oud", (String) payload.get("oud"));
            userInfoPayload.put(SESSION_ID, (String) payload.get(SESSION_ID));
            final String refreshToken = jwtTokenUtil.generateReToken(userName, userInfoPayload);
            response.setHeader(HEADER_REFRESH_TOKEN, HEADER_JWT_TOKEN_VALUE_PREFIX.concat(refreshToken));
            Date newExpirationDate = jwtTokenUtil.getExpirationDate(refreshToken);
            return ResponseEntity.ok(ResponseOfAuthenticate.builder().result(result).expiration(newExpirationDate).build());
        } catch (Exception e) {
            log.info("token refreshtoken failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ResponseOfAuthenticate.builder().result(false).errorMessage("TOKEN_INVALID_EXPIRED - ".concat(e.getMessage())).build());
        }
    }

    @PostMapping(value = "v2/sso/relogin")
    public ResponseEntity<ResponseOfAuthenticate> relogin(@RequestBody RequestOfRelogin requestOfRelogin, HttpServletRequest request,
        HttpServletResponse response) {
        try {
            String jwtToken = retrieveToken(request.getHeader(HEADER_REFRESH_TOKEN));
            boolean result = jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuer(jwtToken, JWT_ISSUER_REFRESH);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.validateSession(payload.get(SESSION_ID));
            final String userName = payload.get("sub");
            final String oudString = payload.get("oud");
            final String sessionId = payload.get(SESSION_ID);
            Map<String, Object> returnObject = buildEntities(response, userName, oudString, sessionId);
            final List<Entity> entities = (List<Entity>) returnObject.get("entities");
            jwtToken = (String) returnObject.get("token");
            userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            final String entitlementsToken = (String) returnObject.get("entitlementsToken");
            final List<Map<String, Object>> drawers = (List<Map<String, Object>>) returnObject.get("drawers");
            return ResponseEntity
                .ok(ResponseOfAuthenticate.builder().entitlementsToken(entitlementsToken).oud(oudString).result(result).drawers(drawers)
                    .entities(entities)
                    .userInfo(userInfo).build());
        } catch (Exception e) {
            log.info("token relogin failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ResponseOfAuthenticate.builder().result(false).errorMessage("TOKEN_INVALID_EXPIRED - ".concat(e.getMessage())).build());
        }
    }

    @PostMapping(value = "v2/sso/logout")
    public ResponseEntity<ResponseOfAuthenticate> logout(@RequestBody RequestOfJWT requestOfJWT, HttpServletResponse response) {
        try {
            String jwtToken = retrieveToken(requestOfJWT.getSingleUIAuthorization());
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.create(payload.get(SESSION_ID));
        } catch (Exception e) {
            log.info("token logout failed, reason: {}", e.getMessage());
        }
        httpSession.invalidate();
        clearCookie(response);
        response.setHeader(HEADER_JWT_TOKEN, StringUtils.EMPTY);
        return ResponseEntity.ok(ResponseOfAuthenticate.builder().result(true).build());
    }

}