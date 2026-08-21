#!/usr/bin/env python3
"""Validate built-in Markdown templates without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"
HEADING = re.compile(r"^(#{1,5})\s+(.+?)\s*$")
H2_NUMBER = re.compile(r"^(?:\d+\.\s+.+|附录\s+[A-ZＡ-Ｚ][：:].+)")
H3_NUMBER = re.compile(r"^\d+\.\d+\s+.+")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
EXPECTED_TEMPLATES = {
    "项目前期": {"项目章程.md", "调研方案.md", "调研报告.md", "实施方案.md"},
    "项目过程": {
        "需求规格说明书.md",
        "详细设计说明书.md",
        "数据库设计.md",
        "测试方案与用例.md",
        "测试报告.md",
        "运维手册.md",
        "系统接口文档.md",
        "操作手册.md",
    },
    "项目收尾": {"验收报告.md", "试运行报告.md"},
}


def split_frontmatter(text: str, path: Path) -> tuple[list[str], dict[str, str], list[str]]:
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0] != "---":
        return lines, {}, [f"{path}: missing YAML front matter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return lines, {}, [f"{path}: unterminated YAML front matter"]
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    if metadata.get("cover_company") != "XX科技":
        errors.append(f"{path}: cover_company must default to XX科技")
    for field in ("cover_title", "project_name", "document_version", "document_date"):
        if field not in metadata:
            errors.append(f"{path}: front matter missing {field}")
    if "【待补充：" not in metadata.get("project_name", ""):
        errors.append(f"{path}: project_name must remain an anonymous placeholder")
    return lines[end + 1 :], metadata, errors


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines, metadata, errors = split_frontmatter(text, path)
    headings: list[tuple[int, int, str]] = []
    for line_no, line in enumerate(lines, start=1):
        match = HEADING.match(line)
        if match:
            headings.append((line_no, len(match.group(1)), match.group(2)))
    h1 = [item for item in headings if item[1] == 1]
    if len(h1) != 1:
        errors.append(f"{path}: exactly one H1 is required; found {len(h1)}")
    elif metadata.get("cover_title") != h1[0][2]:
        errors.append(f"{path}: cover_title must match the H1 document title")
    for previous, current in zip(headings, headings[1:]):
        if current[1] > previous[1] + 1:
            errors.append(f"{path}:{current[0]}: heading levels must not skip")
    for line_no, level, title in headings:
        if level == 2 and not H2_NUMBER.match(title):
            errors.append(f"{path}:{line_no}: H2 must use '1. 标题' numbering")
        if level == 3 and not H3_NUMBER.match(title):
            errors.append(f"{path}:{line_no}: H3 must use '1.1 标题' numbering")
    if EMAIL.search(text):
        errors.append(f"{path}: email addresses are not allowed in built-in templates")
    if PHONE.search(text):
        errors.append(f"{path}: phone numbers are not allowed in built-in templates")
    return errors


def main() -> int:
    paths = sorted(TEMPLATE_DIR.rglob("*.md"))
    if not paths:
        print("No Markdown templates found.")
        return 1
    errors: list[str] = []
    category_directories = {path.name for path in TEMPLATE_DIR.iterdir() if path.is_dir()}
    missing_categories = sorted(set(EXPECTED_TEMPLATES) - category_directories)
    extra_categories = sorted(category_directories - set(EXPECTED_TEMPLATES))
    if missing_categories:
        errors.append("missing template categories: " + ", ".join(missing_categories))
    if extra_categories:
        errors.append("unexpected template categories: " + ", ".join(extra_categories))
    actual_by_category = {
        category: {path.name for path in (TEMPLATE_DIR / category).glob("*.md")}
        for category in EXPECTED_TEMPLATES
    }
    for category, expected in EXPECTED_TEMPLATES.items():
        missing = sorted(expected - actual_by_category[category])
        extra = sorted(actual_by_category[category] - expected)
        if missing:
            errors.append(f"{category}: missing templates: {', '.join(missing)}")
        if extra:
            errors.append(f"{category}: unexpected templates: {', '.join(extra)}")
    root_templates = sorted(path.name for path in TEMPLATE_DIR.glob("*.md"))
    if root_templates:
        errors.append("templates must be stored in a project-phase directory: " + ", ".join(root_templates))
    errors.extend(error for path in paths for error in validate(path))
    if errors:
        print("Template validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PASS: {len(paths)} templates validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
