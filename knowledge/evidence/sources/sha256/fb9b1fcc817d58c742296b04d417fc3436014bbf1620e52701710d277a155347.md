# 1. Introduction

Within the mission-critical applications, the process of maintaining business logic within the source code can become too complicated. Rule engines make it easy to separate the business logic from the source code. We may view a rule engine is a sophisticated if/then statement interpreted.

Image a rule engine as a system which takes data and rules as input, it will apply those data on the data and give us and output based on the rule definition.

# 2. Rule Engine for Java

In this section, we'll go through some popular rule engines for Java. In the Java world, most of the rules engines libraries implement JSR94 standard known as [Java Rule API Engine](https://jcp.org/en/jsr/detail?id=94).

| Name | Latest Version | Release Date | GitHub Stars |
| --- | --- | --- | --- |
| Drools | 8.41.0.Final | Jul 6, 2023 | 5.3K |
| Easy Rules | 4.1.0 | Dec 7, 2020 | 4.5K |
| LiteFlow | 2.9.7 | Jul 3, 2023 | 2K |

## 2.1 [Drools](https://www.drools.org/)

Drools is a Business Rules Management System (BRMS) solution. It provides:

- A core Business Rules Engine
- A web authoring and rules management application (Drools Workbench)
- Full runtime support for Decision Model and Notation (DMN) models
- An eclipse IDE plugin for development

If you want to read more, the document to Drools is available [here](https://docs.drools.org/7.69.0.Final/drools-docs/html_single/index.html).

### 2.1.1 Drools Basics

We are going to look at basic concepts of Drools:

- **Facts - **represent data that serves as input for rules.
- **Working Memory - **a storage with Facts, where they are used for pattern matching and can be modified, inserted and removed.
- **Rule - **represents a single rule which associates Facts with matching actions. It can be written in Drools Rule Language in the .drl files.
- **Pattern Matcher -** match all the rules with the Facts inserted into working memory.
- **Agenda -** the actions will be taken if some rules are fired.

### 2.1.2 Drools Rule Language

DRL (Drools Rule Language) rules are business rules that you define directly in .drl text files. A sample of DRL files is shown as below:

```text
package

import

function // Optional

query // Optional

declare // Optional

global // Optional

rule "rule name"
	// Attributes
	when
		// Conditions
	then
		// Actions
end

rule "rule2 name"

...


```

A DRL file can contain single or multiple rules, queries, and functions, and can define resource declarations such as imports, globals, and attributes that are assigned and used by your rules and queries. Each rule must have a unique name within the rule package.

As for the details to DRL, please refer to the following link [Drools Rule Language Reference](https://docs.drools.org/7.69.0.Final/drools-docs/html_single/index.html#drl-rules-con_drl-rules).

### 2.1.3 Drools Example

Here is a simple example of how the Drools works by using a DRL file containing the business rules. First, let's import its dependencies which reply on ***org.kie.kie-spring*** module:

```text
<properties>
	<drools.version>7.69.0.Final</drools.version>
</properties>

<dependencies>
	<dependency>
		<groupId>org.kie</groupId>
    	<artifactId>kie-spring</artifactId>
    	<version>${drools.version}</version>
	</dependency>
</dependencies>
```

Next, we need to set the *KieContainer *which is a placeholder for all the *KieBase *for particular *KieModule*. *KieContainer *is built with the help of other beans including *KieFileSystem*, *KieModule*, and *KieBuilder*.

```java
@Configuration
public class DroolsConfig {
    private static final String RULE_PATH = "rules/";
    private static final String SIMPLE_RULES_DRL = RULE_PATH + "simple.drl";
    private static final KieServices kieServices = KieServices.Factory.get();

    private Resource[] getRuleFiles() throws IOException {
        ResourcePatternResolver resourcePatternResolver = new PathMatchingResourcePatternResolver();
        return resourcePatternResolver.getResources("classpath*:" + RULE_PATH + "**/*.*");
    }

    @Bean
    public KieContainer kieContainer() throws IOException {
        KieFileSystem kieFileSystem = kieServices.newKieFileSystem();
        for (Resource file : getRuleFiles()) {
            kieFileSystem
                    .write(ResourceFactory.newClassPathResource(RULE_PATH + file.getFilename(), "UTF-8"));
        }
        kieFileSystem.write(ResourceFactory.newClassPathResource(SIMPLE_RULES_DRL, "UTF-8"));

        KieBuilder kieBuilder = kieServices.newKieBuilder(kieFileSystem);
        kieBuilder.buildAll();

        KieModule kieModule = kieBuilder.getKieModule();
        return kieServices.newKieContainer(kieModule.getReleaseId());
    }
}
```

Now, a OrderRequest POJO:

```java
package org.example.drools.model;

import lombok.Data;

@Data
public class OrderRequest {
    private String customerNumber;
    private Integer age;
    private Integer amount;
    private CustomerType customerType;
}



```

And an enum that will represent the customer type:

```java
package org.example.drools.model;

public enum CustomerType {
    LOYAL, NEW, DISSATISFIED;

    public String getValue() {
        return this.toString();
    }
}
```

Now that we're done with the setup, let's implement the business rules. Simply put, the Drools rules contains all business rules. ***A rule includes a When-Then construct***, here the *When *section lists the condition to be checked, and *Then *section lists the action to be taken if the condition is met:

```text
import org.example.drools.model.OrderRequest;
import org.example.drools.model.CustomerType;

global org.example.drools.model.OrderDiscount orderDiscount;

dialect "mvel"

rule "Age based discount"
    when
        OrderRequest(age < 20 || age > 50)
    then
        System.out.println("==========Adding 10% discount for Kids/senior customer==========");
        orderDiscount.setDiscount(orderDiscount.getDiscount() + 10);
end

rule "Customer type base discount - Local customer"
    when
        OrderRequest(customerType.getValue == "LOYAL")
    then
        System.out.println("============Adding %5 discount for LOYAL customer=========");
        orderDiscount.setDiscount(orderDiscount.getDiscount() + 5);
end

rule "Customer type based discount - others"
    when
        OrderRequest(customerType.getValue != "LOYAL")
    then
        System.out.println("============Adding %5 discount for LOYAL customer=========");
        orderDiscount.setDiscount(orderDiscount.getDiscount() + 3);
end

rule "Amount based discount"
    when
        OrderRequest(amount > 1000L)
    then
        System.out.println("============Adding %5 discount for amount more than $1000=========");
        orderDiscount.setDiscount(orderDiscount.getDiscount() + 5);
end
```

Finally, this rule can be fired by inserting the *OrderRequest *facts in *KieSession*:

```java
@Test
public void orderRequestTest() {
	OrderDiscount orderDiscount = new OrderDiscount();

    KieSession kieSession = kieContainer.newKieSession();
    kieSession.setGlobal("orderDiscount", orderDiscount);

    OrderRequest orderRequest = new OrderRequest();
    orderRequest.setCustomerNumber("A0000001");
    orderRequest.setAge(55);
    orderRequest.setAmount(1005);
    orderRequest.setCustomerType(CustomerType.LOYAL);

    kieSession.insert(orderRequest);
    kieSession.fireAllRules();
    kieSession.dispose();

    assertThat(orderDiscount.getDiscount()).isEqualTo(20);
}
```

### 2.1.3 Decision Model and Notation (DMN)

Decision Model and Notation (DMN) is a standard established by Object Management for describing and modeling operational decisions. DMN define an XML schema that enable DMN models to be shared between DMN-compliant platforms and across organizations so that business analysts and business rules developers can collaborate in designing and implementing DMN decision services.

A decision requirement diagram (DRD) is a visual representation of your DMN model. Use the DMN Designer in Business Central to define the decision logic of the DRD components.

### 2.1.4 Pros & Cons

1) **Pros**

- Drools is well integrated with programing language Java and supports spring integration as well.
- Fast, good performance rule engine based on the rete algorithm.
- Provide the IDE plugins for core developments, e.g., rule syntax pre-check, pre-compile and auto-completion etc. However, it seems only support Eclipse.
- Can be easily integrated with workflow engine, such as JBPM.
- Actively community support and the latest version 8.41.0. Final has been released on Jul 6, 2023.

2) **Cons**

- Learning curve is high for beginners.
- May need to take time and efforts to deeply understand the Drools Rule Language before writing the business rules.
- Debugging and troubleshooting may be difficult.

## 2.2 [Easy Rules](https://github.com/j-easy/easy-rules)

Easy Rules is a simple Java rules engine providing a lightweight and POJO based framework to define business rules. In contrast to the most traditional rules engines, easy rules recommend you using annotation-based classes and methods for injecting business logic into the application.

- Lightweight library and easy to learn API.
- POJO based development with and annotation programming model.
- Useful abstractions to define business rules and apply them easily with Java.
- The ability to define rules using an Expression Language (Like MVEL, SpEL and JEXL).

### 2.2.1 Easy Rules Basics

Easy Rules can be handy for developers to create and maintain applications with business logic that's entirely separated from the application itself. The below example is shown to define the rules in a declarative way using annotations:

```java
@Rule(name = "Rule for amount based discount", description = "", priority = 4)
public class AmountBasedRule {

    @Condition
    public boolean when(@Fact("orderRequest")OrderRequest orderRequest) {
        return orderRequest.getAmount() > 1000L;
    }

    @Action
    public void then(@Fact("orderDiscount")OrderDiscount orderDiscount) {
        System.out.println("Adding %5 discount for amount more than 1000");
        orderDiscount.setDiscount(orderDiscount.getDiscount() + 5);
    }
}
```

Or in a programmatic way with a fluent API:

```java
MVELRule ageBasedRule = new MVELRule()
	.name("age based discount")
    .priority(1)
    .when("orderRequest.age < 20 || orderRequest.age > 50")
    .then("System.out.println(\"Adding 10% discount for Kids/senior customer\");")
    .then("orderDiscount.setDiscount(orderDiscount.discount + 10);");
```

Or using a rule descriptor, like in the following *rule01.yml* example file:

```text
name: "Customer type base discount"
description: ""
priority: 2
condition: "orderRequest.customerType.getValue == \"LOYAL\""
actions:
  - "System.out.println(\"Adding %5 discount for LOYAL customer\");"
  - "orderDiscount.setDiscount(orderDiscount.discount + 5);"
```

### 2.2.2 Easy Rules Example

Here we provide the "Calculate the discount based on the Order Request" example. Let's import the required dependencies based on the easy-rules core modules:

```text
<properties>
	<easy-rules.version>4.1.0</easy-rules.version>
</properties>

<dependencies>
     <dependency>
     	<groupId>org.jeasy</groupId>
        <artifactId>easy-rules-core</artifactId>
        <version>${easy-rules.version}</version>
     </dependency>
</dependencies>
```

Next, we create a Launcher class to define the rules, and load all the rules into rule engine:

```java
package org.example.easy;

import org.example.easy.model.CustomerType;
import org.example.easy.model.OrderDiscount;
import org.example.easy.model.OrderRequest;
import org.example.easy.rules.AmountBasedRule;
import org.jeasy.rules.api.Facts;
import org.jeasy.rules.api.Rule;
import org.jeasy.rules.api.Rules;
import org.jeasy.rules.api.RulesEngine;
import org.jeasy.rules.core.DefaultRulesEngine;
import org.jeasy.rules.mvel.MVELRule;
import org.jeasy.rules.mvel.MVELRuleFactory;
import org.jeasy.rules.support.reader.YamlRuleDefinitionReader;

import java.io.InputStreamReader;
import java.io.Reader;

public class Launcher {

    public static void registerNewYamlRule(MVELRuleFactory ruleFactory, Rules rules, String yamlFile) throws Exception {
        Reader rulesReader = new InputStreamReader(Launcher.class.getResourceAsStream(yamlFile));
        Rule yamlRule = ruleFactory.createRule(rulesReader);
        rules.register(yamlRule);
    }

    public static void main(String[] args) throws Exception {
        // Create facts
        OrderRequest orderRequest = new OrderRequest();
        orderRequest.setCustomerNumber("A0000001");
        orderRequest.setAge(55);

        orderRequest.setAmount(1005);
        orderRequest.setCustomerType(CustomerType.LOYAL);
        OrderDiscount orderDiscount = new OrderDiscount();

        Facts facts = new Facts();
        facts.put("orderRequest", orderRequest);
        facts.put("orderDiscount", orderDiscount);

        // Create a rule set
        Rules rules = new Rules();

		// Define the rule with fluent API
        MVELRule ageBasedRule = new MVELRule()
                .name("age based discount")
                .priority(1)
                .when("orderRequest.age < 20 || orderRequest.age > 50")
                .then("System.out.println(\"Adding 10% discount for Kids/senior customer\");")
                .then("orderDiscount.setDiscount(orderDiscount.discount + 10);");
        rules.register(ageBasedRule);

	  	// Using rule descriptor with yaml file 
        MVELRuleFactory ruleFactory = new MVELRuleFactory(new YamlRuleDefinitionReader());
        registerNewYamlRule(ruleFactory, rules, "/rules/rule02.yml");
        registerNewYamlRule(ruleFactory, rules, "/rules/rule03.yml");
		
		// Using rule annotations
        rules.register(new AmountBasedRule());

        // Create a default rules engine and fire rules on know facts
        RulesEngine rulesEngine = new DefaultRulesEngine();
        rulesEngine.fire(rules, facts);

        System.out.println(orderDiscount.getDiscount() + "% discount for customer " + orderRequest.getCustomerNumber());
    }
}


```

### 2.2.3 Pros & Cons

1) **Pros**

- Easy Rules can be handy for developer to define the business logic with the straightforward API.
- Easy to debugger and troubleshooting for POJO based and annotation programming model.
- Minimize required third-party library dependencies, which means it can be easily integrated with another development framework, such as Spring Boot

2) **Cons**

- Easy Rules doesn't implement the JSR94 standard, and the business logic has to be coded straight to Java code.
- The latest version 4.1.0 was released three years ago, there're no changes or fixing since Dec 7, 2020.
- Lacking success cases to prove how it can support the complex business scenarios.

## 2.3 [LiteFlow](https://liteflow.yomahub.com/en/)

LiteFlow is a lightweight, fast and *component-based* rule engine. The core features of LiteFlow are shown as below:

- Component based; each business rule will be treated as a separate component in LiteFlow.
- Support nested rules, you can use the multiple-layer nested rules and orchestrate the rules to fulfil the complex business logics.
- Well integrated with SpringBoot, support SpringBoot 2.x through the latest version SpringBoot 3.x.
- Support various script languages, e.g., Groovy, Javascript, QLExpress, Python, Lua, and Aviator.
- Built-in monitoring to let you identify the time-consuming steps.
- Support external rules storage such as databases, nacos, zookeeper and etcd.

### 2.3.1 LiteFlow Basics

Components play an important part in LiteFlow framework, the most common component type is *NodeComponent. *Here's an example to demonstrate how do we use the *NodeComponent *to implement a* when/action *business logic in LiteFlow:

```java
@Component("ageBased")
public class AgeBasedCmp extends NodeComponent {

	// Checked whether the rule is matched
    @Override
    public boolean isAccess() {
        OrderContext context = this.getContextBean(OrderContext.class);
        OrderRequest request = context.getRequest();

        return request != null && (request.getAge() < 20 || request.getAge() > 50);
    }

	// The action will be taken when the isAccess() return true
    @Override
    public void process() throws Exception {
        System.out.println("Adding 10% discount for Kids/Senior customer");

        OrderContext context = this.getContextBean(OrderContext.class);
        OrderDiscount discount = context.getDiscount();
        discount.addDiscount(10);
    }
}
```

In addition, there are various component types available in LiteFlow framework, such as *SwitchComponent*, *IfComponent*, *LoopComponent *and *BreakComponent*. Hence, we can use these components to implement the complex business logic.

Next, the important part of LiteFlow framework we need to understand is the *flow. *A *flow *is responsible to ***orchestrate ***the components you've developed to fulfil the complicate business flow in real world. Here're some *flow *examples:

- **Serial Mode** ```yml <chain name="chain1"> THEN(a, b, c, d); </chain> ``` ![FlowInSerialMode.PNG](attachments/FlowInSerialMode.PNG)
- **Parallel Mode** ```yml <chain name="chain1"> THEN( a, WHEN(b, c, d), e ); </chain> ``` **![FlowInParallelMode.PNG](attachments/FlowInParallelMode.PNG) **
- **IF Mode** ```yml <chain name="chain1"> THEN( IF(x, a, b), c ); </chain> ``` ![FlowInIfMode.PNG](attachments/FlowInIfMode.PNG)
- **Complex Example** ```yml <chain name="chain1"> THEN( A, WHEN( THEN(B, C), THEN(D, E, F), THEN( SWITCH(G).to( THEN(H, I, WHEN(J, K)).id("t1"), THEN(L, M).id("t2") ), N ) ), Z ); </chain> ``` ![ComplexExample.PNG](attachments/ComplexExample.PNG)

If you would like to read more about the flow modes, please refer to the [link](https://liteflow.yomahub.com/en/pages/16eca9/) here.

### 2.3.2 LiteFlow Example

Please refer to the concrete example of LiteFlow.

### 2.3.3 Pros & Cons

1) **Pros**

- Handy for developers and provide IDEA plugin for core developments.
- Easy to debugger and troubleshooting since most business logics are encouraged to implement in code.
- Fully support Java and Spring Boot framework.
- Support rules hot deployment / refreshment.

2)** Cons**

- LiteFlow is not compliance with Java standard Rule Engine API, some terms have different meanings in contrast to other JSR94 compatible Rule Engines.
- LiteFlow is more suite for the complex business flow orchestration, rather than isolate the business logics from the codes.

# 3. Conclusion

In conclusion, we propose using Drools as the rule engine solution as it is the most mature open-source solution with the powerful and rich features.

**
**

**
**