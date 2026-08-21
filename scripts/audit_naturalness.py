#!/usr/bin/env python3
"""Audit Chinese technical prose for high-confidence AI-like writing residue."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from docx import Document


BLOCKED_PATTERNS = {
    "AI 身份或能力说明": re.compile(r"作为(?:一个|一名)?\s*(?:AI|人工智能|语言模型)", re.I),
    "面向用户的生成式开场": re.compile(r"(?:以下是|下面是)(?:我|为您)?(?:整理|生成|撰写|提供|给出)"),
    "客服式结尾": re.compile(r"(?:希望|期望)(?:以上|这些|本回答).*?(?:帮助|有所帮助)"),
    "继续提问提示": re.compile(r"如果您还有.*?(?:问题|需要|疑问).*?(?:告诉|提出|联系)"),
    "泛化说明标签": re.compile(r"(?m)^\s*>?\s*说明\s*[：:]"),
}

STYLE_PATTERNS = {
    "机械总结词": re.compile(r"综上所述|总而言之|由此可见"),
    "空泛强调词": re.compile(r"至关重要|不言而喻|毋庸置疑|显而易见|值得注意的是|需要指出的是"),
    "宣传性表达": re.compile(r"全面提升|显著提升|有效赋能|深度赋能|强力支撑|坚实保障|保驾护航"),
    "泛化目的句": re.compile(r"本文旨在|本方案旨在|本章节旨在"),
}

TRANSITIONS = ("首先", "其次", "再次", "此外", "同时", "最后", "综上")
MODAL_PATTERNS = {
    "应": re.compile(r"应(?=当|在|先|按|保持|采用|支持|提供|具备|确保|完成|记录|配置|部署|设置|检查|验证|执行|遵循|符合|满足|禁止|由|为|与|向|将|不|仅|至少)"),
    "通常": re.compile(r"通常"),
    "一般情况下": re.compile(r"一般情况下"),
    "建议": re.compile(r"建议"),
}


def read_text(path: Path) -> str:
    if path.suffix.casefold() == ".docx":
        document = Document(path)
        chunks = [paragraph.text for paragraph in document.paragraphs]
        for table in document.tables:
            for row in table.rows:
                chunks.extend(cell.text for cell in row.cells)
        return "\n".join(chunks)
    return path.read_text(encoding="utf-8")


def remove_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.S)
    return re.sub(r"`[^`]+`", "", text)


def audit(path: Path) -> dict:
    text = remove_code(read_text(path))
    prose = "\n".join(
        line
        for line in text.splitlines()
        if line.strip()
        and not line.lstrip().startswith(("#", "|", "---", "<!--"))
    )
    blocked: list[dict] = []
    style_signals: list[dict] = []

    for label, pattern in BLOCKED_PATTERNS.items():
        matches = [match.group(0) for match in pattern.finditer(text)]
        if matches:
            blocked.append({"type": label, "count": len(matches), "examples": matches[:3]})

    for label, pattern in STYLE_PATTERNS.items():
        matches = [match.group(0) for match in pattern.finditer(text)]
        if matches:
            style_signals.append({"type": label, "count": len(matches), "examples": matches[:3]})

    transition_counts = {word: len(re.findall(word, text)) for word in TRANSITIONS}
    overused = {word: count for word, count in transition_counts.items() if count >= 3}
    if overused:
        style_signals.append({"type": "连接词重复", "count": sum(overused.values()), "examples": overused})

    modal_counts = {word: len(pattern.findall(prose)) for word, pattern in MODAL_PATTERNS.items()}
    modal_overused = {
        word: count
        for word, count in modal_counts.items()
        if (word == "应" and count >= 6)
        or (word == "通常" and count >= 2)
        or (word == "一般情况下" and count >= 1)
        or (word == "建议" and count >= 3)
    }
    if modal_overused:
        style_signals.append({
            "type": "模态词重复",
            "count": sum(modal_overused.values()),
            "examples": modal_overused,
            "review": "仅保留有合同、规范或操作责任依据的应/须/不得；其余改写为事实、直接动作或待确认项。",
        })

    paragraphs = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    paragraphs = [
        line
        for line in paragraphs
        if len(line) >= 12 and not line.startswith(("#", "|"))
    ]
    duplicates = [text for text, count in Counter(paragraphs).items() if count > 1]
    if duplicates:
        style_signals.append({"type": "重复段落", "count": len(duplicates), "examples": duplicates[:3]})

    return {
        "input": str(path),
        "blocked_meta_signals": blocked,
        "style_signals": style_signals,
        "ok": not blocked and not style_signals,
        "blocked_ok": not blocked,
        "note": "This is an editorial heuristic, not an AI detector.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--strict", action="store_true", help="Fail on explicit AI/chat residue.")
    args = parser.parse_args()
    report = audit(args.input)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and not report["ok"] else 0


if __name__ == "__main__":
    sys.exit(main())
