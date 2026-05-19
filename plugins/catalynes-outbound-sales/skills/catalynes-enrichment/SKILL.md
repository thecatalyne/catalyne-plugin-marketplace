---
name: catalynes-enrichment
description: Catalyne's enrichment skill. Use when the user has a CSV of qualified leads (typically the output of the catalynes-lead-qualification skill) and wants to enrich each one with LinkedIn data via Apify — last 2 posts, confirmed current company and title (in an ICP-qualifying role), and the company description from LinkedIn. Triggers on phrases like "enrich these leads," "get their LinkedIn posts," "confirm the company," "Apify enrich," or when the user references the qualified CSV and asks for content suitable for personalized outreach. Orchestrates 10 parallel sub-agents that each call the Apify harvestapi LinkedIn scrapers for a batch.
---

# Catalyne's Enrichment Skill

This skill takes a CSV of qualified leads (output of `catalynes-lead-qualification`), pulls the qualified-only subset, splits them into 10 batches, dispatches one sub-agent per batch in parallel, and merges the LinkedIn enrichment data back into the CSV.

## What gets added per lead

- **Confirmed current company** — verified against an ICP-qualifying title (founder / co-founder / CEO / CSO / COO / CCO / CGO / Head of Sales / Head of Growth / Head of BD / AE / Business Developer / VP Sales / Chief Sales Officer / Gründer / Mitgründer / Fondateur)
- **Confirmed current title** at that company
- **Company description** — from LinkedIn About / position description
- **Last post 1**: text (truncated to ~600 chars), URL, date
- **Last post 2**: text (truncated to ~600 chars), URL, date

These fields are what the downstream `catalynes-linkedin-dms` skill needs to write personalized outreach.

## Required tool

This skill depends on the **Apify MCP server** being connected, specifically the `mcp__Apify__call-actor` and `mcp__Apify__get-actor-output` tools. If they are not available, ask the user to connect the Apify MCP before proceeding. The actors used are:

- `harvestapi/linkedin-profile-posts` (last-2-posts per profile)
- `harvestapi/linkedin-profile-scraper` (current company / title / description)

Both run without LinkedIn cookies.

## Orchestration workflow

### Step 1 — Identify qualified leads

Read the QUALIFIED CSV. Extract rows where `Qualification == "qualified"`. Note the original `row_number` for each so you can merge back.

```python
import csv
with open('PATH_TO_QUALIFIED_CSV', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
qualified = [(i+1, r) for i, r in enumerate(rows) if r.get('Qualification','').lower() == 'qualified']
```

### Step 2 — Split into 10 batches

Distribute the qualified leads across 10 batches as evenly as possible (typically 5–6 per batch). Write each batch as `enrich_batch_N.json` containing per-lead: `row_number`, `full_name`, `linkedin_url`, `current_company_csv`, `current_job_csv`.

### Step 3 — Dispatch 10 parallel sub-agents

**Single message containing 10 `Agent` tool calls.** Sequential dispatch defeats the purpose.

Each sub-agent gets the prompt from [AGENT.md](AGENT.md). Substitute the batch number into the input path.

Use `subagent_type: "general-purpose"` so the sub-agent has access to the Apify MCP tools.

### Step 4 — Merge results

Each sub-agent writes `enrich_batch_N_results.json`. Merge by `row_number` and append these columns to the input CSV:

- `Confirmed Current Company`
- `Confirmed Current Title`
- `Company Description (LinkedIn)`
- `Last Post 1 Text`
- `Last Post 1 URL`
- `Last Post 1 Date`
- `Last Post 2 Text`
- `Last Post 2 URL`
- `Last Post 2 Date`

Write to `<original-filename> + ENRICHED.csv`.

### Step 5 — Report

Output a short summary with:

- Fill rate per new column (X/N filled)
- Notable corrections the LinkedIn data revealed vs. the input CSV (e.g., lead's real current role differs from CSV)
- Path to the output CSV as a `computer://` link

## Efficiency notes

The sub-agents make **2 Apify calls per batch** (not 2 per lead) — one batched call to the posts scraper and one to the profile scraper, each with all 5-6 URLs as input. Both actors accept arrays. This is enforced in AGENT.md.

## Output format

A single CSV in the outputs folder, named `<original-filename> + ENRICHED.csv`, containing the qualified CSV's columns plus the 9 new enrichment columns.
