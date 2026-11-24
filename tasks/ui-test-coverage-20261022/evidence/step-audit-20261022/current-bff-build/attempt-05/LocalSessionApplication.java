package local.portalsession;

import com.auth0.jwt.JWT;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.config.*;
import com.scb.sso.singleuibff.controller.v2.JwtAuthenticationController;
import com.scb.sso.singleuibff.dto.ems2.v2.Ems2Result;
import com.scb.sso.singleuibff.dto.ems2.v2.Entity;
import com.scb.sso.singleuibff.dto.request.RequestOfAuthenticate;
import com.scb.sso.singleuibff.entity.*;
import com.scb.sso.singleuibff.exceptions.AuthenticationException;
import com.scb.sso.singleuibff.repository.*;
import com.scb.sso.singleuibff.service.v1.*;
import com.scb.sso.singleuibff.service.v1.implementation.*;
import com.scb.sso.singleuibff.service.v2.AuthorizationService;
import com.scb.sso.singleuibff.util.*;
import jakarta.persistence.EntityManagerFactory;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.lang.reflect.Proxy;
import java.nio.charset.StandardCharsets;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.*;
import javax.sql.DataSource;
import org.jasypt.util.text.BasicTextEncryptor;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.data.jpa.JpaRepositoriesAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration;
import org.springframework.boot.autoconfigure.ldap.LdapAutoConfiguration;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.data.jpa.repository.support.JpaRepositoryFactoryBean;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.SharedEntityManagerCreator;
import org.springframework.orm.jpa.persistenceunit.PersistenceManagedTypes;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.filter.OncePerRequestFilter;

@SpringBootConfiguration
@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class,HibernateJpaAutoConfiguration.class,JpaRepositoriesAutoConfiguration.class,LdapAutoConfiguration.class})
@Import({JwtAuthenticationController.class, com.scb.sso.singleuibff.controller.v1.ApplicationCategoryController.class, com.scb.sso.singleuibff.controller.v1.ApplicationTileController.class, com.scb.sso.singleuibff.controller.v1.ImportMapController.class, com.scb.sso.singleuibff.filter.RestExceptionHandler.class, LocalSessionApplication.Health.class, LocalSessionApplication.Fixture.class})
public class LocalSessionApplication {
    public static final String USER="user-a";
    public static final String PASSWORD="FixturePass1!";
    static volatile boolean analyticsFailure=false, entitlementsFailure=false;
    static volatile List<Entity> fixtureEntities=null;
    static boolean fault(String name){
        var attrs=org.springframework.web.context.request.RequestContextHolder.getRequestAttributes();
        return attrs instanceof org.springframework.web.context.request.ServletRequestAttributes a && name.equals(a.getRequest().getHeader("X-UI-Audit-Fault"));
    }
    public static void main(String[] args) {
        SpringApplication app=new SpringApplication(LocalSessionApplication.class);
        app.setDefaultProperties(Map.ofEntries(
            Map.entry("server.address","127.0.0.1"), Map.entry("server.port",8090),
            Map.entry("server.servlet.context-path","/api/auth"),
            Map.entry("spring.config.location","optional:classpath:/local-only.properties"),
            Map.entry("spring.main.banner-mode","off"), Map.entry("spring.jpa.open-in-view",false),
            Map.entry("spring.flyway.enabled",false), Map.entry("logging.level.root","WARN"),
            Map.entry("logging.level.com.scb.sso.singleuibff.controller.v2.JwtAuthenticationController","INFO"),
            Map.entry("logging.level.org.hibernate.orm.deprecation","ERROR"),
            Map.entry("logging.level.org.hibernate.SQL","DEBUG"),
            Map.entry("logging.level.org.hibernate.tool.schema","DEBUG")
        ));
        app.run(args);
    }

    @Bean com.scb.sso.singleuibff.service.v2.filter.AuthFilterExecutor authFilterExecutor() {
        return new com.scb.sso.singleuibff.service.v2.filter.AuthFilterExecutor();
    }
    @Bean com.scb.sso.singleuibff.service.v2.filter.TileRegionProperties tileRegionProperties() {
        return new com.scb.sso.singleuibff.service.v2.filter.TileRegionProperties();
    }
    @Bean com.scb.sso.singleuibff.service.v2.filter.AuthFilter authFilter() {
        return new com.scb.sso.singleuibff.service.v2.filter.AuthFilter() {
            public String getFilterType() {return "LOCAL_DISABLED_EXTERNAL_EMS3";}
        };
    }
    @Bean JWTConfigProperties jwtConfigProperties() throws Exception {
        KeyPairGenerator generator=KeyPairGenerator.getInstance("RSA"); generator.initialize(2048);
        KeyPair pair=generator.generateKeyPair();
        JWTConfigProperties p=new JWTConfigProperties();
        p.setPrv(Base64.getEncoder().encodeToString(pair.getPrivate().getEncoded()));
        p.setPub(Base64.getEncoder().encodeToString(pair.getPublic().getEncoded()));
        p.setTokenExpiration(1); p.setReTokenExpiration(2); p.setAbsoluteExpiration(60); return p;
    }
    @Bean JwtTokenUtil jwtTokenUtil(JWTConfigProperties p) {return new JwtTokenUtil(p);}
    @Bean DataSource dataSource() {
        DriverManagerDataSource source=new DriverManagerDataSource(); source.setDriverClassName("org.postgresql.Driver");
        source.setUrl("jdbc:postgresql://127.0.0.1:54390/postgres?currentSchema=post_trade_portal_service");
        source.setUsername("ui_audit"); source.setPassword(""); return source;
    }
    @Bean LocalContainerEntityManagerFactoryBean entityManagerFactory(DataSource dataSource) {
        LocalContainerEntityManagerFactoryBean bean=new LocalContainerEntityManagerFactoryBean();
        bean.setDataSource(dataSource); bean.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
        bean.setManagedTypes(PersistenceManagedTypes.of(ApplicationSession.class.getName(),ApplicationCategory.class.getName(),ApplicationCategoryAudit.class.getName(),ApplicationTile.class.getName(),ApplicationTileAudit.class.getName(),ImportMap.class.getName(),ImportMapAudit.class.getName()));
        bean.setJpaPropertyMap(Map.of("hibernate.hbm2ddl.auto","none","hibernate.default_schema","post_trade_portal_service","hibernate.show_sql","false","hibernate.physical_naming_strategy","org.hibernate.boot.model.naming.CamelCaseToUnderscoresNamingStrategy"));
        return bean;
    }
    @Bean PlatformTransactionManager transactionManager(EntityManagerFactory factory) {return new JpaTransactionManager(factory);}
    @Bean
    JpaRepositoryFactoryBean<ApplicationSessionRepo,ApplicationSession,Long> applicationSessionRepo(EntityManagerFactory factory) {
        JpaRepositoryFactoryBean<ApplicationSessionRepo,ApplicationSession,Long> bean=new JpaRepositoryFactoryBean<>(ApplicationSessionRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));
        bean.setTransactionManager("transactionManager");
        return bean;
    }
    @Bean SessionService sessionService(ApplicationSessionRepo repo) {return new SessionServiceImplementation(repo);}
    @Bean OUDAuthenticationService oudAuthenticationService() {
        return new OUDAuthenticationService(null,null,null,null) {
            @Override public Map<String,String> authenticate(RequestOfAuthenticate request) {
                if (!List.of(USER,"alice","bob","user-b","UI-ADMIN-01","UI-ADMIN-02","UI-CHECKER-01","UI-SUPER-01","admin-a","admin-b","admin-c","admin-s").contains(request.getUsername()) || !PASSWORD.equals(request.getPassword()))
                    throw AuthenticationException.builder().code("LOCAL_FIXTURE").message("Invalid synthetic local credentials").build();
                return new HashMap<>(Map.of("userId",request.getUsername(),"fullName",request.getUsername(),"emailId","session-local@example.invalid","country","LOCAL","locale","en"));
            }
        };
    }
    @Bean MFAAuthenticationService mfaAuthenticationService() {
        return new MFAAuthenticationService(null,null,null) {
            @Override public Map<String,String> authenticate(RequestOfAuthenticate request) {throw new IllegalStateException("Remote MFA disabled in local fixture");}
        };
    }
    @Bean EntraAuthenticationService entraAuthenticationService() {
        return request->{throw new IllegalStateException("Remote Entra disabled in local fixture");};
    }
    @Bean AuthorizationService authorizationService() {
        return (username,requested)->{
            if(entitlementsFailure||fault("entitlements"))throw new IllegalStateException("Local entitlement fixture failure");
            if(fixtureEntities!=null){Ems2Result result=new Ems2Result();result.setEntities(fixtureEntities);return result;}
            Entity entity=new Entity(); entity.setId(1L); entity.setName("FMO PORTAL ADMIN"); entity.setApplicationName("LOCAL");
            entity.setRoleId(1L); entity.setRoleName(List.of("UI-SUPER-01","admin-s").contains(username)?"SUPER_USER":List.of("admin-a","admin-b","admin-c").contains(username)?"FMO_ADMIN":"TEST_OWNER"); entity.setSubjects(List.of());
            Ems2Result result=new Ems2Result(); result.setEntities(List.of(entity)); return result;
        };
    }
    @Bean FmaaProperties fmaaProperties(){FmaaProperties p=new FmaaProperties();p.setCreationEnabled(true);return p;}
    @Bean ApplicationCategoryService applicationCategoryService(FmaaProperties p,ApplicationCategoryRepo repo){return new ApplicationCategoryServiceImpl(p,repo);}
    @Bean ApplicationCategoryAuditService applicationCategoryAuditService(ApplicationCategoryAuditRepo repo){return new ApplicationCategoryAuditServiceImpl(repo);}
    @Bean ApplicationTileService applicationTileService(FmaaProperties p,ApplicationTileRepo repo){return new ApplicationTileServiceImpl(p,repo);}
    @Bean ApplicationTileAuditService applicationTileAuditService(ApplicationTileAuditRepo repo){return new ApplicationTileAuditServiceImpl(repo);}
    @Bean ImportMapService importMapService(FmaaProperties p,ImportMapRepo repo){return new ImportMapServiceImpl(p,repo);}
    @Bean ImportMapAuditService importMapAuditService(ImportMapAuditRepo repo){return new ImportMapAuditServiceImpl(repo);}
    @Bean JpaRepositoryFactoryBean<ApplicationCategoryRepo,ApplicationCategory,Long> applicationCategoryRepo(EntityManagerFactory factory){
        JpaRepositoryFactoryBean<ApplicationCategoryRepo,ApplicationCategory,Long> bean=new JpaRepositoryFactoryBean<>(ApplicationCategoryRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));bean.setTransactionManager("transactionManager");return bean;
    }
    @Bean JpaRepositoryFactoryBean<ApplicationCategoryAuditRepo,ApplicationCategoryAudit,Long> applicationCategoryAuditRepo(EntityManagerFactory factory){
        JpaRepositoryFactoryBean<ApplicationCategoryAuditRepo,ApplicationCategoryAudit,Long> bean=new JpaRepositoryFactoryBean<>(ApplicationCategoryAuditRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));bean.setTransactionManager("transactionManager");return bean;
    }
    @Bean JpaRepositoryFactoryBean<ApplicationTileRepo,ApplicationTile,Long> applicationTileRepo(EntityManagerFactory factory){
        JpaRepositoryFactoryBean<ApplicationTileRepo,ApplicationTile,Long> bean=new JpaRepositoryFactoryBean<>(ApplicationTileRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));bean.setTransactionManager("transactionManager");return bean;
    }
    @Bean JpaRepositoryFactoryBean<ApplicationTileAuditRepo,ApplicationTileAudit,Long> applicationTileAuditRepo(EntityManagerFactory factory){
        JpaRepositoryFactoryBean<ApplicationTileAuditRepo,ApplicationTileAudit,Long> bean=new JpaRepositoryFactoryBean<>(ApplicationTileAuditRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));bean.setTransactionManager("transactionManager");return bean;
    }
    @Bean JpaRepositoryFactoryBean<ImportMapRepo,ImportMap,Long> importMapRepo(EntityManagerFactory factory){
        JpaRepositoryFactoryBean<ImportMapRepo,ImportMap,Long> bean=new JpaRepositoryFactoryBean<>(ImportMapRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));bean.setTransactionManager("transactionManager");return bean;
    }
    @Bean JpaRepositoryFactoryBean<ImportMapAuditRepo,ImportMapAudit,Long> importMapAuditRepo(EntityManagerFactory factory){
        JpaRepositoryFactoryBean<ImportMapAuditRepo,ImportMapAudit,Long> bean=new JpaRepositoryFactoryBean<>(ImportMapAuditRepo.class);
        bean.setEntityManager(SharedEntityManagerCreator.createSharedEntityManager(factory));bean.setTransactionManager("transactionManager");return bean;
    }
    @Bean org.springframework.boot.ApplicationRunner initializeSequences(DataSource dataSource){return args->{
        try(var connection=dataSource.getConnection();var stmt=connection.createStatement()){
            for(String table:List.of("application_category","application_tile","import_map"))stmt.execute("CREATE SEQUENCE IF NOT EXISTS post_trade_portal_service."+table+"_seq START WITH 1000");
        }
    };}
    @Bean AnalyticService analyticService() {
        return new AnalyticService() {
            public void insertData(com.scb.sso.singleuibff.dto.request.RequestOfAnalytics request,String username,String ip) {if(analyticsFailure||fault("analytics"))throw new IllegalStateException("Local analytics fixture failure");}
            public com.scb.sso.singleuibff.dto.elastic.Response filterData(String filter) {throw new UnsupportedOperationException("Analytics disabled in local fixture");}
        };
    }
    @Bean OudUtil oudUtil() {return new OudUtil(new WhitelistedProperties(),new BasicTextEncryptor());}
    @Bean EMS2ConfigProperties ems2ConfigProperties() {EMS2ConfigProperties p=new EMS2ConfigProperties();p.setAdminModuleEntity("FMO PORTAL ADMIN");return p;}
    @Bean AdminModuleUtil adminModuleUtil(JwtTokenUtil jwt,ObjectMapper mapper,SessionService session) {return new AdminModuleUtil(jwt,mapper,session,ems2ConfigProperties());}
    @Bean FilterRegistrationBean<OncePerRequestFilter> auditFilter(ObjectMapper mapper) {
        OncePerRequestFilter filter=new OncePerRequestFilter() {
            @Override protected void doFilterInternal(HttpServletRequest req,HttpServletResponse res,FilterChain chain) throws ServletException,IOException {
                long start=System.nanoTime(); String started=Instant.now().toString();
                try {chain.doFilter(req,res);} finally {
                    Map<String,Object> event=new LinkedHashMap<>(); event.put("event","local_http"); event.put("started_at",started);
                    event.put("method",req.getMethod()); event.put("route",req.getRequestURI()); event.put("status",res.getStatus());
                    event.put("elapsed_ms",(System.nanoTime()-start)/1_000_000.0);
                    Map<String,Object> tokens=new LinkedHashMap<>();
                    for (String header:List.of("Single-UI-Authorization","Single-UI-Refresh")) {
                        String raw=res.getHeader(header);
                        if (raw!=null && !raw.isBlank()) {
                            try {
                                String token=raw.substring(raw.lastIndexOf(' ')+1); DecodedJWT decoded=JWT.decode(token);
                                Map<String,Object> info=new LinkedHashMap<>(); info.put("sha256",HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(raw.getBytes(StandardCharsets.UTF_8))));
                                info.put("iss",decoded.getIssuer()); info.put("iat",decoded.getIssuedAt().toInstant().toString()); info.put("exp",decoded.getExpiresAt().toInstant().toString());
                                tokens.put(header,info);
                            } catch(Exception e) {tokens.put(header,Map.of("inspection","FAILED","class",e.getClass().getSimpleName()));}
                        }
                    }
                    event.put("issued_tokens",tokens); System.out.println(mapper.writeValueAsString(event));
                }
            }
        };
        FilterRegistrationBean<OncePerRequestFilter> registration=new FilterRegistrationBean<>(filter); registration.setOrder(-100); return registration;
    }
    @RestController public static class Fixture {
        @org.springframework.beans.factory.annotation.Autowired DataSource dataSource;
        @org.springframework.beans.factory.annotation.Autowired ObjectMapper mapper;
        @org.springframework.beans.factory.annotation.Autowired FmaaProperties creation;
        @org.springframework.beans.factory.annotation.Autowired JwtTokenUtil jwt;
        @org.springframework.beans.factory.annotation.Autowired ApplicationCategoryRepo categories;
        @org.springframework.beans.factory.annotation.Autowired ImportMapRepo maps;
        @org.springframework.beans.factory.annotation.Autowired ApplicationTileRepo tiles;
        @org.springframework.beans.factory.annotation.Autowired ApplicationCategoryAuditRepo categoryAudits;
        @org.springframework.beans.factory.annotation.Autowired ImportMapAuditRepo mapAudits;
        @org.springframework.beans.factory.annotation.Autowired ApplicationTileAuditRepo tileAudits;
        static final List<String> TABLES=List.of("application_category","import_map","application_tile","application_category_audit","import_map_audit","application_tile_audit");
        @org.springframework.web.bind.annotation.PostMapping("/local/fixture/sql")
        public Map<String,Object> sql(@org.springframework.web.bind.annotation.RequestBody Map<String,Object> body)throws Exception{
            List<Map<String,Object>> results=new ArrayList<>();
            try(var c=dataSource.getConnection();var stmt=c.createStatement()){
                for(Object raw:(List<?>)body.getOrDefault("statements",List.of())){
                    String statement=raw.toString();boolean hasRows=stmt.execute(statement);Map<String,Object> result=new LinkedHashMap<>();
                    if(hasRows){var rs=stmt.getResultSet();var metadata=rs.getMetaData();List<Map<String,Object>> rows=new ArrayList<>();
                        while(rs.next()){Map<String,Object> row=new LinkedHashMap<>();for(int i=1;i<=metadata.getColumnCount();i++)row.put(metadata.getColumnLabel(i),rs.getObject(i));rows.add(row);}result.put("rows",rows);
                    }else result.put("updateCount",stmt.getUpdateCount());results.add(result);
                }
            }return Map.of("results",results);
        }
        @org.springframework.web.bind.annotation.PostMapping("/local/fixture/reset")
        public Map<String,Object> reset()throws Exception{
            creation.setCreationEnabled(true);analyticsFailure=false;entitlementsFailure=false;fixtureEntities=null;
            try(var c=dataSource.getConnection();var stmt=c.createStatement()){
                for(String table:TABLES)stmt.execute("ALTER TABLE post_trade_portal_service."+table+" DROP CONSTRAINT IF EXISTS ui_audit_fail");
                stmt.execute("TRUNCATE post_trade_portal_service.application_tile_audit,post_trade_portal_service.application_category_audit,post_trade_portal_service.import_map_audit,post_trade_portal_service.application_tile,post_trade_portal_service.application_category,post_trade_portal_service.import_map,post_trade_portal_service.application_session CASCADE");
                for(String table:TABLES)stmt.execute("ALTER SEQUENCE post_trade_portal_service."+table+"_seq RESTART WITH 1000");
            }return Map.of("reset",true,"database","disposable PostgreSQL18.4");
        }
        @org.springframework.web.bind.annotation.PostMapping("/local/fixture/seed")
        public Map<String,Object> seed(@org.springframework.web.bind.annotation.RequestBody Map<String,Object> body)throws Exception{
            for(Object v:(List<?>)body.getOrDefault("categories",List.of()))categories.save(mapper.convertValue(v,ApplicationCategory.class));
            for(Object v:(List<?>)body.getOrDefault("importMaps",List.of()))maps.save(mapper.convertValue(v,ImportMap.class));
            for(Object v:(List<?>)body.getOrDefault("tiles",List.of()))tiles.save(mapper.convertValue(v,ApplicationTile.class));
            for(Object v:(List<?>)body.getOrDefault("categoryAudits",List.of()))categoryAudits.save(mapper.convertValue(v,ApplicationCategoryAudit.class));
            for(Object v:(List<?>)body.getOrDefault("importMapAudits",List.of()))mapAudits.save(mapper.convertValue(v,ImportMapAudit.class));
            for(Object v:(List<?>)body.getOrDefault("tileAudits",List.of()))tileAudits.save(mapper.convertValue(v,ApplicationTileAudit.class));
            if(body.containsKey("creationEnabled"))creation.setCreationEnabled(Boolean.TRUE.equals(body.get("creationEnabled")));
            if(body.containsKey("analyticsFailure"))analyticsFailure=Boolean.TRUE.equals(body.get("analyticsFailure"));
            if(body.containsKey("entitlementsFailure"))entitlementsFailure=Boolean.TRUE.equals(body.get("entitlementsFailure"));
            if(body.containsKey("entities")){fixtureEntities=new ArrayList<>();for(Object v:(List<?>)body.get("entities"))fixtureEntities.add(mapper.convertValue(v,Entity.class));}
            if(body.get("failure")!=null){String value=body.get("failure").toString();String table=switch(value){case "category-save"->"application_category";case "category-audit"->"application_category_audit";case "importmap-save"->"import_map";case "importmap-audit"->"import_map_audit";case "tile-save"->"application_tile";case "tile-audit"->"application_tile_audit";default->throw new IllegalArgumentException("Unsupported fixture failure");};
                try(var c=dataSource.getConnection();var stmt=c.createStatement()){stmt.execute("ALTER TABLE post_trade_portal_service."+table+" ADD CONSTRAINT ui_audit_fail CHECK(FALSE) NOT VALID");}
            }
            return Map.of("seeded",true,"creationEnabled",creation.isCreationEnabled());
        }
        @org.springframework.web.bind.annotation.PostMapping("/local/fixture/token")
        public Map<String,Object> token(@org.springframework.web.bind.annotation.RequestBody Map<String,Object> body)throws Exception{
            String subject=Objects.toString(body.getOrDefault("subject","user-a"));String issuer=Objects.toString(body.getOrDefault("issuer","single-ui-bff"));
            long seconds=((Number)body.getOrDefault("expiresInSeconds",600)).longValue();String id=Objects.toString(body.getOrDefault("id",UUID.randomUUID().toString()));
            Map<String,String> payload=new HashMap<>();payload.put("id",id);payload.put("oud",mapper.writeValueAsString(Map.of("userId",subject,"fullName",subject)));
            var method=JwtTokenUtil.class.getDeclaredMethod("doGenerateToken",String.class,Map.class,Date.class,String.class);method.setAccessible(true);
            String token=(String)method.invoke(jwt,subject,payload,new Date(System.currentTimeMillis()+seconds*1000),issuer);
            return Map.of("token","Bearer "+token,"fixture",true,"issuer",issuer,"expiresInSeconds",seconds,"id",id);
        }
    }
    @RestController public static class Health {
        @GetMapping("/local/health") public Map<String,Object> health() {
            return Map.of("status","UP","scope","actual BFF controller/JWT/session code with local fixtures","access_minutes",1,"refresh_minutes",2,"refresh_extra_seconds",24,"absolute_minutes",60,"database","isolated PostgreSQL18.4; exact current migrations; actual JPA repositories","remote_access","DISABLED");
        }
    }
}
