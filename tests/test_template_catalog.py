#!/usr/bin/env python3
"""Validate the categorized template catalog and render every built-in template."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_document import render  # noqa: E402
from validate_templates import EXPECTED_TEMPLATES, validate  # noqa: E402
from verify_document import verify  # noqa: E402


class TemplateCatalogTest(unittest.TestCase):
    def test_interface_template_uses_apifox_as_a_source_snapshot(self) -> None:
        text = (ROOT / "templates" / "项目过程" / "系统接口文档.md").read_text(encoding="utf-8")

        self.assertIn("Apifox", text)
        self.assertIn("OpenAPI JSON/YAML", text)
        self.assertIn("导出定义、Mock 示例", text)
        self.assertIn("同一模型只定义一次", text)
        self.assertIn("来源与接口覆盖矩阵", text)

    def test_requirements_template_converts_prd_into_delivery_requirements(self) -> None:
        text = (ROOT / "templates" / "项目过程" / "需求规格说明书.md").read_text(encoding="utf-8")

        self.assertIn("PRD 作为产品需求的主要上游材料", text)
        self.assertIn("PRD 优先级不自动等于项目交付范围", text)
        self.assertIn("技术方案与需求的分界", text)
        self.assertIn("需求来源与覆盖矩阵", text)
        self.assertIn("验收场景与用例", text)
        self.assertIn("一个需求项只表达一项可验证行为", text)

    def test_research_report_inherits_prior_materials_without_rewriting_them(self) -> None:
        text = (ROOT / "templates" / "项目前期" / "调研报告.md").read_text(encoding="utf-8")

        self.assertIn("前序材料承接与变化", text)
        self.assertIn("不在本报告重复展开", text)
        self.assertIn("本次核验或变化", text)
        self.assertIn("前序材料中的约定或方案不自动证明当前现状", text)

    def test_catalog_is_complete_and_every_template_renders(self) -> None:
        template_root = ROOT / "templates"
        paths = sorted(template_root.rglob("*.md"))
        self.assertEqual(len(paths), 14)

        actual = {
            category: {path.name for path in (template_root / category).glob("*.md")}
            for category in EXPECTED_TEMPLATES
        }
        self.assertEqual(actual, EXPECTED_TEMPLATES)

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory)
            for path in paths:
                self.assertEqual(validate(path), [], path)
                output = output_root / f"{path.parent.name}-{path.stem}.docx"
                render(path, ROOT / "assets" / "master-template.docx", output)
                report = verify(output)
                self.assertTrue(report["ok"], f"{path}: {report['errors']}")
                body_text = "\n".join(paragraph.text for paragraph in Document(output).paragraphs)
                self.assertNotIn("编写提示", body_text, path)
                self.assertIn("XX科技", body_text, path)


if __name__ == "__main__":
    unittest.main()
