---
name: catalynes-linkedin-dms
description: Catalyne's LinkedIn DM writing skill. Use when the user has a CSV of qualified+enriched leads (typically the output of catalynes-enrichment) and wants personalized LinkedIn outreach drafted for each lead. Triggers on phrases like "write DMs for these leads," "draft LinkedIn outreach," "write the connection requests," "personalized DMs," or when the user references the enriched CSV and asks for outreach copy. Produces TWO versions per lead — a 75-word in-conversation DM and a ≤300-character connection-request DM — orchestrated across 10 parallel sub-agents following Catalyne's 5-step writing sequence and 4 hard rules.
---

# Catalyne's LinkedIn DM Skill

This skill takes a CSV of qualified+enriched leads and produces, per lead, **both** of the following:

- **v2 — In-conversation DM**: 60–80 words, used after a connection request is accepted.
- **v3 — Connection request DM**: ≤300 characters (LinkedIn's hard limit on connection-request notes).

Both versions reference the same trigger and use the same rapport bridge — v3 is the compressed form of v2. Always output both.

## The 5-step writing sequence (per lead)

The sub-agent applies these steps in order. Skipping or re-ordering reliably produces "bolted-on" rapport that reads transactional.

1. **trigger-event-detection** — pick the single strongest "why now" from the lead's enrichment data. Ranking: raised since 2026 > active fundraising > program attendance > recent post (last 30 days) > hiring sales > older post > job change. Cite the trigger source URL when available.
2. **building-rapport** (planning, before writing) — decide the rapport bridge. What genuine observation links the writer to the lead's actual work? Always tie to a specific post, milestone, or business event — never to a job title.
3. **social-selling** (planning, before writing) — set peer-to-peer frame. Plan a 1-line peer insight or pattern observation. Not a pitch.
4. **copywriting** — write the v2 in-conversation DM (60–80 words, target 70).
5. **copy-editing** — tighten: cut hedges, verify trigger is front-and-center, check CTA is low-friction. Then compress to v3 (≤300 chars).

Detailed rules in [references/dm-rules.md](references/dm-rules.md). Scoring rubric for QA in [references/dm-rubric.md](references/dm-rubric.md). Sub-agent brief in [AGENT.md](AGENT.md).

## The 4 hard rules (every DM must comply)

1. **WIIFM mandatory.** Every DM includes an explicit 5–10 word reciprocity offer signaling what the recipient gets from replying ("Happy to share what we're seeing in X" / "Glad to swap notes on Y").
2. **No snark, no jabs.** First-DM tone test: would a stranger feel laughed-at or laughed-with? If unclear, rewrite.
3. **Language rule.** If the lead's last 2 posts are **both** in German → write the DM in German. All other cases (English-only, mixed, Dutch, French, Portuguese, Slovenian, Japanese, etc.) → write the DM in English. Rationale: the operator speaks DE/EN/JP; Japanese founders deliberately receive English to test their internationalization readiness.
4. **Always output both versions.** v2 (60–80 words) and v3 (≤300 chars). Draft v2 first to force full thinking, then compress to v3.

## Orchestration workflow

### Step 1 — Build per-lead consolidated input

Read the enriched CSV. Pull qualified leads only. For each lead, build a consolidated record combining the enrichment fields (LinkedIn posts, confirmed company, etc.) with the qualification trigger signals (fundraising, hiring, program, etc.). Without both, the sub-agent can't pick the strongest trigger.

### Step 2 — Split into 10 batches

Distribute the qualified leads across 10 batches (typically 5–6 per batch). Write each batch as `dm_batch_N.json`.

### Step 3 — Dispatch 10 parallel sub-agents

**Single message containing 10 `Agent` tool calls.** Each sub-agent gets the prompt from [AGENT.md](AGENT.md). Substitute the batch number into the input path.

Use `subagent_type: "general-purpose"`.

### Step 4 — Merge and validate

Each sub-agent writes `dm_batch_N_results.json` with both versions per lead. Before merging, programmatically verify:

- All `dm_v3_char_count` values ≤ 300 (HARD)
- All `dm_v2_word_count` values in 60–80 range
- Re-count from the actual string in Python (don't trust the sub-agent's self-reported count alone)

```python
v3_violations = [(r['row_number'], len(r['dm_v3_connection_request'])) for r in all_dms if len(r['dm_v3_connection_request']) > 300]
v2_violations = [(r['row_number'], len(r['dm_v2_long'].split())) for r in all_dms if not (60 <= len(r['dm_v2_long'].split()) <= 80)]
```

If any violations exist, re-dispatch that batch's sub-agent with the specific failing leads called out.

Append these columns to the enriched CSV:

- `DM Language`
- `Primary Trigger`
- `Trigger Source URL`
- `DM v2 (75-word in-conversation)`
- `DM v2 Word Count`
- `DM v3 (connection request, ≤300 chars)`
- `DM v3 Char Count`

### Step 5 — Report

Output a short summary with:

- Validation results (0 violations expected)
- Language distribution
- v2/v3 length distribution (min, max, mean)
- Any flagged weak-trigger leads
- Path to the output CSV as a `computer://` link

## Output format

A single CSV in the outputs folder, named `<input-filename> + DMs.csv`, containing the input columns plus the 7 new DM columns.

## Operational note

If the sub-agent produces a v3 over 300 chars, the canonical fix is to *tighten WIIFM specificity and switch the question to a binary*. If a DM can't survive compression and still hit ≥45 on the rubric, the trigger probably wasn't strong enough to justify outreach in the first place.
