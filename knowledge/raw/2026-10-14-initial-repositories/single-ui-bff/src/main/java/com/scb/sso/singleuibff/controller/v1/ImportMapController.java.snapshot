package com.scb.sso.singleuibff.controller.v1;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.dto.request.RequestOfImportMap;
import com.scb.sso.singleuibff.dto.response.ResponseOfAdminModule;
import com.scb.sso.singleuibff.entity.ImportMap;
import com.scb.sso.singleuibff.entity.ImportMapAudit;
import com.scb.sso.singleuibff.exceptions.RecordNotCreatedException;
import com.scb.sso.singleuibff.exceptions.RecordNotFoundException;
import com.scb.sso.singleuibff.exceptions.RecordNotUpdatedException;
import com.scb.sso.singleuibff.service.v1.ImportMapAuditService;
import com.scb.sso.singleuibff.service.v1.ImportMapService;
import com.scb.sso.singleuibff.util.AdminModuleUtil;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.jetbrains.annotations.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Slf4j
@RestController
public class ImportMapController {

    @Autowired
    private ObjectMapper objectMapper;
    @Autowired
    private AdminModuleUtil adminModuleUtil;
    @Autowired
    private ImportMapService importMapService;
    @Autowired
    private ImportMapAuditService importMapAuditService;

    @GetMapping(value = "v1/fmo/admin/importmap/active")
    public ResponseEntity<?> getAllActive() {
        try {
            List<ImportMap> result = importMapService.findByIsActive(true).get();
            HashMap<String, String> objects = new HashMap<>();
            result.stream().forEach(item -> {
                if (item.getKeyName().equalsIgnoreCase("single-spa") || item.getKeyName().equalsIgnoreCase("react")
                    || item.getKeyName().equalsIgnoreCase("react-dom")) {
                    objects.put(item.getKeyName(), item.getPath());
                } else {
                    objects.put("@fm/".concat(item.getKeyName()), item.getPath());
                }
            });
            HashMap<String, Object> data = new HashMap<>();
            data.put("imports", objects);
            return ResponseEntity.ok().body(data);
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/importmap/update")
    public ResponseEntity<?> update(@NotNull @RequestBody RequestOfImportMap requestOfImportMap,
        HttpServletRequest httpServletRequest) {
        try {
            ImportMap importMap = importMapService.getById(requestOfImportMap.getImportMapId()).get();
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfImportMap.getEntitlementsToken());
            final String userName = payload.get("sub");
            String ems2Role = payload.get("ems2Role");
            if (!importMap.getEms2Role().equalsIgnoreCase(ems2Role)) {
                throw RecordNotUpdatedException.builder().message("You do not have access to this record.").build();
            }
            if (!importMap.isActive() && requestOfImportMap.getMode().trim().equalsIgnoreCase("checker")) {
                if (importMap.getUpdatedBy().equalsIgnoreCase(userName)) {
                    throw RecordNotUpdatedException.builder().message("Maker and Checker should be different user.").build();
                }
                importMap.setActive(true);
            } else if (requestOfImportMap.getMode().trim().equalsIgnoreCase("deactivate")) {
                importMap.setActive(false);
            } else {
                String path = adminModuleUtil.checkIfNull(requestOfImportMap.getPath(), "");
                String keyName = adminModuleUtil.checkIfNull(requestOfImportMap.getKeyName(), "");
                if (path.contains(" ") || keyName.contains(" ")) {
                    throw RecordNotUpdatedException.builder()
                        .message("You should not enter any space character on the Module Name or Path.").build();
                }
                if (StringUtils.isBlank(path) || StringUtils.isBlank(keyName)) {
                    throw RecordNotUpdatedException.builder().message("Please provide the value for the Module Name or Path").build();
                }
                importMap.setActive(false);
                importMap.setPath(path);
                importMap.setKeyName(keyName);
            }
            importMap.setEms2Role(ems2Role);
            importMap.setUpdatedBy(userName);
            importMap.setUpdatedAt(new Date());
            importMap = importMapService.update(importMap);
            audit(importMap, requestOfImportMap.getMode().trim());
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(importMap).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        } catch (RecordNotUpdatedException | RecordNotCreatedException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/importmap/create")
    public ResponseEntity<?> create(@NotNull @RequestBody RequestOfImportMap requestOfImportMap,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfImportMap.getEntitlementsToken());
            final String userName = payload.get("sub");
            String ems2Role = payload.get("ems2Role");
            String path = adminModuleUtil.checkIfNull(requestOfImportMap.getPath(), "");
            String keyName = adminModuleUtil.checkIfNull(requestOfImportMap.getKeyName(), "");
            if (path.contains(" ") || keyName.contains(" ")) {
                throw RecordNotCreatedException.builder().message("You should not enter any space character on the Module Name or Path.")
                    .build();
            }
            if (StringUtils.isBlank(path) || StringUtils.isBlank(keyName)) {
                throw RecordNotCreatedException.builder().message("Please provide the value for the Module Name or Path.").build();
            }
            ImportMap importMap = importMapService.create(ImportMap.builder()
                .ems2Role(ems2Role)
                .path(path)
                .keyName(keyName)
                .createdBy(userName)
                .updatedBy(userName)
                .updatedAt(new Date())
                .createdAt(new Date())
                .isActive(false)
                .build());
            audit(importMap, "create");
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(importMap).build());
        } catch (RecordNotCreatedException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/importmap/audit")
    public ResponseEntity<?> getAuditData(@NotNull @RequestBody RequestOfImportMap requestOfImportMap,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfImportMap.getEntitlementsToken());
            Optional<List<ImportMapAudit>> result = importMapAuditService.findByImportMapId(requestOfImportMap.getImportMapId());
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(result.get()).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/importmap/data")
    public ResponseEntity<?> getData(@NotNull @RequestBody RequestOfImportMap requestOfImportMap,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfImportMap.getEntitlementsToken());
            final String ems2Role = payload.get("ems2Role");
            Optional<List<ImportMap>> result = importMapService.findByEms2Role(ems2Role);
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(result.get()).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    private void audit(@NotNull ImportMap importMap, String mode) throws RecordNotCreatedException {
        String path = adminModuleUtil.checkIfNull(importMap.getPath(), "");
        String keyName = adminModuleUtil.checkIfNull(importMap.getKeyName(), "");
        importMapAuditService.create(ImportMapAudit.builder()
            .importMapId(importMap.getImportMapId())
            .ems2Role(importMap.getEms2Role())
            .path(path)
            .keyName(keyName)
            .createdBy(importMap.getCreatedBy())
            .updatedBy(importMap.getUpdatedBy())
            .updatedAt(importMap.getUpdatedAt())
            .createdAt(importMap.getCreatedAt())
            .isActive(importMap.isActive())
            .transactionMode(mode)
            .build());
    }

}
