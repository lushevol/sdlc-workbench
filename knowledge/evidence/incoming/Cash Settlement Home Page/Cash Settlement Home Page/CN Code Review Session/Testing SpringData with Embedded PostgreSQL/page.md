> **INFO**
> This solution haven't been widely verified yet, please reach out to us if you've any suggestions or find any issues.

## 1. Introduction

### 1.1. Why test is necessary

SpringData provides JPA for interacting with rational databases out of the box. We can simplifily define a `@Repository` interface to query the database.

We could create a query by naming convension:
Optional<CashFlowData> findByCashflowIndex(String cashflowIndex)
or with customized sql:
@Query("select max(version) from t_event where aggregate_type = :aggregateType")
Long findMaxVersion(String aggregateType);
Most of the dirty work is done by SpringBoot Data, which provides convenience for us, but it can also lead to mistakes. If the repository is not working as expected, it could be due to the following reasons:

- Mistakes in flyway scripts
- Incorrect method name
- Incorrect SQL grammar
- Unsupported feature by PostgreSQL
- The funtion is not returning the expected result

### 1.2. General testing approaches

There are several ways to test the repository:

- Use `@DataJpaTest` to do the unit test of the repository
- Use `@SpringBootTest` to do the integration test of the application, which also covers the repository layer

There are a few approaches to set up the database for testing, as shown in Table 1.

| **Database Type** | **Platform** | **Compability with PG** |
| --- | --- | --- |
| Real PG | * | 😁 |
| H2 | in-memory | 😞 |
| Testcontainers | Docker | 😁 |
| otj-pg-embedded | in-memory¹ | 😞 |
| Zonky | Local PG | 😁 |

Table 1: Approaches for setting test database

Using a real PostgreSQL database is not recommended for testing due to lack of isolation. H2 is also not a suitable option considering its compatibility with PostgreSQL. The industry standard for testing is to use Testcontainers, but it may not be feasible in our bank environment as Docker is not available on our devices.

otj-pg-embedded is created in 2018 to support in-memory PG, however the latest version has already migrated to Testcontainers. [Zonky](https://github.com/zonkyio/embedded-postgres?tab=readme-ov-file) forks it and continus to support native binaries of PG without virtualization.

Therefore, Zonky is the only possible option for us currently.

### 1.3. How Zonky works

Zonky automatically fetches the PostgreSQL binaries and starts a PostgreSQL server in the background.
[ prefetching-1] i.z.t.d.p.embedded.EmbeddedPostgres : Postgres binaries at C:\Users\2022123\AppData\Local\Temp\embedded-pg\PG-b95a81b3f867f51765631fc19cc132c3
As we can see it downloads the binaries to a temporary folder and starts the server:
C:\Users\2022123\AppData\Local\Temp\embedded-pg\PG-b95a81b3f867f51765631fc19cc132c3\bin>ls -lh | grep exe
-rwxr-xr-x 1 2022123 1049089 195K Mar 24 15:33 initdb.exe
-rwxr-xr-x 1 2022123 1049089 120K Mar 24 15:33 pg_ctl.exe
-rwxr-xr-x 1 2022123 1049089 7.5M Mar 24 15:33 postgres.exe
Zonky PG offers the following features²:

- Lightweight bundles of PostgreSQL binaries with reduced size ( 10MB)
- Embedded PostgreSQL 11+ binaries even for Linux platform
- Configurable version of PostgreSQL binaries

### 1.4. Known limitations

Since Zonky uses native PG, which downloads exe files to local devices, it might be blocked if the security stretegy changes in the future.

## 2. Testing repository with Zonky

### 2.1. Maven Dependencies

First, zonky dependencies need to be added to the `pom.xml`:
<dependency>
<groupId>io.zonky.test</groupId>
<artifactId>embedded-database-spring-test</artifactId>
<version>2.6.0</version>
<scope>test</scope>
</dependency>
<dependency>
<groupId>io.zonky.test</groupId>
<artifactId>embedded-postgres</artifactId>
<version>2.1.0</version>
<scope>test</scope>
</dependency>
Also be aware that zonky test suit requires Junt4 and not work with Junt5, so additionally we need to add junit-vintage-engine:
<dependency>
<groupId>org.junit.vintage</groupId>
<artifactId>junit-vintage-engine</artifactId>
<version>5.11.4</version>
<scope>test</scope>
</dependency>
### 2.2. Enable flyway in tests

Since we are using flyway to manage the database schema, we need to enable flyway in the test environment. If flyway is disabled previously, make sure to enable it in the test application properties.

### 2.3. `@DataJpaTest` with zonky

Zonky provides a `@AutoConfigureEmbeddedDatabase` annotation to set up the embedded PostgreSQL database. The provider must be set to `ZONKY` to use the local PostgreSQL database.
@RunWith(SpringRunner.class)
@DataJpaTest
@AutoConfigureEmbeddedDatabase(provider = ZONKY)
public class TodoRepositoryTest {
@Autowired
TodoRepository repository;
Then you should be able to test the repository:
import org.junit.Test; // MUST use Junit4!

@Test
public void testMethod() {
Iterable<TodoEntity> result = repository.findAll();
List<TodoEntity> list = new ArrayList<>();
result.iterator().forEachRemaining(list::add);
assertEquals(1, list.size());
}
### 2.4. `@SpringBootTest` with zonky

You can also use zonky in `@SpringBootTest`, just use the same configuration:
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@AutoConfigureEmbeddedDatabase(provider = ZONKY)
@Sql(scripts = "/script/test-cashflow-data.sql")
public class GraphQlIntegrationTest {
Note that you can use Junit5 in `@SpringBootTest` with zonky.

### 2.5. Insert test data

It's important that you should not mock the repository in JPA test or integration test. Instead, you should insert data into the database. You can use the following approach to insert data:

- Use `@Sql` to insert data by sql scripts in integration tests, see Section 2.4.
- Use `@TestEntityManager` to insert data programmatically.
- Use autowired repositories to insert data. This is should not be used when do unit testing of a repository.

For example, you can autowire the `TestEntityManager` and insert entities in `@Before` method in the test class:
public class TodoRepositoryTest {
@Autowired
TestEntityManager entityManager;

@Before
public void prepare() {
TodoEntity e = new TodoEntity();
e.setId("id1");

e = entityManager.persist(e);
}
}
### 2.6. Set default schema of PG

Zonky uses a default schema `public` for the embedded PostgreSQL database. If you have a different schema in your flyway scripts, you need to set the default schema to the same schema as your flyway scripts.

For example, to use `cash_settlement_query_cn` as default schema, you can set the following properties in the test application properties:
zonky:
test:
database:
postgres:
client:
properties:
currentSchema: cash_settlement_query_cn
### 2.7. Example

A real example of using zonky in the repository test can be found in the following commit:

- Commit: [#7177438: added demo of using embedded-postgres for jpa test](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/commit/d6bba744aa058814791d612353da1b47d27040e3?refName=refs%2Fheads%2Ffeature%2F7177438-entitlement-tranche) 1. `GraphQlIntegrationTest`: integration test of PG with GraphQL query 2. `CashflowDataRepositoryTest`: unit test of repository
- Pipeline: [cash-settlement-query-service #20250324.1](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=5529864&view=results)