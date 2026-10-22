"""Check the reference-based workspace through its public interfaces."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.runtime import Workbench
from ai_sdlc_workbench.workspace import initialize_workspace, load_workspace


CANONICAL_SKILL_IDS = (
    "analyze-requirement", "code-review", "connectors", "detect-gaps", "gherkin-quality", "govern-knowledge",
    "impact-analysis", "ingest-knowledge", "query-knowledge", "release-clinic", "release-confidence", "repository-onboarding",
    "service-dependencies-graph", "validate-sdlc-documents", "verify-implementation",
)

BROWSER_LOCAL_FILES = (
    "adapters/browser/browser.mjs",
    "adapters/browser/node_modules/playwright/README.md",
    "adapters/browser/.browsers/chromium/browser",
    "adapters/browser/evidence/result.json",
)

TASK_LOCAL_FILES = (
    "tasks/private-task/intake.md",
    "tasks/private-task/evidence/request.txt",
    "tasks/private-task/evidence/trace.zip",
)

KNOWLEDGE_EVIDENCE_FILES = (
    "evidence/knowledge/sources/private.txt",
    "evidence/knowledge/audit/private.yaml",
    "evidence/knowledge/findings/private.md",
)

REPOSITORY_LOCAL_FILES = (
    "repos/services/private-api/.git/config",
    "repos/services/private-api/src/main.py",
)


class WorkspacePackagingTests(unittest.TestCase):
    def test_runtime_data_excludes_imported_external_tool_trees(self):
        from setuptools import Distribution
        from setuptools.command.build_py import build_py
        from setuptools.config.pyprojecttoml import read_configuration

        source = Path(__file__).resolve().parents[1]
        config = read_configuration(str(source / "pyproject.toml"))["tool"]["setuptools"]
        distribution = Distribution({
            "packages": config["packages"],
            "package_dir": {name: str(source / path) for name, path in config["package-dir"].items()},
            "package_data": config["package-data"],
            "include_package_data": config["include-package-data"],
        })
        command = build_py(distribution)
        command.ensure_finalized()
        command.get_data_files()
        assets = {str(Path(directory) / name) for _, directory, _, names in command.data_files for name in names}
        expected = {str(path) for pattern in ("schemas/*.json", "skills/*.md")
                    for path in (source / "core").glob(pattern)}
        self.assertEqual(assets, expected)

    def test_reused_build_removes_stale_files_and_ships_all_canonical_skills(self):
        from setuptools import Distribution
        from setuptools.command.build_py import build_py

        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-package-stage-") as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            shutil.copy2(source_root / "setup.py", source / "setup.py")
            shutil.copy2(source_root / "scaffold.json", source / "scaffold.json")
            manifest = json.loads((source / "scaffold.json").read_text(encoding="utf-8"))
            alias_paths = {source_root / relative for relative in manifest["skill_aliases"]}

            def ignore_aliases(directory, names):
                return [name for name in names if Path(directory) / name in alias_paths
                        or name == "__pycache__" or name.endswith(".pyc")]

            for relative in manifest["paths"]:
                original, destination = source_root / relative, source / relative
                if original.is_dir():
                    shutil.copytree(original, destination, ignore=ignore_aliases)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(original, destination)
            for relative in (*BROWSER_LOCAL_FILES, *TASK_LOCAL_FILES, *REPOSITORY_LOCAL_FILES,
                             *KNOWLEDGE_EVIDENCE_FILES):
                local = source / relative
                local.parent.mkdir(parents=True, exist_ok=True)
                local.write_bytes(b"Local browser tooling and evidence.\n")
            clinic_source = source / "core/release-clinic"
            shutil.copytree(source_root / "core/release-clinic", clinic_source,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (clinic_source / ".env").write_text("TEST_SECRET=excluded\n", encoding="utf-8")
            (clinic_source / ".env.private").write_text("TEST_SECRET=excluded\n", encoding="utf-8")
            onboarding = source / ".agents/skills/repository-onboarding"
            (onboarding / ".DS_Store").write_bytes(b"Local file metadata.\n")
            (onboarding / "scripts/cached.pyc").write_bytes(b"Cached Python code.\n")
            (onboarding / "scripts/__pycache__").mkdir(exist_ok=True)
            (onboarding / "scripts/__pycache__/cached.pyc").write_bytes(b"Cached Python code.\n")
            with patch("setuptools.setup"):
                build_workspace = runpy.run_path(str(source / "setup.py"))["BuildWorkspace"]
            build_lib = Path(temporary) / "lib"
            package = build_lib / "ai_sdlc_workbench"
            retired = package / "relationships/graph"
            retired.mkdir(parents=True)
            (retired / "build_graph.py").write_bytes(b"Retired graph engine.\n")
            (retired / "viewer.html").write_bytes(b"Retired viewer.\n")
            unrelated = build_lib / "other_package/keep.py"
            unrelated.parent.mkdir()
            unrelated.write_bytes(b"Preserve the other package.\n")
            current = package / "__init__.py"

            def write_current_package(command):
                self.assertFalse(retired.exists())
                current.parent.mkdir(parents=True, exist_ok=True)
                current.write_bytes(b'"""Current package."""\n')

            command = build_workspace(Distribution())
            command.build_lib = str(build_lib)
            with patch.object(build_py, "run", autospec=True, side_effect=write_current_package) as parent_run:
                command.run()
            parent_run.assert_called_once_with(command)
            self.assertEqual(current.read_bytes(), b'"""Current package."""\n')
            self.assertFalse(retired.exists())
            self.assertEqual(unrelated.read_bytes(), b"Preserve the other package.\n")
            scaffold = package / "scaffold"
            clinic = package / "release-clinic"
            self.assertTrue((clinic / "release_clinic_env.py").is_file())
            self.assertTrue((clinic / "plugins/test/dtp-tda-service/service/stream_config.yaml").is_file())
            self.assertFalse((clinic / ".env").exists())
            self.assertFalse((clinic / ".env.private").exists())
            self.assertFalse((scaffold / "core/release-clinic").exists())
            for relative in (*BROWSER_LOCAL_FILES, *TASK_LOCAL_FILES, *REPOSITORY_LOCAL_FILES,
                             *KNOWLEDGE_EVIDENCE_FILES):
                self.assertFalse((scaffold / relative).exists(), relative)
            self.assertEqual(sorted(path.name for path in (scaffold / "repos").iterdir()), ["README.md"])
            self.assertEqual((scaffold / "tasks/README.md").read_bytes(),
                             (source / "tasks/README.md").read_bytes())
            self.assertEqual(sorted(path.name for path in (scaffold / "tasks").iterdir()), ["README.md"])
            for adapter in ("claude-code", "copilot", "mcp", "sources"):
                self.assertTrue((scaffold / "adapters" / adapter / "README.md").is_file())
            canonical = scaffold / ".agents/skills/service-dependencies-graph"
            for relative in ("SKILL.md", "scripts/graph.py", "tools/viewer.html", "tests/test_portability.py"):
                self.assertTrue((canonical / relative).is_file(), relative)
            engines = [path.relative_to(package).as_posix() for path in package.rglob("build_graph.py")]
            self.assertEqual(engines, ["scaffold/.agents/skills/service-dependencies-graph/tools/build_graph.py"])
            canonical_onboarding = scaffold / ".agents/skills/repository-onboarding"
            for relative in ("SKILL.md", "scripts/scan_repo.py", "scripts/validate_evidence.py",
                             "references/registry-contracts.md", "references/external-dependencies.md",
                             "assets/assessment.template.md"):
                self.assertEqual((canonical_onboarding / relative).read_bytes(), (onboarding / relative).read_bytes())
            scanners = [path.relative_to(package).as_posix() for path in package.rglob("scan_repo.py")]
            self.assertEqual(scanners, ["scaffold/.agents/skills/repository-onboarding/scripts/scan_repo.py"])
            for identifier in CANONICAL_SKILL_IDS:
                skill = Path(".agents/skills") / identifier / "SKILL.md"
                self.assertEqual((scaffold / skill).read_bytes(), (source / skill).read_bytes())
            report_skill = Path("plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md")
            canonical_clinic = scaffold / ".agents/skills/release-clinic"
            self.assertEqual((canonical_clinic / "references/dtp-tda-report.md").read_bytes(),
                             (clinic / report_skill).read_bytes())
            self.assertEqual((canonical_clinic / "scripts/check_report_parity.py").read_bytes(),
                             (source / ".agents/skills/release-clinic/scripts/check_report_parity.py").read_bytes())
            self.assertFalse((scaffold / "skills").exists())
            for relative in manifest["skill_aliases"]:
                self.assertFalse((scaffold / relative).exists(), relative)
            self.assertEqual(list(scaffold.rglob(".DS_Store")), [])
            self.assertEqual(list(scaffold.rglob("*.pyc")), [])
            self.assertEqual(list(scaffold.rglob("__pycache__")), [])


class WorkspaceLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-layout-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        initialize_workspace(self.root, name="Reference workspace")

    def manifest(self):
        return yaml.safe_load((self.root / "workspace.yaml").read_text(encoding="utf-8"))

    def write_manifest(self, payload):
        (self.root / "workspace.yaml").write_text(yaml.safe_dump(payload), encoding="utf-8")

    def catalog_path(self, category):
        return self.root / self.manifest()["registries"][category]

    def write_catalog(self, category, records):
        self.catalog_path(category).write_text(
            yaml.safe_dump({"schema_version": 1, category: records}), encoding="utf-8")

    def knowledge_tool(self, directory, *, identifier="requirements", grants=None):
        return {"id": identifier, "kind": "knowledge", "provider": "knowledge.local",
                "environment": "local", "config": {"path": str(directory)},
                "allowed_operations": ["read"] if grants is None else grants}

    def test_clean_initialization_has_the_requested_roots_without_business_fixtures(self):
        directories = (
            "registry", "knowledge/requirements", "knowledge/architecture", "knowledge/decisions",
            "relationships/requirement-code", "relationships/code-test", "relationships/service-dependencies",
            *(f".agents/skills/{identifier}" for identifier in CANONICAL_SKILL_IDS),
            "core/context", "core/relationships", "core/evidence", "core/execution",
            "adapters/claude-code", "adapters/copilot", "adapters/mcp",
            "knowledge/candidates", "evidence/knowledge/audit", "evidence/knowledge/findings",
            "evidence/knowledge/sources",
            "core/knowledge/schemas", "core/knowledge/templates", "core/ingestion", "core/understanding",
            "core/governance", "adapters/sources", "tasks", "repos",
        )
        for directory in directories:
            with self.subTest(directory=directory):
                self.assertTrue((self.root / directory).is_dir())
        self.assertTrue((self.root / "workspace.yaml").is_file())
        for name in ("workspace.json", "project", "logs", "database"):
            self.assertFalse((self.root / name).exists(), name)
        for relative in ("README.md", "AGENTS.md", "docs/WORKSPACE_DESIGN.md", "docs/BEHAVIOR_REVIEW.md",
                         "docs/GHERKIN_QUALITY.md", "docs/examples/gherkin-session/session.md",
                         "docs/examples/gherkin-session/ambiguous.md", "docs/examples/gherkin-session/manifest.json",
                         "workspace.local.example.yaml", "registry/examples/contracts.yaml", "tasks/README.md",
                         "repos/README.md", "core/knowledge/README.md", "evidence/knowledge/README.md"):
            self.assertTrue((self.root / relative).is_file(), relative)
        ignored = (self.root / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertTrue({".workbench/", "workspace.local.yaml"} <= set(ignored))
        self.assertNotIn("repos/", ignored)
        self.assertEqual(sorted(path.name for path in (self.root / "repos").iterdir()), ["README.md"])
        for relative in ("workspace.local.yaml", "src", "tests", "pyproject.toml",
                         "core/__init__.py", "core/cli.py", "core/runtime.py", "core/gherkin_quality.py",
                         "core/schemas/gherkin-evidence.schema.json"):
            self.assertFalse((self.root / relative).exists(), relative)
        self.assertEqual(list((self.root / "core").rglob("*.py")), [])
        for relative in ("knowledge/raw", "knowledge/audit", "knowledge/findings",
                         "knowledge/schemas", "knowledge/templates"):
            self.assertFalse((self.root / relative).exists(), relative)
        self.assertEqual(yaml.safe_load((self.root / "evidence/knowledge/manifest.yaml").read_text()),
                         {"schema_version": 1, "sources": []})
        self.assertTrue((self.root / "core/knowledge/schemas/requirement.schema.json").is_file())
        self.assertEqual(sorted(path.name for path in (self.root / "tasks").iterdir()), ["README.md"])
        description = Workbench(self.root).describe()
        self.assertEqual(description["workspace"]["name"], "Reference workspace")
        self.assertEqual(description["resources"], [])
        self.assertEqual(description["catalogs"], {
            name: {"count": 0, "ids": []}
            for name in ("repositories", "services", "capabilities", "contracts", "sources")})

    @unittest.skipUnless(shutil.which("git"), "Git is required for repository boundary checks.")
    def test_parent_git_excludes_checkouts_while_child_git_manages_its_source(self):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}

        def git(directory, *arguments):
            return subprocess.run(
                ["git", "-C", str(directory), *arguments], env=environment,
                check=True, capture_output=True, text=True).stdout

        git(self.root, "init", "--template=")
        child = self.root / "repos/services/example-api"
        child.mkdir(parents=True)
        git(child, "init", "--template=")
        (child / "src").mkdir()
        (child / "src/main.py").write_text("print('child source')\n", encoding="utf-8")
        copied = self.root / "repos/ui/source-copy"
        copied.mkdir(parents=True)
        (copied / "index.ts").write_text("export {};\n", encoding="utf-8")
        (child.parent / "README.md").write_text("# Service repository placement\n", encoding="utf-8")

        expected = {"?? repos/README.md", "?? repos/services/README.md"}
        self.assertEqual(set(git(self.root, "status", "--porcelain", "--untracked-files=all", "--", "repos").splitlines()),
                         expected)
        self.assertEqual(git(child, "status", "--porcelain", "--untracked-files=all"), "?? src/main.py\n")
        git(child, "add", "--", "src/main.py")
        self.assertEqual(git(child, "ls-files"), "src/main.py\n")
        git(self.root, "add", "--", "repos")
        self.assertEqual(set(git(self.root, "ls-files", "--", "repos").splitlines()),
                         {"repos/README.md", "repos/services/README.md"})

    def test_initialization_excludes_project_records_and_preserves_source_bytes(self):
        source = self.root.parent / "project-source"
        shutil.copytree(self.root, source)
        shutil.copy2(Path(__file__).resolve().parents[1] / "scaffold.json", source / "scaffold.json")
        onboarding = source / ".agents/skills/repository-onboarding"
        (onboarding / ".DS_Store").write_bytes(b"Local file metadata.\n")
        (onboarding / "scripts/cached.pyc").write_bytes(b"Cached Python code.\n")
        (onboarding / "scripts/__pycache__").mkdir(exist_ok=True)
        (onboarding / "scripts/__pycache__/cached.pyc").write_bytes(b"Cached Python code.\n")
        tool = self.knowledge_tool("/private/project/source")
        records = {
            "repositories": [{"id": "project-code", "source_ids": ["project-source"]}],
            "services": [{"id": "project-service", "repository_ids": ["project-code"]}],
            "capabilities": [{"id": "project-capability", "service_ids": ["project-service"]}],
            "contracts": [],
            "sources": [{"id": "project-source", "type": "filesystem", "purpose": "context",
                         "location": "/private/project/source", "read_only": True}],
            "tools": [tool],
        }
        for category, entries in records.items():
            (source / f"registry/{category}.yaml").write_text(
                yaml.safe_dump({"schema_version": 1, category: entries}), encoding="utf-8")
        configuration = yaml.safe_load((source / "workspace.yaml").read_text(encoding="utf-8"))
        configuration.update(plugins=["project.provider"], resources=[{**tool, "id": "inline-project-tool"}])
        (source / "workspace.yaml").write_text(yaml.safe_dump(configuration), encoding="utf-8")
        private_paths = (
            "knowledge/raw/project-source.bin", "knowledge/candidates/project.md",
            "knowledge/repository-profiles/project.md", "knowledge/audit/project.yaml",
            "knowledge/findings/project.md", "knowledge/requirements/project.md",
            "knowledge/architecture/project.md", "knowledge/decisions/project.md",
            *BROWSER_LOCAL_FILES,
            *TASK_LOCAL_FILES,
            *REPOSITORY_LOCAL_FILES,
            *KNOWLEDGE_EVIDENCE_FILES,
        )
        for relative in private_paths:
            (source / relative).parent.mkdir(parents=True, exist_ok=True)
            (source / relative).write_bytes(b"Private project fixture bytes.\x00\xff\n")
        (source / "evidence/knowledge/manifest.yaml").write_text(
            "schema_version: 1\nsources:\n- id: private-project-source\n", encoding="utf-8")
        before = {str(path.relative_to(source)): path.read_bytes()
                  for path in source.rglob("*") if path.is_file()}
        target = self.root.parent / "new-workspace"
        with patch("ai_sdlc_workbench.workspace.scaffold_root", return_value=source):
            initialize_workspace(target)
        generated, resources = load_workspace(target)
        self.assertEqual(generated["plugins"], [])
        self.assertEqual(generated["resources"], [])
        self.assertEqual(resources, {})
        self.assertTrue(all(entries == [] for entries in generated["_catalogs"].values()))
        self.assertEqual(yaml.safe_load((target / "evidence/knowledge/manifest.yaml").read_text()),
                         {"schema_version": 1, "sources": []})
        for relative in private_paths:
            self.assertFalse((target / relative).exists(), relative)
        self.assertEqual((target / "tasks/README.md").read_bytes(), (source / "tasks/README.md").read_bytes())
        self.assertEqual(sorted(path.name for path in (target / "tasks").iterdir()), ["README.md"])
        self.assertEqual(list(target.rglob(".DS_Store")), [])
        self.assertEqual(list(target.rglob("*.pyc")), [])
        self.assertEqual(list(target.rglob("__pycache__")), [])
        after = {str(path.relative_to(source)): path.read_bytes()
                 for path in source.rglob("*") if path.is_file()}
        self.assertEqual(after, before)

    def test_shared_skills_have_readable_titles_and_canonical_workspace_copies(self):
        workbench = Workbench(self.root)
        skills = {item["id"]: item for item in workbench.skill_list()}
        self.assertTrue(set(CANONICAL_SKILL_IDS) | {"inspect-workspace", "verify-change"} <= skills.keys())
        for identifier in CANONICAL_SKILL_IDS:
            with self.subTest(skill=identifier):
                content = workbench.skill_read(identifier)
                heading = next(line.removeprefix("# ") for line in content.splitlines() if line.startswith("# "))
                self.assertEqual(skills[identifier]["title"], heading)
                canonical_directory = self.root / ".agents/skills" / identifier
                self.assertTrue((canonical_directory / "SKILL.md").is_file())
                alias = self.root / ".claude/skills" / identifier
                self.assertTrue(alias.is_symlink())
                self.assertEqual(alias.resolve(), canonical_directory.resolve())
        self.assertFalse((self.root / "skills").exists())
        with self.assertRaises(WorkbenchError):
            workbench.skill_read("../unregistered-skill")

    def test_document_validation_skill_alias_keeps_the_canonical_source(self):
        canonical = self.root / ".agents/skills/validate-sdlc-documents"
        source = Path(__file__).resolve().parents[1] / ".agents/skills/validate-sdlc-documents/SKILL.md"
        self.assertEqual((canonical / "SKILL.md").read_bytes(), source.read_bytes())
        alias = self.root / ".claude/skills" / canonical.name
        self.assertTrue((alias / "SKILL.md").is_file())
        if alias.is_symlink():
            self.assertEqual(alias.resolve(), canonical.resolve())
        self.assertEqual(Workbench(self.root).skill_read(canonical.name), source.read_text(encoding="utf-8"))

    def test_repository_onboarding_assets_and_alias_resolve_to_the_canonical_skill(self):
        canonical = self.root / ".agents/skills/repository-onboarding"
        for relative in ("scripts/scan_repo.py", "scripts/validate_evidence.py", "references/registry-contracts.md",
                         "references/readiness-and-evidence.md", "references/external-dependencies.md",
                         "assets/assessment.template.md", "assets/AGENTS.template.md"):
            self.assertTrue((canonical / relative).is_file(), relative)
        reference = Path("references/external-dependencies.md")
        source = Path(__file__).resolve().parents[1] / ".agents/skills/repository-onboarding"
        self.assertEqual((canonical / reference).read_bytes(), (source / reference).read_bytes())
        alias = self.root / ".claude/skills/repository-onboarding"
        if alias.is_symlink():
            self.assertEqual(alias.resolve(), canonical.resolve())
        else:
            self.assertTrue((alias / "SKILL.md").is_file())
        self.assertEqual(Workbench(self.root).skill_read("repository-onboarding"),
                         (canonical / "SKILL.md").read_text(encoding="utf-8"))

    def test_code_review_helpers_and_references_ship_with_canonical_skill(self):
        canonical = self.root / ".agents/skills/code-review"
        source = Path(__file__).resolve().parents[1] / ".agents/skills/code-review"
        for relative in ("SKILL.md", "agents/openai.yaml", "scripts/review_context.py", "scripts/scan_changes.py",
                         "scripts/validate_review.py", "references/language-checks.md", "references/review-schema.md",
                         "references/helpers.md", "references/review-checklist.md", "references/validation.md",
                         "references/integrations.md", "assets/review-report.template.md", "assets/review-report.template.json"):
            with self.subTest(asset=relative):
                self.assertEqual((canonical / relative).read_bytes(), (source / relative).read_bytes())
        result = subprocess.run(
            [os.sys.executable, str(canonical / "scripts/review_context.py"), "--help"],
            cwd=self.root.parent, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run(
            [os.sys.executable, str(canonical / "scripts/validate_review.py"), "--help"],
            cwd=self.root.parent, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run(
            [os.sys.executable, str(canonical / "scripts/scan_changes.py"), "--help"],
            cwd=self.root.parent, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_link_denial_preserves_each_skill_identity_and_canonical_forwarding_target(self):
        target = self.root.parent / "without-directory-links"
        with patch.object(Path, "symlink_to", side_effect=OSError("Directory links unavailable")):
            initialize_workspace(target)
        workbench = Workbench(target)
        for identifier in CANONICAL_SKILL_IDS:
            canonical = target / ".agents/skills" / identifier
            self.assertEqual(workbench.skill_read(identifier), (canonical / "SKILL.md").read_text(encoding="utf-8"))
            alias = target / ".claude/skills" / identifier
            self.assertFalse(alias.is_symlink())
            content = (alias / "SKILL.md").read_text(encoding="utf-8")
            frontmatter = yaml.safe_load(content.split("---", 2)[1])
            self.assertEqual(frontmatter["name"], identifier)
            reference = next(line for line in content.splitlines() if "](" in line)
            document_target = reference.split("](", 1)[1].split(")", 1)[0]
            self.assertEqual((alias / document_target).resolve(), (canonical / "SKILL.md").resolve())
            self.assertEqual(sorted(path.name for path in alias.iterdir()), ["SKILL.md"])
        self.assertTrue((target / ".agents/skills/repository-onboarding/scripts/scan_repo.py").is_file())
        self.assertTrue((target / ".agents/skills/repository-onboarding/references/external-dependencies.md").is_file())

    def test_standard_yaml_takes_precedence_and_legacy_json_remains_supported(self):
        legacy = {"schema_version": 1, "id": "legacy", "name": "Legacy workspace", "resources": []}
        (self.root / "workspace.json").write_text(json.dumps(legacy), encoding="utf-8")
        (self.root / "workspace.yaml").write_text(
            "# Standard YAML, including a block scalar.\n"
            "schema_version: 1\nid: yaml-first\nname: |-\n  YAML workspace\nresources: []\n"
            "registries:\n  repositories: registry/repositories.yaml\n"
            "  services: registry/services.yaml\n  capabilities: registry/capabilities.yaml\n"
            "  tools: registry/tools.yaml\n", encoding="utf-8")
        payload, resources = load_workspace(self.root)
        self.assertEqual(payload["id"], "yaml-first")
        self.assertEqual(payload["name"], "YAML workspace")
        self.assertEqual(resources, {})
        self.assertEqual(Workbench(self.root).describe()["workspace"]["name"], "YAML workspace")
        (self.root / "workspace.yaml").unlink()
        self.assertEqual(Workbench(self.root).describe()["workspace"]["name"], "Legacy workspace")

    def test_invalid_yaml_and_duplicate_keys_do_not_fall_back_to_valid_json(self):
        (self.root / "workspace.json").write_text(json.dumps({
            "schema_version": 1, "id": "legacy", "name": "Valid legacy fallback", "resources": []}),
            encoding="utf-8")
        valid_yaml = (self.root / "workspace.yaml").read_text(encoding="utf-8")
        for content in ("schema_version: [unterminated", valid_yaml + "\nid: hidden-override\n"):
            with self.subTest(content=content[:50]):
                (self.root / "workspace.yaml").write_text(content, encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)

    def test_duplicate_catalog_keys_are_rejected(self):
        self.catalog_path("tools").write_text(
            "schema_version: 1\ntools: []\ntools: []\n", encoding="utf-8")
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)

    def test_missing_catalog_is_reported_before_operations_can_run(self):
        self.catalog_path("services").unlink()
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)

    def test_catalog_paths_cannot_leave_the_workspace(self):
        outside = self.root.parent / "external-tools.yaml"
        outside.write_text("schema_version: 1\ntools: []\n", encoding="utf-8")
        original = self.manifest()
        for location in ("../external-tools.yaml", str(outside)):
            with self.subTest(location=location):
                payload = {**original, "registries": {**original["registries"], "tools": location}}
                self.write_manifest(payload)
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)
                self.assertEqual(outside.read_text(encoding="utf-8"), "schema_version: 1\ntools: []\n")

    def test_invalid_registry_path_returns_the_workspace_error_contract(self):
        payload = self.manifest()
        payload["registries"]["tools"] = "registry/invalid\x00.yaml"
        self.write_manifest(payload)
        with self.assertRaises(WorkbenchError):
            Workbench(self.root)
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main(["--workspace", str(self.root), "status"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["error"]["code"], "WORKBENCH_ERROR")
        self.assertEqual(errors.getvalue(), "")
        self.assertFalse((self.root / ".workbench").exists())

    def test_external_requirement_is_read_at_its_original_location_without_mutation(self):
        outside = self.root.parent / "original-requirements"
        outside.mkdir()
        source = outside / "payment.md"
        content = (self.root / "core/knowledge/templates/requirement.md").read_bytes()
        source.write_bytes(content)
        self.write_catalog("tools", [self.knowledge_tool(outside)])
        workbench = Workbench(self.root)
        action = workbench.call("requirements", "read", {"path": "payment.md"})
        self.assertEqual(action["status"], "SUCCEEDED")
        document = action["result"]["document"]
        self.assertEqual(Path(document["path"]), source.resolve())
        self.assertEqual(document["content"], content.decode("utf-8"))
        self.assertEqual(document["sha256"], hashlib.sha256(content).hexdigest())
        self.assertEqual(source.read_bytes(), content)
        self.assertEqual(list(outside.iterdir()), [source])
        self.assertEqual(list((self.root / "knowledge/requirements").glob("payment.md")), [])
        self.assertEqual(workbench.run(action["id"])["result"], action["result"])

    def test_catalog_tool_grants_deny_and_retain_a_write_attempt(self):
        outside = self.root.parent / "original-requirements"
        outside.mkdir()
        self.write_catalog("tools", [self.knowledge_tool(outside, grants=["read"])])
        workbench = Workbench(self.root)
        action = workbench.call("requirements", "ingest", {"path": "blocked.md", "content": "Must not write."})
        self.assertEqual(action["status"], "DENIED")
        self.assertEqual(workbench.run(action["id"])["status"], "DENIED")
        self.assertEqual(list(outside.iterdir()), [])

    def test_catalog_and_inline_tools_merge_without_losing_existing_resource_operations(self):
        outside = self.root.parent / "requirements"
        outside.mkdir()
        tool = self.knowledge_tool(outside)
        inline = {**self.knowledge_tool(outside, identifier="inline-knowledge"), "allowed_operations": ["list"]}
        payload = self.manifest()
        payload["resources"] = [inline]
        self.write_manifest(payload)
        self.write_catalog("tools", [tool])
        workbench = Workbench(self.root)
        self.assertEqual({item["id"] for item in workbench.describe()["resources"]},
                         {"requirements", "inline-knowledge"})
        self.assertEqual(workbench.call("inline-knowledge", "list")["status"], "SUCCEEDED")
        self.assertNotIn("tools", workbench.describe()["catalogs"])

    def test_duplicate_tool_ids_grants_and_incompatible_kinds_are_rejected(self):
        tool = self.knowledge_tool(self.root / "knowledge")
        original = self.manifest()
        cases = (([tool, tool], []), ([tool], [tool]),
                 ([{**tool, "allowed_operations": ["read", "read"]}], []),
                 ([{**tool, "kind": "repository"}], []))
        for tools, inline in cases:
            with self.subTest(tools=tools, inline=inline):
                self.write_manifest({**original, "resources": inline})
                self.write_catalog("tools", tools)
                with self.assertRaises(WorkbenchError):
                    Workbench(self.root)


if __name__ == "__main__":
    unittest.main()
