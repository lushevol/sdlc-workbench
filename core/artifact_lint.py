"""Read-only lint for SDLC authoring documents, separate from knowledge governance."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator, FormatChecker
import yaml

from .context.catalogs import UniqueKeyLoader
from .governance.schemas import CRITERION
from .models import WorkbenchError


_MAX_BYTES = 1024 * 1024
_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z", re.S)
_PLACEHOLDER = re.compile(r"\{\{[^{}\n]+\}\}")
_SAMPLE_ID = re.compile(r"(?<![A-Za-z0-9_.:-])SAMPLE-[A-Za-z0-9][A-Za-z0-9_.:-]*")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_HEADING = re.compile(r"^ {0,3}##[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")
_FORMATS = FormatChecker()
_LIMITATIONS = [
    "Lint checks authoring structure and selected BDD rules; it does not establish business correctness.",
    "Review fields are recorded claims. Lint does not authenticate reviewers or grant approval.",
    "Source references are not fetched or authenticated. Lint does not prove provenance or runtime relationships.",
    "Markdown checks cover selected structures; lint is not a complete CommonMark parser.",
    "Gherkin checks cover an English subset. No business step definitions execute.",
    "Lint does not establish complete ASD-STE100 compliance or passing business execution.",
]


@_FORMATS.checks("date-time")
def _date_time(value):
    if not isinstance(value, str):
        return True  # JSON Schema type validation handles non-text values.
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except ValueError:
        return False


def artifact_schema() -> dict:
    """Return the installed authoring contract, independent of workspace copies."""
    path = Path(__file__).parent / "schemas" / "sdlc-artifact.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml_object(text, *, object_required=True):
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
        json.dumps(value, allow_nan=False)
        if object_required and not isinstance(value, dict):
            raise WorkbenchError("YAML must contain an object.")
        return value
    except (yaml.YAMLError, TypeError, ValueError, RecursionError) as error:
        raise WorkbenchError("Use unique YAML keys and finite JSON-compatible values; quote timestamps.") from error


def _visible_line(line, comment):
    """Remove HTML comments while preserving escapes and matched inline code."""
    visible, position = [], 0
    while position < len(line):
        if comment:
            end = line.find("-->", position)
            if end < 0:
                break
            position, comment = end + 3, False
        elif line[position] == "\\" and position + 1 < len(line):
            visible.append(line[position:position + 2])
            position += 2
        elif line[position] == "`":
            delimiter = re.match(r"`+", line[position:]).group()
            end = re.search(r"(?<!`)" + re.escape(delimiter) + r"(?!`)", line[position + len(delimiter):])
            stop = position + len(delimiter) + end.end() if end else position + len(delimiter)
            visible.append(line[position:stop])
            position = stop
        elif line.startswith("<!--", position):
            position, comment = position + 4, True
        else:
            visible.append(line[position])
            position += 1
    return "".join(visible), comment


def _sections(body, report):
    """Collect real headings and code blocks without accepting fenced headings."""
    sections, blocks = {}, []
    current, fence, language, content = None, None, "", []
    comment = False
    for number, line in enumerate(body.splitlines(), 1):
        if fence is None:
            line, comment = _visible_line(line, comment)
        marker = _FENCE.match(line)
        if marker:
            token, suffix = marker.groups()
            if fence is None:
                fence, language, content = token, suffix.strip().split(" ")[0].lower(), []
            elif token[0] == fence[0] and len(token) >= len(fence) and not suffix.strip():
                blocks.append((language, "\n".join(content)))
                fence = None
            else:
                content.append(line)
            if current is not None:
                sections[current].append(line)
            continue
        if fence is not None:
            content.append(line)
        heading = _HEADING.match(line) if fence is None else None
        if heading:
            current = heading.group(1).strip()
            if current in sections:
                report("duplicate_section", f"Required section '{current}' must occur once.", line=number)
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    if fence is not None:
        report("unclosed_fence", "Close every Markdown code fence.")
    if comment:
        report("unclosed_comment", "Close every HTML comment outside code fences.")
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}, blocks


def _meaningful(text):
    # _sections already removes real comments outside code. Literal code remains content.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if _FENCE.match(line):
            continue
        if line.startswith("|"):
            cells = line.strip("|").split("|")
            if all(not cell.strip() for cell in cells):
                continue
            if all(re.fullmatch(r"[\s:-]+", cell) for cell in cells):
                continue
            if index + 1 < len(lines) and lines[index + 1].startswith("|"):
                next_cells = lines[index + 1].strip("|").split("|")
                if all(re.fullmatch(r"[\s:-]+", cell) for cell in next_cells):
                    continue
        if line:
            return True
    return False


def _gherkin(text, report):
    """Check the documented English subset without pretending to execute Gherkin."""
    features, scenarios, background, rule_background = 0, [], [], []
    current, examples, in_rule, doc_string = None, None, False, None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if doc_string is not None:
            if line == doc_string:
                doc_string = None
            continue
        if line.startswith(('"""', "'''")):
            doc_string = line[:3]
            continue
        if not line or line.startswith(("#", "@")):
            continue
        match = re.match(r"^(Feature|Rule|Background|Scenario Outline|Scenario|Examples):\s*(.*)$", line)
        if match:
            kind, title = match.groups()
            if features == 0 and kind != "Feature":
                report("gherkin_feature_order", "Place Feature before Rule, Background, Scenario, and Examples.", line=number)
            if not title and kind not in {"Examples", "Background"}:
                report("gherkin_title", f"Add a title after {kind}.", line=number)
            if kind == "Feature":
                features += 1
                current = None
            elif kind == "Rule":
                in_rule, rule_background, current = True, [], None
            elif kind == "Background":
                current = {"kind": kind, "steps": [], "line": number}
                if in_rule:
                    rule_background = current["steps"]
                else:
                    background = current["steps"]
            elif kind in {"Scenario", "Scenario Outline"}:
                current = {"kind": kind, "steps": [], "line": number, "examples": [],
                           "background": list(background) + list(rule_background)}
                scenarios.append(current)
            elif current is None or current["kind"] != "Scenario Outline":
                report("gherkin_examples", "Examples must belong to a Scenario Outline.", line=number)
            else:
                examples = []
                current["examples"].append(examples)
            if kind != "Examples":
                examples = None
            continue
        if line.startswith("|") and examples is not None:
            if not line.endswith("|"):
                report("gherkin_examples", "Close each Examples row with '|'.", line=number)
            examples.append([cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]])
            continue
        step = re.match(r"^(Given|When|Then|And|But|\*)\s+(.+)$", line)
        if step:
            if current is None:
                report("gherkin_step", "Place steps inside a Scenario or Background.", line=number)
                continue
            keyword, clause = step.groups()
            if keyword in {"And", "But", "*"}:
                prior = current["steps"] or current.get("background", [])
                keyword = prior[-1][0] if prior else ""
            current["steps"].append((keyword, clause))
            if current["kind"] == "Background" and keyword != "Given":
                report("gherkin_background", "Use Given conditions in Background.", line=number)
    if doc_string is not None:
        report("gherkin_doc_string", "Close the Gherkin Doc String.")
    if features != 1:
        report("gherkin_feature", "Each Gherkin block needs exactly one Feature.")
    if not scenarios:
        report("gherkin_scenario", "Add at least one Scenario.")
    for scenario in scenarios:
        steps = scenario["background"] + scenario["steps"]
        keywords = [keyword for keyword, _ in steps]
        if any(keyword not in keywords for keyword in ("Given", "When", "Then")):
            report("gherkin_steps", "Each scenario needs Given, When, and Then conditions, actions, and results.", line=scenario["line"])
        ranks = [{"Given": 0, "When": 1, "Then": 2}.get(keyword, -1) for keyword in keywords]
        if -1 in ranks or ranks != sorted(ranks):
            report("gherkin_order", "Order steps as Given, When, and Then; And and But inherit their preceding clause.", line=scenario["line"])
        if scenario["kind"] == "Scenario Outline":
            parameters = set(re.findall(r"<([^<>]+)>", " ".join(clause for _, clause in steps)))
            if not scenario["examples"]:
                report("gherkin_examples", "Scenario Outline needs an Examples table with data rows.", line=scenario["line"])
            for rows in scenario["examples"]:
                if len(rows) < 2 or not rows[0] or any(not cell for cell in rows[0]):
                    report("gherkin_examples", "Examples needs nonempty column names and at least one data row.", line=scenario["line"])
                    continue
                if len(rows[0]) != len(set(rows[0])) or not parameters.issubset(rows[0]):
                    report("gherkin_examples", "Examples columns must be unique and contain every outline parameter.", line=scenario["line"])
                if any(len(row) != len(rows[0]) for row in rows[1:]):
                    report("gherkin_examples", "Every Examples row must match the header width.", line=scenario["line"])


def _criteria(metadata, blocks, report):
    criteria_sets = []
    if "acceptance_criteria" in metadata:
        criteria_sets.append(metadata["acceptance_criteria"])
    gherkin = []
    for language, text in blocks:
        if language in {"yaml", "yml"}:
            try:
                value = _yaml_object(text, object_required=False)
                if isinstance(value, dict) and "acceptance_criteria" in value:
                    criteria_sets.append(value["acceptance_criteria"])
            except WorkbenchError as error:
                report("yaml_invalid", str(error))
        elif language == "gherkin":
            gherkin.append(text)
            _gherkin(text, report)
    kind = metadata.get("artifact_kind")
    if kind in {"requirement", "nonfunctional-requirement", "bdd-feature"} and not gherkin:
        report("gherkin_missing", "Add a fenced Gherkin specification for this artifact kind.")
    if kind in {"requirement", "nonfunctional-requirement"} and not criteria_sets:
        report("criteria_missing", "Add structured acceptance_criteria with measurable Given, When, and Then clauses.")
    validator = Draft202012Validator({"type": "array", "minItems": 1, "items": CRITERION})
    for criteria in criteria_sets:
        errors = list(validator.iter_errors(criteria))
        for error in errors:
            report("criteria_schema", "acceptance_criteria: " + error.message)
        if errors:
            continue
        identifiers = set()
        for criterion in criteria:
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", criterion["id"]):
                report("criterion_id", "Use a stable acceptance criterion ID without whitespace or path separators.")
            if criterion["id"] in identifiers:
                report("criterion_duplicate", "Acceptance criterion IDs must be unique.")
            identifiers.add(criterion["id"])
            for field, keyword in (("given", "Given"), ("when", "When"), ("then", "Then")):
                if not re.match(rf"^{keyword}\s+\S", criterion[field]):
                    report("criterion_clause", f"Start each {field} clause with {keyword} and meaningful text.")
            if any(not isinstance(value, str) or not value.strip() for value in
                   (criterion["id"], criterion["measure"]["metric"], criterion["measure"]["unit"])):
                report("criterion_measure", "Criterion IDs, metrics, and units must contain nonblank text.")
    if len(criteria_sets) > 1 and any(criteria != criteria_sets[0] for criteria in criteria_sets[1:]):
        report("criteria_conflict", "Repeated structured acceptance criteria must match.")


def lint_artifacts(paths: list[str | Path], *, strict: bool = False) -> dict:
    """Lint explicit files or artifact-only directories without loading a workspace."""
    findings, selected, identities = [], {}, {}

    def report(path, code, message, severity="error", **details):
        findings.append({"path": str(path), "code": code, "severity": severity, "message": message, **details})

    def select(path, boundary=None):
        if path.is_symlink() or (boundary is not None and not path.resolve().is_relative_to(boundary)):
            report(path, "unsafe_path", "Use artifact files within the selected directory; do not follow symbolic links.")
        elif path.is_file() and path.suffix.lower() == ".md":
            selected.setdefault(path.resolve(), path)

    if not paths:
        report("", "inputs_required", "Select at least one Markdown artifact or artifact-only directory.")
    for supplied in paths:
        path = Path(supplied).expanduser().absolute()
        try:
            if path.is_symlink():
                report(path, "unsafe_path", "Select an actual artifact path instead of a symbolic link.")
            elif path.is_dir():
                boundary, before = path.resolve(), len(selected)
                candidates = sorted(path.rglob("*"))
                found_markdown = False
                for candidate in candidates:
                    if candidate.suffix.lower() == ".md" and candidate.is_file() and not candidate.is_symlink():
                        found_markdown = True
                    if candidate.is_symlink() or candidate.suffix.lower() == ".md":
                        select(candidate, boundary)
                if not found_markdown and len(selected) == before:
                    report(path, "artifacts_missing", "The selected directory contains no Markdown artifacts.")
            elif not path.is_file():
                report(path, "path_missing", "Select an existing readable Markdown file or directory.")
            elif path.suffix.lower() != ".md":
                report(path, "extension_invalid", "Authoring artifacts must use the .md extension.")
            else:
                select(path)
        except (OSError, ValueError, RuntimeError):
            report(path, "path_invalid", "The artifact path could not be inspected.")

    validator = Draft202012Validator(artifact_schema(), format_checker=_FORMATS)
    for _, path in sorted(selected.items(), key=lambda item: str(item[0])):
        emit = lambda code, message, severity="error", **details: report(path, code, message, severity, **details)
        try:
            with path.open("rb") as stream:
                raw = stream.read(_MAX_BYTES + 1)
            if len(raw) > _MAX_BYTES:
                raise WorkbenchError("Artifacts must not exceed one MiB.")
            text = raw.decode("utf-8")
            match = _FRONTMATTER.match(text)
            if not match:
                raise WorkbenchError("Start an authored artifact with YAML frontmatter. Copy the Template block, not the whole guide.")
            metadata = _yaml_object(match.group(1))
            sections, blocks = _sections(match.group(2), emit)
            for error in validator.iter_errors({"metadata": metadata, "sections": sections}):
                location = ".".join(str(part) for part in error.absolute_path)
                emit("artifact_schema", f"{location or 'artifact'}: {error.message}")
            for heading, content in sections.items():
                if not _meaningful(content):
                    emit("section_empty", f"Section '{heading}' needs meaningful text, table data, or code.")
            if _PLACEHOLDER.search(text):
                emit("placeholder_unresolved", "Replace every {{placeholder}} with supported content or an explicit unknown value.")
            identifier = metadata.get("id")
            if isinstance(identifier, str):
                if identifier in identities:
                    emit("artifact_duplicate", f"Artifact ID '{identifier}' also occurs in {identities[identifier]}.")
                identities[identifier] = str(path)
            _criteria(metadata, blocks, emit)
            owner = metadata.get("owner")
            if isinstance(owner, str) and owner.strip().casefold() == "unknown":
                emit("owner_unknown", "Artifact owner is unknown. Identify the responsible owner.", "warning")
            if metadata.get("source_refs") == []:
                emit("sources_missing", "No source references are recorded. Identify the supporting source revisions.", "warning")
            sample_reference = any(
                isinstance(references, list) and any(
                    isinstance(reference, str) and reference.startswith("SAMPLE-") for reference in references)
                for references in (metadata.get("source_refs"), metadata.get("related_ids")))
            if (isinstance(identifier, str) and identifier.startswith("SAMPLE-")) or sample_reference or _SAMPLE_ID.search(text):
                emit("sample_content", "Sample identifiers and references are illustrative; replace them before real use.", "warning")
            review = metadata.get("review")
            if isinstance(review, dict) and review.get("state") == "pending":
                emit("review_pending", "Business review remains pending. Record actual review before applicable publication.", "warning")
            writing = metadata.get("writing_review")
            if isinstance(writing, dict) and writing.get("asd_review") != "PASSED":
                emit("writing_review_pending", "Full ASD writing review remains pending or failed. Automated lint cannot complete that review.", "warning")
            if re.search(r"\b(?:unknown|TBD|TODO)\b", match.group(2), re.I):
                emit("unresolved_content", "The body contains unresolved values. Read the findings and obtain missing inputs.", "warning")
        except (WorkbenchError, OSError, UnicodeError, RecursionError, TypeError, ValueError) as error:
            emit("artifact_invalid", str(error) if isinstance(error, WorkbenchError) else "Use a readable UTF-8 artifact with JSON-compatible metadata.")

    findings.sort(key=lambda item: (item["path"], item["severity"], item["code"], item["message"], item.get("line", 0)))
    failed = any(item["severity"] == "error" or strict for item in findings)
    return {"schema_version": 1, "status": "FAILED" if failed else "PASSED", "valid": not failed,
            "artifacts": len(selected), "findings": findings, "limitations": list(_LIMITATIONS)}
