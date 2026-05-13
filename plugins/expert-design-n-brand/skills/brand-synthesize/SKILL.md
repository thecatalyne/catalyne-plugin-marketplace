---
name: brand-synthesize
description: "This skill should be used when the user asks to synthesize brand inputs, compare team discovery results, merge brand responses, resolve brand divergences, see where the team agrees or disagrees, or says \"brand-synthesize\". It compares multiple team members' brand discovery entries and produces a synthesis report."
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob"]
---

Entry point for brand synthesis — comparing team members' discovery inputs and producing a unified brand direction. Perform the full analysis directly.

## Startup

1. Read `brand-identity.yaml` from the current working directory. If it doesn't exist, inform the user: "No brand identity file found. Run /brand-discover first to start the discovery process."

2. Check discovery entries:
   - List all `discovery.*` entries and their statuses.
   - Count how many are `complete`.
   - If zero complete: "No completed discovery sessions found. At least one team member needs to finish /brand-discover first."
   - If one complete: "One discovery is complete ({name}). Synthesis works best with multiple perspectives, but I can analyze {name}'s responses for internal consistency. Want to proceed?"
   - If 2+ complete: Report who's finished and who hasn't. "Ready to synthesize {n} team members' inputs."

3. Check if synthesis has been run before:
   - If `synthesis.status` is `draft` or `review`: "A previous synthesis exists. Would you like to re-run it (this will overwrite the previous synthesis), or review the existing one?"
   - If `synthesis.status` is `complete`: "Synthesis is already marked complete. Would you like to re-run it with any new discovery data, or move on to /brand-build?"

## Analyst Behavior

After confirming the user wants to proceed, update `meta.phase` to `synthesis` and conduct the full analysis directly.

### Philosophy

Present the data fairly first, then offer expert interpretation. Never smooth over genuine disagreements — surface them clearly so the team can make informed decisions.

### Reference Loading

Load these before analysis:
- `${CLAUDE_PLUGIN_ROOT}/assets/techniques-registry.yaml` — canonical technique definitions, concept groups, YAML path mappings. You MUST consult this before rendering the Methods Used ledger or deciding which optional sections to include.
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/personality-dimensions.md` — for Aaker divergence thresholds
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/scoring-criteria.md` — for quality evaluation

### Phase 1: Data Collection

For each team member's discovery entry:
1. Record the complete `techniques_used[]` slugs from their discovery entry. These slugs MUST match registry slugs; if any don't, flag the discrepancy rather than silently dropping. This list drives the Methods Used ledger.
2. For each technique in the registry, check whether the participant's YAML has populated any of the technique's `yaml_paths`. Mark "Used" if yes, "—" if no. Do not infer "Used" from adjacent fields — only the technique's own paths count.
3. Extract positioning, personality, visual, voice, and stress-test data for each participant, keyed by the technique that produced it. This keeps the origin legible downstream.
4. Read `{name}-brand-quotes.md` if it exists in the working directory. These raw quotes supplement the YAML data with exact language, metaphors, and emotional texture that structured fields compress away. Use them as primary evidence when attributing positions in the report.

**Critical**: Do NOT coerce missing data into zeros. If a participant did not run Aaker Sliders, their Aaker row is "—", not a row of zeros. Zero-fills are indistinguishable from "scored 0" and corrupt the synthesis signal.

### Phase 2: Consensus Identification

For each dimension (positioning, personality, visual, voice):
1. Identify where team members agree (same archetype, similar Aaker scores, overlapping keywords, compatible color preferences).
2. Assess strength of agreement:
   - **Strong consensus**: Same or very similar answers with aligned reasoning
   - **Directional agreement**: Different words/techniques but pointing the same direction
   - **Weak consensus**: Superficial similarity that may mask different underlying motivations

Write consensus findings to `synthesis.consensus.{dimension}`.

### Phase 3: Divergence Identification

For each dimension:
1. Identify where team members disagree.
2. For each divergence, document:
   - **Dimension**: Which brand dimension
   - **Description**: Plain-language description of the disagreement
   - **Positions**: Each person's position WITH the evidence (quote their responses, reference their technique)
   - **Significance**: Why this divergence matters for design decisions
3. Score overall agreement (0.0-1.0) based on ratio of consensus to divergence, weighted by significance.

Write divergences to `synthesis.divergences[]`.

### Phase 4: Report Generation

Produce the report using `${CLAUDE_PLUGIN_ROOT}/assets/synthesis-report-template.md` as the exact structural scaffold. Section order, slug names, and heading hierarchy are fixed — do not rename or reorder anything. Optional sections render IFF at least one participant ran the driving technique (per registry `drives_sections`); otherwise they are omitted entirely. The Methods Used ledger (near the top) is mandatory and never omitted.

Polymorphic rule for the **Voice Constraints** section: the canonical heading is fixed. For each participant, render one italicized `*via {Technique Label}*` subblock per voice-constraint technique they ran (never-say-list, specificity-test, voice-card-sort). If a participant ran two voice-constraint techniques, they get two subblocks stacked under their name. If no participant ran any, omit the Voice Constraints section.

After presenting the report inline in the conversation, write the populated report to `brand-assets/synthesis-report.md` (create the directory if needed). Replace all `{{ }}` placeholders with actual values. For more than 2 participants, see the "Variable Participant Count" note below.



**Section 1: Neutral Report** (facts only)
- "Here's what each person said, dimension by dimension."
- Present each person's responses side by side.
- Note technique differences that may explain response differences.
- No interpretation, no judgment.

**Section 2: Opinionated Analysis** (expert interpretation)
- "Here's what the divergences mean and why they matter."
- For each significant divergence:
  - What design decisions does this affect?
  - Which position is better supported by brand strategy principles?
  - What's the risk of going either way?
  - Suggested resolution approach
- When quoting team members to support a position, prefer exact quotes from their `{name}-brand-quotes.md` file over paraphrased YAML summaries. Raw voice is more persuasive and precise than compressed data.
- Overall brand identity assessment using Paul Rand's criteria (from scoring-criteria.md)
- Specific recommendations for resolution

### Phase 5: Writing Results

1. Write all findings to `synthesis` section of `brand-identity.yaml`.
2. Populate `synthesis.methods_used[]` — one entry per (dimension, technique) pair in the registry, with `status` (used / inferred / —), `participants[]`, and optional `notes`. This backs the rendered ledger and is the durable machine-readable artifact.
3. Set `synthesis.status` to `draft`.
4. Set `synthesis.last_run` to current timestamp.
5. Calculate and set `synthesis.agreement_score`.
6. Confirm `brand-assets/synthesis-report.md` was written in Phase 4. Inform: "Synthesis report saved to `brand-assets/synthesis-report.md`."
7. Add changelog entry with action `synthesis_run`.

### Phase 6: Self-Verification (Mandatory)

Before declaring synthesis done, walk the relevant subset of the canonical
checklist (`${CLAUDE_PLUGIN_ROOT}/assets/export-verification-checklist.md`)
against `brand-assets/synthesis-report.md`. The report is markdown — no
screenshots needed, but every check must be grep-evidenced, not asserted.

**Sections to walk**: §1.2 (no `{{` left), §2 (Methods Used ledger correct),
§3 (polymorphic voice slot — heading, italic subtitles, omitted-when-empty),
§4 (variable-N: principle/palette/expressions row counts; formality
denominator), §11 (optional quality sections render IFF YAML populated).

**For each FAIL on first pass**: apply the auto-fix from the playbook
table at the bottom of the checklist (e.g., rebuild ledger from registry,
re-render polymorphic voice from concept-group declaration order, replace
hardcoded loop bound with `len(array)`). Re-write the affected section of
`synthesis-report.md`. Re-run the failed checks once.

**Hard cap**: one auto-fix pass. If a check still fails, surface it with a
specific recommended fix and stop.

**Reporting**: append a `## Verification` block at the end of
`synthesis-report.md` using the Reporting format from the checklist
(SUMMARY line + Failures + Warnings + Auto-fix log). Print the SUMMARY
line and any STILL-FAILs inline so the user sees them.

If FAIL count > 0 after the auto-fix pass: tell the user the synthesis
report is **blocked** and list the specific fixes needed. Do not move to
`/brand-build` until the report passes.

### Variable Participant Count

The template at `${CLAUDE_PLUGIN_ROOT}/assets/synthesis-report-template.md` shows two side-by-side columns as a reference shape. Extend it to as many columns as there are participants — there is no upper limit. Add one column per person to every comparison table. Keep the leftmost "Aspect" / "Dimension" column unchanged.

For the Aaker Scores table, the "Spread" column is `max − min` across all participants **who ran Aaker**. Participants who did not run Aaker are excluded from the spread calculation; they are not counted as zero. Their entire Aaker column is "—".

In the Divergences section, list every participant's position in the same evidence table — one row per person, not one row per pairwise comparison. Linear in N, never quadratic.

Do not collapse, summarize, or aggregate columns. Every participant gets their own column with their own answers — that is the standardization promise of this report.

### Handling Special Cases

**Solo user (1 discovery entry)**:
- Skip comparison. Instead, analyze internal consistency:
  - Do the positioning and personality align?
  - Do visual preferences match the stated personality?
  - Does the voice match the visual and personality choices?
- Produce a "self-consistency report" instead of a comparison.

**Incomplete entries**:
- Note which dimensions are incomplete for each person.
- Analyze what's available but flag gaps.

**Different techniques used**:
- This is expected — participants will often pick different techniques per dimension. The Methods Used ledger makes the differences transparent. Optional sections render only when at least one participant ran the technique; others see "—" in that column. Do NOT zero-fill or infer scores silently.
- Where the registry declares an inference edge (e.g. `archetype-selection.can_infer: [aaker-sliders]`), you MAY synthesize inferred Aaker values for an archetype-only participant — but ONLY if you mark them "Inferred" (not "Used") in the ledger, and ONLY if at least one other participant ran Aaker directly so the table has ground truth to anchor against. If you are the sole Aaker source, do not render the Aaker table at all.

## Resolution Flow

After presenting the report, if divergences exist, offer facilitated resolution:
1. Take one divergence at a time, starting with the most significant.
2. Present both positions with evidence.
3. Ask: "Which direction feels right? Or is there a middle ground?"
4. If they resolve it: update `synthesis.divergences[].resolved = true`, add resolution, resolver, timestamp.
5. If they want to discuss with the team: note it as unresolved and move on.

Do not average or split the difference silently. Every resolution should be an explicit, attributed decision.

### Critical Rules

- **Neutral first, opinionated second.** Always present the data before interpreting it.
- **Evidence-based.** Every claim references specific responses from specific people.
- **Attribute everything.** "{participant_name} said X (via archetype selection)" not just "the team said X."
- **Don't smooth over disagreements.** Surface them clearly. Healthy conflict produces better brands.
- **Write incrementally.** Save to YAML as you go, not just at the end.
