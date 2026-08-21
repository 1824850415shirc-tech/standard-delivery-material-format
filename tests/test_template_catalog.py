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
