"""Opt-in, read-only UI Gherkin checks. Evidence reviews remain recorded claims."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator

from .artifact_lint import _FENCE, _FORMATS, _gherkin, _visible_line


_MAX_BYTES = 8 * 1024 * 1024
COMPONENT_TYPES = (
    "icon button", "button", "link", "textbox", "text input", "textarea", "combobox", "dropdown",
    "option", "menu item", "menu", "checkbox", "radio button", "switch", "tab", "tablist", "dialog", "modal",
    "tooltip", "data grid", "table", "row", "column", "cell", "label", "text", "heading",
    "status indicator", "status text", "notification", "alert", "toast", "date picker", "search field",
    "tree item", "tree", "list item", "list", "section", "image", "tabpanel", "spinbutton", "chip", "backdrop",
    "drawer panel",
)
_COMPONENT = re.compile(r"\b(?:" + "|".join(re.escape(item) for item in COMPONENT_TYPES) + r")\b", re.I)
_ACTION = re.compile(
    r"\b(?:clicks?|taps?|press(?:es)?|enters?|types?|selects?|checks?|unchecks?|toggles?|hovers?|"
    r"drags?|drops?|focus(?:es)?|uploads?|scrolls?|opens?|closes?|clears?|pastes?|fills?|replaces?|"
    r"moves?(?=\s+(?:the\s+)?(?:mouse|pointer|cursor)\b))\b", re.I)
_SCOPE = re.compile(
    r"\b(?:in|inside|within|on|from|into)\b.+\b(?:page|dialog|modal|panel|form|menu|row|region|section|"
    r"tab|tablist|tabpanel|table|grid|list|window|sidebar|toolbar|tree|drawer|application bar)\b", re.I)
_IDENTITY = re.compile(r'"[^"\n]+"|`[^`\n]+`|\b(?:test ID|testid|identifier)\s+\S+', re.I)
_VAGUE = re.compile(
    r"\b(?:works? correctly|(?:operation|action|request) (?:is successful|succeeds)|"
    r"correct (?:information|result|data)|expected (?:result|outcome)|session (?:is |has been )?extended|"
    r"(?:page|application) (?:shows?|displays?) success)\b", re.I)
_OBSERVABLE = re.compile(
    r"\b(?:visible|hidden|absent|displayed|disabled|enabled|focused|checked|unchecked|selected|"
    r"equals?|contains?|matches?|disappears?|remains? authenticated|accessible|valid|invalid|"
    r"returns? (?:HTTP )?\d{3}|(?:is|are) (?:true|false|null|empty))\b", re.I)
_STEP = re.compile(r"^\s*(Given|When|Then|And|But|\*)\s+(.+)$")
_DECLARATION = re.compile(r"^\s*(Feature|Rule|Background|Scenario Outline|Scenario|Examples):\s*(.*)$")
_LIMITATIONS = [
    "Checks cover a documented English Gherkin subset and selected UI wording rules, not complete Cucumber syntax.",
    "Hashes and line bounds confirm local source bytes, not semantic truth, source authority, or reviewer identity.",
    "PASS relies on recorded evidence and semantic reviews. The checker does not inspect a live DOM or execute bindings.",
    "Automation readiness is a reviewed mapping claim. It does not establish business approval or passing execution.",
    "Outline rows share reviewed bindings; actual parameter handling and assertion semantics require review.",
]


def evidence_schema():
    return json.loads((Path(__file__).parent / "schemas" / "gherkin-evidence.schema.json").read_text(encoding="utf-8"))


def _read(path):
    if path.stat().st_size > _MAX_BYTES:
        raise ValueError("Input exceeds the eight MiB size limit.")
    return path.read_bytes()


def _local(root, name):
    path = Path(name)
    if path.is_absolute():
        raise ValueError("Use a path relative to the evidence root.")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Evidence paths must stay inside the evidence root, including symbolic links.")
    return resolved


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _blocks(text, suffix, report):
    if suffix == ".feature":
        return [(text, 0)]
    blocks, content, fence, language, start, comment = [], [], None, "", 0, False
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw
        if fence is None:
            line, comment = _visible_line(line, comment)
        marker = _FENCE.match(line)
        if marker:
            token, rest = marker.groups()
            if fence is None:
                fence, language, start, content = token, rest.strip().split(" ")[0].lower(), number, []
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip():
                if language == "gherkin":
                    blocks.append(("\n".join(content), start))
                fence = None
            else:
                content.append(raw)
        elif fence is not None:
            content.append(raw)
    if fence is not None:
        report("FAIL", "markdown_fence", "A Markdown fence is not closed.", "Close the fence.", line=start)
    if comment:
        report("FAIL", "markdown_comment", "An HTML comment is not closed.", "Close the comment.")
    if not blocks:
        report("FAIL", "gherkin_missing", "No Gherkin specification was found.", "Add a fenced gherkin block.")
    return blocks


def _scenarios(text, offset, report):
    """Retain original line numbers, inherited backgrounds, and step arguments."""
    scenarios, feature_background, rule_background = [], [], []
    current, background, in_rule, tags, prior, doc, examples = None, None, False, [], None, None, False
    for number, raw in enumerate(text.splitlines(), offset + 1):
        line = raw.strip()
        if doc is not None:
            if line == doc:
                doc = None
            continue
        if line.startswith(('"""', "'''")):
            if prior is None:
                report("FAIL", "gherkin_argument", "A Doc String has no step.", "Attach the argument to a step.", line=number)
            doc = line[:3]
            continue
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            tags.extend(line.split())
            continue
        declaration = _DECLARATION.match(line)
        if declaration:
            kind, title = declaration.groups()
            prior, examples = None, kind == "Examples"
            if kind == "Feature":
                feature_background, rule_background, in_rule, current, background = [], [], False, None, None
            elif kind == "Rule":
                rule_background, in_rule, current, background = [], True, None, None
            elif kind == "Background":
                background = []
                if in_rule:
                    rule_background = background
                else:
                    feature_background = background
                current = None
            elif kind in {"Scenario", "Scenario Outline"}:
                inherited = list(feature_background) + list(rule_background)
                current = {"id": tags[-1][1:] if tags else None, "title": title, "line": number,
                           "steps": inherited, "outline": kind == "Scenario Outline"}
                scenarios.append(current)
                background = None
            tags = []
            continue
        match = _STEP.match(raw)
        if match:
            keyword, clause = match.groups()
            steps = current["steps"] if current is not None else background
            if steps is None:
                continue  # Existing structural checks report this error.
            inherited = steps[-1]["keyword"] if steps else ""
            keyword = inherited if keyword in {"And", "But", "*"} else keyword
            prior = {"line": number, "keyword": keyword, "text": clause}
            steps.append(prior)
            continue
        if line.startswith("|") and (examples or prior is not None):
            if not line.endswith("|"):
                report("FAIL", "gherkin_argument", "A data row has no closing separator.", "Close the row with '|'.", line=number)
            continue
        if prior is not None or current is not None:
            report("FAIL", "gherkin_unrecognized", "Text after scenario steps is outside the supported syntax.",
                   "Use an English step, comment, table, or Doc String; review other dialects separately.", line=number,
                   scenario_id=current["id"] if current else None)
    return scenarios


def _status(findings):
    for state in ("FAIL", "UNVERIFIED", "WARNING"):
        if any(item["status"] == state for item in findings):
            return state
    return "PASS"


def check_gherkin(paths, *, manifest=None, root=None, strict=False, scenario_ids=None):
    """Check explicit files. Missing evidence cannot silently produce PASS."""
    findings, results, source_cache, source_excerpts, documents = [], [], {}, {}, []

    def report(status, rule, explanation, correction, *, path=None, line=None, scenario_id=None, evidence=None):
        findings.append({"status": status, "rule": rule, "path": str(path) if path else None,
                         "scenario_id": scenario_id, "line": line, "explanation": explanation,
                         "correction": correction, "evidence": evidence or []})

    data = {"evidence": {}, "scenarios": {}}
    try:
        evidence_root = Path(root).resolve() if root else (Path(manifest).resolve().parent if manifest else Path.cwd().resolve())
    except (OSError, ValueError, RuntimeError) as error:
        report("FAIL", "root_invalid", str(error), "Select a valid evidence root.")
        evidence_root = Path.cwd().resolve()
    if manifest:
        try:
            raw_manifest = _read(Path(manifest)).decode("utf-8")
            candidate = json.loads(raw_manifest, object_pairs_hook=_unique_pairs,
                                   parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"Nonfinite JSON: {value}")))
            errors = list(Draft202012Validator(evidence_schema(), format_checker=_FORMATS).iter_errors(candidate))
            if errors:
                for error in errors[:20]:
                    report("FAIL", "manifest_schema", error.message,
                           "Follow the installed Gherkin evidence schema.", path=manifest,
                           evidence=["/" + "/".join(str(part) for part in error.absolute_path)])
            else:
                data = candidate
        except (OSError, UnicodeError, ValueError, RecursionError, RuntimeError) as error:
            report("FAIL", "manifest_invalid", str(error), "Supply a readable, unique-key JSON manifest.", path=manifest)

    def evidence_refs(refs, emit, *, kind=None, authoritative=False):
        if not refs:
            emit("UNVERIFIED", "evidence_missing", "Supporting evidence is missing.", "Record exact source lines and file hashes.")
            return False
        valid = True
        for ref in refs:
            source = data["evidence"].get(ref)
            if source is None:
                emit("UNVERIFIED", "evidence_unknown", f"Evidence '{ref}' is not defined.", "Define this source or correct its ID.", evidence=[ref])
                valid = False
                continue
            if ref not in source_cache:
                try:
                    path = _local(evidence_root, source["path"])
                    payload = _read(path)
                    lines = payload.decode("utf-8").splitlines()
                    if hashlib.sha256(payload).hexdigest() != source["sha256"]:
                        raise ValueError("Source bytes differ from the recorded SHA-256.")
                    if not 1 <= source["start_line"] <= source["end_line"] <= len(lines):
                        raise ValueError("Source line range is outside the recorded file.")
                    source_cache[ref] = None
                    source_excerpts[ref] = "\n".join(lines[source["start_line"] - 1:source["end_line"]])
                except (OSError, UnicodeError, ValueError, RuntimeError) as error:
                    source_cache[ref] = str(error)
            if source_cache[ref]:
                emit("UNVERIFIED", "evidence_stale", source_cache[ref], "Inspect the source and renew its evidence record.", evidence=[ref])
                valid = False
            if kind and source["kind"] != kind:
                emit("UNVERIFIED", "evidence_kind", f"Evidence '{ref}' does not identify {kind} evidence.",
                     "Link evidence for the required responsibility.", evidence=[ref])
                valid = False
            if authoritative and source["authority"] not in {"approved", "established"}:
                emit("UNVERIFIED", "expectation_authority", "The expectation has draft or unknown authority.",
                     "Resolve intent or label this case as a proposal.", evidence=[ref])
                valid = False
        return valid

    def review(value, emit, rule):
        if not value or value["state"] != "PASS" or not value["reviewer"] or not value["reviewed_at"]:
            emit("UNVERIFIED", rule, "A complete evidence review is not recorded.",
                 "Inspect the definitions and source meaning; record the actual reviewer and date.")
            return False
        # A timestamp is a claim. Reject future dates without authenticating the actor.
        instant = datetime.fromisoformat(value["reviewed_at"].replace("Z", "+00:00"))
        if instant > datetime.now(instant.tzinfo):
            emit("UNVERIFIED", rule, "The recorded review date is in the future.", "Record the actual completed review time.")
            return False
        return True

    seen = set()
    for selected in paths:
        try:
            path = Path(selected).resolve()
        except (OSError, ValueError, RuntimeError) as error:
            report("FAIL", "input_invalid", str(error), "Select a valid file path.", path=selected)
            continue
        if path in seen:
            continue
        seen.add(path)
        start = len(findings)

        def file_report(status, rule, explanation, correction, **kwargs):
            report(status, rule, explanation, correction, path=path, **kwargs)

        try:
            if path.suffix.lower() not in {".feature", ".md"}:
                raise ValueError("Select explicit .feature or .md files.")
            payload = _read(path)
            text = payload.decode("utf-8")
        except (OSError, UnicodeError, ValueError) as error:
            file_report("FAIL", "input_invalid", str(error), "Supply a readable Gherkin input.")
            continue
        scenarios = []
        for block, offset in _blocks(text, path.suffix.lower(), file_report):
            def syntax_report(rule, message, *, line=None):
                file_report("FAIL", rule, message, "Correct the Gherkin structure.", line=offset + line if line else offset + 1)
            _gherkin(block, syntax_report)
            scenarios.extend(_scenarios(block, offset, file_report))
        if scenario_ids is not None:
            scenarios = [scenario for scenario in scenarios if scenario["id"] in scenario_ids]
        documents.append((path, payload, scenarios, start, len(findings)))

    ids = set()
    counts = {}
    for _, _, scenarios, _, _ in documents:
        for scenario in scenarios:
            counts[scenario["id"]] = counts.get(scenario["id"], 0) + 1
    for path, payload, scenarios, file_start, file_end in documents:
        for scenario in scenarios:
            start = len(findings)
            identifier = scenario["id"]

            def emit(status, rule, explanation, correction, *, line=None, evidence=None):
                report(status, rule, explanation, correction, path=path, scenario_id=identifier,
                       line=line or scenario["line"], evidence=evidence)

            if not identifier:
                emit("FAIL", "scenario_id", "The scenario has no stable identifier tag.", "Add @CASE-ID immediately before Scenario.")
            elif counts[identifier] > 1:
                emit("FAIL", "scenario_duplicate", "The scenario identifier occurs more than once.", "Use one canonical definition for each case.")
            ids.add(identifier)
            entry = data["scenarios"].get(identifier)
            if not entry:
                emit("UNVERIFIED", "scenario_evidence", "The scenario has no evidence manifest entry.",
                     "Map business intent, UI targets, steps, reviews, and automation separately.")
            else:
                try:
                    if _local(evidence_root, entry["file"]) != path:
                        raise ValueError("The manifest names a different scenario file.")
                    if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
                        raise ValueError("Scenario bytes changed after the evidence review.")
                except (OSError, ValueError, RuntimeError) as error:
                    emit("UNVERIFIED", "scenario_stale", str(error), "Review the current definition before renewing its hash.")
                evidence_refs([entry["behavior"]["requirement"]], emit, kind="behavior", authoritative=True)
                review(entry["review"], emit, "semantic_review")
            expected_lines = {str(step["line"]) for step in scenario["steps"]}
            if entry and set(entry["steps"]) - expected_lines:
                emit("FAIL", "step_orphan", "The manifest contains lines outside this scenario's steps.", "Remove stale mappings after source review.")
            automation = entry.get("automation") if entry else None
            if not automation:
                emit("UNVERIFIED", "automation_missing", "Automation bindings have not been reviewed.",
                     "Inspect the existing framework and map every setup, action, and assertion.")
            else:
                review(automation["review"], emit, "automation_review")
                if set(automation["bindings"]) - expected_lines:
                    emit("FAIL", "binding_orphan", "An automation binding names a line outside this scenario.", "Correct the binding line after review.")
            for step in scenario["steps"]:
                line, keyword, clause = step["line"], step["keyword"], step["text"]

                def step_emit(status, rule, explanation, correction, **kwargs):
                    emit(status, rule, explanation, correction, line=line, **kwargs)

                detail = entry["steps"].get(str(line)) if entry else None
                # Quoted labels can contain action verbs. They are target names, not additional actions.
                action_text = re.sub(r'"[^"\n]*"|`[^`\n]*`', "", clause)
                actions = [match for match in _ACTION.finditer(action_text)
                           if not (match.group().lower() == "open" and re.search(
                               r"\b(?:is|are|was|were|remains?|stays?)\s+$", action_text[:match.start()], re.I))
                           and not (match.group().lower() == "focus" and re.search(
                               r"\b(?:has|have|had)\s+$", action_text[:match.start()], re.I))]
                interaction = bool(actions) and keyword != "Then"
                ui_reference = bool(_COMPONENT.search(action_text))
                if interaction and len(actions) > 1:
                    step_emit("FAIL", "ui_multiple_actions", "The step contains more than one UI action.",
                              "Use one ordered action per step and map each target.")
                if detail:
                    valid_kinds = {"Given": {"condition", "interaction"}, "When": {"interaction", "event"}, "Then": {"assertion"}}
                    if detail["kind"] not in valid_kinds.get(keyword, set()):
                        step_emit("FAIL", "step_kind", "The step classification conflicts with its Gherkin clause.", "Align the classification with the actual step.")
                    # A declared event must not bypass observable UI action checks.
                    interaction = interaction or detail["kind"] == "interaction"
                    if interaction and detail["kind"] == "event":
                        step_emit("FAIL", "event_ui_action", "A UI action is classified as a system event.", "Record the UI target and interaction.")
                    evidence_refs(detail["evidence"], step_emit, authoritative=keyword == "Then")
                else:
                    step_emit("UNVERIFIED", "step_evidence", "The step has no evidence mapping.", "Map this exact source line to inspected evidence.")
                if keyword == "When" and not interaction and (not detail or detail["kind"] != "event"):
                    step_emit("UNVERIFIED", "interaction_unknown", "The action does not identify a supported UI interaction or reviewed event.",
                              "State the concrete interaction, or identify the non-UI event in the manifest.")
                if interaction:
                    if not actions:
                        step_emit("UNVERIFIED", "ui_action", "The declared interaction has no supported action verb.",
                                  "State its concrete action and review any vocabulary extension.")
                    if not _COMPONENT.search(action_text):
                        step_emit("FAIL", "ui_type", "The UI action does not identify a component type.", "Name the actual button, textbox, option, or other component.")
                    if not _IDENTITY.search(clause):
                        step_emit("FAIL", "ui_identity", "The UI action does not identify a quoted label, name, or stable identifier.", "Use the verified label, accessible name, or stable ID.")
                    if not _SCOPE.search(clause):
                        step_emit("FAIL", "ui_scope", "The UI action has no explicit containing region.", "Name the page, dialog, panel, form, or business-identified row.")
                    if detail and not detail.get("components"):
                        step_emit("UNVERIFIED", "ui_inventory", "The interaction has no component inventory mapping.", "Link every interaction target to the inventory.")
                refs = detail.get("components", []) if detail else []
                if ui_reference and not refs:
                    step_emit("UNVERIFIED", "ui_reference", "A UI reference has no component inventory mapping.",
                              "Verify each referenced component's identity and scope, including preconditions.")
                for component_id in refs:
                    component = entry["components"].get(component_id)
                    if not component:
                        step_emit("FAIL", "component_unknown", f"Component '{component_id}' is not defined.", "Define the verified target before using its ID.")
                        continue
                    if component["type"].lower() not in COMPONENT_TYPES:
                        step_emit("UNVERIFIED", "component_vocabulary", "The component type is outside the supported vocabulary.",
                                  "Inspect its actual semantics before extending the vocabulary.")
                    quoted = [match[0] or match[1] for match in re.findall(r'"([^"\n]+)"|`([^`\n]+)`', clause)]
                    for field in ("type", "identity", "scope"):
                        # Visible names and stable identifiers are case-sensitive; type is not.
                        actual, expected = clause, component[field]
                        if field == "type":
                            present = re.search(r"\b" + re.escape(expected) + r"\b", action_text, re.I) is not None
                        elif field == "identity":
                            present = expected in quoted or re.search(
                                r"\b(?:test ID|testid|identifier)\s+" + re.escape(expected) + r"(?!\w)", clause, re.I) is not None
                        else:
                            present = expected in actual
                        if not present:
                            step_emit("FAIL", "component_reference", f"The step omits the inventory's {field}.",
                                      "Align the step with its exact verified target and scope.", evidence=component["evidence"])
                    evidence_refs(component["evidence"], step_emit, kind="ui")
                    if component["identity_kind"] == "stable_identifier":
                        step_emit("WARNING", "identifier_maintainability", "The target uses an application-specific identifier.",
                                  "Prefer a verified role and name when they identify the same unique target.", evidence=component["evidence"])
                if keyword == "Then":
                    if _VAGUE.search(clause):
                        step_emit("FAIL", "result_vague", "The assertion states success without a sufficient observable result.",
                                  "Name the UI state, exact value, or functional probe that establishes the result.")
                    elif not _OBSERVABLE.search(clause):
                        step_emit("UNVERIFIED", "result_unknown", "The assertion uses an unrecognized observation form.",
                                  "Define its exact observation and review the matching assertion.")
                    if detail and not detail.get("observation"):
                        step_emit("FAIL", "result_kind", "The assertion does not distinguish UI observation from functional verification.",
                                  "Set observation to ui or functional and inspect supporting evidence.")
                    if detail and detail.get("observation") == "ui" and not refs:
                        step_emit("UNVERIFIED", "result_target", "The UI assertion has no verified component reference.", "Map the observed UI component and its scope.")
                if automation:
                    binding = automation["bindings"].get(str(line))
                    if not binding:
                        step_emit("UNVERIFIED", "binding_missing", "This step has no inspected automation binding.",
                                  "Map the framework keyword or function, including every assertion.")
                    else:
                        evidence_refs(binding["evidence"], step_emit, kind="automation")
                        # Presence is necessary for a symbol binding. It does not prove execution compatibility.
                        for ref in binding["evidence"]:
                            if source_cache.get(ref) is None and binding["symbol"] in source_excerpts.get(ref, ""):
                                break
                        else:
                            step_emit("UNVERIFIED", "binding_symbol", "The binding symbol is absent from its cited source lines.",
                                      "Link the exact framework keyword or function definition.", evidence=binding["evidence"])
            own = findings[start:] + findings[file_start:file_end]
            state = _status(own)
            ready = state in {"PASS", "WARNING"} and not (strict and state == "WARNING")
            results.append({"id": identifier, "path": str(path), "line": scenario["line"], "status": state, "automation_ready": ready})
    if not paths:
        report("FAIL", "input_missing", "No scenario files were selected.", "Select at least one .md or .feature file.")
    if scenario_ids is not None:
        for identifier in set(scenario_ids) - ids:
            report("FAIL", "scenario_selection", f"Selected scenario '{identifier}' was not found.",
                   "Use an exact identifier tag from the selected files.", scenario_id=identifier)
    status = _status(findings)
    ready = bool(results) and all(item["automation_ready"] for item in results) and status not in {"FAIL", "UNVERIFIED"}
    return {"schema_version": 1, "status": status, "automation_ready": ready,
            "exit_code": 1 if status == "FAIL" or (strict and status == "WARNING") else 2 if status == "UNVERIFIED" else 0,
            "findings": findings, "scenarios": results, "limitations": _LIMITATIONS}
