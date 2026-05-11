"""Unit tests for lib.look_loader.

Run with: cd plugins/expert-design-n-brand && python3 -m pytest scripts/test_look_loader.py -v
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from lib.look_loader import (
    load_tokens,
    flatten_dtcg,
    resolve_references,
    coerce_legacy_paths,
    build_look,
)


@pytest.fixture
def canonical_tokens() -> dict:
    return {
        "primitive": {
            "color": {
                "palette": {
                    "primary": {"$value": "#3B82F6", "$type": "color"},
                    "neutral": {"$value": "#0B1220", "$type": "color"},
                },
                "scales": {
                    "brand": {
                        "500": {"$value": "#2563EB", "$type": "color"},
                        "600": {"$value": "#1D4ED8", "$type": "color"},
                    },
                    "neutral": {
                        "50":  {"$value": "#F8FAFC", "$type": "color"},
                        "900": {"$value": "#0B1220", "$type": "color"},
                    },
                },
            },
            "typography": {
                "fontFamily": {
                    "heading": {"$value": ["Inter"], "$type": "fontFamily"},
                    "body":    {"$value": ["Inter"], "$type": "fontFamily"},
                },
                "fontSize": {"body": {"$value": "1rem", "$type": "dimension"}},
            },
            "space": {"4": {"$value": "1rem", "$type": "dimension"}},
        },
        "semantic": {
            "light": {
                "color": {
                    "text-primary": {"$value": "{primitive.color.scales.neutral.900}", "$type": "color"},
                    "link":         {"$value": "{primitive.color.scales.brand.600}",   "$type": "color"},
                }
            },
            "dark": {
                "color": {
                    "text-primary": {"$value": "{primitive.color.scales.neutral.50}",  "$type": "color"},
                }
            },
            "status": {
                "success": {"$value": "#16A34A", "$type": "color"},
            },
        },
    }


def test_flatten_dtcg_strips_metadata(canonical_tokens):
    flat = flatten_dtcg(canonical_tokens)
    assert flat["primitive"]["color"]["palette"]["primary"] == "#3B82F6"
    assert flat["primitive"]["typography"]["fontFamily"]["heading"] == ["Inter"]
    assert flat["semantic"]["status"]["success"] == "#16A34A"


def test_resolve_references_replaces_pointers(canonical_tokens):
    flat = flatten_dtcg(canonical_tokens)
    resolved = resolve_references(flat)
    assert resolved["semantic"]["light"]["color"]["text-primary"] == "#0B1220"
    assert resolved["semantic"]["light"]["color"]["link"] == "#1D4ED8"


def test_coerce_legacy_typography_family():
    legacy = {
        "primitive": {
            "typography": {
                "family": {"heading": ["Inter"], "body": ["Inter"]}
            }
        }
    }
    coerced = coerce_legacy_paths(legacy)
    assert coerced["primitive"]["typography"]["fontFamily"]["heading"] == ["Inter"]


def test_coerce_legacy_spacing_to_space():
    legacy = {"primitive": {"spacing": {"4": "1rem"}}}
    coerced = coerce_legacy_paths(legacy)
    assert coerced["primitive"]["space"]["4"] == "1rem"


def test_coerce_legacy_breakpoints_plural_to_singular():
    legacy = {"primitive": {"breakpoints": {"md": "768px"}}}
    coerced = coerce_legacy_paths(legacy)
    assert coerced["primitive"]["breakpoint"]["md"] == "768px"


def test_coerce_legacy_motion_top_level():
    legacy = {"motion": {"easing": {"standard": "ease-out"}}}
    coerced = coerce_legacy_paths(legacy)
    assert coerced["primitive"]["motion"]["easing"]["standard"] == "ease-out"


def test_coerce_legacy_nested_categorical_text(canonical_tokens):
    legacy = {
        "semantic": {
            "light": {
                "color": {
                    "text": {"primary": "#000"}
                }
            }
        }
    }
    coerced = coerce_legacy_paths(legacy)
    assert coerced["semantic"]["light"]["color"]["text-primary"] == "#000"


def test_build_look_end_to_end(canonical_tokens):
    look = build_look(canonical_tokens, brand_name="Test Brand", brand_tagline="A tagline")
    assert look["look_schema_version"] == "0.1.0"
    assert look["name"] == "Test Brand"
    assert look["tokens"]["primitive"]["color"]["palette"]["primary"] == "#3B82F6"
    # Reference-resolved at the semantic layer:
    assert look["tokens"]["semantic"]["light"]["color"]["text-primary"] == "#0B1220"
    # Surface controls populated with sensible defaults:
    assert look["surface_controls"]["mode"] == "light"
    assert look["surface_controls"]["density"] in ("compact", "comfortable", "spacious")


# ─── Role compatibility ───────────────────────────────────────────────────────

def test_resolve_canonical_roles_first_match_wins():
    from lib.look_loader import resolve_canonical_roles
    # A brand that uses `action-primary` instead of canonical `primary`
    src = {"action-primary": "#3B82F6", "text-muted": "#6B7280"}
    out = resolve_canonical_roles(src)
    # Original keys preserved
    assert out["action-primary"] == "#3B82F6"
    assert out["text-muted"] == "#6B7280"
    # Canonical aliases written
    assert out["primary"] == "#3B82F6"
    assert out["text-secondary"] == "#6B7280"


def test_resolve_canonical_roles_canonical_wins_over_candidate():
    from lib.look_loader import resolve_canonical_roles
    # Both canonical and candidate present — canonical preserved unchanged
    src = {"primary": "#000", "action-primary": "#FFF"}
    out = resolve_canonical_roles(src)
    assert out["primary"] == "#000"
    assert out["action-primary"] == "#FFF"


def test_resolve_status_compat_ben_status_danger():
    from lib.look_loader import resolve_status_compat
    # Ben's brand uses `status-danger` for error
    semantic_light = {"status-danger": "#DC2626"}
    status_block = {}
    out = resolve_status_compat(status_block, semantic_light)
    assert out["error"] == "#DC2626"


def test_resolve_status_compat_explicit_status_wins():
    from lib.look_loader import resolve_status_compat
    semantic_light = {"status-danger": "#000"}
    status_block = {"error": "#DC2626"}
    out = resolve_status_compat(status_block, semantic_light)
    assert out["error"] == "#DC2626"  # explicit wins


# ─── Dark derivation ──────────────────────────────────────────────────────────

def test_derive_dark_swaps_page_ground_and_text():
    from lib.look_loader import derive_dark_colors_from_source
    light = {
        "background": "#FFFFFF",
        "inverse": "#0B1220",
        "text-primary": "#0B1220",
        "text-inverse": "#FFFFFF",
        "primary": "#3B82F6",  # untouched
    }
    dark = derive_dark_colors_from_source(light)
    assert dark["background"] == "#0B1220"  # was light.inverse
    assert dark["inverse"] == "#FFFFFF"     # was light.background
    assert dark["text-primary"] == "#FFFFFF"
    assert dark["text-inverse"] == "#0B1220"
    assert dark["primary"] == "#3B82F6"     # passes through


def test_derive_dark_via_observed_candidates():
    """When the brand uses observed-candidate names (bg-default, bg-inverse), derivation still works."""
    from lib.look_loader import derive_dark_colors_from_source
    light = {
        "bg-default": "#FFFFFF",
        "bg-inverse": "#0B1220",
        "text": "#0B1220",
        "text-on-inverse": "#FFFFFF",
    }
    dark = derive_dark_colors_from_source(light)
    # Canonical keys written so downstream emit_css_vars finds them
    assert dark["background"] == "#0B1220"
    assert dark["inverse"] == "#FFFFFF"
    assert dark["text-primary"] == "#FFFFFF"
    assert dark["text-inverse"] == "#0B1220"


# ─── End-to-end via build_look ────────────────────────────────────────────────

def test_build_look_auto_derives_dark_when_missing():
    from lib.look_loader import build_look
    raw = {
        "primitive": {"color": {"palette": {}, "scales": {}}, "typography": {"fontFamily": {}, "fontSize": {}}, "space": {}},
        "semantic": {
            "light": {"color": {
                "background": "#FFFFFF", "inverse": "#0B1220",
                "text-primary": "#0B1220", "text-inverse": "#FFFFFF",
            }},
            # NO dark block
        },
    }
    look = build_look(raw, brand_name="Auto-Dark Brand")
    dark = look["tokens"]["semantic"]["dark"]["color"]
    assert dark["background"] == "#0B1220"
    assert dark["text-primary"] == "#FFFFFF"


def test_build_look_preserves_authored_dark_when_present():
    from lib.look_loader import build_look
    raw = {
        "primitive": {"color": {"palette": {}, "scales": {}}, "typography": {"fontFamily": {}, "fontSize": {}}, "space": {}},
        "semantic": {
            "light": {"color": {"background": "#FFFFFF", "text-primary": "#000"}},
            "dark":  {"color": {"background": "#111", "text-primary": "#EEE"}},
        },
    }
    look = build_look(raw)
    dark = look["tokens"]["semantic"]["dark"]["color"]
    assert dark["background"] == "#111"  # authored value preserved
    assert dark["text-primary"] == "#EEE"


def test_build_look_resolves_status_danger_to_error():
    """End-to-end: a brand like Ben's that uses `status-danger` should produce a canonical `error` in semantic.status."""
    from lib.look_loader import build_look
    raw = {
        "primitive": {"color": {"palette": {}, "scales": {}}, "typography": {"fontFamily": {}, "fontSize": {}}, "space": {}},
        "semantic": {
            "light": {"color": {
                "background": "#FFF", "text-primary": "#000",
                "status-success": "#16A34A",
                "status-warning": "#D97706",
                "status-danger":  "#DC2626",
                "status-info":    "#0EA5E9",
            }},
        },
    }
    look = build_look(raw)
    status = look["tokens"]["semantic"]["status"]
    assert status["success"] == "#16A34A"
    assert status["warning"] == "#D97706"
    assert status["error"]   == "#DC2626"  # ← the gap this task closes
    assert status["info"]    == "#0EA5E9"
