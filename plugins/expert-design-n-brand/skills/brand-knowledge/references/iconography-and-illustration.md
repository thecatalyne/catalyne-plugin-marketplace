# Iconography & Illustration Style

Reference for icon system design, illustration style definition, and the decision framework for custom vs. licensed visual assets. Used during build (when the design system needs iconography and illustration guidelines) and export (when documenting the brand's visual asset standards).

## How to Use This Reference

- **During build**: After color, typography, and form language are established, icon and illustration style should be defined to maintain system coherence.
- **During export**: The brand quick reference and design system document should include icon and illustration guidelines.
- **When users ask about tools or libraries**: The icon/illustration landscape changes frequently. **Do not recommend specific tools from memory.** Search for current, well-evidenced, popular-among-practitioners options.

---

## 1. Icon System Design

### The Standard Grid

Professional icon systems use pixel grids. The industry standard is **24×24px** (used by most major design systems). Key specs:

| Property | Standard Value | Notes |
|----------|---------------|-------|
| Canvas size | 24×24px | Industry default for web and mobile |
| Padding/trim area | 2px | Creates a 20×20px live area |
| Design canvas (for detail work) | 512×512px | 32px subdivisions for pixel-perfect scaling |

### Consistency Variables

An icon system must document these variables to maintain coherence:

**Stroke weight**: Consistent across all icons. 2px is standard for 24px icons. Thinner = more refined/sophisticated; thicker = bolder/friendlier.

**Corner radius**: Must match the design system's form language.
- Geometric brand → sharp corners (0px radius on icon strokes)
- Mixed brand → slight rounding (1-2px)
- Organic brand → rounded corners (2-4px)

**Stroke cap**: Round caps feel friendlier; butt/square caps feel more precise. This is a personality expression point.

**Fill vs. outline**:
- Filled icons scan faster and work better at small sizes. Good for selected/active states.
- Outlined icons feel more minimal and contemporary. Good for default/inactive states.
- **Never mix filled and outlined icons side by side** in the same context.

**Color**: Build icons in a single color using `currentColor` in SVG/CSS. This allows the icon to inherit text color and adapt to themes.

### Optical Balance

Pixel-perfect alignment isn't enough — icons need optical balance:
- **Circular shapes** take up less visual space than squares at the same pixel dimensions. Circular icons should extend to the full live area edges.
- **Square icons** should be slightly smaller than the live area to appear the same size as circular ones.
- **Triangular shapes** (like play buttons) need optical centering — shift slightly right of mathematical center.

### Mapping Icons to Brand Personality

| Personality | Icon Style |
|------------|------------|
| High sincerity | Rounded strokes, medium weight, friendly caps |
| High excitement | Bold weight, dynamic angles, filled style |
| High competence | Precise strokes, consistent weight, sharp caps |
| High sophistication | Thin strokes, refined details, outline style |
| High ruggedness | Heavy strokes, rough edges, filled style |

---

## 2. Illustration Style Definition

Illustration style is defined by measurable variables — not vibes. Documenting these ensures consistency whether one person or fifty are creating illustrations.

### The Variables

**Line weight**: Thick/thin, consistent/variable. Consistent weight feels more controlled; variable weight feels more hand-drawn and human.

**Color application**: How the brand palette maps to illustrations.
- Brand palette only vs. extended illustration palette
- Flat color vs. gradients
- Full opacity vs. transparency/overlay

**Perspective & dimension**:
- Flat (2D) — clean, modern, scalable
- Isometric (2.5D) — technical, structured, engaging
- Full 3D — immersive, complex, harder to maintain consistency

**Character design** (if using people):
- Proportions (realistic, slightly stylized, highly abstract)
- Facial features (detailed, simplified, none)
- Diversity representation guidelines

**Level of detail**: From minimal/abstract to highly detailed. More detail = harder to maintain consistency across multiple illustrators.

**Texture**: Clean vector (scalable, modern) vs. grain/noise (warm, tactile, editorial).

**Abstraction level**: Literal representations vs. metaphorical/conceptual.

### Illustration Tiers

Most brands benefit from defining 2-3 tiers:

| Tier | Purpose | Complexity | Where Used |
|------|---------|------------|------------|
| **Spot** | Simple concepts, inline with text | Low — 2-3 colors, minimal detail | Empty states, feature callouts, list items |
| **Hero** | Complex metaphorical stories | Medium-high — full palette, detail | Landing pages, blog headers, onboarding |
| **Narrative** | Sequential or scene-based | High — characters, environments | Case studies, explainers, presentations |

### Mapping Illustration to Brand Personality

| Personality | Illustration Approach |
|------------|----------------------|
| High sincerity | Warm colors, rounded shapes, white space, friendly characters |
| High excitement | Dynamic compositions, vivid colors, movement, bold shapes |
| High competence | Clean vectors, structured layouts, data-viz style, restrained palette |
| High sophistication | Minimal detail, generous negative space, refined line work |
| High ruggedness | Textured, raw, hand-drawn feel, earth tones |

---

## 3. Custom vs. Licensed: Decision Framework

### When to Use Free/Open-Source Libraries

**For icons**: Start here. Major open-source libraries have thousands of well-designed, consistent icons. Use when:
- Budget is limited
- Speed matters more than uniqueness
- The brand identity is expressed through color/typography/layout, not custom iconography

**For illustrations**: Free illustration libraries work for early-stage marketing (landing pages, onboarding). Use when:
- Validating product-market fit (don't invest in custom art for a pivot)
- Internal tools and documentation
- The illustration style can be customized (color, composition) to match the brand

### When to Invest in Custom

**For icons**: When the brand needs a distinctive icon style that differentiates (rare — most brands don't need custom icons).

**For illustrations**: When brand differentiation becomes a growth lever — typically post-funding or when visual identity is a competitive advantage. Signs it's time:
- Multiple competitors use the same illustration libraries
- The brand voice is distinct but the visual language is generic
- Marketing materials need to tell complex, brand-specific stories

### Cost Framework

| Asset Type | DIY/Free | Freelance | Agency |
|-----------|----------|-----------|--------|
| Icon set (50-100 icons) | Free (open-source library) | Varies widely | Varies widely |
| Spot illustrations (10-20) | Free (open-source sets, customized) | Varies widely | Varies widely |
| Full brand illustration system | Not practical | Moderate investment | Significant investment |

**Note**: Specific pricing changes constantly. When users need current rates, search for recent freelance marketplace data and agency rate surveys.

### Documentation for Contractors

If commissioning custom illustration work, provide:

1. **Visual examples** — Approved and disapproved references (the single most effective method for communicating style)
2. **Brand guidelines** — Personality traits, design principles, the design system's color/type/form specs
3. **Existing illustrations** — For consistency matching
4. **Color palette** — Exact hex/RGB values, not "something blue-ish"
5. **Specific deliverables** — Sizes, formats (SVG preferred), intended usage context
6. **Licensing/ownership terms** — Work-for-hire vs. licensed, exclusivity, modification rights

---

## 4. Icon & Illustration in the Design System

### Token Integration

Icons and illustrations should reference design system tokens:

```
icon-size-sm: 16px
icon-size-md: 24px    (default)
icon-size-lg: 32px
icon-size-xl: 48px
icon-color-default: {color-text-primary}
icon-color-muted: {color-text-secondary}
icon-color-accent: {color-accent-default}
icon-stroke-weight: 2px
```

### Accessibility Requirements

- Icons used as interactive elements need accessible labels (`aria-label` or visually hidden text)
- Decorative icons should be hidden from assistive technology (`aria-hidden="true"`)
- Icon + text combinations: the text provides the label; the icon is decorative
- Icon-only buttons must have an accessible name
- Color alone must never be the only way an icon conveys meaning (e.g., red vs. green status icons need shape differences too)

---

## Searching for Current Tools

When users ask about icon libraries, illustration tools, or asset marketplaces:

1. **Search for current information**. Icon libraries rise and fall in popularity. What's dominant today may be deprecated tomorrow.
2. **Prioritize**: libraries with active maintenance, broad icon coverage, multiple weight/style options, permissive licenses (MIT, Apache 2.0, CC0), and SVG format support.
3. **For illustration**: distinguish between customizable sets (color/composition can be adjusted) and fixed-style sets. Customizable sets integrate better with brand palettes.
4. **Check licenses carefully**: "Free for commercial use" has many flavors. Attribution requirements, modification rights, and redistribution terms vary significantly.
5. **AI illustration tools**: The landscape is evolving rapidly. Search for current capabilities, but flag that AI-generated illustrations may have consistency challenges across a series and copyright uncertainty in some jurisdictions.
