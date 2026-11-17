# 1. DRL files hot deployment & refreshment

Drools doesn't support the hot deployment of DRL rule files. However, Drools provides the API to enable developers to build everything during runtime environment, which means a rule can be created and compiled dynamically in a programmatic way and we don't need to restart the application.

## 1.1 KIE (Knowledge is Everything) Core Components

1. ***org.kie.api.runtime.KieSession: ***KieSession is the most common way to interact with the rule engine. A KieSession allows the application to establish an iterative conversation with the engine. After the application finishes using the session, though, it must call the* dispose () *method to free the resources and used memory.
2. ***org.kie.api.KieBase:*** KieBase is a repository of all the application's knowledge definitions. It will contain rules, processes, functions and type models. The KieBase does not contain the runtime data, instead sessions are created from KieBase in which data can be inserted and processes instances started.
3. ***org.kie.api.builder.KieModule:*** A KieModule is a container of all resources necessary to define a set of KieBase. Like pom.xml defining its Release Id, a kmodule.xml file declaring the KieBase names and configurations together with all KieSession that can be created from them and all the files necessary to build the KieBase themselves.
4. ***org.kie.api.builder.KieFileSystem: ***like all other Kie core components*** ***you can*** ***obtain an instance of the KieFileSystem from the KieServices.

## 1.2 Implementation

- Preparing the rule template as below, it will be merged with the data to generate the real rule file.

```text
package org.example.drools

import java.util.Map;
import org.example.drools.model.SuppressionResponse;

global java.util.List allRes;

dialect "mvel"

<#list rules as rule>
rule "rule_${rule.id}"
  when
    $m : Map(${rule.rule})
  then
    SuppressionResponse res = new SuppressionResponse(${rule.id}, "${rule.reason}");
    allRes.add(res);
end

</#list>
```

- Using the KieHelper class to compile the generated rule file, and then create a KieSession to insert the runtime data and fire the rules if matched.

```java
public List<SuppressionResponse> checkRules(Map<String, Object> fact) throws Exception {
	// Generated the drl file based on the loading rules
    Template tpl = tplConfig.getTemplate(SUPPRESSION_RULE_TPL);

    Map<String, List<SuppressionRule>> mergedRoot = new HashMap<>();
    mergedRoot.put(MERGE_DATA_ROOT, listAllRules());

    Writer out = new StringWriter();
    tpl.process(mergedRoot, out);
    log.info("generated rule.drl file: %n {}", out);

    // Add generated rule content into KieSystem
    KieHelper kieHelper = new KieHelper();
    kieHelper.addContent(out.toString(), ResourceType.DRL);

    // Verify the syntax of rule files
    Results results = kieHelper.verify();
    if (results.hasMessages(Message.Level.WARNING, Message.Level.ERROR)) {
    	List<Message> messages = results.getMessages(Message.Level.WARNING, Message.Level.ERROR);
        for (Message message : messages) {
        	throw new RuntimeException("Rule syntax errors: " + message.getText());
        }
    }

    // Build the resources necessary for creating a KieBase
    KieBaseConfiguration config = kieHelper.ks.newKieBaseConfiguration();
    KieBase kieBase = kieHelper.build(config);

    // Create an iterative conversion called KieSession in Drools
    KieSession kieSession = kieBase.newKieSession();
    List<SuppressionResponse> allRes = new ArrayList<>();
    try {
    	// Set global variable
        kieSession.setGlobal(ALL_SUPPRESSION_RES, allRes);

        // Insert the fact
        kieSession.insert(fact);

        // Fire the rules
        kieSession.fireAllRules();
    }
    finally {
        if (kieSession != null) {
        	kieSession.dispose();
        }
    }
    return allRes;
}
```

- Open Issues - MVEL doesn't support the Null-Safe Bean Property Navigation. - Compiling and verifying the rule files during runtime may be a time-consuming activity.

# 2. Supported operators in DRL pattern constraints

DRL supports standard Java semantics for operators in pattern constraints, with some exceptions and with some additional operators that are unique in DRL. The following list summarizes the operators that are handled differently in DRL constraints than in standard Java semantics or that are unique in DRL constraints.

| Operator | Description |
| --- | --- |
| >, >=, <, <= | - For ***Date ***field, the operator < means before. - For ***String ***field, the operator < means alphabetically before. |
| ==, != | - Null-safe equality / non-equality operators. - Use these operators as equals() and !equals() methods in constraints. |
| &&, || | Use these operators to create an abbreviated combined relation condition that adds more than one restriction on a field. You can group constraints with parentheses () to create a recursive syntax pattern. For example: *// Simple abbreviated combined relation condition using a single `&&`: * Person (age > 30 && < 40) *// Complex abbreviated combined relation using groupings: * Person (age ((> 30 && < 40) || (> 20 && < 25))) *// Mixing abbreviated combined relation with constraint connectives: * Person (age > 30 && < 40 || location == "london") |
| matches, not matches | Indicate that a field matches or does not matches a specified java regular expression. For example: Person( country matches "(USA)?\\S*UK" ); Person( country not matches "(USA)?\\S*UK"); |
| contains, not contains | - Verify whether a field that is an Array or a Collection contains or does not contain a specified value. - These operators apply to Array or Collection properties, but you can also use these operators in place of String.contains() and !String.contains() constraints check. |
| memberOf, not memberOf | Use these operators to verify whether a field is a member of or is not a member of an Array or a Collection that is defined as a variable. |
| in, notin | Use these operators to specify more than one possible value to match in a constraint (compound value restriction). This functionality of compound value restriction is supported only in the `in` and `not in` operators. |

# 3. Eval function in DRL pattern constraints

The conditional element eval is essentially a catch-all which allows any semantic code (that returns a primitive Boolean) to be executed. This code can refer to variables that were bound in the conditions of the rule and functions in the rule package. The below is an example for http calling:

```text
import org.example.drools.model.Customer;
import org.example.drools.model.CustomerType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

function Boolean httpCall(Customer c) {
    RestTemplate restTemplate = new RestTemplate();

    try {
        ResponseEntity<CustomerType> res = restTemplate.getForEntity("http://localhost:9999/customers/" + c.getName(), CustomerType.class);
        if (res.getStatusCode().is2xxSuccessful()) {
            return res.getBody() == CustomerType.LOYAL;
        }
        return false;
    }
    catch(Exception e) {
        System.err.println(e);
        return false;
    }
}

rule "http calling tests01"
    when
        $c : Customer()
        eval(httpCall($c))
    then
        System.out.println($c.getName() + " is LOYAL customer");
end
```

```java
import org.example.drools.model.Customer;
import org.kie.api.KieServices;
import org.kie.api.builder.KieBuilder;
import org.kie.api.builder.KieFileSystem;
import org.kie.api.builder.KieModule;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.kie.internal.io.ResourceFactory;

public class HttpCallTests {

    public static void main(String[] args) {
        KieServices kieServices = KieServices.Factory.get();

        KieFileSystem kieFileSystem = kieServices.newKieFileSystem();
        kieFileSystem.write(ResourceFactory.newClassPathResource("rules/httpcall.drl", "utf-8"));

        KieBuilder kieBuilder = kieServices.newKieBuilder(kieFileSystem);
        kieBuilder.buildAll();

        KieModule kieModule = kieBuilder.getKieModule();
        KieContainer kieContainer = kieServices.newKieContainer(kieModule.getReleaseId());

        KieSession kieSession = kieContainer.newKieSession();

        Customer customer = new Customer("jonny");
        kieSession.insert(customer);

        kieSession.fireAllRules();
        kieSession.dispose();
    }
}
```