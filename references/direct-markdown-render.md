# Direct Markdown formatting and rendering

Use this workflow only when the user supplies a complete Markdown document as the content baseline and asks to format it or render it as DOCX.

## Outcome

Produce two artifacts:

1. a UTF-8 Markdown copy that conforms to `markdown-standard.md`;
2. an editable DOCX rendered from that normalized copy through `assets/master-template.docx`.

Do not overwrite the supplied Markdown unless the user explicitly requests it. Prefer a sibling name such as `<stem>-formatted.md` and `<stem>.docx`, or another clear user-requested name.

## Inspect before editing

1. Read the entire Markdown file and inventory every referenced local image or attachment.
2. Identify the title, apparent document type, existing front matter, heading hierarchy, tables, code blocks, lists, callouts, and unresolved placeholders.
3. Record exact technical tokens whose spelling must survive formatting, including commands, paths, identifiers, versions, interface names, configuration keys, thresholds, and contractual terms.
4. If the document type clearly matches a built-in template, use that template only to detect structural conventions. Do not import its guidance text or add empty chapters solely for template parity.

Missing project facts do not trigger the drafting workflow. Preserve existing placeholders or use a precise `【待补充：具体字段】` marker when a required cover field cannot be derived safely.

## Normalize the Markdown

Make presentational and structural repairs that preserve the supplied meaning:

- Add or repair YAML front matter with `project_name`, `cover_title`, `cover_company`, `document_version`, and `document_date`. Derive `cover_title` from the H1 when unambiguous; default only `cover_company` to `XX科技`; never invent the other values.
- Keep exactly one H1 as the document title. Normalize body headings to continuous H2-H5 levels and explicit hierarchical numbering; do not silently rename headings in a way that changes their intent.
- Add the blank lines required around headings, lists, tables, block quotes, and fenced code blocks.
- Repair list markers, fenced-code language labels, Markdown tables, inline-code spans, supported attention/warning/constraint callouts, and local image syntax.
- Keep image paths relative to the normalized Markdown file. Verify that each local image exists and that its optional caption remains accurate. Never fetch a remote image as part of formatting.
- Remove raw HTML, template guidance comments, decorative separators, generic `说明：` labels, and other syntax prohibited by `markdown-standard.md` when removal does not discard source content.
- Split or reshape content only when required for valid Markdown or readable A4 rendering, and preserve every source-backed value.

Formatting does not authorize factual completion, new conclusions, content expansion, or silent deletion. If a repair has more than one materially different interpretation, preserve the original content and ask the user to choose. A missing or remote image that is necessary to the document must be reported rather than silently omitted.

## Validate and render

1. Save the normalized Markdown copy before rendering.
2. Run `scripts/lint_markdown.py` and fix all errors. Treat warnings as review items and resolve those relevant to the document.
3. If wording was changed at the user's request, follow `natural-writing.md`, run `scripts/audit_naturalness.py --strict`, and compare the protected technical tokens before and after editing.
4. Complete the common Markdown-to-DOCX workflow in `SKILL.md`, including structural verification, every-page visual inspection, office field refresh, finalization, and final verification.

In the handoff, link both artifacts and summarize formatting changes, unresolved placeholders, omitted or blocked media, and the final verification status.
