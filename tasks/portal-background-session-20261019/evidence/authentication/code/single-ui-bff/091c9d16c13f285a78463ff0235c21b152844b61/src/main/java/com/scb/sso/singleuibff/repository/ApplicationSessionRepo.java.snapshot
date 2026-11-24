package com.scb.sso.singleuibff.repository;

import com.scb.sso.singleuibff.entity.ApplicationSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ApplicationSessionRepo extends JpaRepository<ApplicationSession, Long> {

    @Query(value = "SELECT c.*  FROM application_session c WHERE c.session_id = ?1", nativeQuery = true)
    Optional<ApplicationSession> findBySessionId(String sessionId);

}
