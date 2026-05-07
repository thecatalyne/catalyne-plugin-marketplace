# Voice-to-Component Patterns

How brand voice traits map to concrete copy patterns in UI components. Loaded by `brand-build` when generating voice guidelines and by `brand-export` when rendering the LLM operating manual's `voice.implementation` section.

Closes the gap between voice discovery (what was captured) and voice implementation (how it renders in real product surfaces).

## Mapping Rules

### Formality Score → Copy Register

The `voice.formality` score (1-5) from discovery drives component copy register:

| Score | Register | Button | Form label | Empty state |
|-------|----------|--------|------------|-------------|
| 1 — very casual | Conversational, contractions OK, questions as prompts | "Let's go" | "Name?" | "Nothing here yet — want to add the first one?" |
| 2 — casual | Direct, contractions OK, friendly | "Get started" | "Your name" | "No items yet. Add one to get started." |
| 3 — neutral | Clear, action-oriented, no contractions | "Continue" | "Full name" | "No items." |
| 4 — formal | Polished, precise, no personal pronouns | "Proceed" | "Full legal name" | "No records available." |
| 5 — very formal | Authoritative, declarative | "Submit" | "Legal name" | "This list contains no entries." |

### Aaker Sincerity → Personal Pronouns

- **High (≥ 7)** — "we", "you", first person OK. Warm greetings acceptable in onboarding and success states.
- **Medium (4-6)** — Neutral. Avoid pronouns in confirmation dialogs and error states; keep them in onboarding.
- **Low (≤ 3)** — Avoid pronouns entirely. Focus on the object/action.

### Aaker Excitement → Verb Energy

- **High (≥ 7)** — Active, energetic verbs: "Launch", "Spark", "Unlock", "Ignite". Exclamation points permissible on success states only.
- **Medium (4-6)** — Standard action verbs: "Start", "Save", "Send". No exclamation points.
- **Low (≤ 3)** — Restrained verbs: "Confirm", "Record", "Submit". Never exclamation points.

### Aaker Competence → Specificity

- **High (≥ 7)** — Name the exact object: "Export 3 tokens as CSS" rather than "Export".
- **Low (≤ 3)** — Generic action labels are fine: "Export", "Save", "Continue".

### Never-Say List → Pattern Substitution

Every entry in `voice.never_say[]` must ship with a replacement. When rendering component copy:

1. If proposed copy contains a banned word, substitute the paired replacement.
2. If no replacement is listed, fall back to the semantic nearest neighbor in `voice.language.preferred[]`.
3. Log the substitution to the methods ledger so reviewers can see the replacement was intentional.

### Specificity Test

Every piece of component copy must pass one check: **could a competitor brand use this exact string?** If yes, it's too generic — apply at least one of:

- Name the specific object using brand terminology from `voice.language.brand_terms[]`.
- Reference a specific brand promise from `positioning.promise`.
- Use a signature verb from the Excitement/Competence mappings above.

## Component-by-Component Defaults

### Buttons

- Label length: ≤ 3 words when Competence ≥ 6; otherwise ≤ 5.
- Verb-first when Excitement ≥ 5; noun-first otherwise.
- Destructive actions always specific: "Delete brand-identity.yaml" not "Delete".
- Secondary/ghost actions match the same register as the primary — never mix formality levels in one button group.

### Form Labels

- Match formality register from the table above.
- Error messages: same register, but always name the specific problem ("Email must include @") rather than generic ("Invalid input").
- Placeholder text: never substitute for the label; use it only for input hints ("e.g. jane@company.com").

### Empty States

- High Sincerity: inviting tone, ends with a call-to-action question.
- Low Sincerity: factual, no call-to-action.
- Every empty state names what the list/area is for — "No brand identity files yet" beats "No items".

### Confirmations & Dialogs

- Yes/No verbs must match the action. Avoid "OK / Cancel" for destructive actions — use "Delete / Keep" or similar pairs.
- Formality register dictates form: full sentences ("Are you sure you want to delete this?") vs. imperative ("Delete this brand?").
- Never use "Are you sure?" alone — always name the consequence.

### Onboarding & First-Run

- Sincerity dominates over Formality here. A formal brand can still open warmly if Sincerity ≥ 6.
- Use `positioning.promise` verbatim somewhere in the first screen if it's under 15 words.

## When to Override

These are defaults — not laws. Individual brands may override at the `voice.component_overrides[]` level in `brand-identity.yaml`. Record every override with a one-line rationale so governance reviewers can audit the drift.

## Relationship to Other References

- Load with `personality-dimensions.md` when the voice implementation needs to cite specific Aaker scores.
- Load with `scoring-criteria.md` when evaluating whether draft component copy meets the specificity test.
- `brand-build` consults this during voice guideline generation; `brand-export` consults it when producing the `voice` and `output_constraints` blocks of `brand.extensions.yaml`.
