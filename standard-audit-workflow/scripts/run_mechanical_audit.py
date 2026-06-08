# -*- coding: utf-8 -*-
"""Run mechanical audit for standard-audit-workflow.

This is a workflow entrypoint. The deterministic rules live in
md2std-standard-auditor.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys


def _candidate_auditor_roots() -> list[Path]:
    roots: list[Path] = []
    env_root = os.environ.get("MD2STD_AUDITOR_ROOT")
    if env_root:
        roots.append(Path(env_root))

    skill_root = Path(__file__).resolve().parents[1]
    ai_agent_root = next(
        (parent for parent in skill_root.parents if parent.name == "AI_AGENT"),
        None,
    )
    roots.extend(
        [
            skill_root.parent / "md2std-standard-auditor",
        ]
    )
    if ai_agent_root:
        roots.append(ai_agent_root / "CLI" / "md2std-standard-auditor")
    return roots


def _add_local_auditor_source():
    for candidate in _candidate_auditor_roots():
        if (candidate / "md2std_standard_auditor").is_dir():
            sys.path.insert(0, str(candidate))
            return


def _normalize_args(argv: list[str]) -> list[str]:
    normalized: list[str] = []
    for arg in argv:
        if arg == "--json":
            normalized.extend(["--format", "json"])
        else:
            normalized.append(arg)
    return normalized


def main(argv: list[str] | None = None) -> int:
    argv = _normalize_args(list(argv or []))
    try:
        from md2std_standard_auditor.cli import main as auditor_main
    except ModuleNotFoundError as exc:
        if exc.name != "md2std_standard_auditor":
            raise
        _add_local_auditor_source()
        try:
            from md2std_standard_auditor.cli import main as auditor_main
        except ModuleNotFoundError:
            sys.stderr.write(
                "md2std-standard-auditor is not installed. Run one of:\n"
                "  python -m pip install -e <path-to-md2std-standard-auditor>\n"
                "  set MD2STD_AUDITOR_ROOT=<path-to-md2std-standard-auditor>\n"
            )
            return 1
    return auditor_main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
