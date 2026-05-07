# Design Rules

Concrete rules for color, typography, motion, and composition in design systems. These rules translate brand personality into implementable constraints.

## Color Rules

### The 60-30-10 Rule

Apply colors in a hierarchy:
- **60% — Background/dominant**: The color that covers most surface area. Usually the lightest or most neutral color. Sets the overall mood.
- **30% — Primary/supporting**: The main brand color. Used for major UI elements, headers, cards, sections.
- **10% — Accent**: The pop of contrast. Used for CTAs, highlights, badges, key interactions.

This ratio creates visual harmony. Breaking it intentionally (e.g., dark mode with 60% dark) changes the mood.

### WCAG Contrast Requirements

All text must meet minimum contrast ratios:

| Standard | Ratio | When |
|----------|-------|------|
| AA Normal text | 4.5:1 | Body text (under 18pt regular, under 14pt bold) |
| AA Large text | 3:1 | Headings (18pt+ regular, 14pt+ bold) |
| AAA Normal text | 7:1 | Enhanced accessibility target |
| AAA Large text | 4.5:1 | Enhanced accessibility target |
| Non-text UI | 3:1 | Icons, borders, form controls against background |

**Checking contrast**: Use the `${CLAUDE_PLUGIN_ROOT}/scripts/validate-contrast.sh` script to check hex value pairs.

**Common failures**:
- Light grey text on white (`#999 on #FFF` = 2.85:1 — FAILS AA)
- Brand color as text on white (many brand colors fail at body text size)
- White text on light accent colors

**Fix patterns**:
- Darken text colors until they pass (often `-700` or `-800` shades)
- Use brand colors only on large text or as backgrounds (with contrasting text)
- For accessibility-critical elements, test with the primitive color scale and pick the darkest shade that maintains brand feeling

### Color Psychology: What Evidence Actually Supports

Color psychology is one of the most oversimplified topics in branding. Knowing what's real vs. myth helps you give well-grounded guidance.

**What the research supports**:
- Hue can map to broad personality dimensions, but effects are contextual (a color that increases attraction on a date may trigger anxiety in a test context)
- **Saturation and value matter as much or more than hue** — higher saturation = greater perceived potency and product efficacy
- Color affects perception through **learned associations**, not innate triggers
- **Cultural context is paramount** — white signifies purity in the West but mourning in East Asia
- Category-appropriateness matters more than abstract color meaning — your colors should be *appropriate for your category* and *distinctive from competitors*

**What is myth or oversimplified**:
- "Red makes people hungry" — lacks rigorous causal evidence
- "Blue is always calming" — mood effects dissipate quickly and are context-dependent
- Any claim that a single color universally triggers a specific emotion

**Practical guidance for the plugin**:
- When users say "I want blue because it's trustworthy," gently reframe: "Blue is common in your category, which creates an association with trust through familiarity. But the *shade* and *saturation* matter just as much — a desaturated navy feels very different from an electric cyan."
- When choosing colors, optimize for: (1) category appropriateness, (2) competitor differentiation, (3) palette harmony and contrast, (4) accessibility. These are more evidence-based criteria than abstract color meanings.
- If users reference color psychology confidently, don't dismiss it — redirect toward the nuanced truth: "There's some truth to that, and it's more about learned associations and context than universal triggers. Let's focus on what the color *communicates in your specific market*."

### Color Harmony

When generating palettes from synthesis:

**Complementary**: Colors opposite on the color wheel. High contrast, energetic.
**Analogous**: Colors adjacent on the color wheel. Harmonious, cohesive.
**Triadic**: Three evenly spaced colors. Balanced, vibrant.
**Split-complementary**: Base + two colors adjacent to its complement. Versatile.

**From brand personality**:
- High excitement → complementary or triadic (dynamic contrast)
- High sophistication → analogous or monochromatic (restrained harmony)
- High sincerity → warm analogous (comfortable, consistent)
- High ruggedness → earth-tone analogous (grounded)

### Gradient Rules

Gradients should:
- Follow the 60-30-10 hierarchy (gradients as the 30% or 10%, rarely 60%)
- Use colors from the same palette (not arbitrary combinations)
- Flow in a direction that supports reading order (typically top-left to bottom-right, or top to bottom)
- Be subtle in professional contexts, bolder in energetic brands

**Avoid**:
- Rainbow gradients (unless the brand is explicitly playful/colorful)
- Gradients on text (accessibility nightmare)
- Gradients as the primary background in most cases

---

## Typography Rules

### Modular Scale

A modular scale generates a harmonious set of sizes from a base size and ratio.

**Formula**: `size = base × ratio^n`

| Scale Name | Ratio | Character |
|-----------|-------|-----------|
| Minor Second | 1.067 | Very tight — almost uniform sizes. Subtle hierarchy. |
| Major Second | 1.125 | Gentle progression. Good for dense UIs. |
| Minor Third | 1.200 | Moderate. Good all-purpose choice. |
| **Major Third** | **1.250** | **Recommended default.** Clear hierarchy without extremes. |
| Perfect Fourth | 1.333 | Generous. Good for marketing/editorial. |
| Augmented Fourth | 1.414 | Dramatic. Strong heading/body contrast. |
| Perfect Fifth | 1.500 | Very dramatic. Large headings. |

**Example Major Third scale (base 16px)**:

| Step | Size | Use |
|------|------|-----|
| -2 | 10.24px → 0.64rem | Captions, fine print |
| -1 | 12.80px → 0.80rem | Small text, labels |
| 0 | 16.00px → 1.00rem | Body text (base) |
| 1 | 20.00px → 1.25rem | Large body, lead text |
| 2 | 25.00px → 1.56rem | H4 / subheading |
| 3 | 31.25px → 1.95rem | H3 |
| 4 | 39.06px → 2.44rem | H2 |
| 5 | 48.83px → 3.05rem | H1 |
| 6 | 61.04px → 3.81rem | Display heading |

**Choosing the ratio from personality**:
- High sophistication → Minor Third (1.200) — subtle, elegant
- Balanced → Major Third (1.250) — clear but not dramatic
- High excitement → Perfect Fourth (1.333) or higher — bold, energetic
- High competence → Major Third (1.250) — structured, professional

### Line Height Rules

| Text Type | Line Height | Why |
|-----------|------------|-----|
| Body text | 1.5-1.7 | Readable for sustained reading |
| Short text (UI labels, buttons) | 1.2-1.4 | Compact, doesn't waste space |
| Headings | 1.1-1.3 | Tight — headings don't need reading-length spacing |
| Display text (hero, splash) | 1.0-1.15 | Very tight — impact over readability |

### Letter Spacing Rules

| Text Type | Letter Spacing | Why |
|-----------|---------------|-----|
| Body text | 0 (normal) | Default tracking is optimized for body |
| Small text (<14px) | +0.01-0.02em | Open up for legibility at small sizes |
| All-caps text | +0.05-0.1em | Caps need extra breathing room |
| Large headings (>36px) | -0.01-0.02em | Tighten — large text looks loose at normal tracking |
| Display headings | -0.02-0.04em | Tighter still for impact |

### Variable Fonts

Variable fonts contain an entire design space of variations in a single file, along axes like weight, width, optical size, grade, and slant.

**Why they matter for brand identity**:
- **Performance**: A site using multiple static font weights might save significant bandwidth by switching to one variable font file, improving load times.
- **Responsive width**: Font width can adapt to viewport, allowing tighter text on mobile without changing the typeface.
- **Grade axis**: Allows hover-state emphasis without layout shift — the text gets visually "bolder" without changing its dimensions.
- **Animation**: CSS transitions can smoothly animate weight and width changes — impossible with static fonts.
- **Fewer files**: One variable font replaces multiple static weight files.

**When to recommend variable fonts**:
- The brand uses 3+ weights of the same typeface
- Performance is a priority (especially mobile-first products)
- The design system includes animated or responsive typography
- The primary typeface is available as a variable font (many Google Fonts now are)

**Note**: Not all typefaces have variable versions. When recommending specific fonts, check current availability. The variable font ecosystem is expanding rapidly — **search for current options** rather than relying on a static list.

### Font Licensing Pitfalls

Critical gotchas that non-designers rarely know about:

1. **Weight-level licensing**: A "font license" typically covers one font within a typeface family. Helvetica Regular ≠ Helvetica Bold — they may be separate licenses.
2. **Web font metering**: Web font licenses are often metered by pageviews. High-traffic sites can face unexpected costs.
3. **Separate platform licenses**: Desktop, web, and app licenses are typically separate purchases.
4. **"Personal use only" trap**: Using a personal-use font commercially creates legal liability. Always verify the license.
5. **Subscription dependency**: Some font services require ongoing subscriptions — fonts stop working if the subscription lapses.
6. **GDPR and font CDNs**: Loading fonts from third-party CDNs (like Google Fonts' default CDN) collects visitor IP addresses. For EU compliance, self-hosting fonts is safer. Privacy-first CDN alternatives exist — **search for current options** when this comes up.
7. **Open-source as default**: For startups, open-source fonts (SIL Open Font License) eliminate all licensing complexity. The quality of open-source fonts has improved dramatically.

**Practical rule**: Start with open-source fonts unless there's a compelling reason not to. The design quality ceiling is high enough for most startups.

### Font Pairing Rules

1. **Contrast, not conflict.** Pair typefaces with different structures (serif + sans, geometric + humanist) but similar x-heights.
2. **One display, one workhorse.** The heading font can be expressive; the body font must be readable above all.
3. **Two is enough.** Three typefaces maximum, and only if the third serves a specific purpose (e.g., monospace for code).
4. **Match the era.** Don't pair a 16th-century Garamond with a 21st-century geometric sans unless the contrast is the point.

---

## Spacing and Layout Rules

### Spacing Scale

Use a consistent spacing scale derived from a base unit:

**Base-4 system** (most common):
`4, 8, 12, 16, 24, 32, 48, 64, 96, 128` (px)

**Base-8 system** (more dramatic jumps):
`8, 16, 24, 32, 48, 64, 96, 128, 192` (px)

**Which to choose**:
- High competence, high sophistication → Base-4 (more granular control)
- High excitement, high ruggedness → Base-8 (bolder spacing)

### Layout Density

| Personality | Layout Approach |
|------------|----------------|
| High competence | Structured grid, moderate density, clear hierarchy |
| High sophistication | Generous white space, minimal density, editorial feel |
| High excitement | Dynamic, asymmetric, varied density |
| High sincerity | Comfortable spacing, not too dense, not too sparse |
| High ruggedness | Grounded, sturdy spacing, heavy borders acceptable |

### Composition Hierarchy

Three models for visual hierarchy:

**Size-based** (most brands): Larger = more important. H1 > H2 > H3 > body.
**Weight-based** (sophisticated brands): Bold vs. regular weight creates hierarchy without size variation.
**Color-based** (accent-driven brands): Hierarchy through color contrast rather than size.

Most systems combine all three, but one should lead.

---

## Motion and Animation Rules

### Duration Scale

| Category | Duration | Use |
|----------|----------|-----|
| Instant | 0-100ms | Color changes, opacity shifts |
| Fast | 100-200ms | Button hover, small element transitions |
| Normal | 200-400ms | Modal open/close, panel slide, page transitions |
| Slow | 400-700ms | Complex animations, orchestrated sequences |
| Deliberate | 700ms+ | Loading states, onboarding, storytelling |

### Easing Functions

| Name | CSS | Character |
|------|-----|-----------|
| ease-out | `cubic-bezier(0, 0, 0.2, 1)` | Arrives quickly, settles gently. Best for entering elements. |
| ease-in | `cubic-bezier(0.4, 0, 1, 1)` | Starts slow, accelerates out. Best for exiting elements. |
| ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` | Smooth both ends. Best for moving/transforming elements. |
| spring | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Overshoots then settles. Playful, energetic. |

**From personality**:
- High excitement → spring easing, shorter durations
- High sophistication → ease-in-out, longer durations
- High competence → ease-out, fast durations (efficient, no waiting)
- High sincerity → ease-out, normal durations (natural, comfortable)

### Reduce-motion

Always include `prefers-reduced-motion` support:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Form Language Rules

### Border Radius

| Form Language | Default Radius | Button Radius | Card Radius |
|--------------|----------------|---------------|-------------|
| Geometric | 0-4px | 2-4px | 0-4px |
| Mixed | 4-8px | 6-8px | 8-12px |
| Organic | 8-16px | 12-24px | 16-24px |
| Pill/Rounded | full (9999px) | full | 16-24px |

**From personality**:
- High ruggedness → geometric, sharp
- High sincerity → mixed to organic, rounded
- High sophistication → geometric or subtle mixed
- High excitement → bold, distinctive (either very sharp or very rounded)

### Shadow Styles

| Form Language | Shadow Character |
|--------------|-----------------|
| Geometric | Sharp, defined — `0 2px 4px rgba(0,0,0,0.1)` |
| Mixed | Soft but present — `0 4px 12px rgba(0,0,0,0.08)` |
| Organic | Diffused, gentle — `0 8px 24px rgba(0,0,0,0.06)` |
| None | Flat design — borders only, no shadows |

---

## Applying Rules During Build

When brand-build generates the system:

1. **Read personality scores** from `synthesis.consensus.personality` (or `discovery.{name}.personality` for solo users).
2. **Map scores to rule selections** using the tables above.
3. **Generate tokens** following the token architecture (primitive → semantic → component).
4. **Validate contrast** on all text/background combinations using the WCAG thresholds.
5. **Document rationale** — every design principle should trace back to a personality dimension or synthesis decision.

The design system should feel *inevitable* — a natural expression of the brand personality, not an arbitrary collection of design choices.
