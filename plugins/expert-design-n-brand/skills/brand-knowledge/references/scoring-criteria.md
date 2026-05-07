# Brand & Design Quality Scoring Criteria

Frameworks for evaluating brand identity quality, design system coherence, and overall brand effectiveness. Used during synthesis to assess where the brand stands and during build to validate design system output.

## How to Use This Reference

- **After synthesis**: Score the emerging brand identity against Rand's criteria to identify weak spots before building the design system.
- **After design system build**: Score the design system against the coherence framework to validate internal consistency.
- **When presenting to stakeholders**: Use the effectiveness metrics to frame what "good" looks like.

---

## 1. Paul Rand's 7 Criteria for Brand Identity Quality

Paul Rand (designer of the IBM, UPS, and ABC logos) proposed seven tests for evaluating brand identity. Adapted here for full brand systems, not just logos.

### The Seven Tests

#### 1. Distinctive
**Question**: Would someone recognize this brand from a fragment?
**Scoring (1-10)**:
- 1-3: Generic — could be any company in the category
- 4-6: Has some recognizable elements but relies on the name
- 7-8: Distinctive palette/voice/form that's identifiable without the name
- 9-10: Iconic — a color, shape, or phrase instantly signals the brand

**How to evaluate**: Cover the brand name. Can you still tell whose it is from the colors, typography, and voice alone?

#### 2. Visible
**Question**: Does it work at every scale and context?
**Scoring (1-10)**:
- 1-3: Only works in one context (web-only, print-only)
- 4-6: Works in primary contexts but breaks in others
- 7-8: Consistent across digital, print, small, large
- 9-10: Unmistakable at favicon size and billboard size

**How to evaluate**: Test the design system at extremes — 16px favicon, mobile screen, A0 poster, black-and-white print.

#### 3. Adaptable
**Question**: Can it evolve without losing identity?
**Scoring (1-10)**:
- 1-3: Rigid — any change breaks it
- 4-6: Can handle minor variations
- 7-8: Has a flexible system that accommodates new contexts
- 9-10: Built for evolution — has clear invariants and clear flex points

**How to evaluate**: Imagine the brand in 3 new contexts it hasn't been designed for. Does the system give you enough to work with?

#### 4. Memorable
**Question**: Can someone describe it from memory?
**Scoring (1-10)**:
- 1-3: Forgettable — nothing sticks
- 4-6: One or two elements are remembered
- 7-8: The overall feeling and key elements persist
- 9-10: People can draw it, quote it, describe it accurately from memory

**How to evaluate**: Show someone the brand for 30 seconds. Ask them to describe it 10 minutes later. What did they remember?

#### 5. Universal
**Question**: Does it work across cultures and contexts?
**Scoring (1-10)**:
- 1-3: Culture-specific or niche to the point of alienation
- 4-6: Works in its primary market
- 7-8: Translates across cultures with minor adaptation
- 9-10: Transcends cultural boundaries (like Nike's swoosh)

**How to evaluate**: Consider your target audience diversity. Would the brand identity make sense to all segments?

#### 6. Timeless
**Question**: Will it look dated in 5 years?
**Scoring (1-10)**:
- 1-3: Follows current trends closely — will feel dated soon
- 4-6: Mix of timeless and trendy elements
- 7-8: Grounded in principles that outlast trends
- 9-10: Classic — could have been designed 10 years ago or 10 years from now

**How to evaluate**: Identify which elements follow current design trends. If you removed all trend-dependent choices, what remains?

#### 7. Simple
**Question**: Can you describe the brand identity in one sentence?
**Scoring (1-10)**:
- 1-3: Requires a paragraph to explain what the brand is about
- 4-6: Can be explained but requires some setup
- 7-8: One sentence captures the essence
- 9-10: One word or image captures it (like Apple = simplicity)

**How to evaluate**: Try to describe the brand identity to someone who's never seen it, in one sentence. If you can't, it's not simple enough.

### Scoring Summary

| Score Range | Overall Quality |
|-------------|----------------|
| 49-70 | Exceptional — rare for early-stage brands |
| 35-48 | Strong — solid foundation to build on |
| 21-34 | Developing — clear areas for improvement |
| 7-20 | Needs significant work |

**Target for first build**: 28-42 (developing to strong). Perfect scores come from years of iteration, not first attempts.

---

## 2. Design System Coherence Framework

Evaluates whether the design system's parts work together as a unified whole.

### Internal Consistency (does everything agree?)

#### Color-Personality Alignment
**Question**: Do the color choices reflect the personality scores?
- High sincerity + cold blue palette = misalignment
- High excitement + muted earth tones = misalignment
- High sophistication + neon palette = misalignment

**Scoring (1-5)**:
- 1: Colors contradict personality
- 3: Colors are neutral (don't contradict but don't reinforce)
- 5: Colors are a direct expression of the personality

#### Typography-Voice Alignment
**Question**: Does the type selection match the brand voice?
- Formal voice + playful rounded sans = misalignment
- Casual voice + traditional serif = misalignment
- Bold voice + thin weight = misalignment

**Scoring (1-5)**:
- 1: Type contradicts voice
- 3: Type is neutral
- 5: Type reinforces and embodies the voice

#### Form-Energy Alignment
**Question**: Does the form language match the brand energy?
- High excitement + static, symmetrical layouts = misalignment
- High ruggedness + delicate, rounded forms = misalignment
- High sophistication + busy, dense compositions = misalignment

**Scoring (1-5)**:
- 1: Forms contradict energy
- 3: Forms are neutral
- 5: Forms embody the brand energy

#### Voice-Visual Harmony
**Question**: If you read the voice guidelines and then looked at the visuals without labels, would they feel like the same brand?

**Scoring (1-5)**:
- 1: Voice and visuals seem like different brands
- 3: No obvious conflict but no obvious harmony
- 5: Voice and visuals feel like natural extensions of each other

### Practical Utility (can someone use this?)

#### Token Completeness
**Question**: Could a developer implement a full page using only the design tokens?
- Missing sizes, spacing, or color values = incomplete
- Missing responsive behavior = incomplete
- Ambiguous naming = incomplete

**Scoring (1-5)**:
- 1: Major gaps — developer would have to invent values
- 3: Core values present, some gaps in edge cases
- 5: Comprehensive — developer can build confidently

#### Decision Support
**Question**: When facing an unstated design decision, do the principles provide enough guidance?
- "Should this button be rounded or square?" — do the principles answer this?
- "Should this error message be formal or casual?" — do the voice guidelines answer this?

**Scoring (1-5)**:
- 1: Principles are too vague to guide decisions
- 3: Principles help with some decisions but not edge cases
- 5: Principles provide clear guidance for novel situations

### Coherence Score

| Score Range | Interpretation |
|-------------|---------------|
| 25-30 | Exceptional coherence — unified system |
| 18-24 | Strong — minor inconsistencies |
| 12-17 | Developing — some misalignments to address |
| 6-11 | Needs work — significant internal contradictions |

---

## 3. Brand Effectiveness Metrics

Higher-level measures of whether the brand identity achieves its goals. Less about design quality, more about strategic fit.

### Differentiation
**Question**: In a lineup of competitors, would this brand stand out?
- List 3-5 direct competitors. If you swapped the brand identity onto any of them, would it still work? If yes, differentiation is low.

### Audience Fit
**Question**: Would the target audience feel this brand is "for them"?
- Consider demographics, psychographics, and cultural context
- A brand for young developers should feel different from a brand for enterprise CFOs

### Strategic Alignment
**Question**: Does the identity support the business strategy?
- If the strategy is premium pricing, does the identity feel premium?
- If the strategy is accessibility, does the identity feel approachable?
- If the strategy is disruption, does the identity feel bold?

### Internal Adoption
**Question**: Would the team actually use and maintain this system?
- Overly complex systems get abandoned
- Systems that don't match how the team works get ignored
- The best system is one the team will actually follow

---

## Applying Scores During the Plugin Workflow

### After Synthesis (`/brand-synthesize`)
Run a quick Rand's 7 assessment on the emerging brand direction:
- Focus on Distinctive, Simple, and Memorable
- Low scores here suggest the synthesis needs more refinement before building

### After Build (`/brand-build`)
Run the full coherence framework:
- Check all alignment scores
- Flag any dimension scoring below 3
- Use misalignments as specific, actionable revision targets

### Before Export (`/brand-export`)
Final quality gate:
- Rand's 7 total should be 28+ (developing or better)
- Coherence total should be 18+ (strong or better)
- Any individual Rand criterion below 4 should be flagged as an area for future iteration
