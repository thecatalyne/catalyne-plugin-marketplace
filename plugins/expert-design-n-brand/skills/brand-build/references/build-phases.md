# Build Phases — Full Procedure

Loaded by `brand-build/SKILL.md` during design system generation. Contains the detailed step-by-step procedure for each of the nine build phases, plus the YAML shape self-verification protocol.

Read sections on demand — not every build runs every phase's expanded guidance. Phases execute in numeric order: 1 → 2 → 3 → 3B → 4 → 5 → 6 → 7 → 7.5 → 7.6 → 7.7 → 7.8 → 7.9 → 8 → 9.

## Phase 1: Extract Brand Parameters

From synthesis consensus (or solo discovery), extract:

### Personality profile

Use whichever source(s) are available, in this order:

- If Aaker sliders were run, use the direct scores.
- Else if archetype was selected, derive a personality characterization from the archetype (do not fabricate 1–10 Aaker numbers unless the registry declares the inference).
- Else if tension-spectrum-mapping was run, use the axes + scores.
- Do NOT zero-fill Aaker when it wasn't run. Omit `system.personality.aaker_scores` entirely in that case — the ledger will mark Aaker as "—".

### Personality synthesis sentence

Compose a single sentence capturing the personality in plain language and write it to `system.personality.synthesis`. This sentence appears verbatim in `design-system.html#personality` (the canonical surface) as the opening prose before the archetype / Aaker / keyword rows.

Source priority:

1. If the user has pre-authored `system.personality.synthesis`, preserve it — do not overwrite.
2. Otherwise auto-compose from: primary + secondary archetype (and self-typed blend if present), top-scoring Aaker dimension name, and first 3 entries of `system.personality.keywords[]`. Template: `"{brand_name} is a {primary}-{secondary} brand with high {top_aaker_dim}{ — {keyword_list}}."` — single sentence, no purple prose, no hedging.
3. If neither archetype nor Aaker was run, fall back to a keyword-only sentence: `"{brand_name}'s personality: {keyword_1}, {keyword_2}, {keyword_3}."`

Brand-export will emit this sentence directly; keep it under 25 words.

### Archetype character paragraph

Compose a short character paragraph (~40–70 words) and write it to `system.personality.character`. This sits beneath the synthesis sentence in `design-system.html#personality` and gives canonical readers the texture that the taxonomy labels miss — the human thread behind the archetype.

Example pattern (generic): *"Think {primary-archetype}-{secondary-archetype} with a {modifier} edge: the {character-noun} who {distinctive-verb-phrase}. {Named-reference-A}, not {Named-reference-B}. The {role-metaphor} who {concrete-behavior-1}, {concrete-behavior-2}, and {concrete-behavior-3}."* — concretize the archetype pairing, borrow cultural reference points the brand resonates with, then name three concrete behaviors rather than abstractions.

Source priority:

1. Pre-authored `system.personality.character` → preserve.
2. Else compose from: primary archetype's core trait, secondary archetype's modifier, and the most evocative metaphor from `personality.metaphors[]` if run. Keep concrete — name the character thread, don't generalize.
3. If neither archetype nor metaphors ran, omit the field (do not fabricate character). Brand-export will soft-skip the subblock.

Keep the character paragraph distinct from the synthesis sentence: synthesis is the taxonomic summary, character is the human thread. Both render; they're not redundant.

### Section summaries

For each canonical design-system section (`foundation, identity, color, typography, visual_language, spacing, components, voice, platforms, governance, llm_manual, quickref`), populate `system.section_summaries.{slug}` with a single brand-specific paragraph. The rendered doc pairs a fixed definition paragraph ("what this section IS in a brand system") with this summary paragraph ("what THIS brand's answer is"). Keep each summary 15–50 words; name concrete brand-level choices rather than abstractions. This field is Required-v6 — if missing, brand-export HARD-FAILS at startup (see `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/build-export-contract.md`). Do not leave empty and do not rely on export-time fallback; the fix for a missing summary is to compose one here.

### Semantic theme colors

Populate `system.semantic.affirm_color` and `system.semantic.warn_color` (and optionally `success_color`, `warning_color`, `danger_color`) from the brand's palette. Affirm is the brand's "this is us" positive accent (commonly an active / signal hex); warn is the brand's "don't do this" accent (commonly a warm / ignition hex).

Resolution priority: pre-authored → expressions tagged `intent: affirm|warn` → hue-matched anchor (affirm = 150–200°, warn = 0–30°) → omit (brand-export falls back to neutral green/red). Do-not-hardcode stock greens and reds anywhere else in the system; every rendered Do/Don't pair routes through these two tokens.

### Visual preferences

- Color: resonating palettes, rejected palettes, reasoning
- Typography: formality, warmth, liked pairings
- Form language: geometric / organic / mixed
- Mood references, anti-inspiration, texture/material (each optional per registry)

### Voice parameters (polymorphic — see `concepts.voice_constraints` in registry)

- Formality: `formality_score` on `formality_scale_max` (carry the original scale; do not rescale to /10)
- Voice constraints: any combination of `never_say_words`, `specificity_test`, `voice_card_sort.sounds_like_us / doesnt_sound_like_us` — each rendered as a distinct concept-slot subblock downstream. Preserve the raw shape; do NOT coerce into a single prefer/avoid list.

## Phase 2: Generate Design Principles

Create 3–7 design principles (not a fixed number — go with what the brand evidence supports). Each principle:

- Has a short, memorable name (2-4 words)
- Has `rationale_short`: one italicized sentence, used in the primary render of the design system doc (e.g., *"Competence 8. Caretaker's promise is replacing pitch-deck promises with verifiable market data."*)
- Has `rationale`: the full paragraph, used in the appendix
- Has `sources[]`: which discovery/synthesis signals produced this principle (e.g. `[archetypes, aaker.competence, tensions.evidence-first]`)

Process:

1. Map dominant personality signals to design approaches (using design-rules.md tables). Use whichever personality instrument was run (Aaker, archetype, tensions).
2. Identify principles that trace back to specific signals; don't invent ones for dimensions that had no data.
3. Check for consistency: do the principles tell a coherent story together?

Write to `system.principles[]`. Variable-N: render as many rows as are justified, not a hardcoded 5.

## Phase 3: Generate Color Palette

1. Start from the resonating palettes identified in discovery.
2. Select or blend a **variable-N palette** (any number of roles, typically 3–9). Populate `system.color.palette.core[]` with one entry per role, each with `{role, name, hex, usage, percent?}`. Use industry-standard role names where possible: `background`, `surface`, `primary`, `neutral`, `accent`, `secondary`, `success`, `warning`, `error`, `info`. Do NOT force a fixed 4-role shape. (Legacy `anchor` is auto-normalized to `neutral` by Phase 3B.)
3. If the brand has multiple visual expressions (e.g. a named signature motif, a secondary decorative treatment, or a named gradient family), populate `system.color.palette.expressions[]` — each entry is `{name, anchors[{name,hex}], spectral_range?, when_to_use, gradient_ref?}`. Otherwise leave the array empty.
4. Generate full 10-step scales for each non-neutral role using HSL lightness progression. Populate `system.color.palette.scales[]` with entries of shape `{name, family, hex_steps[10], description?}`. (Legacy callers may still see `system.color.scales.{family}` — see Phase 3B normalizer.)
5. Generate a neutral scale from the background color's temperature.
6. Define gradients if appropriate (check personality signal: high sophistication or excitement → gradients; high ruggedness → no gradients). Populate `system.color.palette.gradients[]` — each entry is `{name, slug, direction, stops[{color, position}], description?, usage?}`. brand-export emits each as `--gradient-{slug}` and renders a labeled strip.
7. **Populate `palette.anchors[]`** if the brand has named anchor hexes distinct from its functional roles. Each anchor is `{name, hex, usage, family?}`. Useful for rich brands whose named anchor set exceeds their functional role count (e.g. 8–10 named hexes vs. 3–4 roles) — both render, each in its own subsection of the Color section.
8. **Validate contrast**: Run all foreground/background combinations through WCAG checks. Use `${CLAUDE_PLUGIN_ROOT}/scripts/validate-contrast.sh`. Store each pairing in `system.color.contrast_pairs[]` with `{fg, bg, ratio, rating}` where rating is `AAA | AA | FAIL`. This drives the contrast-badge rendering in design-system HTML.

Write to `system.color`.

## Phase 3B: Normalize Legacy Palette Shapes

If the YAML already contains legacy or loose palette paths (from older builds or manual editing), consolidate them into the canonical `palette.*` structure BEFORE writing Phase 3 output. This makes re-runs idempotent and eliminates the WARN §1.1 "palette shape mismatch" category at export time. Preserve legacy paths in place — do not delete them — so downstream tooling that depends on older shapes continues to work.

Normalization rules:

1. **4-role palette object → `palette.core[]`**. If `system.color.palette` is an object with keys like `{background, primary, anchor, accent, ...}` (or the canonical `{background, primary, neutral, accent, ...}`) rather than a `core[]` array, promote each key into a `palette.core[]` entry: `{role: <key>, name: <key.name or titlecased>, hex: <key.hex>, usage: <key.usage>}`. Keep the object in place (non-breaking for legacy readers) AND write the new array alongside.

   **Legacy role-name normalization**: When promoting, also rewrite legacy role names to canonical: `anchor` → `neutral` in the `role` field of the new `palette.core[]` entry. The legacy object key stays as-is for backward compat; only the canonical array gets the new vocabulary.

2. **Flat `system.color.anchors` (dict or list of named hexes) → `palette.anchors[]`**. Common legacy shape: `anchors: {ink_navy: {hex: '#112233', name: 'Ink Navy', usage: 'primary text'}, ...}`. Each anchor becomes `{name, hex, usage, family}` in `palette.anchors[]`. Where an anchor's role is inferrable (e.g. most-used on backgrounds → role `background`), also include it in `palette.core[]`.

3. **`system.color.flourish_system` dict → `palette.expressions[]`**. Each expression dict (e.g. `flame: {anchors: [...], spectral_range: '...', when_to_use: '...'}`) becomes an array entry `{name: 'Flame', anchors: [...], spectral_range, when_to_use}`.

4. **`system.color.gradients[]` at `system.color.*` (non-canonical location) → `palette.gradients[]`**. Move each gradient into the canonical array with the new sub-schema `{name, slug, direction, stops[{color, position}], description, usage}`. If the legacy shape was a simple CSS string (e.g. `"135deg, #FBBF24, #F59E0B"`), parse it into the structured form.

5. **`system.color.scales.{family}.{step}` → `palette.scales[]`**. Collect each family's 10 steps into an array entry `{name: '<family_title>', family: <family_key>, hex_steps: [50, 100, ..., 900]}`. **Family-name normalization**: rewrite legacy `anchor` → `neutral` in both `name` and `family` fields. The legacy `system.color.scales.anchor.*` paths stay in place.

6. **Legacy token-naming normalization (token-level)**. When emitting `tokens.json`:
   - `primitive.color.scales.anchor` → `primitive.color.scales.neutral`
   - `primitive.color.palette.anchor` → `primitive.color.palette.neutral`
   - `fontWeight.{default-heading,default-body,emphasis,strong,flourish}` → `fontWeight.{light,regular,medium,semibold,bold}`
   - `shadow.{default,elevated,glow}` → `shadow.{sm,md,lg}` (and `glow` moves to `extensions.color.flourish-glow`)
   - `motion.easing.{default,spark}` → `motion.easing.{standard,spring}` (and `spark` is also exposed as `extensions.motion.easing.spark`)
   - `letterSpacing.loose-eyebrow` → `letterSpacing.wide`
   - `lineHeight.default` → `lineHeight.normal`
   These rewrites happen in-memory at export time. They do NOT modify `brand-identity.yaml`.

After normalization, the YAML is a superset: every canonical path is populated, every legacy path preserved. brand-export prefers canonical paths when both exist.

## Phase 4: Generate Typography Scale

1. Select typefaces:
   - Match to personality profile using curated-option-sets pairings as starting points.
   - If discovery identified specific pairings, use those.
   - Include fallback stacks for web safety.
2. Choose modular scale ratio (from design-rules.md, mapped to personality). Store scale `name` (e.g. "Major Third") AND `ratio` (1.250) — the name is used in the cover ledger.
3. Generate full size scale from base size (typically 16px) using the ratio.
4. Define weights, line heights, and letter spacing for each size step.
5. Populate `system.typography.sample_text{display, h1, h2, h3, body, small}` with brand-relevant specimens. Fallback chain, in order: a hand-picked phrase from voice guidelines → `positioning.elevator_pitch` clause → `voice.sample_celebration` → `voice.sample_apology` → "The quick brown fox jumps over the lazy dog." Do NOT leave blank — exports render these as the type specimen.

Write to `system.typography`.

## Phase 5: Generate Form Language

1. Set border radius scale based on form language preference (geometric → sharp, organic → rounded). Write `system.form.radius_interactive` and `system.form.radius_card` explicitly (the quickref renders both).
2. Define shadow style (from design-rules.md mapping). Write `system.form.shadow`.
3. Populate `system.form.character` — a single line that evokes the form in one breath ("spark motif", "quiet arches", "teal bar accents"). Used in the quickref and design-system cover.
4. Identify motifs from discovery visual preferences. Write `system.form.motifs[]` for detail; if the brand has a signature hero-worthy motif, populate `system.motif{name, description, svg_hint?, asset_path?}` so exports can render the motif panel.
5. Define composition rules (layout density, hierarchy model, spacing scale).

Write to `system.form` and `system.motif`.

## Phase 6: Generate Voice Guidelines

1. Before generating voice content, read all `*-brand-quotes.md` files in the working directory. These contain the exact language, metaphors, and phrasing team members used during discovery — the raw material for authentic voice guidelines.
2. Set formality — write BOTH `system.voice.formality_score` and `system.voice.formality_scale_max` (don't rescale; carry the original instrument's scale).
3. **Voice constraints are polymorphic.** The `concepts.voice_constraints` group in the registry says any of never-say-list / specificity-test / voice-card-sort can fill this slot, and multiples stack. Populate `system.voice.vocabulary` with whatever the team actually produced:
   - If participants wrote never-say lists → `vocabulary.never_say[]`.
   - If Brennan-style specificity-test → `vocabulary.specificity_test.{rule, pass_examples[], fail_examples[]}`.
   - If voice-card-sort → `vocabulary.card_sort.{sounds_like_us[], doesnt_sound_like_us[]}`.
   - Do NOT collapse these into a single `prefer`/`avoid` pair — each technique's shape carries signal that the single-pair collapse destroys. Leave `prefer[]`/`avoid[]` empty unless the team explicitly produced those lists.
4. Write specific guidelines with examples — do's and don'ts. For "do" examples, use actual participant quotes from the quotes files wherever possible. Real language is more instructive than fabricated samples.

Write to `system.voice`.

## Phase 7: Quality Check

Run the design system coherence framework from scoring-criteria.md. Each item is scored 1–5; sum the first six for the coherence score out of 30 (range 6–30 — the framework reserves 0 for "not applicable / not scored," in which case omit the item rather than counting it).

1. Color-personality alignment
2. Typography-voice alignment
3. Form-energy alignment
4. Voice-visual harmony
5. Token completeness
6. Decision support

Flag any dimension scoring below 3. Adjust before finalizing.

Write the result to `system.quality.coherence_score` and `system.quality.coherence_notes`. If you also scored against Paul Rand's 7 criteria, populate `system.quality.rand_seven.{distinctive, memorable, simple, appropriate, timeless, legible, reducible_to_essence, total}` (each 0–10, sum max 70). Rand's 7 is optional — skip the field entirely if you did not score it, and the design-system export will soft-skip the section.

## Phase 7.5: Visual Language Craft (v6)

Emit the visual-language fields that brand-export will render into `brand-guidelines.html` (§5 Visual Language) and into `brand.extensions.yaml` (structured rules for LLM consumption). Each sub-block is derived from existing synthesis/discovery data — no new elicitation required.

Write to `system.visual_language`:

1. **Form primitives** (`.form_primitives[]`) — From `form_language` preference, name 3–5 primitives with construction math (radius, stroke, geometry). Each primitive: `{name, construction, stroke_range_px}`. Also emit `.form_primitives_forbidden[]` with ≥ 3 opposites.
2. **Curvature rationale** (`.curvature_rationale`) — one sentence explaining why this radius/stroke range fits the personality.
3. **Composition archetypes** (`.composition_archetypes[]`) — From personality + density preference, name 3–5 hero patterns. Each: `{name, trigger, layout_description, visual_weight_ratio}`.
4. **Elevation levels** (`.elevation_levels[]`) — 4–6 semantic levels bound to component classes (`0-flat`, `1-card`, `2-modal`, `3-flourish`). Each maps to a shadow token from `system.form_language.shadow`.
5. **Translucency policy** (`.translucency`) — `{allowed: bool, reason: str}`. Matte/paper material → forbidden; glass/tech material → allowed.
6. **Texture & material** (`.texture_material`) — Name 1–3 physical anchors from discovery mood board. Emit: `adjectives[]`, `digital_translation{}`, `anti_patterns[]`.
7. **Motion principles** (`.motion`) — 3 principles from personality (meaningful vs decorative, purposeful springs, reduced-motion fallback). Also emit `.motion_tokens{}` (ease-default, ease-spark, duration-instant/fast/normal/slow).
8. **Gradient policy** (`.gradients`) — `{policy: "generation-rule-based" | "forbidden", rule?: str, reason?: str, allowed_contexts[], forbidden_contexts[]}`.
9. **Motif library** (`.motif_library[]`) — The brand's signature motifs from discovery. Each: `{name, definition, when, anti_use}`. Also emit `.motif_grammar` — which motifs can co-occur, which are mutually exclusive.
10. **Photography** (`.photography`) — `{subject_rules[], lighting{temp, direction}, crop, post, reference_bank[5_approved], counter_bank[5_rejected]}`.
11. **Illustration** (`.illustration`) — `{shape_vocabulary[], stroke_px_range, perspective, palette_constraint, emotion_inventory[≥4], cultural_anchors[≥3 each with anchors_property]}`.
12. **3D / spatial** (`.spatial_3d`) — `{policy: "not_used" | "used", rules[]}`. Most brands: `not_used`.

## Phase 7.6: Platform Entries (v6)

Write to `system.platforms[]`. Infer from typical set OR read from user-declared list: web, pitch, google-slides, figma, keynote, print, social-square, email.

For each entry: `{name, font_chain[], color_slots{}, template_url?, export_profile, probe_notes[], caveats[]}`.

- `font_chain[]` — from `system.typography.fontFamily` + web-safe fallbacks, preserving the weight-hierarchy invariant (heading lighter OR heavier than body — whichever the brand chose).
- `color_slots{}` — if platform has a slot-limited palette (Pitch: 4 slots; Slides: 10), map brand's core roles to slots.
- `template_url` — populate only if user has provided one. Else `TBD`.
- `probe_notes[]` — populate only if user has actively used the platform and documented gotchas. Else empty.
- `caveats[]` — known limitations (e.g., "custom fonts require plan upgrade on Pitch free tier").

## Phase 7.7: Voice Expansions (v6)

Extend `system.voice` with v6 structures (additive — does not replace v5 voice fields):

- `voice.banned[]` — each entry `{word, replacement, reason}`. Migrate existing never-say list items into this structure, explicitly assigning a replacement for each. Minimum ≥ 5 entries for a shipped brand.
- `voice.card_sort[]` — each entry `{scenario, on_brand, off_brand, why}`. Minimum ≥ 4 entries.
- `voice.tone_matrix[]` — each entry `{state, register, posture, example}`. `state` = audience emotional state (confused / celebrating / frustrated / exploring). `register` within `voice.formality` range.
- `voice.specificity_test` — if brand has a canonical voice gate, capture as `{rule, examples_pass[≥2], examples_fail[≥2]}`.

## Phase 7.8: Governance Scaffold (v6)

Write to `system.governance`:

- `owner` — brand steward (email or name).
- `version` — current semver.
- `semver_triggers{major, minor, patch}` — short text per level.
- `deprecation_window_min_days: 90` (default; can be extended).
- `changelog[]` — initialize with this build's entry `{version, date, notes}`.
- `adrs[]` — if any design decisions were made with notable trade-offs (e.g., "chose teal over amber as accent because..."), capture each as `{id, title, status, decision, consequences}`. ≥ 3 ADRs for a first-run brand (infer from synthesis trade-offs if not explicit).
- `contribution_flow` — proposal → review → promote.

## Phase 7.9: Cultural Anchors (v6)

Write to `system.cultural_anchors[]`. For every mood-board reference, anti-inspiration entry, or named cultural touchstone in discovery:

- `anchor` — the name (e.g., "Wabi-sabi pottery glaze", "Apothecary-shelf typography", "Mid-century Swiss signage")
- `anchors_property` — what exactly is being anchored (e.g., "flame + prismatic + indigo palette; magic-in-ordinary-moments tone"; "ink-on-warm-paper substrate, economy of stroke, negative space as content")

**Critical**: every cultural_anchor MUST name what property it anchors. No vapor references. A bare name without `anchors_property` fails verification.

## Phase 8: Self-Verification (Mandatory)

Before finalizing, walk the YAML-shape checks from the canonical checklist (`${CLAUDE_PLUGIN_ROOT}/assets/export-verification-checklist.md`) against the freshly-written `system` section. brand-build does not render visual artifacts, so visual sections (§5–§10) are skipped — but the *shape* of the YAML must be sound, because every downstream artifact depends on it.

### Sections to walk

- §1.1 (every `expected-paths.yaml → system_floor` path is populated)
- §2.3 (status assignments match ground truth — no zero-fill on Aaker when not run; Aaker block omitted entirely if not used)
- §3.1/§3.2 applied to YAML shape: voice constraints preserve their source technique's shape (never_say[] OR specificity_test{} OR card_sort{}), never collapsed into a single prefer/avoid pair
- §4 applied to YAML: `system.principles[]` has 3–7 entries (not padded); `system.color.palette.core[]` has the role count the brand actually needs; `system.color.palette.expressions[]` empty array allowed but must not be a placeholder string
- §11 applied to YAML: `system.quality.coherence_score` populated only if scoring actually happened; `system.quality.rand_seven` populated only if Rand was scored

### Additional brand-build-specific shape checks

- `system.typography.sample_text.{display, h1, h2, h3, body, small}` — every field must be populated using the documented fallback chain. No blank strings; no literal "{{ sample_h1 }}".
- `system.color.contrast_pairs[]` — non-empty; every text/background pair the design system can produce has a recorded `{fg, bg, ratio, rating}`.
- `system.principles[*].rationale_short` AND `rationale` — both fields populated; short form is one italicized sentence, long form is a paragraph.
- `system.form.character` — populated (one-line evocative phrase).

### Auto-fix policy

For each FAIL on first pass: apply the obvious shape fix — re-derive the value from synthesis/discovery data, walk the documented fallback chain, or strip the malformed block. Re-write the relevant YAML section. Re-run only the failed checks.

**Hard cap**: one auto-fix pass. If a check still fails, surface it with a specific recommended fix and stop.

### Reporting

Write `system.quality.build_verification` to the YAML with `{timestamp, summary: "PASS N · WARN N · FAIL N", acceptance, auto_fix_passes}`, and print the SUMMARY line + any STILL-FAILs inline.

If FAIL count > 0 after the auto-fix pass: tell the user the design system is **blocked** and list the specific fixes needed. Do not move to `/brand-export` until the build passes.

## Phase 9: Finalize

1. Set `system.status` to `draft`.
2. Set `system.last_built` to current timestamp.
3. Update `meta.phase` to `system`.
4. Add changelog entry.
5. **Initialize `system.quality.export_log: []`** if the key is absent. This is the per-artifact render log that `brand-export` appends to (see `build-export-contract.md → system.quality.export_log[] schema (v7)`). Do NOT populate entries here — brand-build only ensures the key exists so brand-export can read it without a null check.
6. Present the complete design system to the user as a summary:
   - Design principles (list)
   - Color palette (hex values with roles)
   - Typography (typefaces, scale ratio)
   - Form language (radius, shadow character)
   - Voice (formality, key guidelines)
   - Quality scores
   - Verification summary (PASS/WARN/FAIL counts)
7. Ask: "Does this feel right? Any adjustments before we finalize?"
