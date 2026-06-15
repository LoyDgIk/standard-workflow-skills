---
name: md2std-standard
description: Prepare and convert Chinese standard document Markdown with md2std. Use when Codex needs the md2std generator input contract, cover metadata such as draft_version and cover_form_protection, table/figure/formula caption and cross-reference syntax, or DOCX generation through scripts/run_md2std.py. This skill does not own the audit workflow; run auditing from standard-audit-workflow before generation.
---

# md2std Standard

## Core Rule

Use the current md2std Markdown contract and the default cover-blueprint DOCX generation path. Do not suggest alternate generation backends in user-facing output.

This skill is generation-facing only. It documents what the `md2std` generator accepts and how to run the generator wrapper. Audit orchestration belongs to `standard-audit-workflow`; deterministic audit rules belong to `md2std-standard-auditor`.

Never hand-write generated numbering in Markdown:

- Do not write heading numbers such as `4.2.1` in headings.
- Do not write caption labels such as `表1`、`图A.1`、`式（1）` in titles.
- Do not write LaTeX `\tag{...}`.
- Do not use old cross-reference syntax `{@id}`.

## Workflow

1. Inspect the source brief, PDF-converted Markdown, or example document before writing.
2. Create or normalize a single Markdown file with YAML front matter at the top.
3. Use typed anchors for every referenced table, figure, and equation.
4. Use `{{...}}` cross references only after the target anchor exists.
5. Run md2std through this skill's `scripts/run_md2std.py` wrapper and fix parser warnings/errors before delivering the DOCX.
6. Use Word COM post-processing only when final Word pagination, field update, and continuation-table splitting are required and Windows Microsoft Word is available.

For a compact complete sample, read `examples/智能井盖运行维护规范.md` inside this skill.

## Front Matter

Use YAML front matter as the only source for cover and boilerplate metadata:

```yaml
---
standard_type: 团体标准
number: T/XXXX XXX—XXXX
replaces: T/XXXX XXX—2020
title: 标准中文名称
title_en: English title
draft_version: （征求意见稿）
ics: "27.010"
ccs: D10
publish_date: XXXX-XX-XX
implement_date: XXXX-XX-XX
publisher: 发布单位
odd_even_pages: false
cover_form_protection: false
foreword:
  patent_note: true
  proposer: 提出单位
  owner: 归口单位
  draft_orgs:
    - 起草单位一
  drafters:
    - 起草人一
  replace_changes:
    - 更改了……
  extra_notes:
    - 本文件为首次发布。
introduction: |
  引言第一段。
---
```

Use `standard_type: 国家标准` or a `GB...` standard number for national standards. Quote ICS values and other values that may be parsed as numbers.

Use `draft_version` to set the cover legacy dropdown for 草案版次. Common values are `草案版次选择`, `（工作组讨论稿）`, `（征求意见稿）`, `（送审讨论稿）`, `（送审稿）`, and `（报批稿）`; shorthand values without full-width parentheses, such as `征求意见稿`, are normalized.

Use `cover_form_protection: true` only when the generated Word cover needs legacy `FORMDROPDOWN` controls to be active immediately. It enables forms protection for the cover section only and keeps later sections editable. The command-line flags `--cover-form-protection` and `--no-cover-form-protection` override YAML.

`foreword.extra_notes` supports nested dash items:

```yaml
extra_notes:
  - 本文件及其所代替文件的历次版本发布情况为：
  - - 1994年首次发布为GB 15082—1994；
    - 本次为第三次修订。
```

## Body Structure

Write chapters in standard order when applicable:

```md
# 范围
# 规范性引用文件
# 术语和定义
# 符号和缩略语
# 技术章标题
# 附录 规范性 附录标题
# 参考文献
# 索引
```

Use Markdown heading depth for titled clauses and let md2std number them:

```md
# 范围
## 一般要求
### 子要求
#### 更细要求
```

For no-title clauses, use explicit level syntax instead of writing the visible number:

```md
{无标题条:2} 这是 X.Y 级无标题条正文。
{无标题条:3} 这是 X.Y.Z 级无标题条正文。
{无标题条:4} 这是 X.Y.Z.W 级无标题条正文。
```

Do not use `{无标题条:n}` in foundational chapters: `# 范围`, `# 规范性引用文件`,
`# 术语和定义`, or `# 符号和缩略语`. Write those sections as ordinary
paragraphs, normative-reference entries, symbol entries, or term blocks. Use
no-title clauses only in technical chapters after `# 术语和定义`, or in
appendices.

If source text contains old manual no-title clauses such as `4.2.1 正文`, keep them as ordinary text only if preserving source evidence is necessary; otherwise convert them to `{无标题条:n}`.

Use a standalone page break marker when a standard requires an explicit new page:

```md
<!-- pagebreak -->
```

Also accepted: `<!-- md2std:pagebreak -->`、`\pagebreak`、`\newpage`、`[pagebreak]`.

## Lists, Notes, and Examples

Use plain Markdown list syntax. Let Word numbering styles render the final list labels:

```md
- 破折号列项；
- 另一个破折号列项。

1. 一级有序列项，渲染为 a)。
2. 另一个一级有序列项：
   1. 二级有序列项，渲染为 1)。
   2. 另一个二级有序列项。
```

Use standard note/example prefixes directly:

```md
注：这是注。
注1：这是编号注。
示例：这是示例。
示例1：这是编号示例。
```

For examples that contain several blocks, close the example explicitly:

```md
示例：

第一段示例内容。

{表：#tbl:example} 示例表

| 项目 | 值 |
| --- | --- |
| A | 1 |

第二段示例内容。

{示例结束}
```

Without `{示例结束}`, the single-paragraph example style remains available.

## Inline Superscript and Subscript

md2std supports Typora/Obsidian-style extended Markdown for simple inline superscript and subscript in ordinary paragraphs, list items, notes, examples, headings, and formula symbol explanations:

```md
2^10^       # renders as 2¹⁰
H~2~O       # renders as H₂O
T~r~        # renders T with r as subscript
m^3^/d      # renders cubic metres per day
```

Rules:

- Use `^...^` for superscript and `~...~` for subscript.
- Use this for short symbols, units, and formula explanations such as `Q~e~ ——统计期内实际开采的地热流体总量`.
- `<sup>...</sup>` and `<sub>...</sub>` are also accepted for compatibility, but the `^...^` and `~...~` forms are preferred in md2std Markdown.
- For full equations, keep using display LaTeX with typed equation anchors.

When a symbol in running text must keep the same math font as equations, use an inline formula fragment:

```md
式中，$$T_r$$ 为热储温度，$$Q_e$$ 为统计期内实际开采的地热流体总量。
```

Inline `$$...$$` fragments are converted to Word native math (OMML). Use them for mathematical variables, not for long prose or generated equation numbers.

## Terms

In `# 术语和定义`, the renderer inserts the default lead before local term
entries when it is omitted:

```md
下列术语和定义适用于本文件。
```

If the chapter is empty, the renderer inserts:

```md
本文件没有需要界定的术语和定义。
```

If the terms are only imported from another standard, write `……界定的术语和定义适用于本文件。`.
If both imported terms and local entries are used, write `……界定的以及下列术语和定义适用于本文件。`.

Write each local term as a second-level heading. Separate Chinese and English terms with two spaces:

```md
## 地热温泉  geothermal hot spring

由地球内部热源加热……
```

Alternatively, use the explicit term marker when a term title should not be a Markdown heading:

```md
{术语：地热温泉 | geothermal hot spring}

由地球内部热源加热……
```

Do not include the generated term number in Markdown. The renderer makes both the Chinese and English term bold. Do not italicize ordinary English equivalents. Use Markdown italic only for names that should be italic in the source text, such as Latin scientific or taxonomic names:

```md
{术语：大肠埃希氏菌 | *Escherichia coli*}
```

## Symbols and Abbreviations

If `# 符号和缩略语` is present, the renderer inserts a default lead when it
is omitted. Write one of these leads explicitly when the wording needs to
distinguish symbols from abbreviations:

```md
下列符号适用于本文件。
下列缩略语适用于本文件。
下列符号和缩略语适用于本文件。
```

Then list each symbol or abbreviation as an ordinary paragraph, without a generated no-title clause marker.

## Normative References

In `# 规范性引用文件`, write one standard per paragraph:

```md
GB 5749  生活饮用水卫生标准
GB/T 11615  地热资源地质勘查规范
```

The renderer inserts the GB/T 1.1 fixed lead before the list when it is
omitted. If writing the lead manually, use the fixed wording and do not
paraphrase it.

According to GB/T 1.1—2020, 8.6.3.2, list normative references in this overall order:

1. 国家标准化文件
2. 行业标准化文件
3. 本行政区域的地方标准化文件（仅适用于地方标准化文件的起草）
4. 团体标准化文件
5. ISO、ISO/IEC或IEC标准化文件
6. 其他机构或组织的标准化文件
7. 其他文献

Within the same type:

- 国家标准、ISO或IEC标准：按标准顺序号（文件编号中的阿拉伯数字）从小到大排列，与标准代号无关。例如，`GB 2760` 排在 `GB 27950` 之前，`ISO 9001` 排在 `ISO 14001` 之前。
- 行业标准、地方标准、团体标准、其他国际标准化文件：先按文件代号（标准编号中的字母部分）的拉丁字母和/或阿拉伯数字顺序排列，再按文件顺序号从小到大排列。

Notes:

- 标准中不应引用法律法规等政策性文件。
- 文件清单不应包含不能公开获得的文件、资料性引用文件、标准编制过程中参考过的文件。
- 同类标准中不区分强制性标准和推荐性标准，统一按顺序号排序。
- 如有特殊领域要求（如工程建设标准），需按“先工程建设标准、后产品标准”的顺序，依标准编号顺序排列。

Reference standard numbers with exact text matching:

```md
各阶段工作应符合{{std:GB/T 11615}}的规定。
```

If there are no normative references, write:

```md
# 规范性引用文件

本文件没有规范性引用文件。
```

An empty `# 规范性引用文件` chapter is also accepted; the renderer inserts
`本文件没有规范性引用文件。`.

## Tables

Put the table caption marker immediately before the table. The caption title must be pure title text:

```md
{表：#tbl:test-speed} 测试车速

| 最高设计车速 | 测试车速 |
| --- | --- |
| ≤45 | 80%最高设计车速 |

{单位} 单位为千米每小时
```

Rules:

- Use typed IDs: `#tbl:id`.
- Do not write `表1` or `表A.1` in the caption text.
- GFM tables and HTML `<table>` are supported.
- Use HTML tables when source tables need `rowspan`, `colspan`, empty merged cells, or fine border control.
- Use inline formula `$$...$$` inside ordinary paragraphs, table cells, table notes, figure paragraphs, sources, and footnotes. `<eq>...</eq>` is legacy-compatible only; do not use it in new examples.
- Table headers are centered by default. Body cells with short values, numbers, symbols, or codes are centered by default; longer explanatory text is left-aligned.
- In HTML tables, override cell alignment with `data-align="left"`, `data-align="center"`, `data-align="right"`, or `data-align="decimal"`. `decimal` is a practical numeric-column control and is emitted as right alignment.
- Table unit, source, and footnotes are block add-ons after the target table: `{单位} ...`, `{来源} ...`, `{脚注} ...`.
- In table cells, write ordinary notes as inline `〔注：...〕`; a cell may contain only notes, and consecutive notes in the same cell are numbered automatically.
- In table cells, write footnote reference points as inline `〔脚注〕`; the matching footnote content is a following block `{脚注} ...`.
- Do not use removed table add-ons such as `{表注：...}`、`{表单位：...}`、`{表脚注a：...}`.
- Continuation captions such as `表1　原表题（续）` are generated only by Word COM post-processing after real pagination.

HTML table example:

```md
{表：#tbl:limit} 限值

<table data-border-outer="thick" data-border-inner="thin">
  <tr>
    <th rowspan="2" data-border-right="thick">类别</th>
    <th colspan="2">指标</th>
  </tr>
  <tr>
    <th>限值</th>
    <th data-border-bottom="none">说明</th>
  </tr>
  <tr>
    <td>一类</td>
    <td data-align="decimal">12.5</td>
    <td data-align="left">同上</td>
  </tr>
  <tr>
    <td colspan="3">〔注：空单元格保持为空，“同上”按普通文本输出。〕</td>
  </tr>
</table>
```

`data-border-outer`, `data-border-inner`, and cell-level `data-border-top/right/bottom/left` accept `none`, `thin`, or `thick`. Invalid merge or border values should be fixed in Markdown instead of relying on Word cleanup.
Header cells use a thick bottom border by default; explicit `data-border-bottom` on a cell overrides this default.

## Figures

Use Markdown image syntax with a typed anchor in the alt text:

```md
![分级流程图 {#fig:flow}](images/flow.png)
```

Rules:

- Use typed IDs: `#fig:id`.
- Do not write `图1` or `图A.1` in the figure title.
- Resolve relative image paths from the Markdown file location.
- Figure unit, source, and footnotes use the same block add-ons as tables: `{单位} ...`, `{来源} ...`, `{脚注} ...`.
- Use `{图标引}` for automatically numbered figure key explanations; numbering restarts for each figure.
- Use `{图段}` only for paragraphs that belong inside the figure block. Ordinary unmarked paragraphs remain body text.
- Do not use removed figure add-ons such as `{图注：...}`、`{图单位：...}`、`{图脚注a：...}`、`{图标引1：...}`、`{图段：...}`.

Subfigure group example:

```md
{图：#fig:subparts} 分图示例

{单位} 关于单位的陈述

{分图组:2}

![第一张分图题](images/subfigure-a.png)

![第二张分图题](images/subfigure-b.png)

{图标引} 第一项说明

{图标引} 第二项说明

{图段} 图内段落内容〔注：图内普通注内容。〕

{脚注} 图脚注内容。

{来源} 资料来自图样设计文件。
```

## Equations

Use LaTeX display math with a typed anchor after the closing `$$`:

```md
按{{eq:depth:label}}计算：

$$H = \frac{T_{r} - T_{0}}{G} + h$${#eq:depth}

式中：

H ——循环深度，单位为米（m）；

$$T_r$$ ——热储温度，单位为摄氏度（℃）；
```

Rules:

- Use typed IDs: `#eq:id`.
- Do not use `\tag{1}`.
- Do not write visible equation numbers manually.
- Use `式中：` and following symbol explanations as ordinary paragraphs; use inline `$$...$$` for symbols that should match equation math font, and use `~...~` or `^...^` for simple text-level subscript/superscript units.

## Cross References

Use only double-brace references:

```md
{{tbl:classify}}        # 仅编号，如 1 或 A.1
{{tbl:classify:label}}  # 表1 或 表A.1
{{tbl:classify:full}}   # 表1　温泉利用分类
{{fig:flow:label}}      # 图1
{{fig:flow:full}}       # 图1　分级流程图
{{eq:depth}}            # 1
{{eq:depth:label}}      # 式（1）
{{std:GB/T 11615}}      # GB/T 11615
```

Rules:

- Target IDs must exist and must match the reference type.
- IDs must be unique within their type.
- Use `:label` when the sentence needs the type name.
- Use `:full` when the sentence needs the complete caption.

## Appendices

Write appendix headings as first-level headings. Let md2std assign A, B, C:

```md
# 附录 规范性 分级判定流程

## 判定步骤

……

# 附录 资料性 数据示例
```

Appendix table, figure, and equation numbers automatically use appendix scopes such as `表A.1`、`图B.1`、`式（A.1）`.

## References and Index

Reference section is optional:

```md
# 参考文献

GB/T 1.1—2020　标准化工作导则……
ISO 11783　Tractors……
```

Index section is optional. Use pinyin initial groups and `术语：位置列表` entries:

```md
# 索引

## B

- 必备要素：3.2.5，6.2.2.1，6.2.2.3
- 标准：3.1.2，4.1，4.2
```

Do not hand-write dot leaders; Word styles generate the index layout.

## Conversion Commands

Install the generator dependency once when it is not available:

```powershell
python -m pip install -r scripts/requirements.txt
```

Run conversion through the skill wrapper:

```powershell
python -X utf8 scripts/run_md2std.py examples/智能井盖运行维护规范.md -o examples/智能井盖运行维护规范.docx
```

Override standard kind only when auto-detection is not enough:

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --kind national
python -X utf8 scripts/run_md2std.py input.md -o output.docx --kind group
```

Use Word COM post-processing only for final DOCX pagination/field work:

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

The post-process step requires Windows Microsoft Word and `pywin32`. It updates fields, repaginates, saves, and handles continuation tables based on actual Word pagination.

Enable cover legacy dropdowns only when needed:

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --cover-form-protection
```

This activates legacy `FORMDROPDOWN` controls on the cover by protecting only the cover section. Use `--no-cover-form-protection` to override `cover_form_protection: true` in YAML.

## Generation Check

Before final delivery, `standard-audit-workflow` should already have run mechanical audit and AI checklist review. This skill's final check is only that DOCX generation succeeds with:

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx
```
