<!-- TIER 1 AUTHOR NOTE — external reference. Renders to `platform-matrix.md`. The single consolidated reference for applying the brand across web, design tools, and presentation surfaces. Master tables show one row per token/component, one column per surface — designers and developers read across the row to find the right slot/value/key for the surface they're using. Per-platform details below cover fallback chains, probe notes, setup steps, and platform-specific caveats. Keep reader-visible content in end-user language; no plugin-internal file names, build phases, slash commands, or status vocabulary in the rendered output. -->

# {{ brand_name }} — Platform matrix

The single reference for applying {{ brand_name }} on every supported surface. Read across each row in the master tables to find the right slot for your tool, then jump to the per-platform section below for fallback chains, setup steps, and caveats.

**Surfaces covered**: Web (CSS), Tailwind CSS, Figma (via Tokens Studio), Google Slides, PowerPoint, Keynote, Canva.

Machine import files (paste, don't transcribe):
- **Web** → `tokens.css` — `<link rel="stylesheet">` or `@import` it.
- **Tailwind** → `tailwind.config.js` — drop into the project root; Tailwind picks it up.
- **Figma** → `theme-figma.json` — Figma → Plugins → Tokens Studio → Tools → Load from JSON.

The master tables below cover everything else: the per-surface slot a hex / font / size belongs in. Per-platform setup, fallback chains, and caveats follow in §4.

---

## 1. Color tokens

Each row is a color role. Each column is the slot in that surface where the role's hex value belongs.

| Token / role           | CSS variable          | Tailwind class             | Figma (TS)            | Google Slides   | PowerPoint  | Keynote     | Canva (Pro / Free)              |
|------------------------|-----------------------|----------------------------|-----------------------|-----------------|-------------|-------------|---------------------------------|
| Background             | `--color-bg`          | `bg-background`            | `bg`                  | Light 1         | `bg1`       | slot 1      | background  / color 1 (Pro–Free)|
| Surface (cards)        | `--color-surface`     | `bg-surface`               | `surface`             | Light 2         | `bg2`       | —           | (n/a) / —                       |
| Text — primary         | `--color-text-primary`| `text-primary`             | `text-primary`        | Dark 1          | `tx1`       | slot 2      | text / color 2                  |
| Text — secondary       | `--color-text-secondary`| `text-secondary`         | `text-secondary`      | Dark 2          | `tx2`       | —           | (n/a) / —                       |
| Text — tertiary        | `--color-text-tertiary`| `text-tertiary`           | `text-tertiary`       | (use Dark 2)    | (use `tx2`) | —           | (n/a) / —                       |
| Text — inverse         | `--color-text-inverse`| `text-inverse`             | `text-inverse`        | (use Light 1)   | (use `bg1`) | —           | (n/a) / —                       |
| Brand — primary        | `--color-primary`     | `bg-primary` / `text-primary-brand` | `primary`     | Accent 1        | `accent1`   | slot 3      | primary / color 3 (Free)        |
| Brand — accent         | `--color-accent`      | `bg-accent`                | `accent`              | Accent 2        | `accent2`   | slot 4      | accent / —                      |
| Neutral mid            | `--color-neutral-500` | `bg-neutral-500`           | `neutral-500`         | Accent 3        | `accent3`   | slot 5      | neutral / —                     |
| Status — success       | `--color-success`     | `bg-success`               | `success`             | Accent 4        | `accent4`   | slot 6      | success / —                     |
| Status — warning       | `--color-warning`     | `bg-warning`               | `warning`             | Accent 5        | `accent5`   | —           | warning / —                     |
| Status — error         | `--color-error`       | `bg-error`                 | `error`               | Accent 6        | `accent6`   | —           | error / —                       |
| Status — info          | `--color-info`        | `bg-info`                  | `info`                | (use Accent 4)  | —           | —           | — / —                           |
| Border                 | `--color-border`      | `border-default`           | `border`              | (n/a)           | (n/a)       | —           | (n/a) / —                       |
| Border — strong        | `--color-border-strong`| `border-strong`           | `border-strong`       | (n/a)           | (n/a)       | —           | (n/a) / —                       |
| Link                   | `--color-link`        | `text-link`                | `text-link`           | Hyperlink       | `hlink`     | —           | (n/a) / —                       |
| Link (visited)         | `--color-link-visited`| `text-link-visited`        | (use brand 800)       | Followed        | `folHlink`  | —           | (n/a) / —                       |

**Hex values** — read from the brand palette below and paste into the slot the column points to:

| Role               | Hex                    |
|--------------------|------------------------|
| Background         | `{{ hex_bg }}`         |
| Surface            | `{{ hex_surface }}`    |
| Text — primary     | `{{ hex_text_primary }}`   |
| Text — secondary   | `{{ hex_text_secondary }}` |
| Text — tertiary    | `{{ hex_text_tertiary }}`  |
| Brand — primary    | `{{ hex_primary }}`    |
| Brand — accent     | `{{ hex_accent }}`     |
| Neutral 500        | `{{ hex_neutral_500 }}`|
| Success            | `{{ hex_success }}`    |
| Warning            | `{{ hex_warning }}`    |
| Error              | `{{ hex_error }}`      |
| Info               | `{{ hex_info }}`       |
| Link               | `{{ hex_link }}`       |
| Link visited       | `{{ hex_link_visited }}`|

---

## 2. Typography tokens

Each row is a typography token. Each column is the slot/key in that surface. **Slot names only** — fallback chains and per-platform substitution rationale live in §4.

| Token / role           | CSS variable             | Tailwind                | Figma (TS)              | Google Slides       | PowerPoint        | Keynote           | Canva (Pro / Free) |
|------------------------|--------------------------|-------------------------|-------------------------|---------------------|-------------------|-------------------|--------------------|
| Heading family         | `--font-heading`         | `font-heading`          | `family.heading`        | Theme heading       | Heading           | Title style       | Heading            |
| Body family            | `--font-body`            | `font-body`             | `family.body`           | Theme body          | Body              | Body style        | Body               |
| Mono family            | `--font-mono`            | `font-mono`             | `family.mono`           | (n/a)               | (n/a)             | (n/a)             | (n/a)              |
| Display size           | `--font-size-display`    | `text-display`          | `size.display`          | (custom)            | (custom)          | (custom)          | —                  |
| Heading 1              | `--font-size-h1`         | `text-h1`               | `size.h1`               | Title style         | Title             | Title             | (Title)            |
| Heading 2              | `--font-size-h2`         | `text-h2`               | `size.h2`               | Heading style       | Heading 1         | Heading           | (Heading)          |
| Heading 3              | `--font-size-h3`         | `text-h3`               | `size.h3`               | Subheading          | Heading 2         | Subheading        | —                  |
| Body                   | `--font-size-body`       | `text-base`             | `size.body`             | Body                | Body              | Body              | Body               |
| Caption                | `--font-size-caption`    | `text-caption`          | `size.caption`          | (smallest)          | Caption           | Caption           | —                  |
| Weight — light         | `--font-weight-light`    | `font-light`            | `weight.light` (300)    | (300)               | (Light)           | (Light)           | —                  |
| Weight — regular       | `--font-weight-regular`  | `font-normal`           | `weight.regular` (400)  | (400)               | (Regular)         | (Regular)         | —                  |
| Weight — medium        | `--font-weight-medium`   | `font-medium`           | `weight.medium` (500)   | (500)               | (Medium)          | (Medium)          | —                  |
| Weight — semibold      | `--font-weight-semibold` | `font-semibold`         | `weight.semibold` (600) | (600)               | (Semibold)        | (Semibold)        | —                  |
| Weight — bold          | `--font-weight-bold`     | `font-bold`             | `weight.bold` (700)     | (700)               | (Bold)            | (Bold)            | —                  |
| Line height — tight    | `--line-height-tight`    | `leading-tight`         | `lineHeight.tight` (1.2)| (custom)            | (custom)          | (custom)          | —                  |
| Line height — normal   | `--line-height-normal`   | `leading-normal`        | `lineHeight.normal` (1.5)| (default)          | (default)         | (default)         | —                  |
| Letter spacing — tight | `--letter-spacing-tight` | `tracking-tight`        | `letterSpacing.tight` (-0.02em) | (custom)    | (custom)          | (custom)          | —                  |

**Font choices for {{ brand_name }}**:

| Role     | Family                 |
|----------|------------------------|
| Heading  | `{{ heading_family }}` |
| Body     | `{{ body_family }}`    |
| Mono     | `{{ mono_family }}`    |

---

## 3. Form & spacing tokens

Mostly applies to web/design surfaces. Presentation tools don't expose granular control here — use the values when designing custom shapes manually.

| Token / role          | CSS variable             | Tailwind                | Figma (TS)            | Notes for presentation tools |
|-----------------------|--------------------------|-------------------------|-----------------------|------------------------------|
| Radius — sm           | `--radius-sm`            | `rounded-sm`            | `radius.sm`           | Apply manually to shapes     |
| Radius — md           | `--radius-md`            | `rounded-md`            | `radius.md`           | Apply manually to shapes     |
| Radius — lg           | `--radius-lg`            | `rounded-lg`            | `radius.lg`           | Apply manually to shapes     |
| Radius — pill         | `--radius-pill`          | `rounded-full`          | `radius.pill`         | Apply manually to shapes     |
| Shadow — sm           | `--shadow-sm`            | `shadow-sm`             | `shadow.sm`           | Apply manually to shapes     |
| Shadow — md           | `--shadow-md`            | `shadow-md`             | `shadow.md`           | Apply manually to shapes     |
| Shadow — lg           | `--shadow-lg`            | `shadow-lg`             | `shadow.lg`           | Apply manually to shapes     |
| Border width — thin   | `--border-width-thin`    | `border`                | `borderWidth.thin`    | (n/a)                        |
| Border width — thick  | `--border-width-thick`   | `border-2`              | `borderWidth.thick`   | (n/a)                        |
| Space — 4 (16px)      | `--space-4`              | `p-4` / `m-4` / `gap-4` | `space.4`             | Use 16px as base unit        |
| Space — 8 (32px)      | `--space-8`              | `p-8` / `m-8`           | `space.8`             | Use 32px for section gaps    |

**{{ brand_name }} form values**:

| Token              | Value                        |
|--------------------|------------------------------|
| Radius interactive | `{{ radius_interactive }}`   |
| Radius card        | `{{ radius_card }}`          |
| Shadow default     | `{{ shadow_default }}`       |
| Border default     | `{{ border_width_default }}` |

---

## 4. Per-platform details

One section per platform. Includes setup steps, typography fallback chain (which fonts to try if the primary isn't available, with rationale), probe notes, and caveats specific to that surface.

### Google Slides

**Setup**:
1. Open *Slide → Theme builder → Theme colors*.
2. Paste each hex from §1 into the slot named in the Google Slides column. Use the HEX field directly — the picker shifts hue 1–2 units.
3. *Insert → More fonts*: add the heading + body families.
4. Set Title / Heading / Body / Caption styles in the slide master to match §2.

**Typography fallback chain**:
- Heading: `{{ gslides_heading_chain }}`
  - *Rationale*: {{ gslides_heading_rationale }}
- Body: `{{ gslides_body_chain }}`
  - *Rationale*: {{ gslides_body_rationale }}

**Probe notes**:
{{ gslides_probe_notes_list }}

**Caveats**:
- Color picker shifts hex by 1–2 hue units. Always paste the literal hex.
- Custom fonts are per-document, not workspace-level — they don't persist across presentations.
- For a new presentation: copy a template slide from a pre-styled deck to bypass setup.

---

### PowerPoint

**Setup**:
1. *Design → Variants → Colors → Customize Colors*. Paste hexes into the 12 slots from §1's PowerPoint column. Save the palette as "{{ brand_name }}".
2. *Design → Variants → Fonts → Customize Fonts*. Set heading + body. Save.
3. At save time: *File → Options → Save → Embed fonts in the file → Embed all characters* — recipients see the deck exactly as designed without the fonts installed.

**Typography fallback chain**:
- Heading: `{{ powerpoint_heading_chain }}`
  - *Rationale*: {{ powerpoint_heading_rationale }}
- Body: `{{ powerpoint_body_chain }}`
  - *Rationale*: {{ powerpoint_body_rationale }}

**Probe notes**:
{{ powerpoint_probe_notes_list }}

**Caveats**:
- Mac and Windows render paragraph spacing slightly differently. Verify on both if cross-platform fidelity matters.
- Smart Art and chart palettes can override the theme — check *Format → Chart Styles* and *Format → Smart Art Styles* if visuals look off.
- PowerPoint for the Web has limited theme-customization features; the desktop app is the canonical authoring tool.

---

### Keynote

**Setup**:
1. *Document inspector → Colors → Edit custom palette*. Add the slot 1–6 hexes from §1's Keynote column.
2. *View → Show Styles Drawer*. Define Title, Heading, Subheading, Body, Caption to match §2.
3. Master slides: apply title / content / divider layouts via *View → Show Master Slides*.

**Typography fallback chain**:
- Heading: `{{ keynote_heading_chain }}`
  - *Rationale*: {{ keynote_heading_rationale }}
- Body: `{{ keynote_body_chain }}`
  - *Rationale*: {{ keynote_body_rationale }}

**Probe notes**:
{{ keynote_probe_notes_list }}

**Caveats**:
- `.key` files do **not** embed fonts. Recipients see substitutes if the font isn't installed locally.
- For cross-machine fidelity: *Export to → PowerPoint → Include Fonts* (PPTX embeds), or PDF (rasterizes — loses text selectability).
- Install custom brand fonts via *Font Book → File → Add Fonts…* on the authoring machine.

---

### Canva (Pro)

**Setup**:
1. *Brand kit → Add new brand kit → Name: "{{ brand_name }}"*. Paste each hex from §1's Canva column into Brand colors.
2. *Brand fonts → Upload font*: upload heading + body family files (`.ttf` / `.otf` / `.woff` / `.woff2`).
3. Set defaults: heading family for Titles, body family for Body.
4. Logos: upload `logo-construction.svg` variants via *Brand kit → Logos → Upload*.
5. Photos: upload approved imagery to *Brand kit → Photos* so team members use them instead of stock.

**Typography fallback chain**:
- Heading: custom upload (no fallback needed when the brand font is uploaded).
- Body: custom upload.

**Caveats**:
- Exported designs convert fonts to outlines at certain resolutions. Always preview at actual size before sharing.
- Brand kit color and font settings only apply when team members select the brand kit in the design.

---

### Canva (Free)

**Setup**:
1. *Brand kit → Add new brand kit*. Paste the three Free-column hexes (color 1 / 2 / 3) — the Free plan limit.
2. Use library fonts matching the brand's typography character (no upload available).
3. For additional brand hexes beyond 3, paste manually into each design's color picker.

**Typography fallback chain**:
- Heading: `{{ canva_free_heading_chain }}`
  - *Rationale*: {{ canva_free_heading_rationale }}
- Body: `{{ canva_free_body_chain }}`
  - *Rationale*: {{ canva_free_body_rationale }}

**Caveats**:
- Canva's font library rotates. If the listed fallback isn't available, pick the nearest character-compatible option.
- 3-color Brand Kit limit makes brand enforcement harder. Upgrade to Pro for team adoption.
- No custom font upload is available on the Free plan — designs must use library fonts only.

---

### Figma (Tokens Studio)

**Setup**:
1. Install the Tokens Studio plugin in Figma (free for basic use; paid for some advanced features).
2. *Plugins → Tokens Studio → Tools → Load from JSON*.
3. Select `theme-figma.json`. The plugin imports primitive, semantic, and component tokens as Figma Variables.

**Typography fallback chain**:
- Heading: `{{ figma_heading_chain }}`
  - *Rationale*: {{ figma_heading_rationale }}
- Body: `{{ figma_body_chain }}`
  - *Rationale*: {{ figma_body_rationale }}

**Caveats**:
- Tokens Studio is a third-party plugin; the import file is provided, but you're depending on the plugin's continued availability.
- Figma's native Variables feature has been catching up — Tokens Studio's main edge today is multi-mode + cross-token aliasing.
- Re-import the JSON when the brand updates `tokens.json` to pull in token-value changes.

---

## 5. Where the source values come from

This document is generated from the brand's canonical token set:

- `tokens.json` — the authoritative source; W3C DTCG format
- `surface-translations.yaml` — declares which token path fills which surface slot

If a row above is empty for a given surface, that surface doesn't expose a slot for that role — apply the value manually where it appears in your work.
