#!/usr/bin/env python3
"""Create the anonymous executable DOCX master used by the Skill."""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document


REPLACEMENTS = {
    "XX项目": "{{PROJECT_NAME}}",
    "技术规格说明书": "{{COVER_TITLE}}",
    "XX科技": "{{COVER_COMPANY}}",
    "XX年X月X日": "{{DOCUMENT_DATE}}",
}


def replace_complete_paragraph(paragraph, source: str, value: str) -> None:
    for run in paragraph.runs:
        if source in run.text:
            run.text = run.text.replace(source, value)
            return
    raise RuntimeError(f"Template cover text is split across unsupported runs: {source}")


def sanitize(source: Path, output: Path) -> None:
    document = Document(source)
    seen: set[str] = set()
    for paragraph in document.paragraphs:
        if paragraph.text in REPLACEMENTS:
            seen.add(paragraph.text)
            source_text = paragraph.text
            replace_complete_paragraph(paragraph, source_text, REPLACEMENTS[source_text])
    required_roles = {"XX项目", "技术规格说明书", "XX年X月X日"}
    if not required_roles.issubset(seen):
        missing = ", ".join(sorted(required_roles - seen))
        raise RuntimeError(f"Template cover roles not found: {missing}")
    company_roles = {"XX科技"}
    if not seen.intersection(company_roles):
        raise RuntimeError("Template company role not found")

    core = document.core_properties
    core.author = ""
    core.last_modified_by = ""
    core.title = "标准交付材料模板"
    core.subject = ""
    core.keywords = ""
    core.comments = ""
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sanitize(args.source, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
