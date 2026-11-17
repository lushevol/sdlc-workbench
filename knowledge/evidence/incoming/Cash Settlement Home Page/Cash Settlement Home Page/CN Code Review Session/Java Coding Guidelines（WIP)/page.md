## Contents

**1.Introduction  ⁠1**

1.1.Motivation  ⁠1
1.2.Scope  ⁠1

**2.Specification  ⁠1**

2.1.Naming Conventions  ⁠1
2.1.1.Use lower snake case for package name  ⁠1
2.1.2.Prefer lower camel case style  ⁠1
2.1.3.Use upper snake case for constants  ⁠1
2.1.4.Use single capital letter for type parameter  ⁠1
2.1.5.Constants must be final  ⁠1
2.2.Code Style  ⁠1
2.2.1.Remove unused imports  ⁠1
2.3.OOP  ⁠1
2.3.1.Follow OOP principles  ⁠1
2.3.2.Use most restrictive access level  ⁠1
2.3.3.Don't use raw Map for JSON  ⁠1
2.3.4.Avoid raw types  ⁠1
2.3.5.Method should not be too complex  ⁠1
2.3.6.Minimize scope of parameter  ⁠1
2.3.7.Combine OOP with *functional-style* programming  ⁠1
2.3.8.Mitigate side effects of method  ⁠1
2.4.Best Practices  ⁠1
2.4.1.Use new language features of JDK17  ⁠1
2.4.2.Remove unsed private method  ⁠1
2.4.3.Remove unsed local variable  ⁠1
2.4.4.Remove useless assignment  ⁠1
2.4.5.Don't commit debug code  ⁠1
2.4.6.Prefer constructor injection  ⁠1
2.4.7.Use text blocks for multi-line string  ⁠1
2.4.8.Avoid using template engine for XML generation  ⁠1
2.5.Collections  ⁠1
2.5.1.Prefer `Stream.toList()` over `Collectors.toList()`  ⁠1
2.5.2.Prefer `isEmpty` to check if collection is empty  ⁠1
2.6.Concurrency & Safety  ⁠1
2.6.1.Handle `InterruptedException` correctly  ⁠1
2.6.2.Release resources in all cases  ⁠1
2.7.Database  ⁠1
2.7.1.Remember to update `update_at` field  ⁠1
2.8.Comments  ⁠1
2.8.1.Avoid JavaDoc comments for application code  ⁠1
2.8.2.Avoid commented-out code  ⁠1
2.8.3.Add comments to explain if not obvious  ⁠1
2.8.4.Add @Deprecated for deprecated code  ⁠1
2.9.Logging  ⁠1
2.9.1.Log when request received  ⁠1
2.9.2.Log request and response of API call  ⁠1
2.9.3.Don't log large field  ⁠1
2.9.4.Use place holder in log  ⁠1
2.9.5.Use business description as log marker  ⁠1
2.10.Testing  ⁠1
2.10.1.Write unit test for each class  ⁠1
2.10.2.Follow F.I.R.S.T principle when writing tests  ⁠1
2.10.3.Use Given-When-Then structure  ⁠1
2.10.4.Use assertions  ⁠1
2.10.5.Don't add `main` for testing  ⁠1
2.10.6.Ensure enough assertions  ⁠1
2.10.7.Test only one scenerio in one case  ⁠1
2.10.8.Mock external dependencies  ⁠1
2.10.9.Add integration test for APIs  ⁠1
2.10.10.Add integration test for async listeners  ⁠1
2.10.11.Use package visibility for tests  ⁠1
2.10.12.Add tests when fixing bug  ⁠1

**Bibliography  ⁠1**

"MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 [1].

## 1. Introduction

### 1.1. Motivation

As with any programming language, following coding standards and best practices is essential for producing cleaner, better readable, and more efficient code with minimal bugs and errors. In addition, they offer an uniform way for developers to build highly functional code.

RATAN is a highly complex system of servel hundred thousand lines code, while it's still in very earlier stage, being developed by developers with diverse experiences and backgrounds. As Java is highly expressive programming language, it's important to define coding standards as a team agreement, which helps to avoid opinioned styles and improve code quality.

In some other industry, there's open sourced Java coding speficications [2]. However, not all of the items in such speficications applies to our context. As a result, we build our own version of Java coding guidelines, and we'll keep updating it accroding to our needs.

This guideline SHOULD be used as reference in code review.

### 1.2. Scope

This guidelines applies to any Java stack repositories inside RATAN, limited to the code implementations, including automated tests maintained by developers.

Note that it's not intended to cover everything in this guideline, please also pay attention to SonarQube reported issues.

## 2. Specification

### 2.1. Naming Conventions

#### 2.1.1. Use lower snake case for package name

Package names SHOULD be in *lower_snake_case* [3].
package com.example.deep_space; // Compliant
package com.scb.ratan.nostroRefresh; // Non-compliant
#### 2.1.2. Prefer lower camel case style

Method names, parameter names, member variable names, and local variable names MUST be written in *lowerCamelCase* [4], [5].
String cashflowId; // Compliant
KafkaTemplate<String, String> kafkaTemplate; // Compliant

String CashflowId; // Non-compliant
String Cashflow__Cashflow_Id; // Non-compliant
When a name contains abbreviate, it's also RECOMMENDED to use lower case:
String FMID; // Non-compliant, prefer fmId
#### 2.1.3. Use upper snake case for constants

Constants and enums MUST be named use *UPPER_SNAKE_CASE* [6], [7].

enum RuleType { NSTP, SWIFT_SUPPRESSION } // Compliant
enum GuiFileHeaderName { indexedTerm } // Non-compliant
public static final float pi = 3.14159f; // Non-compliant
Note that `static final` is not equivlent to constants. Constants are static final fields whose contents are deeply immutable and whose methods have no detectable side effects.
// Not constants
static final Logger logger = Logger.getLogger(MyClass.getName());
#### 2.1.4. Use single capital letter for type parameter

Type parameter MUST be a single capital letter [8] .
public class Data<T> {} // Compliant
public class Entity<ID> {} // Non-compliant
#### 2.1.5. Constants must be final

Constants MUST NOT be declared as `static` without `final` [9].
public static Set<String> // Non-compliant
COLLATERAL_SECURITIES = new HashSet<>();
### 2.2. Code Style

#### 2.2.1. Remove unused imports

Unnecessary imports refer to importing types that are not used or referenced anywhere in the code. Although they don’t affect the runtime behavior of the application after compilation, removing them will improve the readability and maintainability of the code [10].

Figure 1: Unused imports shown in IDEA.

### 2.3. OOP

#### 2.3.1. Follow OOP principles

You SHOULD follow OOP(Object-Oriented Programming) design principles when coding:

- Don't Repeat Yourself (DRY) [11]
- Open-Closed Principle [12]
- Single Responsibility Principle [12]
- Common Closure Principle [12]
- Law of Demeter (LoD), or Principle of Least Knowledge [13]

#### 2.3.2. Use most restrictive access level

You MUST use the most restrictive access level that makes sense for a particular member. Use `private` unless you have a good reason not to.

Avoid `public` fields except for constants. Public fields tend to link you to a particular implementation and limit your flexibility in changing your code [14].
public class Service {
public void process() {
internalProcess();
}

public void internalProcess() { // Non-compliant, should be private
// ...
}
}
#### 2.3.3. Don't use raw Map for JSON

public List<CounterParty> fetchCounterParties(List<String> fmIds) {
List<Map<String, ?>> queryResults = fetchCounterPartyByfmIds(fmIds);
List<CounterParty> response = new ArrayList<>();
for (Map<String, ?> map : queryResults) {
Map<String, String> fmAccount = (HashMap) map.get("fmAccount");
CounterParty counterParty = CounterParty.builder()
.fmId(fmAccount.get("fmId"))
.fmCode(fmAccount.get("fmCode")).build();
response.add(counterParty);
}
return response;
}
#### 2.3.4. Avoid raw types

When generic types are used raw (without type parameters), the compiler is not able to do generic type checking.

For this reason, it is sometimes necessary to cast objects and defer type-checking to runtime.

When a cast fails, a ClassCastException is thrown and the program most likely crashes. Therefore, this issue might impact the availability and reliability of your application [15].
HashMap metadata = new HashMap(); // Non-compliant
public CamundaApiResponse makerInput() { // Non-compliant
// ...
}
#### 2.3.5. Method should not be too complex

The *Cyclomatic Complexity* of methods SHOULD not exceed 10. The *Cognitive Complexity* [16] is a measure of how hard the control flow of a method is to understand, SHOULD be less than 15.

Complex code can perform poorly and will in any case be difficult to understand and therefore to maintain [17], [18] .

Figure 2: Branches and conditions will add Cyclomatic Complexity.Figure 3: Nested branches adds lots of Cognitive Complexity.

#### 2.3.6. Minimize scope of parameter

You SHOULD use proper type of parameter to protect encapsulation.
public List<String> values(VostroStampingData stampingData) {
String settlementMethod = stampingData
.getScbmlCashflowInstance()
.getSettlementMethod(); // Non-compliant with LoD
if (StringUtils.isBlank(settlementMethod)) {
return Arrays.asList(SETTLEMENT_TYPE_CASH, SETTLEMENT_TYPE_FEDWIRE);
}
return Arrays.asList(settlementMethod.toUpperCase(), SETTLEMENT_TYPE_FEDWIRE);
}
#### 2.3.7. Combine OOP with *functional-style* programming

Java supports *functional-style* programming since Java8. A combination of OOP with the benefits of functional programming can go a long way. This can lead to concise code that has fewer errors and is easier to understand, maintain, and parallelize. We gained quite a bit from the functional-style version, compared with the imperative-style version: [19]

- We avoided explicit mutation or reassignment of variables, which are often sources of bugs and result in code that’s hard to make concurrent
- The functional version can easily be parallelized.
- The code is more expressive.
- The functional-style version is more concise.
- The functional-style version is intuitive—code reads more like how we’d state the problem—and it’s easier to understand once we’re familiar with the syntax.

#### 2.3.8. Mitigate side effects of method

In general, any lasting effect that occurs in a function, not through its return value, is called a side effect.

Side effects can make code harder to reason about, test, and maintain. By minimizing side effects, code becomes more predictable, deterministic, and easier to understand. This is particularly important in functional programming, where immutability and pure functions are key principles.
public static <T> T fromXmlAndValidation(String xml, Class<T> clazz)
throws Exception {
T obj = clazz.getDeclaredConstructor().newInstance();
List<String> validationResult = new ArrayList<>();
// ...
if (!validationResult.isEmpty()) { // Non-compliant
PropertyDescriptor pd = Arrays.stream(propertyDescriptors)
.filter(p -> p.getName().equalsIgnoreCase("validationResult"))
.findAny().orElse(null);
if (pd != null) {
pd.getWriteMethod().invoke(obj, validationResult);
}
}
return obj;
}
To mitigate side effects, you could:

- Follow Single Responsibility Principle and seperate method responsibilities
- Use functional-style programming and leverage on immutability

The above case could be refacored by throwing exception with validation results:
public static <T> T fromXmlAndValidation(String xml, Class<T> clazz)
throws ValidationException {
T obj = clazz.getDeclaredConstructor().newInstance();
List<String> validationResult = new ArrayList<>();
// ...
if (!validationResult.isEmpty()) { // Compliant
throw new ValidationException(validationResult);
}
return obj;
}
### 2.4. Best Practices

#### 2.4.1. Use new language features of JDK17

You MAY use use new language features [20] that is generally available in *JDK17*, as they would simplify programming or bring improvment.

Note that you MUST NOT use any features that are still in preview or experimental.

#### 2.4.2. Remove unsed private method

`private` methods that are never executed are dead code: unnecessary, inoperative code that should be removed. Cleaning out dead code decreases the size of the maintained codebase, making it easier to understand the program and preventing bugs from being introduced [21].

Figure 4: Unused "private" methods should be removed.

#### 2.4.3. Remove unsed local variable

An unused local variable is a variable that has been declared but is not used anywhere in the block of code where it is defined. It is dead code, contributing to unnecessary complexity and leading to confusion when reading the code. Therefore, it should be removed from your code to maintain clarity and efficiency [22].

Figure 5: Variable is assigned but never accessed.

#### 2.4.4. Remove useless assignment

Dead stores refer to assignments made to local variables that are subsequently never used or immediately overwritten. Such assignments are unnecessary and don’t contribute to the functionality or clarity of the code. They may even negatively impact performance [23].
public void sendEbbs(@RequestBody MessageReq request) {
// useless assignment
Map<String, Object> headers = new HashMap();
headers = JSON.parseObject(request.getHeader());
}
#### 2.4.5. Don't commit debug code

Code that is used for debug purpose MUST NOT be committed into production.
@PostMapping(value = "/enrich")
@ResponseBody
public TradeStampingResponse enrich(@RequestBody TradeStampingRequest request, HttpServletResponse response) {
if (request.isScbml()) { // Non-compliant, it's for debug
request.setMessage(Base64Util.encoderMessage(request.getMessage()));
}
// ...
}
#### 2.4.6. Prefer constructor injection

@Component
public class AdditionalFieldsPropertiesHolder {
@Autowired // Non-compliant
FieldsXpathRepository repository;
}
Generally speaking, field injection is discouraged. It allows the creation of objects in an invalid state and makes testing more difficult. The dependencies are not explicit when instantiating a class that uses field injection.

Apart from that, field injection is not compatible with final fields. Keeping dependencies immutable where possible makes the code easier to understand, easing development and maintenance [24].

You SHOULD use constructor injection instead of field injection:
@Service
public class TradeVostroQueryService {
private final VostroService vostroService;

public TradeVostroQueryService(VostroService vostroService) {
this.vostroService = vostroService;
}
}
#### 2.4.7. Use text blocks for multi-line string

String settlementInstruction = "{ " + // Non-compliant
" \"Settlement_Instruction\": { " +
" \"Account\": { " +
" \"Beneficiary_Account_Name\": null, " +
" \"Beneficiary_BIC_code\": \"SBOSUS3QGLK\", " +
...@Query(""" // Compliant
select
csle.*
from
cashflow_stamping_legacy_exception csle,
cashflow_stamping cs,
stamped_vostro_account sva
where csle.ssi_exception = :ssiException
and csle.status = :status
and csle.cashflow_id = cs.cashflow_id
and sva.cashflow_stamping_id = cs.cashflow_id
and sva.ssi_id = :ssiId
and cs.updated_at >= current_date - 6""")
List<LegacyRatanException> findExceptionBySsiId(String ssiId, String ssiException, String status);
#### 2.4.8. Avoid using template engine for XML generation

We've noticed a practice that using thymeleaf template engine to generate outbound XMLs in some services:
<?xml version="1.0" encoding="UTF-8"?>
<MxPayMLResponse>
<sourceSystem>RATAN</sourceSystem>
<objectNature>cashflow</objectNature>
<timestamp th:text="${CashFlowACKInfo.acknowledgedTime}"></timestamp>
<sourceID th:text="${CashFlowACKInfo.nettingId}"></sourceID>
...
This approach has some disadvances:

- Not easy to do unit testing, because it generates a string and need to be unmarshalled in order to make assertions
- Requires Spring framework to inject the template engine, which is also tricky in unit test
- Would be hard to maintain and reuse when logic becomes complex
- Not possible to control pretty print
- Some information might loss if work with other XML parse library

Instead you SHOULD use a XML library to generate XML from java beans, eg. using jackson `XmlMapper`:
XmlMapper mapper = XmlMapper.builder()
.defaultPrettyPrinter(new DefaultXmlPrettyPrinter()
.withCustomNewLine("\n"))
.build();
mapper.writerWithDefaultPrettyPrinter()
.writeValueAsString(instruction);
### 2.5. Collections

#### 2.5.1. Prefer `Stream.toList()` over `Collectors.toList()`

The key problem is that .collect(Collectors.toList()) actually returns a mutable kind of List while in the majority of cases unmodifiable lists are preferred [25].
List<String> sendCashFlowIds = cashFlowStampingRequest.getLifecycleRequests()
.stream()
.map(StampedCashFlow::getCashflowId)
.collect(Collectors.toList()); // Non-compliant
"Stream.toList()" method SHOULD be used instead of "collectors" when unmodifiable list needed:
List<String> sendCashFlowIds = cashFlowStampingRequest.getLifecycleRequests()
.stream()
.map(StampedCashFlow::getCashflowId)
.toList(); // Compliant
#### 2.5.2. Prefer `isEmpty` to check if collection is empty

When you call `isEmpty()`, it clearly communicates the code’s intention, which is to check if the collection is empty. Using `size() == 0` for this purpose is less direct and makes the code slightly more complex. More over, `isEmpty()` has complexity of while `size()` is [26].
List<NostroAccount> nostroAccounts = getDefaultNostro(tradeCurrency);
if (nostroAccounts.size() < 1) { // Non-compliant
tradeCurrency.setNostroStampingResult(StampingResult.MISSING_NOSTRO_ERROR);
}
### 2.6. Concurrency & Safety

#### 2.6.1. Handle `InterruptedException` correctly

If an `InterruptedException` or a `ThreadDeath` error is not handled properly, the information that the thread was interrupted will be lost. Simply logging the exception is not sufficient and counts as ignoring it.

Failing to interrupt the thread (or to re-throw) risks delaying the thread shutdown and losing the information that the thread was interrupted - probably without finishing its task [27].
public void run () {
try {
/* ... */
} catch (InterruptedException e) {
LOGGER.log(Level.WARN, "Interrupted!", e);
/* Clean up whatever needs to be handled before interrupting */
Thread.currentThread().interrupt(); // Compliant
}
}
#### 2.6.2. Release resources in all cases

Some objects, such as open files, locks and manually allocated memory, behave as resources which require every acquire operation to be paired with a definite release. It is easy to overlook the vast possibilities for executions paths when exceptions are thrown. Resources should always be released promptly no matter what [28].

*try-with-resources* syntax SHOULD be used to guarantees that the resource in question will be closed [29].
try ( // Compliant
FileReader fr = new FileReader(fileName);
BufferedReader br = new BufferedReader(fr)
) {
return br.readLine();
}
catch (...) {}
If any lock mechanism is used, you SHOULD use `try..finally` to unlock it [30]:
public R locked(Action action) {
lock.lock();
try {
return action.run();
} finally {
lock.unlock(); // Compliant
}
}
### 2.7. Database

#### 2.7.1. Remember to update `update_at` field

When table contains `update_at` field, you MUST update it when saving:
CREATE TABLE IF NOT EXISTS maker_checker_request
// ...
created_at TIMESTAMP NOT NULL DEFAULT NOW(),
updated_at TIMESTAMP NOT NULL DEFAULT NOW()
)inbound.getCommonAttributes()
.setUpdatedAt(LocalDateTime.now()); // Compliant
mxgCashflowInboundRepository.save(inbound);
### 2.8. Comments

#### 2.8.1. Avoid JavaDoc comments for application code

Java uses JavaDoc to create document for code, it's useful when creating foundation libraries or frameworks that would be used by other people. However, the benefit of JavaDoc is not obvoius in the case of application codes, while it adds costs of maintainance.

You SHOULD NOT configure the IDE to generate "Noice comments" [31] like bellow:
This creator information is less helpful, developers SHOULD use git to track changes.

/**
 * @author JetBrains
 * @since Mar 8, 2022
*
*/
#### 2.8.2. Avoid commented-out code

You MUST NOT leave commented-out code in codebase, commented-out code distracts the focus from the actual executed code. It creates a noise that increases maintenance code. And because it is never executed, it quickly becomes out of date and invalid [31], [32].

Commented-out code should be deleted and can be retrieved from source control history if required.
// remove since now cn exception logic // Non-compliant, delete unused code
// case MULTI_NOSTRO: {
For some reason it's reasonable that some tests should be ignord but there's a good reason for keeping it in the codebase, use `@Disabled` (Junit5) or `@Ignore`(Junit4) instead of commenting tests out.
// @Test // Non-compliant, use @Disabled instead
// @Rollback(true)
// void testSaveAndFindMethod() {
// ...
#### 2.8.3. Add comments to explain if not obvious

Comments should describe things that aren’t obvious from the code [33].
if (businessVersion.equalsIgnoreCase("N/A")) {
// to bypass the url error // Compliant, it's not obvious
businessVersion = "NA";
}
If code is not stright forward to understand, you SHOULD either refactor it or add necessary comments to explain it:
public static int getScenarioNumber(VostroAccountFacade f) {
// Scenario 1 // Non-compliant, not helpful
if (f.hasLocalAgent() &&
!f.hasCustodian() &&
!f.hasCorrespondent()) {
return 1;
}
Note that for common business logics, it should be documented in ADO instead of code, make sure it could be tracked by ADO number in commit messages.

#### 2.8.4. Add @Deprecated for deprecated code

When a method or class is deprecated, you SHOULD add `@Deprecated` annotation to it. you MUST also add explaination in the comment why it's deprecated and what's the alternative.
/**
 * @deprecated
 * This api is no longer used in front end, will be removed in next release.
 * /
@Deprecated // Compliant
@Slf4j
@DgsComponent
@RequiredArgsConstructor
public class DashBoardFetcher {
// ...
}
### 2.9. Logging

#### 2.9.1. Log when request received

You MUST add log to record incoming request at the beginning of each request, unless you have a good reason to omit it. This will be helpful when diagnosing issues, especially in the case of interacting with other systems.
@PostMapping(value = "/bic/netting")
public ResponseEntity bicNettingCashFlow(
@RequestBody NettingRequestList nettingRequests) {
log.info("bic netting cashFlow starts, input: {}", nettingRequests);
...
#### 2.9.2. Log request and response of API call

You MUST log the request and response of API call to external systems.
log.info("QueryVostroAccount query string is:\n{}", queryString);
GraphQLResponse response = blockingDqslClient.executeQuery(queryString);
log.info("QueryVostroAccount response is: {}", response);
#### 2.9.3. Don't log large field

You MUST NOT log large field(such as encoded xml). This will potentially cause huge disk occupation of log system, and it's not friendly when diagnosing issues.

For assets with business value, save them in database instead.

#### 2.9.4. Use place holder in log

Concatenated arguments in a logging message lead to concatenation and therefore an evaluation, even if the logging level is too low to show a message [34].

This leads to a needless performance reduction.
// Non-compliant
log.info("get checker reject ssi open adhoc request " + request.toString());
Instead you SHOULD use string formatting placeholders `{}` and moving the concatenated parts to be parameters:
// Compliant
log.info("get checker reject ssi open adhoc request {}", request);
#### 2.9.5. Use business description as log marker

Often we need some unique log marker so that it could be easily searched in ELK. However, you SHOULD NOT use some strange symbols just in order to search:
// Non-compliant
log.info("+++++++++++ sendToMurex start : {} +++++++++++", LocalDateTime.now());
It looks ugly and not professional, and will soon become non-unique unless you add more strange symbols. Instead, you SHOULD use some sentense to describe what happened:
// Compliant
log.info("Start send b-ack to Murex: cashflow={}", cashflowId);
### 2.10. Testing

#### 2.10.1. Write unit test for each class

You SHOULD write unit test for each Java class in a corresponding ~Test class, and put test in the same package under test source directory.

Unit tests are necessary except for classes without logics, such as POJOs, constants, feign classes and framework generated classes, etc.

#### 2.10.2. Follow F.I.R.S.T principle when writing tests

You MUST follow F.I.R.S.T rules [31] to do unit testing：

- **Fast**: Tests should run fast. Usually, a unit test should finish in at most few seconds.
- **Independent**: Tests should not depend on each other, you could run each test independently and in any order.
- **Repeatable**: Tests should be repeatable in any environment.
- **Self-Validating**: Tests should either pass or fail.
- **Timely**: Write tests as earlier as you can and keep the code testable.

#### 2.10.3. Use Given-When-Then structure

You MUST follow *Given-When-Then* convension [35], [36] to structure a test:

- The **given** part describes the state of the world before you begin the behavior you're specifying in this scenario. You can think of it as the pre-conditions to the test.
- The **when** section is that behavior that you're specifying.
- Finally the **then** section describes the changes you expect due to the specified behavior.

Below is an example of test structure, note that `given` part is not always required, however, `when` and `then` MUST be included in a test case:
@Test
void test() {
// given
given(client.fetchCounterParties(List.of("10075222", "400803810")))
.willReturn(List.of());

// when
TradeStampingResponse result = service.handleStpStamping(instance);

// then
assertNotNull(result);
assertEquals(2, result.getSingleLegResult().size());
}
#### 2.10.4. Use assertions

A test case without assertions ensures only that no exceptions are thrown. Beyond basic runnability, it ensures nothing about the behavior of the code under test [37].

You MUST add assertions in test case in order to check the behavior. Without assertions, tests aren't self-validating.
@Test
void shouldReturnTradeDateStr_GivenIsNewProductAndPathExists() {
String scbml = TestUtil.getTestResource("5416524516.xml");
String tradeDate = mapping.map(scbml);

assertEquals("2024-10-16", tradeDate); // Compliant
}
Note that `System.out.println` is not assertion.
@Test
void testGenerateSwiftMessage {
String data = generator.generateMT();
System.out.println(data); // Non-compliant, use assertions instead
}
#### 2.10.5. Don't add `main` for testing

You MUST NOT add `main` method for testing purpose.
public class SomeUtil {
public static void main(String[] args) { // Non-compliant
// ...
}
}
#### 2.10.6. Ensure enough assertions

You MUST ensure enough assertions in the test. Depends on the specific functionality, you may need to add lines of assertions to cover necessary logics:
@Test
void shouldReturnTradeInstance_givenIsFixingRequest() {
TradeStampingRequest request = createRequest("fixing.xml", "spot");

ScbmlTradeInstance tradeInstance = factory.getTradeInstance(request);

assertEquals("4715530586.FIX", tradeInstance.getTradeId());
assertEquals("CASH", tradeInstance.getSettlementMethod());
assertEquals("fixing", tradeInstance.getProductType());
assertEquals("cfiCodeFromRequest", tradeInstance.getCfiCode());
assertEquals("trackingId", tradeInstance.getTrackingId());
assertEquals("400521212", tradeInstance.getParty1FmId());
assertEquals("400202766", tradeInstance.getParty2FmId());
assertEquals("CASH", tradeInstance.getSettlementType());
// ...
}
For example, the bellow service handle trade stamping and returns a trade instance, it's not enough to just verify the result is not null, you must also validate if fields of this instance are expected.
@Test
void test() {
TradeStampingResponse trade = service.handleStpStamping(instance);

assertNotNull(trade); // Non-compliant, not fully covered
}
#### 2.10.7. Test only one scenerio in one case

You shoukd only test one scenerio in a test, which is also known as *single concept per test* [31].

#### 2.10.8. Mock external dependencies

External dependencies MUST be mocked in unit tests. For example, you should not connect to a real database, or call other real API. Make sure tests can be executed in any environment including a local computer.

Figure 6: Test failed because database could not be connected.

#### 2.10.9. Add integration test for APIs

Integration testing [38] is a crucial part of the software development process, as it helps ensure that all individual components of an application work together seamlessly. When it comes to Spring Boot applications, integration testing becomes even more important due to the complexity of the framework. You SHOULD add integration test for each API to verify the behavior of it [39].

In SpringBoot, you can use `@SpringBootTest` to start the container :
@SpringBootTest
class IntegrationTest {
@Mockbean CashflowClient client;

@Test
void test() {
var e = new Cashflow(1L, "FM Forward");
given(client.queryById(1L))
.willReturn(Optional.of(e));

RestAssured
.when()
.get("/v1/cashflow/{id}", 1L)
.then()
.statusCode(200)
.body("id", equalTo(1L),
"type", equalTo("FM Forward"));
}
}
Note that you SHALL use `WebEnvironment.RANDOM_PORT` option to start an embedding web container, otherwise the web layer is mocked by spring [40] .

#### 2.10.10. Add integration test for async listeners

For async listeners, you don't need to start a web container, you can use the default `@WebEnvironment.MOCK` option to speed up.
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class IntegrationTest {
@Mockbean Repository repository;

@Autowired MessageListener listener;

@Test
void test() {
Acknowledgment mockAck = mock(Acknowledgment.class);
ConsumerRecord mockRecord = createMockKafkaMessage(xml);
// mock triggering Kafka message
listener.handleMessage(mockRecord, mockAck);

verify(mockAck).acknowledge();
// ...
}
}
#### 2.10.11. Use package visibility for tests

JUnit5 test classes and methods should generally have package visibility [41].
@Test
public void test() { // Non-compliant, remove public
// ...
}
#### 2.10.12. Add tests when fixing bug

You MUST try the best to to cover the missed cases when fixing bugs.
$ git show 2f73e83
#6164546: fixed a bug that default nostro is absent in generated scbml

...
+ @Test
+ void shouldReturnSellerWithDefaultNostroInstruction() {
...
## Bibliography

[1] “RFC2119:Key words for use in RFCs to Indicate Requirement
Levels.” [Online]. Available: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)
[2] “Alibaba Java Coding Guidelines.” [Online]. Available: [https://alibaba.github](https://alibaba.github).
io/Alibaba-Java-Coding-Guidelines/
[3] “java:S120 - Package names should comply with a naming
convention.” [Online]. Available: [https://sonarqube.vx.standardchartered](https://sonarqube.vx.standardchartered).
com/coding_rules?open=java%3AS120&rule_key=java%3AS120
[4] “java:S116 - Field names should comply with a naming
convention.” [Online]. Available: [https://sonarqube.vx.standardchartered](https://sonarqube.vx.standardchartered).
com/coding_rules?open=java%3AS116&rule_key=java%3AS116
[5] “java:S117 - Local variable and method parameter names should comply
with a naming convention.” [Online]. Available: [https://sonarqube.vx.standa](https://sonarqube.vx.standa)
[rdchartered.com/coding_rules?open=java%3AS117&rule_key=java%3AS117](http://rdchartered.com/coding_rules?open=java%3AS117&rule_key=java%3AS117)
[6] “Google code style - Naming.” [Online]. Available: [https://google.github.io/](https://google.github.io/)
styleguide/javaguide.html#s5-naming
[7] “java:S115 - Constant names should comply with a naming
convention.” [Online]. Available: [https://sonarqube.vx.standardchartered](https://sonarqube.vx.standardchartered).
com/coding_rules?open=java%3AS115&rule_key=java%3AS115
[8] “java:S119 - Type parameter names should comply with a naming
convention.” [Online]. Available: [https://sonarqube.vx.standardchartered](https://sonarqube.vx.standardchartered).
com/coding_rules?open=java%3AS119&rule_key=java%3AS119
[9] “java:S1444 - "public static" fields should be constant.” [Online]. Available:
[https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS](https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS)
1444&rule_key=java%3AS1444
[10] “java:S1128 - Unnecessary imports should be removed.” [Online]. Available:
[https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS](https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS)
1128&rule_key=java%3AS1128
[11] D. Thomas and A. Hunt, The Pragmatic Programmer: From Journeyman to
Master. Addison-Wesley Professional, 1999.
[12] R. C. Martin, Agile Software Development: Principles, Patterns, and Practices.
Pearson, 2002.
[13] “Law of Demeter: Principle of Least Knowledge.” [Online]. Available: https://
[www.khoury.northeastern.edu/home/lieber/LoD.html](http://www.khoury.northeastern.edu/home/lieber/LoD.html)
[14] “Controlling Access to Members of a Class.” [Online]. Available: [https://docs](https://docs).
[oracle.com/javase/tutorial/java/javaOO/accesscontrol.html](http://oracle.com/javase/tutorial/java/javaOO/accesscontrol.html)
[15] “java:S3740 - Raw types should not be used.” [Online]. Available: https://
[sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS3740&](http://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS3740&)
rule_key=java%3AS3740
[16] G. A. Campbell, Cognitive Complexity a new way of measuring
understandability. 2023.
[17] “java:S1541 - Methods should not be too complex.” [Online]. Available:
[https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS](https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS)
1541&rule_key=java%3AS1541
[18] “java:S3776 - "Cognitive Complexity of methods should not be too
high.” [Online]. Available: [https://sonarqube.vx.standardchartered.com/](https://sonarqube.vx.standardchartered.com/)
coding_rules?open=java%3AS3776&rule_key=java%3AS3776
[19] V. Subramaniam, Functional Programming in Java. Pragmatic Bookshelf,
2023.
[20] “A categorized list of all Java and JVM features since JDK 8 to 21.” [Online].
Available: [https://advancedweb.hu/a-categorized-list-of-all-java-and-jvmfeatures-](https://advancedweb.hu/a-categorized-list-of-all-java-and-jvmfeatures-)
since-jdk-8-to-21/
[21] “java:S1144 - Unused "private" methods should be removed.” [Online].
Available: [https://sonarqube.vx.standardchartered.com/coding_rules?open=](https://sonarqube.vx.standardchartered.com/coding_rules?open=)
java%3AS1144&rule_key=java%3AS1144
[22] “java:S1481 - Unused assignments should be removed.” [Online]. Available:
[https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS](https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS)
1481&rule_key=java%3AS1481
[23] “java:S1854 - Unused assignments should be removed.” [Online]. Available:
[https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS](https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS)
1854&rule_key=java%3AS1854
[24] “java:S6813 - Avoid field dependency injection.” [Online]. Available: https://
[sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS6813&](http://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS6813&)
rule_key=java%3AS6813
[25] “java:S6204 - "Stream.toList()" method should be used instead of
"collectors" when unmodifiable list needed.” [Online]. Available: https://
[sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS6204&](http://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS6204&)
rule_key=java%3AS6204
[26] “java:S1155 - "Collection.isEmpty()" should be used to test for
emptiness.” [Online]. Available: [https://sonarqube.vx.standardchartered](https://sonarqube.vx.standardchartered).
com/coding_rules?open=java%3AS1155&rule_key=java%3AS1155
[27] “java:S2142 - "InterruptedException" and "ThreadDeath" should not be
ignored.” [Online]. Available: [https://sonarqube.vx.standardchartered.com/](https://sonarqube.vx.standardchartered.com/)
coding_rules?open=java%3AS2142&rule_key=java%3AS2142
23/24
INTERNAL
[28] “Secure Coding Guidelines for Java SE.” [Online]. Available: [https://www](https://www).
[oracle.com/java/technologies/javase/seccodeguide.html](http://oracle.com/java/technologies/javase/seccodeguide.html)
[29] “java:S2093 - Try-with-resources should be used.” [Online]. Available:
[https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS](https://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS)
2093&rule_key=java%3AS2093
[30] B. Goetz, Java Concurrency in Practice. Addison-Wesley Professional, 2006.
[31] R. C. Martin, Clean Code. Pearson, 2008.
[32] “java:S125 - Sections of code should not be commented out.” [Online].
Available: [https://sonarqube.vx.standardchartered.com/coding_rules?open=](https://sonarqube.vx.standardchartered.com/coding_rules?open=)
java%3AS125&rule_key=java%3AS125
[33] J. Ousterhout, A Philosophy of Software Design. 2021.
[34] “java:S2629 - "Preconditions" and logging arguments should not require
evaluation.” [Online]. Available: [https://sonarqube.vx.standardchartered](https://sonarqube.vx.standardchartered).
com/coding_rules?open=java%3AS2629&rule_key=java%3AS2629
[35] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns: Elements of
Reusable Object-Oriented Software. Addison-Wesley Professional, 1994.
[36] “Given When Then.” [Online]. Available: [https://martinfowler.com/bliki/](https://martinfowler.com/bliki/)
GivenWhenThen.html
[37] “java:S2699 - Tests should include assertions.” [Online]. Available: https://
[sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS2699&](http://sonarqube.vx.standardchartered.com/coding_rules?open=java%3AS2699&)
rule_key=java%3AS2699
[38] M. Fowler, “Integration Test.” [Online]. Available: [https://martinfowler.com/](https://martinfowler.com/)
bliki/IntegrationTest.html
[39] “Testing Strategies in a Microservice Architecture.” [Online]. Available:
[https://martinfowler.com/articles/microservice-testing/](https://martinfowler.com/articles/microservice-testing/)
[40] “Testing Spring Boot Applications.” [Online]. Available: [https://docs.spring](https://docs.spring).
io/spring-boot/reference/testing/spring-boot-applications.html
[41] “java:S5786 - JUnit5 test classes and methods should have default package
visibility.” [Online]. Available: [https://sonarqube.vx.standardchartered.com/](https://sonarqube.vx.standardchartered.com/)
coding_rules?open=java%3AS5786&rule_key=java%3AS5786