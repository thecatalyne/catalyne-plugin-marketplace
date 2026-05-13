# Build → Export Data Contract

Canonical schema for the `brand-identity.yaml` `system.*` tree that flows from `brand-build` to `brand-export`. Both skills reference this file. Fields are classified by enforcement:

- **Required**: must be present with valid content. `brand-build` hard-fails on Phase 8 self-verify if missing. `brand-export` hard-fails at startup if missing.
- **Optional**: export soft-skips the rendered section if missing; no build hard-fail.

---

## Meta fields

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `meta.brand_name` | string (≥1 char) | Required | Drives cover, ledger, section summaries |
| `meta.tagline` | string | Required | Renders under H1 in `brand.md`; one-liner |
| `meta.version` | integer | Required | Starts at 1; increments per published revision |
| `meta.generated` | ISO date | Required | Written at `system.last_built` time |
| `meta.architecture` | enum | Optional | `branded-house` (default) / `endorsed` / `sub-brand` / `independent` |

## System status

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.status` | enum (`draft` / `review` / `complete`) | Required | Set by brand-build Phase 9 |
| `system.last_built` | ISO timestamp | Required | UTC |

## Personality

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.personality.synthesis` | string (5–25 words) | Required | One-sentence summary |
| `system.personality.character` | string (40–70 words) | **Required** | Narrative texture — "what does this brand feel like in a room?" |
| `system.personality.archetype_primary` | string | Required | Archetype label |
| `system.personality.archetype_blend` | string | Optional | Secondary archetype |
| `system.personality.triad.{product, brand, client}` | object | Optional | Three archetypes for product/brand/client |
| `system.personality.keywords[]` | string[] (3–5) | Optional | Earlier discovery field. If populated, export does not render as a standalone row — consumers should derive texture from `character` + `archetype_in_action[]`. Dead-field candidate (see Dead fields section below). |
| `system.personality.aaker_scores` | object (5 floats 0–10) | Optional | Omit entirely if not run — NEVER zero-fill |
| `system.personality.archetype_in_action[]` | object[] (≥3) | **Required** | Each: `{context, text}` — worked examples of archetype in copy |
| `system.personality.do_dont` | object | **Required** | `{do: string[]≥3, dont: string[]≥3}` — voice exemplars |

## Principles

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.principles[]` | array (3–7 items) | Required | Each: `{name, rationale_short≤30w, rationale, sources[]}` |

## Color

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.color.palette.core[]` | array (3–12) | Required | Each: `{role, name, hex, usage, percent?}` |
| `system.color.palette.anchors[]` | array | Optional | Named hexes distinct from roles |
| `system.color.palette.scales[]` | array (≥1) | Required | Each: `{name, family, hex_steps[10]}` |
| `system.color.palette.expressions[]` | array | Optional | Each: `{name, anchors[], spectral_range?, when_to_use}` |
| `system.color.palette.gradients[]` | array | Optional | Each: `{name, slug, direction, stops[], description?}` |
| `system.color.contrast_pairs[]` | array (≥1) | Required | Each: `{fg, bg, ratio, rating: AAA/AA/FAIL}` |
| `system.color.roles[]` | array (≥8) | **Required** | Each: `{role, token, hex, when_to_use, dont_use_for}` — drives Color Role Playbook section |
| `system.semantic.affirm_color` | hex | Optional | Fallback chain: YAML explicit → expression intent → hue-match 150–200° → `#16A34A` |
| `system.semantic.warn_color` | hex | Optional | Fallback chain: YAML explicit → expression intent → hue-match 0–30° → `#DC2626` |

## Typography

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.typography.heading.primary` | object | Required | `{family, weight_preference, source: {type, url, license}}` |
| `system.typography.heading.character` | string (taxonomy slug) | **Required** | From `skills/design-system/references/typography-taxonomy.md` |
| `system.typography.heading.alternatives[]` | string[] | **Required** | Ordered fallback chain, platform-agnostic |
| `system.typography.body.primary` | object | Required | Same shape as heading |
| `system.typography.body.character` | string | **Required** | Taxonomy slug |
| `system.typography.body.alternatives[]` | string[] | **Required** | Ordered fallback chain |
| `system.typography.display` | object | Optional | For extreme headlines |
| `system.typography.mono` | object | Optional | Monospace slot |
| `system.typography.scale.ratio` | float (1.0–2.0) | Required | Modular scale ratio |
| `system.typography.scale.sizes[11]` | number[] | Required | Concrete sizes |
| `system.typography.sample_text` | object | Required | `{display, h1, h2, h3, body, small}` — each ≥10 chars (body ≥20) |
| `system.typography.per_platform.{slug}` | object | **Required** | Per platform: `{heading_chain[], body_chain[], heading_weight_used, body_weight_used, rationale}` — populated by brand-build from `platform-fonts.yaml` via substitution rules (see below) |

### Typography substitution rules (enforced by brand-build)

1. **R1 — primary first**: the brand's primary family is always index 0 of the chain when the platform accepts it (custom upload, or the primary is natively available).
2. **R2 — no collapse**: `heading_chain[1]` (the first non-primary fallback) MUST NOT equal `body.primary.family` when a character-appropriate alternative exists on that platform. Prevents the "Inter-everywhere" silent collapse.
3. **R3 — weight-preference match**: prefer fonts with exact `weight_preference` match over fonts whose nearest weight is further away.
4. **R4 — licensing fallback**: if the platform doesn't support custom upload AND the primary isn't in the platform's native list, skip the primary entry and start the chain from the character-compatible native candidates.
5. **R5 — always terminate safely**: every chain ends with a system-safe fallback (`Arial` for sans, `Georgia` for serif, `Menlo`/`monospace` for mono) so rendering never breaks.
6. **R6 — single-family exception**: if `heading.primary.family == body.primary.family` AND `heading.character == body.character`, the brand has deliberately chosen one family throughout. R2 does not apply. Note in rationale.

## Form language

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.form.radius_interactive` | px or rem | Required | Buttons, inputs |
| `system.form.radius_card` | px or rem | Required | Larger containers |
| `system.form.shadow` | CSS shadow string | Required | Default elevation |
| `system.form.character` | string (2–10 words) | Required | Evocative phrase |
| `system.form.motifs[]` | array | Optional | Each: `{name, description, svg_hint?, asset_path?}` |
| `system.motif` | object | Optional | Hero motif used in `#in-practice` |

## Voice

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.voice.formality.home` | number | Required | On the scale the brand chose |
| `system.voice.formality.scale_max` | number | Required | Preserve source scale (do NOT rescale to /10) |
| `system.voice.formality.range` | number[2] | Required | `[min, max]` — acceptable variance |
| `system.voice.vocabulary.never_say[]` | array | Optional | Each: `{word, reason}` |
| `system.voice.vocabulary.specificity_test` | object | Optional | `{rule, pass_examples[], fail_examples[]}` |
| `system.voice.vocabulary.card_sort` | object | Optional | `{sounds_like_us[], doesnt_sound_like_us[]}` |
| `system.voice.banned[]` | array (≥5) | Optional | Each: `{word, replacement, reason}` |
| `system.voice.card_sort[]` | array (≥4) | Optional | Each: `{scenario, on_brand, off_brand, why}` |
| `system.voice.tone_matrix[]` | array | Optional | Each: `{state, register, posture, example}` |

## Section summaries

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.section_summaries.{slug}` | string (15–50 words) | **Required** | Keys: `foundation, identity, color, typography, visual_language, spacing, components, voice, platforms, governance, llm_manual, quickref`. Each is the brand-specific answer for one section. Universal definition copy lives in the template, not here. |

## Visual language

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.visual_language.form_primitives[]` | array | Optional | Each: `{name, construction, stroke_range_px}` |
| `system.visual_language.form_primitives_forbidden[]` | array | Optional |  |
| `system.visual_language.curvature_rationale` | string | Optional | One sentence |
| `system.visual_language.composition_archetypes[]` | array | Optional | Each: `{name, trigger, layout_description, visual_weight_ratio}` |
| `system.visual_language.elevation_levels[]` | array | Optional | Each: `{level, class, shadow_token, component_examples[]}` |
| `system.visual_language.translucency` | object | Optional | `{allowed, reason}` |
| `system.visual_language.texture_material` | object | Optional | `{adjectives[], digital_translation, anti_patterns[]}` |
| `system.visual_language.motion` | object | Optional | `{principles[], motion_tokens}` |
| `system.visual_language.gradients` | object | Optional | `{policy, rule?, allowed_contexts[], forbidden_contexts[]}` |
| `system.visual_language.motif_library[]` | array | Optional | Each: `{name, definition, when, anti_use}` |
| `system.visual_language.motif_grammar` | object | Optional |  |
| `system.visual_language.photography` | object | Optional | `{subject_rules[], lighting, crop, post, reference_bank[], counter_bank[]}` |
| `system.visual_language.illustration` | object | Optional | `{shape_vocabulary[], stroke_px_range, perspective, palette_constraint, emotion_inventory[], cultural_anchors[]}` |
| `system.visual_language.spatial_3d` | object | Optional | `{policy, rules[]}` |

## Platforms

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.platforms[]` | array (≥1) | **Required** | Each: `{slug, name?, font_chain_heading[], font_chain_body[], color_slots?, template_url?, export_profile, probe_notes[], caveats[]}`. Default target set: `[web_app, google_slides, figma, pitch, keynote, canva_free, email_html]`. Derived from `typography.per_platform.*` + `platform-fonts.yaml` slots. |

## Governance

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.governance.owner.name` | string | **Required** | Full name or preferred attribution string — NOT email-inferred |
| `system.governance.owner.email` | string | Optional | Separate from name |
| `system.governance.version` | semver string | Optional | e.g. `"1.0.0"` |
| `system.governance.semver_triggers` | object | Optional | Major/minor/patch rules |
| `system.governance.deprecation_window_min_days` | integer | Optional | Default 90 |
| `system.governance.changelog[]` | array | Optional | Each: `{version, date, notes}` |
| `system.governance.adrs[]` | array (≥3 if present) | Optional | Each: `{id, title, status, decision, consequences}` |
| `system.governance.contribution_flow` | string | Optional | Plain prose |

## Cultural anchors

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.cultural_anchors[]` | array | Optional | Each: `{anchor, anchors_property}` — **`anchors_property` is required on every entry if the array is present** (no vapor anchors). Hard-fail if present-but-empty. |

## Quotes (round-trip wiring)

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.techniques[].quotes[]` | array | Optional | Per-technique quotes from `{name}-brand-quotes.md`. Each: `{speaker, context, text}`. Synthesize populates; export renders in `brand-methods-template.html` technique blocks. |

## Quality

| Field | Type | Enforcement | Notes |
|---|---|---|---|
| `system.quality.coherence_score` | integer (6–30) | Optional | Omit if not scored |
| `system.quality.coherence_notes` | string | Optional | Interpretation |
| `system.quality.rand_seven` | object | Optional | 7 dimensions 0–10, total 0–70 |
| `system.quality.build_verification` | object | Required | `{timestamp, summary, acceptance, auto_fix_passes}` |
| `system.quality.export_verification` | object | Optional | Populated after `brand-export` verification (Step D). `{timestamp, summary, acceptance, auto_fix_passes, normalizations_applied}` |
| `system.quality.export_log[]` | array | **Required** | Per-artifact render + structural-validation log. Populated by `brand-export` after each render (and initialized to `[]` by `brand-build` Phase 9 if absent). See schema below. |

### `system.quality.export_log[]` schema

Per-artifact append-only log. The **last entry** per `artifact` slug is the authoritative state — the skill reads this at startup to build the resume table and decide what needs re-rendering.

```yaml
system:
  quality:
    export_log:
      - artifact: "brand-guidelines.html"        # canonical slug (matches artifact-schemas.yaml key where possible)
        status: "rendered"                        # rendered | failed | skipped
        last_exported: "2026-04-23T12:34:56Z"     # ISO-8601 UTC, time of successful Write
        structural_check: "pass"                  # pass | fail | not_applicable
        auto_fix_attempted: false                 # true if Step S triggered a one-shot re-render
        structural_check_after_fix: null          # pass | fail | null (null if no auto-fix ran)
        verified_at: "2026-04-23T12:34:58Z"       # time the validator emitted its verdict
        bundle: "core"                            # bundle name the artifact was rendered under (core | pdfs | companions | methods | synthesis | llm | <single>)
```

**Field semantics**:

- `status`: `rendered` = file written to disk; `failed` = write attempted but errored (file may or may not exist); `skipped` = user declined in the resume prompt.
- `structural_check`: result of `validate-structure.py`. `not_applicable` when the artifact has no oracle entry (rare).
- `auto_fix_attempted`: `true` ONLY if `structural_check: fail` triggered the single re-render pass inside Step S. False otherwise (including when the initial check passed).
- `structural_check_after_fix`: outcome of the re-validation after the auto-fix re-render. `null` when `auto_fix_attempted: false`.
- `bundle`: which bundle argument the artifact rendered under. Useful for the summary + resume logic.

**Append semantics**: one entry appended per render attempt. For re-renders of the same artifact in later sessions, the old entries remain (as an audit trail) and the new entry becomes the authoritative state. Skills SHOULD read the last entry per `artifact` slug; they MAY prune old entries if the log grows unbounded, but default is keep-all.

**No direct user editing**: the log is managed by `brand-export` and `brand-build`. Users who want to force a re-render should use `/brand-export {bundle}` with the bundle's rebuild option rather than editing this log manually.

---

## Dead fields to prune

These fields persist in brand-identity.yaml but export never reads. Build should stop writing them (or demote to `_meta.*`):

- `system.personality.keywords[]` — earlier discovery field. Build no longer writes it as a required output; if present in an incoming YAML, normalize in-memory (do not strip source). Replaced in Tier 1 renders by `personality.character` + `archetype_in_action[]`.
- `meta.phase` — not consumed by export
- `synthesis.*` — persists in full; compress or move to sibling `synthesis.yaml` after build completes
- `discovery.{name}.techniques_used[]` — not consumed downstream

---

## Enforcement flow

### brand-build (Phase 8 self-verify)

1. Load this contract.
2. For every Required field, confirm presence and type/shape.
3. Apply auto-fix playbook (see `build-phases.md`) for any FAIL; one pass only.
4. Report `{PASS, WARN, FAIL}` counts; block finalization if any FAIL remains.
5. Run the typography-substitution algorithm (R1–R6) over `system.platforms[]` × `platform-fonts.yaml` to populate `typography.per_platform.*`.

### brand-export (startup)

1. Load this contract.
2. Walk every Required path; hard-fail at startup if any missing. Fail message cites the specific field + contract section + "run brand-build to populate."
3. Apply input-path normalization (e.g., `palette` dict → `palette.core[]`).
4. Render. Soft-skip every Optional section whose data is empty. Never auto-compose a Required field at export time — that's brand-build's job. Review each Tier 1 draft against the external-facing principle in `rendering-rules.md` before writing.
5. Run `export-verification-checklist.md`; hard-fail on any red gate.

---

## Notes

- **No auto-compose at export time.** If the build didn't produce `personality.character`, `archetype_in_action[]`, `color.roles[]`, `section_summaries.*`, `typography.*.character`, `typography.*.alternatives[]`, `typography.per_platform.*`, `governance.owner.name`, or `platforms[]`, export HARD-FAILS. Don't paper over. The fix is to re-run brand-build.
- **Aaker zero-fill prevention**: if the Aaker technique wasn't run, omit `personality.aaker_scores` entirely — do not write zeros.
- **Voice constraint shape preservation**: keep `never_say[]`, `specificity_test{}`, `card_sort{}` in their source shape. Do not coerce into a single "prefer / avoid" list.
- **Cultural anchor vapor check**: if `cultural_anchors[]` exists, every entry's `anchors_property` must be non-empty. Hard-fail otherwise. Applies at both build and export.
