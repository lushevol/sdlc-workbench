package com.scb.sso.singleuibff.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;

import static com.scb.sso.singleuibff.util.Constant.ADMIN_MODULE_SCHEMA;

@Entity
@Data
@Builder
@AllArgsConstructor(access = AccessLevel.PACKAGE)
@NoArgsConstructor(access = AccessLevel.PACKAGE)
@Table(schema = ADMIN_MODULE_SCHEMA)
public class ApplicationSession {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "application_session_seq")
    @SequenceGenerator(name = "application_session_seq", schema = ADMIN_MODULE_SCHEMA, sequenceName = "application_session_seq", allocationSize = 1)
    private long applicationSessionId;

    @Column(nullable = false)
    @Builder.Default
    private String sessionId = "";
    @Column(nullable = false)
    @Builder.Default
    private Date createdAt = new Date();

}
