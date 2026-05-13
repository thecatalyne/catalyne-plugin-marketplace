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
    normalize_input_paths,
    resolve_canonical_roles,
    resolve_status_compat,
    derive_dark_colors_from_source,
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


# ─── Input path normalization ─────────────────────────────────────────────────

def test_normalize_typography_family_to_fontFamily():
    raw = {
        "primitive": {
            "typography": {
                "family": {"heading": ["Inter"], "body": ["Inter"]}
            }
        }
    }
    out = normalize_input_paths(raw)
    assert out["primitive"]["typography"]["fontFamily"]["heading"] == ["Inter"]


def test_normalize_spacing_to_space():
    raw = {"primitive": {"spacing": {"4": "1rem"}}}
    out = normalize_input_paths(raw)
    assert out["primitive"]["space"]["4"] == "1rem"


def test_normalize_breakpoints_plural_to_singular():
    raw = {"primitive": {"breakpoints": {"md": "768px"}}}
    out = normalize_input_paths(raw)
    assert out["primitive"]["breakpoint"]["md"] == "768px"


def test_normalize_top_level_motion_to_primitive_motion():
    raw = {"motion": {"easing": {"standard": "ease-out"}}}
    out = normalize_input_paths(raw)
    assert out["primitive"]["motion"]["easing"]["standard"] == "ease-out"


def test_normalize_nested_categorical_text():
    raw = {
        "semantic": {
            "light": {
                "color": {
                    "text": {"primary": "#000"}
                }
            }
        }
    }
    out = normalize_input_paths(raw)
    assert out["semantic"]["light"]["color"]["text-primary"] == "#000"


def test_normalize_dtcg_leaf_at_role_key_not_treated_as_nested(canonical_tokens):
    """A canonical DTCG-wrapped value at a role-key overlapping with a
    category name (`link: {$value, $type}`) must NOT be rewritten as a
    nested categorical. Without this guard, the role gets rewritten into
    `link-$value` garbage and `link` is deleted.
    """
    out = normalize_input_paths(canonical_tokens)
    light = out["semantic"]["light"]["color"]
    assert "link" in light
    assert isinstance(light["link"], dict)
    assert "$value" in light["link"]
    assert "link-$value" not in light


def test_build_look_end_to_end(canonical_tokens):
    look = build_look(canonical_tokens, brand_name="Test Brand", brand_tagline="A tagline")
    assert look["look_schema_version"] == "0.1.0"
    assert look["name"] == "Test Brand"
    assert look["tokens"]["primitive"]["color"]["palette"]["primary"] == "#3B82F6"
    assert look["tokens"]["semantic"]["light"]["color"]["text-primary"] == "#0B1220"
    assert look["surface_controls"]["mode"] == "light"
    assert look["surface_controls"]["density"] in ("compact", "comfortable", "spacious")


# ─── Role / status aliasing ──────────────────────────────────────────────────

def test_resolve_canonical_roles_first_match_wins():
    src = {"action-primary": "#3B82F6", "text-muted": "#6B7280"}
    out = resolve_canonical_roles(src)
    assert out["action-primary"] == "#3B82F6"
    assert out["text-muted"] == "#6B7280"
    assert out["primary"] == "#3B82F6"
    assert out["text-secondary"] == "#6B7280"


def test_resolve_canonical_roles_canonical_wins_over_alias():
    src = {"primary": "#000", "action-primary": "#FFF"}
    out = resolve_canonical_roles(src)
    assert out["primary"] == "#000"
    assert out["action-primary"] == "#FFF"


def test_resolve_status_compat_status_danger_alias():
    semantic_light = {"status-danger": "#DC2626"}
    out = resolve_status_compat({}, semantic_light)
    assert out["error"] == "#DC2626"


def test_resolve_status_compat_explicit_status_wins():
    semantic_light = {"status-danger": "#000"}
    out = resolve_status_compat({"error": "#DC2626"}, semantic_light)
    assert out["error"] == "#DC2626"


# ─── Dark derivation ─────────────────────────────────────────────────────────

def test_derive_dark_swaps_page_ground_and_text():
    light = {
        "background": "#FFFFFF",
        "inverse": "#0B1220",
        "text-primary": "#0B1220",
        "text-inverse": "#FFFFFF",
        "primary": "#3B82F6",
    }
    dark = derive_dark_colors_from_source(light)
    assert dark["background"] == "#0B1220"
    assert dark["inverse"] == "#FFFFFF"
    assert dark["text-primary"] == "#FFFFFF"
    assert dark["text-inverse"] == "#0B1220"
    assert dark["primary"] == "#3B82F6"


def test_derive_dark_via_observed_aliases():
    light = {
        "bg-default": "#FFFFFF",
        "bg-inverse": "#0B1220",
        "text": "#0B1220",
        "text-on-inverse": "#FFFFFF",
    }
    dark = derive_dark_colors_from_source(light)
    assert dark["background"] == "#0B1220"
    assert dark["inverse"] == "#FFFFFF"
    assert dark["text-primary"] == "#FFFFFF"
    assert dark["text-inverse"] == "#0B1220"


# ─── End-to-end via build_look ───────────────────────────────────────────────

def test_build_look_auto_derives_dark_when_missing(capsys):
    raw = {
        "primitive": {"color": {"palette": {}, "scales": {}}, "typography": {"fontFamily": {}, "fontSize": {}}, "space": {}},
        "semantic": {
            "light": {"color": {
                "background": "#FFFFFF", "inverse": "#0B1220",
                "text-primary": "#0B1220", "text-inverse": "#FFFFFF",
            }},
        },
    }
    look = build_look(raw, brand_name="Auto-Dark Brand")
    dark = look["tokens"]["semantic"]["dark"]["color"]
    assert dark["background"] == "#0B1220"
    assert dark["text-primary"] == "#FFFFFF"
    captured = capsys.readouterr()
    assert "dark-mode color block missing" in captured.err


def test_build_look_preserves_authored_dark_when_present(capsys):
    raw = {
        "primitive": {"color": {"palette": {}, "scales": {}}, "typography": {"fontFamily": {}, "fontSize": {}}, "space": {}},
        "semantic": {
            "light": {"color": {"background": "#FFFFFF", "text-primary": "#000"}},
            "dark":  {"color": {"background": "#111", "text-primary": "#EEE"}},
        },
    }
    look = build_look(raw)
    dark = look["tokens"]["semantic"]["dark"]["color"]
    assert dark["background"] == "#111"
    assert dark["text-primary"] == "#EEE"
    # No fallback notice when dark is authored
    captured = capsys.readouterr()
    assert "dark-mode color block missing" not in captured.err


def test_build_look_resolves_status_alias_to_error():
    """A brand that uses `status-danger` produces a canonical `error` in semantic.status."""
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
    assert status["error"]   == "#DC2626"
    assert status["info"]    == "#0EA5E9"
