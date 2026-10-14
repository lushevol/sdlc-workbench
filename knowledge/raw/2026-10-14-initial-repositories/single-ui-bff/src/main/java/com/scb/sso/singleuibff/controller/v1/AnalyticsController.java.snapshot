package com.scb.sso.singleuibff.controller.v1;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.dto.elastic.Response;
import com.scb.sso.singleuibff.dto.request.RequestOfAnalytics;
import com.scb.sso.singleuibff.dto.request.RequestOfGetAnalytics;
import com.scb.sso.singleuibff.dto.response.ResponseOfAnalytics;
import com.scb.sso.singleuibff.exceptions.JwtException;
import com.scb.sso.singleuibff.service.v1.AnalyticService;
import com.scb.sso.singleuibff.service.v1.SessionService;
import com.scb.sso.singleuibff.util.JwtTokenUtil;
import com.scb.sso.singleuibff.util.OudUtil;
import jakarta.servlet.http.HttpServletRequest;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;

import static com.scb.sso.singleuibff.util.Constant.*;

@Slf4j
@RestController
public class AnalyticsController {

    @Autowired
    private OudUtil oudUtil;
    @Autowired
    private JwtTokenUtil jwtTokenUtil;
    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private AnalyticService analyticService;
    @Autowired
    private SessionService sessionService;

    @PostMapping(value = "v1/fmo/print")
    public ResponseEntity<ResponseOfAnalytics> analytics(@RequestBody RequestOfAnalytics requestOfAnalytics,
        HttpServletRequest httpServletRequest) {
        try {
            String jwtToken = retrieveToken(requestOfAnalytics.getSingleUIAuthorization());
            boolean result = jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuerAnalytics(jwtToken, JWT_ISSUER, JWT_ISSUER_REFRESH);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.validateSession(payload.get(SESSION_ID));
            String userName = payload.get("sub");
            analyticService.insertData(requestOfAnalytics, userName, oudUtil.getIp(httpServletRequest));
            return ResponseEntity.ok(ResponseOfAnalytics.builder()
                .result(result).build());
        } catch (Exception e) {
            log.info("token analytics failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ResponseOfAnalytics.builder().result(false).errorMessage("token validation failed").build());
        }
    }

    @PostMapping(value = "v1/fmo/analytics")
    public ResponseEntity<ResponseOfAnalytics> getAnalytics(@RequestBody RequestOfGetAnalytics requestOfGetAnalytics) {
        try {
            String jwtToken = retrieveToken(requestOfGetAnalytics.getSingleUIAuthorization());
            boolean result = jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuerAnalytics(jwtToken, JWT_ISSUER, JWT_ISSUER_ANALYTICS);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.validateSession(payload.get(SESSION_ID));
            HashMap<String, Object> filter = requestOfGetAnalytics.getFilter();
            filter.put("from", requestOfGetAnalytics.getFrom());
            filter.put("size", requestOfGetAnalytics.getSize());
            Response data = analyticService.filterData(objectMapper.writeValueAsString(filter));
            List<Object> dataList = new ArrayList<>();
            HashMap<String, Object> total = new HashMap<>();
            if (Objects.nonNull(data)) {
                dataList = data.getHits().getHits();
                total = data.getHits().getTotal();
            }
            return ResponseEntity.ok(ResponseOfAnalytics.builder()
                .result(result).data(dataList)
                .total(total).build());
        } catch (Exception e) {
            log.info("token analytics failed, reason: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ResponseOfAnalytics.builder().result(false).errorMessage("token validation failed::" + e.getMessage()).build());
        }
    }

    @SneakyThrows
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

}
