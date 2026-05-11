"""look_loader — load + normalize a brand bundle into a `Look` dict.

Used by:
- scripts/render-playground.py  (this plan)
- scripts/render-look.py        (Plan A — when present)

The Look shape is the bake-time data representation the playground HTML
consumes via embedded JSON. It mirrors `assets/tokens-template.json`
structurally but: (a) DTCG metadata stripped, (b) `{a.b.c}` references
resolved to concrete values, (c) common legacy paths coerced to canonical.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

LOOK_SCHEMA_VERSION = "0.1.0"
REFERENCE_PATTERN = re.compile(r"^\{([^}]+)\}$")


def load_tokens(path: Path) -> dict[str, Any]:
    """Load tokens.json from disk. Raises FileNotFoundError with a clear hint."""
    if not path.exists():
        raise FileNotFoundError(
            f"tokens.json not found at {path}. Run `/brand-export core` to generate it."
        )
    return json.loads(path.read_text())


def flatten_dtcg(node: Any) -> Any:
    """Strip DTCG metadata recursively. A DTCG leaf is a dict with `$value`.

    Drops `$type`, `$description`, `$schema`, `$meta`, `$note`, `__note`,
    `__comment`. For dicts that have `$value`, returns the value. For
    dicts without `$value`, recurses into children. For non-dicts, returns
    as-is.
    """
    META_KEYS = {"$type", "$description", "$schema", "$meta", "$note", "__note", "__comment"}
    if isinstance(node, dict):
        if "$value" in node:
            return node["$value"]
        return {
            k: flatten_dtcg(v)
            for k, v in node.items()
            if k not in META_KEYS
        }
    if isinstance(node, list):
        return [flatten_dtcg(item) for item in node]
    return node


def _walk_path(root: dict, dotted: str) -> Any:
    """Walk a dotted path like `primitive.color.scales.brand.500`. Return None if missing."""
    cur = root
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def resolve_references(root: dict, max_depth: int = 8) -> dict:
    """Replace string values matching `{a.b.c}` with the targeted concrete value.

    Works iteratively until no references remain or `max_depth` is exceeded.
    Unresolvable references are left in place (renderer logs WARN).
    """
    out = deepcopy(root)

    def step(node: Any) -> Any:
        if isinstance(node, dict):
            return {k: step(v) for k, v in node.items()}
        if isinstance(node, list):
            return [step(item) for item in node]
        if isinstance(node, str):
            m = REFERENCE_PATTERN.match(node.strip())
            if m:
                target = _walk_path(out, m.group(1))
                if target is not None and not (
                    isinstance(target, str) and REFERENCE_PATTERN.match(target.strip())
                ):
                    return target
        return node

    for _ in range(max_depth):
        next_out = step(out)
        if next_out == out:
            break
        out = next_out
    return out


# ─── Legacy-path coercion ──────────────────────────────────────────────────────

def coerce_legacy_paths(root: dict) -> dict:
    """Mutate-and-return: rewrite known legacy shapes into canonical positions.

    Documented legacy patterns we accept (from `playground-look-mapping.md` and
    real brand exports, primarily Ben's and Brennan's earlier exports):

    - `primitive.typography.family.{role}` → `primitive.typography.fontFamily.{role}`
    - `primitive.typography.weight.{label}` → `primitive.typography.fontWeight.{label}`
    - `primitive.font.{role}` → `primitive.typography.fontFamily.{role}` (top-level `font`)
    - `primitive.spacing.{step}` → `primitive.space.{step}`
    - `primitive.breakpoints.{label}` → `primitive.breakpoint.{label}`
    - `motion.*` (top-level) → `primitive.motion.*`
    - `semantic.{mode}.color.text.{role}` (nested-categorical) → `semantic.{mode}.color.text-{role}` (flat-hyphenated)
    - same for `border.{name}` → `border-{name}` and `link.{state}` → `link-{state}`

    Idempotent: re-running on already-canonical shapes is a no-op.
    """
    out = deepcopy(root)

    prim = out.setdefault("primitive", {})
    typ = prim.setdefault("typography", {})

    # typography.family → fontFamily
    if "family" in typ and "fontFamily" not in typ:
        typ["fontFamily"] = typ.pop("family")
    # typography.weight → fontWeight
    if "weight" in typ and "fontWeight" not in typ:
        typ["fontWeight"] = typ.pop("weight")
    # primitive.font → primitive.typography.fontFamily (rare — Brennan's earlier export)
    if "font" in prim and "fontFamily" not in typ:
        typ["fontFamily"] = prim.pop("font")

    # primitive.spacing → primitive.space
    if "spacing" in prim and "space" not in prim:
        prim["space"] = prim.pop("spacing")

    # primitive.breakpoints → primitive.breakpoint
    if "breakpoints" in prim and "breakpoint" not in prim:
        prim["breakpoint"] = prim.pop("breakpoints")

    # top-level motion → primitive.motion
    if "motion" in out and "motion" not in prim:
        prim["motion"] = out.pop("motion")

    # nested-categorical → flat-hyphenated under semantic.{mode}.color
    # Real brand exports (e.g. Ben's) nest by category: text.primary, bg.default,
    # status.danger, action.primary, surface.elevated, border.default. After
    # coercion these all become flat hyphenated keys (text-primary, bg-default,
    # etc.) so ROLE_COMPAT and STATUS_COMPAT can find them.
    NESTED_CATEGORIES = ("text", "border", "link", "bg", "action", "status", "surface")
    sem = out.setdefault("semantic", {})
    for mode in ("light", "dark"):
        mode_block = sem.get(mode, {})
        if not isinstance(mode_block, dict):
            continue
        color_block = mode_block.setdefault("color", {})
        for cat in NESTED_CATEGORIES:
            nested = color_block.get(cat)
            if isinstance(nested, dict):
                for sub_role, sub_value in nested.items():
                    flat_key = f"{cat}-{sub_role}"
                    color_block.setdefault(flat_key, sub_value)
                del color_block[cat]

    return out


# ─── Role compatibility (mirrors catalyne-design-playground/src/lib/lookToCss.ts) ─

ROLE_COMPAT: dict[str, list[str]] = {
    "primary":         ["primary", "action-primary", "color-primary"],
    "accent":          ["accent", "action-accent"],
    "secondary":       ["secondary", "color-secondary", "brand-authority"],
    "text-primary":    ["text-primary", "text"],
    "text-secondary":  ["text-secondary", "text-muted"],
    "text-tertiary":   ["text-tertiary", "text-subtle"],
    "text-inverse":    ["text-inverse", "text-on-inverse"],
    "background":      ["background", "bg-default", "bg"],
    "surface":         ["surface", "bg-elevated", "surface-default"],
    "muted":           ["muted", "bg-subtle"],
    "inverse":         ["inverse", "surface-dark", "bg-inverse"],
    "border":          ["border", "border-default"],
    "border-strong":   ["border-strong"],
    "link":            ["link", "text-link"],
    "border-focus":    ["border-focus", "focus-ring"],
}

# Brands export `error` under different names — Ben uses `status-danger`.
# Each canonical key maps to the brand-authored candidate keys we'll search.
STATUS_COMPAT: dict[str, list[str]] = {
    "success": ["success", "status-success", "status-affirm"],
    "warning": ["warning", "status-warning", "status-warn"],
    "error":   ["error", "status-error", "status-danger"],
    "info":    ["info", "status-info"],
}


def resolve_canonical_roles(source: dict[str, Any]) -> dict[str, Any]:
    """First-match aliasing for semantic color roles.

    Preserves the original brand-authored keys (so downstream code that uses
    them keeps working) AND writes the canonical key alongside when missing.
    Idempotent: if both canonical and candidate are present, canonical wins
    and is preserved unchanged.

    Mirrors `resolveCanonicalRoles` in lookToCss.ts:39-54.
    """
    out: dict[str, Any] = dict(source)
    for canonical, candidates in ROLE_COMPAT.items():
        if canonical in out:
            continue
        for candidate in candidates:
            if candidate in source:
                out[canonical] = source[candidate]
                break
    return out


def resolve_status_compat(
    status_block: dict[str, Any],
    semantic_light_color: dict[str, Any],
) -> dict[str, Any]:
    """Populate canonical status keys (success/warning/error/info) by first-match.

    Search order per canonical key: explicit `semantic.status.{key}` (preserved)
    → `semantic.light.color.{candidate}` for each candidate in STATUS_COMPAT.

    The `error` ↔ `status-danger` mapping is the one Ben's brand needs.
    """
    out: dict[str, Any] = dict(status_block)
    for canonical, candidates in STATUS_COMPAT.items():
        if canonical in out:
            continue
        for candidate in candidates:
            if candidate in semantic_light_color:
                out[canonical] = semantic_light_color[candidate]
                break
    return out


def derive_dark_colors_from_source(source: dict[str, Any]) -> dict[str, Any]:
    """Best-effort light → dark color derivation for brands without a dark block.

    Rules (mirror deriveDarkColors.ts):
      - Page ground swap: dark.background = light.inverse, dark.inverse = light.background.
        Both canonical and observed-candidate keys (bg-default, bg-inverse) are
        written so emit_css_vars + the JS engine find a value regardless of which
        name the brand used.
      - Text swap: dark.text-primary = light.text-inverse, dark.text-inverse = light.text-primary.
      - All unmapped keys pass through untouched.
    """
    def pick(canonical: str) -> Any:
        for cand in ROLE_COMPAT.get(canonical, []):
            if cand in source:
                return source[cand]
        return source.get(canonical)

    def write(target: dict[str, Any], canonical: str, value: Any) -> None:
        if value is None:
            return
        target[canonical] = value
        for cand in ROLE_COMPAT.get(canonical, []):
            if cand in source:
                target[cand] = value

    out: dict[str, Any] = dict(source)
    background = pick("inverse")
    inverse = pick("background")
    if background is not None:
        write(out, "background", background)
    if inverse is not None:
        write(out, "inverse", inverse)
    text_primary = pick("text-inverse")
    text_inverse = pick("text-primary")
    if text_primary is not None:
        write(out, "text-primary", text_primary)
    if text_inverse is not None:
        write(out, "text-inverse", text_inverse)
    return out


# ─── Look assembly ─────────────────────────────────────────────────────────────

def _density_default(space_scale: dict[str, Any]) -> str:
    """Infer a sensible density default from the brand's base space step."""
    base = space_scale.get("4")
    if base is None:
        return "comfortable"
    if isinstance(base, str) and base.endswith("rem"):
        try:
            n = float(base[:-3])
            if n < 0.875:
                return "compact"
            if n > 1.125:
                return "spacious"
            return "comfortable"
        except ValueError:
            return "comfortable"
    return "comfortable"


def build_look(
    tokens_raw: dict,
    *,
    brand_name: str = "Design Playground",
    brand_tagline: str = "Open in any modern browser",
    extensions_raw: dict | None = None,
    surface_translations_raw: dict | None = None,
) -> dict:
    """End-to-end transform: tokens.json (DTCG) → Look dict ready to embed.

    Pipeline: legacy-coerce → DTCG-flatten → reference-resolve → role-resolve
    → dark-derive → assemble.

    Output keys mirror the contract in `playground-look-mapping.md`. The
    semantic.{light,dark}.color blocks always carry canonical role keys
    (primary, text-primary, background, etc.) AND the brand's original keys.
    semantic.status always carries success/warning/error/info, resolved from
    explicit status block or from `status-{name}` candidates in semantic.light.
    """
    coerced = coerce_legacy_paths(tokens_raw)
    flat = flatten_dtcg(coerced)
    resolved = resolve_references(flat)

    primitive = resolved.get("primitive", {})
    semantic  = resolved.get("semantic", {}) or {}
    component = resolved.get("component", {})
    extensions = resolved.get("extensions", {})

    # ── Role-resolve the semantic light + dark blocks ────────────────────────
    light_color = (semantic.get("light") or {}).get("color") or {}
    light_resolved = resolve_canonical_roles(light_color)

    dark_block = semantic.get("dark") or {}
    dark_color = dark_block.get("color") or {}
    if dark_color:
        dark_resolved = resolve_canonical_roles(dark_color)
    else:
        # Auto-derive dark from light when brand didn't author one
        dark_resolved = resolve_canonical_roles(derive_dark_colors_from_source(light_resolved))

    # ── Status compat: canonical success/warning/error/info ──────────────────
    status_block = semantic.get("status") or {}
    if not isinstance(status_block, dict):
        status_block = {}
    # Status entries may be either flat strings or nested {value, foreground, ...} dicts.
    # We pass through dicts and resolve flat strings via STATUS_COMPAT.
    flat_status = {k: v for k, v in status_block.items() if isinstance(v, (str, int, float))}
    nested_status = {k: v for k, v in status_block.items() if isinstance(v, dict)}
    status_resolved = {**resolve_status_compat(flat_status, light_resolved), **nested_status}

    # ── Reassemble semantic block with the resolved sub-blocks ───────────────
    semantic_out = dict(semantic)
    semantic_out["light"] = {**(semantic.get("light") or {}), "color": light_resolved}
    semantic_out["dark"]  = {**dark_block, "color": dark_resolved}
    semantic_out["status"] = status_resolved

    # ── Merge brand-extensions (vocabulary, voice, visual_language) ──────────
    if extensions_raw:
        ext_flat = flatten_dtcg(coerce_legacy_paths(extensions_raw))
        extensions = {**extensions, "brand_namespace": ext_flat}

    # ── Platform matrix from surface-translations.yaml ───────────────────────
    platform_matrix: dict[str, list] = {"surfaces": []}
    if surface_translations_raw:
        for surface in surface_translations_raw.get("surfaces", []):
            platform_matrix["surfaces"].append({
                "id": surface.get("id"),
                "category": surface.get("category"),
                "column_label": surface.get("column_label"),
                "fallback_chain": surface.get("typography_fallback") or surface.get("fonts", {}).get("fallback") or [],
            })

    space_scale = primitive.get("space", {})

    return {
        "look_schema_version": LOOK_SCHEMA_VERSION,
        "name": brand_name,
        "description": brand_tagline,
        "tokens": {
            "primitive": primitive,
            "semantic": semantic_out,
            "component": component,
            "extensions": extensions,
        },
        "platform_matrix": platform_matrix,
        "surface_controls": {
            "density": _density_default(space_scale),
            "scale_ratio": primitive.get("typography", {}).get("scale", {}).get("ratio", 1.250),
            "shadow_intensity": "default",
            "radius_card": primitive.get("radius", {}).get("card") or primitive.get("radius", {}).get("lg", "0.75rem"),
            "radius_interactive": primitive.get("radius", {}).get("interactive") or primitive.get("radius", {}).get("md", "0.5rem"),
            "mode": "light",
        },
    }
