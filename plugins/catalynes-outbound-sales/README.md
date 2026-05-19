# Catalyne's Outbound Sales Plugin

End-to-end outbound sales workflow for Catalyne: qualify a CSV of leads against the ICP (European B2B founders and sales executives), enrich the qualified subset with LinkedIn data via Apify, and generate two versions of a personalized LinkedIn DM per lead.

## What's in this plugin

| Component | Type | Purpose |
|---|---|---|
| `catalyne-outbound` | Command | Slash command that chains all three skills end-to-end |
| `catalynes-lead-qualification` | Skill | Qualifies leads against the Catalyne ICP. 10 parallel sub-agents per run. |
| `catalynes-enrichment` | Skill | Pulls last 2 LinkedIn posts + confirmed current company via Apify. 10 parallel sub-agents per run. |
| `catalynes-linkedin-dms` | Skill | Writes both DM versions (75-word in-conversation + ≤300-char connection request). 10 parallel sub-agents per run. |

Every skill that dispatches sub-agents has its own `AGENT.md` inside the skill directory specifying exactly what the sub-agent does. The orchestrator skill loads `AGENT.md` and passes it as the sub-agent prompt.

## Quick start

```
/catalyne-outbound
```

Then attach (or specify the path to) a CSV of leads. The command runs the full workflow and delivers a final CSV with qualification status, enrichment data, and both DM versions per lead.

## Individual skills

Each skill can also be invoked on its own:

- "Qualify these leads against my ICP" → triggers `catalynes-lead-qualification`
- "Enrich the qualified leads with LinkedIn posts" → triggers `catalynes-enrichment`
- "Write DMs for the enriched leads" → triggers `catalynes-linkedin-dms`

## ICP encoded in this plugin

- **Founders OR sales executives**
- Based in **Europe**
- Actively involved in **B2B sales**

Qualifying titles: Founder, Co-Founder, CEO, COO, CSO, CTO *(only when founder)*, Gründer, Mitgründer, Fondateur, Chief Sales Officer, Head of Sales, Business Developer, Account Executive, Head of BD, CCO, CGO, Head of Growth, VP Sales, Director of Sales.

## DM hard rules (encoded in `catalynes-linkedin-dms`)

1. **WIIFM mandatory** — explicit 5–10 word reciprocity offer per DM
2. **No snark, no jabs** — would a stranger feel laughed-at? rewrite
3. **Language rule** — German DM only if BOTH last 2 posts are in German; all other cases (English-only, mixed, Dutch, French, Portuguese, Slovenian, Japanese, etc.) → English DM
4. **Always output both versions** — v2 (60–80 words, target 70) and v3 (≤300 chars, hard limit)

Full reference: [`skills/catalynes-linkedin-dms/references/dm-rules.md`](skills/catalynes-linkedin-dms/references/dm-rules.md).

## Quality rubric (used by the DM skill)

10 criteria scored 1–5 each (max 50). Send threshold = 45.

1. Trigger strength • 2. Trigger urgency • 3. Length • 4. Personalization specificity • 5. Peer-to-peer tone • 6. Earned rapport bridge • 7. Social-selling integration • 8. CTA friction • 9. WIIFM clarity • 10. No red flags

Calibrated to 2026 LinkedIn outreach benchmarks. Sources in [`skills/catalynes-linkedin-dms/references/dm-rubric.md`](skills/catalynes-linkedin-dms/references/dm-rubric.md).

## Dependencies

- **Apify MCP server** must be connected for the enrichment skill. The skill uses two actors:
  - `harvestapi/linkedin-profile-posts` — last 2 posts per profile
  - `harvestapi/linkedin-profile-scraper` — current company, title, description
- **WebSearch tool** is required for the qualification skill (sub-agents do web research per lead).

## Author

Catalyne (Ben Kimura-Gross) — ben@thecatalyne.com
