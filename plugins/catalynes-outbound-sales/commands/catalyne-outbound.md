---
description: Run Catalyne's full outbound sales workflow on a CSV of leads — qualify, enrich, and write personalized LinkedIn DMs in one shot.
argument-hint: "[path to leads CSV, or attach a CSV file]"
---

# /catalyne-outbound

Run Catalyne's end-to-end outbound sales workflow. Chains the three Catalyne skills sequentially to deliver a fully enriched CSV with personalized LinkedIn DMs for every qualified lead.

## What this command does

1. Asks the user for a CSV of leads (or accepts the path as an argument / attached file).
2. Runs **catalynes-lead-qualification** — qualifies every lead against Catalyne's ICP and identifies trigger signals (fundraising, hiring, program attendance, etc.). 10 sub-agents in parallel.
3. Runs **catalynes-enrichment** — for the qualified subset, pulls last 2 LinkedIn posts + confirmed current company/title via Apify. 10 sub-agents in parallel.
4. Runs **catalynes-linkedin-dms** — for every qualified+enriched lead, writes both DM versions (75-word in-conversation + ≤300-char connection request). 10 sub-agents in parallel.
5. Delivers a single final CSV with all original columns plus qualification, enrichment, and DM columns.

## Workflow instructions for Claude

Execute these steps in order. Do not skip steps. Each step's output is the next step's input.

### Step 0 — Get the CSV

If `$ARGUMENTS` contains a path → use it.

Otherwise, check the uploads folder (`/Users/ben-k-g/Library/Application Support/Claude/local-agent-mode-sessions/babcff20-1735-4859-bc58-88223a560dbe/8736fbd6-ebdb-4b3e-9216-5fea40d7af0f/local_85145ae7-ea79-4bc5-b04e-f10d06eabd9c/uploads`) for a recent CSV the user attached.

If neither is present, ask the user (using AskUserQuestion) to upload a CSV of leads. Required columns: at minimum `First Name`, `Last Name`, `Linkedin URL Public`, `Company Name`, `Current Job`, `Location`. The richer the CSV (LinkedIn industry, profile headline, company description, etc.) the better.

### Step 1 — Pre-flight checks

Before any work:

- Verify the **Apify MCP server** is connected (needed for step 3). If not, ask the user to connect it before continuing. Without Apify, the enrichment step can't run.
- Confirm CSV size with the user if >300 rows — the full workflow uses ~30 parallel sub-agents and may take 15-30 min for large CSVs.

### Step 2 — Run lead qualification

Invoke the **catalynes-lead-qualification** skill. Pass the CSV path. The skill orchestrates 10 parallel sub-agents and produces `<filename> - QUALIFIED.csv`.

After it finishes, report back to the user with the qualified/disqualified/unclear breakdown before proceeding to step 3.

### Step 3 — Run enrichment

Invoke the **catalynes-enrichment** skill. Pass the QUALIFIED CSV path. The skill orchestrates 10 parallel sub-agents (Apify calls) and produces `<filename> + ENRICHED.csv`.

After it finishes, report the enrichment fill rate per column before proceeding to step 4.

### Step 4 — Write LinkedIn DMs

Invoke the **catalynes-linkedin-dms** skill. Pass the ENRICHED CSV path. The skill orchestrates 10 parallel sub-agents and produces `<filename> + DMs.csv` containing both v2 (75-word in-conversation) and v3 (≤300-char connection request) per qualified lead.

The DM skill applies its 4 hard rules:

1. WIIFM mandatory
2. No snark, no jabs
3. Language rule (German only if both posts in German; else English)
4. Always output both versions

### Step 5 — Deliver

Output a final summary with:

- Total leads processed
- Qualification breakdown
- Enrichment fill rate
- DM validation results (v3 ≤300 chars compliance, language split)
- A `computer://` link to the final CSV

The final CSV is the working artifact the user loads into Apollo, Salesloft, Outreach, or their LinkedIn sequencer of choice. v3 goes into the LinkedIn connection-request modal; v2 is the first follow-up after the connection is accepted.

## Notes

- **All three skills dispatch 10 sub-agents per batch in parallel.** This is non-negotiable for speed — sequential processing burns the context window and takes 5x as long.
- **If any step fails** (e.g., one sub-agent times out), re-dispatch only that batch with the same prompt. Don't restart the whole workflow.
- **Operator language rule:** Catalyne speaks DE / EN / JP. The DM skill encodes the language rule accordingly — German only if both posts are German, else English.

$ARGUMENTS
