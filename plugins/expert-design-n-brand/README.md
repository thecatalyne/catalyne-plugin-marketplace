# expert-design-n-brand

A Claude Code plugin that guides non-designers through structured brand identity development — from discovery through design system generation.

## What It Does

1. **Discover** — Each team member runs a guided brand elicitation session (~30-45 min). Multiple techniques per dimension (positioning, personality, visual, voice) adapt to how each person thinks.
2. **Synthesize** — Compare all team members' inputs. See where you agree, where you diverge, and why it matters. Resolve conflicts through facilitated conversation.
3. **Build** — Generate a complete design system from resolved synthesis: color palette, typography scale, design principles, form language, voice guidelines.
4. **Export** — Produce concrete artifacts: CSS custom properties, JSON design tokens, interactive HTML design system document, one-page brand quick reference card.

## Quick Start

### Install

Add the Catalyne plugin marketplace, then install the plugin:

```
/plugin marketplace add thecatalyne/catalyne-plugin-marketplace
/plugin install expert-design-n-brand@catalyne-plugin-marketplace
```

### Run

```
# First time? Start here for a warm welcome and process overview — or
# run it anytime to see where things stand.
/expert-design-n-brand:brand-guide

# Start brand discovery for yourself
/expert-design-n-brand:brand-discover

# After 2+ team members complete discovery
/expert-design-n-brand:brand-synthesize

# Generate design system from resolved synthesis
/expert-design-n-brand:brand-build

# Export artifacts (self-verifies before declaring done)
/expert-design-n-brand:brand-export
```

> Verification is **inlined into the producer skills** — `brand-build`,
> `brand-synthesize`, and `brand-export` each render → walk the canonical
> checklist → apply one bounded auto-fix pass → re-verify → report. There
> is no separate verify command; the artifacts arrive already checked.

### How It Works

The plugin creates a single `brand-identity.yaml` file in your current working directory. All generated artifacts also land under `./brand-assets/` relative to that directory. This is your brand's source of truth — every discovery session, synthesis run, and design system build reads from and writes to this one file.

The file is human-readable YAML. You can edit it directly, share it with non-Claude users, or use it as input to any design toolchain.

### Working Directory

`cd` into your brand project directory **before** invoking any skill. Everything is CWD-relative:

- `./brand-identity.yaml` — the source-of-truth file
- `./brand-assets/` — generated artifacts (tokens, HTML, PDFs, quickref)
- `./brand-assets/{name}-tests/` — per-participant checkpoint HTML files

If you start from the wrong directory, artifacts land there. No env vars required.

### For Teams

Each team member runs `/brand-discover` independently. The plugin keeps each person's responses isolated within the same file. When ready, `/brand-synthesize` compares everyone's inputs and identifies consensus and divergences.

No conversation context is needed between sessions — the YAML file is the complete handoff.

## Without Claude Code

The reference documents in this plugin are valuable standalone:

- `skills/brand-knowledge/references/` — Jungian archetypes, Aaker personality dimensions, quality scoring frameworks
- `skills/elicitation-engine/references/` — Complete technique library for brand workshops, curated palettes/typography/voice examples
- `skills/design-system/references/` — Token architecture guides, design rules (color, typography, motion)
- `assets/brand-identity-template.yaml` — The full brand identity schema you can fill manually

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| `brand-guide` | Skill (user-invoked) | Welcome for first-time users, status report + next-step recommendation for returning users |
| `brand-discover` | Skill (user-invoked) | Start/resume brand discovery for a team member |
| `brand-synthesize` | Skill (user-invoked) | Compare and merge team inputs |
| `brand-build` | Skill (user-invoked) | Generate design system from synthesis |
| `brand-export` | Skill (user-invoked) | Export tokens, HTML doc, quick reference, print PDF; self-verifies and auto-fixes one pass before reporting |
| `elicitation-engine` | Skill (auto-activating reference) | Technique library and elicitation patterns |
| `design-system` | Skill (auto-activating reference) | Token architecture and design rules |
| `brand-knowledge` | Skill (auto-activating reference) | Brand frameworks, archetypes, scoring, voice-to-component patterns |

## Prerequisites

- Claude Code
- Core discovery, synthesis, build, and export flows are conversational — no external services required
- Optional AI-prompting research technique in `/brand-discover` uses `WebSearch`/`WebFetch` when active
- `scripts/validate-contrast.sh` requires `bc` (default on macOS; install via your package manager on minimal Linux)
- `scripts/validate-structure.py` requires Python 3 with `PyYAML` (typically pre-installed)
- PDF page-image verification probes `pdftoppm` (from `poppler`), then a headless browser (`chromium`/`chrome`/`msedge`); install one if you want pixel verification

## License

MIT
