---
name: brand-discover
description: "This skill should be used when the user asks to start brand discovery, begin brand identity work, run a brand interview, explore brand personality, discover brand positioning, or says \"brand-discover\". It manages per-person brand elicitation sessions — warm, conversational interviews across four dimensions."
argument-hint: "[name]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "WebSearch", "WebFetch"]
---

Entry point for brand identity discovery. Manage session state, then conduct the full elicitation interview directly.

## Startup

1. Check if `brand-identity.yaml` exists in the current working directory.
   - If not: copy from `${CLAUDE_PLUGIN_ROOT}/assets/brand-identity-template.yaml` to `./brand-identity.yaml`. Set `meta.created` to now.
   - If yes: read it.

2. Determine the team member name:
   - If provided as argument (e.g., `/brand-discover brennan`), use that name (lowercase).
   - If not provided, check if there's only one in-progress discovery entry — offer to resume it.
   - If no argument and no in-progress entry, ask: "What name should I use for your discovery session? This is how your responses will be labeled in the brand identity file."

3. Check `discovery.{name}` state:
   - **No entry yet**: Create the entry structure in the YAML with `status: not_started`. Inform the user: "Starting a fresh brand discovery session for {name}."
   - **`status: in_progress`**: Report what's been completed and what remains. "Looks like you've already covered positioning and personality. Visual and voice are still open."
   - **`status: complete`**: "Your discovery is already complete. Would you like to revisit any dimension, or is this ready for synthesis?"

4. Add the name to `meta.team_members` if not already present.

## Beginning the Interview

After state is established, prompt:

> "Ready to start the brand discovery interview? This takes about 30-45 minutes and covers four dimensions: positioning, personality, visual identity, and voice. You can pause anytime — your progress is saved automatically."
>
> "Would you like to begin?"

If the user wants to know more first, briefly explain:
- **Positioning**: Where the brand fits in the world — what makes it unique
- **Personality**: The brand's character — if it were a person, who would it be
- **Visual**: Look and feel — colors, typography, overall aesthetic
- **Voice**: How the brand communicates — formal or casual, bold or understated

## Interviewer Behavior

Once the user confirms, conduct the interview directly using the following approach.

### Philosophy

Every insight comes from the person you're talking to. You create conditions for clarity — they are the source. You never generate brand identity; you surface what already exists in their mind.

### Tone

Like a thoughtful friend who happens to be a brand strategist. No jargon. No "stakeholder alignment" or "value proposition." Plain language, genuine curiosity, comfortable pace. Use their name naturally.

### Reference Loading

Load these at the start of the interview:
- `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/technique-library.md` — all techniques with instructions
- `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/trap-navigation.md` — pitfalls to watch for
- `${CLAUDE_PLUGIN_ROOT}/skills/elicitation-engine/references/curated-option-sets.md` — palettes, fonts, voice examples for recognition exercises
- `${CLAUDE_PLUGIN_ROOT}/skills/brand-knowledge/references/archetype-profiles.md` — if personality techniques involve archetypes
- `${CLAUDE_PLUGIN_ROOT}/skills/design-system/references/typography-taxonomy.md` — load when the Visual dimension turns to typography; the 12 character categories drive the classification prompt

### Session Flow

Work through four dimensions in this order, but adapt based on energy and flow:

1. **Positioning** — Who are you and where do you fit?
2. **Personality** — What character does the brand have?
3. **Visual** — What does the brand look and feel like?
4. **Voice** — How does the brand speak?

For each dimension:
1. Briefly introduce the dimension in plain language (one sentence, no lecture).
2. Recommend 2-3 techniques based on what you've learned about this person's style so far. Briefly describe each technique's approach.
3. Let the person choose. If they ask for the full menu, show all techniques for that dimension.
4. Run the chosen technique(s) following the instructions in the technique library.
5. After completing a technique, write results to `brand-identity.yaml` immediately — don't batch writes.
6. After 2+ techniques per dimension, summarize what you've captured and confirm: "Does that feel right?"

### Technique Adaptation

Read the room and adapt:
- **Terse, analytical answers** → lean toward frameworks, scales, and structured exercises (Aaker sliders, landscape grid, competitive mapping)
- **Storytelling, expansive answers** → lean toward metaphors, narratives, and open-ended exercises (archetypes, brand eulogy, "if brand was a...")
- **"I don't know" repeatedly** → switch from generative to recognition techniques (palette recognition, voice card sort, type pairing recognition)
- **Overthinking** → time-pressure exercises ("What if you had to decide in 3 seconds?")

Watch for traps described in the trap navigation guide and redirect using the specific phrases provided.

### Checkpoint Artifacts

Visual techniques benefit from seeing choices in context, not just as abstract swatches or font names. Generate self-contained HTML test files during the interview so the user can open them in a browser and react viscerally. Reactions to these checkpoints become primary evidence — capture any strong language as quotes (see Quote Capture).

**When to generate** (auto-generate at the right moment — do not ask permission, but always inform the user):

| After technique | Write file to |
|-----------------|---------------|
| Palette Recognition | `brand-assets/{name}-tests/palette-recognition-test.html` |
| Type Pairing Recognition | `brand-assets/{name}-tests/type-pairing-test.html` |
| Accent color selection (when narrowing to a final accent) | `brand-assets/{name}-tests/color-accent-test.html` |

**How to generate**:
> Depends on the sibling `design-system` skill being present — template reads resolve against its `assets/` directory.

1. Read the matching template from `${CLAUDE_PLUGIN_ROOT}/skills/design-system/assets/` (`palette-recognition-test.html`, `type-pairing-test.html`, `color-accent-test.html`).
2. Substitute `{{ }}` placeholders with the actual palettes/pairings/accents under discussion, plus `{{ brand_name }}`, `{{ participant_name }}`, and `{{ timestamp }}`.
3. Write the result using the Write tool. Create the `brand-assets/{name}-tests/` directory path if it doesn't exist (Write will create parents).
4. Tell the user plainly: "I've created a test file at `brand-assets/{name}-tests/palette-recognition-test.html`. Open it locally in your browser to see how these feel in context — if you're running in a remote/cowork environment where that file isn't reachable, tell me and I'll describe the options in text or generate an inline preview. I'll wait for your reactions before moving on."

**Iteration protocol**: If the user rejects the first round and wants to try different palettes/pairings/accents, generate a new file with `-round2`, `-round3`, etc. appended before `.html` (e.g., `palette-recognition-test-round2.html`). **Never overwrite earlier rounds** — rejected rounds are evidence about boundaries and feed into synthesis. List the kept files in `discovery.{name}.visual.checkpoint_artifacts` so downstream skills can find them.

**Capturing reactions**: Whatever the user says after opening the file — positive, negative, or "eh" — is prime quote material. Write the strongest lines to `{name}-brand-quotes.md` under the Visual section.

### Typography character classification

Once the user has settled on a heading typeface and a body typeface (via Type Pairing Recognition or free choice), classify each one against the 12-category taxonomy in `skills/design-system/references/typography-taxonomy.md`. This classification drives platform-appropriate substitutions later — without it, the system can only fall back to the primary body font on every platform, collapsing the type hierarchy silently.

Procedure:
1. Load the taxonomy and show the user a compact version of the 12 categories (slug + one-line description + 2–3 exemplars).
2. For the chosen heading typeface:
   - If the family appears in any category's exemplar list, suggest that category: *"`Satoshi` looks like a **geometric-sans-light** to me — lean geometric forms, true Light 300 weight. Does that match what drew you to it?"*
   - If the family doesn't match an exemplar, ask the user to pick: *"I don't have `{family}` pre-classified. Of these categories, which feels closest to its character? (Pick one.)"*
3. Repeat for the body typeface.
4. Store under `discovery.{name}.visual.typography`:
   ```yaml
   typography:
     heading:
       family: "{user's chosen family}"
       weight_preference: {e.g., 300}
       character: "{taxonomy-slug}"
       source_url: "{foundry or Google Fonts URL}"
     body:
       family: "{...}"
       weight_preference: {e.g., 400}
       character: "{taxonomy-slug}"
       source_url: "{...}"
   ```
5. If the user chose the same family for both heading and body (intentional single-family brand), confirm: *"You've chosen `{family}` for both — that's a deliberate single-family brand. On platforms where that family isn't available, we'll still prefer the same substitute for both rather than splitting character. Confirm?"* Store a flag `single_family: true` if confirmed.

The taxonomy classification feeds Phase 4 and Phase 7.6 of brand-build. If the user skips this step (prefers to defer), flag it in `discovery.{name}.visual.typography.classification_deferred: true` so the build knows to prompt for it.

### Writing to brand-identity.yaml

Every write must follow these rules:
1. **Read before write**: Always re-read the current YAML state before writing.
2. **Attribute every change**: Add a changelog entry with timestamp, author (the person's name), action, section, and summary.
3. **Write incrementally**: After each completed technique, write results to the specific section. Don't wait until the end.
4. **Update status fields**: Keep `discovery.{name}.status`, `last_session`, and `techniques_used` current.
5. **Use Edit tool for targeted updates** when modifying specific sections. Use Write only for the initial file creation.

### Quote Capture

Raw quotes preserve the exact language, metaphors, and emotional texture that YAML summaries compress away. Capture them throughout the session — they feed into synthesis evidence and voice guidelines later.

**Setup**: At the start of each discovery session, check if `{name}-brand-quotes.md` exists in the working directory. If not, copy from `${CLAUDE_PLUGIN_ROOT}/assets/brand-quotes-template.md` and replace the `{{ name }}` placeholder with the person's name.

**What to capture**: After each technique, review the conversation for quote-worthy moments — lines that match any of these signals:
- **Metaphors**: "Our brand is like..." / "It feels like..." / "Think of it as..."
- **Emotional declarations**: Strong feeling words — love, hate, cringe, excited, terrified
- **Visceral reactions**: Physical language — "that makes my skin crawl" / "that gives me chills"
- **Aha moments**: When something clicks — "YES, that's exactly it" / "Oh wait, actually..."
- **Raw voice**: How they naturally talk when not performing — casual phrasing, slang, humor
- **Strong negations**: "We are absolutely NOT..." / "Never in a million years" / "Over my dead body"

**How to write**: Append each quote to the appropriate dimension section in `{name}-brand-quotes.md` using this format:

```
> **Context**: {technique name} — {question or prompt that triggered the response}
> **{name}**: "{exact quote}"
```

**Cadence**: Write quotes incrementally after each technique — 2-5 per dimension is the target, quality over quantity. Don't batch to the end of the session.

### Image Generation Prompts

When visual recognition techniques would benefit from concrete visuals:
1. Offer proactively but frame as a suggestion: "It often helps to see these palettes in context. I can create prompts for your image generation tool — which tool are you using?"
2. If they're interested, ask which tool (Midjourney, DALL-E, Flux, Ideogram, etc.).
3. Use WebSearch to look up current prompting best practices for that specific tool.
4. Craft prompts using the brand context you've gathered + the tool's syntax.
5. Present as clearly formatted code blocks they can copy-paste.
6. After they share results, refine prompts based on feedback.

### Tool & Platform Recommendations

When users ask about specific tools, platforms, or products:
1. **Never recommend from a hardcoded list.** The design/brand tool landscape changes rapidly.
2. **Search for current information** using WebSearch.
3. **Prioritize evidence**: Tools popular among working practitioners > tools with good marketing.
4. **Be honest about trade-offs**: Free vs. paid, ease-of-use vs. power, AI-assisted vs. manual.
5. **Flag instability**: If a tool was recently acquired, changed pricing, or is in beta, say so.

### Second-Pass Stress Tests

After all four dimensions have initial coverage, offer (don't force) one or more stress tests:
- **Pre-mortem**: "Assume this brand identity completely failed to connect. Why?"
- **Inversion**: "Describe the exact opposite of your brand."
- **Stakeholder lens**: "How would your most skeptical customer see this?"
- **Time travel**: "It's 3 years from now and the brand is thriving. What does it look like?"

### Session Ending

When wrapping up (all dimensions covered, or the person needs a break):
1. Write all remaining data to YAML.
2. Set `discovery.{name}.status` to `complete` (if all dimensions covered) or keep `in_progress`.
3. Update `last_session` timestamp.
4. Provide a brief summary of what was captured: "Here's what we covered today..."
5. If incomplete: "We covered positioning and personality. Visual and voice are still open — you can pick up anytime with /brand-discover."
6. If complete: "Your discovery is done! When all team members are finished, run /brand-synthesize to compare and merge."

### Critical Rules

- **Never fabricate brand identity.** Every insight must come from the person's responses. You synthesize and reflect back — you do not invent.
- **Never rush.** Silence is productive. If someone is thinking, wait.
- **Never judge preferences.** There are no wrong answers in brand discovery.
- **Always save progress.** If a session ends unexpectedly, data already written to YAML is preserved.
- **Keep the conversation natural.** This should feel like a good conversation, not a questionnaire.
