"""Check Release Clinic root selection and environment precedence without external services."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock


CLINIC = Path(__file__).resolve().parents[1] / "core" / "release-clinic"
SERVICE = CLINIC / "plugins" / "test" / "dtp-tda-service"
REPORT = CLINIC / "plugins" / "test" / "dtp-tda-report" / "skills" / "dtp-tda-report" / "scripts"
_SPEC = importlib.util.spec_from_file_location("release_clinic_env_test", CLINIC / "release_clinic_env.py")
environment = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(environment)


class ReleaseClinicEnvironmentTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="release-clinic-env-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        (self.root / "workspace.yaml").write_text("schema_version: 1\n", encoding="utf-8")
        self.nested = self.root / "core" / "release-clinic" / "scripts"
        self.nested.mkdir(parents=True)
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {}, clear=True).start()
        patch.object(environment, "__file__", str(self.nested.parent / "release_clinic_env.py")).start()

    def write_env(self, content, root=None):
        path = (root or self.root) / ".env"
        path.write_text(content, encoding="utf-8")
        return path

    def test_source_root_ignores_cwd_and_nested_environment(self):
        expected = self.write_env("CLINIC_VALUE=root\n")
        self.write_env("CLINIC_VALUE=nested\nNESTED_ONLY=wrong\n", self.nested)
        with patch.object(environment.Path, "cwd", return_value=self.nested):
            path, keys = environment.load_environment()
        self.assertEqual(path, str(expected))
        self.assertEqual(keys, ["CLINIC_VALUE"])
        self.assertEqual(os.environ["CLINIC_VALUE"], "root")
        self.assertNotIn("NESTED_ONLY", os.environ)

    def test_explicit_workspace_overrides_source_checkout(self):
        self.write_env("CLINIC_VALUE=source\n")
        other = self.root / "selected-workspace"
        other.mkdir()
        expected = self.write_env("CLINIC_VALUE=selected\n", other)
        os.environ["AI_SDLC_WORKSPACE"] = str(other)
        self.assertEqual(environment.load_environment()[0], str(expected))
        self.assertEqual(os.environ["CLINIC_VALUE"], "selected")

    def test_process_values_including_empty_values_override_file(self):
        self.write_env("CLINIC_VALUE=file\nCLINIC_EMPTY=file\n")
        os.environ.update(CLINIC_VALUE="process", CLINIC_EMPTY="")
        self.assertEqual(environment.load_environment()[1], [])
        self.assertEqual(os.environ["CLINIC_VALUE"], "process")
        self.assertEqual(os.environ["CLINIC_EMPTY"], "")

    def test_root_connector_aliases_populate_collector_keys_without_file_changes(self):
        values = {
            "AZURE_DEVOPS_PAT": "test-ado-token",
            "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/example",
            "CONFLUENCE_BASE_URL": "https://confluence.example",
            "CONFLUENCE_PAT": "test-confluence-token",
            "SONAR_BASE_URL": "https://sonar.example",
            "SCWIKI_TOKEN": "test-wiki-token",
            "SCWIKI_WIKI": "test-wiki",
        }
        content = "".join(f"{key}={value}\n" for key, value in values.items())
        path = self.write_env(content)
        environment.load_environment()
        for target, source in environment._ALIASES.items():
            if source in values:
                self.assertEqual(os.environ[target], values[source])
        self.assertEqual(os.environ["ADO_ORGANIZATION"], "example")
        self.assertEqual(os.environ["ADO_ORG_URL"], values["AZURE_DEVOPS_ORG_URL"])
        self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_organization_precedence_keeps_endpoint_and_identity_together(self):
        cases = (
            ({"ADO_ORGANIZATION": "process-org"}, "AZURE_DEVOPS_ORG_URL=https://ado.example/tfs/File\n",
             "https://dev.azure.com/process-org", "process-org"),
            ({"AZURE_DEVOPS_ORG_URL": "https://ado.example/tfs/Process"}, "ADO_ORGANIZATION=file-org\n",
             "https://ado.example/tfs/Process", "Process"),
            ({"ADO_ORG_URL": "https://ado.example/tfs/Explicit", "ADO_ORGANIZATION": "metadata"},
             "AZURE_DEVOPS_ORG_URL=https://dev.azure.com/file-org\n", "https://ado.example/tfs/Explicit", "metadata"),
            ({}, "ADO_ORGANIZATION=direct-org\nAZURE_DEVOPS_ORG_URL=https://dev.azure.com/alias-org\n",
             "https://dev.azure.com/direct-org", "direct-org"),
        )
        for process, file_content, url, organization in cases:
            with self.subTest(process_keys=list(process)):
                with patch.dict(os.environ, process, clear=True):
                    self.write_env(file_content)
                    environment.load_environment()
                    self.assertEqual(os.environ["ADO_ORG_URL"], url)
                    self.assertEqual(os.environ["ADO_ORGANIZATION"], organization)

    def test_alias_precedence_preserves_process_values_across_variable_names(self):
        cases = (
            ({"ADO_TOKEN": "process-direct", "AZURE_DEVOPS_PAT": "process-alias"},
             "ADO_TOKEN=file-direct\nAZURE_DEVOPS_PAT=file-alias\n", "process-direct"),
            ({"AZURE_DEVOPS_PAT": "process-alias"}, "ADO_TOKEN=file-direct\n", "process-alias"),
            ({"ADO_TOKEN": "process-direct"}, "AZURE_DEVOPS_PAT=file-alias\n", "process-direct"),
            ({}, "ADO_TOKEN=file-direct\nAZURE_DEVOPS_PAT=file-alias\n", "file-direct"),
            ({"ADO_TOKEN": ""}, "AZURE_DEVOPS_PAT=file-alias\n", ""),
        )
        for process, file_content, expected in cases:
            with self.subTest(process_keys=list(process), expected=expected):
                with patch.dict(os.environ, process, clear=True):
                    self.write_env(file_content)
                    environment.load_environment()
                    self.assertEqual(os.environ["ADO_TOKEN"], expected)

    def test_relative_runtime_paths_resolve_from_root(self):
        self.write_env(
            "TDA_OUTPUT_DIR=generated/reports\nTDA_LOG_DIR=generated/logs\n"
            "TDA_REGISTRY_PATH=generated/registry.jsonl\n"
            "TDA_STREAM_CONFIG=config/collector.yaml\nTDA_FIELD_CONFIG=config/fields.yaml\n"
            "STREAM_CONFIG_FILE=config/service.yaml\n"
        )
        environment.load_environment()
        for name, relative in (
            ("TDA_OUTPUT_DIR", "generated/reports"), ("TDA_LOG_DIR", "generated/logs"),
            ("TDA_REGISTRY_PATH", "generated/registry.jsonl"),
            ("TDA_STREAM_CONFIG", "config/collector.yaml"), ("TDA_FIELD_CONFIG", "config/fields.yaml"),
            ("STREAM_CONFIG_FILE", "config/service.yaml"),
        ):
            self.assertEqual(os.environ[name], str(self.root / relative))

    def test_runtime_defaults_stay_within_workspace(self):
        environment.load_environment()
        self.assertEqual(os.environ["TDA_OUTPUT_DIR"], str(self.root / ".workbench/release-clinic/reports"))
        self.assertEqual(os.environ["TDA_LOG_DIR"], str(self.root / ".workbench/release-clinic/logs"))

    def test_vault_development_startup_uses_environment_without_http(self):
        session = MagicMock()
        requests = types.ModuleType("requests")
        requests.Session = lambda: session
        urllib = types.ModuleType("urllib3")
        urllib.disable_warnings = lambda *args: None
        urllib.exceptions = types.SimpleNamespace(InsecureRequestWarning=Warning)
        patch.dict(sys.modules, {"requests": requests, "urllib3": urllib}).start()
        name = "release_clinic_vault_test"
        spec = importlib.util.spec_from_file_location(name, SERVICE / "service" / "vault_client.py")
        vault = importlib.util.module_from_spec(spec)
        patch.dict(sys.modules, {name: vault}).start()
        spec.loader.exec_module(vault)
        os.environ.update(VAULT_DEV_MODE=" true ", ADO_TOKEN="test-ado", SONAR_TOKEN="test-sonar",
                          GENIE_TOKEN="test-genie", CONFLUENCE_TOKEN="test-confluence", USER_EMAIL="test@example")
        client = vault.VaultClient()
        self.assertFalse(client.is_connected)
        client.connect()
        self.assertTrue(client.is_connected)
        self.assertEqual(client.load_credentials().ado_token, "test-ado")
        session.post.assert_not_called()
        session.get.assert_not_called()
        os.environ["VAULT_DEV_MODE"] = "false"
        session.post.return_value.json.return_value = {"auth": {"client_token": "test-vault"}}
        client = vault.VaultClient()
        client.connect()
        session.post.assert_called_once()
        self.assertTrue(client.is_connected)

    def collector_config(self):
        # Crypto is optional for these offline configuration checks.
        crypto = types.ModuleType("cryptography")
        fernet = types.ModuleType("cryptography.fernet")
        fernet.Fernet = object
        patch.dict(sys.modules, {"cryptography": crypto, "cryptography.fernet": fernet,
                                 "release_clinic_env": environment}).start()
        name = "release_clinic_collector_config_test"
        spec = importlib.util.spec_from_file_location(name, REPORT / "tda" / "config.py")
        module = importlib.util.module_from_spec(spec)
        patch.dict(sys.modules, {name: module}).start()
        spec.loader.exec_module(module)
        return module

    def test_collector_routes_cloud_and_collection_api_urls(self):
        config = self.collector_config()
        base_values = {
            "AI_SDLC_WORKSPACE": str(self.root), "ADO_TOKEN": "test-token", "ADO_PROJECT": "Project",
            "SONAR_URL": "https://sonar.example", "SONAR_TOKEN": "test-token",
            "CONFLUENCE_URL": "https://confluence.example", "CONFLUENCE_TOKEN": "test-token",
            "GENIE_TOKEN": "test-token", "GENIE_REPORT_LINK": "https://genie.example", "SNOW_ENABLED": "false",
        }
        for url, organization in (
            ("https://dev.azure.com/cloud-org", "cloud-org"),
            ("https://ado.example/tfs/Collection", "Collection"),
        ):
            with self.subTest(url=url):
                with patch.dict(os.environ, {**base_values, "AZURE_DEVOPS_ORG_URL": url}, clear=True):
                    environment.load_environment()
                    actual = config.Config.from_env()
                    self.assertEqual(actual.ado_org_url, url)
                    self.assertEqual(actual.ado_organization, organization)
                    self.assertEqual(actual.ado_base_url, f"{url}/Project/_apis/")

    def test_collector_and_service_configuration_paths_stay_separate(self):
        config = self.collector_config()
        collector = self.root / "collector.yaml"
        collector.write_text("streams: {EXAMPLE: {snow_enabled: false}}\n", encoding="utf-8")
        fields = self.root / "fields.yaml"
        fields.write_text("story_type_field: Custom.TestStory\n", encoding="utf-8")
        service = self.root / "service.yaml"
        service.write_text("streams: {EXAMPLE: {pit_url_template: service-only}}\n", encoding="utf-8")
        os.environ.update(AI_SDLC_WORKSPACE=str(self.root), TDA_STREAM_CONFIG="collector.yaml",
                          TDA_FIELD_CONFIG="fields.yaml", STREAM_CONFIG_FILE="service.yaml")
        environment.load_environment()
        self.assertEqual(config._find_config_file("stream_config.yaml"), str(collector))
        self.assertEqual(config.load_ado_field_config()["story_type_field"], "Custom.TestStory")
        self.assertFalse(config._load_stream_config_yaml()["streams"]["EXAMPLE"]["snow_enabled"])
        http = types.ModuleType("tda.http_client")
        http.ADOClient = object
        patch.dict(sys.modules, {"tda": types.ModuleType("tda"), "tda.config": config,
                                 "tda.http_client": http}).start()
        spec = importlib.util.spec_from_file_location("clinic_build_resolver_test", REPORT / "tda" / "build_resolver.py")
        resolver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(resolver)
        self.assertEqual(resolver._find_yaml("stream_config.yaml"), str(collector))
        spec = importlib.util.spec_from_file_location("clinic_service_streams_test", SERVICE / "service" / "stream_config.py")
        streams = importlib.util.module_from_spec(spec)
        patch.dict(sys.modules, {spec.name: streams}).start()
        spec.loader.exec_module(streams)
        self.assertEqual(streams.StreamConfigStore().get("EXAMPLE").pit_url_template, "service-only")
        os.environ["TDA_STREAM_CONFIG"] = "missing.yaml"
        with self.assertRaisesRegex(FileNotFoundError, "TDA_STREAM_CONFIG"):
            config._find_config_file("stream_config.yaml")

    def test_missing_root_file_does_not_fall_back_to_nested_file(self):
        self.write_env("NESTED_ONLY=wrong\n", self.nested)
        self.assertEqual(environment.load_environment(), (None, []))
        self.assertNotIn("NESTED_ONLY", os.environ)

    def test_explicit_file_resolves_from_root_and_does_not_fall_back(self):
        expected = self.root / "settings.env"
        expected.write_text("CLINIC_VALUE=selected\n", encoding="utf-8")
        os.environ["AI_SDLC_ENV_FILE"] = "settings.env"
        self.assertEqual(environment.load_environment()[0], str(expected))
        os.environ["AI_SDLC_ENV_FILE"] = "missing.env"
        self.write_env("CLINIC_VALUE=wrong\n")
        with self.assertRaises(FileNotFoundError):
            environment.load_environment()

    def test_relative_workspace_is_rejected(self):
        os.environ["AI_SDLC_WORKSPACE"] = "relative-workspace"
        with self.assertRaisesRegex(ValueError, "absolute"):
            environment.load_environment()

    def test_export_quotes_comments_and_proxy_precedence(self):
        self.write_env(
            '\ufeffexport CLINIC_QUOTED="value # retained" # ignored\n'
            "CLINIC_UNQUOTED=value # ignored\n"
            "NO_PROXY=localhost,127.0.0.1\n"
            "INVALID KEY=ignored\n"
        )
        os.environ["no_proxy"] = "process.example"
        environment.load_environment()
        self.assertEqual(os.environ["CLINIC_QUOTED"], "value # retained")
        self.assertEqual(os.environ["CLINIC_UNQUOTED"], "value")
        self.assertEqual(os.environ["no_proxy"], "process.example")
        self.assertNotIn("INVALID KEY", os.environ)

    def test_portfolio_entrypoint_uses_root_environment_from_nested_cwd(self):
        registry = self.root / "expected.jsonl"
        registry.write_text("", encoding="utf-8")
        self.write_env(f"TDA_REGISTRY_PATH={registry}\n")
        self.write_env("TDA_REGISTRY_PATH=wrong.jsonl\n", self.nested)
        result = subprocess.run(
            [sys.executable, str(SERVICE / "scripts" / "aggregate_portfolio.py")],
            cwd=self.nested,
            env={"AI_SDLC_WORKSPACE": str(self.root)},
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(result.stdout)["meta"]["registry_path"], str(registry))

    def test_service_loads_root_settings_before_runner_and_logging_imports(self):
        self.write_env("TDA_OUTPUT_DIR=/selected-output\nTDA_LOG_DIR=/selected-logs\n")
        self.write_env("TDA_OUTPUT_DIR=/wrong-output\n", self.nested)
        # Replace external web/Vault dependencies. Import the real service entrypoint and runner.
        probe = r'''
import json
import os
import sys
import types

sys.path.insert(0, sys.argv[1])

class Application:
    def __init__(self, **kwargs):
        pass
    def get(self, *args, **kwargs):
        return lambda function: function
    post = get

def module(name, **members):
    result = types.ModuleType(name)
    result.__dict__.update(members)
    sys.modules[name] = result

module('fastapi', FastAPI=Application, HTTPException=RuntimeError)
module('fastapi.responses', FileResponse=object)
module('service.job_runner', JobRunner=object)
module('service.job_store', JobStore=object)
module('service.logging_config', configure_logging=lambda: os.environ.get('TDA_LOG_DIR'))
module('service.models', **{name: object for name in (
    'HealthResponse', 'JobLogsResponse', 'JobStatus', 'JobStatusResponse',
    'JobSubmitResponse', 'TDAJobRequest')})
module('service.stream_config', StreamConfigStore=object)
module('service.vault_client', VaultClient=object)

import service.main
import service.runner
print(json.dumps({'output': service.runner.get_output_dir(), 'logs': service.main._log_path}))
'''
        result = subprocess.run(
            [sys.executable, "-c", probe, str(SERVICE)],
            cwd=self.nested,
            env={"AI_SDLC_WORKSPACE": str(self.root)},
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(result.stdout), {"output": "/selected-output", "logs": "/selected-logs"})

    def test_audit_entrypoints_accept_root_environment_without_nested_file(self):
        self.write_env("CLINIC_VALUE=selected-root\n")
        probe = r'''
import os
from pathlib import Path
import runpy
import sys
import types

sys.path.insert(0, sys.argv[1])
from release_clinic_env import load_environment

class Complete(Exception):
    pass

class Client:
    def __init__(self, configuration):
        assert os.environ['CLINIC_VALUE'] == 'selected-root'
        raise Complete()

configuration = types.ModuleType('tda.config')
configuration.load_env_file = load_environment
configuration.Config = type('Config', (), {'from_env': staticmethod(lambda: object())})
http_client = types.ModuleType('tda.http_client')
http_client.ADOClient = Client
sys.modules['tda'] = types.ModuleType('tda')
sys.modules['tda.config'] = configuration
sys.modules['tda.http_client'] = http_client
script = sys.argv[2]
sys.argv = [script] + sys.argv[3:]
try:
    runpy.run_path(script, run_name='__main__')
except Complete:
    print('ROOT_ENVIRONMENT_REACHED_CLIENT')
'''
        for script, arguments in (
            ("run_tda_audit.py", ["--attachments", str(self.root / "attachments")]),
            ("rwi_tda_presence_check.py", ["--output", str(self.root / "presence.html")]),
        ):
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, "-c", probe, str(CLINIC), str(REPORT / "tda_audit" / script), *arguments],
                    cwd=self.nested,
                    env={"AI_SDLC_WORKSPACE": str(self.root)},
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertIn("ROOT_ENVIRONMENT_REACHED_CLIENT", result.stdout)


if __name__ == "__main__":
    unittest.main()
