# Existing DOCX import and re-render

Use this workflow when the user supplies an existing `.docx` file and asks to reformat it to the Skill standard, refresh its layout, or re-render it through the standard template. The supplied DOCX is the content baseline; this path does not open the drafting gates in `docs/HITL工作流.md`.

## Outcome

Produce three artifacts:

1. an extraction report (JSON) produced by the extractor;
2. a UTF-8 Markdown copy that conforms to `markdown-standard.md`;
3. an editable DOCX rendered from that normalized copy through `assets/master-template.docx`.

Never overwrite, rename, or delete the supplied DOCX. When the output stays in the same directory, use a name that cannot collide with the input, such as `<stem>-standard.docx` for the DOCX and `<stem>-extracted.md` / `<stem>-formatted.md` for the intermediate and normalized Markdown.

## Extract the source

1. Resolve `PYTHON_BIN` and run the extractor with a report:

   ```bash
   "$PYTHON_BIN" scripts/docx_to_markdown.py input.docx --output input-extracted.md --report input-extraction.json
   ```

2. Read the report before editing anything. It records extracted counts (headings, paragraphs, lists, tables), skipped blocks (front matter, cover, TOC, empty), inline image count, section count, and warnings.
3. The extractor skips the original cover and TOC. Open the supplied DOCX and read its cover fields (project name, document title, version, date, organization) to populate front matter when they are clearly present. Never invent these values; use `【待补充：具体字段】` when the source cover does not state them.
4. Review every warning with the user:
   - Inline images are counted, not extracted. Ask the user to supply the original images as desensitized local files, or mark each missing figure as `【待补充：图…】`. Do not fabricate or fetch replacements.
   - A multi-section source will not keep section-specific layout. Confirm the user accepts the single standard A4 layout before rendering.

## Repair the extraction

Extraction is a lossy projection of the DOCX. Repair these known losses before normalizing, always using the supplied DOCX as the reference:

- Restore flattened blocks. Multi-line YAML and other configuration, shell commands, directory trees, and log samples usually arrive as single run-on paragraphs because indentation and line breaks are collapsed. Re-detect them by content, rebuild the original line structure from the DOCX, and write them back as fenced code blocks with a language label. Never retype their values from memory.
- Restore ordered lists. Numbered source paragraphs often arrive as unordered `- ` items. Where the source sequence matters, write them back as ordered `1.` items.
- Verify every table. The extractor pads ragged rows and forces a header row. Confirm the first source row is really a header; when it is not, restructure the table instead of presenting data as a fake header. Keep cell text exactly as extracted.
- Confirm heading depth. The extractor shifts heading levels to guarantee a single H1. Check that the resulting H2/H3 hierarchy reflects the source chapter intent.

These repairs recover source formatting only. They do not authorize new content, merged conclusions, or silent deletion. When a repair has more than one materially different interpretation, preserve the extracted form and ask the user to choose.

## Normalize and render

1. Follow `direct-markdown-render.md` for inspection, normalization, validation, and the common Markdown-to-DOCX workflow in `SKILL.md`. Treat the extracted Markdown as the supplied Markdown in that workflow.
2. Use the matching built-in template only as a structural comparison when the document type is unambiguous. Keep the original chapter intent, order, and numbering; do not reorder or add chapters solely for template parity.
3. Run naturalness auditing only when the user also asks for prose editing. Pure import and re-render must preserve the source wording.
4. Complete every-page visual inspection, office field refresh, finalization, and final verification before calling the DOCX final.

## Handoff

Link the normalized Markdown and the rendered DOCX. Summarize the extraction counts, the flattened blocks restored as code, list and table repairs, skipped original elements (cover, TOC, headers/footers are rebuilt from the standard template), image placeholders awaiting user files, and the final verification status.
