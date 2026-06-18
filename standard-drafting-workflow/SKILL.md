---
name: standard-drafting-workflow
description: |
  Use for end-to-end Chinese standard drafting: collect intent, search and read real evidence,
  build an evidence table, draft md2std Markdown, delegate audit to standard-audit-workflow,
  revise findings, and delegate DOCX generation to md2std-standard.
---

# Standard Drafting Workflow

This skill owns evidence-backed standard drafting. It does not implement audit rules or DOCX rendering: delegate audit to `standard-audit-workflow`, and delegate generation to `md2std-standard`.

## References

Read only when needed:

- `references/gbt-writing-rules.md` — GB/T 1.1-2020 writing rules summary.
- `references/toolchain.md` — tool responsibilities and handoff commands.

Companion skills:

- `gbmcp-standards`: standards search, metadata, and download boundaries.
- `ckcest`: policy, project, and statistics retrieval.
- `standard-audit-workflow`: mechanical audit plus AI checklist review.
- `md2std-standard`: md2std input contract and DOCX generation.

## Non-Negotiable Rules

- Read source standards, policies, papers, or user documents before drafting technical clauses.
- Do not fabricate data, dates, standard numbers, policy names, references, indicators, limits, test methods, issuing bodies, or implementation dates.
- Use database/tool results as evidence first: GBMCP for standards, CKCEST for policies/projects/statistics, and extracted user-provided documents for source text.
- Keep normative references minimal and necessary. Prefer fewer than 8 unless the scope genuinely requires more.
- Every final clause containing technical requirements, data, limits, classifications, or test methods should be traceable to a source, user requirement, or clearly marked drafting judgment.

## Workflow

### 1. Collect Intent

Establish the fields below. Ask only for items that cannot be inferred:

```text
主题：
标准化对象：
拟定标准类型：
适用范围：
核心技术章节：
需查证的问题：
预期交付：
```

Also note source materials, domain risks, region/industry constraints, and whether DOCX/Word COM post-processing is required.

### 2. Search Real Evidence

Use retrieval before writing requirements:

- GBMCP for similar standards, candidate normative references, downloadable texts, terms, classifications, methods, limits, tests, and inspection rules.
- CKCEST for policy basis, research projects, technology trends, and statistical indicators.

Record source title, identifier, issuing body, date, URL/tool result ID, and downloaded file path. Mark unresolved facts as `待核实` and keep them out of final requirements.

### 3. Extract and Map Sources

For each useful source, extract/read the text and summarize facts into:

- scope and standardization object
- terms and definitions
- classifications or system structure
- technical requirements
- test/inspection methods
- labels, packaging, storage, transport, safety, or environmental requirements
- candidate normative references
- data and policy basis

Keep a compact evidence table. Do not paste long source text into the final standard.

### 4. Decide References

Separate:

- Normative references: documents whose content forms necessary provisions.
- Bibliography: background, policy, research, data, or informative references.

Rules:

- Every normative reference listed in `# 规范性引用文件` must start with an explicit registration marker, for example `{{std:GB/T 11615}} GB/T 11615  地热资源地质勘查规范`.
- Every registered normative reference must be cited in the body with `{{std:...}}`.
- Every body `{{std:...}}` citation must match a registered normative reference entry or its derivable dated/undated alias.
- Use dated references when citing a specific chapter, clause, figure, table, or formula, or when future changes cannot be automatically accepted.
- If no normative references exist, write exactly: `本文件没有规范性引用文件。`
- Do not mix normative references into `# 参考文献`.

### 5. Draft md2std Markdown

Only draft after evidence is populated and source documents have been read. Follow `md2std-standard` for syntax details; do not restate generator syntax here.

Drafting rules:

- Use `本文件` for the document itself.
- Do not hand-write generated heading, table, figure, or formula numbers.
- Use `应/不应` for requirements, `宜/不宜` for recommendations, `可/不必` for permissions.
- In `# 范围`, use statement clauses, not requirements.
- Keep citations traceable to the evidence table.

### 6. Audit and Revise

Delegate audit to `standard-audit-workflow`.

Mechanical audit, from the audit skill root:

```powershell
python -X utf8 scripts/run_mechanical_audit.py input.md
python -X utf8 scripts/run_mechanical_audit.py input.md --json
```

Then perform the audit skill's AI checklist review. Fix every mechanical `error` and every AI `必须修改` item. Treat mechanical `warning` and AI `建议复核` items as review prompts.

### 7. Convert to DOCX

Use `md2std-standard` after audit/revision.

From the generation skill root:

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

Parser or generator failures are drafting errors; revise the Markdown until conversion succeeds.

### 8. Deliver

Deliver:

- Final Markdown path.
- DOCX path if requested.
- Evidence summary and source files read.
- Audit result from `standard-audit-workflow`.
- md2std conversion status.
- Remaining assumptions, unread sources, or expert-review items.

Do not claim full compliance if only mechanical audit ran. Distinguish mechanical format/reference checks, AI checklist review, and technical expert review.

## Quality Checklist

- User intent and scope are explicit.
- Real standards/policies/data were searched and read before drafting.
- No data or source facts were fabricated.
- Evidence sources are traceable.
- Normative references and bibliography are separated.
- Normative references are necessary and cited.
- Scope uses statement clauses only.
- Terms use definition-style wording.
- Requirements use correct modal verbs.
- `standard-audit-workflow` reports no mechanical errors.
- md2std DOCX generation succeeds.
