#!/usr/bin/env python3
"""Run all SVG validation profiles and print a compact compatibility matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_svg import validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    reports = {profile: validate(args.svg, profile) for profile in ("web", "pure-svg", "wechat", "email")}
    print(f"Compatibility: {args.svg}")
    print(f"{'PROFILE':10} {'ERRORS':>7} {'WARNINGS':>9}  STATUS")
    for profile, report in reports.items():
        summary = report.get("summary", {})
        errors = summary.get("errors", 1)
        warnings = summary.get("warnings", 0)
        status = "PASS" if errors == 0 else "FAIL"
        print(f"{profile:10} {errors:7} {warnings:9}  {status}")

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(reports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
