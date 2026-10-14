"""Validate linked metadata without treating declarations as execution grants."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from ai_sdlc_workbench.context.catalogs import (
    CATALOG_NAMES, CONTRACT_TYPES, REPOSITORY_TYPES, SOURCE_TYPES,
    _ENTRY_SCHEMAS, load_catalogs,
)
from ai_sdlc_workbench.models import WorkbenchError, validate_arguments, validate_schema
from ai_sdlc_workbench.runtime import Workbench
from ai_sdlc_workbench.workspace import initialize_workspace


ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-catalogs-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def load(self, entries):
        locations = {}
        for category, records in entries.items():
            locations[category] = f"{category}.yaml"
            (self.root / locations[category]).write_text(
                yaml.safe_dump({"schema_version": 1, category: records}), encoding="utf-8")
        return load_catalogs(self.root, locations)

    def fixture(self):
        return {
            "repositories": [
                {"id": "payments", "primary_type": "backend", "responsibility": "Process payments.",
                 "ownership": {"team": "Payments", "contact": "owner@example.invalid"},
                 "provides_contract_ids": ["http"], "source_ids": ["git"]},
                {"id": "shared", "primary_type": "library", "consumes_contract_ids": ["http"]},
                {"id": "deploy", "primary_type": "deployment"},
            ],
            "services": [
                {"id": "api", "repository_ids": ["payments", "shared"],
                 "deployment_repository_ids": ["deploy"], "provides_contract_ids": ["http"]},
                {"id": "worker", "repository_id": "payments", "repository_ids": ["shared"],
                 "deployment_repository_ids": ["deploy"], "consumes_contract_ids": ["http"]},
            ],
            "capabilities": [{"id": "settlement", "service_ids": ["api", "worker"],
                              "repository_ids": ["payments", "shared"], "source_ids": ["git"]}],
            "contracts": [{"id": "http", "type": "http", "status": "documented",
                           "source": {"repository_id": "payments", "path": "contracts/openapi.yaml",
                                      "revision": "1" * 40},
                           "service_ids": ["api"], "repository_ids": ["payments"], "source_ids": ["git"]}],
            "sources": [{"id": "git", "type": "git", "purpose": "technical",
                         "location": "https://example.invalid/payments.git", "repository_id": "payments"}],
            "tools": [],
        }

    def test_legacy_minimal_entries_and_repository_id_remain_valid(self):
        records = {
            "repositories": [{"id": "code"}],
            "services": [{"id": "service", "repository_id": "code"}],
            "capabilities": [{"id": "business", "service_ids": ["service"]}],
        }
        catalogs, tools = self.load(records)
        self.assertEqual(catalogs, records)
        self.assertEqual(tools, [])
        self.assertNotIn("contracts", catalogs)
        self.assertNotIn("sources", catalogs)

    def test_many_to_many_links_and_separate_deployment_repositories_are_preserved(self):
        records = self.fixture()
        catalogs, tools = self.load(records)
        self.assertEqual(catalogs["services"], records["services"])
        self.assertEqual(catalogs["capabilities"], records["capabilities"])
        self.assertEqual(catalogs["contracts"][0]["source"], records["contracts"][0]["source"])
        self.assertTrue(catalogs["sources"][0]["read_only"])
        self.assertEqual(tools, [])

    def test_each_registered_reference_rejects_unknown_ids(self):
        references = {
            "repositories": ("provides_contract_ids", "consumes_contract_ids", "source_ids"),
            "services": ("repository_ids", "deployment_repository_ids", "provides_contract_ids",
                         "consumes_contract_ids", "source_ids"),
            "capabilities": ("service_ids", "repository_ids", "source_ids"),
            "contracts": ("service_ids", "repository_ids", "source_ids"),
        }
        for category, fields in references.items():
            for field in fields:
                with self.subTest(category=category, field=field):
                    records = self.fixture()
                    records[category][0][field] = ["missing"]
                    with self.assertRaisesRegex(WorkbenchError, rf"{category}\."):
                        self.load(records)
        for category in ("services", "sources"):
            with self.subTest(category=category, field="repository_id"):
                records = self.fixture()
                records[category][0]["repository_id"] = "missing"
                with self.assertRaisesRegex(WorkbenchError, rf"{category}\."):
                    self.load(records)
        records = self.fixture()
        records["contracts"][0]["source"]["repository_id"] = "missing"
        with self.assertRaisesRegex(WorkbenchError, r"contracts\.http\.source"):
            self.load(records)

    def test_reference_lists_reject_duplicate_nonstring_and_nonlist_values(self):
        fields = {
            "repositories": ("provides_contract_ids", "consumes_contract_ids", "source_ids", "responsibilities"),
            "services": ("repository_ids", "deployment_repository_ids", "provides_contract_ids",
                         "consumes_contract_ids", "source_ids"),
            "capabilities": ("service_ids", "repository_ids", "source_ids"),
            "contracts": ("service_ids", "repository_ids", "source_ids", "verified_claims"),
        }
        for category, names in fields.items():
            for field in names:
                for invalid in (["duplicate", "duplicate"], [None], [{}], "one", ["   "]):
                    with self.subTest(category=category, field=field, invalid=invalid):
                        records = self.fixture()
                        records[category][0][field] = invalid
                        with self.assertRaises(WorkbenchError):
                            self.load(records)

    def test_all_enum_values_are_accepted_and_unknown_values_are_rejected(self):
        for category, field, values in (("repositories", "primary_type", REPOSITORY_TYPES),
                                        ("contracts", "type", CONTRACT_TYPES),
                                        ("sources", "type", SOURCE_TYPES)):
            for value in (*values, "unsupported"):
                with self.subTest(category=category, value=value):
                    records = self.fixture()
                    records[category][0][field] = value
                    records["sources"][0]["read_only"] = True
                    if value == "unsupported":
                        with self.assertRaises(WorkbenchError):
                            self.load(records)
                    else:
                        self.load(records)
        for value in ("technical", "context", "unsupported"):
            with self.subTest(purpose=value):
                records = self.fixture()
                records["sources"][0]["purpose"] = value
                if value == "unsupported":
                    with self.assertRaises(WorkbenchError):
                        self.load(records)
                else:
                    self.load(records)

    def test_all_catalog_ids_reject_duplicates_and_path_shaped_identifiers(self):
        for category in CATALOG_NAMES:
            records = self.fixture()
            records["tools"] = [{"id": "tool", "kind": "knowledge", "provider": "knowledge.local",
                                 "environment": "local", "config": {"path": "knowledge"},
                                 "allowed_operations": ["read"]}]
            valid = records[category][0]
            self.load(records)
            for identifier in (valid["id"], "../outside", "x" * 81, None):
                with self.subTest(category=category, identifier=identifier):
                    changed = deepcopy(records)
                    changed[category].append({**deepcopy(valid), "id": identifier})
                    with self.assertRaises(WorkbenchError):
                        self.load(changed)

    def test_new_contracts_require_exact_source_fields(self):
        for field in ("repository_id", "path", "revision"):
            for mutation in ("missing", "blank", "wrong-type"):
                with self.subTest(field=field, mutation=mutation):
                    records = self.fixture()
                    source = records["contracts"][0]["source"]
                    if mutation == "missing":
                        del source[field]
                    else:
                        source[field] = "  " if mutation == "blank" else 123
                    with self.assertRaisesRegex(WorkbenchError, r"contracts\.http"):
                        self.load(records)
        for revision in ("main", "HEAD", "v1.0", "abcdef0", "g" * 40, "a" * 41, "a" * 63):
            with self.subTest(revision=revision):
                records = self.fixture()
                records["contracts"][0]["source"]["revision"] = revision
                with self.assertRaisesRegex(WorkbenchError, r"contracts\.http\.source\.revision"):
                    self.load(records)
        for revision in ("a" * 40, "F" * 64):
            with self.subTest(revision=revision):
                records = self.fixture()
                records["contracts"][0]["source"]["revision"] = revision
                self.load(records)
        for path in ("../outside.yaml", "/absolute.yaml", "C:/outside.yaml", "C:\\outside.yaml",
                     "contracts/../../outside.yaml", ".", "file\x00.yaml"):
            with self.subTest(path=path):
                records = self.fixture()
                records["contracts"][0]["source"]["path"] = path
                with self.assertRaises(WorkbenchError):
                    self.load(records)

    def test_candidates_require_documentation_gaps_and_cannot_claim_verification(self):
        records = self.fixture()
        contract = records["contracts"][0]
        contract["status"] = "candidate"
        with self.assertRaisesRegex(WorkbenchError, "documentation gap"):
            self.load(records)
        contract["documentation_gap"] = "The interface has no approved specification."
        self.load(records)
        contract["verified_claims"] = []
        self.load(records)
        contract["verified_claims"] = ["Executed successfully."]
        with self.assertRaisesRegex(WorkbenchError, "cannot have verified claims"):
            self.load(records)
        contract["verified_claims"] = []
        contract["verified"] = True
        with self.assertRaises(WorkbenchError):
            self.load(records)
        del contract["verified"]
        contract["status"] = "verified"
        with self.assertRaises(WorkbenchError):
            self.load(records)

    def test_confluence_requires_an_explicit_read_only_declaration(self):
        for value in (None, False, "true", True):
            with self.subTest(read_only=value):
                records = self.fixture()
                records["sources"][0]["type"] = "confluence"
                if value is not None:
                    records["sources"][0]["read_only"] = value
                if value is True:
                    self.load(records)
                else:
                    with self.assertRaisesRegex(WorkbenchError, r"sources\.git"):
                        self.load(records)

    def test_source_catalog_cannot_create_tools_or_grant_operations(self):
        records = self.fixture()
        for field, value in (("provider", "knowledge.local"), ("config", {"path": "outside"}),
                             ("allowed_operations", ["read"]), ("tools", [{"id": "hidden"}])):
            with self.subTest(field=field):
                changed = deepcopy(records)
                changed["sources"][0][field] = value
                with self.assertRaises(WorkbenchError):
                    self.load(changed)
        self.load(records)
        manifest = {"schema_version": 1, "id": "metadata-only", "name": "Metadata only",
                    "resources": [], "registries": {name: f"{name}.yaml" for name in records}}
        (self.root / "workspace.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
        workbench = Workbench(self.root)
        self.assertEqual(workbench.describe()["resources"], [])
        self.assertEqual(workbench.describe()["catalogs"], {
            category: {"count": len(entries), "ids": [entry["id"] for entry in entries]}
            for category, entries in records.items() if category != "tools"})
        for resource, operation in (("git", "read"), ("payments", "status")):
            with self.subTest(resource=resource):
                with self.assertRaises(WorkbenchError):
                    workbench.call(resource, operation)
        self.assertEqual(workbench.runs(), [])

    def test_registry_structural_schemas_match_loader_and_validate_generated_catalogs_and_examples(self):
        generated = self.root / "generated"
        initialize_workspace(generated)
        workspace = json.loads((ROOT / "core/schemas/workspace.schema.json").read_text())
        schemas = {**_ENTRY_SCHEMAS, "tools": workspace["properties"]["resources"]["items"]}
        for category, entry_schema in schemas.items():
            with self.subTest(category=category):
                schema = json.loads((ROOT / "registry" / f"{category}.schema.json").read_text())
                self.assertEqual(schema["properties"][category]["items"], entry_schema)
                validate_schema(schema)
                for directory in (generated / "registry", ROOT / "registry/examples"):
                    payload = yaml.safe_load((directory / f"{category}.yaml").read_text())
                    validate_arguments(payload, schema, category)
                default = yaml.safe_load((generated / "registry" / f"{category}.yaml").read_text())
                self.assertEqual(default, {"schema_version": 1, category: []})
        example_root = ROOT / "registry/examples"
        catalogs, tools = load_catalogs(example_root, {name: f"{name}.yaml" for name in CATALOG_NAMES})
        self.assertEqual(tools, [])
        self.assertEqual({entry["primary_type"] for entry in catalogs["repositories"]}, set(REPOSITORY_TYPES))
        self.assertEqual({entry["type"] for entry in catalogs["contracts"]}, set(CONTRACT_TYPES))
        self.assertEqual({entry["type"] for entry in catalogs["sources"]}, set(SOURCE_TYPES))


if __name__ == "__main__":
    unittest.main()
