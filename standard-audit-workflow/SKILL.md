---
name: standard-audit-workflow
description: Audit Chinese standard Markdown before delivery. Use when Codex needs to review a GB/T-style, group-standard, national-standard, or md2std Markdown draft; run deterministic mechanical checks through md2std-standard-auditor; perform an AI checklist review for GB/T 1.1-style issues that scripts cannot verify; interpret findings; and produce an audit report for the standard-drafting workflow.
---

# Standard Audit Workflow

This skill owns the audit task for Chinese standard drafts. It combines deterministic mechanical checks with an AI checklist review, then reports what must be fixed before DOCX generation or final delivery.

## Role Boundaries

- `standard-audit-workflow`: owns the audit workflow, review checklist, finding triage, and audit report.
- `md2std-standard-auditor`: owns mechanical Markdown audit rules and machine-readable findings.
- `standard-drafting-workflow`: owns the full drafting process and delegates audit work here.
- `md2std-standard`: owns generator input guidance and DOCX generation wrapper only.
- `md2std` / `MdToStandardWord`: owns Markdown-to-DOCX rendering only.

Do not duplicate mechanical rules in this skill. Add deterministic rules to `md2std-standard-auditor`; add non-deterministic review prompts to `references/ai-review-checklist.md`.

## Required Inputs

Ask only for missing inputs that cannot be inferred:

- Standard Markdown path.
- Intended standard type and delivery target if not obvious.
- Evidence table, source summaries, or downloaded source paths when technical content must be reviewed.
- Mechanical audit strictness: default fails on `error`; use warning-level failure only when requested.

If evidence is missing, still run mechanical audit, but mark evidence-based AI findings as `待核实` instead of inventing source support.

## Workflow

1. Inspect the Markdown enough to understand structure, scope, normative references, and technical chapters.
2. Run mechanical audit:

```powershell
# Run from this skill root.
python -X utf8 scripts/run_mechanical_audit.py input.md
```

For JSON output:

```powershell
# Run from this skill root.
python -X utf8 scripts/run_mechanical_audit.py input.md --json
```

3. Parse mechanical findings. Treat `error` as must-fix before generation; treat `warning` as review prompts.
4. Read `references/ai-review-checklist.md` and perform the AI checklist review.
5. Produce a compact audit report with these sections:
   - mechanical audit summary
   - AI checklist required fixes
   - AI checklist review prompts
   - evidence gaps or expert-review items
   - recommended next action

## AI Review Rules

AI checklist review covers items that scripts cannot reliably decide, such as whether scope wording is declarative, terms use definition-style wording, normative references are necessary, technical requirements are source-backed, modal verbs match clause type, and source evidence is sufficient.

Do not claim full compliance from this review alone. Use precise wording:

- `机械审校通过`: deterministic checks returned no errors.
- `AI 清单未发现明显问题`: checklist review found no obvious issues from available material.
- `仍需专家确认`: technical correctness, safety, measurement, test methods, legal compliance, and domain limits still need expert review.

## Finding Format

Use this table shape unless the user asks for another format:

| 严重性 | 类型 | 位置 | 问题 | 建议 |
| --- | --- | --- | --- | --- |
| error/warning/review | mechanical/ai | line/chapter | concise finding | concrete fix |

Severity guidance:

- `error`: breaks md2std contract, contradicts GB/T 1.1 essentials, or blocks generation/delivery.
- `warning`: likely drafting issue that should be reviewed.
- `review`: cannot be verified mechanically or without domain evidence.

Keep evidence-dependent findings scoped to available sources. If source documents were not provided or not read, state that limitation.
