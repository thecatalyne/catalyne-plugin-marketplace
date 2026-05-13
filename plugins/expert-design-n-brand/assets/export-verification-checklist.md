# Self-Verification Checklist

> **Canonical vocabulary source.** Token names, role labels, surface slot names, and CSS/Tailwind/Figma keys used in this document are defined in `assets/platform-matrix-template.md`. If a name here appears to disagree with the Platform Matrix, the Platform Matrix wins.

Loaded by `brand-export/SKILL.md` (and by `brand-build/SKILL.md` at Phase 8 for the contract-side subset). Every gate is **PASS or FAIL** — there is no WARN. The protocol blocks acceptance on any FAIL that remains after one bounded auto-fix pass.

References:
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/build-export-contract.md` — data contract
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/rendering-rules.md` — cross-artifact render rules, including the Tier 1 external-facing principle
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/artifacts.md` — tier-classified catalog
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/verification-protocol.md` — render → verify flow

## How gates work

Every gate specifies:
- **Applies to**: which tier(s) the gate runs against
- **Check**: a grep pattern, file presence test, or visual inspection
- **On FAIL**: pointer to the auto-fix playbook entry (if any) OR "manual rewrite required"

Gates are grep-able or visually verifiable. Visual items (font fidelity in PDF, contrast badges colored, components in brand palette, gradient library strips) require screenshots — inspect pixels, not source CSS.

## Producer responsibilities

| Producer | Gates to walk |
|---|---|
| `brand-build` | Phase 8 — contract-side subset: §CT (contract), §PF (placeholders in emitted YAML) |
| `brand-synthesize` | §CT-quotes, §PF on `synthesis-report.md` |
| `brand-export` | ALL gates — contract, Tier 1 structure, Tier 1 content, Tier 1 tone, Tier 1 visual, Tier 2, Tier 3, cross-artifact integrity |

---

# §CT — Contract conformance (applies: brand-identity.yaml)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| CT.1 | Every Required path in contract is present with valid content. | Walk `build-export-contract.md` Required table. For each row, confirm field exists in `brand-identity.yaml` with matching type/shape. | run brand-build to populate (fails before export starts) |
| CT.2 | Every Required path is present with valid content. | Walk contract Required table. For each: `personality.character` 40–70 words; `personality.archetype_in_action[]` ≥3 items each `{context, text}`; `personality.do_dont.do[]` ≥3 and `dont[]` ≥3; `color.roles[]` ≥8 items each `{role, token, hex, when_to_use, dont_use_for}`; `section_summaries.*` has all 12 slugs each 15–50 words; `typography.heading.character` + `body.character` are valid taxonomy slugs; `typography.heading.alternatives[]` + `body.alternatives[]` non-empty; `typography.per_platform.{slug}` has `heading_chain[]` + `body_chain[]` for every platform in `system.platforms[]`; `governance.owner.name` non-empty string; `system.platforms[]` ≥1 entry. | run brand-build to populate |
| CT.3 | No Aaker zero-fill. | If `personality.aaker_scores` is present, all 5 dimensions have scores > 0 OR the field is entirely absent (no partial zero-fills). | brand-build must omit field entirely when technique not run |
| CT.4 | Cultural-anchor vapor check. | If `cultural_anchors[]` is present, every entry has non-empty `anchors_property`. | populate `anchors_property` or remove entry |
| CT.5 | Voice-constraint shape preservation. | `voice.vocabulary.never_say[]`, `.specificity_test{}`, `.card_sort{}` are in their source-technique shape. NOT collapsed into a single prefer/avoid list. | re-run brand-build Phase 6 |
| CT.6 | Typography heading fallback ≠ body primary (R2). | For every `typography.per_platform.{slug}`: `heading_chain[1]` (first non-primary) ≠ `body.primary.family` UNLESS R6 applies (same family + character for both). | re-run brand-build Phase 7.6 substitution |
| CT.7 | Quotes round-trip. | `system.techniques[].quotes[]` is populated when `{name}-brand-quotes.md` exists in working dir. | re-run brand-synthesize with quote-ingestion |

---

# §PF — Placeholder integrity (applies: every rendered artifact)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| PF.1 | No unresolved `{{ }}` placeholders in any rendered file. | `grep -c '{{' <artifact>` returns 0 for every emitted file (HTML, Markdown, CSS, JSON, YAML, SVG). | auto-fix: re-render the affected artifact after populating missing fields |
| PF.2 | No `TODO:` or `FIXME:` in Tier 1 or Tier 2 artifacts. | `grep -Ei '\b(TODO|FIXME):' <artifact>` returns 0. | manual rewrite |
| PF.3 | No `[TBD`, `[to be generated]`, `[pending]` placeholders in Tier 1 artifacts. | `grep -Ei '\[(TBD|to be|pending)' <T1 artifact>` returns 0. | populate in brand-build and re-export |

---

# §S — Structural shape validation (applies: every templated artifact)

These gates read directly from `system.quality.export_log[]` — the per-artifact structural validator (Step S in `verification-protocol.md`) has already run during rendering and emitted JSON verdicts consumed by the skill at that time. Step B does not re-invoke the validator; it inspects the log.

Source oracle: `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/artifact-schemas.yaml`.
Validator: `${CLAUDE_PLUGIN_ROOT}/scripts/validate-structure.py`.

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| S.1 | Every artifact in the bundle has a structural-validation entry in `export_log[]`. | For each rendered artifact, `system.quality.export_log[]` contains a last-entry with `structural_check` ∈ {`pass`, `fail`, `not_applicable`}. | re-invoke `validate-structure.py` and append to log |
| S.2 | Section-order matches template (HTML artifacts). | For each HTML artifact with an oracle entry, the validator's `required_sections.result == "pass"` — all declared section IDs present in declared order. | one-shot auto-fix (Step S itself) already ran; STILL-FAIL is surfaced to user |
| S.3 | No invented top-level sections. | `required_sections.detail.invented_sections` is empty for every HTML artifact. | the render regenerated the file from scratch instead of copying the template — re-render per Rule 0 |
| S.4 | Required section-anatomy classes present. | `required_sections.detail.anatomy_failures` is empty for every HTML artifact. | verify `section_summaries.*` and personality fields populated; re-render |
| S.5 | Required CSS variables declared (tokens.css). | Validator's `required_variables.result == "pass"` — every declared `--variable` is defined. | re-render tokens.css from the semantic resolution chain in rendering-rules.md |
| S.6 | Required JSON/YAML keys present (tokens.json, theme-figma.json, brand.extensions.yaml). | Validator's `required_keys.result == "pass"` — every dotted path resolves in the emitted document. | re-render the affected file |
| S.7 | Required Markdown headings present and ordered (brand.md, governance.md, platform-matrix.md, brand-quickref.md, synthesis-report.md). | Validator's `required_headings.result == "pass"` — every declared heading present (with optional substring match). | re-render from template |
| S.8 | Required frontmatter fields present (brand.md). | Validator's `required_frontmatter.result == "pass"` — `name`, `tagline`, `version`, `language` all populated. | repopulate frontmatter block at top of brand.md; re-render |

**Auto-fix posture**: Step S is advisory. One re-render pass runs inside the render loop (per-artifact, triggered by the validator's fail verdict). If the re-render still fails, the run continues and the failure surfaces in Step D's summary. Acceptance is NOT blocked on §S fails — the user decides whether to ship or re-run. This is deliberate: structural drift is a class of problem that the user can quickly inspect and fix manually, and blocking the whole export would lose the value of the bundles that rendered correctly.

---

# §T1S — Tier 1 structural gates (applies: Tier 1 artifacts)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| T1S.1 | All T1 artifacts present in output folder. | 13 expected files: brand-guidelines.html, brand-guidelines.pdf, brand-quickref.md, tokens.css, tokens.json, tailwind.config.js, theme-figma.json, platform-matrix.md, logo-construction.svg, illustration-system.html, photography-reference-grid.html, governance.md, email-template.html. | emit missing file(s) |
| T1S.2 | No internal artifacts emitted to user folder. | Output folder has NO `TEST_PROTOCOL.md`, `export-verification.md`. | delete from folder; ensure brand-export doesn't re-emit |
| T1S.3 | Every brand-guidelines.html section has def+summary paragraphs. | `grep -c '<section' brand-guidelines.html` equals count of `<p class="section-definition">` AND count of `<p class="section-summary">`. Every `<section>` element has both child `<p>` tags before any data display. | auto-fix: re-render after confirming `section_summaries.*` populated |
| T1S.4 | brand-guidelines.pdf size + page count. | PDF file ≥ 1 MB and ≥ 25 pages. | re-render PDF via headless-browser probe chain; ensure webfonts loaded (`--virtual-time-budget=5000`) |
| T1S.5 | brand-guidelines.html canonical scope. | Includes all 12 required sections (Cover/Foundation/Identity/Color/Typography/Visual Language/Spacing/Components/Voice/Platforms/Governance/LLM pointer) + appendices. | re-render canonical after verifying template covers all 12 |
| T1S.6 | Platform matrix has one §4 sub-section AND one column per brand-target platform. | In `platform-matrix.md`: `grep -c '^### ' platform-matrix.md` (under §4) equals `len(system.platforms[])`. Master-table column header count in §1/§2/§3 also equals `len(system.platforms[])` (after subtracting the leading "Token / role" + machine-artifact columns CSS / Tailwind / Figma). | re-render platform-matrix |
| T1S.7 | Each cross-surface deliverable exists and is non-stub. | For each of tailwind.config.js, theme-figma.json, platform-matrix.md, email-template.html: file exists, size > 500 bytes, contains resolved brand values (not placeholders). platform-matrix.md must contain one column header per surface declared in surface-translations.yaml AND one §4 sub-section per presentation surface. | populate templates with brand values; re-emit |

---

# §T1C — Tier 1 content quality gates (applies: Tier 1 artifacts)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| T1C.1 | Personality character paragraph renders. | brand-guidelines.html contains `<p class="personality-character">` with content 40–70 words. | verify CT.2 then re-render |
| T1C.2 | Personality archetype-in-action block renders. | brand-guidelines.html has `<section class="personality-archetype-in-action">` with ≥3 `<div class="archetype-example">` children. | verify CT.2 then re-render |
| T1C.3 | Personality do/don't exemplars render. | brand-guidelines.html has `<section class="personality-do-dont">` with ≥3 do items AND ≥3 don't items. | verify CT.2 then re-render |
| T1C.4 | Color Role Playbook sub-section present. | brand-guidelines.html §3 Color contains `<section class="color-role-playbook">` (or equivalent) with ≥8 role rows. | verify CT.2 (`color.roles[]` ≥8) then re-render |
| T1C.5 | Never-Say principle renders both halves. | In any voice-constraint block: both the bolded positive constraint AND the italicized test question are emitted. | auto-fix: re-render voice section |
| T1C.6 | Semantic theme tokens resolved. | tokens.css contains `--color-affirm` and `--color-warn` with non-placeholder hex values. | apply resolution chain from rendering-rules.md; re-render tokens |
| T1C.7 | Variable-N collections render all items. | Principles, palette core, color roles, motif library, platforms, scales, expressions, gradients: rendered row count equals YAML array length for each. | re-render affected section |
| T1C.8 | Typography substitution chains embedded in per-platform sub-sections. | In `platform-matrix.md` §4: each per-platform sub-section contains a "Typography fallback chain" block with both heading + body chains + rationale, populated from `system.typography.per_platform.{slug}`. | re-render platform-matrix |
| T1C.9 | Platform matrix font fallbacks have no heading=body collapse. | In platform-matrix.md §4 Per-platform details: for every per-platform sub-section, the heading-chain's first non-primary fallback is NOT the same family as body-chain's primary (unless R6 applies). | re-run brand-build Phase 7.6 |
| T1C.10 | Sample text is brand-relevant. | In typography specimens, `{{ sample_display }}` / `h1` / `h2` / `h3` / `body` / `small` are NOT "The quick brown fox" or Lorem Ipsum. | verify CT.1 (`typography.sample_text.*` populated); re-render |
| T1C.11 | Cover ledger segments omit missing data. | If `quality.coherence_score` absent, cover ledger does NOT show `Coherence —/30`. Same for Rand's Seven. | re-render cover |

---

# §T1T — Tier 1 external-facing tone (applies: Tier 1 artifacts)

One gate, reviewer-judged against the principle in `rendering-rules.md § Tier 1 is external-facing`. Regex denylists are not used here — they over-match on legitimate prose and miss new vocabulary as it drifts. Review instead.

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| T1T.1 | Tier 1 prose reads as external reference. | Open each Tier 1 file. Read every reader-visible string (prose, table labels, link text, visible code-block comments). Confirm: no references to build phases, skill / agent / plugin-file names, slash commands, configuration file paths, or internal status vocabulary (`PASS/WARN/FAIL`, `hard-fail`, `auto-compose`, `soft-skip`, `floor validation`). The reader should be able to understand every sentence without knowing this plugin exists. | rewrite the offending sentences in end-user language; re-render |

---

# §T1V — Tier 1 visual fidelity gates (applies: Tier 1 rendered artifacts)

Requires screenshots (see verification-protocol.md Step A).

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| T1V.1 | PDF fonts render — brand heading + body typefaces, not fallback. | Inspect `_build/verification/brand-guidelines-page-*.png`. Heading font matches `typography.heading.primary.family`. | re-render PDF with longer `--virtual-time-budget`; verify font sources load |
| T1V.2 | Component specimens in brand palette. | Inspect rendered components in brand-guidelines.html screenshot. Buttons / badges / inputs / cards use `--color-primary`, `--color-text-primary`, etc. | re-render after tokens.css populated |
| T1V.3 | Contrast badges colored. | In palette section, WCAG AA / AAA badges render with semantic color (affirm for AAA, warn/danger for FAIL). | verify semantic resolution; re-render |
| T1V.4 | Spacing blocks render as visual artifacts (not a table). | `.spacing-grid` in form-language section contains `<div class="spacing-block">` with inline `width: Xpx; height: Xpx`. Spacing is NOT a plain `<table>`. | apply Form Language specimens rule from rendering-rules.md; re-render |
| T1V.5 | Per-section method chips render. | In each brand-guidelines.html section with `methods_for_{slug}` data, inline chips appear under the heading. Used = colored badge, unrun = grey strikethrough. | apply per-section chip rule; re-render |
| T1V.6 | Gradient library strips render. | `.gradients-grid` contains N `<div class="gradient-strip">` with linear-gradient fills matching YAML stops. | re-render color section |
| T1V.7 | Logo construction SVG renders without errors. | Open logo-construction.svg in a renderer (browser or headless Chromium); valid XML, all paths render. | fix SVG markup or re-generate |
| T1V.8 | brand-guidelines.pdf page breaks clean. | No orphan section titles (heading on page N, content starts page N+1). Every `<section>` first page starts fresh (via `page-break-before: page` on `.section-title`). | apply print CSS rules; re-render PDF |

---

# §T2 — Tier 2 structural + content gates (applies: brand-methods.html + .pdf + synthesis-report.md)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| T2.1 | brand-methods.html contains ledger. | Grep for `id="methods-ledger"` or `class="methods-ledger"`. | re-render brand-methods |
| T2.2 | Ledger row count matches registry. | Number of ledger rows = count in `techniques-registry.yaml → techniques`. | re-render |
| T2.3 | Every "Used" ledger row has a matching technique block. | For each `Used` row, a `<article class="technique-block">` exists with the technique's anchor. | re-render; check registry-to-block wiring |
| T2.4 | Every "Used" technique's `yaml_paths` are populated. | Cross-reference ledger status against brand-identity.yaml. | re-run brand-build to populate |
| T2.5 | Each technique block has quote ingestion attempted. | For each block: either a `<section class="technique-quotes">` with quotes, or the block renders cleanly without one (no empty shell). | CT.7 quotes wiring |
| T2.6 | Not-Run appendix present and collapsible. | Ensure `.not-run-appendix` or equivalent section at the bottom with all `—` techniques. | re-render |
| T2.7 | brand-methods.html has NO top-level methods-used block in Tier 1 files. | `grep -c 'id="methods-used"' brand-guidelines.html` = 0. | (T1 only has per-section chips) re-render brand-guidelines |
| T2.8 | synthesis-report.md populated (if synthesize ran). | File exists, size > 500 bytes, contains per-participant sections. | re-run brand-synthesize |

---

# §T3 — Tier 3 brand.md + extensions conformance (applies: brand.md + brand.extensions.yaml)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| T3.1 | brand.md has valid YAML frontmatter. | File starts with `---`, has closing `---`, contains required keys: `name`, `tagline`, `version` (integer), `language` (`en` / `pt-BR` / ...). | regenerate brand.md |
| T3.2 | brand.md has all 12 required sections. | Grep for `## Strategy` with sub-headings Overview / Positioning / Personality / Promise / Guardrails; `## Voice` with Identity / Tagline & Slogans / Message Pillars / Phrases / Tonal Rules; `## Visual` with Colors / Typography. | regenerate with template |
| T3.3 | brand.md H1 matches frontmatter `name`. | The single H1 in brand.md equals `{{ meta.brand_name }}`. | fix template variable |
| T3.4 | brand.md extensions pointer present. | Frontmatter contains `extensions: "./brand.extensions.yaml"`. | add to frontmatter |
| T3.5 | brand.extensions.yaml parses. | `yaml.safe_load` returns a dict with `sibling_of`, `meta` top-level keys. | regenerate |
| T3.6 | brand.extensions.yaml points to brand.md. | `sibling_of: "./brand.md"` at top. | add key |
| T3.7 | brand.extensions.yaml has required plugin sections. | Keys: `vocabulary.banned[]`, `voice`, `tone_matrix`, `output_constraints`, `cultural_anchors`, `platforms`, `governance`, `self_validation`. | populate missing keys |
| T3.8 | Cultural anchors in extensions have `anchors_property`. | Every entry in `extensions.cultural_anchors[]` has non-empty `anchors_property`. (Also CT.4 — same rule both sides.) | populate or remove |
| T3.9 | Banned vocab entries have replacement + reason. | Every `extensions.vocabulary.banned[]` entry has `word`, `replacement`, `reason` all non-empty. | populate |

---

# §X — Cross-artifact integrity (applies: entire output folder)

| # | Gate | Check | On FAIL |
|---|------|-------|---------|
| X.1 | All internal links resolve. | For every `<a href="./...">` in Tier 1 HTML files, target file exists in output folder. | fix links |
| X.2 | Cross-references point to correct tier. | brand-guidelines.html links to platform-matrix.md, tokens.{css,json}, tailwind.config.js, theme-figma.json, logo-construction.svg, illustration-system.html, photography-reference-grid.html, governance.md, email-template.html — all Tier 1. It does NOT link directly to brand-methods.html as a companion (Tier 2 is referenced only in Appendix E "Companion Files"). | re-render with correct links |
| X.3 | tokens.css and tokens.json agree. | Every `--color-*` in tokens.css has a corresponding entry in tokens.json `primitive.color.*`. Same for scales, gradients. | regenerate both from same source |
| X.4 | brand.md colors match tokens.json primitive colors. | brand.md's `## Visual > Colors` section hex values are a subset of tokens.json `primitive.color.*.$value`. | regenerate brand.md |
| X.5 | No brand-specific hardcoding in plugin templates. | Scan `assets/*-template.*` (and `assets/tokens-template.json` / `assets/theme-figma-template.json` / `assets/brand-template.md` / `assets/brand-extensions-template.yaml` / `assets/surface-translations.yaml`) for literal brand names, typeface names used as defaults (not as exemplars), or hex values that belong to a specific brand's palette. Every brand-specific value should be a template variable, not a hardcode. | replace with template variable or neutral fallback; re-render |

---

# Auto-fix playbook

Applied during Step C of the verification protocol. Each entry maps a failure pattern → first-pass fix. One pass only.

| Failure pattern | Auto-fix | Re-render |
|---|---|---|
| `{{` remains in rendered file (PF.1) | Re-populate the corresponding YAML field; re-render the file. | Affected artifact |
| Missing Required field (CT.2) | Block at startup; do not auto-fix. User must re-run brand-build. | N/A |
| Personality section missing character/archetype-in-action/do-dont (T1C.1–3) | Verify `system.personality.*` is populated per contract; if YES, re-render; if NO, block with "re-run brand-build Phase 1". | brand-guidelines.html + PDF |
| Color Role Playbook absent (T1C.4) | Verify `system.color.roles[]` has ≥8 entries; re-render §3 Color. | brand-guidelines.html + PDF |
| Never-Say only test question (T1C.5) | Re-render voice-constraint block with both paragraphs per rendering-rules.md. | brand-guidelines.html + brand-methods.html + PDFs |
| Semantic token hex missing (T1C.6) | Apply resolution chain; emit fallback hex; re-render tokens. | tokens.css, tokens.json, affected HTML |
| Variable-N mismatch (T1C.7) | Re-expand REPEAT blocks from YAML array; re-render section. | Affected artifact |
| Heading=body collapse (T1C.9, CT.6) | Block — do not auto-fix. User must re-run brand-build Phase 7.6 substitution. | N/A |
| Tier 1 tone breach (T1T.1) | Rewrite the offending sentences in end-user language. Reviewer-judged; no auto-fix. | Affected file |
| brand-guidelines.pdf < 25 pages (T1S.4) | Increase `--virtual-time-budget`; check for soft-skipped sections that should have rendered. | brand-guidelines.pdf |
| Orphan section title in PDF (T1V.8) | Apply `@page { orphans: 3; widows: 3; }` and `h2 { break-before: page; }`; re-render PDF. | brand-guidelines.pdf |
| Ledger row count mismatch (T2.2) | Re-render brand-methods with current registry. | brand-methods.html + PDF |
| Missing quotes section (T2.5) | If `system.techniques[].quotes[]` populated, re-render; if not, re-run brand-synthesize. | brand-methods.html + PDF |
| brand.md section missing (T3.2) | Re-render brand.md from template with current YAML data. | brand.md |
| brand.extensions.yaml key missing (T3.7) | Re-render extensions template with current YAML data. | brand.extensions.yaml |
| Internal link broken (X.1) | Check filename typos; re-render. | Affected file |
| Brand-specific hardcoding in template (X.5) | Replace with template variable or neutral fallback; re-render affected artifact. | All affected |

---

# Reporting format

Write `_build/export-verification.md` (NOT the user-facing output folder) with this structure:

```
# Export Verification Report

**Generated**: {timestamp}
**Brand**: {brand_name}
**Artifacts emitted**: {N} Tier 1 · {N} Tier 2 · {N} Tier 3

## Contract validation (§CT)
- Required paths: {N}/{N} PASS
- Required paths: {N}/{N} PASS
- Input shapes normalized: {N}

## Gate results
(table: gate ID · status · evidence · auto-fix-applied? · final-status)

## Auto-fix log
(list of fixes applied in Step C; one line per fix)

## Normalization log (Step 0)
(list of input-shape normalizations; e.g., "palette role-keyed object → core[]")

## Summary
PASS {N} · FAIL {N}
Acceptance: {ready | blocked-on-N-fails}
{If blocked: list each FAIL with recommended fix.}
```

Also write `system.quality.export_verification` into brand-identity.yaml:
```yaml
quality:
  export_verification:
    timestamp: ...
    summary: "PASS {N} · FAIL {N}"
    acceptance: ...
    auto_fix_passes: 0 | 1
    normalizations_applied: {N}
```

And a changelog entry with action `export_verification_run`.

---

# Acceptance decision

- **All PASS**: artifacts are ready. Point user to verification report for audit trail.
- **Any FAIL remaining after one auto-fix pass**: HARD-BLOCK acceptance. List every still-failing gate with specific recommended fix. Do not surface as "almost done."
