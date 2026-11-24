"""Prepare isolated, synthetic inputs for independent skill evaluation.

This helper does not call a model, grade prose, or run business tests.
The separate rubric belongs to the assessor, not the evaluating agent.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CASES = Path(__file__).with_name("skill-evaluation-cases.json")


def git(repository, *arguments):
    return subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "-c", "user.name=Skill fixture",
         "-c", "user.email=skill-fixture@example.invalid", *arguments],
        cwd=repository, check=True, text=True, capture_output=True,
    ).stdout.strip()


def write_files(root, files, substitutions):
    for relative, content in files.items():
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Fixture paths must stay inside their output root.")
        for key, value in substitutions.items():
            content = content.replace("{{" + key + "}}", value)
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def prepare(case_id, destination, skills_root):
    catalog = json.loads(CASES.read_text(encoding="utf-8"))
    case = next(case for case in catalog["cases"] if case["id"] == case_id)
    fixture = catalog["fixtures"][case["fixture"]]
    skills = []
    for identifier in case["skills"]:
        entrypoint = skills_root / identifier / "SKILL.md"
        if not entrypoint.is_file():
            raise ValueError(f"Missing skill: {identifier}")
        skills.append({"id": identifier, "path": str(entrypoint)})

    # Refuse an existing run, including an empty directory or a symlink.
    destination.mkdir(parents=True, exist_ok=False)
    repository = destination / "repo"
    repository.mkdir()
    git(repository, "init", "-q", "--initial-branch=main")
    # Isolate fixture commits from user hooks without changing global settings.
    hooks = destination / "empty-hooks"
    hooks.mkdir()
    git(repository, "config", "core.hooksPath", str(hooks))
    write_files(repository, fixture["base"], {})
    git(repository, "add", "--all")
    git(repository, "commit", "-q", "-m", "Synthetic baseline")
    base = git(repository, "rev-parse", "HEAD")
    write_files(repository, fixture["candidate"], {})
    git(repository, "add", "--all")
    git(repository, "commit", "-q", "-m", "Synthetic candidate")
    head = git(repository, "rev-parse", "HEAD")
    substitutions = {"BASE": base, "HEAD": head}
    write_files(destination, fixture["files"], substitutions)
    prompt = case["prompt"].replace("{{ROOT}}", str(destination))
    prompt = prompt.replace("{{BASE}}", base).replace("{{HEAD}}", head)
    skill_inputs = {}
    for skill in skills:
        for source in sorted(Path(skill["path"]).parent.rglob("*.md")):
            skill_inputs[str(source)] = hashlib.sha256(source.read_bytes()).hexdigest()
    files = {
        path.relative_to(destination).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(destination.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(destination).parts
    }
    result = {
        "schema_version": 1, "case_id": case_id, "synthetic": True,
        "fixture_root": str(destination), "repository": str(repository),
        "base_revision": base, "candidate_revision": head,
        "skills": skills, "skill_inputs_sha256": skill_inputs,
        "prompt": prompt, "input_files_sha256": files,
        "limits": ["Synthetic evaluation inputs do not establish business behavior.",
                   "No model execution or semantic grading was performed by this helper."],
    }
    (destination / "evaluation-input.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    catalog = json.loads(CASES.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, choices=[case["id"] for case in catalog["cases"]])
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--skills-root", type=Path, default=ROOT / ".agents/skills")
    args = parser.parse_args()
    result = prepare(args.case, args.output.absolute(), args.skills_root.resolve())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
