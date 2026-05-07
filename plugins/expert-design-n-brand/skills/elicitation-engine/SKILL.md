---
name: elicitation-engine
description: "This skill should be used when conducting brand discovery sessions, choosing elicitation techniques, running brand exercises (archetype card sort, personality sliders, palette recognition, voice calibration), navigating interview traps, or when the user asks about brand positioning, personality, visual preferences, or voice discovery techniques."
allowed-tools: ["Read", "Grep", "Glob"]
---

Core engine for brand discovery sessions. Provides the technique library, curated recognition options, brand strategy frameworks, and trap navigation patterns.

## Available References

### Technique Library
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/technique-library.md`
**When to load**: At the start of any discovery session. Contains all techniques organized by dimension (positioning, personality, visual, voice) with full instructions, writes-to fields, and interviewer notes.

### Curated Option Sets
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/curated-option-sets.md`
**When to load**: During visual recognition exercises (palette recognition, type pairing recognition), voice card sort, archetype quick selection, or formality spectrum calibration. Contains specific hex palettes, Google Font pairings, voice examples, and archetype quick cards.

### Brand Frameworks
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/brand-frameworks.md`
**When to load**: When explaining brand strategy concepts, when a technique references a framework (Wolff Olins, Aaker, Neumeier), or when grounding analysis in professional methodology.

### Trap Navigation
**File**: `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/trap-navigation.md`
**When to load**: At the start of any discovery session (alongside technique library). Contains 10 common elicitation traps with recognition signals and specific redirect phrases.

## Usage Notes

- Present 2-3 recommended techniques per dimension based on cognitive style. Minimum 2 per dimension for triangulated signal.
- Always let the person choose — recommendations, not prescriptions.
- Record which techniques were used in `discovery.{name}.techniques_used`.
