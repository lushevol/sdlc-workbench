package com.scb.sso.singleuibff.controller.v1;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.dto.request.RequestOfApplicationCategory;
import com.scb.sso.singleuibff.dto.response.ResponseOfAdminModule;
import com.scb.sso.singleuibff.entity.ApplicationCategory;
import com.scb.sso.singleuibff.entity.ApplicationCategoryAudit;
import com.scb.sso.singleuibff.exceptions.RecordNotCreatedException;
import com.scb.sso.singleuibff.exceptions.RecordNotFoundException;
import com.scb.sso.singleuibff.exceptions.RecordNotUpdatedException;
import com.scb.sso.singleuibff.service.v1.ApplicationCategoryAuditService;
import com.scb.sso.singleuibff.service.v1.ApplicationCategoryService;
import com.scb.sso.singleuibff.service.v1.ApplicationTileService;
import com.scb.sso.singleuibff.util.AdminModuleUtil;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Slf4j
@RestController
public class ApplicationCategoryController {

    @Autowired
    private ObjectMapper objectMapper;
    @Autowired
    private AdminModuleUtil adminModuleUtil;
    @Autowired
    private ApplicationCategoryService applicationCategoryService;
    @Autowired
    private ApplicationTileService applicationTileService;
    @Autowired
    private ApplicationCategoryAuditService applicationCategoryAuditService;

    @PostMapping(value = "v1/fmo/admin/category/update")
    public ResponseEntity<?> update(@NotNull @RequestBody RequestOfApplicationCategory requestOfApplicationCategory,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationCategory.getEntitlementsToken());
            ApplicationCategory applicationCategory = applicationCategoryService
                .getById(requestOfApplicationCategory.getApplicationCategoryId()).get();
            final String userName = payload.get("sub");
            String ems2Role = payload.get("ems2Role");
            if (!applicationCategory.getEms2Role().equalsIgnoreCase(ems2Role)) {
                throw RecordNotUpdatedException.builder().message("You do not have access to this record.").build();
            }
            if (!applicationCategory.isActive() && requestOfApplicationCategory.getMode().equalsIgnoreCase("checker")) {
                if (applicationCategory.getUpdatedBy().equalsIgnoreCase(userName)) {
                    throw RecordNotUpdatedException.builder().message("Maker and Checker should be different user.").build();
                }
                applicationCategory.setActive(true);
            } else if (requestOfApplicationCategory.getMode().equalsIgnoreCase("deactivate")) {
                applicationCategory.setActive(false);
            } else {
                String label = adminModuleUtil.checkIfNull(requestOfApplicationCategory.getLabel(), "");
                applicationCategory.setActive(false);
                applicationCategory.setLabel(label);
                applicationCategory.setOrderNo(requestOfApplicationCategory.getOrderNo());
            }
            applicationCategory.setEms2Role(ems2Role.trim());
            applicationCategory.setUpdatedAt(new Date());
            applicationCategory.setUpdatedBy(userName);
            applicationCategory = applicationCategoryService.update(applicationCategory);
            audit(applicationCategory, requestOfApplicationCategory.getMode().trim());
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(applicationCategory).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        } catch (RecordNotUpdatedException | RecordNotCreatedException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/category/create")
    public ResponseEntity<?> create(@NotNull @RequestBody RequestOfApplicationCategory requestOfApplicationCategory,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationCategory.getEntitlementsToken());
            final String userName = payload.get("sub");
            String ems2Role = payload.get("ems2Role");
            String label = adminModuleUtil.checkIfNull(requestOfApplicationCategory.getLabel(), "");
            ApplicationCategory applicationCategory = applicationCategoryService.create(ApplicationCategory.builder()
                .ems2Role(ems2Role.trim())
                .createdBy(userName.trim())
                .updatedBy(userName.trim())
                .updatedAt(new Date())
                .createdAt(new Date())
                .label(label)
                .isActive(false)
                .build());
            audit(applicationCategory, "create");
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(applicationCategory).build());
        } catch (RecordNotCreatedException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/category/audit")
    public ResponseEntity<?> getAuditData(@NotNull @RequestBody RequestOfApplicationCategory requestOfApplicationCategory,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationCategory.getEntitlementsToken());
            Optional<List<ApplicationCategoryAudit>> result = applicationCategoryAuditService
                .findByApplicationCategoryId(requestOfApplicationCategory.getApplicationCategoryId());
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(result.get()).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/category/data")
    public ResponseEntity<?> getData(@NotNull @RequestBody RequestOfApplicationCategory requestOfApplicationCategory,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationCategory.getEntitlementsToken());
            final String ems2Role = payload.get("ems2Role");
            Optional<List<ApplicationCategory>> result = applicationCategoryService.findByEms2Role(ems2Role);
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(result.get()).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    private void audit(@NotNull ApplicationCategory applicationCategory, String mode) throws RecordNotCreatedException {
        String label = adminModuleUtil.checkIfNull(applicationCategory.getLabel(), "");
        applicationCategoryAuditService.create(ApplicationCategoryAudit.builder()
            .applicationCategoryId(applicationCategory.getApplicationCategoryId())
            .ems2Role(applicationCategory.getEms2Role().trim())
            .createdBy(applicationCategory.getCreatedBy().trim())
            .updatedBy(applicationCategory.getUpdatedBy().trim())
            .updatedAt(applicationCategory.getUpdatedAt())
            .createdAt(applicationCategory.getCreatedAt())
            .label(label)
            .isActive(applicationCategory.isActive())
            .transactionMode(mode)
            .orderNo(applicationCategory.getOrderNo())
            .build());
    }

}
