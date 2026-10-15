package com.scb.sso.singleuibff.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.filter.RequestFilter;
import com.scb.sso.singleuibff.filter.RestExceptionHandler;
import com.scb.sso.singleuibff.repository.*;
import com.scb.sso.singleuibff.service.v1.*;
import com.scb.sso.singleuibff.service.v1.implementation.*;
import com.scb.sso.singleuibff.service.v2.AuthorizationService;
import com.scb.sso.singleuibff.service.v2.implementation.EMS2AuthorizationImplementation;
import com.scb.sso.singleuibff.util.*;

import org.apache.commons.lang3.StringUtils;
import org.jasypt.util.text.BasicTextEncryptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.ImportAutoConfiguration;
import org.springframework.boot.autoconfigure.web.client.RestTemplateAutoConfiguration;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.web.client.RestTemplate;

import java.net.InetSocketAddress;
import java.net.Proxy;

@Configuration
@ImportAutoConfiguration(RestTemplateAutoConfiguration.class)
public class AuthConfig {

    @Autowired
    private LdapTemplate ldapTemplate;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private EMS2ConfigProperties ems2ConfigProperties;

    @Autowired
    private JWTConfigProperties jwtConfigProperties;

    @Autowired
    private MFAConfigProperties mfaConfigProperties;

    @Autowired
    private EntraConfigProperties entraConfigProperties;

    @Autowired
    private WhitelistedProperties whitelistedProperties;

    @Autowired
    private OUDProperties oudProperties;

    @Autowired
    private ElasticProperties elasticProperties;

    @Autowired
    private FmaaProperties fmaaProperties;

    @Autowired
    private ApplicationCategoryRepo applicationCategoryRepo;

    @Autowired
    private ApplicationTileRepo applicationTileRepo;

    @Autowired
    private ImportMapRepo importMapRepo;

    @Autowired
    private ImportMapAuditRepo importMapAuditRepo;

    @Autowired
    private ApplicationCategoryAuditRepo applicationCategoryAuditRepo;

    @Autowired
    private ApplicationTileAuditRepo applicationTileAuditRepo;

    @Autowired
    private ApplicationSessionRepo applicationSessionRepo;

    @Bean
    public OudUtil buildOudUtil() {
        return new OudUtil(whitelistedProperties, new BasicTextEncryptor());
    }

    @Bean
    public OUDAuthenticationService buildOUDAuthenticationService() {
        return new OUDAuthenticationService(ldapTemplate, whitelistedProperties, oudProperties, buildOudUtil());
    }

    @Bean
    public MFAAuthenticationService buildMFAAuthenticationService(RestTemplateBuilder builder) {
        RestTemplate restTemplate = builder
                .setConnectTimeout(mfaConfigProperties.getConnectTimeoutDuration())
                .setReadTimeout(mfaConfigProperties.getReadTimeoutDuration())
                .build();
        return new MFAAuthenticationService(restTemplate, objectMapper, mfaConfigProperties);
    }

    @Bean
    public EntraAuthenticationService buildEntraAuthenticationService(RestTemplateBuilder builder) {
        RestTemplate restTemplate = builder
                .setConnectTimeout(entraConfigProperties.getConnectTimeoutDuration())
                .setReadTimeout(entraConfigProperties.getReadTimeoutDuration())
                .requestFactory(() -> {
                    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
                    if (StringUtils.isNotBlank(entraConfigProperties.getProxyHost()) && entraConfigProperties.getProxyPort() > 0) {
                        Proxy proxy = new Proxy(Proxy.Type.HTTP,
                                new InetSocketAddress(entraConfigProperties.getProxyHost(),
                                        entraConfigProperties.getProxyPort()));
                        factory.setProxy(proxy);
                    }
                    return factory;
                })
                .build();
        return new EntraAuthenticationServiceImpl(restTemplate, objectMapper, entraConfigProperties,
                buildClientAssertionGenUtil());
    }

    @Bean
    public ClientAssertionGenUtil buildClientAssertionGenUtil() {
        return new ClientAssertionGenUtil(entraConfigProperties);
    }

    @Bean
    public AuthorizationService buildAuthorizationService(RestTemplateBuilder builder) {
        RestTemplate restTemplate = builder
                .setConnectTimeout(ems2ConfigProperties.getConnectTimeout())
                .setReadTimeout(ems2ConfigProperties.getReadTimeout())
                .build();
        return new EMS2AuthorizationImplementation(restTemplate, objectMapper, ems2ConfigProperties);
    }

    @Bean
    public JwtTokenUtil buildJwtTokenUtil() {
        return new JwtTokenUtil(jwtConfigProperties);
    }

    @Bean
    public Elasticsearch buildElasticsearch(RestTemplateBuilder builder) {
        RestTemplate restTemplate = builder
                .setConnectTimeout(elasticProperties.getConnectTimeout())
                .setReadTimeout(elasticProperties.getReadTimeout())
                .build();
        return new Elasticsearch(restTemplate, objectMapper, elasticProperties);
    }

    @Bean
    public SessionService buildSessionService() {
        return new SessionServiceImplementation(applicationSessionRepo);
    }

    @Bean
    public RequestFilter buildRequestFilter() {
        return new RequestFilter();
    }

    @Bean
    public RestExceptionHandler buildRestExceptionHandler() {
        return new RestExceptionHandler();
    }

    @Bean
    public AnalyticService buildAnalyticService(RestTemplateBuilder builder) {
        return new AnalyticServiceImplementation(buildElasticsearch(builder), objectMapper);
    }

    @Bean
    public AdminModuleUtil buildAdminModuleUtil() {
        return new AdminModuleUtil(buildJwtTokenUtil(), objectMapper, buildSessionService(), ems2ConfigProperties);
    }

    @Bean
    public ApplicationCategoryService buildApplicationCategoryService() {
        return new ApplicationCategoryServiceImpl(fmaaProperties, applicationCategoryRepo);
    }

    @Bean
    public ApplicationTileService buildApplicationTileService() {
        return new ApplicationTileServiceImpl(fmaaProperties, applicationTileRepo);
    }

    @Bean
    public ImportMapService buildImportMapService() {
        return new ImportMapServiceImpl(fmaaProperties, importMapRepo);
    }

    @Bean
    public ImportMapAuditService buildImportMapAuditService() {
        return new ImportMapAuditServiceImpl(importMapAuditRepo);
    }

    @Bean
    public ApplicationCategoryAuditService buildApplicationCategoryAuditService() {
        return new ApplicationCategoryAuditServiceImpl(applicationCategoryAuditRepo);
    }

    @Bean
    public ApplicationTileAuditService buildApplicationTileAuditService() {
        return new ApplicationTileAuditServiceImpl(applicationTileAuditRepo);
    }

    @Bean
    public CsvUtility buildCsvUtility() {
        return new CsvUtility();
    }

    @Bean
    public ApplicationConfigService buildApplicationConfigService(RestTemplateBuilder builder) {
        RestTemplate restTemplate = builder
                .setConnectTimeout(fmaaProperties.getConnectTimeout())
                .setReadTimeout(fmaaProperties.getReadTimeout())
                .build();
        return new ApplicationConfigServiceImpl(restTemplate, objectMapper, fmaaProperties);
    }

}
