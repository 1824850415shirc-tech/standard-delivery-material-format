#!/usr/bin/env python3
"""Checks that the editorial gates reject the regressions reported by users."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_naturalness import audit  # noqa: E402
from lint_markdown import lint  # noqa: E402


class QualityGateTest(unittest.TestCase):
    def write_markdown(self, text: str) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "document.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_lint_rejects_generic_explanation_and_template_comment(self) -> None:
        path = self.write_markdown(
            "# 测试文档\n\n## 1. 范围\n\n说明：这里是普通正文。\n\n<!-- 编写提示：不应进入正文。 -->\n"
        )
        report = lint(path)
        self.assertFalse(report["ok"])
        messages = "\n".join(item["message"] for item in report["errors"])
        self.assertIn("说明", messages)
        self.assertIn("模板编写提示", messages)

    def test_strict_naturalness_flags_repeated_modal_prose(self) -> None:
        path = self.write_markdown(
            "# 测试文档\n\n## 1. 范围\n\n"
            "系统应部署在内网。服务应支持审计。接口应提供鉴权。"
            "数据应保持一致。任务应记录日志。人员应完成复核。\n"
        )
        report = audit(path)
        self.assertFalse(report["ok"])
        signals = {item["type"] for item in report["style_signals"]}
        self.assertIn("模态词重复", signals)


if __name__ == "__main__":
    unittest.main()
