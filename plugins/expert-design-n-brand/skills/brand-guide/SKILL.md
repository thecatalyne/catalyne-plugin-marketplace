---
name: brand-guide
description: "This skill should be used when the user first opens the project, asks how to begin, says \"where do I start\", \"what is this\", checks brand progress, asks what to do next or what step they're on, wants a status report, or says \"brand-guide\", \"brand-start\", or \"brand-status\". Welcomes first-time users with a warm overview, shows current workflow state for returning users, and always recommends the next action."
allowed-tools: ["Read", "Grep", "Glob"]
---

Orient the user to the brand identity toolkit. For first-time users (no `brand-identity.yaml` in the current working directory), deliver a warm welcome and explain the four-phase process. For returning users, show a status report derived from the file and recommend the next action. Never conduct discovery, synthesis, build, or export from here — those are separate skills. This is the doormat, not the living room.

## Startup

1. Read `brand-identity.yaml` from the current working directory.
   - **Not found** → deliver the **Cold Welcome** below, then stop.
   - **Found** → deliver the **Status Report** below, then stop.

2. Never write to `brand-identity.yaml`. If the user answers by saying "let's begin" or similar, tell them to run `/brand-discover` — do not silently transition.

## Cold Welcome

Deliver this message when no `brand-identity.yaml` is present:

> Welcome. This is a guided brand identity toolkit — built for founders and teams who are not designers. You'll end with a real, usable design system: hex codes, font choices, voice guidelines, and concrete artifacts you can hand to a developer.
>
> **Here's how it works — four phases, always in order:**
>
> 1. **Discover** — A warm conversational interview. Each team member takes their own session (about 30-45 minutes) to articulate what the brand stands for, how it feels, how it looks, and how it speaks. Every insight comes from you; nothing is invented.
> 2. **Synthesize** — If more than one person did discovery, we compare everyone's responses side by side. You'll see where you already agree, where you diverge, and what those differences mean. Solo founders get a self-consistency check instead.
> 3. **Build** — The toolkit generates a complete design system from what was captured: design principles, a color palette with accessibility-validated contrast, typography, form language, voice guidelines.
> 4. **Export** — Concrete files you can use anywhere: CSS tokens, JSON tokens, an interactive HTML design system document, a printable PDF, and a one-page brand quick reference.
>
> **Everything lives in one file** — `brand-identity.yaml` in your working directory. You can read it, edit it, share it, or start over any time.
>
> | What you want to do | Run this |
> |---------------------|----------|
> | Start a discovery session | `/brand-discover` |
> | Compare team inputs (2+ people done) | `/brand-synthesize` |
> | Generate the design system | `/brand-build` |
> | Export final artifacts | `/brand-export` |
> | Check progress any time | `/brand-guide` |
>
> **Ready to begin?** Run `/brand-discover` and I'll walk you through your first session.

## Status Report

When `brand-identity.yaml` exists, deliver a structured overview. Open with a one-line greeting using `meta.brand_name` if set.

### Phase

Show current phase from `meta.phase`: `discovery` | `synthesis` | `system` | `active`.

### Discovery Status

For each entry in `discovery.*`:

| Member | Status | Dimensions Covered | Techniques Used | Last Session |
|--------|--------|--------------------|-----------------|--------------|
| {name} | {status} | {list completed dimensions} | {count} | {last_session} |

Show which dimensions have data (positioning, personality, visual, voice) based on whether those sections are populated.

### Synthesis Status

If `synthesis.status` is not `not_started`:
- Status: {synthesis.status}
- Agreement score: {synthesis.agreement_score}
- Divergences: {count total} ({count unresolved} unresolved)
- Last run: {synthesis.last_run}

### Design System Status

If `system.status` is not `not_started`:
- Status: {system.status}
- Principles: {count}
- Color: {palette hex summary}
- Typography: {typeface names}
- Contrast validated: {yes/no}
- Last built: {system.last_built}

### Exported Artifacts

Check whether `brand-assets/` exists (relative to CWD) and list any generated files.

### Recent Activity

Show the last 5 entries from `meta.changelog[]` if present.

### Next Step

Pick the first matching row and present as a single one-line recommendation with the command to run:

| Condition | Recommendation |
|-----------|----------------|
| No `discovery.*` entries | "No discovery sessions recorded. Run `/brand-discover` to start your first session." |
| Any `discovery.{name}.status == "in_progress"` | "{name}'s discovery is in progress. Run `/brand-discover {name}` to resume." |
| All discoveries complete, `synthesis.status == "not_started"`, 1 person | "Solo discovery complete. Run `/brand-build` (or `/brand-synthesize` first for a self-consistency check)." |
| All discoveries complete, `synthesis.status == "not_started"`, 2+ people | "{N} discovery sessions complete; no synthesis yet. Run `/brand-synthesize` to compare team inputs." |
| `synthesis.status` is `draft` or `review` with unresolved divergences | "Synthesis has unresolved divergences. Run `/brand-synthesize` to work through them." |
| `synthesis.status == "complete"` and `system.status == "not_started"` | "Synthesis complete; design system not yet built. Run `/brand-build`." |
| `system.status` is `draft` or higher and `brand-assets/` missing | "Design system built; artifacts not yet exported. Run `/brand-export` to produce the final files." |
| `meta.phase == "active"` or all artifacts exist | "Brand identity is active. Edit `brand-identity.yaml` directly for updates." |

## Tone

Warm and welcoming in the Cold Welcome. Plain and informative in the Status Report. No jargon, no CLI syntax in prose — the command tables do the work. Keep each mode to one screen.
