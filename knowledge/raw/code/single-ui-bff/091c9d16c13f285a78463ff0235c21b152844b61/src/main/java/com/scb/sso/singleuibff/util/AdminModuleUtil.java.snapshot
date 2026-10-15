package com.scb.sso.singleuibff.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.config.EMS2ConfigProperties;
import com.scb.sso.singleuibff.dto.ems2.v2.Entity;
import com.scb.sso.singleuibff.dto.ems2.v2.Subject;
import com.scb.sso.singleuibff.dto.request.RequestOfApplicationTile;
import com.scb.sso.singleuibff.entity.ApplicationCategory;
import com.scb.sso.singleuibff.entity.ApplicationTile;
import com.scb.sso.singleuibff.entity.ImportMap;
import com.scb.sso.singleuibff.exceptions.JwtException;
import com.scb.sso.singleuibff.service.v1.SessionService;
import jakarta.servlet.http.HttpServletRequest;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.*;
import java.util.stream.Collectors;

import static com.scb.sso.singleuibff.util.Constant.*;

@Slf4j
@AllArgsConstructor
public class AdminModuleUtil {

    @Autowired
    private JwtTokenUtil jwtTokenUtil;
    @Autowired
    private ObjectMapper objectMapper;
    @Autowired
    private SessionService sessionService;

    @Autowired
    private EMS2ConfigProperties ems2ConfigProperties;

    public Map<String, String> validate(HttpServletRequest httpServletRequest, String entitlementsToken) {
        try {
            String jwtToken = jwtTokenUtil.retrieveHeaderToken(httpServletRequest.getHeader(HEADER_JWT_TOKEN));
            jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuer(jwtToken, JWT_ISSUER);

            jwtTokenUtil.validateToken(entitlementsToken);
            jwtTokenUtil.handleIssuer(entitlementsToken, JWT_ISSUER_ENTITLEMENT);
            String content = jwtTokenUtil.retrieveUserInfoFromToken(entitlementsToken);
            Map<String, String> entitlementsPayload = objectMapper.readValue(content, HashMap.class);
            Map<String, String> entitlements = objectMapper.readValue(entitlementsPayload.get("entitlements"), HashMap.class);
            String ems2Role = entitlements.keySet().stream()
                .filter(i -> i.startsWith(ems2ConfigProperties.getAdminModuleEntity()))
                .map(i -> {
                    String[] s = i.split(":");
                    return s[1];
                }).toList().get(0);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            payload.put("ems2Role", ems2Role);
            sessionService.validateSession(payload.get(SESSION_ID));
            return payload;
        } catch (Exception e) {
            throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - token validation failed.").build();
        }
    }

    public Map<String, String> validate(HttpServletRequest httpServletRequest) {
        try {
            String jwtToken = jwtTokenUtil.retrieveHeaderToken(httpServletRequest.getHeader(HEADER_JWT_TOKEN));
            jwtTokenUtil.validateToken(jwtToken);
            jwtTokenUtil.handleIssuer(jwtToken, JWT_ISSUER);
            String userInfo = jwtTokenUtil.retrieveUserInfoFromToken(jwtToken);
            Map<String, String> payload = objectMapper.readValue(userInfo, HashMap.class);
            sessionService.validateSession(payload.get(SESSION_ID));
            return payload;
        } catch (Exception e) {
            throw JwtException.builder().message("TOKEN_INVALID_EXPIRED - token validation failed.").build();
        }
    }

    private List<String> cleanEntity(Map<String, Object> item) {
        String ems2_entities = (String) item.get("ems2_entities");
        List<String> returnData = new ArrayList<>();
        if (!Objects.isNull(ems2_entities) && StringUtils.isNotBlank(ems2_entities)) {
            returnData.addAll(Arrays.asList(ems2_entities.split(",")));
        }
        return returnData.stream().map(String::trim).filter(s -> StringUtils.isNotBlank(s))
            .distinct().collect(Collectors.toList());
    }

    public List<String> getEntityFromApplicationCategory(List<Map<String, Object>> applicationCategories) {
        List<String> resultEntity = new ArrayList<>();
        for (Map<String, Object> item : applicationCategories) {
            resultEntity.addAll(cleanEntity(item));
        }
        return resultEntity.stream().distinct().collect(Collectors.toList());
    }

    public List<Map<String, Object>> filterDrawers(List<Map<String, Object>> drawers, List<Entity> entities) {
        return drawers.stream().map(d -> {
            List<Map<String, Object>> newTiles = new ArrayList<>();
            List<Map<String, Object>> tiles = (List<Map<String, Object>>) d.get("tiles");
            for (Map<String, Object> tile : tiles) {
                boolean isTemplate = (boolean) tile.get("isTemplate");
                if (isTemplate) {
                    newTiles.add(tile);
                } else {
                    String[] entitiesDrawer = (String[]) tile.get("entity");
                    String subject = (String) tile.get("subject");
                    for (Entity entity1 : entities) {
                        if (Arrays.asList(entitiesDrawer).contains(entity1.getName())) {
                            // skip subject checking if leave empty
                            if (StringUtils.isBlank(subject)) {
                                newTiles.add(tile);
                            } else {
                                List<Subject> subjects = entity1.getSubjects().stream()
                                    .filter(s -> s.getLongName().equalsIgnoreCase(subject) || s.getName().equalsIgnoreCase(subject))
                                    .collect(Collectors.toList());
                                if (subjects.size() > 0) {
                                    newTiles.add(tile);
                                }
                            }
                        }
                    }
                }
            }
            newTiles = newTiles.stream().distinct().collect(Collectors.toList());
            d.put("tiles", newTiles);
            return d;
        })
            .filter(d -> {
                List<Map<String, Object>> tiles = (List<Map<String, Object>>) d.get("tiles");
                return tiles.size() > 0;
            })
            .collect(Collectors.toList());
    }

    public List<Map<String, Object>> getDrawer(List<Map<String, Object>> applicationCategories, List<Entity> entities) {
        List<Map<String, Object>> drawers = new ArrayList<>();
        for (Map<String, Object> item : applicationCategories) {
            Map<String, Object> tile = new HashMap<>();
            tile.put("id", item.get("application_tile_id"));
            tile.put("container", "@fm/".concat((String) item.get("key_name")));
            tile.put("entity", cleanEntity(item).toArray(String[]::new));
            tile.put("subject", item.get("ems2_subject"));
            tile.put("isTemplate", item.get("is_template"));
            tile.put("module", "/".concat((String) item.get("module")));
            tile.put("tile", "/".concat((String) item.get("tile")));
            tile.put("title", item.get("title"));
            tile.put("subtitle", item.get("subtitle"));
            tile.put("imageDarkTheme", item.get("image_dark_theme"));
            tile.put("imageLightTheme", item.get("image_light_theme"));
            tile.put("emailSupport", item.get("email_support"));
            Map<String, Object> resultCheck = drawers.stream()
                .filter(t -> t.get("id").equals(item.get("application_category_id")))
                .findFirst()
                .orElse(null);
            if (Objects.isNull(resultCheck)) {
                List<Map<String, Object>> tiles = new ArrayList<>();
                tiles.add(tile);
                Map<String, Object> record = new HashMap<>();
                record.put("id", item.get("application_category_id"));
                record.put("label", item.get("label"));
                record.put("tiles", tiles);
                drawers.add(record);
            } else {
                List<Map<String, Object>> tiles = (List<Map<String, Object>>) resultCheck.get("tiles");
                tiles.add(tile);
            }
        }
        return filterDrawers(drawers, entities);
    }

    public String checkIfNull(String input, String defaultValue) {
        return Objects.isNull(input) ? defaultValue : input.trim();
    }

    public boolean checkEms2Role(String ems2Role, ImportMap importMap, ApplicationCategory applicationCategory,
        ApplicationTile applicationTile) {
        return (!applicationTile.getEms2Role().equalsIgnoreCase(ems2Role) || !applicationCategory.getEms2Role().equalsIgnoreCase(ems2Role)
            || !importMap.getEms2Role().equalsIgnoreCase(ems2Role));
    }

    public boolean validateChecker(ApplicationTile applicationTile, RequestOfApplicationTile requestOfApplicationTile) {
        return (!applicationTile.isActive() && requestOfApplicationTile.getMode().equalsIgnoreCase("checker"));
    }

    public boolean checkSpaces(String module, String tile) {
        return (module.contains(" ") || tile.contains(" "));
    }

    public boolean checkBlank(String title, String module, String tile) {
        return (StringUtils.isBlank(title) || StringUtils.isBlank(module) || StringUtils.isBlank(tile));
    }

}
