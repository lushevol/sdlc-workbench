"""Local defense-in-depth policy; Rundeck ACLs remain authoritative."""
import json
from pathlib import Path

class PolicyError(Exception):
    pass

class Policy:
    def __init__(self, config):
        if not isinstance(config, dict):
            raise PolicyError("Policy must be a JSON object")
        self.config = config

    @classmethod
    def load(cls, filename=None):
        path = Path(filename) if filename else Path(__file__).with_name("policy.json")
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def max_items(self):
        return self._positive_int("max_list_items", 100, 500)

    def max_log_lines(self):
        return self._positive_int("max_log_lines", 200, 1000)

    def max_response_bytes(self):
        return self._positive_int("max_response_bytes", 1048576, 5 * 1048576)

    def _positive_int(self, key, default, maximum):
        value = self.config.get(key, default)
        if type(value) is not int or not 1 <= value <= maximum:
            raise PolicyError(f"Invalid {key}: expected integer between 1 and {maximum}")
        return value

    def check_project(self, name):
        allowed = self.config.get("allowed_projects", [])
        if not isinstance(allowed, list) or not all(isinstance(v, str) for v in allowed):
            raise PolicyError("allowed_projects must be an array of names")
        # Empty array: read-only operations across projects allowed by Rundeck ACLs.
        if allowed and name not in allowed:
            raise PolicyError("Project is not in the local allowlist")

    def check_definition(self):
        if self.config.get("enable_job_definition_read") is not True:
            raise PolicyError("Job definition export disabled in policy.json")

    def check_execution(self, project, job_id, options):
        if self.config.get("enable_job_execution") is not True:
            raise PolicyError("Job execution is disabled in policy.json")
        self.check_project(project)
        jobs = self.config.get("executable_jobs", {})
        if not isinstance(jobs, dict) or job_id not in jobs:
            raise PolicyError("Job ID is not in the execution allowlist")
        rule = jobs[job_id]
        if not isinstance(rule, dict) or rule.get("project") != project:
            raise PolicyError("Job/project combination is not allowed")
        allowed_options = rule.get("allowed_options", [])
        if not isinstance(allowed_options, list) or not all(isinstance(x, str) for x in allowed_options):
            raise PolicyError("Invalid allowed_options policy")
        if set(options) - set(allowed_options):
            raise PolicyError("One or more job options are not allowlisted")
