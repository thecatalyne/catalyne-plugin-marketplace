<!-- TIER 1 AUTHOR NOTE — external reference. Renders to `governance.md` that ships to clients / consultants / designers / developers. Keep reader-visible content in end-user language about the *brand system*; references to the plugin's internal workflow do not belong here. -->

# {{brand_name}} Brand — Governance

> Who owns it, how it evolves, when it breaks.

> **Canonical vocabulary source.** Token names, role labels, surface slot names, and CSS/Tailwind/Figma keys used in this document are defined in `assets/platform-matrix-template.md`. If a name here appears to disagree with the Platform Matrix, the Platform Matrix wins.

**Version**: {{version}} · **Status**: {{status}} · **Generated**: {{generated_date}}

---

## Ownership

| Role | Owner | Responsibility |
|---|---|---|
| Brand steward | {{steward_name}} · `{{steward_email}}` | Canonical decisions on voice, palette, principles. Final approval on breaking changes. |
| Design system | {{ds_owner_or_open}} | Token updates, component library, Figma library. |
| Content | {{content_owner_or_open}} | Copy patterns, voice card sort, never-say list. |
| Accessibility | {{a11y_owner_or_open}} | WCAG contrast validation, reduced-motion, keyboard paths. |
| Brand system maintenance | {{maintenance_owner_or_open}} | Token updates, template changes, quality verification. |

{{ownership_notes}}

---

## Versioning — SemVer

Format: `vMAJOR.MINOR.PATCH`.

| Bump | Trigger | Examples |
|---|---|---|
| **MAJOR** | Breaking change to anchor palette, principles, archetype, or voice constraints. Requires deprecation window. | {{major_examples}} |
| **MINOR** | Additive, backward-compatible. | {{minor_examples}} |
| **PATCH** | Fix, typo, contrast tweak within same token role. | {{patch_examples}} |

Pre-release suffixes allowed: `{{version_next}}-beta.1`.

---

## Changelog

<!-- Populate from brand-identity.yaml → system.changelog[] OR construct from per-version synthesis records -->

### {{current_version}} — {{current_date}} (current)

{{current_version_notes}}

<!-- Repeat per prior version -->

---

## Deprecation policy

**Minimum window: 90 days.** When a MAJOR-bump change lands:

1. **Announce** — add deprecation note to `governance.md` changelog with sunset date.
2. **Dual-ship** — keep deprecated token/pattern alongside new one for the window. Deprecated entries get a `$deprecated: true` field in `tokens.json` plus a `$deprecated.reason` and `$deprecated.replacement` pointer.
3. **Warn** — downstream consumers see deprecation notice in `tokens.json` parser output.
4. **Remove** — at sunset date, delete deprecated entry. Release as next MAJOR.

---

## Contribution flow

For additions to the system:

1. **Open a proposal** — brief markdown doc in `docs/proposals/` with:
   - Problem statement
   - Proposed addition (spec'd at same detail as existing entries)
   - Example usage (concrete)
   - Anti-pattern (what's NOT being added, why)
   - Impact (MAJOR/MINOR/PATCH)
2. **Review by brand steward** — aligns against principles, coherence impact, anti-inspiration list.
3. **Promote** — merge into the brand system; regenerate artifacts; bump version.

Review criteria — accepted:
- Fills a real gap (not speculative)
- Composes with existing primitives (doesn't create parallel system)
- Has anti-pattern specified alongside the pattern
- Passes the Specificity Test if voice-related
- Does not lower the coherence score

Review criteria — rejected:
- "Nice to have" without concrete use case
- Additions that would require also deprecating something existing
- Anything that violates a stated brand principle

---

## Decision log (ADRs)

<!-- ≥ 3 ADRs required. Format per entry: -->

### ADR-001 — {{adr_1_date}} · {{adr_1_title}}

**Context**: {{adr_1_context}}

**Decision**: {{adr_1_decision}}

**Alternatives considered**: {{adr_1_alternatives}}

**Consequence**: {{adr_1_consequence}}

<!-- Repeat per ADR -->

---

## Health checks

Run these quarterly or on every MAJOR bump:

- [ ] Coherence score ≥ {{coherence_floor}} (current: {{coherence_current}})
- [ ] Paul Rand criteria ≥ {{rand_floor}} (current: {{rand_current}})
- [ ] WCAG AA contrast minimum on all semantic color pairs (current: {{wcag_pairs_validated}} pairs validated)
- [ ] Design tokens validate against DTCG W3C 2025.10
- [ ] `brand.md` conforms to the brand.md v0.2.0 specification
- [ ] `brand.extensions.yaml` parses and its `self_validation` block passes
- [ ] Platform matrix covers ≥ 5 shipped platforms with caveats populated
- [ ] No never-say entries appear in approved copy (reference bank)
- [ ] Principles count unchanged OR documented in ADR if changed

---

## When to bump major

A checklist. If any are true, next release is MAJOR:

- [ ] Anchor set changed (add, remove, or renamed)
- [ ] Any principle removed or renamed (rewording a rationale is PATCH)
- [ ] Archetype changed
- [ ] Voice `formality.home` shifted
- [ ] A banned word removed from `voice.banned[]`
- [ ] A required section removed from the template
- [ ] A palette role remapped

---

## File inventory

Three tiers of artifacts:

**External reference (public-facing — clients, consultants, agencies, developers)**:

| File | Purpose |
|---|---|
| `brand-guidelines.html` + `.pdf` | The definitive brand guide |
| `brand-quickref.md` | One-pager card |
| `tokens.css` | CSS custom properties |
| `tokens.json` | DTCG W3C design tokens |
| `logo-construction.svg` | Signature device construction + misuse grid |
| `illustration-system.html` | Illustration primitives + emotion inventory |
| `photography-reference-grid.html` | Photography do/don't gallery |
| `platform-matrix.md` | Single consolidated cross-surface reference. Master tables (rows = tokens, columns = surfaces) for color / typography / form & spacing, plus per-platform sub-sections covering setup steps, typography fallback chains, probe notes, and caveats. |
| `governance.md` | This file |
| `tailwind.config.js` | Tailwind v4 theme config |
| `theme-figma.json` | Figma Tokens Studio import |
| `email-template.html` | HTML email base |

**Operator / process record (for the team maintaining the brand)**:

| File | Purpose |
|---|---|
| `brand-methods.html` + `.pdf` | Process record — every technique applied, with quotes |
| `synthesis-report.md` | Cross-participant discovery synthesis |

**LLM-optimized (machine-readable sibling for automated generation + validation)**:

| File | Purpose |
|---|---|
| `brand.md` | Canonical brand definition (brand.md v0.2.0 spec) |
| `brand.extensions.yaml` | Plugin-specific structured rules (tone matrix, output constraints, platforms, etc.) |

---

*End of governance. Previous versions archived at git tags.*
