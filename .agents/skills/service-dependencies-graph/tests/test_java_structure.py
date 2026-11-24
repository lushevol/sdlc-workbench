"""Check Java structure, binding evidence, ambiguity, and value exclusion."""
from pathlib import Path
import json
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name("_support.py")))["load_tool"]
structure = load_tool("extract_java_structure")
build_graph = load_tool("build_graph")


class JavaStructureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-java-structure-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.repo = self.workspace / "repos" / "app"
        self.write("pom.xml", "<project><groupId>fixture</groupId><artifactId>app</artifactId><version>1</version></project>")

    def write(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def java(self, name, source):
        return self.write("src/main/java/" + name + ".java", source)

    def test_config_roles_bindings_reads_profiles_and_values_are_separate(self):
        self.java("Props", '''package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Profile;
import lombok.Data;
@Data @Profile("dev") @ConfigurationProperties(prefix="app.auth")
class Props { private String host = "DO_NOT_RETAIN_JAVA"; private String password; }
''')
        self.java("WorkerImpl", '''package app;
import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
@Service @RequiredArgsConstructor class WorkerImpl {
  private final Props props;
  String endpoint(){ return props.getHost(); }
}
''')
        self.write("src/main/resources/application-dev.yml", "app:\n  auth:\n    host: DO_NOT_RETAIN_YAML\n    password: ${AUTH_SECRET:DO_NOT_RETAIN_DEFAULT}\n")
        result = structure.extract(self.repo)
        self.assertEqual(result["statistics"]["configuration_classes"], 1)
        self.assertEqual(result["statistics"]["configuration_bindings"], 2)
        self.assertEqual([row["key"] for row in result["configuration_reads"]], ["app.auth.host"])
        read = result["configuration_reads"][0]
        source = (self.repo / read["path"]).read_bytes()
        self.assertEqual(source[read["source_start_byte"]:read["source_end_byte"]], b"props.getHost()")
        self.assertEqual({row["role"] for row in result["types"]}, {"CONFIGURATION_PROPERTIES", "APPLICATION_SERVICE"})
        self.assertTrue(all(row["profile"] == "dev" for row in result["configuration_keys"]))
        self.assertEqual([row["key"] for row in result["configuration_references"]], ["AUTH_SECRET"])
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(result))
        self.assertTrue(any(row["relationship"] == "INJECTS" for row in result["type_dependencies"]))

    def test_value_and_environment_reads_keep_only_keys_and_account_for_dynamic_keys(self):
        self.java("Reader", '''package app;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
class Reader {
 @Value("${db.password:DO_NOT_RETAIN_DEFAULT}") private String password;
 private Environment env;
 String read(String dynamic){
  env.getProperty("api.endpoint", "DO_NOT_RETAIN_FALLBACK");
  env.getRequiredProperty(dynamic);
  return password;
 }
}
''')
        result = structure.extract(self.repo)
        self.assertEqual({row["key"] for row in result["configuration_reads"]}, {"db.password", "api.endpoint"})
        unknown = [row for row in result["ledger"] if row["family"] == "configuration_read" and row["disposition"] == "UNRESOLVED"]
        self.assertEqual(len(unknown), 1)
        self.assertEqual(unknown[0]["reason"], "UNRESOLVED_CONFIGURATION_READ")
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(result))

    def test_local_configuration_getter_keeps_implicit_and_explicit_receiver_context(self):
        self.java("Props", '''package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
@ConfigurationProperties("app") class Props {
 private String host;
 String getHost(){ return host; }
 String implicit(){ return getHost(); }
 String explicit(){ return this.getHost(); }
}
''')
        result = structure.extract(self.repo)
        reads = [row for row in result["configuration_reads"] if row["read_kind"] == "PROPERTIES_GETTER"]
        self.assertEqual({row["source_method"] for row in reads}, {"implicit", "explicit"})
        self.assertEqual({row["key"] for row in reads}, {"app.host"})
        self.assertTrue(all(row["receiver_name"] == "this" for row in reads))

    def test_lexical_shadowing_does_not_read_configuration_field(self):
        self.java("Props", '''package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Data;
@Data @ConfigurationProperties("app") class Props { private String host; }
''')
        self.java("Reader", '''package app;
class Reader {
 Props props;
 void read(String props){ props.getHost(); this.props.getHost(); }
 void other(){ java.util.List.of("x").forEach(props -> props.getHost()); }
}
''')
        result = structure.extract(self.repo)
        self.assertEqual([row["key"] for row in result["configuration_reads"]], ["app.host"])
        calls = [row for row in result["type_dependencies"] if row["relationship"] == "CALLS_COMPONENT"]
        self.assertEqual(len(calls), 1)

    def test_interface_dependencies_do_not_choose_an_implementation(self):
        self.java("Worker", "package api; public interface Worker { void run(); }")
        self.java("One", "package impl; import api.Worker; class One implements Worker { public void run(){} }")
        self.java("Two", "package impl; import api.Worker; class Two implements Worker { public void run(){} }")
        self.java("Consumer", '''package app;
import api.Worker;
import org.springframework.stereotype.Service;
@Service class Consumer { final Worker worker; Consumer(Worker worker){this.worker=worker;} void call(){worker.run();} }
''')
        result = structure.extract(self.repo)
        type_by_id = {row["type_id"]: row for row in result["types"]}
        calls = [row for row in result["type_dependencies"] if row["relationship"] in {"INJECTS", "CALLS_COMPONENT"}]
        self.assertEqual(len(calls), 2)
        self.assertTrue(all(type_by_id[row["target_type"]]["qualified_name"] == "api.Worker" for row in calls))
        self.assertTrue(all(row["dispatch"] == "DECLARED_INTERFACE" for row in calls))
        self.assertTrue(all(row["implementation_candidates"] == ["impl.One", "impl.Two"] for row in calls))
        self.assertIn("AMBIGUOUS_JAVA_INTERFACE_DISPATCH", {row["code"] for row in result["diagnostics"]})

    def test_bounded_superclass_calls_require_accessible_unique_name_and_arity(self):
        self.java("base/Base", '''package app.base;
public class Base {
 protected void token() {}
 void packageOnly() {}
 private void secret() {}
 protected void overloaded(String value) {}
 protected void overloaded(int value) {}
}
''')
        self.java("base/Same", '''package app.base;
class Same extends Base {
 void run() { token(); packageOnly(); secret(); overloaded(null); }
}
''')
        self.java("child/Child", '''package app.child;
import app.base.Base;
class Child extends Base {
 void run() { token(); packageOnly(); secret(); }
}
''')
        self.java("bridge/Mid", '''package app.bridge;
import app.base.Base;
public class Mid extends Base {}
''')
        self.java("base/Return", '''package app.base;
import app.bridge.Mid;
class Return extends Mid { void run() { packageOnly(); } }
''')
        self.java("api/DefaultApi", '''package app.api;
public interface DefaultApi { default void ping() {} }
''')
        self.java("api/Impl", '''package app.api;
class Impl implements DefaultApi { void run() { ping(); } }
''')
        self.java("child/StaticImport", '''package app.child;
import app.base.Base;
import static java.util.Collections.emptyList;
class StaticImport extends Base { void run() { emptyList(); } }
''')
        result = structure.extract(self.repo)
        types = {row["type_id"]: row for row in result["types"]}
        calls = [row for row in result["type_dependencies"] if row["relationship"] == "CALLS_COMPONENT"]
        resolved = {(types[row["source_type"]]["qualified_name"], types[row["target_type"]]["qualified_name"], row["method"], row["dispatch"]): row for row in calls}
        self.assertIn(("app.base.Same", "app.base.Base", "token", "DECLARED_SUPERCLASS"), resolved)
        self.assertIn(("app.base.Same", "app.base.Base", "packageOnly", "DECLARED_SUPERCLASS"), resolved)
        self.assertIn(("app.child.Child", "app.base.Base", "token", "DECLARED_SUPERCLASS"), resolved)
        self.assertNotIn(("app.child.Child", "app.base.Base", "packageOnly", "DECLARED_SUPERCLASS"), resolved)
        self.assertNotIn(("app.base.Return", "app.base.Base", "packageOnly", "DECLARED_SUPERCLASS"), resolved)
        self.assertNotIn(("app.base.Same", "app.base.Base", "secret", "DECLARED_SUPERCLASS"), resolved)
        self.assertNotIn(("app.base.Same", "app.base.Base", "overloaded", "DECLARED_SUPERCLASS"), resolved)
        self.assertEqual(resolved[("app.base.Same", "app.base.Base", "token", "DECLARED_SUPERCLASS")]["target_method_line"], 3)
        self.assertFalse(any(types[row["source_type"]]["qualified_name"] == "app.api.Impl" and row["method"] == "ping" for row in calls))
        self.assertFalse(any(types[row["source_type"]]["qualified_name"] == "app.child.StaticImport" for row in calls))
        self.assertIn("AMBIGUOUS_JAVA_INHERITED_CALL", {row["code"] for row in result["diagnostics"]})

    def test_method_calls_survive_class_aggregation_and_keep_deferred_bodies_separate(self):
        self.java("Worker", "package app; class Worker { void load(){} void save(){} }")
        self.java("Api", '''package app;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
@RestController class Api {
 Worker worker;
 @GetMapping("/first") void first(){ helper(); }
 void helper(){ worker.load(); }
 @GetMapping("/second") void second(){ worker.save(); }
 void later(){ Runnable callback = () -> worker.load(); }
 void ambiguous(){ overloaded(1); }
 void overloaded(int value){}
 void overloaded(String value){}
}
''')
        graph = build_graph.Graph(self.workspace)
        repository = graph.add_repository(self.repo, "SPRING", True)
        build_graph.extract_spring(graph, self.repo, repository)
        nodes = graph.nodes
        calls = [edge for edge in graph.edges.values() if edge["relationship"] == "CALLS_COMPONENT"]
        worker_call = next(edge for edge in calls if nodes[edge["target"]]["name"] == "Worker")
        self.assertEqual(worker_call["properties"]["methods"], ["load", "save"])
        sites = worker_call["properties"]["call_sites"]
        self.assertEqual({(site["source_method"], site["target_method"], site["deferred"]) for site in sites},
                         {("helper", "load", False), ("second", "save", False), ("later", "load", True)})
        self.assertTrue(all(site["evidence"] and site["source_method_line"] and site["target_method_line"] for site in sites))
        self_call = next(edge for edge in calls if edge["source"] == edge["target"])
        self.assertEqual([(site["source_method"], site["target_method"]) for site in self_call["properties"]["call_sites"]],
                         [("first", "helper")])
        invokes = [edge for edge in graph.edges.values() if edge["relationship"] == "INVOKES"]
        self.assertEqual({edge["properties"]["handler"] for edge in invokes}, {"first", "second"})
        for edge in invokes:
            methods = nodes[edge["target"]]["properties"]["declared_methods"]
            self.assertIn({"name": edge["properties"]["handler"], "line": edge["properties"]["handler_line"], "arity": 0}, methods)

    def test_configuration_getter_read_keeps_its_lexical_method(self):
        self.java("Props", '''package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Data;
@Data @ConfigurationProperties("client") class Props { private String host; }
''')
        self.java("Worker", "package app; class Worker { Props props; String load(){return props.getHost();} }")
        graph = build_graph.Graph(self.workspace)
        repository = graph.add_repository(self.repo, "SPRING", True)
        build_graph.extract_spring(graph, self.repo, repository)
        read = next(edge for edge in graph.edges.values() if edge["relationship"] == "READS_CONFIG")
        self.assertEqual(read["properties"]["call_sites"][0]["source_method"], "load")
        self.assertEqual(read["properties"]["call_sites"][0]["deferred"], False)

    def test_exact_imports_and_ambiguous_wildcards_remain_distinct(self):
        self.java("a/Worker", "package a; public class Worker { void run(){} }")
        self.java("b/Worker", "package b; public class Worker { void run(){} }")
        self.java("Exact", "package app; import a.Worker; class Exact { Worker worker; void call(){worker.run();} }")
        self.java("Unknown", "package app; import a.*; import b.*; class Unknown { Worker worker; void call(){worker.run();} }")
        result = structure.extract(self.repo)
        types = {row["type_id"]: row for row in result["types"]}
        calls = [row for row in result["type_dependencies"] if row["relationship"] == "CALLS_COMPONENT"]
        self.assertEqual(len(calls), 1)
        self.assertEqual(types[calls[0]["target_type"]]["qualified_name"], "a.Worker")
        self.assertEqual({row["code"] for row in result["diagnostics"]}, {"AMBIGUOUS_JAVA_TYPE", "AMBIGUOUS_JAVA_CALL_TARGET"})

    def test_custom_getter_cannot_imply_an_unrelated_property_read(self):
        self.java("Props", '''package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Data;
@Data @ConfigurationProperties("app") class Props {
 private String host; private String password;
 String getHost(){ return password; }
 String getPassword(){ return "DO_NOT_RETAIN_CUSTOM"; }
}
''')
        self.java("Reader", "package app; class Reader { Props p; void read(){p.getHost();p.getPassword();p.getClass();} }")
        result = structure.extract(self.repo)
        self.assertEqual([row["key"] for row in result["configuration_reads"]], ["app.password"])
        self.assertEqual([row["code"] for row in result["diagnostics"]], ["UNRESOLVED_CONFIGURATION_ACCESSOR"])
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(result))

    def test_type_argument_is_not_a_superclass_and_initialized_field_is_not_injection(self):
        self.java("Model", "package app; class Model {}")
        self.java("Port", "package app; interface Port<T> {}")
        self.java("Worker", '''package app;
import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
@Service @RequiredArgsConstructor class Worker implements Port<Model> { private final Model model = new Model(); }
''')
        result = structure.extract(self.repo)
        types = {row["type_id"]: row for row in result["types"]}
        self.assertEqual([types[row["target_type"]]["name"] for row in result["type_dependencies"] if row["relationship"] == "IMPLEMENTS_TYPE"], ["Port"])
        self.assertFalse(any(row["relationship"] == "INJECTS" for row in result["type_dependencies"]))

    def test_profiles_duplicate_keys_and_placeholder_defaults_preserve_uncertainty(self):
        self.java("Reader", "class Reader {}")
        self.write("src/main/resources/application.yml", '''spring:
 config:
  activate:
   on-profile: dev
client:
 host: ${API_HOST:DO_NOT_RETAIN_DEV}
 host: DO_NOT_RETAIN_DUPLICATE
---
spring:
 config:
  activate:
   on-profile: prod
client:
 host: ${API_HOST:DO_NOT_RETAIN_PROD}
''')
        result = structure.extract(self.repo)
        hosts = [row for row in result["configuration_keys"] if row["key"] == "client.host"]
        self.assertEqual(len(hosts), 3)
        self.assertEqual({row["profile"] for row in hosts}, {"dev", "prod"})
        self.assertIn("DUPLICATE_CONFIGURATION_KEY", {row["code"] for row in result["diagnostics"]})
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(result))

    def test_graph_keeps_exact_class_id_and_creates_detail_for_grouped_impl(self):
        self.java("Props", '''package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Data;
@Data @ConfigurationProperties("app") class Props { private String host; }
''')
        path = self.java("WorkerImpl", "package app; class WorkerImpl { Props props; String call(){return props.getHost();} }")
        graph = build_graph.Graph(self.workspace)
        repository = graph.add_repository(self.repo, "SPRING", True)
        source = path.relative_to(self.workspace).as_posix()
        ev = graph.add_evidence(repository, source, 1, "Source declaration", "fixture")
        for identity, name, props in [("service:app", "app", {}), ("component:old-exact", "Props", {"detail_level": "CLASS"}), ("component:group", "group", {})]:
            graph.add_node(identity, "SERVICE" if identity == "service:app" else "COMPONENT", name, repository, dimensions=("RUNTIME",),
                           component_kind=None, functional_role="Fixture", business_meaning="Fixture", source_paths=(source,), evidence=(ev,), properties=props)
        mapping = {"src/main/java/Props.java": "component:old-exact", "src/main/java/WorkerImpl.java": "component:group"}
        result = structure.add_to_graph(graph, self.repo, repository, mapping)
        self.assertEqual(mapping["src/main/java/Props.java"], "component:old-exact")
        self.assertNotEqual(mapping["src/main/java/WorkerImpl.java"], "component:group")
        self.assertTrue(any(row["relationship"] == "READS_CONFIG" for row in graph.edges.values()))
        self.assertTrue(all(row["evidence"] for row in result["ledger"] if row["disposition"] == "EXTRACTED"))
        self.assertEqual(result["configuration_reads"][0]["component_id"], mapping["src/main/java/WorkerImpl.java"])

    def test_computed_accessor_records_source_fields_without_retaining_values(self):
        self.java("Props", """package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Data;
@Data @ConfigurationProperties("app") class Props {
 private int connectTimeout;
 java.time.Duration getConnectTimeoutDuration(){ return java.time.Duration.ofSeconds(connectTimeout); }
}
""")
        self.java("Reader", "package app; class Reader { Props p; void read(){p.getConnectTimeoutDuration();} }")
        result = structure.extract(self.repo)
        self.assertEqual([row["key"] for row in result["configuration_reads"]], ["app.connect-timeout"])
        self.assertFalse(result["diagnostics"])

    def test_declared_module_sources_are_included_and_undeclared_sources_are_excluded(self):
        self.write("pom.xml", "<project><artifactId>app</artifactId><modules><module>sdk</module></modules></project>")
        self.write("sdk/pom.xml", "<project><artifactId>sdk</artifactId></project>")
        self.write("sdk/src/main/java/Props.java", """package app;
import org.springframework.boot.context.properties.ConfigurationProperties;
import lombok.Data;
@Data @ConfigurationProperties("app") class Props { private String host; }
""")
        self.write("other/src/main/java/Hidden.java", "class Hidden {}")
        result = structure.extract(self.repo)
        self.assertEqual(result["statistics"]["java_files"], 1)
        self.assertEqual(result["statistics"]["configuration_classes"], 1)
        self.assertEqual(result["types"][0]["path"], "sdk/src/main/java/Props.java")

    def test_unrelated_same_named_annotation_is_not_spring_configuration(self):
        self.java("ConfigurationProperties", "package app; public @interface ConfigurationProperties { String value(); }")
        self.java("Props", "package app; import org.springframework.boot.context.properties.*; @ConfigurationProperties(\"not-spring\") class Props { String value; }")
        result = structure.extract(self.repo)
        self.assertFalse(result["configuration_classes"])
        self.assertFalse(result["configuration_bindings"])


if __name__ == "__main__":
    unittest.main()
