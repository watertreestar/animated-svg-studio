#!/usr/bin/env python3
"""Build a self-contained HTML review page for an SVG file."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--title", default="Animated SVG Preview")
    parser.add_argument("--template", type=Path, help="Optional custom HTML template")
    args = parser.parse_args()

    svg = args.svg.read_text(encoding="utf-8")
    if args.template:
        template = args.template.read_text(encoding="utf-8")
    else:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "preview-template.html"
        template = template_path.read_text(encoding="utf-8")

    page = template.replace("__TITLE__", html.escape(args.title)).replace("__SVG__", svg)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
