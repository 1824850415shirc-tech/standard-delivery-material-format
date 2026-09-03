---
name: standard-delivery-material-format
description: Create source-grounded Chinese project delivery documents as editable DOCX files from categorized Markdown templates through a mandatory human-in-the-loop workflow. Use for project charters, research plans and reports, implementation plans, requirements specifications, detailed or database designs, test plans and cases, test reports, operations manuals, system interface documents, user operation manuals, acceptance reports, and trial-operation reports. First collect source materials, then propose an outline for explicit confirmation, and only after approval generate natural prose and render it through the retained document styles.
---

# Standard Delivery Material Format

Use the built-in Markdown templates and the retained executable DOCX master to create Chinese delivery documents. Keep the process human-controlled, source-bound, and editable.

## Load resources

- Read `docs/材料清单.md` for the selected document type before requesting materials.
- Select the project phase, then read the matching file under `templates/项目前期/`, `templates/项目过程/`, or `templates/项目收尾/` before proposing the outline.
- Read `references/markdown-standard.md` and `references/natural-writing.md` before drafting the body.
- Read `references/style-map.json` before rendering DOCX.
- Use `assets/master-template.docx` as the executable template. Do not rebuild the document from a blank file.
- For operation manuals and other screenshot-based documents, keep approved local images with the Markdown source and use the image syntax defined in `references/markdown-standard.md`; do not fetch or embed remote images.
- When multiple iterations of test plans, cases, execution records, or test reports must be consolidated into a test-plan-and-case deliverable, read `references/test-material-merge.md`. Apply the merge method internally; do not add a standalone merge-history chapter unless the user requests one.
- Use the Documents skill to render and inspect every final page.

## Mandatory HITL workflow

Follow the phases in order. Never combine the outline and full body in one response.

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
8. Save the approved UTF-8 Markdown and run:

   ```bash
   "$PYTHON_BIN" scripts/lint_markdown.py output.md
   "$PYTHON_BIN" scripts/audit_naturalness.py output.md --strict
   ```

9. Resolve `PYTHON_BIN` from the bundled workspace dependencies, then render and verify the editable DOCX:

   ```bash
   "$PYTHON_BIN" scripts/render_document.py output.md --output output.docx
   "$PYTHON_BIN" scripts/verify_document.py output.docx
   ```

10. Render every page with the Documents skill and inspect the cover, lists, tables, callouts, page breaks, and font fallback. Revise and rerender until clean.
11. Refresh fields in WPS or Word, save, then run `scripts/finalize_document.py` and `scripts/verify_document.py --final` before calling the DOCX final.

When templates change, also run `python3 scripts/validate_templates.py`.

If the user changes the approved chapter structure materially during body generation, pause, show the revised outline, and request approval again.

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
