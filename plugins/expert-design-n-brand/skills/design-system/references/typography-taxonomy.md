# Typography Character Taxonomy

Purpose: classify a typeface by its visual character so that when the primary family isn't available on a platform, the substitution logic picks a character-appropriate alternative — not a random one.

Every brand typeface in `brand-identity.yaml` carries a `character` slug from this list. Slugs are lowercase, hyphenated, stable (changing one breaks every brand manifest downstream).

---

## 1. geometric-sans-light

Geometric sans-serifs tuned for low-weight rendering (Light 300 / Thin 200). Circles are near-perfect, proportions are wide, ascenders are tall, and the design reads "calm, modern, editorial" at display sizes.

- **Shape**: geometric, single-story 'a' common, circular 'o'
- **Weight palette**: typically 100–900 with a crucial 300 weight
- **Aperture**: open but not humanist
- **Exemplars**: Satoshi, Jost, Nunito Sans, Manrope, Quicksand, Gotham Light
- **When chosen**: modern tech, wellness, editorial, brands that want "airy" and "intentional" without warmth

## 2. humanist-sans

Sans-serifs with calligraphic DNA — slightly varying stroke widths, two-story 'a', humanist proportions. Workhorse UI type.

- **Shape**: slightly narrower than geometric, open apertures
- **Weight palette**: typically 300–800, 400 is the anchor
- **Aperture**: wide, legible at small sizes
- **Exemplars**: Inter, Source Sans 3, PT Sans, Lato, Open Sans, IBM Plex Sans, Söhne, Roboto (hybrid)
- **When chosen**: product UI, documentation, brands that prioritize readability over distinctive voice

## 3. neo-grotesque

Mid-20th-century Swiss sans-serifs. Closed apertures, tighter proportions, "neutral" voice. Heavier than humanist sans.

- **Shape**: condensed-feeling, geometric but not circular, tight apertures
- **Weight palette**: 300–900
- **Aperture**: closed ('a', 'e' have small openings)
- **Exemplars**: Helvetica, Helvetica Neue, Arial, Univers, Akzidenz-Grotesk, Inter Tight
- **When chosen**: brands invoking Swiss design, institutional neutrality, industrial/manufacturing voice

## 4. humanist-serif

Serifs designed for screen and long-form reading. Sturdy slabs of ink, generous x-height, traditional but comfortable.

- **Shape**: bracketed serifs, moderate contrast, open counters
- **Weight palette**: 300–900 but often 4-weight range
- **Exemplars**: Source Serif 4, Lora, Merriweather, Crimson Pro, Libre Caslon
- **When chosen**: editorial, publishing, long-form content, brands that want warmth without being "old"

## 5. modern-serif

High-contrast "Didone" serifs. Thin hairlines, heavy verticals, fashion/luxury vocabulary.

- **Shape**: vertical axis, extreme thick/thin contrast, flat serifs
- **Weight palette**: 400–900 typically; light weights risk hairline dropout
- **Exemplars**: Playfair Display, Didot, Bodoni, Tiempos Headline
- **When chosen**: luxury, fashion, editorial magazines, brands invoking elegance/formality

## 6. display-serif

Expressive, character-forward serifs. Often variable, often "wonky." Heavier personality than modern-serif.

- **Shape**: often variable (Fraunces has a wonk axis), exaggerated curves
- **Weight palette**: full range, frequently variable
- **Exemplars**: Fraunces, Canela, Recoleta, DM Serif Display, Abril Fatface
- **When chosen**: brands that want personality + editorial credibility, content studios, publications with a POV

## 7. display-sans

Heavy, impact sans-serifs. Designed for headlines at 48pt+. Often condensed or extended, always expressive.

- **Shape**: extreme weights, often condensed, tight tracking
- **Weight palette**: usually 700–1000
- **Exemplars**: Obviously, Monument Grotesk, Druk, Bebas Neue, Antonio
- **When chosen**: agencies, cultural brands, editorial covers, merch-first brands

## 8. slab-serif

Square serifs, low contrast. Feels industrial/typewriter-adjacent.

- **Shape**: blocky serifs, even stroke weight
- **Weight palette**: 300–800
- **Exemplars**: Roboto Slab, Zilla Slab, Arvo, Bitter, Sentinel, Tiempos Slab
- **When chosen**: brands with industrial, academic, or typewriter voice; editorial pairing with humanist-sans

## 9. mono-humanist

Monospace with humanist DNA. Warm, readable, feels "software-craft."

- **Shape**: humanist proportions forced to monospace grid
- **Weight palette**: 300–700
- **Exemplars**: JetBrains Mono, Fira Code, IBM Plex Mono, Commit Mono
- **When chosen**: developer tools, technical brands, code examples inside non-technical brands

## 10. mono-geometric

Monospace with geometric DNA. Colder, more "retrofuturist."

- **Shape**: circular, wide, sometimes with programming ligatures
- **Weight palette**: 400–700 commonly
- **Exemplars**: Space Mono, Roboto Mono, DM Mono, Major Mono Display
- **When chosen**: brands with retro-tech or cypherpunk voice

## 11. script-hand

Handwritten, brush, or script faces. Not typically used for body.

- **Exemplars**: Caveat, Dancing Script, Homemade Apple, Pacifico, Shadows Into Light
- **When chosen**: personal brands, creative studios, accent type only

## 12. technical-display

Monospaced or grid-locked display type; often OCR-derived, MICR-derived, or stencil/industrial. Rare as a primary, common as an accent.

- **Exemplars**: Major Mono Display, Share Tech Mono, VT323, Silkscreen
- **When chosen**: cypherpunk, data-forward, industrial brands

---

## Cross-reference table (for substitution logic)

Used by `brand-build` when populating `typography.per_platform.*.heading_chain` and `body_chain`. When the primary isn't available on a platform, walk the compatible slugs in order; within each slug, pick the best-ranked entry from `platform-fonts.yaml`.

| character-slug        | compatible fallback slugs                              |
|-----------------------|--------------------------------------------------------|
| geometric-sans-light  | geometric-sans-light > humanist-sans > neo-grotesque   |
| humanist-sans         | humanist-sans > neo-grotesque > geometric-sans-light   |
| neo-grotesque         | neo-grotesque > humanist-sans > geometric-sans-light   |
| humanist-serif        | humanist-serif > slab-serif > modern-serif             |
| modern-serif          | modern-serif > display-serif > humanist-serif          |
| display-serif         | display-serif > modern-serif > humanist-serif          |
| display-sans          | display-sans > neo-grotesque (heavy) > geometric-sans-light (heavy) |
| slab-serif            | slab-serif > humanist-serif                            |
| mono-humanist         | mono-humanist > mono-geometric                         |
| mono-geometric        | mono-geometric > mono-humanist                         |
| script-hand           | script-hand only; no safe fallback — flag and warn     |
| technical-display     | technical-display > mono-geometric                     |

---

## Classification process (used by brand-discover)

When the user names their brand typefaces, the discover skill offers a curated picker (not free text) from the 12 categories above, with exemplars shown alongside each option. The user classifies heading, body, and optionally display/mono. If the chosen family is already an exemplar, the classification is auto-suggested; the user confirms or overrides.

Never infer character from the font name alone — `Söhne` and `Source Sans` both contain "S" but classify into different categories. Always confirm with the user.
