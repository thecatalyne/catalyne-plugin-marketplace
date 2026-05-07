# Examples — try the plugin without running discovery yourself

This folder gives you two ways to evaluate the plugin without going through a full team brand-discovery first.

## `sample-brand-identity.yaml`

A fictional brand — **"Slow Press"**, an imagined small letterpress + reading room — with two fictional team members (`marin`, `theo`) who have already completed `/brand-discover`. Synthesis is marked complete with two real divergences resolved.

The file is set up so the next step is `/brand-build`. Run the plugin against it to see the full pipeline produce a real design system end-to-end.

### Use it

```bash
# 1. Copy the sample input to a fresh working directory
mkdir ~/slow-press && cd ~/slow-press
cp /path/to/this/repo/plugins/expert-design-n-brand/examples/sample-brand-identity.yaml ./brand-identity.yaml

# 2. Build the design system from the synthesis
# (in Claude Code, with the plugin installed)
/expert-design-n-brand:brand-build

# 3. Export all artifacts
/expert-design-n-brand:brand-export
```

After step 3, the directory will contain a `brand-assets/` folder with:

- `brand-guidelines.html` — the canonical interactive design system document
- `brand-guidelines.pdf` — print-ready version of the same
- `tokens.css` — CSS custom properties (W3C DTCG–compatible)
- `tokens.json` — JSON design tokens
- `brand-quickref.md` — one-page reference card
- `tailwind.config.js` — Tailwind preset
- `theme-figma.json` — Figma Tokens Studio import
- `platform-matrix.md` — cross-surface design map (Slides / Keynote / PowerPoint / Canva)
- `brand.md` + `brand-extensions.yaml` — LLM-readable brand definition
- `brand-methods.html` + `brand-methods.pdf` — process record showing which techniques produced which sections
- A few smaller companions (logo construction SVG, illustration system reference, photography grid, governance, email template)

## What "Slow Press" is and isn't

It's a **fictional brand** invented for this demo. It's not a Catalyne client, not a real business, and not modeled on any specific real-world press shop. Two fictional team members ("Marin" and "Theo") completed brand-discover with the plugin, and their inputs were synthesized into the consensus + divergences you see in the file.

Some things the demo brand is designed to exercise:

- **Two-stakeholder synthesis** — there are two actual divergences in the file (secondary archetype, typography pairing) so you can see how `/brand-build` and `/brand-export` reflect resolved divergences in the methods record.
- **Variable color depth** — the consensus has core roles only, no anchor set, no hue scales. You'll see brand-build expand this into a working palette during build.
- **Typography rules per surface** — the resolution to one of the divergences is a *per-surface* typography rule (all-serif for print, serif + sans for digital). This shows the plugin handling conditional design rules.
- **A real "never-say" list** — voice constraints that translate into the LLM-readable `brand.md` output.

## Want a faster preview?

If you'd rather see what the output *looks like* before installing anything, watch this folder — pre-rendered `sample-output/` files (the actual artifacts produced when running the steps above) will be published here in a follow-up release. For now, the most direct path is: install the plugin, run the three commands above, and look at what shows up under `brand-assets/`.
