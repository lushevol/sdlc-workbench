package com.scb.sso.singleuibff.service.v2.implementation;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.Maps;
import com.scb.sso.singleuibff.config.EMS2ConfigProperties;
import com.scb.sso.singleuibff.dto.ems2.v2.*;
import com.scb.sso.singleuibff.service.v2.AuthorizationService;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.client.RestTemplate;

import java.util.*;
import java.util.stream.Collectors;

@Slf4j
@AllArgsConstructor
public class EMS2AuthorizationImplementation implements AuthorizationService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;
    private final EMS2ConfigProperties ems2ConfigProperties;

    @Override
    @SneakyThrows
    public Ems2Result getEntitlements(String userId, List<String> tileEntities) {
        Ems2RoleResult entitlementTypes = fetchDataEntitlementRoles(userId);
        List<Entity> entities = generateEntities(entitlementTypes.getEntitlementTypes());
        if (!CollectionUtils.isEmpty(entities)) {
            if (!CollectionUtils.isEmpty(tileEntities)) {
                entities = entities.stream().filter(entity -> tileEntities.contains(entity.getName())).collect(Collectors.toList());
            }
            List<String> ems2EntityList = entities.stream().map(Entity::getName).collect(Collectors.toList());
            List<Entitlement> userEntitlementList = getRawEntitlements(ems2EntityList, userId);
            entities.stream().forEach(entity -> {
                List<Entitlement> userEntitlementListFiltered = userEntitlementList.stream()
                    .filter(entitlement -> entitlement.getRole().getId().equals(entity.getRoleId()))
                    .map(entitlement -> {
                        entitlement.getAction().setEntitlementId(entitlement.getId());
                        return entitlement;
                    })
                    .collect(Collectors.toList());
                entity.setSubjects(
                    userEntitlementListFiltered
                        .stream()
                        .map(entitlement -> {
                            Subject subject = entitlement.getSubject();
                            List<Action> actions = userEntitlementListFiltered.stream()
                                .filter(entitlement1 -> entitlement1.getSubject().getId().equals(subject.getId()))
                                .map(entitlement1 -> entitlement1.getAction())
                                .collect(Collectors.toList());
                            subject.setActions(actions);
                            return subject;
                        })
                        .distinct()
                        .collect(Collectors.toList()));
            });
        }
        Ems2Result ems2Result = new Ems2Result();
        ems2Result.setEntities(entities);
        ems2Result.setAccountName(entitlementTypes.getAccountName());
        ems2Result.setFullName(entitlementTypes.getFullName());
        ems2Result.setAccountOwner(entitlementTypes.getAccountOwner());
        ems2Result.setAccountType(entitlementTypes.getAccountType());
        ems2Result.setAccountStatus(entitlementTypes.getAccountStatus());
        return ems2Result;
    }

    private Ems2RoleResult fetchDataEntitlementRoles(String userId) {
        try {
            ResponseEntity<String> responseEntity = restTemplate.getForEntity(
                String.format(ems2ConfigProperties.getUserRoles(), userId), String.class);
            return objectMapper.readValue(responseEntity.getBody(), Ems2RoleResult.class);
        } catch (Exception e) {
            log.error("fetchDataEntitlementRoles, e: {}", e);
        }
        return new Ems2RoleResult();
    }

    private List<Entity> generateEntities(List<Ems2RoleResult.EntitlementType> entitlementTypes) {
        if (!CollectionUtils.isEmpty(entitlementTypes)) {
            return entitlementTypes.stream()
                .filter(Objects::nonNull)
                .filter(element -> StringUtils.isNotBlank(element.getUniqueName()))
                .map(this::getEntity)
                .collect(Collectors.toList());
        }
        return Collections.emptyList();
    }

    private Entity getEntity(Ems2RoleResult.EntitlementType entitlementType) {
        String[] uniqueNames = StringUtils.split(entitlementType.getUniqueName(), "|", 6);
        Entity entity = new Entity();
        entity.setId(Long.parseLong(uniqueNames[0]));
        entity.setName(uniqueNames[1]);
        entity.setApplicationName(entitlementType.getApplicationName());
        entity.setRoleId(Long.parseLong(uniqueNames[2]));
        entity.setRoleName(uniqueNames[3]);
        return entity;
    }

    private List<Entitlement> getRawEntitlements(List<String> ems2EntityList, String userId) {
        try {
            ResponseEntity<String> response = getPermissionFromEms2OnEntityAndUserNew(ems2EntityList, userId);
            Map<String, EntitlementList> resultMap = objectMapper.readValue(response.getBody(),
                new TypeReference<Map<String, EntitlementList>>() {});
            EntitlementList resultList = resultMap.values().stream().findFirst().get();
            return resultList.getCount() > 0 ? resultList.getEntitlements() : Collections.emptyList();
        } catch (Exception e) {
            log.error("getRawEntitlements, e: {}", e);
        }
        return Collections.emptyList();
    }

    private ResponseEntity<String> getPermissionFromEms2OnEntityAndUserNew(List<String> entityList, String userId)
        throws JsonProcessingException {
        HashMap<String, List<String>> map = Maps.newHashMap();
        map.put(userId, entityList);
        String requestJson = objectMapper.writeValueAsString(map);
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> request = new HttpEntity<>(requestJson, headers);
        ResponseEntity<String> responseEntity = restTemplate.postForEntity(ems2ConfigProperties.getNewUserAuthorizationOnEntity(),
            request,
            String.class);
        return responseEntity;
    }

}
