package com.scb.sso.singleuibff.controller.v1;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.dto.request.RequestOfApplicationTile;
import com.scb.sso.singleuibff.dto.response.ResponseOfAdminModule;
import com.scb.sso.singleuibff.entity.ApplicationCategory;
import com.scb.sso.singleuibff.entity.ApplicationTile;
import com.scb.sso.singleuibff.entity.ApplicationTileAudit;
import com.scb.sso.singleuibff.entity.ImportMap;
import com.scb.sso.singleuibff.exceptions.RecordNotCreatedException;
import com.scb.sso.singleuibff.exceptions.RecordNotFoundException;
import com.scb.sso.singleuibff.exceptions.RecordNotUpdatedException;
import com.scb.sso.singleuibff.service.v1.ApplicationCategoryService;
import com.scb.sso.singleuibff.service.v1.ApplicationTileAuditService;
import com.scb.sso.singleuibff.service.v1.ApplicationTileService;
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
public class ApplicationTileController {

    @Autowired
    private ObjectMapper objectMapper;
    @Autowired
    private ApplicationTileService applicationTileService;
    @Autowired
    private ApplicationTileAuditService applicationTileAuditService;
    @Autowired
    private ApplicationCategoryService applicationCategoryService;
    @Autowired
    private ImportMapService importMapService;
    @Autowired
    private AdminModuleUtil adminModuleUtil;

    @PostMapping(value = "v1/fmo/admin/tile/update")
    public ResponseEntity<?> update(@NotNull @RequestBody RequestOfApplicationTile requestOfApplicationTile,
        HttpServletRequest httpServletRequest) {
        try {
            ApplicationTile applicationTile = applicationTileService.getById(requestOfApplicationTile.getApplicationTileId()).get();
            ApplicationCategory applicationCategory = applicationCategoryService
                .getById(requestOfApplicationTile.getApplicationCategory().getApplicationCategoryId()).get();
            ImportMap importMap = importMapService.getById(requestOfApplicationTile.getImportMap().getImportMapId()).get();
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationTile.getEntitlementsToken());
            final String userName = payload.get("sub");
            String ems2Role = payload.get("ems2Role");
            if (adminModuleUtil.checkEms2Role(ems2Role, importMap, applicationCategory, applicationTile)) {
                throw RecordNotUpdatedException.builder().message("You do not have access to this record.").build();
            }
            if (adminModuleUtil.validateChecker(applicationTile, requestOfApplicationTile)) {
                if (applicationTile.getUpdatedBy().equalsIgnoreCase(userName)) {
                    throw RecordNotUpdatedException.builder().message("Maker and Checker should be different user.").build();
                }
                applicationTile.setActive(true);
            } else if (requestOfApplicationTile.getMode().equalsIgnoreCase("deactivate")) {
                applicationTile.setActive(false);
            } else {
                String title = adminModuleUtil.checkIfNull(requestOfApplicationTile.getTitle(), "");
                String subtitle = adminModuleUtil.checkIfNull(requestOfApplicationTile.getSubtitle(), "");
                String emailSupport = adminModuleUtil.checkIfNull(requestOfApplicationTile.getEmailSupport(), "");
                String ems2Subject = adminModuleUtil.checkIfNull(requestOfApplicationTile.getEms2Subject(), "");
                String ems2Entities = adminModuleUtil.checkIfNull(requestOfApplicationTile.getEms2Entities(), "");
                String tile = adminModuleUtil.checkIfNull(requestOfApplicationTile.getTile(), "");
                String module = adminModuleUtil.checkIfNull(requestOfApplicationTile.getModule(), "");
                String imageLightTheme = adminModuleUtil.checkIfNull(requestOfApplicationTile.getImageLightTheme(), "");
                String imageDarkTheme = adminModuleUtil.checkIfNull(requestOfApplicationTile.getImageDarkTheme(), "");
                if (adminModuleUtil.checkSpaces(module, tile)) {
                    throw RecordNotUpdatedException.builder()
                        .message("You should not enter any space character on the Module Path or Tile Path.").build();
                }
                if (adminModuleUtil.checkBlank(title, module, tile)) {
                    throw RecordNotCreatedException.builder()
                        .message("Please provide the value for the Title or Module Path or Tile Path.").build();
                }
                applicationTile.setActive(false);
                applicationTile.setTitle(title);
                applicationTile.setSubtitle(subtitle);
                applicationTile.setImageDarkTheme(imageDarkTheme);
                applicationTile.setImageLightTheme(imageLightTheme);
                applicationTile.setApplicationCategory(applicationCategory);
                applicationTile.setImportMap(importMap);
                applicationTile.setModule(module);
                applicationTile.setTile(tile);
                applicationTile.setEms2Entities(ems2Entities);
                applicationTile.setEms2Subject(ems2Subject);
                applicationTile.setEmailSupport(emailSupport);
                applicationTile.setTemplate(requestOfApplicationTile.isTemplate());
                applicationTile.setOrderNo(requestOfApplicationTile.getOrderNo());
            }
            applicationTile.setEms2Role(ems2Role.trim());
            applicationTile.setUpdatedBy(userName);
            applicationTile.setUpdatedAt(new Date());
            applicationTile = applicationTileService.update(applicationTile);
            audit(applicationTile, applicationCategory, importMap, requestOfApplicationTile.getMode().trim());
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(applicationTile).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        } catch (RecordNotUpdatedException | RecordNotCreatedException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/tile/create")
    public ResponseEntity<?> create(@NotNull @RequestBody RequestOfApplicationTile requestOfApplicationTile,
        HttpServletRequest httpServletRequest) {
        try {
            ApplicationCategory applicationCategory = applicationCategoryService
                .getById(requestOfApplicationTile.getApplicationCategory().getApplicationCategoryId()).get();
            ImportMap importMap = importMapService.getById(requestOfApplicationTile.getImportMap().getImportMapId()).get();
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationTile.getEntitlementsToken());
            final String userName = payload.get("sub");
            String ems2Role = payload.get("ems2Role");
            String title = adminModuleUtil.checkIfNull(requestOfApplicationTile.getTitle(), "");
            String subtitle = adminModuleUtil.checkIfNull(requestOfApplicationTile.getSubtitle(), "");
            String emailSupport = adminModuleUtil.checkIfNull(requestOfApplicationTile.getEmailSupport(), "");
            String ems2Subject = adminModuleUtil.checkIfNull(requestOfApplicationTile.getEms2Subject(), "");
            String ems2Entities = adminModuleUtil.checkIfNull(requestOfApplicationTile.getEms2Entities(), "");
            String tile = adminModuleUtil.checkIfNull(requestOfApplicationTile.getTile(), "");
            String module = adminModuleUtil.checkIfNull(requestOfApplicationTile.getModule(), "");
            String imageLightTheme = adminModuleUtil.checkIfNull(requestOfApplicationTile.getImageLightTheme(), "");
            String imageDarkTheme = adminModuleUtil.checkIfNull(requestOfApplicationTile.getImageDarkTheme(), "");
            if (module.contains(" ") || tile.contains(" ")) {
                throw RecordNotCreatedException.builder()
                    .message("You should not enter any space character on the Module Path or Tile Path.").build();
            }
            if (StringUtils.isBlank(title) || StringUtils.isBlank(module) || StringUtils.isBlank(tile)) {
                throw RecordNotCreatedException.builder().message("Please provide the value for the Title or Module Path or Tile Path.")
                    .build();
            }
            ApplicationTile applicationTile = applicationTileService.create(ApplicationTile.builder()
                .applicationCategory(applicationCategory)
                .ems2Role(ems2Role)
                .createdBy(userName)
                .updatedBy(userName)
                .updatedAt(new Date())
                .createdAt(new Date())
                .title(title)
                .subtitle(subtitle)
                .imageDarkTheme(imageDarkTheme)
                .imageLightTheme(imageLightTheme)
                .importMap(importMap)
                .module(module)
                .tile(tile)
                .ems2Entities(ems2Entities)
                .ems2Subject(ems2Subject)
                .emailSupport(emailSupport)
                .isTemplate(requestOfApplicationTile.isTemplate())
                .isActive(false)
                .build());
            audit(applicationTile, applicationCategory, importMap, "create");
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(applicationTile).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        } catch (RecordNotCreatedException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/tile/audit")
    public ResponseEntity<?> getAuditData(@NotNull @RequestBody RequestOfApplicationTile requestOfApplicationTile,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationTile.getEntitlementsToken());
            Optional<List<ApplicationTileAudit>> result = applicationTileAuditService
                .findByApplicationTileId(requestOfApplicationTile.getApplicationTileId());
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(result.get()).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    @PostMapping(value = "v1/fmo/admin/tile/data")
    public ResponseEntity<?> getData(@NotNull @RequestBody RequestOfApplicationTile requestOfApplicationTile,
        HttpServletRequest httpServletRequest) {
        try {
            Map<String, String> payload = adminModuleUtil.validate(httpServletRequest, requestOfApplicationTile.getEntitlementsToken());
            final String ems2Role = payload.get("ems2Role");
            Optional<List<ApplicationTile>> result;
            if (Objects.isNull(requestOfApplicationTile.getApplicationCategory())) {
                result = applicationTileService.findByEms2Role(ems2Role);
            } else {
                result = applicationTileService
                    .findByApplicationCategoryIdEms2Role(requestOfApplicationTile.getApplicationCategory().getApplicationCategoryId(),
                        ems2Role);
            }
            return ResponseEntity.ok().body(ResponseOfAdminModule.builder().result(true).data(result.get()).build());
        } catch (RecordNotFoundException | NoSuchElementException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ResponseOfAdminModule.builder().result(false).errorMessage(e.getMessage()).build());
        }
    }

    private void audit(@NotNull ApplicationTile applicationTile, ApplicationCategory applicationCategory, ImportMap importMap, String mode)
        throws RecordNotCreatedException {
        String title = adminModuleUtil.checkIfNull(applicationTile.getTitle(), "");
        String subtitle = adminModuleUtil.checkIfNull(applicationTile.getSubtitle(), "");
        String emailSupport = adminModuleUtil.checkIfNull(applicationTile.getEmailSupport(), "");
        String ems2Subject = adminModuleUtil.checkIfNull(applicationTile.getEms2Subject(), "");
        String ems2Entities = adminModuleUtil.checkIfNull(applicationTile.getEms2Entities(), "");
        String tile = adminModuleUtil.checkIfNull(applicationTile.getTile(), "");
        String module = adminModuleUtil.checkIfNull(applicationTile.getModule(), "");
        String imageLightTheme = adminModuleUtil.checkIfNull(applicationTile.getImageLightTheme(), "");
        String imageDarkTheme = adminModuleUtil.checkIfNull(applicationTile.getImageDarkTheme(), "");
        applicationTileAuditService.create(ApplicationTileAudit.builder()
            .importMap(importMap)
            .applicationCategory(applicationCategory)
            .applicationTileId(applicationTile.getApplicationTileId())
            .ems2Role(applicationTile.getEms2Role().trim())
            .createdBy(applicationTile.getCreatedBy().trim())
            .updatedBy(applicationTile.getUpdatedBy().trim())
            .updatedAt(applicationTile.getUpdatedAt())
            .createdAt(applicationTile.getCreatedAt())
            .title(title)
            .subtitle(subtitle)
            .imageDarkTheme(imageLightTheme)
            .imageLightTheme(imageDarkTheme)
            .module(module)
            .tile(tile)
            .ems2Entities(ems2Entities)
            .ems2Subject(ems2Subject)
            .emailSupport(emailSupport)
            .isTemplate(applicationTile.isTemplate())
            .isActive(applicationTile.isActive())
            .transactionMode(mode)
            .orderNo(applicationTile.getOrderNo())
            .build());
    }

}
