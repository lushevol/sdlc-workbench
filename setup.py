"""Ship the canonical workspace files without maintaining a second source copy."""

import json
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWorkspace(build_py):
    def run(self):
        package_target = Path(self.build_lib) / "ai_sdlc_workbench"
        if package_target.exists():
            shutil.rmtree(package_target)
        super().run()
        root = Path(__file__).resolve().parent
        target = package_target / "scaffold"
        target.mkdir(parents=True)
        shutil.copy2(root / "scaffold.json", target / "scaffold.json")
        manifest = json.loads((root / "scaffold.json").read_text(encoding="utf-8"))
        alias_paths = {root / relative for relative in manifest.get("skill_aliases", {})}

        def ignore(directory, names):
            return [name for name in names if name == "__pycache__" or name.endswith(".pyc")
                    or Path(directory) / name in alias_paths]

        for relative in manifest["paths"]:
            source = root / relative
            destination = target / relative
            if source.is_dir():
                shutil.copytree(source, destination, ignore=ignore)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)


setup(cmdclass={"build_py": BuildWorkspace})
