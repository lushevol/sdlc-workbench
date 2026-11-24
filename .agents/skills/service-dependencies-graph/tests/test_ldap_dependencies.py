"""Check typed directory calls, argument exclusion, and identity limits."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name("_support.py")))["load_tool"]
ldap = load_tool("extract_ldap_dependencies")
builder = load_tool("build_graph")
validator = load_tool("validate_graph")
queries = load_tool("graph_query")


class LdapDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-ldap-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)

    def java(self, name, source):
        path = self.repo / "src/main/java" / (name + ".java")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        return path

    def test_spring_calls_include_observed_context_chain_without_values(self):
        self.java("Auth", '''import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.core.ContextSource;
class Auth {
 private LdapTemplate ldap;
 void login(ContextSource source) {
  ldap.getContextSource().getContext("DO_NOT_RETAIN_DN", "DO_NOT_RETAIN_PASSWORD");
  this.ldap.lookup("DO_NOT_RETAIN_DN");
  source.getReadOnlyContext();
 }
}''')
        operations = ldap.extract(self.repo)["operations"]
        self.assertEqual([row["method"] for row in operations], ["getContext", "lookup", "getReadOnlyContext"])
        self.assertEqual([row["line"] for row in operations], [6, 7, 8])
        self.assertEqual({row["protocol"] for row in operations}, {"LDAP"})
        self.assertEqual({row["provider_identity"] for row in operations}, {"UNKNOWN"})
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(operations))

    def test_jndi_retains_generic_directory_protocol(self):
        self.java("Directory", '''import javax.naming.directory.InitialDirContext;
import javax.naming.directory.DirContext;
import javax.naming.ldap.InitialLdapContext;
class Directory {
 void open(java.util.Hashtable env, DirContext existing) throws Exception {
  new InitialDirContext(env);
  new InitialLdapContext(env, null);
  existing.getAttributes("DO_NOT_RETAIN_DN");
  existing.close();
 }
}''')
        operations = ldap.extract(self.repo)["operations"]
        self.assertEqual([(row["method"], row["protocol"]) for row in operations],
                         [("<init>", "DIRECTORY"), ("<init>", "LDAP"), ("getAttributes", "DIRECTORY")])

    def test_imports_declarations_comments_and_foreign_types_do_not_establish_calls(self):
        self.java("NoCall", '''import org.springframework.ldap.core.LdapTemplate;
class NoCall {
 LdapTemplate ldap;
 String text = "ldap.lookup(SECRET)";
 // ldap.lookup(SECRET);
 void configure() { new LdapTemplate(); ldap.getContextSource(); }
}''')
        self.java("Foreign", '''import unrelated.LdapTemplate;
class Foreign { LdapTemplate ldap; void run() { ldap.lookup("SECRET"); } }''')
        self.assertEqual(ldap.extract(self.repo)["operations"], [])

    def test_shadowed_receivers_and_types_stay_unselected(self):
        self.java("Shadow", '''import org.springframework.ldap.core.LdapTemplate;
class Shadow {
 LdapTemplate ldap;
 void parameter(Object ldap) { ldap.lookup("SECRET"); this.ldap.lookup("SECRET"); }
 void local() { Object ldap = other(); ldap.lookup("SECRET"); }
 void lambda() { accept(ldap -> ldap.lookup("SECRET")); }
 void loop() { for (Object ldap : values) { ldap.lookup("SECRET"); } }
 void resource() { try (Object ldap = other()) { ldap.lookup("SECRET"); } }
}''')
        operations = ldap.extract(self.repo)["operations"]
        self.assertEqual([(row["method"], row["line"]) for row in operations], [("lookup", 4)])
        self.java("Collision", '''import org.springframework.ldap.core.LdapTemplate;
class Collision { class LdapTemplate {} LdapTemplate ldap; void run() { ldap.lookup("SECRET"); } }''')
        self.assertEqual(len(ldap.extract(self.repo)["operations"]), 1)

    def test_wildcards_fully_qualified_types_and_package_collisions(self):
        self.java("Wildcard", '''package safe; import org.springframework.ldap.core.*;
class Wildcard { LdapOperations ldap; void run() { ldap.authenticate("SECRET"); } }''')
        self.java("Qualified", '''class Qualified {
 void run() throws Exception { new javax.naming.ldap.InitialLdapContext(null, null); }
}''')
        self.java("LocalType", '''package collision; class LdapTemplate {}''')
        self.java("UseLocal", '''package collision; import org.springframework.ldap.core.*;
class UseLocal { LdapTemplate ldap; void run() { ldap.lookup("SECRET"); } }''')
        operations = ldap.extract(self.repo)["operations"]
        self.assertEqual({row["method"] for row in operations}, {"authenticate", "<init>"})
        self.assertFalse(any(row["path"].endswith("UseLocal.java") for row in operations))

    def test_generic_class_and_method_types_shadow_imports_only_within_their_scope(self):
        self.java("GenericShadow", '''import org.springframework.ldap.core.LdapTemplate;
class Other { void lookup(String value) {} }
class ClassShadow<LdapTemplate extends Other> {
 void read(LdapTemplate client) { client.lookup("DO_NOT_RETAIN_CLASS"); }
}
class MethodShadow {
 <LdapTemplate extends Other> void read(LdapTemplate client) { client.lookup("DO_NOT_RETAIN_METHOD"); }
 void actual(LdapTemplate client) { client.lookup("DO_NOT_RETAIN_REAL"); }
}''')
        operations = ldap.extract(self.repo)["operations"]
        self.assertEqual([(row["api"], row["method"], row["line"]) for row in operations],
                         [("org.springframework.ldap.core.LdapTemplate", "lookup", 8)])
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(operations))

    def test_graph_retains_bff_class_calls_as_sanitized_unresolved_boundaries(self):
        workspace = self.repo
        self.repo = workspace / "repos/bff"
        self.java("DirectoryAuth", '''package auth;
import org.springframework.ldap.core.LdapTemplate;
class DirectoryAuth {
 private final LdapTemplate ldap;
 DirectoryAuth(LdapTemplate ldap) { this.ldap = ldap; }
 void authenticate() {
  ldap.getContextSource().getContext("DO_NOT_RETAIN_DN", "DO_NOT_RETAIN_PASSWORD");
 }
}''')
        (self.repo / "pom.xml").write_text("<project><groupId>fixture</groupId><artifactId>bff</artifactId><version>1</version></project>")
        graph = builder.Graph(workspace)
        repository = graph.add_repository(self.repo, "SPRING", True)
        builder.extract_spring(graph, self.repo, repository)
        builder.resolve_cross_repository(graph)
        document = graph.document()
        self.assertEqual(validator.validate(document, workspace), [])
        directories = [node for node in document["nodes"] if node.get("properties", {}).get("protocol") == "LDAP"]
        self.assertEqual(len(directories), 1)
        directory, = directories
        self.assertEqual(directory["type"], "DATA_PLATFORM")
        self.assertIsNone(directory["repository"])
        self.assertEqual(directory["properties"]["platform_kind"], "DIRECTORY")
        self.assertEqual(directory["properties"]["provider_identity"], "UNKNOWN")
        edges = [edge for edge in document["edges"] if edge["target"] == directory["id"]]
        self.assertEqual(len(edges), 1)
        edge, = edges
        self.assertEqual((edge["relationship"], edge["assertion_status"], edge["resolution_status"]),
                         ("QUERIES_DATA_PLATFORM", "CONFIRMED", "UNRESOLVED"))
        caller = graph.nodes[edge["source"]]
        self.assertEqual(caller["type"], "COMPONENT")
        self.assertEqual(caller["repository"], repository)
        self.assertTrue(any(path.endswith("DirectoryAuth.java") for path in caller["source_paths"]))
        evidence = [graph.evidence[key] for key in edge["evidence"]]
        self.assertTrue(all(row["extractor"] == "java-ldap-client" and row["line"] == 7 for row in evidence))
        self.assertNotIn("DO_NOT_RETAIN", json.dumps(document))
        self.assertNotIn("OUD", json.dumps(directories))
        self.assertFalse(any(edge["resolution_status"] == "RESOLVED" for edge in edges))
        dependencies = builder.dependencies(graph)
        projected = dependencies["repositories"][repository]["data_platforms"]
        self.assertEqual(len(projected), 1)
        self.assertEqual(projected[0]["protocol"], "LDAP")
        self.assertEqual(projected[0]["provider_identity"], "UNKNOWN")
        self.assertEqual(projected[0]["resolution_statuses"], ["UNRESOLVED"])
        services = queries.service_catalog(document, dependencies)["services"]
        service, = services
        self.assertEqual(service["runtime"]["data_platforms"], projected)


if __name__ == "__main__":
    unittest.main()
