---
name: design-playground
description: "This skill should be used when the user asks to generate a playground, design playground, single-file HTML playground, brand-themed playground, interactive token explorer, or says \"design-playground\". Produces one self-contained playground.html from a brand-export bundle that demonstrates the brand's full token tree across Marketing, App, Slide, and Glossary surfaces with compare mode + live token controls."
argument-hint: "[no args | --no-presets]"
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

Emit a single-file HTML playground from a brand bundle. The output is `./brand-assets/playground.html` — open in any modern browser, no build step.

The skill is callable directly OR runs as part of `/brand-export companions` (when the playground-html artifact is opted into the bundle). It follows the same template-first rendering convention as every other artifact in `brand-export`: the renderer copies `assets/playground-template.html` and substitutes placeholders.

## Startup

1. Read `brand-identity.yaml` and `tokens.json` from the current working directory.
   - If `tokens.json` is missing, inform: "No tokens.json. Run /brand-export core first."
   - If `brand-identity.yaml` is missing, the renderer falls back to a generic name + tagline ("Design playground", "Open in any modern browser") — log INFO but do not block.

2. **Load references** (MUST read before rendering):
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/rendering-rules.md` — Rule 0 (template-first) applies here too.
   - `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/playground-look-mapping.md` — when present, defines the Look shape this playground consumes at runtime via paste-look. (Plan A; may not exist yet — do not block if absent.)

3. Resolve the output directory: `./brand-assets/`. Create if missing.

## Rendering

1. Invoke the renderer: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render-playground.py --brand-dir . --out ./brand-assets/playground.html`. Pass `--no-presets` only when the user requested it.
2. The renderer copies `${CLAUDE_PLUGIN_ROOT}/assets/playground-template.html` to the output path, then substitutes placeholders. It does NOT restructure the template.
3. **Validate structure** (advisory, non-blocking): invoke `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate-structure.py --artifact ./brand-assets/playground.html --schema playground-html`. Parse the JSON verdict.
4. If validation fails, re-run the renderer once. If it still fails, log the failure prominently and continue — the validator is advisory.
5. Append to `system.quality.export_log[]` in `brand-identity.yaml` per the brand-export convention (artifact = `playground-html`, status, last_exported, structural_check, verified_at).

## Critical invariants

- **Template-first**: never reconstruct the playground from scratch. The renderer fills placeholders, nothing else.
- **No restructuring**: section IDs, surface tab order, control-panel tab order, and CSS-variable names in `:root` are part of the contract. The structural validator enforces this.
- **Generic content**: hero copy and section labels read from `brand-extensions.yaml` when available; otherwise the template ships placeholder text that obviously wants replacing. Nothing in the template is Catalyne-flavored.

## Output summary

Print to the user:

```
playground.html written to ./brand-assets/playground.html ({size_kb} KB)
Surfaces: Marketing, App, Slide, Glossary
Compare-mode presets: {N} baked-in
Open in a browser to start tweaking. Share state via the URL hash.
```
