# Standard Workflow Skills

This repository manages the Codex skills used for Chinese standard drafting workflows.

## Skills

| Skill | Responsibility |
| --- | --- |
| `standard-drafting-workflow` | Evidence-backed drafting orchestration, source reading discipline, audit delegation, revision planning, and delivery checklist. |
| `standard-audit-workflow` | Mechanical audit wrapper plus AI checklist review for Chinese standard Markdown. |
| `md2std-standard` | md2std Markdown input contract and DOCX generation wrapper. |

## External Tools

The skills in this repository orchestrate these external projects but do not vendor their source code:

- `MdToStandardWord` / `md2std`: Markdown-to-DOCX renderer.
- `md2std-standard-auditor`: deterministic Markdown auditor.
- `GBMCP`: standards search and download MCP.
- `CKCEST`: policy, project, and statistics retrieval MCP.

## Local Installation

Expose each skill from the Codex skills directory by creating symbolic links. Replace the placeholders with your local checkout paths:

```powershell
New-Item -ItemType SymbolicLink -Path <codex-skills-dir>\standard-drafting-workflow -Target <repo-root>\standard-drafting-workflow
New-Item -ItemType SymbolicLink -Path <codex-skills-dir>\standard-audit-workflow -Target <repo-root>\standard-audit-workflow
New-Item -ItemType SymbolicLink -Path <codex-skills-dir>\md2std-standard -Target <repo-root>\md2std-standard
```

Keep CLI projects in a separate tools directory or install them into the active Python environment. The audit wrapper also supports `MD2STD_AUDITOR_ROOT` when the auditor checkout is elsewhere.
