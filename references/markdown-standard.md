# Standard Markdown contract

## Required structure

- Encode as UTF-8.
- Use exactly one H1 (`#`) for the document title.
- Start major sections at H2 (`##`), subsections at H3 (`###`), and continue without skipping levels.
- Do not use headings deeper than H5.
- Number major body headings explicitly because the retained template does not contain a linked multilevel numbering definition.
- Use `1. 标题`, `1.1 标题`, `1.1.1 标题`, and `1.1.1.1 标题` consistently.
- Use `附录 A：标题` for appendices.
- Put one blank line before and after headings, lists, tables, block quotes, and fenced code blocks.
- Treat H1 as the document title only. The generated TOC excludes H1, maps H2 to TOC level 1, and maps H3 to TOC level 2.

Example:

```markdown
# 软件配置说明书

## 1. 文档概述

### 1.1 编制目的

正文内容。

## 2. 配置说明

### 2.1 配置项
```

## Content rules

- Write formal, objective, testable Chinese.
- Preserve technical identifiers with inline code, such as `app_config.yml`, `GPU_ID`, `/data`, and `0.1.1`.
- Use fenced blocks with a language label for configuration, commands, logs, JSON, YAML, shell, Python, or plain text.
- Use unordered lists for parallel items and ordered lists for procedures.
- Use `- [ ]` only for executable checks or acceptance checklists. The DOCX renderer converts it to one compact checkbox marker; do not add another bullet or checkbox character.
- Use block quotes only for explicitly labeled `注意`、`警告`、`约束` or failure conditions. Do not write `> 说明：...`; remove the label and use a normal paragraph instead.
- Use tables only when rows share comparable fields. Keep narrative explanation outside tables.
- Do not use raw HTML, manual tabs, repeated blank lines, or decorative Unicode separators.
- Do not put credentials, tokens, secrets, or private keys into the document.
- Represent missing required facts as `【待补充：具体字段】`; never fabricate them.

## Table rules

- Provide a non-empty header row.
- Use a Markdown separator row immediately after the header.
- Keep the number of cells consistent across rows.
- Prefer short field names and concise cell content.
- Move long rationale or procedure text into prose beneath the table.

## Source transformation

When converting rough AI output:

1. Identify the document purpose and intended reader.
2. Group facts by lifecycle: overview, scope, baseline/configuration, deployment/use, change, validation, troubleshooting, and acceptance/appendix as applicable.
3. Preserve exact commands and configuration values.
4. Remove conversational lead-ins, repeated conclusions, unsupported claims, and meta-comments about being an AI.
5. Add no section merely to fill space. Use only sections supported by the source or requested standard.
6. Run `scripts/lint_markdown.py` and fix errors before rendering.
7. When naturalization is requested, follow `natural-writing.md`, audit the result, and compare protected technical tokens before and after editing.
8. Before final DOCX rendering, remove template guidance sentences and all generic `说明：` labels. Template descriptions guide drafting; they are not body content.
