---
name: brand-export
description: "This skill should be used when the user asks to export brand artifacts, generate CSS tokens, create design tokens, export the design system, generate the HTML doc, generate the brand methods record, or says \"brand-export\". It produces brand artifacts in phased bundles — core (tokens + guidelines + quickref), then optional PDFs, companions, methods, synthesis, and LLM-readable tier — so long runs can be paused and handed off to a fresh session."
argument-hint: "[core | pdfs | companions | methods | synthesis | llm | all | <artifact-slug>]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

Export concrete artifacts from the brand system defined in `brand-identity.yaml`. Rendering is template-first (copy the template, fill placeholders — see Rule 0 in `rendering-rules.md`), and runs are structured as bundles you can invoke independently. Every artifact is structurally validated after write; a single bounded auto-fix pass runs on failure.

**Every Tier 1 artifact is external-reference**: written for clients, consultants, designers, and developers who have no context about this plugin. Keep Tier 1 content in end-user language — no build phases, skill names, slash commands, configuration-file names, or internal status vocabulary in Tier 1 output. This is a standing rule; review drafts against it before writing.

## Startup

1. Read `brand-identity.yaml` from the current working directory. If it doesn't exist or `system.status` is `not_started`, inform: "No brand system to export. Run /brand-build first."

2. **Load references** (MUST read before rendering):
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/build-export-contract.md` — the canonical data contract. Drives the hard-fail validation at startup (step 3). Also defines the `system.quality.export_log[]` schema (see step 4a).
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/rendering-rules.md` — cross-artifact render rules. **Rule 0 (template-first rendering) is the overriding policy** — every templated artifact is rendered by copy-then-fill.
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/artifacts.md` — tier-classified artifact catalog with per-artifact specs. Every entry carries a `Render mode: copy-first, fill-only` marker.
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/artifact-schemas.yaml` — declarative structural oracle used by the validator (step 8 of Rendering below).
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/verification-protocol.md` — the render → verify flow. Re-load before the verification pass.
   - `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/typography-taxonomy.md` — only when rendering typography sections or theme-builder companion files; confirms character classifications.
   - `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/platform-fonts.yaml` — only when rendering platform-matrix or theme-builder companion files; the per-platform font knowledge base.

3. **Contract validation** against `build-export-contract.md`:
   - Walk every Required-atomic path — missing = hard-fail with: "Brand system missing {field}. Run /brand-build to populate before re-trying export." Cite the contract section.
   - Walk every Required-v6 path — same hard-fail behavior. **Do not auto-compose at export time**; that's brand-build's job. If `personality.character`, `archetype_in_action[]`, `do_dont`, `color.roles[]`, `section_summaries.*`, `typography.*.character`, `typography.*.alternatives[]`, `typography.per_platform.*`, `governance.owner.name`, or `platforms[]` are missing, block and direct user to re-run brand-build.
   - For Legacy-compat shapes (`palette` as 4-role object, flat `anchors` dict, etc.), normalize in-memory — do NOT modify the source YAML. Log each normalization as INFO in the verification report.

4. **Cultural anchor vapor check**: if `system.cultural_anchors[]` is present, every entry must have non-empty `anchors_property`. If any entry lacks it, hard-fail with the offending entries listed.

5. **Resume awareness (export log)**: load `system.quality.export_log[]` (initialize to `[]` if absent — brand-build Phase 9 should populate this going forward). For each artifact in the resolved bundle (step 6 below), build a summary table:

   | artifact | last_exported | structural_check | age |
   |---|---|---|---|

   Present to the user:

   > I'll export {N} artifacts for bundle `{name}`. {M} are already on disk and passed structural validation on their last run. Options:
   > 1. **Missing/failed only** — re-render only artifacts not already rendered + passed (default).
   > 2. **Full rebuild** — re-render every artifact in the bundle regardless of state.
   > 3. **Cancel**.

   Default to option 1 on any confirmation. If the bundle arg is literally `all`, treat that as an implicit request for full rebuild (option 2) and skip the prompt.

6. **Resolve bundle**: dispatch the argument to an artifact list.

   | Arg | Expands to |
   |---|---|
   | `core` *(default when no arg)* | `tokens.css`, `tokens.json`, `brand-guidelines.html`, `brand-quickref.md` |
   | `pdfs` | `brand-guidelines.pdf`, `brand-methods.pdf` — requires HTML counterparts already on disk; if missing, prompt: "No {file}. Run `/brand-export core` (for brand-guidelines.html) or `/brand-export methods` (for brand-methods.html) first." |
   | `companions` | `logo-construction.svg`, `illustration-system.html`, `photography-reference-grid.html`, `governance.md`, `email-template.html`, `tailwind.config.js`, `theme-figma.json`, `platform-matrix.md` (8 files) |
   | `methods` | `brand-methods.html` |
   | `synthesis` | `synthesis-report.md` — only if `synthesis.status != not_started`; otherwise inform user no synthesis data exists and skip. |
   | `llm` | `brand.md`, `brand.extensions.yaml` |
   | `all` | core + pdfs + companions + methods + synthesis + llm (full rebuild) |
   | `<artifact-slug>` | Single artifact by canonical slug. Valid slugs: `tokens-css`, `tokens-json`, `tailwind-config`, `theme-figma`, `platform-matrix`, `brand-guidelines`, `brand-guidelines-pdf`, `brand-quickref`, `logo`, `illustration`, `photography`, `governance`, `email`, `brand-methods`, `brand-methods-pdf`, `synthesis`, `brand-md`, `brand-extensions`. (Legacy slugs `brand-cross-surface-map`, `cross-surface-map`, `theme-google-slides`, `theme-powerpoint`, `theme-keynote`, `theme-canva`, `theme-pitch`, `themes` are deprecated and map to `platform-matrix`. Print a one-line deprecation note and continue.) |
   | legacy synonyms (`tokens`, `canonical`, `themes`, `quickref`) | Preserved. Map to new equivalent (`tokens` → `tokens.css + tokens.json`; `canonical` → `brand-guidelines.html + brand-quickref.md`; `themes` → 5 theme-* files; `quickref` → `brand-quickref.md`). Print a one-line deprecation note: `/brand-export {legacy}` is deprecated; use `/brand-export {new}`. Continue the run. |

7. Create the output directory: `./brand-assets/` (CWD-relative). Inside it, create `./brand-assets/_build/` for internal diagnostics (never exposed as user-facing output).

## Cross-surface theme rendering (surface-translations.yaml)

All cross-surface theme outputs are driven by a single declarative file:

```
${CLAUDE_PLUGIN_ROOT}/assets/surface-translations.yaml
```

That file declares one block per surface, each with:
- `output` — relative filename written under `./brand-assets/`
- `transform` — render function name
- `template?` — optional Markdown/JSON template the transform fills
- `color_slots` — surface's color slot → token-path map (e.g. `Accent1: "{primitive.color.palette.primary}"`)
- `text_styles`, `fonts`, `constraints` — same shape

**At export time**, walk the file in two passes:

```
load tokens.json
load surface-translations.yaml

# Pass 1: per-surface machine artifacts
for each surface where machine_output is set (web_css, tailwind_config, figma_tokens_studio):
    resolve token-path references against tokens.json
    apply surface.transform
    write surface.machine_output
    validate (Step S)
    append to export_log[]

# Pass 2: consolidated human-facing platform-matrix.md
copy consolidated_map.template → ./brand-assets/platform-matrix.md
for each surface in surfaces:
    column = surface.column_label
    fill the column for that surface's row in §1 (Color), §2 (Typography), §3 (Form)
    fill the §4 per-platform sub-section for that surface (presentation surfaces only):
       - typography fallback chain + rationale (from system.typography.per_platform.{slug})
       - probe notes (from platform-fonts.yaml)
       - caveats (per-surface constraints)
validate (Step S)
append to export_log[]
```

There are no per-surface .md guides — every presentation/graphic surface (Slides / PowerPoint / Keynote / Canva) renders as a column in `platform-matrix.md`'s master tables PLUS its own §4 sub-section, rather than a separate file.

To opt a brand into a non-default surface (Pitch, iOS, Android, etc.), uncomment that surface's block in surface-translations.yaml AND add its `column_label` to `consolidated_map.columns`. The new column appears in the master tables.

## Rendering

For each artifact in the resolved bundle, in the order declared by the bundle:

1. Look up the artifact in `references/artifacts.md` and confirm its `Template:` path.
2. **Copy the template file verbatim** to the output destination under `./brand-assets/`. Use the `Bash` tool: `cp "${CLAUDE_PLUGIN_ROOT}/assets/{template-filename}" "./brand-assets/{output-filename}"`. (Every render template lives in plugin-root `assets/` — see the `template:` field for the artifact in `artifact-schemas.yaml`.) This is the working draft. Do NOT recreate the document from scratch.
3. **Fill in place.** Walk the working draft and replace every `{{ placeholder }}` with the matching value from `brand-identity.yaml`. Expand `<!-- REPEAT:name -->` blocks over the matching collection. Remove `<!-- OPTIONAL:name -->` blocks only when the driving technique was not run.
4. **Never restructure.** Do NOT rename section IDs, reorder sections, invent new sections, rewrite CSS variable names, rename JSON keys, or change Markdown heading text that carries a slug. Creative surface is the content inside placeholders — nothing else. If a template seems wrong, stop the render, update the template file under `assets/`, and re-run.
5. Apply the cross-artifact rules from `references/rendering-rules.md` (voice-constraint polymorphism, semantic color routing, per-section chips, etc.). These constrain *content within placeholders*; they do not license structural changes.
6. **Before writing a Tier 1 artifact**, re-read the draft as an external reader. If any sentence references this plugin, a slash command, a skill name, a build phase, a configuration file path, or internal status vocabulary, rewrite it in end-user language. Tier 2 operator files may reference the workflow in plain prose; Tier 3 files are machine-formatted per the brand.md spec.
7. Write the file.
8. **Validate structure** (see `verification-protocol.md` Step S): invoke `${CLAUDE_PLUGIN_ROOT}/scripts/validate-structure.py --artifact ./brand-assets/{filename} --schema {oracle-key}`. Parse the JSON verdict.
9. **One-shot auto-fix if failed.** If `passed: false`, re-run steps 2–7 once for this artifact — start from a fresh `cp` of the template. Re-validate. If still failing, log the failure prominently in the run summary and move on (the validator is advisory, not blocking).
10. **Append to export log.** Record `{artifact, status, last_exported, structural_check, auto_fix_attempted, structural_check_after_fix, verified_at}` to `system.quality.export_log[]` in `brand-identity.yaml`. Last entry per `artifact` slug is the authoritative state.

Do not skip a rendering rule because it "looks correct" — the rules in `rendering-rules.md` are the stem every verification gate hangs from.

## Bundle completion checkpoint

After the requested bundle finishes (before any follow-on work), print a summary:

```
{bundle} bundle complete — {N} artifacts rendered.
Structural validation: {P} pass, {F} auto-fixed, {S} still failing.
Export log updated at brand-identity.yaml → system.quality.export_log[].

Next likely steps:
  /brand-export pdfs          (PDF variants of the HTML docs)
  /brand-export companions    (theme builders + visual-system assets)
  /brand-export methods       (process-record with technique blocks)
  /brand-export llm           (LLM-readable tier)

Handoff to a fresh session is safe — export log persists. Run /brand-export again to resume.
```

Do NOT auto-continue into another bundle. The user decides what to run next.

## Execution order (by bundle)

Artifacts within a bundle render in the order below. When the user runs `all`, bundles execute in the listed order (core → pdfs → companions → methods → synthesis → llm).

### `core` (4 artifacts)
1. `tokens.css` (programmatic — no template; validator checks required custom-property set)
2. `tokens.json` (template copy-fill)
3. `brand-guidelines.html` (template copy-fill — heaviest render)
4. `brand-quickref.md` (template copy-fill — depends on tokens + guidelines for cross-references)

### `pdfs` (2 artifacts — HTML dependencies must exist)
1. `brand-guidelines.pdf` (headless-browser render of brand-guidelines.html)
2. `brand-methods.pdf` (headless-browser render of brand-methods.html)

Probe chain for headless rendering: chrome → chromium → chromium-browser → macOS app paths → wkhtmltopdf last-resort. Use `--virtual-time-budget=5000` for webfont load. A4, print-friendly page breaks.

### `companions` (8 artifacts)
1. `logo-construction.svg`
2. `illustration-system.html`
3. `photography-reference-grid.html`
4. `governance.md`
5. `email-template.html`
6. `tailwind.config.js`     ← machine artifact for web framework
7. `theme-figma.json`       ← machine artifact for Figma Tokens Studio import
8. `platform-matrix.md`     ← single consolidated cross-surface reference (master tables + per-platform details)

`platform-matrix.md` is the single source of truth for applying the brand on every supported surface. Master tables (rows = tokens/components, columns = surfaces: Web CSS, Tailwind, Figma, Google Slides, PowerPoint, Keynote, Canva). Per-platform sections below the tables cover typography fallback chains, setup steps, probe notes, and platform-specific caveats. It replaces what used to be three separate things: `platform-matrix.html` (per-platform card layout), `brand-cross-surface-map.md` (the master grid), and the per-surface `theme-*.md` guides.

All cross-surface output is driven by `${CLAUDE_PLUGIN_ROOT}/assets/surface-translations.yaml`:
- `tokens.css` (in `core` bundle), `tailwind.config.js`, and `theme-figma.json` are machine artifacts emitted as their own files.
- All `category: presentation` and `category: graphic` surfaces feed into the master tables + per-platform sections in `platform-matrix.md`. There are no per-surface guides.

Pitch / iOS / Android / Notion / SCSS / email-HTML / InDesign are opt-in only — uncomment in `surface-translations.yaml` to enable.

### `methods` (1 artifact)
1. `brand-methods.html`

### `synthesis` (1 artifact, conditional)
1. `synthesis-report.md` (only if `synthesis.status != not_started`)

### `llm` (2 artifacts)
1. `brand.md`
2. `brand.extensions.yaml`

### Internal (to `./brand-assets/_build/`; not user-facing)
- `_build/export-verification.md` (quality report from verification protocol, written after the final bundle in a run)

## Critical invariants (across all bundles)

- **Template-first rendering** (`rendering-rules.md` Rule 0): every templated artifact starts life as a verbatim `cp` of the template file. The LLM fills; the LLM does not restructure.
- **Contract-first**: no Required-atomic or Required-v6 field is auto-composed at export time. Missing fields block export with a message pointing to brand-build.
- **Advisory validator**: the structural validator emits PASS/FAIL verdicts per artifact and triggers at most one auto-fix re-render. Still-failing artifacts are logged prominently but do not block the rest of the run.
- **Export log is authoritative**: `system.quality.export_log[]` is the cross-session resume record. Always append after a render, even on failure. Reading it at startup lets a fresh session pick up cleanly.
- **No "extensions" output**: `design-system-extensions.html` is retired; do not emit. Fold any still-valuable content into `brand-guidelines.html` as part of its canonical sections.
- **No legacy sibling files**: `brand-llm-manual.yaml` is retired (replaced by Tier 3 `brand.md` + `brand.extensions.yaml`). Do not emit. Delete if present in the output folder during migration.
- **Three-tier separation**: no Tier 1 file references plugin internals, slash commands, phase numbers, or skill filenames. Tier 2 operator docs may reference the workflow in end-user prose. Tier 3 follows the brand.md spec.
- **Typography no-collapse (R2)**: for every `typography.per_platform.{slug}`, confirm `heading_chain[1]` ≠ `body.primary.family` unless R6 (single-family brand) applies. Flag in the verification report if violated.
- **Weight-hierarchy preservation**: the brand's chosen heading vs. body weight differential (heading lighter, heavier, or same) is preserved in every platform substitution chain.
- **Anchor-set closure**: all named colors appear in `tokens.json → primitive.color.*`; no artifact introduces colors outside this set.
- **Cultural-anchor non-vapor**: every `cultural_anchors[]` entry names what property is anchored. Vapor anchors hard-fail at startup (step 4) and are checked again at verification.
- **Personality anatomy**: brand-guidelines.html personality section renders synthesis + character + archetype labels + Aaker + keywords + archetype-in-action (≥3) + do/don't (≥3 each). This is the canonical location — not brand-methods.
- **Color Role Playbook**: brand-guidelines.html §3 Color renders the ≥8-row Role Playbook table. Theme-builder companion files reference it.
- **Semantic token routing**: every Do/Don't, rating badge, status chip routes through `--color-affirm` / `--color-warn` / `--color-success` / `--color-warning` / `--color-danger`. Never hardcode stock green/red.
- **Progressive disclosure**: Quickref (shallow) → brand-guidelines.html (full canonical) → brand.md + brand.extensions.yaml (LLM-readable). Each deeper layer adds detail without contradicting the shallower one.
- **Platform-primary**: `platform-matrix.md` is a first-class consolidated document — master tables (rows = tokens, columns = surfaces) plus per-platform sub-sections covering Google Slides, PowerPoint, Keynote, Canva, and Figma with setup steps, fallback chains, and caveats. Machine-import companions (`tokens.css`, `tailwind.config.js`, `theme-figma.json`, `email-template.html`) are paste-ready deliverables, not footnotes.

## After the final bundle — verification

The per-artifact structural validator (Rendering step 8) runs inside the render loop. The *batch* verification pass runs once, after the final bundle of the current run:

- **Step 0** already ran at startup (contract validation + cultural-anchor vapor check + normalization log).
- **Step S** already ran per-artifact during Rendering (structural validator + bounded auto-fix). Results are already in `export_log[]`.
- **Step A** — render screenshots of HTML and PDF artifacts (probe `pdftoppm`, headless Chromium `--screenshot`, `sips` in that order).
- **Step B** — walk `${CLAUDE_PLUGIN_ROOT}/assets/export-verification-checklist.md`: every gate is PASS/FAIL (no WARN). Cite evidence per gate (file + grep pattern OR screenshot region). Tier 1 prose is reviewed against the external-facing principle (no plugin-internal language, slash commands, skill names, or build phases in reader-visible text) rather than a regex list. §S structural gates read directly from `export_log[]` — no re-validation.
- **Step C** — apply one bounded auto-fix pass for any FAIL that has a playbook entry. Re-render affected artifacts. Re-check. **Hard cap: one auto-fix pass per gate** — STILL-FAIL reports directly, no second attempt. (This is a *separate* auto-fix pass from Step S's per-artifact one; Step C targets checklist gates, Step S targets structural shape.)
- **Step D** — write `./brand-assets/_build/export-verification.md` (NOT the user-facing folder), update `system.quality.export_verification` in brand-identity.yaml, print the summary, and surface any remaining FAILs to the user (advisory — the run still completes).

Report to the user: if all PASS, point them to `_build/export-verification.md` for the audit trail. If any FAIL, list each with the specific recommended fix.
