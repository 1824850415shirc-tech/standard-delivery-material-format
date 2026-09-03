# Retained template evidence

- Reference DOCX: `assets/master-template.docx`
- Reference DOCX SHA-256: `8027cfde0defc18eaab5f675fac32cfe64e2bb4623850becbfee56e6491de2f4`
- Original WPT: `assets/master-template.wpt`
- Original WPT SHA-256: `04658cebb7079a820b3f534f3937a1f6edbe04171b8298e5458b79aa4a2df3d7`
- Source WPT: two A4 portrait pages: a fixed cover followed by a blank page reserved for the TOC.
- Executable DOCX: three-page minimum layout: fixed cover, real TOC field, then `{{AI_CONTENT}}` on the first page after the TOC.
- Sections: one, new-page start, no distinct first-page header/footer.
- Page: 11906 × 16838 DXA-equivalent OOXML units (A4 portrait).
- Margins: 1440 DXA (25.4 mm) on all four sides, applied uniformly to the cover, TOC, and body.
- Header distance: 851 DXA. Footer distance: 992 DXA.
- Columns: one. Document grid line pitch: 312.
- Editable slot: the paragraph whose complete text is `{{AI_CONTENT}}` in `word/document.xml`.
- Preserve: cover paragraphs, page breaks, TOC field, styles, theme, font table, settings, document properties, section properties, relationships, and content types.

## Front matter and flow

- Page 1 is the fixed cover. Preserve the cover layout and text roles. The executable template uses `{{PROJECT_NAME}}`, `{{COVER_TITLE}}`, `{{COVER_COMPANY}}`, and `{{DOCUMENT_DATE}}`; rendering defaults `{{COVER_COMPANY}}` to `XX科技`.
- The last cover paragraph ends with an explicit page break.
- Page 2 begins with the centered title `目  录` and a real `TOC \\o "1-2" \\h \\z` field. Markdown H1 uses the non-outline `文档标题` style and is excluded; Markdown H2/H3 use `heading 1`/`heading 2` and become TOC levels 1/2.
- A second explicit page break follows the complete TOC field. If the TOC expands to multiple pages, the break moves with its end.
- Generated body content begins only at `{{AI_CONTENT}}`. It starts on page 3 when the TOC fits on one page; otherwise it starts on the first page after the expanded TOC.
- Set `w:updateFields` to true, then refresh all fields in WPS or Word and save before delivery.

## Styles

- `封面`: based on Normal, centered, bold, 22 pt, source-defined East Asian cover font. Preserve this fixed cover style; do not normalize it to the body font.
- `Normal`: 14 pt Chinese, exact 28 pt line spacing, two-character first-line indent, left aligned. Generated copies normalize its font mapping to FangSong_GB2312/仿宋_GB2312.
- `文档标题`: based on Normal, bold, 15 pt, zero indent, non-outline; used only for Markdown H1 and excluded from the TOC.
- `heading 1`: based on Normal, bold, 15 pt, keep-with-next/keep-lines, outline level 0.
- `heading 2`: based on Normal, bold, 15 pt, keep-with-next/keep-lines, outline level 1.
- `heading 3`: based on Normal, bold, 14 pt, keep-with-next/keep-lines, outline level 2.
- `heading 4`: based on Normal, bold, inherited 14 pt, keep-with-next/keep-lines, outline level 3.
- `heading 5`: based on Normal, bold, inherited 14 pt, keep-with-next/keep-lines, outline level 4.
- `表格正文`: based on Normal, 四号 (14 pt), single line spacing, no first-line indent.
- `Normal Table`: default table style with 108 DXA left/right cell margins.
- Local PNG and JPEG images are inserted as centered inline shapes, scaled proportionally to the available body width and at most 72% of the body height. Markdown alt text is stored in `wp:docPr/@descr`; an optional quoted image title is rendered as a centered caption below the image.
- `toc 1` is created from `heading 1` (Markdown H2) with zero left indent. `toc 2` is created from `heading 2` (Markdown H3) with a 420-twip (about 7.41 mm/two-character) left indent. Both use zero first-line indent, dot leaders, and a right-aligned page-number tab at 9026 twips. No third TOC level is included.

## Known limitations

- Cached TOC text is not final until fields are refreshed after body generation. WPS/Word field refresh is a required delivery step.
- LibreOffice may omit Chinese glyphs when FangSong_GB2312 is unavailable on macOS. Use the unchanged DOCX in WPS for visual QA and keep the requested Windows font mapping in the final package.
- Image paths are resolved from the Markdown file and must point to local PNG or JPEG files. The renderer rejects remote URLs and missing images instead of producing an incomplete document.
