#!/usr/bin/env python3
"""Validate Markdown against the Standard Delivery Material contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_RE = re.compile(r"^(?:\d+(?:\.\d+)*[.、]?|附录\s+[A-ZＡ-Ｚ])(?:\s|：|:)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$")


def strip_frontmatter(lines: list[str]) -> tuple[list[str], int]:
    if not lines or lines[0].strip() != "---":
        return lines, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[idx + 1 :], idx + 1
    return lines, 0


def lint(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines, offset = strip_frontmatter(text.splitlines())
    errors: list[dict] = []
    warnings: list[dict] = []
    headings: list[tuple[int, int, str]] = []
    in_fence = False
    fence_marker = ""
    first_content_seen = False

    def issue(bucket: list[dict], line: int, message: str) -> None:
        bucket.append({"line": line + offset, "message": message})

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        fence = re.match(r"^(```+|~~~+)", stripped)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
                if stripped in {"```", "~~~"}:
                    issue(warnings, i, "代码块建议声明语言，例如 ```bash 或 ```yaml。")
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue
        if not stripped:
            continue
        if re.match(r"^>\s*说明\s*[：:]", stripped):
            issue(errors, i, "不要用引用块承载泛化的“说明”；删除标签并写成正文，或改为具体的注意、警告、约束。")
        elif re.match(r"^说明\s*[：:]", stripped):
            issue(errors, i, "不要使用泛化的“说明”标签，直接写清事实、条件或限制。")
        if "\t" in line:
            issue(warnings, i, "不要使用制表符控制版式。")
        line_without_inline_code = re.sub(r"`[^`]*`", "", line)
        if "<!--" in line_without_inline_code or re.search(r"<\/?[A-Za-z][^>]*>", line_without_inline_code):
            issue(errors, i, "最终正文不要保留原始 HTML 或模板编写提示。")
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            headings.append((i, level, title))
            if level > 5:
                issue(errors, i, "标题不得深于五级。")
            if not first_content_seen and level != 1:
                issue(errors, i, "第一个内容块必须是唯一的 H1 文档标题。")
            if level >= 2 and not NUMBERED_RE.match(title):
                issue(warnings, i, "正文标题建议使用层级编号或“附录 A：”格式。")
            first_content_seen = True
            continue
        if not first_content_seen:
            issue(errors, i, "文档标题之前存在正文内容。")
            first_content_seen = True

        if "|" in line and i < len(lines):
            next_line = lines[i].strip() if i < len(lines) else ""
            if next_line and TABLE_SEPARATOR_RE.match(next_line):
                header_cells = [c.strip() for c in stripped.strip("|").split("|")]
                if any(not c for c in header_cells):
                    issue(errors, i, "表格表头不得为空。")

    if in_fence:
        errors.append({"line": len(lines) + offset, "message": "代码围栏未闭合。"})
    if not headings:
        errors.append({"line": 1, "message": "文档必须包含标题。"})
    h1_count = sum(1 for _, level, _ in headings if level == 1)
    if h1_count != 1:
        errors.append({"line": 1, "message": f"必须且只能有一个 H1 文档标题；当前为 {h1_count} 个。"})
    for previous, current in zip(headings, headings[1:]):
        if current[1] > previous[1] + 1:
            errors.append({
                "line": current[0] + offset,
                "message": f"标题从 H{previous[1]} 跳到了 H{current[1]}。",
            })

    return {
        "input": str(path),
        "headings": len(headings),
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = lint(args.input)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Markdown: {args.input}")
        for item in report["errors"]:
            print(f"ERROR line {item['line']}: {item['message']}")
        for item in report["warnings"]:
            print(f"WARN  line {item['line']}: {item['message']}")
        print("PASS" if report["ok"] else "FAIL")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
