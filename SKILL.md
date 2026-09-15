---
name: standard-delivery-material-format
description: Create source-grounded Chinese project delivery documents as editable DOCX files, or normalize a user-supplied Markdown document to the Skill contract and render it directly, or import an existing DOCX and re-render it in the standard format. Use for project charters, research plans and reports, implementation plans, requirements specifications, detailed or database designs, test plans and cases, test reports, operations manuals, system interface documents, user operation manuals, acceptance reports, and trial-operation reports. New-document drafting uses a mandatory material and outline confirmation workflow; direct Markdown formatting and existing-DOCX import skip that drafting gate while preserving the supplied content.
---

# Standard Delivery Material Format

Use the built-in Markdown templates and the retained executable DOCX master to create Chinese delivery documents. Keep the process source-bound and editable, and select the operating mode before requesting materials or changing the input.

## Choose the operating mode

### Mode 1: draft a document

Use drafting mode when the user asks to write, create, compile, or substantially rewrite a supported delivery document and has not supplied a complete Markdown document as the content baseline.

- Follow the mandatory HITL workflow below.
- Collect source materials, prepare a source-aware outline, and wait for explicit outline confirmation before drafting the body or rendering DOCX.

### Mode 2: format and render supplied Markdown

Use direct Markdown mode when the user supplies a complete `.md` file or Markdown text and asks to adjust its format, make it conform to this Skill, or render it as DOCX.

- Treat the supplied Markdown as the approved content baseline. Do not restart material collection or request outline confirmation merely because the file does not match a built-in template.
- Read and follow `references/direct-markdown-render.md`.
- Normalize a copy of the Markdown before rendering. Preserve the original file unless the user explicitly asks to overwrite it.
- Preserve facts, meaning, technical tokens, section scope, and local evidence. Formatting authorization does not authorize invented content or a substantive rewrite.
- Deliver both the normalized Markdown and the rendered DOCX.

### Mode 3: import and re-render an existing DOCX

Use existing-DOCX mode when the user supplies a `.docx` file and asks to reformat it to the Skill standard, refresh its layout, or re-render it through the standard template.

- Follow `references/existing-docx-import.md` to extract the DOCX, repair the known extraction losses, and normalize the copy before rendering.
- Treat the extracted content as the approved content baseline. Do not restart material collection or request outline confirmation.
- Read the cover fields from the supplied DOCX where clearly present; never invent front-matter values.
- Preserve the supplied DOCX. Write the rendered output under a name that cannot collide with the input, and deliver both the normalized Markdown and the rendered DOCX.

If a Markdown file or a DOCX is only one source among several for a new document, use drafting mode. If the requested change would materially alter scope, conclusions, obligations, or chapter intent, pause for that decision instead of treating it as formatting.

## Load resources by mode

- In drafting mode, read `docs/材料清单.md` for the selected document type before requesting materials. Select the project phase, then read the matching file under `templates/项目前期/`, `templates/项目过程/`, or `templates/项目收尾/` before proposing the outline. Read `references/markdown-standard.md` and `references/natural-writing.md` before drafting the body.
- In direct Markdown mode, read `references/direct-markdown-render.md` and `references/markdown-standard.md`. Use the matching categorized template only as a structural comparison when the document type is unambiguous; do not add unsupported chapters just to match it. Read `references/natural-writing.md` only when the user also requests prose editing.
- In existing-DOCX mode, read `references/existing-docx-import.md` and `references/markdown-standard.md`. The normalization rules of `references/direct-markdown-render.md` also apply to the extracted copy. Read `references/natural-writing.md` only when the user also requests prose editing.
- Read `references/style-map.json` before rendering DOCX.
- Use `assets/master-template.docx` as the executable template. Do not rebuild the document from a blank file.
- For operation manuals and other screenshot-based documents, keep approved local images with the Markdown source and use the image syntax defined in `references/markdown-standard.md`; do not fetch or embed remote images.
- When multiple iterations of test plans, cases, execution records, or test reports must be consolidated into a test-plan-and-case deliverable, read `references/test-material-merge.md`. Apply the merge method internally; do not add a standalone merge-history chapter unless the user requests one.
- Use the Documents skill to render and inspect every final page.

## Drafting mode: mandatory HITL workflow

This workflow applies only to Mode 1. Follow the phases in order. Never combine the outline and full body in one response.

### Phase 1: request source materials

When the user asks for one of the supported documents:

1. Identify the matching file under `templates/`.
2. Read `docs/材料清单.md` and select the relevant material list.
3. Ask the user to provide existing materials before drafting, such as specifications, source code, contracts, diagrams, interface documents, operating records, screenshots, or prior documents.
4. Explain that the user may state that a material does not exist. Do not require irrelevant files.
5. Stop and wait for the user's materials or explicit statement that no further materials are available.

Do not generate a full outline or body during this phase. A short provisional chapter list is allowed only when it helps explain which materials are needed; clearly label it as provisional.

### Phase 2: inspect materials and draft the outline

After the user supplies materials:

1. Inventory every supplied file or source.
2. Separate:
   - verified facts and constraints;
   - information that can support a specific chapter;
   - conflicts between sources;
   - missing facts that block or weaken the document.
3. Use the matching template to draft the document outline.
4. Under every proposed heading, add a brief describing what the section will cover. Keep each brief concise; do not write the full body yet.
5. Mark the basis of the section as one of:
   - `来源：<材料名称或文件名>`;
   - `来源：用户已确认`;
   - `【待补充：具体信息】`.
6. Present the outline confirmation card defined in `docs/HITL工作流.md`.
7. Stop and ask the user to confirm or modify the outline.

Do not generate body paragraphs, detailed procedures, complete interface definitions, or invented project facts in this phase.

### Approval gate: explicit outline confirmation

Proceed only when the user clearly confirms the current outline, for example “确认大纲”“按这个大纲写”“大纲没问题”。

- Questions, partial feedback, silence, or general praise are not approval.
- If the user requests changes, revise the outline and ask for confirmation again.
- If new materials arrive, reassess source coverage and update the outline before asking again.
- Record which outline version was approved in the working response or generated file.

### Phase 3: generate the full body

After explicit approval:

1. Generate the body against the approved outline and matching template.
2. Use exactly one H1 title. Use numbered H2/H3 headings without skipped levels.
3. Preserve verified commands, identifiers, interfaces, paths, configuration values, scope clauses, and acceptance criteria.
4. Attribute material-specific conclusions to their source where useful.
5. Keep unsupported required facts as `【待补充：具体字段】`; never fabricate them.
6. Distinguish confirmed facts, design proposals, assumptions, and unresolved items.
7. Rewrite the draft at `standard` naturalization intensity before delivery. Preserve source-backed technical and contractual terms, but remove mechanical prose:
   - Use `应`、`须`、`不得` only for source-backed obligations, safety boundaries, or explicit operating responsibilities.
   - Describe current design and deployment as facts instead of expectations.
   - Write procedures as direct actions instead of repeated “运维人员应……”句式。
   - Avoid `通常`、`一般情况下` and `建议` unless real alternatives and their conditions are known.
   - Never output a generic `说明：` label or `> 说明：` block. Write the useful content as a normal paragraph; keep callouts only for clearly labeled attention, warning, risk, or constraint.
   - Treat every descriptive sentence in a Markdown template as drafting guidance. Do not copy guidance text into the final body.
   - For operation manuals, check that each confirmed function has an applicable role, entry point, prerequisites, steps, result verification, exception handling, and source or screenshot evidence. Delete conditional sections that do not apply instead of leaving empty chapters.
   - For test plans and cases, keep planned scope and criteria separate from actual execution results. Verify stable case IDs, detailed-case counts, requirement coverage, version applicability, execution rounds, evidence, and unresolved threshold conflicts before rendering.
8. Save the approved UTF-8 Markdown and complete the common validation, rendering, and finalization workflow below.

When templates change, also run `python3 scripts/validate_templates.py`.

If the user changes the approved chapter structure materially during body generation, pause, show the revised outline, and request approval again.

## Direct Markdown mode

Follow `references/direct-markdown-render.md` to inspect the supplied file, produce a non-destructive normalized Markdown copy, and resolve format issues before rendering. Do not apply the drafting-mode material request or outline approval gate unless the user expands the task into substantive document creation.

## Existing DOCX mode

Follow `references/existing-docx-import.md` to extract the supplied DOCX with `scripts/docx_to_markdown.py`, review the extraction report with the user, repair flattened code blocks, ordered lists, and tables against the source, and normalize the copy before the common rendering workflow. The supplied DOCX stays untouched. Do not apply the drafting-mode gates unless the user expands the task into substantive document creation.

## Common Markdown-to-DOCX completion

Both modes finish through this workflow:

1. Resolve `PYTHON_BIN` from the bundled workspace dependencies.
2. Run Markdown lint and fix every error before rendering:

   ```bash
   "$PYTHON_BIN" scripts/lint_markdown.py output.md
   ```

3. When prose was drafted or rewritten, also run the strict naturalness audit and resolve its findings without changing source-backed facts:

   ```bash
   "$PYTHON_BIN" scripts/audit_naturalness.py output.md --strict
   ```

4. Render and verify the editable DOCX:

   ```bash
   "$PYTHON_BIN" scripts/render_document.py output.md --output output.docx
   "$PYTHON_BIN" scripts/verify_document.py output.docx
   ```

5. Use the Documents skill to render every page and inspect the cover, lists, tables, callouts, images, page breaks, and font fallback. Revise the normalized Markdown and rerender until clean.
6. Refresh fields in WPS or Word, save, then run `scripts/finalize_document.py` and `scripts/verify_document.py --final` before calling the DOCX final.

## Supported templates

### 项目前期

- `templates/项目前期/项目章程.md`
- `templates/项目前期/调研方案.md`
- `templates/项目前期/调研报告.md`
- `templates/项目前期/实施方案.md`

### 项目过程

- `templates/项目过程/需求规格说明书.md`
- `templates/项目过程/详细设计说明书.md`
- `templates/项目过程/数据库设计.md`
- `templates/项目过程/测试方案与用例.md`
- `templates/项目过程/测试报告.md`
- `templates/项目过程/运维手册.md`
- `templates/项目过程/系统接口文档.md`
- `templates/项目过程/操作手册.md`

### 项目收尾

- `templates/项目收尾/验收报告.md`
- `templates/项目收尾/试运行报告.md`

## Content and privacy rules

- Default `cover_company` to `XX科技`.
- Populate `project_name`, `cover_title`, `cover_company`, `document_version`, and `document_date` in Markdown front matter. The renderer must not leave legacy company text or cover placeholders in a generated DOCX.
- Do not add personal names, contact details, real organization names, credentials, tokens, private keys, or unapproved customer information.
- Never treat a contract, tender document, or old manual as proof of the current implementation without corroboration.
- When source files conflict, report the conflict and ask for a decision instead of selecting a convenient value.
- Keep the template's section descriptions as drafting guidance; replace them with source-backed content only after outline approval.
