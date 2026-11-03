#!/usr/bin/env python3
"""Validate SVG structure, safety, animation, and target-profile compatibility."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1].lower()


def issue(level: str, code: str, message: str, element: str | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {"level": level, "code": code, "message": message}
    if element:
        item["element"] = element
    return item


def parse_clock(value: str) -> float | None:
    value = value.strip().lower()
    try:
        if value.endswith("ms"):
            return float(value[:-2]) / 1000
        if value.endswith("s"):
            return float(value[:-1])
        if re.fullmatch(r"\d+(?:\.\d+)?", value):
            return float(value)
    except ValueError:
        return None
    return None


def validate(path: Path, profile: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {"file": str(path), "profile": profile, "valid_xml": False, "findings": [issue("error", "read-failed", str(exc))]}

    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        return {"file": str(path), "profile": profile, "valid_xml": False, "findings": [issue("error", "invalid-xml", str(exc))]}

    if local_name(root.tag) != "svg":
        findings.append(issue("error", "root-not-svg", "The document root must be <svg>."))
    if not root.tag.startswith("{" + SVG_NS + "}"):
        findings.append(issue("warning", "missing-svg-namespace", "Declare xmlns=\"http://www.w3.org/2000/svg\" for portability."))
    if "viewBox" not in root.attrib and "viewbox" not in root.attrib:
        findings.append(issue("error", "missing-viewbox", "Add a viewBox so the SVG scales predictably."))

    elements = list(root.iter())
    tags = Counter(local_name(el.tag) for el in elements)
    ids = [el.attrib["id"] for el in elements if el.attrib.get("id")]
    duplicates = sorted(name for name, count in Counter(ids).items() if count > 1)
    for name in duplicates:
        findings.append(issue("error", "duplicate-id", f"ID '{name}' occurs more than once."))

    if not any(local_name(child.tag) == "title" for child in list(root)):
        findings.append(issue("warning", "missing-title", "Add a direct child <title> for an accessible name."))
    if not any(local_name(child.tag) == "desc" for child in list(root)):
        findings.append(issue("warning", "missing-desc", "Add a direct child <desc> for explanatory graphics."))

    references: set[str] = set()
    for match in re.finditer(r"(?:url\(#|(?:href|xlink:href)=[\"']#)([-\w:.]+)", source, re.I):
        references.add(match.group(1))
    for ref in sorted(references - set(ids)):
        findings.append(issue("error", "missing-reference", f"Reference '#{ref}' has no matching ID."))

    event_attributes: list[str] = []
    external_urls: list[str] = []
    for el in elements:
        tag = local_name(el.tag)
        if tag == "script":
            level = "warning" if profile == "web" else "error"
            findings.append(issue(level, "script-element", "Script elements are not portable and are forbidden by this profile.", tag))
        if tag == "foreignobject":
            level = "warning" if profile == "web" else "error"
            findings.append(issue(level, "foreign-object", "foreignObject is frequently stripped or unsupported.", tag))
        for raw_name, value in el.attrib.items():
            name = local_name(raw_name)
            if name.startswith("on"):
                event_attributes.append(name)
            if name in {"href", "src"}:
                candidate = value.strip()
                if candidate and not candidate.startswith(("#", "data:")):
                    external_urls.append(candidate)
        if tag in {"animate", "animatetransform", "animatemotion", "set"}:
            dur = el.attrib.get("dur")
            if not dur:
                findings.append(issue("warning", "animation-no-duration", f"<{tag}> has no dur attribute.", tag))
            elif parse_clock(dur) is None and dur != "indefinite":
                findings.append(issue("warning", "complex-duration", f"Could not statically interpret duration '{dur}'.", tag))
            repeat = el.attrib.get("repeatCount") or el.attrib.get("repeatcount")
            if repeat == "indefinite" and profile == "email":
                findings.append(issue("warning", "email-animation", "Email clients may freeze or remove animation.", tag))

    if event_attributes:
        level = "warning" if profile == "web" else "error"
        findings.append(issue(level, "inline-events", "Inline event handlers found: " + ", ".join(sorted(set(event_attributes)))))
    if external_urls:
        level = "warning" if profile in {"web", "pure-svg"} else "error"
        findings.append(issue(level, "external-resources", "External resources reduce portability: " + ", ".join(sorted(set(external_urls))[:5])))

    style_blocks = "\n".join((el.text or "") for el in elements if local_name(el.tag) == "style")
    style_attrs = "\n".join(el.attrib.get("style", "") for el in elements)
    css_text = style_blocks + "\n" + style_attrs
    if re.search(r"@(?:-webkit-)?keyframes|animation(?:-name)?\s*:|transition\s*:", css_text, re.I):
        level = "warning" if profile == "web" else "error" if profile in {"wechat", "email"} else "warning"
        findings.append(issue(level, "css-animation", "CSS animation/transition rules may not survive the selected target."))

    if profile == "wechat":
        forbidden = {"script", "foreignobject", "iframe", "audio", "video", "canvas"}
        found = sorted(forbidden.intersection(tags))
        if found:
            findings.append(issue("error", "wechat-forbidden-elements", "Unsupported rich-text elements: " + ", ".join(found)))
        if tags["filter"]:
            findings.append(issue("warning", "wechat-filter", "SVG filters can render inconsistently in rich-text clients; test on-device."))
        if tags["use"]:
            findings.append(issue("warning", "wechat-use", "Some sanitizers rewrite <use> references; inline critical shapes when reliability matters."))

    if profile == "email":
        animated = sum(tags[name] for name in ("animate", "animatetransform", "animatemotion", "set"))
        if animated:
            findings.append(issue("warning", "email-static-fallback", "Provide a static image fallback; SVG animation support in email is inconsistent."))
        if tags["style"]:
            findings.append(issue("warning", "email-style", "Inline presentation attributes are safer than style blocks in email."))

    if len(source.encode("utf-8")) > 500_000:
        findings.append(issue("warning", "large-file", "SVG exceeds 500 KB; consider simplifying paths or externalizing nonessential raster data."))

    counts = Counter(item["level"] for item in findings)
    return {
        "file": str(path),
        "profile": profile,
        "valid_xml": True,
        "summary": {
            "errors": counts["error"],
            "warnings": counts["warning"],
            "info": counts["info"],
            "elements": len(elements),
            "animations": sum(tags[name] for name in ("animate", "animatetransform", "animatemotion", "set")),
            "bytes": len(source.encode("utf-8")),
        },
        "findings": findings,
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [f"SVG validation: {report['file']} [{report['profile']}]", ""]
    if not report.get("valid_xml"):
        lines.append("XML parsing failed.")
    for item in report.get("findings", []):
        lines.append(f"{item['level'].upper():7} {item['code']}: {item['message']}")
    summary = report.get("summary")
    if summary:
        lines.extend(["", f"Errors: {summary['errors']}  Warnings: {summary['warnings']}  Animations: {summary['animations']}  Bytes: {summary['bytes']}"])
    if not report.get("findings"):
        lines.append("No findings.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path, help="SVG file to validate")
    parser.add_argument("--profile", choices=["web", "pure-svg", "wechat", "email"], default="pure-svg")
    parser.add_argument("--json", dest="json_path", type=Path, help="Write the full JSON report to this path")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Console output format")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    report = validate(args.svg, args.profile)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.format == "json" else render_text(report))
    errors = report.get("summary", {}).get("errors", 1 if not report.get("valid_xml") else 0)
    warnings = report.get("summary", {}).get("warnings", 0)
    return 1 if errors or (args.fail_on_warning and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
