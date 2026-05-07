---
name: brand-build
description: "This skill should be used when the user asks to build a design system, generate design tokens, create the brand system, create brand guidelines, build a style guide, generate design foundations, or says \"brand-build\". It generates a complete design system from resolved brand synthesis."
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

Entry point for design system generation. Validate synthesis readiness, then conduct the full nine-phase build directly.

## Startup

1. Read `brand-identity.yaml` from the current working directory. If it doesn't exist, inform the user: "No brand identity file found. Run /brand-discover first."

2. Check prerequisites:
   - **Solo user path**: If there's only one discovery entry and it's `complete`, synthesis is optional. Offer: "You have one completed discovery. Would you like to build the design system directly from your responses, or run /brand-synthesize first for a consistency check?"
   - **Team path**: Check `synthesis.status`:
     - `not_started`: "Synthesis hasn't been run yet. Run /brand-synthesize first to compare team inputs."
     - `draft` with unresolved divergences: List the unresolved divergences. "There are {n} unresolved divergences. The design system can proceed with the current consensus, but unresolved items may need revisiting. Continue?"
     - `review` or `complete`: "Synthesis is ready. Proceed with design system generation?"

3. Check if a design system already exists:
   - If `system.status` is `draft` or higher: "A design system already exists (built {last_built}). Would you like to rebuild from scratch, or refine specific sections?"

## Builder Behavior

After confirmation, conduct the full design system build directly.

### Philosophy

Every design decision traces back to the brand identity. Nothing is arbitrary. The system should feel like the inevitable visual expression of who the brand is.

### Reference Loading (mandatory before building)

Load these before starting Phase 1:

- `${CLAUDE_PLUGIN_ROOT}/skills/brand-build/references/build-phases.md` — full procedure for every phase. This is the authoritative step-by-step; the phase list below is an index.
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/build-export-contract.md` — the canonical data contract. `brand-build` must populate every Required-atomic and Required-v6 field or Phase 8 verification blocks finalization.
- `${CLAUDE_PLUGIN_ROOT}/assets/techniques-registry.yaml` — technique → output-section mapping. Consult first to know which techniques each participant ran and which voice-constraint / personality-scoring slots have data.
- `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/token-architecture.md` — 3-layer token taxonomy
- `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/design-rules.md` — color, typography, spacing, motion rules
- `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/typography-taxonomy.md` — 12-category font-character taxonomy (required for Phase 4 to classify the brand's typefaces)
- `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/platform-fonts.yaml` — per-platform font availability knowledge base (required for Phase 7.6 substitution logic)
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/scoring-criteria.md` — quality evaluation framework
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/voice-component-patterns.md` — load during Phase 6 when generating voice guidelines.

### Build Phases — Index

Execute in order: 1 → 2 → 3 → 3B → 4 → 5 → 6 → 7 → 7.5 → 7.6 → 7.7 → 7.8 → 7.9 → 8 → 9. Full detail per phase lives in `references/build-phases.md` — open it before running each phase.

| Phase | What it does | Writes to |
|-------|--------------|-----------|
| **1** | Extract personality — synthesis sentence, **character paragraph (40–70 words, required)**, **archetype-in-action worked examples (≥3, required)**, **voice do/don't pairs (≥3 each, required)**, section summaries (12 slugs, each 15–50 brand-specific words), semantic theme colors from synthesis consensus. | `system.personality.*`, `system.section_summaries.*`, `system.semantic.*` |
| **2** | Generate 3–7 design principles, each with short italicized rationale + full rationale + source attribution. Variable-N; do not pad. | `system.principles[]` |
| **3** | Generate variable-N color palette (3–9 core roles, prefer industry-standard names: `background`, `primary`, `neutral`, `accent`, `secondary`, `success`/`warning`/`error`/`info`), 10-step scales per family, expressions, gradients, anchors. **Also populate `color.roles[]` (≥8 roles, each `{role, token, hex, when_to_use, dont_use_for}`) for the Color Role Playbook.** Validate contrast via `scripts/validate-contrast.sh`. | `system.color.*` |
| **3B** | Normalize legacy palette shapes (4-role object, flat anchors dict, flourish_system) AND legacy role/token names (`anchor`→`neutral`, `default-body`→`regular`, `flourish`→`bold`, `spark`→`spring`, etc.) into canonical `palette.{core,anchors,scales,expressions,gradients}[]` + canonical token vocabulary. Preserve legacy paths in YAML; canonical names win in tokens.json. | `system.color.palette.*` |
| **4** | Typography — typefaces, modular ratio, full size scale, weights, line heights, letter spacing, sample text per specimen. **Classify heading + body typefaces using `typography-taxonomy.md` (pick a `character` slug) and populate platform-agnostic `alternatives[]`.** | `system.typography.heading.*`, `system.typography.body.*`, `system.typography.scale.*`, `system.typography.sample_text.*` |
| **5** | Form language — radius, shadow, one-line `character` phrase, motifs. | `system.form.*`, `system.motif` |
| **6** | Voice guidelines — formality + scale, polymorphic vocabulary constraints, do's and don'ts using participant quotes from `{name}-brand-quotes.md`. **Populate `techniques[].quotes[]` (each `{speaker, context, text}`) so quotes round-trip into the process record.** | `system.voice.*`, `system.techniques[].quotes[]` |
| **7** | Quality check — coherence framework /30 (+ optional Rand's Seven /70). Flag anything < 3; adjust before finalizing. | `system.quality.*` |
| **7.5** | Visual-language craft — form primitives, composition archetypes, elevation, motion, motif library, photography, illustration. | `system.visual_language.*` |
| **7.6** | **Platform entries — for every brand-target platform, run the substitution algorithm (R1–R6 in `build-export-contract.md`) against `platform-fonts.yaml` to build character-appropriate `heading_chain[]` and `body_chain[]`. R2 hard check: `heading_chain[1]` ≠ `body.primary.family` unless R6 applies.** Also populate color_slots, probe_notes, caveats per platform. | `system.platforms[]`, `system.typography.per_platform.*` |
| **7.7** | Voice expansions — banned (with replacements + reasons), card_sort, tone_matrix, specificity_test. | `system.voice.*` (additive) |
| **7.8** | Governance scaffold — **`owner.name` (string, required; full name or preferred attribution — NOT email-inferred)**, optional owner.email, SemVer triggers, changelog, ≥3 ADRs, deprecation window. | `system.governance.*` |
| **7.9** | Cultural anchors — every reference names `anchors_property`; no vapor allowed. Hard-fail if any `cultural_anchors[]` entry is missing `anchors_property`. | `system.cultural_anchors[]` |
| **8** | Self-verify YAML shape against `skills/brand-export/references/build-export-contract.md`. Every Required-atomic and Required-v6 field must be present with valid content. One bounded auto-fix pass. Block on remaining FAILs. | `system.quality.build_verification` |
| **9** | Finalize — set `system.status` to `draft`, set `system.last_built`, append changelog, present summary to user, confirm. | `meta.version`, `meta.generated`, `system.status`, `system.last_built` |

### Critical Rules

- **Trace everything.** Every choice must connect back to discovery/synthesis data. If you can't explain why, reconsider.
- **Don't invent preferences.** If the synthesis doesn't have clear data for a dimension, acknowledge the gap and make a conservative default choice with explanation.
- **Validate contrast.** Never ship colors that fail WCAG AA for their intended usage.
- **Write incrementally.** Save to YAML after each phase, not just at the end.
- **Be specific.** Output actual hex values, actual font names, actual pixel/rem values. Abstract guidelines without concrete values aren't a design system.
- **Respect variable-N.** Principles, palette roles, motifs, platforms — render the count the brand actually needs. Do not pad to fixed numbers.
- **Preserve technique shape.** Voice constraints stay in their source technique's shape (never_say[] OR specificity_test{} OR card_sort{}). Do not collapse into a single prefer/avoid pair.
- **Typography substitution never collapses heading into body.** When running Phase 7.6 per-platform substitution, the first non-primary fallback in `heading_chain[]` must differ from `body.primary.family` unless the brand deliberately uses one family throughout (R6 in the contract). Produce character-appropriate fallbacks from `platform-fonts.yaml` — never default to the body font.
- **Required-v6 fields are not optional.** `personality.character`, `personality.archetype_in_action[]`, `personality.do_dont`, `color.roles[]`, `section_summaries.*` (12 slugs), `typography.*.character`, `typography.*.alternatives[]`, `typography.per_platform.*`, `governance.owner.name`, and `platforms[]` are required. Phase 8 hard-fails if any are missing. Don't paper over at finalize — go back and populate.
- **No Aaker zero-fill.** If the Aaker technique wasn't run, omit `system.personality.aaker_scores` entirely rather than writing zeros.
- **Cultural anchor vapor check.** Every `cultural_anchors[]` entry must have a non-empty `anchors_property`. Phase 7.9 and Phase 8 both enforce.

## Tool & Platform Recommendations

When users ask about design tools, token management platforms, font resources, color tools, or any specific products:

1. **Never recommend from a hardcoded list.** The design tool landscape changes rapidly.
2. **Search for current information** using web search.
3. **Prioritize**: open-source and well-maintained tools, tools that integrate with the user's existing stack.
4. **For design tokens specifically**: The token tooling ecosystem is evolving fast. Search for the current state.
5. **For fonts**: Direct users toward open-source fonts as the default for startups.
