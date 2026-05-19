# Catalyne DM Hard Rules — Full Reference

These rules are the deliberate output of comparing multiple DM-writing approaches against the rubric in `dm-rubric.md`. Every rule was added because dropping it cost measurable rubric points.

## Rule 1 — WIIFM mandatory

Every DM includes an explicit 5–10 word reciprocity offer signaling what the recipient gets from replying.

**Why:** Peer-to-peer openers without WIIFM cap reply rates because the recipient has no answer to "why bother?". The 2026 LinkedIn benchmarks consistently show explicit value-exchange clauses lift reply rates 15–30%.

**Patterns:**

- "Happy to share what we're seeing across [their specific space]"
- "Glad to swap notes on [specific peer pattern]"
- "Happy to compare notes on [adjacent challenge]"

**Anti-patterns (do NOT use):**

- "Worth a quick call?" → meeting ask, not WIIFM
- "Would love to chat" → vague, no exchange offered
- "Let me know if interested" → puts the work on them

## Rule 2 — No snark, no jabs

First-DM tone test: would a stranger feel laughed-at or laughed-with? If unclear, rewrite.

**Why:** Snark from someone they don't know reads as condescension. It poisons the rapport bridge regardless of how clever it is.

**Anti-patterns:**

- "without sounding like SEO circa 2018"
- "unlike most [category] which is glorified [thing]"
- "if you're tired of the AI hype" (assumes they are)
- Any rhetorical eye-roll

**Replacement pattern:** State the same observation neutrally. "fluent in how buyers actually search now" instead of "without sounding like SEO circa 2018."

## Rule 3 — Language rule

If **both** of the lead's last 2 posts are in **German**, write the DM in German. All other cases (English-only, mixed, Dutch, French, Portuguese, Slovenian, Japanese, anything else) → write the DM in English.

**Why:**

- The operator (Catalyne) speaks DE / EN / JP fluently. Writing in French, Portuguese, Slovenian etc. would be inauthentic and the conversation would have to switch languages anyway.
- Japanese founders deliberately receive English to test their internationalization readiness — Catalyne wants the conversation to continue in English.
- Mixed-language posters (e.g., Dutch + English) default to English because that's the lead's working international language already.

**Operational note:** "Both posts in German" means both `last_post_1_text` and `last_post_2_text` are predominantly German. If only one post exists and it's German, default to English (insufficient signal).

## Rule 4 — Always output both versions

Every lead gets:

- **v2 — 60–80 words, target 70.** The in-conversation DM, sent after a connection request is accepted.
- **v3 — ≤300 characters, HARD LIMIT.** The connection-request DM (LinkedIn's character cap).

**Why both:** v3 alone tempts shortcuts — too short means dropped WIIFM or vague trigger. Drafting v2 first forces the full thinking, then v3 is a deliberate compression that preserves trigger + bridge + WIIFM but tightens the question.

**Operational rule for compression:**

- Tighten WIIFM specificity from "Happy to share what we're seeing across other post-Series A sustainable-packaging teams selling into CPG" → "Happy to swap notes on what's working in the space."
- Switch open-ended question to a binary or near-binary.
- Drop softening framing ("Was mich interessieren würde," "Out of curiosity").
- Keep: the specific trigger reference, the rapport bridge, the WIIFM offer, the question.

## Rule 5 — No pitch, no meeting ask in the first DM

The first message earns the reply with curiosity, not commitment. Meeting requests in DM #1 cut reply rates roughly in half across 2026 benchmarks.

**OK:** open question, observation, peer insight, value-add offer.

**Not OK:** "15 min next week?" / "calendar link" / "Are you the right person for [product]?" / "We help X do Y" anywhere in the message.

## Rule 6 — No fabrication

If a trigger is "unclear" in the enrichment data, fall back to a recent post or company milestone you CAN cite. Never invent a fact, a quote, or a URL.

**Fallback ranking when triggers are weak:**

1. Most recent post text (even if older than 30 days) → use its actual content as the bridge
2. Confirmed company description → use a specific element of their positioning
3. Their qualification reason → use a fact already established

If none of those work and the trigger is genuinely thin, return the lead with a flagged note. Don't ship a DM that lies.

## Rule 7 — Format discipline

- No em-dashes inside the DM if the language is German (the German convention prefers commas / colons).
- No emojis unless the lead's posts heavily use them (mirror their style).
- No greetings beyond the first name ("Hi Katya," → just "Katya —" works fine).
- No sign-off if v3 (saves characters); v2 can end with "— [first name]" if it fits.
