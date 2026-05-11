"""Smoke + structural tests for render-playground.py.

Run with: cd plugins/expert-design-n-brand && python3 -m pytest scripts/test_render_playground.py -v
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "render-playground.py"
TEMPLATE = PLUGIN_ROOT / "assets" / "playground-template.html"
BEN_FIXTURE = Path("/Users/breakfast/Desktop/Catalyne/Brand Exercize/ben/brand-assets")


def _run(brand_dir: Path, out_path: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--brand-dir", str(brand_dir), "--out", str(out_path), *extra],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def rendered_html(tmp_path: Path) -> str:
    """Render against the Ben fixture into a temp file, return the HTML."""
    if not BEN_FIXTURE.exists():
        pytest.skip(f"Fixture not found: {BEN_FIXTURE}")
    if not (BEN_FIXTURE / "tokens.json").exists():
        pytest.skip("Ben fixture missing tokens.json")
    out = tmp_path / "playground.html"
    result = _run(BEN_FIXTURE, out)
    assert result.returncode == 0, f"renderer failed: {result.stderr}"
    assert out.exists()
    return out.read_text()


def test_smoke_renders_without_errors(rendered_html: str) -> None:
    assert "<title>" in rendered_html
    assert "</html>" in rendered_html


def test_no_unfilled_placeholders(rendered_html: str) -> None:
    """No `{{ANYTHING}}` should remain after render."""
    leftovers = re.findall(r"\{\{[A-Z_]+\}\}", rendered_html)
    assert not leftovers, f"unfilled placeholders: {leftovers[:5]}"


def test_contains_all_four_surfaces(rendered_html: str) -> None:
    for surface in ("marketing", "app", "slide", "glossary"):
        assert f'data-surface="{surface}"' in rendered_html, f"missing surface: {surface}"


def test_contains_all_four_control_tabs(rendered_html: str) -> None:
    for tab in ("colors", "type", "form", "mode"):
        assert f'data-tab="{tab}"' in rendered_html, f"missing control tab: {tab}"


def test_compare_mode_scope_blocks_present(rendered_html: str) -> None:
    assert '<style id="look-root">' in rendered_html
    assert '<style id="look-a">'    in rendered_html
    assert '<style id="look-b">'    in rendered_html


def test_presets_data_block_present(rendered_html: str) -> None:
    """The baked-in presets are embedded as JSON in a script block."""
    assert 'id="presets-data"' in rendered_html
    m = re.search(r'<script type="application/json" id="presets-data">(.*?)</script>', rendered_html, re.S)
    assert m, "presets-data block missing or malformed"
    presets = json.loads(m.group(1))
    assert isinstance(presets, list)


def test_brand_data_block_present_and_valid_json(rendered_html: str) -> None:
    """The brand's Look is embedded as JSON for runtime use."""
    m = re.search(r'<script type="application/json" id="look-data">(.*?)</script>', rendered_html, re.S)
    assert m, "look-data block missing"
    look = json.loads(m.group(1))
    assert look["look_schema_version"] == "0.1.0"
    assert "tokens" in look


def test_yaml_paste_fallback_present(rendered_html: str) -> None:
    """The engine references window.jsyaml so YAML paste falls back gracefully."""
    assert "window.jsyaml" in rendered_html


def test_js_yaml_bundle_inlined(rendered_html: str) -> None:
    """The js-yaml UMD shim is present (or the missing-vendor stub)."""
    has_bundle = "jsyaml" in rendered_html and "function" in rendered_html
    has_stub   = "js-yaml vendor missing" in rendered_html
    assert has_bundle or has_stub


def test_compare_mode_scoping_css_present(rendered_html: str) -> None:
    """The compare-mode CSS rules that split-grid the active surface must be present."""
    assert 'body[data-compare="on"] .pg-surfaces > section.active' in rendered_html
    assert 'body:not([data-compare="on"]) .pg-surfaces > section.active > [data-look="b"]' in rendered_html


def test_share_link_engine_present(rendered_html: str) -> None:
    """Sanity-check that the JS engine has the share + restore wiring."""
    assert "data-share-link" in rendered_html
    assert "location.hash" in rendered_html
    assert "atob(" in rendered_html  # restore path
    assert "btoa(" in rendered_html  # share path


def test_baked_presets_present(rendered_html: str) -> None:
    """The presets file is embedded; check by counting expected names."""
    m = re.search(r'<script type="application/json" id="presets-data">(.*?)</script>', rendered_html, re.S)
    presets = json.loads(m.group(1))
    names = {p.get("name") for p in presets}
    assert {"Maximalist", "Minimalist", "Dark-first"}.issubset(names)


def test_renders_against_plugin_template_tokens(tmp_path: Path) -> None:
    """The renderer must not crash on the plugin's own template tokens.json
    (mostly empty $value strings). Surfaces will look like the system fallback
    palette, but the file should still parse + open."""
    plugin_template = PLUGIN_ROOT / "assets" / "tokens-template.json"
    if not plugin_template.exists():
        pytest.skip(f"plugin template missing: {plugin_template}")
    brand_dir = tmp_path / "placeholder-brand"
    brand_dir.mkdir()
    (brand_dir / "tokens.json").write_bytes(plugin_template.read_bytes())
    out = tmp_path / "placeholder.html"
    result = _run(brand_dir, out)
    assert result.returncode == 0, f"renderer crashed on placeholder tokens: {result.stderr}"
    assert out.exists()
    html = out.read_text()
    for surface in ("marketing", "app", "slide", "glossary"):
        assert f'data-surface="{surface}"' in html
    assert not re.findall(r"\{\{[A-Z_]+\}\}", html)


def test_each_surface_has_a_and_b_clones(rendered_html: str) -> None:
    """Every surface must contain both a [data-look="a"] and [data-look="b"] subtree.

    Slice between consecutive `data-surface=` markers so nested <section> tags
    inside surface bodies (Marketing has many) don't break the boundary detection.
    """
    surfaces = ("marketing", "app", "slide", "glossary")
    positions = {}
    for s in surfaces:
        # Anchor on the surface SECTION, not the surface-tab button at the top.
        idx = rendered_html.index(f'<section data-surface="{s}"')
        positions[s] = idx
    for i, s in enumerate(surfaces):
        start = positions[s]
        end = positions[surfaces[i + 1]] if i + 1 < len(surfaces) else len(rendered_html)
        body = rendered_html[start:end]
        assert 'data-look="a"' in body, f"{s} missing data-look=a clone"
        assert 'data-look="b"' in body, f"{s} missing data-look=b clone"
