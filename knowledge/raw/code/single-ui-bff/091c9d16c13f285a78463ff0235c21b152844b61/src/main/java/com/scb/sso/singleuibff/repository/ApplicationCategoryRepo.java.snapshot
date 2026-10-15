package com.scb.sso.singleuibff.repository;

import com.scb.sso.singleuibff.entity.ApplicationCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public interface ApplicationCategoryRepo extends JpaRepository<ApplicationCategory, Long> {

    @Query(value = "SELECT c.*  FROM application_category c WHERE c.ems2_role = ?1 order by c.updated_at desc", nativeQuery = true)
    Optional<List<ApplicationCategory>> findByEms2Role(String ems2Role);

    @Query(value = "SELECT c.*  FROM application_category c WHERE c.is_active = ?1 or c.ems2_role='SUPER_USER'", nativeQuery = true)
    Optional<List<ApplicationCategory>> findByIsActive(boolean isActive);

    @Query(value = "SELECT c.*  FROM application_category c WHERE c.label = ?1 and c.is_active = ?2", nativeQuery = true)
    Optional<ApplicationCategory> findByLabelAndIsActive(String label, boolean isActive);

    @Query(value = "SELECT c.application_category_id, c.label, m.key_name, t.*  FROM application_category c, application_tile t, import_map m WHERE c.application_category_id=t.application_category_id and t.import_map_id=m.import_map_id and c.is_active = true and t.is_active = true and m.is_active = true order by c.order_no, t.order_no", nativeQuery = true)
    Optional<List<Map<String, Object>>> getDrawers();

    @Query(value = "SELECT setval('post_trade_portal_service.application_category_seq', (select max(application_category_id)+1 from post_trade_portal_service.application_category), true)", nativeQuery = true)
    Optional<Long> setApplicationCategorySeq();

    @Query(value = "SELECT nextval('post_trade_portal_service.application_category_seq')", nativeQuery = true)
    Optional<Long> getApplicationCategorySeq();

}
