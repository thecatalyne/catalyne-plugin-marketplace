---
name: design-system
description: "This skill should be used when generating design tokens, applying 60-30-10 color rules, resolving WCAG contrast questions, making typography-scale or spacing decisions, choosing motion/easing values, or working with the 3-layer token taxonomy (primitive → semantic → component). Reference library consulted by brand-build and brand-export — not invoked directly by users."
allowed-tools: ["Read", "Grep", "Glob"]
---

Reference library for design system generation. Provides the token architecture, concrete design rules, and template assets used by the brand-build and brand-export skills. This skill is consulted, not invoked — users run `/brand-build` or `/brand-export`; those skills load references from here.

## Available References

### Token Architecture
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/token-architecture.md`
**When to load**: When generating design tokens, creating CSS custom properties, structuring JSON token output, or explaining the 3-layer token system (primitive → semantic → component).

Covers: complete 3-layer taxonomy with naming conventions, generation rules from brand identity, CSS and JSON output formats, and token naming rules.

### Design Rules
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/design-rules.md`
**When to load**: When making specific design decisions — color application (60-30-10), typography scales (modular ratios), spacing systems, motion/animation, form language (border radius, shadows), or WCAG contrast requirements.

Covers: color rules (60-30-10, WCAG contrast, harmony), typography rules (modular scales, line height, letter spacing, font pairing), spacing/layout rules, motion rules (duration, easing), and form language rules (radius, shadows). Each rule maps to Aaker personality dimensions.

### Typography Taxonomy
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/typography-taxonomy.md`
**When to load**: When classifying the brand's typefaces during brand-discover, or resolving per-platform fallback chains during brand-build Phase 7.6.

Covers: 12 character categories (geometric-sans-light, humanist-sans, neo-grotesque, humanist-serif, modern-serif, display-serif, display-sans, slab-serif, mono-humanist, mono-geometric, script-hand, technical-display) with exemplars. Cross-reference table for substitution ordering.

### Platform Fonts Knowledge Base
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/platform-fonts.yaml`
**When to load**: When brand-build runs the typography substitution algorithm (Phase 7.6) or when brand-export renders platform-matrix or theme-builder companion files.

Covers: per-platform font availability across Google Slides, Google Docs, Figma, Pitch, Keynote, PowerPoint/M365, Canva (free + Pro), Notion, web-safe/email, and web apps. Lists best-available typefaces per taxonomy category, plus color-slot structures and probe notes per platform.

## Template Assets

All render templates live in plugin-root `${CLAUDE_PLUGIN_ROOT}/assets/`. The `skills/design-system/assets/` folder holds only the three discovery checkpoint pages (palette/type/accent recognition tests) shown to users during `/brand-discover`.

### Core Templates

**`tokens-template.json`** — DTCG W3C 2025.10 scaffold. Every leaf has `$value`, `$type`, `$description`. Three-tier structure (primitive → semantic → component) with explicit light/dark modes, `semantic.status` + `semantic.elevation`, `platform.*` section. Consumed by brand-export to produce `tokens.json`.

**`design-system-template.html`** — canonical Tier 1 HTML template. Produces `brand-guidelines.html` (the unified canonical doc covering §§0–12 + appendices A–E).

**`design-system-print.html`** — print-media variant for PDF render.

**`brand-methods-template.html`** + **`brand-methods-print.html`** — Tier 2 process record (methods ledger + per-technique blocks).

### Tier 1 companion templates

**`platform-matrix-template.md`** — single consolidated cross-surface reference. Master tables (rows = tokens, columns = surfaces) for color, typography, and form & spacing. Per-platform sub-sections below carry setup steps, typography fallback chains with rationale, probe notes, and caveats. Replaces the prior `platform-matrix.html` per-platform-card layout AND the prior per-surface `theme-*.md` guides AND the prior `brand-cross-surface-map.md`. Enforces the R2 no-collapse rule across all per-platform sections.

**`governance-template.md`** — ownership, SemVer policy, changelog, deprecation window (≥90 days), contribution flow, ADR decision log, health-check list, tier-classified file inventory. End-user vocabulary only.

**`illustration-system-template.html`** — shape primitives, stroke table (allowed + forbidden), perspective rule, palette constraint, emotion inventory (≥4 states), composition rules, decision tree (photo vs illustration vs type), ≥3 cultural anchors each naming what property is anchored.

**`photography-reference-grid-template.html`** — 4 rules (subject, lighting, crop, post), ≥5 approved + ≥5 rejected references with `why`, lighting diagrams, post-processing targets, decision tree.

**`logo-construction-template.svg`** — signature device construction. Wordmark/mark, clearspace, minimum size (px + mm), variants (primary / reversed / accent), misuse grid (≥6 items), construction intent block.

### Cross-surface companions (Tier 1)

Surface-to-token slot mapping is declared in `${CLAUDE_PLUGIN_ROOT}/assets/surface-translations.yaml` (one block per surface). The cross-surface output is split between machine artifacts (one file per format) and the consolidated human-facing reference:

- **`tokens.css`** *(in `core` bundle, not companions)* — universal CSS custom properties (machine artifact). No template; generated programmatically.
- **`tailwind.config.js`** — Tailwind v4 theme config (machine artifact). No template; generated programmatically from `tokens.json`.
- **`theme-figma-template.json`** — Tokens Studio JSON for Figma Variables import (machine artifact).
- **`platform-matrix-template.md`** — single consolidated human-facing reference. Master tables (rows = tokens/components, columns = surfaces: Web CSS, Tailwind, Figma, Google Slides, PowerPoint, Keynote, Canva Pro+Free). Plus per-platform §4 sub-sections (Google Slides, PowerPoint, Keynote, Canva Pro, Canva Free, Figma) with setup steps, typography fallback chains, probe notes, and caveats.
- **`email-template.html`** — self-contained HTML email with inline styles.

This single `platform-matrix.md` deliverable replaces three separate things we used to render: the prior `platform-matrix.html` (per-platform card layout), the prior `brand-cross-surface-map.md` (master grid only), and the four per-surface `theme-*.md` guides (Google Slides, PowerPoint, Keynote, Canva). One source of truth.

Pitch / iOS / Android / Notion / SCSS / InDesign are opt-in only — uncomment in `surface-translations.yaml` to add them as columns and per-platform sections.

### Tier 2 operator templates

**`brand-methods-template.html`** (above) and the plugin-root `assets/brand-quotes-template.md`, `assets/synthesis-report-template.md` (working files during discovery and synthesis).

### Tier 3 LLM templates

**`brand-template.md`** — canonical brand definition following the brand.md v0.2.0 specification (YAML frontmatter + 12 required sections across Strategy / Voice / Visual). Emitted as `brand.md` in the output folder.

**`brand-extensions-template.yaml`** — plugin-specific machine-enforceable rules the brand.md spec doesn't cover: tone matrix, output constraints, structured banned vocab, refusal triggers, visual-language details, cultural-anchor properties, per-platform font chains, self-validation. Emitted as `brand.extensions.yaml`. Points back to `brand.md` via `sibling_of` (plugin-local pointer, not part of the brand.md v0.2.0 spec).

## Motif Spectrum Mapping

Motifs are named with semantic intent. A motif's rendered color gradient must match the spectrum its name implies, drawn from the brand's own palette — not a single stock brand gradient. `brand-export` applies this at render time; this section is the mapping table it consults.

The name patterns below are a starting point — any brand can declare additional motif families in its own palette. The principle is that the name predicts the spectrum, and the spectrum is built from the brand's declared anchors.

| Name pattern | Spectrum | How to resolve from brand palette |
|---|---|---|
| Warm-fire family (`ember`, `flame`, `fire`, `burn`, `spark`, `heat`) | Warm (red → orange → amber) | Pick the brand's warm-lineage anchors in order. Never substitute a cool-spectrum hex. |
| Cool-signal family (`electric`, `current`, `signal`, `pulse`) | Active accent / signal | The expression the brand has tagged as its default signal expression in `palette.expressions[]`. |
| Celestial family (`star`, `sun`, `gold`, `celestial`, `constellation`) | Gold-core | Anchor on the gold / amber hex with only subtle grace notes at edges. Single-hue focus. |
| Transition family (`match`, `strike`, `ignite`, `threshold`) | Warm-core into ignition | Bright center sliding into the brand's warm spectrum at one edge. |
| Prismatic family (`prism`, `rainbow`, `spectrum`) | Prismatic (multi-hue rotation) | Full hue rotation. Route through the brand's prismatic anchor if present; if not declared, skip. |
| *no match* | Monochrome accent | Single anchor from `palette.core.accent` with a lighter tint stop. Do not invent a gradient the brand hasn't declared. |

**Invariant:** A motif's spectrum must match its name. If a brand lacks the spectrum a motif's name requires (e.g. a `flame` motif but no warm anchors), record the mismatch in the verification report and substitute the closest available anchor rather than silently routing through the primary brand color — the mismatch is the signal.

## Usage Notes

- The brand-build skill loads these references during the build phase.
- Token generation follows: resolved synthesis → personality-to-design mapping → primitive tokens → semantic tokens → contrast validation.
- Export artifacts (CSS, JSON, HTML) are produced separately during the export phase.
