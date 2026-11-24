"""Load the copied skill tools without Workbench or a parent project."""

import hashlib
import importlib
import importlib.util
from pathlib import Path
import sys


def load_tool(name):
    tools = Path(__file__).resolve().parents[1] / "tools"
    namespace = "_graph_skill_tests_" + hashlib.sha256(str(tools).encode()).hexdigest()[:16]
    if namespace not in sys.modules:
        specification = importlib.util.spec_from_file_location(
            namespace, tools / "__init__.py", submodule_search_locations=[str(tools)])
        package = importlib.util.module_from_spec(specification)
        sys.modules[namespace] = package
        specification.loader.exec_module(package)
    return importlib.import_module(namespace + "." + name)
