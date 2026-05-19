---
name: catalynes-lead-qualification
description: Catalyne's lead qualification skill. Use when the user uploads a CSV of leads and wants to qualify them against the Catalyne ICP (European B2B founders and sales executives). Triggers on phrases like "qualify these leads," "check my lead list," "run qualification on this CSV," "qualify against my ICP," or when the user pastes a Linked-In-export-style CSV and asks for an ICP fit assessment. Orchestrates 10 parallel sub-agents that each research a batch of leads via web search, then merges results into an enriched CSV with qualification status and trigger signals.
---

# Catalyne's Lead Qualification Skill

This skill takes a CSV of leads (typically a LinkedIn Sales Navigator or Apollo export), splits it into 10 batches, dispatches one sub-agent per batch in parallel, and merges the results into a final CSV with qualification status and trigger signals.

## The ICP

Catalyne only works with:

- **Founders or sales executives**
- Based in **Europe**
- Actively involved in **B2B sales**

Qualifying titles include (non-exhaustive): Founder, Co-Founder, Cofounder, CEO, COO, CSO, CTO *(only when also a founder)*, Gründer, Mitgründer, Fondateur, Chief Sales Officer, Head of Sales, Business Developer, Account Executive, Head of Business Development, Chief Commercial Officer (CCO), Chief Growth Officer (CGO), Head of Growth, VP Sales, Director of Sales.

**Disqualify** if: not a founder AND not in a sales role; not in Europe; clearly B2C-only with no B2B element; intern; junior analyst; non-sales / non-founder operational role.

## Orchestration workflow

Follow these steps exactly. Do not skip the parallel dispatch — qualifying 100 leads sequentially takes too long and burns the context window.

### Step 1 — Read the CSV

Read the uploaded CSV using Python (it may be too large for the Read tool). Capture the original column order so it can be preserved in the final output.

```bash
python3 -c "
import csv
with open('PATH_TO_CSV', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    leads = list(reader)
print(f'Total leads: {len(leads)}')
print(f'Columns: {list(leads[0].keys())}')
"
```

### Step 2 — Split into 10 batches

Distribute leads as evenly as possible across 10 batches. For 100 leads → 10 batches of 10. For other sizes, use `[ceil(n/10), ..., n - 9*ceil(n/10)]` or another even split.

Write each batch as a JSON file (`batch_1.json` … `batch_10.json`) in the working directory with these per-lead fields: `row_number`, `first_name`, `last_name`, `full_name`, `current_job`, `linkedin_url`, `company_name`, `company_domain`, `company_website`, `company_industry`, `company_description` (truncate to 500 chars), `company_location`, `profile_location`, `profile_headline`, `profile_summary` (truncate to 400 chars), `current_jobs_number`, `years_in_position`, `company_year_founded`, `company_employee_range`.

### Step 3 — Dispatch 10 parallel sub-agents

**This must be a single message containing 10 `Agent` tool calls.** That is the only way they truly run in parallel. Do not dispatch them one-at-a-time in separate turns.

Each sub-agent gets the prompt defined in [AGENT.md](AGENT.md) — load that file and substitute the batch number (1 through 10) into the input path.

Use `subagent_type: "general-purpose"` so the sub-agent has WebSearch and web_fetch tools.

### Step 4 — Merge results

Each sub-agent writes `batch_N_results.json` (10 records). Merge them keyed by `row_number` and append these columns to the original CSV:

- `Multiple companies` (yes/no/unclear)
- `URL source multiple companies`
- `Program attendance` (yes/no/unclear)
- `URL source program attendance`
- `Fundraising activity` (yes/no/unclear)
- `URL source fundraising activity`
- `Raised since start of 2026` (yes/no/unclear)
- `URL source successful raise`
- `Hiring sales staff` (yes/no/unclear)
- `URL source hiring sales staff`
- `Qualification` (qualified/disqualified/unclear)
- `Qualification reason` (one-sentence rationale)

Write the merged file as `<original-filename> - QUALIFIED.csv` in the outputs folder.

### Step 5 — Report

Output a short summary with:

- Total qualified / disqualified / unclear counts
- Top common disqualification reasons
- Counts for each trigger signal (fundraising, hiring, program, raise)
- Path to the output CSV as a `computer://` link

## Hard rules for sub-agents

These are repeated in `AGENT.md` but stated here for the orchestrator's awareness:

- **Real URLs only.** If a fact can't be verified, mark "unclear" and leave the URL blank.
- **Today is the operative date.** "Recent" means the date shown in the env block, not training data.
- **Web research is mandatory.** The CSV's industry/description fields are insufficient — sub-agents must search the actual lead and company.

## Output format

A single CSV in the outputs folder, named `<original-filename> - QUALIFIED.csv`, containing the original columns plus the 12 new qualification columns listed above.
