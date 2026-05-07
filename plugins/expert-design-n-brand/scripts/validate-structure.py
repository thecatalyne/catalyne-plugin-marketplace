#!/usr/bin/env python3
"""
validate-structure.py — Structural invariant checker for rendered brand artifacts.

Usage:
    validate-structure.py --artifact <path-to-rendered-file> --schema <oracle-key>
    validate-structure.py --artifact ./brand-assets/brand-guidelines.html --schema brand-guidelines

Output:
    JSON verdict object to stdout. Exit code 0 if every check passes, 1 otherwise.

Oracle:
    Reads skills/brand-export/references/artifact-schemas.yaml (relative to the
    plugin root, resolved via ${CLAUDE_PLUGIN_ROOT} if set, else walked upward
    from this script).

Design:
    The validator checks PRESENCE and ORDER of structural anchors declared in
    the oracle — it does not inspect content inside those anchors. Content is
    the LLM's creative surface per rendering-rules.md Rule 0.

Dependencies:
    Python 3.8+, PyYAML. If PyYAML is unavailable, the script prints an install
    hint and exits 2 (distinct from validation failure).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write(
        "validate-structure.py: PyYAML is required. Install with `pip install pyyaml`.\n"
    )
    sys.exit(2)


def find_plugin_root() -> Path:
    """Resolve plugin root from env var or by walking up from this script."""
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        return Path(env_root)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise SystemExit(
        "validate-structure.py: cannot locate plugin root. "
        "Set CLAUDE_PLUGIN_ROOT or run from within the plugin tree."
    )


def load_oracle(root: Path) -> dict[str, Any]:
    oracle_path = root / "skills" / "brand-export" / "references" / "artifact-schemas.yaml"
    if not oracle_path.exists():
        raise SystemExit(f"validate-structure.py: oracle not found at {oracle_path}")
    with oracle_path.open() as f:
        return yaml.safe_load(f)


def read_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"validate-structure.py: artifact not found: {path}")
    return path.read_text()


# ─── Checkers ──────────────────────────────────────────────────────────────


def check_required_sections(content: str, schema: dict) -> dict:
    """HTML check: each required `<section id="...">` is present, optionally in order."""
    sections = schema.get("required_sections") or []
    if not sections:
        return {"name": "required_sections", "result": "skip", "detail": "no sections declared"}

    # Accept section-like container tags. The canonical brand-guidelines template uses
    # <header id="cover"> for the cover and <section id=...> for every other block.
    found_ids = re.findall(
        r'<(?:section|header|article|nav|main)[^>]*\bid="([a-z][a-z0-9-]*)"',
        content,
        re.IGNORECASE,
    )
    missing = []
    out_of_order = []
    anatomy_failures = []

    cursor = 0
    enforce_order = schema.get("enforce_order", False)
    for decl in sections:
        sid = decl["id"]
        optional = decl.get("optional", False)
        required_anatomy = decl.get("required_anatomy", [])
        if sid in found_ids:
            if enforce_order:
                idx = found_ids.index(sid, cursor) if sid in found_ids[cursor:] else -1
                if idx == -1:
                    out_of_order.append(sid)
                else:
                    cursor = idx + 1
            # Check anatomy inside section: scan between this section and the next
            if required_anatomy:
                section_block = extract_section_block(content, sid)
                for cls in required_anatomy:
                    if cls not in section_block:
                        anatomy_failures.append({"section": sid, "missing_class": cls})
        else:
            if not optional:
                missing.append(sid)

    invented = [sid for sid in found_ids if sid not in {d["id"] for d in sections}]

    passed = not missing and not out_of_order and not anatomy_failures
    detail = {
        "found": found_ids,
        "missing_required": missing,
        "out_of_order": out_of_order,
        "anatomy_failures": anatomy_failures,
        "invented_sections": invented,
    }
    return {
        "name": "required_sections",
        "result": "pass" if passed else "fail",
        "detail": detail,
    }


def extract_section_block(content: str, section_id: str) -> str:
    """Extract text from this section's opening tag to the next *top-level* sibling.

    A top-level sibling is any <section|header|article|nav|main> tag that also
    carries an `id=` attribute. Nested <section class=...> blocks (e.g. the
    personality subsections) are kept inside the parent block so anatomy
    classes declared inside them are discoverable.
    """
    start = re.search(
        rf'<(?:section|header|article|nav|main)[^>]*\bid="{re.escape(section_id)}"',
        content,
    )
    if not start:
        return ""
    rest = content[start.end():]
    next_id_block = re.search(
        r'<(?:section|header|article|nav|main)[^>]*\bid="[a-z][a-z0-9-]*"',
        rest,
    )
    if next_id_block:
        return rest[: next_id_block.start()]
    return rest


def check_required_headings(content: str, schema: dict) -> dict:
    """Markdown + HTML check: each required heading is present, optionally in order."""
    headings = schema.get("required_headings") or []
    if not headings:
        return {"name": "required_headings", "result": "skip", "detail": "no headings declared"}

    # Capture both Markdown (# heading) and HTML (<h1>...</h1>) headings.
    md_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
    html_pattern = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.DOTALL | re.IGNORECASE)

    found = []
    for match in md_pattern.finditer(content):
        found.append((len(match.group(1)), match.group(2).strip()))
    for match in html_pattern.finditer(content):
        text = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        found.append((int(match.group(1)), text))

    missing = []
    out_of_order = []
    cursor = 0
    enforce_order = schema.get("enforce_order", False)
    for decl in headings:
        text = decl["text"]
        level = decl.get("level")
        substring = decl.get("substring_match", False)
        optional = decl.get("optional", False)

        matched_idx = -1
        for i, (lv, txt) in enumerate(found[cursor:], start=cursor):
            if level is not None and lv != level:
                continue
            if substring and text in txt:
                matched_idx = i
                break
            if not substring and txt == text:
                matched_idx = i
                break

        if matched_idx == -1:
            # Try non-ordered search before giving up
            for i, (lv, txt) in enumerate(found):
                if level is not None and lv != level:
                    continue
                if (substring and text in txt) or (not substring and txt == text):
                    if enforce_order:
                        out_of_order.append(text)
                    matched_idx = i
                    break
            if matched_idx == -1 and not optional:
                missing.append(text)
        else:
            if enforce_order:
                cursor = matched_idx + 1

    passed = not missing and not out_of_order
    return {
        "name": "required_headings",
        "result": "pass" if passed else "fail",
        "detail": {
            "missing": missing,
            "out_of_order": out_of_order,
            "found_count": len(found),
        },
    }


def check_required_variables(content: str, schema: dict) -> dict:
    """CSS check: each required `--variable-name` custom property is declared."""
    variables = schema.get("required_variables") or []
    if not variables:
        return {"name": "required_variables", "result": "skip", "detail": "no variables declared"}
    missing = [v for v in variables if not re.search(re.escape(v) + r"\s*:", content)]
    return {
        "name": "required_variables",
        "result": "pass" if not missing else "fail",
        "detail": {"missing": missing, "checked": len(variables)},
    }


def check_required_keys(content: str, schema: dict, artifact_type: str) -> dict:
    """JSON or YAML check: each required dotted key path is present."""
    keys = schema.get("required_keys") or []
    if not keys:
        return {"name": "required_keys", "result": "skip", "detail": "no keys declared"}

    if artifact_type == "json":
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            return {"name": "required_keys", "result": "fail", "detail": {"parse_error": str(e)}}
    elif artifact_type == "yaml":
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            return {"name": "required_keys", "result": "fail", "detail": {"parse_error": str(e)}}
    else:
        return {
            "name": "required_keys",
            "result": "skip",
            "detail": f"unsupported type: {artifact_type}",
        }

    missing = [k for k in keys if not dotted_lookup(data, k)]
    return {
        "name": "required_keys",
        "result": "pass" if not missing else "fail",
        "detail": {"missing": missing, "checked": len(keys)},
    }


def dotted_lookup(data: Any, path: str) -> bool:
    """Return True iff every segment in a dotted path resolves to a present key."""
    cursor = data
    for segment in path.split("."):
        if not isinstance(cursor, dict) or segment not in cursor:
            return False
        cursor = cursor[segment]
    return True


def check_required_classes(content: str, schema: dict) -> dict:
    """HTML/SVG check: each required CSS class name appears at least once."""
    classes = schema.get("required_classes") or []
    if not classes:
        return {"name": "required_classes", "result": "skip", "detail": "no classes declared"}
    missing = [c for c in classes if not re.search(rf'class="[^"]*\b{re.escape(c)}\b', content)]
    return {
        "name": "required_classes",
        "result": "pass" if not missing else "fail",
        "detail": {"missing": missing, "checked": len(classes)},
    }


def check_required_frontmatter(content: str, schema: dict) -> dict:
    """Markdown check: YAML frontmatter block contains required fields."""
    fields = schema.get("required_frontmatter") or []
    if not fields:
        return {"name": "required_frontmatter", "result": "skip", "detail": "none declared"}
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {
            "name": "required_frontmatter",
            "result": "fail",
            "detail": {"parse_error": "no YAML frontmatter block"},
        }
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        return {"name": "required_frontmatter", "result": "fail", "detail": {"parse_error": str(e)}}
    missing = [f for f in fields if f not in data]
    return {
        "name": "required_frontmatter",
        "result": "pass" if not missing else "fail",
        "detail": {"missing": missing, "checked": len(fields)},
    }


def check_patterns(content: str, schema: dict, key: str, must_match: bool) -> dict:
    """Generic pattern check. `must_match=True` → required; `False` → forbidden."""
    patterns = schema.get(key) or []
    if not patterns:
        return {"name": key, "result": "skip", "detail": "none declared"}
    failures = []
    for p in patterns:
        hit = bool(re.search(p["pattern"], content))
        if must_match and not hit:
            failures.append({"pattern": p["pattern"], "description": p.get("description", "")})
        if not must_match and hit:
            failures.append({"pattern": p["pattern"], "description": p.get("description", "")})
    return {
        "name": key,
        "result": "pass" if not failures else "fail",
        "detail": {"failures": failures, "checked": len(patterns)},
    }


# ─── Dispatch ──────────────────────────────────────────────────────────────


def resolve_schema_key(oracle: dict[str, Any], requested: str) -> str | None:
    """Resolve a requested schema arg to an oracle key. Honors `arg_aliases: [...]`."""
    if requested in oracle:
        return requested
    for key, entry in oracle.items():
        if isinstance(entry, dict) and requested in (entry.get("arg_aliases") or []):
            return key
    return None


def format_alias_index(oracle: dict[str, Any]) -> str:
    pairs = []
    for key, entry in sorted(oracle.items()):
        aliases = entry.get("arg_aliases") if isinstance(entry, dict) else None
        if aliases:
            pairs.append(f"{','.join(aliases)}→{key}")
    return "; ".join(pairs) if pairs else "(none)"


def validate(artifact_path: Path, schema: dict) -> dict:
    content = read_file(artifact_path)
    artifact_type = schema.get("type", "unknown")
    checks = []

    if artifact_type == "html":
        checks.append(check_required_sections(content, schema))
        checks.append(check_required_headings(content, schema))
        checks.append(check_required_classes(content, schema))
        if schema.get("required_patterns"):
            checks.append(check_patterns(content, schema, "required_patterns", must_match=True))
        if schema.get("forbidden_patterns"):
            checks.append(check_patterns(content, schema, "forbidden_patterns", must_match=False))
    elif artifact_type == "md":
        checks.append(check_required_headings(content, schema))
        checks.append(check_required_frontmatter(content, schema))
        if schema.get("required_patterns"):
            checks.append(check_patterns(content, schema, "required_patterns", must_match=True))
        if schema.get("forbidden_patterns"):
            checks.append(check_patterns(content, schema, "forbidden_patterns", must_match=False))
    elif artifact_type == "css":
        checks.append(check_required_variables(content, schema))
    elif artifact_type == "json":
        checks.append(check_required_keys(content, schema, "json"))
    elif artifact_type == "yaml":
        checks.append(check_required_keys(content, schema, "yaml"))
    elif artifact_type == "svg":
        checks.append(check_required_classes(content, schema))
        if schema.get("required_patterns"):
            checks.append(check_patterns(content, schema, "required_patterns", must_match=True))
        if schema.get("forbidden_patterns"):
            checks.append(check_patterns(content, schema, "forbidden_patterns", must_match=False))
    else:
        checks.append({"name": "type_dispatch", "result": "fail", "detail": f"unknown type: {artifact_type}"})

    checks = [c for c in checks if c.get("result") != "skip"]
    passed = all(c["result"] == "pass" for c in checks)

    return {
        "artifact": str(artifact_path),
        "schema": schema.get("__key", ""),
        "type": artifact_type,
        "passed": passed,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Structural validator for brand artifacts.")
    parser.add_argument("--artifact", required=True, help="Path to the rendered artifact file.")
    parser.add_argument("--schema", required=True, help="Oracle key (e.g. brand-guidelines).")
    parser.add_argument(
        "--oracle",
        default=None,
        help="Optional override path to artifact-schemas.yaml.",
    )
    args = parser.parse_args()

    artifact_path = Path(args.artifact)

    if args.oracle:
        oracle_path = Path(args.oracle)
        with oracle_path.open() as f:
            oracle = yaml.safe_load(f)
    else:
        oracle = load_oracle(find_plugin_root())

    resolved_key = resolve_schema_key(oracle, args.schema)
    if resolved_key is None:
        sys.stderr.write(
            f"validate-structure.py: no oracle entry for key or alias '{args.schema}'.\n"
            f"  Known keys: {', '.join(sorted(oracle.keys()))}\n"
            f"  Known aliases: {format_alias_index(oracle)}\n"
        )
        return 2

    schema = oracle[resolved_key]
    schema["__key"] = resolved_key

    verdict = validate(artifact_path, schema)
    json.dump(verdict, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if verdict["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
