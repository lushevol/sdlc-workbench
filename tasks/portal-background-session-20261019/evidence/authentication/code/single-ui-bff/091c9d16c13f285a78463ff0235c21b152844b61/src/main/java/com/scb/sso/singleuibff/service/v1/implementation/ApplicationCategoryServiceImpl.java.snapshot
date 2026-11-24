package com.scb.sso.singleuibff.service.v1.implementation;

import com.scb.sso.singleuibff.config.FmaaProperties;
import com.scb.sso.singleuibff.entity.ApplicationCategory;
import com.scb.sso.singleuibff.exceptions.RecordNotCreatedException;
import com.scb.sso.singleuibff.exceptions.RecordNotFoundException;
import com.scb.sso.singleuibff.exceptions.RecordNotUpdatedException;
import com.scb.sso.singleuibff.repository.ApplicationCategoryRepo;
import com.scb.sso.singleuibff.service.v1.ApplicationCategoryService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.*;

@Slf4j
@AllArgsConstructor
public class ApplicationCategoryServiceImpl implements ApplicationCategoryService {

    private FmaaProperties fmaaProperties;
    private ApplicationCategoryRepo applicationCategoryRepo;

    @Override
    public Optional<List<ApplicationCategory>> findByEms2Role(String ems2Role) throws RecordNotFoundException {
        try {
            return this.applicationCategoryRepo.findByEms2Role(ems2Role);
        } catch (NoSuchElementException e) {
            throw RecordNotFoundException.builder().message("No record found.").build();
        }
    }

    @Override
    public Optional<List<ApplicationCategory>> findAll() throws RecordNotFoundException {
        try {
            return Optional.of(this.applicationCategoryRepo.findAll());
        } catch (NoSuchElementException e) {
            throw RecordNotFoundException.builder().message("No record found.").build();
        }
    }

    @Override
    public ApplicationCategory create(ApplicationCategory applicationCategory) throws RecordNotCreatedException {
        try {
            if (!fmaaProperties.isCreationEnabled()) {
                throw RecordNotCreatedException.builder().message("Adding new record is not permitted. Record not created.").build();
            } else if (this.applicationCategoryRepo.existsById(applicationCategory.getApplicationCategoryId())) {
                throw RecordNotCreatedException.builder().message("Duplicate Id.").build();
            } else {
                applicationCategory.setApplicationCategoryId(this.applicationCategoryRepo.getApplicationCategorySeq().get());
                applicationCategory.setOrderNo(applicationCategory.getApplicationCategoryId());
                return this.applicationCategoryRepo.save(applicationCategory);
            }
        } catch (RuntimeException e) {
            throw RecordNotCreatedException.builder().message("Record not created.").build();
        }
    }

    @Override
    public ApplicationCategory update(ApplicationCategory applicationCategory) throws RecordNotFoundException, RecordNotUpdatedException {
        try {
            if (!this.applicationCategoryRepo.existsById(applicationCategory.getApplicationCategoryId())) {
                throw RecordNotFoundException.builder().message("Id does not exists.").build();
            } else {
                return this.applicationCategoryRepo.save(applicationCategory);
            }
        } catch (RuntimeException e) {
            throw RecordNotUpdatedException.builder().message("Record not updated.").build();
        }
    }

    @Override
    public Optional<List<ApplicationCategory>> findByIsActive(boolean isActive) throws RecordNotFoundException {
        try {
            return this.applicationCategoryRepo.findByIsActive(isActive);
        } catch (NoSuchElementException e) {
            throw RecordNotFoundException.builder().message("No record found.").build();
        }
    }

    @Override
    public void saveAll(List<ApplicationCategory> applicationCategories) throws RecordNotCreatedException {
        try {
            this.applicationCategoryRepo.saveAll(applicationCategories);
        } catch (RuntimeException e) {
            throw RecordNotCreatedException.builder().message("Records not created.").build();
        }
    }

    @Override
    public Optional<ApplicationCategory> getById(Long id) throws RecordNotFoundException {
        try {
            return this.applicationCategoryRepo.findById(id);
        } catch (NoSuchElementException e) {
            throw RecordNotFoundException.builder().message("No record found.").build();
        }
    }

    @Override
    public Optional<ApplicationCategory> getByLabelAndIsActive(String label, boolean isActive) throws RecordNotFoundException {
        try {
            return this.applicationCategoryRepo.findByLabelAndIsActive(label, isActive);
        } catch (NoSuchElementException e) {
            throw RecordNotFoundException.builder().message("No record found.").build();
        }
    }

    @Override
    public Optional<List<Map<String, Object>>> getDrawers() throws RecordNotFoundException {
        try {
            return this.applicationCategoryRepo.getDrawers();
        } catch (NoSuchElementException e) {
            throw RecordNotFoundException.builder().message("No record found.").build();
        }
    }

    @Override
    public Optional<Long> setApplicationCategorySeq() {
        return this.applicationCategoryRepo.setApplicationCategorySeq();
    }

}
