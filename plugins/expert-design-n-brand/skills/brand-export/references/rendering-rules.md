# Rendering Rules — Cross-Artifact

Loaded by `brand-export/SKILL.md` before rendering any artifact. These rules apply across every artifact the plugin emits. Read this file in full before starting a render — most failures at verification time trace back to a rule on this page.

> **Canonical vocabulary source.** Token names, role labels, surface slot names, and CSS/Tailwind/Figma keys mentioned anywhere in these rules are defined in `assets/platform-matrix-template.md`. The 14-slot L/D color-role parity contract is in `skills/design-system/references/token-architecture.md`. If a name in this file appears to disagree with either source, the Matrix wins; treat the disagreement as a bug.

Every rule specifies which **tier** it applies to. Tiers are defined in `build-export-contract.md`:

- **Tier 1** — external reference (brand-guidelines.html, quickref, tokens, logo, illustration, photography, platform-matrix, governance, theme-builder companions, email-template)
- **Tier 2** — operator / process-facing (brand-methods.html, brand-quotes, synthesis-report)
- **Tier 3** — LLM-optimized (brand.md + brand.extensions.yaml, following the brand.md v0.2.0 spec)

Tier membership matters because some rules (section definition+summary scaffolds, external-facing tone) are Tier-1 only; others (technique-block anatomy) are Tier-2 only; a few (semantic theme tokens, cultural-anchor vapor check) are universal.

---

## Rule 0 — Template-first rendering (universal, overriding)

**Every templated artifact is rendered by copy-first, fill-only.** This rule overrides any other rule on this page when the two conflict.

The procedure for every artifact listed in `artifacts.md`:

1. **Copy** the template file at its `Template:` path to the output location under `./brand-assets/` (or wherever the artifact is destined). Use `cp`, not `Write` — start the render with a byte-identical working draft.
2. **Fill** the draft in place: replace every `{{ placeholder }}` with the matching value from `brand-identity.yaml`; expand `<!-- REPEAT:name -->` blocks over the driving collection; drop `<!-- OPTIONAL:name -->` blocks whose driving technique was not run.
3. **Never restructure.** Do not rename section IDs, reorder sections, invent new sections, rewrite CSS variable names, rename JSON keys, or change Markdown heading text that carries a slug. Creative surface lives *inside* placeholders — not in the scaffold around them.
4. After the fill pass, apply the remaining rules on this page (voice-constraint polymorphism, semantic color routing, Tier-1 external-facing tone, etc.) — but only to content the template asks for. The structural skeleton is already correct by construction.
5. Structural compliance is checked by `${CLAUDE_PLUGIN_ROOT}/scripts/validate-structure.py` after write. If the check fails, re-render from the template once (one shot only) and re-check. Record the outcome in `system.quality.export_log[]` regardless of final status.

Why this rule exists: LLM-authored HTML/Markdown drifts across runs when the model is asked to "draft" a document the template already contains. Two brands rendered from the same template have shown ~85% structural divergence (different section IDs, dropped sections, renamed variables) when each render started from scratch. Copy-first removes the drift surface almost entirely; fill-only confines creativity to content.

If a template seems wrong (missing a block you want, wrong structure for this brand) — **do not improvise in the render**. Update the template file under plugin-root `assets/`, commit the change, and the next render will use it. Templates are the source of truth; renders are mechanical outputs from them.

---

## Canonical vs process-record separation (universal)

`brand-guidelines.html` (Tier 1) is a publishable working doc real users reference and use. `brand-methods.html` (Tier 2) is the process-record artifact where every used technique appears as a block. The registry `drives_sections` edges are the routing source of truth:

- **Any technique whose `drives_sections` contains `brand_methods.*` but no `design_system.*` edge MUST NOT produce content in `brand-guidelines.html`**, even if the YAML holds matching data. Examples: `metaphors`, `celebrity-casting`, `brand-playlist`, `tension-spectrum-mapping`, `mood-board`, `landscape-grid`, `pre-mortem`, `inversion`, `stakeholder-lens`, `time-travel`.
- **Any technique with a `brand_methods.*` edge MUST produce a technique block in `brand-methods.html`** regardless of whether it also renders in brand-guidelines.html.
- **Techniques with `design_system.*` edges only** (canonical-only — `elevator-pitch`, `wolff-olins-butterfly`, `palette-recognition`, `type-pairing`, `form-language`, `texture-material`, `sample-writing`, `formality-spectrum`, `never-say-list`, `specificity-test`, `voice-card-sort`, `rand-seven`, `coherence-check`) render in brand-guidelines.html AND produce a brand-methods block via `artifact_routing.brand_methods.one_block_per_used_technique: true`. Their brand-methods block is a thin process record: technique name + description + "what it produced" summary. **Exception: `form-language`** — the form-language technique does NOT get a brand-methods block (its output IS the canonical form system; there is no separable process record).

## Section definition + summary pairs (Tier 1)

Every section in the canonical Tier 1 doc opens with TWO paragraphs before any data display:

1. `<p class="section-definition">` — *universal* copy describing what this section IS in a brand system (fixed template copy that reads the same for every brand).
2. `<p class="section-summary">` — *brand-specific* answer to that definition, sourced from `system.section_summaries.{slug}` in brand-identity.yaml.

The template source MUST include literal `<p class="section-definition">...</p>` and `<p class="section-summary">{{ section_summary }}</p>` for every section. This rule is TEMPLATE-ENFORCED — do not leave it to the model to "remember" at render time.

Recognized section slugs (per `build-export-contract.md`): `foundation, identity, color, typography, visual_language, spacing, components, voice, platforms, governance, llm_manual, quickref`.

Every slug must have a summary in `system.section_summaries.*`. If missing, brand-build Phase 8 HARD-FAILS — summaries are Required per the contract. Do not auto-compose at export time.

## Personality anatomy (Tier 1 canonical doc)

The personality section in `brand-guidelines.html` renders in this order:

1. **Essence + Archetype split** (`<section class="personality-essence-archetype">`) — two side-by-side cards:
   - Left card: `<div class="personality-essence"><h4>Essence</h4><p>{{ essence_name }}</p><p class="essence-blurb">{{ essence_blurb }}</p></div>` — the brand's signature identity, sourced from `system.identity.essence`.
   - Right card: `<div class="personality-archetype"><h4>Archetype</h4><p>{{ archetype_primary }}{% if archetype_secondary %} · {{ archetype_secondary }}{% endif %}</p><p class="archetype-register">Register: {{ register }}</p></div>` — Jungian/Mark-Pearson archetype + optional register modifier.

   **Never compound these.** Render `essence.name` and `archetype_primary` as two distinct labels in adjacent cards. Any "{essence}-{archetype}" or "{essence} {archetype}" compound is forbidden, in any spacing or punctuation. The compound label is meaningless to a reader — essence is the brand's chosen identity statement, archetype is the personality framework category. Keep them visually and grammatically separate.

2. `<p class="personality-synthesis">{{ personality_synthesis }}</p>` — one-sentence taxonomy (from `system.personality.synthesis`).
3. `<p class="personality-character">{{ personality_character }}</p>` — 40–70 word narrative texture (from `system.personality.character`). **Required per contract; do not soft-skip.**
4. Archetype label row (primary + optional blend + optional triad) — this is a more detailed expansion of the archetype card above; keep order.
5. Aaker scores row (5 dimensions; render only if all 5 present — never zero-fill partials).
6. Keyword chip row (3–5 items).
7. **Archetype in action** (`<section class="personality-archetype-in-action">`) — ≥3 worked examples from `system.personality.archetype_in_action[]`. Each example: `<div class="archetype-example"><h4>{{ context }}</h4><p>{{ text }}</p></div>`. Shows *how* the archetype sounds in actual copy (landing line, onboarding, celebration, apology).
8. **Do / Don't voice exemplars** (`<section class="personality-do-dont">`) — two columns from `system.personality.do_dont.{do, dont}`. Each column ≥3 items; render as lists with affirm/warn semantic coloring (via `--color-affirm` / `--color-warn`).

The canonical personality carries enough texture to be applied by a designer or content writer without opening brand-methods. The longer reasoning prose, metaphor galleries, playlists, tension spectra, and celebrity casting still route to brand-methods.

## Never-Say / Specificity principle — both halves (Tier 1 and Tier 2)

When rendering the never-say-list or specificity-test technique subblock, the principle MUST surface both halves:

1. **Positive constraint:** "Never use a word as decoration — every word must add specificity and meaning."
2. **Test question (derived):** "Does this word add specificity, or is it just performing?"

Emit both as separate paragraphs — the positive constraint bolded, the test question italicized beneath — inside the `.voice-constraint` block. A rendering that shows only the test question FAILS verification; the positive constraint is the stem the test grows from. Applies in both brand-guidelines.html AND brand-methods.html.

```html
<p><strong>Never use a word as decoration.</strong> Every word must add specificity and meaning.</p>
<p><em>The test: "Does this word add specificity, or is it just performing?"</em></p>
```

## Semantic theme tokens (Tier 1)

Templates expose semantic role tokens that every Do/Don't pair, rating badge, and status chip routes through: `--color-affirm`, `--color-warn`, `--color-success`, `--color-warning`, `--color-danger`. These let a brand's own voice carry through — instead of every rendered system showing the same stock green/red, a brand's semantic colors derive from its palette.

Resolution order (first match wins; emit the chosen hex into `{{ color_*_fallback }}` slots in the template `:root`):

1. **Explicit YAML:** `system.semantic.affirm_color`, `system.semantic.warn_color`, `system.semantic.success_color`, `system.semantic.warning_color`, `system.semantic.danger_color` — use verbatim if set.
2. **Expression inference:** walk `system.color.palette.expressions[]`. For `affirm`, prefer expressions tagged `intent: affirm|positive|electric|success` (use expression's representative anchor hex). For `warn`, prefer `intent: warn|danger|flame`.
3. **Anchor inference:** walk `system.color.anchors[]`. Pick the teal/green/cyan anchor for affirm; pick the red/orange anchor for warn by hue-matching. Hue bands: affirm = 150–200° (greens/teals); warn = 0–30° (reds/oranges).
4. **Neutral fallback:** `#16A34A` for affirm, `#DC2626` for warn, `#F59E0B` for warning; success=affirm, danger=warn.

Record the resolution in the verification report: `"semantic.affirm resolved from {source}: {hex}"`. Never hardcode stock green/red into rendered output — always route via the tokens.

## Color Role Playbook (Tier 1)

Every Tier 1 canonical doc renders a "Color Role Playbook" sub-section inside §3 Color, between the palette display and the contrast matrix. Data source: `system.color.roles[]` (Required per contract; ≥8 roles).

Rendering as a table: columns = Role · Token · Hex · When to use · Don't use for. One row per entry in `system.color.roles[]`. The role column uses the brand's role name; the token column uses the CSS custom property name; the hex column shows the resolved color with a small swatch swatch.

This is the authoritative mapping from "which color plays which role" for the brand — the canonical source any theme-builder companion file references. If a role is later used in the doc for tertiary text / caption / meta (via `.subblock-via` class or similar), it must trace back to an entry in the Role Playbook.

Minimum expected role coverage (roles may be named per brand but the concepts must be present): primary-body-text, secondary-text, tertiary-or-meta-text, link, heading, inverse-text, error-or-warn, success-or-affirm. Brands may add flourish-only, decorative-only, or other custom roles — the row count is variable-N.

## Typography substitution (Tier 1)

Per-platform type substitution is driven by three inputs:

1. The brand's `typography.heading.character` and `typography.body.character` slugs (Required; from `typography-taxonomy.md`).
2. `typography.heading.primary.family` + `typography.body.primary.family`.
3. The target platform's entry in `skills/design-system/references/platform-fonts.yaml`.

The substitution algorithm (R1–R6, defined in `build-export-contract.md`) is run by `brand-build` Phase 7.6 and stored in `system.typography.per_platform.{platform}`. Export reads that stored field directly — does NOT re-compute at render time.

**R2 (the "no collapse" rule)** is the load-bearing invariant: `heading_chain[1]` (first non-primary fallback) MUST NOT equal `body.primary.family` unless R6 applies (the brand uses the same family for both, deliberately). R6 is signaled by `discovery.{name}.visual.typography.single_family: true` or by build detecting `heading.primary.family == body.primary.family AND heading.character == body.character`.

Export-side verification: for every `typography.per_platform.*` entry, confirm `heading_chain` respects R2. If violated, block render with a diagnostic pointing to brand-build for re-derivation.

## Motif color-spectrum mapping (Tier 1, motif gallery)

Motifs are **named with semantic intent** (not generic labels like "motif 1") and must render in the color spectrum their name implies. The mapping derives from `system.motif_library[].name` and the brand's available expressions/anchors.

General rules (no hardcoded brand-specific hexes). Patterns below are semantic groupings drawn from common motif vocabularies — add or remove patterns per the brand's own motif lexicon:

- Warm / fire family (fire, flame, ember, heat, ignite) → warm spectrum built from the brand's red / orange / amber anchors if present. Brand-specific poetic names belong in `extensions.*` per `assets/platform-matrix-template.md` §6.
- Cool-signal family (electric, current, signal, pulse) → the brand's declared accent-signal expression (whichever `expressions[]` entry the brand flagged as its active / signal expression).
- Celestial family (star, gold, sun, constellation) → the brand's gold / amber anchor as core, secondary accent at edges.
- Transition family (match, strike, ignite, threshold) → transitional from a warm core into the brand's ignition spectrum.
- Prismatic family (prism, rainbow, spectrum) → full multi-hue rotation through the brand's declared prismatic expression, if one exists.
- **No name match** → single-anchor monochrome using `system.color.palette.core[accent].hex` with a lighter stop. Do not invent gradients the brand hasn't declared.

Record the choice in the verification report: `"motif '{name}' rendered in {spectrum} spectrum: {hex1} → {hex2} → {hex3}"`.

## Hero motif placement (Tier 1, in-practice / hero panel)

The hero SVG / motif must not visually compete with the headline. Before emission:

1. Compute the motif's bounding-box region.
2. Compute an approximate headline bounding box: left-aligned by default, width ≈ `min(hero_width, 32em)`, height ≈ 2× headline line-height.
3. **If the motif overlaps ANY headline word region**, take exactly one mitigation:
   - Offset the motif to a headline-free region (preferred order: bottom-right below headline + sub-copy, top-right above headline right-aligned, far-left under eyebrow).
   - If no offset is viable, drop motif opacity to `0.25` or less and keep it as atmospheric background.
4. Never render the motif at full opacity behind the most important word of the headline.

## Form Language specimens (Tier 1, form-language / spacing sections)

The Form Language section MUST render visual specimens — never collapse to a token table:

- For each radius token: emit `<div class="radius-pill" style="border-radius: {value}"></div>` with a caption showing token name and value.
- For each spacing step: emit `<div class="spacing-item"><div class="spacing-block" style="width: {value}; height: {value}"></div><div class="spacing-label">{token} · {value}</div></div>` inside `.spacing-grid`.
- For each type-scale step: emit `<div class="type-specimen" style="font-size: {value}">{sample_text}</div>` with the token name and computed size labelled adjacent.

A plain `<table>` of radius names, spacing values, or type steps is NOT acceptable. The template's `.radius-pill`, `.spacing-block`, `.type-specimen` CSS exists so these concepts render as visual artifacts.

## Pairing grid vs butterfly (Tier 2, brand-methods)

`.output-butterfly` is reserved for true 2×2 Is/Isn't/Does/Doesn't content (Wolff-Olins butterfly only). For any other 2-up content in brand-methods.html (voice card sort Passes/Fails, texture base/flourish pairs, inversion values-vs-inverted-brand, etc.), use `.output-pairing-grid` — it has `align-items: stretch` and `min-height` on children so cells don't collapse. Never render a 2-child `.output-butterfly`; validators fail.

## Per-section method chips (Tier 1 and Tier 2)

Each rendered section gets inline method chips under its heading:

1. For each `<!-- REPEAT: methods_for_{section_slug} -->` marker, look up the slug in the registry. A technique belongs to a section if the section_slug appears in the technique's `drives_sections[]`.
2. Mark `used` if at least one participant ran it AND their `yaml_paths` are populated. Mark `unrun` otherwise.
3. Render used as `method-chip--used`; unrun as `method-chip--unrun` (grey, strikethrough).
4. Suppress the entire `.section-methods` div if no techniques are associated with the section.

## Methods ledger (Tier 2, brand-methods)

Artifact B owns the full ledger. Render exactly ONCE as the Table of Contents:

1. For each technique in `techniques-registry.yaml → techniques`, in declaration order, emit a row with Dimension · Technique label · Status (`Used` or `—`) · `#anchor` link (if Used).
2. Inferred entries (from `synthesis.methods_used[]` with status `inferred`) render as a distinct third tier between `Used` and `—`.
3. `Used` rows link to the per-technique block below; `—` rows are unlinked and grey.

## Per-technique blocks (Tier 2, brand-methods)

One `<article class="technique-block">` per USED technique, in registry declaration order. Populate `{{ technique.output_html }}` based on the technique's dimension/semantics. See `artifacts.md` for the per-technique rendering specs.

## Quote ingestion (Tier 2, brand-methods)

For each per-technique block, attempt to ingest relevant quotes:

1. Check `system.techniques[].quotes[]` in brand-identity.yaml (populated by brand-synthesize from raw `{name}-brand-quotes.md` files).
2. For each technique with a `quotes[]` array, populate `{{ technique_quotes }}` inside `<section class="technique-quotes">` using `<!-- REPEAT: technique_quotes -->`. Render each quote as `<blockquote><p>"{{ text }}"</p><footer>— {{ speaker }}{{ " · " + context if context }}</footer></blockquote>`.
3. If `system.techniques[].quotes[]` is empty, fall back to parsing raw `*_Brand_Quotes.md` files in the working directory. If no quotes available from either source, omit the `technique-quotes` section entirely (do not leave an empty shell).

## Polymorphic concept slots (Tier 1)

For each `<!-- OPTIONAL:{concept_anchor} -->` marker, consult `techniques-registry.yaml → concepts`:

- The canonical heading renders IFF at least one technique in the concept group is `used`.
- Render one subblock per `used` technique, in the group's declaration order.
- Each subblock is tagged with italic `*via {technique.label}*` (markdown) or `<div class="voice-constraint-method">via {label}</div>` (HTML).
- Concept groups: `voice_constraints`, `personality_scoring`, `positioning_frames`, `visual_references`.

## Multi-layer palette rendering (Tier 1)

The Color section renders these stacked subsections, each soft-skipping when empty:

1. **Core Roles** (`palette_core`) — N swatches. Every swatch surfaces BOTH its role AND its `name` field.
2. **Color Role Playbook** (`color_role_playbook`) — Required sub-section; see rule above.
3. **Anchor Set** (`palette_anchors`) — card grid of named hexes distinct from core roles.
4. **Color Scales** (`palette_scales`) — 10-step strip per family with per-step names.
5. **Expressions** (`palette_expressions`) — spectral range cards for flourish expressions.
6. **Gradient Library** (`palette_gradients`) — labeled gradient strips.
7. **Contrast matrix** (`palette_contrast_pairs`) — fg/bg pair table with WCAG rating per row.

## Variable-N collections

- `system.principles[]` renders N rows — do NOT pad to 5 or cap at 7.
- `system.color.palette.core[]` renders N swatches — 3 or 9, template adapts.
- `system.color.palette.{anchors,scales,expressions,gradients}[]` render iff non-empty.
- `system.color.roles[]` renders N rows in the Role Playbook — ≥8 required.
- `system.form_language.motifs[]` renders in the Motif Gallery section.
- `system.platforms[]` adds N columns in the master tables AND N per-platform sub-sections in `platform-matrix.md`.

## Cover ledger (Tier 1)

The cover ledger line on both the interactive HTML and print PDF reads:
`Primary {hex} · Accent {hex} · Type {heading}/{body} · Scale {scale_name}` with `· Coherence {n}/30` appended only if `system.quality.coherence_score` is set, and `· Rand {n}/70` only if `system.quality.rand_seven.total` is set. Omit segments that have no data.

## Sample text injection (Tier 1)

Typography specimens MUST use brand-relevant sample text, NOT "The quick brown fox". Read `system.typography.sample_text.{display, h1, h2, h3, body, small}` — all six are Required per contract. Do not leave `{{ sample_* }}` unresolved.

## Cultural anchor vapor check (universal)

If `system.cultural_anchors[]` is present, every entry MUST have a non-empty `anchors_property` field. If any entry is missing the property, HARD-FAIL both at build time (Phase 7.9) and export time (startup). An anchor without a named property is decoration — the plugin does not produce decoration.

## Tier 1 is external-facing (principle)

Every Tier 1 artifact reaches readers who have no context about this plugin. Write for that reader.

Before writing a Tier 1 file, read the draft as an outside designer, consultant, or developer encountering the brand for the first time. Anything in the content (prose, table labels, code comments that ship visible, link text) that only makes sense to someone who has been inside the plugin's workflow gets rewritten in end-user language. Concretely:

- **Don't reference the plugin's internal structure**: skill names, slash commands, file paths inside the plugin tree, "contracts" / "registries" / "expected paths" / "system floors" / phase numbers.
- **Don't expose build-time status vocabulary**: PASS / WARN / FAIL tallies, "hard-fail", "auto-compose", "soft-skip", "floor validation" are process labels, not reader concepts.
- **Don't narrate the plugin or the build**: phrases like "the plugin emits", "this version", "retrofit", or version-tagged artifact-set names do not belong in output that ships.
- **Use end-user nouns**: "brand guidelines", "design tokens", "typography scale", "color role", "governance policy". If a sentence still reads like an internal handoff, rewrite.

Tier 2 (operator / process-record) may reference the workflow in plain prose — "this brand system was built through discovery, synthesis, and export" is fine — but keep vocabulary end-user friendly. Tier 3 follows the brand.md spec and is machine-formatted.

This principle is enforced by author judgment and review, not by regex — regex denylists false-positive on prose and miss variant phrasings. When editing or reviewing a Tier 1 template or its output, assume the reader has never heard of this plugin.

## Tier-3 conformance (brand.md + brand.extensions.yaml)

The Tier 3 output must conform to the brand.md v0.2.0 specification:

- `brand.md` has YAML frontmatter with required keys (`name`, `tagline`, `version`, `language`) and 12 required sections across Strategy (Overview, Positioning, Personality, Promise, Guardrails), Voice (Identity, Tagline & Slogans, Message Pillars, Phrases, Tonal Rules), and Visual (Colors, Typography).
- `brand.extensions.yaml` has a `sibling_of: "./brand.md"` pointer back to the canonical Tier 3 file, and plugin-specific structured rules (tone_matrix, output_constraints, vocabulary with replacements, refusal_triggers, visual_language details, cultural_anchors with properties, platforms, governance, self_validation).
- Both files are emitted to the output folder root (alongside `brand-guidelines.html`).
- Both are exempt from the Tier 1 denylist — they're machine-readable artifacts by design.

## Cross-artifact token-name consistency (universal)

Every token name that appears in `tokens.json` `semantic.{light,dark}.color.*` MUST appear with the exact same string in every cross-reference: `design-system.yaml`, `brand-quickref.md`, `brand-guidelines.html`, `brand.md`, `brand.extensions.yaml`, and `playground.html`. The canonical names are defined in `assets/platform-matrix-template.md` §1. The compliance checklist in `brand-export/SKILL.md` (gate 4) verifies consistency on every artifact.

If a sibling artifact uses a different string for the same role after render, the compliance checklist fails and the artifact gets one auto-fix pass (re-render from template). If the inconsistency persists, log the failure and surface to the user — do NOT ship inconsistent token names across sibling artifacts. The whole purpose of the canonical vocabulary is that any team can read any artifact and find the same slot names in the same places.

Brand-specific poetic names (signature gradients, named motion easings, motifs) live in `extensions.*` per `assets/platform-matrix-template.md` §6 — never as replacements for core role names.

## Render sequence

Export runs in this order:

1. Load the data contract (`build-export-contract.md`).
2. Walk Required paths; hard-fail at startup on any missing.
3. Apply input-path normalization in-memory.
4. Render Tier 1 artifacts one at a time. Before each write, review the draft against the external-facing principle above.
5. Render Tier 2 artifacts (brand-methods.html + .pdf, synthesis-report.md).
6. Render Tier 3 (`brand.md` + `brand.extensions.yaml`); validate against the brand.md v0.2.0 schema.
7. Run the verification checklist (`assets/export-verification-checklist.md`); hard-fail on any RED gate.
8. Write the verification report into `_build/export-verification.md` (not shipped to user-facing folder).
