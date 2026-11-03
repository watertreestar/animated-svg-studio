#!/usr/bin/env python3
"""Apply a bundled semantic color theme to an SVG."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_themes() -> dict:
    path = Path(__file__).resolve().parent.parent / "assets" / "themes.json"
    return json.loads(path.read_text(encoding="utf-8"))


DEFAULT_ALIASES = {
    "#F3EDE1": "surface",
    "#EFE7D8": "surface",
}


THEME_FONT_STACKS = {
    "crimson-conference": "'Open Sans','Noto Sans SC','PingFang SC','Microsoft YaHei',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
    "orange-blue-architecture": "'Poppins','Noto Sans SC','PingFang SC','Microsoft YaHei',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
}


def main() -> int:
    themes = load_themes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path, nargs="?")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--theme", choices=sorted(themes), default="default-editorial")
    parser.add_argument("--list", action="store_true", help="List bundled themes and exit")
    args = parser.parse_args()

    if args.list:
        for theme_id, theme in themes.items():
            print(f"{theme_id:18} {theme['name']}: {theme['description']}")
        return 0
    if not args.svg or not args.output:
        parser.error("SVG input and --output are required unless --list is used")

    source = args.svg.read_text(encoding="utf-8")
    default = themes["default-editorial"]["tokens"]
    target = themes[args.theme]["tokens"]
    for role, old_color in default.items():
        source = re.sub(re.escape(old_color), target[role], source, flags=re.I)
    for old_color, role in DEFAULT_ALIASES.items():
        source = re.sub(re.escape(old_color), target[role], source, flags=re.I)
    if args.theme in THEME_FONT_STACKS:
        source = re.sub(
            r'font-family="[^"]*"',
            f'font-family="{THEME_FONT_STACKS[args.theme]}"',
            source,
            count=1,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(source, encoding="utf-8")
    print(f"Applied {args.theme} ({themes[args.theme]['name']}) -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
