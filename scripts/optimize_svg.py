#!/usr/bin/env python3
"""Conservatively clean SVG without rewriting paths or animation references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import xml.etree.ElementTree as ET


def strip_editor_nodes(root: ET.Element) -> None:
    removable = {"metadata", "namedview"}
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag.rsplit("}", 1)[-1].lower() in removable:
                parent.remove(child)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    source = args.svg.read_text(encoding="utf-8")
    source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
    root = ET.fromstring(source)
    strip_editor_nodes(root)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    output = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    output = re.sub(r">\s+<", "><", output).strip() + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    before = len(source.encode("utf-8"))
    after = len(output.encode("utf-8"))
    print(f"Wrote {args.output} ({before} -> {after} bytes, {before - after} saved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
