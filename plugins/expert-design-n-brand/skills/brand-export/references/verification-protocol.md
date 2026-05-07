# Self-Verification Protocol

Loaded by `brand-export/SKILL.md` at two points: (1) at startup, to load the data contract; (2) after all artifacts are written, to run the verification checklist. Producing artifacts is only half the job — every export ends with the render → verify flow below.

References (load before starting):
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/build-export-contract.md` — canonical data contract (Required-atomic + Required-v6 fields, optional fields, enforcement rules)
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/rendering-rules.md` — cross-artifact render rules, including Rule 0 (template-first rendering) and the Tier 1 external-facing principle
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/artifacts.md` — tier-classified catalog
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-export/references/artifact-schemas.yaml` — structural oracle consumed by the validator in Step S
- `${CLAUDE_PLUGIN_ROOT}/assets/export-verification-checklist.md` — the quality gates

## Phase structure

```
Startup → Contract-validate input (Step 0)
         ↓
      Render each artifact in the requested bundle
         cp template → fill placeholders → write → Step S (validate structure, 1-pass auto-fix) → log to export_log[]
         ↓  (repeat per artifact)
      Screenshot + visual verification (Step A)      ← runs once, after the bundle finishes
         ↓
      Walk checklist (Step B) — every gate is PASS/FAIL, no WARN
         ↓
      Auto-fix any FAIL once (Step C) if playbook entry exists
         ↓
      Re-verify failed gates after fix
         ↓
      Write report to _build/export-verification.md (Step D)
         ↓
      Surface summary to user; advisory-flag any remaining FAILs (run does not block on advisory fails)
```

**Step S and Step C are distinct auto-fix passes.** Step S targets *structural shape* (section IDs, required classes, JSON keys, CSS variables — the oracle in `artifact-schemas.yaml`) and runs per-artifact during rendering. Step C targets *checklist-gate failures* (content presence, contrast, prose tone, cross-artifact consistency) and runs once at the end. Each may trigger one re-render pass; they don't compound.

## Step 0 — Contract validation at startup

Before rendering any artifact, walk the contract:

1. Load `build-export-contract.md`.
2. For every Required-atomic path, confirm presence and valid type/shape in `brand-identity.yaml`.
3. For every Required-v6 path, same.
4. For Legacy-compat shapes, normalize in-memory. Log each normalization as INFO.
5. If any Required-atomic or Required-v6 field is missing or invalid: HARD-FAIL at startup with a diagnostic citing the specific field, the contract section, and "run brand-build to populate before re-trying /brand-export."

Do NOT auto-compose Required-v6 fields at export time. That's brand-build's responsibility. Export is a rendering step, not a data-generation step.

## Step S — Structural validation (per artifact, during rendering)

Runs inside the render loop, immediately after each artifact is written (see `brand-export/SKILL.md` Rendering step 8). Not a separate phase — documented here because it's the checkpoint that keeps template-fidelity honest.

1. After `Write` completes for artifact X, invoke:

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/validate-structure.py \
     --artifact ./brand-assets/<filename> \
     --schema <oracle-key>
   ```

   The oracle key is the artifact's canonical slug (see `artifact-schemas.yaml`): `brand-guidelines`, `tokens-css`, `theme-figma`, etc.

2. Parse the JSON verdict from stdout:

   ```json
   {
     "artifact": "./brand-assets/brand-guidelines.html",
     "schema": "brand-guidelines",
     "type": "html",
     "passed": true | false,
     "checks": [
       {"name": "required_sections", "result": "pass" | "fail", "detail": {...}},
       ...
     ]
   }
   ```

3. **If `passed: false`**, run exactly one re-render pass of this single artifact — start again from Rendering step 2 (`cp` the template, fill placeholders). Re-invoke the validator.

4. Append an entry to `system.quality.export_log[]` with the final outcome:

   ```yaml
   - artifact: "brand-guidelines.html"
     status: "rendered"                    # rendered | failed | skipped
     last_exported: "<ISO-8601 UTC>"
     structural_check: "pass" | "fail"
     auto_fix_attempted: true | false
     structural_check_after_fix: "pass" | "fail" | null
     verified_at: "<ISO-8601 UTC>"
   ```

5. **Continue the bundle** even if the final structural_check is "fail". Step S is advisory — it flags the problem, logs it, and lets the run finish. Step B (below) will surface it again when the full checklist walks.

**No oracle entry?** If `artifact-schemas.yaml` has no entry for the artifact (rare — typically only for brand-new artifacts mid-authoring), skip Step S for that artifact and log `structural_check: not_applicable`. Add an oracle entry in a follow-up change; do not fabricate one at export time.

**Oracle entry authoring rule**: the oracle is derived from the TEMPLATE, not from an existing rendered output. A rendered output that diverges from the template is the *problem* Step S is meant to catch — using it as the oracle would bake drift into the contract.

## Step A — Render screenshots

Visual checks (font fidelity, contrast badges, components in palette, spacing-as-blocks, per-section chips, gradient library strips) require pixels. Produce screenshots before walking the checklist.

```bash
mkdir -p _build/verification
```

PDF pages → images. Probe in order:

1. `pdftoppm -r 144 -png <pdf> _build/verification/<prefix>-page` (preferred — requires `poppler`)
2. Headless Chromium `--screenshot` per page
3. macOS `sips -s format png`

Interactive HTML → full-page screenshot. Probe for a headless-capable browser in order:

```bash
BROWSER_BIN=""
for CAND in chromium google-chrome chrome chrome-browser msedge; do
  if command -v "$CAND" >/dev/null 2>&1; then BROWSER_BIN="$CAND"; break; fi
done
# Fallback: respect user-set $BROWSER only if it resolves to an executable.
if [[ -z "$BROWSER_BIN" && -n "${BROWSER:-}" ]] && command -v "$BROWSER" >/dev/null 2>&1; then
  BROWSER_BIN="$BROWSER"
fi

if [[ -n "$BROWSER_BIN" ]]; then
  for FILE in brand-guidelines brand-methods; do
    "$BROWSER_BIN" --headless --disable-gpu \
      --virtual-time-budget=5000 \
      --window-size=1200,2400 \
      --screenshot="_build/verification/${FILE}-full.png" \
      "file://$PWD/${FILE}.html"
  done
fi
```

If no screenshot tool is available: mark all visual items FAIL with a note "could not screenshot — install poppler or chromium for pixel verification" — do NOT soft-skip. The checklist is hard-fail-only.

## Step B — Walk the checklist

Walk every applicable gate. For each gate:

- Cite specific evidence: file path + grep pattern, or screenshot region.
- Mark **PASS** or **FAIL** only. (The rewritten checklist deprecated WARN — every gate is hard.)
- Use Read to actually inspect screenshots; don't infer from source. Particularly for visual gates (font rendering in PDF, component/hero color, badge colors, spacing blocks, chip rendering, gradient strips, contrast badges in palette).

Track the result set. Don't write the report yet.

## Step C — Auto-fix (bounded, one pass only)

For each FAIL with an entry in the checklist's **Auto-fix playbook**:

1. Apply the first-pass fix to the source template or rendered file.
2. Re-render only the affected artifact(s).
3. Re-run only the failed checks against the re-rendered artifacts.
4. Mark each as `PASS-after-fix` or `STILL-FAIL`.

**Hard cap**: one auto-fix pass per failed gate. No second attempt. If STILL-FAIL, report it.

For FAILs with no playbook entry: skip auto-fix; report directly.

## Step D — Write the report

1. Write `_build/export-verification.md` following the **Reporting format** at the bottom of the checklist. Include the auto-fix log, the palette-normalization log (INFO entries from Step 0), and the contract-validation log.
2. Add a `system.quality.export_verification` block to `brand-identity.yaml`: `{timestamp, summary: "PASS N · FAIL N", acceptance, auto_fix_passes, normalizations_applied}`.
3. Add a changelog entry with action `export_verification_run`.
4. Print the SUMMARY line and any STILL-FAILs inline so the user sees them immediately.
5. If FAIL count > 0: tell the user acceptance is **blocked**, list specific recommended fixes. Do not pretend success.
6. If all PASS: confirm artifacts are ready. Point to `_build/export-verification.md` for the full audit trail (the verification report is a build artifact — not a user-facing deliverable).

## Final report template

```
Brand system exported. Tier 1 artifacts (shipping, public-facing):
  Canonical documents:
    - brand-guidelines.html        ({size})        ← the definitive brand guide
    - brand-guidelines.pdf         ({size}, {pages} pages)
    - brand-quickref.md            ({lines} lines)
  Tokens:
    - tokens.css                   ({size})
    - tokens.json                  ({size})
  Identity + visual:
    - logo-construction.svg        ({size})
    - illustration-system.html     ({size})
    - photography-reference-grid.html ({size})
  Platform & themes:
    - platform-matrix.md               ({size})  ← single consolidated cross-surface reference
    - tailwind.config.js
    - theme-figma.json
    - email-template.html
  Governance:
    - governance.md                ({lines} lines)

Tier 2 artifacts (operator / process record):
    - brand-methods.html           ({size})
    - brand-methods.pdf            ({size}, {pages} pages)
    - synthesis-report.md          ({size}) {{ if synthesize was run }}
    (Per-participant `*-brand-quotes.md` files remain in the working directory.)

Tier 3 artifacts (LLM-optimized sibling):
    - brand.md                     ({size})        ← brand.md v0.2.0 spec
    - brand.extensions.yaml        ({size})

Contract validation: {N} Required-atomic paths OK · {N} Required-v6 paths OK · {N} legacy shapes normalized
Verification: PASS {N} · FAIL {N}   (auto-fix passes: 0 or 1)
Acceptance: {ready | blocked-on-N-fails}
{If blocked: list each FAIL with the recommended fix.}
```

The user-facing output folder contains only Tier 1 + Tier 2 + Tier 3. Internal artifacts (`_build/export-verification.md`, any failed-render artifacts, old-format legacy files during migration) stay in `_build/` and are not part of the shipping set.
