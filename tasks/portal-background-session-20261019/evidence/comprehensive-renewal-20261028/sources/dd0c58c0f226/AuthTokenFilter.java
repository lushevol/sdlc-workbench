package com.scb.fmoportal.auth.filter;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.fmoportal.auth.properties.AuthProperties;
import com.scb.fmoportal.auth.util.JWTSessionData;
import com.scb.fmoportal.auth.util.JwtTokenUtil;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.util.AntPathMatcher;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.*;

@Slf4j
@AllArgsConstructor
public class AuthTokenFilter extends OncePerRequestFilter {

    private static final String HEADER_JWT_TOKEN = "Single-UI-Authorization";
    private static final String HEADER_JWT_TOKEN_VALUE_PREFIX = "Bearer ";
    private static final String USER_INFO_HEADER = "userInfo";
    private final List<JWTSessionData> sessionProperties;
    private final AuthProperties authProperties;
    private final ObjectMapper objectMapper;
    private final JwtTokenUtil jwtTokenUtil;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
        throws ServletException, IOException {
        if (needSkip(request)) {
            filterChain.doFilter(request, response);
            return;
        }
        if (urlNeedCheck(request.getRequestURI())) {
            check(request, response, filterChain);
            return;
        }
        filterChain.doFilter(request, response);
    }

    private boolean urlNeedCheck(String requestUrl) {
        if (checkIfUrlIsMatched(requestUrl, authProperties.getExcludeUrls())) {
            return false;
        }
        if (CollectionUtils.isEmpty(authProperties.getIncludeUrls())) {
            return true;
        }
        return checkIfUrlIsMatched(requestUrl, authProperties.getIncludeUrls());
    }

    private boolean needSkip(HttpServletRequest request) {
        if (CollectionUtils.isEmpty(authProperties.getSkipJwtHeaders())) {
            return false;
        }
        for (String configuredHeader : authProperties.getSkipJwtHeaders()) {
            if (StringUtils.hasLength(request.getHeader(configuredHeader))) {
                return true;
            }
        }
        return false;
    }

    private boolean checkIfUrlIsMatched(String requestUrl, List<String> inputUrls) {
        AntPathMatcher pathMatcher = new AntPathMatcher();
        if (CollectionUtils.isEmpty(inputUrls)) {
            return false;
        }
        Optional<Boolean> result = inputUrls.stream()
            .map(item -> pathMatcher.match(item, requestUrl))
            .filter(item -> item)
            .findFirst();
        return result.isPresent();
    }

    private void check(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
        throws ServletException, IOException {
        try {
            String url = request.getRequestURI();
            String jwtToken = retrieveHeaderToken(request.getHeader(HEADER_JWT_TOKEN));
            Optional<String> resultOptional = jwtTokenUtil.validateToken(jwtToken);
            JsonNode userInfo = objectMapper.readValue(resultOptional.get(), JsonNode.class);
            Map<String, String> userPayload = new HashMap<>();
            if (Objects.nonNull(userInfo)) {
                if (Objects.nonNull(userInfo.get("id"))) {
                    String sessionId = userInfo.get("id").asText();
                    userPayload.put("sessionId", sessionId);
                    jwtTokenUtil.validateSession(jwtToken, sessionId, url, sessionProperties);
                }
                if (Objects.nonNull(userInfo.get("entitlements"))) {
                    userPayload.put("entitlements", userInfo.get("entitlements").asText());
                }
                if (Objects.nonNull(userInfo.get("oud"))) {
                    userPayload.put("oud", userInfo.get("oud").asText());
                }
                if (Objects.nonNull(userInfo.get("sub"))) {
                    userPayload.put("userId", userInfo.get("sub").asText());
                }
            }
            userPayload.put("version", "3");
            request.setAttribute(USER_INFO_HEADER, objectMapper.writeValueAsString(userPayload));
            log.info("current url: {} fmoportal token is valid, will proceed", url);
        } catch (Exception e) {
            byte[] responseToSend = restResponseBytes(ResponseOfError.builder().message(e.getMessage()).build());
            response.setHeader("Content-Type", "application/json");
            response.setStatus(HttpStatus.UNAUTHORIZED.value());
            response.getOutputStream().write(responseToSend);
            return;
        }
        setHeader(response);
        filterChain.doFilter(request, response);
    }

    private byte[] restResponseBytes(ResponseOfError errorResponse) throws IOException {
        String serialized = new ObjectMapper().writeValueAsString(errorResponse);
        return serialized.getBytes();
    }

    private String retrieveHeaderToken(String inputHeaderValue) {
        if (!StringUtils.hasLength(inputHeaderValue)) {
            throw new RuntimeException("TOKEN_INVALID_EXPIRED", new Error("Invalid format"));
        }
        String[] headerValue = inputHeaderValue.split(HEADER_JWT_TOKEN_VALUE_PREFIX);
        if (headerValue.length == 2) {
            return headerValue[1];
        }
        throw new RuntimeException("TOKEN_INVALID_EXPIRED", new Error("Invalid format"));
    }

    private void setHeader(HttpServletResponse response) {
        response.setHeader("Server", " ");
        response.setHeader("X-Powered-By", " ");
        response.setHeader("Cache-Control", "private, no-cache, must-revalidate");
        response.setHeader("Expires", "-1");
        response.setHeader("X-XSS-Protection", "1; mode=block");
        response.setHeader("X-Content-Type-Options", "nosniff");
        response.setHeader("X-Frame-Options", "SAMEORIGIN");
        response.setHeader("Referrer-Policy", "same-origin");
        response.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
    }
}
