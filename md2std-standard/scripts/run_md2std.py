# -*- coding: utf-8 -*-
"""Run the md2std CLI from the skill scripts directory."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    try:
        from md2std.cli import main as md2std_main
    except ModuleNotFoundError as exc:
        if exc.name != "md2std":
            raise
        sys.stderr.write(
            "md2std is not installed. Run: "
            "python -m pip install -r scripts/requirements.txt\n"
        )
        return 1
    return md2std_main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
