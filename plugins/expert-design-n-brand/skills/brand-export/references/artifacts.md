# Artifact Catalog — Tier-Classified

Loaded by `brand-export/SKILL.md` when producing individual artifacts. The catalog is organized by tier (per `build-export-contract.md`): Tier 1 external-reference, Tier 2 operator-process, Tier 3 LLM-optimized. Build artifacts internal to the plugin flow never appear here — they live in `_build/` and are not part of the shipping catalog.

Every section assumes the cross-artifact rules in `rendering-rules.md` have been loaded first — those are the defaults; what appears here is artifact-specific.

---

# Tier 1 — External reference (shipping, public-facing)

Twelve artifacts. These are the files a client, consultant, designer, or open-web consumer sees. Every draft is reviewed against the Tier 1 external-facing principle in `rendering-rules.md` before it is written.

## T1.1 — Brand Guidelines canonical doc (`brand-guidelines.html` + `brand-guidelines.pdf`)

The single definitive brand guidelines document. Covers §§ 0–12: Cover, Foundation, Identity, Color, Typography, Visual Language, Spacing/Grid, Components, Voice, Platform & Application, Governance, LLM Operating Manual pointer, Quick Reference pointer. Appendices: In Practice, Coherence, Quality Scorecards, Anti-Inspiration, Companion Files.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/design-system-template.html` (renamed canonical source — the "extensions" concept is retired).

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

Render:
1. Every section opens with `<p class="section-definition">` + `<p class="section-summary">` (contract-required, see rendering-rules.md).
2. Personality renders synthesis + character paragraph + archetype-in-action (≥3) + do/don't voice exemplars (≥3 each) per rendering-rules.md.
3. §3 Color renders palette + Color Role Playbook (≥8 roles) + contrast matrix per rendering-rules.md.
4. §5 Visual Language renders 10 sub-blocks (form primitives, composition, elevation, texture, motion, gradients, motifs, photography pointer, illustration pointer, 3D/spatial). Photography and illustration details are pointers to Tier 1 companion files T1.6/T1.7.
5. §9 Platform is a narrative overview linking to T1.8 Platform Matrix (the single consolidated cross-surface reference) and T1.10–T1.12 (Figma, Tailwind, email).
6. Sticky sidebar TOC listing only sections that actually render.
7. Cover page matches data from `meta` + `system`.

PDF: render HTML to PDF via headless-browser probe chain (chrome/chromium/chromium-browser; macOS app paths; wkhtmltopdf last-resort). Use `--virtual-time-budget=5000` so webfonts load. Use `--no-pdf-header-footer`. Output at A4 with print-friendly page breaks.

Verify after write: HTML opens without errors, PDF ≥ 1MB, page count 25–40, every `<section>` has both def+summary paragraphs, no `design-system-extensions` references.

## T1.2 — Brand Quick Reference (`brand-quickref.md`)

One-pager card. For non-designers and quick lookup.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/brand-quickref-template.md`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

Render: replace `{{ }}` placeholders with `system` + `meta` values. Variable-N principles, palette rows, expressions. Polymorphic Voice Constraints per rendering-rules.md. Compact enough to print on one page (≤ 60 lines target; 2-page acceptable with explicit note).

## T1.3 — Tokens CSS (`tokens.css`)

CSS custom properties from `system`:

- Primitive tokens: `--color-{role}-{step}`, `--spacing-*`, `--font-size-*`, `--radius-*`, `--shadow-*`. Role names from `system.color.palette.core[].role` (variable-N, not hardcoded).
- Scale tokens: `--color-{family}-{step}` for each `palette.scales[]` entry.
- Gradient tokens: `--gradient-{slug}` for each `palette.gradients[]` entry.
- Semantic tokens: `--color-bg-*`, `--color-text-*`, `--color-surface-*`, `--color-affirm`, `--color-warn`, `--color-success`, `--color-warning`, `--color-danger` (via semantic resolution in rendering-rules.md).
- `@import` Google Fonts for specified typefaces.
- `@media (prefers-reduced-motion)` reset.
- File-header comment with brand name + generation timestamp.

**Render mode:** no static template — `tokens.css` is generated programmatically from `system.color.palette.*`, `system.typography.*`, `system.form.*`. Still subject to the structural validator: the emitted CSS must declare every required `--color-*`, `--font-*`, `--space-*` custom property enumerated in `artifact-schemas.yaml → tokens-css`.

## T1.4 — Tokens JSON (`tokens.json`)

Design Tokens Community Group format (DTCG W3C 2025.10):

- Three-layer structure: `primitive`, `semantic`, `component`.
- Template: `${CLAUDE_PLUGIN_ROOT}/assets/tokens-template.json`. Variable-N palette roles become object keys. **Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.
- Every leaf has `$value` + `$type` + optional `$description`.
- Reference syntax `{path.to.token}` valid throughout.
- Multi-mode `semantic.light` / `semantic.dark` if brand declares dark-mode variants.

## T1.5 — Logo Construction (`logo-construction.svg`)

Valid SVG specifying the brand's wordmark and/or pictorial mark construction, clearspace, minimum size (px + mm), variants (primary, reversed, accent), misuse grid (≥ 6 entries). If the brand has no pictorial mark, publish construction INTENT (future-mark constraints).

Template: `${CLAUDE_PLUGIN_ROOT}/assets/logo-construction-template.svg`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T1.6 — Illustration System (`illustration-system.html`)

3–5 shape primitives (including flourish-vector if brand has one). Stroke-weight table (allowed + forbidden with px values). Perspective rule, palette constraint, emotion inventory (≥ 4 states), composition rules, decision tree (photography vs illustration vs type-only). Cultural anchors (≥ 3) each naming what property is anchored — vapor anchors (missing `anchors_property`) hard-fail.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/illustration-system-template.html`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T1.7 — Photography Reference Grid (`photography-reference-grid.html`)

Four rules (subject, lighting, crop, post), ≥ 5 approved references with `why`, ≥ 5 rejected references with `why`, lighting diagrams (preferred/acceptable/forbidden), post-processing target table, decision tree.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/photography-reference-grid-template.html`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T1.8 — Platform Matrix (`platform-matrix.md`)

The single consolidated cross-surface reference for applying the brand on every supported surface. Replaces what used to be three separate things: the prior `platform-matrix.html` (per-platform card layout), the prior `brand-cross-surface-map.md` (master grid), and the prior per-surface `theme-google-slides.md` / `theme-powerpoint.md` / `theme-keynote.md` / `theme-canva.md` / `theme-pitch.md` guides. One source of truth, markdown format, scannable.

Sections:
- §1 Color tokens — master table (rows = roles, cols = surfaces) + hex value table
- §2 Typography tokens — master table (rows = font family / size / weight / line-height / letter-spacing, cols = surfaces; **slot names only**, no fallback chain hints) + font choices for the brand
- §3 Form & spacing tokens — radius / shadow / border-width / spacing (mostly web/design; presentation surfaces apply manually)
- §4 Per-platform details — one sub-section per platform (Google Slides, PowerPoint, Keynote, Canva Pro, Canva Free, Figma). Each sub-section includes:
  - Setup steps (paste-ready instructions)
  - Typography fallback chain (heading + body) with rationale for why this character-matched chain was chosen
  - Probe notes (platform quirks specific to this surface)
  - Caveats (licensing, plan gates, rendering differences)
- §5 Where the source values come from (provenance: `tokens.json` + `surface-translations.yaml`)

Template: `${CLAUDE_PLUGIN_ROOT}/assets/platform-matrix-template.md`.

**Driven by:** `${CLAUDE_PLUGIN_ROOT}/assets/surface-translations.yaml` — every surface's slot mapping fills its column in the master tables; presentation surfaces additionally fill their §4 sub-section.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T1.9 — Governance (`governance.md`)

Ownership table (named roles), SemVer policy (major/minor/patch triggers), changelog (≥ 1 entry for current build), deprecation policy (≥ 90-day dual-ship window), contribution flow, decision log (≥ 3 ADRs if applicable — infer from synthesis trade-offs if not explicit), health check list (quarterly), file inventory listing every T1 shipping artifact.

**Tone**: end-user-facing, sanitized. No references to plugin internals, skill names, phase numbers, or internal concepts like "registry rows" / "expected-paths". The `Plugin maintenance` row that previously leaked into this template is retired — governance is about the *brand system*, not the plugin.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/governance-template.md`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T1.10 — Theme: Figma (`theme-figma.json`)

Tokens Studio-compatible JSON subset — a pre-formatted import file a Figma user can drop into the Tokens Studio plugin and have the brand's semantic tokens immediately available as variables.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/theme-figma-template.json`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T1.11 — Tailwind config (`tailwind.config.js`)

Tailwind v4 theme config object generated from the canonical token set. Drop into a project root; Tailwind picks it up automatically. Maps every primitive scale (color, fontSize, fontFamily, spacing, borderRadius, boxShadow, borderWidth, opacity, zIndex, screens) into the corresponding `theme.*` key.

Driven by: `surface-translations.yaml → surfaces[id=tailwind_config]`. No static template — generated programmatically from `tokens.json`.

**Render mode:** programmatic (no template). Validator checks that the file is valid JS and contains the required theme keys.

## T1.12 — Email Template (`email-template.html`)

Self-contained HTML email with inline styles drawn from the brand's tokens. Header (wordmark), body (prose with role-mapped text colors — primary body, tertiary meta), CTA button (primary on anchor), footer. Uses web-safe font stack ending in the brand's character-appropriate web-safe choice (Arial / Verdana / Georgia / Courier New depending on character).

Template: `${CLAUDE_PLUGIN_ROOT}/assets/email-template.html`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

---

# Tier 2 — Operator / process-facing (3 artifacts)

These serve the team using the plugin and the brand's internal stewards. They carry process context and auditability that Tier 1 deliberately omits. Still end-user-prose (no raw plugin jargon), but can reference the workflow explicitly.

## T2.1 — Brand Methods Record (`brand-methods.html` + `brand-methods.pdf`)

Process record — every used technique gets a block.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/brand-methods-template.html`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

Render:
1. Methods Ledger as Table of Contents — every technique in `techniques-registry.yaml`, Used/Inferred/— status, linked if Used.
2. One `<article class="technique-block">` per USED technique in registry declaration order. Populate per the technique-block specs below.
3. Ingest quotes via `system.techniques[].quotes[]` (populated by brand-synthesize) or fall back to parsing raw `*_Brand_Quotes.md`. Embed each block's matched quotes in `<section class="technique-quotes">`.
4. Collapsed Not-Run Appendix at bottom.

PDF: mirror structure via headless-browser probe chain. Output: `brand-methods.pdf`.

### Per-technique block render specs

**Positioning**
- `elevator-pitch` → styled blockquote + speaker-tagged if multi-participant
- `wolff-olins-butterfly` → 2×2 cells (IS / ISN'T / DOES / DOESN'T) with colored quadrants
- `landscape-grid` → 2×2 with axis labels + dot placements for competitors + the brand
- `brand-eulogy` → serif prose block with eyebrow framing line
- `competitive-mapping` → table: Competitor · Voice · Visual · Value Prop · Differentiation

**Personality**
- `archetype-selection` → Primary + Secondary archetype cards + reasoning paragraph
- `aaker-sliders` → 5-row scored table with bar indicators
- `tension-spectrum-mapping` → N-row table with spectrum, anchor points, scored position
- `keyword-distillation` → keyword chips in the brand palette
- `metaphors` → card gallery: name + type + trait list + one-line mapping
- `celebrity-casting` → two-column list: Role → Person (Why)
- `brand-playlist` → song list with artist, year, one-line "why this fits"

**Visual**
- `palette-recognition` → summary of what was chosen + elimination set
- `type-pairing` → summary pair + rejected alternatives + character classifications
- `mood-board` → bulleted list of cultural/image references; thumbnails if image paths in YAML
- `form-language` → SKIP (output lives in Tier 1 only)
- `anti-inspiration` → list of brand names with one-line rejections
- `texture-material` → material description paragraph + swatch references

**Voice**
- `sample-writing` → three samples (tweet / apology / celebration) as styled blockquotes
- `formality-spectrum` → visual slider with marked position + scale_max
- `never-say-list` → list + rationale, both halves of the specificity principle (see rendering-rules.md)
- `specificity-test` → the rule + pass/fail examples in two columns
- `voice-card-sort` → two columns (`.output-pairing-grid` — NOT `.output-butterfly`)
- `competitor-voice-comparison` → comparison table

**Stress tests** (all Tier 2 only)
- `pre-mortem` → risk list with likelihood/severity indicators
- `inversion` → `.output-pairing-grid` two columns (Values / Inverted Brand)
- `stakeholder-lens` → per-stakeholder paragraph
- `time-travel` → `.output-pairing-grid` two columns (past / future)

**Quality**
- `rand-seven` → 7-row scored table
- `coherence-check` → 6-axis table with total

## T2.2 — Brand Quotes (`brand-quotes.md`)

Raw quotes harvested across discovery + feedback iterations. Each per-participant `{name}-brand-quotes.md` file is a working artifact during discovery/synthesis. Content round-trips into `system.techniques[].quotes[]` during synthesize — so it is *readable* in the canonical output via brand-methods' quote-ingestion rule.

The template is `${CLAUDE_PLUGIN_ROOT}/assets/brand-quotes-template.md` (copied + renamed per participant during discovery).

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0. The per-participant copy step is the literal `cp` — only the `{{ }}` placeholders (participant name, quote paste slots) get filled.

Not shipped as a single output file; multiple per-participant files live in the working directory. Their content persists into T2.1 via `system.techniques[].quotes[]`.

## T2.3 — Synthesis Report (`synthesis-report.md`)

Side-by-side discovery data from N participants — where the team agrees, where they diverge, what was resolved. Populated by `brand-synthesize`.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/synthesis-report-template.md`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

---

# Tier 3 — LLM-optimized (2 files, following brand.md v0.2.0 spec)

Machine-readable sibling for downstream generation. Conforms to the brand.md standard (https://github.com/thebrandmd/brand.md) with plugin-specific extensions.

## T3.1 — Brand.md canonical (`brand.md`)

Follows the brand.md v0.2.0 spec: YAML frontmatter + 12 required sections across Strategy (Overview, Positioning, Personality, Promise, Guardrails), Voice (Identity, Tagline & Slogans, Message Pillars, Phrases, Tonal Rules), and Visual (Colors, Typography). Optional sections: Manifesto, Social Bios, Photography, Style.

Frontmatter required: `name`, `tagline`, `version` (integer), `language`. Optional: `type`, `architecture`. Plugin-specific: `extensions: "./brand.extensions.yaml"`, `owner`, `generated`.

Template: `${CLAUDE_PLUGIN_ROOT}/assets/brand-template.md`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

## T3.2 — Brand extensions (`brand.extensions.yaml`)

Plugin-specific machine-enforceable rules that the brand.md spec doesn't cover: tone_matrix, output_constraints, vocabulary (with replacements + reasons), refusal_triggers, visual_language details (form_primitives, composition, elevation, motion tokens, gradients, motif_library, illustration, spatial_3d), cultural_anchors (each with `anchors_property`), platforms (font chains + color slots + export profiles), governance, reference_bank + counter_bank, self_validation targets.

Points back to `brand.md` via `sibling_of: "./brand.md"` (plugin-local pointer, not part of the brand.md v0.2.0 spec).

Template: `${CLAUDE_PLUGIN_ROOT}/assets/brand-extensions-template.yaml`.

**Render mode:** copy-first, fill-only. Do not recreate from scratch; see `rendering-rules.md` Rule 0.

---

# Build artifacts (internal — not shipped to output folder)

These stay in a `_build/` subdirectory of the output folder if retained at all; they are NEVER surfaced as user-facing deliverables. Default behavior: do not emit unless operator explicitly requests `--keep-build-artifacts`.

- `export-verification.md` — quality report from the verification protocol; useful for operator debugging, not for clients
- `design-system.html` / `.pdf` — legacy intermediate subsumed by T1.1 (retain only as temporary migration aid; delete in v0.8)
- `design-system-extensions.html` — retired concept (DELETE; do not re-emit)
- `brand-llm-manual.yaml` — retired format (replaced by T3.1 + T3.2; DELETE)
- `tokens.legacy.json` — retired archive (DELETE unless brand explicitly migrating from v5)
- `TEST_PROTOCOL.md` — plugin dev scaffolding; belongs in plans/, NEVER emitted

---

# Emission sequence (for `/brand-export all`)

1. Load contract + rendering rules.
2. Walk Required-atomic + Required-v6 paths; hard-fail at startup on any missing.
3. Emit Tier 1 (review each draft against the external-facing principle before write):
   1. T1.3 `tokens.css`
   2. T1.4 `tokens.json`
   3. T1.5 `logo-construction.svg`
   4. T1.6 `illustration-system.html`
   5. T1.7 `photography-reference-grid.html`
   6. T1.8 `platform-matrix.md` — single consolidated cross-surface reference
   7. T1.9 `governance.md`
   8. T1.10 `theme-figma.json` — Figma Tokens Studio import
   9. T1.11 `tailwind.config.js` — Tailwind v4 theme config
   10. T1.12 `email-template.html`
   11. T1.1 `brand-guidelines.html` + PDF (canonical — rendered last so it can cross-link to all the above)
   12. T1.2 `brand-quickref.md`
4. Emit Tier 2:
   1. T2.1 `brand-methods.html` + `.pdf`
   2. T2.3 `synthesis-report.md` (if synthesize was run)
   - T2.2 quotes live as per-participant files in the working directory; no new emission
5. Emit Tier 3:
   1. T3.1 `brand.md`
   2. T3.2 `brand.extensions.yaml`
6. Run `export-verification-checklist.md`. Block on any RED gate.
7. Write the verification report to `_build/export-verification.md` (NOT the user-facing output folder).
