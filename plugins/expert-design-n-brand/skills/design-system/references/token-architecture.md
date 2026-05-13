# Design Token Architecture

Three-layer token taxonomy for translating brand identity into implementable design decisions, plus an optional `extensions` namespace for brand-specific expressive tokens. This architecture ensures tokens are meaningful, maintainable, and portable across platforms — and recognizable to any designer or front-end engineer reading the output.

> **Canonical vocabulary source.** Token names, role labels, surface slot names, and CSS/Tailwind/Figma keys are defined in `assets/platform-matrix-template.md`. This document explains the *architecture* (why three layers, how generation works, naming rules) — the *vocabulary itself* (which roles exist, what their canonical names are) lives in the Platform Matrix. If anything below appears to disagree with the Platform Matrix, the Platform Matrix wins; treat the disagreement as a bug.

## Vocabulary policy

The standard floor uses industry-standard terminology (Tailwind, Material, Apple HIG, IBM Carbon all converge). Brand-specific poetic naming (named gradients, signature motifs, flourish moments) lives in the optional `extensions` namespace and never replaces standard role names.

For the authoritative lists — color roles, typography tokens, form/spacing tokens, font weights, easing names, radius scale — see `assets/platform-matrix-template.md` §1 (color), §2 (typography), and §3 (form & spacing). The Platform Matrix also defines the per-surface translation vocabulary (Tailwind class names, Figma Tokens Studio paths, Google Slides theme slots, etc.).

**Extensions layer** (optional, brand-poetic) — see `assets/platform-matrix-template.md` §6 "Core vs. Extensions" for the full policy and worked examples. Common shapes:
- `extensions.color.expressions[]` — named gradients with intent tags
- `extensions.color.gradients` — concrete named gradients (e.g. `amber-glow`)
- `extensions.color.flourish-glow` — signature glow shadow
- `extensions.motion.easing.flourish` — brand-poetic easing name (functionally a spring)
- `extensions.elevation.flourish` — brand-specific elevation tier
- `extensions.form.motifs[]` — named decorative shapes
- `extensions.form.hero-motif` — principal signature visual

A tool that doesn't recognize the `extensions` namespace ignores it; the rest of the token set still works.

## Color-role parity contract

Light and dark mode MUST define identical sets of these 14 color-role slots (canonical names from `assets/platform-matrix-template.md` §1):

| Slot | Role |
|---|---|
| `bg` | Page background |
| `surface` | Card / container surface |
| `surface-elevated` | Modal / popover surface (higher elevation) |
| `inverse` | Inverse surface (dark on a light page; light on a dark page) |
| `text-primary` | Primary body text |
| `text-secondary` | Secondary / supporting text |
| `text-tertiary` | Tertiary / meta text |
| `text-disabled` | Disabled text |
| `text-inverse` | Text on inverse surfaces |
| `border` | Default border |
| `border-strong` | Emphasised border |
| `border-focus` | Focus ring |
| `link` | Hyperlink rest state |
| `link-hover` | Hyperlink hover state |

Status tokens (`success`, `warning`, `error`, `info`) live in `semantic.status` and are **mode-invariant** — the same hex in light and dark; the surrounding surface changes, not the signal.

A build that produces fewer than 14 color-role slots in either mode is rejected with a user-visible warning naming the missing slot(s). The build-time check happens in `skills/brand-build/references/build-phases.md` Phase 1.

**Worked example — light to dark contrast walk:**

```yaml
semantic.light.color:
  bg:               "#FFFCF8"   # Washi (warm white)
  surface:          "#FFFFFF"   # Pure white card on Washi page
  surface-elevated: "#F5F2EC"   # Slightly warmer for modals
  inverse:          "#1A1A2E"   # Ink Navy — for dark-on-light callouts
  text-primary:     "#000000"   # 21:1 on bg
  text-secondary:   "#404048"   # ~10:1 on bg
  text-tertiary:    "#6B6699"   # Muted Indigo, ~6.5:1 on bg
  text-disabled:    "#A8A3C9"   # ~3.5:1 on bg (decorative)
  text-inverse:     "#FFFCF8"   # Washi on inverse surfaces
  border:           "#E5E0D5"   # Hairline on Washi
  border-strong:    "#1A1A2E"   # Ink Navy emphasis
  border-focus:     "#FFCB47"   # Star Amber — brand-primary focus
  link:             "#6B6699"   # Muted Indigo, ~6.5:1 on bg
  link-hover:       "#4B4675"   # Deeper indigo

semantic.dark.color:
  bg:               "#1A1A2E"   # Ink Navy
  surface:          "#252540"   # Lifted from page
  surface-elevated: "#2E2E4A"   # Modal surface
  inverse:          "#FFFCF8"   # Washi — for light-on-dark callouts
  text-primary:     "#FFFCF8"   # 18:1 on bg
  text-secondary:   "#D6D2E5"   # ~12:1 on bg
  text-tertiary:    "#A8A3C9"   # Indigo 300, ~7.2:1 on bg
  text-disabled:    "#6B6699"   # ~3.5:1 on bg (decorative)
  text-inverse:     "#000000"   # Black on inverse surfaces
  border:           "#3D3D5C"   # Soft separator on Ink Navy
  border-strong:    "#A8A3C9"   # Indigo 300 emphasis
  border-focus:     "#FFCB47"   # Star Amber — same focus signal in both modes
  link:             "#A8A3C9"   # Indigo 300, lighter step for AA on dark surface
  link-hover:       "#C9C4DD"   # Even lighter
```

Note the parity: every slot in `semantic.light.color` has a counterpart in `semantic.dark.color` with the same name. Hex values change to maintain contrast against the mode-specific `bg`; the slot *vocabulary* is identical.

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

Canonical slot names from `assets/platform-matrix-template.md` §1 (color), §2 (typography), §3 (form & spacing). The example below shows the **light-mode** branch; the **dark-mode** branch under `semantic.dark.color` uses the identical 14 slot names with mode-appropriate hex values — see "Color-role parity contract" above.

```json
{
  "semantic.light.color": {
    "bg":               "{primitive.color.scales.neutral.50}",
    "surface":          "{primitive.color.scales.neutral.0}",
    "surface-elevated": "{primitive.color.scales.neutral.100}",
    "inverse":          "{primitive.color.scales.neutral.900}",

    "text-primary":   "{primitive.color.scales.neutral.900}",
    "text-secondary": "{primitive.color.scales.neutral.600}",
    "text-tertiary":  "{primitive.color.scales.neutral.500}",
    "text-disabled":  "{primitive.color.scales.neutral.400}",
    "text-inverse":   "{primitive.color.scales.neutral.50}",

    "border":         "{primitive.color.scales.neutral.200}",
    "border-strong":  "{primitive.color.scales.neutral.900}",
    "border-focus":   "{primitive.color.scales.primary.500}",

    "link":           "{primitive.color.scales.primary.600}",
    "link-hover":     "{primitive.color.scales.primary.700}"
  },

  "semantic.status": {
    "success": "#16A34A",
    "warning": "#D97706",
    "error":   "#DC2626",
    "info":    "#2563EB"
  },

  "spacing": {
    "page-gutter":  "{primitive.spacing.4}",
    "section-gap":  "{primitive.spacing.12}",
    "card-padding": "{primitive.spacing.6}",
    "inline-gap":   "{primitive.spacing.2}"
  },

  "font": {
    "heading.family": "\"Playfair Display\", Georgia, serif",
    "heading.weight": "{primitive.font-weight.bold}",
    "body.family":    "\"Source Sans 3\", \"Helvetica Neue\", sans-serif",
    "body.weight":    "{primitive.font-weight.regular}"
  },

  "radius": {
    "interactive": "{primitive.border-radius.md}",
    "card":        "{primitive.border-radius.lg}",
    "avatar":      "{primitive.border-radius.full}"
  }
}
```

**Rules**:
- Semantic tokens always reference primitive tokens (never raw values, except the mode-invariant status colors).
- Names match the Platform Matrix canonical vocabulary exactly. No drift, no aliases at this layer — brand-poetic names belong in `extensions.*` (Platform Matrix §6).
- This is where dark mode, themes, and brand variations happen — swap the primitive references, semantic slot names stay identical.
- States (`-hover`, `-focus`, `-active`, `-disabled`, `-selected`) are explicit suffixes.

### Layer 3: Component Tokens (UI-Specific)

Map semantic tokens to specific UI components. Optional but valuable for complex systems.

**Naming convention**: `component.{component}.{element?}.{property}.{variant?}.{state?}`

```json
{
  "component.button.primary": {
    "background":        "{semantic.light.color.link}",
    "background-hover":  "{semantic.light.color.link-hover}",
    "text":              "{semantic.light.color.text-inverse}",
    "border-radius":     "{semantic.radius.interactive}",
    "padding-x":         "{primitive.spacing.4}",
    "padding-y":         "{primitive.spacing.2}"
  },

  "component.card": {
    "background":        "{semantic.light.color.surface}",
    "border":            "{semantic.light.color.border}",
    "border-radius":     "{semantic.radius.card}",
    "padding":           "{semantic.spacing.card-padding}",
    "shadow":            "0 1px 3px rgba(0,0,0,0.1)"
  },

  "component.input": {
    "background":        "{semantic.light.color.surface}",
    "border":            "{semantic.light.color.border}",
    "border-focus":      "{semantic.light.color.border-focus}",
    "border-radius":     "{semantic.radius.interactive}",
    "padding":           "{primitive.spacing.3}",
    "text":              "{semantic.light.color.text-primary}",
    "placeholder":       "{semantic.light.color.text-secondary}"
  },

  "component.nav": {
    "background":        "{semantic.light.color.surface}",
    "text":              "{semantic.light.color.text-primary}",
    "text-active":       "{semantic.light.color.link}",
    "border":            "{semantic.light.color.border}"
  }
}
```

**Rules**:
- Component tokens reference semantic tokens (never primitives directly).
- Slot names within a component are descriptive (`background`, `text`, `border`) — these are component-internal labels, not core-schema role names.
- Only create component tokens for recurring UI patterns.
- These are the tokens developers actually use in component code.

## Generating Tokens from Brand Identity

### Color Palette → Primitive Color Tokens

From `brand-identity.yaml → system.color.palette`:

| Brand Palette Role | Generates |
|-------------------|-----------|
| background | `color.neutral-50` through `color.neutral-200` (light end) |
| primary | Full 10-step scale (`color.brand-50` through `color.brand-900`) |
| neutral | Full 10-step scale for the foreground/text anchor (the dark color that anchors composition) |
| accent | Full 10-step scale for accent color |

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

The export step generates CSS custom properties from all three layers. Variable names match the Platform Matrix §1 / §2 / §3 CSS-variable column exactly — no aliases, no drift.

```css
/* ─── Primitive Tokens ─── */
:root {
  --color-primary-50: #EBF5FF;
  --color-primary-500: #3399FF;
  --color-primary-900: #1E3A8A;
  /* ... full scales for primary, neutral, accent ... */

  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  /* ... */

  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  /* ... */
}

/* ─── Semantic Tokens (light mode) ─── */
:root {
  --color-bg:               var(--color-neutral-50);
  --color-surface:          var(--color-neutral-0);
  --color-surface-elevated: var(--color-neutral-100);
  --color-inverse:          var(--color-neutral-900);

  --color-text-primary:   var(--color-neutral-900);
  --color-text-secondary: var(--color-neutral-600);
  --color-text-tertiary:  var(--color-neutral-500);
  --color-text-disabled:  var(--color-neutral-400);
  --color-text-inverse:   var(--color-neutral-50);

  --color-border:        var(--color-neutral-200);
  --color-border-strong: var(--color-neutral-900);
  --color-border-focus:  var(--color-primary-500);

  --color-link:       var(--color-primary-600);
  --color-link-hover: var(--color-primary-700);

  --color-success: #16A34A;
  --color-warning: #D97706;
  --color-error:   #DC2626;
  --color-info:    #2563EB;
}

/* ─── Semantic Tokens (dark mode) ─── */
[data-theme="dark"] {
  --color-bg:               var(--color-neutral-900);
  --color-surface:          var(--color-neutral-800);
  --color-surface-elevated: var(--color-neutral-700);
  --color-inverse:          var(--color-neutral-50);

  --color-text-primary:   var(--color-neutral-50);
  --color-text-secondary: var(--color-neutral-300);
  --color-text-tertiary:  var(--color-neutral-400);
  --color-text-disabled:  var(--color-neutral-600);
  --color-text-inverse:   var(--color-neutral-900);

  --color-border:        var(--color-neutral-700);
  --color-border-strong: var(--color-neutral-50);
  --color-border-focus:  var(--color-primary-400);

  --color-link:       var(--color-primary-300);
  --color-link-hover: var(--color-primary-200);

  /* Status colors are mode-invariant — same hex as light mode. */
}

/* ─── Component Tokens ─── */
:root {
  --button-primary-background:       var(--color-link);
  --button-primary-background-hover: var(--color-link-hover);
  --button-primary-text:             var(--color-text-inverse);

  --card-background: var(--color-surface);
  --card-border:     var(--color-border);
}
```

## JSON Output Format

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "primitive": {
    "color": {
      "scales": {
        "primary": { "500": { "$value": "#3399FF", "$type": "color" } }
      }
    }
  },
  "semantic": {
    "light": {
      "color": {
        "bg":   { "$value": "{primitive.color.scales.neutral.50}", "$type": "color" },
        "link": { "$value": "{primitive.color.scales.primary.600}", "$type": "color" }
      }
    },
    "dark": {
      "color": {
        "bg":   { "$value": "{primitive.color.scales.neutral.900}", "$type": "color" },
        "link": { "$value": "{primitive.color.scales.primary.300}", "$type": "color" }
      }
    },
    "status": {
      "success": { "$value": "#16A34A", "$type": "color" }
    }
  },
  "component": {
    "button": {
      "primary": {
        "background": { "$value": "{semantic.light.color.link}", "$type": "color" }
      }
    }
  },
  "extensions": {
    "color": {
      "gradients": {
        "amber-glow": {
          "$type": "gradient",
          "$value": [
            { "color": "{primitive.color.scales.primary.400}", "position": 0 },
            { "color": "{primitive.color.scales.primary.600}", "position": 1 }
          ]
        }
      }
    }
  }
}
```

## Token Naming Rules

Canonical names live in `assets/platform-matrix-template.md`. The rules below explain *how* names are formed; *which* names exist is the Matrix's job.

1. **Kebab-case only**: `color.text-primary` not `colorTextPrimary` or `color_text_primary`.
2. **Category first**: `color.*`, `spacing.*`, `font.*`, `radius.*`, `shadow.*`.
3. **No raw values in names**: `color.primary.500` not `color.blue-3399FF`.
4. **States are suffixed**: `link-hover`, `border-focus`, `button.primary.background-hover`.
5. **Variants use descriptive names**: `button.primary` / `button.ghost` / `button.danger`, not `button-1` / `button-2`.
6. **Never replace a core role name with a brand-poetic alias.** The core slot is mandatory; poetic names live under `extensions.*` as additions, not substitutions.
