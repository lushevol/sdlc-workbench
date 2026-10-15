package com.scb.sso.singleuibff.service.v1.implementation;

import com.scb.sso.singleuibff.entity.ApplicationSession;
import com.scb.sso.singleuibff.exceptions.JwtException;
import com.scb.sso.singleuibff.repository.ApplicationSessionRepo;
import com.scb.sso.singleuibff.service.v1.SessionService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.*;

@Slf4j
@AllArgsConstructor
public class SessionServiceImplementation implements SessionService {

    private ApplicationSessionRepo applicationSessionRepo;

    @Override
    public void create(String sessionId) {
        try {
            this.applicationSessionRepo.save(ApplicationSession.builder().sessionId(sessionId).build());
        } catch (NoSuchElementException e) {
            log.info("SessionServiceImplementation create: {}", e.getMessage());
        }
    }

    @Override
    public void validateSession(String sessionId) {
        Optional<ApplicationSession> applicationSessionOptional = this.applicationSessionRepo.findBySessionId(sessionId);
        if (!applicationSessionOptional.isEmpty()) {
            throw JwtException.builder().message("invalid token").build();
        }
    }

}
