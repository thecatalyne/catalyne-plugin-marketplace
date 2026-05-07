# {{ brand_name }} — Synthesis Report

> Comparing {{ participant_count }} team member(s)' brand discovery inputs.
> Generated: {{ timestamp }}

---

## Methods Used

*This ledger shows every technique registered in `techniques-registry.yaml`
and whether each participant ran it. Use it to distinguish "scored low" from
"not collected" — a dash (—) means the technique was not used by that person.*

| Dimension | Technique | {{ participant_1 }} | {{ participant_2 }} | … |
|---|---|:---:|:---:|:---:|
| Positioning | Elevator Pitch | {{ p1_elevator }} | {{ p2_elevator }} | … |
| Positioning | Wolff-Olins Butterfly | {{ p1_butterfly }} | {{ p2_butterfly }} | … |
| Positioning | Landscape Grid | {{ p1_landscape }} | {{ p2_landscape }} | … |
| Positioning | Brand Eulogy | {{ p1_eulogy }} | {{ p2_eulogy }} | … |
| Positioning | Competitive Mapping | {{ p1_competitive }} | {{ p2_competitive }} | … |
| Personality | Archetype Selection | {{ p1_archetype }} | {{ p2_archetype }} | … |
| Personality | Aaker Sliders | {{ p1_aaker }} | {{ p2_aaker }} | … |
| Personality | Tension Spectrum Mapping | {{ p1_tensions }} | {{ p2_tensions }} | … |
| Personality | Keyword Distillation | {{ p1_keywords }} | {{ p2_keywords }} | … |
| Personality | Metaphors | {{ p1_metaphors }} | {{ p2_metaphors }} | … |
| Visual | Palette Recognition | {{ p1_palette }} | {{ p2_palette }} | … |
| Visual | Type Pairing | {{ p1_type }} | {{ p2_type }} | … |
| Visual | Form Language | {{ p1_form }} | {{ p2_form }} | … |
| Visual | Anti-Inspiration | {{ p1_anti }} | {{ p2_anti }} | … |
| Visual | Texture & Material | {{ p1_texture }} | {{ p2_texture }} | … |
| Voice | Sample Writing | {{ p1_samples }} | {{ p2_samples }} | … |
| Voice | Formality Spectrum | {{ p1_formality }} | {{ p2_formality }} | … |
| Voice | Never-Say List | {{ p1_never_say }} | {{ p2_never_say }} | … |
| Voice | Specificity Test | {{ p1_specificity }} | {{ p2_specificity }} | … |
| Voice | Voice Card Sort | {{ p1_card_sort }} | {{ p2_card_sort }} | … |
| Stress | Pre-Mortem | {{ p1_premortem }} | {{ p2_premortem }} | … |
| Stress | Inversion | {{ p1_inversion }} | {{ p2_inversion }} | … |
| Stress | Stakeholder Lens | {{ p1_stakeholder }} | {{ p2_stakeholder }} | … |
| Stress | Time Travel | {{ p1_timetravel }} | {{ p2_timetravel }} | … |

*Cells use "Used" when the participant completed that technique, or "—" when
they did not. If every participant shows "—" for a technique, the
corresponding section below is omitted.*

---

## Section 1: Neutral Report

*Facts only. No interpretation. Each person's responses side by side. Sections
below are rendered only if at least one participant ran the driving technique;
omitted sections are marked "—" in the Methods Used ledger above.*

### Positioning

#### Elevator Pitch

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Elevator Pitch | {{ p1_pitch }} | {{ p2_pitch }} | … |
| Differentiator | {{ p1_diff }} | {{ p2_diff }} | … |

#### Wolff-Olins Butterfly *(optional — omit if no participant ran this)*

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Special (what only you can do) | {{ p1_special }} | {{ p2_special }} | … |
| World needs | {{ p1_needs }} | {{ p2_needs }} | … |
| Magic overlap | {{ p1_overlap }} | {{ p2_overlap }} | … |

For participants who did not run Butterfly: row cells show "—".

#### Landscape Grid *(optional)*

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Placement | {{ p1_grid_xy }} | {{ p2_grid_xy }} | … |
| Reasoning | {{ p1_grid_reason }} | {{ p2_grid_reason }} | … |

#### Brand Eulogy *(optional)*

| {{ participant_1 }} | {{ participant_2 }} | … |
|---|---|---|
| {{ p1_eulogy_text }} | {{ p2_eulogy_text }} | … |

#### Competitive Mapping *(optional)*

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Competitors | {{ p1_competitors }} | {{ p2_competitors }} | … |
| Axis of differentiation | {{ p1_axis }} | {{ p2_axis }} | … |

---

### Personality Profile

*Canonical heading. Each participant's sub-block below is tagged with the
technique they used (archetype / Aaker / tensions). Multiple techniques for
a single participant stack as separate sub-blocks.*

#### Archetypes *(via Archetype Selection, optional)*

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Primary archetype | {{ p1_archetype_1 }} | {{ p2_archetype_1 }} | … |
| Secondary archetype | {{ p1_archetype_2 }} | {{ p2_archetype_2 }} | … |
| Reasoning | {{ p1_archetype_reason }} | {{ p2_archetype_reason }} | … |

#### Aaker Scores *(via Aaker Spectrum Sliders, optional)*

*Render only for participants who ran Aaker. For others, show "—" in the entire
column. If no participant ran Aaker, omit this entire sub-section.*

| Dimension | {{ participant_1 }} | {{ participant_2 }} | … | Spread |
|-----------|---------------------|---------------------|---|:------:|
| Sincerity | {{ p1_sincerity }} | {{ p2_sincerity }} | … | {{ spread_sincerity }} |
| Excitement | {{ p1_excitement }} | {{ p2_excitement }} | … | {{ spread_excitement }} |
| Competence | {{ p1_competence }} | {{ p2_competence }} | … | {{ spread_competence }} |
| Sophistication | {{ p1_sophistication }} | {{ p2_sophistication }} | … | {{ spread_sophistication }} |
| Ruggedness | {{ p1_ruggedness }} | {{ p2_ruggedness }} | … | {{ spread_ruggedness }} |

*Spread = max − min across all participants who ran Aaker. Participants who did not run Aaker are excluded from the spread calculation, not counted as 0.*

#### Tension Spectrums *(via Tension Spectrum Mapping, optional)*

| Axis | {{ participant_1 }} | {{ participant_2 }} | … |
|------|---------------------|---------------------|---|
| {{ axis_1 }} | {{ p1_axis_1 }} | {{ p2_axis_1 }} | … |
| {{ axis_2 }} | {{ p1_axis_2 }} | {{ p2_axis_2 }} | … |

*Participants may mark an axis as "not a tension" when they see the two
anchors as synergistic rather than opposing. Preserve that signal verbatim.*

#### Keywords & Metaphors

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Keywords | {{ p1_keywords }} | {{ p2_keywords }} | … |
| Metaphors | {{ p1_metaphor_list }} | {{ p2_metaphor_list }} | … |

---

### Visual

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Resonating palettes | {{ p1_palettes }} | {{ p2_palettes }} | … |
| Rejected palettes | {{ p1_rejected }} | {{ p2_rejected }} | … |
| Typography preference | {{ p1_type }} | {{ p2_type }} | … |
| Form language | {{ p1_form }} | {{ p2_form }} | … |

#### Anti-Inspiration *(optional)*

| {{ participant_1 }} | {{ participant_2 }} | … |
|---|---|---|
| {{ p1_anti_list }} | {{ p2_anti_list }} | … |

#### Texture & Material *(optional)*

| {{ participant_1 }} | {{ participant_2 }} | … |
|---|---|---|
| {{ p1_texture_text }} | {{ p2_texture_text }} | … |

---

### Voice

#### Formality *(optional)*

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Score | {{ p1_formality_score }} / {{ p1_formality_max }} | {{ p2_formality_score }} / {{ p2_formality_max }} | … |
| Context drift (if noted) | {{ p1_formality_drift }} | {{ p2_formality_drift }} | … |

*Each participant's score is rendered on their own scale (e.g. `3/5` or `4/10`).
Do not rescale to a single shared scale; the original instrument is the data.*

#### Voice Constraints *(canonical heading; subblocks vary by technique)*

*For each participant, render a subblock per technique they ran — tagged with
an italic subtitle. At least one of never-say-list, specificity-test, or
voice-card-sort must be present for this section to render; otherwise the
whole section is omitted.*

**{{ participant_1 }}** — *via {{ p1_voice_technique_label }}*

{{ p1_voice_constraint_content }}

**{{ participant_2 }}** — *via {{ p2_voice_technique_label }}*

{{ p2_voice_constraint_content }}

*For participants who ran multiple voice-constraint techniques (e.g. both
specificity-test AND card-sort), repeat the subblock once per technique.*

#### Sample Writing *(optional)*

| Prompt | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| Tweet | {{ p1_tweet }} | {{ p2_tweet }} | … |
| Apology | {{ p1_apology }} | {{ p2_apology }} | … |
| Celebration | {{ p1_celebration }} | {{ p2_celebration }} | … |

---

### Stress Tests *(entire section optional — omit if no stress test was run)*

Render only sub-sections for stress tests at least one participant ran.

#### Pre-Mortem *(optional)*

| {{ participant_1 }} | {{ participant_2 }} | … |
|---|---|---|
| {{ p1_premortem_text }} | {{ p2_premortem_text }} | … |

#### Inversion *(optional)*

| {{ participant_1 }} | {{ participant_2 }} | … |
|---|---|---|
| {{ p1_inversion_text }} | {{ p2_inversion_text }} | … |

#### Stakeholder Lens *(optional)*

| View | {{ participant_1 }} | {{ participant_2 }} | … |
|------|---------------------|---------------------|---|
| Skeptic | {{ p1_skeptic }} | {{ p2_skeptic }} | … |
| Supporter | {{ p1_supporter }} | {{ p2_supporter }} | … |
| Compatible? | {{ p1_compatible }} | {{ p2_compatible }} | … |

#### Time Travel *(optional)*

| Aspect | {{ participant_1 }} | {{ participant_2 }} | … |
|--------|---------------------|---------------------|---|
| 3-year future | {{ p1_future }} | {{ p2_future }} | … |
| What evolved | {{ p1_evolved }} | {{ p2_evolved }} | … |
| What stayed | {{ p1_stayed }} | {{ p2_stayed }} | … |

---

## Section 2: Opinionated Analysis

*Expert interpretation. What the data means and why it matters.*

### Agreement Score: {{ agreement_score }} / 1.0

{{ agreement_interpretation }}

### Consensus

{{ consensus_summary }}

### Divergences

For each divergence, list every participant's position in the same evidence
table — one row per person, not one row per pairwise comparison. Linear in N,
never quadratic.

#### Divergence 1: {{ divergence_1_title }}

**Dimension**: {{ divergence_1_dimension }}
**Description**: {{ divergence_1_description }}

| Participant | Position | Evidence |
|---|---|---|
| **{{ participant_1 }}** | {{ p1_position }} | {{ p1_evidence }} |
| **{{ participant_2 }}** | {{ p2_position }} | {{ p2_evidence }} |
| … | … | … |

**Why this matters**: {{ divergence_1_significance }}
**Recommendation**: {{ divergence_1_recommendation }}

*(Repeat one subsection per divergence.)*

---

### Quality Check (Paul Rand Criteria)

| Criterion | Score | Notes |
|-----------|:---:|-------|
| Distinctive | {{ score_distinctive }} | {{ note_distinctive }} |
| Memorable | {{ score_memorable }} | {{ note_memorable }} |
| Simple | {{ score_simple }} | {{ note_simple }} |
| Appropriate | {{ score_appropriate }} | {{ note_appropriate }} |
| Timeless | {{ score_timeless }} | {{ note_timeless }} |
| Legible | {{ score_legible }} | {{ note_legible }} |
| Reducible to essence | {{ score_reducible }} | {{ note_reducible }} |

**Overall direction assessment**: {{ overall_assessment }}

### Recommended Next Steps

1. {{ next_step_1 }}
2. {{ next_step_2 }}
3. {{ next_step_3 }}

---

*Generated by expert-design-n-brand &middot; {{ timestamp }}*
