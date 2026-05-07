# Design Token Architecture

Three-layer token taxonomy for translating brand identity into implementable design decisions, plus an optional `extensions` namespace for brand-specific expressive tokens. This architecture ensures tokens are meaningful, maintainable, and portable across platforms — and recognizable to any designer or front-end engineer reading the output.

## Vocabulary policy

The standard floor — primitive role names, semantic aliases, fontWeight names, shadow/easing/radius scales — uses **industry-standard terminology** (Tailwind, Material, Apple HIG, IBM Carbon all converge on the same vocabulary). Brand-specific poetic naming (named gradients, signature motifs, flourish moments) lives in the optional `extensions` namespace and never replaces standard role names.

**Standard floor names**
- Color: `bg`, `surface`, `text-primary`, `text-secondary`, `text-tertiary`, `text-inverse`, `text-disabled`, `border`, `border-strong`, `border-focus`, `link`, `link-hover`, status `success`/`warning`/`error`/`info`
- Color scales: `brand`, `neutral`, `accent`, plus any free-form named scale
- Font weight: `light` (300), `regular` (400), `medium` (500), `semibold` (600), `bold` (700)
- Shadow: `sm`, `md`, `lg`, `xl`
- Easing: `linear`, `standard`, `ease-in`, `ease-in-out`, `spring`
- Radius: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- State suffixes: `-hover`, `-active`, `-focus`, `-disabled`, `-selected`

**Extensions layer** (optional, brand-poetic)
- `extensions.color.expressions[]` — named gradients with intent tags
- `extensions.color.gradients` — concrete named gradients
- `extensions.color.flourish-glow` — signature glow shadow
- `extensions.motion.easing.spark` — brand alias for `spring`
- `extensions.elevation.flourish` — brand-specific elevation tier
- `extensions.form.motifs[]` — named decorative shapes
- `extensions.form.hero-motif` — principal signature visual

A tool that doesn't recognize the `extensions` namespace ignores it; the rest of the token set still works.

## The Three Layers

### Layer 1: Primitive Tokens (Raw Values)

The atomic building blocks. These are raw values with no semantic meaning — they're the palette the design system draws from.

**Naming convention**: `{category}-{scale}`

```json
{
  "color": {
    "blue-50": "#EBF5FF",
    "blue-100": "#D6EBFF",
    "blue-200": "#ADd6FF",
    "blue-300": "#85C2FF",
    "blue-400": "#5CADFF",
    "blue-500": "#3399FF",
    "blue-600": "#2979CC",
    "blue-700": "#1F5A99",
    "blue-800": "#143C66",
    "blue-900": "#1E3A8A",

    "neutral-50": "#FAFAFA",
    "neutral-100": "#F5F5F5",
    "neutral-200": "#E5E5E5",
    "neutral-300": "#D4D4D4",
    "neutral-400": "#A3A3A3",
    "neutral-500": "#737373",
    "neutral-600": "#525252",
    "neutral-700": "#404040",
    "neutral-800": "#262626",
    "neutral-900": "#171717"
  },
  "spacing": {
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "6": "1.5rem",
    "8": "2rem",
    "12": "3rem",
    "16": "4rem",
    "24": "6rem"
  },
  "font-size": {
    "xs": "0.75rem",
    "sm": "0.875rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
    "5xl": "3rem"
  },
  "font-weight": {
    "light": 300,
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700
  },
  "border-radius": {
    "none": "0",
    "sm": "0.125rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "full": "9999px"
  }
}
```

**Rules**:
- Primitives are generated from the brand's color palette, typography scale, and form language
- They are the only layer that contains actual values (hex codes, rem values, pixel sizes)
- Every other layer references primitives — never hardcodes values

### Layer 2: Semantic Tokens (Intent-Based)

Map primitives to purposes. These describe what the token is *for*, not what it *is*.

**Naming convention**: `{category}-{usage}-{variant?}-{state?}`

```json
{
  "color-background-primary": "{color.neutral-50}",
  "color-background-secondary": "{color.neutral-100}",
  "color-background-inverse": "{color.neutral-900}",

  "color-text-primary": "{color.neutral-900}",
  "color-text-secondary": "{color.neutral-600}",
  "color-text-inverse": "{color.neutral-50}",
  "color-text-link": "{color.blue-600}",
  "color-text-link-hover": "{color.blue-700}",

  "color-border-default": "{color.neutral-200}",
  "color-border-focus": "{color.blue-500}",

  "color-surface-brand": "{color.blue-500}",
  "color-surface-brand-hover": "{color.blue-600}",
  "color-surface-success": "#16A34A",
  "color-surface-warning": "#D97706",
  "color-surface-error": "#DC2626",

  "spacing-page-gutter": "{spacing.4}",
  "spacing-section-gap": "{spacing.12}",
  "spacing-card-padding": "{spacing.6}",
  "spacing-inline-gap": "{spacing.2}",

  "font-heading-family": "\"Playfair Display\", Georgia, serif",
  "font-heading-weight": "{font-weight.bold}",
  "font-body-family": "\"Source Sans 3\", \"Helvetica Neue\", sans-serif",
  "font-body-weight": "{font-weight.regular}",

  "radius-interactive": "{border-radius.md}",
  "radius-card": "{border-radius.lg}",
  "radius-avatar": "{border-radius.full}"
}
```

**Rules**:
- Semantic tokens always reference primitive tokens (never raw values)
- Names describe purpose, not appearance ("background-primary" not "white")
- This is where dark mode, themes, and brand variations happen — swap the primitive references, semantic names stay the same
- States (hover, focus, active, disabled) are explicit in the name

### Layer 3: Component Tokens (UI-Specific)

Map semantic tokens to specific UI components. Optional but valuable for complex systems.

**Naming convention**: `{component}-{element?}-{property}-{variant?}-{state?}`

```json
{
  "button-background": "{color-surface-brand}",
  "button-background-hover": "{color-surface-brand-hover}",
  "button-text": "{color-text-inverse}",
  "button-border-radius": "{radius-interactive}",
  "button-padding-x": "{spacing.4}",
  "button-padding-y": "{spacing.2}",

  "card-background": "{color-background-primary}",
  "card-border": "{color-border-default}",
  "card-border-radius": "{radius-card}",
  "card-padding": "{spacing-card-padding}",
  "card-shadow": "0 1px 3px rgba(0,0,0,0.1)",

  "input-background": "{color-background-primary}",
  "input-border": "{color-border-default}",
  "input-border-focus": "{color-border-focus}",
  "input-border-radius": "{radius-interactive}",
  "input-padding": "{spacing.3}",
  "input-text": "{color-text-primary}",
  "input-placeholder": "{color-text-secondary}",

  "nav-background": "{color-background-primary}",
  "nav-text": "{color-text-primary}",
  "nav-text-active": "{color-surface-brand}",
  "nav-border": "{color-border-default}"
}
```

**Rules**:
- Component tokens reference semantic tokens (never primitives directly)
- Only create component tokens for recurring UI patterns
- These are the tokens developers actually use in component code

## Generating Tokens from Brand Identity

### Color Palette → Primitive Color Tokens

From `brand-identity.yaml → system.color.palette`:

| Brand Palette Role | Generates |
|-------------------|-----------|
| background | `color.neutral-50` through `color.neutral-200` (light end) |
| primary | Full 10-step scale (`color.brand-50` through `color.brand-900`) |
| neutral | Full 10-step scale for the foreground/text anchor (the dark color that anchors composition) |
| accent | Full 10-step scale for accent color |

> **Legacy note**: earlier versions of this plugin used the role name `anchor` instead of `neutral` for the dark-text foreground role. Brand identity files written with the older vocabulary are accepted by `/brand-build` Phase 3B normalization (which rewrites `anchor` → `neutral` in-memory) but new identities should use `neutral`.

**Scale generation**: Given a base hex value, generate a 10-step scale from lightest (50) to darkest (900) by adjusting lightness in HSL space. The base value typically maps to the 500 step.

### Typography → Primitive + Semantic Font Tokens

From `brand-identity.yaml → system.typography`:

| Brand Typography | Generates |
|-----------------|-----------|
| typefaces[0] (heading) | `font-heading-family`, `font-heading-weight` |
| typefaces[1] (body) | `font-body-family`, `font-body-weight` |
| scale.ratio | Full modular scale (`font-size.xs` through `font-size.5xl`) |
| scale.base_size | `font-size.base` (anchor for the scale) |

### Form Language → Shape Tokens

From `brand-identity.yaml → system.form_language`:

| Brand Form Language | Generates |
|--------------------|-----------|
| border_radius | `border-radius.*` scale (geometric = small radii, organic = large) |
| shadow_style | Shadow tokens (sharp = crisp shadows, soft = diffused) |
| motifs | Guidance for component tokens (not direct generation) |

## Cross-surface output

A single canonical `tokens.json` (this file's three layers + the `extensions` namespace) is the source for every per-surface output. Per-surface theme rendering is driven by `assets/surface-translations.yaml` — one declarative file with a block per surface (web CSS, Tailwind config, Figma Tokens Studio, Google Slides, PowerPoint, Keynote, Canva). Each surface block declares which token paths fill which surface slot. There is no per-surface duplication of color/font mappings.

## CSS Custom Properties Output

The export step generates CSS custom properties from all three layers:

```css
/* ─── Primitive Tokens ─── */
:root {
  --color-brand-50: #EBF5FF;
  --color-brand-500: #3399FF;
  --color-brand-900: #1E3A8A;
  /* ... full scales ... */

  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  /* ... */

  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  /* ... */
}

/* ─── Semantic Tokens ─── */
:root {
  --color-bg-primary: var(--color-neutral-50);
  --color-text-primary: var(--color-neutral-900);
  --color-surface-brand: var(--color-brand-500);
  /* ... */
}

/* ─── Component Tokens ─── */
:root {
  --button-bg: var(--color-surface-brand);
  --button-text: var(--color-text-inverse);
  --card-bg: var(--color-bg-primary);
  /* ... */
}
```

## JSON Output Format

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "primitive": {
    "color": { "brand-500": { "$value": "#3399FF", "$type": "color" } }
  },
  "semantic": {
    "color-surface-brand": { "$value": "{primitive.color.brand-500}", "$type": "color" }
  },
  "component": {
    "button-background": { "$value": "{semantic.color-surface-brand}", "$type": "color" }
  }
}
```

## Token Naming Rules

1. **Kebab-case only**: `color-background-primary` not `colorBackgroundPrimary`
2. **Category first**: `color-*`, `spacing-*`, `font-*`, `radius-*`, `shadow-*`
3. **No raw values in names**: `color-brand-500` not `color-blue-3399FF`
4. **States are suffixed**: `button-background-hover`, `input-border-focus`
5. **Variants use descriptive names**: `button-background-secondary` not `button-background-2`
