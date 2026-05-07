---
name: brand-knowledge
description: "This skill should be used when discussing brand personality, Jungian archetypes, Aaker personality dimensions, logo types or the logo design process, icon systems, illustration style, voice-to-component copy mapping, brand quality evaluation (Paul Rand criteria), archetype blending, personality-to-design mapping, or when the user asks 'what archetype is my brand' or 'how do I evaluate brand identity quality.'"
allowed-tools: ["Read", "Grep", "Glob"]
---

Reference library for brand identity theory and evaluation. Load the relevant reference when working on brand-related tasks.

## Available References

### Archetype Profiles
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/archetype-profiles.md`
**When to load**: During personality discovery (archetype selection technique), when explaining archetypes, when blending primary/secondary archetypes, or when someone asks "what archetype is my brand?"

Covers all 12 Jungian archetypes with: core desire, brand promise, voice characteristics, visual associations, strengths/risks, brand examples, key diagnostic question, and common archetype blends.

### Personality Dimensions
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/personality-dimensions.md`
**When to load**: During personality discovery (Aaker spectrum sliders technique), when scoring or comparing personality profiles, when mapping personality to design decisions, or during synthesis when analyzing divergences.

Covers Aaker's 5 dimensions (Sincerity, Excitement, Competence, Sophistication, Ruggedness) with: scoring guides, visual implications, voice implications, profile shape patterns, and divergence analysis thresholds.

### Scoring Criteria
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/scoring-criteria.md`
**When to load**: During synthesis quality checks, after design system build, before export, or when evaluating brand identity quality.

Covers: Paul Rand's 7 criteria for brand identity quality, design system coherence framework (alignment scoring), and brand effectiveness metrics.

### Logo Design & Mark-Making
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/logo-and-marks.md`
**When to load**: During visual discovery when discussing how the brand will visually manifest, when users ask about logo types or the logo design process, during synthesis when logo direction is a divergence point, or during build when the design system needs to harmonize with the logo.

Covers: 7 logo types with strategic guidance, responsive logo systems, file format requirements, the professional design process, common startup mistakes, and how the logo relates to the design system.

### Iconography & Illustration
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/iconography-and-illustration.md`
**When to load**: During build when defining the visual asset standards, during export when documenting brand guidelines, or when users ask about icon libraries, illustration styles, or custom vs. licensed assets.

Covers: Icon grid systems, illustration style variables, custom-vs-licensed decision framework, personality-to-icon/illustration mapping, and documentation templates for contractors.

### Voice-to-Component Patterns
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/voice-component-patterns.md`
**When to load**: During build when generating voice guidelines, during export when rendering the LLM operating manual's `voice.implementation` block, or when mapping Aaker scores / formality scores to concrete UI copy patterns (buttons, form labels, empty states, confirmations).

Covers: formality score → copy register mapping, Aaker Sincerity/Excitement/Competence → pronouns/verbs/specificity, never-say list substitution flow, component-by-component defaults, and the specificity test that every string must pass.

## Usage Rules

- Read the specific reference file needed — do not load all five unless the task requires it.
- These references inform conversation and evaluation. They are not scripts to read aloud.
- Present frameworks conversationally, adapted to the user's thinking style.
- When citing specific scores or criteria, reference them naturally ("Rand would ask: is it distinctive?"), not academically.
