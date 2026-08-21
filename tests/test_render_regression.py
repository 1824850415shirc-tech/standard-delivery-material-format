#!/usr/bin/env python3
"""Regression checks for cover metadata, checklist spacing, and callout handling."""

from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from docx import Document
from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_document import render  # noqa: E402
from verify_document import verify  # noqa: E402


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


class RenderRegressionTest(unittest.TestCase):
    def test_cover_checklists_and_callouts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "regression.docx"
            render(
                ROOT / "tests" / "fixtures" / "render-regression.md",
                ROOT / "assets" / "master-template.docx",
                output,
            )

            report = verify(output)
            self.assertTrue(report["ok"], report["errors"])

            document = Document(output)
            body_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
            self.assertIn("XX科技", body_text)
            self.assertNotIn("这里只用于指导写作", body_text)
            self.assertEqual(document.core_properties.author, "XX科技")
            self.assertEqual(document.core_properties.last_modified_by, "XX科技")

            checklist_paragraphs = [
                paragraph
                for paragraph in document.paragraphs
                if paragraph.text.startswith(("已确认维护窗口", "已核对配置文件"))
            ]
            self.assertEqual(len(checklist_paragraphs), 2)
            for paragraph in checklist_paragraphs:
                self.assertNotIn("[ ]", paragraph.text)
                self.assertFalse(paragraph._p.xpath("./w:pPr/w:pBdr"))
                self.assertTrue(paragraph._p.xpath("./w:pPr/w:numPr"))

            explanation = next(
                paragraph for paragraph in document.paragraphs if paragraph.text.startswith("这段内容会转成普通正文")
            )
            self.assertFalse(explanation.text.startswith("说明："))
            self.assertFalse(explanation._p.xpath("./w:pPr/w:pBdr"))

            warning = next(paragraph for paragraph in document.paragraphs if paragraph.text.startswith("注意："))
            self.assertTrue(warning._p.xpath("./w:pPr/w:pBdr"))

            with zipfile.ZipFile(output) as package:
                numbering = etree.fromstring(package.read("word/numbering.xml"))
            checkbox_levels = numbering.xpath("//w:lvl[w:lvlText/@w:val='□']", namespaces=NS)
            self.assertTrue(checkbox_levels)
            level = checkbox_levels[0]
            self.assertEqual(level.xpath("string(w:suff/@w:val)", namespaces=NS), "space")
            self.assertEqual(level.xpath("string(w:pPr/w:ind/@w:left)", namespaces=NS), "480")
            self.assertEqual(level.xpath("string(w:pPr/w:ind/@w:hanging)", namespaces=NS), "240")


if __name__ == "__main__":
    unittest.main()
