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


def markdown_table_widths(text: str) -> list[int]:
    widths: list[int] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            widths.append(len(stripped.split("|")) - 2)
    return widths


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

    def test_operations_manual_teaches_customer_maintenance(self) -> None:
        text = (ROOT / "templates" / "项目过程" / "运维手册.md").read_text(encoding="utf-8")

        self.assertIn("明确本手册由建设方编制", text)
        self.assertIn("客户与建设方职责分工", text)
        self.assertIn("日常运维操作", text)
        self.assertIn("数据恢复与恢复验证", text)
        self.assertIn("建设方支持与问题升级", text)
        self.assertIn("客户日常运维检查清单", text)
        self.assertIn("超出客户授权或能力边界的操作转建设方技术支持处理", text)
        self.assertIn("高风险命令不放入客户日常命令清单", text)

    def test_operation_manual_is_role_scenario_and_evidence_driven(self) -> None:
        text = (ROOT / "templates" / "项目过程" / "操作手册.md").read_text(encoding="utf-8")

        self.assertIn("编制依据与版本基线", text)
        self.assertIn("用户角色与权限", text)
        self.assertIn("场景、角色与前置条件", text)
        self.assertIn("操作结果与验证方法", text)
        self.assertIn("异常处理、撤销和风险提示", text)
        self.assertIn("功能与操作覆盖矩阵", text)
        self.assertIn("历史手册和页面截图只代表对应版本的操作快照", text)
        self.assertIn('![页面说明](images/example.png "图 1-1 页面说明")', text)

    def test_test_plan_and_cases_are_executable_and_iteration_safe(self) -> None:
        text = (ROOT / "templates" / "项目过程" / "测试方案与用例.md").read_text(encoding="utf-8")

        self.assertIn("测试依据与版本", text)
        self.assertIn("需求与用例覆盖关系", text)
        self.assertIn("测试数据与标准结果", text)
        self.assertIn("详细用例编号、名称和数量必须与 6.2 一致", text)
        self.assertIn("操作步骤与预期结果", text)
        self.assertIn("复测通过不删除首轮失败记录", text)
        self.assertNotIn("测试组织", text)
        numbered_h2 = [
            line[3:5]
            for line in text.splitlines()
            if line.startswith("## ") and len(line) > 4 and line[3].isdigit()
        ]
        self.assertEqual(numbered_h2, ["1.", "2.", "3.", "4.", "5.", "6."])
        self.assertLessEqual(max(markdown_table_widths(text)), 6)

        merge_rules = (ROOT / "references" / "test-material-merge.md").read_text(encoding="utf-8")
        self.assertIn("内部撰写方法", merge_rules)
        self.assertIn("不要求在交付文档中增加独立的合并历史章节", merge_rules)
        self.assertIn("不同编号但文字相近的用例不得仅凭相似度自动合并", merge_rules)
        self.assertIn("首轮、复测和回归", merge_rules)
        self.assertIn("用例清单、详细用例和报告中的编号或数量不一致", merge_rules)

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
