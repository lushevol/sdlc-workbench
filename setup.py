"""Ship the canonical workspace files without maintaining a second source copy."""

import json
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWorkspace(build_py):
    def run(self):
        super().run()
        root = Path(__file__).resolve().parent
        target = Path(self.build_lib) / "ai_sdlc_workbench" / "scaffold"
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        shutil.copy2(root / "scaffold.json", target / "scaffold.json")
        for relative in json.loads((root / "scaffold.json").read_text(encoding="utf-8"))["paths"]:
            source = root / relative
            destination = target / relative
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)


setup(cmdclass={"build_py": BuildWorkspace})
