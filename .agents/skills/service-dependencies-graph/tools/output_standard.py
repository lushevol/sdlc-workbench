"""Check selected ASD-STE100 report rules without claiming full compliance."""

from __future__ import annotations

import json
import html
import re
from typing import Any


SENTENCE_WORD_LIMIT = 20
PARAGRAPH_SENTENCE_LIMIT = 6
CHECK_LIMITATION = "Automated checks do not check the complete approved dictionary or grammar rules."
_WORDS = re.compile(r"[\w]+(?:[-'][\w]+)*", re.UNICODE)
_VAGUE = {
    "probably": "State the evidence and uncertainty.",
    "obviously": "State the evidence that supports the claim.",
    "simply": "Give the specific action or condition.",
    "somehow": "State the known mechanism or mark it unresolved.",
    "as appropriate": "State the condition that controls the action.",
    "as necessary": "State the condition that controls the action.",
    "etc.": "List the required items or define the scope.",
}
_PASSIVE = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being)\s+"
    r"(?:executed|implemented|verified|approved|reviewed|processed|generated|"
    r"retained|recorded|stored|provided|identified|assigned|rejected|accepted|"
    r"updated|removed|added|changed|supported|required|configured|tested)\b",
    re.IGNORECASE,
)


def _inline_prose(text: str) -> str:
    text = re.sub(r"(`+).*?\1", "TECHNICAL_TERM", text)
    text = re.sub(r"!\[([^\]]*)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)
    text = re.sub(r"<https?://[^>]+>", "TECHNICAL_TERM", text)
    text = re.sub(r"https?://\S+", "TECHNICAL_TERM", text)
    return html.unescape(text.replace("**", "").replace("__", "").replace("*", "").replace("~~", ""))


def _prose_units(text: str) -> list[tuple[int, str]]:
    """Keep prose blocks separate from exact evidence and Markdown structure."""
    units: list[tuple[int, str]] = []
    paragraph: list[str] = []
    start = 0
    fence: str | None = None
    in_comment = False

    def flush() -> None:
        if paragraph:
            units.append((start, "\n".join(paragraph)))
            paragraph.clear()

    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            continue
        if marker:
            flush()
            fence = marker.group(1)
            continue
        if in_comment or "<!--" in stripped:
            flush()
            in_comment = "-->" not in stripped
            continue
        if (not stripped or line.startswith(("    ", "\t")) or
                re.match(r"^\s{0,3}(?:>|#{1,6}\s|\[[^]]+\]:)", line) or
                re.fullmatch(r"\s*(?:-{3,}|\*{3,}|_{3,}|={3,})\s*", line)):
            flush()
            continue
        if stripped.startswith("|"):
            flush()
            # Escaped and inline-code pipes belong to cells, not table structure.
            cells = re.split(r"(?<!\\)\|(?=(?:[^`]*`[^`]*`)*[^`]*$)", stripped.strip("|"))
            for cell in cells:
                cell = cell.strip().replace(r"\|", "|")
                if cell and not re.fullmatch(r":?-+:?", cell):
                    units.append((line_number, cell))
            continue
        item = re.match(r"^\s{0,3}(?:[-+*]|\d+[.)])\s+(?:\[[ xX]\]\s+)?", line)
        if item:
            flush()
            start = line_number
            paragraph.append(line[item.end():])
        else:
            if not paragraph:
                start = line_number
            paragraph.append(line)
    flush()
    return units


def _sentences(prose: str) -> list[tuple[int, str]]:
    # Protect common abbreviations while keeping offsets for useful line numbers.
    protected = re.sub(r"\b(?:e\.g\.|i\.e\.|vs\.)", lambda match: match.group().replace(".", "~"), prose)
    parts: list[tuple[int, str]] = []
    position = 0
    for boundary in re.finditer(r"[.!?](?:[\"')\]]*)(?=\s|$)", protected):
        fragment = prose[position:boundary.end()]
        if fragment.strip():
            parts.append((position + len(fragment) - len(fragment.lstrip()), fragment.strip()))
        position = boundary.end()
    fragment = prose[position:]
    if fragment.strip():
        parts.append((position + len(fragment) - len(fragment.lstrip()), fragment.strip()))
    return parts


def _lint_units(units: list[tuple[int, str]], *, markdown: bool) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for start_line, raw in units:
        prose = _inline_prose(raw) if markdown else raw
        sentences = _sentences(prose)
        if len(sentences) > PARAGRAPH_SENTENCE_LIMIT:
            findings.append({"rule": "paragraph_length", "severity": "ERROR", "line": start_line,
                             "message": "Use no more than six sentences in each paragraph.",
                             "excerpt": raw, "count": len(sentences), "limit": PARAGRAPH_SENTENCE_LIMIT})
        for offset, sentence in sentences:
            line_number = start_line + prose[:offset].count("\n")
            words = _WORDS.findall(sentence)
            if len(words) > SENTENCE_WORD_LIMIT:
                findings.append({"rule": "sentence_length", "severity": "ERROR", "line": line_number,
                                 "message": "Use no more than 20 words in each prose sentence.",
                                 "excerpt": sentence, "count": len(words), "limit": SENTENCE_WORD_LIMIT})
            for phrase, message in _VAGUE.items():
                if re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", sentence, re.IGNORECASE):
                    findings.append({"rule": "vague_term", "severity": "REVIEW", "line": line_number,
                                     "message": message, "excerpt": sentence, "term": phrase})
            for match in _PASSIVE.finditer(sentence):
                findings.append({"rule": "passive_voice", "severity": "REVIEW", "line": line_number,
                                 "message": "Use active voice and name the actor.",
                                 "excerpt": sentence, "term": match.group()})
    return findings


def lint_text(text: str) -> list[dict[str, Any]]:
    """Check Markdown prose. Exact evidence blocks keep their original text."""
    return _lint_units(_prose_units(text), markdown=True)


def lint_authored_text(text: str) -> list[dict[str, Any]]:
    """Check authored fields before rendering; Markdown grants no exemption."""
    units = []
    line = 1
    for paragraph in re.split(r"(\n\s*\n)", text):
        if paragraph.strip():
            units.append((line, paragraph))
        line += paragraph.count("\n")
    return _lint_units(units, markdown=False)


class OutputStandardError(ValueError):
    """A report contains authored prose that needs correction."""


def render_prose(text: str) -> str:
    """Render authored text as visible Markdown text, without structural markup."""
    return "\n".join(re.sub(r"([\\`*_{}\[\]()#+.!|~>-])", r"\\\1", html.escape(line.strip(), quote=False))
                     for line in text.splitlines())


def render_quotation(text: str) -> str:
    """Display exact evidence inside a quote and a collision-free literal fence."""
    fence = "`" * max(3, 1 + max((len(match.group()) for match in re.finditer(r"`+", text)), default=0))
    return "> " + fence + "text\n> " + text.replace("\n", "\n> ") + "\n> " + fence


def finalize_report(text: str, *, authored_fields: dict[str, str] | None = None) -> str:
    """Gate authored fields and the rendered report, then append review state."""
    for name, value in (authored_fields or {}).items():
        if lint_authored_text(value):
            raise OutputStandardError(f"Authored field {name} fails automated ASD-STE100 text checks.")
    review = check_document(text)
    if review["automated_check"] != "PASSED":
        locations = ", ".join(str(item["line"]) for item in review["findings"])
        raise OutputStandardError(f"The report fails automated ASD-STE100 text checks at lines {locations}.")
    return text.rstrip() + "\n\n## Output review\n\n```json\n" + json.dumps(review, indent=2, sort_keys=True) + "\n```\n"


def check_document(text: str) -> dict[str, Any]:
    """Keep automated findings separate from the mandatory ASD review."""
    findings = lint_text(text)
    return {
        "standard": "ASD-STE100",
        "automated_check": "FAILED" if findings else "PASSED",
        "findings": findings,
        "asd_review": "PENDING",
        "reviewer": None,
        "reviewed_at": None,
        "limitations": [CHECK_LIMITATION],
    }
